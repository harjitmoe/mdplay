"""HTML writer for the DOM, derived from the XML writer of minidom.

Modes:

html: Well-formed plain HTML syntax.

xhtml: XHTML syntax which should work with most plain HTML parsers.

xml: XHTML but not suited for general interchange (reliant upon
being parsed as XML syntax).

nml: Naggum syntax, illustrative, not used in general interchange.

"""

__copying__ = """
minidom is part of the Python Standard Library.

Copy of the Python licence incuded as LICENSE-Python.txt

This file is a derivative work by HarJIT, may be used under same terms.
"""

import xml.dom.minidom

# Empty elements from HTML5 and HTML4-Transitional, called "void elements" in HTML5.
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

# Elements that are CDATA in HTML (not XHTML), HTML5's "raw text elements".
ALL_HTML_CDATA_ELEMENTS = ("script", "style")

# Elements that are PCDATA in HTML, HTML5's "escapable raw text elements".
ALL_HTML_PCDATA_ELEMENTS = ("textarea", "title")

def _simul_replace(a, b, c, d, e):
    """Simultaneously replace (b with c) and (d with e) in a, returning the result."""
    r = []
    for f in a.split(b):
        r.append(f.replace(d, e))
    return c.join(r)

def _write_data(writer, data, mode="xml"):
    if data:
        data = str(data) # not str(data)
        if mode == "xml": # i.e. not xhtml or html
            data = data.replace("&", "&amp;").replace("<", "&lt;"). \
                        replace("\"", "&quot;").replace(">", "&gt;"). \
                        replace("'", "&apos;")
        elif mode != "nml":
            data = data.replace("&", "&amp;").replace("<", "&lt;"). \
                        replace("\"", "&quot;").replace(">", "&gt;")
        else:
            data = _simul_replace(data, "[", "[lbrack]", "]", "[rbrack]"). \
                         replace("<", "[lt]").replace(">", "[gt]")
        writer.write(data)

def writehtml(node, writer, indent="", addindent="", newl="", encoding=None, mode="xhtml", 
              parenttag=None, dommodule=xml.dom.minidom):
    # indent = current indentation
    # addindent = indentation to add to higher levels
    # newl = newline string
    is_implied_cdata = parenttag in ALL_HTML_CDATA_ELEMENTS
    is_pcdata = parenttag in ALL_HTML_PCDATA_ELEMENTS
    _d = dommodule
    if isinstance(node, _d.Text):
        if (mode == "html") and is_implied_cdata:
            if "</" in node.data: # HTML5 is a bit more lenient here but whatever...
                raise ValueError("'</' is not allowed in a %s element" % parenttag)
            writer.write(node.data)
        elif (mode == "xhtml") and is_implied_cdata:
            # The needful polygloty here is difficult...
            if "</" in node.data:
                raise ValueError("'</' is not allowed in a %s element" % parenttag)
            elif "]]>" in node.data:
                raise ValueError("']]>' is not allowed in a %s element" % parenttag)
            # Both CSS and JS support /* */ comments thank goodness...
            writer.write("/* <![CDATA[ */\n" + node.data + "\n/* ]]> */")
        elif (mode == "xml") and isinstance(node, _d.CDATASection) \
                and ("]]>" not in node.data):
            writer.write("<![CDATA[%s]]>" % node.data)
        else:
            _write_data(writer, "%s%s%s" % (indent, node.data, newl), mode)
    elif (is_implied_cdata or is_pcdata) and (mode in ("html", "xhtml")):
        raise ValueError("%s nodes are not allowed in a %s element"
            % (node.__class__.__name__, parenttag))
    elif isinstance(node, _d.Element):
        if is_pcdata or is_implied_cdata:
            raise ValueError
        if (mode == "nml") and ("|" in node.tagName):
            raise ValueError("pipe in tag name %r" % node.tagName)
        writer.write(indent+"<" + node.tagName)
        attrs = node.attributes
        if hasattr(attrs, "keys"): # minidom (implementing dict interface)
            a_names = list(attrs.keys())
        else: # standard (allowing numerical indices, which minidom doesn't)
            a_names = [attrs[i].name for i in range(attrs.length)]
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
                writehtml(node.childNodes[0], writer, '', '', '', mode=mode, parenttag=node.tagName)
            else:
                writer.write(newl)
                for cnode in node.childNodes:
                    writehtml(cnode, writer, indent+addindent, addindent, newl, mode=mode, parenttag=node.tagName)
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
    # Undefined what (if anything) the following are supposed to be rendered as in NML:
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
            pass # TODO surely there must be some way of doing this???
    #
    elif isinstance(node, _d.Document):
        if mode == "xml":
            if encoding is None:
                writer.write('<?xml version="1.0" ?>'+newl)
            else:
                writer.write('<?xml version="1.0" encoding="%s"?>%s' % (encoding, newl))
        for cnode in node.childNodes:
            writehtml(cnode, writer, indent, addindent, newl, mode=mode)
    else:
        raise TypeError("%r is not a DOM node" % node)

def tohtml(node, encoding="utf-8", indent="", newl="", mode="xhtml", 
           dommodule=xml.dom.minidom):
    # indent = the indentation string to prepend, per level
    # newl = the newline string to append
    import io
    if encoding is None:
        writer = io.StringIO()
    else:
        writer = io.TextIOWrapper(io.BytesIO(),
                                  encoding=encoding,
                                  errors="xmlcharrefreplace",
                                  newline='\n')
    writehtml(node, writer, "", indent, newl, encoding=encoding, mode=mode,
              dommodule=dommodule)
    if encoding is None:
        return writer.getvalue()
    else:
        return writer.detach().getvalue()

