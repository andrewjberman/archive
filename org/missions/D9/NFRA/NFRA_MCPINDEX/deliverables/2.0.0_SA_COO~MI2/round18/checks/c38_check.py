"""c38_check.py -- grades MX-c-38 (NFRA_MCPINDEX round 18, workstream RESEARCH-EXCL): the 32 catalog rows the CTO ruled out of the finish line leave the
row files, and the row generator reads an entity-exclusions file so a regeneration does not bring them back. Run from the repo root.

  python c38_check.py scope   AC1: none of the 32 entities of entity_exclusions.json is a row file; a fresh generator run (the generator's own default
                              exclusions, no extra argument) exits 0, writes exactly 183 rows, none of the 32, prints one `excluded <entity>: <reason>`
                              line per entity, and every row it writes equals the committed row of the same name outside read_tool/tools/gap_owner
                              (MX-c-31's three fields; the control that no OTHER row moves)
  python c38_check.py tests   AC2: the new test file exists, passes, and collects at least 5 tests

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

ENTRIES = os.environ.get("C38_ENTRIES") or "workflows/atom_decomposition/catalog_entries"
DELIV = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables"
PIN = DELIV + "/0.9.0_WK_NFRA_MCPINDEX~38"
R17 = DELIV + "/2.0.0_SA_COO~MI/round17"
R18 = DELIV + "/2.0.0_SA_COO~MI2/round18"
EXCL = R18 + "/entity_exclusions.json"
WRITTEN = 182
LINK_FIELDS = ("read_tool", "tools", "gap_owner")
NEW_TESTS = ("workflows/atom_decomposition/tests/test_entity_exclusions.py",)


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def entry_rows(folder):
    out = {}
    for p in sorted(glob.glob(os.path.join(folder, "*.yaml"))):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        if isinstance(d, dict) and "contract" in d:
            out[os.path.basename(p)[:-5]] = d
    return out


def scope():
    exp = json.load(open(EXCL, encoding="utf-8"))["entities"]
    committed = entry_rows(ENTRIES)
    tmp = tempfile.mkdtemp(prefix="c38_gen_")
    cmd = [sys.executable, "workflows/atom_decomposition/gen_silver_rows.py",
           "--g2", PIN + "/G2_pinned.md", "--g4", PIN + "/G4_pinned.md", "--g5", PIN + "/G5_pinned.md", "--g6", PIN + "/G6_pinned.md",
           "--g3", PIN + "/G3_pinned.md", "--g2f", PIN + "/G2f_pinned.md", "--out", tmp,
           "--deployed-tools", R18 + "/deployed_r18.json", "--firm-map", R17 + "/f1_firm_map.json"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=100)
    fresh = entry_rows(tmp)
    lines = set(re.findall(r"^excluded (\S+): (\S+)\s*$", r.stdout or "", re.M))
    odd = sorted(e for e in fresh if e in committed and
                 {k: v for k, v in fresh[e].items() if k not in LINK_FIELDS} != {k: v for k, v in committed[e].items() if k not in LINK_FIELDS})
    print("DENOMINATOR entities %d; committed row files %d; fresh generator rows %d (rc=%d)" % (len(exp), len(committed), len(fresh), r.returncode))
    return report([("none of the %d entities is a committed row file (%d are)" % (len(exp), len([e for e in exp if e in committed])), not [e for e in exp if e in committed]),
                   ("the fresh run exits 0 and writes exactly %d rows (rc=%d, wrote %d)" % (WRITTEN, r.returncode, len(fresh)), r.returncode == 0 and len(fresh) == WRITTEN),
                   ("the fresh run writes none of the %d entities (%d written)" % (len(exp), len([e for e in exp if e in fresh])), not [e for e in exp if e in fresh]),
                   ("one `excluded <entity>: <reason>` line per entity with the file's reason (%d of %d)" % (len([e for e in exp if (e, exp[e]) in lines]), len(exp)),
                    all((e, exp[e]) in lines for e in exp)),
                   ("every fresh row is a committed row (%d fresh rows are not)" % len(set(fresh) - set(committed)), set(fresh) <= set(committed)),
                   ("every fresh row equals its committed row outside %s (%d differ)" % ("/".join(LINK_FIELDS), len(odd)), not odd)])


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
    return report([("pytest rc=0 (rc=%d)" % r.returncode, r.returncode == 0), ("at least 5 tests passed (%d)" % passed, passed >= 5)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("scope", "tests"):
        print(__doc__)
        return 9
    return {"scope": scope, "tests": tests}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
