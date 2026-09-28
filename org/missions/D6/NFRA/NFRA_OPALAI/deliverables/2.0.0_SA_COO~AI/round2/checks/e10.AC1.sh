#!/usr/bin/env bash
# OA-e-10 AC1 (the census): E10_LOGIN_CENSUS.md is COMMITTED at HEAD and states LOGIN_USES with its WINDOW and SOURCE,
# DEPENDENTS (the server-held identities that still read the email-keyed cache /login writes), and a BRANCH consistent
# with them: REMOVE when DEPENDENTS is 0, NARROW otherwise.
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~16/E10_LOGIN_CENSUS.md"
git cat-file -e "HEAD:$F" 2>/dev/null || { echo "census not committed at HEAD"; echo "RESULT: FAIL"; exit 1; }
t=$(git show "HEAD:$F" | tr -d '\r')
uses=$(printf '%s\n' "$t" | grep -m1 -oE '^LOGIN_USES: [0-9]+' | grep -oE '[0-9]+')
win=$(printf '%s\n' "$t" | grep -m1 -cE '^WINDOW: [0-9]{4}-[0-9]{2}-[0-9]{2}.*\.\..*[0-9]{4}-[0-9]{2}-[0-9]{2}')
src=$(printf '%s\n' "$t" | grep -m1 -cE '^SOURCE: .+')
dep=$(printf '%s\n' "$t" | grep -m1 -oE '^DEPENDENTS: [0-9]+' | grep -oE '[0-9]+')
br=$(printf '%s\n' "$t" | grep -m1 -oE '^BRANCH: (REMOVE|NARROW)' | awk '{print $2}')
ok=no
if [ "$dep" = 0 ] && [ "$br" = REMOVE ]; then ok=yes; fi
if [ -n "$dep" ] && [ "$dep" != 0 ] && [ "$br" = NARROW ]; then ok=yes; fi
echo "login_uses=${uses:-NONE} window=$win source=$src dependents=${dep:-NONE} branch=${br:-NONE} consistent=$ok"
if [ -n "$uses" ] && [ "$win" = 1 ] && [ "$src" = 1 ] && [ "$ok" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
