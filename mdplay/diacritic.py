__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import unicodedata

DIACRITICS = {
    "`": u"\u0300", # Grave
    "'": u"\u0301", # Acute
    "^": u"\u0302", # Circumflex
    "~": u"\u0303", # Tilde
    "=": u"\u0304", # Macron
    # 305: overline
    "u": u"\u0306", # Breve or micron
    # 307: dot above
    '"': u"\u0308", # Trema or umlaut
    # 309: comma above
    "r": u"\u030a", # Ring
    "H": u"\u030b", # Double actue
    "v": u"\u030c", # Caron or h{\'a}{\vc}ek
    # 30d: vertical dash above
    # 30e: two vertical dashes above
    # 30f: double grave
    "c": u"\u0327", # Cedilla
    "k": u"\u0328", # Ogonek
    "B": u"\u0338", # Slash (see also SLASHES below)
}

SHORTHANDS = {
    "aa": ("r", "a"),
    "AA": ("r", "A"),
    "l": ("B", "l"),
    "L": ("B", "L"),
    "o": ("B", "o"),
    "O": ("B", "O"),
}

DIGRAPHS = {
    "OE": u"\u0152", # Microsoft 0x8c
    "oe": u"\u0153", # Microsoft 0x9c
    "AE": u"\u00c6",
    "DH": u"\u00d0",
    "TH": u"\u00de",
    "ss": u"\u00df",
    "ae": u"\u00e6",
    "dh": u"\u00f0",
    "th": u"\u00fe",
}

SLASHES = {
    # While this dict was derived from code previously in umlaut.py, it was my
    # own code added in mdplay version 3.9 rather than from the original.
    'o': u'\u00f8',
    'O': u'\u00d8',
    'D': u'\u0110',
    'd': u'\u0111',
    'L': u'\u0141',
    'l': u'\u0142'
}

def diacritic(command, arg):
    if (command == 'B') and (arg in SLASHES):
        return SLASHES[arg]
    if (command in SHORTHANDS) and (not arg):
        return diacritic(*SHORTHANDS[command])
    elif (command in DIGRAPHS) and (not arg):
        return DIGRAPHS[command]
    elif command in DIACRITICS:
        return unicodedata.normalize(
            "NFC",
            arg.decode("utf-8") + DIACRITICS[command]
        ).encode("utf-8")
    else:
        raise ValueError("unsupported diacritic: " + command + " with " + arg)

