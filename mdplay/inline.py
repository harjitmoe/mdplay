# -*- mode: python; coding: utf-8 -*-

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import nodes, diacritic, uriregex, cjk, emoji, harbnf
from mdplay import htmlentitydefs_latest as htmlentitydefs
import os, re, string

#punct = string.punctuation + string.whitespace

def _parse_inline(content):
    out = []
    for c in content:
        if not isinstance(c, tuple):
            out.append(c)
            continue
        tag, inner, offset = c
        ### BibTeX diacritics ###
        if tag == "bibuml":
            assert len(inner) == 1
            c2 = inner[0][2:-1]
            braced = False
            if ("{" in c2) and c2.endswith("}"):
                braced = True
                c2, c3 = c2[:-1].split("{", 1)
            else:
                c2, c3 = c2[:1], c2[1:]
            try:
                r = diacritic.diacritic(c2, c3)
            except ValueError:
                try:
                    if not braced:
                        r = diacritic.diacritic(c2 + c3, '')
                    else:
                        raise ValueError #yeah yeah I know
                except ValueError:
                    out.append(inner[0])
                else:
                    out.append(r)
            else:
                out.append(r)
        ### Code spans ###
        elif tag == "codespan":
            assert len(inner) == 1
            backticks = len(inner[0]) - len(inner[0].lstrip("`"))
            out.append(nodes.CodeSpanNode(inner[0][backticks:-backticks]))
        ### Escaping ###
        elif tag == "escape":
            assert len(inner) == 1 and len(inner[0]) == 2
            c2 = inner[0][1]
            if c2 not in " \n":
                out.append(c2)
        elif tag == "entity":
            assert len(inner) == 1
            c2 = inner[0][1:]
            if c2[0] == "#":
                if c2[1] == "x":
                    out.append(chr(int(c2[2:].rstrip(";"), 16)))
                else:
                    out.append(chr(int(c2[1:].rstrip(";"), 10)))
            else:
                trail = ""
                while c2 and (c2 not in htmlentitydefs.html5):
                    trail = c2[-1] + trail
                    c2 = c2[:-1]
                if c2:
                    out.append(htmlentitydefs.html5[c2])
                else:
                    out.append("&")
                if trail:
                    out.append(trail)
        ### Newlines ###
        elif tag == "newline":
            out.append(nodes.NewlineNode())
        ### Emphases ###
        #### /With asterisks
        elif tag == "boldemphatic":
            out.append(nodes.BoldNode(_parse_inline(inner), emphatic=True))
        elif tag == "italicemphatic":
            out.append(nodes.ItalicNode(_parse_inline(inner), emphatic=True))
        #### /With underscores or apostrophes
        elif tag == "boldnonemphatic":
            out.append(nodes.BoldNode(_parse_inline(inner), emphatic=False))
        elif tag == "underline":
            out.append(nodes.UnderlineNode(_parse_inline(inner), emphatic=False))
        elif tag == "italicnonemphatic":
            out.append(nodes.ItalicNode(_parse_inline(inner), emphatic=False))
        #### /Others
        elif tag == "strikethru":
            # emphatic=True would be <del>, emphatic=False would be <s>
            out.append(nodes.StrikeNode(_parse_inline(inner), emphatic=True))
        ### New Reddit spoilers ###
        elif tag == "inlinespoiler":
            out.append(nodes.InlineSpoilerNode(_parse_inline(inner)))
        ### HREFs (links and embeds, plus CJK extensions) ###
        elif tag == "plainhref":
            assert len(inner) == 2
            assert inner[0][0] == "content"
            assert inner[1][0] == "uri"
            assert len(inner[1][1]) == 1
            if inner[1][1][0].strip().split(None, 1)[0] in ("/spoiler", "/s", "#spoiler", "#s"):
                if " " not in inner[1][1][0].strip():
                    out.append(nodes.InlineSpoilerNode(_parse_inline(inner[0][1])))
                else:
                    out.append(nodes.InlineSpoilerNode([inner[1][1][0].strip().split(None, 1)[1]], 
                        _parse_inline(inner[0][1])))
            else:
                out.append(nodes.HrefNode(inner[1][1][0], _parse_inline(inner[0][1]), "url"))
        elif tag == "embedhref":
            assert len(inner) == 3
            assert inner[0][0] == "content"
            assert inner[1][0] == "uri"
            assert len(inner[1][1]) == 1
            assert inner[2][0] == "dimensions"
            assert len(inner[2][1]) == 1
            if inner[2][1][0].lstrip():
                width, height = [int(i) if i else None 
                        for i in inner[2][1][0].lstrip().lstrip("=").split("x", 1)]
            else:
                width = height = None
            out.append(nodes.HrefNode(inner[1][1][0], _parse_inline(inner[0][1]), "img", 
                    width=width, height=height))
        elif tag == "specialhref":
            assert len(inner) == 3
            assert inner[0][0] == "tagname"
            assert len(inner[0][1]) == 1
            assert inner[1][0] == "content"
            assert inner[2][0] == "whateveruri"
            assert len(inner[2][1]) == 1
            if inner[0][1][0].lower() == "deseret":
                out.append(nodes.DeseretNode(inner[2][1][0]))
            elif cjkv := cjk.cjk_handler(inner[0][1][0], inner[2][1][0], _parse_inline(inner[1][1])):
                out.append(cjkv)
            else:
                out.append(nodes.HrefNode(inner[2][1][0], _parse_inline(inner[1][1]), 
                    inner[0][1][0]))
        elif tag == "redditref":
            assert len(inner) == 1
            out.append(nodes.HrefNode("https://reddit.com" + inner[0], [inner[0]], "url"))
        ### Superscripts and Subscripts ###
        elif tag == "superscript":
            out.append(nodes.SuperNode(_parse_inline(inner)))
        elif tag == "subscript":
            out.append(nodes.SubscrNode(_parse_inline(inner)))
        ### HZ escapes / codes / whatever (todo dedupe this repeated code) ###
        elif tag == "hz":
            assert len(inner) == 1
            code = inner[0]
            assert not (len(code) % 2)
            codec = "gb18030"
            if code.startswith("~jis"):
                codec = "euc-jp"
                code = code[4:]
            code = code[2:-2]
            buf = list(code)
            obuf = []
            while buf:
                mine = buf.pop(0)
                if buf and (0x21 <= ord(mine) <= 0x7E):
                    mine = bytes([ord(mine) | 0x80, ord(buf.pop(0)) | 0x80]).decode(codec)
                obuf.append(mine)
            out.extend(obuf)
        ### Emoticons and shortcodes ###
        elif emote := emoji.emote_handler(tag, inner):
            out.append(emote)
        ### Other ###
        elif tag == "#ERROR":
            out.append(inner[0])
        else:
            raise ValueError(f"unrecognised tag: {tag!r}")
    return out


def parse_inline(content, flags, state):
    rules, attributes = harbnf.parse(harbnf.read_prog(open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "inline.harbnf"), 
    "r"), flags))
    tree = harbnf.strip_and_fold(harbnf.execute(rules, content, attributes, soft=True), attributes)
    return _parse_inline(tree)


