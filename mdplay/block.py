import re,string
try:
    from StringIO import StringIO
except:
    from io import StringIO

from mdplay import nodes
from mdplay import inline
from mdplay.LinestackIter import LinestackIter

class _TitleItem(object):
    c=None
    def __init__(self,l,n):
        self.l=l
        self.n=n
    def setchar(self,c):
        self.l.bychar[c]=self
        self.c=c

class TitleLevels(dict):
    def __init__(self):
        self.bychar={}
        dict.__init__(self)
    def __getitem__(self,k):
        try:
            return dict.__getitem__(self,k)
        except KeyError:
            self[k]=_TitleItem(self,k)
            return self[k]

def all_same(l):
    if len(l)==0:
        return False
    elif (len(l)==1) or (l[0]==all_same(l[1:])):
        return l[0]
    else:
        return False

def _parse_block(f,titlelevels):
    within="root"
    minibuf=""
    depth=0
    number=0
    depths=[]
    fence=None
    fenceinfo=None

    isrule=lambda line:re.match(r"\s*((?P<c>\*|_|-)\s?)\s*(?P=c)+\s*((?P=c)+\s+)*$",line+" ")
    isheadatx=lambda line:line.strip() and re.match(r"(#+) .*(\S#|[^#]|\\#)( \1)?$",line)
    isheadmw=lambda line:line.strip() and re.match(r"\s*(=+)([^=](.*[^=])?)\1\s*$",line)
    isulin=lambda line:line.strip() and (all_same(line.strip()) in tuple(string.punctuation))
    isfence=lambda line:line.strip() and re.match(r"\s*(```+[^`]*$|~~~+.*$)",line)
    isbq=lambda line:line.strip() and re.match(r"\s*>([^!].*)?$",line)
    issp=lambda line:line.strip() and line.lstrip().startswith(">!")
    iscb=lambda line:len(line)>=4 and all_same(line[:4])==" "
    isul=lambda line:line.strip() and re.match(r"\s*[*+-](\s.*)?$",line)

    for line in f:
        line=line.replace("\0","\xef\xbf\xbd").replace("\t","    ")
        if within=="root":
            assert depth==0
            if isheadatx(line):
                within="atxhead"
                f.rtpma()
                continue
            elif line.strip() == "::":
                within="icode"
                #NO rtpma
                continue
            elif isheadmw(line):
                within="mwhead"
                f.rtpma()
                continue
            elif isrule(line):
                within="rule"
                f.rtpma()
                continue
            elif isulin(line):
                within="sthead"
                #NO rtpma
                continue
            elif isul(line):
                within="ul"
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
            elif issp(line):
                within="spoiler"
                f.rtpma()
                continue
            elif line.strip():
                within="para"
                f.rtpma()
                continue
        elif within=="atxhead":
            if not isheadatx(line):
                yield (nodes.TitleNode(inline.parse_inline(minibuf),depth))
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
            titlelevels[deep] #Yes, just eval this.
            if depth and deep!=depth:
                yield (nodes.TitleNode(inline.parse_inline(minibuf),depth))
                minibuf=""
            depth=deep
            if all_same(line[-depth:])=="#":
                line=line[:-depth]
            line=line.strip()
            minibuf+=line+" "
        elif within=="mwhead":
            depth=0
            line=line.strip()
            while line.startswith("="):
                depth+=1
                line=line[1:]
            titlelevels[depth] #Yes, just eval this.
            #all_same(line[-depth:])=="=" assuming the regexp is correct
            line=line[:-depth]
            line=line.strip()
            yield (nodes.TitleNode(inline.parse_inline(line),depth))
            depth=0
            within="root"
        elif within in ("para","sthead"):
            depth+=1
            if isulin(line.rstrip()) and ((depth==2) or (within=="sthead")):
                # Combining vanilla-Setext and ATX headers is obvious.
                # Combining ReST and ATX headers is not.
                # For each new char, use the first level without a char.
                # Exception is "-" which is not assigned highest level,
                # unless it is used for literally the first heading in 
                # the document.
                # Thus implement ReST-style but mostly MD-compatible.
                char=line.strip()[0]
                if char in titlelevels.bychar:
                    depth=titlelevels.bychar[char].n
                else:
                    depth=1
                    while 1:
                        if (depth>1) or (char!="-") or (not titlelevels.keys()):
                            i=titlelevels[depth]
                            if i.c==char:
                                break
                            elif i.c==None:
                                i.setchar(char)
                                break
                        depth+=1
                yield (nodes.TitleNode(inline.parse_inline(minibuf),depth))
                minibuf=""
                depth=0
                within="root"
                #NO rtpma
                continue
            elif not line.strip():
                yield (nodes.ParagraphNode(inline.parse_inline(minibuf)))
                minibuf=""
                depth=0
                within="root"
                f.rtpma()
                continue
            elif isrule(line):
                yield (nodes.ParagraphNode(inline.parse_inline(minibuf)))
                minibuf=""
                depth=0
                within="rule"
                f.rtpma()
                continue
            if line.rstrip()[-3:]==" ::":
                if line.rstrip("\r\n").endswith("  "):
                    minibuf+=line.rstrip()[:-2].rstrip()+"\n"
                else:
                    minibuf+=line.rstrip()[:-2].rstrip()
            elif line.rstrip()[-2:]=="::":
                if line.rstrip("\r\n").endswith("  "):
                    minibuf+=line.rstrip()[:-1].rstrip()+"\n"
                else:
                    minibuf+=line.rstrip()[:-1].rstrip()
            elif line.rstrip("\r\n").endswith("  "):
                minibuf+=line.strip()+"\n"
            else:
                minibuf+=line.strip()+" "
            if line.rstrip().endswith("::"):
                yield (nodes.ParagraphNode(inline.parse_inline(minibuf)))
                minibuf=""
                depth=0
                within="icode"
                #NO rtpma
                continue
        elif within=="ul":
            if not line.strip():
                yield (nodes.UlliNode(parse_block(minibuf,titlelevels),depth))
                minibuf=""
                depth=0
                depths=[]
                within="root"
                f.rtpma()
                continue
            elif isrule(line):
                yield (nodes.UlliNode(parse_block(minibuf,titlelevels),depth))
                minibuf=""
                depth=0
                depths=[]
                within="rule"
                f.rtpma()
                continue
            elif isul(line):
                if minibuf:
                    yield (nodes.UlliNode(parse_block(minibuf,titlelevels),depth))
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
        elif within=="rule":
            yield (nodes.RuleNode())
            within="root"
        elif within=="icode":
            if (depth==0) and (not line.strip()):
                continue
            if depth==0:
                depth=len(line)-len(line.lstrip())
            if depth==0: #if depth /* still */ == 0...
                minibuf=""
                depth=0
                fence=None
                within="root"
                f.rtpma()
                continue
            if not line.startswith(" "*depth):
                yield (nodes.CodeBlockNode(minibuf,clas="::"))
                minibuf=""
                depth=0
                fence=None
                within="root"
                f.rtpma()
                continue
            else:
                minibuf+=line[depth:].rstrip("\r\n")+"\n"
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
                yield (nodes.CodeBlockNode(minibuf,clas=fenceinfo))
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
            if isbq(line) or (line.strip() and not iscb(line) and not isulin(line) and not isfence(line) and not isul(line) and not isheadatx(line) and not issp(line)):
                line=line.lstrip()
                if line[:1]==">":line=line[1:]
                if line[:1]==" ":line=line[1:]
                minibuf+=line.rstrip("\r\n")+"\n"
            else:
                yield (nodes.BlockQuoteNode(parse_block(minibuf,titlelevels)))
                minibuf=""
                within="root"
                f.rtpma()
                continue
        elif within=="spoiler":
            if issp(line) or (line.strip() and not iscb(line) and not isulin(line) and not isfence(line) and not isul(line) and not isheadatx(line) and not isbq(line)):
                line=line.lstrip()
                if line[:2]==">!":line=line[2:]
                if line[:1]==" ":line=line[1:]
                minibuf+=line.rstrip("\r\n")+"\n"
            else:
                yield (nodes.SpoilerNode(parse_block(minibuf,titlelevels)))
                minibuf=""
                within="root"
                f.rtpma()
                continue
        else:
            raise AssertionError("Unknown syntax feature %r"%within)
    if minibuf:
        if within=="fence":
            yield (nodes.CodeBlockNode(minibuf,clas=fenceinfo))
            minibuf=""
            depth=0
            fence=None
            within="root"
        elif within=="icode":
            yield (nodes.CodeBlockNode(minibuf,clas="::"))
            minibuf=""
            depth=0
            within="root"

def parse_block(content,titlelevels):
    return _parse_block(LinestackIter(StringIO(content)),titlelevels)

