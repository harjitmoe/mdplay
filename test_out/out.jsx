html({}, head({}, meta({content: "text/html; charset=UTF-8", "http-equiv": "Content-Type"}), title({}, "test.md")), body({}, h1({}, "Heading "), h2({}, "Subheading "), h2({}, "Overcast "), p({}, "Paragraphs are very nice.", br({}), "I think so too. "), "", ul({}, li({}, "Knives ", ul({}, li({}, "Forks "), li({}, "Spoons "), li({}, p({}, "Ceramic", br({}), "knifes "), p({}, "rule. ")))), li({}, "Reality "), li({}, "Hello World. ")), p({}, "Another paragraph. "), p({}, "(The following page makes use of Twemoji, by Twitter, Inc.\u00a0 ", a({href: "http://creativecommons.org/licenses/by/4.0/"}, "CC-BY 4.0"), ", ", a({href: "https://github.com/twitter/twemoji"}, "origin"), ".) "), p({}, "I can use ", em({}, "italic"), ", ", strong({}, "bold"), ", ", code({}, "monospace"), ", ", b({}, "bold"), ".\u00a0 I can ", a({href: "http://egscomics.com"}, "link"), ", or include ", img({src: "http://i.imgur.com/YW5So8y.jpg"}), " images and ", media({alt: "embeds with site-specific tags", src: "http://i.imgur.com/YW5So8y.jpg"}), ", or even ", a({href: "http://egscomics.com"}, "link images ", img({alt: "like this", src: "http://i.imgur.com/YW5So8y.jpg"})), "! "), pre({}, "#!/usr/bin/env python\n# -*- python -*-\nimport utility\n\n#so as to pass JSON to eval\nnull=None\nfalse=False\ntrue=True\n\nimport os,sys\n\nmain_db=eval(open(\".build/MegaDb.txt\",\"rU\").read())\n\narcs=[]\ncuratitl=\"\"\n\nuseless=\"\"\"\n~~~~~~~\n\"\"\"\n#Of note, this is where GitHub's own parser goes wrong.\n#A seven-tilde sequence should embed in an eight-tilde fence.\n#This is still in the code-block.\n#Repeating to humour GitHub:\nuseless=\"\"\"\n~~~~~~~\n\"\"\"\n\ndef handle_line(line):\n    atitl,ltitl=line[\"Title\"].split(\": \",1)\n    if atitl!=curatitl:\n        arcs.append({\"Title\":atitl,\"StoryLines\":[]})\n        curatitl=atitl\n    arcs[-1][\"StoryLines\"].append({\"Title\":ltitl,\"Comics\":line[\"Comics\"]})\n\nmap(handle_line,main_db)\n\nopen(\".build/MegaDb.txt\",\"w\").write(repr(arcs))\n"), blockquote({}, h1({}, "Can he fix it??? "), p({}, "Bob the builder yes we can ")), h2({}, "Verily "), hr({}), h2({}, "Escaping and stuff "), h1({}, "Escaping and stuff "), h3({}, "Escaping and stuff "), p({}, "![This is not](an embed.) "), p({}, "!", a({href: "http://i.imgur.com/YW5So8y.jpg"}, "This is not an embed either."), " "), p({}, "Nor is ![this.](", a({href: "http://i.imgur.com/YW5So8y.jpg"}, "http://i.imgur.com/YW5So8y.jpg"), ") "), p({}, "Whereas this is: ", img({alt: "an embed", src: "http://i.imgur.com/YW5So8y.jpg"}), " "), p({}, img({alt: "This embed", src: "http://i.imgur.com/YW5So8y.jpg"}), " is also an embed. "), p({}, "[This is not](a link). "), p({}, "Th[is isn't](either). "), p({}, "Th", a({href: "http://egscomics.com"}, "is is."), " "), p({}, "At the start of a", br({}), a({href: "http://egscomics.com"}, "line"), " "), p({}, "Likewise", br({}), img({src: "http://i.imgur.com/YW5So8y.jpg"}), " "), p({}, "C:\\WINDOWS\\--hello-- "), p({}, "\\", em({}, "Italics"), " "), p({}, "--- "), hr({}), p({}, a({href: "http://tvtropes.org/pmwiki/pmwiki.php/UsefulNotes/UNIX"}, "Useful Notes: UNIX"), " "), h2({}, "Superscripts and subscripts "), p({}, "m=Ec", sup({}, "-2"), " "), p({}, "E=(mv", sup({}, "2"), ")/2 "), p({}, "CH", sub({}, "3"), "COOH "), p({}, "Back", sup({}, "(not Backside)"), " "), p({}, "(^Not a superscript.^) (^Not a superscript either.^) ^(Nor this.) ^(Or this.) "), div({"class": "spoilerwrapper"}, p({}, a({href: "javascript:void(0)", onclick: "document.getElementById('spoil1').style.display = (document.getElementById('spoil1').style.display=='none')?('block'):('none');"}, "Expand/Hide Spoiler")), div({"class": "spoiler", id: "spoil1", style: "border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;"}, "The lie is a muffin. "), script({type: "text/javascript"}, "document.getElementById('spoil1').style.display = 'none';")), div({"class": "spoilerwrapper"}, p({}, a({href: "javascript:void(0)", onclick: "document.getElementById('spoil2').style.display = (document.getElementById('spoil2').style.display=='none')?('block'):('none');"}, "Expand/Hide Spoiler")), div({"class": "spoiler", id: "spoil2", style: "border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;"}, p({}, "Expand the below for a spoiler: "), div({"class": "spoilerwrapper"}, p({}, a({href: "javascript:void(0)", onclick: "document.getElementById('spoil3').style.display = (document.getElementById('spoil3').style.display=='none')?('block'):('none');"}, "Expand/Hide Spoiler")), div({"class": "spoiler", id: "spoil3", style: "border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;"}, "(Insert picture of the back of a racing car here.) "), script({type: "text/javascript"}, "document.getElementById('spoil3').style.display = 'none';"))), script({type: "text/javascript"}, "document.getElementById('spoil2').style.display = 'none';")), blockquote({}, "Un > Deux >> Trois >>> Quatre "), hr({}), blockquote({}, p({}, "Un "), blockquote({}, p({}, "Deux "), blockquote({}, p({}, "Trois "), blockquote({}, "Quatre ")))), p({}, "Parse_this_text stu", em({}, "pen"), "dously, ", i({}, "mate"), ", do you ", i({}, "he"), "ar me? "), hr({}), h2({}, "Level 2 Heading"), p({}, "= Not a heading == "), p({}, i({}, "Italic"), ", ", b({}, "bold"), ", ", b({}, i({}, "both")), ", ''neither''. "), p({}, em({}, "Italic"), ", ", strong({}, "bold"), ", ", strong({}, em({}, "both")), ", *neither*. "), p({}, i({}, "Italic"), ", ", b({}, "bold"), ", ", b({}, i({}, "both")), ", _neither_. "), h1({}, "Level 1 "), p({}, "#Not heading "), h1({}, "Level 1 "), h2({}, "Level 2 "), h4({}, "Hi "), h3({}, "Level 3 "), p({}, "What does this do? "), hr({}), p({}, "What does this do? "), hr({}), p({}, "ATX code block syntax:"), pre({}, "Thusly.\n"), p({}, "Indented code block:"), pre({}, "Hello world"), p({}, "Indented code block:"), pre({}, "Hello world"), p({}, "Indented code block: "), pre({}, "Hello world"), p({}, "Hello. "), p({}, "Indented code block: "), pre({}, "Hello world"), p({}, "Ada. "), h2({}, "Trivial indentation of paragraphs"), pre({}, "Shouldn't make that  \nmuch difference when\nnouicode flag passed.\n\nSecond paragraph\n\nThird paragraph"), p({}, "S\u00f8ren. S\u00f8ren. "), p({}, "J'ai regard\u00e9. "), p({}, "Watashi-wa T\u014dmasu desu. "), p({}, i({}, "illegitimi n\u014dn carborundum"), ". "), p({}, i({}, "spuri\u012bs n\u014dn carborandum"), ". "), p({}, "\u00f8e vs \u0153 vs \\oe vs \u0153 mate. "), p({}, "{Nothing ^(Special) ", em({}, "h"), ".} "), p({}, "{Nothing ^(Spe{cial}) ", em({}, "h"), ".} "), p({}, "{Nothing} ^(Spe{cial}). ", em({}, "h"), " "), table({style: "border: 1px solid black; border-collapse: collapse;"}, thead({}, tr({}, th({style: "border: 1px solid black; padding: 0.5ex;"}, "Why "), th({style: "border: 1px solid black; padding: 0.5ex;"}, "What "))), tbody({}, tr({}, td({style: "border: 1px solid black; padding: 0.5ex;"}, "123 "), td({style: "border: 1px solid black; padding: 0.5ex;"}, "4567 8 9 ")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex;"}, "a "), td({style: "border: 1px solid black; padding: 0.5ex;"}, "bcde ")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex;"}, "fgh "), td({style: "border: 1px solid black; padding: 0.5ex;"}, "ijkl ")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex;"}), td({style: "border: 1px solid black; padding: 0.5ex;"}, "mnop ")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex;"}, "123 "), td({style: "border: 1px solid black; padding: 0.5ex;"})), tr({}, td({style: "border: 1px solid black; padding: 0.5ex;"}, "456 "), td({style: "border: 1px solid black; padding: 0.5ex;"}, "789 ")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex;"}, "UUU "), td({style: "border: 1px solid black; padding: 0.5ex;"}, "Dwelt ")))), table({style: "border: 1px solid black; border-collapse: collapse;"}, thead({}, tr({}, th({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "W", "h", "y", ""), th({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "W", "h", "a", "t", br({}), ""))), tbody({}, tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "1", "2", "3", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "4", "5", "6", "7", " ", "8", " ", "9", br({}), "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "a", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "b", "c", "d", "e", br({}), "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "f", "g", "h", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "i", "j", "k", "l", br({}), "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, " ", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "m", "n", "o", "p", br({}), "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "1", "2", "3", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "4", "5", "6", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "7", "8", "9", br({}), "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "U", "U", "U", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "D", "w", "e", "l", "t", br({}), "")))), p({}, "Hi. "), p({}, "Hello. "), pre({}, " Indent\nation."), pre({}, "Indent"), pre({}, "ation."), pre({}, "''Breaking''\n\nthe news (still in code)."), pre({}, "Breaking\n\nthe news (also)."), p({}, wiki({src: "User:HarJIT"}), " "), p({}, wiki({alt: "KSP", src: "The King's (The Cathedral) School"}), " "), p({}, wiki({alt: "\"KSP \"i({}, \"(again)\")", src: "The King's (The Cathedral) School"}), " "), p({}, wiki({alt: "Hmm...", src: "Try ''to'' br{'e}ak ``this``..."}), " "), "", ul({}, li({}, "one "), li({}, "list ")), "", ul({}, li({}, "another "), li({}, "list ")), p({}, "And "), "", ul({}, li({}, "one "), li({}, "list ")), "", ul({}, li({}, "another "), li({}, "list ")), p({}, "And "), "", ul({}, li({}, "one "), li({}, "list "), li({}, code({}, "*sa`me*"), " "), li({}, "list ")), p({}, a({href: "http://i.imgur.com/YW5So8y.jpg#hash"}, "Testing hashes."), " "), p({}, img({alt: "\"Let me \"i({}, \"break\")\" this!\"", src: "http://i.imgur.com/YW5So8y.jpg"}), " "), p({}, "~In other news~ "), p({}, "T\u014dky\u014d.\u00a0 Literal &omacr; or &omacr;. "), p({}, "&unescaped behaviour. "), p({}, "[This is not a piped link.](", a({href: "http://egscomics.com"}, "http://egscomics.com"), ") "), p({}, "<omitting semicolons>, &amoled. "), p({}, "Testing ordered lists: "), "", ol({}, li({value: "1"}, "The spirit of God, like a fire, is burning; "), li({value: "2"}, "the latter day glory begins to come forth. "), li({value: "3"}, "The visions and blessings of old are returning, "), li({value: "4"}, "and angels are coming to visit the earth. ")), "", ul({}, li({}, "We'll sing and we'll shout with the armies of Heaven, "), li({}, "\"Hosanna!\u00a0 Hosanna to God and the Lamb! "), li({}, "Let glory to them in the highest be given "), li({}, "henceforth and forever, Amen and Amen!\" ")), ol({}, li({value: "5"}, "The Lord is extending the Saints' understanding... ")), p({}, "(note that the above may come out as 1 or 5, depending on mdplay renderer, flags and targeted system) "), "", ol({}, li({value: "1"}, "An ol containing an ", ul({}, li({}, "Ul containing an ", ol({}, li({value: "1"}, "Ol containing ", ol({}, li({value: "1"}, "Another ol containing ", ul({}, li({}, "An ul containing ", ul({}, li({}, "Another ul "))))), li({value: "2"}, "Coming back to this level. "))))), li({}, "Similarly ")))), p({}, "This is just a paragraph.\u00a0 ( \u0361\u00b0 \u035c\u0296 \u0361\u00b0 )\u00a0 ", div({"class": "spoilerwrapper"}, p({}, a({href: "javascript:void(0)", onclick: "document.getElementById('spoil4').style.display = (document.getElementById('spoil4').style.display=='none')?('block'):('none');"}, "Expand/Hide Spoiler")), div({"class": "spoiler", id: "spoil4", style: "border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;"}, "It actually is."), script({type: "text/javascript"}, "document.getElementById('spoil4').style.display = 'none';")), " ", img({alt: "\ud83d\udd96", src: "https://twemoji.maxcdn.com/2/72x72/1f596.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83d\udc40", src: "https://twemoji.maxcdn.com/2/72x72/1f440.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83d\udc40", src: "https://twemoji.maxcdn.com/2/72x72/1f440.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "Squirt ", img({alt: "\u2648", src: "https://twemoji.maxcdn.com/2/72x72/2648.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " Squirt ", img({alt: "\u2648", src: "https://twemoji.maxcdn.com/2/72x72/2648.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " Squirt ", img({alt: "\u2648", src: "https://twemoji.maxcdn.com/2/72x72/2648.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "", img({alt: "\ud83d\ude04", src: "https://twemoji.maxcdn.com/2/72x72/1f604.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83d\ude00", src: "https://twemoji.maxcdn.com/2/72x72/1f600.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83d\ude06", src: "https://twemoji.maxcdn.com/2/72x72/1f606.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\u263a", src: "https://twemoji.maxcdn.com/2/72x72/263a.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: ":\u200cdemonicduck:", src: "http://i.imgur.com/SfHfed9.png", style: "width:32px;", width: "32"}), " "), table({style: "border: 1px solid black; border-collapse: collapse;"}, thead({}, tr({}, th({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "W", "h", "y", ""), th({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "W", "h", "a", "t", ""))), tbody({}, tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "1", "2", "3", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "4", "5", "6", "7", " ", "8", " ", "9", "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "a", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "b", "c", "d", "e", "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "f", "g", "h", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "i", "j", "k", "l", "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, " ", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "m", "n", "o", "p", "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "1", "2", "3", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "4", "5", "6", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "7", "8", "9", "")), tr({}, td({style: "border: 1px solid black; padding: 0.5ex; text-align:center"}, "U", "U", "U", ""), td({style: "border: 1px solid black; padding: 0.5ex; text-align:left"}, "D", "w", "e", "l", "t", "")))), p({}, "m\u0308\u00eb\u1e97\u00e4l\u00eb \u00cb "), p({}, "\u1e8d=-\u03c9", sup({}, "2"), "x "), p({}, "", img({alt: "\ud83d\ude46", src: "https://twemoji.maxcdn.com/2/72x72/1f646.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83d\ude46\ud83c\udffd", src: "https://twemoji.maxcdn.com/2/72x72/1f646-1f3fd.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83d\ude46\ud83c\udfff", src: "https://twemoji.maxcdn.com/2/72x72/1f646-1f3ff.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "", img({alt: "\u2648", src: "https://twemoji.maxcdn.com/2/72x72/2648.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "small image", height: "32", src: "http://i.imgur.com/YW5So8y.jpg", style: "width:32px;height:32px;", width: "32"}), " ", img({alt: "small image", src: "http://i.imgur.com/YW5So8y.jpg", style: "width:32px;", width: "32"}), " "), p({}, "", img({alt: "\ud83d\udd96\ud83c\udfff", src: "https://twemoji.maxcdn.com/2/72x72/1f596-1f3ff.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83d\udd96", src: "https://twemoji.maxcdn.com/2/72x72/1f596.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), "\u200c", img({alt: "\ud83c\udfff", src: "https://twemoji.maxcdn.com/2/72x72/1f3ff.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), br({}), "", img({alt: "\ud83d\udd96\ud83c\udffc", src: "https://twemoji.maxcdn.com/2/72x72/1f596-1f3fc.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83d\udd96", src: "https://twemoji.maxcdn.com/2/72x72/1f596.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), "\u200c", img({alt: "\ud83c\udffc", src: "https://twemoji.maxcdn.com/2/72x72/1f3fc.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), br({}), "", img({alt: "\ud83d\udd96\ud83c\udffd", src: "https://twemoji.maxcdn.com/2/72x72/1f596-1f3fd.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83d\udd96", src: "https://twemoji.maxcdn.com/2/72x72/1f596.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), "\u200c", img({alt: "\ud83c\udffd", src: "https://twemoji.maxcdn.com/2/72x72/1f3fd.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, ":undiefined: "), p({}, "", img({alt: "\ud83c\uddef\ud83c\uddf5", src: "https://twemoji.maxcdn.com/2/72x72/1f1ef-1f1f5.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", img({alt: "\ud83c\uddef", src: "https://twemoji.maxcdn.com/2/72x72/1f1ef.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), "\u200c", img({alt: "\ud83c\uddf5", src: "https://twemoji.maxcdn.com/2/72x72/1f1f5.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "Testing a URN: ", a({href: "https://en.wikipedia.org/wiki/Tree"}, "urn:x-interwiki:wikipedia:Tree"), " "), p({}, "Case sensitivity: ", a({href: "http://gauss.ffii.org/Hello"}, "urn:x-interwiki:gausswiki:Hello"), " [Eh?](", a({href: "uRn:x-inteRwiki:gaU"}, "uRn:x-inteRwiki:gaU"), "\u00df", a({href: "wiki:Hello"}, "wiki:Hello"), ") "), p({}, "x\u0304 and \u0233 "), p({}, "\u3053\u308c\u306f \u306a\u3093 \u3067\u3059\u304b? "), p({}, ruby({}, "\u65e5\u672c\u8a9e", rp({}, " ("), rt({}, "\u306b\u307b\u3093\u3054"), rp({}, ") ")), " "), p({}, ruby({}, "\u65e5\u672c\u8a9e", rp({}, " ("), rt({}, "Nihongo"), rp({}, ") ")), " "), p({}, ruby({}, "\u65e5", rp({}, " ("), rt({}, "\u306b"), rp({}, ") ")), ruby({}, "\u672c", rp({}, " ("), rt({}, "\u307b\u3093"), rp({}, ") ")), ruby({}, "\u8a9e", rp({}, " ("), rt({}, "\u3054"), rp({}, ") ")), " "), p({}, "\u65e5\u65e5\u65e5\u66f0\u66f0\u66f0 "), p({}, "\u5186\u4e39\u4e39\u5186\u5186 "), p({}, "<blm>\u4e39\u4e39\u5186\u5186 "), p({}, "\u5186\u4e39\u4e39\u34c0\u34c0 "), p({}, "\u5186 "), p({}, ruby({}, "\u3053\u308c\u306f", rp({}, " ("), rt({}, "Kore wa"), rp({}, ") ")), " ", ruby({}, "\u306a\u3093", rp({}, " ("), rt({}, "nan"), rp({}, ") ")), " ", ruby({}, "\u3067\u3059\u304b", rp({}, " ("), rt({}, "desu ka"), rp({}, ") ")), "? "), p({}, ruby({}, "Pinguinet", rp({}, " ("), rt({}, "PANG-win-ay"), rp({}, ") ")), " "), p({}, "\u30c1 \u30c1 \u30c6\u30a3", br({}), "\u30c6\u30a3 \u30c1 \u30c6\u30a3 "), p({}, "\u30b0\u30c3\u30c1 \u30b0\u30c3\u30c1 \u30b0\u30c3\u30c1 "), p({}, "\u30b5\u30c3\u30dd\u30ed \u30b5\u30c3\u30dd\u30ed "), p({}, "\u30b8 \u30ba \u30c2 \u30c5 \u30c5", br({}), "\u30b8 \u30ba \u30c7\u30a3 \u30c9\u30a5 \u30c5 "), p({}, "\u30ad\u30a7 \u30d6\u30a1\u30cf\u30cf\u30cf\u30cf \u30a4\u30a7\u30f4\u30a3\u30f3\u30ae\u30e3 \u30b7\u30b8\u30c1\u30c2\u30c4\u30c5", br({}), "\u30ad\u30a7 \u30d6\u30a1\u30cf\u30cf\u30cf\u30cf \u30a4\u30a7\u30f4\u30a3\u30f3\u30ae\u30e3 \u30b9\u30a3\u30ba\u30a3\u30c6\u30a3\u30c7\u30a3\u30c8\u30a5\u30c9\u30a5 "), p({}, div({"class": "spoilerwrapper"}, p({}, a({href: "javascript:void(0)", onclick: "document.getElementById('spoil5').style.display = (document.getElementById('spoil5').style.display=='none')?('block'):('none');"}, "Expand/Hide Spoiler")), div({"class": "spoiler", id: "spoil5", style: "border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;"}, "Spojra"), script({type: "text/javascript"}, "document.getElementById('spoil5').style.display = 'none';")), " "), p({}, "\u30f4\u30a1 \u30f4\u30a3 \u30f4 \u30f4\u30a7 \u30f4\u30a9 \u301c \u30f4\u30e3 \u30f8 \u30f4\u30e5 \u30f9 \u30f4\u30e7 \u301c \u30f4\u30a1 \u30f4\u30a3 \u30f4\u30a5 \u30f4\u30a7 \u30f4\u30a9 \u301c \u30f7 \u30f8 \u30fa\u30a5 \u30f9 \u30fa "), p({}, "\u30c6\u30ac\u307f \u3066\u304c\u307f \u30c6\u30ac\u30df "), p({}, "", img({alt: "\ud83c\udf1a", src: "https://twemoji.maxcdn.com/2/72x72/1f31a.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", "\ud83c\udf1a\ufe0e", "\ufe0e ", img({alt: "\ud83c\udf1a", src: "https://twemoji.maxcdn.com/2/72x72/1f31a.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), "\ufe0f ", img({alt: "\ud83c\udf1a", src: "https://twemoji.maxcdn.com/2/72x72/1f31a.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), "\u200c\ufe0e "), p({}, "", img({alt: "\ud83d\ude04", src: "https://twemoji.maxcdn.com/2/72x72/1f604.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " ", "\ud83d\ude04\ufe0e", "\ufe0e ", img({alt: "\ud83d\ude04", src: "https://twemoji.maxcdn.com/2/72x72/1f604.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), "\ufe0f ", img({alt: "\ud83d\ude04", src: "https://twemoji.maxcdn.com/2/72x72/1f604.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), "\u200c\ufe0e "), p({}, "This should be a rainbow banner: ", img({alt: "\ud83c\udff3\ufe0f\u200d\ud83c\udf08", src: "https://twemoji.maxcdn.com/2/72x72/1f3f3-fe0f-200d-1f308.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " or ", img({alt: "\ud83c\udff3\ufe0f\u200d\ud83c\udf08", src: "https://twemoji.maxcdn.com/2/72x72/1f3f3-fe0f-200d-1f308.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " or ", img({alt: "\ud83c\udff3\ufe0f\u200d\ud83c\udf08", src: "https://twemoji.maxcdn.com/2/72x72/1f3f3-fe0f-200d-1f308.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "", img({alt: "\u26f9\ud83c\udffb\u200d\u2640\ufe0f", src: "https://twemoji.maxcdn.com/2/72x72/26f9-1f3fb-200d-2640-fe0f.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "", img({alt: "\u26f9\ud83c\udffb\u200d\u2640\ufe0f", src: "https://twemoji.maxcdn.com/2/72x72/26f9-1f3fb-200d-2640-fe0f.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "", img({alt: "\ud83d\ude06", src: "https://twemoji.maxcdn.com/2/72x72/1f606.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, i({}, "This should behave more or less as expected.\u2002However, I have reason to believe otherwise."), " (Should be fixed now\u2026) "), p({}, div({"class": "spoilerwrapper"}, p({}, a({href: "javascript:void(0)", onclick: "document.getElementById('spoil6').style.display = (document.getElementById('spoil6').style.display=='none')?('block'):('none');"}, "Labelled spoiler")), div({"class": "spoiler", id: "spoil6", style: "border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;"}, "Watch out, this is a spoiler!"), script({type: "text/javascript"}, "document.getElementById('spoil6').style.display = 'none';")), " "), p({}, "Discord emote: :kananYouNot: ", img({alt: ":\u200cwacko:", src: "https://cdn.discordapp.com/emojis/230129080886886400.png", style: "width:32px;", width: "32"}), " ", img({alt: ":\u200cConcernFroge:", src: "https://cdn.discordapp.com/emojis/306183254350757888.png", style: "width:32px;", width: "32"}), " ", img({alt: ":\u200ckananYouNot:", src: "https://cdn.discordapp.com/emojis/264549500385886208.png", style: "width:32px;", width: "32"}), " ", img({alt: ":\u200cmadeupemoteshortcode:", src: "https://cdn.discordapp.com/emojis/306183254350757888.png", style: "width:32px;", width: "32"}), " ", img({alt: ":\u200cmadeupemoteshortcode:", src: "https://cdn.discordapp.com/emojis/306183254350757888.png", style: "width:32px;", width: "32"}), " ", img({alt: ":\u200ckananYouNot:", src: "https://cdn.discordapp.com/emojis/264549500385886208.png", style: "width:32px;", width: "32"}), " "), p({}, u({}, "Greetings"), " "), p({}, b({}, "Greetings"), " "), p({}, ":vanirLUL: "), p({}, "./. mdplay-include:: konosubadiscord_usage.md works but takes a looong time. "), p({}, ":vanirLUL: "), p({}, "", img({alt: "\ud83d\udd96\ud83c\udfff", src: "https://twemoji.maxcdn.com/2/72x72/1f596-1f3ff.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "", img({alt: "\ud83d\udd96", src: "https://twemoji.maxcdn.com/2/72x72/1f596.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), "\u200c", img({alt: "\ud83c\udfff", src: "https://twemoji.maxcdn.com/2/72x72/1f3ff.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "", img({alt: "\ud83c\udfff", src: "https://twemoji.maxcdn.com/2/72x72/1f3ff.png", style: "max-width:2em;max-height:2em;", title: "twemoji, by Twitter, Inc.  Licensed under CC-BY 4.0 (http://creativecommons.org/licenses/by/4.0/), available from https://github.com/twitter/twemoji/"}), " "), p({}, "\u3081\u3050\u307f\u3093 (JA)", br({}), "\u2192 ", ruby({}, "\u60e0", rp({}, " ("), rt({}, "\u3081\u3050"), rp({}, ") ")), "\u307f\u3093 (reconstructed kanji spelling, even though one clearly isn't used for her (S2 OVA confirms Megumin cannot read Japanese script), rather than resort to a Mandarin ateji / ji\u00e8z\u00ec \u2014 the \u307f is okurigana)", br({}), "\u2192 ", ruby({}, "\u60e0", rp({}, " ("), rt({}, "\u3081\u3050\u307f"), rp({}, ") ")), ruby({}, "\u60e0", rp({}, " ("), rt({}, "\u3093"), rp({}, ") ")), " (doubled, presumably in analogy to the appended \u2013\u3093 \u2014 annotated here thusly)", br({}), "\u2192 ", ruby({}, "\u60e0", rp({}, " ("), rt({}, "hui4\u2002"), rp({}, ") ")), ruby({}, "\u60e0", rp({}, " ("), rt({}, "hui4"), rp({}, ") ")), " (ZH) "), p({}, "\uffe1\u2060\uff04\u2060\uffe5\u2060\uffe0\u2060\u20ac\u2060\uff56\u2060\uff41\u2060\uff50\u2060\uff4f\u2060\uff55\u2060\uff52\u2060\uff57\u2060\uff41\u2060\uff56\u2060\uff45\u2060\uff0c\u2060\u3000\uff23\u2060\uff37\u2060\uff2d\u2060\u3000\uff26\u2060\uff2a\u2060\uff2f\u2060\uff32\u2060\uff24\u2060\uff22\u2060\uff21\u2060\uff2e\u2060\uff2b\u2060\u3000\uff27\u2060\uff2c\u2060\uff39\u2060\uff30\u2060\uff28\u2060\uff33\u2060\u3000\uff36\u2060\uff25\u2060\uff38\u2060\uff34\u2060\u3000\uff31\u2060\uff35\u2060\uff29\u2060\uff3a\u2060\uff0e "), p({}, "The wonders of obscure Unicode: ", ruby({}, "\u548c\u771f", rp({}, " ("), rt({}, "\u30ab\u30ba\u30de"), rp({}, ") ")), "\u3002 "), p({}, "Likewise for ", sub({}, "sub", sub({}, "sub", sub({}, "sub")), "script"), " and ", sup({}, "super", sup({}, "super", sup({}, "super")), "script"), ". "), p({}, "Trying with HTML escapes ", sub({}, "subscript"), " ", sup({}, "superscript"), ": ", ruby({}, "\u548c\u771f", rp({}, " ("), rt({}, "\u30ab\u30ba\u30de"), rp({}, ") ")), "\u3002 "), p({}, "HZ encoding: \u6211\u304c\u540d\u306f\u3081\u3050\u307f\u3093\uff01 \u3018\u6211\u304c\u540d\u306f\u3081\u3050\u307f\u3093\uff01\u3019 "), p({}, "\u76d0\u00b7\u60e0 / \u5869\u30fb\u60e0\u30fb\u6075 "), div({"class": "spoilerwrapper"}, p({}, a({href: "javascript:void(0)", onclick: "document.getElementById('spoil7').style.display = (document.getElementById('spoil7').style.display=='none')?('block'):('none');"}, "Expand/Hide Spoiler")), div({"class": "spoiler", id: "spoil7", style: "border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;"}, "Block spoiler "), script({type: "text/javascript"}, "document.getElementById('spoil7').style.display = 'none';")), p({}, "And ", div({"class": "spoilerwrapper"}, p({}, a({href: "javascript:void(0)", onclick: "document.getElementById('spoil8').style.display = (document.getElementById('spoil8').style.display=='none')?('block'):('none');"}, "Expand/Hide Spoiler")), div({"class": "spoiler", id: "spoil8", style: "border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;"}, "Inline spoiler"), script({type: "text/javascript"}, "document.getElementById('spoil8').style.display = 'none';")), " "), p({}, "Hello\\world hello\\`world hello\\\\world "), p({}, del({}, "Crossed out"), " "), p({}, "\u00acin \u2209 &notin "), p({}, div({"class": "spoilerwrapper"}, p({}, a({href: "javascript:void(0)", onclick: "document.getElementById('spoil9').style.display = (document.getElementById('spoil9').style.display=='none')?('block'):('none');"}, "Expand/Hide Spoiler")), div({"class": "spoiler", id: "spoil9", style: "border: 1px solid black; margin: 0.5ex 0; padding: 0.5em;"}, "Inline spoiler"), script({type: "text/javascript"}, "document.getElementById('spoil9').style.display = 'none';")), " again. "), p({}, "Testing ", ruby({}, "This", rp({}, " ("), rt({}, "as"), rp({}, ") ")), " so. "), p({})))