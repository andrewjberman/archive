"""HVST-ai-6 AC2 (issuer, read-only): FWD-11 limb 2a graded PER CHALLENGE with a +/-2 minute guard band
(CTO ruling, self-drive tick 2 @bb3c328367, msg "RULED: HARVST FWD-11 limb 2a grades per challenge").

Runs `python -m lib.opal_data_harvest.load_window_grade --json` over the REAL monitor windows. PASS requires:
- top level `rule` == "per_challenge_guard_band" and `guard_band_minutes` == 2, and no clean-minute count gates a verdict;
- all five publishers carry `verdict`, `requests`, `challenges_presented`, `challenges_void`, `challenges_nonvoid`,
  `challenges_nonvoid_passed`, with challenges_void + challenges_nonvoid == challenges_presented;
- every verdict follows the ruling from those fields: MET-BY-ABSENCE when none was presented; else NOT-MET when a
  non-void challenge did not pass; else INSUFFICIENT when every presented challenge is void; else MET.
The verdict VALUES are not predicted here; the CVO grades limb 2a on them.
"""
import json
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
FIELDS = ("verdict", "requests", "challenges_presented", "challenges_void", "challenges_nonvoid",
          "challenges_nonvoid_passed")


def expected(p):
    if p["challenges_presented"] == 0:
        return "MET-BY-ABSENCE"
    if p["challenges_nonvoid_passed"] < p["challenges_nonvoid"]:
        return "NOT-MET"
    if p["challenges_nonvoid"] == 0:
        return "INSUFFICIENT"
    return "MET"


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
    print("RULE %s guard_band %s" % (d.get("rule"), d.get("guard_band_minutes")))
    if d.get("rule") != "per_challenge_guard_band" or d.get("guard_band_minutes") != 2:
        failures.append("rule/guard band not per the per-challenge ruling")
    for pub in ("bbg", "wsj", "barrons", "ft", "sa"):
        p = (d.get("publishers") or {}).get(pub)
        if not p or [k for k in FIELDS if k not in p]:
            failures.append("%s missing or missing fields" % pub)
            continue
        print("PUB %-8s %s" % (pub, " ".join("%s=%s" % (k, p.get(k)) for k in FIELDS)))
        if p["challenges_void"] + p["challenges_nonvoid"] != p["challenges_presented"]:
            failures.append("%s void + nonvoid != presented" % pub)
        if p["verdict"] != expected(p):
            failures.append("%s verdict %s, ruling gives %s" % (pub, p["verdict"], expected(p)))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
