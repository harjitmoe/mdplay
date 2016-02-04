import block
from LinestackIter import LinestackIter

def parse_string(s,flags=()):
    block.reinit()
    return block.parse_block(s,block.TitleLevels(),flags)
def parse_file(f,flags=()):
    return block._parse_block(LinestackIter(f),block.TitleLevels(),flags)

class NoSuchDecoderError(ValueError):pass
writers={"bbcode":"out_bb","html":"out_html_dom","htmlalt":"out_html_nondom"}
def _load_renderer(modname):
    renderer_module=getattr(__import__("mdplay."+modname),modname)
    return getattr(renderer_module,renderer_module.__mdplay_renderer__)
def load_renderer(codename):
    if codename in writers:
        return _load_renderer(writers[codename])
    else:
        raise NoSuchDecoderError(codename)
