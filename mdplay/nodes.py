#Increasingly a misnomer.

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
        self.content=content
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

from mdplay import utfsupport
from mdplay.twem2support import TWEM
from mdplay.eac import eac
from mdplay.pickups_util import SMILEYS

TWEM2 = {}
for i2 in TWEM:
    i = tuple([utfsupport.unichr4all(int(j,16)) for j in i2.split("-")])
    if (len(i)>1) or (utf16_ord(i[0])>0xff): #No fancy copyright symbols here mate
        TWEM2[i] = i2

from collections import defaultdict

_defaultdictception = lambda:defaultdict(_defaultdictception)

TWEMD = _defaultdictception()
TWEMD[u"\U000FDECD"] = ":demonicduck:"

def _apply(lat, stack, fing):
    if len(stack)>1:
        return _apply(lat[stack[0]], stack[1:], fing)
    lat[stack[0]]["\x00"] = fing

for _twem in TWEM2.keys():
    _apply(TWEMD, _twem, TWEM2[_twem])

def emoji_scan(nodes):
    nodesz2 = []
    for node in nodes:
        if type(node) == type(""):
            node = list(node.decode("utf8"))
            node2 = []
            while node:
                c = node.pop(0)
                if (0xD800<=ord(c)<0xDC00) and node and (0xDC00<=ord(node[0])<0xE000):
                    c += node.pop(0)
                node2.append(c)
            out = ""
            while node2:
                c = node2.pop(0)
                node3 = node2[:]
                d = []
                td = TWEMD
                while (node3) and (c in td):
                    d.append(c)
                    td = td[c]
                    c = node3.pop(0)
                if tuple(d) in TWEM2:
                    if c != u"\ufe0e":
                        nodesz2.append(out)
                        out = ""
                        node2 = node3
                        node2.insert(0, c)
                        hexcode = TWEM2[tuple(d)]
                        emoji = u"".join(d)
                        shortcode = eac[hexcode.decode("latin1")]["alpha code"] if hexcode in eac else None
                        asciimote = SMILEYS[emoji] if emoji in SMILEYS else None
                        nodesz2.append(EmojiNode(emoji.encode("utf-8"), (asciimote, shortcode, hexcode)))
                    else:
                        out += (u"".join(d) + c).encode("utf-8")
                elif tuple(d) == (u"\U000FDECD",):
                    nodesz2.append(EmojiNode(u"".join(d).encode("utf-8"), (None, ":demonicduck:", None)))
                else:
                    out += c.encode("utf-8")
            if out:
                nodesz2.append(out)
        else:
            nodesz2.append(node)
    return nodesz2

def agglomerate(nodelist):
    outlist=[]
    for i in nodelist:
        #NOTE: assumes Python 2
        if isinstance(i,type(u"")):
            i=i.encode("utf-8")
        if isinstance(i,type("")) and outlist and isinstance(outlist[-1],type("")): #NOT elif
            outlist[-1]+=i
        else:
            outlist.append(i)
    return emoji_scan(outlist)

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
            out.extend(flatten_flags_parser(["norest","nospoilertag","nowikitext",
                                  "noredditstyle","nopandocstyle","nospecialhrefs",
                                  "nodiacritic","noemoticon","noembedspoiler",
                                  "nocjk","norubi","nocomment"]))
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

def simul_replace(a, b, c, d, e):
    r = []
    for f in a.split(b):
        r.append(f.replace(d, e))
    return c.join(r)
