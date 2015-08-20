import block
from LinestackIter import LinestackIter

def parse_string(s):
    block.reinit()
    return block.parse_block(s,block.TitleLevels())
def parse_file(f):
    return block._parse_block(LinestackIter(f),block.TitleLevels())