#!/usr/bin/env python2

import os
import sys
import email
from subprocess import Popen, PIPE, STDOUT


try:
    os.chdir("/tmp")
except:
    sys.exit("Couldn't chdir to /tmp")

m           = email.message_from_file( sys.stdin )
body        = ''
attachments = []

for part in m.walk():
    ct = part.get_content_type()
    cd = part.get('Content-Disposition')
    if ct == 'text/plain':
        body += r'\\'.join(part.get_payload(decode=True).splitlines())
    else:
        fn = part.get_filename()
        if fn is not None: attachments.append( fn )

TEX_REPLACE = { # not an exhaustive list
        "<" : r"\textless ",
        ">" : r"\textgreater ",
        "&" : r"\&",
        "$" : r"\$",
        "#" : r"\#",
        "%" : r"\%",
        "_" : r"\_",
        "{" : r"\{",
        "}" : r"\}",
        r"\\" : r"\\ \relax " # see: http://tex.stackexchange.com/questions/64098/brackets-in-first-column-in-table-give-missing-number-treated-as-zero-error
}

from textwrap import wrap


def texify(s):
    for c in TEX_REPLACE.keys():
        s = '  '.join(wrap(s.replace(c, TEX_REPLACE[c]), 50))
    return s

date = to = ffrom = subject = None
try:
    date, to, ffrom, subject = texify(m['date']), texify(m['to']), texify(m['from']), texify(m['subject'])
except AttributeError: # header missing?
    pass

from os.path import join, dirname
attachments = [texify(a) for a in attachments]
body        = texify(body)
template    = open(join(dirname(__file__), 'template.tex'), 'r').read() % (
    date,
    to,
    ffrom,
    subject,
    len( attachments ),
    ', '.join( attachments ),
    body
)

p       = Popen(['xelatex'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
tex_log = p.communicate(input=template)[0]

# for debugging:
print template
print( tex_log)
