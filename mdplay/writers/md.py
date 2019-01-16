__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import nodes, mdputil
import re

def md_out(nodes,titl_ignored=None,flags=()):
    r=md_out_body(nodes,flags=flags)
    if r and (r[0]==r[-1]=="\n"):
        r=r[1:-1]
    return r

def md_out_body(nodel,flags=()):
    r=""
    for node in nodel:
        add=_md_out_body(node,flags=flags)
        r+=add
    return r

def _md_out_body(node,flags=()):
    if not isinstance(node,nodes.Node): #i.e. is a string
        #XXX any more needed?  are these appropriate?
        return node.replace("\\","\\\\").replace("[","\\[").replace("*","\\*").replace("_","\\_").replace("^","\\^").replace("-","\\-").replace("''","'\\'").replace("&","&amp;")
    elif isinstance(node,nodes.TitleNode):
        return "\n"+("#"*node.depth)+" "+md_out_body(node.content,flags).rstrip()+"\n"
    elif isinstance(node,nodes.ParagraphNode):
        return "\n"+md_out_body(node.content,flags).rstrip(" ")+"\n"
    elif isinstance(node,nodes.BlockQuoteNode):
        return "\n> "+md_out_body(node.content,flags).strip("\r\n").replace("\n","\n> ")+"\n"
    elif isinstance(node,nodes.BlockSpoilerNode):
        return "\n>! "+md_out_body(node.content,flags).strip("\r\n").replace("\n","\n>! ")+"\n"
    elif isinstance(node,nodes.InlineSpoilerNode):
        if not node.label:
            if "classicsubredditspoiler" in flags:
                return "["+md_out_body(node.content,flags)+"](/spoiler)"
            elif "nobackslashspace" in flags:
                return ">!"+md_out_body(node.content,flags)+"!<"
            else:
                return "\ >!"+md_out_body(node.content,flags)+"!<"
        else:
            return "["+md_out_body(node.label,flags)+"](/s "+md_out_body(node.content,flags)+")"
    elif isinstance(node,nodes.CodeBlockNode):
        rcontent="".join(node.content)
        bullet="~~~~~~"
        while bullet in rcontent:
            bullet+="~"
        if rcontent[-1] != "\n":
            rcontent += "\n"
        return "\n"+bullet+" "+node.clas+"\n"+rcontent+bullet+"\n"
    elif isinstance(node,nodes.CodeSpanNode):
        rcontent="".join(node.content)
        bullet="`"
        while bullet in rcontent:
            bullet+="`"
        return bullet+rcontent+bullet
    elif isinstance(node,nodes.UlliNode):
        return ("\x20\x20"*node.depth)+"* "+md_out_body(node.content,flags).strip("\r\n").replace("\n","\n"+("\x20\x20"*(node.depth+1)))+"\n"
    elif isinstance(node,nodes.OlliNode):
        return ("\x20\x20"*node.depth)+str(node.bullet)+") "+md_out_body(node.content,flags).strip("\r\n").replace("\n","\n"+("\x20\x20"*(node.depth+1))+(" "*+len(str(node.bullet))))+"\n"
    elif isinstance(node,nodes.BoldNode):
        if node.emphatic or ("nobackslashspace" in flags) or ("noemphunderscore" in flags) or ("discordunderline" in flags):
            return "**"+md_out_body(node.content,flags)+"**"
        else:
            return "\ __"+md_out_body(node.content,flags)+"__\ "
    elif isinstance(node,nodes.UnderlineNode):
        if "discordunderline" in flags:
            return "__"+md_out_body(node.content,flags)+"__"
        else:
            return "<u>"+md_out_body(node.content,flags)+"</u>"
    elif isinstance(node,nodes.ItalicNode):
        if node.emphatic or ("nobackslashspace" in flags) or ("noemphunderscore" in flags):
            return "*"+md_out_body(node.content,flags)+"*"
        else:
            return "\ _"+md_out_body(node.content,flags)+"_\ "
    elif isinstance(node,nodes.ItalicNode):
        return "~~"+md_out_body(node.content,flags)+"~~"
    elif isinstance(node,nodes.SuperNode):
        if ("pandoc" in flags):
            return "(^"+md_out_body(node.content,flags).replace(")","\\)")+"^)"
        else:
            return "^("+md_out_body(node.content,flags).replace(")","\\)")+")"
    elif isinstance(node,nodes.SubscrNode):
        return "(~"+md_out_body(node.content,flags).replace(")","\\)")+"~)"
    elif isinstance(node,nodes.RubiNode):
        label = md_out_body(node.label)
        content = md_out_body(node.content)
        return content+" ("+label+") "
    elif isinstance(node,nodes.HrefNode):
        label=md_out_body(node.label,flags)
        ht=node.hreftype
        content=node.content
        if ht=="url":
            return "["+label+"]("+content.replace("\\","\\\\").replace(")","\\)")+")"
        elif ht=="img":
            siz="x"
            if node.width: siz = str(node.width) + siz
            if node.height: siz += str(node.height)
            if siz=="x": siz = ""
            else: siz = "\x20=" + siz
            if "nosizes" in flags: siz = ""
            return "!["+label+"]("+content.replace("\\","\\\\").replace(")","\\)")+siz+")"
        else:
            return "!"+ht+"["+label+"]("+content.replace("\\","\\\\").replace(")","\\)")+")"
    elif isinstance(node,nodes.NewlineNode):
        return "\x20\x20\n"
    elif isinstance(node,nodes.RuleNode):
        return "\n- - -\n"
    elif isinstance(node,nodes.TableNode):
        r=""
        for row in node.table_head[:1]:
            r+="\n|"
            for cell in row:
                r+=md_out_body(list(cell)).strip().replace("|","\\|").replace("\n","&#10;")+"|"
        r+="\n"
        for colno in range(len(node.table_head[0])):
            if node.aligns and node.aligns[colno] and (len(node.aligns)>colno) and (node.aligns[colno] in ("left","center","right")):
                r+={"left":"|:--","center":"|:-:","right":"|--:"}[node.aligns[colno]]
            else:
                r+="|---"
        r+="|"
        for row in node.table_head[1:]+node.table_body:
            r+="\n|"
            for cell in row:
                r+=md_out_body(list(cell)).strip().replace("|","\\|").replace("\n","&#10;")+"|"
        return r+"\n"
    elif isinstance(node,nodes.EmptyInterrupterNode):
        return "\n\n"
    elif isinstance(node,nodes.EmojiNode):
        force_shortcode=("shortcodes" in flags) and node.label[1]
        if ("notwemoji" not in flags) and node.emphatic and (not force_shortcode):
            hexcode = node.label[2]
            altcode = node.content
            if "oldtwemoji" in flags:
                return "![%s](https://twemoji.maxcdn.com/36x36/%s.png)"%(altcode, hexcode)
            else:
                if "nosizes" not in flags:
                    siz = "\x20=32x32"
                else:
                    siz = ""
                return "![%s](https://twemoji.maxcdn.com/2/72x72/%s.png%s)"%(altcode, hexcode, siz)
        if ("nouseemoji" not in flags) and (not force_shortcode):
            return node.content
        elif ((node.hreftype=="ascii") or ("asciimotes" in flags)) and (not force_shortcode):
            return node.label[0]
        else:
            return ":"+(node.label[1] or "unnamed")+":"
    else:
        return "ERROR"+repr(node)

__mdplay_renderer__="md_out"
__mdplay_snippet_renderer__="md_out_body"

