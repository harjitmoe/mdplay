# cool_parser is imported at bottom of module

class Node(object):
    pass

class NonContainerNode(Node):
    pass

class InlineNode(Node):
    def __init__(self,content,label="",hreftype=""):
        self.content=content
        self.hreftype=hreftype
        self.label=label

class BlockContainerNode(Node):
    def __init__(self,content,depth=-1,number=None):
        self.content=list(cool_parser.parse_block(content))
        self.depth=depth
        self.number=number

class InlineContainerNode(Node):
    def __init__(self,content,depth=-1,number=None):
        self.content=list(cool_parser.parse_inline(content))
        self.depth=depth
        self.number=number

class RawContainerNode(Node):
    def __init__(self,content,depth=-1,number=None,clas=None):
        self.content=content
        self.depth=depth
        self.number=number
        self.clas=clas

class TitleNode(InlineContainerNode):
    pass

class ParagraphNode(InlineContainerNode):
    pass

class BlockQuoteNode(BlockContainerNode):
    pass

class UlliNode(BlockContainerNode):
    pass

class CodeBlockNode(RawContainerNode):
    pass

class MonoNode(InlineNode):
    pass

class BoldNode(InlineNode):
    pass

class ItalicNode(InlineNode):
    pass

class HrefNode(InlineNode):
    pass

class NewlineNode(NonContainerNode):
    pass

class RuleNode(NonContainerNode):
    pass

class LinestackIter(object):
    _stack=None
    _n=None
    _c=None
    def __init__(self,stack):
        self._stack=list(stack)
        self._n=-1
        self._c=0 #Number of calls to __next__
    def __next__(self):
        self._c+=1
        self._n+=1
        if self._n==len(self._stack):
            return ""
        if self._n>=(len(self._stack)+1):
            raise StopIteration
        return self._stack[self._n]
    def peek_back(self,n=1):
        if (self._n-n)<0:
            return None
        return self._stack[self._n-n]
    def peek_ahead(self,n=1):
        if (self._n+n)>=len(self._stack):
            return None
        return self._stack[self._n+n]
    def rtpma(self): #Run that past me again
        self._n-=1
    #
    # Tell Python to use iterator __next__/next API
    def __iter__(self):
        return self
    #
    # Wrappers for older iterator APIs
    def next(self):
        return self.__next__()
    def __getitem__(self,i):
        if i==self._c:
            return self.__next__()
        else:
            raise TypeError("indexing an iterator")

import cool_parser
