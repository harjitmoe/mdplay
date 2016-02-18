convert a derivative of Markdown to BBCode or HTML.

flags can turn features and extensions off, the obvious one being the strict
flag.

no special support is included for ordered lists, paralleling the absence of
such in BBCode.  unordered lists are converted, though.  this may be changed
in a future release, or it may not.

version 5.1

change-log:

5.1: correct TVTropes heading syntax.  further work on list processing,
     especially on the BBcode side, adding several flags.  other tweaks.
5.0: work on lists, including rudimentary ordered list support at long
     length.  allow (but make disablable) un-escaping of sloppy (no 
     semicolon) html entities listed as accepted thusly in the Python html5
     entity table.
4:13:entity un-escape input during, not before, parsing so as to allow
     syntax features to be escaped using entities, as well as other tweaks.
4:12:add TVTropes-style-syntax renderer.  fix serious entity un-escaping bug
     of decoding &amp; at the wrong time (and not predictably either).  add
     escaping to the MediaWiki-syntax renderer.
4.11:fix to htmlalt and bbcode: terminate list even if last node in document
     or snippet.  actually use Reddit-style table alignments in HTML output.
4:10:stop always outputting debug output to mega.txt.  process bare URLs as
     links (not needed by the BBCode/MediaWiki outputs but benefits the HTML
     output substantially).  html5 entity un-escaping in markdown sources.
     stop nowikitext discarding ReST tables (derp).
4.9: don't utterly bork on markup within alt text.  iron out some old quirks
     which i put into the parser, including enabling non-designated indented
     code blocks by default.  add HTML5 entities from the current Python 
     source tree.  add support for MediaWiki-style wikilinks (not external
     links) in Markdown input (useful if used to write a wiki-page).  fix
     htmlalt newline-stripping code blocks.
4.8: added nobackslashspace flag to markdown renderer, fixed flag support
     in markdown renderer.  fixed problem with UTF-8 input causing renderers
     to fail with a UnicodeDecodeError (by splitting into Unicode characters,
     not bytes, in the inline parser).  added strict mode.
4.7: markdown renderer, enabling distillation to an extent as well as
     round-trip testing.  by that means, fix bug involving detection of
     opening fences without classes as ReST-style headings.  furthermore
     add support for Reddit-style tables (in input) and code spans.  also
     avoid extraneous whitespace in HTML where possible.
4.6: make the undocumented TVTropes link exposure feature in the writers an
     optional feature enablable through a flag.  use valid HTML for nested
     lists in the non-DOM writer also.  make existing renderers implement
     the flag system properly.  allow escaping of close-brackets in link
     targets (including wikilinks).  fix fusing of separate lists.  STILL
     NO <OL>S, and seems more trouble than worth anyway (MD list syntax
     seems disputed at best).
4.5: added experimental MediaWiki-dialect wikitext renderer.  fixed handling
     of two-space line breaks in list items.  use valid (rather than merely
     browser-condoned) HTML for nested lists (DOM-based renderer only).
4.4: better indented code parsing.  flag system API for writers as well as
     the parser.  add table handling to BBCode writer (was only present in
     HTML at first) - might work depending on targeted BBCode dialect.
     added snippet renderer API.  fix detecting headings as tables.
4.3: added a subset of ReST simple table support, and add a flag system for
     enabling non-designated indented code blocks.  <ol> still pending.
4.2: added polish.  now functions as an importable Python package. added
     load_renderer mechanism.  added HTML5 mode.  proper entity escaping.
4.1: spanking new HTML export code using minidom.  no added syntax 
     features.  command-line interface.
4.0: added HTML output support, sorted out handling of instances where
     braces do not contain a BibTeX diacritic.
3.9: much better BibTeX diacritic support.
3.8: added partial BibTeX umlaut support, including code derived from the
     Python Documentation LaTeX-to-ReST converter (under a "BSD" licence,
     almost certainly the same one as Sphinx itself, hence that is what I
     attached to the file so as to satisfy its terms).  to my own licence
     for the rest of the program, added a non-misrepresentation clause.
3.7: ReST indented code block support, fixing a nasty residual bug in the
     process.
3.6: fix paras disappearing etc if followed by rules without empty line.
3.5: fix ReST heading over-lines being detected/parsed as MW headings.
3.4: fix a nested emphasis bug that has been in here since the get-go.
     also add MediaWiki emphases.
3.3: more accurate regexps, regexps in place of convoluted testing, fix 
     problem of rules being swallowed (since 3.1), MediaWiki headings.
3.2: fix the global variables problem properly this time.
3.1: complete support for ReST headings, this has a slight risk of breaking 
     compatibility with a given Markdown doc, but only slight.  Fix, in 
     theory, as stopgap, the more-than-one-doc problem.
3.0: fix handling of underscore emphasis before (semi)colons, as in 2.1, and 
     split from a script into many modules and implement partial support for 
     ReST-style extended Setext headings.  Note that this will not behave 
     correctly if used to translate more than one document.
[later 2.x revisions (2.1 through 2.4) back-ported fixes from 3.x]
2.0: code spans were not correctly implemented (they were merely implemented 
     as monospace format spans) and i have no intent of improving upon this so
     i removed it.  fixed middle-of-word underscore behaviour.
1.4: more conventional link escaping rules.
1.3: fix compatibility with Python (2.5 < version < 3.0), i.e. Python 2.6 and 
     2.7.
1.2: fixed some crashes.  added subscript, and alternate syntaxes for bold, 
     italic and superscript, and spoilers.
1.1: bug-fix: handle "\\" correctly
1.0: first "release"

i wrote this fairly recently, and i do not believe that i interpolated code 
from anywhere else.  it is not impossible that i may have forgotten, albeit 
unlikely as i nowadays tend to avoid doing that without noting in comments.

with that in mind, this software is, unless otherwise specified:

Copyright (c) 2015, 2016 Thomas Hori.  All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its 
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.
4. Altered versions in any form must not be misrepresented as being the
   original software.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT 
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
