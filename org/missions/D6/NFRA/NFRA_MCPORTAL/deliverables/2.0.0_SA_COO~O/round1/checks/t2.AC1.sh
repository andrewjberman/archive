#!/usr/bin/env bash
# MP-t-2 AC1 (seam, REAL neighbour = the naming builder): name('mcportal', None, 'grant-writer', 'lambda') RESOLVES (the
# systems.json row exists), and lambda-source-map.json carries exactly one entry under THAT name whose source_dir and
# tf_file both exist in this worktree.
. "$(dirname "$0")/_root.sh"
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
e=$(mp_writer_entry); cnt=$(printf '%s\n' "$e" | sed -n 1p); key=$(printf '%s\n' "$e" | sed -n 2p); src=$(printf '%s\n' "$e" | sed -n 3p); tf=$(printf '%s\n' "$e" | sed -n 4p)
sd=no; [ -n "$src" ] && [ -d "$src" ] && sd=yes; tfe=no; [ -n "$tf" ] && [ -f "$tf" ] && tfe=yes
echo "name()=$nm; source-map entries=$cnt key=$key; source_dir exists=$sd; tf_file exists=$tfe"
if [ "$cnt" = 1 ] && [ "$key" = "$nm" ] && [ "$sd" = yes ] && [ "$tfe" = yes ] && ! printf '%s' "$nm" | grep -qiE 'error|refus'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
