#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# By HarJIT in 2021.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re, os

tokens = [
    ("identifier", re.compile(r"\b\w+\b"), lambda m: m.group(0)),
    ("attribute", re.compile(r"\$(STRIP|FOLD|EXPLODE|NONEST)\b"), lambda m: m.group(1)),
    ("regexpr", re.compile(r"/((?:[^\\/]|\\.)+)/(\w*)"), lambda m: (m.group(1), m.group(2))),
    ("sqstring", re.compile(r"(#?)(@?)'((?:[^\\']|\\.)*)'"), lambda m: (
        m.group(3), bool(m.group(1)), bool(m.group(2)))),
    ("dqstring", re.compile(r'(#?)(@?)"((?:[^\\"]|\\.)*)"'), lambda m: (
        m.group(3), bool(m.group(1)), bool(m.group(2)))),
    ("spacer", re.compile(r"\s+"), lambda m: None),
    ("alternator", re.compile(r"\|"), lambda m: None),
    ("allocator", re.compile(r"<-"), lambda m: None),
    ("attributor", re.compile(r"::"), lambda m: None),
    ("delimiter", re.compile(r";"), lambda m: None),
    ("bottom", re.compile(r"&"), lambda m: None),
    ("comment", re.compile(r"(?m)^\.\.\s.*\n"), lambda m: None),
]

class ParsingOfBnfError(Exception): pass
class ParsingWithBnfError(Exception): pass

def tokenise(instr):
    pos = 0
    while pos < len(instr):
        for (tokname, rgx, procfunc) in tokens:
            m = rgx.match(instr, pos=pos)
            if m:
                yield (tokname, procfunc(m), pos)
                pos = m.end()
                break
        else:
            context = instr[pos-10:pos+10]
            raise ParsingOfBnfError(f"unrecognised syntax at position {pos:d}; context {context!r}")
    yield ("EOF", (lambda: None), pos)

def unescape(data):
    # Yes, really, this is how you unescape stuff in a string (intermediately escaping non-ASCII)
    return data.encode("us-ascii", errors="backslashreplace").decode("unicode_escape")

def parse(instr):
    rules = {}
    attributes = {"STRIP": frozenset(), "FOLD": frozenset(), "EXPLODE": frozenset(), "NONEST": frozenset()}
    currule = []
    curalt = []
    curname = None
    mode = "initial"
    for tokname, data, pos in tokenise(instr):
        if tokname in ("spacer", "comment"):
            continue
        elif mode == "initial":
            if tokname == "identifier":
                curname = data
                mode = "want_allocator"
            elif tokname == "attribute":
                curname = data
                mode = "want_attributor"
            elif tokname == "EOF":
                break
            else:
                context = instr[pos-10:pos+10]
                raise ParsingOfBnfError(f"expecting left identifier at position {pos:d}, got {tokname}; context {context!r}")
        elif mode == "want_allocator":
            if tokname == "allocator":
                mode = "in_rule"
            else:
                context = instr[pos-10:pos+10]
                raise ParsingOfBnfError(f"expecting <- at position {pos:d}, got {tokname}; context {context!r}")
        elif mode == "want_attributor":
            if tokname == "attributor":
                mode = "in_attribute"
            else:
                context = instr[pos-10:pos+10]
                raise ParsingOfBnfError(f"expecting :: at position {pos:d}, got {tokname}; context {context!r}")
        elif mode == "in_attribute":
            if tokname == "delimiter":
                attributes[curname] |= frozenset(currule)
                del currule[:]
                mode = "initial"
            elif tokname == "identifier":
                currule.append(data)
            else:
                context = instr[pos-10:pos+10]
                raise ParsingOfBnfError(f"unexpected {tokname} in attribute at position {pos:d}; context {context!r}")
        elif mode == "in_rule":
            if tokname == "delimiter":
                currule.append(tuple(curalt))
                del curalt[:]
                if curname in rules:
                    raise ParsingOfBnfError(f"redefinition of {curname} at position {pos:d}")
                rules[curname] = tuple(currule)
                del currule[:]
                mode = "initial"
            elif tokname == "alternator":
                currule.append(tuple(curalt))
                del curalt[:]
            elif tokname == "identifier":
                curalt.append(("rule", data))
            elif tokname == "bottom":
                curalt.append(("bottom", None))
            elif tokname in ("sqstring", "dqstring"):
                raw, is_strip, is_raw = data
                if is_raw:
                    curalt.append(("string" if not is_strip else "stripstring", raw))
                else:
                    curalt.append(("string" if not is_strip else "stripstring", unescape(raw)))
            elif tokname == "regexpr":
                regexpr, attribs = data
                # We know that \/ is always an escape, because any / that isn't part of an
                #   escape will have been interpreted as a terminator and not included.
                regexpr = regexpr.replace("\\/", "/")
                if attribs:
                    curalt.append(("regexpr", re.compile("(?" + attribs + ")" + regexpr)))
                else:
                    curalt.append(("regexpr", re.compile(regexpr)))
            else:
                context = instr[pos-10:pos+10]
                raise ParsingOfBnfError(f"unexpected {tokname} at position {pos:d}; context {context!r}")
    return rules, attributes

def _run_alt(curalt, rulestack, rules, upon, attributes, pos, out):
    if not curalt:
        yield (tuple(out), pos)
        return
    elmname, element = curalt[0]
    if elmname == "regexpr":
        if m := element.match(upon, pos=pos):
            yield from _run_alt(curalt[1:], rulestack, rules, upon, attributes, m.end(), out + (m.group(0),))
    elif elmname == "string":
        if upon[pos : pos + len(element)] == element:
            yield from _run_alt(curalt[1:], rulestack, rules, upon, attributes, pos + len(element), out + (element,))
    elif elmname == "stripstring":
        if upon[pos : pos + len(element)] == element:
            yield from _run_alt(curalt[1:], rulestack, rules, upon, attributes, pos + len(element), out)
    elif elmname == "rule":
        if element in attributes["NONEST"] and element in rulestack:
            return
        for rule, moreout, newpos in _execute(rules, upon, attributes, pos, rulestack + (element,)):
            yield from _run_alt(curalt[1:], rulestack, rules, upon, attributes, newpos, out + ((rule, moreout, newpos),))
    elif elmname == "bottom":
        return
    else:
        raise ValueError(f"unrecognised element type {elmname!r}")

def _execute(rules, upon, attributes, pos, rulestack):
    if rulestack[-1] not in rules:
        raise ValueError(f"no rule named {rulestack[-1]!r}")
    currule = rules[rulestack[-1]]
    if len(currule) == 2:
        smol, big = sorted(currule, key=len)
        foldable = rulestack[-1] in (attributes["FOLD"] | attributes["EXPLODE"])
        if big[:len(smol)] == smol and big[-1] == ("rule", rulestack[-1]) and foldable:
            # Tail recursive rule
            xtra = big[len(smol):-1]
            queue = [((), pos)]
            while queue:
                out1, pos1 = queue.pop(0)
                for out2, pos2 in _run_alt(smol, rulestack, rules, upon, attributes, pos1, out1):
                    yield (rulestack[-1], out2, pos2)
                    queue.extend(_run_alt(xtra, rulestack, rules, upon, attributes, pos2, out2))
            return
    for curalt in currule:
        for i in _run_alt(curalt, rulestack, rules, upon, attributes, pos, ()):
            yield (rulestack[-1],) + i

def execute(rules, upon, attributes, soft=False, rule="top", initend=0):
    possibilities = list(_execute(rules, upon, attributes, initend, (rule,)))
    possibilities.sort(key=lambda i: -i[2])
    max_possibilities = [i for i in possibilities if i[2] == possibilities[0][2]]
    if len(max_possibilities) > 1:
        print(f"WARNING: {len(max_possibilities)} equally valid parses for {upon!r}")
    _rule, out, end = possibilities[0]
    assert _rule == rule
    if end == len(upon):
        return ((rule, out, end),)
    elif soft:
        start = [(rule, out, end), ("#ERROR", upon[end], end + 1)]
        start.extend(execute(rules, upon, attributes, soft, rule, end + 1))
        return tuple(start)
    else:
        raise ParsingWithBnfError(f"data after position {end} is not valid")

def _strip_and_fold(executor_outlist, attributes, container):
    accumulator = []
    for item in executor_outlist:
        if not isinstance(item, tuple):
            accumulator.append(item)
        else:
            rule, out, end = item
            if rule in attributes["STRIP"]:
                continue
            nest = _strip_and_fold(out, attributes, rule)
            if rule in attributes["EXPLODE"] or (rule in attributes["FOLD"] and container == rule):
                for i in nest:
                    if not isinstance(i, tuple):
                        accumulator.append(i)
                    else:
                        if accumulator:
                            yield "".join(accumulator)
                            del accumulator[:]
                        yield i
            else:
                if accumulator:
                    yield "".join(accumulator)
                    del accumulator[:]
                yield rule, tuple(nest), end
    if accumulator:
        yield "".join(accumulator)
        del accumulator[:]

def strip_and_fold(executor_output, attributes):
    return tuple(_strip_and_fold(executor_output, attributes, None))

def read_prog(file, flags=frozenset()):
    out = []
    condstack = []
    for line in file:
        in_business = True
        for instr, argument in condstack:
            if instr in ("ifdef", "else_of_ifndef"):
                if argument not in flags:
                    in_business = False
                    break
            elif instr in ("ifndef", "else_of_ifdef"):
                if argument in flags:
                    in_business = False
                    break
            else:
                raise AssertionError(f"invalid directive: {instr!r}")
        #
        if line.startswith("%:"):
            rr = line[2:].strip().split(None, 1)
            if len(rr) == 2:
                rule, rest = rr
            else:
                rule, = rr
                rest = ""
            rule = rule.casefold()
            if rule == "ifdef":
                condstack.append(("ifdef", rest))
            elif rule == "ifndef":
                condstack.append(("ifndef", rest))
            elif rule == "else":
                if rest:
                    raise ParsingOfBnfError("%:else does not take arguments")
                if not condstack:
                    raise ParsingOfBnfError("%:else outside a conditional")
                outerrule, outerarg = condstack.pop()
                if outerrule == "ifdef":
                    condstack.append(("else_of_ifdef", outerarg))
                elif outerrule == "ifndef":
                    condstack.append(("else_of_ifndef", outerarg))
                elif outerrule.startswith("else_"):
                    raise ParsingOfBnfError("multiple %:else within a single conditional")
                else:
                    raise AssertionError(f"invalid directive: {outerrule!r}")
            elif rule == "endif":
                if not condstack:
                    raise ParsingOfBnfError("%:endif outside a conditional")
                condstack.pop()
            else:
                raise ParsingOfBnfError(f"unrecognised directive: {rule!r}")
        elif in_business:
            out.append(line)
    return "".join(out)
        
tester = r"""

identifier <- /\b\w+\b/;
attribute <- /\$(STRIP|FOLD|EXPLODE|NONEST)\b/;
regexpr <- /\/((?:[^\\\/]|\\.)+)\/(\w*)/;
string <- /(#?)(@?)'((?:[^\\']|\\.)*)'/ | /(#?)(@?)"((?:[^\\"]|\\.)*)"/;

spacer <- /\s*/;
allocator <- "<-";
attributor <- "::";
delimiter <- ";";
alternator <- "|";
comment <- /^\.\.\s.*\n/m;
$STRIP :: spacer allocator attributor delimiter alternator;

bottom <- "&";

top <- statement spacer | statement top;
statement <- rule | attributeline | spacer comment;
attributeline <- spacer attribute spacer attributor spacer attributebody spacer delimiter;
attributebody <- identifier | identifier spacer attributebody;
rule <- spacer identifier spacer allocator spacer rulebody spacer delimiter;
rulebody <- rulealternation | rulealternation spacer alternator spacer rulebody;
rulealternation <- ruleelement | ruleelement spacer rulealternation;
ruleelement <- identifier | regexpr | string | bottom | &;
$STRIP :: comment;
$FOLD :: rulealternation;
$EXPLODE :: top statement attributebody ruleelement rulebody;

.. this is a comment

"""

if __name__ == "__main__":
    import pprint
    prog = read_prog(open("inline.harbnf", "r"))
    data = open("uuu.txt", "r").read()
    rules, attributes = parse(prog)
    pprint.pprint(strip_and_fold(execute(rules, data, attributes, soft=True), attributes))



