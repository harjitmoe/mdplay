import re
from mdplay import nodes

def md_out(nodes,titl_ignored=None,flags=()):
    r=md_out_body(nodes,flags=flags)
    if r and (r[0]==r[-1]=="\n"):
        r=r[1:-1]
    return r

def md_out_body(nodel,flags=()):
    r=""
    for node in nodes.agglomerate(nodel):
        r+=_md_out_body(node,flags=flags)
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
    elif isinstance(node,nodes.SpoilerNode):
        return "\n>! "+md_out_body(node.content,flags).strip("\r\n").replace("\n","\n>! ")+"\n"
    elif isinstance(node,nodes.CodeBlockNode):
        rcontent="".join(node.content)
        bullet="~~~~~~"
        while bullet in rcontent:
            bullet+="~"
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
        if node.emphatic or ("nobackslashspace" in flags) or ("noemphunderscore" in flags):
            return "**"+md_out_body(node.content,flags)+"**"
        else:
            return "\ __"+md_out_body(node.content,flags)+"__\ "
    elif isinstance(node,nodes.ItalicNode):
        if node.emphatic or ("nobackslashspace" in flags) or ("noemphunderscore" in flags):
            return "*"+md_out_body(node.content,flags)+"*"
        else:
            return "\ _"+md_out_body(node.content,flags)+"_\ "
    elif isinstance(node,nodes.SuperNode):
        if ("pandoc" in flags):
            return "(^"+md_out_body(node.content,flags).replace(")","\\)")+"^)"
        else:
            return "^("+md_out_body(node.content,flags).replace(")","\\)")+")"
    elif isinstance(node,nodes.SubscrNode):
        return "(~"+md_out_body(node.content,flags).replace(")","\\)")+"~)"
    elif isinstance(node,nodes.HrefNode):
        label=md_out_body(node.label,flags)
        ht=node.hreftype
        content=node.content
        if ht=="url":
            return "["+label+"]("+content.replace("\\","\\\\").replace(")","\\)")+")"
        elif ht=="img":
            return "!["+label+"]("+content.replace("\\","\\\\").replace(")","\\)")+")"
        else:
            return "!"+ht+"["+label+"]("+content.replace("\\","\\\\").replace(")","\\)")+")"
    elif isinstance(node,nodes.NewlineNode):
        return "\x20\x20\n"
    elif isinstance(node,nodes.RuleNode):
        return "\n- - -\n"
    elif isinstance(node,nodes.TableNode):
        r="\n"
        rows_header=[]
        rows_body=[]
        for arow in node.table_head:
            row=[]
            for cell in arow:
                row.append(md_out_body(cell,flags).strip("\r\n"))
            rows_header.append(row)
        for arow in node.table_body:
            row=[]
            for cell in arow:
                row.append(md_out_body(cell,flags).strip("\r\n"))
            rows_body.append(row)
        column_guage=[]
        for col in range(len(rows_header[0])):
            guage=0
            for row in rows_header+rows_body:
                for line in row[col].split("\n"):
                    if len(line)>guage:
                        guage=len(line)
            column_guage.append(guage)
        rule=" ".join(["="*l for l in column_guage])+"\n"
        r+=rule
        def pad_to_len(line,guage):
            while len(line)<guage:
                line+=" "
            return line
        for row in rows_header:
            if row and (not row[0].strip()): row[0]="\\"
            lines=zip(*[i.split("\n") for i in row])
            for line in lines:
                if line:
                    r+=(" ".join(map(pad_to_len,line[:-1],column_guage[:-1])))+" "+line[-1]+"\n"
        r+=rule
        for row in rows_body:
            if row and (not row[0].strip()): row[0]="\\"
            lines=zip(*[i.split("\n") for i in row])
            for line in lines:
                if line:
                    r+=(" ".join(map(pad_to_len,line[:-1],column_guage[:-1])))+" "+line[-1]+"\n"
        r+=rule
        return r
    elif isinstance(node,nodes.EmptyInterrupterNode):
        return "\n\n"
    else:
        return "ERROR"+repr(node)

__mdplay_renderer__="md_out"
__mdplay_snippet_renderer__="md_out_body"

