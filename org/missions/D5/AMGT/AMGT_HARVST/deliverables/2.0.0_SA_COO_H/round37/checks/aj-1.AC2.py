"""HVST-aj-1 AC2 (issuer, read-only): the presentation-anchored, windowed limb-2a grader re-grades ROUND 36's windows
(round-36 analysis ruling 1; enrichment item 1).

Runs `python -m lib.opal_data_harvest.load_window_grade --json --runtimes <round37/runtimes.round36_windows.json>`,
which lists monitor windows 1 and 2 only (2026-10-01 ~09:5xZ .. 2026-10-02 04:03Z). PASS requires:
- rule "per_challenge_guard_band", guard_band_minutes 2;
- bbg: challenges_nonvoid == 9 and challenges_nonvoid_passed == 9 (CVO~Z's true-band re-derivation, ADJUDICATION_v47);
- barrons: verdict NOT_EVALUATED with requests == 0 (requests are counted inside the monitor windows only).
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
PINNED = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round37/runtimes.round36_windows.json")


def main():
    failures = []
    r = subprocess.run([sys.executable, "-m", "lib.opal_data_harvest.load_window_grade", "--json", "--runtimes", PINNED],
                       cwd=ROOT, capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        print("GRADER rc=%d, stdout not JSON: %s" % (r.returncode, (r.stdout + r.stderr)[:300]))
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: grader produced no JSON")
        return 1
    print("RULE %s guard_band %s windows %d" % (d.get("rule"), d.get("guard_band_minutes"), len(d.get("windows") or [])))
    if d.get("rule") != "per_challenge_guard_band" or d.get("guard_band_minutes") != 2:
        failures.append("rule/guard band not per_challenge_guard_band / 2")
    print("REQUESTS COUNTED %s" % d.get("requests_counted"))
    if d.get("requests_counted") != "inside_monitor_windows":
        failures.append("requests_counted %s, want inside_monitor_windows" % d.get("requests_counted"))
    pubs = d.get("publishers") or {}
    for pub in ("bbg", "wsj", "barrons", "ft", "sa"):
        p = pubs.get(pub) or {}
        print("PUB %-8s verdict=%s requests=%s presented=%s void=%s nonvoid=%s nonvoid_passed=%s" % (
            pub, p.get("verdict"), p.get("requests"), p.get("challenges_presented"), p.get("challenges_void"),
            p.get("challenges_nonvoid"), p.get("challenges_nonvoid_passed")))
    b = pubs.get("bbg") or {}
    if b.get("challenges_nonvoid") != 9 or b.get("challenges_nonvoid_passed") != 9:
        failures.append("bbg nonvoid/passed %s/%s, want 9/9" % (b.get("challenges_nonvoid"), b.get("challenges_nonvoid_passed")))
    br = pubs.get("barrons") or {}
    if br.get("verdict") != "NOT_EVALUATED" or br.get("requests") != 0:
        failures.append("barrons verdict %s requests %s, want NOT_EVALUATED / 0" % (br.get("verdict"), br.get("requests")))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
