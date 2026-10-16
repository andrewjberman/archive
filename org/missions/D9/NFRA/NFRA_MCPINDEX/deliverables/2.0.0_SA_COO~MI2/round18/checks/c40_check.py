"""c40_check.py -- grades the LANDING of the read links (NFRA_MCPINDEX round 18, workstream RESEARCH; the issuer's direct act after OG-ap-23 is live). Run from the repo root.

  python c40_check.py landed   all 34 links of read_links.json are in the committed row files (read_tool == the linked tool, tools == [tool], gap_owner null); a fresh generator
                               run with the deployed list changes NO committed row (so the rows are what the released list produces); and no RESEARCH row (every row outside
                               opal_data_assets_) has a null read_tool (the 34 excluded entities are not rows).
  env C40_DEPLOYED   the deployed-tools list file (default: round18/deployed_future.json; on release day: the live list)
Exit 0 PASS, 1 FAIL, 9 no run. c31.AC1 and c31.AC2 are MX-c-31's own gates (6 rows differ from base; 28 rows still to land) and read FAIL by design once the links land.
"""
import glob
import json
import os
import subprocess
import sys
import tempfile

import yaml

ENTRIES = os.environ.get("C40_ENTRIES") or "workflows/atom_decomposition/catalog_entries"
DELIV = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables"
PIN = DELIV + "/0.9.0_WK_NFRA_MCPINDEX~38"
R17 = DELIV + "/2.0.0_SA_COO~MI/round17"
R18 = DELIV + "/2.0.0_SA_COO~MI2/round18"
DEPLOYED = os.environ.get("C40_DEPLOYED") or R18 + "/deployed_future.json"
LINKS = R18 + "/read_links.json"
ASSETS = "opal_data_assets_"


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def rows(folder):
    out = {}
    for p in sorted(glob.glob(os.path.join(folder, "*.yaml"))):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        if isinstance(d, dict) and "contract" in d:
            out[os.path.basename(p)[:-5]] = d
    return out


def landed():
    links = json.load(open(LINKS, encoding="utf-8"))["links"]
    com = rows(ENTRIES)
    tmp = tempfile.mkdtemp(prefix="c40_gen_")
    cmd = [sys.executable, "workflows/atom_decomposition/gen_silver_rows.py",
           "--g2", PIN + "/G2_pinned.md", "--g4", PIN + "/G4_pinned.md", "--g5", PIN + "/G5_pinned.md", "--g6", PIN + "/G6_pinned.md",
           "--g3", PIN + "/G3_pinned.md", "--g2f", PIN + "/G2f_pinned.md", "--out", tmp,
           "--deployed-tools", DEPLOYED, "--read-links", LINKS, "--firm-map", R17 + "/f1_firm_map.json"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=100)
    fresh = rows(tmp)
    unlinked = [e for e, t in links.items() if not (e in com and com[e].get("read_tool") == t and com[e].get("tools") == [t] and com[e].get("gap_owner") is None)]
    differ = [e for e in fresh if fresh[e] != com.get(e)]
    nulls = [e for e, d in com.items() if not e.startswith(ASSETS) and e in fresh and d.get("read_tool") is None]
    print("DENOMINATOR links %d; committed rows %d; fresh rows %d (rc=%d); deployed list %s" % (len(links), len(com), len(fresh), r.returncode, DEPLOYED))
    return report([("the generator exits 0", r.returncode == 0),
                   ("all %d links are landed in the committed rows (%d are not)" % (len(links), len(unlinked)), not unlinked),
                   ("a fresh run with the deployed list changes no committed row (%d differ)" % len(differ), not differ),
                   ("no RESEARCH row has a null read_tool (%d do)" % len(nulls), not nulls)])


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] != "landed":
        print(__doc__)
        sys.exit(9)
    sys.exit(landed())
