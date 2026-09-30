#!/usr/bin/env bash
# MP-v-1 AC1 (A2, FWD-2 LIVE): inside the worker's recorded window, the gateway's own access log holds a 403 for EACH of
# the dashboard's owner-gated handlers, and NO 200 on any of them. A 403 is by construction a VERIFIED non-owner
# (owner_gate.py:113-117: no identity is 401, a verified non-owner is 403), so this reads the refusal on the server.
# Denominator = 1 page (GET /) + every Route in app/admin_api.py at HEAD; the census is printed, and a census other than
# the 5 admin routes counted at the cut (whoami, grant GET, narrow POST, widen POST, changes GET) FAILS, because the
# denominator would then be stale.
. "$(dirname "$0")/_root.sh"
routes=$(git show "HEAD:infra/aws/ec2/opal-gateway/app/admin_api.py" 2>&1 | grep -cE '^\s*Route\(')
. "$(dirname "$0")/_journal.sh"
res=$(printf '%s\n' "$J" | python -c "
import re, sys
lines = sys.stdin.read().splitlines()
want = [('GET', r'/'), ('GET', r'/api/admin/whoami'), ('GET', r'/api/admin/grants/[^/ ]+/[^/ ]+'),
        ('POST', r'/api/admin/grants/[^/ ]+/[^/ ]+/narrow'), ('POST', r'/api/admin/grants/[^/ ]+/[^/ ]+/widen'),
        ('GET', r'/api/admin/changes')]
out = []; ok = 0; admitted = 0
for m, p in want:
    rx = re.compile(r'\"%s %s(\?[^ ]*)? HTTP/1.1\" (\d{3})' % (m, p))
    codes = [x.group(2) for l in lines for x in [rx.search(l)] if x]
    n403 = codes.count('403'); n200 = codes.count('200'); admitted += n200
    ok += 1 if n403 >= 1 else 0
    out.append('%s %s: 403=%d 200=%d' % (m, p.replace('[^/ ]+', '*'), n403, n200))
print('; '.join(out)); print('refused=%d of %d; admitted=%d' % (ok, len(want), admitted))
" 2>&1 | tr -d '\r')
echo "admin_api.py Route census at HEAD=$routes (cut: 5)"
echo "$res"
if [ "$routes" = 5 ] && printf '%s' "$res" | grep -q 'refused=6 of 6; admitted=0'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
