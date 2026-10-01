"""Round-31 close run (2.0.0_SA_COO~H): re-run every drained order's criterion invocation at the trunk.

Each output goes to round31/rerun/<id>.txt. Tracked files a script rewrites are listed, then restored,
so the workers' committed outputs stay the record and this run adds only its own files.
"""
import datetime
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round31")
D = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/"
RUNS = [
    ("ad1_ac1", [sys.executable] + ['org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~87/scripts/ad1_ac1_store_readback.py']),
    ("ad1_ac2", [sys.executable] + ['-m', 'pytest', 'lib/opal_data_harvest/test_ad1_token_store.py', '-rA', '--tb=line']),
    ("ad1_ac3", [sys.executable] + ['-m', 'pytest', 'lib/opal_data_harvest/', '-rA', '--tb=line']),
    ("ad2_ac1", [sys.executable] + ['org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round31/checks/ad-2.AC1.py']),
    ("ad2_ac2", [sys.executable] + ['org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round31/checks/ad-2.AC2.py']),
    ("ad3_ac1", [sys.executable] + ['org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~89/scripts/ad3_ac1_assignability.py']),
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
