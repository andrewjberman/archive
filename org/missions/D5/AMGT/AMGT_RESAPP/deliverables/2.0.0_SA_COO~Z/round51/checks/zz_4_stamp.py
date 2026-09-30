"""AMGT_RESAPP round 51, AMGT-zz-4 AC1 -- the stamp is GREEN at this tree and the four prefix constants did NOT move (CTO round-50 ruling 4:
"the restamp that unblocks HEAD lands WITH this cell, and its diff shows the four constants unchanged"; row Z-S306).
(a) `python infra/aws/terraform/harvest/gen_harvest_prefixes.py --check` exits 0 on this tree;
(b) the four constants in lib/research/api/_harvest_prefixes.py are byte-equal to their values at the cut (commit 78425f62a7).
usage: python <this>   (from the repo root)"""
import re
import subprocess
import sys

MOD = "lib/research/api/_harvest_prefixes.py"
CUT = "78425f62a7"
NAMES = ("BLOOMBERG_BRONZE_PREFIX", "BRIGHT_DATA_SERP_BRONZE_PREFIX", "FILING_ATTEMPT_STATE_PREFIX", "SEEKING_ALPHA_BRONZE_PREFIX")


def consts(text):
    return {n: (re.search(r"^%s = (.+)$" % n, text, re.M) or [None, None])[1] for n in NAMES}


def main():
    p = subprocess.run([sys.executable, "infra/aws/terraform/harvest/gen_harvest_prefixes.py", "--check"],
                       capture_output=True, text=True, timeout=90)
    print("(a) gen_harvest_prefixes --check rc=%d %s" % (p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] or ""))
    base = subprocess.run(["git", "show", "%s:%s" % (CUT, MOD)], capture_output=True, text=True, timeout=30)
    if base.returncode != 0 or "REGISTRY_HASH" not in base.stdout:
        print("positive control failed: git show %s:%s returned nothing usable (rc=%d)" % (CUT, MOD, base.returncode))
        return 2
    before, now = consts(base.stdout), consts(open(MOD, encoding="utf-8").read())
    moved = [n for n in NAMES if before[n] != now[n] or now[n] is None]
    print("(b) constants at the cut vs now: %d of %d byte-equal; moved %s" % (len(NAMES) - len(moved), len(NAMES), moved))
    ok = p.returncode == 0 and not moved
    print("THE STAMP IS GREEN AND THE FOUR CONSTANTS DID NOT MOVE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
