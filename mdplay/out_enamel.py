import re
from xml.dom import minidom

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import nodes

from mdplay.out_html_dom import html_out_part, _html_out_part

from mdplay.enamelfacey import tonml

#import htmlentitydefs
from mdplay import htmlentitydefs_latest as htmlentitydefs
def _escape(text,html5=0):
    text=text.decode("utf-8")
    if not html5:
        keys=htmlentitydefs.name2codepoint.keys()
    else:
        keys=htmlentitydefs.html5.keys()
    for name in keys:
        if name not in ("lbrack","lt","rbrack","gt"): #handled already and would mess up syntax
            if not html5:
                codept=unichr(htmlentitydefs.name2codepoint[name])
            else:
                codept=htmlentitydefs.html5[name]
            if (len(codept)==1) and (ord(codept)<0xff) and (name not in htmlentitydefs.name2codepoint):
                continue #or face insanity.
            text=text.replace(codept,("["+name.rstrip(";")+"]").decode("ascii"))
    return text.encode("utf-8")

def nml_out(nodem,titl="",flags=()):
    if "fragment" in flags:
        return nml_out_body(nodem,flags)
    html5=("html5" in flags)
    mdi=minidom.getDOMImplementation() #minidom: other xml.dom imps don't necessarily support toxml
    document=mdi.createDocument("http://www.w3.org/1999/xhtml","html",mdi.createDocumentType("html","-//W3C//DTD XHTML 1.1//EN","http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd")) #never actually seen.
    head=document.createElement("head")
    document.documentElement.appendChild(head)
    body=document.createElement("body")
    document.documentElement.appendChild(body)
    #Head
    if titl:
        titlebar=document.createElement("title")
        head.appendChild(titlebar)
        titlebar.appendChild(document.createTextNode(titl.decode("utf-8")))
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
    #Body
    nodem=list(nodem)
    for domn in html_out_part(nodem,document,flags=flags):
        body.appendChild(domn)
    retval=_escape(tonml(document,encoding="utf-8"),html5)
    document.unlink()
    return retval

def nml_out_body(nodem,flags=()):
    html5=("html5" in flags)
    mdi=minidom.getDOMImplementation() #minidom: other xml.dom imps don't necessarily support ._get_attributes()
    document=mdi.createDocument("http://www.w3.org/1999/xhtml","html",mdi.createDocumentType("html","-//W3C//DTD XHTML 1.1//EN","http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd")) #never actually seen.
    ret=""
    nodem=list(nodem)
    for domn in html_out_part(nodem,document,flags=flags):
        ret+=tonml(domn,encoding="utf-8")
    document.unlink()
    return _escape(ret,html5)

__mdplay_renderer__="nml_out"
__mdplay_snippet_renderer__="nml_out_body"

