from nodes import *

try:
    import json
except:
    import simplejson as json

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
    if in_list and ((not isinstance(node,UlliNode)) or ((node.depth+1)<in_list)):
        _r=_bb_out(node,in_list-1)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
            in_list+=1
        return "[/list]\n"+_r,in_list-1
    if isinstance(node,basestring):
        return node
    elif isinstance(node,TitleNode):
        #Yeah, BBCode sucks at titles
        return ("\n[size=%d][b]"%(8-node.depth))+bb_out(node.content)+"[/b][/size]\n"
    elif isinstance(node,ParagraphNode):
        return "\n"+bb_out(node.content)+"\n"
    elif isinstance(node,BlockQuoteNode):
        return "\n[quote]"+bb_out(node.content)+"[/quote]\n"
    elif isinstance(node,CodeBlockNode):
        return "\n[code]"+bb_out(node.content)+"[/code]\n"
    elif isinstance(node,UlliNode):
        r=""
        while (node.depth+1)>in_list:
            r+="\n[list]" if in_list==0 else "[list]"
            in_list+=1
        r+="[*]"+bb_out(node.content)+"\n"
        return r,in_list
    elif isinstance(node,BoldNode):
        return "[b]"+bb_out(node.content)+"[/b]"
    elif isinstance(node,ItalicNode):
        return "[i]"+bb_out(node.content)+"[/i]"
    elif isinstance(node,MonoNode):
        return "[font=\"Monaco, Courier, Liberation Mono, DejaVu Sans Mono, monospace\"]"+bb_out(node.content)+"[/font]"
    elif isinstance(node,HrefNode):
        if node.hreftype=="link":
            return ("[url=%s]"%json.dumps(node.content))+bb_out(node.label)+"[/url]"
        elif node.hreftype=="img":
            label=bb_out(node.label).strip()
            if label:
                return ("[img alt=%s]"%json.dumps(label))+node.content+"[/img]"
            return "[img]"+node.content+"[/img]"
        else:
            #e.g. [media]...[/media], [youtube]...[/youtube], [video]...[/video]
            return "["+node.hreftype+"]"+node.content+"[/media]"
    elif isinstance(node,NewlineNode):
        return "[br]"
    elif isinstance(node,RuleNode):
        return "\n[rule]\n"
    else:
        return "ERROR"+repr(node)