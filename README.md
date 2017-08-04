# MDPlay #

a Markdown-based syntax targeting web destinations such as forums or wikis, as well as HTML.  with support for emoji, including Twemoji integration.

flags can turn features and extensions off and configure exporters, the obvious one being the "strict" flag.  see flag_chart.md for a list.

code version 8.1.0

change-log:

|ver|changes|
|---|---|
|8.1.0|improvements to rubi support, including more versatile internal interface and, building on this, support for Unicode interlinear annotation special characters.|
|8.0.6|add mdplay-pgcontext directive and tidy some existing yield statements (now requires a Python version supporting the `yield from` syntax).|
|8.0.5|HTML writer: hopefully allow keyboard activation of spoilers even without <details> element support.|
|8.0.4|fix issue preventing parsing of nested directives.|
|8.0.3|improved fullwidth effect (use word joiners).|
|8.0.2|add the fullwidth effect.|
|8.0.1|allow hyphens in asciimotes.|
|8.0.0|port to Python 3.  this warrents a major version bump even though everything else is working more-or-less the same.|
|7.0.6|tidied, cleaner spoiler tag HTML output code, and remove the extended Python Documentation Converter based BibTeX diacritic support in favour of a much tidier alternative.|
|7.0.5|make use of the HTML5 details tag in html5 output where available, should still mostly work if not though.  tying into this, improvements to handling of polyglot HTML-XML script and style tags (when in xhtml mode) in the customised minidom markup writing code.|
|7.0.4|minor fix.|
|7.0.3|HTML writer/renderer compliance improvements.  fix some bugs where writer flags would not be propagated.  add support for illustrative output in the abandoned XHTML2 format, with and without XHTML5 extensions.  discontinue the separate enamel writer in favour of writer modes.|
|7.0.2|HTML writing improvements (fork the writexml/toxml methods from minidom to versions that can reliably output data compatible with a plain-HTML parser).  accordingly more fully merge the NML writer code into the HTML writer code than before.|
|7.0.1|code/module/package organisation improvements.|
|7.0.0|up-to-date / more full-featured and reliable emoji support.  wound up ripping out much of the existing emoji parser code and rethinking my design decisions.  mdplay- and html- directives.  now only one HTML renderer (DOM) with its weaknesses fixed.  miscellaneous fixes.  source tree organisation improvements.|
|6.1.7|slight adjustment to what is considered "hepburn" romaji (allow "hu" - see code comments).  text/graphical style specifiers for emoji.|
|6.1.6|ditch my modified romkan in favour of my entirely new support module, which uses a rather different approach to conversion, and proves substantially faster albeit one-way.  also, switch to MPL.|
|6.1.5|conversion to hiragana now converts katakana where possible as well as romaji, and vice-versa.|
|6.1.4|kanrom fixes (still unused).|
|6.1.3|a fix to (unused, still very flawed) kanrom (prioritise chi over ci), and romkan tweak to undefined sequence yi with reference to https://en.wikipedia.org/wiki/Okinawan_scripts|
|6.1.2|fix errors introduced into romkan, bring [romkan direction] into conformance with jawikipedia page on JIS X 4063:2000.|
|6.1.1|more romkan improvement.|
|6.1|add enamel output.|
|6.0.8|romkan improvements including precalculation (as it were).|
|6.0.7|severely rework romkan backend, add an alternate Reddit-spoiler syntax.|
|6.0.6|some romaji-kana improvements, including a Hepburn-only option (this branches off from the romkan package).|
|6.0.5|more Sôketsu adjustments (completely disregard frequency "data" from v5 table)|
|6.0.4|fix a late mistake in 6.0.3|
|6.0.3|adjustments to Sôketsu (Cangjie) support (the v5 DB prioritised punctuation but not Kanji, so use the v3 list for that - this naturally drops the priority of codes which changed.....), also, make the unversioned syntax accept both versions.)|
|6.0.2|bugfixing, improved rubi support.|
|6.0.1|romkan support, potentially useful for !hkana[](Nihongo) input.|
|6.0|experimental Cangjie [Sôketsu] input support, potentially useful for !cang[](a dm yrmmr) input (sorts per priority in the source Ibus database, then per codepoint).|
|5.9.5|attempt source Twemoji attribution for BBCode, and add source attribution even if starting from roundtripped Markdown.|
|5.9.4|Twitter consider attribution in HTML source adequate, so do this automatically.  also, add an express attribution to test.md.|
|5.9.3|allow fusion of emoji flag or ethnicity sequences for emoji given by shortcodes as well as those given verbatim (as usual, use the zwnj; character (ampersand-code) to prevent fusion).  misc improvements.|
|5.9.2|restore the Demonic Duck.|
|5.9.1|improved twemoji support.|
|5.9|muchly improved emoji support, including Twemoji.  slightly more lenient table detection.  combining the combining diacritical marks using the unicodedata module.|
|5.8.2|add support for the (rather limited) ATX-style designated code blocks.|
|5.8.1|add support for inline markup within tables.|
|5.8|add support for falling back to use of combining-diacritic codepoints.  round-trip table alignments properly.|
|5.7.3:|output tables in roundtrip in Markdown, not ReST, syntax, and treat MD tables as if they are standard MD (might add properly thought-through flags at some point) considering that Github understands Reddit-style syntax (unsure about vice-versa).|
|5.7.2:|fix being less lenient than Github itself over table syntax.  also fix readme typo which brought this to light.|
|5.7.1:|improve handling of hypothetical non-sensible Reddit-Github fusion syntaxes.  better form the Github-targeting Readme.|
|5.7:|fix error in Reddit-style table parser, and extend it to handle Github-style tables.|
|5.6:|repair Windows support.  HTML output can now target new 910 forum.  disable broken JSON debug-output target.|
|5.5:|emoji, degdegs, native BBCode ols compatible with 910CMX, Reddit-style spoilers, |
|5.4:|fixed mistake causing altogether wrong behaviour of nosetexthead flag.  convert the readme and flag chart to be mdplay input themselves.  make double-spaces in input pass through to the HTML output.  fix bug splitting list items into two paragraphs between the second and third markdown line.|
|5.3:|fix some glitches with escaping in output by means of new "agglomerate" function fusing adjacent text nodes in the mdplay tree.  make IDs given to spoiler tags by renderers which have to assign their own such IDs more deterministic, so as to facilitate diffing html output before and after changes.  re-organise flags system, ironing out some faults in the process.|
|5.2:|fix issues with nested ol lists, including ul/ol combinations.  ordered lists are, at length, altogether supported (subject to output limitations).|
|5.1:|correct TVTropes heading syntax.  further work on list processing, especially on the BBcode side, adding several flags.  other tweaks.|
|5.0:|work on lists, including rudimentary ordered list support at long length.  allow (but make disablable) un-escaping of sloppy (no  semicolon) html entities listed as accepted thusly in the Python html5 entity table.|
|4:13|entity un-escape input during, not before, parsing so as to allow syntax features to be escaped using entities, as well as other tweaks.|
|4:12|add TVTropes-style-syntax renderer.  fix serious entity un-escaping bug of decoding ampersand entity at the wrong time (and not predictably either).  add escaping to the MediaWiki-syntax renderer.|
|4:11|fix to htmlalt and bbcode: terminate list even if last node in document or snippet.  actually use Reddit-style table alignments in HTML output.|
|4:10|stop always outputting debug output to mega.txt.  process bare URLs as links (not needed by the BBCode/MediaWiki outputs but benefits the HTML output substantially).  html5 entity un-escaping in markdown sources.  stop nowikitext discarding ReST tables (derp).|
|4.9:|don't utterly bork on markup within alt text.  iron out some old quirks which i put into the parser, including enabling non-designated indented code blocks by default.  add HTML5 entities from the current Python  source tree.  add support for MediaWiki-style wikilinks (not external links) in Markdown input (useful if used to write a wiki-page).  fix htmlalt newline-stripping code blocks.|
|4.8:|added nobackslashspace flag to markdown renderer, fixed flag support in markdown renderer.  fixed problem with UTF-8 input causing renderers to fail with a UnicodeDecodeError (by splitting into Unicode characters, not bytes, in the inline parser).  added strict mode.|
|4.7:|markdown renderer, enabling distillation to an extent as well as round-trip testing.  by that means, fix bug involving detection of opening fences without classes as ReST-style headings.  furthermore add support for Reddit-style tables (in input) and code spans.  also avoid extraneous whitespace in HTML where possible.|
|4.6:|make the undocumented TVTropes link exposure feature in the writers an optional feature enablable through a flag.  use valid HTML for nested lists in the non-DOM writer also.  make existing renderers implement the flag system properly.  allow escaping of close-brackets in link targets (including wikilinks).  fix fusing of separate lists.  STILL NO OL TAGS, and seems more trouble than worth anyway (MD list syntax seems disputed at best).|
|4.5:|added experimental MediaWiki-dialect wikitext renderer.  fixed handling of two-space line breaks in list items.  use valid (rather than merely browser-condoned) HTML for nested lists (DOM-based renderer only).|
|4.4:|better indented code parsing.  flag system API for writers as well as the parser.  add table handling to BBCode writer (was only present in HTML at first) - might work depending on targeted BBCode dialect.  added snippet renderer API.  fix detecting headings as tables.|
|4.3:|added a subset of ReST simple table support, and add a flag system for enabling non-designated indented code blocks.  ol still pending.|
|4.2:|added polish.  now functions as an importable Python package.  added load_renderer mechanism.  added HTML5 mode.  proper entity escaping.|
|4.1:|spanking new HTML export code using minidom.  no added syntax  features.  command-line interface.|
|4.0:|added HTML output support, sorted out handling of instances where braces do not contain a BibTeX diacritic.|
|3.9:|much better BibTeX diacritic support.|
|3.8:|added partial BibTeX umlaut support, including code derived from the Python Documentation LaTeX-to-ReST converter (under a "BSD" licence, almost certainly the same one as Sphinx itself, hence that is what i attached to the file so as to satisfy its terms).  to my own licence for the rest of the program, added a non-misrepresentation clause.|
|3.7:|ReST indented code block support, fixing a nasty residual bug in the process.|
|3.6:|fix paras disappearing etc if followed by rules without empty line.|
|3.5:|fix ReST heading over-lines being detected/parsed as MW headings.|
|3.4:|fix a nested emphasis bug that has been in here since the get-go.  also add MediaWiki emphases.|
|3.3:|more accurate regexps, regexps in place of convoluted testing, fix  problem of rules being swallowed (since 3.1), MediaWiki headings.|
|3.2:|fix the global variables problem properly this time.|
|3.1:|complete support for ReST headings, this has a slight risk of breaking  compatibility with a given Markdown doc, but only slight.  fix, in  theory, as stopgap, the more-than-one-doc problem.|
|3.0:|fix handling of underscore emphasis before (semi)colons, as in 2.1, and  split from a script into many modules and implement partial support for  ReST-style extended Setext headings.  note that this will not behave  correctly if used to translate more than one document.|
|2.x:|[later 2.x revisions (2.1 through 2.4) back-ported fixes from 3.x]|
|2.0:|code spans were not correctly implemented (they were merely implemented  as monospace format spans) and i have no intent of improving upon this so i removed it.  fixed middle-of-word underscore behaviour.|
|1.4:|more conventional link escaping rules.|
|1.3:|fix compatibility with Python (2.5 < version < 3.0), i.e.  Python 2.6 and  2.7.|
|1.2:|fixed some crashes.  added subscript, and alternate syntaxes for bold,  italic and superscript, and spoilers.|
|1.1:|bug-fix: handle "\\" correctly.|
|1.0:|first "release".|

this software is, unless otherwise specified:

Copyright (c) 2015, 2016 HarJIT.  All rights reserved.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
