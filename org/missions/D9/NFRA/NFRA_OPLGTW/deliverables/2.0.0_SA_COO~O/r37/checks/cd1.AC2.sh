#!/usr/bin/env bash
# OPLGTW OG-cd-1 AC2 (round-37 R3, FWD-20 PROOF, off-host arm): W/CD1_LIVE_READ.json is ONE run of family_depth's read
# against live AWS. This check re-reads two live values itself and compares them to the record:
#  - the schwab family's schedule equals the live ScheduleExpression of rule opal-assets-silver-schwab-sweep-daily;
#  - the schwab family's backfill frontier equals frontier_date in the first backfill-status key the record names, read
#    live from S3.
# Also: every family value carries a claim in {measured, inferred, absent}, and the family count equals the record's
# own denominator.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~65/CD1_LIVE_READ.json"
[ -f "$REC" ] || { echo "CD1_LIVE_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
AWS=".tools/aws"
live_sched=$(timeout 30 "$AWS" events describe-rule --name opal-assets-silver-schwab-sweep-daily --region us-east-1 --query ScheduleExpression --output text | tr -d '\r')
key=$(python -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
f=[x for x in d.get('families',[]) if x.get('family')=='schwab']
ks=(f[0].get('depth',{}).get('backfill_status_keys') or []) if f else []
print(ks[0] if ks else '')" "$(native "$REC")" | tr -d '\r')
live_front=""
[ -n "$key" ] && live_front=$(timeout 30 "$AWS" s3 cp "$key" - --region us-east-1 | python -c "
import json,sys
d=json.loads(sys.stdin.buffer.read().decode('utf-8'))
print((d.get('layers',{}).get('silver') or {}).get('frontier_date',''))" | tr -d '\r')
res=$(python - "$(native "$REC")" "$live_sched" "$live_front" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
live_sched, live_front = sys.argv[2], sys.argv[3]
CL = {"measured", "inferred", "absent"}
fams = d.get("families", [])
den = d.get("denominator")
bad = 0
def walk(v):
    global bad
    if isinstance(v, dict):
        if "value" in v and v.get("claim") not in CL:
            bad += 1
        for x in v.values():
            walk(x)
    elif isinstance(v, list):
        for x in v:
            walk(x)
walk(fams)
s = [f for f in fams if f.get("family") == "schwab"]
rec_sched = (s[0].get("schedule") or {}).get("value") if s else None
rec_front = ((s[0].get("depth") or {}).get("backfill_frontier") or {}).get("value") if s else None
ok_s = bool(live_sched) and rec_sched == live_sched
ok_f = bool(live_front) and rec_front == live_front
print("families %d; denominator %s (%s); claim-less values %d" % (len(fams), den, d.get("denominator_source", "NONE"), bad))
print("schwab schedule record=%s live=%s equal=%s" % (rec_sched, live_sched or "UNREAD", "yes" if ok_s else "no"))
print("schwab backfill frontier record=%s live=%s equal=%s" % (rec_front, live_front or "UNREAD", "yes" if ok_f else "no"))
print("VERDICT " + ("PASS" if (fams and den == len(fams) and bad == 0 and ok_s and ok_f) else "FAIL"))
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | grep -v '^VERDICT'
printf '%s\n' "$res" | grep -q '^VERDICT PASS' && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
