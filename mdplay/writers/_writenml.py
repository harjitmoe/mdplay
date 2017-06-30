"""Enamel writer for minidom, derived from the XML writer of minidom.

minidom is part of the Python Standard Library.

Copy of the Python licence incuded as LICENSE-Python.txt

This file is a derivative work by Thomas Hori, may be used under same terms.

"""

import xml.dom.minidom as _d

def simul_replace(a, b, c, d, e):
    """Simultaneously replace (b with c) and (d with e) in a, returning the result."""
    r = []
    for f in a.split(b):
        r.append(f.replace(d, e))
    return c.join(r)

def _write_data(writer, data):
    if data:
        data = simul_replace(data, "[", "[lbrack]", "]", "[rbrack]").replace("<", "[lt]").replace(">", "[gt]")
        writer.write(data)

def writenml(node, writer, indent="", addindent="", newl=""):
    if isinstance(node, _d.Element):
        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        if "|" in node.tagName:
            raise ValueError("pipe in tag name %r" % node.tagName)
        writer.write(indent+"<" + node.tagName)

        attrs = node._get_attributes()
        a_names = attrs.keys()
        a_names.sort()

        for a_name in a_names:
            if "|" in a_name:
                raise ValueError("pipe in attribute name %r" % a_name)
            writer.write("<%s|" % a_name)
            _write_data(writer, attrs[a_name].value)
            writer.write(">")
        if node.childNodes:
            writer.write("|")
            if (len(node.childNodes) == 1 and
                    node.childNodes[0].nodeType == _d.Node.TEXT_NODE):
                writenml(node.childNodes[0], writer, '', '', '')
            else:
                writer.write(newl)
                for cnode in node.childNodes:
                    writenml(cnode, writer, indent+addindent, addindent, newl)
                writer.write(indent)
            writer.write(">%s"%(newl))
        else:
            writer.write(">%s"%(newl))
    elif isinstance(node, _d.Text): #including CDATASection
        _write_data(writer, "%s%s%s" % (indent, node.data, newl))
    # Unclear what the following are supposed to be rendered as:
    elif isinstance(node, _d.DocumentType):
        pass
    elif isinstance(node, _d.ProcessingInstruction):
        writer.write("%s<?%s|%s>%s" % (indent, node.target, node.data, newl))
    elif isinstance(node, _d.Comment):
        writer.write("%s<!--|" % indent)
        _write_data(writer, node.data)
        writer.write(">%s" % newl)
    elif isinstance(node, _d.Document):
        for cnode in node.childNodes:
            writenml(cnode, writer, indent, addindent, newl)
    else:
        raise TypeError

def tonml(node, encoding="utf-8", indent="", newl=""):
    # indent = the indentation string to prepend, per level
    # newl = the newline string to append
    writer = _d._get_StringIO()
    if encoding is not None:
        import codecs
        # Can't use codecs.getwriter to preserve 2.0 compatibility
        writer = codecs.lookup("utf-8")[3](writer)
    writenml(node, writer, "", indent, newl)
    return writer.getvalue()
