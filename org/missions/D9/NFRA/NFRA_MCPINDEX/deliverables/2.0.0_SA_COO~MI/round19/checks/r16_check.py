"""r16_check.py -- the MX-r-16 release candidate against the LIVE catalog (round 18's v3, git ref BASE_REF), from the repo root.

  python r16_check.py ac1   the difference control: candidate catalog C16_CATALOG (default infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml) against the live one
                            - the candidate holds every live row, and exactly four more: opal_data_bd_silver_{unrealized,transactions,allocations,fees}, each with bucket
                              opal-data-bd, prefix silver/<t>/, address blackdiamond/49f-live/silver/<t>/, read_tool the mapped client tool, vendor blackdiamond, firm 49financial;
                            - the eight frozen-copy rows (49financial_<t>_silver_legacy) differ from live in bucket (opal-data-bd -> opal-data-assets), prefix and key_template ONLY;
                            - every other live row is byte-equal, except the gold book row whose open_items lose exactly the MX-c-25 stale item (a row-level difference elsewhere is a defect, printed with its keys);
                            - exactly four rows carry `address`; the tool index lists the same tools; its `serves` equals the row-derived pairs (graded by c23.AC4 too)
  python r16_check.py ac2   the visibility difference control: vis_matrix.py (round 17) run under the live gateway tree and under the same tree with the candidate catalog placed:
                            opal-internal sees exactly the four more rows; the 49financial principal sees exactly those four more; every other principal sees nothing new; the
                            unknown and the empty firm see nothing; the eight re-bucketed rows keep their visibility; cross-firm leaks 0

Exit 0 PASS, 1 FAIL, 9 no run."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

BASE_REF = "38fe44d5cb"
GW = "infra/aws/ec2/opal-gateway"
CAT = os.environ.get("C16_CATALOG") or GW + "/app/refs/DATA_CATALOG.yaml"
HERE = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(HERE, "..", "..", "round17", "checks", "vis_matrix.py")
TOOLS = {"unrealized": "client_get_holdings", "transactions": "client_get_transactions", "allocations": "client_get_allocation", "fees": "client_get_fees"}
LEGACY = ["opal_data_assets_silver_49financial_%s_silver_legacy" % t for t in ("allocations", "assets", "fees", "prices", "realized", "transactions_enriched", "transactions", "unrealized")]
NEW = ["opal_data_bd_silver_" + t for t in TOOLS]
SECS = ("silver_datasets", "portal_datasets", "harvest_datasets")


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def rows(doc):
    return {r["entity"]: r for s in SECS for r in (doc.get(s) or []) if isinstance(r, dict) and r.get("entity")}


def base_doc():
    r = subprocess.run(["git", "show", "%s:%s/app/refs/DATA_CATALOG.yaml" % (BASE_REF, GW)], capture_output=True)
    if r.returncode != 0:
        print("ERROR: git show %s catalog rc %d" % (BASE_REF, r.returncode))
        sys.exit(9)
    return yaml.safe_load(r.stdout.decode("utf-8"))


def ac1():
    b, c = rows(base_doc()), None
    cand = yaml.safe_load(open(CAT, encoding="utf-8"))
    c = rows(cand)
    res = []
    added = sorted(set(c) - set(b))
    removed = sorted(set(b) - set(c))
    print("DENOMINATOR live rows %d; candidate rows %d; added %d; removed %d" % (len(b), len(c), len(added), len(removed)))
    res.append(("the candidate holds every live row and exactly the four live 49F rows more", not removed and added == sorted(NEW)))
    bad = []
    for t, tool in TOOLS.items():
        r = c.get("opal_data_bd_silver_" + t) or {}
        if not (r.get("bucket") == "opal-data-bd" and r.get("prefix") == "silver/%s/" % t and r.get("address") == "blackdiamond/49f-live/silver/%s/" % t
                and r.get("read_tool") == tool and r.get("vendor") == "blackdiamond" and r.get("firm") == "49financial" and not r.get("retired")):
            bad.append(t)
    res.append(("the four new rows carry bucket, prefix, address, read_tool, vendor, firm (wrong: %s)" % (",".join(bad) or "none"), not bad))
    leg_bad = []
    for e in LEGACY:
        x, y = b.get(e) or {}, c.get(e) or {}
        diff = sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
        if sorted(diff) != sorted(k for k in ("bucket", "prefix", "key_template") if k in set(x) | set(y) and x.get(k) != y.get(k)) or "bucket" not in diff \
                or y.get("bucket") != "opal-data-assets" or not str(y.get("prefix", "")).startswith("blackdiamond/49financial/silver_legacy/"):
            leg_bad.append((e, diff))
        elif set(diff) - {"bucket", "prefix", "key_template"}:
            leg_bad.append((e, diff))
    res.append(("the eight frozen-copy rows differ from live in bucket, prefix, key_template only (wrong: %d)" % len(leg_bad), not leg_bad))
    if leg_bad:
        for e, d in leg_bad[:3]:
            print("   legacy %s differs in %s" % (e, d))
    other = []
    for e in sorted(set(b) & set(c)):
        if e in LEGACY:
            continue
        if e == "opal_data_etfs_gold_book":   # MX-c-25: the one stale open_items item is gone and nothing else moved
            x = dict(b[e])
            y = dict(c[e])
            xo, yo = x.pop("open_items", []), y.pop("open_items", [])
            if x != y or yo != [i for i in xo if not ("implicitDeny" in str(i) and "gold/book" in str(i))] or len(yo) != len(xo) - 1:
                other.append((e, ["open_items beyond the MX-c-25 removal"]))
            continue
        if b[e] != c[e]:
            other.append((e, sorted(k for k in set(b[e]) | set(c[e]) if b[e].get(k) != c[e].get(k))))
    print("DENOMINATOR other live rows %d; differing %d" % (len(set(b) & set(c)) - len(LEGACY), len(other)))
    for e, d in other[:5]:
        print("   other %s differs in %s" % (e, d))
    res.append(("every other live row is byte-equal in the candidate (%d differ)" % len(other), not other))
    addr = sorted(e for e, r in c.items() if "address" in r)
    res.append(("exactly four rows carry `address` (%d)" % len(addr), addr == sorted(NEW)))
    tb = [e["tool"] for e in base_doc().get("tool_index") or []]
    tc = [e["tool"] for e in cand.get("tool_index") or []]
    res.append(("the tool index lists the same %d tools in the same order" % len(tb), tb == tc))
    return report(res)


def tree_with(candidate):
    d = tempfile.mkdtemp(prefix="r16_vis_")
    p = subprocess.run("git archive %s %s | tar -x -C %s" % (BASE_REF, GW, d.replace("\\", "/")), shell=True, capture_output=True)
    if p.returncode != 0:
        print("ERROR: git archive failed: %s" % p.stderr[-200:])
        sys.exit(9)
    root = os.path.join(d, GW)
    if candidate:
        shutil.copyfile(CAT, os.path.join(root, "app", "refs", "DATA_CATALOG.yaml"))
    return root


def matrix(root):
    r = subprocess.run([sys.executable, VIS, root], capture_output=True, text=True, timeout=250)
    line = (r.stdout or "").strip().splitlines()[-1:] or [""]
    try:
        return json.loads(line[0])
    except ValueError:
        print("ERROR: vis_matrix under %s rc %d: %s" % (root, r.returncode, (r.stderr or r.stdout)[-300:]))
        sys.exit(9)


def ac2():
    b, n = matrix(tree_with(False)), matrix(tree_with(True))
    principals = [k for k in b if k == "opal-internal" or k.startswith("firm:")]
    res = []
    newrows = {}
    for p in principals:
        newrows[p] = sorted(set(n[p]) - set(b[p]))
        lost = sorted(set(b[p]) - set(n[p]))
        if lost:
            res.append(("principal %s loses no row (%s)" % (p, ",".join(lost[:3])), False))
    res.append(("opal-internal sees exactly the four more rows (%d)" % len(newrows["opal-internal"]), newrows["opal-internal"] == sorted(NEW)))
    res.append(("firm:49financial sees exactly the four more rows (%d)" % len(newrows["firm:49financial"]), newrows["firm:49financial"] == sorted(NEW)))
    others = {p: v for p, v in newrows.items() if p not in ("opal-internal", "firm:49financial")}
    res.append(("no other principal sees a new row (%s)" % ",".join("%s=%d" % (p, len(v)) for p, v in others.items()), not any(others.values())))
    res.append(("the unknown and the empty firm see nothing", not n.get("firm:nosuchfirm") and not n.get("firm:")))
    keep = [e for e in LEGACY if e in b["opal-internal"]]
    res.append(("the eight re-bucketed rows keep their visibility to every principal", all((e in b[p]) == (e in n[p]) for e in keep for p in principals)))
    leaks = sum(1 for e in NEW for p in principals if p.startswith("firm:") and p != "firm:49financial" and e in n[p])
    print("DENOMINATOR silver rows base %d candidate %d x principals %d; newly visible per principal %s; cross-firm leaks %d"
          % (b["rows"], n["rows"], len(principals), {p: len(v) for p, v in newrows.items() if v}, leaks))
    res.append(("cross-firm leaks 0 (%d)" % leaks, leaks == 0))
    res.append(("no error in either run", not n.get("errors") and not b.get("errors")))
    return report(res)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
