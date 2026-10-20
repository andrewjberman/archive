#!/usr/bin/env bash
# OPLGTW OG-mp-1 AC1 (round 47; the CTO's ferry 17:30Z, NFRA_MCPORTAL PRD v0.10 F3): app/admin_api.py mounts admin_people_access.routes behind owner_only.
# One fresh process, MOCK_GRAPH=1, starlette TestClient on admin_api.admin_app with NO identity header:
#  (a) GET and POST /people/{tid}/{oid}/access answer 401 {"error":"no verified identity"} (the owner gate refuses; before the mount: 404);
#  (b) controls: GET /whoami answers 401 (a gated route), GET /no/such/route answers 404 (an unmounted path), GET /people (the existing route) answers 401;
#  (c) the route table of admin_api.routes holds the two new paths exactly once each (GET, POST), and the route count grew by exactly 2 over the pinned count 16;
#  (d) the module's own routes are the ones mounted: every Route of admin_people_access.routes is present in admin_api.routes.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
G=infra/aws/ec2/opal-gateway
res=$(MOCK_GRAPH=1 python3 -I - "$(native "$G")" <<'PYEOF'
import os, sys
G = sys.argv[1]
sys.path.insert(0, G)
os.environ["MOCK_GRAPH"] = "1"
import warnings
warnings.simplefilter("ignore")
from starlette.testclient import TestClient
from app import admin_api, admin_people_access as pa
ok = True


def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NOT OK", (" (%s)" % extra) if extra else ""))


c = TestClient(admin_api.admin_app)
codes = {}
for m, p in (("GET", "/people/t1/o1/access"), ("POST", "/people/t1/o1/access"), ("GET", "/whoami"), ("GET", "/no/such/route"), ("GET", "/people")):
    r = c.request(m, p)
    codes[(m, p)] = (r.status_code, r.text)
g, po = codes[("GET", "/people/t1/o1/access")], codes[("POST", "/people/t1/o1/access")]
say("the new GET and POST answer 401 no verified identity with no owner header", g[0] == 401 and po[0] == 401 and "no verified identity" in g[1] and "no verified identity" in po[1], "GET %s POST %s" % (g[0], po[0]))
say("controls: /whoami 401, /people 401, an unmounted path 404", codes[("GET", "/whoami")][0] == 401 and codes[("GET", "/people")][0] == 401 and codes[("GET", "/no/such/route")][0] == 404)
paths = [(r.path, tuple(sorted(r.methods))) for r in admin_api.routes if hasattr(r, "path")]
want_get = ("/people/{tid}/{oid}/access", ("GET", "HEAD"))
want_post = ("/people/{tid}/{oid}/access", ("POST",))
say("the route table holds the two new routes exactly once each; count %d (want 16 + 2 = 18)" % len(admin_api.routes), paths.count(want_get) == 1 and paths.count(want_post) == 1 and len(admin_api.routes) == 18)
mounted = all(any(r is x for x in admin_api.routes) for r in pa.routes)
say("every Route object of admin_people_access.routes is the one mounted", mounted and len(pa.routes) == 2)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
