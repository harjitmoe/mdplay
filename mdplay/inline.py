# -*- mode: python; coding: utf-8 -*-
import re,string

from mdplay import nodes, umlaut
from mdplay.uriregex import uriregex
from mdplay import htmlentitydefs_latest as htmlentitydefs
from mdplay.eac import eac
from mdplay.pickups_util import SMILEYS
from mdplay.utfsupport import unichr4all
from mdplay.twem2support import TWEM2
from mdplay.cangjie import proc_cang
from mdplay.romkan import to_hiragana, to_katakana

#Note that :D may come out as several things depending on
#Python's arbitrary dict ordering; not sure what is best
#option here.
SMILEYA=dict(zip(SMILEYS.values(),SMILEYS.keys()))

def is_emotic(s):
    for i in SMILEYA.keys():
        if s.startswith(i):
            return i
    return False

del SMILEYS[SMILEYA[":/"]]
del SMILEYA[":/"] # https://

_eacd={"lenny":u"( ͡° ͜ʖ ͡° )","degdeg":u"( ͡° ͜ʖ ͡° )", "darkmoon":u"🌚","thefinger":u"🖕","ntr":u"🤘","blush":u"😳","wink":u"😉","happy":u"😊", "rolleyes":u"🙄","angry":u"😠","biggrin":u"😁","aw_yeah":u"😏","bigcry":u"😭","evil":u"👿", "twisted":u"😈","sasmile":u"😈","tongue":u"😝","sleep":u"😴","conf":u"😕","confused":u"😕", "eek":u"😲","cry":u"😢","sweat1":u"😅","worshippy":u"🙇","wub":u"😍","mellow":u"😐", "shifty":u"👀","eyes":u"👀","demonicduck":u"󽻍","shruggie":u"¯\_(ツ)_/¯"}
_eacdr=dict(zip(_eacd.values(),_eacd.keys()))
for _euc in eac.keys():
    _ec=u""
    for _eucs in _euc.split("-"):
        _ec+=unichr4all(int(_eucs,16))
    _eacd[eac[_euc]["alpha_code"].strip(":").encode("utf-8")]=_ec
    _eacdr[_ec]=eac[_euc]["alpha_code"].strip(":").encode("utf-8")
    for _alias in eac[_euc]["aliases"]:
        _eacd[_alias.strip(":")]=_ec

punct=string.punctuation+string.whitespace

def _group_surrogates(content):
    #Because Windows uses UTF-16, not UTF-32, that's why!
    while content:
        c=content.pop(0)
        if content and (0xD800<=ord(c.decode("utf-8"))<0xDC00) and (0xDC00<=ord(content[0].decode("utf-8"))<0xE000): 
            #UTF-16 surrogates (cat in UCS form, not UTF-8, to avoid CESU)
            c=c.decode("utf-8")+content.pop(0).decode("utf-8")
            c=c.encode("utf-8")
        yield c

def _parse_inline(content,levs=("root",),flags=()):
    # Note: the recursion works by the list being a Python
    # mutable, "passed by reference" as it were
    lastchar=" "
    if ("noverifyurl" not in flags):
        urireg="("+uriregex+"|/spoiler)"
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
    do_fuse=None
    dfstate=0
    while content:
        if dfstate==1:
            dfstate=2
        elif dfstate==2:
            do_fuse=None
            dfstate=0
        c=content.pop(0)
        isurl=re.match(uriregex,c+("".join(content))) #NOT urireg
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
        elif c=="&" and (len(content)>1) and ((content[0]+content[1]) in approaching_entity) and ("nohtmldeentity" not in flags):
            c=content[0]+content[1] #NOT +=
            n=2
            while c in approaching_entity:
                c+=content[n]
                n+=1
            if c in htmlentitydefs.html5.keys():
                out.append(htmlentitydefs.html5[c].encode("utf-8"))
                content=content[n:]
            elif (c[:-1] in htmlentitydefs.html5.keys()) and ("nohtmlsloppyentity" not in flags):
                n -= 1; c = c[:-1]
                out.append(htmlentitydefs.html5[c].encode("utf-8"))
                content=content[n:]
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
        elif c=="'" and "".join(content).startswith("''") and ("boldmw" not in levs) and (lev!="wikilink" or out2) and ("nowikiemph" not in flags):
            del content[0]
            del content[0] #yes, again
            out.append(nodes.BoldNode(_parse_inline(content,("boldmw",)+levs,flags=flags),emphatic=False))
        elif c=="'" and "".join(content).startswith("''") and lev=="boldmw" and ("nowikiemph" not in flags):
            del content[0]
            del content[0] #yes, again
            return out
        elif c=="'" and content[0]=="'" and ("italicmw" not in levs) and (lev!="wikilink" or out2) and ("nowikiemph" not in flags):
            del content[0]
            out.append(nodes.ItalicNode(_parse_inline(content,("italicmw",)+levs,flags=flags),emphatic=False))
        elif c=="'" and content[0]=="'" and lev=="italicmw" and ("nowikiemph" not in flags):
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
                hreftype="url"
            else:
                hreftype=hreftype[1:] #Minus the leading !
            width = height = ""
            def gogo(s):
                if not s: return None
                return int(s, 10)
            if (hreftype=="img") and (" =" in href):
                href, size = href.split(" =",1)
                width, height = size.split("x")
            if (href == "/spoiler") and (hreftype == "url") and ("noredditspoiler" not in flags):
                out.append(nodes.InlineSpoilerNode(label))
            elif (hreftype.lower() == "spoiler") and ("noembedspoiler" not in flags):
                if (not label) and (href.strip()):
                    out.append(nodes.InlineSpoilerNode(list(href)))
                else:
                    out.append(nodes.InlineSpoilerNode(label))
            elif (hreftype.lower() in ("cang","cang3")) and ("nocangjie" not in flags):
                kanji = proc_cang(href, 3)
                #print `kanji`, `label`
                if label and ("norubi" not in flags):
                    out.append(nodes.RubiNode(kanji, label))
                else:
                    out.append(kanji)
            elif (hreftype.lower() == "cang5") and ("nocangjie" not in flags):
                kanji = proc_cang(href, 5)
                if label and ("norubi" not in flags):
                    out.append(nodes.RubiNode(kanji, label))
                else:
                    out.append(kanji)
            elif (hreftype.lower() in ("kana","kkana","katakana")) and ("noromkan" not in flags):
                kana = to_katakana(href)
                if label and ("norubi" not in flags):
                    out.append(nodes.RubiNode(kana, label))
                else:
                    out.append(kana)
            elif (hreftype.lower() in ("hkana","hgana","hiragana")) and ("noromkan" not in flags):
                kana = to_hiragana(href)
                if label and ("norubi" not in flags):
                    out.append(nodes.RubiNode(kana, label))
                else:
                    out.append(kana)
            elif (hreftype.lower() in ("rubi","ruby","furi")) and ("norubi" not in flags):
                out.append(nodes.RubiNode(href, label))
            else:
                out.append(nodes.HrefNode(href,label,hreftype,width=gogo(width),height=gogo(height)))
        elif c=="]" and lev=="label":
            return out
        elif c=="[" and content[0]=="[" and (lev!="wikilink" or out2) and ("nowikilinks" not in flags):
            del content[0]
            x,y=_parse_inline(content,("wikilink",)+levs,flags=flags)
            out.append(nodes.HrefNode("".join(x),y,"wiki"))
        elif c=="|" and lev=="wikilink" and ("nowikilinks" not in flags):
            out2,out=out,[]
        elif c=="]" and content[0]=="]" and lev=="wikilink" and ("nowikilinks" not in flags):
            del content[0]
            if not out2:
                out2=out[:]
            return out2,out
        ### Superscripts and Subscripts ###
        elif c=="^" and content[0]=="(" and (lev!="wikilink" or out2) and ("noredditstylesuper" not in flags):
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,("supred",)+levs,flags=flags)))
        elif c==")" and lev=="supred" and ("noredditstylesuper" not in flags):
            return out
        elif c=="(" and content[0]=="^" and (lev!="wikilink" or out2) and ("nopandocstyle" not in flags):
            del content[0]
            out.append(nodes.SuperNode(_parse_inline(content,("suppan",)+levs,flags=flags)))
        elif c=="^" and content[0]==")" and lev=="suppan" and ("nopandocstyle" not in flags):
            del content[0]
            return out
        elif c=="(" and content[0]=="~" and (lev!="wikilink" or out2) and ("nopandocstyle" not in flags):
            del content[0]
            out.append(nodes.SubscrNode(_parse_inline(content,("sub",)+levs,flags=flags)))
        elif c=="~" and content[0]==")" and lev=="sub" and ("nopandocstyle" not in flags):
            del content[0]
            return out
        ### Badass echoes ###
        #elif c=="^" and content[:2]=="((" and (lev!="wikilink" or out2) and ("nobadass" not in flags):
        #    del content[0]
        #    out.append(nodes.BadassEchoNode(_parse_inline(content,("badass",)+levs,flags=flags)))
        #elif c==")" and content[:2]=="))" and lev=="badass" and ("nobadass" not in flags):
        #    return out
        ### Emoticons and Emoji ###
        elif re.match(r":(\w|_|-)+:",c+("".join(content))) and ("noshortcodeemoji" not in flags):
            kwontenti=""
            c=content.pop(0)
            while (c!=":"):
                kwontenti+=c
                c=content.pop(0)
            kwontent=kwontenti
            if kwontent.startswith("icon_"): #Is this one always okay?
                kwontent=kwontent[5:]
            elif kwontent.startswith("eusa_"):
                kwontent=kwontent[5:]
            elif kwontent.startswith("dan_"):
                kwontent=kwontent[4:] 
            if kwontent in _eacd: 
                emoji=_eacd[kwontent.decode("utf-8")]
                if emoji in SMILEYS:
                    emote=SMILEYS[emoji]
                else:
                    emote=":"+kwontenti+":"
                nodo=nodes.EmojiNode(emoji.encode("utf-8"), (emote, kwontenti), "shortcode")
                out.append(nodo)
                if do_fuse!=None and ((do_fuse.content.decode("utf-8"), nodo.content.decode("utf-8")) in TWEM2):
                    do_fuse.fuse=nodo
                    do_fuse=None
                do_fuse=nodo
                dfstate=1
            else:
                out.append(":"+kwontenti+":")
        elif is_emotic(c+("".join(content))) and ("noasciiemoticon" not in flags):
            emote=is_emotic(c+("".join(content)))
            for iii in range(len(emote)-1): #Already popped the first (to c)!
                content.pop(0)
            emoji=SMILEYA[emote].encode("utf-8")
            shortcode=None
            if emoji in _eacdr:
                shortcode=_eacdr[emoji]
            nodo=nodes.EmojiNode(emoji, (emote, shortcode), "ascii")
            out.append(nodo) 
            if do_fuse!=None and ((do_fuse.content.decode("utf-8"), nodo.content.decode("utf-8")) in TWEM2):
                do_fuse.fuse=nodo
                do_fuse=None
            do_fuse=nodo
            dfstate=1
        #
        elif c=="{" and (lev!="wikilink" or out2) and ("nodiacritic" not in flags):
            out.extend(_parse_inline(content,("bibuml",)+levs,flags=flags))
        elif (((c.decode("utf-8"),) in TWEM2) or (c.decode("utf-8")==u"\U000FDECD")) and ("label" not in levs):
            emoji=c.decode("utf-8")
            if emoji in _eacdr:
                shortcode=_eacdr[emoji]
            else:
                shortcode=None
            emote=":unnamed:"
            if emoji in SMILEYS:
                emote=SMILEYS[emoji]
            elif shortcode:
                emote=":"+shortcode+":"
            nodo=nodes.EmojiNode(c, (emote, shortcode), "verbatim")
            out.append(nodo) 
            if do_fuse!=None and ((do_fuse.content.decode("utf-8"), nodo.content.decode("utf-8")) in TWEM2):
                do_fuse.fuse=nodo
                do_fuse=None
            do_fuse=nodo
            dfstate=1
        else:
            lastchar=c
            out.append(c)
    return out

def cautious_replace(strn,frm,to):
    """Replace string provided not backslash-escaped."""
    def count_yen(s):
        n=0
        while s.endswith(u"\\"):
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
for _entity in htmlentitydefs.html5.keys():
    while 1:
        _entity=_entity[:-1]
        if not _entity:
            break
        if _entity not in approaching_entity:
            approaching_entity.append(_entity)

def parse_inline(content,flags=()):
    d=content.decode("utf-8")
    return _parse_inline(list(_group_surrogates([i.encode("utf-8") for i in list(d)]+[""])),flags=flags)
