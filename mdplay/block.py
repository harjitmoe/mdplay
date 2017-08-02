__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import re, string, os
try:
    from io import StringIO
except:
    from io import StringIO

from mdplay import nodes, mdputil, inline
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

class State(object):
    def __init__(self):
        self.titlelevels = TitleLevels()
        self.custom_eac = {}

def all_same(l):
    if len(l)==0:
        return False
    elif len(l)==1:
        return l[0]
    else:
        for i in l:
            if i!=l[0]:
                return False
        return l[0]

def _parse_block(f,state,flags):
    within="root"
    minibuf=""
    depth=0
    depths=[]
    fence=None
    fenceinfo=None
    cellwid=[]
    cellrows=[]
    def handle_directive():
        #print(repr(direname), repr(cellwid))
        if direname.strip() in ("", "mdplay-nonoutput"):
            list(parse_block(minibuf,state,flags))
        elif direname.strip() == "mdplay-flag":
            newflags = list(flags[:])
            for i in cellwid:
                for j in i.replace(",", " ").split():
                    if j:
                        if j.startswith("-"):
                            k = j[1:]
                            while k in newflags:
                                newflags.remove(k)
                        elif j != "extradirective":
                            newflags.append(j)
            yield from parse_block(minibuf,state,mdputil.flatten_flags_parser(tuple(newflags)))
        elif direname.strip() == "mdplay-include":
            for i in cellwid:
                if i:
                    mf = os.path.join(os.path.dirname(__file__), "headers", os.path.basename(i.strip()))
                    mf = open(mf, "rU")
                    yield from parse_block(mf.read(), state, flags)
                    mf.close()
        elif direname.strip() == "mdplay-pgcontext":
            yield from mdputil.normalise_child_nodes(parse_block(minibuf, state, flags))
        elif ("extradirective" in flags):
            yield nodes.DirectiveNode(parse_block(minibuf,state,flags),direname,cellwid,cellrows)

    isrule=lambda line:re.match(r"\s*((?P<c>\*|_|-)\s?)\s*(?P=c)+\s*((?P=c)+\s+)*$",line+" ")
    istablerest=lambda line:re.match(r"(=+ )+=+\s*$",line)
    isheadatx=lambda line:line.strip() and re.match(r"(#+) .*(\S#|[^#]|\\#)( \1)?$",line)
    isheadmw=lambda line:line.strip() and re.match(r"\s*(=+)([^=](.*[^=])?)\1\s*$",line)
    if ("noresthead" not in flags):
        isulin=lambda line:line.strip() and (all_same(line.strip()) in tuple(string.punctuation))
    else:
        isulin=lambda line:line.strip() and (all_same(line.strip()) in tuple("=-"))
    isfence=lambda line:line.strip() and re.match(r"\s*(```+[^`]*$|~~~+.*$)",line)
    if ("noblockspoiler" not in flags):
        isbq=lambda line:line.strip() and re.match(r"\s*>([^!].*)?$",line)
        issp=lambda line:line.strip() and line.lstrip().startswith(">!")
    else:
        isbq=lambda line:line.strip() and re.match(r"\s*>.*$",line)
        issp=lambda line:0
    iscb=lambda line:len(line)>=4 and all_same(line[:4])==" "
    isul=lambda line:line.strip() and re.match(r"\s*[*+-](\s.*)?$",line)
    #isol=lambda line:line.strip() and re.match(r"\s*(\d+[).:]|[#])(\s.*)?$",line)
    isol=lambda line:line.strip() and re.match(r"\s*(\d+[).:])(\s.*)?$",line)
    isalign=lambda line:(line!=None) and line.strip() and re.match(r"\|?((:--+|:-+:|--+:|---+)\|)+(:--+|:-+:|--+:|---+)\|?",line)

    for line in f:
        line=line.replace("\0","\xef\xbf\xbd").replace("\t"," "*4)
        if within=="root":
            assert depth==0
            if line.startswith(" "*4) and ("nouicode" not in flags):
                within="icode"
                depth=4
                f.reconsume()
                continue
            elif isheadatx(line):
                within="atxhead"
                f.reconsume()
                continue
            elif line.startswith(".. ") and ("::" in line) and ("nodirective" not in flags):
                within="directive"
                f.reconsume()
                continue
            elif (line.strip() == "::") and ("nodicode" not in flags):
                within="icode"
                #NO reconsume
                continue
            elif isheadmw(line) and ("nowikihead" not in flags):
                within="mwhead"
                f.reconsume()
                continue
            elif istablerest(line) and ("noresttable" not in flags):
                within="tablerest"
                f.reconsume()
                continue
            elif isrule(line):
                within="rule"
                f.reconsume()
                continue
            elif isfence(line) and ("nofcode" not in flags):
                within="fence"
                f.reconsume()
                continue
            elif isulin(line) and ("noresthead" not in flags):
                within="sthead"
                #NO reconsume
                continue
            elif isul(line):
                within="ul"
                f.reconsume()
                continue
            elif isol(line):
                within="ol"
                f.reconsume()
                continue
            elif isbq(line):
                within="quote"
                f.reconsume()
                continue
            elif issp(line) and ("noblockspoiler" not in flags):
                within="spoiler"
                f.reconsume()
                continue
            elif ("|" in line) and isalign(f.peek_ahead()) and ("nomdtable" not in flags):
                within="table"
                f.reconsume()
                continue
            elif line.startswith(".. ") and ("nocomment" not in flags):
                #No reconsume or within change.
                continue
            elif line.strip():
                within="para"
                f.reconsume()
                continue
        elif within=="atxhead":
            if not isheadatx(line):
                yield nodes.TitleNode(inline.parse_inline(minibuf,flags,state),depth)
                minibuf=""
                depth=0
                within="root"
                f.reconsume()
                continue
            deep=0
            line=line.strip()
            while line.startswith("#"):
                deep+=1
                line=line[1:]
            state.titlelevels[deep] #Yes, just eval this.
            if depth and deep!=depth:
                yield nodes.TitleNode(inline.parse_inline(minibuf,flags,state),depth)
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
            state.titlelevels[depth] #Yes, just eval this.
            #all_same(line[-depth:])=="=" assuming the regexp is correct
            line=line[:-depth]
            line=line.strip()
            yield nodes.TitleNode(inline.parse_inline(line,flags,state),depth)
            depth=0
            within="root"
        elif within in ("para","sthead"):
            depth+=1
            if isulin(line.rstrip()) and (((depth==2) and ("noplainsetexthead" not in flags)) or (within=="sthead")):
                # Combining vanilla-Setext and ATX headers is obvious.
                # Combining ReST and ATX headers is not.
                # For each new char, use the first level without a char.
                # Exception is "-" which is not assigned highest level,
                # unless it is used for literally the first heading in
                # the document.
                # Thus implement ReST-style but mostly MD-compatible.
                char=line.strip()[0]
                if char in state.titlelevels.bychar:
                    depth=state.titlelevels.bychar[char].n
                else:
                    depth=1
                    while 1:
                        if (depth>1) or (char!="-") or (not list(state.titlelevels.keys())):
                            i=state.titlelevels[depth]
                            if i.c==char:
                                break
                            elif i.c==None:
                                i.setchar(char)
                                break
                        depth+=1
                yield nodes.TitleNode(inline.parse_inline(minibuf,flags,state),depth)
                minibuf=""
                depth=0
                within="root"
                #NO reconsume
                continue
            elif not line.strip():
                yield nodes.ParagraphNode(inline.parse_inline(minibuf,flags,state))
                minibuf=""
                depth=0
                within="root"
                f.reconsume()
                continue
            elif isrule(line):
                yield nodes.ParagraphNode(inline.parse_inline(minibuf,flags,state))
                minibuf=""
                depth=0
                within="rule"
                f.reconsume()
                continue
            if (line.rstrip()[-3:]==" ::") and ("nodicode" not in flags):
                if line.rstrip("\r\n").endswith("  "):
                    minibuf+=line.rstrip()[:-2].rstrip()+"\n"
                else:
                    minibuf+=line.rstrip()[:-2].rstrip()
            elif (line.rstrip()[-2:]=="::") and ("nodicode" not in flags):
                if line.rstrip("\r\n").endswith("  "):
                    minibuf+=line.rstrip()[:-1].rstrip()+"\n"
                else:
                    minibuf+=line.rstrip()[:-1].rstrip()
            elif line.rstrip("\r\n").endswith("  "):
                minibuf+=line.strip()+"\n"
            else:
                minibuf+=line.strip()+" "
            if line.rstrip().endswith("::"):
                yield nodes.ParagraphNode(inline.parse_inline(minibuf,flags,state))
                minibuf=""
                depth=0
                within="icode"
                #NO reconsume
                continue
        elif within=="ul":
            if fence == {}:
                fence=line.lstrip()[0]
            elif not fence:
                fence=line.lstrip()[0]
                yield nodes.EmptyInterrupterNode()
            if isol(line):
                yield nodes.UlliNode(parse_block(minibuf,state,flags),depth,bullet=fence)
                minibuf=""
                #Don't reset depths
                within="ol"
                fence={}
                f.reconsume()
                continue
            elif ( (not line.strip()) and ( (f.peek_ahead()==None) or (not f.peek_ahead().strip()) or (f.peek_ahead()[0] not in (" ",fence)) or ("breaklists" in flags) ) ) or isrule(line):
                yield nodes.UlliNode(parse_block(minibuf,state,flags),depth,bullet=fence)
                minibuf=""
                depth=0
                depths=[]
                fence=None
                within="root"
                f.reconsume()
                continue
            elif isul(line):
                if minibuf:
                    yield nodes.UlliNode(parse_block(minibuf,state,flags),depth,bullet=fence)
                    minibuf=""
                if fence!=line.lstrip()[0]:
                    yield nodes.EmptyInterrupterNode()
                fence=line.lstrip()[0]
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
                minibuf+=line.lstrip()[1:].lstrip()
            else:
                minibuf+=line.lstrip().rstrip("\r\n")+"\n"
        elif within=="ol":
            if (fence!={}) and not fence:
                yield nodes.EmptyInterrupterNode()
            if isul(line):
                yield nodes.OlliNode(parse_block(minibuf,state,flags),depth,bullet=int(fence,10))
                minibuf=""
                #Don't reset depths
                within="ul"
                fence={}
                f.reconsume()
                continue
            # FIXME fence usage not the appropriate thing here
            elif ( (not line.strip()) and ( (f.peek_ahead()==None) or (not f.peek_ahead().strip()) or (f.peek_ahead()[0] not in (" ",fence)) or ("breaklists" in flags) ) ) or isrule(line):
                yield nodes.OlliNode(parse_block(minibuf,state,flags),depth,bullet=int(fence,10))
                minibuf=""
                depth=0
                depths=[]
                fence=None
                within="root"
                f.reconsume()
                continue
            elif isol(line):
                if minibuf:
                    yield nodes.OlliNode(parse_block(minibuf,state,flags),depth,bullet=int(fence,10))
                    minibuf=""
                fence=""
                for char in line.lstrip():
                    if char not in "0123456789":
                        break
                    fence+=char
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
                minibuf+=line.lstrip()[len(fence)+1:].lstrip()
            else:
                minibuf+=line.lstrip().rstrip("\r\n")+"\n"
        elif within=="rule":
            yield nodes.RuleNode()
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
                if ("noatxcode" not in flags):
                    within="atxcode"
                else:
                    within="root"
                f.reconsume()
                continue
            if line.strip() and (not line.startswith(" "*depth)):
                yield nodes.CodeBlockNode(minibuf,clas="::")
                minibuf=""
                depth=0
                fence=None
                within="root"
                f.reconsume()
                continue
            else:
                minibuf+=line[depth:].rstrip("\r\n")+"\n"
        elif within=="atxcode":
            if not line.strip():
                yield nodes.CodeBlockNode(minibuf,clas="::")
                minibuf=""
                depth=0
                fence=None
                within="root"
                f.reconsume()
                continue
            else:
                minibuf+=line.rstrip("\r\n")+"\n"
        elif within=="fence":
            if fence==None:
                fence=0
                depth=len(line)-len(line.lstrip())
                line=line.lstrip()
                fchar=line[0]
                while line[:1]==fchar:
                    fence+=1
                    line=line[1:]
                fenceinfo=line.strip()
                fence*=fchar
            elif all_same(line.strip()) and (fence in line):
                yield nodes.CodeBlockNode(minibuf,clas=fenceinfo)
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
                yield nodes.BlockQuoteNode(parse_block(minibuf,state,flags))
                minibuf=""
                within="root"
                f.reconsume()
                continue
        elif within=="spoiler":
            if issp(line) or (line.strip() and not iscb(line) and not isulin(line) and not isfence(line) and not isul(line) and not isheadatx(line) and not isbq(line)):
                line=line.lstrip()
                if line[:2]==">!":line=line[2:]
                if line[:1]==" ":line=line[1:]
                minibuf+=line.rstrip("\r\n")+"\n"
            else:
                yield nodes.BlockSpoilerNode(parse_block(minibuf,state,flags))
                minibuf=""
                within="root"
                f.reconsume()
                continue
        elif within=="directive":
            if line.strip() and (line != line.lstrip()) and (depth == 0):
                depth = len(line) - len(line.lstrip())
            # Not elif:
            if (not cellwid) and line.startswith(".. ") and ("::" in line):
                direname, direargs = line[3:].split("::",1)
                direfulfilled = 0
                depth = 0
                cellwid = [direargs.strip()]
            elif line.strip() and (depth > 0) and line[:depth].strip():
                yield from handle_directive()
                cellwid = []; cellrows = []
                minibuf=""
                within="root"
                depth = 0
                f.reconsume()
                continue
            elif (not direfulfilled) and (not line.strip()):
                direfulfilled = 1
            elif (not direfulfilled) and line.lstrip().startswith(":") and (":" in line.lstrip()[1:]):
                cellrows.append(list(map(str.strip, line.lstrip()[1:].split(":",1))))
            elif not direfulfilled:
                cellwid.append(line.strip())
            else:
                minibuf += line[depth:].rstrip("\r\n")+"\n"
        elif within=="tablerest":
            def validly(line,cellwid):
                for cell in cellwid:
                    line=line[cell:]
                    if line.strip() and line[0]!=" ":
                        return 0
                    line=line[1:]
                return 1
            def splice(line,cellwid):
                lines=[]
                for cell in cellwid:
                    lines.append(line[:cell].rstrip())
                    line=line[cell:]
                    line=line[1:] #Assume validity already tested
                return lines
            if (not cellwid) and (istablerest(line)):
                cellwid=list(map(len,line.strip().split(" ")))
                cellrows=[[],[]]
            elif (depth==0) and (not istablerest(line)) and validly(line,cellwid):
                cellrows[0].append(splice(line,cellwid))
            elif (depth==0) and (istablerest(line)):
                depth=1
            elif (depth==1) and (not istablerest(line)) and validly(line,cellwid):
                cellrows[1].append(splice(line,cellwid))
            else:
                cellrows2=[[],[]]
                for row in cellrows[0]:
                    if cellrows2[0] and (not row[0].strip()):
                        for n,i in enumerate(row):
                            if n>=len(cellrows2[0][-1]):
                                cellrows2[0][-1].append("")
                            cellrows2[0][-1][n]+="\n"+i
                    else:
                        cellrows2[0].append([])
                        cellrows2[0][-1].extend(row)
                for row in cellrows2[0]:
                    for i in range(len(row)):
                        row[i]=mdputil.normalise_child_nodes(list(parse_block(row[i],flags)))
                for row in cellrows[1]:
                    if cellrows2[1] and (not row[0].strip()):
                        for n,i in enumerate(row):
                            if n>=len(cellrows2[1][-1]):
                                cellrows2[1][-1].append("")
                            cellrows2[1][-1][n]+="\n"+i
                    else:
                        cellrows2[1].append([])
                        cellrows2[1][-1].extend(row)
                for row in cellrows2[1]:
                    for i in range(len(row)):
                        row[i]=mdputil.normalise_child_nodes(list(parse_block(row[i],flags)))
                yield nodes.TableNode(cellrows2)
                within="root"
                cellwid=[]
                cellrows=[]
                depth=0
                if (not istablerest(line)) or (not validly(line,cellwid)):
                    f.reconsume()
                continue
        elif within=="table":
            def splitcols(line):
                cols=[""]
                esc=0
                for char in line:
                    if esc==1:
                        cols[-1]+=char
                        esc=0
                    elif char=="\\":
                        esc=1
                        cols[-1]+=char
                    elif char=="|":
                        cols.append("")
                    else:
                        cols[-1]+=char
                if not cols[-1].strip(): cols[-1]=""
                return cols
            if depth:
                line=line.strip()
                if line.strip().startswith("|"):
                    line=line[1:]
                if line.strip().endswith("|"):
                    line=line[:-1]
            if (not cellwid) and (cellrows):
                cellwid=[( (((i.strip()[0]+i.strip()[-1])=="::") and "center") or ((i.strip()[0]==":") and "left") or ((i.strip()[-1]==":") and "right") or None ) for i in splitcols(line.strip())]
            elif not cellwid:
                depth=line.strip().startswith("|") and line.strip().endswith("|")
                if depth:
                    line=line.strip()[1:-1]
                cellrows=[[splitcols(line)],[]]
            elif len(splitcols(line))==len(cellwid):
                cellrows[1].append(splitcols(line))
            else:
                cellrows=[[[inline.parse_inline(k,flags,state) for k in j] for j in i] for i in cellrows]
                yield nodes.TableNode(cellrows,cellwid)
                within="root"
                cellwid=[]
                cellrows=[]
                depth=0
                f.reconsume()
                continue
        else:
            raise AssertionError("Unknown syntax feature %r"%within)
    ####
    if within=="directive":
        yield from handle_directive()
        cellwid = []; cellrows = []
        minibuf=""
        within="root"
    elif minibuf:
        if within=="fence":
            yield nodes.CodeBlockNode(minibuf,clas=fenceinfo)
            minibuf=""
            depth=0
            fence=None
            within="root"
        elif within in ("icode","atxcode"):
            yield nodes.CodeBlockNode(minibuf,clas="::")
            minibuf=""
            depth=0
            within="root"

def parse_block(content,state,flags=()):
    return _parse_block(LinestackIter(StringIO(content)),state,mdputil.flatten_flags_parser(flags))
