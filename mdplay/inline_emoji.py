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
from mdplay.twem2support import TWEM2, TWEM3, TWEM4
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

def fusion_check(do_fuse, nodo):
    # Note: this will probably bork on narrow (Windows)!
    tupl = tuple(nodo.content.decode("utf-8"))
    while do_fuse:
        tupl = tuple(do_fuse.content.decode("utf-8")) + tupl
        do_fuse = do_fuse.fyzi
    return (tupl in TWEM4) or (tupl in TWEM2)

def emoji_handler(out, c, content, levs, do_fuse, dfstate, flags):
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
            if emoji in SMILEYS:
                emote=SMILEYS[emoji]
            else:
                emote=":"+kwontenti+":"
            nodo=nodes.EmojiNode(emoji.encode("utf-8"), (emote, kwontenti), "shortcode")
            out.append(nodo)
            if do_fuse!=None:
                if fusion_check(do_fuse, nodo):
                    do_fuse.fuse=nodo
                    nodo.fyzi=do_fuse
                elif emoji == u"\ufe0e":
                    do_fuse.force_text=1
            do_fuse=nodo
            dfstate=1
        else:
            out.append(":"+kwontenti+":")
    elif is_emotic(c+("".join(content))) and ("noasciiemoticon" not in flags):
        emote=is_emotic(c+("".join(content)))
        for iii in range(len(emote)-1): #Already popped the first (to c)!
            content.pop(0)
        emoji=SMILEYA[emote].encode("utf-8")
        shortcode=None
        if emoji in eacdr:
            shortcode=eacdr[emoji]
        nodo=nodes.EmojiNode(emoji, (emote, shortcode), "ascii")
        out.append(nodo) 
        if do_fuse!=None:
            if fusion_check(do_fuse, nodo):
                do_fuse.fuse=nodo
                nodo.fyzi=do_fuse
            elif emoji.decode("utf-8") == u"\ufe0e":
                do_fuse.force_text=1
        do_fuse=nodo
        dfstate=1
    elif ((c.decode("utf-8") in TWEM3) or (c.decode("utf-8") in (u"\U000FDECD",u"\ufe0e"))) and ("label" not in levs):
        emoji=c.decode("utf-8")
        if emoji in eacdr:
            shortcode=eacdr[emoji]
        else:
            shortcode=None
        emote=":unnamed:"
        if emoji in SMILEYS:
            emote=SMILEYS[emoji]
        elif shortcode:
            emote=":"+shortcode+":"
        nodo=nodes.EmojiNode(c, (emote, shortcode), "verbatim")
        out.append(nodo) 
        if do_fuse!=None:
            if fusion_check(do_fuse, nodo):
                do_fuse.fuse=nodo
                nodo.fyzi=do_fuse
            elif emoji == u"\ufe0e":
                do_fuse.force_text=1
        do_fuse=nodo
        dfstate=1
    else:
        return False
    return (do_fuse, dfstate)
