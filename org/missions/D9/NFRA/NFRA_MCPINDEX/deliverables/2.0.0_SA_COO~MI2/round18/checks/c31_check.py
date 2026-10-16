"""c31_check.py -- grades MX-c-31 (NFRA_MCPINDEX round 18, workstream RESEARCH): the generator's --read-links, which gives 27 RESEARCH rows the one tool that reads
them, each link taking effect only when its tool is in the deployed-tools list. Run from the repo root.

  python c31_check.py live     AC1: with the 99 tools the gateway serves today, EXACTLY the 6 rows whose tool is live now are linked in the committed row files (each changes
                               only read_tool null -> its tool, tools [] -> [tool], gap_owner -> null, against BASE_REF); every other row file equals its row at BASE_REF
  python c31_check.py future   AC2: a fresh generator run with the deployed list extended by the 14 tools that are built but not yet live links EXACTLY the 27 rows (the
                               6 plus 21 more) to the tools of read_links.json, and changes no other row's read_tool; 13 of the 27 links also equal NFRA_OPLGTW's own
                               classification (OG-gp-1 worker 109, OG-gf-1 worker 110); and the same run with today's 99 tools links only the 6
  python c31_check.py tests    AC3: the new test file exists, passes, and collects at least 6 tests

Exit 0 PASS, 1 FAIL, 9 no run.
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

import yaml

BASE_REF = "6321876e2e"
ENTRIES = os.environ.get("C31_ENTRIES") or "workflows/atom_decomposition/catalog_entries"
LINKS = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI2/round18/read_links.json"
HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables"
PIN = DELIV + "/0.9.0_WK_NFRA_MCPINDEX~38"
R17 = DELIV + "/2.0.0_SA_COO~MI/round17"
R18 = DELIV + "/2.0.0_SA_COO~MI2/round18"
CLASS = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~%d/CLASSIFICATION.json"
LIVE_NOW = ("opal_data_portal_v2_platinum_etfs_positioning_data", "opal_data_portal_v2_platinum_mdpf_account_distribution",
            "opal_data_portal_v2_platinum_mdpf_aggregate_aua_timeseries", "opal_data_portal_v2_platinum_mdpf_aum_metrics",
            "opal_data_portal_v2_served_model_portfolio_benchmarks", "opal_data_portal_v2_served_sentiment_singletons")
NEW_TESTS = ("workflows/atom_decomposition/tests/test_read_links.py",)


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def git_show(ref, path):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        print("ERROR: git show %s:%s rc %d" % (ref, path, r.returncode))
        sys.exit(9)
    return r.stdout


def entry_rows(folder):
    out = {}
    for p in sorted(glob.glob(os.path.join(folder, "*.yaml"))):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        if isinstance(d, dict) and "contract" in d:
            out[os.path.basename(p)[:-5]] = d
    return out


def links():
    return json.load(open(LINKS, encoding="utf-8"))["links"]


def generate(deployed):
    tmp = tempfile.mkdtemp(prefix="c31_gen_")
    cmd = [sys.executable, "workflows/atom_decomposition/gen_silver_rows.py",
           "--g2", PIN + "/G2_pinned.md", "--g4", PIN + "/G4_pinned.md", "--g5", PIN + "/G5_pinned.md", "--g6", PIN + "/G6_pinned.md",
           "--g3", PIN + "/G3_pinned.md", "--g2f", PIN + "/G2f_pinned.md", "--out", tmp,
           "--deployed-tools", R18 + "/" + deployed, "--read-links", LINKS, "--firm-map", R17 + "/f1_firm_map.json"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=100)
    return r, entry_rows(tmp)


def live():
    exp = links()
    new = entry_rows(ENTRIES)
    ls = subprocess.run(["git", "ls-tree", "--name-only", BASE_REF, "workflows/atom_decomposition/catalog_entries/"], capture_output=True, text=True)
    base = {}
    for n in ls.stdout.split():
        if n.endswith(".yaml"):
            d = yaml.safe_load(git_show(BASE_REF, n).decode("utf-8"))
            if isinstance(d, dict) and "contract" in d:
                base[os.path.basename(n)[:-5]] = d
    changed = sorted(e for e in new if new[e] != base.get(e))
    odd = [e for e in changed if e in base and sorted(f for f in set(new[e]) | set(base[e]) if new[e].get(f) != base[e].get(f)) != sorted(f for f in ("read_tool", "tools", "gap_owner") if new[e].get(f) != base[e].get(f))]
    right = all(new[e].get("read_tool") == exp.get(e) and new[e].get("tools") == [exp.get(e)] and new[e].get("gap_owner") is None for e in LIVE_NOW if e in new)
    print("DENOMINATOR table rows %d (base %d); rows differing from %s %d" % (len(new), len(base), BASE_REF, len(changed)))
    return report([("exactly the 6 live-now rows differ from base (%s)" % ",".join(c.replace("opal_data_", "") for c in changed), changed == sorted(LIVE_NOW)),
                   ("each carries its tool, tools == [tool] and gap_owner null", right),
                   ("they differ only in read_tool, tools and gap_owner (%d differ elsewhere)" % len(odd), not odd)])


def future():
    exp = links()
    committed = entry_rows(ENTRIES)
    r1, now = generate("deployed_r18.json")
    r2, fut = generate("deployed_future.json")
    print("DENOMINATOR links %d; generator rc now=%d future=%d; rows now %d future %d" % (len(exp), r1.returncode, r2.returncode, len(now), len(fut)))
    changed_f = sorted(e for e in fut if fut[e].get("read_tool") != committed.get(e, {}).get("read_tool"))
    linked_f = sorted(e for e in fut if fut[e].get("read_tool") and e in exp and fut[e]["read_tool"] == exp[e])
    others = [e for e in fut if e not in exp and fut[e].get("read_tool") != committed.get(e, {}).get("read_tool")]
    changed_now = sorted(e for e in now if now[e].get("read_tool") != committed.get(e, {}).get("read_tool"))
    cls = {}
    for w in (109, 110):
        p = CLASS % w
        if os.path.isfile(p):
            for k, v in json.load(open(p, encoding="utf-8"))["rows"].items():
                if v.get("class") in ("COVERED", "BUILT"):
                    cls[k] = v.get("tool")
    agree = [e for e in cls if exp.get(e) == cls[e]]
    return report([("both generator runs exit 0", r1.returncode == 0 and r2.returncode == 0),
                   ("with the future list all %d links take effect (%d)" % (len(exp), len(linked_f)), sorted(exp) == linked_f),
                   ("no other row's read_tool changes (%d do)" % len(others), not others),
                   ("the future run changes read_tool against the committed rows on exactly the %d rows not yet linked" % (len(exp) - len(LIVE_NOW)),
                    changed_f == sorted(set(exp) - set(LIVE_NOW))),
                   ("with today's 99 tools the committed rows are already right (%d rows would still change)" % len(changed_now), not changed_now),
                   ("the %d COVERED/BUILT links agree with OPLGTW's classification (%d of %d)" % (len(cls), len(agree), len(cls)), len(cls) == 13 and len(agree) == 13)])


def tests():
    missing = [t for t in NEW_TESTS if not os.path.isfile(t)]
    if missing:
        print("DENOMINATOR new test files present 0 of 1")
        return report([("the new test file exists", False)])
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + list(NEW_TESTS), capture_output=True, text=True, timeout=100)
    for ln in [x for x in (r.stdout or "").splitlines() if x.strip()][-3:]:
        print(ln[:200])
    m = re.search(r"(\d+) passed", r.stdout or "")
    passed = int(m.group(1)) if m else 0
    print("DENOMINATOR new test files 1; tests passed %d" % passed)
    return report([("pytest rc=0 (rc=%d)" % r.returncode, r.returncode == 0), ("at least 6 tests passed (%d)" % passed, passed >= 6)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("live", "future", "tests"):
        print(__doc__)
        return 9
    return {"live": live, "future": future, "tests": tests}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
