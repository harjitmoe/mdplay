# -*- mode: python; coding: utf-8 -*-

import re

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay.eac import eac
from mdplay.pickups_util import SMILEYS
from mdplay.utfsupport import unichr4all
from mdplay import nodes

#Note that :D may come out as several things depending on
#Python's arbitrary dict ordering; not sure what is best
#option here.
SMILEYA=dict(zip(SMILEYS.values(),SMILEYS.keys()))

def is_emotic(s):
    for i in SMILEYA.keys():
        if s.startswith(i):
            return i
    return False

del SMILEYS[SMILEYA[":/"]]
del SMILEYA[":/"] # https://

eacd={"lenny":u"( ͡° ͜ʖ ͡° )","degdeg":u"( ͡° ͜ʖ ͡° )", "darkmoon":u"🌚","thefinger":u"🖕","ntr":u"🤘","blush":u"😳","wink":u"😉","happy":u"😊", "rolleyes":u"🙄","angry":u"😠","biggrin":u"😁","aw_yeah":u"😏","bigcry":u"😭","evil":u"👿", "twisted":u"😈","sasmile":u"😈","tongue":u"😝","sleep":u"😴","conf":u"😕","confused":u"😕", "eek":u"😲","cry":u"😢","sweat1":u"😅","worshippy":u"🙇","wub":u"😍","mellow":u"😐", "shifty":u"👀","eyes":u"👀","demonicduck":u"󽻍","shruggie":u"¯\_(ツ)_/¯", "textstyle":u"\ufe0e","emojistyle":u"\ufe0f"}
eacdr=dict(zip(eacd.values(),eacd.keys()))
for _euc in eac.keys():
    _ec=u""
    for _eucs in _euc.split("-"):
        _ec+=unichr4all(int(_eucs,16))
    eacd[eac[_euc]["alpha code"].strip(":").encode("utf-8")]=_ec
    eacdr[_ec]=eac[_euc]["alpha code"].strip(":").encode("utf-8")
    for _alias in eac[_euc]["aliases"]:
        eacd[_alias.strip(":")]=_ec

def emoji_handler(out, c, content, levs, flags):
    ### Emoticons and Emoji ###
    if re.match(r":(\w|_|-)+:",c+("".join(content))) and ("noshortcodeemoji" not in flags):
        kwontenti=""
        c=content.pop(0)
        while (c!=":"):
            kwontenti+=c
            c=content.pop(0)
        kwontent=kwontenti
        if kwontent.startswith("icon_"): #Is this one always okay?
            kwontent=kwontent[5:]
        elif kwontent.startswith("eusa_"):
            kwontent=kwontent[5:]
        elif kwontent.startswith("dan_"):
            kwontent=kwontent[4:] 
        if kwontent in eacd: 
            emoji=eacd[kwontent.decode("utf-8")]
            out.append(emoji)
        else:
            out.append(":"+kwontenti+":")
        return True
    elif is_emotic(c+("".join(content))) and ("noasciiemoticon" not in flags):
        emote=is_emotic(c+("".join(content)))
        for iii in range(len(emote)-1): #Already popped the first (to c)!
            content.pop(0)
        emoji=SMILEYA[emote].encode("utf-8")
        out.append(emoji)
        return True
    else:
        return False







