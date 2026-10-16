#!/usr/bin/env bash
# OPLGTW OG-ev-2 AC1 (round 39 E1 measurement + the allocation weight scale): E1_PARTITION_MEASURE.json is complete and self-consistent.
#  - tables transactions and fees: partitions >= 2, pairs_checked >= 3, every overlap ratio in [0,1], classification matches the rule on the MEDIAN ratio (<= 0.05 increment, >= 0.9 snapshot, else mixed);
#  - allocations: accounts_sampled >= 20, scale counts sum to accounts_sampled, weight_scale matches the majority rule (near_1 majority -> fraction, near_100 majority -> percent, else unclear);
#  - no content: only ints, floats, booleans and the fixed words; no digit run of 9 or more outside ISO dates; no e-mail.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV2_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/E1_PARTITION_MEASURE.json}"
[ -f "$REC" ] || { echo "E1_PARTITION_MEASURE.json is absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$REC")" <<'PYEOF'
import json, re, statistics, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw)
body = d.get("body", d)
tabs = body.get("tables") or {}
lines, ok = [], True
for name in ("transactions", "fees"):
    t = tabs.get(name) or {}
    ratios = t.get("overlap_ratios") or []
    good = (isinstance(t.get("partitions"), int) and t["partitions"] >= 2 and isinstance(t.get("pairs_checked"), int) and t["pairs_checked"] >= 3
            and len(ratios) == t.get("pairs_checked") and all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in ratios))
    cls = t.get("classification")
    med = statistics.median(ratios) if ratios else None
    want = None if med is None else ("increment" if med <= 0.05 else "snapshot" if med >= 0.9 else "mixed")
    cls_ok = good and cls == want
    ok = ok and cls_ok
    lines.append("%s: partitions %s, pairs checked %s, median overlap %s, classification %s (rule says %s)" % (
        name, t.get("partitions"), t.get("pairs_checked"), None if med is None else round(med, 4), cls, want))
a = body.get("allocations") or {}
sc = a.get("scale_counts") or {}
n1, n100, no = sc.get("near_1"), sc.get("near_100"), sc.get("other")
ints = all(isinstance(x, int) and x >= 0 for x in (n1, n100, no))
tot_ok = ints and a.get("accounts_sampled") == n1 + n100 + no and a["accounts_sampled"] >= 20
want_scale = None
if ints:
    want_scale = "fraction" if n1 > n100 + no else "percent" if n100 > n1 + no else "unclear"
al_ok = tot_ok and a.get("weight_scale") == want_scale
ok = ok and al_ok
lines.append("allocations: accounts sampled %s; near_1 %s, near_100 %s, other %s; weight_scale %s (rule says %s)" % (
    a.get("accounts_sampled"), n1, n100, no, a.get("weight_scale"), want_scale))
runs = [m for m in re.findall(r"(?<![\d-])\d{9,}(?![\d-])", raw)]
mails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", raw)
clean = not runs and not mails
ok = ok and clean
lines.append("content hygiene: long digit runs %d (want 0); e-mail addresses %d (want 0)" % (len(runs), len(mails)))
print("\n".join(lines))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
