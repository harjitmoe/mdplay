#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import re, string, pprint, functools

# Rather than trying to select for whitespace outside literals,
#   split at the tokens themselves, keep the split strings
#   (effected by the outer parethetical) and discard the
#   whitespace parts.
token_splitter = re.compile(r"""("[^"]*"|'[^']*'|\S+)""")

def parse_bnf(input):
    rules = {}
    for line in input.split("\n"):
        if not line.strip():
            continue
        if line[0] == ";":
            continue
        assert "≔" in line
        lhs, rhs = line.split("≔", 1)
        name = lhs.strip()
        tokens = token_splitter.split(rhs.strip())[1::2]
        tokens.append(...) # Sentinel value
        possibilities_nonselfref = []
        possibilities_selfref = []
        possibilities_headselfref = []
        possibility = []
        for token in tokens:
            if token in ("|", ...): # Either "or" or the end sentinel
                if name not in possibility:
                    possibilities_nonselfref.append(tuple(possibility))
                elif possibility[0] == name:
                    possibilities_headselfref.append(tuple(possibility))
                else:
                    possibilities_selfref.append(tuple(possibility))
                del possibility[:]
            else:
                possibility.append(token)
        rules[name] = tuple(possibilities_selfref + possibilities_nonselfref + possibilities_headselfref)
    return rules

def get_shortcuts(rules):
    shorts = {}
    def get_short(rule, stack):
        if rule in shorts:
            return shorts[rule]
        short = []
        for possibility in rules[rule]:
            p = list(possibility[:])
            ftoken = "''"
            while p and (ftoken in ("''", '""')):
                ftoken = p.pop(0)
            if ftoken in ("''", '""'):
                short.append("")
            elif ftoken[0] in "'\"":
                short.append(ftoken[1])
            elif ftoken in stack:
                # Ignore first-element (GNU-style) recursion
                pass
            elif ftoken == "EOL":
                short.append("\n")
            else:
                short.extend(get_short(ftoken, stack + (rule,)))
        shorts[rule] = frozenset(short)
        return frozenset(short)
    for rule in rules:
        shorts[rule] = get_short(rule, ())
    return shorts

def only_one(possibilities):
    possiblechars = set()
    for i in possibilities:
        if i[0][0] in "'\"":
            subpossiblechar = i[0][1:-1][:1]
            if not subpossiblechar:
                break
            elif subpossiblechar in possiblechars:
                break
            else:
                possiblechars |= {subpossiblechar}
        else:
            subpossiblechars = shorts[i[0]]
            if "" in subpossiblechars:
                break
            elif subpossiblechars & possiblechars:
                break
            else:
                possiblechars |= subpossiblechars
    else: # i.e. didn't encounter break
        return True
    return False

def is_charclass(possibilities):
    if len(possibilities) < 2:
        return False
    for i in possibilities:
        if len(i) > 1:
            return False
        j = i[0]
        if j[0] not in "'\"":
            return False
        elif j[-1] != j[0]:
            raise AssertionError("mismatched quotes?")
        elif len(j) != 3:
            return False
    return True

times = []
def run_bnf(rules, shorts, root, input, handlers):
    exact_stacks = []
    stack = [(root, 0, 0, 0)]
    ipos = 0
    failure_points = []
    active_content = []
    while 1:
        assert (tuple(stack), ipos) not in exact_stacks
        exact_stacks.append((tuple(stack), ipos))
        rule, nth_alternation, nth_conjunction, opos = stack[-1]
        times.append(rule)
        possibilities = rules[rule]
        assert possibilities
        if nth_alternation >= len(possibilities):
            stack, ipos, active_content = failure_points.pop()
            stack = list(stack)
            active_content = list(active_content)
            stack[-1] = (stack[-1][0], stack[-1][1] + 1, stack[-1][2], stack[-1][3])
            continue
        elif len(possibilities) > 1:
            if is_charclass(possibilities) and (nth_conjunction == 0):
                class_ = tuple(i[0][1] for i in possibilities)
                if input[ipos] in class_:
                    active_content.extend(handlers[rule]((input[ipos],)))
                    ipos += 1
                    stack[-1] = (stack[-1][0], stack[-1][1], stack[-1][2] + 1, stack[-1][3])
                    continue
                else:
                    stack, ipos, active_content = failure_points.pop()
                    stack = list(stack)
                    active_content = list(active_content)
                    stack[-1] = (stack[-1][0], stack[-1][1] + 1, stack[-1][2], stack[-1][3])
                    continue
            elif len(set(i[:nth_conjunction] for i in possibilities)) == 1 and (
               len(set(i[:nth_conjunction + 1] for i in possibilities)) != 1):
                # i.e. at the point of divergence
                failure_points.append((tuple(stack), ipos, tuple(active_content)))
        possibility = possibilities[nth_alternation]
        if nth_conjunction >= len(possibility):
            if rule in handlers:
                result = list(handlers[rule](active_content[opos:]))
                del active_content[opos:]
                active_content.extend(result)
            stack.pop()
            if not stack:
                return active_content
            stack[-1] = (stack[-1][0], stack[-1][1], stack[-1][2] + 1, stack[-1][3])
            continue
        this_token = possibility[nth_conjunction]
        if this_token == "EOL":
            this_token = "'\n'"
        #
        if this_token == "EOF":
            if ipos == len(input):
                stack[-1] = (stack[-1][0], stack[-1][1], stack[-1][2] + 1, stack[-1][3])
                continue
            else:
                stack, ipos, active_content = failure_points.pop()
                stack = list(stack)
                active_content = list(active_content)
                stack[-1] = (stack[-1][0], stack[-1][1] + 1, stack[-1][2], stack[-1][3])
                continue
        elif this_token[0] in "'\"":
            literal = this_token[1:-1]
            if input[ipos:(ipos + len(literal))] == literal:
                if only_one(possibilities) and failure_points and (failure_points[-1][1] == ipos):
                    # Useless failure point since no later alternation will match:
                    failure_points.pop()
                active_content.extend(tuple(literal))
                ipos += len(literal)
                stack[-1] = (stack[-1][0], stack[-1][1], stack[-1][2] + 1, stack[-1][3])
                continue
            else:
                stack, ipos, active_content = failure_points.pop()
                stack = list(stack)
                active_content = list(active_content)
                stack[-1] = (stack[-1][0], stack[-1][1] + 1, stack[-1][2], stack[-1][3])
                continue
        else:
            if ("" in shorts[this_token]) or (input[ipos:][:1] in shorts[this_token]):
                stack.append((this_token, 0, 0, len(active_content)))
            else:
                stack, ipos, active_content = failure_points.pop()
                stack = list(stack)
                active_content = list(active_content)
                stack[-1] = (stack[-1][0], stack[-1][1] + 1, stack[-1][2], stack[-1][3])
                continue

class DummyHandler(dict):
    def __getitem__(self, rule):
        try:
            return super().__getitem__(rule)
        except KeyError:
            return (lambda x: [(rule, x)])
    def __contains__(self, rule):
        return True


def handle_chainer(x, rule):
    for i in x:
        if isinstance(i, tuple) and (i[0] == rule):
            assert len(i) == 2
            yield from iter(i[1])
        else:
            yield i

def make_handle_chainer(rule):
    return (lambda x: [(rule, list(handle_chainer(x, rule)))])

if __name__ == "__main__":
    test_handler = DummyHandler()
    test_handler["opt-whitespace"] = lambda x: []
    test_handler["whitespace"] = lambda x: []
    test_handler["maybe-expr"] = lambda x: x
    test_handler["line-end"] = lambda x: []
    test_handler["maybe-list"] = lambda x: x
    test_handler["text1"] = lambda x: x
    test_handler["text2"] = lambda x: x
    test_handler["character"] = lambda x: x
    test_handler["character1"] = lambda x: x
    test_handler["character2"] = lambda x: x
    test_handler["letter"] = lambda x: x
    test_handler["digit"] = lambda x: x
    test_handler["symbol"] = lambda x: x
    test_handler["literal"] = lambda x: [("literal", "".join(x[1:-1]))]
    test_handler["rule-name"] = lambda x: [("rule-name", "".join(x))]
    test_handler["rule-char"] = lambda x: x
    test_handler["rule-chars"] = lambda x: x
    test_handler["term"] = lambda x: x
    test_handler["expression"] = make_handle_chainer("expression")
    test_handler["list"] = make_handle_chainer("list")
    test_handler["syntax"] = lambda x: x
    test_handler["comment"] = lambda x: [("comment", "".join(x[1:-1]))]
    test_handler["comment-char"] = lambda x: x
    test_handler["comment-data"] = lambda x: x

    test = open("test.bnf", "r", encoding="utf-8").read()
    print("Parsing")
    rules = parse_bnf(test)
    print("Shortcutting")
    shorts = get_shortcuts(rules)
    print("Running")
    out = run_bnf(rules, shorts, "root", test, test_handler)
    pprint.pprint(sorted([(i, times.count(i)) for i in set(times)], key=(lambda a: -a[1])))
    pprint.pprint(out)
