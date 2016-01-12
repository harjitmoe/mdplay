convert a derivative of Markdown to BBCode.

no special support is included for ordered lists, paralleling the absence of 
such in BBCode.  unordered lists are converted, though.

headings are converted in the best way possible, considering that BBCode has 
no concept of semantic headings.

version 3.9

changelog:

3.9: much better BibTeX dieretic support.
3.8: added partial BibTeX umlaut support, including code derived from the
     Python Documentation LaTeX-to-ReST converter (under a "BSD" licence,
     almost certainly the same one as Sphinx uses, hence that is what I've
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
2.0: code spans were not correctly implemented (they were merely implemented 
     as monospace format spans) and i have no intent of improving upon this so
     i removed it.  fixed middle-of-word underscore behaviour.
1.4: more conventional link escaping rules.
1.3: fix compatibility with Python (2.5 < version < 3.0), i.e. Python 2.6 and 
     2.7.
1.2: fixed some crashes.  added subscript, and alternate syntaxes for bold, 
     italic and superscript, and spoilers.
1.1: bugfix: handle "\\" correctly
1.0: first "release"

i wrote this fairly recently, and i do not believe that i interpolated code 
from anywhere else.  it is not impossible that i may have forgotten, albeit 
unlikely as i nowadays tend to avoid doing that without noting in comments.

with that in mind, this software is:

Copyright (c) 2015, 2016 HarJIT.  All rights reserved.

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
