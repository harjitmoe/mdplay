"""Waapuro roomaji parser support module.  By HarJIT.

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
syllabic = t("nm")
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
    def __next__(self): return next(self)
    def __next__(self):
        if self.pf: return self.pf.pop(0)
        self.cou += 1
        try: return self.it.__next__()
        except AttributeError: return next(self.it)

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

    - NUL, which drops the current sequence (ready to be re-fed a modified
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
            c = next(gagh)
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
        elif (gli1 == gli2 == vow == None) and ( (c in glide) or (c and con and (con in "td") and (c=="'")) or (c and con and (con+c in list(assocs.keys())) and (force != "kunrei")) ):
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
                #Of attention: si, zi, ti, tu, di, du, debatably hu
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
                #Below would be tdh not td, but "hu" was acknowleged by Hepburn and is used
                #in at least one variant of Hepburn.
                elif (con in t("td")) and (not (gli1 or gli2)) and (vow == "u"):
                    gli1 = "w"
                elif (con in t("td")) and (gli1 == "w") and (not gli2) and (vow != "u"):
                    force_o_as_w = 1
            #print siz , con , gli1 , gli2 , vow 
            if not vow:
                if (not gli1) and (not gli2) and (not siz) and (con in syllabic):
                    if c not in termina:
                        gagh.cou -= 1
                        xcou = 1
                    norma = (con if con != "m" else "n")+"'"
                elif (not gli1) and (not gli2) and (not siz) and (con in extendercons) and (force != "kunrei"):
                    if c not in termina:
                        gagh.cou -= 1
                        xcou = 1
                    norma = "-"
                elif (not gli2) and gli1 and ((con+gli1) in list(assocs.keys())):
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
                    if con in list(assocs.keys()):
                        aso = assocs[con]
                    else:
                        aso = con+"u"
                    #
                    if (not siz) and (aso in nonglide_have_lil):
                        norma = "x"+aso
                    elif (force != "kunrei") and (aso[:-1] == con) and (aso in list(assocs.values())) and (aso not in assocs_selfplain):
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
                elif con in list(assocs.keys()):
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
                    if con in list(assoc2.keys()):
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

_to_kana = {'gu': '\u30b0', '-': '\u30fc', 'ge': '\u30b2', 'ga': '\u30ac', 'go': '\u30b4', 'gi': '\u30ae', 'xo': '\u30a9', 'xtu': '\u30c3', 'tu': '\u30c4', 'to': '\u30c8', 'ti': '\u30c1', 'xto': '\u31f3', 'xmu': '\u31fa', '^': '\u30fc', 'ta': '\u30bf', 'do': '\u30c9', 'yo': '\u30e8', 'di': '\u30c2', 'ya': '\u30e4', 'de': '\u30c7', 'ye': '\U0001b001', 'da': '\u30c0', 'du': '\u30c5', 'yu': '\u30e6', 'xsu': '\u31f2', 't': '\u30c3', 'xsi': '\u31f1', 'xhi': '\u31f6', 'zo': '\u30be', 'zi': '\u30b8', 'ze': '\u30bc', 'za': '\u30b6', 'zu': '\u30ba', 'ru': '\u30eb', 're': '\u30ec', 'ra': '\u30e9', 'ro': '\u30ed', 'ri': '\u30ea', 'be': '\u30d9', 'we': '\u30f1', 'ba': '\u30d0', 'wa': '\u30ef', 'wo': '\u30f2', 'bo': '\u30dc', 'bi': '\u30d3', 'wi': '\u30f0', 'bu': '\u30d6', 'xyo': '\u30e7', 'xnu': '\u31f4', 'so': '\u30bd', 'o': '\u30aa', '~': '\u301c', 'xi': '\u30a3', 'xyu': '\u30e5', 'xa': '\u30a1', 'xe': '\u30a7', 'xya': '\u30e3', 'xu': '\u30a5', 'pu': '\u30d7', '.': '\u3002', 'pa': '\u30d1', 'pe': '\u30da', 'pi': '\u30d4', 'po': '\u30dd', 'hu': '\u30d5', 'hi': '\u30d2', 'ho': '\u30db', 'ha': '\u30cf', 'he': '\u30d8', 'me': '\u30e1', 'xha': '\u31f5', 'te': '\u30c6', 'ma': '\u30de', 'xhe': '\u31f8', 'mo': '\u30e2', 'xho': '\u31f9', 'mu': '\u30e0', 'xhu': '\u31f7', 'xwa': '\u30ee', 'va': '\u30f7', 've': '\u30f9', 'vi': '\u30f8', 'vo': '\u30fa', 'vu': '\u30f4', 'ni': '\u30cb', 'xro': '\u31ff', 'xri': '\u31fc', 'no': '\u30ce', 'xre': '\u31fe', 'na': '\u30ca', 'xka': '\u30f5', 'xra': '\u31fb', 'ne': '\u30cd', 'xke': '\u30f6', 'xru': '\u31fd', 'mi': '\u30df', 'nu': '\u30cc', 'xku': '\u31f0', 'a': '\u30a2', 'ka': '\u30ab', 'e': '\u30a8', 'ke': '\u30b1', 'i': '\u30a4', 'ki': '\u30ad', 'ko': '\u30b3', 'su': '\u30b9', "n'": '\u30f3', 'si': '\u30b7', 'u': '\u30a6', 'ku': '\u30af', 'sa': '\u30b5', 'se': '\u30bb'}

_to_dumbroma = {}

for (k, v) in _to_kana.items():
    _to_dumbroma[v] = k

#Note: do not add Small Ke - must remain Katakana.
_katahiral = [('\u30a1', '\u3041'), ('\u30a2', '\u3042'), ('\u30a3', '\u3043'), ('\u30a4', '\u3044'), ('\u30a5', '\u3045'), ('\u30a6', '\u3046'), ('\u30a7', '\u3047'), ('\u30a8', '\u3048'), ('\u30a9', '\u3049'), ('\u30aa', '\u304a'), ('\u30ab', '\u304b'), ('\u30ac', '\u304c'), ('\u30ad', '\u304d'), ('\u30ae', '\u304e'), ('\u30af', '\u304f'), ('\u30b0', '\u3050'), ('\u30b1', '\u3051'), ('\u30b2', '\u3052'), ('\u30b3', '\u3053'), ('\u30b4', '\u3054'), ('\u30b5', '\u3055'), ('\u30b6', '\u3056'), ('\u30b7', '\u3057'), ('\u30b8', '\u3058'), ('\u30b9', '\u3059'), ('\u30ba', '\u305a'), ('\u30bb', '\u305b'), ('\u30bc', '\u305c'), ('\u30bd', '\u305d'), ('\u30be', '\u305e'), ('\u30bf', '\u305f'), ('\u30c0', '\u3060'), ('\u30c1', '\u3061'), ('\u30c2', '\u3062'), ('\u30c3', '\u3063'), ('\u30c4', '\u3064'), ('\u30c5', '\u3065'), ('\u30c6', '\u3066'), ('\u30c7', '\u3067'), ('\u30c8', '\u3068'), ('\u30c9', '\u3069'), ('\u30ca', '\u306a'), ('\u30cb', '\u306b'), ('\u30cc', '\u306c'), ('\u30cd', '\u306d'), ('\u30ce', '\u306e'), ('\u30cf', '\u306f'), ('\u30d0', '\u3070'), ('\u30d1', '\u3071'), ('\u30d2', '\u3072'), ('\u30d3', '\u3073'), ('\u30d4', '\u3074'), ('\u30d5', '\u3075'), ('\u30d6', '\u3076'), ('\u30d7', '\u3077'), ('\u30d8', '\u3078'), ('\u30d9', '\u3079'), ('\u30da', '\u307a'), ('\u30db', '\u307b'), ('\u30dc', '\u307c'), ('\u30dd', '\u307d'), ('\u30de', '\u307e'), ('\u30df', '\u307f'), ('\u30e0', '\u3080'), ('\u30e1', '\u3081'), ('\u30e2', '\u3082'), ('\u30e3', '\u3083'), ('\u30e4', '\u3084'), ('\u30e5', '\u3085'), ('\u30e6', '\u3086'), ('\u30e7', '\u3087'), ('\u30e8', '\u3088'), ('\u30e9', '\u3089'), ('\u30ea', '\u308a'), ('\u30eb', '\u308b'), ('\u30ec', '\u308c'), ('\u30ed', '\u308d'), ('\u30ee', '\u308e'), ('\u30ef', '\u308f'), ('\u30f0', '\u3090'), ('\u30f1', '\u3091'), ('\u30f2', '\u3092'), ('\u30f3', '\u3093'), ('\u30f4', '\u3094')]


_katahira = dict(_katahiral)
_hirakata = dict(zip(_katahira.values(), _katahira.keys()))

def unicify(j):
    """Convert parse_roma output to Unicode kana.

    Use only on parse_roma output.  If converting a fixed string of 
    user input, use kanafy, which runs it through parse_roma first.
    For real-time user input, use in conjunction with parse_roma.
    """
    r = ""
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
            r += _to_kana[u]
    return r

class _StringGenIter(object):
    count = 0
    loge = ""
    nulo = 0
    out = ""
    rrom = None
    def __init__(self,roma): self.rrom = list(roma)
    def __iter__(self): return self
    def __next__(self):
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
        ftdi.out += i+unicify(j)
    return ftdi.out

def _aggloma(func):
    return lambda i,func=func:"".join(tuple(func(i)))

@_aggloma
def hiraise(inpt):
    """Convert Unicode Katakana to Hiragana."""
    for i in inpt:
        if i in _katahira:
            yield _katahira[i]
        else:
            yield i

@_aggloma
def kataise(inpt):
    """Convert Unicode Hiragana to Katakana."""
    for i in inpt:
        if i in _hirakata:
            yield _hirakata[i]
        else:
            yield i

if __name__=="__main__":
    import tty, sys
    class STDIter(object):
        count = 0
        filed = ""
        pending = ""
        loge = ""
        nulo = 0
        def __iter__(self): return self
        def __next__(self):
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
            sys.stdout.flush()
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
                return next(self)
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
