"""Issuer's check for NFRA_CTLPLN.TO-CT-i-11 (round 6, workstream INBOUND): the gateway's GET allowlist admits exactly the
three channel-read Graph paths, still refuses a neighbour path and any new POST, and the app mounts the three contract routes
GET-only. Offline: imports the app with MOCK_GRAPH; no network. Last line: CONTRACT-CT-i-11 ok=<True|False>."""
from __future__ import annotations

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 8)))
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway")
sys.path.insert(0, GW)
os.environ.setdefault("MOCK_GRAPH", "1")

TEAM = "9c4ab816-548f-47af-913c-ad5d5086f5ad"
CHANNEL = "19:abcdef0123@thread.tacv2"
WANT_GRAPH = ["/me/joinedTeams", "/teams/%s/channels" % TEAM, "/teams/%s/channels/%s/messages" % (TEAM, CHANNEL)]
WANT_ROUTES = ["/hx/teams/teams", "/hx/teams/teams/{team_id}/channels", "/hx/teams/channels/{team_id}/{channel_id}/messages"]


def main() -> int:
    checks = []
    try:
        from app import teams_route as t
        from app import server
    except Exception as exc:  # noqa: BLE001 -- an import failure is a FAIL, printed
        print("import failed: %s" % type(exc).__name__)
        print("CONTRACT-CT-i-11 ok=False")
        return 1
    for p in WANT_GRAPH:
        checks.append(("get-allows %s" % p, any(rx.match(p) for rx in t._GET_ALLOWED)))
        checks.append(("post-refuses %s" % p, not any(rx.match(p) for rx in t._POST_ALLOWED)))
    checks.append(("get-refuses members", not any(rx.match("/teams/%s/members" % TEAM) for rx in t._GET_ALLOWED)))
    mounted = {getattr(r, "path", None): set(getattr(r, "methods", None) or ()) for r in server.app.routes}
    for r in WANT_ROUTES:
        methods = mounted.get(r)
        checks.append(("mounted %s" % r, methods is not None))
        checks.append(("get-only %s" % r, methods is not None and "POST" not in methods))
    for name, ok in checks:
        print("CHECK %s ok=%s" % (name, ok))
    ok = all(v for _, v in checks)
    print("CONTRACT-CT-i-11 ok=%s" % ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
