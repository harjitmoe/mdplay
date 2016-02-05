import sys, getopt

import mdplay

def help():
    sys.stderr.write("\nUsage: pymdplay -f ["+("|".join(mdplay.writers.keys()))+"] [-o out_file] [-t title] [-P parserflag,parserflag...] [-W writerflag,writerflag...] [-5] in_file\n\n")
    sys.stderr.write("""\
Parser flag uicode enables detection of sufficiently large indents
as code blocks, a la standard behaviour, rather than assuming indents
are purely aesthetic unless indicated otherwise.

Writer flag html5 enables HTML5 output.  -5 is a shorthand.
""")
    sys.exit()

try:
    opts,args=getopt.gnu_getopt(sys.argv[1:],"5f:o:h?P:W:")
except getopt.GetoptError:
    help()

if len(args)!=1: help()

format="bbcode"
output="-"
titl=args[0] #default title is input filename
flags=[]
oflags=[]

for opt,val in opts:
    if opt in ("-h","-?"):
        help()
    elif opt=="-f":
        format=val
    elif opt=="-P":
        flags.extend(val.split(","))
    elif opt=="-W":
        oflags.extend(val.split(","))
    elif opt=="-o":
        output=val
    elif opt=="-t":
        titl=val
    elif opt=="-5":
        oflags.append("html5")
    else:
        help()

f=open(args[0],"rU")
try:
    #Two parentheticals, as it is a second-order function: not a mistake
    ret=mdplay.load_renderer(format)(mdplay.parse_file(f,flags),titl,oflags)
except mdplay.NoSuchRendererError:
    help()
f.close()

if output=="-":
    fo=sys.stdout
else:
    fo=open(output,"w")
fo.write(ret)
