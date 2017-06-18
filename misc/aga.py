from mdplay.parse_roma import *

b=open("standard.py").read()
b=eval(b)
for i,j in b:
    for k in j:
        if hiraise(kanafy(k))!=i:
            print "Romaji:",k
            print "Standard says:",i
            print "Library says:",hiraise(kanafy(k))
            print

