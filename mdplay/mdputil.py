__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

unichr4all = chr

# Give more deterministic IDs to expandable spoiler nodes in HTML/MWiki.
_curid = 1
_idded = {}
def newid(node):
    """Assign an unique ID to an object, or return the existing one if already assigned."""
    global _curid
    if id(node) not in _idded:
        _idded[id(node)] = _curid
        _curid += 1
    return _idded[id(node)]

def flatten_flags_parser(flags):
    """Given a list of parser flags (atomic or group), expand to a list of atomic parser flags."""
    out=[]
    for flag in flags:
        if flag == "strict":
            out.extend(flatten_flags_parser(["norest", "nospoilertag", "nowikitext",
                                  "noredditstyle", "nopandocstyle", "nospecialhrefs",
                                  "nodiacritic", "noemoticon", "noembedspoiler",
                                  "nocjk", "norubi", "nocomment", "nodirective"]))
        elif flag == "norest":
            out.extend(flatten_flags_parser(["noresthead", "nodicode", "noresttable"]))
        elif flag == "nowikitext":
            out.extend(flatten_flags_parser(["nowikihead", "nowikiemph", "nowikilinks"]))
        elif flag == "noredditstyle":
            out.extend(flatten_flags_parser(["noredditstylesuper", "noredditspoiler"]))
        elif flag == "noredditspoiler":
            out.extend(flatten_flags_parser(["noredditcssspoiler", "noredditrealspoiler"]))
        elif flag == "nospoilertag":
            out.extend(flatten_flags_parser(["noblockspoiler", "noredditspoiler"]))
        elif flag == "nosetexthead":
            out.extend(flatten_flags_parser(["noplainsetexthead", "noresthead"]))
        elif flag == "notable":
            out.extend(flatten_flags_parser(["noresttable", "nomdtable"]))
        elif flag == "nosupersubscript":
            out.extend(flatten_flags_parser(["noredditstylesuper", "nopandocstyle"]))
        elif flag == "noemoticon":
            out.extend(flatten_flags_parser(["noasciiemoticon", "noshortcodeemoji"]))
        elif flag == "nocjk":
            out.extend(flatten_flags_parser(["noromkan", "nocangjie"]))
        else:
            out.append(flag)
    return list(set(out))

