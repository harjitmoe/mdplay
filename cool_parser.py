try:
    from io import StringIO
except:
    from StringIO import StringIO

class Node(object):
    pass

class NonContainerNode(Node):
    pass

class BlockContainerNode(Node):
    def __init__(self,content,depth=-1,number=None):
        self.content=list(parse_block(content))
        self.depth=depth
        self.number=number

class InlineContainerNode(Node):
    def __init__(self,content,depth=-1,number=None):
        self.content=list(parse_inline(content))
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

class OlliNode(BlockContainerNode):
    pass

class CodeBlockNode(RawContainerNode):
    pass

class RuleNode(NonContainerNode):
    pass

try:
    StopIteration=StopIteration
except NameError:
    StopIteration=IndexError

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

def all_same(l):
    if len(l)==0:
        return False
    elif (len(l)==1) or (l[0]==all_same(l[1:])):
        return l[0]
    else:
        return False

f=open("test.txt","rb")

def _parse_block(f):
    within="root"
    minibuf=""
    depth=0
    number=0
    depths=[]
    fence=None
    fenceinfo=None

    import re
    rule_re=" ? ? ?((- ?)(- ?)(- ?)+|(_ ?)(_ ?)(_ ?)+|(\* ?)(\* ?)(\* ?)+)"
    isheadatx=lambda line:line.strip() and line.startswith("#") and (not line.lstrip("#")[:1].strip()) and ((len(line)-len(line.lstrip("#")))<=6)
    isulin=lambda line:line.strip() and ((len(line)-len(line.lstrip()))<=3) and (all_same(line.strip()) in tuple("=-"))
    isfence=lambda line:line.strip() and ((len(line)-len(line.lstrip()))<=3) and (line.lstrip()[0]==line.lstrip()[1]==line.lstrip()[2]) and (line.lstrip()[0] in "`~") and ((line.lstrip()[0]=="~") or ("`" not in line.lstrip().lstrip("`")))
    isbq=lambda line:line.strip() and ((len(line)-len(line.lstrip()))<=3) and (line.lstrip().startswith(">"))
    iscb=lambda line:len(line)>=4 and all_same(line[:4])==" "
    isul=lambda line:line.strip() and (line.lstrip()[0] in "*+-") and (line.lstrip()[1:][:1] in (""," "))

    for line in f:
        line=line.replace("\0","\xef\xbf\xbd")
        if within=="root":
            if iscb(line):
                within="codeblock"
                f.rtpma()
                continue
            elif isheadatx(line):
                within="atxhead"
                f.rtpma()
                continue
            elif isul(line):
                within="ul"
                f.rtpma()
                continue
            elif line.lstrip() and line.lstrip()[0] in "0123456789":
                within="ol"
                f.rtpma()
                continue
            elif re.match(rule_re, line.rstrip()):
                within="rule"
                f.rtpma()
                continue
            elif isfence(line):
                within="fence"
                f.rtpma()
                continue
            elif isbq(line):
                within="quote"
                f.rtpma()
                continue
            elif line.strip():
                within="para"
                f.rtpma()
                continue
        elif within=="atxhead":
            if not isheadatx(line):
                yield (TitleNode(minibuf,depth))
                minibuf=""
                depth=0
                within="root"
                f.rtpma()
                continue
            deep=0
            line=line.strip()
            while line.startswith("#"):
                deep+=1
                line=line[1:]
            if depth and deep!=depth:
                yield (TitleNode(minibuf,depth))
                minibuf=""
            depth=deep
            if all_same(line[-depth:])=="#":
                line=line[:-depth]
            line=line.strip()
            minibuf+=line+" "
        elif within=="para":
            depth+=1
            if depth==2 and isulin(line.rstrip()):
                yield (TitleNode(minibuf,(1 if line.strip()[0]=="=" else 2)))
                minibuf=""
                depth=0
                within="root"
                f.rtpma()
                continue
            elif not line.strip():
                yield (ParagraphNode(minibuf))
                minibuf=""
                depth=0
                within="root"
                f.rtpma()
                continue
            elif re.match(rule_re, line.rstrip()):
                within="rule"
                depth=0
                f.rtpma()
                continue
            if line.rstrip("\r\n").endswith("  "):
                minibuf+=line.strip()+"\n"
            else:
                minibuf+=line.strip()+" "
        elif within=="ul":
            if not line.strip():
                yield (UlliNode(minibuf,depth))
                minibuf=""
                depth=0
                depths=[]
                within="root"
                f.rtpma()
                continue
            elif re.match(rule_re, line.rstrip()):
                yield (UlliNode(minibuf,depth))
                minibuf=""
                depth=0
                depths=[]
                within="rule"
                f.rtpma()
                continue
            elif isul(line):
                if minibuf:
                    yield (UlliNode(minibuf,depth))
                    minibuf=""
                deep=len(line.replace("\t"," "*4))-len(line.replace("\t"," "*4).lstrip())
                if not depths:
                    depths.append(deep)
                    depth=0
                elif deep>depths[-1]:
                    depths.append(deep)
                    depth+=1
                elif deep in depths:
                    depth=depths.index(deep)
                    depths=depths[:depth+1]
                minibuf+=line.lstrip()[1:].strip()+" "
            else:
                minibuf+=line.strip()+" "
        elif within=="ol":
            if not line.strip():
                yield (OlliNode(minibuf,depth,number))
                minibuf=""
                depth=number=0
                depths=[]
                within="root"
                f.rtpma()
                continue
            elif re.match(rule_re, line.rstrip()):
                yield (OlliNode(minibuf,depth,number))
                minibuf=""
                depth=number=0
                depths=[]
                within="rule"
                f.rtpma()
                continue
            elif line.lstrip()[0] in "0123456789":
                if minibuf:
                    yield (OlliNode(minibuf,depth,number))
                    minibuf=""
                deep=len(line.replace("\t"," "*4))-len(line.replace("\t"," "*4).lstrip())
                if not depths:
                    depths.append(deep)
                    depth=0
                elif deep>depths[-1]:
                    depths.append(deep)
                    depth+=1
                elif deep in depths:
                    depth=depths.index(deep)
                    depths=depths[:depth+1]
                number=line.lstrip().split()[0].split(".")[0].split(")")[0]
                minibuf+=line.lstrip()[len(number):].lstrip(".)").strip()+" "
                number=int(number,10)
            else:
                minibuf+=line.strip()+" "
        elif within=="rule":
            yield (RuleNode())
            within="root"
        elif within=="codeblock":
            if (not line.replace("\t"," "*4).startswith("    ")) and line.rstrip():
                yield (CodeBlockNode(minibuf))
                minibuf=""
                within="root"
                f.rtpma()
                continue
            minibuf+=line[4:].rstrip("\r\n")+"\n"
        elif within=="fence":
            if fence==None:
                fence=0
                depth=len(line)-len(line.lstrip())
                line=line.lstrip()
                fchar=line[0]
                while line[:1]==fchar:
                    fence+=1
                    line=line[1:]
                fenceinfo=line
                fence*=fchar
            elif all_same(line.strip()) and (fence in line):
                yield (CodeBlockNode(minibuf,clas=fenceinfo))
                minibuf=""
                depth=0
                fence=None
                within="root"
            else:
                for i in range(depth):
                    if line[:1]==" ":
                        line=line[1:]
                minibuf+=line.rstrip("\r\n")+"\n"
        elif within=="quote":
            if isbq(line) or (line.strip() and not iscb(line) and not isulin(line) and not isfence(line) and not re.match(rule_re, line.rstrip()) and not isul(line)):
                line=line.lstrip()
                if line[:1]==">":line=line[1:]
                if line[:1]==" ":line=line[1:]
                minibuf+=line.rstrip("\r\n")+"\n"
            else:
                yield (BlockQuoteNode(minibuf))
                minibuf=""
                within="root"
                f.rtpma()
                continue
    if minibuf:
        if within=="fence":
            yield (CodeBlockNode(minibuf,clas=fenceinfo))
            minibuf=""
            depth=0
            fence=None
            within="root"
        if within=="codeblock":
            yield (CodeBlockNode(minibuf))
            minibuf=""
            within="root"
            f.rtpma()

def parse_block(content):
    return _parse_block(LinestackIter(StringIO(content)))

parse_inline=lambda f:[f] #For now

doc=list(_parse_block(LinestackIter(f)))

