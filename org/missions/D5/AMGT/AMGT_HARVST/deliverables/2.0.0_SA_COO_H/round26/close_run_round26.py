"""Round-26 close run (2.0.0_SA_COO~H): re-run every drained order's criterion invocation at the trunk.

Each output goes to round26/rerun/<id>.txt. Tracked files a script rewrites are listed, then restored,
so the workers' committed outputs stay the record and this run adds only its own files.
"""
import datetime
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round26")
D = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/"
RUNS = [
    ("p1_ac1", [sys.executable, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round26/checks/p-1.AC1.py"]),
    ("p1_ac2", [sys.executable, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round26/checks/p-1.AC2.py"]),
    ("p2_ac1", [sys.executable, D + "0.9.0_WK_AMGT_HARVST~67/scripts/p2_ac1_causes.py"]),
    ("p2_ac2", [sys.executable, "-m", "pytest", "lib/opal_data_harvest/test_p2_fetched_and_stored_keys.py", "-rA", "--tb=line"]),
    ("p2_ac3", [sys.executable, "-m", "pytest", "lib/opal_data_harvest/", "-rA", "--tb=line"]),
    ("p3_ac1", [sys.executable, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round26/checks/p-3.AC1.py"]),
    ("p3_ac2", [sys.executable, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round26/checks/p-3.AC2.py"]),
    ("p4_ac1", [sys.executable, D + "0.9.0_WK_AMGT_HARVST~69/scripts/p4_ac1_refusals.py"]),
    ("p4_ac2", [sys.executable, D + "0.9.0_WK_AMGT_HARVST~69/scripts/p4_ac2_route.py"]),
]


def tracked_changes():
    out = subprocess.run(["git", "diff", "--name-only", "--", D], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return set(out.split())


def main():
    os.makedirs(os.path.join(HERE, "rerun"), exist_ok=True)
    trunk = subprocess.run(["git", "rev-parse", "--short=10", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    print("== trunk %s %s" % (trunk, datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    before = tracked_changes()
    for rid, argv in RUNS:
        t0 = datetime.datetime.now()
        p = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=900)
        body = (p.stdout + p.stderr).decode("utf-8", errors="replace")
        with open(os.path.join(HERE, "rerun", rid + ".txt"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        last = [ln for ln in body.splitlines() if ln.strip()][-1:] or [""]
        secs = (datetime.datetime.now() - t0).total_seconds()
        print("%s rc=%d lines=%d secs=%.0f last=%s" % (rid, p.returncode, len(body.splitlines()), secs, last[0][:160]))
    touched = sorted(tracked_changes() - before)
    print("tracked files rewritten by the scripts: %d" % len(touched))
    for f in touched:
        print("  restored: " + f)
    if touched:
        subprocess.run(["git", "checkout", "--"] + touched, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
