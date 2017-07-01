"""HTML writer for minidom, derived from the XML writer of minidom."""

__copying__ = """
minidom is part of the Python Standard Library.

Copy of the Python licence incuded as LICENSE-Python.txt

This file is a derivative work by Thomas Hori, may be used under same terms.
"""

import xml.dom.minidom as _d

ALL_HTML_EMPTY_ELEMENTS = """\
area
base
basefont
br
col
embed
frame
hr
img
input
isindex
keygen
link
meta
param
source
track
wbr""".split()

def _simul_replace(a, b, c, d, e):
    """Simultaneously replace (b with c) and (d with e) in a, returning the result."""
    r = []
    for f in a.split(b):
        r.append(f.replace(d, e))
    return c.join(r)

def _write_data(writer, data, mode):
    if data:
        if mode != "nml":
            data = data.replace("&", "&amp;").replace("<", "&lt;"). \
                        replace("\"", "&quot;").replace(">", "&gt;")
        else:
            data = _simul_replace(data, "[", "[lbrack]", "]", "[rbrack]"). \
                         replace("<", "[lt]").replace(">", "[gt]")
        writer.write(data)

def writehtml(node, writer, indent="", addindent="", newl="", encoding=None, mode="xhtml"):
    if isinstance(node, _d.Element):
        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        if (mode == "nml") and ("|" in node.tagName):
            raise ValueError("pipe in tag name %r" % node.tagName)
        writer.write(indent+"<" + node.tagName)

        attrs = node._get_attributes()
        a_names = attrs.keys()
        a_names.sort()

        for a_name in a_names:
            if mode != "nml":
                writer.write(" %s=\"" % a_name)
                _write_data(writer, attrs[a_name].value, mode)
                writer.write("\"")
            else:
                if "|" in a_name:
                    raise ValueError("pipe in attribute name %r" % a_name)
                writer.write("<%s|" % a_name)
                _write_data(writer, attrs[a_name].value, mode)
                writer.write(">")
        if node.childNodes:
            writer.write(">" if mode != "nml" else "|")
            if (len(node.childNodes) == 1 and
                    node.childNodes[0].nodeType == _d.Node.TEXT_NODE):
                writehtml(node.childNodes[0], writer, '', '', '', mode = mode)
            else:
                writer.write(newl)
                for cnode in node.childNodes:
                    writehtml(cnode, writer, indent+addindent, addindent, newl, mode = mode)
                writer.write(indent)
            if mode != "nml":
                writer.write("</%s>%s" % (node.tagName, newl))
            else:
                writer.write(">%s" % (newl))
        else:
            # Now, *this* is where the different modes really start to show...
            empty_type = node.tagName.lower().strip() in ALL_HTML_EMPTY_ELEMENTS
            if mode == "nml":
                writer.write(">%s" % (newl))
            elif mode == "xml":
                writer.write("/>%s" % (newl))
            elif mode == "xhtml":
                if empty_type:
                    writer.write("/>%s" % (newl))
                else:
                    writer.write("></%s>%s" % (node.tagName, newl))
            else: # mode == "html"
                if empty_type:
                    writer.write(">%s" % (newl))
                else:
                    writer.write("></%s>%s" % (node.tagName, newl))
    elif isinstance(node, _d.Text):
        if (mode == "xml") and isinstance(node, _d.CDATASection) \
                and (node.data.find("]]>") < 0):
            writer.write("<![CDATA[%s]]>" % node.data)
        else:
            _write_data(writer, "%s%s%s" % (indent, node.data, newl), mode)
    # Unclear what the following are supposed to be rendered as in NML:
    elif isinstance(node, _d.DocumentType):
        if mode != "nml":
            writer.write("<!DOCTYPE ")
            writer.write(node.name)
            if node.publicId and node.systemId:
                writer.write(" PUBLIC '%s' '%s'" % (node.publicId, node.systemId))
            elif node.publicId:
                writer.write(" PUBLIC '%s'" % (node.publicId))
            elif node.systemId:
                writer.write(" SYSTEM '%s'" % (node.systemId))
            if node.internalSubset is not None:
                writer.write(" [")
                writer.write(node.internalSubset)
                writer.write("]")
            writer.write(">"+newl)
        else:
            pass
    elif isinstance(node, _d.ProcessingInstruction):
        if mode == "xml":
            writer.write("%s<?%s %s?>%s" % (indent, node.target, node.data, newl))
        else:
            pass
    elif isinstance(node, _d.Comment):
        if mode != "nml":
            if "--" in node.data:
                raise ValueError("'--' is not allowed in a comment node")
            writer.write("%s<!--%s-->%s" % (indent, node.data, newl))
        else:
            pass
    #
    elif isinstance(node, _d.Document):
        if mode == "xml":
            if encoding is None:
                writer.write('<?xml version="1.0" ?>'+newl)
            else:
                writer.write('<?xml version="1.0" encoding="%s"?>%s' % (encoding, newl))
        for cnode in node.childNodes:
            writehtml(cnode, writer, indent, addindent, newl, mode = mode)
    else:
        raise TypeError

def tohtml(node, encoding="utf-8", indent="", newl="", mode="xhtml"):
    # indent = the indentation string to prepend, per level
    # newl = the newline string to append
    writer = _d._get_StringIO()
    if encoding is not None:
        import codecs
        # Can't use codecs.getwriter to preserve 2.0 compatibility
        writer = codecs.lookup("utf-8")[3](writer)
    writehtml(node, writer, "", indent, newl, encoding = encoding, mode = mode)
    return writer.getvalue()
