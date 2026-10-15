"""c23_check.py -- grades MX-c-23 (ASSETS: C-GROUP item 2 on every opal-data-assets and opal-data-bd row, and the 12 Schwab dim_* rows), from the repo root.

  python c23_check.py ac1   the emitted catalog (infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml, or C23_CATALOG): every entity of the issuer's map (with its curated nl_tags where the map gives them, and no nl_tags_basis)
                            org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round18/assets_group_map.json (136) is a row carrying bucket, vendor and firm equal to the map;
                            no other row carries a vendor; vendor and firm values are inside the C-GROUP lists; the registry catalog_fork_keys.json holds every vendor and firm value in its `labels` list
  python c23_check.py ac2   the 12 Schwab dim_* rows (4 tables x masters 08242234, 08335338, 08403355): present, bucket opal-data-assets, vendor schwab, firm 49financial, read_tool null,
                            gap_owner NFRA_OPLGTW, a key_template, not retired; the table rows number the base's plus 12 minus the rows removed (an ASSETS row is never removed: RESEARCH's scope drop may remove others);
                            against the catalog at BASE_REF every other table row differs only in bucket, vendor, firm and the curated tags
  python c23_check.py ac4   the `serves` field (PRD v0.17 C-GROUP item 2, amended by the CTO @5ba12d1de5): every tool_index entry that catalog rows of the opal-data-assets or opal-data-bd buckets name as read_tool carries
                            `serves`, the sorted list of the DISTINCT {vendor, firm} pairs of those rows; an entry with no such row carries no `serves`; the list equals the row-derived set for every tool
  python c23_check.py ac3   the visibility difference control (vis_matrix.py, BASE tree against the NEW tree): each known firm sees its old rows plus exactly the firm-scoped rows whose firm it is; no row is
                            visible to another firm; multi, none and unresolved rows are visible to no firm principal; unknown and empty firm see nothing; opal-internal sees every row. Prints the pair
                            count and the newly-visible count per firm

The NEW gateway tree is infra/aws/ec2/opal-gateway of the worktree (or C23_GW). Exit 0 PASS, 1 FAIL, 9 no run."""
import json
import os
import subprocess
import sys
import tempfile

import yaml

BASE_REF = "c4c106aea1"
GW = "infra/aws/ec2/opal-gateway"
NEWGW = os.environ.get("C23_GW") or GW
CATALOG = os.environ.get("C23_CATALOG") or GW + "/app/refs/DATA_CATALOG.yaml"
MAP = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round18/assets_group_map.json"
REG = "infra/logic/registry/catalog_fork_keys.json"
HERE = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(HERE, "..", "..", "round17", "checks", "vis_matrix.py")
VENDORS = ("schwab", "blackdiamond", "orion", "eclipse", "smartx", "commonwealth", "gateway", "market")
FIRMS = ("49financial", "cottonwood", "inflection", "multi", "none", "unresolved")
KNOWN = ("49financial", "inflection", "cottonwood")
NEW12 = ["opal_data_assets_silver_schwab_%s_dim_%s" % (m, t) for m in ("08242234", "08335338", "08403355") for t in ("asset", "balance", "position", "transaction")]


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def load(path):
    with open(path, encoding="ascii") as fh:
        return yaml.safe_load(fh)


def table_rows(cat):
    return {r["entity"]: r for sec in ("silver_datasets", "portal_datasets") for r in (cat.get(sec) or []) if isinstance(r, dict) and r.get("entity")}


def all_rows(cat):
    return {r["entity"]: r for sec in ("silver_datasets", "portal_datasets", "harvest_datasets") for r in (cat.get(sec) or []) if isinstance(r, dict) and r.get("entity")}


def base_cat():
    r = subprocess.run(["git", "show", "%s:%s/app/refs/DATA_CATALOG.yaml" % (BASE_REF, GW)], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        print("ERROR: git show base rc %d" % r.returncode)
        sys.exit(9)
    p = os.path.join(tempfile.mkdtemp(prefix="c23_"), "base.yaml")
    open(p, "wb").write(r.stdout)
    return load(p)


def ac1():
    want = json.load(open(MAP, encoding="utf-8"))["rows"]
    rows = table_rows(load(CATALOG))
    reg = json.loads(os.environ["C23_REG_OVERRIDE"]) if os.environ.get("C23_REG_OVERRIDE") else json.load(open(REG, encoding="utf-8"))   # the override is the issuer's planted-arm hook
    labels = set(reg.get("labels") or [])
    wrong = [e for e, w in want.items() if e not in rows or any(rows[e].get(k) != w[k] for k in ("bucket", "vendor", "firm"))
             or ("nl_tags" in w and (rows[e].get("nl_tags") != w["nl_tags"] or "nl_tags_basis" in rows[e]))]
    inferred = sorted(e for e in want if (rows.get(e) or {}).get("nl_tags_basis") == "inferred")
    stray = sorted(e for e, r in all_rows(load(CATALOG)).items() if e not in want and (r.get("vendor") is not None or r.get("bucket") in ("opal-data-assets", "opal-data-bd")))
    badval = sorted(e for e, r in rows.items() if r.get("vendor") not in (None,) + VENDORS or (r.get("vendor") and r.get("firm") not in FIRMS))
    need = {w[k] for w in want.values() for k in ("vendor", "firm")}
    print("DENOMINATOR map entities %d; rows equal to the map %d; stray rows %d; values outside the lists %d; registry labels %d (need %d); ASSETS rows still inferred %d" %
          (len(want), len(want) - len(wrong), len(stray), len(badval), len(labels), len(need), len(inferred)))
    for e in wrong[:5]:
        print("  WRONG %s: %s" % (e, {k: (rows.get(e) or {}).get(k) for k in ("bucket", "vendor", "firm")}))
    return report([("all %d map entities are rows equal to the map" % len(want), len(want) == 136 and not wrong), ("no other row carries a vendor or an assets bucket", not stray),
                   ("every vendor and firm value is inside the C-GROUP lists", not badval), ("the registry labels list holds every vendor and firm value", need <= labels), ("no ASSETS row still carries inferred tags (Z-C-S61)", not inferred)])


def ac2():
    cat = load(CATALOG)
    rows = table_rows(cat)
    base = table_rows(base_cat())
    missing = [e for e in NEW12 if e not in rows]
    bad = []
    for e in NEW12:
        r = rows.get(e)
        if r and not (r.get("bucket") == "opal-data-assets" and r.get("vendor") == "schwab" and r.get("firm") == "49financial" and r.get("read_tool") is None and r.get("gap_owner") == "NFRA_OPLGTW"
                      and r.get("key_template") and r.get("retired") is False):
            bad.append(e)
    n_table = sum(1 for r in rows.values() if "contract" in r)
    removed = sorted(set(base) - set(rows))
    removed_assets = [e for e in removed if e in json.load(open(MAP, encoding="utf-8"))["rows"]]
    base_table = sum(1 for r in base.values() if "contract" in r)
    odd = []
    for e, r in base.items():
        if e in rows:
            diff = set(k for k in set(r) | set(rows[e]) if r.get(k) != rows[e].get(k))
            if diff - {"bucket", "vendor", "firm", "nl_tags", "nl_tags_basis"}:
                odd.append((e, sorted(diff)))
    extra = sorted(set(rows) - set(base) - set(NEW12))
    print("DENOMINATOR new rows present %d of 12; wrong %d; table rows %d (base %d + 12 - removed %d); base rows changed outside bucket/vendor/firm %d; unexpected new rows %d" %
          (12 - len(missing), len(bad), n_table, base_table, len(removed), len(odd), len(extra)))
    for o in odd[:5]:
        print("  ODD %s" % (o,))
    return report([("the 12 Schwab dim_* rows are present", not missing), ("each carries the expected fields", not bad), ("the table rows number the base's plus 12 minus the removed (%d)" % len(removed), n_table == base_table + 12 - len([e for e in removed if "contract" in base[e]])),
                   ("no ASSETS row was removed (%d)" % len(removed_assets), not removed_assets),
                   ("every other row differs from the base only in bucket, vendor, firm and the curated tags", not odd), ("no other row was added", not extra)])


def matrix(root):
    r = subprocess.run([sys.executable, VIS, root], capture_output=True, text=True, timeout=250)
    line = (r.stdout or "").strip().splitlines()[-1:] or [""]
    try:
        return json.loads(line[0])
    except ValueError:
        print("ERROR: vis_matrix under %s rc %d: %s" % (root, r.returncode, (r.stderr or r.stdout)[-300:]))
        sys.exit(9)


def ac3():
    d = tempfile.mkdtemp(prefix="c23_base_")
    p = subprocess.run("git archive %s %s | tar -x -C %s" % (BASE_REF, GW, d.replace("\\", "/")), shell=True, capture_output=True)
    if p.returncode != 0:
        print("ERROR: git archive failed")
        return 9
    b, n = matrix(os.path.join(d, GW)), matrix(os.path.abspath(NEWGW))
    rows = table_rows(load(os.path.join(NEWGW, "app", "refs", "DATA_CATALOG.yaml")))
    removed_silver = len(set(e for e in table_rows(base_cat()) if e not in rows))
    res = [("the silver row sets differ only by the 12 new rows less the %d removed" % removed_silver, n["rows"] == b["rows"] + 12 - removed_silver), ("opal-internal sees every row", len(n["opal-internal"]) == n["rows"]),
           ("the unknown and the empty firm see nothing", not n["firm:nosuchfirm"] and not n["firm:"]), ("no error in either run", not n.get("errors") and not b.get("errors"))]
    leaks = 0
    newly = 0
    for f in KNOWN:
        key = "firm:" + f
        expect = {e for e, r in rows.items() if r.get("firm") == f and r.get("firm_scope_rule") == "firm-scoped" and e in n["opal-internal"]}
        got = set(n[key])
        newly += len(got - set(b[key]))
        leaks += sum(1 for e in got if rows.get(e, {}).get("firm") not in (f, None) and e not in b[key])
        res.append(("firm %s sees its old %d rows plus exactly its %d firm-scoped rows" % (f, len(b[key]), len(expect)), got == set(b[key]) | expect))
    hidden = sorted(e for e, r in rows.items() if r.get("firm") in ("multi", "none", "unresolved") and any(e in n["firm:" + f] and e not in b["firm:" + f] for f in KNOWN))
    res.append(("multi, none and unresolved rows are visible to no firm principal (%d seen)" % len(hidden), not hidden))
    res.append(("no row is newly visible to a firm other than its own (leaks %d)" % leaks, leaks == 0))
    print("DENOMINATOR silver rows %d x principals 6 = %d pairs; newly visible (summed over firms) %d; cross-firm leaks %d" % (n["rows"], n["rows"] * 6, newly, leaks))
    return report(res)


def ac4():
    cat = load(CATALOG)
    rows = all_rows(cat)
    pairs = {}
    for r in rows.values():
        if r.get("read_tool") and r.get("bucket") in ("opal-data-assets", "opal-data-bd") and r.get("vendor") and r.get("firm"):
            pairs.setdefault(r["read_tool"], set()).add((r["vendor"], r["firm"]))
    bad = []
    n_with = 0
    for e in cat.get("tool_index") or []:
        t = e.get("tool")
        want = [{"vendor": v, "firm": f} for v, f in sorted(pairs.get(t, ()))]
        if want:
            n_with += 1
            if e.get("serves") != want:
                bad.append("%s: %r != %r" % (t, e.get("serves"), want))
        elif "serves" in e:
            bad.append("%s: serves on a tool no assets or bd row names" % t)
    print("DENOMINATOR tool_index entries %d; with assets or bd rows %d; serves wrong %d" % (len(cat.get("tool_index") or []), n_with, len(bad)))
    for b in bad[:5]:
        print("  BAD %s" % b)
    return report([("every tool the assets and bd rows name carries serves equal to the row-derived pairs (%d of %d)" % (n_with - len([b for b in bad if "serves on" not in b]), n_with), n_with > 0 and not bad)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3", "ac4"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3, "ac4": ac4}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
