#Increasingly a misnomer.

class Node(object):
    pass

class SpoilerNode(Node):
    pass

class NonContainerNode(Node):
    pass

class BlockNode(Node):
    def __init__(self,content,depth=-1,bullet=None):
        self.content=filter_paratags(list(content))
        self.depth=depth
        self.bullet=bullet

class TableNode(Node):
    def __init__(self,content,aligns=None):
        self.table_head=content[0]
        self.table_body=content[1]
        self.aligns=aligns

class InlineNode(Node):
    def __init__(self,content,label="",hreftype="",emphatic=False,width=None,height=None):
        self.content=content
        self.hreftype=hreftype
        self.emphatic=emphatic
        self.label=label
        self.width=width
        self.height=height
        self.fuse=None
        self.completed=0

class CodeBlockNode(Node):
    def __init__(self,content,depth=-1,clas=None):
        self.content=content
        self.depth=depth
        self.clas=clas

class EmojiNode(InlineNode):
    pass

class TitleNode(BlockNode):
    pass

class ParagraphNode(BlockNode):
    pass

class BlockQuoteNode(BlockNode):
    pass

class BlockSpoilerNode(BlockNode,SpoilerNode):
    pass

class InlineSpoilerNode(InlineNode,SpoilerNode):
    pass

class LiNode(BlockNode):
    pass

class UlliNode(LiNode):
    pass

class OlliNode(LiNode):
    pass

class BadassEchoNode(InlineNode):
    pass

class CodeSpanNode(InlineNode):
    pass

class BoldNode(InlineNode):
    pass

class ItalicNode(InlineNode):
    pass

class SuperNode(InlineNode):
    pass

class SubscrNode(InlineNode):
    pass

class HrefNode(InlineNode):
    pass

class RubiNode(InlineNode):
    pass

class NewlineNode(NonContainerNode):
    pass

class RuleNode(NonContainerNode):
    pass

class EmptyInterrupterNode(NonContainerNode):
    pass

def filter_paratags(content):
    if len(content)==1 and isinstance(content[0],ParagraphNode):
        return content[0].content
    return content

def agglomerate(nodelist):
    outlist=[]
    for i in nodelist:
        #NOTE: assumes 2k
        if isinstance(i,type(u"")):
            i=i.encode("utf-8")
        if isinstance(i,type("")) and outlist and isinstance(outlist[-1],type("")): #NOT elif
            outlist[-1]+=i
        else:
            outlist.append(i)
    return outlist

def agglomerate_inplace(nodelist):
    """The way the DOM renderer works with lists necessitates this."""
    agglo=agglomerate(nodelist)
    del nodelist[:]
    nodelist.extend(agglo)
    return nodelist

# Give more deterministic IDs to expandable spoiler nodes in HTML/MWiki.
_curid = 1
_idded={}
def newid(node):
    global _curid
    if id(node) not in _idded:
        _idded[id(node)]=_curid
        _curid+=1
    return _idded[id(node)]

def flatten_flags_parser(flags):
    out=[]
    for flag in flags:
        if flag=="strict":
            out.extend(flatten_flags_parser(["norest","nospoilertag","nowikitext","noredditstyle","nopandocstyle","nospecialhrefs","nodiacritic","noemoticon","noembedspoiler","nocjk","norubi"]))
        elif flag=="norest":
            out.extend(flatten_flags_parser(["noresthead","nodicode","noresttable"]))
        elif flag=="nowikitext":
            out.extend(flatten_flags_parser(["nowikihead","nowikiemph","nowikilinks"]))
        elif flag=="noredditstyle":
            out.extend(flatten_flags_parser(["noredditstylesuper","noredditspoiler"]))
        elif flag=="nospoilertag":
            out.extend(flatten_flags_parser(["noblockspoiler","noredditspoiler"]))
        elif flag=="nosetexthead":
            out.extend(flatten_flags_parser(["noplainsetexthead","noresthead"]))
        elif flag=="notable":
            out.extend(flatten_flags_parser(["noresttable","nomdtable"]))
        elif flag=="nosupersubscript":
            out.extend(flatten_flags_parser(["noredditstylesuper","nopandocstyle"]))
        elif flag=="noemoticon":
            out.extend(flatten_flags_parser(["noasciiemoticon","noshortcodeemoji"]))
        elif flag=="nocjk":
            out.extend(flatten_flags_parser(["noromkan","nocangjie"]))
        else:
            out.append(flag)
    return list(set(out))

def utf16_ord(s):
    s=list(s)
    c=s.pop(0)
    if (0xD800<=ord(c)<0xDC00) and (0xDC00<=ord(s[0])<0xE000):
        k=s.pop(0)
        index_from_smp=((ord(c)-0xD800)*1024)+(ord(k)-0xDC00)
        codepoint=0x010000+index_from_smp
        if s: raise ValueError
        return codepoint
    else:
        if s: raise ValueError
        return ord(c)

def simul_replace(a, b, c, d, e):
    r = []
    for f in a.split(b):
        r.append(f.replace(d, e))
    return c.join(r)



