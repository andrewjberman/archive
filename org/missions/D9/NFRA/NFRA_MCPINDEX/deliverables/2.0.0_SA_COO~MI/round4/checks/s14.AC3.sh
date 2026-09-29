#!/usr/bin/env bash
# MX-s-14 AC3 (THE ACCEPTANCE: a SCHEDULED fire, never ad hoc): an SSM run of opal-bd-transaction-download requested at
# or after the first 21:53Z weekday slot following this order's PHASE B GO commit (subject token
# 'go(NFRA_MCPINDEX.TO-MX-s-14') records Status=Success and its own output names the bronze object it wrote
# (an OUTPUT_KEY= line, as the MX-s-9 pull prints). Times are converted to UTC before any comparison (the shim renders
# local offsets).
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
ok = []
for r in """$rows""".strip().splitlines():
    p = r.split()
    if len(p) < 3: continue
    try: t = d.datetime.fromisoformat(p[0]).astimezone(d.timezone.utc)
    except Exception: continue
    if t >= slot - d.timedelta(minutes=2) and p[1] == "Success": ok.append(p[2])
print("slot=%s successful runs at/after slot=%d" % (slot.strftime("%Y-%m-%dT%H:%MZ"), len(ok)))
print("CID " + (ok[-1] if ok else "NONE"))
PY
)
printf '%s\n' "$out" | head -1
cid=$(printf '%s\n' "$out" | sed -n 's/^CID //p')
k=0
if [ -n "$cid" ] && [ "$cid" != NONE ]; then
  inst=$(timeout 40 "$AWS" ssm list-command-invocations --command-id "$cid" --query 'CommandInvocations[0].InstanceId' --output text 2>&1 | tr -d '\r')
  o=$(timeout 40 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id "$inst" --query StandardOutputContent --output text 2>&1 | tr -d '\r')
  k=$(printf '%s\n' "$o" | grep -c 'OUTPUT_KEY=')
fi
echo "run ${cid:-NONE}: OUTPUT_KEY lines=$k"
if [ -n "$cid" ] && [ "$cid" != NONE ] && [ "$k" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
