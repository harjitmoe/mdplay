"""Waapuro roomaji parser support module.  By Thomas Hori.

Run as a script in a Unicode UNIX terminal for a demo.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

# To change l-behaviour, remove it from conso and add it to size, or
# even remove it altogether if that's the behaviour you want.
# You may wish to remove r from "extendercons" then, though.
t=tuple
conso_kunrei = t("kgsztdnhbpmyrlwv")
conso = conso_kunrei+t("qjcf")
glide = t("wyh") #assocs keys can constitute exceptions; must be subset of conso
vowel = t("aiueo")
line = t("-^~")
size = t("x")
syllabic = t("n")
termina = t("'\n")
extendercons = t("hr") # Not l though.  Only "h" is definitive.

# Remove e from no_yagyoo (not no_lil_yagyoo) if you wish to use "HIRAGANA LETTER ARCHAIC YE".
# The small-kana sequences remain available via yhe (with i) and ywe (with yu).
no_yagyoo = t("ie")
no_lil_yagyoo = t("ie")
nonglide_have_lil = ("tu",)

assocs_kunrei = {"v":"vu", "yw":"yu"}
assocs_special = {"w":"u", "y":"i"}
assocs_nonkunrei = {"q":"ku", "sh":"si", "j":"zi", "ch":"ti", "c":"ti", "ts":"tu", "dj":"di", "dz":"du", "f":"hu"} # The "dj" is purely because that symbol would not be typeable in force-Hepburn mode otherwise.
assocs_selfplain = ("ku", "yu", "vu")

assocs = assocs_kunrei.copy()
assocs.update(assocs_nonkunrei)
assoc2 = assocs.copy()
assoc2.update(assocs_special)
assoc2_kunrei = assocs_kunrei.copy()
assoc2_kunrei.update(assocs_special)

glivow = {"y":"i", "w":"u", "h":"e", "'":"e"}

def _proc_siz(siz):
    ot = ""
    for c in siz:
        if c in size:
            ot += "x"
        else:
            ot += "xtu"
    return ot

class _PF(object):
    def __init__(self,it):
        self.it = it
        self.pf = []
    def push_front(self,i):
        self.pf.insert(0,i)
    def __iter__(self): return self
    def __next__(self): return self.next()
    def next(self):
        if self.pf: return self.pf.pop(0)
        self.cou += 1
        try: return self.it.__next__()
        except AttributeError: return self.it.next()

def parse_roma(itr, force="none"):
    """Real-time user input roomaji parser / simplifier.

    Call on an iterator generating individual ASCII characters.
    This will separate out the parts representing kana and convert them into
    a highly simplified syntax, yielding as specified below.

    This interface is intended for systems processing user input as it is
    typed.  See kanafy() for cases where a complete roomaji string is
    available.

    The optional second argument is a string out of "hepburn", "kunrei" and
    "none" (default "none") - it specifies whether the input should be
    assumed to be using Hepburn-shiki, using Kunrei-siki/Nippon-siki, or
    just treated normally.

    The following are special characters or signals controlling the parser:

    - NUL, which drains the current sequence (ready to be re-fed a modified
      sequence if applicable).  (The way this works internally, allowing the
      current sequence to be edited while loaded would be complicated.)

    - LF, which forces a termination of the sequence even when it isn't
      unambiguously complete.

    - The StopIteration exception, which cleanly stops the parser (intended
      to be sent on EOF condition).

    The parser yields tuples of the format (not_for_kana, for_kana, count).

    - The first item is a string of ASCII characters which did not parse
      as input for kana, and which occurred before the input processed
      into the second item (it may be empty).

    - The second is a string in a very simple roomaji encoding with each
      character, large or small, represented individually in a Nippon-siki-
      based format (e.g. si / hu / xya / wo).  This is intended as a 
      charset-agnostic method of outputting something which can relatively
      trivially be rendered into kana, given only info about the layout of
      the charset.  The unicify() function, for conversion from this 
      heavily simplified waapuro into Unicode kana, is provided.

    - The third item is the number of input (not special) characters which
      are represented by the first two items.  Any further characters
      which have been input should be treated as the start of the next
      sequence."""
    assert force in ("hepburn","kunrei","none")
    conso = globals()["conso"] #Local copies of global for temp changes
    assocs = globals()["assocs"]
    assoc2 = globals()["assoc2"]
    if force=="kunrei":
        conso = globals()["conso_kunrei"]
        assocs = globals()["assocs_kunrei"]
        assoc2 = globals()["assoc2_kunrei"]
    ovf = ""
    siz = ""
    xcou = 0
    con = gli1 = gli2 = vow = None
    gagh = _PF(itr)
    gagh.cou = 0
    while 1:
        try:
            c = gagh.next()
            if c: c=c.lower()
        except StopIteration:
            c = None
        if c == "\0":
            # i.e. a "forget about it" signal from the input generator
            # in event of deletion of part or all of the current input
            # should be re-fed the still-current parts, if any
            siz = ""
            con = gli1 = gli2 = vow = None
            gagh.cou = xcou = 0
            continue
        if (not c) and (not siz) and (not con) and (not gli1) and (not gli2) and (not vow):
            break
        elif ((siz or None) == con == gli1 == gli2 == vow == None) and (c in line):
            yield (ovf, c, gagh.cou)
            gagh.cou, xcou = xcou, 0
            ovf = ""
            siz = ""
        elif ((siz or None) == con == gli1 == gli2 == vow == None) and (c in size):
            siz = c
        elif (con == gli1 == gli2 == vow == None) and c in conso:
            con = c
        elif (gli1 == gli2 == vow == None) and (c==con):
            if c==con=="n":
                gagh.push_front("'")
                continue
            siz = c+siz
        elif (force != "kunrei") and (gli1 == gli2 == vow == None) and (con=="t") and (c=="c"):
            siz = con+siz
            con = c
        elif (gli1 == gli2 == vow == None) and ( (c in glide) or (c and con and (con in "td") and (c=="'")) or (c and con and (con+c in assocs.keys()) and (force != "kunrei")) ):
            gli1 = c
        elif (gli2 == vow == None) and (c in glide):
            gli2 = c
        elif (vow == None) and (c in vowel):
            vow = c
            gagh.push_front("'")
            continue
        elif siz or con or gli1 or gli2 or vow:
            force_o_as_w = 0
            if c not in termina:
                gagh.push_front(c)
            if force == "hepburn":
                #Of attention: si, zi, ti, tu, di, du, hu
                if (con in t("sz")) and (not (gli1 or gli2)) and (vow == "i"):
                    gli1 = "w"
                elif (con in t("sz")) and (gli1 == "y") and (not gli2):
                    gli1 = "w"
                    gli2 = "y"
                elif (con in t("td")) and (not (gli1 or gli2)) and (vow == "i"):
                    gli1 = "h"
                elif (con in t("td")) and (gli1 == "y") and (not gli2):
                    gli1 = "h"
                    gli2 = "y"
                elif (con in t("tdh")) and (not (gli1 or gli2)) and (vow == "u"):
                    gli1 = "w"
                elif (con in t("tdh")) and (gli1 == "w") and (not gli2) and (vow != "u"):
                    force_o_as_w = 1
            #print siz , con , gli1 , gli2 , vow 
            if not vow:
                if (not gli1) and (not gli2) and (not siz) and (con in syllabic):
                    if c not in termina:
                        gagh.cou -= 1
                        xcou = 1
                    norma = con+"'"
                elif (not gli1) and (not gli2) and (not siz) and (con in extendercons) and (force != "kunrei"):
                    if c not in termina:
                        gagh.cou -= 1
                        xcou = 1
                    norma = "-"
                elif (not gli2) and gli1 and ((con+gli1) in assocs.keys()):
                    if c not in termina:
                        gagh.cou -= 1
                        xcou = 1
                    norma = _proc_siz(siz)+assocs[con+gli1]
                elif (not gli2) and gli1 and ((con+gli1) == "t'"):
                    if c not in termina:
                        gagh.cou -= 1
                        xcou = 1
                    norma = _proc_siz(siz)+"to"
                elif (not gli1) and (not gli2):
                    if c not in termina:
                        gagh.cou -= 1
                        xcou = 1
                    if con in assocs.keys():
                        aso = assocs[con]
                    else:
                        aso = con+"u"
                    #
                    if (not siz) and (aso in nonglide_have_lil):
                        norma = "x"+aso
                    elif (force != "kunrei") and (aso[:-1] == con) and (aso in assocs.values()) and (aso not in assocs_selfplain):
                        norma = _proc_siz(siz)+con+"o"
                    else:
                        norma = _proc_siz(siz)+aso
                else:
                    ovf += siz or con
                    if siz:
                        siz = ""
                    else:
                        con = gli1; gli1 = gli2; gli2 = None
                    continue
            elif (not con) and (not gli1) and (not gli2): # a
                norma = _proc_siz(siz)+vow
            elif (not gli1) and (not gli2): # sa
                if (con == "w") and (vow not in "ao"):
                    if vow!="u":
                        norma = _proc_siz(siz)+"ux"+vow
                    else:
                        norma = _proc_siz(siz)+"wox"+vow
                elif (con == "y") and (vow in no_yagyoo):
                    norma = _proc_siz(siz)+"ix"+vow
                elif con in assocs.keys():
                    aso = assocs[con]
                    if vow == aso[-1]:
                        norma = _proc_siz(siz)+aso
                    elif (vow in no_lil_yagyoo) or (aso[-1] != "i"):
                        norma = _proc_siz(siz)+aso+"x"+vow
                    else:
                        norma = _proc_siz(siz)+aso+"xy"+vow
                else:
                    norma = _proc_siz(siz)+con+vow
            elif (not gli2): # sya
                if (con+gli1) in assoc2:
                    aso = assoc2[con+gli1]
                elif con in assoc2:
                    aso = assoc2[con]
                else:
                    aso = con+glivow[gli1]
                #
                # Special cases for otherwise untypable kana:
                if (gli1 == "y") and (con in "wv") and (vow in no_lil_yagyoo):
                    # Special cases (in standard for wyi/wye)
                    norma = _proc_siz(siz)+con+vow
                elif (gli1 == "w") and (con == "v") and (vow != "u"):
                    # Special cases (mine, undefined in std)
                    norma = _proc_siz(siz)+"v"+vow
                #
                # Rules:
                elif (con+gli1) in assocs:
                    aso = assocs[con+gli1]
                    if vow == aso[-1]:
                        norma = _proc_siz(siz)+aso
                    elif (vow in no_lil_yagyoo) or (aso[-1] != "i"):
                        norma = _proc_siz(siz)+aso+"x"+vow
                    else:
                        norma = _proc_siz(siz)+aso+"xy"+vow
                elif glivow[gli1] == "u":
                    if (aso == (con+"u")) and ((vow == "u") or force_o_as_w):
                        norma = _proc_siz(siz)+con+"ox"+vow
                    elif (aso != (con+"u")) and (vow == "a"):
                        norma = _proc_siz(siz)+aso+"xwa"
                    elif aso[-1] == "u":
                        norma = _proc_siz(siz)+aso+"x"+vow
                    else:
                        norma = _proc_siz(siz)+aso+"xux"+vow
                elif glivow[gli1] == "i":
                    if vow not in no_lil_yagyoo:
                        norma = _proc_siz(siz)+aso+"xy"+vow
                    elif aso[-1]=="i":
                        norma = _proc_siz(siz)+aso+"x"+vow
                    else:
                        norma = _proc_siz(siz)+aso+"xix"+vow
                elif gli1 == "h":
                    if con in assoc2.keys():
                        norma = _proc_siz(siz)+assoc2[con]+"x"+vow
                    elif (vow in no_lil_yagyoo):
                        norma = _proc_siz(siz)+con+"ex"+vow
                    else:
                        norma = _proc_siz(siz)+con+"exy"+vow
                elif gli1 == "'": # con will only be t
                    if vow in t("ue"):
                        norma = _proc_siz(siz)+con+"ox"+vow
                    else:
                        norma = _proc_siz(siz)+con+"ex"+vow
                else:
                    raise RuntimeError("this should never happen")
            else: # swya
                if (con+gli1) in assoc2:
                    aso = assoc2[con+gli1]
                elif con in assoc2:
                    aso = assoc2[con]
                    if aso[-1] != glivow[gli1]:
                        aso += "x"+glivow[gli1]
                else:
                    aso = con+glivow[gli1]
                #
                if gli2 == "w":
                    if vow == "a":
                        norma = _proc_siz(siz)+aso+"xwa"
                    elif aso[-1] == "u":
                        norma = _proc_siz(siz)+aso+"x"+vow
                    elif aso[-1] == "i":
                        norma = _proc_siz(siz)+aso+"xyux"+vow
                    else:
                        norma = _proc_siz(siz)+aso+"xux"+vow
                elif gli2 == "y":
                    if vow not in no_lil_yagyoo:
                        norma = _proc_siz(siz)+aso+"xy"+vow
                    elif aso[-1] == "i":
                        norma = _proc_siz(siz)+aso+"x"+vow
                    else:
                        norma = _proc_siz(siz)+aso+"xix"+vow
                elif gli2 == "h":
                    norma = _proc_siz(siz)+aso+"x"+vow
                else:
                    raise RuntimeError("this should never happen")
            yield (ovf, norma.replace("l","r"), gagh.cou)
            gagh.cou, xcou = xcou, 0
            ovf = ""
            siz = ""
            con = gli1 = gli2 = vow = None
        elif c != "\n":
            ovf += c
        else:
            gagh.cou -= 1 # Signal not included in cou.
    if ovf:
        yield (ovf, None, gagh.cou)

_to_kana = {'gu': '\xe3\x82\xb0', 'xra': '\xe3\x87\xbb', 'ge': '\xe3\x82\xb2', 'ga': '\xe3\x82\xac', 'go': '\xe3\x82\xb4', 'gi': '\xe3\x82\xae', 'xyu': '\xe3\x83\xa5', 'xtu': '\xe3\x83\x83', 'tu': '\xe3\x83\x84', 'to': '\xe3\x83\x88', 'ti': '\xe3\x83\x81', 'xto': '\xe3\x87\xb3', 'xmu': '\xe3\x87\xba', '^': '\xe3\x83\xbc', 'ta': '\xe3\x82\xbf', 'do': '\xe3\x83\x89', 'yo': '\xe3\x83\xa8', 'di': '\xe3\x83\x82', 'ya': '\xe3\x83\xa4', 'de': '\xe3\x83\x87', 'da': '\xe3\x83\x80', 'du': '\xe3\x83\x85', 'yu': '\xe3\x83\xa6', 'xsu': '\xe3\x87\xb2', 't': '\xe3\x83\x83', 'xsi': '\xe3\x87\xb1', 'mo': '\xe3\x83\xa2', 'zo': '\xe3\x82\xbe', 'zi': '\xe3\x82\xb8', 'ze': '\xe3\x82\xbc', 'za': '\xe3\x82\xb6', 'zu': '\xe3\x82\xba', 'ru': '\xe3\x83\xab', 're': '\xe3\x83\xac', 'ra': '\xe3\x83\xa9', 'ro': '\xe3\x83\xad', 'ri': '\xe3\x83\xaa', 'be': '\xe3\x83\x99', 'we': '\xe3\x83\xb1', 'ba': '\xe3\x83\x90', 'wa': '\xe3\x83\xaf', 'wo': '\xe3\x83\xb2', 'bo': '\xe3\x83\x9c', 'bi': '\xe3\x83\x93', 'wi': '\xe3\x83\xb0', 'bu': '\xe3\x83\x96', 'mi': '\xe3\x83\x9f', 'xnu': '\xe3\x87\xb4', 'o': '\xe3\x82\xaa', '~': '\xe3\x80\x9c', 'xu': '\xe3\x82\xa5', 'xi': '\xe3\x82\xa3', 'xo': '\xe3\x82\xa9', 'xa': '\xe3\x82\xa1', 'xe': '\xe3\x82\xa7', 'xya': '\xe3\x83\xa3', 'xyo': '\xe3\x83\xa7', 'pu': '\xe3\x83\x97', '.': '\xe3\x80\x82', 'pa': '\xe3\x83\x91', 'pe': '\xe3\x83\x9a', 'pi': '\xe3\x83\x94', 'po': '\xe3\x83\x9d', 'hu': '\xe3\x83\x95', 'hi': '\xe3\x83\x92', 'ho': '\xe3\x83\x9b', 'ha': '\xe3\x83\x8f', 'he': '\xe3\x83\x98', 'me': '\xe3\x83\xa1', 'xha': '\xe3\x87\xb5', 'te': '\xe3\x83\x86', 'ma': '\xe3\x83\x9e', 'xhe': '\xe3\x87\xb8', 'xhi': '\xe3\x87\xb6', 'xho': '\xe3\x87\xb9', 'mu': '\xe3\x83\xa0', 'xhu': '\xe3\x87\xb7', 'xwa': '\xe3\x83\xae', 'va': '\xe3\x83\xb7', 've': '\xe3\x83\xb9', 'vi': '\xe3\x83\xb8', 'vo': '\xe3\x83\xba', 'vu': '\xe3\x83\xb4', 'ni': '\xe3\x83\x8b', 'xro': '\xe3\x87\xbf', 'xri': '\xe3\x87\xbc', 'no': '\xe3\x83\x8e', 'xre': '\xe3\x87\xbe', 'na': '\xe3\x83\x8a', 'xka': '\xe3\x83\xb5', '-': '\xe3\x83\xbc', 'ne': '\xe3\x83\x8d', 'xke': '\xe3\x83\xb6', 'xru': '\xe3\x87\xbd', 'u': '\xe3\x82\xa6', 'nu': '\xe3\x83\x8c', 'xku': '\xe3\x87\xb0', 'a': '\xe3\x82\xa2', 'ka': '\xe3\x82\xab', 'e': '\xe3\x82\xa8', 'ye': '\xf0\x9b\x80\x81', 'ke': '\xe3\x82\xb1', 'i': '\xe3\x82\xa4', 'ki': '\xe3\x82\xad', 'ko': '\xe3\x82\xb3', 'su': '\xe3\x82\xb9', "n'": '\xe3\x83\xb3', 'si': '\xe3\x82\xb7', 'so': '\xe3\x82\xbd', 'ku': '\xe3\x82\xaf', 'sa': '\xe3\x82\xb5', 'se': '\xe3\x82\xbb'}

_katahiral = [('\xe3\x82\xa1', '\xe3\x81\x81'), ('\xe3\x82\xa2', '\xe3\x81\x82'), ('\xe3\x82\xa3', '\xe3\x81\x83'), ('\xe3\x82\xa4', '\xe3\x81\x84'), ('\xe3\x82\xa5', '\xe3\x81\x85'), ('\xe3\x82\xa6', '\xe3\x81\x86'), ('\xe3\x82\xa7', '\xe3\x81\x87'), ('\xe3\x82\xa8', '\xe3\x81\x88'), ('\xe3\x82\xa9', '\xe3\x81\x89'), ('\xe3\x82\xaa', '\xe3\x81\x8a'), ('\xe3\x82\xab', '\xe3\x81\x8b'), ('\xe3\x82\xac', '\xe3\x81\x8c'), ('\xe3\x82\xad', '\xe3\x81\x8d'), ('\xe3\x82\xae', '\xe3\x81\x8e'), ('\xe3\x82\xaf', '\xe3\x81\x8f'), ('\xe3\x82\xb0', '\xe3\x81\x90'), ('\xe3\x82\xb1', '\xe3\x81\x91'), ('\xe3\x82\xb2', '\xe3\x81\x92'), ('\xe3\x82\xb3', '\xe3\x81\x93'), ('\xe3\x82\xb4', '\xe3\x81\x94'), ('\xe3\x82\xb5', '\xe3\x81\x95'), ('\xe3\x82\xb6', '\xe3\x81\x96'), ('\xe3\x82\xb7', '\xe3\x81\x97'), ('\xe3\x82\xb8', '\xe3\x81\x98'), ('\xe3\x82\xb9', '\xe3\x81\x99'), ('\xe3\x82\xba', '\xe3\x81\x9a'), ('\xe3\x82\xbb', '\xe3\x81\x9b'), ('\xe3\x82\xbc', '\xe3\x81\x9c'), ('\xe3\x82\xbd', '\xe3\x81\x9d'), ('\xe3\x82\xbe', '\xe3\x81\x9e'), ('\xe3\x82\xbf', '\xe3\x81\x9f'), ('\xe3\x83\x80', '\xe3\x81\xa0'), ('\xe3\x83\x81', '\xe3\x81\xa1'), ('\xe3\x83\x82', '\xe3\x81\xa2'), ('\xe3\x83\x83', '\xe3\x81\xa3'), ('\xe3\x83\x84', '\xe3\x81\xa4'), ('\xe3\x83\x85', '\xe3\x81\xa5'), ('\xe3\x83\x86', '\xe3\x81\xa6'), ('\xe3\x83\x87', '\xe3\x81\xa7'), ('\xe3\x83\x88', '\xe3\x81\xa8'), ('\xe3\x83\x89', '\xe3\x81\xa9'), ('\xe3\x83\x8a', '\xe3\x81\xaa'), ('\xe3\x83\x8b', '\xe3\x81\xab'), ('\xe3\x83\x8c', '\xe3\x81\xac'), ('\xe3\x83\x8d', '\xe3\x81\xad'), ('\xe3\x83\x8e', '\xe3\x81\xae'), ('\xe3\x83\x8f', '\xe3\x81\xaf'), ('\xe3\x83\x90', '\xe3\x81\xb0'), ('\xe3\x83\x91', '\xe3\x81\xb1'), ('\xe3\x83\x92', '\xe3\x81\xb2'), ('\xe3\x83\x93', '\xe3\x81\xb3'), ('\xe3\x83\x94', '\xe3\x81\xb4'), ('\xe3\x83\x95', '\xe3\x81\xb5'), ('\xe3\x83\x96', '\xe3\x81\xb6'), ('\xe3\x83\x97', '\xe3\x81\xb7'), ('\xe3\x83\x98', '\xe3\x81\xb8'), ('\xe3\x83\x99', '\xe3\x81\xb9'), ('\xe3\x83\x9a', '\xe3\x81\xba'), ('\xe3\x83\x9b', '\xe3\x81\xbb'), ('\xe3\x83\x9c', '\xe3\x81\xbc'), ('\xe3\x83\x9d', '\xe3\x81\xbd'), ('\xe3\x83\x9e', '\xe3\x81\xbe'), ('\xe3\x83\x9f', '\xe3\x81\xbf'), ('\xe3\x83\xa0', '\xe3\x82\x80'), ('\xe3\x83\xa1', '\xe3\x82\x81'), ('\xe3\x83\xa2', '\xe3\x82\x82'), ('\xe3\x83\xa3', '\xe3\x82\x83'), ('\xe3\x83\xa4', '\xe3\x82\x84'), ('\xe3\x83\xa5', '\xe3\x82\x85'), ('\xe3\x83\xa6', '\xe3\x82\x86'), ('\xe3\x83\xa7', '\xe3\x82\x87'), ('\xe3\x83\xa8', '\xe3\x82\x88'), ('\xe3\x83\xa9', '\xe3\x82\x89'), ('\xe3\x83\xaa', '\xe3\x82\x8a'), ('\xe3\x83\xab', '\xe3\x82\x8b'), ('\xe3\x83\xac', '\xe3\x82\x8c'), ('\xe3\x83\xad', '\xe3\x82\x8d'), ('\xe3\x83\xae', '\xe3\x82\x8e'), ('\xe3\x83\xaf', '\xe3\x82\x8f'), ('\xe3\x83\xb0', '\xe3\x82\x90'), ('\xe3\x83\xb1', '\xe3\x82\x91'), ('\xe3\x83\xb2', '\xe3\x82\x92'), ('\xe3\x83\xb3', '\xe3\x82\x93'), ('\xe3\x83\xb4', '\xe3\x82\x94')]

_katahira = dict(_katahiral)
_hirakata = dict(zip(*zip(*_katahiral)[::-1]))

def unicify(j):
    """Convert parse_roma output to Unicode kana.

    Use only on parse_roma output.  If converting a fixed string of 
    user input, use kanafy, which runs it through parse_roma first.
    For real-time user input, use in conjunction with parse_roma.
    """
    r = u""
    while j:
        u = j
        j = ""
        while (u) and (u not in _to_kana):
            j = u[-1] + j
            u = u[:-1]
        if (not u) and j:
            r += j[0]
            j=j[1:]
        elif u:
            r += _to_kana[u].decode("utf-8")
    return r

class _StringGenIter(object):
    count = 0
    loge = ""
    nulo = 0
    out = ""
    rrom = None
    def __init__(self,roma): self.rrom = list(roma)
    def __iter__(self): return self
    def __next__(self): return self.next()
    def next(self):
        if self.nulo:
            self.out += "\n"
            self.nulo = 0
            self.count = 0
            self.loge = ""
        if not self.rrom:
            raise StopIteration
        r = self.rrom.pop(0)
        if r == "\n":
            self.nulo = 1
            return "\n"
        if (len(r)==1) and (0x20<=ord(r)<0x7f):
            self.loge += r
            self.count += 1
        return r

def kanafy(roma, force="none"):
    """Convert waapuro roomaji string to Unicode Kana.

    Second argument is same as with parse_roma().
    """
    ftdi = _StringGenIter(roma)
    for i,j,cou in parse_roma(ftdi, force):
        ftdi.out += i+unicify(j).encode("utf-8")
    return ftdi.out.decode("utf-8")

def _aggloma(func):
    return lambda i,func=func:u"".join(tuple(func(i)))

@_aggloma
def hiraise(input):
    """Convert Unicode Katakana to Hiragana."""
    for i in input:
        if i.encode("utf-8") in _katahira.keys():
            yield _katahira[i.encode("utf-8")].decode("utf-8")
        else:
            yield i

@_aggloma
def kataise(input):
    """Convert Unicode Hiragana to Katakana."""
    for i in input:
        if i.encode("utf-8") in _hirakata.keys():
            yield _hirakata[i.encode("utf-8")].decode("utf-8")
        else:
            yield i

if __name__=="__main__":
    import tty,sys
    class STDIter(object):
        count = 0
        filed = ""
        pending = ""
        loge = ""
        nulo = 0
        def __iter__(self): return self
        def __next__(self): return self.next()
        def next(self):
            if self.nulo:
                sys.stdout.write("\r\n") #Yes, both (raw mode, so LF is literal LF)
                self.nulo = 0
                self.count = 0
                self.loge = ""
                self.filled = ""
                self.pending = ""
            if self.pending:
                r,self.pending = self.pending[0],self.pending[1:]
                return r
            r = sys.stdin.read(1)
            if r in "\x03": #^C
                raise KeyboardInterrupt #User pressed ^C
            if r in "\x04\x1A": #^D and ^Z
                raise StopIteration
            if r == "\r": #Raw terminal mode, remember
                self.nulo = 1
                return "\n"
            if r in "\b\x7f": #Backspace and Rubout
                sys.stdout.write("\b \b")
                if self.count:
                    self.count -= 1
                    self.pending, self.filed = self.filed[:-1], ""
                    return "\0"
                return self.next()
            if (len(r)==1) and (0x20<=ord(r)<0x7f):
                self.loge += r
                sys.stdout.write(r)
                self.filed += r
                self.count += 1
            return r
    stdi = STDIter()
    det = 0
    bts = tty.tcgetattr(0)
    try:
        tty.setraw(0, tty.TCSANOW)
        for i,j,cou in parse_roma(stdi):
            #print stdi.count,cou
            sys.stdout.write("\b"*(stdi.count))
            sys.stdout.write(" "*(stdi.count))
            sys.stdout.write("\b"*(stdi.count))
            det = stdi.count-cou
            #print "\r\n\r\n",stdi.count,cou,det,`stdi.loge[-det:]`,"\r\n\r\n"
            stdi.filed = ""
            stdi.count = 0
            if det>0:
                stdi.count = det
                stdi.filed = stdi.loge[-det:]
            sys.stdout.write(i+unicify(j))
            if det>0:
                sys.stdout.write(stdi.loge[-det:])
    finally:
        tty.tcsetattr(0, tty.TCSANOW, bts)
    sys.stdout.write("\n")
