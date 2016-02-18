import re
from mdplay import nodes

def tvwiki_out(nodes,titl_ignored=None,flags=()):
    return tvwiki_out_body(nodes,flags=flags)

def tvwiki_out_body(nodes,flags=()):
    r=""
    for node in nodes:
        r+=_tvwiki_out_body(node,flags=flags)
    return r

def _tvwiki_out_body(node,flags=()):
    if not isinstance(node,nodes.Node): #i.e. is a string
        return node.replace("&","&amp;").replace("[","&#91;").replace("]","&#93;").replace("{","&#123;").replace("}","&#125;").replace("<","&lt;").replace(">","&gt;").replace("''","&#39;&#39;").replace("/","&#47;")
    elif isinstance(node,nodes.TitleNode):
        return "\n"+("!"*node.depth)+" "+tvwiki_out_body(node.content)+"\n"
    elif isinstance(node,nodes.ParagraphNode):
        return "\n"+tvwiki_out_body(node.content)+"\n"
    elif isinstance(node,nodes.BlockQuoteNode):
        if "forum" in flags:
            return "\n[[quoteblock]]"+bb_out_body(node.content,flags=flags)+"[[/quoteblock]]\n"
        else:
            def incrindent(data):
                data=data.split("\n")
                for i in range(len(data)):
                    if data[i].startswith("-") and data[i].lstrip("-").startswith(">"):
                        data[i]="-"+data[i]
                    else:
                        data[i]="->"+data[i]
                return "\n".join(data)
            return "\n"+incrindent(tvwiki_out_body(node.content).strip("\r\n"))+"\n"
    elif isinstance(node,nodes.SpoilerNode):
        return '\n[[spoiler:'+tvwiki_out_body(node.content)+"]]\n"
    elif isinstance(node,nodes.CodeBlockNode):
        return "\n@@[="+("".join(node.content)).replace("=]","=]=[=]").replace("\n","=]@@\n@@[=")+"=]@@\n"
    elif isinstance(node,nodes.CodeSpanNode):
        return "@@[="+("".join(node.content)).replace("=]","=]=[=]")+"=]@@"
    elif isinstance(node,nodes.UlliNode):
        return ("*"*node.depth)+"* "+tvwiki_out_body(node.content).strip("\r\n")+"\n"
    elif isinstance(node,nodes.OlliNode):
        return ("#"*node.depth)+"# "+tvwiki_out_body(node.content).strip("\r\n")+"\n"
    elif isinstance(node,nodes.BoldNode):
        return "'''"+tvwiki_out_body(node.content)+"'''"
    elif isinstance(node,nodes.ItalicNode):
        return "''"+tvwiki_out_body(node.content)+"''"
    elif isinstance(node,nodes.SuperNode):
        return "[[superscript:"+tvwiki_out_body(node.content)+"]]"
    elif isinstance(node,nodes.SubscrNode):
        return "[[subscript:"+tvwiki_out_body(node.content)+"]]"
    elif isinstance(node,nodes.HrefNode):
        label=tvwiki_out_body(node.label)
        ht=node.hreftype
        content=node.content
        if ht in ("wiki","wikilink"):
            namespace=""
            if ":" in content:
                namespace,content=content.split(":",1)
                namespace=namespace.lstrip()
            if namespace:
                if not label:
                    label=namespace+":"+content
                namespace+="/"
            if label and (label!=content):
                return "[["+namespace+"{{"+content+"}} "+label+"]]"
            else:
                return "{{"+content+"}}"
        else:
            #showtropes is a tad redundant here.
            #%-escapes will be parsed by browser and may be already present,
            #so NO escaping of % here.
            if (label) and (label!=content):
                return "[["+content.replace(" ","%20")+" "+label+"]]"
            else:
                return content.replace(" ","%20")
    elif isinstance(node,nodes.NewlineNode):
        return "[softreturn]"
    elif isinstance(node,nodes.RuleNode):
        return "\n----\n"
    elif isinstance(node,nodes.TableNode):
        r='\n||border=1"'
        for row in node.table_head:
            r+="\n||"
            for cell in row:
                r+=tvwiki_out_body(list(cell)).strip().replace("\n","[softreturn]")+"||"
        for row in node.table_body:
            r+="\n||"
            for cell in row:
                r+=tvwiki_out_body(list(cell)).strip().replace("\n","[softreturn]")+"||"
        return r+"\n"
    elif isinstance(node,nodes.EmptyInterrupterNode):
        return "\n"
    else:
        return "ERROR"+repr(node)

__mdplay_renderer__="tvwiki_out"
__mdplay_snippet_renderer__="tvwiki_out_body"

