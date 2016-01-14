import sys, getopt

import public
import out_bb
import out_html

def help():
    sys.stderr.write("Usage: mdplay -f [bbcode|html] [-o out_file] [-t title] in_file\n")
    sys.exit()

opts,args=getopt.gnu_getopt(sys.argv[1:],"f:o:h?")
if len(args)!=1: help()

format="bbcode"
output="-"
titl=args[0]

for opt,val in opts:
    if opt in ("-h","-?"):
        help()
    elif opt=="-f":
        format=val
    elif opt=="-o":
        output=val
    elif opt=="-t":
        titl=val
    else:
        help()

f=open(args[0],"rU")
if format=="bbcode":
    ret=out_bb.bb_out(public.parse_file(f),titl)
elif format=="html":
    ret=out_html.html_out(public.parse_file(f),titl)
else:
    help()
f.close()

if output=="-":
    fo=sys.stdout
else:
    fo=open(output,"w")
fo.write(ret)
