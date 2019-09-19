"""HTML writer for the DOM, derived from the XML writer of minidom.

Modes:

html: Well-formed plain HTML syntax.

xhtml: XHTML syntax which should work with most plain HTML parsers.

xml: XHTML but not suited for general interchange (reliant upon
being parsed as XML syntax).

nml: Naggum syntax, illustrative, not used in general interchange.

jsx: JSX/E4X syntax, in the JSX de-sugared form, i.e. parsable as
ECMAScript syntax.

"""

__copying__ = """
minidom is part of the Python Standard Library.

Copy of the Python licence incuded as LICENSE-Python.txt

This file is a derivative work by HarJIT, may be used under same terms.
"""

import xml.dom.minidom, json

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

JAVASCRIPT_WORD_CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyz$_"

JAVASCRIPT_KEYWORDS = """await break case catch class const continue debugger default 
delete do else export extends finally for function if import in instanceof new return 
super switch this throw try typeof var void while with yield enum

let static implements package protected interface private public""".split()

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
            # [ and ] are used for entities. < and > are used for nodes.
            # I'm using the # for comments (see below).
            data = _simul_replace(data, "[", "[lbrack]", "]", "[rbrack]"). \
                         replace("<", "[lt]").replace(">", "[gt]").replace("#", "[num]")
        writer.write(data)

_valid_js_idf = (lambda s: ((s[0] not in "0123456789") and 
                            not s.casefold().strip(JAVASCRIPT_WORD_CHARACTERS) and
                            s not in JAVASCRIPT_KEYWORDS))

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
        elif (mode == "jsx"):
            writer.write("%s%s" % (indent, json.dumps(node.data)))
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
        if (mode == "jsx") and not _valid_js_idf(node.tagName):
            raise ValueError("tag name %r is not a valid JS identifier" % node.tagName)
        if mode != "jsx":
            writer.write(indent + "<" + node.tagName)
        else:
            writer.write(indent + node.tagName + "({")
        attrs = node.attributes
        if hasattr(attrs, "keys"): # nonstandard minidom interface (implementing dict interface)
            a_names = list(attrs.keys())
        else: # DOM standard interface (allowing numerical indices, which minidom doesn't)
            a_names = [attrs[i].name for i in range(attrs.length)]
        a_names.sort()
        firstloop = True
        for a_name in a_names:
            if mode == "nml":
                if "|" in a_name:
                    raise ValueError("pipe in attribute name %r" % a_name)
                writer.write("<%s|" % a_name)
                _write_data(writer, attrs[a_name].value, mode)
                writer.write(">")
            elif mode == "jsx":
                if firstloop:
                    firstloop = False
                else:
                    writer.write(", ")
                if _valid_js_idf(a_name):
                    writer.write(a_name)
                else:
                    writer.write(json.dumps(a_name))
                writer.write(": ")
                writer.write(json.dumps(attrs[a_name].value))
            else:
                writer.write(" %s=\"" % a_name)
                _write_data(writer, attrs[a_name].value, mode)
                writer.write("\"")
        if node.childNodes:
            if mode == "nml":
                writer.write("|")
            elif mode == "jsx":
                writer.write("}")
            else:
                writer.write(">")
            if (len(node.childNodes) == 1 and
                    node.childNodes[0].nodeType == _d.Node.TEXT_NODE):
                if mode == "jsx":
                    writer.write(", ")
                writehtml(node.childNodes[0], writer, '', '', '', mode=mode, parenttag=node.tagName)
            else:
                if mode != "jsx": # Where newline will be added as part of comma management
                    writer.write(newl)
                for cnode in node.childNodes:
                    if mode == "jsx":
                        if not isinstance(cnode, (_d.DocumentType, _d.Comment,
                                                  _d.ProcessingInstruction)):
                            writer.write(",%s" % (newl or " "))
                        elif isinstance(cnode, _d.Comment):
                            writer.write(newl)
                    writehtml(cnode, writer, indent+addindent, addindent, newl, mode=mode, parenttag=node.tagName)
                if mode == "jsx":
                    writer.write(newl)
                writer.write(indent)
            if mode == "nml":
                writer.write(">%s" % (newl))
            elif mode == "jsx":
                writer.write(")")
            else:
                writer.write("</%s>%s" % (node.tagName, newl))
        else:
            # Now, *this* is where the different modes really start to show...
            empty_type = node.tagName.lower().strip() in ALL_HTML_EMPTY_ELEMENTS
            if mode == "nml":
                writer.write(">%s" % (newl))
            elif mode == "xml":
                writer.write("/>%s" % (newl))
            elif mode == "jsx":
                writer.write("})")
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
    elif isinstance(node, _d.DocumentType):
        # Undefined what (if anything) this is supposed to be rendered as in NML.
        # I'm not sure if doctypes were ever processed by JSX, but suspect not.
        if mode not in ("nml", "jsx"):
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
        # Really makes basically no sense outside of XML.
        if mode == "xml":
            writer.write("%s<?%s %s?>%s" % (indent, node.target, node.data, newl))
        else:
            pass
    elif isinstance(node, _d.Comment):
        if mode == "nml":
            # FIXME: this is not part of the orthodox NML in that it isn't mentioned
            # in the (admittedly informal) defining message. Rather, that does not
            # mention comment syntax. I'm borrowing this one from Common Lisp.
            if "|#" in node.data:
                raise ValueError("'|#' is not allowed in an NML comment node")
            writer.write("%s#||%s||#%s" % (indent, node.data, newl))
        elif mode == "jsx":
            if "*/" in node.data:
                raise ValueError("'*/' is not allowed in a JS comment node")
            writer.write("%s/*%s*/" % (indent, node.data))
        else:
            if "--" in node.data:
                raise ValueError("'--' is not allowed in a comment node")
            writer.write("%s<!--%s-->%s" % (indent, node.data, newl))
    #
    elif isinstance(node, _d.Document):
        if mode == "xml":
            if encoding is None:
                writer.write('<?xml version="1.0" ?>'+newl)
            else:
                writer.write('<?xml version="1.0" encoding="%s"?>%s' % (encoding, newl))
        firstloop = True
        for cnode in node.childNodes:
            if mode == "jsx":
                if not isinstance(cnode, (_d.DocumentType, _d.Comment,
                                          _d.ProcessingInstruction)):
                    if firstloop:
                        firstloop = False
                    else:
                        writer.write(",%s" % (newl or " "))
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
    writehtml(node, writer, indent="", addindent=indent, newl=newl,
              encoding=encoding, mode=mode, dommodule=dommodule)
    if encoding is None:
        return writer.getvalue()
    else:
        return writer.detach().getvalue()

