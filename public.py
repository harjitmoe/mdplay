import block
from LinestackIter import LinestackIter

def parse_string(s):
    block.reinit()
    return block.parse_block(s)
def parse_file(f):
    block.reinit()
    return block._parse_block(LinestackIter(f))