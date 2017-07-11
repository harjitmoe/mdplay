#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
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
    return r
