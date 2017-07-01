__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from mdplay.writers.html import html_out, html_out_body

def nml_out(nodem,titl="",flags=()):
    return html_out(nodem, titl, flags, mode="nml")

def nml_out_body(nodem,flags=()):
    return html_out_body(nodem, flags, mode="nml")

__mdplay_renderer__="nml_out"
__mdplay_snippet_renderer__="nml_out_body"

