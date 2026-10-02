#!/usr/bin/env bash
# OPLGTW OG-gr-1 AC1 (row Z-W10-S1; analysis round 12 s.3a): GRAIN_R13.json measures the declared and the candidate
# grain over its PRINTED denominator of qualified snapshots (more than the 8 already measured), one row per snapshot,
# and its verdict follows the ruling: ADOPT only if the candidate is unique on EVERY snapshot AND its added column is
# never blank; otherwise REFUSE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~22/GRAIN_R13.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
N = d.get("denominator", {}).get("qualified_snapshots"); rows = d.get("snapshots", [])
need = ("master", "dataset", "date", "declared_unique", "candidate_unique", "candidate_blank")
shaped = [r for r in rows if all(k in r for k in need)]
allu = all(r["candidate_unique"] is True for r in shaped); blanks = sum(int(r["candidate_blank"]) for r in shaped)
coll = sum(1 for r in shaped if r["declared_unique"] is False)
want = "ADOPT" if (shaped and allu and blanks == 0) else "REFUSE"
print("denominator %s; snapshot rows %d (shaped %d); declared grain collides on %d; candidate unique on all %s; candidate blanks %d; verdict %s (rule says %s)"
      % (N, len(rows), len(shaped), coll, allu, blanks, d.get("verdict"), want))
ok = isinstance(N, int) and N > 8 and len(shaped) == N == len(rows) and d.get("verdict") == want
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
EOF
