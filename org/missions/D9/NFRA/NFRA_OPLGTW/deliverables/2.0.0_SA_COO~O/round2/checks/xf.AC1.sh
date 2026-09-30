#!/usr/bin/env bash
# OPLGTW OG-x-4 AC1 (CTO ruling msg 26488 (1)): on the HOST, the export's peak child RSS at 11 columns is FLAT across
# 25,000 / 125,000 / 250,000 rows -- every export job completed ok and each peak is within 10% of the 25k peak.
# Reads the recorded on-host measurement the worker assembles at PHASE B (CAPACITY_X4.json, same shape as OG-r-3's
# CAPACITY.json: ac2.jobs[] with labels "export:<case> (<N> rows x <C> columns)"). XF_CAPACITY is a TEST-ONLY override
# (dry-run / mutant control); the criterion's invocation never sets it.
. "$(dirname "$0")/_root.sh"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~11"
F="${XF_CAPACITY:-$D/CAPACITY_X4.json}"
[ -f "$F" ] || { echo "measurement $F absent; export sizes graded 0 of 3"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'EOF'
import json, re, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
jobs = d.get("ac2", {}).get("jobs", [])
want = {25000: None, 125000: None, 250000: None}
pat = re.compile(r"^export:\S+ \((\d+) rows x (\d+) columns\)$")
for j in jobs:
    m = pat.match(str(j.get("job", "")))
    if m and int(m.group(2)) == 11 and int(m.group(1)) in want:
        want[int(m.group(1))] = j
missing = [n for n, j in want.items() if j is None]
if missing:
    print("export jobs at 11 columns missing for rows %s; graded %d of 3" % (missing, 3 - len(missing)))
    print("RESULT: FAIL"); sys.exit(1)
base = int(want[25000]["peak_child_rss_bytes"])
bound = base * 1.10
ok = True
for n in (25000, 125000, 250000):
    j = want[n]; pk = int(j["peak_child_rss_bytes"])
    good = bool(j.get("ok")) and pk <= bound
    ok = ok and good
    print("rows=%d columns=11 ok=%s peak=%d ratio_to_25k=%.4f %s" % (n, j.get("ok"), pk, pk / base, "within" if good else "OUT"))
print("bound = 1.10 x 25k peak = %d; export sizes graded 3 of 3" % bound)
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
EOF
