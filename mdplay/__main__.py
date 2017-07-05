import sys, getopt

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import mdplay

def help():
    sys.stderr.write("\nUsage: pymdplay -f ["+("|".join(mdplay.writernames))+"] [-F writer_mode] [-o out_file] [-t title] [-P parserflag,parserflag...] [-W writerflag,writerflag...] [-5] [-s] in_file\n\n")
    sys.stderr.write("""\
You put %s.

Writer modes only used by the html renderer, those appropriate for
general interchange are html and xhtml

Writer flag html5 enables HTML5 output.  -5 (five) is a shorthand.

For a list of flags, see flag_chart.md

Parser flag "strict" disables syntax extensions, some of which are
shared by other implementations.

Parser flag notable isn't "notable", it's "no table".
"""%sys.argv)
    sys.exit()

try:
    opts,args = getopt.gnu_getopt(sys.argv[1:],"5f:o:h?P:W:F:s")
except getopt.GetoptError:
    help()

if len(args) == 0:
    args.append("-")
elif len(args) != 1:
    help()

rformat = "bbcode"
inputf = args[0]
output = "-"
titl = args[0] #default title is input filename
flags = []
oflags = []
omode = None
nostart = 0

for (opt, val) in opts:
    if opt in ("-h", "-?"):
        help()
    elif opt == "-f":
        rformat = val
    elif opt == "-P":
        flags.extend(val.split(","))
    elif opt == "-W":
        oflags.extend(val.split(","))
    elif opt == "-F":
        omode = val
    elif opt == "-o":
        output = val
    elif opt == "-t":
        titl = val
    elif opt == "-5":
        oflags.append("html5")
    elif opt == "-s":
        nostart = 1
    else:
        help()

if not nostart:
    sys.stderr.write("\nMDPlay by HarJIT (use -s (lowercase S) to suppress this message)\n")

if inputf != "-":
    f = open(inputf, "rU")
else:
    f = sys.stdin
try:
    renderer = mdplay.load_renderer(rformat)
    if not omode:
        ret = renderer(mdplay.parse_file(f, flags), titl, oflags)
    else:
        ret = renderer(mdplay.parse_file(f, flags), titl, oflags, mode=omode) #error if mode arg unsupported
except mdplay.NoSuchRendererError:
    help()
f.close()

if output == "-":
    fo = sys.stdout
else:
    fo = open(output, "w")
fo.write(ret)
