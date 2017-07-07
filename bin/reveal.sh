#!/bin/sh
fullpath=$1
/usr/bin/osascript > /dev/null <<EOT
tell application "Finder"
  set fullpath to POSIX file "$fullpath" as text
  reveal fullpath
  activate
end tell
EOT
