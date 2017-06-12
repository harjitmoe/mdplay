# -*- mode: python; coding: utf-8 -*-
"""Parse alphacodes/shortcodes and asciimotes to Unicode.

Does not create EmojiNode nodes, as these can be multiple-character
(ZWJ and combining characters), and are therefore best handled after
all emoji are convered to Unicode already.  Hence the current code
for creation of EmojiNode nodes is in mdputil.py"""

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

# "That one with all the verbatim unicode."
# Yeeeeah, should I change all those to escapes for consistency?

from mdplay import eac, utfsupport, pickups_util, mdputil
import re

SMILEYA = dict(zip(pickups_util.SMILEYS.values(), pickups_util.SMILEYS.keys()))
del SMILEYA[":/"] # https://
SMILEYA[":D"] = u"😆" # Make it non-implementation-defined behaviour at any rate.

def is_emotic(s):
    for i in SMILEYA.keys():
        if s.startswith(i):
            return i
    return False

# Some of these are for compatibility with (former) 910, some are custom.
# Run this module (python -m mdplay.inline_emoji) to test for overdefinition / collision with mdplay.eac
#
eacd={"lenny": u"( ͡° ͜ʖ ͡° )", "degdeg": u"( ͡° ͜ʖ ͡° )", "darkmoon": u"🌚", "thefinger": u"🖕", "happy":u"😊", "rolleyes": u"🙄", "biggrin": u"😁", "aw_yeah": u"😏", "bigcry": u"😭", "evil": u"👿", "twisted": u"😈", "sasmile": u"😈", "sleep": u"😴", "conf": u"😕", "eek": u"😲", "sweat1": u"😅", "worshippy": u"🙇", "wub": u"😍", "mellow": u"😐", "shifty": u"👀", "danshiftyeyes": u"👀", "demonicduck": u"󽻍", "shruggie": u"¯\_(ツ)_/¯", "textstyle": u"\ufe0e", "emojistyle": u"\ufe0f"}

eacd2 = eacd.copy()

for _euc in eac.eac.keys():
    _ec = u""
    _euc2 = _euc
    if _euc2 in mdputil.TWEMmap:
        _euc2 = mdputil.TWEMmap[_euc2]
    for _eucs in _euc2.split("-"):
        _ec += utfsupport.unichr4all(int(_eucs, 16))
    eacd[eac.eac[_euc]["alpha code"].strip(":").encode("utf-8")] = _ec
    for _alias in eac.eac[_euc]["aliases"]:
        eacd[_alias.strip(":").encode("utf-8")] = _ec

def emoji_handler(out, c, content, levs, flags):
    ### Emoticons and Emoji ###
    if re.match(r":(\w|_|-)+:", c + ("".join(content))) and ("noshortcodeemoji" not in flags):
        kwontenti = ""
        c = content.pop(0)
        while (c != ":"):
            kwontenti += c
            c = content.pop(0)
        kwontent = kwontenti
        if kwontent.startswith("icon_"):
            kwontent = kwontent[5:]
        elif kwontent.startswith("eusa_"):
            kwontent = kwontent[5:]
        elif kwontent.startswith("dan_"):
            kwontent = kwontent[4:] 
        if kwontent in eacd: 
            emoji = eacd[kwontent.decode("utf-8")]
            out.append(emoji)
        else:
            out.append(":"+kwontenti+":")
        return True
    elif is_emotic(c + ("".join(content))) and ("noasciiemoticon" not in flags):
        emote = is_emotic(c + ("".join(content)))
        for iii in range(len(emote)-1): #Already popped the first (to c)!
            content.pop(0)
        emoji = SMILEYA[emote].encode("utf-8")
        out.append(emoji)
        return True
    else:
        return False

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


