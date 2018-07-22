__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

# Deal with all features that should be treated identically whatever weird and wonderful way they
# were escaped. Needless to say, none of these are Markdown syntax (as escaped data should be
# literal from a Markdown perspective) but may regard Unicode emoji and control characters and
# their ilk.

from mdplay.emoji import emoji_scan
from mdplay import nodes, interwiki

def agglomerate(nodelist): # From mdputil.py
    """Given a list of nodes, fuse adjacent text nodes."""
    outlist = []
    for i in nodelist:
        if isinstance(i,type("")) and outlist and isinstance(outlist[-1],type("")):
            outlist[-1] += i
        else:
            outlist.append(i)
    return outlist 

def normalise_child_nodes(content): # From mdputil.py
    content = list(content)
    if len(content) == 1 and isinstance(content[0], nodes.ParagraphNode):
        return content[0].content
    else:
        return agglomerate(interprocess_nodes(emoji_scan(agglomerate(content))))

def _interprocess_string(content, levs = ("root",), flags = (), state = None):
    # Note: the recursion works by the list being a Python
    # mutable, "passed by reference" as it were
    lastchar = " "
    out = []
    out2 = []
    lev = levs[0]
    while content:
        c = content.pop(0)
        if c=="\u001b" and content and (0x40 <= ord(content[0]) < 0x60):
            # Normalise ESC sequences to C1 sequences where applicable.
            c = chr(ord(content.pop(0)) + 0x40)
        #
        # Convert ANSI-escape rubi to Unicode rubi.
        # Todo: should this really require the backslashes to be escaped as it does now (edits to
        # inline.py would be needed to change this)? Allowing the ESC or CSI to be an entity and
        # still allowing the backslash to be unescaped would be prohibitively convoluted, so likely
        # it shouldn't.
        if c == "\x9b" and content[1:] and (content[0] == "1") and (content[1] == "\\"):
            c = "\ufff9"
            del content[:2]
        elif c == "\x9b" and content[1:] and (content[0] == "3") and (content[1] == "\\"):
            c = "\ufffa"
            del content[:2]
        elif c == "\x9b" and content[1:] and (content[0] == "4") and (content[1] == "\\"):
            c = "\ufffa"
            del content[:2]
        elif c == "\x9b" and content[1:] and (content[0] == "5") and (content[1] == "\\"):
            c = "\ufffb"
            del content[:2]
            content.insert(0, "\ufff9")
        elif c == "\x9b" and content[1:] and (content[0] == "0") and (content[1] == "\\"):
            c = "\ufffb"
            del content[:2]
        elif c == "\x9b" and content[1:] and (content[1] == "\\"):
            c = "\ufffb"
            content.pop(0)
        #
        ### Superscript ###
        if c=="\u008C" and (lev != "subuni") and ("noc1supersub" not in flags): # PLU
            out.append(nodes.SuperNode(_interprocess_string(content,("supuni",)+levs,flags=flags,state=state)))
        elif c=="\u008B" and (lev != "supuni") and ("noc1supersub" not in flags): # PLD
            out.append(nodes.SubscrNode(_interprocess_string(content,("subuni",)+levs,flags=flags,state=state)))
        elif ((c=="\u008B" and lev=="supuni") or (c=="\u008C" and lev=="subuni")) and ("noc1supersub" not in flags):
            return out
        ### Unicode-syntax Rubi and Furigana (mdplay.cjk handles the href-based syntaces) ###
        elif (c == "\ufff9") and ("norubi" not in flags):
            dat1 = list(_interprocess_string(content,("unirubimain",)+levs,flags=flags,state=state))
            dat2 = ""
            termina = dat1.pop()
            if termina == "\ufffa":
                dat2 = list(_interprocess_string(content,("unirubiannot",)+levs,flags=flags,state=state))
                dat2.pop()
            out.append(nodes.RubiNode(dat1, dat2))
        elif (c == "\ufffa") and (lev == "unirubimain"): # i.e. not if already in the annotation.
            out.append(c) # So we can tell if initial span broken with fffa or ended with fffb.
            return out
        elif (c == "\ufffb") and (lev.startswith("unirubi")):
            out.append(c) # So we can tell if initial span broken with fffa or ended with fffb.
            return out
        # TODO: SGR (CSI...m) sequences (CSI is \x9b by this point, already conv'd from \x1b[)
        else:
            lastchar = c
            out.append(c)
    return out

def interprocess_string(content, flags, state):
    return _interprocess_string(list(content) + [""], flags=flags, state=state)

def _interprocess_nodes(nodesz, flags, state):
    for node in nodesz:
        if type(node) == type(""):
            yield from interprocess_string(node, flags, state)
        elif isinstance(node, nodes.HrefNode):
            if node.content.lower().startswith("urn:x-interwiki:"): # Not .casefold here as trimming hard.
                c = node.content[len("urn:x-interwiki:"):]
                if ":" in c:
                    p, d = c.split(":", 1)
                    if p.casefold() in interwiki.interwikis:
                        node.content = interwiki.interwikis[p.casefold()].replace("$1", d)
            yield node
        else:
            yield node

interprocess_nodes = lambda nodesz, flags=(), state=None: list(_interprocess_nodes(nodesz, flags, state))

