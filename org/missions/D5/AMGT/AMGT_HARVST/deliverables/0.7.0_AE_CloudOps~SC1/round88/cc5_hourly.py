"""HVST-cc-5 step 6: the hourly interim read, read only, the runner is never stopped.

Usage: python cc5_hourly.py <N>      writes cc5_check_interim<N>.out beside this file and prints its verdict lines.

Runs `seed_silver_known check --since <T0_3>` from the runner pin over every publisher in the snapshot, then reads the
runner's S3 ledger since T0_3 for the per-command GET sums, the largest single upload-harvest line, and the R7 projection.
IMMEDIATE BRANCH F flags (step 6b): one upload-harvest line above 50 GETs, upload GETs above 1 GiB since T0_3, a
duplicate, or R7 above 5 GiB. The flags are printed, never acted on here.
"""
from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

T0_3 = "2026-10-16T16:19:39Z"
PIN = Path(r"C:\dev\wk-harvest-runner-pin-ddd7dcdc38")
RUNTIME = r"C:\dev\ajb_workspace\.runtime\harvest-cycle\runtime"
LEDGER = Path(RUNTIME) / "s3_get_ledger.jsonl"
LOG = Path(r"C:\dev\ajb_workspace\.runtime\harvest-cycle\state\cycle_runner.log")
HERE = Path(__file__).resolve().parent
GIB = 2 ** 30


def main(n):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = ["HVST-cb-15 interim check %s taken %s: check --since %s (cc-5 T0, held in the name T0_3) over wsj barrons sa bbg (bbg is off the list; its tables stay in the snapshot)" % (n, now, T0_3)]
    proc = subprocess.run(
        [sys.executable, "-m", "lib.opal_data_harvest.seed_silver_known", "check", "--runtime-root", RUNTIME,
         "--publishers", "wsj", "barrons", "sa", "bbg", "--since", T0_3],
        cwd=str(PIN), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out.extend(proc.stdout.strip().splitlines())
    if proc.stderr.strip():
        out.append("STDERR: " + proc.stderr.strip()[:400])
    out.append("check rc=%d" % proc.returncode)
    dup = [ln for ln in proc.stdout.splitlines() if ln.startswith("DUPLICATES=")]
    rows = [json.loads(ln) for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()]
    a = [r for r in rows if r["ended_at"] > T0_3]
    run = [r for r in a if r["command"] == "run"]
    up = [r for r in a if r["command"] == "upload-harvest"]
    upg = sum(r["get_count"] for r in up)
    upb = sum(r["get_bytes"] for r in up)
    mx = max([r["get_count"] for r in up] or [0])
    out.append("R7 ledger lines after T0_3: %d" % len(a))
    out.append("R7 command=run lines=%d sum_get_count=%d sum_get_bytes=%d" % (len(run), sum(r["get_count"] for r in run), sum(r["get_bytes"] for r in run)))
    out.append("R7 command=upload-harvest lines=%d sum_get_count=%d sum_get_bytes=%d max_single_line_get_count=%d" % (len(up), upg, upb, mx))
    avg_run = (sum(r["get_bytes"] for r in run) / len(run)) if run else 0
    avg_up = (upb / len(up)) if up else 0
    per_job = (len(up) / len(run)) if run else 0
    proj = (avg_run + avg_up * per_job) * 242
    out.append("R7 projection of a 242-pair cycle = (%.0f + %.0f x %.4f) x 242 = %.0f bytes = %.4f GiB (bar 5 GiB; over bar: %s)" % (avg_run, avg_up, per_job, proj, proj / GIB, proj / GIB > 5))
    flags = []
    if mx > 50:
        flags.append("a single upload-harvest line above 50 GETs")
    if upb > GIB:
        flags.append("upload GET bytes above 1 GiB since T0_3")
    if not dup or dup[-1] != "DUPLICATES=0" or proc.returncode != 0:
        flags.append("the check did not end DUPLICATES=0 rc=0")
    if proj / GIB > 5:
        flags.append("R7 above 5 GiB")
    out.append("BRANCH-F FLAGS: %s" % ("; ".join(flags) if flags else "none"))
    jobs = [ln for ln in LOG.read_text(encoding="utf-8", errors="replace").splitlines() if ln[:20] >= T0_3 and " JOB sa " in ln]
    st = {}
    for ln in jobs:
        s = ln.split("status=")[1].split(" ")[0]
        st[s] = st.get(s, 0) + 1
    out.append("sa JOB lines since cc-5 T0: %d %s ; last log line: %s" % (len(jobs), st, LOG.read_text(encoding="utf-8", errors="replace").splitlines()[-1][:120]))
    (HERE / ("cc5_check_interim%d.out" % n)).write_text("\n".join(out) + "\n", encoding="ascii", errors="replace")
    print("\n".join(out[-9:]))


if __name__ == "__main__":
    main(int(sys.argv[1]))
