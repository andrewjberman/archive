"""Round-25 close run (2.0.0_SA_COO~H): re-run every drained order's criterion invocation at the trunk.

Each output goes to round25/rerun/<id>.txt. Tracked files a script rewrites are listed, then restored,
so the workers' committed outputs stay the record and this run adds only its own files.
"""
import datetime
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round25")
D = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/"
RUNS = [
    ("o1_ac1", [sys.executable, "-m", "pytest", "lib/opal_data_harvest/test_o1_run_record_reach.py", "lib/research/harvest/tests/test_o1_run_record_coverage.py", "lib/research/harvest/tests/test_publication_gold_daily.py", "-rA", "--tb=line"]),
    ("o1_ac2", [sys.executable, D + "0.9.0_WK_AMGT_HARVST~61/scripts/o1_ac2_coverage_before_after.py"]),
    ("o1_ac3", [sys.executable, "-m", "pytest", "lib/opal_data_harvest/", "lib/research/harvest/tests/", "-rA", "--tb=line"]),
    ("o2_ac1", [sys.executable, D + "0.9.0_WK_AMGT_HARVST~62/scripts/o2_ac1_stub_argv.py"]),
    ("o2_ac2", [sys.executable, "-m", "pytest", "lib/opal_data_harvest/", "-rA", "--tb=line"]),
    ("o3_ac1", [sys.executable, "-m", "pytest", "lib/research/harvest/tests/test_o3_silver_tie_break.py", "-rA", "--tb=line"]),
    ("o3_ac2", [sys.executable, D + "0.9.0_WK_AMGT_HARVST~63/scripts/o3_ac2_readers_and_served_ties.py"]),
    ("o3_ac3", [sys.executable, "-m", "pytest", "lib/research/harvest/tests/", "lib/research/api/tests/test_timeline_routes.py", "-rA", "--tb=line"]),
    ("o4_ac1", [sys.executable, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round25/checks/" + "o-4.AC1.py"]),
    ("o4_ac2", [sys.executable, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round25/checks/" + "o-4.AC2.py"]),
    ("o5_ac1", [sys.executable, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round25/checks/" + "o-5.AC1.py"]),
    ("o5_ac2", [sys.executable, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round25/checks/" + "o-5.AC2.py"]),
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
