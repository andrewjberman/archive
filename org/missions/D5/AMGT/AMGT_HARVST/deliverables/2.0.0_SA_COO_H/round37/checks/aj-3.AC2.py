"""HVST-aj-3 AC2 (issuer, read-only): barrons is exercised under the monitor (round-36 analysis ruling 3).

Runs the live grader over every monitor window (`python -m lib.opal_data_harvest.load_window_grade --json`). PASS
requires top-level requests_counted == "inside_monitor_windows" (aj-1), barrons requests >= 1 and the barrons verdict MET or
MET-BY-ABSENCE. The verdict VALUE among those two is not predicted.
"""
import json
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()


def main():
    failures = []
    r = subprocess.run([sys.executable, "-m", "lib.opal_data_harvest.load_window_grade", "--json"], cwd=ROOT,
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        print("GRADER rc=%d, stdout not JSON: %s" % (r.returncode, (r.stdout + r.stderr)[:300]))
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: grader produced no JSON")
        return 1
    print("REQUESTS COUNTED %s" % d.get("requests_counted"))
    if d.get("requests_counted") != "inside_monitor_windows":
        failures.append("grader does not count requests inside the monitor windows (requests_counted=%s)"
                        % d.get("requests_counted"))
    p = (d.get("publishers") or {}).get("barrons") or {}
    print("PUB barrons verdict=%s requests=%s presented=%s void=%s nonvoid=%s nonvoid_passed=%s" % (
        p.get("verdict"), p.get("requests"), p.get("challenges_presented"), p.get("challenges_void"),
        p.get("challenges_nonvoid"), p.get("challenges_nonvoid_passed")))
    if not isinstance(p.get("requests"), int) or p.get("requests") < 1:
        failures.append("barrons windowed requests %s, want >= 1" % p.get("requests"))
    if p.get("verdict") not in ("MET", "MET-BY-ABSENCE"):
        failures.append("barrons verdict %s, want MET or MET-BY-ABSENCE" % p.get("verdict"))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
