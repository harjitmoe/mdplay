__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

class Node(object):
    pass

class SpoilerNode(Node):
    pass

class NonContainerNode(Node):
    pass

class BlockNode(Node):
    def __init__(self,content,depth=-1,bullet=None):
        from mdplay import interprocesses
        self.content=interprocesses.normalise_child_nodes(list(content))
        self.depth=depth
        self.bullet=bullet
        self.label="" # Spoiler kludge

class TableNode(Node):
    def __init__(self,content,aligns=None):
        self.table_head=content[0]
        self.table_body=content[1]
        self.aligns=aligns

class InlineNode(Node):
    def __init__(self,content,label="",hreftype="",emphatic=False,width=None,height=None):
        from mdplay import interprocesses
        self.content=content
        if isinstance(content, type([])):
            self.content=interprocesses.agglomerate(list(content))
        self.hreftype=hreftype
        self.emphatic=emphatic
        self.label=label
        if isinstance(label, type([])) and not isinstance(self, EmojiNode):
            self.label=interprocesses.agglomerate(list(label))
        self.width=width
        self.height=height
        self.fuse=None
        self.fyzi=0
        self.completed=0
        self.force_text=0

class CodeBlockNode(Node):
    def __init__(self,content,depth=-1,clas=None):
        self.content=content
        self.depth=depth
        self.clas=clas

class DirectiveNode(Node):
    def __init__(self,content,typ,args,opts):
        from mdplay import interprocesses
        self.content=interprocesses.normalise_child_nodes(list(content))
        self.type=typ
        self.args=args
        self.opts=opts

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

class CodeSpanNode(InlineNode):
    pass

class BoldNode(InlineNode):
    pass

class ItalicNode(InlineNode):
    pass

class UnderlineNode(InlineNode):
    pass

class SuperNode(InlineNode):
    pass

class SubscrNode(InlineNode):
    pass

class HrefNode(InlineNode):
    pass

class DeseretNode(InlineNode):
    pass

class RubiNode(InlineNode):
    pass

class NewlineNode(NonContainerNode):
    pass

class RuleNode(NonContainerNode):
    pass

class EmptyInterrupterNode(NonContainerNode):
    pass

