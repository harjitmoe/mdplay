# -*- mode: python; coding: utf-8 -*-

# *** ATTENTION - IF YOU CHANGE THIS FILE, DELETE data.pickle PRECALC CACHE FILE ***

from __future__ import unicode_literals

class Firenze(list):
    start = 0
    def push(self, id, elem):
        """Push front if id==1, back if id==0, original front if id==2."""
        if id==1: return self.append(elem)
        self.start += 1
        if id==2: return self.insert(self.start-1,elem)
        if id==0: return self.insert(0,elem)
        raise ValueError

#Note - not a dict.  Order is important, and keys are not necessarily unique.
KATATAB=Firenze([('ヵ',('xka','xka')), ('ㇰ',('xku','xku')), ('ヶ',('xke','xke')), ('ㇱ',('xsi','xshi')), ('ㇲ',('xsu','xsu')), ('ㇳ',('xto','xto')), ('ㇴ',('xnu','xnu')), ('ㇵ',('xha','xha')), ('ㇶ',('xhi','xhi')), ('ㇷ',('xhu','xfu')), ('ㇸ',('xhe','xhe')), ('ㇹ',('xho','xho')), ('ㇺ',('xmu','xmu')), ('ㇻ',('xra','xra')), ('ㇼ',('xri','xri')), ('ㇽ',('xru','xru')), ('ㇾ',('xre','xre')), ('ㇿ',('xro','xro')), ('ヨ', ('yo', 'yo')), ('ル', ('ru', 'ru')), ('ォ', ('xo', 'xo')), ('シ', ('si', 'shi')), ('ボ', ('bo', 'bo')), ('オ', ('o', 'o')), ('ジ', ('zi', 'ji')), ('ウ', ('u', 'u')), ('ヤ', ('ya', 'ya')), ('デ', ('de', 'de')), ("ー", ("^", "^")), ('ー', ('-', '-')), ('ヅ', ('du', 'dzu')), ('ド', ('do', 'do')), ('ヘ', ('he', 'he')), ('ヰ', ('wi', 'wi')), ('ョ', ('xyo', 'xyo')), ('ャ', ('xya', 'xya')), ('ェ', ('xe', 'xe')), ('ベ', ('be', 'be')), ('カ', ('ka', 'ka')), ('ハ', ('ha', 'ha')), ('メ', ('me', 'me')), ('ラ', ('ra', 'ra')), ('ヷ', ('va', 'va')), ('ヸ', ('vi', 'vi')), ('ヴ', ('vu', 'vu')), ('ヹ', ('ve', 've')), ('ヺ', ('vo', 'vo')), ('ポ', ('po', 'po')), ('ヮ', ('xwa', 'xwa')), 
('フ', ('hu', 'hu')), #"fu is an aspirate, and might, for the sake of uniformity, be written hu." -- Hepburn himself.
('フ', ('hu', 'fu')), #Later so higher priority
('ホ', ('ho', 'ho')), ('ア', ('a', 'a')), ('ム', ('mu', 'mu')), ('ァ', ('xa', 'xa')), ('エ', ('e', 'e')), ('ゴ', ('go', 'go')),
('チ', ('ti', 'ci')), #'Thus, "tsi" [see later] "ti" "ci" and "chi" will all yield the same "kana" symbol even though only "ti" and "chi" conform to known systems.' -- https://web.archive.org/web/20080416175444/http://www.cic.sfu.ca/tqj/JapaneseStudy/romaji.html (well, it certainly isn't Kunrei!) ---- BUT -- tsi should yield tuxi, nonetheless cya should yield tixya -- https://ja.wikipedia.org/wiki/%E3%83%AD%E3%83%BC%E3%83%9E%E5%AD%97%E5%85%A5%E5%8A%9B
('チ', ('ti', 'chi')), #Higher priority! (later in list)
('ワ', ('wa', 'wa')), ('サ', ('sa', 'sa')), ('ヲ', ('wo', 'wo')), ('ロ', ('ro', 'ro')), ('バ', ('ba', 'ba')), ('リ', ('ri', 'ri')), ('ギ', ('gi', 'gi')), ('パ', ('pa', 'pa')), ('タ', ('ta', 'ta')), ('ガ', ('ga', 'ga')), ('ニ', ('ni', 'ni')), ('ュ', ('xyu', 'xyu')), ('ザ', ('za', 'za')), ('キ', ('ki', 'ki')), ('ィ', ('xi', 'xi')), ('コ', ('ko', 'ko')), ('レ', ('re', 're')), ('ゼ', ('ze', 'ze')), ('グ', ('gu', 'gu')), ('ユ', ('yu', 'yu')), ('ン', ("n'", "m'")), ('ン', ('n', 'm')), ('ン', ("n'", "n'")), ('ン', ('n', 'n')), ('ツ', ('tu', 'tsu')), ('ヂ', ('di', 'dzi')),  ('ヂ', ('di', 'dji')), ('ビ', ('bi', 'bi')), ('ソ', ('so', 'so')), ('ヱ', ('we', 'we')), ('ト', ('to', 'to')), ('プ', ('pu', 'pu')), ('ク', ('ku', 'ku')), ('ゾ', ('zo', 'zo')), ('ゥ', ('xu', 'xu')), ('ペ', ('pe', 'pe')), ('ミ', ('mi', 'mi')), ('イ', ('i', 'i')), ('ゲ', ('ge', 'ge')), ('ピ', ('pi', 'pi')), ('ケ', ('ke', 'ke')), ('ズ', ('zu', 'zu')), ('モ', ('mo', 'mo')), ('ダ', ('da', 'da')), ('ノ', ('no', 'no')), ('ブ', ('bu', 'bu')), ('マ', ('ma', 'ma')), ('ナ', ('na', 'na')), ('ス', ('su', 'su')), ('ッ', ('t', 't')), ('ッ', ('xtu', 'xtsu')), ('ヌ', ('nu', 'nu')), ('セ', ('se', 'se')), ('ヒ', ('hi', 'hi')), ('ネ', ('ne', 'ne')), ('テ', ('te', 'te')), ("～", ("~", "~")), ("〜", ("~", "~")), ("。", (".", "."))])

TOHIRA = {'ィ': 'ぃ', 'ク': 'く', 'ヒ': 'ひ', 'ェ': 'ぇ', 'ブ': 'ぶ', 'ゾ': 'ぞ', 'ヮ': 'ゎ', 'ヲ': 'を', 'バ': 'ば', 'ォ': 'ぉ', 'ミ': 'み', 'ヅ': 'づ', 'ズ': 'ず', 'ヨ': 'よ', 'ダ': 'だ', 'ョ': 'ょ', 'ラ': 'ら', 'ュ': 'ゅ', 'ー': 'ー', 'ゲ': 'げ', 'プ': 'ぷ', 'ス': 'す', 'ド': 'ど', 'ヰ': 'ゐ', 'ヌ': 'ぬ', 'ジ': 'じ', 'ザ': 'ざ', 'セ': 'せ', 'コ': 'こ', 'ツ': 'つ', 'ネ': 'ね', 'テ': 'て', 'マ': 'ま', 'ワ': 'わ', 'ノ': 'の', 'チ': 'ち', 'シ': 'し', 'グ': 'ぐ', 'デ': 'で', 'エ': 'え', 'ロ': 'ろ', 'パ': 'ぱ', 'フ': 'ふ', 'ボ': 'ぼ', 'オ': 'お', 'ウ': 'う', 'ホ': 'ほ', 'ヱ': 'ゑ', 'ペ': 'ぺ', 'サ': 'さ', 'モ': 'も', 'タ': 'た', 'ハ': 'は', 'ッ': 'っ', 'ビ': 'び', 'ソ': 'そ', 'ヴ': 'ゔ', 'ヂ': 'ぢ', 'ゼ': 'ぜ', 'ヘ': 'へ', 'ピ': 'ぴ', 'ゥ': 'ぅ', 'ム': 'む', 'ト': 'と', 'ル': 'る', 'カ': 'か', 'ユ': 'ゆ', 'ゴ': 'ご', 'ア': 'あ', 'キ': 'き', 'ガ': 'が', 'リ': 'り', 'ベ': 'べ', 'ァ': 'ぁ', 'ギ': 'ぎ', 'レ': 'れ', 'ン': 'ん', 'メ': 'め', 'ナ': 'な', 'ヤ': 'や', 'ポ': 'ぽ', 'イ': 'い', 'ケ': 'け', 'ャ': 'ゃ', 'ニ': 'に'}