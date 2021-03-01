# -*- mode: python; coding: utf-8 -*-

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay.emoji import twem2support, eac, emoticon
from mdplay import mdputil, nodes, uriregex
import collections, re, os, pprint

#-------------------------------------------------------------------------------------------------

eacd2 = {
"lenny": "( ͡° ͜ʖ ͡° )", "degdeg": "( ͡° ͜ʖ ͡° )", "shruggie": "¯\_(ツ)_/¯", "kome": "※",

"darkmoon": "🌚", "thefinger": "🖕", "happy":"😊", "rolleyes": "🙄", "biggrin": "😁", "aw_yeah": "😏", "bigcry": "😭", "evil": "👿", "twisted": "😈", "sasmile": "😈", "sleep": "😴", "conf": "😕", "eek": "😲", "sweat1": "😅", "worshippy": "🙇", "wub": "😍", "mellow": "😐", "shifty": "👀", "danshiftyeyes": "👀", 

"textstyle": "\ufe0e", "emojistyle": "\ufe0f"
}

# Converting eac hexcodes to twemoji hexcodes where needed.
twmf = os.path.join(os.path.dirname(__file__), "twemmap.py")
if os.path.exists(twmf):
    from mdplay.emoji.twemmap import TWEMmap
else:
    TWEMmap = {}
    for i2 in twem2support.TWEM:
        i = "-"+i2+"-"
        i = i.replace("-200c-", "-")
        i = i.replace("-200d-", "-")
        i = i.replace("-fe0e-", "-")
        i = i.replace("-fe0f-", "-")
        i = i.strip("-")
        if i != i2:
            TWEMmap[i] = i2
    open(twmf, "w").write("TWEMmap = " + pprint.pformat(TWEMmap))

# Generating shortcode-to-unicode mapping.
eacdf = os.path.join(os.path.dirname(__file__), "eacd.py")
eacaf = os.path.join(os.path.dirname(__file__), "eacalt.py")
if os.path.exists(eacdf) and os.path.exists(eacaf):
    from mdplay.emoji.eacd import eacd
    from mdplay.emoji.eacalt import eacalt
else:
    eacd = eacd2.copy()
    eacalt = {}
    for _euc in list(eac.eac.keys()):
        _ec = ""
        _euc2 = _euc
        if _euc2 in TWEMmap:
            _euc2 = TWEMmap[_euc2]
            eacalt[TWEMmap[_euc]] = eac.eac[_euc]
        else:
            eacalt[_euc] = eac.eac[_euc]
        for _eucs in _euc2.split("-"):
            _ec += mdputil.unichr4all(int(_eucs, 16))
        eacd[eac.eac[_euc]["alpha code"].strip(":")] = _ec
        for _alias in eac.eac[_euc]["aliases"].split("|"):
            eacd[_alias.strip(":")] = _ec
    open(eacdf, "w", encoding="utf-8").write("eacd = " + pprint.pformat(eacd))
    open(eacaf, "w", encoding="utf-8").write("eacalt = " + pprint.pformat(eacalt))

#-------------------------------------------------------------------------------------------------

def _utf16_ord(s):
    s = list(s)
    c = s.pop(0)
    if (0xD800 <= ord(c) < 0xDC00) and (0xDC00 <= ord(s[0]) < 0xE000):
        k = s.pop(0)
        index_from_smp = ((ord(c) - 0xD800) * 1024) + (ord(k) - 0xDC00)
        codepoint = 0x010000 + index_from_smp
        if s: raise ValueError("trailing data in _utf16_ord argument")
        return codepoint
    else:
        if s: raise ValueError("trailing data in _utf16_ord argument")
        return ord(c)

TWEM2 = {}
for i2 in twem2support.TWEM:
    i = tuple([mdputil.unichr4all(int(j,16)) for j in i2.split("-")])
    if (len(i)>1) or (_utf16_ord(i[0])>0xff): #No fancy copyright symbols here mate
        TWEM2[i] = i2

_nesting_defaultdict = lambda: collections.defaultdict(_nesting_defaultdict)

TWEMD = _nesting_defaultdict()
TWEMD["\U000FDECD"] = ":demonicduck:"

def _apply(lat, stack, fing):
    if len(stack)>1:
        return _apply(lat[stack[0]], stack[1:], fing)
    lat[stack[0]]["\x00"] = fing

for _twem in list(TWEM2.keys()):
    _apply(TWEMD, _twem, TWEM2[_twem])

#-------------------------------------------------------------------------------------------------

def _emoji_scan(nodesz):
    """Remove Unicode emoji from text nodes to dedicated EmojiNode nodes."""
    for node in nodesz:
        if type(node) == type(""):
            node2 = list(node)
            out = ""
            while node2:
                ccc = node2.pop(0)
                node3 = node2[:]
                d = []
                c = ccc
                td = TWEMD
                while c in td:
                    d.append(c)
                    td = td[c]
                    if node3:
                        c = node3.pop(0)
                    else:
                        c = ""
                        break
                if tuple(d) in TWEM2:
                    emojistyle = (c != "\ufe0e")
                    yield out
                    out = ""
                    node2 = node3
                    node2.insert(0, c)
                    hexcode = TWEM2[tuple(d)]
                    emoji = "".join(d)
                    if not emojistyle:
                        emoji += "\ufe0e"
                    asciimote = emoticon.SMILEYS[emoji] if emoji in emoticon.SMILEYS else None
                    uhexcode = hexcode
                    uuhexcode = "-" + uhexcode + "-"
                    if uhexcode in eacalt:
                        shortcode = eacalt[uhexcode]["alpha code"]
                    elif ("-200d-" in uuhexcode) or ("-200c-" in uuhexcode) or ("-fe0e-" in uuhexcode) or ("-fe0f-" in uuhexcode):
                        uhexcodes = uuhexcode.replace("-200d-", "#200d#").replace("-200c-", "#200c#").replace("-fe0e-", "#fe0e#").replace("-fe0f-", "#fe0f#").strip("#-").split("#")
                        shortcode = ""
                        for hexc in uhexcodes:
                            if hexc in eacalt:
                                shortcode += eacalt[hexc]["alpha code"]
                            elif hexc == "200d":
                                shortcode += "&zwj;"
                            elif hexc == "200c":
                                shortcode += "&zwnj;"
                            elif hexc == "fe0e":
                                shortcode += ":textstyle:"
                            elif hexc == "fe0f":
                                shortcode += ":emojistyle:"
                            else:
                                shortcode = None
                                break
                    else:
                        shortcode = None                        
                    yield nodes.EmojiNode(emoji, (asciimote, shortcode, hexcode), emphatic = emojistyle)
                else:
                    out += ccc
            if out:
                yield out
        else:
            yield node

emoji_scan = lambda nodesz: list(_emoji_scan(nodesz))

#-------------------------------------------------------------------------------------------------

def _emoteid_to_url(s):
    if ":" in s: # i.e. probably URI and not a number
        return s
    else:
        return "https://cdn.discordapp.com/emojis/" + s + ".png"

def _is_emotic(s):
    for i in list(SMILEYA.keys()):
        if s.startswith(i):
            return i
    return False

def emote_handler(tag, inner):
    """Handle ASCII emoticons and shortcodes, converting as appropriate."""
    zw = "\u200c" # Insert zero-width char as round-trip kludge.
    ### Emoticons and Emoji ###
    if tag == "shortcode":
        assert len(inner) == 1
        code = inner[0]
        assert code[0] == code[-1] == ":"
        alphaname = code[1:-1]
        alpha_alt_text = ":" + zw + alphaname + ":"
        alphaname_lookup = alphaname
        # Strip certain prefixes, added here mainly for (pre-Crash) 910 compatibility
        if alphaname_lookup.startswith("icon_"):
            alphaname_lookup = alphaname_lookup[5:]
        elif alphaname_lookup.startswith("eusa_"):
            alphaname_lookup = alphaname_lookup[5:]
        elif alphaname_lookup.startswith("dan_"):
            alphaname_lookup = alphaname_lookup[4:] 
        if alphaname_lookup in eacd: 
            return eacd[alphaname_lookup]
        #elif alphaname_lookup in state.custom_eac:
        #    emoteurl = _emoteid_to_url(state.custom_eac[alphaname_lookup])
        #    out.append(nodes.HrefNode(emoteurl, alpha_alt_text, "img", width = 32))
        else:
            return code # Pass through, i.e. do NOT use colon_then_wj
    elif False:
        alphaname = ""
        emoteid = ""
        del content[0] # the <
        c = content.pop(0)
        while (c != ":"):
            alphaname += c
            c = content.pop(0)
        alt_text = ":" + zw + alphaname + ":"
        c = content.pop(0)
        while (c != ">"):
            emoteid += c
            c = content.pop(0)
        emoteurl = _emoteid_to_url(emoteid) # id is not a URL here as regex enforces numerical
        if alphaname not in eacd:
            state.custom_eac[alphaname] = emoteurl # could alternatively use emoteid I suppose
        out.append(nodes.HrefNode(emoteurl, alt_text, "img", width = 32))
        return True
    return None

#-------------------------------------------------------------------------------------------------

if __name__=="__main__":
    for _euc in list(eac.eac.keys()):
        unit = eac.eac[_euc]
        az = [unit["alpha code"].strip(":")]
        az.extend([a.strip(":") for a in unit["aliases"]])
        for a in az:
            if a in eacd2:
                print(("%s %s" % (a, "overdefined")))
            elif a.startswith("icon_") or a.startswith("dan_") or a.startswith("eusa_"):
                print(("%s %s" % (a, "currently inaccessible")))
