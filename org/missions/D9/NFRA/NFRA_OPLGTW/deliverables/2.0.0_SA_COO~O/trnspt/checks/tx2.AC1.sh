#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-tx-2 AC1 (transcript spec section 6 steps 1-4 through the RELEASED interactive tools as
# Andrew): the reach record shows, for 4 of 4 allowlisted meetings, REACH (rows >= 1), COMPLETENESS (total_bytes equals
# the body length, last cue within 60 s of endDateTime) and ATTRIBUTION (speaker tags > 0); plus the REACH negative arm
# refused; and every recorded read resolves to an audit record with the same transcript id and byte count.
. "$(dirname "$0")/_root.sh"
J="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/TRANSCRIPT_REACH.json"
[ -f "$J" ] || { echo "$J absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 30 python - "$(native "$J")" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
ms = d.get("meetings", [])
ok = [m for m in ms if m.get("rows", 0) >= 1 and m.get("total_bytes") == m.get("body_bytes_measured")
      and abs(m.get("last_cue_vs_end_s", 9e9)) <= 60 and m.get("speaker_tags", 0) > 0 and m.get("audit_match") is True]
neg = d.get("negative_arm", {}).get("refused") is True
print("meetings passing all four of 4 required: %d of %d recorded; negative arm refused=%s" % (len(ok), len(ms), neg))
print("OK" if len(ok) == 4 and len(ms) == 4 and neg else "BAD")
EOF
)
printf '%s\n' "$out"
if [ "$(printf '%s\n' "$out" | tail -1)" = OK ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
