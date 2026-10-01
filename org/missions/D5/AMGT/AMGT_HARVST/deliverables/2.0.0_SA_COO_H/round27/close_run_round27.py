"""Round-27 close run (2.0.0_SA_COO~H): re-run every drained order's criterion invocation at the trunk.

Each output goes to round27/rerun/<id>.txt. Tracked files a script rewrites are listed, then restored,
so the workers' committed outputs stay the record and this run adds only its own files.
"""
import datetime
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round27")
D = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/"
RUNS = [
    ("q2_ac1", [sys.executable] + ['-m', 'pytest', 'lib/opal_data_harvest/test_q2_bbg_as_received.py', '-rA', '--tb=line']),
    ("q2_ac2", [sys.executable] + ['org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~71/scripts/q2_ac2_real_bbg_objects.py']),
    ("q2_ac3", [sys.executable] + ['-m', 'pytest', 'lib/opal_data_harvest/', 'lib/research/harvest/tests/', '-rA', '--tb=line']),
    ("q3_ac1", [sys.executable] + ['org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~72/scripts/q3_ac1_eligibility_census.py']),
    ("q4_ac1", [sys.executable] + ['-m', 'pytest', 'lib/research/metrics/tests/test_q4_rank_declared_set.py', '-rA', '--tb=line']),
    ("q4_ac2", [sys.executable] + ['org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~73/scripts/q4_ac2_gold_branch_in_memory.py']),
    ("q4_ac3", [sys.executable] + ['-m', 'pytest', 'lib/research/metrics/tests/', '-rA', '--tb=line']),
    ("q5_ac1", [sys.executable] + ['-m', 'pytest', 'lib/research/harvest/tests/test_q5_covered_vs_found.py', '-rA', '--tb=line']),
    ("q5_ac2", [sys.executable] + ['org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~74/scripts/q5_ac2_lenovo_2026_02_12.py']),
    ("q5_ac3", [sys.executable] + ['-m', 'pytest', 'lib/research/harvest/tests/', 'lib/research/api/tests/test_timeline_routes.py', '-rA', '--tb=line']),
    ("q6_ac1", [sys.executable] + ['-m', 'pytest', 'lib/opal_data_harvest/test_q6_barrons_guard_ft_body.py', '-rA', '--tb=line']),
    ("q6_ac2", [sys.executable] + ['org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~75/scripts/q6_ac2_replay_recorded_shapes.py']),
    ("q6_ac3", [sys.executable] + ['-m', 'pytest', 'lib/opal_data_harvest/', '-rA', '--tb=line']),
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
