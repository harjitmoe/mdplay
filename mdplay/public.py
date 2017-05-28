import block,nodes
from mdplay.LinestackIter import LinestackIter

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

def parse_string(s,flags=()):
    return block.parse_block(s,block.TitleLevels(),flags)
def parse_file(f,flags=()):
    return block._parse_block(LinestackIter(f),block.TitleLevels(),nodes.flatten_flags_parser(flags))

class MdplayError(ValueError):pass
class NoSuchRendererError(MdplayError):pass
class NoSnippetRendererError(MdplayError):pass

writers={"debug":"out_repr","bbcode":"out_bb","html":"out_html_dom","htmlalt":"out_html_nondom","mwiki":"out_mwiki", "md":"out_markdown","tvwiki":"out_tvwiki","enamel":"out_enamel"}

def _load_renderer(modname):
    renderer_module=getattr(__import__("mdplay."+modname),modname)
    return getattr(renderer_module,renderer_module.__mdplay_renderer__)
def load_renderer(codename):
    if codename in writers:
        return _load_renderer(writers[codename])
    else:
        raise NoSuchRendererError(codename)

def _load_snippet_renderer(modname):
    renderer_module=getattr(__import__("mdplay."+modname),modname)
    if renderer_module.__mdplay_snippet_renderer__==None:
        raise NoSnippetRendererError(codename)
    return getattr(renderer_module,renderer_module.__mdplay_snippet_renderer__)
def load_snippet_renderer(codename):
    if codename in writers:
        return _load_snippet_renderer(writers[codename])
    else:
        raise NoSuchRendererError(codename)
