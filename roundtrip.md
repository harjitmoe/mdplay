# Heading

## Subheading

## Overcast

Paragraphs are very nice.  
I think so too.


* Knives 
  * Forks 
  * Spoons 
  * Ceramic  
    knifes
    
    rule.
* Reality 
* Hello World. 

Another paragraph.

I can use *italic*, **bold**, `monospace`, \ __bold__\ .  I can [link](http://egscomics.com), or include ![](http://i.imgur.com/YW5So8y.jpg) images and !media[embeds with site\-specific tags](http://i.imgur.com/YW5So8y.jpg), or even [link images ![like this](http://i.imgur.com/YW5So8y.jpg)](http://egscomics.com)!

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
> 
> Bob the builder yes we can

## Verily

- - -

## Escaping and stuff

# Escaping and stuff

### Escaping and stuff

!![This is not](an embed.)

!\[This is not](an embed) either.

Th![is likewise isn\'t](an embed).

Whereas this is: !![an embed](http://i.imgur.com/YW5So8y.jpg)

![This embed](http://i.imgur.com/YW5So8y.jpg) is also an embed.

\[This is not](a link).

Th\[is isn\'t](either).

Th[is is.](http://egscomics.com)

At the start of a  
[line](http://egscomics.com)

Likewise  
![](http://i.imgur.com/YW5So8y.jpg)

C:\\WINDOWS\\\-\-hello\-\-

\\*Italics*

\-\-\-

- - -

[Useful Notes: UNIX](http://tvtropes.org/pmwiki/pmwiki.php/UsefulNotes/UNIX)

## Superscripts and subscripts

m=Ec^(\-2)

E=(mv^(2))/2

CH(~3~)COOH

Back^((not Backside\))

(\^Not a superscript.\^) (\^Not a superscript either.\^) \^(Nor this.) \^(Or this.)

>! The lie is a muffin. 

>! Expand the below for a spoiler:
>! 
>! >! (Insert picture of the back of a racing car here.) 

Parse\_this\_text stu*pen*dously, \ _mate_\ , do you \ _he_\ ar me?

- - -

## Level 2 Heading

= Not a heading ==

\ _Italic_\ , \ __bold__\ , \ __\ _both_\ __\ , \'\'neither\'\'.

*Italic*, **bold**, ***both***, \*neither\*.

\ _Italic_\ , \ __bold__\ , \ __\ _both_\ __\ , \_neither\_.

# Level 1

#Not heading

# Level 1

## Level 2

#### Hi

### Level 3

What does this do?

- - -

What does this do?

- - -

Faking:

Thusly.

Indented code block:

~~~~~~ ::
Hello world

~~~~~~

Indented code block:

~~~~~~ ::
Hello world

~~~~~~

Indented code block:

~~~~~~ ::
Hello world

~~~~~~

Hello.

Indented code block:

~~~~~~ ::
Hello world

~~~~~~

Ada.

## Trivial indentation of paragraphs

Shouldn\'t make that  
much difference. Except when uicode flag passed.

Second paragraph

Third paragraph

Søren. Søren.

J\'ai regardé.

Watashi\-wa Tōmasu desu.

\ _illegitimi nōn carborundum_\ .

\ _spuriīs nōn carborandum_\ .

øe vs œ vs \\oe vs œ mate.

{Nothing \^(Special) *h*.}

{Nothing \^(Spe{cial}) *h*.}

{Nothing} \^(Spe{cial}). *h*

==== =========
Why  What 
==== =========
123  4567 8 9 
a    bcde 
fgh  ijkl 
\    mnop 
123  
456  789 
UUU  Dwelt 
==== =========

=== ========
Why What
=== ========
123 4567 8 9
a   bcde
fgh ijkl
\   mnop
123 
456 789
UUU Dwelt
=== ========

Hi.

Hello.

Indent ation.

~~~~~~ ::
Indent
~~~~~~

ation.

~~~~~~ ::
''Breaking''

the news (still in code).

~~~~~~

~~~~~~ ::
Breaking

the news (also).


~~~~~~

!wikilink[](User:HarJIT)

!wikilink[KSP](The King's (The Cathedral\) School)


* one 
* list 


* another 
* list 

And


* one 
* list 


* another 
* list 

And


* one 
* list 
* ``*sa`me*`` 
* list 
