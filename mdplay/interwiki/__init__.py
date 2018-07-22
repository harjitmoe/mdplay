__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import sys, os
rp = os.path.split(os.path.abspath(sys.modules[__name__].__file__))[0]
d = {}
# Better (more up to date) should be later:
for p in ["usemod", "meatball", "moin", "wikimedia"]:
    for l in open(os.path.join(rp, p + ".interwiki.txt")):
        if not l.strip() or l[0] == "#":
            continue
        a, b = l.strip().split(None, 1)
        if "$1" not in b:
            if "$PAGE" in b:
                b = b.replace("$PAGE", "$1")
            else:
                b += "$1"
        if b.startswith("//"):
            b = "https:" + b
        d[a.casefold()] = b

interwikis = d
__all__ = ["interwikis"]

