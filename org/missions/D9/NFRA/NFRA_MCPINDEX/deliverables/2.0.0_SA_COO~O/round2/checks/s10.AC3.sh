#!/usr/bin/env bash
# MX-s-10 AC3 (THE ACCEPTANCE: the first SCHEDULED fire, not the ad-hoc test): an SSM run of opal-bd-asset-dim-download
# requested at or after the first 22:10Z weekday slot following the issuance records Status=Success, and
# silver/bd_assets_dim.parquet was rewritten after that run was requested.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
ISSUED="$(git log -1 --format=%cI --grep='issue(NFRA_MCPINDEX.TO-MX-s-10' HEAD)"
[ -n "$ISSUED" ] || { echo "issuance commit not found -- RESULT: FAIL"; exit 1; }
cmds=$(timeout 90 "$AWS" ssm list-commands --filters key=DocumentName,value=opal-bd-asset-dim-download --query 'Commands[].[RequestedDateTime,Status]' --output text 2>&1 | tr -d '\r')
lm=$(timeout 60 "$AWS" s3api head-object --bucket opal-data-bd --key silver/bd_assets_dim.parquet --query LastModified --output text 2>&1 | tr -d '\r')
out=$(python - "$ISSUED" "$lm" <<PY 2>&1
import sys, datetime as d
issued = d.datetime.fromisoformat(sys.argv[1]).astimezone(d.timezone.utc)
lm = sys.argv[2].strip()
# the first weekday 22:10Z slot at or after the issuance
slot = issued.replace(hour=22, minute=10, second=0, microsecond=0)
if slot < issued: slot += d.timedelta(days=1)
while slot.weekday() >= 5: slot += d.timedelta(days=1)
rows = """$cmds""".strip().splitlines()
hits = []
for r in rows:
    p = r.split()
    if len(p) < 2: continue
    try: t = d.datetime.fromisoformat(p[0].replace('Z', '+00:00')).astimezone(d.timezone.utc)
    except Exception: continue
    if t >= slot - d.timedelta(minutes=2): hits.append((t, p[1]))
ok = [h for h in hits if h[1] == 'Success']
try: lmt = d.datetime.fromisoformat(lm.replace('Z', '+00:00')).astimezone(d.timezone.utc)
except Exception: lmt = None
rewritten = bool(ok) and lmt is not None and lmt > min(h[0] for h in ok)
print('first slot=%s runs at/after slot=%d success=%d dim rewritten after the successful run=%s' % (slot.strftime('%Y-%m-%dT%H:%MZ'), len(hits), len(ok), 'yes' if rewritten else 'no'))
print('OK' if rewritten else 'NOT-OK')
PY
)
printf '%s\n' "$out" | head -1
if printf '%s\n' "$out" | tail -1 | grep -qx OK; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
