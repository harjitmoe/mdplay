import re,string

from mdplay import nodes, umlaut

punct=string.punctuation+string.whitespace
def _parse_inline(content,levs=("root",),flags=()):
    # Note: the recursion works by the list being a Python
    # mutable, "passed by reference" as it were
    lastchar=" "
    out=[]
    lev=levs[0]
    while content:
        c=content.pop(0)
        ### BibTeX diacritics
        if c=="\\" and ("bibuml" in levs):
            c2=""
            umldep=0
            while content:
                c2+=content.pop(0)
                if c2[-1]=="{":
                    umldep+=1
                if c2[-1]=="}":
                    umldep-=1
                if umldep<0:
                    break
            if c2.endswith("}"): #i.e. did not run into EOF
                c2=c2[:-1]
            braced=0
            if ("{" in c2) and c2.endswith("}"): #a second }
                braced=1
                c2=c2[:-1]
                c2,c3=c2.split("{",1)
            else:
                c2,c3=c2[:1],c2[1:]
            try:
                r=umlaut.umlaut(c2,c3).encode("utf-8")
            except ValueError:
                try:
                    if not braced:
                        r=umlaut.umlaut(c2+c3,'').encode("utf-8")
                    else:
                        raise ValueError #yeah yeah I know
                except ValueError:
                    lastchar=c+c2+c3
                    out.append(lastchar)
                else:
                    lastchar=r
                    out.append(r)
            else:
                lastchar=r
                out.append(r)
            return out
        elif "bibuml" in levs: #but not c=="\\"
            lastchar=c
            out.append("{")
            out.append(c)
            return out
        ### Escaping ###
        if c=="\\" and content and (content[0] in punct):
            c2=content.pop(0)
            if c2 in " \n":
                lastchar=" "
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
            out.append(nodes.BoldNode(_parse_inline(content,("bold",)+levs,flags=flags),emphatic=True))
        elif c=="*" and content[0]=="*" and lev=="bold":
            del content[0]
            return out
        elif c=="*" and content[0]!="*" and ("italic" not in levs):
            out.append(nodes.ItalicNode(_parse_inline(content,("italic",)+levs,flags=flags),emphatic=True))
        elif c=="*" and lev=="italic":
            return out
        #### /With underscores
        elif c=="_" and content[0]=="_" and ("boldalt" not in levs) and (lastchar in punct):
            del content[0]
            out.append(nodes.BoldNode(_parse_inline(content,("boldalt",)+levs,flags=flags),emphatic=False))
        elif c=="_" and content[0]=="_" and lev=="boldalt" and ("".join(content[1:2]) in punct):
            del content[0]
            return out
        elif c=="_" and content[0]!="_" and ("italicalt" not in levs) and (lastchar in punct):
            out.append(nodes.ItalicNode(_parse_inline(content,("italicalt",)+levs,flags=flags),emphatic=False))
        elif c=="_" and (content[0] in punct) and lev=="italicalt":
            return out
        #### /With apostrophes
        elif c=="'" and "".join(content).startswith("''") and ("boldmw" not in levs):
            del content[0]
            del content[0] #yes, again
            out.append(nodes.BoldNode(_parse_inline(content,("boldmw",)+levs,flags=flags),emphatic=False))
        elif c=="'" and "".join(content).startswith("''") and lev=="boldmw":
            del content[0]
            del content[0] #yes, again
            return out
        elif c=="'" and content[0]=="'" and ("italicmw" not in levs):
            del content[0]
            out.append(nodes.ItalicNode(_parse_inline(content,("italicmw",)+levs,flags=flags),emphatic=False))
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
            label=_parse_inline(content,("label",)+levs,flags=flags)
            href=""
            if content[0]=="(":
                del content[0]
                c=content.pop(0)
                while c!=")":
                    if (c=="\\") and (content[0] in "\\)"):
                        c=content.pop(0)
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
            out.append(nodes.SuperNode(_parse_inline(content,("supred",)+levs,flags=flags)))
        elif c==")" and lev=="supred":
            return out
        elif c=="(" and content[0]=="^":
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,("suppan",)+levs,flags=flags)))
        elif c=="^" and content[0]==")" and lev=="suppan":
            del content[0]
            return out
        elif c=="(" and content[0]=="~":
            del content[0]
            out.append(nodes.SubscrNode(_parse_inline(content,("sub",)+levs,flags=flags)))
        elif c=="~" and content[0]==")" and lev=="sub":
            del content[0]
            return out
        #
        elif c=="{":
            out.extend(_parse_inline(content,("bibuml",)+levs,flags=flags))
        else:
            lastchar=c
            out.append(c)
    return out

def parse_inline(content,flags=()):
    return _parse_inline(list(content)+[""],flags=flags)
