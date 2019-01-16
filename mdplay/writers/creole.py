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

def _creole_out_body(node,flags=()):
    if not isinstance(node,nodes.Node): #i.e. is a string
        return node.replace("~","~~").replace("[","~[").replace("]","~]").replace("{","~{").replace("}","~}").replace("*","~*").replace("#","~#").replace("/","~/").replace("\\","~\\")
    elif isinstance(node,nodes.TitleNode):
        return "\n"+("="*node.depth)+" "+creole_out_body(node.content,flags=flags)+"\n"
    elif isinstance(node,nodes.ParagraphNode):
        return "\n"+creole_out_body(node.content,flags=flags)+"\n"
    elif isinstance(node,nodes.BlockQuoteNode):
        return "\n:"+creole_out_body(node.content,flags=flags).strip("\r\n").replace("\n","\n:")+"\n"
    #elif isinstance(node,nodes.SpoilerNode):
    elif isinstance(node,nodes.CodeBlockNode):
        return "\n{{{\n"+creole_out_body(node.content,flags=flags).replace("\n}}}\n", "\n }}}\n")+"\n}}}\n"
    elif isinstance(node,nodes.CodeSpanNode):
        return "{{{"+creole_out_body(node.content,flags=flags)+"}}}"
    elif isinstance(node,nodes.UlliNode):
        return ("*"*node.depth)+"* "+creole_out_body(node.content,flags=flags).strip("\r\n")+"\n"
    elif isinstance(node,nodes.OlliNode):
        return ("#"*node.depth)+"# "+creole_out_body(node.content,flags=flags).strip("\r\n")+"\n"
    elif isinstance(node,nodes.BoldNode):
        return "**"+creole_out_body(node.content,flags=flags)+"**"
    #elif isinstance(node,nodes.UnderlineNode):
    #    return "<u>"+creole_out_body(node.content,flags=flags)+"</u>"
    elif isinstance(node,nodes.ItalicNode):
        return "//"+creole_out_body(node.content,flags=flags)+"//"
    #elif isinstance(node,nodes.StrikeNode):
    #    if note.emphatic:
    #        return "<del>"+creole_out_body(node.content,flags=flags)+"</del>"
    #    else:
    #        return "<s>"+creole_out_body(node.content,flags=flags)+"</s>"
    #elif isinstance(node,nodes.SuperNode):
    #    return "<sup>"+creole_out_body(node.content,flags=flags)+"</sup>"
    #elif isinstance(node,nodes.SubscrNode):
    #    return "<sub>"+creole_out_body(node.content,flags=flags)+"</sub>"
    #elif isinstance(node,nodes.RubiNode):
    #    label = creole_out_body(node.label, flags=flags)
    #    content = creole_out_body(node.content, flags=flags)
    #    return "<ruby>"+content+"<rp> (</rp><rt>"+label+"</rt><rp>) </rp></ruby>"
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
                return "[["+content.replace(" ","%20").replace("|","%7C")+" "+label+"]]"
            else:
                return content.replace(" ","%20")
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

