"""c30_check.py -- grades MX-c-30 (NFRA_MCPINDEX round 18, workstream RESEARCH): the two advisor-intelligence rows out of the catalog, and (at the drain)
CONTRACT C-GROUP item 1 `bucket` on the RESEARCH row set. Run from the repo root.

  python c30_check.py scope    AC1: the two advisor-intelligence rows are gone from the row files and from the emitted catalog, a fresh generator run writes 214 rows
                               and neither file, every one of the 214 equals the committed file of the same name (the difference control), and no remaining row
                               sits under platinum/advi/ or platinum/irpt/
  python c30_check.py tests    AC2: the new test file exists, passes, and collects at least 5 tests
  python c30_check.py bucket   DRAIN (the issuer's, on the catalog emitted with the ASSETS emitter MX-c-21 and its group map): every RESEARCH-set row carries a
                               `bucket` in the C-GROUP spelling (an S3 bucket name `opal-data-*`, or the store name `dynamodb`); the 10 dynamodb rows say `dynamodb`;
                               the 5 portal_datasets rows say `opal-data-portal-v2`; every other RESEARCH row keeps its base value; no RESEARCH row is still `inferred` (the curated tags replace them); every row outside the set differs
                               from BASE_REF only in the keys the ASSETS cells add (bucket, vendor, firm, nl_tags, nl_tags_basis, read_tool, tools, gap_owner)

C30_CATALOG overrides the emitted catalog path, C30_ENTRIES the row folder (planted arms). Exit 0 PASS, 1 FAIL, 9 no run.
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

import yaml

BASE_REF = "5858411c5c"      # HEAD at the cut: the committed catalog and rows the cell starts from
GW = "infra/aws/ec2/opal-gateway"
CATALOG = os.environ.get("C30_CATALOG") or GW + "/app/refs/DATA_CATALOG.yaml"
ENTRIES = os.environ.get("C30_ENTRIES") or "workflows/atom_decomposition/catalog_entries"
HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables"
PIN = DELIV + "/0.9.0_WK_NFRA_MCPINDEX~38"
R17 = DELIV + "/2.0.0_SA_COO~MI/round17"
RESEARCH_PREFIX = ("opal_data_etfs_", "opal_data_mdpf_", "opal_data_news_", "opal_data_portal_v2_", "dynamodb_")
DROPPED = ("opal_data_portal_v2_platinum_advi_49financial_perfrp", "opal_data_portal_v2_platinum_advi_49financial_twins")
S3_SPELLING = re.compile(r"^opal-data-[a-z0-9]+(-[a-z0-9]+)*$")
STORES = ("dynamodb", "graph")
NEW_TESTS = ("workflows/atom_decomposition/tests/test_scope_exclusions.py",)


def git_show(ref, path):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        print("ERROR: git show %s:%s rc %d" % (ref, path, r.returncode))
        sys.exit(9)
    return r.stdout


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def load_catalog():
    return yaml.safe_load(open(CATALOG, encoding="utf-8", errors="replace").read())


def base_catalog():
    return yaml.safe_load(git_show(BASE_REF, GW + "/app/refs/DATA_CATALOG.yaml").decode("utf-8", errors="replace"))


def in_set(section, row):
    if section in ("harvest_datasets", "portal_datasets"):
        return True
    return str(row.get("entity", "")).startswith(RESEARCH_PREFIX)


def bucket():
    new, base = load_catalog(), base_catalog()
    bnew = {(s, r["entity"]): r for s in ("silver_datasets", "portal_datasets", "harvest_datasets") for r in new.get(s, [])}
    bold = {(s, r["entity"]): r for s in ("silver_datasets", "portal_datasets", "harvest_datasets") for r in base.get(s, [])}
    graded = {k: r for k, r in bnew.items() if in_set(k[0], r)}
    bad_spelling = [k[1] for k, r in graded.items() if not (isinstance(r.get("bucket"), str) and (S3_SPELLING.match(r["bucket"]) or r["bucket"] in STORES))]
    dyn = [k[1] for k, r in graded.items() if k[1].startswith("dynamodb_") and r.get("bucket") != "dynamodb"]
    port = [k[1] for k, r in graded.items() if k[0] == "portal_datasets" and r.get("bucket") != "opal-data-portal-v2"]
    moved = [k[1] for k, r in graded.items()
             if not k[1].startswith("dynamodb_") and k[0] != "portal_datasets" and k in bold and bold[k].get("bucket") != r.get("bucket")]
    outside = [k for k, r in bnew.items() if not in_set(k[0], r)]
    assets_keys = {"bucket", "vendor", "firm", "nl_tags", "nl_tags_basis", "read_tool", "tools", "gap_owner", "gap"}
    drift = [k[1] for k in outside if k in bold and sorted(f for f in set(bnew[k]) | set(bold[k]) if bnew[k].get(f) != bold[k].get(f) and f not in assets_keys)]
    # the rows the cell may change: the research set only (bucket on 15, and the 2 dropped)
    top_new = {k: v for k, v in new.items() if k not in ("silver_datasets", "portal_datasets", "harvest_datasets", "built_at_git_head", "supersedes", "tool_index")}
    top_old = {k: v for k, v in base.items() if k not in ("silver_datasets", "portal_datasets", "harvest_datasets", "built_at_git_head", "supersedes", "tool_index")}
    top_diff = sorted(k for k in set(top_new) | set(top_old) if top_new.get(k) != top_old.get(k))
    print("DENOMINATOR research-set rows graded %d (harvest %d, portal %d, silver %d); rows outside the set %d"
          % (len(graded), sum(1 for k in graded if k[0] == "harvest_datasets"), sum(1 for k in graded if k[0] == "portal_datasets"),
             sum(1 for k in graded if k[0] == "silver_datasets"), len(outside)))
    other_fields = [k[1] for k, r in graded.items() if k in bold and
                    sorted(f for f in set(r) | set(bold[k]) if f not in ("bucket", "nl_tags", "nl_tags_basis") and r.get(f) != bold[k].get(f))]
    still_inferred = [k[1] for k, r in graded.items() if r.get("nl_tags_basis") == "inferred"]
    res = [("every research-set row's bucket is an opal-data-* name or a store name (%d do not)" % len(bad_spelling), not bad_spelling),
           ("the 10 dynamodb rows say dynamodb (%d do not)" % len(dyn), not dyn and sum(1 for k in graded if k[1].startswith("dynamodb_")) == 10),
           ("the 5 portal_datasets rows say opal-data-portal-v2 (%d do not)" % len(port), not port and sum(1 for k in graded if k[0] == "portal_datasets") == 5),
           ("every other research-set row keeps its base bucket (%d moved)" % len(moved), not moved),
           ("the research rows differ from base only in bucket and the curated tags (%d rows differ elsewhere)" % len(other_fields), not other_fields),
           ("no research-set row still carries inferred tags (%d do)" % len(still_inferred), not still_inferred),
           ("every row outside the set differs from %s only in the ASSETS cells' keys (%d differ otherwise)" % (BASE_REF, len(drift)), not drift),
           ("the top-level sections other than the three row sections and the tool index (the ASSETS issuer's) are unchanged (%s)" % ",".join(top_diff), not top_diff)]
    return report(res)


def entry_names():
    return sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ENTRIES, "*.yaml")))


def scope():
    names = entry_names()
    cat = load_catalog()
    ents = [r["entity"] for s in ("silver_datasets", "portal_datasets", "harvest_datasets") for r in cat.get(s, [])]
    under = [r["entity"] for r in cat.get("silver_datasets", []) if str(r.get("prefix") or "").startswith(("platinum/advi/", "platinum/irpt/"))]
    tmp = tempfile.mkdtemp(prefix="c30_gen_")
    cmd = [sys.executable, "workflows/atom_decomposition/gen_silver_rows.py",
           "--g2", PIN + "/G2_pinned.md", "--g4", PIN + "/G4_pinned.md", "--g5", PIN + "/G5_pinned.md", "--g6", PIN + "/G6_pinned.md",
           "--g3", PIN + "/G3_pinned.md", "--g2f", PIN + "/G2f_pinned.md", "--out", tmp,
           "--deployed-tools", R17 + "/deployed_ap20.json", "--firm-map", R17 + "/f1_firm_map.json"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"wrote (\d+) rows", out)
    wrote = int(m.group(1)) if m else -1
    made = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(tmp, "*.yaml")))
    unequal = [n for n in made if not os.path.isfile(os.path.join(ENTRIES, n + ".yaml")) or
               open(os.path.join(tmp, n + ".yaml"), "rb").read() != open(os.path.join(ENTRIES, n + ".yaml"), "rb").read()]
    print("DENOMINATOR row files %d; catalog entities %d; generator wrote %d (rc=%d)" % (len(names), len(ents), wrote, r.returncode))
    res = [("neither advisor-intelligence row file is in the row folder", not [n for n in DROPPED if n in names]),
           ("neither is an entity of the emitted catalog", not [n for n in DROPPED if n in ents]),
           ("a fresh generator run exits 0 and writes 214 rows (rc=%d, wrote %d)" % (r.returncode, wrote), r.returncode == 0 and wrote == 214),
           ("the fresh run wrote neither file", not [n for n in DROPPED if n in made]),
           ("every file the fresh run wrote equals the committed file of the same name (%d differ)" % len(unequal), not unequal),
           ("no emitted silver row sits under platinum/advi/ or platinum/irpt/ (%d do)" % len(under), not under)]
    return report(res)


def tests():
    missing = [t for t in NEW_TESTS if not os.path.isfile(t)]
    if missing:
        print("DENOMINATOR new test files present 0 of 1")
        return report([("the new test file exists", False)])
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + list(NEW_TESTS), capture_output=True, text=True, timeout=250)
    tail = [ln for ln in (r.stdout or "").splitlines() if ln.strip()][-3:]
    for ln in tail:
        print(ln[:200])
    m = re.search(r"(\d+) passed", r.stdout or "")
    passed = int(m.group(1)) if m else 0
    failed = bool(re.search(r"\d+ (failed|error)", r.stdout or ""))
    print("DENOMINATOR new test files 1; tests passed %d" % passed)
    return report([("pytest rc=0 (rc=%d)" % r.returncode, r.returncode == 0 and not failed),
                   ("at least 5 tests passed (%d)" % passed, passed >= 5)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("scope", "tests", "bucket"):
        print(__doc__)
        return 9
    return {"scope": scope, "tests": tests, "bucket": bucket}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
