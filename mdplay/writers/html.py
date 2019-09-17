__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import nodes, mdputil, deseret
from mdplay.writers._writehtml import tohtml

import re
from xml.dom import minidom

def _createScriptTag(content, document):
    se = document.createElement("script")
    se.setAttribute("type", "text/javascript")
    script = document.createCDATASection(content)
    se.appendChild(script)
    return se

def _shim_ht5_element(tag, document):
    # Somethimes improves vintage MSIE support
    return _createScriptTag("document.createElement(%r);" % tag, document)

def html_out_part(nodem, document, in_list=(), flags=(), mode="xhtml"):
    return list(_html_out_part(nodem, document, in_list, flags=flags, mode=mode))

def _html_out_part(nodem, document, in_list=(), flags=(), mode="xhtml"):
    is_xhtml2 = mode in ("xhtml2", "xhtml2nml")
    while nodem:
        node = nodem.pop(0)
        if isinstance(node, nodes.UlliNode):
            if (node.depth+1)>len(in_list):
                r = document.createElement("ul")
                r2 = document.createElement("li")
                r.appendChild(r2)
                for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                    r2.appendChild(domn)
                for domn in html_out_part(nodem, document, ("ul",) + in_list, flags=flags, mode=mode):
                    if domn.tagName not in ("ul","ol"):
                        r.appendChild(domn)
                    elif not len(r2.childNodes):
                        r3 = document.createElement("li")
                        r.appendChild(r3)
                        r3.appendChild(domn)
                    else:
                        r.lastChild.appendChild(domn)
                yield r
            elif ((node.depth + 1) < len(in_list)) or (in_list[0] == "ol"):
                nodem.insert(0, node)
                return
            else:
                r=document.createElement("li")
                for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                    r.appendChild(domn)
                yield r
        elif isinstance(node, nodes.OlliNode):
            if (node.depth + 1) > len(in_list):
                r=document.createElement("ol")
                r2=document.createElement("li")
                if "autonumberonly" not in flags:
                    r2.setAttribute("value", str(node.bullet))
                r.appendChild(r2)
                for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                    r2.appendChild(domn)
                for domn in html_out_part(nodem, document, ("ol",) + in_list, flags=flags, mode=mode):
                    if domn.tagName not in ("ul", "ol"):
                        r.appendChild(domn)
                    elif not len(r2.childNodes):
                        r3 = document.createElement("li")
                        r.appendChild(r3)
                        r3.appendChild(domn)
                    else:
                        r.lastChild.appendChild(domn)
                yield r
            elif ((node.depth + 1) < len(in_list)) or (in_list[0] == "ul"):
                nodem.insert(0, node)
                return
            else:
                r = document.createElement("li")
                if ("autonumberonly" not in flags):
                    r.setAttribute("value", str(node.bullet))
                for domn in html_out_part(node.content, document, flags=flags):
                    r.appendChild(domn)
                yield r
        elif in_list: #A non-list node at list-stack level
            nodem.insert(0, node)
            return
        elif not isinstance(node, nodes.Node): #i.e. is a string
            yield document.createTextNode(node.replace("\x20\x20","\xa0\x20"))
        elif isinstance(node, nodes.EmojiNode):
            if ("notwemoji" not in flags) and node.emphatic:
                hexcode = node.label[2]
                if "nounicodeemoji" not in flags:
                    altcode = node.content
                else:
                    altcode = node.label[0] or node.label[1] or ":"+hexcode+":"
                r=document.createElement("img")
                r.setAttribute("src", "https://twemoji.maxcdn.com/2/72x72/%s.png" % hexcode)
                r.setAttribute("style", "max-width:2em;max-height:2em;")
                # https://github.com/twitter/twemoji/blob/b33c30e78db45be787410567ad6f4c7b56c137a0/README.md#attribution-requirements
                r.setAttribute("title", "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/")
                if not is_xhtml2:
                    r.setAttribute("alt", altcode)
                else:
                    # XHTML2 regularises the asset-alt relation, asset in src=, alt as children.
                    r.appendChild(document.createTextNode(altcode))
                yield r
            else:
                if "nounicodeemoji" not in flags:
                    yield document.createTextNode(node.content)
                else:
                    yield document.createTextNode(node.label[0] or node.label[1] or ":"+node.label[2]+":")
        elif isinstance(node, nodes.TitleNode):
            if node.depth > 6:
                node.depth = 6
            # TODO leverage XHTML2 <h> element (strictly in the respective mode only).
            r = document.createElement("h%d" % node.depth)
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.ParagraphNode):
            r = document.createElement("p")
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.BlockQuoteNode):
            r = document.createElement("blockquote")
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.SpoilerNode):
            if "ipsspoilers" in flags:
                if node.label:
                    splabel = document.createElement("div")
                    for domn in html_out_part(node.label, document, flags=flags, mode=mode):
                        splabel.appendChild(domn)
                    yield splabel
                metar=document.createElement("blockquote")
                metar.setAttribute("class", 'ipsStyle_spoiler')
                metar.setAttribute("data-ipsspoiler", '')
                metar.setAttribute("tabindex", '0')
                r=document.createElement("div")
                metar.appendChild(r)
                r.setAttribute("class", 'ipsSpoiler_header')
                r2=document.createElement("span")
                r.appendChild(r2)
                # Spoiler-block header text will be overriden.
                r2.appendChild(document.createTextNode("Spoiler"))
                r3=document.createElement("div")
                metar.appendChild(r3)
                r3.setAttribute("class", 'ipsSpoiler_contents')
                for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                    r3.appendChild(domn)
                yield metar
            else:
                # Set up wrapper and title/toggle, define event handler as appropriate
                handler_script = "document.getElementById('spoil%d').style.display = (document.getElementById('spoil%d').style.display=='none')?('block'):('none');" % (mdputil.newid(node), mdputil.newid(node))
                if "html5" not in flags:
                    metar = document.createElement("div")
                    metar.setAttribute("class", 'spoilerwrapper')
                    r2 = document.createElement("p")
                    metar.appendChild(r2)
                    r = document.createElement("a")
                    r2.appendChild(r)
                    r.setAttribute("href", "javascript:void(0)")
                else:
                    handler_script = "if (!window.HTMLDetailsElement) { %s }" % (handler_script)
                    if is_xhtml2:
                        metar = document.createElement("html:details")
                        r = document.createElement("html:summary")
                    else:
                        yield _shim_ht5_element("details", document)
                        yield _shim_ht5_element("summary", document)
                        metar = document.createElement("details")
                        r = document.createElement("summary")
                    metar.appendChild(r)
                    metar.setAttribute("class", 'spoilerwrapper')
                    metar.setAttribute("style", 'display: block;')
                    r.setAttribute("style", 'display: block; color: blue; cursor: pointer; text-decoration: underline;')
                    r.setAttribute("tabindex", '0') #i.e. focusable but in source order.
                # Add text to title/toggle
                if not node.label:
                    r.appendChild(document.createTextNode("Expand/Hide Spoiler"))
                else:
                    for domn in html_out_part(node.label, document, flags=flags, mode=mode):
                        r.appendChild(domn)
                # Install event handler
                if not is_xhtml2:
                    r.setAttribute("onclick", handler_script)
                    keyhandle = "if ((event.keyCode || event.which) == 13 || (event.keyCode || event.which) == 32) { %s }"
                    # Pressing Return on an <a> tag seems to activate onclick (understandably) and they cancel out.
                    # This in spite of onkeypress being present, which you'd have thought would disable that.
                    # This does not occur in the html5 instance, possibly becouse it only occurs for <a> elements?
                    # Tested so far on Seamonkey (modern) and on Firefox 2.0 (vintage).
                    if "html5" in flags:
                        r.setAttribute("onkeypress", keyhandle % handler_script)
                else:
                    r.setAttribute("href", "javascript:void(0);")
                    r.setAttribute("id", 'observerspoil%d' % mdputil.newid(node))
                    handler = _createScriptTag(handler_script, document)
                    handler.setAttribute("type", "text/javascript")
                    handler.setAttribute("ev:event", "DOMActivate")
                    handler.setAttribute("ev:observer", '#observerspoil%d' % mdputil.newid(node))
                    handler.setAttribute("ev:defaultAction", "cancel")
                    metar.appendChild(handler)
                # Add spoiler content
                r3 = document.createElement("div")
                metar.appendChild(r3)
                r3.setAttribute("class", 'spoiler')
                r3.setAttribute("id", 'spoil%d' % mdputil.newid(node))
                r3.setAttribute("style", 'border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;')
                for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                    r3.appendChild(domn)
                # Hde spoiler content if and only if browser doesn't support details element or it's not used
                if "html5" in flags:
                    r4 = _createScriptTag("if (!window.HTMLDetailsElement) { document.getElementById('spoil%d').style.display = 'none'; } else{ document.getElementById('spoil%d').parentNode.firstChild.style.display = null; }" % (mdputil.newid(node), mdputil.newid(node)), document)
                else:
                    r4 = _createScriptTag("document.getElementById('spoil%d').style.display = 'none';" % mdputil.newid(node), document)
                metar.appendChild(r4)
                yield metar
        elif isinstance(node, nodes.CodeBlockNode):
            r = document.createElement("pre" if not is_xhtml2 else "blockcode")
            r.appendChild(document.createTextNode("".join(node.content)))
            yield r
        elif isinstance(node, nodes.CodeSpanNode):
            r = document.createElement("code")
            r.appendChild(document.createTextNode("".join(node.content)))
            yield r
        elif isinstance(node,nodes.BoldNode):
            if node.emphatic:
                r = document.createElement("strong")
            elif not is_xhtml2:
                r = document.createElement("b")
            elif "html5" in flags:
                r = document.createElement("html:b")
            else:
                r = document.createElement("strong")
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.UnderlineNode):
            if not is_xhtml2:
                r = document.createElement("u")
            elif "html5" in flags:
                r = document.createElement("html:u")
            else:
                r = document.createElement("span")
                r.setAttribute("style", "text-decoration: underline;")
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.ItalicNode):
            if node.emphatic:
                r = document.createElement("em")
            elif not is_xhtml2:
                r = document.createElement("i")
            elif "html5" in flags:
                r = document.createElement("html:i")
            else:
                r = document.createElement("em")
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.StrikeNode):
            if node.emphatic:
                r = document.createElement("del")
            elif not is_xhtml2:
                r = document.createElement("s")
            elif "html5" in flags:
                r = document.createElement("html:s")
            else:
                r = document.createElement("del")
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.SuperNode):
            r = document.createElement("sup") # Thankfully never earmarked, even in XHTML2.
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.SubscrNode):
            r = document.createElement("sub") # Thankfully never earmarked, even in XHTML2.
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.RubiNode):
            content = node.content
            r = document.createElement("ruby")
            #r.setAttribute("lang","jp")
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            #r.appendChild(document.createTextNode(content))
            rp1 = document.createElement("rp")
            rp1.appendChild(document.createTextNode(" ("))
            r.appendChild(rp1)
            rt = document.createElement("rt")
            for domn in html_out_part(node.label, document, flags=flags, mode=mode):
                rt.appendChild(domn)
            r.appendChild(rt)
            rp2 = document.createElement("rp")
            rp2.appendChild(document.createTextNode(") "))
            r.appendChild(rp2)
            yield r
        elif isinstance(node, nodes.HrefNode):
            ht = node.hreftype
            content = node.content
            if ht == "url":
                label = html_out_part(node.label, document, flags=flags, mode=mode)
                if ("showtropes" in flags) and re.match("https?://(www\.)?tvtropes.org", content):
                    metar = document.createElement("span")
                    r = document.createElement("span")
                    r.setAttribute("style", "text-decoration: underline;")
                    metar.appendChild(r)
                    for domn in label:
                        r.appendChild(domn)
                    r2 = document.createElement("sup")
                    metar.appendChild(r2)
                    if not is_xhtml2:
                        r3 = document.createElement("a")
                        r2.appendChild(r3)
                    else:
                        # XHTML2: not only can anything be an anchor, anything can be a hyperlink
                        r3 = r2
                    r3.setAttribute("href", content)
                    r3.appendChild(document.createTextNode("(TVTropes)"))
                    yield metar
                    continue
                r = document.createElement("a")
                r.setAttribute("href", content)
                for domn in label:
                    r.appendChild(domn)
                yield r
            elif "script" in "".join(ht.split()):
                pass #No way, Jos{\'e}!
            else: #Including img
                r = document.createElement(ht)
                r.setAttribute("src", content)
                # Note: there seems to be some confusion here about just what the format of node.label
                # can be expected to be, could we clarify?
                if not is_xhtml2:
                    try:
                        label = "".join(node.label)
                    except TypeError:
                        label = html_out_body(node.label, flags=flags, mode=mode) # _body, not _part
                    if label:
                        r.setAttribute("alt", label)
                else:
                    try:
                        label = [document.createTextNode(("".join(node.label)))]
                    except TypeError:
                        label = html_out_part(node.label, document, flags=flags, mode=mode) # _part this time
                    for domn in label:
                        r.appendChild(domn)
                styl = ""
                if node.width:
                    styl += "width:%dpx;" % node.width
                    if not is_xhtml2:
                        r.setAttribute("width", str(node.width))
                    elif "html5" in flags:
                        r.setAttribute("html:width", str(node.width))
                if node.height:
                    styl += "height:%dpx;" % node.height
                    if not is_xhtml2:
                        r.setAttribute("height", str(node.height))
                    elif "html5" in flags:
                        r.setAttribute("html:height", str(node.height))
                if styl:
                    r.setAttribute("style", styl)
                if "//twemoji.maxcdn.com" in content:
                    # https://github.com/twitter/twemoji/blob/b33c30e78db45be787410567ad6f4c7b56c137a0/README.md#attribution-requirements
                    yield document.createComment(" twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/ ")
                yield r
        elif isinstance(node, nodes.NewlineNode): # TODO: <br /> in XHTML2 present but deprecated, use of <l> how?
            r = document.createElement("br")
            yield r
        elif isinstance(node, nodes.RuleNode):
            r = document.createElement("hr" if not is_xhtml2 else "separator")
            yield r
        elif isinstance(node, nodes.DeseretNode):
            yield from deseret.characters_to_nodes(document, node.content)
        elif isinstance(node, nodes.DirectiveNode) and node.type.startswith("html-") and ("insecuredirective" in flags):
            r = document.createElement(node.type[len("html-"):].strip())
            for i,j in node.opts:
                r.setAttribute(i, j)
            for i in node.args:
                if i.strip():
                    r.setAttribute(i, i)
            for domn in html_out_part(node.content, document, flags=flags, mode=mode):
                r.appendChild(domn)
            yield r
        elif isinstance(node, nodes.TableNode):
            r = document.createElement("table")
            r.setAttribute("style", "border: 1px solid black; border-collapse: collapse;")
            cellstyle = "border: 1px solid black; padding: 0.5ex;"
            thead = document.createElement("thead")
            r.appendChild(thead)
            for row in node.table_head:
                tr = document.createElement("tr")
                thead.appendChild(tr)
                for colno, cell in enumerate(row):
                    th = document.createElement("th")
                    tr.appendChild(th)
                    th.setAttribute("style", cellstyle)
                    if node.aligns and (len(node.aligns) > colno) and node.aligns[colno]:
                        th.setAttribute("style", cellstyle + " text-align:" + node.aligns[colno])
                    for domn in html_out_part(list(cell), document, flags=flags, mode=mode):
                        th.appendChild(domn)
            tbody = document.createElement("tbody")
            r.appendChild(tbody)
            for row in node.table_body:
                tr = document.createElement("tr")
                tbody.appendChild(tr)
                for colno,cell in enumerate(row):
                    td = document.createElement("td")
                    tr.appendChild(td)
                    td.setAttribute("style", cellstyle)
                    if node.aligns and (len(node.aligns) > colno) and node.aligns[colno]:
                        td.setAttribute("style", cellstyle + " text-align:" + node.aligns[colno])
                    for domn in html_out_part(list(cell), document, flags=flags, mode=mode):
                        td.appendChild(domn)
            yield r
        elif isinstance(node,nodes.EmptyInterrupterNode):
            yield document.createTextNode("")
        else:
            yield document.createTextNode("ERROR" + repr(node))

#import htmlentitydefs
from mdplay import htmlentitydefs_latest as htmlentitydefs
def _escape(text, html5=0, mode="xhtml"):
    if mode == "xml": # as opposed to xhtml or html
        return
    if not html5:
        keys = list(htmlentitydefs.name2codepoint.keys())
    else:
        keys = list(htmlentitydefs.html5.keys())
    c2n4 = htmlentitydefs.codepoint2name
    for name in keys:
        if ((mode != "nml") and (name not in ("amp","lt","quot","gt","apos"))) or \
           ((mode == "nml") and (name not in ("lbrack","lt","rbrack","gt"))):
            # Not a syntax-critical escape so appropriate to do now.
            if not html5:
                codept=chr(htmlentitydefs.name2codepoint[name])
            else:
                codept=htmlentitydefs.html5[name]
            if (len(codept) == 1) and (ord(codept)<0x7f) and (name not in htmlentitydefs.name2codepoint):
                continue #or face insanity.
            elif (len(codept) == 1) and (ord(codept) in c2n4) and (name.rstrip(";") != c2n4[ord(codept)]):
                # Non-HTML4 names redundant with HTML4 names.  Avoid.
                continue
            elif mode != "nml":
                text=text.replace(codept,("&"+name.rstrip(";")+";"))
            else:
                text=text.replace(codept,("["+name.rstrip(";")+"]"))
    return text

mode_identifiers = {
    # Keyed by (serialisation, is_html5)
    ("xml", True): {
        # For XML parsers; HTML parsers won't necessarily parse it correctly
        "xmlns": "http://www.w3.org/1999/xhtml",
        "root": "html",
        "xsi": None,
        # WHATWG HTML is apathetic about xml-MIME-served doctype content.
        # Could make something up like "-//WHATWG//DTD XHTML5//EN" but... probably
        # best to stick to the legacy-format HTML5 doctype.
        # (The FPI "-//WHATWG//NONSGML HTML5//EN" was considered before it was
        # decided that HTML5 should not have an FPI.)
        "fpi": None,
        "fsi": "about:legacy-compat", # Condoned by HTML5.
        "other_xmlns": (),
        "syntax": "xml"
    },
    ("xhtml", True): {
        # For HTML5 and HTML5-entity-and-doctype-aware XML parsers
        "xmlns": "http://www.w3.org/1999/xhtml",
        "root": "html",
        "xsi": None,
        "fpi": None,
        "fsi": None,
        "other_xmlns": (),
        "syntax": "xhtml"
    },
    ("html", True): {
        # For HTML5 parsers, likely not to be valid XML
        "xmlns": None,
        "root": "html",
        "xsi": None,
        "fpi": None,
        "fsi": None,
        "other_xmlns": (),
        "syntax": "html"
    },
    ("xml", False): {
        # For XML parsers; HTML parsers won't necessarily parse it correctly
        "xmlns": "http://www.w3.org/1999/xhtml",
        "root": "html",
        "xsi": None,
        "fpi": "-//W3C//DTD XHTML 1.1//EN",
        "fsi": "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd",
        "other_xmlns": (),
        "syntax": "xml"
    },
    ("xhtml", False): {
        # For HTML parsers (not NS4) and XHTML1.1-entity-aware XML parsers
        "xmlns": "http://www.w3.org/1999/xhtml",
        "root": "html",
        "xsi": None,
        "fpi": "-//W3C//DTD XHTML 1.1//EN",
        "fsi": "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd",
        "other_xmlns": (),
        "syntax": "xhtml"
    },
    ("html", False): {
        # For HTML4 parsers, likely not to be valid XML
        "xmlns": None,
        "root": "html",
        "xsi": None,
        "fpi": "-//W3C//DTD HTML 4.01 Transitional//EN",
        "fsi": "https://www.w3.org/TR/html4/loose.dtd",
        "other_xmlns": (),
        "syntax": "html"
    },
    #
    # Now the niche, abandoned or experimental formats:
    ("nml", True): {
        # Naggum syntax serialisation of HTML5
        "xmlns": None,
        "root": "html",
        "xsi": None,
        "fpi": None,
        "fsi": None,
        "other_xmlns": (),
        "syntax": "nml"
    },
    ("nml", False): {
        # Naggum syntax serialisation of HTML4 (plus [lbrack] and [rbrack])
        "xmlns": None,
        "root": "html",
        "xsi": None,
        "fpi": None,
        "fsi": None,
        "other_xmlns": (),
        "syntax": "nml"
    },
    ("jsx", True): {
        # JSX syntax serialisation of HTML5
        "xmlns": None,
        "root": "html",
        "xsi": None,
        "fpi": None,
        "fsi": None,
        "other_xmlns": (),
        "syntax": "jsx"
    },
    ("jsx", False): {
        # JSX syntax serialisation of HTML4
        "xmlns": None,
        "root": "html",
        "xsi": None,
        "fpi": None,
        "fsi": None,
        "other_xmlns": (),
        "syntax": "jsx"
    },
    # The latest and likely terminal draft of XHTML 2 still defines the namespace as
    # being http://www.w3.org/1999/xhtml i.e. the same as XHTML 1 or 5.  However, the 
    # (presently no-op) schema http://www.w3.org/MarkUp/SCHEMA/xhtml2.xsd referenced
    # in said draft defines said namespace as being http://www.w3.org/2002/06/xhtml2/
    # which does in fact exist and calls itself the "XHTML 2.0 namespace".
    # Considering also the compatibility break between XHTML 1 or 5 and XHTML 2, and
    # the fact that XHTML 5 is the current version of XHTML, I'm using the latter.
    ("xhtml2", False): {
        # Abandoned compatibility-breaking version of HTML.
        "xmlns": "http://www.w3.org/2002/06/xhtml2/",
        "root": "html",
        "xsi": "http://www.w3.org/2002/06/xhtml2/ http://www.w3.org/MarkUp/SCHEMA/xhtml2.xsd",
        "fpi": "-//W3C//DTD XHTML 2.0//EN",
        "fsi": "http://www.w3.org/MarkUp/DTD/xhtml2.dtd",
        "other_xmlns": (("ev", "http://www.w3.org/2001/xml-events"),),
        "syntax": "xml"
    },
    # The unique namespaces become an identifying features of XHTML2 versus XHTML5.
    ("xhtml2", True): {
        # And you thought normal XHTML2 output was silly.
        "xmlns": "http://www.w3.org/2002/06/xhtml2/",
        "root": "html",
        "xsi": "http://www.w3.org/2002/06/xhtml2/ http://www.w3.org/MarkUp/SCHEMA/xhtml2.xsd",
        "fpi": "-//W3C//DTD XHTML 2.0//EN",
        "fsi": "http://www.w3.org/MarkUp/DTD/xhtml2.dtd",
        "other_xmlns": (("ev", "http://www.w3.org/2001/xml-events"), 
                        ("html", "http://www.w3.org/1999/xhtml")),
        "syntax": "xml"
    },
    # Similarly with NML syntax, which has no standard syntax for a doctype
    ("xhtml2nml", False): {
        # Yes, I went there.
        "xmlns": "http://www.w3.org/2002/06/xhtml2/",
        "root": "html",
        "xsi": "http://www.w3.org/2002/06/xhtml2/ http://www.w3.org/MarkUp/SCHEMA/xhtml2.xsd",
        "fpi": None, # No standard doctype syntax in NML.
        "fsi": None,
        "other_xmlns": (),
        "syntax": "nml"
    },
    ("xhtml2nml", True): {
        # And the most hipster format supported by this writer is...
        "xmlns": "http://www.w3.org/2002/06/xhtml2/",
        "root": "html",
        "xsi": "http://www.w3.org/2002/06/xhtml2/ http://www.w3.org/MarkUp/SCHEMA/xhtml2.xsd",
        "fpi": None,
        "fsi": None,
        "other_xmlns": (("ev", "http://www.w3.org/2001/xml-events"), 
                        ("html", "http://www.w3.org/1999/xhtml")),
        "syntax": "nml"
    },
}

def html_out(nodem,titl="",flags=(),mode="xhtml"):
    if "fragment" in flags:
        return html_out_body(nodem,flags)
    html5 = ("html5" in flags)
    mdi = minidom.getDOMImplementation() #minidom: other xml.dom imps don't necessarily support _get_attributes()
    fm = mode_identifiers[(mode, html5)]
    is_xhtml2 = mode in ("xhtml2", "xhtml2nml")
    document = mdi.createDocument(fm["xmlns"], fm["root"], mdi.createDocumentType(fm["root"], fm["fpi"], fm["fsi"]))
    if fm["xmlns"]:
        # not done automatically by minidom, though you'd expect it to given its provision above
        document.documentElement.setAttribute("xmlns", fm["xmlns"])
    for (ns, nsuri) in fm["other_xmlns"]:
        document.documentElement.setAttribute("xmlns:"+ns, nsuri)
    if fm["xsi"]:
        # not provided above so would not be expected to be done automatically
        document.documentElement.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        document.documentElement.setAttribute("xsi:schemaLocation", fm["xsi"])
    head = document.head = document.createElement("head")
    document.documentElement.appendChild(head)
    body = document.createElement("body")
    document.documentElement.appendChild(body)
    #Head
    if not html5:
        charset = document.createElement("meta")
        head.appendChild(charset)
        charset.setAttribute("http-equiv", "Content-Type")
        charset.setAttribute("content", "text/html; charset=UTF-8")
    else:
        if is_xhtml2:
            charset = document.createElement("html:meta")
        else:
            charset = document.createElement("meta")
        head.appendChild(charset)
        charset.setAttribute("charset", "UTF-8")
        xua = document.createElement("meta")
        head.appendChild(xua)
        xua.setAttribute("http-equiv", "X-UA-Compatible")
        xua.setAttribute("content", "IE=Edge")
    if titl:
        titlebar = document.createElement("title")
        head.appendChild(titlebar)
        titlebar.appendChild(document.createTextNode(titl))
    #Body
    nodem = list(nodem)
    for domn in html_out_part(nodem, document, flags=flags, mode=mode):
        body.appendChild(domn)
    retval = _escape(tohtml(document, "utf-8", mode=fm["syntax"]).decode("utf-8"), html5, mode=mode)
    document.unlink()
    return retval

def html_out_body(nodem, flags=(), mode="xhtml"):
    html5 = ("html5" in flags)
    fm = mode_identifiers[(mode, html5)]
    mdi = minidom.getDOMImplementation() #minidom: other xml.dom imps don't necessarily support _get_attributes()
    document = mdi.createDocument(None, "html", mdi.createDocumentType("html", None, None)) #never actually seen.
    document.head = document.createElement("head") #never actually seen, don't bother appending
    ret = ""
    nodem = list(nodem)
    for domn in html_out_part(nodem, document, flags=flags, mode=mode):
        ret += tohtml(domn, "utf-8", mode=fm["syntax"]).decode("utf-8")
    document.unlink()
    return _escape(ret, html5, mode=mode)

__mdplay_renderer__="html_out"
__mdplay_snippet_renderer__="html_out_body"

