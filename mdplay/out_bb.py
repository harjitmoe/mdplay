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
    while in_list>0:
        if ("htmllists" not in flags):
            r+="[/li][/ul]"
        elif ("semihtmllists" not in flags):
            r+="[/li][/list]"
        else:
            r+="[/list]"
        in_list-=1
    while in_list<0:
        if ("htmllists" not in flags):
            r+="[/li][/ol]"
        elif ("semihtmllists" not in flags):
            r+="[/li][/list]"
        else:
            r+="[/list]"
        in_list+=1
    return r.strip("\r\n")

def _bb_out(node,in_list,flags):
    if (in_list>0) and ((not isinstance(node,nodes.UlliNode)) or ((node.depth+1)<in_list)):
        _r=_bb_out(node,in_list-1,flags=flags)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
            in_list+=1
        if ("htmllists" in flags):
            return "[/li][/ul]\n"+_r,in_list-1
        elif ("semihtmllists" in flags):
            return "[/li][/list]\n"+_r,in_list-1
        else:
            return "[/list]\n"+_r,in_list-1
    if (in_list<0) and ((not isinstance(node,nodes.OlliNode)) or ((-node.depth-1)<in_list)):
        _r=_bb_out(node,in_list+1,flags=flags)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
            in_list-=1
        if ("htmllists" in flags):
            return "[/li][/ol]\n"+_r,in_list+1
        elif ("semihtmllists" in flags):
            return "[/li][/list]\n"+_r,in_list+1
        else:
            return "[/list]\n"+_r,in_list+1
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
        if (node.depth+1)>in_list:
            while (node.depth+1)>in_list:
                if ("htmllists" in flags):
                    r+="\n[ul][li]" if in_list==0 else "[ul][li]"
                elif ("semihtmllists" in flags):
                    r+="\n[list][li]" if in_list==0 else "[list][li]"
                else:
                    r+="\n[list][*]" if in_list==0 else "[list][*]"
                in_list+=1
        elif ("htmllists" in flags) or ("semihtmllists" in flags):
            r+="[/li]\n[li]"
        else:
            r+="[*]"
        r+=bb_out_body(node.content,flags=flags)+"\n"
        return r,in_list
    elif isinstance(node,nodes.OlliNode):
        r=""
        def gen_liopen(fence, flags):
            if ("autonumberonly" not in flags):
                return "[li value=%s]"%json.dumps(str(fence))
            else:
                return "[li]"
        if (node.depth+1)>(-in_list):
            while (node.depth+1)>(-in_list):
                if ("htmllists" in flags):
                    r+=("\n[ol]" if in_list==0 else "[ol]")+gen_liopen(node.fence, flags)
                elif ("semihtmllists" in flags):
                    r+=("\n[list][li]" if in_list==0 else "[list][li]")+("[%d]"%node.fence)
                else:
                    r+=("\n[list][*]" if in_list==0 else "[list][*]")+("[%d]"%node.fence)
                in_list-=1
        elif ("htmllists" in flags):
            r+="[/li]\n"+gen_liopen(node.fence, flags)
        elif ("semihtmllists" in flags):
            r+="[/li]\n[li][%d]"%node.fence
        else:
            r+="[*][%d]"%node.fence
        r+=bb_out_body(node.content,flags=flags)+"\n"
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
            if ("showtropes" in flags) and re.match("https?://(www\.)?tvtropes.org",content):
                return "[u]"+label+("[/u][sup][url=%s](TVTropes)[/url][/sup]"%json.dumps(content))
            return ("[url=%s]"%json.dumps(content))+label+"[/url]"
        elif ht in ("wiki","wikilink"):
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

