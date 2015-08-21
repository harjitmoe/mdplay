import re
try:
    import json
except:
    import simplejson as json

import nodes

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
    if in_list and ((not isinstance(node,nodes.UlliNode)) or ((node.depth+1)<in_list)):
        _r=_bb_out(node,in_list-1)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
            in_list+=1
        return "[/list]\n"+_r,in_list-1
    if not isinstance(node,nodes.Node): #i.e. is a string
        return node
    elif isinstance(node,nodes.TitleNode):
        if node.depth>6: node.depth=6
        #Yeah, BBCode sucks at titles
        return ("\n[size=%d][b]"%(8-node.depth))+bb_out(node.content)+"[/b][/size]\n"
    elif isinstance(node,nodes.ParagraphNode):
        return "\n"+bb_out(node.content)+"\n"
    elif isinstance(node,nodes.BlockQuoteNode):
        return "\n[quote]"+bb_out(node.content)+"[/quote]\n"
    elif isinstance(node,nodes.SpoilerNode):
        return "\n[spoiler]"+bb_out(node.content)+"[/spoiler]\n"
    elif isinstance(node,nodes.CodeBlockNode):
        return "\n[code]"+bb_out(node.content)+"[/code]\n"
    elif isinstance(node,nodes.UlliNode):
        r=""
        while (node.depth+1)>in_list:
            r+="\n[list]" if in_list==0 else "[list]"
            in_list+=1
        r+="[*]"+bb_out(node.content)+"\n"
        return r,in_list
    elif isinstance(node,nodes.BoldNode):
        return "[b]"+bb_out(node.content)+"[/b]"
    elif isinstance(node,nodes.ItalicNode):
        return "[i]"+bb_out(node.content)+"[/i]"
    elif isinstance(node,nodes.SuperNode):
        return "[sup]"+bb_out(node.content)+"[/sup]"
    elif isinstance(node,nodes.SubscrNode):
        return "[sub]"+bb_out(node.content)+"[/sub]"
    elif isinstance(node,nodes.HrefNode):
        label=bb_out(node.label)
        ht=node.hreftype
        content=node.content
        if ht=="url":
            if re.match("https?://(www\.)?tvtropes.org",content):
                return "[u]"+label+("[/u][sup][url=%s](TVTropes)[/url][/sup]"%json.dumps(content))
            return ("[url=%s]"%json.dumps(content))+label+"[/url]"
        else: #Including img
            label=label.strip()
            if label:
                return ("[%s alt=%s]"%(ht,json.dumps(label)))+content+"[/"+ht+"]"
            return "["+ht+"]"+content+"[/"+ht+"]"
    elif isinstance(node,nodes.NewlineNode):
        return "[br]"
    elif isinstance(node,nodes.RuleNode):
        return "\n[rule]\n"
    else:
        return "ERROR"+repr(node)
