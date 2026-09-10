#!/usr/bin/env bash
# f9_hook_laptop.sh -- F9-AC3 reader. 0.9.0_WK_NFRA_CLDGRPH~5, TO-CG-F-9 (CG-s-29).
#
# READS (never edits) this laptop's device hook file by ABSOLUTE path and reports:
#   STITCH_HOOK_LINES_LAPTOP=<n> of <total lines>   -- must be 0
#   OTHER_HOOK_ENTRIES=<m>                          -- the positive control: the other
#                                                      hook entries are still installed
#   HOOK_READ_AT=<UTC instant>
# The device act is 0.0.0_AB_MSTR's; this criterion's world is that act.
# The file is OUTSIDE the repo corpus, so a direct grep on it is on-rail.
set -u
HOOK="C:/Users/AndrewBerman/Desktop/ajb_workspace/.git/hooks/post-commit"
echo "F9-AC3 -- THE LAPTOP'S DEVICE ACT READ (read-only)"
echo "HOOK_PATH=$HOOK"
echo "HOOK_READ_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ ! -f "$HOOK" ]; then
  echo "HOOK_FILE_EXISTS=false"
  echo "STITCH_HOOK_LINES_LAPTOP=UNREADABLE of UNREADABLE"
  echo "OTHER_HOOK_ENTRIES=UNREADABLE"
  exit 1
fi
echo "HOOK_FILE_EXISTS=true"
echo "HOOK_FILE_BYTES=$(wc -c < "$HOOK" | tr -d ' ')"
echo "HOOK_FILE_MTIME_LOCAL=$(stat -c %y "$HOOK")"
TOTAL="$(cat "$HOOK" | wc -l | tr -d ' ')"
N="$(cat "$HOOK" | grep -c 'stitch-refresh')"
echo "STITCH_HOOK_LINES_LAPTOP=$N of $TOTAL"
# the positive control: every OTHER installed hook entry, by name
M="$(cat "$HOOK" | grep -c 'git-hooks/[a-z0-9-]*\.sh')"
S="$(cat "$HOOK" | grep -c 'git-hooks/stitch-refresh-post-commit\.sh')"
echo "OTHER_HOOK_ENTRIES=$((M - S))"
echo "--- installed entries (invocation lines), by script name ---"
cat "$HOOK" | grep -o 'git-hooks/[a-z0-9-]*\.sh'
echo "--- the file, verbatim, numbered ---"
cat -n "$HOOK"
echo "--- end ---"
# The three deciding values again, in the order F9-AC3's own clause names them
# (count, then the positive control, then the read's instant). Same values as above,
# re-printed so the criterion's expect can be matched against a live run rather than
# against a hand-reordered excerpt.
echo "STITCH_HOOK_LINES_LAPTOP=$N of $TOTAL"
echo "OTHER_HOOK_ENTRIES=$((M - S))"
echo "HOOK_READ_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit 0
