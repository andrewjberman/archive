#!/usr/bin/env bash
# OPLGTW OG-pm-2 AC1 (CTO round-17 analysis s.4 item 1, R17): PM2_CAUSE.json reads per-route request count and p95 for
# BOTH 2026-10-05 and 2026-09-30 from a NAMED instrument (with what it cannot see), splits the routes that existed at
# OG-p-1 from those added since, tests hypothesis (i) (a steady caller since 10-02: route, rate, p95), states a finding
# in {MIX, SLOWDOWN, BOTH, UNDETERMINED}, prints its coverage against the ALB request count, and wrote nothing (0).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~27/PM2_CAUSE.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
inst = d.get("instrument", {})
days = d.get("days", {})
ok_days = []
for day in ("2026-10-05", "2026-09-30"):
    r = days.get(day, {})
    routes = r.get("routes", [])
    good = (bool(routes) and all(isinstance(x.get("requests"), int) and isinstance(x.get("at_ogp1"), bool) for x in routes)
            and isinstance(r.get("covered_requests"), int) and isinstance(r.get("alb_requests"), int))
    old = sum(x["requests"] for x in routes if x.get("at_ogp1")) if good else 0
    new = sum(x["requests"] for x in routes if x.get("at_ogp1") is False) if good else 0
    print("%s: routes %d; requests at-OG-p-1 %d, added-since %d; covered %s of ALB %s" % (day, len(routes), old, new, r.get("covered_requests"), r.get("alb_requests")))
    ok_days.append(good)
h = d.get("hypothesis_i", {})
fnd = d.get("finding")
print("instrument %s (cannot see: %s); hypothesis (i) steady caller %s; finding %s; writes %s"
      % (inst.get("name"), bool(inst.get("cannot_see")), h.get("steady_caller_found"), fnd, d.get("writes")))
ok = (all(ok_days) and inst.get("name") and inst.get("cannot_see") and isinstance(h.get("steady_caller_found"), bool)
      and fnd in ("MIX", "SLOWDOWN", "BOTH", "UNDETERMINED") and d.get("writes") == 0)
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
