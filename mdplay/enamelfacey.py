"""Enamel writer for minidom, derived from the XML writer of minidom.

minidom is part of the Python Standard Library.

Copy of the Python licence incuded as LICENSE-Python.txt

This file is a derivative work by HarJIT, may be used under same terms.

"""

import xml.dom.minidom as _d

from mdplay.nodes import simul_replace

def _write_data(writer, data):
    if data:
        data = simul_replace(data, "[", "[lbrack]", "]", "[rbrack]").replace("<", "[lt]").replace(">", "[gt]")
        writer.write(data)

def writenml(fing, writer, indent="", addindent="", newl=""):
    if isinstance(fing, _d.Element):
        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        if "|" in fing.tagName:
            raise ValueError("pipe in tag name %r" % fing.tagName)
        writer.write(indent+"<" + fing.tagName)

        attrs = fing._get_attributes()
        a_names = attrs.keys()
        a_names.sort()

        for a_name in a_names:
            if "|" in a_name:
                raise ValueError("pipe in attribute name %r" % a_name)
            writer.write("<%s|" % a_name)
            _write_data(writer, attrs[a_name].value)
            writer.write(">")
        if fing.childNodes:
            writer.write("|")
            if (len(fing.childNodes) == 1 and
                    fing.childNodes[0].nodeType == _d.Node.TEXT_NODE):
                writenml(fing.childNodes[0], writer, '', '', '')
            else:
                writer.write(newl)
                for cnode in fing.childNodes:
                    writenml(cnode, writer, indent+addindent, addindent, newl)
                writer.write(indent)
            writer.write(">%s"%(newl))
        else:
            writer.write(">%s"%(newl))
    elif isinstance(fing, _d.Text): #including CDATASection
        _write_data(writer, "%s%s%s" % (indent, fing.data, newl))
    # Unclear what the following are supposed to be rendered as:
    elif isinstance(fing, _d.DocumentType):
        pass
    elif isinstance(fing, _d.ProcessingInstruction):
        writer.write("%s<?%s|%s>%s" % (indent, fing.target, fing.data, newl))
    elif isinstance(fing, _d.Comment):
        writer.write("%s<!--|" % indent)
        _write_data(writer, fing.data)
        writer.write(">%s" % newl)
    elif isinstance(fing, _d.Document):
        for cnode in fing.childNodes:
            writenml(cnode, writer, indent, addindent, newl)
    else:
        raise TypeError

def tonml(fing, encoding="utf-8", indent="", newl=""):
    # indent = the indentation string to prepend, per level
    # newl = the newline string to append
    writer = _d._get_StringIO()
    if encoding is not None:
        import codecs
        # Can't use codecs.getwriter to preserve 2.0 compatibility
        writer = codecs.lookup("utf-8")[3](writer)
    writenml(fing, writer, "", indent, newl)
    return writer.getvalue()
