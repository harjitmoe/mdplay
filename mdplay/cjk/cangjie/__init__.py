__copying__ = """
This file part of MDPlay, not subject to COPYING.tables

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import os

class Agogo(dict):
    def __getitem__(self, key):
        if key not in self:
            self[key] = []
        return dict.__getitem__(self, key)

class Zagogo(dict):
    def __getitem__(self, key):
        if key not in self:
            self[key] = 1 #Note not 0
        return dict.__getitem__(self, key)

def init_proc_cang(cang):
    cang = cang.strip().split("\n")
    d = Agogo()
    dd = Zagogo()
    for can in cang:
        if can[0] in "#z":
            continue
        cangjie, kanji, priori = can.split()
        priori = int(priori, 10)
        d[cangjie].append((kanji, priori))
        dd[kanji] = priori
    return d, dd

cdbf = os.path.join(os.path.dirname(__file__), "cangdb.py")
pdbf = os.path.join(os.path.dirname(__file__), "popdb.py")
if os.path.exists(cdbf) and os.path.exists(pdbf):
    from mdplay.cjk.cangjie.cangdb import cangdb
    cangdb[3] = Agogo(cangdb[3])
    cangdb[5] = Agogo(cangdb[5])
    from mdplay.cjk.cangjie.popdb import popdb
    popdb[3] = Zagogo(popdb[3])
    popdb[5] = Zagogo(popdb[5])
else:
    from mdplay.cjk.cangjie.tables import cang03, cang05
    cangdb = {}
    popdb = {}
    cangdb[3], popdb[3] = init_proc_cang(cang03)
    cangdb[5], popdb[5] = init_proc_cang(cang05)
    open(cdbf, "w").write("# coding: utf-8\ncangdb = " + repr(cangdb))
    open(pdbf, "w").write("# coding: utf-8\npopdb = " + repr(popdb))

def proc_cang(stri, version = -1):
    if version==3:
        cdb = cangdb[3]
        ncdb = cangdb[5]
        nntub = popdb[3]
    elif version==5:
        cdb = cangdb[5]
        ncdb = cangdb[3]
        nntub = popdb[3]
    elif version==-1:
        cdb = cangdb[3]
        ncdb = cangdb[5]
        nntub = popdb[3]
    else:
        raise ValueError("unsupported revision number of Cangjie or not an int: %r"%version)
    stri = stri + "-"
    tub = ""
    out = ""
    for c in stri:
        if c.lower() in "pyfgcrlaoeuidhtnsqjkxbmwvz0123456789":
            tub += c.lower()
        else:
            tub2 = ""
            while tub[-1] in "0123456789":
                tub2 = tub[-1] + tub2
                tub = tub[:-1]
            ind = 0
            if tub2:
                ind = int(tub2, 10)-1
            while tub[-1]=="z":
                ind += 1
                tub = tub[:-1]
            if tub:
                #Recall that cdb and ncdb are Agogo instances
                if (cdb[tub] or ncdb[tub]) and (version==-1):
                    mydb = Zagogo(cdb[tub])
                    for k,v in ncdb[tub]:
                        if k not in mydb:
                            mydb[k] = v*2 #Scale differences between the tables
                    outps = sorted(list(mydb.items()), key=lambda a:("%12d%s"%(100000000000-nntub[a[0]],a[0])))
                    ind %= len(outps)
                    out += outps[ind][0]
                elif cdb[tub]:
                    outps = sorted(cdb[tub], key=lambda a:("%12d%s"%(100000000000-nntub[a[0]],a[0])))
                    ind %= len(outps)
                    out += outps[ind][0]
                else:
                    out += "<"+tub+">"
            tub = ""
    return out
