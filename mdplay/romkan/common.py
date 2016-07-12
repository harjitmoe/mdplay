#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .version import __version__

__copying__ = """
Copyright (c) 2012, 2013 Mort Yao <mort.yao@gmail.com>
Copyright (c) 2010 Masato Hagiwara <hagisan@gmail.com>
Copyright (c) 2001 Satoru Takabayashi <satoru@namazu.org>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---

MDPlay alterations are under the same terms as MDPlay itself.

--- 

cmp_to_key is Written by Nick Coghlan <ncoghlan at gmail.com>,
Raymond Hettinger <python at rcn.com>, and Łukasz Langa <lukasz at langa.pl>.
Copyright (C) 2006-2013 Python Software Foundation.

PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2

1. This LICENSE AGREEMENT is between the Python Software Foundation
("PSF"), and the Individual or Organization ("Licensee") accessing and
otherwise using this software ("Python") in source or binary form and
its associated documentation.

2. Subject to the terms and conditions of this License Agreement, PSF hereby
grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
analyze, test, perform and/or display publicly, prepare derivative works,
distribute, and otherwise use Python alone or in any derivative version,
provided, however, that PSF's License Agreement and PSF's notice of copyright,
i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
2011, 2012, 2013 Python Software Foundation; All Rights Reserved" are retained
in Python alone or in any derivative version prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on
or incorporates Python or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python.

4. PSF is making Python available to Licensee on an "AS IS"
basis.  PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any
relationship of agency, partnership, or joint venture between PSF and
Licensee.  This License Agreement does not grant permission to use PSF
trademarks or trade name in a trademark sense to endorse or promote
products or services of Licensee, or any third party.

8. By copying, installing or otherwise using Python, Licensee
agrees to be bound by the terms and conditions of this License
Agreement."""

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
# The above notice applies to the original library.  For
# subsequent modifications, see romkan/LICENSE file.
#

class Firenze(list):
    def push(self, id, elem):
        """Push front if not id, back otherwise."""
        if id: return self.append(elem)
        return self.insert(0,elem)

KATATAB=Firenze([('ㇰ',('xku','xku')), ('ㇱ',('xsi','xshi')), ('ㇲ',('xsu','xsu')), ('ㇳ',('xto','xto')), ('ㇴ',('xnu','xnu')), ('ㇵ',('xha','xha')), ('ㇶ',('xhi','xhi')), ('ㇷ',('xfu','xfu')), ('ㇸ',('xhe','xhe')), ('ㇹ',('xho','xho')), ('ㇺ',('xmu','xmu')), ('ㇻ',('xra','xra')), ('ㇼ',('xri','xri')), ('ㇽ',('xru','xru')), ('ㇾ',('xre','xre')), ('ㇿ',('xro','xro')), ('ヨ', ('yo', 'yo')), ('ル', ('ru', 'ru')), ('ォ', ('xo', 'xo')), ('シ', ('si', 'shi')), ('ボ', ('bo', 'bo')), ('オ', ('o', 'o')), ('ジ', ('zi', 'ji')), ('ウ', ('u', 'u')), ('ヤ', ('ya', 'ya')), ('デ', ('de', 'de')), ('ー', ('-', '-')), ('ヅ', ('du', 'dzu')), ('ド', ('do', 'do')), ('ヘ', ('he', 'he')), ('ヰ', ('wi', 'wi')), ('ョ', ('xyo', 'xyo')), ('ャ', ('xya', 'xya')), ('ェ', ('xe', 'xe')), ('ベ', ('be', 'be')), ('カ', ('ka', 'ka')), ('ハ', ('ha', 'ha')), ('メ', ('me', 'me')), ('ラ', ('ra', 'ra')), ('ヷ', ('va', 'va')), ('ヸ', ('vi', 'vi')), ('ヴ', ('vu', 'vu')), ('ヹ', ('ve', 've')), ('ヺ', ('vo', 'vo')), ('ポ', ('po', 'po')), ('ヮ', ('xwa', 'xwa')), ('フ', ('hu', 'fu')), ('ホ', ('ho', 'ho')), ('ア', ('a', 'a')), ('ム', ('mu', 'mu')), ('ァ', ('xa', 'xa')), ('エ', ('e', 'e')), ('ゴ', ('go', 'go')), ('チ', ('ti', 'chi')), ('ワ', ('wa', 'wa')), ('サ', ('sa', 'sa')), ('ヲ', ('wo', 'wo')), ('ロ', ('ro', 'ro')), ('バ', ('ba', 'ba')), ('リ', ('ri', 'ri')), ('ギ', ('gi', 'gi')), ('パ', ('pa', 'pa')), ('タ', ('ta', 'ta')), ('ガ', ('ga', 'ga')), ('ニ', ('ni', 'ni')), ('ュ', ('xyu', 'xyu')), ('ザ', ('za', 'za')), ('キ', ('ki', 'ki')), ('ィ', ('xi', 'xi')), ('コ', ('ko', 'ko')), ('レ', ('re', 're')), ('ゼ', ('ze', 'ze')), ('グ', ('gu', 'gu')), ('ユ', ('yu', 'yu')), ('ン', ("n'", "m'")), ('ン', ('n', 'm')), ('ン', ("n'", "n'")), ('ン', ('n', 'n')), ('ツ', ('tu', 'tsu')), ('ヂ', ('di', 'dji')), ('ビ', ('bi', 'bi')), ('ソ', ('so', 'so')), ('ヱ', ('we', 'we')), ('ト', ('to', 'to')), ('プ', ('pu', 'pu')), ('ク', ('ku', 'ku')), ('ゾ', ('zo', 'zo')), ('ゥ', ('xu', 'xu')), ('ペ', ('pe', 'pe')), ('ミ', ('mi', 'mi')), ('イ', ('i', 'i')), ('ゲ', ('ge', 'ge')), ('ピ', ('pi', 'pi')), ('ケ', ('ke', 'ke')), ('ズ', ('zu', 'zu')), ('モ', ('mo', 'mo')), ('ダ', ('da', 'da')), ('ノ', ('no', 'no')), ('ブ', ('bu', 'bu')), ('マ', ('ma', 'ma')), ('ナ', ('na', 'na')), ('ス', ('su', 'su')), ('ッ', ('t', 't')), ('ッ', ('xtu', 'xtsu')), ('ヌ', ('nu', 'nu')), ('セ', ('se', 'se')), ('ヒ', ('hi', 'hi')), ('ネ', ('ne', 'ne')), ('テ', ('te', 'te'))])

TOHIRA = {'ィ': 'ぃ', 'ク': 'く', 'ヒ': 'ひ', 'ェ': 'ぇ', 'ブ': 'ぶ', 'ゾ': 'ぞ', 'ヮ': 'ゎ', 'ヲ': 'を', 'バ': 'ば', 'ォ': 'ぉ', 'ミ': 'み', 'ヅ': 'づ', 'ズ': 'ず', 'ヨ': 'よ', 'ダ': 'だ', 'ョ': 'ょ', 'ラ': 'ら', 'ュ': 'ゅ', 'ー': 'ー', 'ゲ': 'げ', 'プ': 'ぷ', 'ス': 'す', 'ド': 'ど', 'ヰ': 'ゐ', 'ヌ': 'ぬ', 'ジ': 'じ', 'ザ': 'ざ', 'セ': 'せ', 'コ': 'こ', 'ツ': 'つ', 'ネ': 'ね', 'テ': 'て', 'マ': 'ま', 'ワ': 'わ', 'ノ': 'の', 'チ': 'ち', 'シ': 'し', 'グ': 'ぐ', 'デ': 'で', 'エ': 'え', 'ロ': 'ろ', 'パ': 'ぱ', 'フ': 'ふ', 'ボ': 'ぼ', 'オ': 'お', 'ウ': 'う', 'ホ': 'ほ', 'ヱ': 'ゑ', 'ペ': 'ぺ', 'サ': 'さ', 'モ': 'も', 'タ': 'た', 'ハ': 'は', 'ッ': 'っ', 'ビ': 'び', 'ソ': 'そ', 'ヴ': 'う゛', 'ヂ': 'ぢ', 'ゼ': 'ぜ', 'ヘ': 'へ', 'ピ': 'ぴ', 'ゥ': 'ぅ', 'ム': 'む', 'ト': 'と', 'ル': 'る', 'カ': 'か', 'ユ': 'ゆ', 'ゴ': 'ご', 'ア': 'あ', 'キ': 'き', 'ガ': 'が', 'リ': 'り', 'ベ': 'べ', 'ァ': 'ぁ', 'ギ': 'ぎ', 'レ': 'れ', 'ン': 'ん', 'メ': 'め', 'ナ': 'な', 'ヤ': 'や', 'ポ': 'ぽ', 'イ': 'い', 'ケ': 'け', 'ャ': 'ゃ', 'ニ': 'に'}

for ka,(ku,he) in KATATAB[:]:
    if (len(ku) == 2) and ((ku[-1] == "i") or (ku in ("vu","hu"))):
	apriori = 0
        if ku == he:
            hepstem = he[:-1]+"y"
            if ku[0] == "h":
                apriori = 1
        elif ku[-1] != "i":
            hepstem = he[:-1]+"y"
        else:
            hepstem = he[:-1]
        KATATAB.push(apriori,(ka+"ャ",(ku[:-1]+"ya",hepstem+"a")))
        KATATAB.push(apriori,(ka+"ュ",(ku[:-1]+"yu",hepstem+"u")))
        KATATAB.push(apriori,(ka+"ェ",(ku[:-1]+"ye",hepstem+"e")))
        KATATAB.push(apriori,(ka+"ョ",(ku[:-1]+"yo",hepstem+"o")))
    if (len(ku)==2) and (ku in ("su","zu","te","de","to","do","ho")):
        if ku[1]=="u":
            KATATAB.push(0,(ka+"ィ",(ku[:-1]+"yi",ku[:-1]+"i")))
            KATATAB.push(0,(ka+"ィ",(ku[:-1]+"i", ku[:-1]+"i")))
        elif ku[1]=="e":
            KATATAB.push(0,(ka+"ャ",(ku[:-1]+"ya", ku[:-1]+"ya")))
            KATATAB.push(0,(ka+"ィ",(ku[:-1]+"i", ku[:-1]+"i")))
            KATATAB.push(0,(ka+"ュ",(ku[:-1]+"yu", ku[:-1]+"yu")))
            KATATAB.push(0,(ka+"ョ",(ku[:-1]+"yo", ku[:-1]+"yo")))
            KATATAB.push(0,(ka+"ャ",(ku[:-1]+"ha", ku[:-1]+"ya")))
            KATATAB.push(0,(ka+"ィ",(ku[:-1]+"hi", ku[:-1]+"i")))
            KATATAB.push(0,(ka+"ュ",(ku[:-1]+"hu", ku[:-1]+"yu")))
            KATATAB.push(0,(ka+"ョ",(ku[:-1]+"ho", ku[:-1]+"yo")))
        elif ku[1]=="o":
            KATATAB.push(0,(ka+"ゥ",(ku[:-1]+"u", ku[:-1]+"u")))
    #NOT elif
    if (len(ku)==2) and (ku[-1] == "u"):
        KATATAB.push(0,(ka+"ヮ",(ku[:-1]+"wa",he[:-1]+"wa")))
        KATATAB.push(0,(ka+"ァ",(ku[:-1]+"wa",he[:-1]+"wa")))
        KATATAB.push(0,(ka+"ィ",(ku[:-1]+"wi",he[:-1]+"wi")))
        KATATAB.push(0,(ka+"ゥ",(ku[:-1]+"wu",he[:-1]+"wu")))
        KATATAB.push(0,(ka+"ェ",(ku[:-1]+"we",he[:-1]+"we")))
        KATATAB.push(0,(ka+"ォ",(ku[:-1]+"wo",he[:-1]+"wo")))
    if ku == "u":
        KATATAB.push(1,(ka+"ィ",("wi","wi")))
        KATATAB.push(0,(ka+"ゥ",("wu","wu")))
        KATATAB.push(1,(ka+"ェ",("we","we")))
        KATATAB.push(0,(ka+"ォ",("wo","wo")))
    if ku in ("hu","vu"):
	apriori = (ku[0]=="v")
        KATATAB.push(apriori,(ka+"ァ",(ku[:-1]+"a",he[:-1]+"a")))
        KATATAB.push(apriori,(ka+"ィ",(ku[:-1]+"i",he[:-1]+"i")))
        KATATAB.push(apriori,(ka+"ェ",(ku[:-1]+"e",he[:-1]+"e")))
        KATATAB.push(apriori,(ka+"ォ",(ku[:-1]+"o",he[:-1]+"o")))
    if ku == "i":
        KATATAB.push(0,(ka+"ィ",("yi","yi")))
        KATATAB.push(0,(ka+"ェ",("ye","ye")))
#Must be seperate to and after the previous:
for ka,(ku,he) in KATATAB[:]:
    if ku[0] not in "xaiueo":
        #Including cch as is commonly used...
        KATATAB.push(1,("ッ"+ka,(ku[0]+ku,he[0]+he)))
        if ku[0]!=he[0]: #Strict Hepburn is tch, not cch
            if ku[0]=="t":
                KATATAB.push(1,("ッ"+ka,(ku[0]+ku,ku[0]+he)))

def _to_hira(kata):
    """For internal use only."""
    o = ""
    for i in kata:
        if i not in TOHIRA:
            return None
        o += TOHIRA[i]
    return o

HIRATAB=Firenze()

for ka,ro in KATATAB[:]:
    hka = _to_hira(ka)
    if hka != None:
        HIRATAB.push(1,(hka,ro))

KUNREITAB = [(a, b) for (a, (b, c)) in KATATAB]
HEPBURNTAB = [(a, c) for (a, (b, c)) in KATATAB]
KUNREITAB_H = [(a, b) for (a, (b, c)) in HIRATAB]
HEPBURNTAB_H = [(a, c) for (a, (b, c)) in HIRATAB]


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

def to_katakana(str, scheme=WAPURO):
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

def to_hiragana(str, scheme=WAPURO):
    """
    Convert a Romaji string to Hiragana.
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
    return tmp

to_kana = to_katakana

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
