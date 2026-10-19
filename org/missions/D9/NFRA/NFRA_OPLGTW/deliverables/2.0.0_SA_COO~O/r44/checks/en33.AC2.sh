#!/usr/bin/env bash
# OPLGTW OG-en-33 AC2 (round 44; row Z-S399): the first-run flake is REPRODUCED COLD and its cause is named, or it is reported NOT_REPRODUCED after enough cold runs. Cold = the tree changed since the last run: `__pycache__` removed under the gateway folder
# and/or the test files touched (mtime). The 18-file window set of OG-ap-45 AC4 (listed in the order) is the load.
# Record W/BOTHORDERS_COLD.json = {"body": {"runs": [{"n": 1, "how_cold": "pycache_removed|files_touched|both", "forward_tail": "<last 3 lines of the forward output>", "reverse_tail": "<last 3 lines>", "forward_passed": n, "reverse_passed": n}, ... at least 8],
#   "cause": "<at least 40 characters; starts with NOT_REPRODUCED when no run read forward_passed 0 or a count below reverse_passed>", "cause_evidence": "<for a reproduced flake: the quoted forward_tail of one failing run and what it shows>"}}
# Override (dry-run controls only): EN33_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EN33_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~159/BOTHORDERS_COLD.json}"
[ -f "$REC" ] || { echo "BOTHORDERS_COLD.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python -I - "$(native "$REC")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
runs = b.get("runs") or []
isi = lambda v: isinstance(v, int) and not isinstance(v, bool) and v >= 0
runs_ok = len(runs) >= 8 and all(isinstance(r, dict) and r.get("how_cold") in ("pycache_removed", "files_touched", "both") and isinstance(r.get("forward_tail"), str) and isinstance(r.get("reverse_tail"), str)
                                 and isi(r.get("forward_passed")) and isi(r.get("reverse_passed")) for r in runs)
bad = [r for r in runs if isinstance(r, dict) and isi(r.get("forward_passed")) and isi(r.get("reverse_passed")) and r["forward_passed"] != r["reverse_passed"]]
cause = b.get("cause") if isinstance(b.get("cause"), str) else ""
ev = b.get("cause_evidence") if isinstance(b.get("cause_evidence"), str) else ""
if bad:
    cause_ok = len(cause) >= 40 and not cause.startswith("NOT_REPRODUCED") and any(t.strip() and t.strip() in ev for t in [x.get("forward_tail", "") for x in bad]) is True
else:
    cause_ok = cause.startswith("NOT_REPRODUCED") and len(cause) >= 40
leak = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
ok = runs_ok and cause_ok and not leak
print("cold runs recorded %d (want >= 8), each with its forward and reverse text and counts: %s; runs where forward differs from reverse: %d" % (len(runs), "ok" if runs_ok else "NOT OK", len(bad)))
print("cause: %s; %s; email-shaped strings %d (want 0)" % (cause[:60].replace("\n", " "), "consistent with the runs" if cause_ok else "NOT consistent with the runs", len(leak)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
