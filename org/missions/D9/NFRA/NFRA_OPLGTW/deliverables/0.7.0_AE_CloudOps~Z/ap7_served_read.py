"""OG-ap-7 B2 step 6, the SERVED grade (laptop CTO ruling term 3).

Measures GET /hx/teams/teams on the served gateway, the way the route is really called: a
host-side request through the installed app, carrying the one static TEAMS_BEARER the route
accepts (CTO half: ONE bearer from gateway/teams/bearer, compared in constant time, accepted only
on /hx/teams). The other two new routes are probed too, since term 3 names the first but the ask's
blast radius covers all three.

NEVER PRINTS THE BEARER, any token, or any response body. It prints status codes, a byte length,
and whether a body parsed as JSON. The bearer is read from the service's own .env on the host and
held in a local variable only.

COO half condition B: a 403 (tenant consent) or 409 (stale cached token, NeedsLogin) here is a
FINDING, not a rollback trigger. This program therefore reports the status rather than judging it.
"""
import json
import os
import re
import urllib.error
import urllib.request

os.chdir("/opt/opal-gateway")

BASE = "http://localhost:8080"
PATHS = [
    "/hx/teams/teams",
    "/hx/teams/teams/x/channels",
    "/hx/teams/channels/x/y/messages",
]

bearer = None
try:
    for line in open(".env", encoding="utf-8"):
        m = re.match(r"^TEAMS_BEARER=(.*)$", line.rstrip("\n").rstrip("\r"))
        if m:
            bearer = m.group(1)
            break
except OSError:
    bearer = None

R = {"bearer_present": bool(bearer), "results": {}}


def probe(path, with_bearer):
    url = BASE + path
    req = urllib.request.Request(url, method="GET")
    if with_bearer and bearer:
        req.add_header("Authorization", "Bearer " + bearer)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            out = {"status": resp.status, "bytes": len(body)}
            try:
                json.loads(body.decode("utf-8"))
                out["json"] = True
            except Exception:
                out["json"] = False
            return out
    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read()
        except Exception:
            pass
        out = {"status": e.code, "bytes": len(body)}
        # The refusal CODE is a short machine token ("unauthorized", "teams_route_not_configured",
        # a PathRefused reason). It carries no secret, so it is reported to make a 403/409 finding
        # actionable. Anything unexpectedly long is withheld.
        try:
            d = json.loads(body.decode("utf-8"))
            if isinstance(d, dict) and isinstance(d.get("error"), str) and len(d["error"]) <= 64:
                out["error"] = d["error"]
            out["json"] = True
        except Exception:
            out["json"] = False
        return out
    except Exception as e:
        return {"status": "ERR:" + type(e).__name__}


for p in PATHS:
    R["results"][p] = {
        "with_bearer": probe(p, True),
        "no_bearer": probe(p, False),
    }

print("AP7SERVEDJSON " + json.dumps(R, sort_keys=True))
