"""r6_probe.py -- NFRA_MCPINDEX round-6 check helper (2.0.0_SA_COO~MI). In-process on the CHECKED-OUT gateway tree.

usage (cwd = the gateway dir, infra/aws/ec2/opal-gateway):
  python r6_probe.py route     discover names blackdiamond_list_fees for the BD fees ask and a schwab_* tool for
                               "Schwab positions"
  python r6_probe.py control   "ETF positioning" still names etfs_get_positioning (the MX-t-10 control)
  python r6_probe.py reach     every catalog row that names a read tool is REACHABLE: discover, asked each of the
                               row's example_questions, names that tool for at least one of them
Prints one line per ask/row and a denominator; exit 0 only when every line holds.
discover may HEAD served S3 objects (MX-d-4's served_written_at); the routing answer does not depend on it.
"""
import os
import sys

sys.path.insert(0, os.getcwd())

from app.graphql_plumbing import catalog_gate  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

P = catalog_gate.OPAL_INTERNAL


def _named(question):
    ans = od.discover(question, P)
    return ans.get("catalogued"), [((m.get("next_tool") or {}).get("name")) for m in ans.get("matches", [])]


def _schwab_tools():
    try:
        from app.integrations.schwab import integration as sw
        return set(getattr(sw, "TOOL_NAMES", ()) or ())
    except Exception as exc:  # the schwab package must import for this check to mean anything
        print("ERROR: schwab integration does not import: %s" % exc)
        return set()


def route():
    ok = []
    cat, names = _named("what fees did Black Diamond charge")
    hit = "blackdiamond_list_fees" in names
    print("%s BD fees ask: catalogued=%r next_tools=%s (want blackdiamond_list_fees)" % ("OK:" if hit else "MISSING:", cat, names))
    ok.append(hit)
    sw = _schwab_tools()
    cat, names = _named("Schwab positions")
    hit = bool(sw) and any(n in sw for n in names)
    print("%s Schwab positions ask: catalogued=%r next_tools=%s (want one of %s)" % ("OK:" if hit else "MISSING:", cat, names, sorted(sw)))
    ok.append(hit)
    print("routed %d of %d asks" % (sum(ok), len(ok)))
    return all(ok)


def control():
    cat, names = _named("ETF positioning")
    hit = "etfs_get_positioning" in names
    print("%s ETF positioning ask: catalogued=%r next_tools=%s" % ("OK:" if hit else "MISSING:", cat, names))
    return hit


def reach():
    import yaml
    with open("app/refs/DATA_CATALOG.yaml", encoding="utf-8") as f:
        cat = yaml.safe_load(f) or {}
    rows = []
    for sec, entries in cat.items():
        if not isinstance(entries, list):
            continue
        for r in entries:
            if isinstance(r, dict) and r.get("read_tool"):
                rows.append((sec, r))
    bad = 0
    for sec, r in rows:
        tool = r.get("read_tool")
        qs = [q for q in (r.get("example_questions") or []) if isinstance(q, str)]
        hit_q = None
        for q in qs:
            if tool in _named(q)[1]:
                hit_q = q
                break
        if hit_q is None:
            bad += 1
        print("%s %s/%s read_tool=%s asked %d example question(s)%s" % (
            "OK:" if hit_q else "UNREACHABLE:", sec, r.get("entity"), tool, len(qs),
            (" -- routed by %r" % hit_q) if hit_q else ""))
    print("REACHABILITY: %d of %d catalog rows naming a read tool are reachable through discover" % (len(rows) - bad, len(rows)))
    return len(rows) > 0 and bad == 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"route": route, "control": control, "reach": reach}.get(mode)
    if fn is None:
        print(__doc__)
        sys.exit(2)
    sys.exit(0 if fn() else 1)
