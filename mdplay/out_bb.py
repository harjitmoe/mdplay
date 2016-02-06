import re
try:
    import json
except:
    import simplejson as json

from mdplay import nodes

def bb_out(nodes,titl_ignored=None,flags=()):
    return bb_out_body(nodes,flags=flags)

def bb_out_body(nodes,flags=()):
    in_list=0
    r=""
    for node in nodes:
        _r=_bb_out(node,in_list,flags=flags)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
        r+=_r
    return r.strip("\r\n")

def _bb_out(node,in_list,flags):
    if in_list and ((not isinstance(node,nodes.UlliNode)) or ((node.depth+1)<in_list)):
        _r=_bb_out(node,in_list-1,flags=flags)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
            in_list+=1
        return "[/list]\n"+_r,in_list-1
    if not isinstance(node,nodes.Node): #i.e. is a string
        return node
    elif isinstance(node,nodes.TitleNode):
        if node.depth>6: node.depth=6
        #Yeah, BBCode sucks at titles
        return ("\n[size=%d][b]"%(8-node.depth))+bb_out_body(node.content,flags=flags)+"[/b][/size]\n"
    elif isinstance(node,nodes.ParagraphNode):
        return "\n"+bb_out_body(node.content,flags=flags)+"\n"
    elif isinstance(node,nodes.BlockQuoteNode):
        return "\n[quote]"+bb_out_body(node.content,flags=flags)+"[/quote]\n"
    elif isinstance(node,nodes.SpoilerNode):
        return "\n[spoiler]"+bb_out_body(node.content,flags=flags)+"[/spoiler]\n"
    elif isinstance(node,nodes.CodeBlockNode):
        return "\n[code]"+bb_out_body(node.content,flags=flags)+"[/code]\n"
    elif isinstance(node,nodes.CodeSpanNode):
        return "[font=monospace]"+bb_out_body(node.content,flags=flags)+"[/font]"
    elif isinstance(node,nodes.UlliNode):
        r=""
        while (node.depth+1)>in_list:
            r+="\n[list]" if in_list==0 else "[list]"
            in_list+=1
        r+="[*]"+bb_out_body(node.content,flags=flags)+"\n"
        return r,in_list
    elif isinstance(node,nodes.BoldNode):
        return "[b]"+bb_out_body(node.content,flags=flags)+"[/b]"
    elif isinstance(node,nodes.ItalicNode):
        return "[i]"+bb_out_body(node.content,flags=flags)+"[/i]"
    elif isinstance(node,nodes.SuperNode):
        return "[sup]"+bb_out_body(node.content,flags=flags)+"[/sup]"
    elif isinstance(node,nodes.SubscrNode):
        return "[sub]"+bb_out_body(node.content,flags=flags)+"[/sub]"
    elif isinstance(node,nodes.HrefNode):
        label=bb_out(node.label)
        ht=node.hreftype
        content=node.content
        if ht=="url":
            if re.match("https?://(www\.)?tvtropes.org",content):
                return "[u]"+label+("[/u][sup][url=%s](TVTropes)[/url][/sup]"%json.dumps(content))
            return ("[url=%s]"%json.dumps(content))+label+"[/url]"
        elif ht=="wikilink":
            if not label:
                return "[wiki=%s]"%json.dumps(content)
            else:
                return "[wiki=%s title=%s]"%(json.dumps(content),json.dumps(label))
        else: #Including img
            label=label.strip()
            if label:
                return ("[%s alt=%s]"%(ht,json.dumps(label)))+content+"[/"+ht+"]"
            return "["+ht+"]"+content+"[/"+ht+"]"
    elif isinstance(node,nodes.NewlineNode):
        return "[br]"
    elif isinstance(node,nodes.RuleNode):
        return "\n[rule]\n"
    elif isinstance(node,nodes.TableNode):
        r='\n[table]'
        for row in node.table_head:
            r+="[tr]"
            for cell in row:
                r+="[th]"+bb_out_body(list(cell),flags=flags)+"[/th]"
            r+="[/tr]"
        for row in node.table_body:
            r+="[tr]"
            for cell in row:
                r+="[td]"+bb_out_body(list(cell),flags=flags)+"[/td]"
            r+="[/tr]"
        return r+"[/table]\n"
    elif isinstance(node,nodes.EmptyInterrupterNode):
        return ""
    else:
        return "ERROR"+repr(node)

__mdplay_renderer__="bb_out"
__mdplay_snippet_renderer__="bb_out_body"

