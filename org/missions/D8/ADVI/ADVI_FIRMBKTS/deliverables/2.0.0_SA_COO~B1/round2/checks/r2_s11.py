"""ADVI_FIRMBKTS round 2 check for cell FB-e-7 (row S11: the cot price builder's tolerant load), issuer 2.0.0_SA_COO~B1.

Grades the naming gate (LGIC_ENFORCE DEC-6) on the cell's own diff: `git diff <BASE> HEAD` over the builder and its new
test, fed to .tools/naming-gate.py --enforce. The gate that refused the first attempt (row MDPF_DEMQUE-D1-W7-S2) is the
instrument; this file only hands it the diff and reads its verdict. An empty diff is a FAIL (nothing was built).
Run from the repository root. Never edit this file.
"""
import os
import subprocess
import sys
import tempfile

BASE = "fda1c4f0cc"   # the repository as it stood at the round-2 cut
PATHS = ("data/cot/scripts/gold/build_canonical_prices_v2.py",
         "data/cot/scripts/gold/tests/test_s00_missing_tier2.py")


def main():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    d = subprocess.run(["git", "diff", BASE, "HEAD", "--"] + list(PATHS), capture_output=True, text=True, cwd=root)
    added = [ln for ln in d.stdout.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    print("S11 DIFF: %d added line(s) across %s since %s" % (len(added), ", ".join(os.path.basename(p) for p in PATHS), BASE))
    has_test = "test_s00_missing_tier2.py" in d.stdout
    has_builder = "build_canonical_prices_v2.py" in d.stdout and "_load_tier2" in d.stdout
    if not (added and has_test and has_builder):
        print("S11 NAMING GATE: NOT RUN -- the diff does not carry the tolerant load and its test")
        return 1
    with tempfile.NamedTemporaryFile("w", suffix=".diff", delete=False, encoding="utf-8", newline="\n") as fh:
        fh.write(d.stdout)
        path = fh.name
    try:
        out = subprocess.run([sys.executable, os.path.join(root, ".tools", "naming-gate.py"), "--diff", path, "--enforce"],
                             capture_output=True, text=True, cwd=root)
    finally:
        os.unlink(path)
    text = out.stdout + out.stderr
    refuse = [ln for ln in text.splitlines() if ln.startswith("NAMING REFUSE")]
    verdict = [ln for ln in text.splitlines() if ln.startswith("NAMING-GATE:")]
    for ln in refuse[:5]:
        print("  " + ln)
    ok = out.returncode == 0 and not refuse and bool(verdict)
    print("S11 NAMING GATE: %s (%d REFUSE; gate said: %s)" % ("PASS" if ok else "REFUSED", len(refuse),
                                                              verdict[-1] if verdict else "no verdict line"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
