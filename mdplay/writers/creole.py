__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import nodes, mdputil
import re

def creole_out(nodes,titl_ignored=None,flags=()):
    return creole_out_body(nodes,flags=flags)

def creole_out_body(nodel,flags=()):
    r=""
    for node in nodel:
        r+=_creole_out_body(node,flags=flags)
    return r

# Highest authority: https://web.archive.org/web/20190406174234/http://www.wikicreole.org/wiki/Creole1.0
# Higher authority: https://web.archive.org/web/20191229025127/http://www.wikicreole.org/wiki/CreoleAdditions
# Lower authority: https://web.archive.org/web/20200808212700/http://www.wikicreole.org/wiki/HintsOnExtending

tripleclose_re = re.compile(r"\n(\s*)\}\}\}")

def _creole_out_body(node,flags=()):
    if not isinstance(node,nodes.Node): #i.e. is a string
        ret = node.replace("~","~~").replace("[[","[~[").replace("]]","]~]").replace("{{","{~{"
                 ).replace("}}","}~}").replace("**","*~*").replace("__", "_~_").replace("##", "#~#"
                 ).replace("//","/~/").replace("\\\\","\\~\\").replace("^^","^~^"
                 ).replace(",,",",~,").replace("<<","<~<")
        if len(ret) and ret[0] in "#*=|":
            ret = "~" + ret
        return ret
    elif isinstance(node,nodes.TitleNode):
        return "\n"+("="*node.depth)+" "+creole_out_body(node.content,flags=flags)+"\n"
    elif isinstance(node,nodes.ParagraphNode):
        return "\n"+creole_out_body(node.content,flags=flags)+"\n"
    elif isinstance(node,nodes.BlockQuoteNode):
        def incrindent(data):
            data=data.split("\n\n")
            for i in range(len(data)):
                if data[i].startswith(">"):
                    data[i]=">"+data[i]
                else:
                    data[i]="> "+data[i]
            return "\n".join(data)
        return "\n"+incrindent(creole_out_body(node.content).strip("\r\n"))+"\n"
    #elif isinstance(node,nodes.SpoilerNode):
    elif isinstance(node,nodes.CodeBlockNode):
        rcontent="".join(node.content)
        rcontent=tripleclose_re.sub(lambda m: "\n" + m.group(1) + " }}}", rcontent)
        return "\n{{{\n"+rcontent+"\n}}}\n"
    elif isinstance(node,nodes.CodeSpanNode):
        rcontent="".join(node.content)
        if "}}}" not in rcontent.rstrip("}"):
            return "{{{"+rcontent+"}}}"
        else:
            return "##"+_creole_out_body(rcontent,flags=flags)+"##"
    elif isinstance(node,nodes.UlliNode):
        return ("*"*node.depth)+"* "+creole_out_body(node.content,flags=flags).strip("\r\n")+"\n"
    elif isinstance(node,nodes.OlliNode):
        return ("#"*node.depth)+"# "+creole_out_body(node.content,flags=flags).strip("\r\n")+"\n"
    elif isinstance(node,nodes.BoldNode):
        return "**"+creole_out_body(node.content,flags=flags)+"**"
    elif isinstance(node,nodes.UnderlineNode):
        return "__"+creole_out_body(node.content,flags=flags)+"__"
    elif isinstance(node,nodes.ItalicNode):
        return "//"+creole_out_body(node.content,flags=flags)+"//"
    elif isinstance(node,nodes.StrikeNode):
        return "--"+creole_out_body(node.content,flags=flags)+"--"
    elif isinstance(node,nodes.SuperNode):
        return "^^"+creole_out_body(node.content,flags=flags)+"^^"
    elif isinstance(node,nodes.SubscrNode):
        return ",,"+creole_out_body(node.content,flags=flags)+",,"
    elif isinstance(node,nodes.RubiNode):
        label = creole_out_body(node.label, flags=flags)
        content = creole_out_body(node.content, flags=flags)
        return "<<ruby>>"+content+"<<rp>> (<</rp>><<rt>>"+label+"<</rt>><<rp>>) <</rp>><</ruby>>"
    elif isinstance(node,nodes.HrefNode):
        label=creole_out_body(node.label,flags=flags)
        ht=node.hreftype
        content=node.content
        if ht in ("wiki","wikilink"):
            if label:
                return "[["+content+"|"+label+"]]"
            else:
                return "[["+content+"]]"
        elif ht == "img":
            if label:
                return "{{"+content.replace(" ","%20").replace("|","%7C")+"|"+label+"}}"
            else:
                return "{{"+content.replace(" ","%20").replace("|","%7C")+"}}"
        else:
            #%-escapes will be parsed by browser and may be already present,
            #so NO escaping of %.
            if label:
                return "[["+content.replace(" ","%20").replace("|","%7C")+"|"+label+"]]"
            else:
                return "[["+content.replace(" ","%20").replace("|","%7C")+"]]"
    elif isinstance(node,nodes.NewlineNode):
        return r"\\"
    elif isinstance(node,nodes.RuleNode):
        return "\n----\n"
    elif isinstance(node,nodes.TableNode):
        r="\n"
        for row in node.table_head:
            for cell in row:
                r+="|="+creole_out_body(list(cell),flags=flags).strip("\r\n")
            r+="|\n"
        for row in node.table_body:
            for cell in row:
                r+="|"+creole_out_body(list(cell),flags=flags).strip("\r\n")
            r+="|\n"
        return r+"\n"
    elif isinstance(node,nodes.EmptyInterrupterNode):
        return "\n"
    elif isinstance(node,nodes.EmojiNode):
        return node.content
    else:
        return "ERROR"+repr(node)

__mdplay_renderer__="creole_out"
__mdplay_snippet_renderer__="creole_out_body"

