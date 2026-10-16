#!/usr/bin/env bash
# OPLGTW OG-ev-1 AC1 (round-37, CVO v29 @7f1ada5f4e): the applier's served read wrote ONE projected answer body per named marker of the AC3 judgment criteria of OG-ap-18, ap-19, ap-20, ap-21 and ap-23.
# The record W/ANSWER_BODIES.json = {"read_at": "<iso>", "live_commit": "<sha>", "releases": {"ap-18": [{"tool": "...", "marker": "...", "arguments": {...}, "body": <json>}, ...], ...}}.
# Minimum bodies per release (one per marker the CVO named): ap-18 3, ap-19 3, ap-20 3, ap-21 3, ap-23 4. Every body is a non-empty JSON object or array, at most 12000 bytes serialised;
# the file carries no digit run of 8 or more (an unmasked account or phone number), no raw "account_number" key.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
[ -f "$W/ANSWER_BODIES.json" ] || { echo "ANSWER_BODIES.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/ANSWER_BODIES.json")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw)
need = {"ap-18": 3, "ap-19": 3, "ap-20": 3, "ap-21": 3, "ap-23": 4}
rels = d.get("releases", {}) if isinstance(d, dict) else {}
short = []; empty = 0; big = 0; nbodies = 0
for k, n in need.items():
    rows = rels.get(k, [])
    if len(rows) < n:
        short.append(k)
    for r in rows:
        b = r.get("body") if isinstance(r, dict) else None
        nbodies += 1
        if not isinstance(b, (dict, list)) or not b:
            empty += 1
        elif len(json.dumps(b)) > 12000:
            big += 1
runs = len(re.findall(r"(?<![\w*])\d{8,}(?![\w])", raw))
rawkey = raw.count('"account_number"')
print("answer bodies: releases %d of 5; bodies %d; releases short of their minimum %d (want 0); empty or non-JSON bodies %d (want 0); bodies over 12000 bytes %d (want 0); digit runs of 8 or more %d (want 0); raw account_number keys %d (want 0)" % (len([k for k in need if rels.get(k)]), nbodies, len(short), empty, big, runs, rawkey))
print("OK" if not short and empty == 0 and big == 0 and runs == 0 and rawkey == 0 and len([k for k in need if rels.get(k)]) == 5 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
