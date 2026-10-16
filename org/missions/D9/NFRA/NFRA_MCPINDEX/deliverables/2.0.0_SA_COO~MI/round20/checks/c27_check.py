"""c27_check.py -- grades MX-c-27 (R20-1: a regeneration by gen_silver_rows.py loses no hand-set field and no registry row it does not own), from the repo root.

The regeneration is run in a TEMP folder (nothing in the repo is written) with the exact inputs of round18/land_links.sh plus --hand-overlay round20/hand_overlay.json (the issuer's overlay, an explicit option with no default) (the pinned G2..G6 and G2f files, the unskip file, the two read-links files, the f1 firm map,
`--deployed-tools census`) PLUS both registry flags pointed at temp COPIES of infra/logic/registry/legacy_addresses.json and catalog_fork_keys.json.

  python c27_check.py ac1   the entries: every regenerated entry equals the tracked entry of the same name (0 differ; the base differs in the `prefix` of the eight 49financial *_silver_legacy entries); the
                            four blackdiamond_live_<t> entries are not rewritten (absent from the output) and are byte-equal to HEAD in the repo; a planted `address` in a copy of a GENERATED entry
                            survives a second regeneration over that folder
  python c27_check.py ac2   the registries: after the regeneration the fork registry holds every tracked row, byte-equal (the base loses 34 and changes the `restore.bucket` of 8), and the legacy-address file
                            holds every tracked row whose key does not start with `catalog-` byte-equal (the CRO's four *-logical lookup alias rows and the gateway-client-* rows among them)
  python c27_check.py ac3   tests/test_regen_preserves.py (new, at least 6 tests) with tests/test_gen_silver_rows.py, tests/test_read_links.py and tests/test_read_links_repeat.py pass

Exit 0 PASS, 1 FAIL, 9 no run."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

ROOT = os.environ.get("C27_ROOT") or "."
AD = os.path.join(ROOT, "workflows", "atom_decomposition")
ENT = os.path.join(AD, "catalog_entries")
REG = os.path.join(ROOT, "infra", "logic", "registry")
D = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables")
PIN = os.path.join(D, "0.9.0_WK_NFRA_MCPINDEX~38")
LIVE = ["blackdiamond_live_%s" % t for t in ("unrealized", "transactions", "allocations", "fees")]
LEGACY = ["opal_data_assets_silver_49financial_%s_silver_legacy" % t for t in ("allocations", "assets", "fees", "prices", "realized", "transactions_enriched", "transactions", "unrealized")]


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def regen(out, legacy_copy, fork_copy, extra=()):
    cmd = [sys.executable, os.path.join(AD, "gen_silver_rows.py"),
           "--g2", os.path.join(PIN, "G2_pinned.md"), "--g4", os.path.join(PIN, "G4_pinned.md"), "--g5", os.path.join(PIN, "G5_pinned.md"),
           "--g6", os.path.join(PIN, "G6_pinned.md"), "--g3", os.path.join(PIN, "G3_pinned.md"), "--g2f", os.path.join(PIN, "G2f_pinned.md"),
           "--out", out, "--deployed-tools", "census",
           "--unskip", os.path.join(D, "2.0.0_SA_COO~MI", "round18", "unskip_schwab_dim.json"),
           "--read-links", os.path.join(D, "2.0.0_SA_COO~MI2", "round18", "read_links.json"),
           "--read-links", os.path.join(D, "2.0.0_SA_COO~MI", "round18", "assets_read_links.json"),
           "--firm-map", os.path.join(D, "2.0.0_SA_COO~MI", "round17", "f1_firm_map.json"),
           "--registry-file", legacy_copy, "--fork-registry-file", fork_copy,
           "--hand-overlay", os.path.join(D, "2.0.0_SA_COO~MI", "round20", "hand_overlay.json")] + list(extra)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=280)
    if r.returncode != 0:
        print("ERROR: gen_silver_rows rc %d: %s" % (r.returncode, (r.stderr or r.stdout)[-400:]))
        sys.exit(9)
    return r.stdout


def setup():
    t = tempfile.mkdtemp(prefix="c27_")
    lg, fk = os.path.join(t, "legacy_addresses.json"), os.path.join(t, "catalog_fork_keys.json")
    shutil.copyfile(os.path.join(REG, "legacy_addresses.json"), lg)
    shutil.copyfile(os.path.join(REG, "catalog_fork_keys.json"), fk)
    return t, os.path.join(t, "entries"), lg, fk


def load_yaml(p):
    return yaml.safe_load(open(p, encoding="utf-8"))


def ac1():
    t, out, lg, fk = setup()
    regen(out, lg, fk)
    names = sorted(f[:-5] for f in os.listdir(out) if f.endswith(".yaml"))
    differ = [n for n in names if load_yaml(os.path.join(out, n + ".yaml")) != load_yaml(os.path.join(ENT, n + ".yaml"))]
    print("DENOMINATOR regenerated entries %d; differing from the tracked entry %d (%s)" % (len(names), len(differ), ", ".join(differ[:3]) or "none"))
    res = [("every regenerated entry equals the tracked entry of the same name", not differ and len(names) > 0)]
    res.append(("the four blackdiamond_live_<t> entries are hand-kept: not rewritten", not [n for n in LIVE if n in names]))
    st = subprocess.run(["git", "-C", ROOT, "diff", "--quiet", "HEAD", "--"] + [os.path.join("workflows", "atom_decomposition", "catalog_entries", n + ".yaml") for n in LIVE])
    res.append(("the four live entries are byte-equal to HEAD in the repo (nothing was written there)", st.returncode == 0))
    # a planted hand-set `address` on a GENERATED entry survives a second regeneration over that folder
    victim = next((n for n in LEGACY if n in names), None)
    kept = False
    if victim:
        p = os.path.join(out, victim + ".yaml")
        d = load_yaml(p)
        d["address"] = "planted/address/for/c27/"
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            yaml.safe_dump(d, fh, sort_keys=False, allow_unicode=False, width=100)
        regen(out, lg, fk)
        kept = load_yaml(p).get("address") == "planted/address/for/c27/"
    print("DENOMINATOR planted address on %s: kept after a second regeneration %s" % (victim, kept))
    res.append(("a hand-set `address` on a generated entry survives a regeneration", kept))
    return report(res)


def ac2():
    t, out, lg, fk = setup()
    regen(out, lg, fk)
    a, b = json.load(open(os.path.join(REG, "catalog_fork_keys.json"), encoding="utf-8")), json.load(open(fk, encoding="utf-8"))
    ra, rb = a["rows"], b["rows"]
    lost = sorted(set(ra) - set(rb))
    changed = sorted(k for k in ra if k in rb and ra[k] != rb[k])
    print("DENOMINATOR fork registry rows tracked %d; after regeneration %d; lost %d; changed %d" % (len(ra), len(rb), len(lost), len(changed)))
    res = [("the fork registry loses no row and changes none (lost %d, changed %d)" % (len(lost), len(changed)), not lost and not changed)]
    res.append(("the fork registry's other top-level keys are equal", all(a[k] == b.get(k) for k in a if k != "rows")))
    la = json.load(open(os.path.join(REG, "legacy_addresses.json"), encoding="utf-8"))["legacy_addresses"]
    lb = {r["key"]: r for r in json.load(open(lg, encoding="utf-8"))["legacy_addresses"]}
    own = [r for r in la if not str(r.get("key", "")).startswith("catalog-")]
    miss = [r["key"] for r in own if lb.get(r["key"]) != r]
    alias = [r["key"] for r in own if str(r.get("template", "")).startswith("blackdiamond/49f-live/")]
    print("DENOMINATOR legacy-address rows not owned by the generator %d (of %d); missing or changed after regeneration %d; the CRO alias rows among them %d" % (len(own), len(la), len(miss), len(alias)))
    res.append(("every legacy-address row whose key does not start with catalog- is preserved byte-equal (missing or changed %d)" % len(miss), not miss and len(alias) >= 4))
    return report(res)


def ac3():
    f = os.path.join(AD, "tests", "test_regen_preserves.py")
    if not os.path.exists(f):
        print("ERROR: %s absent" % f)
        return report([("the new test file exists", False)])
    env = dict(os.environ, PYTHONPATH=os.path.abspath(AD))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header", "tests/test_regen_preserves.py", "tests/test_gen_silver_rows.py",
                        "tests/test_read_links.py", "tests/test_read_links_repeat.py"], cwd=AD, env=env, capture_output=True, text=True, timeout=280)
    tail = [ln for ln in (r.stdout or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("pytest rc=%d: %s" % (r.returncode, tail[0].strip() if tail else (r.stdout or r.stderr)[-200:]))
    co = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--co", "tests/test_regen_preserves.py"], cwd=AD, env=env, capture_output=True, text=True, timeout=120)
    n_new = sum(1 for ln in (co.stdout or "").splitlines() if "::" in ln)
    print("new tests collected: %d" % n_new)
    return report([("the four test files pass", r.returncode == 0), ("the new file holds at least 6 tests", n_new >= 6)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
