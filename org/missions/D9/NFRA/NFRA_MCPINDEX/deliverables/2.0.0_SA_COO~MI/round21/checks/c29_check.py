"""c29_check.py -- grades MX-c-29 (R21-1: a regeneration that would DROP a registry row REFUSES, naming each dropped row), from the repo root.

The regeneration is run in a TEMP folder (nothing in the repo is written) with the inputs of round18/land_links.sh plus --hand-overlay round20/hand_overlay.json and both registry flags pointed at temp
COPIES of infra/logic/registry/legacy_addresses.json and catalog_fork_keys.json. The new option is --allow-registry-drop FILE: a JSON list of row keys (a legacy_addresses `key`, or a fork registry
hashed id) that the issuer accepts the regeneration to drop. Without it, a registry write that removes any row present before REFUSES: exit 2, NOTHING written (both registry copies byte-equal), and one
line `REGISTRY-DROP <file name> <row key>` printed per dropped row.

  python c29_check.py ac1   today's tracked state: the guard refuses, names the dropped rows (the `catalog-*` keys of legacy_addresses.json the generator no longer produces), writes nothing; a second run
                            whose allow file lists exactly the printed keys succeeds (exit 0) and the rows really dropped equal the printed set; a third run whose allow file lacks ONE printed key refuses
                            naming exactly that key
  python c29_check.py ac2   the planted drop: a fake `catalog-*` row appended to a temp legacy copy; the run whose allow file holds only the real printed keys REFUSES naming the planted key alone;
                            the run whose allow file also lists it succeeds
  python c29_check.py ac3   tests/test_registry_drop_guard.py (new, at least 6 tests) with tests/test_gen_silver_rows.py and tests/test_regen_preserves.py pass

Exit 0 PASS, 1 FAIL, 9 no run."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.environ.get("C29_ROOT") or "."
AD = os.path.join(ROOT, "workflows", "atom_decomposition")
REG = os.path.join(ROOT, "infra", "logic", "registry")
D = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables")
PIN = os.path.join(D, "0.9.0_WK_NFRA_MCPINDEX~38")
LINE = re.compile(r"^REGISTRY-DROP (\S+) (\S+)\s*$", re.M)


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def run(out, lg, fk, allow=None):
    cmd = [sys.executable, os.path.join(AD, "gen_silver_rows.py"),
           "--g2", os.path.join(PIN, "G2_pinned.md"), "--g4", os.path.join(PIN, "G4_pinned.md"), "--g5", os.path.join(PIN, "G5_pinned.md"),
           "--g6", os.path.join(PIN, "G6_pinned.md"), "--g3", os.path.join(PIN, "G3_pinned.md"), "--g2f", os.path.join(PIN, "G2f_pinned.md"),
           "--out", out, "--deployed-tools", "census",
           "--unskip", os.path.join(D, "2.0.0_SA_COO~MI", "round18", "unskip_schwab_dim.json"),
           "--read-links", os.path.join(D, "2.0.0_SA_COO~MI2", "round18", "read_links.json"),
           "--read-links", os.path.join(D, "2.0.0_SA_COO~MI", "round18", "assets_read_links.json"),
           "--firm-map", os.path.join(D, "2.0.0_SA_COO~MI", "round17", "f1_firm_map.json"),
           "--hand-overlay", os.path.join(D, "2.0.0_SA_COO~MI", "round20", "hand_overlay.json"),
           "--registry-file", lg, "--fork-registry-file", fk]
    if allow:
        cmd += ["--allow-registry-drop", allow]
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=280)


def setup():
    t = tempfile.mkdtemp(prefix="c29_")
    lg, fk = os.path.join(t, "legacy_addresses.json"), os.path.join(t, "catalog_fork_keys.json")
    shutil.copyfile(os.path.join(REG, "legacy_addresses.json"), lg)
    shutil.copyfile(os.path.join(REG, "catalog_fork_keys.json"), fk)
    return t, lg, fk


def blob(p):
    with open(p, "rb") as fh:
        return fh.read()


def printed(r):
    return sorted(set(m.group(2) for m in LINE.finditer((r.stdout or "") + (r.stderr or ""))))


def keys_of(lg):
    return {r["key"] for r in json.loads(blob(lg).decode("utf-8"))["legacy_addresses"]}


def write_allow(t, name, keys):
    p = os.path.join(t, name)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(sorted(keys), fh)
    return p


def ac1():
    t, lg, fk = setup()
    b_lg, b_fk = blob(lg), blob(fk)
    before = keys_of(lg)
    r1 = run(os.path.join(t, "o1"), lg, fk)
    p1 = printed(r1)
    print("DENOMINATOR run 1 (no allow file): exit %d; REGISTRY-DROP rows printed %d" % (r1.returncode, len(p1)))
    res = [("without an allow file the regeneration REFUSES (exit 2), naming each dropped row (%d)" % len(p1), r1.returncode == 2 and len(p1) > 0),
           ("a refusal writes nothing: both registry copies are byte-equal to before", blob(lg) == b_lg and blob(fk) == b_fk)]
    allow = write_allow(t, "allow_all.json", p1)
    r2 = run(os.path.join(t, "o2"), lg, fk, allow)
    after = keys_of(lg)
    dropped = sorted(before - after)
    print("DENOMINATOR run 2 (allow file = the printed keys): exit %d; rows really dropped from legacy_addresses.json %d" % (r2.returncode, len(dropped)))
    res.append(("with the allow file listing exactly the printed keys the regeneration succeeds and the rows really dropped equal the printed set", r2.returncode == 0 and dropped == p1))
    t3, lg3, fk3 = setup()
    r3 = run(os.path.join(t3, "o3"), lg3, fk3, write_allow(t3, "allow_short.json", p1[1:]))
    p3 = printed(r3)
    print("DENOMINATOR run 3 (allow file lacks one key): exit %d; printed %s" % (r3.returncode, p3))
    res.append(("an allow file that lacks one printed key refuses naming exactly that key", r3.returncode == 2 and p3 == p1[:1]))
    return report(res)


def ac2():
    t, lg, fk = setup()
    r0 = run(os.path.join(t, "o0"), lg, fk)
    real = printed(r0)
    t2, lg2, fk2 = setup()
    doc = json.loads(blob(lg2).decode("utf-8"))
    doc["legacy_addresses"].append({"key": "catalog-planted-row-c29", "bucket": "opal-data-assets", "template": "planted/c29/", "shape": "prefix", "params": [],
                                    "reader": "NFRA_MCPINDEX", "evidence": "planted by c29_check", "note": "planted"})
    with open(lg2, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1)
    b_lg = blob(lg2)
    r1 = run(os.path.join(t2, "o1"), lg2, fk2, write_allow(t2, "allow_real.json", real))
    p1 = printed(r1)
    print("DENOMINATOR planted run: exit %d; printed %s" % (r1.returncode, p1))
    res = [("the real drops are allowed, a planted catalog-* row is NOT: refusal naming the planted key alone", r1.returncode == 2 and p1 == ["catalog-planted-row-c29"]),
           ("the refusal wrote nothing", blob(lg2) == b_lg)]
    r2 = run(os.path.join(t2, "o2"), lg2, fk2, write_allow(t2, "allow_both.json", real + ["catalog-planted-row-c29"]))
    res.append(("with the planted key allowed too the regeneration succeeds", r2.returncode == 0))
    return report(res)


def ac3():
    f = os.path.join(AD, "tests", "test_registry_drop_guard.py")
    if not os.path.exists(f):
        print("ERROR: %s absent" % f)
        return report([("the new test file exists", False)])
    env = dict(os.environ, PYTHONPATH=os.path.abspath(AD))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header", "tests/test_registry_drop_guard.py", "tests/test_gen_silver_rows.py",
                        "tests/test_regen_preserves.py"], cwd=AD, env=env, capture_output=True, text=True, timeout=280)
    tail = [ln for ln in (r.stdout or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("pytest rc=%d: %s" % (r.returncode, tail[0].strip() if tail else (r.stdout or r.stderr)[-200:]))
    co = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--co", "tests/test_registry_drop_guard.py"], cwd=AD, env=env, capture_output=True, text=True, timeout=120)
    n_new = sum(1 for ln in (co.stdout or "").splitlines() if "::" in ln)
    print("new tests collected: %d" % n_new)
    return report([("the three test files pass", r.returncode == 0), ("the new file holds at least 6 tests", n_new >= 6)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
