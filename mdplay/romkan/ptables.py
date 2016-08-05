# -*- mode: python; coding: utf-8 -*-

#File by Thomas Hori - part of MDPlay.

from __future__ import unicode_literals

import unicodedata

from .tables import *

def gen_tabs():
    for ka,(ku,he) in KATATAB[:]:
        if ((len(ku)==2) and (ku[0] in "wv") and (ku[-1] in "ie")):
            KATATAB.push(0,(ka,(ku[0]+"y"+ku[1],ku[0]+"y"+ku[1])))
        if ku in ("va","vo"):
            KATATAB.push(0,(ka,(ku[0]+"h"+ku[1],ku[0]+"h"+ku[1]))) #For want of a better
        if (len(ku) == 2) and ((ku[-1] == "i") or (ku in ("wu","vu","hu","tu"))) and (ku not in ("wi", "vi")):
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
            if ku not in ("wu", "vu"):
                KATATAB.push(apriori,(ka+"ェ",(ku[:-1]+"ye",hepstem+"e")))
            KATATAB.push(apriori,(ka+"ョ",(ku[:-1]+"yo",hepstem+"o")))
            if hepstem[-1]!="y":
                KATATAB.push(2,(ka+"ャ",(ku[:-1]+"ya",hepstem+"ya")))
                KATATAB.push(2,(ka+"ュ",(ku[:-1]+"yu",hepstem+"yu")))
                if ku not in ("wu", "vu"):
                    KATATAB.push(2,(ka+"ェ",(ku[:-1]+"ye",hepstem+"ye")))
                KATATAB.push(2,(ka+"ョ",(ku[:-1]+"yo",hepstem+"yo")))
            if ku=="tu": #XXX Kunrei is undefined, listing Kr same as Hb for now
                KATATAB.push(0,(ka+"ァ",("tsa","tsa")))
                KATATAB.push(0,(ka+"ィ",("tsi","tsi")))
                KATATAB.push(0,(ka+"ェ",("tse","tse")))
                KATATAB.push(0,(ka+"ォ",("tso","tso")))
        if (len(ku)==2) and (ku in ("su","zu","te","de","to","do","ho")):
            if ku[1]=="u":
                KATATAB.push(0,(ka+"ィ",(ku[:-1]+"yi",ku[:-1]+"i")))
                KATATAB.push(0,(ka+"ィ",(ku[:-1]+"i", ku[:-1]+"i")))
            elif ku[1]=="e":
                KATATAB.push(0,(ka+"ィ",(ku[:-1]+"'i", ku[:-1]+"i")))
                KATATAB.push(0,(ka+"ュ",(ku[:-1]+"'yu", ku[:-1]+"yu")))
                KATATAB.push(0,(ka+"ャ",(ku[:-1]+"ha", ku[:-1]+"ya")))
                KATATAB.push(0,(ka+"ィ",(ku[:-1]+"hi", ku[:-1]+"i")))
                KATATAB.push(0,(ka+"ュ",(ku[:-1]+"hu", ku[:-1]+"yu")))
                KATATAB.push(0,(ka+"ョ",(ku[:-1]+"ho", ku[:-1]+"yo")))
            elif ku[1]=="o":
                KATATAB.push(0,(ka+"ゥ",(ku[:-1]+"u", ku[:-1]+"u")))
        if (len(ku)==2) and (ku[1]=="o"):
            KATATAB.push(1,(ka+"ゥ",(ku[:-1]+"'u", ku[:-1]+"wu")))
        #NOT elif
        if (len(ku)<=2) and (ku[-1] == "u"):
            kku = ku; hhe = he
            if kku == "u":
                kku = hhe = "wu"
            else: 
                # Not ヮ for some reason
                # https://ja.wikipedia.org/wiki/%E3%83%AD%E3%83%BC%E3%83%9E%E5%AD%97%E5%85%A5%E5%8A%9B
                KATATAB.push(0,(ka+"ァ",(kku[:-1]+"wa",hhe[:-1]+"wa")))
                KATATAB.push(0,(ka+"ィ",(kku[:-1]+"wi",hhe[:-1]+"wi")))
                KATATAB.push(0,(ka+"ェ",(kku[:-1]+"we",hhe[:-1]+"we")))
                KATATAB.push(0,(ka+"ォ",(kku[:-1]+"wo",hhe[:-1]+"wo")))
                KATATAB.push(0,(ka+"ャ",(kku[:-1]+"wya",hhe[:-1]+"wya")))
                KATATAB.push(0,(ka+"ュ",(kku[:-1]+"wyu",hhe[:-1]+"wyu")))
                KATATAB.push(0,(ka+"ョ",(kku[:-1]+"wyo",hhe[:-1]+"wyo")))
                if kku[0]=="k":
                    KATATAB.push(0,(ka+"ァ",(kku[:-1]+"wa","qa")))
                    KATATAB.push(0,(ka+"ィ",(kku[:-1]+"wi","qi")))
                    KATATAB.push(0,(ka+"ェ",(kku[:-1]+"we","qe")))
                    KATATAB.push(0,(ka+"ォ",(kku[:-1]+"wo","qo")))
            if (ku[0] not in "sztdhv"):
                KATATAB.push(0,(ka+"ァ",(kku[:-1]+"ha",hhe[:-1]+"ha")))
                KATATAB.push(0,(ka+"ィ",(kku[:-1]+"hi",hhe[:-1]+"hi")))
                KATATAB.push(0,(ka+"ゥ",(kku[:-1]+"hu",hhe[:-1]+"hu")))
                KATATAB.push(0,(ka+"ェ",(kku[:-1]+"he",hhe[:-1]+"he")))
                KATATAB.push(0,(ka+"ォ",(kku[:-1]+"ho",hhe[:-1]+"ho")))
                if kku[0]=="w":
                    KATATAB.push(0,(ka+"ャ",(kku[:-1]+"ya",hhe[:-1]+"ya")))
                    KATATAB.push(0,(ka+"ュ",(kku[:-1]+"yu",hhe[:-1]+"yu")))
                    KATATAB.push(0,(ka+"ョ",(kku[:-1]+"yo",hhe[:-1]+"yo")))
        if ku == "u":
            KATATAB.push(1,(ka+"ィ",("wi","wi")))
            KATATAB.push(1,(ka+"ゥ",("wu","wu"))) # wo is after u in tables.py
            KATATAB.push(1,(ka+"ェ",("we","we")))
            KATATAB.push(0,(ka+"ォ",("wo","wo")))
        if ku == "wo":
            KATATAB.push(1,(ka+"ゥ",("wu","wu")))
        if he in ("fu","vu"):
            apriori = (ku[0]=="v")
            if apriori:
                KATATAB.push(apriori,(ka+"ィ",(ku[:-1]+"hi",he[:-1]+"i")))
                KATATAB.push(apriori,(ka+"ゥ",(ku[:-1]+"hu",he[:-1]+"u")))
                KATATAB.push(apriori,(ka+"ェ",(ku[:-1]+"he",he[:-1]+"e")))
            KATATAB.push(apriori,(ka+"ァ",(ku[:-1]+"a",he[:-1]+"a")))
            KATATAB.push(apriori,(ka+"ィ",(ku[:-1]+"i",he[:-1]+"i")))
            KATATAB.push(apriori,(ka+"ェ",(ku[:-1]+"e",he[:-1]+"e")))
            KATATAB.push(apriori,(ka+"ォ",(ku[:-1]+"o",he[:-1]+"o")))
            if not apriori:
                KATATAB.push(apriori,(ka+"ァ",(ku[:-1]+"ha",he[:-1]+"a")))
                KATATAB.push(apriori,(ka+"ィ",(ku[:-1]+"hi",he[:-1]+"i")))
                KATATAB.push(apriori,(ka+"ェ",(ku[:-1]+"he",he[:-1]+"e")))
                KATATAB.push(apriori,(ka+"ォ",(ku[:-1]+"ho",he[:-1]+"o")))
        if ku == "i":
            KATATAB.push(1,(ka+"ェ",("ye","ye")))
        if ku == "yu":
            KATATAB.push(1,(ka+"ィ",("yi","yi")))
            KATATAB.push(0,(ka+"ェ",("ye","ye")))
    #Must be seperate to and after the previous:
    for ka,(ku,he) in KATATAB[:]:
        if ku[0] not in "xaiueo-~.":
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
                ## Unsure which is more elegant:
                #return None
                return i
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
    return KUNREITAB, HEPBURNTAB, KUNREITAB_H, HEPBURNTAB_H

KUNREITAB, HEPBURNTAB, KUNREITAB_H, HEPBURNTAB_H = gen_tabs()
