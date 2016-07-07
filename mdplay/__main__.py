import sys, getopt

import mdplay

def help():
    sys.stderr.write("\nUsage: pymdplay -f ["+("|".join(mdplay.writers.keys()))+"] [-o out_file] [-t title] [-P parserflag,parserflag...] [-W writerflag,writerflag...] [-5] [-s] in_file\n\n")
    sys.stderr.write("""\
You put %s.

html generates XHTML, which may cause IE to bork if it parses empty 
<a> tags etc as HTML, htmlalt generates HTML which is hopefully valid
XHTML also.

For an exhaustive list of flags, see flag_chart.md

Parser flag uicode enables detection of sufficiently large indents
as code blocks, a la standard behaviour, rather than assuming indents
are purely aesthetic unless indicated otherwise.

Parser flag "strict" disables syntax extensions, some of which are
shared by other implementations.

Parser flag notable isn't "notable", it's "no table".

Writer flag html5 enables HTML5 output.  -5 (five) is a shorthand.
"""%sys.argv)
    sys.exit()

try:
    opts,args=getopt.gnu_getopt(sys.argv[1:],"5f:o:h?P:W:s")
except getopt.GetoptError:
    help()

if len(args)==0: args.append("-")
if len(args)!=1: help()

format="bbcode"
input=args[0]
output="-"
titl=args[0] #default title is input filename
flags=[]
oflags=[]
nostart=0

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
    elif opt=="-s":
        nostart=1
    else:
        help()

sys.stderr.write("\nMDPlay by HarJIT (use -s (lowercase S) to suppress this message)\n")

if input!="-":
    f=open(input,"rU")
else:
    f=sys.stdin
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
