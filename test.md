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
  * Ceramic  
    knifes
    
    rule.
* Reality
* Hello World.

Another paragraph.

(The following page makes use of Twemoji, by Twitter, Inc.  [CC-BY 4.0](http://creativecommons.org/licenses/by/4.0/), [origin](https://github.com/twitter/twemoji).)

I can use *italic*, **bold**, `monospace`, __bold__.  I can [link](http://egscomics.com), or include ![](http://i.imgur.com/YW5So8y.jpg) images and !media[embeds with site-specific tags](http://i.imgur.com/YW5So8y.jpg), or even [link images ![like this](http://i.imgur.com/YW5So8y.jpg)](http://egscomics.com)!

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
#Of note, this is where GitHub's own parser goes wrong.
#A seven-tilde sequence should embed in an eight-tilde fence.
#This is still in the code-block.
#Repeating to humour GitHub:
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

![This is not](an embed.)

\![This is not an embed either.](http://i.imgur.com/YW5So8y.jpg)

Nor is !\[this.](http://i.imgur.com/YW5So8y.jpg)

Whereas this is: ![an embed](http://i.imgur.com/YW5So8y.jpg)

![This embed](http://i.imgur.com/YW5So8y.jpg) is also an embed.

\[This is not](a link).

Th\[is isn't](either).

Th[is is.](http://egscomics.com)

At the start of a  
[line](http://egscomics.com)

Likewise  
![](http://i.imgur.com/YW5So8y.jpg)

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

> Un
>> Deux
>>> Trois
>>>> Quatre

---

> Un
>
>> Deux
>>
>>> Trois
>>>
>>>> Quatre

Parse_this_text stu*pen*dously, _mate_, do you _he_\ ar me?

---

== Level 2 Heading ==

= Not a heading ==

''Italic'', '''bold''', '''''both''''', \''neither\''.

*Italic*, **bold**, ***both***, \*neither\*.

_Italic_, __bold__, ___both___, \_neither\_.

# Level 1

#Not heading

# Level 1 #

## Level 2

####
 Hi
####

### Level 3

What does this do?
- - -

What does this do?

- - -

ATX code block syntax::

Thusly.

Indented code block::

    Hello world

Indented code block: ::
    Hello world

Indented code block:

::

    Hello world

Hello.

Indented code block:

::

    Hello world

Ada.

== Trivial indentation of paragraphs ==

    Shouldn't make that  
    much difference when
    nouicode flag passed.
    
    Second paragraph

    Third paragraph

S{\o}ren.
S{\Bo}ren.

J'ai regard{\'e}.

Watashi-wa T{\=o}masu desu.

''illegitimi n{\=o}n carborundum''.

''spuri{\=i}s n{\=o}n carborandum''.

{\o}e vs {\oe} vs {\o{e}} vs {\oe{}} mate.

{Nothing \^(Special) *h*.}

{Nothing \^(Spe{cial}) *h*.}

{Nothing} \^(Spe{cial}). *h*

=== ====
Why What
=== ====
123 4567
    8 9 
a   bcde
fgh ijkl
\   mnop
123
456 789
UUU Dwe\
    lt
=== ====

Why|What
:-:|:--
123|4567 8 9
a|bcde
fgh|ijkl
 |mnop
123| 
456|789
UUU|Dwelt

Hi.

Hello.

     Indent
    ation.

::

     Indent
    ation.

::

    ''Breaking''

    the news (still in code).

::

    Breaking
    
    the news (also).
    

!wiki[](User:HarJIT)

!wiki[KSP](The King's (The Cathedral\) School)

[[The King's (The Cathedral) School|KSP ''(again)'']]

[[Try ''to'' br{\'e}ak ``this``...|Hmm...]]

* one
* list
- another
- list

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

[Testing hashes.](http://i.imgur.com/YW5So8y.jpg#hash)

![Let me _break_ this!](http://i.imgur.com/YW5So8y.jpg)

~In other news~

T&omacr;ky&omacr;.  Literal \&omacr; or &amp;omacr;.

&unescaped behaviour.

&lsqb;This is not a piped link.](http://egscomics.com)

&ltomitting semicolons&gt, &amoled.

Testing ordered lists:

1. The spirit of God, like a fire, is burning;
2. the latter day glory begins to come forth.
3. The visions and blessings of old are returning,
4. and angels are coming to visit the earth.

* We'll sing and we'll shout with the armies of Heaven,
* "Hosanna!  Hosanna to God and the Lamb!
* Let glory to them in the highest be given
* henceforth and forever, Amen and Amen!"
5. The Lord is extending the Saints' understanding...

(note that the above may come out as 1 or 5, depending
on mdplay renderer, flags and targeted system)

1. An ol containing an
   - Ul containing an
     1. Ol containing
        1. Another ol containing
           - An ul containing
             - Another ul
        2. Coming back to this level.
   - Similarly

This is just a paragraph.  :lenny:  [It actually is.](/spoiler) :vulcan: :dan_shifty: :eyes:

Squirt :aries: Squirt :aries: Squirt ♈ 

.. ::
   
   <:demonicduck:http://i.imgur.com/SfHfed9.png>

:smile: :grinning: :D :) :demonicduck:

|Why|What|
|:---:|:---|
|123|4567 8 9|
|a|bcde|
|fgh|ijkl|
| |mnop|
|123| |
|456|789|
|UUU|Dwelt|

{\"m}{\"e}{\"t}{\"a}l{\"e} {\"E}

{\"x}=-ω^(2)x

🙆 🙆🏽 🙆:tone5:

:aries: ![small image](http://i.imgur.com/YW5So8y.jpg =32x32)
![small image](http://i.imgur.com/YW5So8y.jpg =32x)

:vulcan::tone5: :vulcan:&zwnj;:tone5:  
:vulcan::tone2: :vulcan:&zwnj;:tone2:  
:vulcan:🏽 :vulcan:&zwnj;🏽

:undiefined:

🇯🇵 🇯&zwnj;🇵

Testing a URN: urn:x-interwiki:wikipedia:Tree

Case sensitivity: urn:x-interwiki:gausswiki:Hello [Eh?](uRn:x-inteRwiki:gaUßwiki:Hello)

{\=x} and {\=y}

!hkana[](koreha nan desuka?)

!souketsu[!hkana[](Nihongo)](a-dm yrmmr)

!souketsu[Nihongo](a-dm yrmmr)

!souketsu[!hkana[](Ni)](a)\ !cang[!hkana[](hon)](dm)\ !cang[!hkana[](go)](yrmmr)

!souketsu[](a a1 a01 az a2 a02)

!cang[](blm by by1 byz by2)

!cang3[](blm by by1 byz by2)

!cang5[](blm by by1 byz by2)

!cang5[](blm65535)

!hkana[Kore wa](koreha) !hkana[nan](nan) !hkana[desu ka](desuka)?

!rubi[PANG-win-ay](Pinguinet)

!kana[](ti chi texi)  
!kana_hbn[](ti chi texi)

!kana[](gucchi) !kana[](gutchi) !kana[](gutti)

!kana[](Sapporo) !kana[](Satporo)

!kana[](ji zu di du dzu)  
!kana_hbn[](ji zu di du dzu)

!kana[](kye bwahahahaha yevingya sizitiditudu)  
!kana_hbn[](kye bwahahahaha yevingya sizitiditudu)

[Spojra](#s)

!kana[](va vi vu ve vo ~ vya vyi vyu vye vyo ~ vha vhi vhu vhe vho ~ vwa vwi vwu vwe vwo)

!kana[](teガみ) !hkana[](teガみ) !kkana[](teガみ)

:darkmoon: :darkmoon::textstyle: :darkmoon::emojistyle: :darkmoon:&zwnj;:textstyle:

:smile: :smile::textstyle: :smile::emojistyle: :smile:&zwnj;:textstyle:

This should be a rainbow banner: :flag_white::emojistyle:&zwj;:rainbow: or :rainbow_flag: or :gay_pride_flag:

⛹🏻‍♀️

:basketball_player::tone1:&zwj;:female_sign::emojistyle:

:D

''This should behave more or less as expected.&ensp;However, I have reason to believe otherwise.'' (Should be fixed now…)

[Labelled spoiler](/s Watch out, this is a spoiler!)

Discord emote: :kananYouNot: <:wacko:230129080886886400> <:ConcernFroge:306183254350757888> <:kananYouNot:264549500385886208> <:madeupemoteshortcode:306183254350757888> :madeupemoteshortcode: :kananYouNot:

.. mdplay-flag:: discordunderline
   
   __Greetings__

.. mdplay-flag:: -discordunderline
   
   __Greetings__

:vanirLUL:

./. mdplay-include:: konosubadiscord_usage.md works but takes a looong time.

:vanirLUL:

:vulcan::tone5:

:vulcan:&zwnj;:tone5:

:tone5:

!hkana[](megumin) (JA)  
→ !cang[!hkana[](megu)](jip)!hkana[](min) (reconstructed kanji spelling, even though one clearly isn't used for her (S2 OVA confirms Megumin cannot read Japanese script), rather than resort to a Mandarin ateji / ji{\`e}z{\`i} &mdash; the !hkana[](mi) is okurigana)  
→ !cang[!hkana[](megumi)](jip)!cang[!hkana[](n)](jip) (doubled, presumably in analogy to the appended &ndash;!hkana[](n) &mdash; annotated here thusly)  
→ !cang[hui4&ensp;](jip)!cang[hui4](jip) (ZH)

!fullwidth[](£$¥¢€vapourwave, CWM FJORDBANK GLYPHS VEXT QUIZ.)

The wonders of obscure Unicode: ￹和真￺カズマ￻。

Likewise for KsubsubsubscriptL and supersuperLsuperKscript.

Trying with HTML escapes &#x8b;subscript&#x8c; &#x1b;Lsuperscript&#x1b;K: &#65529;和真&#65530;カズマ&#65531;。

HZ encoding: ~{NR$,C{$O$a$0$_$s#!~} ~{〘NR$,C{$O$a$0$_$s#!〙~}

~{QN!$;]~} / ~jis~{1v!&X*!&7C~}

>! Block spoiler

And >!Inline spoiler!<

Hello\\world hello\\\`world hello\\\\world

~~Crossed out~~

&not;in &notin; &notin

\ >!Inline spoiler!< again.

Testing [1\\This[3\\as[0\\ so.

[This should [actually work now](http://example.com/).]

[This] should [actually work now](http://example.com/).

[This](http://example.com/) should [ideally] actually [work now](http://example.com/).

\