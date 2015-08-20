import re

import nodes

punct="![]*`() \n\\#*+-=~^,.?{}'\"/|<>"
def _parse_inline(content,lev="root"):
    # Note: the recursion works by the list being a Python
    # mutable, "passed by reference" as it were
    lastchar=" "
    out=[]
    while content:
        c=content.pop(0)
        ### Escaping ###
        if c=="\\" and (content[0] in punct):
            c2=content.pop(0)
            if c2 in " \n":
                lastchar=" "
                continue
            else:
                lastchar=c+c2
                out.append(c2)
                continue
        ### Newlines (there are only true newlines by this point) ###
        elif c=="\n":
            out.append(nodes.NewlineNode())
            lastchar=" "
        ### Emphases ###
        elif c=="*":
            if content[0]=="*":
                del content[0]
                if lev=="bold":
                    return out
                out.append(nodes.BoldNode(_parse_inline(content,"bold")))
            else:
                if lev=="italic":
                    return out
                out.append(nodes.ItalicNode(_parse_inline(content,"italic")))
        elif c=="_" and content[0]=="_" and lev!="boldalt" and (lastchar in punct):
            del content[0]
            out.append(nodes.BoldNode(_parse_inline(content,"boldalt")))
        elif c=="_" and content[0]=="_" and lev=="boldalt" and ("".join(content[1:2]) in punct):
            del content[0]
            return out
        elif c=="_" and content[0]!="_" and lev!="italicalt" and (lastchar in punct):
            out.append(nodes.ItalicNode(_parse_inline(content,"italicalt")))
        elif c=="_" and (content[0] in punct) and lev=="italicalt":
            return out
        ### HREFs (links and embeds) ###
        elif (len(lastchar)==1) and re.match("( !\w*|.)\[.*\]\(.*\)",lastchar+c+("".join(content))):
            #(re.match, not re.search, i.e. looks only at start of string)
            hreftype=""
            while c!="[":
                hreftype+=c
                c=content.pop(0)
            label=_parse_inline(content,"label")
            href=""
            if content[0]=="(":
                del content[0]
                c=content.pop(0)
                while c!=")":
                    href+=c
                    c=content.pop(0)
            if hreftype=="!":
                hreftype="img"
            elif hreftype=="":
                hreftype="url"
            else:
                hreftype=hreftype[1:] #Minus the leading !
            out.append(nodes.HrefNode(href,label,hreftype))
        elif c=="]" and lev=="label":
            return out
        ### Superscripts and Subscripts ###
        elif c=="^" and content[0]=="(":
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,"supred")))
        elif c==")" and lev=="supred":
            return out
        elif c=="(" and content[0]=="^":
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,"suppan")))
        elif c=="^" and content[0]==")" and lev=="suppan":
            del content[0]
            return out
        elif c=="(" and content[0]=="~":
            del content[0]
            out.append(nodes.SubscrNode(_parse_inline(content,"sub")))
        elif c=="~" and content[0]==")" and lev=="sub":
            del content[0]
            return out
        else:
            lastchar=c
            out.append(c)
    return out

def parse_inline(content):
    return _parse_inline(list(content)+[""])
