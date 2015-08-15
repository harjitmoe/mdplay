from nodes import *

def bb_out(nodes):
    in_list=0
    r=""
    for node in nodes:
        _r=_bb_out(node,in_list)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
        r+=_r
    return r.strip("\r\n")

def _bb_out(node,in_list):
    if in_list and not isinstance(node,UlliNode):
        return "[/list]\n"+_bb_out(node,False),False
    if isinstance(node,basestring):
        return node
    elif isinstance(node,TitleNode):
        #Yeah, BBCode sucks at titles
        return ("\n[size=%d][b]"%(8-node.depth))+bb_out(node.content)+"[/b][/font]\n"
    elif isinstance(node,ParagraphNode):
        return "\n"+bb_out(node.content)+"\n"
    elif isinstance(node,BlockQuoteNode):
        return "\n[quote]"+bb_out(node.content)+"[/quote]\n"
    elif isinstance(node,CodeBlockNode):
        return "\n[code]"+bb_out(node.content)+"[/code]\n"
    elif isinstance(node,UlliNode):
        r="[*]"+bb_out(node.content)+"\n"
        if not in_list:
            r="\n[list]"+r
        return r,True
    elif isinstance(node,BoldNode):
        return "[b]"+bb_out(node.content)+"[/b]"
    elif isinstance(node,ItalicNode):
        return "[i]"+bb_out(node.content)+"[/i]"
    elif isinstance(node,MonoNode):
        return "[font=\"Monaco, Courier, Liberation Mono, DejaVu Sans Mono, monospace\"]"+bb_out(node.content)+"[/font]"
    elif isinstance(node,HrefNode):
        if node.hreftype=="link":
            return ("[url=%r]"%node.content)+bb_out(node.label)+"[/url]"
        elif node.hreftype=="img":
            return "[img]"+node.content+"[/img]"
        else:
            #e.g. [media]...[/media]
            return "["+node.hreftype+"]"+node.content+"[/media]"
    elif isinstance(node,NewlineNode):
        return "[br]"
    elif isinstance(node,RuleNode):
        return "[rule]"
    else:
        return "ERROR"+repr(node)