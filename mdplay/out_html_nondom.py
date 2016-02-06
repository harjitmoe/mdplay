import re

#Ought to have at least one of these three
try:
    from json import dumps as _strquote
except:
    try:
        from simplejson import dumps as _strquote
    except:
        _strquote=repr

from mdplay import nodes

def html_out_body(nodes,flags=()):
    in_list=0
    r=""
    for node in nodes:
        _r=_html_out_body(node,in_list,flags=flags)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
        r+=_r
    return r.strip("\r\n")

import htmlentitydefs
def _escape(text):
    text=text.decode("utf-8").replace(u"&",u"&amp;") #must be done first, else others get broken.
    for name in htmlentitydefs.name2codepoint.keys():
        if name!="amp":
            text=text.replace(unichr(htmlentitydefs.name2codepoint[name]),("&"+name+";").decode("ascii"))
    return text.encode("utf-8")

def _html_out_body(node,in_list,flags):
    if in_list and ( (not isinstance(node,nodes.UlliNode)) or ((node.depth+1)<in_list) ):
        _r=_html_out_body(node,in_list-1,flags=flags)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
            in_list+=1
        return "</li></ul>"+_r,in_list-1
    if not isinstance(node,nodes.Node): #i.e. is a string
        return _escape(node)
    elif isinstance(node,nodes.TitleNode):
        if node.depth>6: node.depth=6
        return ("<h%d>"%node.depth)+html_out_body(node.content,flags=flags)+("</h%d>"%node.depth)
    elif isinstance(node,nodes.ParagraphNode):
        return "<p>"+html_out_body(node.content,flags=flags)+"</p>"
    elif isinstance(node,nodes.BlockQuoteNode):
        return "<blockquote>"+html_out_body(node.content,flags=flags)+"</blockquote>\n"
    elif isinstance(node,nodes.SpoilerNode):
        return "<p><a href='javascript:void(0);' onclick=\"document.getElementById('spoil%d').style.display=(document.getElementById('spoil%d').style.display=='none')?('block'):('none')\">Expand/Hide Spoiler</a></p><div class='spoiler' id='spoil%d' style='display:none;'>"%(id(node),id(node),id(node))+html_out_body(node.content,flags=flags)+"</div>"
    elif isinstance(node,nodes.CodeBlockNode):
        return "<pre>"+html_out_body(node.content,flags=flags)+"</pre>"
    elif isinstance(node,nodes.CodeSpanNode):
        return "<code>"+html_out_body(node.content,flags=flags)+"</code>"
    elif isinstance(node,nodes.UlliNode):
        r=""
        if (node.depth+1)>in_list:
            while (node.depth+1)>in_list:
                r+="<ul><li>"
                in_list+=1
        else:
            r+="</li><li>"
        r+=html_out_body(node.content,flags=flags)
        return r,in_list
    elif isinstance(node,nodes.BoldNode):
        if node.emphatic:
            return "<strong>"+html_out_body(node.content,flags=flags)+"</strong>"
        else:
            return "<b>"+html_out_body(node.content,flags=flags)+"</b>"
    elif isinstance(node,nodes.ItalicNode):
        if node.emphatic:
            return "<em>"+html_out_body(node.content,flags=flags)+"</em>"
        else:
            return "<i>"+html_out_body(node.content,flags=flags)+"</i>"
    elif isinstance(node,nodes.SuperNode):
        return "<sup>"+html_out_body(node.content,flags=flags)+"</sup>"
    elif isinstance(node,nodes.SubscrNode):
        return "<sub>"+html_out_body(node.content,flags=flags)+"</sub>"
    elif isinstance(node,nodes.HrefNode):
        label=html_out_body(node.label)
        ht=node.hreftype
        content=node.content
        if ht=="url":
            if ("showtropes" in flags) and re.match("https?://(www\.)?tvtropes.org",content):
                return "<u>"+label+("</u><sup><a href=%s>(TVTropes)</a></sup>"%_strquote(content))
            return ("<a href=%s>"%_strquote(content))+label+"</a>"
        else: #Including img
            label=label.strip()
            if label:
                return "<%s alt=%s src=%s />"%(ht,_strquote(label),_strquote(content))
            return "<%s src=%s />"%(ht,_strquote(content))
    elif isinstance(node,nodes.NewlineNode):
        return "<br />"
    elif isinstance(node,nodes.RuleNode):
        return "<hr />"
    elif isinstance(node,nodes.TableNode):
        r='<table border="1"><thead>'
        for row in node.table_head:
            r+="<tr>"
            for cell in row:
                r+="<th>"+html_out_body(list(cell))+"</th>"
            r+="</tr>"
        r+="</thead><tbody>"
        for row in node.table_body:
            r+="<tr>"
            for cell in row:
                r+="<td>"+html_out_body(list(cell))+"</td>"
            r+="</tr>"
        return r+"</tbody></table>"
    elif isinstance(node,nodes.EmptyInterrupterNode):
        return ""
    else:
        return "ERROR"+repr(node)

def html_out(nodes,titl="",flags=()):
    html5=("html5" in flags)
    if not html5:
        return '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml"><head><title>'+_escape(titl)+'</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head><body>'+html_out_body(nodes,flags)+"</body></html>"
    else:
        return '<!DOCTYPE html SYSTEM "about:legacy-compat">\n<html xmlns="http://www.w3.org/1999/xhtml"><head><title>'+_escape(titl)+'</title><meta charset="UTF-8" /></head><body>'+html_out_body(nodes,flags)+"</body></html>"

__mdplay_renderer__="html_out"
__mdplay_snippet_renderer__="html_out_body"

