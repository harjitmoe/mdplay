#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

__copying__ = """
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided this notice is
preserved.  This file is offered as-is, without any warranty.
"""

import unicodedata

h2f = {" ": "\u3000"}

# Exclude white (double or bubble) parens as they don't have true halfwidth equivalents.
for i in list(range(0xff01, 0xff5f)) + list(range(0xffe0, 0xffe7)):
    h2f[unicodedata.normalize("NFKC", chr(i))] = chr(i)

def to_fullwidth(a):
    r = ""
    for c in a:
        if c in h2f:
            r += h2f[c] # This would not be nearly as clean on Python 2
        else:
            r += c
    # Control where line breaks occur, like in halfwidth ASCII:
    return ("\u2060".join(r).replace("\u2060\u3000\u2060", "\u2060\u3000")
            ).replace("\u2060\uff0d\u2060", "\u2060\uff0d")
