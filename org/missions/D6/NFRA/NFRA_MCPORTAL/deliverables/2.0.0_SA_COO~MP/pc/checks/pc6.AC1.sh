#!/usr/bin/env bash
# MP-pc-6 AC1 (FWD-21 DONE WHEN, read half; G1 close): the worker's run file
# deliverables/0.9.0_WK_NFRA_MCPORTAL~24/pc6_run.json carries {"person","store_tools","page_person_tools","channel",
# "breakdown_holder_tools","page_channel_tools","box_no","box_not_recorded","served_box_no","served_box_not_recorded"}:
# the real person's data-grant tools read from the grant store equal the data-grant tools the served /people view lists
# for that person; the channel's tools the breakdown's holder row lists for that person equal the tools /people lists
# under that channel; and the served gitstate reads {"refused": false} for the box whose pointer is rc 0 and
# "not recorded" for a box with no pointer (each pointer read independently with head-object/get-object, never off the page).
. "$(dirname "$0")/_root.sh"
RUN="${MP_PC6_RUN:-org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~24/pc6_run.json}"
v=$(python - "$RUN" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print("run=unreadable(%s)" % type(e).__name__); sys.exit()
eq = lambda a, b: "yes" if d.get(a) and sorted(d[a]) == sorted(d.get(b) or []) else "no"
no = "yes" if d.get("box_no") and d.get("served_box_no") == {"refused": False, "at": d["served_box_no"].get("at")} and d["served_box_no"].get("at") else "no"
nr = "yes" if d.get("box_not_recorded") and d.get("served_box_not_recorded") == "not recorded" else "no"
print("run=read person=%s store==page:%s channel=%s breakdown==page:%s box_no=%s served_no:%s box_not_recorded=%s served_not_recorded:%s" % (
    d.get("person"), eq("store_tools", "page_person_tools"), d.get("channel"), eq("breakdown_holder_tools", "page_channel_tools"),
    d.get("box_no"), no, d.get("box_not_recorded"), nr))
PY
)
echo "$v"
if printf '%s' "$v" | grep -q 'store==page:yes' && printf '%s' "$v" | grep -q 'breakdown==page:yes' \
   && printf '%s' "$v" | grep -q 'served_no:yes' && printf '%s' "$v" | grep -q 'served_not_recorded:yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
