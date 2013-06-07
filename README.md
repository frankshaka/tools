Tools
=====

Some small command line tools to make life easier for developers.

These tools work best on Mac OS X and Linux.

Requirements
------------

*   Python 2.6+

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

*   `beep.py`
    
    This script makes one or more system default beep sounds.
    
    Usage:
    
        $ beep
    
    or
    
        $ beep 5

*   `cate.py`
    
    This script prints out the file content in an escaped format to avoid triggering control characters like backspaces, beeps, line feed, carriage return, etc. Also useful to observe unicode files.
    
    Usage:
    
        $ cate /bin/ln

*   `table2csv.py`
    
    This script converts a single-table HTML file into a Comma Separated Values (CSV) file. A single-table HTML file can be opened directly by Microsoft Excel and thus is used by some service providers (e.g. http://www.10086.cn) to let you download large data in an Excel-compatible format.
    
    Usage:
    
        $ table2csv "data.html" "data.csv"
    
    If you don't specify the first parameter, the script will read the input from `stdin`. If you don't specify the second parameter, the script will write the output to `stdout`. Example:
    
        $ cat "data.html" | iconv -f "gbk" -t "utf-8" | table2csv > "data.csv"

*   `reveal.sh`
    
    This script shows a specified file in the Finder on Mac OS X. Note that it uses AppleScript so it's not possible to run on other platforms.
    
    Usage:
    
        $ reveal /bin/ln
    
    This script comes with a companion `misc/Show In Finder.launch` - an external tool launch configuration for Eclipse developers who wish to reveal the selected resource in Finder.

*   (MORE TO COME)
