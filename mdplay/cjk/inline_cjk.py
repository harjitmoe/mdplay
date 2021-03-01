# -*- mode: python; coding: utf-8 -*-

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay.cjk import cangjie, parse_roma, fullwidth
from mdplay import nodes

def cjk_handler(hreftype, href, label):
    if hreftype.lower() in ("cang", "cangjie", "souketsu", "soketsu"):
        kanji = cangjie.proc_cang(href, -1)
        #print `kanji`, `label`
        if label:
            return nodes.RubiNode([kanji], label)
        else:
            return kanji
    elif hreftype.lower() in ("cang3", "cangjie3", "souketsu3", "soketsu3"):
        kanji = cangjie.proc_cang(href, 3)
        #print `kanji`, `label`
        if label:
            return nodes.RubiNode([kanji], label)
        else:
            return kanji
    elif hreftype.lower() in ("cang5", "cangjie5", "souketsu5", "soketsu5"):
        kanji = cangjie.proc_cang(href, 5)
        if label:
            return nodes.RubiNode([kanji], label)
        else:
            return kanji
    elif hreftype.lower() in ("kana",):
        kana = parse_roma.kanafy(href)
        if label:
            return nodes.RubiNode([kana], label)
        else:
            return kana
    elif hreftype.lower() in ("kkana", "katakana"):
        kana = parse_roma.kataise(parse_roma.kanafy(href))
        if label:
            return nodes.RubiNode([kana], label)
        else:
            return kana
    elif hreftype.lower() in ("hkana", "hgana", "hiragana"):
        kana = parse_roma.hiraise(parse_roma.kanafy(href))
        if label:
            return nodes.RubiNode([kana], label)
        else:
            return kana
    elif hreftype.lower() in ("kana_hbn",):
        kana = parse_roma.kanafy(href, "hepburn")
        if label:
            return nodes.RubiNode([kana], label)
        else:
            return kana
    elif hreftype.lower() in ("kkana_hbn", "katakana_hepburn"):
        kana = parse_roma.kataise(parse_roma.kanafy(href, "hepburn"))
        if label:
            return nodes.RubiNode([kana], label)
        else:
            return kana
    elif hreftype.lower() in ("hkana_hbn", "hgana_hbn", "hiragana_hepburn"):
        kana = parse_roma.hiraise(parse_roma.kanafy(href, "hepburn"))
        if label:
            return nodes.RubiNode([kana], label)
        else:
            return kana
    elif hreftype.lower() in ("fullwidth",):
        fw = fullwidth.to_fullwidth(href)
        if label:
            return nodes.RubiNode([fw], label)
        else:
            return fw
    elif hreftype.lower() in ("rubi", "ruby", "furi"):
        return nodes.RubiNode([href], label)
    else:
        return None
    return True

