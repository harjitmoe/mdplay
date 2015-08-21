# Heading #
## Subheading

Overcast
--------

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

I can use *italic*, **bold**, `monospace`, __bold__.  I can [link](http://egscomics.com), or include ![](http://i.imgur.com/3yXSlqS.jpg) images and !media[embeds with site-specific tags](http://i.imgur.com/3yXSlqS.jpg), or even [link images ![like this](http://i.imgur.com/3yXSlqS.jpg)](http://egscomics.com)!

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

====================
 Escaping and stuff
====================

Escaping and stuff
^^^^^^^^^^^^^^^^^^

!![This is not](an embed.)

\![This is not](an embed) either.

Th![is likewise isn't](an embed).

Whereas this is: !\ ![an embed](http://i.imgur.com/3yXSlqS.jpg)

![This embed](http://i.imgur.com/3yXSlqS.jpg) is also an embed.

\[This is not](a link).

Th\[is isn't](either).

Th[is is.](http://egscomics.com)

At the start of a  
[line](http://egscomics.com)

Likewise  
![](http://i.imgur.com/3yXSlqS.jpg)

C:\WINDOWS\\--hello--

\\*Italics*

\---

---

[Useful Notes: UNIX](http://tvtropes.org/pmwiki/pmwiki.php/UsefulNotes/UNIX)

## Superscripts and subscripts ##

m=Ec^(-2)

E=(mv(^2^))/2

CH(~3~)COOH

Back^((not Backside\))

(\^Not a superscript.^) \(^Not a superscript either.^) \^(Nor this.) ^\(Or this.)

>! The lie is a muffin.

>! Expand the below for a spoiler:
>!
>!>! (Insert picture of the back of a racing car here.)

Parse_this_text stu*pen*dously, _mate_, do you _he_\ ar me?

---

== Level 2 Heading ==

= Not a heading ==
