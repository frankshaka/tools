Tools
=====

Some small command line tools to make life easier for developers.

These tools work on Mac OS X and Linux.

Requirements
------------

*   Python 2.6+

Managed Installation
--------------------

To install all components:

    $ sudo python install.py all

To install specified components:

    $ sudo python install.py beep cate

To uninstall:

    $ sudo python install.py -u all
    $ sudo python install.py -u beep cate

To list available components:

    $ python install.py -l

To see help:

    $ python install.py -h

Manual Installation
-------------------

To install a script, simply copy a script to `/usr/local/bin` (or wherever you can execute from) and make it executable:

    $ sudo cp main/beep.py /usr/local/bin/beep & sudo chmod +x /usr/local/bin/beep

Components
----------

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

    This script shows a specified file in the Finder on Mac OS X. Note that AppleScript is used internally so it's not possible to run this script on other platforms.

    Usage:

        $ reveal /bin/ln

    This script comes with a companion `misc/Show In Finder.launch` - an external tool launch configuration for Eclipse developers who wish to reveal the selected resource in Finder.

*   `svnck.py`

    This script prompts an interactive console for Subversion users. The main feature is that it provides a Git-like 'staging area' in the runtime, so that committers can choose easily which files to be committed without messing up one commit with bulk changes made for different issues. Another benefit of this script is the ability to specify paths using indexed numbers, which removes the pain of tabbing/copying/pasting long path names in the command line environment. Other features include shortcuts to 'svn add', 'svn revert' and deleting un-version-controlled files.

    Usage:

        $ cd ~/myworkspace/svnproject1
        $ svnck

*   `dgen.py`

    This script generates MD5 and/or SHA1 digest/checksum for specified files and stores the digest into respective digest files with the original file name suffixed with ".md5" or ".sha1". It also provides a "--verify" argument to verify that the saved digest equals the generated one.

    This script calls `openssl` program for digest generation.

    Usage:

        $ dgen /path/to/project/mywork.txt
        $ ls /path/to/project/
        mywork.txt   mywork.txt.md5   mywork.txt.sha1
        $ dgen --verify /path/to/project/mywork.txt
        /path/to/project/mywork.txt: MD5 Valid
        /path/to/project/mywork.txt: SHA1 Valid

*   (MORE TO COME)
