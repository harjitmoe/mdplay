# -*- mode: python; coding: utf-8 -*-
import re,string

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay.cangjie import proc_cang
from mdplay.parse_roma import kanafy, hiraise, kataise
from mdplay import nodes

def cjk_handler(out, hreftype, href, label, flags):
    if (hreftype.lower() in ("cang","cangjie","souketsu","soketsu")) and ("nocangjie" not in flags):
        kanji = proc_cang(href, -1)
        #print `kanji`, `label`
        if label and ("norubi" not in flags):
            out.append(nodes.RubiNode(kanji, label))
        else:
            out.append(kanji)
    elif (hreftype.lower() in ("cang3","cangjie3","souketsu3","soketsu3")) and ("nocangjie" not in flags):
        kanji = proc_cang(href, 3)
        #print `kanji`, `label`
        if label and ("norubi" not in flags):
            out.append(nodes.RubiNode(kanji, label))
        else:
            out.append(kanji)
    elif (hreftype.lower() in ("cang5","cangjie5","souketsu5","soketsu5")) and ("nocangjie" not in flags):
        kanji = proc_cang(href, 5)
        if label and ("norubi" not in flags):
            out.append(nodes.RubiNode(kanji, label))
        else:
            out.append(kanji)
    elif (hreftype.lower() in ("kana",)) and ("noromkan" not in flags):
        kana = kanafy(href)
        if label and ("norubi" not in flags):
            out.append(nodes.RubiNode(kana, label))
        else:
            out.append(kana)
    elif (hreftype.lower() in ("kkana","katakana")) and ("noromkan" not in flags):
        kana = kataise(kanafy(href))
        if label and ("norubi" not in flags):
            out.append(nodes.RubiNode(kana, label))
        else:
            out.append(kana)
    elif (hreftype.lower() in ("hkana","hgana","hiragana")) and ("noromkan" not in flags):
        kana = hiraise(kanafy(href))
        if label and ("norubi" not in flags):
            out.append(nodes.RubiNode(kana, label))
        else:
            out.append(kana)
    elif (hreftype.lower() in ("kana_hbn",)) and ("noromkan" not in flags):
        kana = kanafy(href, "hepburn")
        if label and ("norubi" not in flags):
            out.append(nodes.RubiNode(kana, label))
        else:
            out.append(kana)
    elif (hreftype.lower() in ("kkana_hbn","katakana_hepburn")) and ("noromkan" not in flags):
        kana = kataise(kanafy(href, "hepburn"))
        if label and ("norubi" not in flags):
            out.append(nodes.RubiNode(kana, label))
        else:
            out.append(kana)
    elif (hreftype.lower() in ("hkana_hbn","hgana_hbn","hiragana_hepburn")) and ("noromkan" not in flags):
        kana = hiraise(kanafy(href, "hepburn"))
        if label and ("norubi" not in flags):
            out.append(nodes.RubiNode(kana, label))
        else:
            out.append(kana)
    elif (hreftype.lower() in ("rubi","ruby","furi")) and ("norubi" not in flags):
        out.append(nodes.RubiNode(href, label))
    else:
        return False
    return True

