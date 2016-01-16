import sys, getopt

import mdplay

def help():
    sys.stderr.write("Usage: pymdplay -f ["+("|".join(mdplay.writers.keys()))+"] [-o out_file] [-t title] [-5] in_file\n")
    sys.exit()

opts,args=getopt.gnu_getopt(sys.argv[1:],"5f:o:h?")
if len(args)!=1: help()

format="bbcode"
output="-"
html5=False
titl=args[0] #default title is input filename

for opt,val in opts:
    if opt in ("-h","-?"):
        help()
    elif opt=="-f":
        format=val
    elif opt=="-o":
        output=val
    elif opt=="-t":
        titl=val
    elif opt=="-5":
        html5=True
    else:
        help()

f=open(args[0],"rU")
try:
    #Two parentheticals, as it is a second-order function: not a mistake
    ret=mdplay.load_renderer(format)(mdplay.parse_file(f),titl,html5)
except mdplay.NoSuchDecoderError:
    help()
f.close()

if output=="-":
    fo=sys.stdout
else:
    fo=open(output,"w")
fo.write(ret)
