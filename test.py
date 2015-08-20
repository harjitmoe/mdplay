import sys
import block
import out_bb

#if len(sys.argv)!=2:
#    print ("Usage: %s <input file>"%sys.argv[0])
#    sys.exit(1)

f=open(sys.argv[1] if sys.argv[1:] else "test.md","r")
print (out_bb.bb_out(block.parse_file(f)))
