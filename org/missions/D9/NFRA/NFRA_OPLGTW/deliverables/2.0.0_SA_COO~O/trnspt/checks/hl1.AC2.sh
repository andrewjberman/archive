#!/usr/bin/env bash
# OPLGTW OG-hl-1 AC2: deploy/mail_sender_table.txt equals criterion.py DEFAULT_AUTHORS (the Z-S36 durable fix's single
# source), the Graph allowlist gains ^/me/messages$, the listing route is registered, and /ms/* is byte-unchanged since
# the cut base (the parent of the commit that ADDED tests/test_mail_listing.py; the merge-base before it exists).
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
out=$(timeout 60 python "$(native "$H/_hl.py")" 2>&1 | tr -d '\r'); printf '%s\n' "$out"
add=$(git log --diff-filter=A --format=%H HEAD -- "$GW/tests/test_mail_listing.py" | tail -1)
if [ -n "$add" ]; then base=$(git rev-parse "$add^"); else base=$(git merge-base HEAD CLOUD 2>/dev/null); fi
ms=$( [ -n "$base" ] && git diff --name-only "$base" HEAD -- "$GW/app/ms_ingest.py" | grep -c . )
echo "app/ms_ingest.py changed since base ${base:0:10}: ${ms:-UNREAD}"
if printf '%s\n' "$out" | grep -q "^HL ok$" && [ "$ms" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
