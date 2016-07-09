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

import re
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

# Original said: "This table is imported from KAKASI <http://kakasi.namazu.org/>
# and modified."
# Table in this MDPlay alteration has been processed to the extent that no content
# remains other than the romanisation rules themselves, which are of course in 
# any case prior art.

KATATAB=[('ッチ', ('tti', 'cchi')), ('ッチ', ('tti', 'tchi')), ('ヨ', ('yo', 'yo')), ('ル', ('ru', 'ru')), ('ォ', ('xo', 'xo')), ('ニャ', ('nya', 'nya')), ('ニュ', ('nyu', 'nyu')), ('ミョ', ('myo', 'myo')), ('ッリ', ('rri', 'rri')), ('ッリャ', ('rrya', 'rrya')), ('シ', ('si', 'shi')), ('ボ', ('bo', 'bo')), ('ヒョ', ('hyo', 'hyo')), ('オ', ('o', 'o')), ('ヴァ', ('va', 'va')), ('ック', ('kku', 'kku')), ('ジ', ('zi', 'ji')), ('ッコ', ('kko', 'kko')), ('ッチャ', ('ttya', 'ccha')), ('チャ', ('tya', 'cha')), ('ウ', ('u', 'u')), ('ヤ', ('ya', 'ya')), ('デ', ('de', 'de')), ('ッセ', ('sse', 'sse')), ('ッレ', ('rre', 'rre')), ('ッギャ', ('ggya', 'ggya')), ('ッジョ', ('zzyo', 'jjo')), ('ー', ('-', '-')), ('ヅ', ('du', 'du')), ('ド', ('do', 'do')), ('ヘ', ('he', 'he')), ('ッソ', ('sso', 'sso')), ('ミュ', ('myu', 'myu')), ('ッヂャ', ('ddya', 'ddya')), ('ヰ', ('wi', 'wi')), ('ョ', ('xyo', 'xyo')), ('ャ', ('xya', 'xya')), ('ジョ', ('zyo', 'jo')), ('ェ', ('xe', 'xe')), ('ベ', ('be', 'be')), ('ヒャ', ('hya', 'hya')), ('チョ', ('tyo', 'cho')), ('カ', ('ka', 'ka')), ('ショ', ('syo', 'sho')), ('ハ', ('ha', 'ha')), ('シュ', ('syu', 'shu')), ('ッヨ', ('yyo', 'yyo')), ('メ', ('me', 'me')), ('ッファ', ('ffa', 'ffa')), ('チェ', ('tye', 'che')), ('キョ', ('kyo', 'kyo')), ('ピュ', ('pyu', 'pyu')), ('ッホ', ('hho', 'hho')), ('ッタ', ('tta', 'tta')), ('チュ', ('tyu', 'chu')), ('ッビ', ('bbi', 'bbi')), ('ッピ', ('ppi', 'ppi')), ('ラ', ('ra', 'ra')), ('ヴ', ('vu', 'vu')), ('ポ', ('po', 'po')), ('ップ', ('ppu', 'ppu')), ('ヮ', ('xwa', 'xwa')), ('ウォ', ('wo', 'wo')), ('ミャ', ('mya', 'mya')), ('フ', ('hu', 'fu')), ('ホ', ('ho', 'ho')), ('ッザ', ('zza', 'zza')), ('ア', ('a', 'a')), ('ッゴ', ('ggo', 'ggo')), ('ム', ('mu', 'mu')), ('ァ', ('xa', 'xa')), ('ッヒャ', ('hhya', 'hhya')), ('ッヴ', ('vvu', 'vvu')), ('ッフェ', ('ffe', 'ffe')), ('エ', ('e', 'e')), ('ッダ', ('dda', 'dda')), ('ゴ', ('go', 'go')), ('ビョ', ('byo', 'byo')), ('チ', ('ti', 'chi')), ('ギャ', ('gya', 'gya')), ('ッロ', ('rro', 'rro')), ('ギョ', ('gyo', 'gyo')), ('シャ', ('sya', 'sha')), ('リュ', ('ryu', 'ryu')), ('ッキャ', ('kkya', 'kkya')), ('キュ', ('kyu', 'kyu')), ('ッペ', ('ppe', 'ppe')), ('キャ', ('kya', 'kya')), ('ッポ', ('ppo', 'ppo')), ('ッドゥ', ('ddu', 'ddu')), ('ッチュ', ('ttyu', 'cchu')), ('ッヒ', ('hhi', 'hhi')), ('ッジャ', ('zzya', 'jja')), ('ヒュ', ('hyu', 'hyu')), ('ワ', ('wa', 'wa')), ('サ', ('sa', 'sa')), ('ッチェ', ('ttye', 'cche')), ('ヲ', ('wo', 'wo')), ('ッフィ', ('ffi', 'ffi')), ('シェ', ('sye', 'she')), ('ウィ', ('wi', 'wi')), ('フォ', ('fo', 'fo')), ('ッビョ', ('bbyo', 'bbyo')), ('ッキョ', ('kkyo', 'kkyo')), ('ッベ', ('bbe', 'bbe')), ('ロ', ('ro', 'ro')), ('ッキ', ('kki', 'kki')), ('ッチョ', ('ttyo', 'ccho')), ('ティ', ('ti', 'ti')), ('バ', ('ba', 'ba')), ('リ', ('ri', 'ri')), ('ッズ', ('zzu', 'zzu')), ('ギ', ('gi', 'gi')), ('パ', ('pa', 'pa')), ('ヴィ', ('vi', 'vi')), ('ッパ', ('ppa', 'ppa')), ('ッゲ', ('gge', 'gge')), ('タ', ('ta', 'ta')), ('ヴォ', ('vo', 'vo')), ('ッヂ', ('ddi', 'ddi')), ('ッヅ', ('ddu', 'ddu')), ('ッキュ', ('kkyu', 'kkyu')), ('ッヂョ', ('ddyo', 'ddyo')), ('フュ', ('fu', 'fu')), ('ッシ', ('ssi', 'sshi')), ('ガ', ('ga', 'ga')), ('ッヴァ', ('vva', 'vva')), ('ビャ', ('bya', 'bya')), ('ニ', ('ni', 'ni')), ('ッバ', ('bba', 'bba')), ('ッピュ', ('ppyu', 'ppyu')), ('ッジ', ('zzi', 'jji')), ('ッゾ', ('zzo', 'zzo')), ('ュ', ('xyu', 'xyu')), ('ザ', ('za', 'za')), ('ッティ', ('tti', 'tti')), ('キ', ('ki', 'ki')), ('ッデ', ('dde', 'dde')), ('ヂュ', ('dyu', 'dyu')), ('ッヴォ', ('vvo', 'vvo')), ('ィ', ('xi', 'xi')), ('ッル', ('rru', 'rru')), ('コ', ('ko', 'ko')), ('ッユ', ('yyu', 'yyu')), ('レ', ('re', 're')), ('ッヴェ', ('vve', 'vve')), ('ヂャ', ('dya', 'dya')), ('ッゼ', ('zze', 'zze')), ('ゼ', ('ze', 'ze')), ('ドゥ', ('du', 'du')), ('グ', ('gu', 'gu')), ('ッリョ', ('rryo', 'rryo')), ('ユ', ('yu', 'yu')), ('ッヘ', ('hhe', 'hhe')), ('ン', ("n'", "n'")), ('ン', ('n', "n")), ('ッピョ', ('ppyo', 'ppyo')), ('ッシュ', ('ssyu', 'sshu')), ('フェ', ('fe', 'fe')), ('ツ', ('tu', 'tsu')), ('ファ', ('fa', 'fa')), ('ヂ', ('di', 'di')), ('ッショ', ('ssyo', 'ssho')), ('ッケ', ('kke', 'kke')), ('ビ', ('bi', 'bi')), ('ソ', ('so', 'so')), ('ッヴィ', ('vvi', 'vvi')), ('ッヒュ', ('hhyu', 'hhyu')), ('ピョ', ('pyo', 'pyo')), ('ヱ', ('we', 'we')), ('ッフォ', ('ffo', 'ffo')), ('ビュ', ('byu', 'byu')), ('ッガ', ('gga', 'gga')), ('ト', ('to', 'to')), ('ッビュ', ('bbyu', 'bbyu')), ('ッヒョ', ('hhyo', 'hhyo')), ('プ', ('pu', 'pu')), ('ッツ', ('ttu', 'ttsu')), ('ク', ('ku', 'ku')), ('ゾ', ('zo', 'zo')), ('ゥ', ('xu', 'xu')), ('ピャ', ('pya', 'pya')), ('ッジュ', ('zzyu', 'jju')), ('ッカ', ('kka', 'kka')), ('ペ', ('pe', 'pe')), ('ミ', ('mi', 'mi')), ('イ', ('i', 'i')), ('ッヂュ', ('ddyu', 'ddyu')), ('ゲ', ('ge', 'ge')), ('ッブ', ('bbu', 'bbu')), ('ピ', ('pi', 'pi')), ('ジャ', ('zya', 'ja')), ('ケ', ('ke', 'ke')), ('ッボ', ('bbo', 'bbo')), ('ギュ', ('gyu', 'gyu')), ('ッド', ('ddo', 'ddo')), ('ズ', ('zu', 'zu')), ('ッテ', ('tte', 'tte')), ('ッス', ('ssu', 'ssu')), ('モ', ('mo', 'mo')), ('ダ', ('da', 'da')), ('ジュ', ('zyu', 'ju')), ('ッフュ', ('ffu', 'ffu')), ('ウェ', ('we', 'we')), ('フィ', ('fi', 'fi')), ('ノ', ('no', 'no')), ('ッグ', ('ggu', 'ggu')), ('ッギョ', ('ggyo', 'ggyo')), ('ッハ', ('hha', 'hha')), ('ブ', ('bu', 'bu')), ('ッリュ', ('rryu', 'rryu')), ('リョ', ('ryo', 'ryo')), ('ッシェ', ('ssye', 'sshe')), ('ジェ', ('zye', 'je')), ('マ', ('ma', 'ma')), ('ナ', ('na', 'na')), ('ッビャ', ('bbya', 'bbya')), ('ヴェ', ('ve', 've')), ('ス', ('su', 'su')), ('ッ', ('xtu', 'xtsu')), ('ット', ('tto', 'tto')), ('ッギ', ('ggi', 'ggi')), ('ヌ', ('nu', 'nu')), ('セ', ('se', 'se')), ('ヒ', ('hi', 'hi')), ('ディ', ('dyi', 'di')), ('ッラ', ('rra', 'rra')), ('ッピャ', ('ppya', 'ppya')), ('ッギュ', ('ggyu', 'ggyu')), ('ニョ', ('nyo', 'nyo')), ('ネ', ('ne', 'ne')), ('ヂョ', ('dyo', 'dyo')), ('ッシャ', ('ssya', 'ssha')), ('ッヤ', ('yya', 'yya')), ('テ', ('te', 'te')), ('リャ', ('rya', 'rya')), ('ッサ', ('ssa', 'ssa')), ('ッフ', ('hhu', 'ffu'))]

HIRATAB = [('っほ', ('hho', 'hho')), ('ゆ', ('yu', 'yu')), ('っぢゅ', ('ddyu', 'ddyu')), ('っく', ('kku', 'kku')), ('ぃ', ('xi', 'xi')), ('う', ('u', 'u')), ('っしゃ', ('ssya', 'ssha')), ('ゎ', ('xwa', 'xwa')), ('っひゅ', ('hhyu', 'hhyu')), ('あ', ('a', 'a')), ('っびゅ', ('bbyu', 'bbyu')), ('っさ', ('ssa', 'ssa')), ('っきょ', ('kkyo', 'kkyo')), ('っりょ', ('rryo', 'rryo')), ('っぐ', ('ggu', 'ggu')), ('っゆ', ('yyu', 'yyu')), ('れ', ('re', 're')), ('せ', ('se', 'se')), ('ふぃ', ('fi', 'fi')), ('う゛ぃ', ('vi', 'vi')), ('っふぉ', ('ffo', 'ffo')), ('っしゅ', ('ssyu', 'sshu')), ('っふぁ', ('ffa', 'ffa')), ('っそ', ('sso', 'sso')), ('じゃ', ('zya', 'ja')), ('ー', ('-', '-')), ('っだ', ('dda', 'dda')), ('ま', ('ma', 'ma')), ('っひゃ', ('hhya', 'hhya')), ('っづ', ('ddu', 'ddu')), ('ょ', ('xyo', 'xyo')), ('っべ', ('bbe', 'bbe')), ('ろ', ('ro', 'ro')), ('ふぉ', ('fo', 'fo')), ('よ', ('yo', 'yo')), ('い', ('i', 'i')), ('っう゛ぃ', ('vvi', 'vvi')), ('じゅ', ('zyu', 'ju')), ('ぎ', ('gi', 'gi')), ('っ', ('xtu', 'xtsu')), ('け', ('ke', 'ke')), ('げ', ('ge', 'ge')), ('う゛ぇ', ('ve', 've')), ('び', ('bi', 'bi')), ('ず', ('zu', 'zu')), ('ば', ('ba', 'ba')), ('ちぇ', ('tye', 'che')), ('っが', ('gga', 'gga')), ('り', ('ri', 'ri')), ('う゛ぁ', ('va', 'va')), ('ちゅ', ('tyu', 'chu')), ('ぴょ', ('pyo', 'pyo')), ('っぜ', ('zze', 'zze')), ('ひゃ', ('hya', 'hya')), ('っせ', ('sse', 'sse')), ('っふぃ', ('ffi', 'ffi')), ('ご', ('go', 'go')), ('て', ('te', 'te')), ('う゛', ('vu', 'vu')), ('じ', ('zi', 'ji')), ('っつ', ('ttu', 'ttsu')), ('か', ('ka', 'ka')), ('と', ('to', 'to')), ('ちょ', ('tyo', 'cho')), ('そ', ('so', 'so')), ('っけ', ('kke', 'kke')), ('ぶ', ('bu', 'bu')), ('へ', ('he', 'he')), ('み', ('mi', 'mi')), ('っし', ('ssi', 'sshi')), ('みゃ', ('mya', 'mya')), ('みょ', ('myo', 'myo')), ('っひ', ('hhi', 'hhi')), ('っりゃ', ('rrya', 'rrya')), ('ん', ("n'", "n'")), ('ん', ('n', "n")), ('ぜ', ('ze', 'ze')), ('ぺ', ('pe', 'pe')), ('っず', ('zzu', 'zzu')), ('や', ('ya', 'ya')), ('っう゛ぁ', ('vva', 'vva')), ('でぃ', ('dyi', 'dyi')), ('ふぇ', ('fe', 'fe')), ('っぢょ', ('ddyo', 'ddyo')), ('にゅ', ('nyu', 'nyu')), ('ぇ', ('xe', 'xe')), ('ぱ', ('pa', 'pa')), ('ぎゅ', ('gyu', 'gyu')), ('みゅ', ('myu', 'myu')), ('ち', ('ti', 'chi')), ('しゃ', ('sya', 'sha')), ('って', ('tte', 'tte')), ('こ', ('ko', 'ko')), ('っび', ('bbi', 'bbi')), ('っきゅ', ('kkyu', 'kkyu')), ('ふぁ', ('fa', 'fa')), ('っれ', ('rre', 'rre')), ('じぇ', ('zye', 'je')), ('っぺ', ('ppe', 'ppe')), ('っげ', ('gge', 'gge')), ('お', ('o', 'o')), ('っじょ', ('zzyo', 'jjo')), ('ど', ('do', 'do')), ('た', ('ta', 'ta')), ('りゃ', ('rya', 'rya')), ('っぴ', ('ppi', 'ppi')), ('だ', ('da', 'da')), ('ひょ', ('hyo', 'hyo')), ('っふ', ('hhu', 'ffu')), ('っじゃ', ('zzya', 'jja')), ('にゃ', ('nya', 'nya')), ('が', ('ga', 'ga')), ('で', ('de', 'de')), ('め', ('me', 'me')), ('っぢ', ('ddi', 'ddi')), ('は', ('ha', 'ha')), ('ふ', ('hu', 'fu')), ('っう゛ぉ', ('vvo', 'vvo')), ('ざ', ('za', 'za')), ('す', ('su', 'su')), ('の', ('no', 'no')), ('っす', ('ssu', 'ssu')), ('っきゃ', ('kkya', 'kkya')), ('っご', ('ggo', 'ggo')), ('ね', ('ne', 'ne')), ('っや', ('yya', 'yya')), ('っと', ('tto', 'tto')), ('ぁ', ('xa', 'xa')), ('っじゅ', ('zzyu', 'jju')), ('さ', ('sa', 'sa')), ('ぷ', ('pu', 'pu')), ('しゅ', ('syu', 'shu')), ('ゃ', ('xya', 'xya')), ('っり', ('rri', 'rri')), ('っぎ', ('ggi', 'ggi')), ('っろ', ('rro', 'rro')), ('っびゃ', ('bbya', 'bbya')), ('びゅ', ('byu', 'byu')), ('ちゃ', ('tya', 'cha')), ('ぬ', ('nu', 'nu')), ('りゅ', ('ryu', 'ryu')), ('っぎゅ', ('ggyu', 'ggyu')), ('きょ', ('kyo', 'kyo')), ('っぽ', ('ppo', 'ppo')), ('ぢゃ', ('dya', 'dya')), ('ぉ', ('xo', 'xo')), ('ぎゃ', ('gya', 'gya')), ('きゅ', ('kyu', 'kyu')), ('りょ', ('ryo', 'ryo')), ('しょ', ('syo', 'sho')), ('っぎゃ', ('ggya', 'ggya')), ('った', ('tta', 'tta')), ('ぎょ', ('gyo', 'gyo')), ('っふぇ', ('ffe', 'ffe')), ('っぎょ', ('ggyo', 'ggyo')), ('っしょ', ('ssyo', 'ssho')), ('っば', ('bba', 'bba')), ('っで', ('dde', 'dde')), ('っぼ', ('bbo', 'bbo')), ('し', ('si', 'shi')), ('ぢょ', ('dyo', 'dyo')), ('っぱ', ('ppa', 'ppa')), ('ほ', ('ho', 'ho')), ('っちぇ', ('ttye', 'cche')), ('ぐ', ('gu', 'gu')), ('っら', ('rra', 'rra')), ('じょ', ('zyo', 'jo')), ('べ', ('be', 'be')), ('ぞ', ('zo', 'zo')), ('づ', ('du', 'du')), ('な', ('na', 'na')), ('っぞ', ('zzo', 'zzo')), ('ぢゅ', ('dyu', 'dyu')), ('も', ('mo', 'mo')), ('っへ', ('hhe', 'hhe')), ('っぴゅ', ('ppyu', 'ppyu')), ('ゐ', ('wi', 'wi')), ('っりゅ', ('rryu', 'rryu')), ('る', ('ru', 'ru')), ('ぽ', ('po', 'po')), ('ぼ', ('bo', 'bo')), ('っど', ('ddo', 'ddo')), ('を', ('wo', 'wo')), ('っびょ', ('bbyo', 'bbyo')), ('ゑ', ('we', 'we')), ('っぴゃ', ('ppya', 'ppya')), ('ぴゃ', ('pya', 'pya')), ('っち', ('tti', 'cchi')), ('っぷ', ('ppu', 'ppu')), ('っちゅ', ('ttyu', 'cchu')), ('く', ('ku', 'ku')), ('っぢゃ', ('ddya', 'ddya')), ('にょ', ('nyo', 'nyo')), ('に', ('ni', 'ni')), ('ぴ', ('pi', 'pi')), ('つ', ('tu', 'tsu')), ('っちょ', ('ttyo', 'ccho')), ('ひゅ', ('hyu', 'hyu')), ('っぴょ', ('ppyo', 'ppyo')), ('っざ', ('zza', 'zza')), ('ら', ('ra', 'ra')), ('き', ('ki', 'ki')), ('わ', ('wa', 'wa')), ('っひょ', ('hhyo', 'hhyo')), ('ぢ', ('di', 'di')), ('ゅ', ('xyu', 'xyu')), ('っは', ('hha', 'hha')), ('っじ', ('zzi', 'jji')), ('っう゛ぇ', ('vve', 'vve')), ('っよ', ('yyo', 'yyo')), ('ぴゅ', ('pyu', 'pyu')), ('っき', ('kki', 'kki')), ('っう゛', ('vvu', 'vvu')), ('びょ', ('byo', 'byo')), ('っちゃ', ('ttya', 'ccha')), ('ぅ', ('xu', 'xu')), ('ひ', ('hi', 'hi')), ('びゃ', ('bya', 'bya')), ('っこ', ('kko', 'kko')), ('う゛ぉ', ('vo', 'vo')), ('っる', ('rru', 'rru')), ('きゃ', ('kya', 'kya')), ('え', ('e', 'e')), ('っか', ('kka', 'kka')), ('む', ('mu', 'mu')), ('っぶ', ('bbu', 'bbu'))]

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

for kana, roma in KUNREITAB + HEPBURNTAB:
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

# special modification
# wo -> ヲ, but ヲ/ウォ -> wo
# du -> ヅ, but ヅ/ドゥ -> du
# we -> ウェ, ウェ -> we
ROMKAN.update( {"du": "ヅ", "di": "ヂ", "fu": "フ", "ti": "チ",
                "wi": "ウィ", "we": "ウェ", "wo": "ヲ", "t": 'ッ' } )
ROMKAN_HBN.update( {"du": "ヅ", "di": "ヂ", "fu": "フ", 
                "wi": "ウィ", "we": "ウェ", "wo": "ヲ" } )
ROMKAN_KNR.update( {"du": "ヅ", "di": "ヂ", "ti": "チ",
                "wi": "ウィ", "we": "ウェ", "wo": "ヲ" } )

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

TO_HEPBURN = {}
TO_KUNREI = {}

for kun, hep in zip(KUNREI_SEQS, HEPBURN_SEQS):
    TO_HEPBURN[kun] = hep
    TO_KUNREI[hep] = kun

TO_HEPBURN.update( {'ti': 'chi' })



# Use Hiragana

KANROM_H = {}
ROMKAN_H = {}
KANROM_H_HBN = {}
ROMKAN_H_HBN = {}
KANROM_H_KNR = {}
ROMKAN_H_KNR = {}

for pair in KUNREITAB_H + HEPBURNTAB_H:
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

# special modification
# wo -> ヲ, but ヲ/ウォ -> wo
# du -> ヅ, but ヅ/ドゥ -> du
# we -> ウェ, ウェ -> we
ROMKAN_H.update( {"du": "づ", "di": "ぢ", "fu": "ふ", "ti": "ち",
                "wi": "うぃ", "we": "うぇ", "wo": "を", "t": 'っ' } )
ROMKAN_H_HBN.update( {"du": "づ", "di": "ぢ", "fu": "ふ",
                "wi": "うぃ", "we": "うぇ", "wo": "を" } )
ROMKAN_H_KNR.update( {"du": "づ", "di": "ぢ", "ti": "ち",
                "wi": "うぃ", "we": "うぇ", "wo": "を" } )

# Sort in long order so that a longer Romaji sequence precedes.

ROMPAT_H = re.compile("|".join(sorted(ROMKAN_H.keys(), key=_len_cmp)) )
ROMPAT_H_HBN = re.compile("|".join(sorted(ROMKAN_H_HBN.keys(), key=_len_cmp)) )
ROMPAT_H_KNR = re.compile("|".join(sorted(ROMKAN_H_KNR.keys(), key=_len_cmp)) )

KANPAT_H = re.compile("|".join(sorted(KANROM_H.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_H)))))
KANPAT_H_HBN = re.compile("|".join(sorted(KANROM_H_HBN.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_H_HBN)))))
KANPAT_H_KRE = re.compile("|".join(sorted(KANROM_H_HBN.keys(), key=cmp_to_key(_kanpat_cmp(KANROM_H_HBN)))))

KUNREI_H = [y for (x, y) in KUNREITAB_H]
HEPBURN_H = [y for (x, y) in HEPBURNTAB_H]

KUNPAT_H = re.compile("|".join(sorted(KUNREI_H, key=_len_cmp)) )
HEPPAT_H = re.compile("|".join(sorted(HEPBURN_H, key=_len_cmp)) )

TO_HEPBURN_H = {}
TO_KUNREI_H = {}

for kun, hep in zip(KUNREI_H, HEPBURN_H):
    TO_HEPBURN_H[kun] = hep
    TO_KUNREI_H[hep] = kun

TO_HEPBURN_H.update( {'ti': 'chi' })



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
    Convert a Romaji (ローマ字) to a Katakana (片仮名).
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
    Convert a Romaji (ローマ字) to a Hiragana (平仮名).
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
    Convert a Kana (仮名) or a Kunrei-shiki Romaji (訓令式ローマ字) to a Hepburn Romaji (ヘボン式ローマ字).
    """
    tmp = str
    tmp = tmp.lower()
    tmp = normalize_double_n(tmp)
    tmp = KUNPAT.sub(lambda x: TO_HEPBURN[x.group(0)], tmp)
    
    tmp = KANPAT_HBN.sub(lambda x: KANROM[x.group(0)], tmp)
    tmp = KANPAT_H_HBN.sub(lambda x: KANROM_H[x.group(0)], tmp)
    
    # Remove unnecessary apostrophes
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", "n", tmp)
    
    return tmp

def to_kunrei(str):
    """
    Convert a Kana (仮名) or a Hepburn Romaji (ヘボン式ローマ字) to a Kunrei-shiki Romaji (訓令式ローマ字).
    """
    tmp = str
    tmp = tmp.lower()
    tmp = normalize_double_n(tmp)
    tmp = HEPPAT.sub(lambda x: TO_KUNREI[x.group(0)], tmp)
    
    tmp = KANPAT_KNR.sub(lambda x: KANROM[x.group(0)], tmp)
    tmp = KANPAT_H_KNR.sub(lambda x: KANROM_H[x.group(0)], tmp)
    
    # Remove unnecessary apostrophes
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", "n", tmp)
    
    return tmp

def to_roma(str):
    """
    Convert a Kana (仮名) to a Hepburn Romaji (ヘボン式ローマ字).
    """
    
    tmp = str
    tmp = KANPAT.sub(lambda x: KANROM[x.group(0)], tmp)
    tmp = KANPAT_H.sub(lambda x: KANROM_H[x.group(0)], tmp)
    
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
