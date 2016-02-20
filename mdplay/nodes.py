class Node(object):
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
    def __init__(self,content,label="",hreftype="",emphatic=False):
        self.content=content
        self.hreftype=hreftype
        self.emphatic=emphatic
        self.label=label

class CodeBlockNode(Node):
    def __init__(self,content,depth=-1,clas=None):
        self.content=content
        self.depth=depth
        self.clas=clas

class TitleNode(BlockNode):
    pass

class ParagraphNode(BlockNode):
    pass

class BlockQuoteNode(BlockNode):
    pass

class SpoilerNode(BlockNode):
    pass

class LiNode(BlockNode):
    pass

class UlliNode(LiNode):
    pass

class OlliNode(LiNode):
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
            out.extend(flatten_flags_parser(["norest","nospoilertag","nowikitext","noredditstyle","nopandocstyle","nospecialhrefs","nodiacritic"]))
        elif flag=="norest":
            out.extend(flatten_flags_parser(["noresthead","nodicode","noresttable"]))
        elif flag=="nowikitext":
            out.extend(flatten_flags_parser(["nowikihead","nowikiemph","nowikilinks"]))
        elif flag=="noredditstyle":
            out.extend(flatten_flags_parser(["noredditstyletable","noredditstylesuper"]))
        elif flag=="nosetexthead":
            out.extend(flatten_flags_parser(["noplainsetexthead","noresthead"]))
        elif flag=="notable":
            out.extend(flatten_flags_parser(["noresttable","noredditstyletable"]))
        elif flag=="nosupersubscript":
            out.extend(flatten_flags_parser(["noredditstylesuper","nopandocstyle"]))
        else:
            out.append(flag)
    return list(set(out))

