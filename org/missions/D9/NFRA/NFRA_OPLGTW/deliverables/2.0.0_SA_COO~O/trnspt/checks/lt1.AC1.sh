#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-lt-1 AC1 (C7 O3, a MEASUREMENT): the stored sign-in lifetime record exists and carries its claim.
# It names the instrument, each timestamp in UTC, the observed unattended span in hours with its claim class, a silent
# refresh outcome read on demand, and a verdict GE_1_DAY or LT_1_DAY consistent with that span.
. "$(dirname "$0")/_root.sh"
J="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~17/TOKEN_LIFETIME.json"
[ -f "$J" ] || { echo "$J absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 30 python - "$(native "$J")" <<'EOF' 2>&1 | tr -d '\r'
import json, re, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
need = ["identity_class", "instrument", "measured_at_utc", "last_interactive_auth_utc", "last_silent_refresh_utc",
        "silent_refresh_now", "observed_unattended_hours", "observed_unattended_hours_claim", "verdict"]
miss = [k for k in need if k not in d]
ts = [k for k in need if k.endswith("_utc")]
bad_ts = [k for k in ts if k in d and not re.match(r"^\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d)?Z$", str(d[k]))]
claim_ok = d.get("observed_unattended_hours_claim") in ("measured", "inferred", "held", "absent")
v = d.get("verdict"); h = d.get("observed_unattended_hours")
cons = (v == "GE_1_DAY" and isinstance(h, (int, float)) and h >= 24) or (v == "LT_1_DAY")
print("fields present %d of %d; malformed timestamps %d of %d; claim class ok=%s; verdict %s at %s h consistent=%s"
      % (len(need) - len(miss), len(need), len(bad_ts), len(ts), claim_ok, v, h, cons))
print("OK" if not miss and not bad_ts and claim_ok and cons else "BAD")
EOF
)
printf '%s\n' "$out"
if [ "$(printf '%s\n' "$out" | tail -1)" = OK ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
