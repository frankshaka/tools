Tools
=====

Some small command line tools to make life easier for developers.

These tools work on Mac OS X and *maybe* on Linux.


Scripts
-------

*   `bin/cate.py`

    This script prints out the file content in an escaped format to avoid triggering control characters like backspaces, beeps, line feed, carriage return, etc. Useful to observe non-ASCII files.

    Usage:

        $ python bin/cate.py /bin/ln

*   `bin/reveal.sh`

    This script shows a specified file in the Finder on Mac OS X. Note that AppleScript is used internally so it's not possible to run this script on other platforms.

    Usage:

        $ sh bin/reveal.sh /bin/ln

    This script comes with a companion `misc/Show In Finder.launch` - an external tool launch configuration for Eclipse developers who wish to reveal the selected resource in Finder.

*   `bin/table2csv.py`

    This script converts a single-table HTML file into a Comma Separated Values (CSV) file. A single-table HTML file can be opened directly by Microsoft Excel and thus is used by some service providers (e.g. http://www.10086.cn) to let you download large data in an Excel-compatible format.

    Usage:

        $ python bin/table2csv.py "data.html" "data.csv"

    If you don't specify the first parameter, the script will read the input from `stdin`. If you don't specify the second parameter, the script will write the output to `stdout`. Example:

        $ cat "data.html" | iconv -f "gbk" -t "utf-8" | python bin/table2csv.py > "data.csv"

