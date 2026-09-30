#!/usr/bin/env bash
# MX-s-14 AC3 (THE ACCEPTANCE, as amended A1): an SSM run of opal-bd-transaction-download requested at or after the
# first 21:53Z weekday slot following this order's PHASE B GO commit (subject token 'go(NFRA_MCPINDEX.TO-MX-s-14')
# records Status=Success. The document's honest exit makes Success mean the merge completed (MX-m-1 (a)). Times are
# converted to UTC before comparing.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
GO="$(git log -1 --format=%cI --grep='go(NFRA_MCPINDEX.TO-MX-s-14' HEAD)"
[ -n "$GO" ] || { echo "no PHASE B GO commit yet -- RESULT: FAIL"; exit 1; }
rows=$(timeout 90 "$AWS" ssm list-commands --filters key=DocumentName,value=opal-bd-transaction-download --query 'Commands[].[RequestedDateTime,Status,CommandId]' --output text 2>&1 | tr -d '\r')
out=$(python - "$GO" <<PY 2>&1
import sys, datetime as d
go = d.datetime.fromisoformat(sys.argv[1]).astimezone(d.timezone.utc)
slot = go.replace(hour=21, minute=53, second=0, microsecond=0)
if slot < go: slot += d.timedelta(days=1)
while slot.weekday() >= 5: slot += d.timedelta(days=1)
n = ok = 0
for r in """$rows""".strip().splitlines():
    p = r.split()
    if len(p) < 3: continue
    try: t = d.datetime.fromisoformat(p[0]).astimezone(d.timezone.utc)
    except Exception: continue
    if t >= slot - d.timedelta(minutes=2):
        n += 1; ok += p[1] == "Success"
print("slot=%s runs at/after slot=%d success=%d" % (slot.strftime("%Y-%m-%dT%H:%MZ"), n, ok))
print("OK" if ok >= 1 else "NOT-OK")
PY
)
printf '%s\n' "$out" | head -1
if printf '%s\n' "$out" | tail -1 | grep -qx OK; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
