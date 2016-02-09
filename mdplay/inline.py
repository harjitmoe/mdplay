import re,string

from mdplay import nodes, umlaut
from mdplay.uriregex import uriregex

punct=string.punctuation+string.whitespace

open("mega.txt","w").write(uriregex)

def _parse_inline(content,levs=("root",),flags=()):
    # Note: the recursion works by the list being a Python
    # mutable, "passed by reference" as it were
    lastchar=" "
    if ("noverifyurl" not in flags):
        urireg=uriregex
    else:
        urireg=".*"
    if ("strict" not in flags) and ("nospecialhrefs" not in flags):
        hrefre="(!?\[.*\]\("+urireg+"\))|((!\w+)\[.*\]\(.*\))"
    elif ("noembeds" not in flags):
        hrefre="!?\[.*\]\("+urireg+"\)"
    else:
        hrefre="\[.*\]\("+urireg+"\)"
    out=[]
    out2=[]
    lev=levs[0]
    while content:
        c=content.pop(0)
        ### BibTeX diacritics
        if c=="\\" and ("bibuml" in levs) and ("strict" not in flags) and ("nodiacritic" not in flags):
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
        elif ("bibuml" in levs) and ("strict" not in flags) and ("nodiacritic" not in flags): #but not c=="\\"
            lastchar=c
            out.append("{")
            out.append(c)
            return out
        ### Code spans (must be before escaping) ###
        if lev.startswith("codespan"):
            backticks=len(lev)-len("codespan")
            if ( c+("".join(content[:backticks-1])) ) == ( "`"*backticks ):
                for i in range(backticks-1):
                    content.pop(0)
                return out
            out.append(c)
        elif c=="`" and (lev!="wikilink" or out2):
            while content[0]=="`":
                c+=content.pop(0)
            out.append(nodes.CodeSpanNode(_parse_inline(content,("codespan"+c,)+levs,flags=flags)))
        ### Escaping ###
        elif c=="\\" and content and (content[0] in punct):
            c2=content.pop(0)
            if c2 in " \n":
                lastchar=" "
                continue
            lastchar=c+c2
            out.append(c2)
            continue
        ### Newlines (there are only true newlines by this point) ###
        elif c=="\n" and (lev!="wikilink" or out2):
            out.append(nodes.NewlineNode())
            lastchar=" "
        ### Emphases ###
        #### /With asterisks
        elif c=="*" and content[0]=="*" and ("bold" not in levs) and (lev!="wikilink" or out2):
            del content[0]
            out.append(nodes.BoldNode(_parse_inline(content,("bold",)+levs,flags=flags),emphatic=True))
        elif c=="*" and content[0]=="*" and lev=="bold":
            del content[0]
            return out
        elif c=="*" and content[0]!="*" and ("italic" not in levs) and (lev!="wikilink" or out2):
            out.append(nodes.ItalicNode(_parse_inline(content,("italic",)+levs,flags=flags),emphatic=True))
        elif c=="*" and lev=="italic":
            return out
        #### /With underscores
        elif c=="_" and content[0]=="_" and ("boldalt" not in levs) and (lastchar in punct) and (lev!="wikilink" or out2):
            del content[0]
            out.append(nodes.BoldNode(_parse_inline(content,("boldalt",)+levs,flags=flags),emphatic=False))
        elif c=="_" and content[0]=="_" and lev=="boldalt" and ("".join(content[1:2]) in punct):
            del content[0]
            return out
        elif c=="_" and content[0]!="_" and ("italicalt" not in levs) and (lastchar in punct) and (lev!="wikilink" or out2):
            out.append(nodes.ItalicNode(_parse_inline(content,("italicalt",)+levs,flags=flags),emphatic=False))
        elif c=="_" and (content[0] in punct) and lev=="italicalt":
            return out
        #### /With apostrophes
        elif c=="'" and "".join(content).startswith("''") and ("boldmw" not in levs) and (lev!="wikilink" or out2) and ("strict" not in flags) and ("nowikitext" not in flags) and ("nowikiemph" not in flags):
            del content[0]
            del content[0] #yes, again
            out.append(nodes.BoldNode(_parse_inline(content,("boldmw",)+levs,flags=flags),emphatic=False))
        elif c=="'" and "".join(content).startswith("''") and lev=="boldmw" and ("strict" not in flags) and ("nowikitext" not in flags) and ("nowikiemph" not in flags):
            del content[0]
            del content[0] #yes, again
            return out
        elif c=="'" and content[0]=="'" and ("italicmw" not in levs) and (lev!="wikilink" or out2) and ("strict" not in flags) and ("nowikitext" not in flags) and ("nowikiemph" not in flags):
            del content[0]
            out.append(nodes.ItalicNode(_parse_inline(content,("italicmw",)+levs,flags=flags),emphatic=False))
        elif c=="'" and content[0]=="'" and lev=="italicmw" and ("strict" not in flags) and ("nowikitext" not in flags) and ("nowikiemph" not in flags):
            del content[0]
            return out
        ### HREFs (links and embeds) ###
        elif re.match(hrefre,c+("".join(content))) and (lev!="wikilink" or out2):
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
        elif c=="[" and content[0]=="[" and (lev!="wikilink" or out2) and ("strict" not in flags) and ("nowikitext" not in flags) and ("nowikilinks" not in flags):
            del content[0]
            x,y=_parse_inline(content,("wikilink",)+levs,flags=flags)
            out.append(nodes.HrefNode("".join(x),y,"wiki"))
        elif c=="|" and lev=="wikilink" and ("strict" not in flags) and ("nowikitext" not in flags) and ("nowikilinks" not in flags):
            out2,out=out,[]
        elif c=="]" and content[0]=="]" and lev=="wikilink" and ("strict" not in flags) and ("nowikitext" not in flags) and ("nowikilinks" not in flags):
            del content[0]
            if not out2:
                out2=out[:]
            return out2,out
        ### Superscripts and Subscripts ###
        elif c=="^" and content[0]=="(" and (lev!="wikilink" or out2) and ("nosupersubscript" not in flags) and ("strict" not in flags) and ("noredditstyle" not in flags):
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,("supred",)+levs,flags=flags)))
        elif c==")" and lev=="supred" and ("nosupersubscript" not in flags) and ("strict" not in flags) and ("noredditstyle" not in flags):
            return out
        elif c=="(" and content[0]=="^" and (lev!="wikilink" or out2) and ("nosupersubscript" not in flags) and ("strict" not in flags) and ("nopandocstyle" not in flags):
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,("suppan",)+levs,flags=flags)))
        elif c=="^" and content[0]==")" and lev=="suppan" and ("nosupersubscript" not in flags) and ("strict" not in flags) and ("nopandocstyle" not in flags):
            del content[0]
            return out
        elif c=="(" and content[0]=="~" and (lev!="wikilink" or out2) and ("nosupersubscript" not in flags) and ("strict" not in flags) and ("nopandocstyle" not in flags):
            del content[0]
            out.append(nodes.SubscrNode(_parse_inline(content,("sub",)+levs,flags=flags)))
        elif c=="~" and content[0]==")" and lev=="sub" and ("nosupersubscript" not in flags) and ("strict" not in flags) and ("nopandocstyle" not in flags):
            del content[0]
            return out
        #
        elif c=="{" and (lev!="wikilink" or out2) and ("strict" not in flags) and ("nodiacritic" not in flags):
            out.extend(_parse_inline(content,("bibuml",)+levs,flags=flags))
        else:
            lastchar=c
            out.append(c)
    return out

def parse_inline(content,flags=()):
    return _parse_inline([i.encode("utf-8") for i in list(content.decode("utf-8"))]+[""],flags=flags)
