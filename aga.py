from mdplay.romkan import *

b=open("standard.py").read()
b=eval(b)
for i,j in b:
    for k in j:
        if to_hiragana(k)!=i:
            print "Romaji:",k
            print "Standard says:",i
            print "Library says:",to_hiragana(k)
            print
    if (to_hepburn(i) not in j) and (to_kunrei(i) not in j):
        print "Kana:",i
        print "Standard says:", ",".join(j), "(note this is an input, not output, standard)"
        print "Library says:", to_hepburn(i)+","+to_kunrei(i)
        print
    rth = to_hiragana(to_hepburn(i), HEPBURN)
    rtk = to_hiragana(to_kunrei(i), KUNREI)
    if (rth!=i) or (rtk!=i):
        print "Kana:",i
        print "Hepburn-style round trip:", rth
        print "Kunrei-style round trip:", rtk
        print
