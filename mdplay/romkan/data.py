#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re, unicodedata
try:
    from functools import cmp_to_key
except ImportError:
    # for python < 3.2; nicked from python 3.2
    # i.e. Written by Nick Coghlan <ncoghlan at gmail.com>,
    #   Raymond Hettinger <python at rcn.com>,
    #   and Łukasz Langa <lukasz at langa.pl>.
    #     Copyright (C) 2006-2013 Python Software Foundation.
    def cmp_to_key(mycmp):
        """Convert a cmp= function into a key= function"""
        class K(object):
            __slots__ = ['obj']
            def __init__(self, obj):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
            __hash__ = None
        return K

#
# Ruby/Romkan - a Romaji <-> Kana conversion library for Ruby.
#
# Copyright (C) 2001 Satoru Takabayashi <satoru@namazu.org>
#     All rights reserved.
#     This is free software with ABSOLUTELY NO WARRANTY.
#
# You can redistribute it and/or modify it under the terms of 
# the Ruby's licence.
#
# The above notice applies to the original library.  Regarding 
# subsequent modifications, see romkan/LICENSE file.
#

from .ptables import *

# Use Katakana

KANROM = {}
KANROM_HBN = {}
KANROM_KNR = {}
ROMKAN = {}
ROMKAN_HBN = {}
ROMKAN_KNR = {}

for kana, roma in HEPBURNTAB+KUNREITAB:
    KANROM[kana] = roma
    ROMKAN[roma] = kana
for kana, roma in HEPBURNTAB:
    KANROM_HBN[kana] = roma
    ROMKAN_HBN[roma] = kana
for kana, roma in KUNREITAB:
    KANROM_KNR[kana] = roma
    ROMKAN_KNR[roma] = kana
KANROM['ン']="n'"
KANROM_HBN['ン']="n'"
KANROM_KNR['ン']="n'"

# Sort in long order so that a longer Romaji sequence precedes.

_len_cmp = lambda x: -len(x)
ROMPAT = re.compile("|".join(sorted(ROMKAN.keys(), key=_len_cmp)) )
ROMPAT_HBN = re.compile("|".join(sorted(ROMKAN_HBN.keys(), key=_len_cmp)) )
ROMPAT_KNR = re.compile("|".join(sorted(ROMKAN_KNR.keys(), key=_len_cmp)) )

def _kanpat_cmp(KANROM):
    return lambda x, y: (len(y) > len(x)) - (len(y) < len(x)) or (len(KANROM[x]) > len(KANROM[x])) - (len(KANROM[x]) < len(KANROM[x]))
KANPAT = re.compile("|".join(sorted(KANROM.keys(), key=cmp_to_key(_kanpat_cmp(KANROM)))))
KANPAT_HBN = re.compile("|".join(sorted(KANROM_HBN.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_HBN)))))
KANPAT_KNR = re.compile("|".join(sorted(KANROM_KNR.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_KNR)))))

KUNREI_SEQS = [y for (x, y) in KUNREITAB]
HEPBURN_SEQS = [y for (x, y) in HEPBURNTAB]

KUNPAT = re.compile("|".join(sorted(KUNREI_SEQS, key=_len_cmp)) )
HEPPAT = re.compile("|".join(sorted(HEPBURN_SEQS, key=_len_cmp)) )


# Use Hiragana

KANROM_H = {}
ROMKAN_H = {}
KANROM_H_HBN = {}
ROMKAN_H_HBN = {}
KANROM_H_KNR = {}
ROMKAN_H_KNR = {}

for pair in HEPBURNTAB_H+KUNREITAB_H:
    kana, roma = pair
    KANROM_H[kana] = roma
    ROMKAN_H[roma] = kana
for kana, roma in HEPBURNTAB_H:
    KANROM_H_HBN[kana] = roma
    ROMKAN_H_HBN[roma] = kana
for kana, roma in KUNREITAB_H:
    KANROM_H_KNR[kana] = roma
    ROMKAN_H_KNR[roma] = kana
KANROM_H['ん']="n'"
KANROM_H_HBN['ん']="n'"
KANROM_H_KNR['ん']="n'"

# Sort in long order so that a longer Romaji sequence precedes.

ROMPAT_H = re.compile("|".join(sorted(ROMKAN_H.keys(), key=_len_cmp)) )
ROMPAT_H_HBN = re.compile("|".join(sorted(ROMKAN_H_HBN.keys(), key=_len_cmp)) )
ROMPAT_H_KNR = re.compile("|".join(sorted(ROMKAN_H_KNR.keys(), key=_len_cmp)) )

KANPAT_H = re.compile("|".join(sorted(KANROM_H.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_H)))))
KANPAT_H_HBN = re.compile("|".join(sorted(KANROM_H_HBN.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_H_HBN)))))
KANPAT_H_KNR = re.compile("|".join(sorted(KANROM_H_KNR.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_H_KNR)))))

KUNREI_H = [y for (x, y) in KUNREITAB_H]
HEPBURN_H = [y for (x, y) in HEPBURNTAB_H]

KUNPAT_H = re.compile("|".join(sorted(KUNREI_H, key=_len_cmp)) )
HEPPAT_H = re.compile("|".join(sorted(HEPBURN_H, key=_len_cmp)) )
