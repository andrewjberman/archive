#!/usr/bin/env bash
# OPLGTW OG-pm-1 AC1 (row Z-W16-S5, CTO round-16 analysis s.4 item 5): P95_R17.json grades the ALB TargetResponseTime
# p95 of the opal-gateway target over the FULL trading day 2026-10-05 (UTC 00:00..24:00, one 86400 s period, the OG-p-1
# metric), on served 4b6b823fae for the whole window, against OG-p-1's 0.5535 s reference and the 20% cap (0.6642 s).
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
print("window %s..%s; served %s whole window %s; requests %s; p95 %s s vs cap %.4f s; verdict %s; consistent %s"
      % (d.get("window_start"), d.get("window_end"), str(d.get("served_release"))[:10], d.get("served_whole_window"),
         n, p95, 0.5535 * 1.2, verdict, consistent))
ok = (d.get("window_start") == "2026-10-05T00:00:00Z" and d.get("window_end") == "2026-10-06T00:00:00Z"
      and str(d.get("served_release", "")).startswith("4b6b823fae") and d.get("served_whole_window") is True
      and isinstance(n, int) and n > 0 and consistent)
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
