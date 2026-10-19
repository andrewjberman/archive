#!/usr/bin/env bash
# OPLGTW OG-rz-2 AC2 (Phase B): the host is t4g.large and running (LIVE describe-instances), the raised limits are live, and the service answers.
#  - ledger nfra-oplgtw-gateway-resize-t4g-large CLOSED at HEAD, sentinel gone;
#  - LIVE: ec2 describe-instances for the instance id recorded in W/RZ2_BEFORE.json: InstanceType t4g.large, state running;
#  - W/RZ2_SERVED.json: health_after 200, marker_equals_release true, unit limits 5600M and 6400M, memory_total_mb >= 7000,
#    tools_list 103, tools_27_of_27 true, nrestarts_after_deploy 0, large_replies (2 entries, one at a time, complete, peak_mb
#    below memory_high_mb).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"; slug=nfra-oplgtw-gateway-resize-t4g-large
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
rec=$(timeout 60 python - "$(native "$W/RZ2_BEFORE.json")" "$(native "$W/RZ2_SERVED.json")" <<'EOF'
import json, sys
def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None
b, s = load(sys.argv[1]), load(sys.argv[2])
typ = st = None
try:
    import boto3
    r = boto3.client("ec2", region_name="us-east-1").describe_instances(InstanceIds=[(b or {})["instance_id"]])
    i = r["Reservations"][0]["Instances"][0]; typ, st = i["InstanceType"], i["State"]["Name"]
except Exception as e:
    print("live read FAILED %s" % type(e).__name__)
ok_i = typ == "t4g.large" and st == "running"
s = s or {}
lr = s.get("large_replies") or []
ok_h = s.get("health_after") in (200, "200")
ok_m = s.get("marker_equals_release") is True
ok_u = s.get("unit_memory_high") == "5600M" and s.get("unit_memory_max") == "6400M"
ok_mem = isinstance(s.get("memory_total_mb"), (int, float)) and s["memory_total_mb"] >= 7000
ok_t = s.get("tools_list") == 103
ok_27 = s.get("tools_27_of_27") is True
ok_n = s.get("nrestarts_after_deploy") == 0
done = [x for x in lr if x.get("complete") is True and isinstance(x.get("peak_mb"), (int, float)) and x["peak_mb"] < (s.get("memory_high_mb") or 5600)]
ok_l = len(lr) == 2 and len(done) == 2
print("live instance type %s state %s: %s" % (typ, st, "yes" if ok_i else "no"))
print("health 200: %s; marker equals the release: %s; unit limits 5600M and 6400M: %s; memory total >= 7000 MB: %s; tools/list 103: %s; 27 of 27: %s; NRestarts after the deploy 0: %s" % tuple("yes" if x else "no" for x in (ok_h, ok_m, ok_u, ok_mem, ok_t, ok_27, ok_n)))
print("large replies one at a time: %d of 2 complete, peak below MemoryHigh: %s" % (len(done), "yes" if ok_l else "no"))
print("OK" if all((ok_i, ok_h, ok_m, ok_u, ok_mem, ok_t, ok_27, ok_n, ok_l)) else "NO")
EOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
echo "$slug: status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
printf '%s\n' "$rec" | sed '$d'
[ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
