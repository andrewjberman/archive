"""r1_check.py -- grades MX-c-20 / R1 (the six OG-ap-20 tools: read_tool on the rows they read, and the tool index covering the 99 tools the gateway serves
after that release), run from the repo root.

  python r1_check.py ac1   the table rows (workflows/atom_decomposition/catalog_entries/*.yaml): the rows that name one of the six tools are EXACTLY the
                           rows the tools' modules read (EXPECT below); each has tools == [read_tool] and gap_owner null; every OTHER row's read_tool, tools
                           and gap_owner equal those at BASE_REF; no row differs from BASE_REF in any other field
  python r1_check.py ac2   the tool index: the gateway tree AS RELEASED (git ref REF, ap-20) with the emitted catalog: c11_index.py exits 0 with PARTITION
                           sum N of N, N = 99, definitions located 99 of 99
  python r1_check.py ac3   the emitted catalog against the catalog at BASE_REF: only the 7 named rows, the tool_index section and built_at_git_head differ
                           (the 44 inferred tag rows and the 24 firm rows are intact), and the discover control c10_discover.py exits 0 on the released tree

R1_CATALOG overrides the emitted catalog path (default: the one in infra/aws/ec2/opal-gateway/app/refs/); R1_ENTRIES overrides the rows folder (planted arms).
Exit 0 PASS, 1 FAIL, 9 no run.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

BASE_REF = "5d19e142e9"      # the T1 + F1 catalog and rows, as landed
REF = "06cfb6db64"           # the OG-ap-20 release commit (the gateway tree after that release)
GW = "infra/aws/ec2/opal-gateway"
CATALOG = os.environ.get("R1_CATALOG") or GW + "/app/refs/DATA_CATALOG.yaml"
ENTRIES = os.environ.get("R1_ENTRIES") or "workflows/atom_decomposition/catalog_entries"
HERE = os.path.dirname(os.path.abspath(__file__))
C12 = os.path.join(HERE, "..", "..", "round12", "checks")
EXPECT = {
    "opal_data_etfs_gold_daily_partner_ownership": "etfs_get_partner_ownership",
    "opal_data_etfs_platinum_etf_ownership_dashboard": "etfs_get_ownership_rollup",
    "opal_data_etfs_platinum_monthly_ownership_report": "etfs_get_monthly_report",
    "opal_data_etfs_silver_netassets_daily": "etfs_get_fund_nav_history",
    "opal_data_etfs_gold_holding": "etfs_get_fund_holdings",
    "opal_data_etfs_silver_holdings": "etfs_get_fund_holdings",
    "opal_data_portal_v2_platinum_mdpf_category_views": "mdpf_get_category_views",
}
SIX = ("etfs_get_partner_ownership", "etfs_get_ownership_rollup", "etfs_get_monthly_report", "etfs_get_fund_nav_history", "etfs_get_fund_holdings",
       "mdpf_get_category_views")
SECTIONS = ("silver_datasets", "portal_datasets", "harvest_datasets")


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


def entry_rows(entries_dir):
    out = {}
    for p in sorted(glob.glob(os.path.join(entries_dir, "*.yaml"))):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        if isinstance(d, dict) and "contract" in d:
            out[os.path.basename(p)[:-5]] = d
    return out


def base_entries():
    ls = subprocess.run(["git", "ls-tree", "--name-only", BASE_REF, "workflows/atom_decomposition/catalog_entries/"], capture_output=True, text=True)
    out = {}
    for n in ls.stdout.split():
        if not n.endswith(".yaml"):
            continue
        d = yaml.safe_load(git_show(BASE_REF, n).decode("utf-8"))
        if isinstance(d, dict) and "contract" in d:
            out[os.path.basename(n)[:-5]] = d
    return out


def ac1():
    new, base = entry_rows(ENTRIES), base_entries()
    named = {e: d.get("read_tool") for e, d in new.items() if d.get("read_tool") in SIX}
    res = [("the rows naming one of the six tools are exactly the %d the modules read" % len(EXPECT), named == EXPECT),
           ("each names its tool with tools == [read_tool] and gap_owner null",
            all(new[e].get("tools") == [t] and new[e].get("gap_owner") is None for e, t in EXPECT.items() if e in new))]
    changed = sorted(e for e in new if new[e] != base.get(e))
    other = [e for e in changed if e not in EXPECT]
    odd = [e for e in changed if e in EXPECT and set(k for k in set(new[e]) | set(base[e]) if new[e].get(k) != base[e].get(k)) - {"read_tool", "tools", "gap_owner"}]
    res.append(("every other row equals its row at %s (%d rows differ outside the 7)" % (BASE_REF, len(other)), not other))
    res.append(("the 7 rows differ only in read_tool, tools and gap_owner", not odd and len(changed) == len(EXPECT)))
    print("DENOMINATOR table rows %d (base %d); rows differing from %s %d" % (len(new), len(base), BASE_REF, len(changed)))
    return report(res)


def released_tree():
    d = tempfile.mkdtemp(prefix="r1_tree_")
    p = subprocess.run("git archive %s %s | tar -x -C %s" % (REF, GW, d.replace("\\", "/")), shell=True, capture_output=True)
    if p.returncode != 0:
        print("ERROR: git archive %s failed: %s" % (REF, p.stderr[-200:]))
        sys.exit(9)
    root = os.path.join(d, GW)
    shutil.copyfile(CATALOG, os.path.join(root, "app", "refs", "DATA_CATALOG.yaml"))
    sh = open(os.path.join(root, "deploy-to-ec2.sh"), encoding="utf-8").read()
    m = re.search(r'ENABLED_INTEGRATIONS="([^"]*)"', sh)
    return root, (m.group(1).replace(",", " ") if m else "")


def run_py(script, args, root):
    env = dict(os.environ, MOCK_GRAPH="1")
    return subprocess.run([sys.executable, os.path.join(C12, script)] + args, env=env, cwd=root, capture_output=True, text=True, timeout=250)


def ac2():
    root, enabled = released_tree()
    r = run_py("c11_index.py", [root, os.path.join(root, "app", "refs", "DATA_CATALOG.yaml"), enabled], root)
    lines = [ln for ln in (r.stdout or "").splitlines() if ln.startswith(("SERVED", "PARTITION", "  MISSING"))]
    for ln in lines[:8]:
        print(ln[:230])
    part = next((ln for ln in lines if ln.startswith("PARTITION")), "")
    m = re.search(r"sum (\d+) of N=(\d+); definitions located (\d+) of (\d+)", part)
    ok = bool(m) and m.group(1) == m.group(2) == m.group(3) == m.group(4) == "99"
    return report([("c11_index exits 0 (rc=%d)" % r.returncode, r.returncode == 0), ("PARTITION sum 99 of N=99 and definitions located 99 of 99", ok)])


def ac3():
    new = yaml.safe_load(open(CATALOG, encoding="ascii", errors="replace").read())
    base = yaml.safe_load(git_show(BASE_REF, GW + "/app/refs/DATA_CATALOG.yaml").decode("ascii"))
    res = []
    top = sorted(k for k in set(new) | set(base) if k not in SECTIONS and new.get(k) != base.get(k))
    res.append(("top-level sections differ only in tool_index and built_at_git_head (%s)" % ",".join(top), set(top) <= {"tool_index", "built_at_git_head"}))
    diffs = {}
    for sec in SECTIONS:
        o, n = {r["entity"]: r for r in base[sec]}, {r["entity"]: r for r in new[sec]}
        res.append(("%s: the same %d rows" % (sec, len(o)), sorted(o) == sorted(n)))
        for e in o:
            if e in n and o[e] != n[e]:
                diffs[e] = sorted(k for k in set(o[e]) | set(n[e]) if o[e].get(k) != n[e].get(k))
    odd = {e: f for e, f in diffs.items() if e not in EXPECT or set(f) - {"read_tool", "tools", "gap", "gap_owner"}}
    res.append(("only the 7 rows differ, in read_tool, tools and gap fields (%d differ, %d outside)" % (len(diffs), len(odd)), len(diffs) == len(EXPECT) and not odd))
    rows = [r for s in SECTIONS for r in new[s]]
    res.append(("tags and firm fields intact: nl_tags %d, inferred %d, firm %d" % (sum(1 for r in rows if r.get("nl_tags")), sum(1 for r in rows if r.get("nl_tags_basis") == "inferred"),
                                                                                  sum(1 for r in rows if r.get("firm"))),
                sum(1 for r in rows if r.get("nl_tags")) == 304 and sum(1 for r in rows if r.get("nl_tags_basis") == "inferred") == 44 and sum(1 for r in rows if r.get("firm")) == 24))
    root, _en = released_tree()
    r = run_py("c10_discover.py", [root], root)
    for ln in (r.stdout or "").splitlines()[-4:]:
        print(ln[:200])
    res.append(("c10_discover exits 0 on the released tree (rc=%d)" % r.returncode, r.returncode == 0))
    return report(res)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
