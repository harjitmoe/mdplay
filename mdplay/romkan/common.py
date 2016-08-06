#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re, unicodedata

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

from .data import *

def normalize_double_n(str):
    """
    Normalize double n.
    """
    
    # Replace double n with n'
    str = re.sub("nn", "n'", str)
    # Remove unnecessary apostrophes
    str = re.sub("n'(?=[^aiueoyn]|$)", "n", str)
    
    return str

HEPBURN = "hepburn"
KUNREI = "kunrei"
WAPURO = "wapuro"

def to_kana(str, scheme=WAPURO):
    """
    Convert a Romaji string to Katakana.
    """
    
    str = str.lower()
    str = normalize_double_n(str)
    
    if scheme==WAPURO:
        tmp = ROMPAT.sub(lambda x: ROMKAN[x.group(0)], str)
    elif scheme==HEPBURN:
        tmp = ROMPAT_HBN.sub(lambda x: ROMKAN_HBN[x.group(0)], str)
    elif scheme==KUNREI:
        tmp = ROMPAT_KNR.sub(lambda x: ROMKAN_KNR[x.group(0)], str)
    else:
        raise ValueError("invalid scheme= argument: %r"%scheme)
    return tmp

def to_katakana(str, scheme=WAPURO):
    """
    Convert a Romaji or Hiragana string to Katakana.
    """
    
    str = str.lower()
    str = normalize_double_n(str)
    for v,k in TOHIRA.items():
        str = str.replace(k, v)
    
    if scheme==WAPURO:
        tmp = ROMPAT.sub(lambda x: ROMKAN[x.group(0)], str)
    elif scheme==HEPBURN:
        tmp = ROMPAT_HBN.sub(lambda x: ROMKAN_HBN[x.group(0)], str)
    elif scheme==KUNREI:
        tmp = ROMPAT_KNR.sub(lambda x: ROMKAN_KNR[x.group(0)], str)
    else:
        raise ValueError("invalid scheme= argument: %r"%scheme)
    return tmp

def to_hiragana(str, scheme=WAPURO):
    """
    Convert a Romaji or Katakana string to Hiragana.
    """
    
    str = str.lower()
    str = normalize_double_n(str)
    
    if scheme==WAPURO:
        tmp = ROMPAT_H.sub(lambda x: ROMKAN_H[x.group(0)], str)
    elif scheme==HEPBURN:
        tmp = ROMPAT_H_HBN.sub(lambda x: ROMKAN_H_HBN[x.group(0)], str)
    elif scheme==KUNREI:
        tmp = ROMPAT_H_KNR.sub(lambda x: ROMKAN_H_KNR[x.group(0)], str)
    else:
        raise ValueError("invalid scheme= argument: %r"%scheme)
    for k,v in TOHIRA.items():
        tmp = tmp.replace(k, v)
    return tmp

def to_hepburn(str):
    """
    Convert a Kana string or Kunrei-style Romaji string to roughly Hepburn-style Romaji.
    """
    tmp = str
    tmp = tmp.lower()
    tmp = normalize_double_n(tmp)
    tmp = unicodedata.normalize("NFC", to_kana(tmp, KUNREI))
    
    tmp = KANPAT_HBN.sub(lambda x: KANROM_HBN[x.group(0)], tmp)
    tmp = KANPAT_H_HBN.sub(lambda x: KANROM_H_HBN[x.group(0)], tmp)
    
    # Remove unnecessary apostrophes
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", "n", tmp)
    
    return tmp

def to_kunrei(str):
    """
    Convert a Kana string or Hepburn-style Romaji string to roughly Kunrei-style Romaji.
    """
    tmp = str
    tmp = tmp.lower()
    tmp = normalize_double_n(tmp)
    tmp = unicodedata.normalize("NFC", to_kana(tmp, HEPBURN))

    tmp = KANPAT_KNR.sub(lambda x: KANROM_KNR[x.group(0)], tmp)
    tmp = KANPAT_H_KNR.sub(lambda x: KANROM_H_KNR[x.group(0)], tmp)
    
    # Remove unnecessary apostrophes
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", "n", tmp)
    
    return tmp

def to_roma(str):
    """
    Convert a Kana string to (roughly Hepburn-style) Romaji.
    """
    
    tmp = unicodedata.normalize("NFC", str)
    tmp = KANPAT_HBN.sub(lambda x: KANROM_HBN[x.group(0)], tmp)
    tmp = KANPAT_H_HBN.sub(lambda x: KANROM_H_HBN[x.group(0)], tmp)
    
    # Remove unnecessary apostrophes
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", "n", tmp)
    
    return tmp

def is_consonant(str):
    """
    Return a MatchObject if a Latin letter is a consonant in Japanese.
    Return None otherwise.
    """
    
    str = str.lower()
    
    return re.match("[ckgszjtdhfpbmyrwxn]", str)

def is_vowel(str):
    """
    Return a MatchObject if a Latin letter is a vowel in Japanese.
    Return None otherwise.
    """
    
    str = str.lower()
    
    return re.match("[aeiou]", str)

def expand_consonant(str):
    """
    Expand consonant to its related moras.
    Example: 'sh' => ['sha', 'she', 'shi', 'sho', 'shu']
    """
    
    str = str.lower()
    
    return sorted([mora for mora in ROMKAN.keys() if re.match("^%s.$" % str, mora)])
