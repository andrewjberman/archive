#!/usr/bin/env bash
# OPLGTW OG-eg-2 AC2 (round-37 EGRESS, PRD v3.10 E2): the first cycle record written after the re-registration counts its S3 GETs, and the bytes sit inside the bar.
#   Reads <old state dir>/cycles/<P>/*.cycle.json (the proof names the state dir and the registration time). The record newest after registered_at must carry integer s3_get_count and s3_get_bytes,
#   with s3_get_bytes <= 10 GB (the harvest bucket holds about 8 GB, CTO msg 34372: more bytes than the bucket holds means a prefix was read twice in one cycle).
#   Negative control: the number of records written BEFORE registered_at that lack the two fields is printed (must be 1+ -- the instrument can see an absent field).
#   s3_get_bytes counts store.py's GETs only (row Z-W98-S1): a lower bound, said so in the output.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZW"
[ -f "$W/EG2_PROOF.json" ] || { echo "EG2_PROOF.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$W/EG2_PROOF.json" <<'PY'
import datetime as dt, glob, json, os, sys
prf = json.load(open(sys.argv[1], encoding="utf-8"))
reg = dt.datetime.fromisoformat(str(prf.get("registered_at")).replace("Z", "+00:00"))
sd = str(prf.get("old_state_dir", ""))
recs = []
for p in glob.glob(os.path.join(sd, "cycles", "*", "*.cycle.json")):
    try:
        d = json.load(open(p, encoding="utf-8"))
        ended = dt.datetime.strptime(d["ended_at"], "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc) if "T" in str(d.get("ended_at")) and "-" not in str(d.get("ended_at")) else dt.datetime.fromisoformat(str(d["ended_at"]).replace("Z", "+00:00"))
        recs.append((ended, p, d))
    except Exception:
        continue
after = sorted([r for r in recs if r[0] > reg], key=lambda r: r[0])
before_missing = sum(1 for r in recs if r[0] <= reg and "s3_get_bytes" not in r[2])
print("cycle records under %s: %d total, %d after registered_at, %d before without the fields (negative control, want 1+)" % (sd, len(recs), len(after), before_missing))
if not after:
    print("no cycle record after registered_at yet"); sys.exit(1)
e, p, d = after[0]
n, b = d.get("s3_get_count"), d.get("s3_get_bytes")
good = isinstance(n, int) and isinstance(b, int) and b <= 10 * 10**9 and before_missing >= 1
print("first record after registration: %s publisher %s ended %s: s3_get_count %s, s3_get_bytes %s (%.2f GB; a LOWER BOUND, store.py GETs only; bar 10 GB)" % (os.path.basename(p), d.get("publisher"), d.get("ended_at"), n, b, (b or 0) / 1e9))
sys.exit(0 if good else 1)
PY
rc=$?
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
