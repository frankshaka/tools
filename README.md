Tools
=====

Some small command line tools to make life easier for developers.

These tools work best on Mac OS X and Linux.

Requirements
------------

* Python 2.6+

Installation
------------

To install all components:

  $ sudo python install.py all

To install specified components:

  $ sudo python install.py beep cate

To uninstall:

  $ sudo python install.py -u all
  $ sudo python install.py -u beep cate

To see help:

  $ python install.py -h

To list available components:

  $ python install.py -l

Usage
-----

* `beep.py`
  
  This script makes one or more system default beep sounds.
  
  Usage:
  
    $ beep
  
  or
  
    $ beep 5

* `cate.py`
  
  This script prints out the file content in an escaped format to avoid triggering control characters like backspaces, beeps, line feed, carriage return, etc. Also useful to observe unicode files.
  
  Usage:
  
    $ cate /bin/ln

* (MORE TO COME)
