from mdplay.cangjie.tables import cang03, cang05

class Agogo(dict):
    def __getitem__(self, key):
        if key not in self:
            self[key]=[]
        return dict.__getitem__(self, key)

def proc_cang(cang):
    cang = cang.strip().split("\n")
    d = Agogo()
    for can in cang:
        if can[0] in "#z":
            continue
        cangjie, kanji, priori = can.split()
        priori = int(priori, 10)
        d[cangjie].append((kanji, priori))
    return d

cangdb = {}
cangdb[3] = proc_cang(cang03)
cangdb[5] = proc_cang(cang05)

def proc_cang(stri, version = 3):
    if version not in cangdb:
        raise ValueError("unsupported revision number of Cangjie or not an int: %r"%version)
    cdb = cangdb[version]
    stri = stri.decode("utf-8")+u"-"
    tub = u""
    out = u""
    for c in stri:
        if c.lower() in u"pyfgcrlaoeuidhtnsqjkxbmwvz0123456789":
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
                if tub not in cdb:
                    out += "<"+tub+">"
                else:
                    outps = sorted(cdb[tub], key=lambda a:("%10d%s"%(100000000-a[1],a[0])))
                    ind %= len(outps)
                    out += outps[ind][0]
            tub = u""
    return out
