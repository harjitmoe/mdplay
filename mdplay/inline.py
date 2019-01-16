# -*- mode: python; coding: utf-8 -*-
import re,string

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import nodes, diacritic, uriregex, cjk, emoji
from mdplay import htmlentitydefs_latest as htmlentitydefs

punct=string.punctuation+string.whitespace

def _parse_inline(content,levs=("root",),flags=(),state=None):
    # Note: the recursion works by the list being a Python
    # mutable, "passed by reference" as it were
    lastchar=" "
    if ("noverifyurl" not in flags):
        urireg="("+uriregex.uriregex+"|[#/]s(poiler)?( .+)?)"
    else:
        urireg=".*"
    if ("nospecialhrefs" not in flags):
        hrefre="(!?\[.*\]\("+urireg+"( =\d*x\d*)?\))|((!\w+)\[.*\]\(.*\))"
    elif ("noembeds" not in flags):
        hrefre="!?\[.*\]\("+urireg+"( =\d*x\d*)?\)"
    else:
        hrefre="\[.*\]\("+urireg+"\)"
    out=[]
    out2=[]
    lev=levs[0]
    while content:
        c=content.pop(0)
        isurl=re.match(uriregex.uriregex,c+("".join(content))) #NOT urireg
        ### BibTeX diacritics
        if c=="\\" and ("bibuml" in levs) and ("nodiacritic" not in flags):
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
                r=diacritic.diacritic(c2,c3)
            except ValueError:
                try:
                    if not braced:
                        r=diacritic.diacritic(c2+c3,'')
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
        elif ("bibuml" in levs) and ("nodiacritic" not in flags): #but not c=="\\"
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
            out.append(nodes.CodeSpanNode(_parse_inline(content,("codespan"+c,)+levs,flags=flags,state=state)))
        ### Escaping ###
        elif c=="\\" and content and (content[0] in punct):
            c2=content.pop(0)
            if c2 in " \n":
                lastchar=" "
                continue
            lastchar=c+c2
            out.append(c2)
            continue
        elif c=="&" and (len(content)>1) and ((content[0]+content[1]) in approaching_entity) and ("nohtmldeentity" not in flags):
            c=content[0]+content[1] #NOT +=
            n=2
            while c in approaching_entity:
                c+=content[n]
                n+=1
            if c in list(htmlentitydefs.html5.keys()):
                hamayalawa = htmlentitydefs.html5[c]
                out.append(hamayalawa)
                del content[:n]
            elif (c[:-1] in list(htmlentitydefs.html5.keys())) and ("nohtmlsloppyentity" not in flags):
                n -= 1; c = c[:-1]
                hamayalawa = htmlentitydefs.html5[c]
                out.append(hamayalawa)
                del content[:n]
            else:
                out.append("&")
        elif c == "&" and (len(content)>1) and (content[0] == "#") and ("nohtmlnumentity" not in flags):
            c = ""
            n = 1
            while content[n:] and content[n] != ";":
                c += content[n]
                n += 1
            n += 1 # The semicolon.
            if c and not c.strip("0123456789"):
                out.append(chr(int(c, 10)))
                del content[:n]
            elif c[1:] and c[0].casefold() == "x" and not c[1:].casefold().strip("0123456789abcdef"):
                out.append(chr(int(c[1:], 16)))
                del content[:n]
            else:
                out.append("&")
        ### Newlines (there are only true newlines by this point) ###
        elif c=="\n" and (lev!="wikilink" or out2):
            out.append(nodes.NewlineNode())
            lastchar=" "
        ### Bare URLs ###
        elif isurl and ("nolinkbareurl" not in flags) and (lev not in ("wikilink","label")):
            # No unescaping here.  Any escaping should be in %xx URL notation, unless escaping
            # it *being* a URI (as in escaping EGS\:NP for to not look like a URN).
            for i in range(isurl.end()-1):
                c+=content.pop(0)
            out.append(nodes.HrefNode(c,list(c),"url"))
        ### Emphases ###
        #### /With asterisks
        elif c=="*" and content[0]=="*" and ("bold" not in levs) and (lev!="wikilink" or out2):
            del content[0]
            out.append(nodes.BoldNode(_parse_inline(content,("bold",)+levs,flags=flags,state=state),emphatic=True))
        elif c=="*" and content[0]=="*" and lev=="bold":
            del content[0]
            return out
        elif c=="*" and content[0]!="*" and ("italic" not in levs) and (lev!="wikilink" or out2):
            out.append(nodes.ItalicNode(_parse_inline(content,("italic",)+levs,flags=flags,state=state),emphatic=True))
        elif c=="*" and lev=="italic":
            return out
        #### /With underscores
        elif c=="_" and content[0]=="_" and ("boldalt" not in levs) and (lastchar in punct) and (lev!="wikilink" or out2):
            del content[0]
            if "discordunderline" not in flags:
                out.append(nodes.BoldNode(_parse_inline(content,("boldalt",)+levs,flags=flags,state=state),emphatic=False))
            else: # Level still should be called boldalt, but node type should be different
                out.append(nodes.UnderlineNode(_parse_inline(content,("boldalt",)+levs,flags=flags,state=state),emphatic=False))
        elif c=="_" and content[0]=="_" and lev=="boldalt" and ("".join(content[1:2]) in punct):
            del content[0]
            return out
        elif c=="_" and content[0]!="_" and ("italicalt" not in levs) and (lastchar in punct) and (lev!="wikilink" or out2):
            out.append(nodes.ItalicNode(_parse_inline(content,("italicalt",)+levs,flags=flags,state=state),emphatic=False))
        elif c=="_" and (content[0] in punct) and lev=="italicalt":
            return out
        #### /With apostrophes
        elif c=="'" and "".join(content).startswith("''") and ("boldmw" not in levs) and (lev!="wikilink" or out2) and ("nowikiemph" not in flags):
            del content[0]
            del content[0] #yes, again
            out.append(nodes.BoldNode(_parse_inline(content,("boldmw",)+levs,flags=flags,state=state),emphatic=False))
        elif c=="'" and "".join(content).startswith("''") and lev=="boldmw" and ("nowikiemph" not in flags):
            del content[0]
            del content[0] #yes, again
            return out
        elif c=="'" and content[0]=="'" and ("italicmw" not in levs) and (lev!="wikilink" or out2) and ("nowikiemph" not in flags):
            del content[0]
            out.append(nodes.ItalicNode(_parse_inline(content,("italicmw",)+levs,flags=flags,state=state),emphatic=False))
        elif c=="'" and content[0]=="'" and lev=="italicmw" and ("nowikiemph" not in flags):
            del content[0]
            return out
        #### /Others
        elif c=="~" and "".join(content).startswith("~") and ("strikediscord" not in levs) and (lev!="wikilink" or out2) and ("nodiscordstrike" not in flags):
            del content[0]
            # emphatic=True would be <del>, emphatic=False would be <s>
            out.append(nodes.StrikeNode(_parse_inline(content,("strikediscord",)+levs,flags=flags,state=state),emphatic=True))
        elif c=="~" and "".join(content).startswith("~") and lev=="strikediscord" and ("nodiscordstrike" not in flags):
            del content[0]
            return out
        ### New Reddit spoilers (urn:x-reddit-post:8ybmnq) ###
        elif c==">" and content[0]=="!" and ("noredditrealspoiler" not in flags):
            del content[0]
            out.append(nodes.InlineSpoilerNode(_parse_inline(content,("rfmspoiler",)+levs,flags=flags,state=state)))
        elif c=="!" and content[0]=="<" and lev=="rfmspoiler" and ("noredditrealspoiler" not in flags):
            del content[0]
            return out
        ### HREFs (links and embeds, plus CJK extensions) ###
        elif re.match(hrefre,c+("".join(content))) and (lev!="wikilink" or out2):
            # Note: ridiculous amount of work needed here for CommonMark complience.
            #(re.match, not re.search, i.e. looks only at start of string)
            hreftype=""
            while c!="[":
                hreftype+=c
                c=content.pop(0)
            label=_parse_inline(content,("label",)+levs,flags=flags,state=state)
            href=""
            #print hreftype,label,content
            if content[0]=="(":
                del content[0]
                c=content.pop(0)
                while c!=")":
                    if not content:
                        href+=c
                        break
                    if (c=="\\") and (content[0] in "\\)"):
                        c=content.pop(0)
                    href+=c
                    c=content.pop(0)
            if hreftype=="!":
                hreftype="img"
            elif hreftype=="":
                hreftype="url" # Based on BBCode tag naming
            else:
                hreftype=hreftype[1:] #Minus the leading !
            width = height = ""
            def gogo(s):
                if not s: return None
                return int(s, 10)
            if (hreftype=="img") and (" =" in href):
                href, size = href.split(" =",1)
                width, height = size.split("x")
            #print(repr(hreftype), repr(label), repr(href))
            url_is_spoiler = href.strip().split()[0] in ("/spoiler","/s","#spoiler","#s")
            if url_is_spoiler and (hreftype == "url") and ("noredditcssspoiler" not in flags):
                if " " not in href.strip():
                    out.append(nodes.InlineSpoilerNode(label))
                else:
                    out.append(nodes.InlineSpoilerNode(parse_inline(href.strip().split(" ",1)[1],flags=flags,state=state),label))
            elif (hreftype.lower() == "spoiler") and ("noembedspoiler" not in flags):
                if (not label) and href.strip():
                    out.append(nodes.InlineSpoilerNode(parse_inline(href,flags=flags,state=state)))
                elif label and (not href.strip()):
                    out.append(nodes.InlineSpoilerNode(label))
                else:
                    out.append(nodes.InlineSpoilerNode(parse_inline(href,flags=flags,state=state),label))
            elif (hreftype.lower() == "deseret") and ("nodeseret" not in flags):
                out.append(nodes.DeseretNode(href))
            elif not cjk.cjk_handler(out, hreftype, href, label, flags):
                out.append(nodes.HrefNode(href,label,hreftype,width=gogo(width),height=gogo(height)))
        elif c=="]" and lev=="label":
            return out
        elif c=="[" and content[0]=="[" and (lev!="wikilink" or out2) and ("nowikilinks" not in flags):
            del content[0]
            x,y=_parse_inline(content,("wikilink",)+levs,flags=flags,state=state)
            out.append(nodes.HrefNode("".join(x),y,"wiki"))
        elif c=="|" and lev=="wikilink" and ("nowikilinks" not in flags):
            out2,out=out,[]
        elif c=="]" and content[0]=="]" and lev=="wikilink" and ("nowikilinks" not in flags):
            del content[0]
            if not out2:
                out2=out[:]
            return out2,out
        elif content[1:] and (c == content[1] == "/") and (content[0].lower() in "ur") and ("noredditrefs" not in flags):
            hark = c + content.pop(0) + content.pop(0)
            while content and re.compile("[A-Za-z_-]").match(content[0]):
                hark += content.pop(0)
            assert hark[0] == "/"
            out.append(nodes.HrefNode("https://reddit.com" + hark, [hark], "url"))
        ### Superscripts and Subscripts ###
        elif c=="^" and content[0]=="(" and (lev!="wikilink" or out2) and ("noredditstylesuper" not in flags):
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,("supred",)+levs,flags=flags,state=state)))
        elif c==")" and lev=="supred" and ("noredditstylesuper" not in flags):
            return out
        elif c=="(" and content[0]=="^" and (lev!="wikilink" or out2) and ("nopandocstyle" not in flags):
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,("suppan",)+levs,flags=flags,state=state)))
        elif c=="^" and content[0]==")" and lev=="suppan" and ("nopandocstyle" not in flags):
            del content[0]
            return out
        elif c=="(" and content[0]=="~" and (lev!="wikilink" or out2) and ("nopandocstyle" not in flags):
            del content[0]
            out.append(nodes.SubscrNode(_parse_inline(content,("sub",)+levs,flags=flags,state=state)))
        elif c=="~" and content[0]==")" and lev=="sub" and ("nopandocstyle" not in flags):
            del content[0]
            return out
        ### HZ escapes / codes / whatever (todo dedupe this repeated code) ###
        elif c=="~" and content[0]=="{" and (lev!="wikilink" or out2) and ("nohz" not in flags):
            del content[0]
            buf = []
            while content[1:] and (content[:2] != ["~", "}"]):
                buf.append(content.pop(0))
                buf.append(content.pop(0)) # again (only terminate on an *aligned* "~}").
            content = content[2:]
            # Could just use the HZ decoder but the extra EUC-region standard and PUA assignments in 18030
            obuf = []
            while buf:
                mine = buf.pop(0)
                if buf and (0x21 <= ord(mine) <= 0x7E):
                    mine = bytes([ord(mine) | 0x80, ord(buf.pop(0)) | 0x80]).decode("gb18030")
                obuf.append(mine)
            out.extend(obuf)
        elif c=="~" and "".join(content[:5])=="jis~{" and (lev!="wikilink" or out2) and ("nohz" not in flags):
            del content[:5]
            buf = []
            while content[1:] and (content[:2] != ["~", "}"]):
                buf.append(content.pop(0))
                buf.append(content.pop(0)) # again (only terminate on an *aligned* "~}").
            content = content[2:]
            obuf = []
            while buf:
                mine = buf.pop(0)
                if buf and (0x21 <= ord(mine) <= 0x7E):
                    mine = bytes([ord(mine) | 0x80, ord(buf.pop(0)) | 0x80]).decode("euc-jp")
                obuf.append(mine)
            out.extend(obuf)
        ### Emoticons and shortcodes ###
        elif emoji.emote_handler(out, c, content, levs, flags, state):
            pass
        ### Other ###
        elif c=="{" and (lev!="wikilink" or out2) and ("nodiacritic" not in flags):
            out.extend(_parse_inline(content,("bibuml",)+levs,flags=flags,state=state))
        else:
            lastchar=c
            out.append(c)
    return out

def cautious_replace(strn,frm,to):
    """Replace string provided not backslash-escaped."""
    def count_yen(s):
        n=0
        while s.endswith("\\"):
            n+=1
            s=s[:-1]
        return n
    lst=strn.split(frm)
    r=lst.pop(0)
    for i in lst:
        if (count_yen(r)%2): #Odd number of backslashes
            r+=frm+i
        else:
            r+=to+i
    return r

approaching_entity=[]
for _entity in list(htmlentitydefs.html5.keys()):
    while 1:
        _entity=_entity[:-1]
        if not _entity:
            break
        if _entity not in approaching_entity:
            approaching_entity.append(_entity)

def parse_inline(content, flags, state):
    return _parse_inline(list(content) + [""], flags=flags, state=state)
