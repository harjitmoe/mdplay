__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import block, nodes, mdputil, writers
from mdplay.LinestackIter import LinestackIter

def parse_string(s, flags=()):
    return block.parse_block(s,block.State(), flags)

def parse_file(f, flags=()):
    return block._parse_block(LinestackIter(f), block.State(), mdputil.flatten_flags_parser(flags))

class MdplayError(ValueError):
    pass

class NoSuchRendererError(MdplayError):
    pass

class NoSnippetRendererError(MdplayError):
    pass

writernames = ["debug", "bbcode", "html", "mwiki", "md", "tvwiki"]

def _load_renderer(modname):
    __import__("mdplay.writers." + modname)
    renderer_module = getattr(writers, modname)
    return getattr(renderer_module, renderer_module.__mdplay_renderer__)\

def load_renderer(codename):
    if codename in writernames:
        return _load_renderer(codename)
    else:
        raise NoSuchRendererError(codename)

def _load_snippet_renderer(modname):
    __import__("mdplay.writers." + modname)
    renderer_module = getattr(writers, modname)
    if renderer_module.__mdplay_snippet_renderer__ == None:
        raise NoSnippetRendererError(codename)
    return getattr(renderer_module, renderer_module.__mdplay_snippet_renderer__)

def load_snippet_renderer(codename):
    if codename in writernames:
        return _load_snippet_renderer(codename)
    else:
        raise NoSuchRendererError(codename)
