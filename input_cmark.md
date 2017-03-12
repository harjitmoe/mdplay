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

(The following page makes use of Twemoji, by Twitter, Inc.  [CC\-BY 4.0](http://creativecommons.org/licenses/by/4.0/), [origin](https://github.com/twitter/twemoji).)

I can use *italic*, **bold**, `monospace`, **bold**.  I can [link](http://egscomics.com), or include ![](http://i.imgur.com/YW5So8y.jpg) images and !media[embeds with site\-specific tags](http://i.imgur.com/YW5So8y.jpg), or even [link images ![like this](http://i.imgur.com/YW5So8y.jpg)](http://egscomics.com)!

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
> 
> Bob the builder yes we can

## Verily

- - -

## Escaping and stuff

# Escaping and stuff

### Escaping and stuff

!\[This is not](an embed.)

![This is not an embed either.](http://i.imgur.com/YW5So8y.jpg)

Nor is !\[this.]([http://i.imgur.com/YW5So8y.jpg](http://i.imgur.com/YW5So8y.jpg))

Whereas this is: ![an embed](http://i.imgur.com/YW5So8y.jpg)

![This embed](http://i.imgur.com/YW5So8y.jpg) is also an embed.

\[This is not](a link).

Th\[is isn't](either).

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

> Un > Deux >> Trois >>> Quatre 

- - -

> Un
> 
> > Deux
> > 
> > > Trois
> > > 
> > > > Quatre 

Parse\_this\_text stu*pen*dously, *mate*, do you *he*ar me?

- - -

## Level 2 Heading

= Not a heading ==

*Italic*, **bold**, ***both***, '\'neither'\'.

*Italic*, **bold**, ***both***, \*neither\*.

*Italic*, **bold**, ***both***, \_neither\_.

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

ATX code block syntax:

~~~~~~ ::
Thusly.
~~~~~~

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

~~~~~~ ::
Shouldn't make that  
much difference when
nouicode flag passed.

Second paragraph

Third paragraph

~~~~~~

Søren. Søren.

J'ai regardé.

Watashi\-wa Tōmasu desu.

*illegitimi nōn carborundum*.

*spuriīs nōn carborandum*.

øe vs œ vs \\oe vs œ mate.

{Nothing \^(Special) *h*.}

{Nothing \^(Spe{cial}) *h*.}

{Nothing} \^(Spe{cial}). *h*

|Why|What|
|---|---|
|123|4567 8 9|
|a|bcde|
|fgh|ijkl|
||mnop|
|123||
|456|789|
|UUU|Dwelt|

|Why|What|
|:-:|:--|
|123|4567 8 9|
|a|bcde|
|fgh|ijkl|
||mnop|
|123||
|456|789|
|UUU|Dwelt|

Hi.

Hello.

~~~~~~ ::
 Indent
ation.

~~~~~~

~~~~~~ ::
Indent
~~~~~~

~~~~~~ ::
ation.

~~~~~~

~~~~~~ ::
''Breaking''

the news (still in code).

~~~~~~

~~~~~~ ::
Breaking

the news (also).


~~~~~~

!wiki[](User:HarJIT)

!wiki[KSP](The King's (The Cathedral\) School)

!wiki[KSP *(again)*](The King's (The Cathedral\) School)

!wiki[Hmm...](Try ''to'' br{'e}ak ``this``...)


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

[Testing hashes.](http://i.imgur.com/YW5So8y.jpg#hash)

![Let me *break* this!](http://i.imgur.com/YW5So8y.jpg)

~In other news~

Tōkyō.  Literal &amp;omacr; or &amp;omacr;.

&amp;unescaped behaviour.

\[This is not a piped link.]([http://egscomics.com](http://egscomics.com))

<omitting semicolons>, &amp;amoled.

Testing ordered lists:


1) The spirit of God, like a fire, is burning; 
2) the latter day glory begins to come forth. 
3) The visions and blessings of old are returning, 
4) and angels are coming to visit the earth. 


* We'll sing and we'll shout with the armies of Heaven, 
* "Hosanna!  Hosanna to God and the Lamb! 
* Let glory to them in the highest be given 
* henceforth and forever, Amen and Amen!" 
5) The Lord is extending the Saints' understanding... 

(note that the above may come out as 1 or 5, depending on mdplay renderer, flags and targeted system)


1) An ol containing an 
  * Ul containing an 
    1) Ol containing 
      1) Another ol containing 
        * An ul containing 
          * Another ul 
      2) Coming back to this level. 
  * Similarly 

This is just a paragraph.  ( ͡° ͜ʖ ͡° )  [It actually is.](/spoiler) ![🖖](https://twemoji.maxcdn.com/2/72x72/1f596.png =32x32) ![👀](https://twemoji.maxcdn.com/2/72x72/1f440.png =32x32) ![👀](https://twemoji.maxcdn.com/2/72x72/1f440.png =32x32)

Squirt ![♈](https://twemoji.maxcdn.com/2/72x72/2648.png =32x32) Squirt ![♈](https://twemoji.maxcdn.com/2/72x72/2648.png =32x32) Squirt ![♈](https://twemoji.maxcdn.com/2/72x72/2648.png =32x32)

![😄](https://twemoji.maxcdn.com/2/72x72/1f604.png =32x32) ![😀](https://twemoji.maxcdn.com/2/72x72/1f600.png =32x32) ![😆](https://twemoji.maxcdn.com/2/72x72/1f606.png =32x32) ![☺](https://twemoji.maxcdn.com/2/72x72/263a.png =32x32) ![:demonicduck:](http://i.imgur.com/SfHfed9.png)

|Why|What|
|:-:|:--|
|123|4567 8 9|
|a|bcde|
|fgh|ijkl|
||mnop|
|123||
|456|789|
|UUU|Dwelt|

m̈ëẗälë Ë

ẍ=\-ω^(2)x

![🙆](https://twemoji.maxcdn.com/2/72x72/1f646.png =32x32) ![🙆🏽](https://twemoji.maxcdn.com/2/72x72/1f646-1f3fd.png =32x32) ![🙆🏿](https://twemoji.maxcdn.com/2/72x72/1f646-1f3ff.png =32x32)

![♈](https://twemoji.maxcdn.com/2/72x72/2648.png =32x32) ![small image](http://i.imgur.com/YW5So8y.jpg =32x32) ![small image](http://i.imgur.com/YW5So8y.jpg =32x)

![🖖🏿](https://twemoji.maxcdn.com/2/72x72/1f596-1f3ff.png =32x32) ![🖖](https://twemoji.maxcdn.com/2/72x72/1f596.png =32x32)‌![🏿](https://twemoji.maxcdn.com/2/72x72/1f3ff.png =32x32)  
![🖖🏼](https://twemoji.maxcdn.com/2/72x72/1f596-1f3fc.png =32x32) ![🖖](https://twemoji.maxcdn.com/2/72x72/1f596.png =32x32)‌![🏼](https://twemoji.maxcdn.com/2/72x72/1f3fc.png =32x32)  
![🖖🏽](https://twemoji.maxcdn.com/2/72x72/1f596-1f3fd.png =32x32) ![🖖](https://twemoji.maxcdn.com/2/72x72/1f596.png =32x32)‌![🏽](https://twemoji.maxcdn.com/2/72x72/1f3fd.png =32x32)

:undiefined:

![🇯🇵](https://twemoji.maxcdn.com/2/72x72/1f1ef-1f1f5.png =32x32) ![🇯](https://twemoji.maxcdn.com/2/72x72/1f1ef.png =32x32)‌![🇵](https://twemoji.maxcdn.com/2/72x72/1f1f5.png =32x32)

Testing a URN: [x\-wikipedia:Tree](x-wikipedia:Tree)

x̄ and ȳ

これは なん ですか?

日本語 (にほんご)

日本語 (Nihongo)

日 (に) 本 (ほん) 語 (ご)

日日日曰曰曰

円丹丹円円

<blm>丹丹円円

円丹丹㓀㓀

円

これは (Kore wa)  なん (nan)  ですか (desu ka) ?

Pinguinet (PANG\-win\-ay)

チ チ ティ  
ティ チ ティ

グッチ グッチ グッチ

サッポロ サッポロ

ジ ズ ヂ ヅ ヅ  
ジ ズ ディ ドゥ ヅ

キェ ブァハハハハ イェヴィンギャ シジチヂツヅ  
キェ ブァハハハハ イェヴィンギャ スィズィティディトゥドゥ

[Spojra](/spoiler)

ヴァ ヴィ ヴ ヴェ ヴォ 〜 ヴャ ヸ ヴュ ヹ ヴョ 〜 ヴァ ヴィ ヴゥ ヴェ ヴォ 〜 ヷ ヸ ヺゥ ヹ ヺ

テガみ てがみ テガミ

![🌚](https://twemoji.maxcdn.com/2/72x72/1f31a.png =32x32) 🌚︎![︎](https://twemoji.maxcdn.com/2/72x72/fe0e.png =32x32) ![🌚](https://twemoji.maxcdn.com/2/72x72/1f31a.png =32x32)![️](https://twemoji.maxcdn.com/2/72x72/fe0f.png =32x32) ![🌚](https://twemoji.maxcdn.com/2/72x72/1f31a.png =32x32)‌![︎](https://twemoji.maxcdn.com/2/72x72/fe0e.png =32x32)

![😄](https://twemoji.maxcdn.com/2/72x72/1f604.png =32x32) 😄︎![︎](https://twemoji.maxcdn.com/2/72x72/fe0e.png =32x32) ![😄](https://twemoji.maxcdn.com/2/72x72/1f604.png =32x32)![️](https://twemoji.maxcdn.com/2/72x72/fe0f.png =32x32) ![😄](https://twemoji.maxcdn.com/2/72x72/1f604.png =32x32)‌![︎](https://twemoji.maxcdn.com/2/72x72/fe0e.png =32x32)

