import re
from mdplay import nodes

def mwiki_out(nodes,titl_ignored=None,flags=()):
    return mwiki_out_body(nodes,flags=flags)

def mwiki_out_body(nodes,flags=()):
    r=""
    for node in nodes:
        r+=_mwiki_out_body(node,flags=flags)
    return r

def _mwiki_out_body(node,flags=()):
    if not isinstance(node,nodes.Node): #i.e. is a string
        return node.replace("&","&amp;").replace("[","&#91;").replace("]","&#93;").replace("{","&#123;").replace("}","&#125;").replace("<","&lt;").replace(">","&gt;").replace("''","&#39;&#39;")
    elif isinstance(node,nodes.TitleNode):
        return "\n"+("="*node.depth)+" "+mwiki_out_body(node.content)+("="*node.depth)+"\n"
    elif isinstance(node,nodes.ParagraphNode):
        return "\n"+mwiki_out_body(node.content)+"\n"
    elif isinstance(node,nodes.BlockQuoteNode):
        return "\n:"+mwiki_out_body(node.content).strip("\r\n").replace("\n","\n:")+"\n"
    elif isinstance(node,nodes.SpoilerNode):
        return '<span class="mw-customtoggle-%s" style="color:blue;cursor:pointer">Expand/Hide Spoiler</span><div id="mw-customcollapsible-%s" class="mw-collapsible mw-collapsed" style="display:none;">'%(id(node),id(node))+mwiki_out_body(node.content)+"</div>"
    elif isinstance(node,nodes.CodeBlockNode):
        return "\n<pre>"+mwiki_out_body(node.content)+"</pre>\n"
    elif isinstance(node,nodes.CodeSpanNode):
        return "<code>"+mwiki_out_body(node.content)+"</code>"
    elif isinstance(node,nodes.UlliNode):
        return ("*"*node.depth)+"* "+mwiki_out_body(node.content).strip("\r\n")+"\n"
    elif isinstance(node,nodes.OlliNode):
        return ("#"*node.depth)+"# "+mwiki_out_body(node.content).strip("\r\n")+"\n"
    elif isinstance(node,nodes.BoldNode):
        return "'''"+mwiki_out_body(node.content)+"'''"
    elif isinstance(node,nodes.ItalicNode):
        return "''"+mwiki_out_body(node.content)+"''"
    elif isinstance(node,nodes.SuperNode):
        return "<sup>"+mwiki_out_body(node.content)+"</sup>"
    elif isinstance(node,nodes.SubscrNode):
        return "<sub>"+mwiki_out_body(node.content)+"</sub>"
    elif isinstance(node,nodes.HrefNode):
        label=mwiki_out_body(node.label)
        ht=node.hreftype
        content=node.content
        if ht in ("wiki","wikilink"):
            if label:
                return "[["+content+"|"+label+"]]"
            else:
                return "[["+content+"]]"
        else:
            if ("showtropes" in flags) and re.match("https?://(www\.)?tvtropes.org",content):
                return "<u>"+label+("</u><sup>[%s (TVTropes)]</sup>"%content.replace(" ","%20"))
            #%-escapes will be parsed by browser and may be already present,
            #so NO escaping of %.
            if label:
                return "["+content.replace(" ","%20")+" "+label+"]"
            else:
                return content.replace(" ","%20")
    elif isinstance(node,nodes.NewlineNode):
        return "<br />"
    elif isinstance(node,nodes.RuleNode):
        return "\n<hr />\n"
    elif isinstance(node,nodes.TableNode):
        r='\n{|border="1"\n'
        for row in node.table_head:
            r+="|-\n"
            for cell in row:
                r+="!"+mwiki_out_body(list(cell)).strip("\r\n")+"\n"
        for row in node.table_body:
            r+="|-\n"
            for cell in row:
                r+="|"+mwiki_out_body(list(cell)).strip("\r\n")+"\n"
        return r+"|}\n"
    elif isinstance(node,nodes.EmptyInterrupterNode):
        return "\n"
    else:
        return "ERROR"+repr(node)

__mdplay_renderer__="mwiki_out"
__mdplay_snippet_renderer__="mwiki_out_body"

