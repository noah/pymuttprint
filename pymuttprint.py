#!/usr/bin/env python2

import sys
import email
from os import chdir
from os.path import join, abspath, dirname
from subprocess import Popen, PIPE, STDOUT

BASEDIR = dirname(abspath(__file__))

try:
    chdir("/tmp")
except:
    sys.exit("Couldn't chdir to /tmp")

m           = email.message_from_file( sys.stdin )
body        = ''
attachments = []

for part in m.walk():
    ct = part.get_content_type()
    cd = part.get('Content-Disposition')
    if ct == 'text/plain':
        body += r'\\'.join(part.get_payload(decode=True).splitlines(False))
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

to      = texify(m.get('to',''))
date    = texify(m.get('date',''))
ffrom   = texify(m.get('from',''))
subject = texify(m.get('subject',''))

attachments = [texify(a) for a in attachments]
template    = open(join(BASEDIR, 'template.tex'), 'r').read() % (
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
#print m
#print template
#print( tex_log)
