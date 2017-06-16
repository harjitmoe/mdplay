# -*- mode: python; coding: utf-8 -*-

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay.emoji import twem2support, pickups_util, eac
from mdplay import utfsupport, nodes
import collections, re, os

#-------------------------------------------------------------------------------------------------

SMILEYA = dict(zip(pickups_util.SMILEYS.values(), pickups_util.SMILEYS.keys()))
del SMILEYA[":/"] # https://
SMILEYA[":D"] = u"😆" # Otherwise implementation-defined behaviour (multiple mapped to :D in SMILEYS)

#-------------------------------------------------------------------------------------------------

eacd2 = {
"lenny": u"( ͡° ͜ʖ ͡° )", "degdeg": u"( ͡° ͜ʖ ͡° )", "shruggie": u"¯\_(ツ)_/¯", 

"darkmoon": u"🌚", "thefinger": u"🖕", "happy":u"😊", "rolleyes": u"🙄", "biggrin": u"😁", "aw_yeah": u"😏", "bigcry": u"😭", "evil": u"👿", "twisted": u"😈", "sasmile": u"😈", "sleep": u"😴", "conf": u"😕", "eek": u"😲", "sweat1": u"😅", "worshippy": u"🙇", "wub": u"😍", "mellow": u"😐", "shifty": u"👀", "danshiftyeyes": u"👀", 

"textstyle": u"\ufe0e", "emojistyle": u"\ufe0f"
}

custom_eac = {"demonicduck": "http://i.imgur.com/SfHfed9.png"}

# Converting eac hexcodes to twemoji hexcodes where needed.
twmf = os.path.join(os.path.dirname(__file__), "twemmap.py")
if os.path.exists(twmf):
    from mdplay.emoji.twemmap import TWEMmap
else:
    TWEMmap = {}
    for i2 in twem2support.TWEM:
        if i2 not in eac.eac:
            i = "-"+i2+"-"
            i = i.replace("-200c-", "-")
            i = i.replace("-200d-", "-")
            i = i.replace("-fe0e-", "-")
            i = i.replace("-fe0f-", "-")
            i = i.strip("-")
            if i in eac.eac:
                TWEMmap[i] = i2
    open(twmf, "w").write("TWEMmap = " + repr(TWEMmap))

# Generating shortcode-to-unicode mapping.
eacdf = os.path.join(os.path.dirname(__file__), "eacd.py")
eacaf = os.path.join(os.path.dirname(__file__), "eacalt.py")
if os.path.exists(eacdf) and os.path.exists(eacaf):
    from mdplay.emoji.eacd import eacd
    from mdplay.emoji.eacalt import eacalt
else:
    eacd = eacd2.copy()
    eacalt = {}
    for _euc in eac.eac.keys():
        _ec = u""
        _euc2 = _euc
        if _euc2 in TWEMmap:
            _euc2 = TWEMmap[_euc2]
            eacalt[TWEMmap[_euc]] = eac.eac[_euc]
        else:
            eacalt[_euc] = eac.eac[_euc]
        for _eucs in _euc2.split("-"):
            _ec += utfsupport.unichr4all(int(_eucs, 16))
        eacd[eac.eac[_euc]["alpha code"].strip(":").encode("utf-8")] = _ec
        for _alias in eac.eac[_euc]["aliases"]:
            eacd[_alias.strip(":").encode("utf-8")] = _ec
    open(eacdf, "w").write("eacd = " + repr(eacd))
    open(eacaf, "w").write("eacalt = " + repr(eacalt))

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
    i = tuple([utfsupport.unichr4all(int(j,16)) for j in i2.split("-")])
    if (len(i)>1) or (_utf16_ord(i[0])>0xff): #No fancy copyright symbols here mate
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

#-------------------------------------------------------------------------------------------------

def emoji_scan(nodesz):
    nodesz2 = []
    for node in nodesz:
        if type(node) == type(""):
            node = list(node.decode("utf8"))
            node2 = []
            while node:
                # Grumble grumble Windows grumble
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
                    uuhexcode = u"-" + uhexcode + u"-"
                    if uhexcode in eacalt:
                        shortcode = eacalt[uhexcode][u"alpha code"].encode("utf-8")
                    elif (u"-200d-" in uuhexcode) or (u"-200c-" in uuhexcode) or (u"-fe0e-" in uuhexcode) or (u"-fe0f-" in uuhexcode):
                        uhexcodes = uuhexcode.replace(u"-200d-", u"#200d#").replace(u"-200c-", u"#200c#").replace(u"-fe0e-", u"#fe0e#").replace(u"-fe0f-", u"#fe0f#").strip("#-").split(u"#")
                        shortcode = ""
                        for hexc in uhexcodes:
                            if hexc in eacalt:
                                shortcode += eacalt[hexc][u"alpha code"].encode("utf-8")
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
                    nodesz2.append(nodes.EmojiNode(emoji.encode("utf-8"), (asciimote, shortcode, hexcode), emphatic = emojistyle))
                else:
                    out += ccc.encode("utf-8")
            if out:
                nodesz2.append(out)
        else:
            nodesz2.append(node)
    return nodesz2

#-------------------------------------------------------------------------------------------------

def _emoteid_to_url(s):
    if "://" in s:
        return s
    else:
        return "https://cdn.discordapp.com/emojis/" + s + ".png"

def _is_emotic(s):
    for i in SMILEYA.keys():
        if s.startswith(i):
            return i
    return False

def emoji_handler(out, c, content, levs, flags):
    colon_then_wj = u":\u2060".encode("utf-8") # Insert a Word Joiner as round-trip kludge.
    ### Emoticons and Emoji ###
    if re.match(r":(\w|_|-)+:", c + ("".join(content))) and ("noshortcodeemoji" not in flags):
        alphaname = ""
        c = content.pop(0)
        while (c != ":"):
            alphaname += c
            c = content.pop(0)
        alpha_alt_text = colon_then_wj + alphaname + ":"
        alphaname_lookup = alphaname
        # Strip certain prefixes, added here mainly for (pre-Crash) 910 compatibility
        if alphaname_lookup.startswith("icon_"):
            alphaname_lookup = alphaname_lookup[5:]
        elif alphaname_lookup.startswith("eusa_"):
            alphaname_lookup = alphaname_lookup[5:]
        elif alphaname_lookup.startswith("dan_"):
            alphaname_lookup = alphaname_lookup[4:] 
        if alphaname_lookup in eacd: 
            emoji = eacd[alphaname_lookup.decode("utf-8")].encode("utf-8")
            out.append(emoji)
        elif alphaname_lookup in custom_eac: # Note: AFTER checking for a standard emoji.
            emoteurl = _emoteid_to_url(custom_eac[alphaname_lookup])
            out.append(nodes.HrefNode(emoteurl, alpha_alt_text, "img", width = 32, height = 32))
        else:
            out.append(":"+alphaname+":") #TODO do this more elegantly
        return True
    elif re.match(r"<:(\w|_|-)+:\d+>", c + ("".join(content))) and ("nodiscordemotes" not in flags):
        alphaname = ""
        emoteid = ""
        del content[0] # the <
        c = content.pop(0)
        while (c != ":"):
            alphaname += c
            c = content.pop(0)
        alt_text = colon_then_wj + alphaname + ":"
        c = content.pop(0)
        while (c != ">"):
            emoteid += c
            c = content.pop(0)
        emoteurl = _emoteid_to_url(emoteid) # id is not a URL here as regex enforces numerical
        if (alphaname not in custom_eac) and (alphaname not in eacd):
            # Well now you know (for it it's referenced later)
            custom_eac[alphaname] = emoteurl # could alternatively use emoteid I suppose
        out.append(nodes.HrefNode(emoteurl, alt_text, "img", width = 32, height = 32))
        return True
    elif _is_emotic(c + ("".join(content))) and ("noasciiemoticon" not in flags):
        emote = _is_emotic(c + ("".join(content)))
        for iii in range(len(emote)-1): #Already popped the first (to c)!
            content.pop(0)
        emoji = SMILEYA[emote].encode("utf-8")
        out.append(emoji)
        return True
    else:
        return False

#-------------------------------------------------------------------------------------------------

if __name__=="__main__":
    for _euc in eac.eac.keys():
        unit = eac.eac[_euc]
        az = [unit["alpha code"].strip(":").encode("utf-8")]
        az.extend([a.strip(":").encode("utf-8") for a in unit["aliases"]])
        for a in az:
            if a in eacd2:
                print ("%s %s" % (a, "overdefined"))
            elif a.startswith("icon_") or a.startswith("dan_") or a.startswith("eusa_"):
                print ("%s %s" % (a, "currently inaccessible"))
