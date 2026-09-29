"""discover_probe.py -- round-4 helper: call the opal_discover integration IN-PROCESS on the tree's own catalog, as the
opal-internal principal, and print what a criterion needs. No network call is required for (route); (written) reports
whatever served_written_at carries, including `absent` when no S3 read is possible.

usage (from the gateway dir):  python discover_probe.py route "<ask>" <entity-prefix>
                               python discover_probe.py written "<ask>" ["<ask>" ...]
                               python discover_probe.py first "<ask>"
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from app.graphql_plumbing import catalog_gate                      # noqa: E402
from app.integrations.opal_discover import integration as od       # noqa: E402

P = catalog_gate.OPAL_INTERNAL


def route(ask, entity_prefix):
    ans = od.discover(ask, P)
    for m in ans.get("matches") or []:
        if str(m.get("property", {}).get("entity", "")).startswith(entity_prefix):
            nt = m.get("next_tool") or {}
            print("match %s next_tool=%s args=%s" % (m["property"]["entity"], nt.get("name"), json.dumps(nt.get("args"), sort_keys=True)))
            return 0
    print("no match with entity prefix %s among %d matches" % (entity_prefix, len(ans.get("matches") or [])))
    return 1


def written(asks):
    n = ok = 0
    bad = []
    for ask in asks:
        for m in od.discover(ask, P).get("matches") or []:
            if not m.get("servable"):
                continue
            n += 1
            sw = (m.get("freshness") or {}).get("served_written_at")
            claim = sw.get("claim") if isinstance(sw, dict) else None
            if claim == "measured" and sw.get("value"):
                ok += 1
            elif claim == "absent" and sw.get("error_class"):
                ok += 1
            else:
                bad.append("%s: %s" % (m.get("dataset"), json.dumps(sw)[:120]))
    for b in bad[:10]:
        print("  missing or unclaimed: " + b)
    print("servable rows carrying served_written_at (measured, or absent with error_class): %d of %d" % (ok, n))
    return 0 if (n >= 1 and ok == n) else 1


def first(ask):
    ans = od.discover(ask, P)
    ms = ans.get("matches") or []
    print("catalogued=%s first=%s" % (ans.get("catalogued"), ms[0].get("dataset") if ms else "NONE"))
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "route":
        sys.exit(route(sys.argv[2], sys.argv[3]))
    if cmd == "written":
        sys.exit(written(sys.argv[2:]))
    if cmd == "first":
        sys.exit(first(sys.argv[2]))
    sys.exit(2)
