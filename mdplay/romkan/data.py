#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# *** ATTENTION - IF YOU CHANGE THIS FILE, DELETE data.pickle PRECALC CACHE FILE ***

import re, unicodedata
try:
    from functools import cmp_to_key
except ImportError:
    from .cmp_to_key import cmp_to_key

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

import os, pickle

try:
    locals().update(pickle.loads(open(os.path.join(os.path.dirname(__file__),"data.pickle"),"rb").read()))
except (EnvironmentError,EOFError):
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

    def _len_cmp(x): return -len(x)
    RROMPAT = ("|".join(sorted(ROMKAN.keys(), key=_len_cmp)).replace(".","\\.").replace("^","\\^") )
    RROMPAT_HBN = ("|".join(sorted(ROMKAN_HBN.keys(), key=_len_cmp)).replace(".","\\.").replace("^","\\^") )
    RROMPAT_KNR = ("|".join(sorted(ROMKAN_KNR.keys(), key=_len_cmp)).replace(".","\\.").replace("^","\\^") )

    def _kanpat_cmp(KANROM):
        return lambda x, y: (len(y) > len(x)) - (len(y) < len(x)) or (len(KANROM[x]) > len(KANROM[x])) - (len(KANROM[x]) < len(KANROM[x]))
    KKANPAT = ("|".join(sorted(KANROM.keys(), key=cmp_to_key(_kanpat_cmp(KANROM)))))
    KKANPAT_HBN = ("|".join(sorted(KANROM_HBN.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_HBN)))))
    KKANPAT_KNR = ("|".join(sorted(KANROM_KNR.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_KNR)))))

    KUNREI_SEQS = [y for (x, y) in KUNREITAB]
    HEPBURN_SEQS = [y for (x, y) in HEPBURNTAB]

    KKUNPAT = ("|".join(sorted(KUNREI_SEQS, key=_len_cmp)).replace(".","\\.").replace("^","\\^") )
    HHEPPAT = ("|".join(sorted(HEPBURN_SEQS, key=_len_cmp)).replace(".","\\.").replace("^","\\^") )


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

    RROMPAT_H = ("|".join(sorted(ROMKAN_H.keys(), key=_len_cmp)).replace(".","\\.").replace("^","\\^") )
    RROMPAT_H_HBN = ("|".join(sorted(ROMKAN_H_HBN.keys(), key=_len_cmp)).replace(".","\\.").replace("^","\\^") )
    RROMPAT_H_KNR = ("|".join(sorted(ROMKAN_H_KNR.keys(), key=_len_cmp)).replace(".","\\.").replace("^","\\^") )

    KKANPAT_H = ("|".join(sorted(KANROM_H.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_H)))))
    KKANPAT_H_HBN = ("|".join(sorted(KANROM_H_HBN.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_H_HBN)))))
    KKANPAT_H_KNR = ("|".join(sorted(KANROM_H_KNR.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_H_KNR)))))

    KUNREI_H = [y for (x, y) in KUNREITAB_H]
    HEPBURN_H = [y for (x, y) in HEPBURNTAB_H]

    KKUNPAT_H = ("|".join(sorted(KUNREI_H, key=_len_cmp)).replace(".","\\.").replace("^","\\^") )
    HHEPPAT_H = ("|".join(sorted(HEPBURN_H, key=_len_cmp)).replace(".","\\.").replace("^","\\^") )
    _fn = os.path.join(os.path.dirname(__file__),"data.pickle")
    def _dd(a, p=pickle): return p.dumps(a,2)
    del unicodedata
    del os
    del pickle
    dob = {}
    for i in locals().keys():
        if i[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            dob[i] = locals()[i]
    open(_fn,"wb").write(_dd(dob))

ROMPAT = re.compile(RROMPAT)
ROMPAT_HBN = re.compile(RROMPAT_HBN)
ROMPAT_KNR = re.compile(RROMPAT_KNR)

KANPAT = re.compile(KKANPAT)
KANPAT_HBN = re.compile(KKANPAT_HBN)
KANPAT_KNR = re.compile(KKANPAT_KNR)

KUNPAT = re.compile(KKUNPAT)
HEPPAT = re.compile(HHEPPAT)

ROMPAT_H = re.compile(RROMPAT_H)
ROMPAT_H_HBN = re.compile(RROMPAT_H_HBN)
ROMPAT_H_KNR = re.compile(RROMPAT_H_KNR)

KANPAT_H = re.compile(KKANPAT_H)
KANPAT_H_HBN = re.compile(KKANPAT_H_HBN)
KANPAT_H_KNR = re.compile(KKANPAT_H_KNR)

KUNPAT_H = re.compile(KKUNPAT_H)
HEPPAT_H = re.compile(HHEPPAT_H)