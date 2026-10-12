#!/usr/bin/env bash
# OPLGTW OG-tb-1 AC1 (round-35 E3, row Z-S92): W/TB1_READ.json records every GetSecretValue on gateway/teams/bearer over the
# CloudTrail 90-day management-event window: per principal (ARN plus count), the events read (the denominator), and the
# positive control (the gateway's own role appears as a reader). The verdict "none" or "found" concerns
# cloudops-dell-agents-group members.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~59/TB1_READ.json"
[ -f "$F" ] || { echo "TB1_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
pr = d.get("principals", []); ev = d.get("events_read")
ctrl = d.get("positive_control", {})
verdict = d.get("dell_group_verdict")
ok = (isinstance(ev, int) and ev >= 1 and isinstance(pr, list) and pr and all("arn" in p and isinstance(p.get("count"), int) for p in pr)
      and ctrl.get("gateway_role_seen") is True and verdict in ("none", "found") and d.get("window_days", 0) >= 85)
print("window %s days; GetSecretValue events read %s; distinct principals %d; gateway role seen %s; dell group verdict %s"
      % (d.get("window_days"), ev, len(pr), ctrl.get("gateway_role_seen"), verdict))
raise SystemExit(0 if ok else 1)
EOF
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
