import sys
import public
import out_bb
import out_html

#if len(sys.argv)!=2:
#    print ("Usage: %s <input file>"%sys.argv[0])
#    sys.exit(1)

f=open(sys.argv[1] if sys.argv[1:] else "test.md","r")
ret=out_bb.bb_out(public.parse_file(f),"koolamooli")
f.close()
f=open(sys.argv[1] if sys.argv[1:] else "test.md","r") #XXX why needful?
ret2=out_html.html_out(public.parse_file(f),"test.md")
print ret
open("out.txt","w").write(ret)
open("out.html","w").write(ret2)
