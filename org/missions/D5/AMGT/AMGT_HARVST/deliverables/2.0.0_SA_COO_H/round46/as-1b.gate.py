"""Round 46 HVST-as-1b: THE PRE-RUN GATE (CTO ruling @a142505a06, conditions 1 and 2). Read-only; no publisher request.

1. 191/191: the collector universe (`__main__.universe(<shipped config>)`) carries `security_key` for every rank name
   (round46/checks/as-1.AC2.py, re-run here).
2. The sa bound, printed before the GO: names x (max_listing_pages.sa + candidate_limit) requests at most, and the days that
   is at the driver's printed pacing budget.
3. The driver's dry run for each publisher: UNIVERSE 191, 191 PLAN lines, NETWORK CALLS 0.
Prints `GATE: OPEN` only when all three hold.
"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 8)))
PUBLISHERS = ("sa", "ft", "wsj", "bbg", "barrons")


def main():
    ok = True
    ac2 = subprocess.run([sys.executable, os.path.join(HERE, "checks", "as-1.AC2.py")], cwd=ROOT, capture_output=True,
                         text=True, encoding="utf-8", errors="replace", timeout=900)
    for line in ac2.stdout.splitlines():
        if line.startswith("AC2 rank names resolved") or line.startswith("AC2 identity") or line.startswith("AC2 RESULT"):
            print("1. " + line)
    ok = ok and "AC2 RESULT: PASS" in ac2.stdout
    cfg = json.load(open(os.path.join(ROOT, "lib", "opal_data_harvest", "config.json"), encoding="utf-8"))
    pages = cfg["max_listing_pages"]["sa"]
    cand = cfg.get("candidate_limit", 20)
    pace = 86400 / (cfg.get("minimum_request_seconds", 15) + cfg.get("jitter_seconds", 10) / 2)
    bound = 191 * (pages + cand)
    print("2. sa bound: 191 names x (%d pages + %d candidates) = %d requests at most; %.1f days at %d requests/day; "
          "89-name bound for comparison %d. The 2026-01-01 floor stops most names far earlier." % (
              pages, cand, bound, bound / pace, pace, 89 * (pages + cand)))
    tmp = tempfile.mkdtemp(prefix="as1b_gate_")
    for pub in PUBLISHERS:
        r = subprocess.run([sys.executable, "-m", "lib.opal_data_harvest.backfill_driver", "--checkpoint",
                            os.path.join(tmp, pub + ".json"), "--publishers", pub, "--dry-run"], cwd=ROOT,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        out = r.stdout + r.stderr
        plans = sum(1 for line in out.splitlines() if line.startswith("PLAN "))
        good = r.returncode == 0 and "UNIVERSE: 191" in out and "NETWORK CALLS: 0" in out and plans == 191
        print("3. %s: rc %d, UNIVERSE 191 %s, PLAN %d, NETWORK CALLS 0 %s -> %s" % (
            pub, r.returncode, "UNIVERSE: 191" in out, plans, "NETWORK CALLS: 0" in out, "ok" if good else "FAIL"))
        ok = ok and good
    print("GATE: %s" % ("OPEN" if ok else "SHUT"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
