# -*- mode: python; coding: utf-8 -*-
"""
Derived from part of "Python documentation conversion utils".
Original filename util.py

HarJIT added many, many more accented (et cetara) characters, 
including adding circumflexes and macrons full stop, 
and integrated with mdplay3.
Also added Unicode combining-diacritic support.
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
from unicodedata import normalize

#from docutils.nodes import make_id
#from .docnodes import TextNode, EmptyNode, NodeList

def _umlaut(cmd, c):
    try:
        if cmd == '"': #Umlauts and diaereses.
            if c.lower() in "aiueo":
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
            else:
                return c.decode("utf-8")+u"\u0308"
        elif cmd == 'r': #Rings.
            if c.lower() in "au":
                return {'a': u'å',
                        'u': u'ů',
                        'A': u'Å',
                        'U': u'Ů'}[c]
            else:
                return c.decode("utf-8")+u"\u030b"
        elif cmd == 'H': #Double acutes.
            if c.lower() in "ou":
                return {'o': u'ő',
                        'u': u'ű',
                        'O': u'Ő',
                        'U': u'Ű'}[c]
            else:
                return c.decode("utf-8")+u"\u030a"
        elif cmd == "^": #Circumflexes.
            if c.lower() in "aiueo":
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
            else:
                return c.decode("utf-8")+u"\u0302"
        elif cmd == "'": #Acutes.
            if c.lower() in "aiueosznyr":
                return {'a': u'á',
                        'i': u'í',
                        'u': u'ú',
                        'e': u'é',
                        'o': u'ó',
                        's': u'ś',
                        'z': u'ź',
                        'n': u'ń',
                        'y': u'ý',
                        'r': u'ŕ',
                        'A': u'Á',
                        'I': u'Í',
                        'U': u'Ú',
                        'E': u'É',
                        'O': u'Ó',
                        'S': u'Ś',
                        'Z': u'Ź',
                        'N': u'Ń',
                        'Y': U'Ý',
                        'R': u'Ŕ'}[c]
            else:
                return c.decode("utf-8")+u"\u0301"
        elif cmd == "=": #Macrons.
            if c.lower() in "aiueo":
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
            else:
                return c.decode("utf-8")+u"\u0304"
        elif cmd == '~': #Tildes.
            if c.lower() in "on":
                return {'o': u'õ',
                        'n': u'ñ',
                        'O': u'Õ',
                        'N': u'Ñ'}[c]
            else:
                return c.decode("utf-8")+u"\u0303"
        elif cmd in 'ck': #Vowel ogoneks and consonant cedillas.
            if c.lower() in "aecst":
                return {'a': u'ą',
                        'e': u'ę',
                        'c': u'ç',
                        's': u'ş',
                        't': u'ţ',
                        'A': u'Ą',
                        'E': u'Ę',
                        'C': u'Ç',
                        'S': u'Ş',
                        'T': u'Ţ'}[c]
            else:
                return c.decode("utf-8")+u"\u0326"
        elif cmd == '`': #Graves.
            if c.lower() in "aiueo":
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
            else:
                return c.decode("utf-8")+u"\u0300"
        elif cmd == 'v': #Carons.
            if c.lower() in "aiueocsztdnrl":
                return {'a': u'ǎ',
                        'i': u'ǐ',
                        'u': u'ǔ',
                        'e': u'ě',
                        'o': u'ǒ',
                        'c': u'č',
                        's': u'š',
                        'z': u'ž',
                        't': u'ť',
                        'd': u'ď',
                        'n': u'ň',
                        'r': u'ř',
                        'l': u'ľ',
                        'A': u'Ǎ',
                        'I': u'Ǐ',
                        'U': u'Ǔ',
                        'E': u'Ě',
                        'O': u'Ǒ',
                        'C': u'Č',
                        'S': u'Š',
                        'Z': u'Ž',
                        'T': u'Ť',
                        'D': u'Ď',
                        'N': u'Ň',
                        'R': u'Ř',
                        'L': u'Ľ'}[c]
            else:
                return c.decode("utf-8")+u"\u030c"
        elif cmd == 'u': #Breves
            if c.lower() in "ao":
                return {'a': u'ă',
                        'ŏ': u'ŏ',
                        'A': u'Ă',
                        'Ŏ': u'Ŏ'}[c]
            else:
                return c.decode("utf-8")+u"\u0306"
        elif cmd == 'B': #Slashes
            return {'o': u'ø',
                    'd': u'đ', #XXX get ð in somewhere
                    'l': u'ł',
                    'O': u'Ø',
                    'D': u'Đ',
                    'L': u'Ł'}[c]
        elif cmd == 'th': #Thorn
            return {'': u'þ'}[c]
        elif cmd == 'TH': #Thorn
            return {'': u'Þ'}[c]
        elif cmd == 'ss': #Sharp s
            return {'': u'ß'}[c]
        elif cmd == 'oe':
            return {'': u'œ'}[c]
        elif cmd == 'OE':
            return {'': u'Œ'}[c]
        elif cmd == 'ae':
            return {'': u'æ'}[c]
        elif cmd == 'AE':
            return {'': u'Æ'}[c]
        #
        elif cmd == 'aa': #Ringed a
            return {'': u'å'}[c]
        elif cmd == 'AA': #Ringed a
            return {'': u'Å'}[c]
        elif cmd == 'l': #Slashed l
            return {'': u'ł'}[c]
        elif cmd == 'L': #Slashed l
            return {'': u'Ł'}[c]
        elif cmd == 'o': #Slashed o
            return {'': u'ø'}[c]
        elif cmd == 'O': #Slashed o
            return {'': u'Ø'}[c]
        else:
            #from .latexparser import ParserError
            raise ValueError('invalid umlaut \\%s' % cmd)#, 0)
    except KeyError:
        #from .latexparser import ParserError
        raise ValueError('unsupported umlaut \\%s{%s}' % (cmd, c))#, 0)
umlaut = lambda cmd, c: normalize("NFC", _umlaut(cmd, c))

## The following has nothing to do with mdplay. -- HarJIT
#
#def fixup_text(text):
#    return text.replace('``', '"').replace("''", '"').replace('`', "'").\
#           replace('|', '\\|').replace('*', '\\*')
#
#def empty(node):
#    return (type(node) is EmptyNode)
#
#def text(node):
#    """ Return the text for a TextNode or raise an error. """
#    if isinstance(node, TextNode):
#        return node.text
#    elif isinstance(node, NodeList):
#        restext = ''
#        for subnode in node:
#            restext += text(subnode)
#        return restext
#    from .restwriter import WriterError
#    raise WriterError('text() failed for %r' % node)
#
#markup_re = re.compile(r'(:[a-zA-Z0-9_-]+:)?`(.*?)`')
#
#def my_make_id(name):
#    """ Like make_id(), but strip roles first. """
#    return make_id(markup_re.sub(r'\2', name))
#
#alphanum = u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#wordchars_s = alphanum + u'_.-'
#wordchars_e = alphanum + u'+`(-'
#bad_markup_re = re.compile(r'(:[a-zA-Z0-9_-]+:)?(`{1,2})[ ]*(.+?)[ ]*(\2)')
#quoted_code_re = re.compile(r'\\`(``.+?``)\'')
#paren_re = re.compile(r':(func|meth|cfunc):`(.*?)\(\)`')
#
#def repair_bad_inline_markup(text):
#    # remove quoting from `\code{x}'
#    xtext = quoted_code_re.sub(r'\1', text)
#
#    # special: the literal backslash
#    xtext = xtext.replace('``\\``', '\x03')
#    # special: literal backquotes
#    xtext = xtext.replace('``````', '\x02')
#
#    # remove () from function markup
#    xtext = paren_re.sub(r':\1:`\2`', xtext)
#
#    ntext = []
#    lasti = 0
#    l = len(xtext)
#    for m in bad_markup_re.finditer(xtext):
#        ntext.append(xtext[lasti:m.start()])
#        s, e = m.start(), m.end()
#        if s != 0 and xtext[s-1:s] in wordchars_s:
#            ntext.append('\\ ')
#        ntext.append((m.group(1) or '') + m.group(2) + m.group(3) + m.group(4))
#        if e != l and xtext[e:e+1] in wordchars_e:
#            ntext.append('\\ ')
#        lasti = m.end()
#    ntext.append(xtext[lasti:])
#    return ''.join(ntext).replace('\x02', '``````').replace('\x03', '``\\``')
