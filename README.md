# PyMuttPrint

Simple email pretty-printing for [Mutt](http://www.mutt.org/), in Python.

## Installation

You need this in your `.muttrc`:

    set print_command="/path/to/pymuttprint.py && evince /tmp/texput.pdf"
    set print_decode="no"
    set print_split="no"

If you want nice logging, try this for the first line above:

    set print_command="/path/to/pymuttprint.py >> ~/logs/muttprint.log 2>&1 && evince /tmp/texput.pdf >> ~/logs/muttprint.log 2>&1"

## Usage

PyMuttPrint is intended to be easy to use.  Simply edit `template.tex`
to modify the layout of your printed files.


## Motivation (Or, "why not just use [muttprint](http://muttprint.sourceforge.net/)?")

* muttprint is over 2000 SLOC (!) of Perl (yech)
* muttprint has a manpage with a ton of unnecessary options I don't use
* muttprint hasn't been updated since 2007
* muttprint is broken:

I began having problems recently with muttprint -- it was complaining
about a Perl library.  The specific error message was:

    This shouldn't happen at /usr/share/perl5/core_perl/Text/Wrap.pm
    line 84

No, *Perl* shouldn't happen.


## Other

Please send bugs/ pull requests.
