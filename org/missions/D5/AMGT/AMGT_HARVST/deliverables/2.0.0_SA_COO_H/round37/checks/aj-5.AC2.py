"""HVST-aj-5 AC2 (issuer, read-only): limb 2a graded PER RUN with each publisher's window pass rate printed
(round-36 addendum ruling 8a @1c693565e7).

Runs `python -m lib.opal_data_harvest.load_window_grade --json` over the live monitor windows. PASS requires:
- top level `grain` == "per_run" and `requests_counted` == "inside_monitor_windows";
- every publisher carries `verdict`, `window_pass_rate` (non-void passed / non-void presented, or null when none), and
  `runs` = a list of per-run entries, each with `run_id`, `in_window`, `challenges_presented`, `challenges_void`,
  `challenges_nonvoid`, `challenges_nonvoid_passed`, `run_verdict`;
- each publisher's verdict follows ruling 8a from its runs: NOT_EVALUATED when no windowed request; else
  MET-BY-ABSENCE when no challenge was presented in any windowed run; else MET when at least one in-window run has
  every presented challenge non-void and passed; else NOT-MET.
The verdict VALUES are not predicted; the CVO grades limb 2a on them.
"""
import json
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RUN_FIELDS = ("run_id", "in_window", "challenges_presented", "challenges_void", "challenges_nonvoid",
              "challenges_nonvoid_passed", "run_verdict")


def expected(p):
    runs = [r for r in p["runs"] if r.get("in_window")]
    if not p.get("requests"):
        return "NOT_EVALUATED"
    if not any(r["challenges_presented"] for r in runs):
        return "MET-BY-ABSENCE"
    if any(r["challenges_presented"] and r["challenges_void"] == 0
           and r["challenges_nonvoid_passed"] == r["challenges_presented"] for r in runs):
        return "MET"
    return "NOT-MET"


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
    print("GRAIN %s REQUESTS COUNTED %s" % (d.get("grain"), d.get("requests_counted")))
    if d.get("grain") != "per_run":
        failures.append("grain %s, want per_run" % d.get("grain"))
    if d.get("requests_counted") != "inside_monitor_windows":
        failures.append("requests_counted %s" % d.get("requests_counted"))
    for pub in ("bbg", "wsj", "barrons", "ft", "sa"):
        p = (d.get("publishers") or {}).get(pub)
        if not p or "verdict" not in p or "window_pass_rate" not in p or not isinstance(p.get("runs"), list):
            failures.append("%s missing verdict/window_pass_rate/runs" % pub)
            continue
        bad = [x for x in p["runs"] if [k for k in RUN_FIELDS if k not in x]]
        if bad:
            failures.append("%s: %d run entries missing fields" % (pub, len(bad)))
            continue
        inwin = [x for x in p["runs"] if x.get("in_window")]
        print("PUB %-8s verdict=%s window_pass_rate=%s requests=%s runs=%d in_window=%d" % (
            pub, p["verdict"], p["window_pass_rate"], p.get("requests"), len(p["runs"]), len(inwin)))
        if p["verdict"] != expected(p):
            failures.append("%s verdict %s, ruling 8a gives %s" % (pub, p["verdict"], expected(p)))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
