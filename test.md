# Heading #
## Subheading

Paragraphs are
very
nice.  
I think so too.

* Knives
  * Forks
  * Spoons
* Reality
* Hello World.

Another paragraph.

I can use *italic*, **bold**, `monospace`.  I can [link](http://egscomics.com), or include ![](http://i.imgur.com/3yXSlqS.jpg) images and !media[embeds with site-specific tags](http://i.imgur.com/3yXSlqS.jpg), or even [link images ![like this](http://i.imgur.com/3yXSlqS.jpg)](http://egscomics.com)!

~~~~~~~~ python
#!/usr/bin/env python
# -*- python -*-
import utility

#so as to pass JSON to eval
null=None
false=False
true=True

import os,sys

main_db=eval(open(".build/MegaDb.txt","rU").read())

arcs=[]
curatitl=""

useless="""
~~~~~~~
"""

def handle_line(line):
    atitl,ltitl=line["Title"].split(": ",1)
    if atitl!=curatitl:
        arcs.append({"Title":atitl,"StoryLines":[]})
        curatitl=atitl
    arcs[-1]["StoryLines"].append({"Title":ltitl,"Comics":line["Comics"]})

map(handle_line,main_db)

open(".build/MegaDb.txt","w").write(repr(arcs))
~~~~~~~~

> # Can he fix it???
> Bob the
builder
> yes we can
## Verily ##

- - -

Escaping and stuff
------------------

!![This is not](an embed.)

\![This is not](an embed) either.

Whereas this is: !\ ![an embed](http://i.imgur.com/3yXSlqS.jpg)

![This embed](http://i.imgur.com/3yXSlqS.jpg) is also an embed.

\[This is not](a link).

Th[is isn't](either).

Th\ [is is.](http://egscomics.com)

At the start of a  
[line](http://egscomics.com)

Likewise  
![](http://i.imgur.com/3yXSlqS.jpg)

C:\WINDOWS\\--hello--

\---

---

[Useful Notes: UNIX](http://tvtropes.org/pmwiki/pmwiki.php/UsefulNotes/UNIX)

m=Ec^(-2)
