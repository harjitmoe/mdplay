__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

#TODO: delegate Emoji stuff into a separate module.

from mdplay import utfsupport, nodes, twem2support, pickups_util, eac
import collections

def utf16_ord(s):
    s = list(s)
    c = s.pop(0)
    if (0xD800 <= ord(c) < 0xDC00) and (0xDC00 <= ord(s[0]) < 0xE000):
        k = s.pop(0)
        index_from_smp = ((ord(c) - 0xD800) * 1024) + (ord(k) - 0xDC00)
        codepoint = 0x010000 + index_from_smp
        if s: raise ValueError("trailing data in utf16_ord argument")
        return codepoint
    else:
        if s: raise ValueError("trailing data in utf16_ord argument")
        return ord(c)

TWEM2 = {}
for i2 in twem2support.TWEM:
    i = tuple([utfsupport.unichr4all(int(j,16)) for j in i2.split("-")])
    if (len(i)>1) or (utf16_ord(i[0])>0xff): #No fancy copyright symbols here mate
        TWEM2[i] = i2

_nesting_defaultdict = lambda: collections.defaultdict(_nesting_defaultdict)

TWEMD = _nesting_defaultdict()
TWEMD[u"\U000FDECD"] = ":demonicduck:"

def _apply(lat, stack, fing):
    if len(stack)>1:
        return _apply(lat[stack[0]], stack[1:], fing)
    lat[stack[0]]["\x00"] = fing

for _twem in TWEM2.keys():
    _apply(TWEMD, _twem, TWEM2[_twem])

def emoji_scan(nodesz):
    nodesz2 = []
    for node in nodesz:
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
                ccc = node2.pop(0)
                node3 = node2[:]
                d = []
                c = ccc
                td = TWEMD
                while (node3) and (c in td):
                    d.append(c)
                    td = td[c]
                    c = node3.pop(0)
                if tuple(d) in TWEM2:
                    emojistyle = (c != u"\ufe0e")
                    nodesz2.append(out)
                    out = ""
                    node2 = node3
                    node2.insert(0, c)
                    hexcode = TWEM2[tuple(d)]
                    emoji = u"".join(d)
                    if not emojistyle:
                        emoji += u"\ufe0e"
                    asciimote = pickups_util.SMILEYS[emoji] if emoji in pickups_util.SMILEYS else None
                    uhexcode = hexcode.decode("latin1")
                    if uhexcode in eac.eac:
                        shortcode = eac.eac[uhexcode][u"alpha code"].encode("utf-8")
                    elif (u"-200d-" in uhexcode) or (u"-200c-" in uhexcode): # ZWJ and ZWNJ
                        uhexcodes = uhexcode.replace(u"-200d-", u"#200d#").replace(u"-200c-", u"#200c#").split(u"#")
                        shortcode = ""
                        for hexc in uhexcodes:
                            if hexc in eac.eac:
                                shortcode += eac.eac[hexc][u"alpha code"].encode("utf-8")
                            elif hexc == "200d":
                                shortcode += "&zwj;"
                            elif hexc == "200c":
                                shortcode += "&zwnj;"
                            else:
                                shortcode = None
                                break
                    else:
                        shortcode = None                        
                    nodesz2.append(nodes.EmojiNode(emoji.encode("utf-8"), (asciimote, shortcode, hexcode), emphatic = emojistyle))
                elif tuple(d) == (u"\U000FDECD",):
                    nodesz2.append(nodes.EmojiNode(u"".join(d).encode("utf-8"), (None, ":demonicduck:", None), emphatic = True))
                else:
                    out += ccc.encode("utf-8")
            if out:
                nodesz2.append(out)
        else:
            nodesz2.append(node)
    return nodesz2

def agglomerate(nodelist):
    """Given a list of nodes, fuse adjacent text nodes, and split emoji off into emoji nodes."""
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
_idded = {}
def newid(node):
    """Assign an unique ID to an object, or return the existing one if already assigned."""
    global _curid
    if id(node) not in _idded:
        _idded[id(node)] = _curid
        _curid += 1
    return _idded[id(node)]

def flatten_flags_parser(flags):
    """Given a list of parser flags (atomic or group), expand to a list of atomic parser flags."""
    out=[]
    for flag in flags:
        if flag == "strict":
            out.extend(flatten_flags_parser(["norest", "nospoilertag", "nowikitext",
                                  "noredditstyle", "nopandocstyle", "nospecialhrefs",
                                  "nodiacritic", "noemoticon", "noembedspoiler",
                                  "nocjk", "norubi", "nocomment"]))
        elif flag == "norest":
            out.extend(flatten_flags_parser(["noresthead", "nodicode", "noresttable"]))
        elif flag == "nowikitext":
            out.extend(flatten_flags_parser(["nowikihead", "nowikiemph", "nowikilinks"]))
        elif flag == "noredditstyle":
            out.extend(flatten_flags_parser(["noredditstylesuper", "noredditspoiler"]))
        elif flag == "nospoilertag":
            out.extend(flatten_flags_parser(["noblockspoiler", "noredditspoiler"]))
        elif flag == "nosetexthead":
            out.extend(flatten_flags_parser(["noplainsetexthead", "noresthead"]))
        elif flag == "notable":
            out.extend(flatten_flags_parser(["noresttable", "nomdtable"]))
        elif flag == "nosupersubscript":
            out.extend(flatten_flags_parser(["noredditstylesuper", "nopandocstyle"]))
        elif flag == "noemoticon":
            out.extend(flatten_flags_parser(["noasciiemoticon", "noshortcodeemoji"]))
        elif flag == "nocjk":
            out.extend(flatten_flags_parser(["noromkan", "nocangjie"]))
        else:
            out.append(flag)
    return list(set(out))

def simul_replace(a, b, c, d, e):
    """Simultaneously replace (b with c) and (d with e) in a, returning the result."""
    r = []
    for f in a.split(b):
        r.append(f.replace(d, e))
    return c.join(r)

