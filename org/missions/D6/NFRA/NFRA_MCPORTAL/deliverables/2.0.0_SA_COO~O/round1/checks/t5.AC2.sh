#!/usr/bin/env bash
# MP-t-5 AC2 (the seam's shape): the typed API client calls exactly the fixed admin routes -- grants read, narrow, widen
# and changes -- and no route outside /api/admin/.
. "$(dirname "$0")/_root.sh"
F="mcportal/src/api/admin.ts"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for r in '/api/admin/grants/' '/narrow' '/widen' '/api/admin/changes'; do grep -qF "$r" "$F" && n=$((n+1)); done
other=$(grep -oE "['\"\`]/api/[a-z_/-]*" "$F" | grep -v "/api/admin/" | wc -l | tr -d ' ')
echo "fixed route fragments present $n of 4; routes outside /api/admin/=$other"
if [ "$n" = 4 ] && [ "$other" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
