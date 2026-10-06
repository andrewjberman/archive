#!/usr/bin/env bash
# OPLGTW OG-pm-1 AC1 (row Z-W16-S5, CTO round-16 analysis s.4 item 5): P95_R17.json grades the ALB TargetResponseTime
# p95 of the opal-gateway target over the FULL trading day 2026-10-05 (UTC 00:00..24:00, one 86400 s period, the OG-p-1
# metric), across the releases served in the window (A1), against OG-p-1's 0.5535 s reference and the 20% cap (0.6642 s).
# The grade is a measurement either way: PASS needs the record complete and its verdict consistent with its numbers; a
# regression beyond the cap needs a surprise row id to the CTO in the record.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~27/P95_R17.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
p95, ref, cap, n = d.get("p95_seconds"), d.get("reference_seconds"), d.get("cap_fraction"), d.get("request_count")
within = isinstance(p95, (int, float)) and ref == 0.5535 and cap == 0.20 and p95 <= ref * (1 + cap)
verdict = d.get("verdict")
consistent = (verdict == "WITHIN_CAP" and within) or (verdict == "REGRESSION" and not within and bool(d.get("row_id")))
# AMENDED A1 (issuer, 2026-10-06 ~00:1xZ): two releases landed inside the window (r17 e91819e281 at 02:17:58Z, r17c
# 37be3485db at 14:22:36Z, EC2_MANIFEST history), so the record carries served_segments, which must equal the manifest's
# three segments, instead of one release for the whole window.
WANT = [["4b6b823fae", "2026-10-05T00:00:00Z", "2026-10-05T02:17:58Z"],
        ["e91819e281", "2026-10-05T02:17:58Z", "2026-10-05T14:22:36Z"],
        ["37be3485db", "2026-10-05T14:22:36Z", "2026-10-06T00:00:00Z"]]
seg = [[str(s.get("release", ""))[:10], s.get("start"), s.get("end")] for s in d.get("served_segments", [])]
seg_ok = seg == WANT
print("window %s..%s; served segments match the manifest %s (%d); requests %s; p95 %s s vs cap %.4f s; verdict %s; consistent %s"
      % (d.get("window_start"), d.get("window_end"), seg_ok, len(seg), n, p95, 0.5535 * 1.2, verdict, consistent))
ok = (d.get("window_start") == "2026-10-05T00:00:00Z" and d.get("window_end") == "2026-10-06T00:00:00Z"
      and seg_ok and isinstance(n, int) and n > 0 and consistent)
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
