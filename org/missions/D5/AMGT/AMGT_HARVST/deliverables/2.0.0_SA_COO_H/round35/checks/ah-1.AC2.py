"""HVST-ah-1 AC2 (issuer, read-only): a REAL challenge DOM, captured at load, is the planted fixture the real solver passes.

PASS requires:
- `lib/opal_data_harvest/fixtures/challenges/` holds at least one `<pub>.html` with a `<pub>.provenance.json` whose
  `source` is "captured_at_load", with `captured_at`, `runtime_root`, `request_path` and `sanitizer` set;
- `python -m pytest lib/opal_data_harvest/test_ah1_fixture_solve.py -rA` exits 0, and its output names every captured
  publisher on a PASSED line (a real browser opens the fixture from a local server and `verification.solve()` passes it).
"""
import json
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
FIX = os.path.join(ROOT, "lib/opal_data_harvest/fixtures/challenges")
NEED = ("source", "captured_at", "runtime_root", "request_path", "sanitizer")


def main():
    failures, pubs = [], []
    names = sorted(os.listdir(FIX)) if os.path.isdir(FIX) else []
    for n in names:
        if not n.endswith(".provenance.json"):
            continue
        pub = n[: -len(".provenance.json")]
        prov = json.load(open(os.path.join(FIX, n), encoding="utf-8"))
        missing = [k for k in NEED if not prov.get(k)]
        ok = prov.get("source") == "captured_at_load" and not missing and os.path.exists(os.path.join(FIX, pub + ".html"))
        print("FIXTURE %-8s source=%s captured_at=%s path=%s missing=%s -> %s" % (
            pub, prov.get("source"), prov.get("captured_at"), prov.get("request_path"), missing, "OK" if ok else "REJECTED"))
        if ok:
            pubs.append(pub)
    print("CAPTURED FIXTURES: %d (%s) of %d file(s) in %s" % (len(pubs), ", ".join(pubs), len(names), FIX))
    if not pubs:
        failures.append("no captured-at-load fixture")
    else:
        r = subprocess.run([sys.executable, "-m", "pytest", "lib/opal_data_harvest/test_ah1_fixture_solve.py", "-rA",
                            "--tb=line", "--color=no", "-p", "no:cacheprovider"], cwd=ROOT, capture_output=True, text=True)
        out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
        print(out.strip().splitlines()[-1] if out.strip() else "(no pytest output)")
        if r.returncode != 0:
            failures.append("fixture solve test rc=%d" % r.returncode)
        for pub in pubs:
            if not any(line.startswith("PASSED") and pub in line for line in out.splitlines()):
                failures.append("%s: no PASSED fixture-solve test" % pub)
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
