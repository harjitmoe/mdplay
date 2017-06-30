import re
from xml.dom import minidom

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import nodes, mdputil

def _newElementWithEndTag(document,tagname):
    """Create an element containing an empty text node."""
    r = document.createElement(tagname)
    r.appendChild(document.createTextNode(""))
    return r

def html_out_part(nodem,document,in_list=(),flags=()):
    return list(_html_out_part(nodem,document,in_list,flags=flags))

def _html_out_part(nodem,document,in_list=(),flags=()):
    while nodem:
        node=nodem.pop(0)
        if isinstance(node,nodes.UlliNode):
            if (node.depth+1)>len(in_list):
                r=_newElementWithEndTag(document,"ul")
                r2=_newElementWithEndTag(document,"li")
                r.appendChild(r2)
                for domn in html_out_part(node.content,document,flags=flags):
                    r2.appendChild(domn)
                for domn in html_out_part(nodem,document,("ul",)+in_list):
                    if domn.tagName not in ("ul","ol"):
                        r.appendChild(domn)
                    elif not len(r2.childNodes):
                        r3=_newElementWithEndTag(document,"li")
                        r.appendChild(r3)
                        r3.appendChild(domn)
                    else:
                        r.lastChild.appendChild(domn)
                yield r
            elif ((node.depth+1)<len(in_list)) or (in_list[0]=="ol"):
                nodem.insert(0,node)
                return
            else:
                r=_newElementWithEndTag(document,"li")
                for domn in html_out_part(node.content,document,flags=flags):
                    r.appendChild(domn)
                yield r
        elif isinstance(node,nodes.OlliNode):
            if (node.depth+1)>len(in_list):
                r=_newElementWithEndTag(document,"ol")
                r2=_newElementWithEndTag(document,"li")
                if ("autonumberonly" not in flags):
                    r2.setAttribute("value",str(node.bullet))
                r.appendChild(r2)
                for domn in html_out_part(node.content,document,flags=flags):
                    r2.appendChild(domn)
                for domn in html_out_part(nodem,document,("ol",)+in_list):
                    if domn.tagName not in ("ul","ol"):
                        r.appendChild(domn)
                    elif not len(r2.childNodes):
                        r3=_newElementWithEndTag(document,"li")
                        r.appendChild(r3)
                        r3.appendChild(domn)
                    else:
                        r.lastChild.appendChild(domn)
                yield r
            elif ((node.depth+1)<len(in_list)) or (in_list[0]=="ul"):
                nodem.insert(0,node)
                return
            else:
                r=_newElementWithEndTag(document,"li")
                if ("autonumberonly" not in flags):
                    r.setAttribute("value",str(node.bullet))
                for domn in html_out_part(node.content,document,flags=flags):
                    r.appendChild(domn)
                yield r
        elif in_list: #A non-list node at list-stack level
            nodem.insert(0,node)
            return
        elif not isinstance(node,nodes.Node): #i.e. is a string
            yield document.createTextNode(node.decode("utf-8").replace(u"\x20\x20",u"\xa0\x20"))
        elif isinstance(node,nodes.EmojiNode):
            if ("notwemoji" not in flags) and node.emphatic:
                hexcode=node.label[2]
                if "nounicodeemoji" not in flags:
                    altcode=node.content.decode("utf-8")
                else:
                    altcode=node.label[0] or node.label[1] or ":"+hexcode+":"
                r=document.createElement("img")
                r.setAttribute("src","https://twemoji.maxcdn.com/2/72x72/%s.png"%hexcode)
                r.setAttribute("alt",altcode)
                r.setAttribute("style","max-width:2em;max-height:2em;")
                # Acceptable attribution per https://github.com/twitter/twemoji/blob/b33c30e78db45be787410567ad6f4c7b56c137a0/README.md#attribution-requirements
                yield document.createComment(" twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/ ")
                yield r
            else:
                if "nounicodeemoji" not in flags:
                    yield document.createTextNode(node.content.decode("utf-8"))
                else:
                    yield document.createTextNode(node.label[0] or node.label[1] or ":"+node.label[2]+":")
        elif isinstance(node,nodes.TitleNode):
            if node.depth>6: node.depth=6
            r=_newElementWithEndTag(document,"h%d"%node.depth)
            for domn in html_out_part(node.content,document,flags=flags):
                r.appendChild(domn)
            yield r
        elif isinstance(node,nodes.ParagraphNode):
            r=_newElementWithEndTag(document,"p")
            for domn in html_out_part(node.content,document,flags=flags):
                r.appendChild(domn)
            yield r
        elif isinstance(node,nodes.BlockQuoteNode):
            r=_newElementWithEndTag(document,"blockquote")
            for domn in html_out_part(node.content,document,flags=flags):
                r.appendChild(domn)
            yield r
        elif isinstance(node,nodes.SpoilerNode):
            if "ipsspoilers" in flags:
                if node.label:
                    splabel=_newElementWithEndTag(document,"div")
                    for domn in html_out_part(node.label,document,flags=flags):
                        splabel.appendChild(domn)
                    yield splabel
                metar=_newElementWithEndTag(document,"blockquote")
                metar.setAttribute("class",'ipsStyle_spoiler')
                metar.setAttribute("data-ipsspoiler",'')
                metar.setAttribute("tabindex",'0')
                r=_newElementWithEndTag(document,"div")
                metar.appendChild(r)
                r.setAttribute("class",'ipsSpoiler_header')
                r2=_newElementWithEndTag(document,"span")
                r.appendChild(r2)
                # Spoiler-block header text will be overriden.
                r2.appendChild(document.createTextNode("Spoiler"))
                r3=_newElementWithEndTag(document,"div")
                metar.appendChild(r3)
                r3.setAttribute("class",'ipsSpoiler_contents')
                for domn in html_out_part(node.content,document,flags=flags):
                    r3.appendChild(domn)
                yield metar
            else:
                metar=_newElementWithEndTag(document,"div")
                metar.setAttribute("class",'spoilerwrapper')
                r=_newElementWithEndTag(document,"p")
                metar.appendChild(r)
                r2=_newElementWithEndTag(document,"a")
                r.appendChild(r2)
                r2.setAttribute("href",'javascript:void(0);')
                r2.setAttribute("onclick","document.getElementById('spoil%d').style.display=(document.getElementById('spoil%d').style.display=='none')?('block'):('none')"%(mdputil.newid(node),mdputil.newid(node)))
                if not node.label:
                    r2.appendChild(document.createTextNode("Expand/Hide Spoiler"))
                else:
                    for domn in html_out_part(node.label,document,flags=flags):
                        r2.appendChild(domn)
                r3=_newElementWithEndTag(document,"div")
                metar.appendChild(r3)
                r3.setAttribute("class",'spoiler')
                r3.setAttribute("id",'spoil%d'%mdputil.newid(node))
                r3.setAttribute("style",'display:none;')
                for domn in html_out_part(node.content,document,flags=flags):
                    r3.appendChild(domn)
                yield metar
        elif isinstance(node,nodes.CodeBlockNode):
            r=_newElementWithEndTag(document,"pre")
            r.appendChild(document.createTextNode("".join(node.content).decode("utf-8")))
            yield r
        elif isinstance(node,nodes.CodeSpanNode):
            r=_newElementWithEndTag(document,"code")
            r.appendChild(document.createTextNode("".join(node.content).decode("utf-8")))
            yield r
        elif isinstance(node,nodes.BoldNode):
            if node.emphatic:
                r=_newElementWithEndTag(document,"strong")
            else:
                r=_newElementWithEndTag(document,"b")
            for domn in html_out_part(node.content,document,flags=flags):
                r.appendChild(domn)
            yield r
        elif isinstance(node,nodes.UnderlineNode):
            r=_newElementWithEndTag(document,"u")
            for domn in html_out_part(node.content,document,flags=flags):
                r.appendChild(domn)
            yield r
        elif isinstance(node,nodes.ItalicNode):
            if node.emphatic:
                r=_newElementWithEndTag(document,"em")
            else:
                r=_newElementWithEndTag(document,"i")
            for domn in html_out_part(node.content,document,flags=flags):
                r.appendChild(domn)
            yield r
        elif isinstance(node,nodes.SuperNode):
            r=_newElementWithEndTag(document,"sup")
            for domn in html_out_part(node.content,document,flags=flags):
                r.appendChild(domn)
            yield r
        elif isinstance(node,nodes.SubscrNode):
            r=_newElementWithEndTag(document,"sub")
            for domn in html_out_part(node.content,document,flags=flags):
                r.appendChild(domn)
            yield r
        elif isinstance(node,nodes.RubiNode):
            content=node.content
            r=_newElementWithEndTag(document,"ruby")
            #r.setAttribute("lang","jp")
            r.appendChild(document.createTextNode(content.decode("utf-8")))
            rp1=_newElementWithEndTag(document,"rp")
            rp1.appendChild(document.createTextNode(" ("))
            r.appendChild(rp1)
            rt=_newElementWithEndTag(document,"rt")
            for domn in html_out_part(node.label,document):
                rt.appendChild(domn)
            r.appendChild(rt)
            rp2=_newElementWithEndTag(document,"rp")
            rp2.appendChild(document.createTextNode(") "))
            r.appendChild(rp2)
            yield r
        elif isinstance(node,nodes.HrefNode):
            ht=node.hreftype
            content=node.content
            if ht=="url":
                label=html_out_part(node.label,document)
                if ("showtropes" in flags) and re.match("https?://(www\.)?tvtropes.org",content):
                    metar=_newElementWithEndTag(document,"span")
                    r=_newElementWithEndTag(document,"u")
                    metar.appendChild(r)
                    for domn in label:
                        r.appendChild(domn)
                    r2=_newElementWithEndTag(document,"sup")
                    metar.appendChild(r2)
                    r3=_newElementWithEndTag(document,"a")
                    r2.appendChild(r3)
                    r3.setAttribute("href",content.decode("utf-8"))
                    r3.appendChild(document.createTextNode("(TVTropes)"))
                    yield metar
                    continue
                r=_newElementWithEndTag(document,"a")
                r.setAttribute("href",content.decode("utf-8"))
                for domn in label:
                    r.appendChild(domn)
                yield r
            elif "script" in "".join(ht.split()):
                pass #No way, Jos{\'e}!
            else: #Including img
                try:
                    label="".join(node.label)
                except TypeError:
                    label=html_out_body(node.label) #_body, not _part
                r=document.createElement(ht)
                r.setAttribute("src",content.decode("utf-8"))
                if label:
                    r.setAttribute("alt",label.decode("utf-8"))
                styl=""
                if node.width:
                    styl+="width:%dpx;"%node.width
                if node.height:
                    styl+="height:%dpx;"%node.height
                if styl:
                    r.setAttribute("style",styl)
                if "//twemoji.maxcdn.com" in content:
                    # Acceptable attribution per https://github.com/twitter/twemoji/blob/b33c30e78db45be787410567ad6f4c7b56c137a0/README.md#attribution-requirements
                    yield document.createComment(" twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/ ")
                yield r
        elif isinstance(node,nodes.NewlineNode):
            r=document.createElement("br")
            yield r
        elif isinstance(node,nodes.RuleNode):
            r=document.createElement("hr")
            yield r
        elif isinstance(node,nodes.DirectiveNode) and node.type.startswith("html-") and ("insecuredirective" in flags):
            r = _newElementWithEndTag(document,node.type[len("html-"):].strip())
            for i,j in node.opts:
                r.setAttribute(i, j)
            for i in node.args:
                if i.strip():
                    r.setAttribute(i, i)
            for domn in html_out_part(node.content,document):
                r.appendChild(domn)
            yield r
        elif isinstance(node,nodes.TableNode):
            r=_newElementWithEndTag(document,"table")
            r.setAttribute("border","1")
            thead=_newElementWithEndTag(document,"thead")
            r.appendChild(thead)
            for row in node.table_head:
                tr=_newElementWithEndTag(document,"tr")
                thead.appendChild(tr)
                for colno,cell in enumerate(row):
                    th=_newElementWithEndTag(document,"th")
                    tr.appendChild(th)
                    if node.aligns and (len(node.aligns)>colno) and node.aligns[colno]:
                        th.setAttribute("style","text-align:"+node.aligns[colno])
                    for domn in html_out_part(list(cell),document):
                        th.appendChild(domn)
            tbody=_newElementWithEndTag(document,"tbody")
            r.appendChild(tbody)
            for row in node.table_body:
                tr=_newElementWithEndTag(document,"tr")
                tbody.appendChild(tr)
                for colno,cell in enumerate(row):
                    td=_newElementWithEndTag(document,"td")
                    tr.appendChild(td)
                    if node.aligns and (len(node.aligns)>colno) and node.aligns[colno]:
                        td.setAttribute("style","text-align:"+node.aligns[colno])
                    for domn in html_out_part(list(cell),document):
                        td.appendChild(domn)
            yield r
        elif isinstance(node,nodes.EmptyInterrupterNode):
            yield document.createTextNode("")
        else:
            yield document.createTextNode("ERROR"+repr(node))

#import htmlentitydefs
from mdplay import htmlentitydefs_latest as htmlentitydefs
def _escape(text,html5=0):
    text=text.decode("utf-8")
    if not html5:
        keys=htmlentitydefs.name2codepoint.keys()
    else:
        keys=htmlentitydefs.html5.keys()
    for name in keys:
        if name not in ("amp","lt","quot","gt"): #handled already by minidom and would mess up syntax
            if not html5:
                codept=unichr(htmlentitydefs.name2codepoint[name])
            else:
                codept=htmlentitydefs.html5[name]
            if (len(codept)==1) and (ord(codept)<0xff) and (name not in htmlentitydefs.name2codepoint):
                continue #or face insanity.
            text=text.replace(codept,("&"+name.rstrip(";")+";").decode("ascii"))
    return text.encode("utf-8")

def html_out(nodem,titl="",flags=()):
    if "fragment" in flags:
        return html_out_body(nodem,flags)
    html5=("html5" in flags)
    mdi=minidom.getDOMImplementation() #minidom: other xml.dom imps don't necessarily support toxml
    if not html5:
        document=mdi.createDocument("http://www.w3.org/1999/xhtml","html",mdi.createDocumentType("html","-//W3C//DTD XHTML 1.1//EN","http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"))
    else:
        document=mdi.createDocument("http://www.w3.org/1999/xhtml","html",mdi.createDocumentType("html",None,"about:legacy-compat"))
    document.documentElement.setAttribute("xmlns","http://www.w3.org/1999/xhtml") #ehem... minidom... ehem...
    head=document.createElement("head")
    document.documentElement.appendChild(head)
    body=document.createElement("body")
    document.documentElement.appendChild(body)
    #Head
    charset=document.createElement("meta")
    head.appendChild(charset)
    if not html5:
        charset.setAttribute("http-equiv","Content-Type")
        charset.setAttribute("content","text/html; charset=UTF-8")
    else:
        charset.setAttribute("charset","UTF-8")
        xua=document.createElement("meta")
        head.appendChild(xua)
        xua.setAttribute("http-equiv","X-UA-Compatible")
        xua.setAttribute("content","IE=10,chrome=1")
    if titl:
        titlebar=document.createElement("title")
        head.appendChild(titlebar)
        titlebar.appendChild(document.createTextNode(titl.decode("utf-8")))
    #Body
    nodem=list(nodem)
    for domn in html_out_part(nodem,document,flags=flags):
        body.appendChild(domn)
    retval=_escape(document.toxml("utf-8"),html5)
    document.unlink()
    return retval

def html_out_body(nodem,flags=()):
    html5=("html5" in flags)
    mdi=minidom.getDOMImplementation() #minidom: other xml.dom imps don't necessarily support toxml
    document=mdi.createDocument("http://www.w3.org/1999/xhtml","html",mdi.createDocumentType("html","-//W3C//DTD XHTML 1.1//EN","http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd")) #never actually seen.
    ret=""
    nodem=list(nodem)
    for domn in html_out_part(nodem,document,flags=flags):
        ret+=domn.toxml("utf-8")
    document.unlink()
    return _escape(ret,html5)

__mdplay_renderer__="html_out"
__mdplay_snippet_renderer__="html_out_body"

