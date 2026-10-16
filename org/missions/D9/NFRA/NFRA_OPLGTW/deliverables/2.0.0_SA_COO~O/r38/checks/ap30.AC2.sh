#!/usr/bin/env bash
# OPLGTW OG-ap-30 AC2 (round 38, PHASE B, after the two deletes): the LIVE table read back (strongly consistent):
#  - the andrew@ and opalbloomberg@ email_deny records are ABSENT;
#  - the alyssa@ record is still PRESENT and active;
#  - the email_deny total equals the before-record's total minus 2 (no other record moved);
#  - the before-record exists (the rollback source), its write_set is exactly the two labels, and a rollback file DENY_ROLLBACK_ITEMS.json exists but is NOT tracked by git (client identifiers stay out of the repo).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="${AP30_W_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1}"
REC="$W/DENY_BEFORE_OG-ap-30.json"; RB="$W/DENY_ROLLBACK_ITEMS.json"
[ -f "$REC" ] || { echo "DENY_BEFORE_OG-ap-30.json is absent"; echo "RESULT: FAIL"; exit 1; }
rb=no; [ -f "$RB" ] && rb=yes
tracked=$(git ls-files -- "$RB" | grep -c .)
live="${AP30_LIVE_OVERRIDE:-$(timeout 100 python "$(native "$(dirname "$0")/_deny.py")" live | tr -d '\r')}"
res=$(python - "$(native "$REC")" "$live" <<'PYEOF'
import json, sys
rec = json.load(open(sys.argv[1], encoding="utf-8"))
live = dict(kv.split("=", 1) for kv in sys.argv[2].split() if "=" in kv)
total_before = rec.get("email_deny_total_before")
ok = (live.get("live_read") == "ok" and live.get("andrew_present") == "no" and live.get("opalbloomberg_present") == "no"
      and live.get("alyssa_present") == "yes" and live.get("alyssa_active") == "yes"
      and isinstance(total_before, int) and live.get("email_deny_total") == str(total_before - 2)
      and rec.get("write_set") == ["andrew", "opalbloomberg"])
print("live: andrew record present %s, opalbloomberg record present %s (want no, no); alyssa present %s active %s (want yes, yes); email_deny total %s (want before %s minus 2)" % (
      live.get("andrew_present"), live.get("opalbloomberg_present"), live.get("alyssa_present"), live.get("alyssa_active"), live.get("email_deny_total"), total_before))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
echo "rollback file present $rb; tracked by git $tracked (want yes, 0)"
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && [ "$rb" = yes ] && [ "$tracked" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
