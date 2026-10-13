#!/usr/bin/env bash
# OPLGTW OG-sh-1 AC2 (dell2-54ae ruling point 3): W/SH1_0929_READ.json is the one read of the gateway request log for
# 2026-09-29, filtered on the 2026-06-01 meeting's id. The meeting id is named with its source, and the log group is named.
# The verdict is READ, REFUSED or NO_EVENT. A positive control (another tool call in the same group that day) was found.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~63/SH1_0929_READ.json"
[ -f "$F" ] || { echo "SH1_0929_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
pc = d.get("positive_control_events", 0)
print("meeting_id %s (source %s); log_group %s; day %s; events_matched %s; verdict %s; positive control %s"
      % ("set" if d.get("meeting_id") else "NONE", d.get("meeting_id_source"), d.get("log_group"), d.get("day"),
         d.get("events_matched"), d.get("verdict"), pc))
ok = (bool(d.get("meeting_id")) and bool(d.get("meeting_id_source")) and bool(d.get("log_group"))
      and d.get("day") == "2026-09-29" and isinstance(d.get("events_matched"), int)
      and d.get("verdict") in ("READ", "REFUSED", "NO_EVENT") and isinstance(pc, int) and pc >= 1)
raise SystemExit(0 if ok else 1)
PY
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
