"""HVST-ai-3 AC2 (issuer, read-only): capture-at-load is armed on all five publishers, and wsj/barrons share a vendor fixture path.

Runs `python -m pytest lib/opal_data_harvest/test_ai3_capture_all.py -rA --color=no` and then
`python -m lib.opal_data_harvest.challenge_capture --status --json`. PASS requires:
- pytest exits 0, with a PASSED line per publisher for the capture plant (bbg, wsj, barrons, ft, sa in the test id);
- the status JSON lists all five, each with `limb_2b` in PASS-FIXTURE / SAMPLE-CAPTURED / VENDOR-EQUIVALENT / OPEN (NO SAMPLE)
  and never MET-BY-ABSENCE, and `vendor` set (wsj and barrons must name the same vendor).
"""
import json
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
PUBS = ("bbg", "wsj", "barrons", "ft", "sa")
OK = {"PASS-FIXTURE", "SAMPLE-CAPTURED", "VENDOR-EQUIVALENT", "OPEN (NO SAMPLE)"}


def main():
    failures = []
    r = subprocess.run([sys.executable, "-m", "pytest", "lib/opal_data_harvest/test_ai3_capture_all.py", "-rA",
                        "--tb=line", "--color=no", "-p", "no:cacheprovider"], cwd=ROOT, capture_output=True, text=True)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    print(out.strip().splitlines()[-1] if out.strip() else "(no pytest output)")
    if r.returncode != 0:
        failures.append("capture plants rc=%d" % r.returncode)
    for pub in PUBS:
        if not any(line.startswith("PASSED") and pub in line for line in out.splitlines()):
            failures.append("%s: no PASSED capture plant" % pub)
    s = subprocess.run([sys.executable, "-m", "lib.opal_data_harvest.challenge_capture", "--status", "--json"], cwd=ROOT,
                       capture_output=True, text=True)
    try:
        st = json.loads(s.stdout)
    except ValueError:
        st = {}
        failures.append("status produced no JSON: %s" % (s.stdout + s.stderr)[:200])
    pubs = st.get("publishers") or {}
    for pub in PUBS:
        p = pubs.get(pub) or {}
        print("STATUS %-8s limb_2b=%s vendor=%s captures=%s" % (pub, p.get("limb_2b"), p.get("vendor"), p.get("captures")))
        if p.get("limb_2b") not in OK:
            failures.append("%s limb_2b %r" % (pub, p.get("limb_2b")))
        if not p.get("vendor"):
            failures.append("%s has no vendor" % pub)
    if (pubs.get("wsj") or {}).get("vendor") != (pubs.get("barrons") or {}).get("vendor"):
        failures.append("wsj and barrons name different vendors")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
