class Node(object):
    pass

class NonContainerNode(Node):
    pass

class BlockNode(Node):
    def __init__(self,content,depth=-1,number=None,fence=None):
        self.content=filter_paratags(list(content))
        self.depth=depth
        self.number=number
        self.fence=fence

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
    def __init__(self,content,depth=-1,number=None,clas=None):
        self.content=content
        self.depth=depth
        self.number=number
        self.clas=clas

class TitleNode(BlockNode):
    pass

class ParagraphNode(BlockNode):
    pass

class BlockQuoteNode(BlockNode):
    pass

class SpoilerNode(BlockNode):
    pass

class UlliNode(BlockNode):
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
