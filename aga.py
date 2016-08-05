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
    if to_roma(i) not in j:
        print "Kana:",i
        print "Standard says:", ",".join(j)
        print "Library says:",to_roma(i)
        print
