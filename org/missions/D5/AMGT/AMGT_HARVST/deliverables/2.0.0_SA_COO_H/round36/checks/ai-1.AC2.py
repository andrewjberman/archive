"""HVST-ai-1 AC2 (issuer, read-only): FWD-11 limb 2a graded PER MINUTE with a +/-1 minute guard band (CTO r35 ruling 1).

Runs `python -m lib.opal_data_harvest.load_window_grade --json`. PASS requires:
- top level `rule` == "per_minute_guard_band" and `guard_band_minutes` == 1 and `required_clean_minutes` == 1440;
- all five publishers carry `verdict`, `requests`, `clean_minutes`, `challenges_presented`,
  `clean_minute_challenges_presented`, `clean_minute_challenges_passed`;
- every verdict follows the ruling from those fields: INSUFFICIENT when clean_minutes < 1440; else NOT-MET when a
  clean-minute challenge did not pass; else MET-BY-ABSENCE when none was presented in a clean minute; else MET.
"""
import json
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
FIELDS = ("verdict", "requests", "clean_minutes", "challenges_presented", "clean_minute_challenges_presented",
          "clean_minute_challenges_passed")


def expected(p):
    if p["clean_minutes"] < 1440:
        return "INSUFFICIENT"
    if p["clean_minute_challenges_passed"] < p["clean_minute_challenges_presented"]:
        return "NOT-MET"
    if p["clean_minute_challenges_presented"] == 0:
        return "MET-BY-ABSENCE"
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
    print("RULE %s guard_band %s required_clean_minutes %s" % (d.get("rule"), d.get("guard_band_minutes"),
                                                              d.get("required_clean_minutes")))
    if d.get("rule") != "per_minute_guard_band" or d.get("guard_band_minutes") != 1 or d.get("required_clean_minutes") != 1440:
        failures.append("rule/guard band/required minutes not per ruling 1")
    for pub in ("bbg", "wsj", "barrons", "ft", "sa"):
        p = (d.get("publishers") or {}).get(pub)
        if not p or [k for k in FIELDS if k not in p]:
            failures.append("%s missing or missing fields" % pub)
            continue
        print("PUB %-8s %s" % (pub, " ".join("%s=%s" % (k, p.get(k)) for k in FIELDS)))
        if p["verdict"] != expected(p):
            failures.append("%s verdict %s, ruling gives %s" % (pub, p["verdict"], expected(p)))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
