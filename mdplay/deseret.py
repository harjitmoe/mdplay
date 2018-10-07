#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
import re,string

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import nodes, diacritic, uriregex, cjk, emoji
from mdplay import htmlentitydefs_latest as htmlentitydefs

_first_capital_smp = 0x10400
_last_capital_smp = 0x10427
_first_minuscule_smp = 0x10428
_last_minuscule_smp = 0x1044F

_first_capital_csur = 0xE830
_last_capital_csur = 0xE855 # Last following the withdrawn CSUR deseret spec.
_last_unic_capital_csur = 0xE857 # Last as per transplating of the Unicode range.
_last_ext_capital_csur = 0xE85F # Last before the minuscule range / last extension space.
_first_minuscule_csur = 0xE860
_last_minuscule_csur = 0xE885 # Last following the withdrawn CSUR deseret spec.
_last_unic_minuscule_csur = 0xE887 # Last as per transplating of the Unicode range.
_last_ext_minuscule_csur = 0xE88F # Last before the CSUR deseret block end / last extension space.

_diff_capital = _first_capital_smp - _first_capital_csur
_diff_minuscule = _first_minuscule_smp - _first_minuscule_csur

_cols = 12
_rows = 8
width = 264
height = 320
cwidth = width // _cols
cheight = height // _rows

def smp_to_csur(i):
    if _first_capital_smp <= ord(i) <= _last_capital_smp:
        return chr(ord(i) - _diff_capital)
    elif _first_minuscule_smp <= ord(i) <= _last_minuscule_smp:
        return chr(ord(i) - _diff_minuscule)
    else:
        return i

def csur_to_coords(i, bgsz):
    n = ord(i) - _first_capital_csur
    y0 = (n // _cols) * cheight
    x0 = (n % _cols) * cwidth
    # For plugging into CSS background-position
    return "-{:f}em -{:f}em".format(x0 * bgsz / height, y0 * bgsz / height)

def characters_to_nodes(document, s):
    FACTOR = 1.2
    bgsz = FACTOR * height / cheight
    mh = FACTOR ; mw = FACTOR * cwidth / cheight
    templ = "width: {:f}em; height: {:f}em; background-size: auto {:f}em; background-position: {};"
    for c in s:
        cs = smp_to_csur(c)
        if cs == "\x20":
            e = document.createElement("span")
            sty = "width: {:f}em; height: {:f}em; display: inline-block;".format(mw, mh)
            e.setAttribute("style", sty)
            e.appendChild(document.createTextNode(" "))
            yield e
        elif not (_first_capital_csur <= ord(cs) <= _last_ext_minuscule_csur):
            yield document.createTextNode(c)
            continue
        else:
            e = document.createElement("span")
            sty = templ.format(mw, mh, bgsz, csur_to_coords(cs, bgsz))
            e.setAttribute("class", "deseretletter")
            e.setAttribute("style", sty)
            e.appendChild(document.createTextNode(c))
            yield e




