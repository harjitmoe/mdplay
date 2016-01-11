import re,string

import nodes, umlaut

punct=string.punctuation+string.whitespace
def _parse_inline(content,levs=("root",)):
    # Note: the recursion works by the list being a Python
    # mutable, "passed by reference" as it were
    lastchar=" "
    out=[]
    lev=levs[0]
    while content:
        c=content.pop(0)
        ### Escaping ###
        if c=="\\" and (content[0] in punct):
            c2=content.pop(0)
            if c2 in " \n":
                lastchar=" "
                continue
            elif "bibuml" in levs:
                c3=content.pop(0)
                try:
                    r=umlaut.umlaut(c2,c3).encode("utf-8")
                except ValueError:
                    content.insert(0,c3) #undo that...
                    #NO continue
                else:
                    lastchar=r
                    out.append(r)
                    continue
            lastchar=c+c2
            out.append(c2)
            continue
        ### Newlines (there are only true newlines by this point) ###
        elif c=="\n":
            out.append(nodes.NewlineNode())
            lastchar=" "
        ### Emphases ###
        #### /With asterisks
        elif c=="*" and content[0]=="*" and ("bold" not in levs):
            del content[0]
            out.append(nodes.BoldNode(_parse_inline(content,("bold",)+levs)))
        elif c=="*" and content[0]=="*" and lev=="bold":
            del content[0]
            return out
        elif c=="*" and content[0]!="*" and ("italic" not in levs):
            out.append(nodes.ItalicNode(_parse_inline(content,("italic",)+levs)))
        elif c=="*" and lev=="italic":
            return out
        #### /With underscores
        elif c=="_" and content[0]=="_" and ("boldalt" not in levs) and (lastchar in punct):
            del content[0]
            out.append(nodes.BoldNode(_parse_inline(content,("boldalt",)+levs)))
        elif c=="_" and content[0]=="_" and lev=="boldalt" and ("".join(content[1:2]) in punct):
            del content[0]
            return out
        elif c=="_" and content[0]!="_" and ("italicalt" not in levs) and (lastchar in punct):
            out.append(nodes.ItalicNode(_parse_inline(content,("italicalt",)+levs)))
        elif c=="_" and (content[0] in punct) and lev=="italicalt":
            return out
        #### /With apostrophes
        elif c=="'" and "".join(content).startswith("''") and ("boldmw" not in levs):
            del content[0]
            del content[0] #yes, again
            out.append(nodes.BoldNode(_parse_inline(content,("boldmw",)+levs)))
        elif c=="'" and "".join(content).startswith("''") and lev=="boldmw":
            del content[0]
            del content[0] #yes, again
            return out
        elif c=="'" and content[0]=="'" and ("italicmw" not in levs):
            del content[0]
            out.append(nodes.ItalicNode(_parse_inline(content,("italicmw",)+levs)))
        elif c=="'" and content[0]=="'" and lev=="italicmw":
            del content[0]
            return out
        ### HREFs (links and embeds) ###
        elif (len(lastchar)==1) and re.match("( !\w*|.)\[.*\]\(.*\)",lastchar+c+("".join(content))):
            #(re.match, not re.search, i.e. looks only at start of string)
            hreftype=""
            while c!="[":
                hreftype+=c
                c=content.pop(0)
            label=_parse_inline(content,("label",)+levs)
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
            out.append(nodes.SuperNode(_parse_inline(content,("supred",)+levs)))
        elif c==")" and lev=="supred":
            return out
        elif c=="(" and content[0]=="^":
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,("suppan",)+levs)))
        elif c=="^" and content[0]==")" and lev=="suppan":
            del content[0]
            return out
        elif c=="(" and content[0]=="~":
            del content[0]
            out.append(nodes.SubscrNode(_parse_inline(content,("sub",)+levs)))
        elif c=="~" and content[0]==")" and lev=="sub":
            del content[0]
            return out
        #
        elif c=="}" and lev=="bibuml":
            return out
        elif c=="{":
            out.extend(_parse_inline(content,("bibuml",)+levs))
        else:
            lastchar=c
            out.append(c)
    return out

def parse_inline(content):
    return _parse_inline(list(content)+[""])
