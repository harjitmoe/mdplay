"""Isolated from "pickups", an IRC gateway for Google Hangouts.

Altered for Python 2 / mdplay integration."""

__orig_doc__="""Utility functions."""

__copying__="""
Copyright (c) 2014 Michael Tom-Wing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#from hangups.ui.utils import get_conv_name
import hashlib
import re
import unicodedata
from mdplay.utfsupport import unichr4all

CONV_HASH_LEN = 7


def strip_non_printable(s):
    return ''.join(c for c in s
                   if unicodedata.category(c) not in ['Cc', 'Zs', 'So'])


#def conversation_to_channel(conv):
#    """Return channel name for hangups.Conversation."""
#    # Must be 50 characters max and not contain space or comma.
#    conv_hash = hashlib.sha1(conv.id_.encode()).hexdigest()
#    name = get_conv_name(conv).replace(',', '_').replace(' ', '')
#    name = strip_non_printable(name)
#    return '#{}[{}]'.format(name[:50 - CONV_HASH_LEN - 3],
#                            conv_hash[:CONV_HASH_LEN])


def channel_to_conversation(channel, conv_list):
    """Return hangups.Conversation for channel name."""
    match = re.search(r'\[([a-f0-9]+)\]$', channel)
    if match is None:
        return None
    conv_hash = match.group(1)
    return dict([(hashlib.sha1(conv.id_.encode()).hexdigest()[:CONV_HASH_LEN], conv)
            for conv in conv_list.get_all()]).get(conv_hash, None)


def get_nick(user):
    """Return nickname for a hangups.User."""
    # Remove disallowed characters and limit to max length 15
    return re.sub(r'[^\w\[\]\{\}\^`|_\\-]', '', user.full_name)[:15]


def get_hostmask(user):
    """Return hostmask for a hangups.User."""
    return '{}!{}@hangouts'.format(get_nick(user), user.id_.chat_id)


#def get_topic(conv):
#    """Return IRC topic for a conversation."""
#    return 'Hangouts conversation: {}'.format(get_conv_name(conv))


SMILEYS = dict([(unichr4all(k), v) for k, v in {
        0x263a: ':)',
        0x1f494: '</3',
        0x1f49c: '<3',
        0x1f60a: '=D',
        0x1f600: ':D',
        0x1f601: '^_^',
        0x1f602: ':\'D',
        0x1f603: ':D',
        0x1f604: ':D',
        0x1f605: ':D',
        0x1f606: ':D',
        0x1f607: '0:)',
        0x1f608: '}:)',
        0x1f609: ';)',
        0x1f60e: '8)',
        0x1f610: ':|',
        0x1f611: '-_-',
        0x1f613: 'o_o',
        0x1f614: 'u_u',
        0x1f615: ':/',
        0x1f616: ':s',
        0x1f617: ':*',
        0x1f618: ';*',
        0x1f61B: ':P',
        0x1f61C: ';P',
        0x1f61E: ':(',
        0x1f621: '>:(',
        0x1f622: ';_;',
        0x1f623: '>_<',
        0x1f626: 'D:',
        0x1f62E: ':o',
        0x1f632: ':O',
        0x1f635: 'x_x',
        0x1f638: ':3',
}.items()])

def smileys_to_ascii(s):
    res = []
    for i, c in enumerate(s):
        if c in SMILEYS:
            res.append(SMILEYS[c])
            if i < len(s) - 1 and s[i + 1] in SMILEYS: # separate smileys
                res.append(' ')
        else:
            res.append(c)
    return ''.join(res)
