#!/usr/bin/env bash
# OPLGTW OG-en-7 AC1 (round 38 E7, CTO round-37 analysis section 3; CVO v28 enrichment): the SmartX served read counts the 49F candidates whose advisor maps to ANOTHER firm, with the denominator.
# The record W/SMARTX_CROSSFIRM.json = {"read_at": "<iso>", "live_commit": "<sha>", "method": "<one line>", "candidates_checked": n, "candidates_mapping_to_other_firm": k,
#  "denominator": "<what n counts>", "expected": 0, "note": "<one line>"}; n is at least 1, k is between 0 and n, no digit run of 8 or more, no e-mail address, no person key.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
[ -f "$W/SMARTX_CROSSFIRM.json" ] || { echo "SMARTX_CROSSFIRM.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/SMARTX_CROSSFIRM.json")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read(); d = json.loads(raw)
n = d.get("candidates_checked"); k = d.get("candidates_mapping_to_other_firm")
ok_nums = isinstance(n, int) and isinstance(k, int) and n >= 1 and 0 <= k <= n
runs = len(re.findall(r"(?<![\w*])\d{8,}(?![\w])", raw)); mails = len(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", raw))
has = all(d.get(x) for x in ("read_at", "live_commit", "method", "denominator"))
print("smartx cross-firm count: candidates checked %s; mapping to another firm %s (expected 0); fields present %s; digit runs of 8 or more %d (want 0); e-mail addresses %d (want 0)" % (n, k, has, runs, mails))
print("OK" if ok_nums and has and runs == 0 and mails == 0 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
