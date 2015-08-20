Markdown to BBCode converter.

as a conscious decision, no support is included for indented code blocks.  use
fenced code blocks.

no special support is included for ordered lists, paralleling the absence of 
such in BBCode.  unordered lists are converted, though.

headings are converted in the best way possible, considering that BBCode has 
no concept of semantic headings.

version 2.0

changelog:

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

Copyright (c) 2015 HarJIT.  All rights reserved.

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