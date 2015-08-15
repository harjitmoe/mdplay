from nodes import *

try:
    from io import StringIO
except:
    from StringIO import StringIO

try:
    StopIteration=StopIteration
except NameError:
    StopIteration=IndexError

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
    isulin=lambda line:line.strip() and (all_same(line.strip()) in tuple("=-"))
    isfence=lambda line:line.strip() and (line.lstrip()[0]==line.lstrip()[1]==line.lstrip()[2]) and (line.lstrip()[0] in "`~") and ((line.lstrip()[0]=="~") or ("`" not in line.lstrip().lstrip("`")))
    isbq=lambda line:line.strip() and (line.lstrip().startswith(">"))
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
            elif re.match(rule_re, line.rstrip()):
                within="rule"
                f.rtpma()
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
        elif within=="rule":
            yield (RuleNode())
            within="root"
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
            if isbq(line) or (line.strip() and not iscb(line) and not isulin(line) and not isfence(line) and not isul(line) and not isheadatx(line)):
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

def _parse_inline(content,lev="root"):
    lastchar=" "
    out=[]
    import re
    while content:
        c=content.pop(0)
        if c=="\\":
            c2=content.pop(0)
            if c2==" ":
                lastchar=" "
                continue
            else:
                lastchar=c+c2
                out.append(c2)
                continue
        elif c=="\n":
            out.append(NewlineNode())
            lastchar=" "
        elif c=="*":
            if content[0]=="*":
                del content[0]
                if lev=="bold":
                    return out
                out.append(BoldNode(_parse_inline(content,"bold")))
            else:
                if lev=="italic":
                    return out
                out.append(ItalicNode(_parse_inline(content,"italic")))
        elif c=="`":
            if lev=="mono":
                return out
            out.append(MonoNode(_parse_inline(content,"mono")))
        elif c=="]" and lev=="label":
            return out
        #re.match, i.e. looks only at start of string
        elif lastchar==" " and re.match("(!\w*)?\[.*\]\(.*\)",c+("".join(content))):
            hreftype=""
            while c!="[":
                hreftype+=c
                c=content.pop(0)
            label=_parse_inline(content,"label")
            href=""
            if content[0]=="(":
                del content[0]
                c=content.pop(0)
                while c!=")":
                    href+=c
                    c=content.pop(0)
            if hreftype=="!":
                hreftype="img"
            elif hreftype=="":
                hreftype="link"
            else:
                hreftype=hreftype[1:] #Minus the leading !
            out.append(HrefNode(href,label,hreftype))
        else:
            lastchar=c
            out.append(c)
    return out

def parse_inline(content):
    return _parse_inline(list(content))

#parse_inline=lambda f:[f] #For now

if __name__=="__main__":
    doc=list(_parse_block(LinestackIter(f)))
    import bb_out
    dd=bb_out.bb_out(doc)
    print dd
