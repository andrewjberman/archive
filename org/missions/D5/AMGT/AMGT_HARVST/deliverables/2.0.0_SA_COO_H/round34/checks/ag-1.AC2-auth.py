"""HVST-ag-1 AC2 as re-read by the CTO ruling (msg 27860): FWD-11 limb (1) ROBUST AUTH.

Reads `~91/ag1_challenged_pass.json` (the record the act wrote; `publishers.<pub>.attempts`, each with
`signin_renewed` and `error`). PASS requires, for EACH of wsj and barrons: at least 3 fresh-profile sign-ins
or renewals that completed unattended (`signin_renewed` true, no error), inside a monitor window with hardware input 0, and every
challenge met (if any) passed. The CAPTCHA limb (2) is graded elsewhere (a full driver day under the monitor + a
planted challenge fixture).
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RECORD = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~91/ag1_challenged_pass.json")


def main():
    failures = []
    if not os.path.exists(RECORD):
        print("RECORD: absent")
        print("AC2 RESULT: FAIL (1 failure(s))")
        return 1
    r = json.load(open(RECORD, encoding="utf-8"))
    print("INSTRUMENT: %s; window %s .. %s; hardware %s, injected %s" % (r.get("instrument"), r.get("window_start"),
          r.get("window_end"), r.get("hardware_input_events"), r.get("injected_input_events")))
    if r.get("hardware_input_events") != 0:
        failures.append("hardware input events %r" % r.get("hardware_input_events"))
    for pub in ("wsj", "barrons"):
        p = (r.get("publishers") or {}).get(pub) or {}
        mine = p.get("attempts") or []
        ok = [a for a in mine if a.get("signin_renewed") is True and not a.get("error")]
        unpassed = [] if str(p.get("challenge_met")) in ("none", "None", "", "null") or p.get("passed") is True else [p]
        print("  %-8s attempts %d, unattended sign-in/renewal ok %d, challenges met-not-passed %d"
              % (pub, len(mine), len(ok), len(unpassed)))
        if len(ok) < 3:
            failures.append("%s: %d completed unattended sign-ins (< 3)" % (pub, len(ok)))
        if unpassed:
            failures.append("%s: %d challenge(s) met and not passed" % (pub, len(unpassed)))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
