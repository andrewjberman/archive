# ruff: noqa
# OG-rl-18 Phase A probe, the python of mp1.AC1.sh VERBATIM (extracted by rl18_probes_extract.py); run by rl18_host.py in a fresh guarded process with the stage as the gateway folder.
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
