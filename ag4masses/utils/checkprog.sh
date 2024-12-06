#!/bin/bash
#
# When AG4Masses is running, show progress based on infromation written to stderr
#
# Usage: checkprog.sh ag.err

egrep -i 'nodes|Worker initializing|called|returned|returning' "$@"
echo "------------ # DD+AR runs: ---------------"
fgrep failed "$@" | wc -l
