# URI regexes derived from the Public-Domain-dedicated states.py from Docutils.
# Docutils being by David Goodger.

# Valid URI characters (see RFC 2396 & RFC 2732);
# final \x00 allows backslash escapes in URIs:
uric = r"""[-_.!~*'()[\];/:@&=+$,%a-zA-Z0-9\x00]"""

# Delimiter indicating the end of a URI (not part of the URI):
uri_end_delim = r"""[>]"""

# Last URI character; same as uric but no punctuation:
urilast = r"""[_~*/=+a-zA-Z0-9]"""

# End of a URI (either 'urilast' or 'uric followed by a uri_end_delim'):
uri_end = r"""(?:%(urilast)s|%(uric)s(?=%(uri_end_delim)s))""" % locals()

emailc = r"""[-_!~*'{|}/#?^`&=+$%a-zA-Z0-9\x00]"""
email_pattern = r"""
      %(emailc)s+(?:\.%(emailc)s+)*   # name
      (?<!\x00)@                      # at
      %(emailc)s+(?:\.%(emailc)s*)*   # host
      %(uri_end)s                     # final URI char
      """ % locals()

uriregex=r"""
    (?P<whole>
      (?P<absolute>           # absolute URI
        (?P<scheme>             # scheme (http, ftp, mailto)
          [a-zA-Z][a-zA-Z0-9.+-]*
        )
        :
        (
          (                       # either:
            (//?)?                  # hierarchical URI
            %(uric)s*               # URI characters
            %(uri_end)s             # final URI char
          )
          (                       # optional query
            \?%(uric)s*
            %(uri_end)s
          )?
          (                       # optional fragment
            \#%(uric)s*
            %(uri_end)s
          )?
        )
      )
    |                       # *OR*
      (?P<email>              # email address
        """ % locals() + email_pattern + r"""
      )
    )
"""

uriregex="".join([i.split(" #")[0] for i in (uriregex.split("\n"))]).replace(" ","")

# END of URI regexes.