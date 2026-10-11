#!/usr/bin/env bash
# OPLGTW OG-dq-1 AC1 (round-34 E7, row Z-S77): W/DQ1_READ.json records each plane read for the 2026-10-09 15:39Z-16:17Z
# drain of opal-assets-silver-dlq, each with its denominator:
# - cloudtrail_events (management events naming the queue);
# - event_source_mappings (every Lambda mapping on the queue's ARN);
# - metrics (per-minute NumberOfMessagesReceived and NumberOfMessagesDeleted over the window);
# - current_messages (count, and the source key of each);
# - actor (named | unnamed), with its evidence.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~57/DQ1_READ.json"
[ -f "$F" ] || { echo "DQ1_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
need = {"cloudtrail_events": list, "event_source_mappings": list, "metrics": dict, "current_messages": dict}
have = {k: isinstance(d.get(k), t) for k, t in need.items()}
den = all(isinstance(d.get(k + "_denominator"), (int, str)) for k in ("cloudtrail_events", "event_source_mappings"))
actor = d.get("actor", {})
ok_actor = actor.get("verdict") in ("named", "unnamed") and bool(actor.get("evidence"))
cm = d.get("current_messages", {})
print("planes present %s; denominators printed %s; current messages %s; actor %s"
      % (have, den, cm.get("count"), actor.get("verdict")))
raise SystemExit(0 if all(have.values()) and den and isinstance(cm.get("count"), int) and ok_actor else 1)
PY
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
