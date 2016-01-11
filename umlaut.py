# -*- coding: utf-8 -*-
"""
From the Python documentation conversion utils.
Original filename util.py

HarJIT added more accented characters, including adding circumflexes
and macrons full stop, and integrated with mdplay3.
 -- May be distributed under same terms as original.

Copyright (c) 2007-2008 by Georg Brandl.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import re, sys

#from docutils.nodes import make_id

#from .docnodes import TextNode, EmptyNode, NodeList


def umlaut(cmd, c):
    try:
        if cmd == '"':
            return {'a': u'ä',
                    'i': u'ï',
                    'u': u'ü',
                    'e': u'ë',
                    'o': u'ö',
                    'A': u'Ä',
                    'I': u'Ï',
                    'U': u'Ü',
                    'E': u'Ë',
                    'O': u'Ö'}[c]
        elif cmd == "^":
            return {'a': u'â',
                    'i': u'î',
                    'u': u'û',
                    'e': u'ê',
                    'o': u'ô',
                    'A': u'Â',
                    'I': u'Î',
                    'U': u'Û',
                    'E': u'Ê',
                    'O': u'Ô'}[c]
        elif cmd == "'":
            return {'a': u'á',
                    'i': u'í',
                    'u': u'ú',
                    'e': u'é',
                    'o': u'ó',
                    'A': u'Á',
                    'I': u'Í',
                    'U': u'Ú',
                    'E': u'É',
                    'O': u'Ó'}[c]
        elif cmd == "=":
            return {'a': u'ā',
                    'i': u'ī',
                    'u': u'ū',
                    'e': u'ē',
                    'o': u'ō',
                    'A': u'Ā',
                    'I': u'Ī',
                    'U': u'Ū',
                    'E': u'Ē',
                    'O': u'Ō'}[c]
        elif cmd == '~':
            return {'o': u'õ',
                    'n': u'ñ',
                    'O': u'Õ',
                    'N': u'Ñ'}[c]
        elif cmd == 'c':
            return {'c': u'ç',
                    'C': u'Ç'}[c]
        elif cmd == '`':
            return {'a': u'à',
                    'i': u'ì',
                    'u': u'ù',
                    'e': u'è',
                    'o': u'ò',
                    'A': u'À',
                    'I': u'Ì',
                    'U': u'Ù',
                    'E': u'È',
                    'O': u'Ò'}[c]
        elif cmd == 'v':
            return {'a': u'ǎ',
                    'i': u'ǐ',
                    'u': u'ǔ',
                    'e': u'ě',
                    'o': u'ǒ',
                    'A': u'Ǎ',
                    'I': u'Ǐ',
                    'U': u'Ǔ',
                    'E': u'Ě',
                    'O': u'Ǒ'}[c]
        else:
            #from .latexparser import ParserError
            raise ValueError('invalid umlaut \\%s' % cmd)#, 0)
    except KeyError:
        #from .latexparser import ParserError
        raise ValueError('unsupported umlaut \\%s%s' % (cmd, c))#, 0)

def fixup_text(text):
    return text.replace('``', '"').replace("''", '"').replace('`', "'").\
           replace('|', '\\|').replace('*', '\\*')

def empty(node):
    return (type(node) is EmptyNode)

def text(node):
    """ Return the text for a TextNode or raise an error. """
    if isinstance(node, TextNode):
        return node.text
    elif isinstance(node, NodeList):
        restext = ''
        for subnode in node:
            restext += text(subnode)
        return restext
    from .restwriter import WriterError
    raise WriterError('text() failed for %r' % node)

markup_re = re.compile(r'(:[a-zA-Z0-9_-]+:)?`(.*?)`')

def my_make_id(name):
    """ Like make_id(), but strip roles first. """
    return make_id(markup_re.sub(r'\2', name))

alphanum = u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
wordchars_s = alphanum + u'_.-'
wordchars_e = alphanum + u'+`(-'
bad_markup_re = re.compile(r'(:[a-zA-Z0-9_-]+:)?(`{1,2})[ ]*(.+?)[ ]*(\2)')
quoted_code_re = re.compile(r'\\`(``.+?``)\'')
paren_re = re.compile(r':(func|meth|cfunc):`(.*?)\(\)`')

def repair_bad_inline_markup(text):
    # remove quoting from `\code{x}'
    xtext = quoted_code_re.sub(r'\1', text)

    # special: the literal backslash
    xtext = xtext.replace('``\\``', '\x03')
    # special: literal backquotes
    xtext = xtext.replace('``````', '\x02')

    # remove () from function markup
    xtext = paren_re.sub(r':\1:`\2`', xtext)

    ntext = []
    lasti = 0
    l = len(xtext)
    for m in bad_markup_re.finditer(xtext):
        ntext.append(xtext[lasti:m.start()])
        s, e = m.start(), m.end()
        if s != 0 and xtext[s-1:s] in wordchars_s:
            ntext.append('\\ ')
        ntext.append((m.group(1) or '') + m.group(2) + m.group(3) + m.group(4))
        if e != l and xtext[e:e+1] in wordchars_e:
            ntext.append('\\ ')
        lasti = m.end()
    ntext.append(xtext[lasti:])
    return ''.join(ntext).replace('\x02', '``````').replace('\x03', '``\\``')
