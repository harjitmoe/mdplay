__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

def agglomerate(nodelist):
    """Given a list of nodes, fuse adjacent text nodes."""
    outlist = []
    for i in nodelist:
        #NOTE: assumes Python 2
        if isinstance(i,type(u"")):
            i = i.encode("utf-8")
        if isinstance(i,type("")) and outlist and isinstance(outlist[-1],type("")): #NOT elif
            outlist[-1] += i
        else:
            outlist.append(i)
    return outlist

def normalise_child_nodes(content):
    from mdplay import emoji, nodes
    if len(content) == 1 and isinstance(content[0], nodes.ParagraphNode):
        return content[0].content
    else:
        return emoji.emoji_scan(agglomerate(content))

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

