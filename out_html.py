import re
try:
    import json
except:
    import simplejson as json

import nodes

def html_out_body(nodes):
    in_list=0
    r=""
    for node in nodes:
        _r=_html_out_body(node,in_list)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
        r+=_r
    return r.strip("\r\n")

def _html_out_body(node,in_list):
    if in_list and ((not isinstance(node,nodes.UlliNode)) or ((node.depth+1)<in_list)):
        _r=_html_out_body(node,in_list-1)
        if len(_r)==2 and type(_r)==type(()):
            _r,in_list=_r
            in_list+=1
        return "</ul>\n"+_r,in_list-1
    if not isinstance(node,nodes.Node): #i.e. is a string
        return node
    elif isinstance(node,nodes.TitleNode):
        if node.depth>6: node.depth=6
        return ("<h%d>"%node.depth)+html_out_body(node.content)+("</h%d>"%node.depth)
    elif isinstance(node,nodes.ParagraphNode):
        return "<p>"+html_out_body(node.content)+"</p>"
    elif isinstance(node,nodes.BlockQuoteNode):
        return "<blockquote>"+html_out_body(node.content)+"</blockquote>\n"
    elif isinstance(node,nodes.SpoilerNode):
        return "<p><a href='javascript:void(0);' onclick=\"document.getElementById('spoil%d').style.display=(document.getElementById('spoil%d').style.display=='none')?('block'):('none')\">Expand/Hide Spoiler</a></p><div class='spoiler' id='spoil%d' style='display:none;'>"%(id(node),id(node),id(node))+html_out_body(node.content)+"</div>"
    elif isinstance(node,nodes.CodeBlockNode):
        return "<pre>"+html_out_body(node.content)+"</pre>"
    elif isinstance(node,nodes.UlliNode):
        r=""
        while (node.depth+1)>in_list:
            r+="<ul>"
            in_list+=1
        r+="<li>"+html_out_body(node.content)+"</li>"
        return r,in_list
    elif isinstance(node,nodes.BoldNode):
        return "<strong>"+html_out_body(node.content)+"</strong>"
    elif isinstance(node,nodes.ItalicNode):
        return "<em>"+html_out_body(node.content)+"</em>"
    elif isinstance(node,nodes.SuperNode):
        return "<sup>"+html_out_body(node.content)+"</sup>"
    elif isinstance(node,nodes.SubscrNode):
        return "<sub>"+html_out_body(node.content)+"</sub>"
    elif isinstance(node,nodes.HrefNode):
        label=html_out_body(node.label)
        ht=node.hreftype
        content=node.content
        if ht=="url":
            if re.match("https?://(www\.)?tvtropes.org",content):
                return "<u>"+label+("</u><sup><a href=%s>(TVTropes)</a></sup>"%json.dumps(content))
            return ("<a href=%s>"%json.dumps(content))+label+"</a>"
        else: #Including img
            label=label.strip()
            if label:
                return "<%s alt=%s src=%s />"%(ht,json.dumps(label),json.dumps(content))
            return "<%s src=%s />"%(ht,json.dumps(content))
    elif isinstance(node,nodes.NewlineNode):
        return "<br />"
    elif isinstance(node,nodes.RuleNode):
        return "<hr />"
    else:
        return "ERROR"+repr(node)

def html_out(nodes,titl=""):
    #Note: trust is assumed to have been established on titl by this point
    return '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml"><head><title>'+titl+'</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head><body>'+html_out_body(nodes)+"</body></html>"

