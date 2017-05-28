# For debugging.

import re
import pprint

__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay import nodes

def repr_out(nodes,titl_ignored=None,flags=()):
    return repr_out_body(nodes,flags=flags)

def repr_out_body(nodes,flags=()):
    return pprint.pformat(_repr_out_body(nodes,flags=flags))

def _repr_out_body(nodes,flags=()):
    in_list=0
    r=[]
    for node in nodes:
        r.append(_repr_out(node,flags=flags))
    return r

def _repr_out(node,flags):
    if not isinstance(node,nodes.Node): #i.e. is a string
        return node
    else:
        dci=node.__dict__
        dco={}
        dco["NODE_TYPE"]=node.__class__.__name__
        for i in dci.keys():
            if i[0]!="_":
                if i in ("content","label"):
                    dco[i]=map(_repr_out,dci[i],[flags]*len(dci[i]))
                elif i in ("table_head","table_body"):
                    dco[i]=[]
                    for j in dci[i]:
                        dco[i].append([])
                        for k in j:
                            dco[i][-1].append(map(_repr_out,k,[flags]*len(k)))
                else:
                    dco[i]=dci[i]
        return dco

__mdplay_renderer__="repr_out"
__mdplay_snippet_renderer__="repr_out_body"

