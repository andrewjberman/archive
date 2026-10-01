"""HVST-ah-2 AC2 (issuer, read-only): the per-minute load grader VOIDS human-input minutes and grades FWD-11 limb 2a per publisher.

Runs `python -m lib.opal_data_harvest.load_window_grade --json` (its defaults read the issuer's monitor windows under
`.runtime/harvest-backfill/` and every harvest runtime's events). PASS requires the JSON to carry:
- `windows`: every monitor window with `void_minutes` (minutes with hardware input) and, for a window with hardware
  input but no per-minute buckets, `void: true` for the WHOLE window;
- `publishers`: all five of bbg, wsj, barrons, ft, sa, each with `verdict` in MET / MET-BY-ABSENCE / NOT-MET /
  INSUFFICIENT, plus `requests`, `challenges_presented`, `challenges_passed`, `challenges_in_void_minutes`, `clean_hours`.
"""
import json
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
VERDICTS = {"MET", "MET-BY-ABSENCE", "NOT-MET", "INSUFFICIENT"}
FIELDS = ("verdict", "requests", "challenges_presented", "challenges_passed", "challenges_in_void_minutes", "clean_hours")


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
    wins = d.get("windows") or []
    for w in wins:
        print("WINDOW %s .. %s hardware %s per-minute %s void_minutes %d void %s" % (
            w.get("window_start"), w.get("window_end"), w.get("hardware_input_events"), w.get("has_minutes"),
            len(w.get("void_minutes") or []), w.get("void")))
        if w.get("hardware_input_events") and not w.get("has_minutes") and w.get("void") is not True:
            failures.append("window %s has hardware input without minutes and is not void" % w.get("window_start"))
        if "void_minutes" not in w:
            failures.append("window %s carries no void_minutes" % w.get("window_start"))
    if not wins:
        failures.append("no monitor window graded")
    for pub in ("bbg", "wsj", "barrons", "ft", "sa"):
        p = (d.get("publishers") or {}).get(pub)
        if not p:
            failures.append("%s missing" % pub)
            continue
        print("PUB %-8s %s" % (pub, " ".join("%s=%s" % (k, p.get(k)) for k in FIELDS)))
        if p.get("verdict") not in VERDICTS:
            failures.append("%s verdict %r" % (pub, p.get("verdict")))
        if [k for k in FIELDS if k not in p]:
            failures.append("%s missing fields" % pub)
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
