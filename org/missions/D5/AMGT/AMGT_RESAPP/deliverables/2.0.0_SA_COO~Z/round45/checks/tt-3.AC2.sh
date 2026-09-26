#!/usr/bin/env bash
# AMGT_RESAPP round 45, AMGT-tt-3 AC2 -- JUDGMENT, RECORDED, NO VERDICT: each sample member, the clause it exists to exercise, its
# served Base case line, its px_last and the ratio -- for a person to judge beside the issuer's renders of the same fixtures on 5174
# (round45/real-run-<key>/model.png) whether each value reads as a price in a named currency, the same on both surfaces.
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
python - <<'PY'
import json
p = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~164/AC4_SAMPLE.json"
for m in json.load(open(p, encoding="utf-8"))["members"]:
    print("%-18s clauses=%-7s px_last=%s %s ratio=%s" % (m["security_key"], ",".join(m["clauses"]), m.get("px_last"), m.get("crncy"), m.get("ratio")))
    print("    " + m["base_line"])
    print("    why: " + (m.get("why") or ""))
PY
