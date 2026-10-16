"""HVST-cb-15 step 11 (i): the C-a4' close read at T0_3 + 6 h, read only, no stop file, no restart.

Usage: python cb15_c_a4.py       writes cb15_c_a4.out beside this file.

Holds, for the whole window since T0_3: (a) per upload-harvest line the get_count and get_bytes, (b) check --since T0_3 over
wsj, barrons, sa (and bbg, whose tables stay in the snapshot) ending DUPLICATES=0, (c) R7's projection for sa in GiB, with the
run-ledger sums beside it, plus the sa job counts. The verdict line says whether all three hold; it never acts.
"""
from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

T0_3 = "2026-10-16T08:40:17Z"
PIN = Path(r"C:\dev\wk-harvest-runner-pin-ddd7dcdc38")
RUNTIME = r"C:\dev\ajb_workspace\.runtime\harvest-cycle\runtime"
LEDGER = Path(RUNTIME) / "s3_get_ledger.jsonl"
LOG = Path(r"C:\dev\ajb_workspace\.runtime\harvest-cycle\state\cycle_runner.log")
HERE = Path(__file__).resolve().parent
GIB = 2 ** 30


def main():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = ["HVST-cb-15 C-a4' close read (amendment 4, step 11 i), taken %s, window T0_3 %s -> now; no stop file created, no restart" % (now, T0_3), ""]
    rows = [json.loads(ln) for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()]
    a = [r for r in rows if r["ended_at"] > T0_3]
    up = [r for r in a if r["command"] == "upload-harvest"]
    run = [r for r in a if r["command"] == "run"]
    out.append("(a) PER upload-harvest LINE since T0_3 (denominator: %d lines; ledger lines after T0_3 = %d, of which run = %d)" % (len(up), len(a), len(run)))
    for i, r in enumerate(up, 1):
        out.append("  #%d ended_at=%s get_count=%d get_bytes=%d" % (i, r["ended_at"], r["get_count"], r["get_bytes"]))
    upg = sum(r["get_count"] for r in up)
    upb = sum(r["get_bytes"] for r in up)
    mx = max([r["get_count"] for r in up] or [0])
    out.append("  SUM upload-harvest get_count=%d get_bytes=%d max_single_line_get_count=%d (Branch F thresholds: one line above 50; sum above 1 GiB)" % (upg, upb, mx))
    out.append("")
    out.append("(b) check --since %s" % T0_3)
    proc = subprocess.run(
        [sys.executable, "-m", "lib.opal_data_harvest.seed_silver_known", "check", "--runtime-root", RUNTIME,
         "--publishers", "wsj", "barrons", "sa", "bbg", "--since", T0_3],
        cwd=str(PIN), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out.extend(proc.stdout.strip().splitlines())
    out.append("check rc=%d" % proc.returncode)
    dup_ok = proc.returncode == 0 and any(ln == "DUPLICATES=0" for ln in proc.stdout.splitlines())
    out.append("")
    avg_run = (sum(r["get_bytes"] for r in run) / len(run)) if run else 0
    avg_up = (upb / len(up)) if up else 0
    per_job = (len(up) / len(run)) if run else 0
    proj = (avg_run + avg_up * per_job) * 242
    out.append("(c) R7 for sa, since T0_3: run lines=%d sum_get_count=%d sum_get_bytes=%d ; upload-harvest lines=%d sum_get_count=%d sum_get_bytes=%d" % (
        len(run), sum(r["get_count"] for r in run), sum(r["get_bytes"] for r in run), len(up), upg, upb))
    out.append("    projection of a 242-pair cycle = (avg run bytes %.0f + avg upload bytes %.0f x uploads-per-job %.4f) x 242 = %.0f bytes = %.4f GiB (bar 5 GiB; over bar: %s)" % (
        avg_run, avg_up, per_job, proj, proj / GIB, proj / GIB > 5))
    jobs = [ln for ln in LOG.read_text(encoding="utf-8", errors="replace").splitlines() if ln[:20] >= T0_3 and " JOB sa " in ln]
    st = {}
    stored = 0
    for ln in jobs:
        s = ln.split("status=")[1].split(" ")[0]
        st[s] = st.get(s, 0) + 1
        if "stored=" in ln:
            stored += int(ln.split("stored=")[1].split(" ")[0])
    out.append("    sa JOB lines since T0_3: %d %s ; articles stored: %d" % (len(jobs), st, stored))
    ok_a = mx <= 50 and upb <= GIB
    ok_c = proj / GIB <= 5
    out.append("")
    out.append("VERDICT: (a) per-upload GETs within bars=%s ; (b) DUPLICATES=0 rc=0=%s ; (c) R7 under 5 GiB=%s ; all three hold=%s -> %s" % (
        ok_a, dup_ok, ok_c, ok_a and dup_ok and ok_c, "C-a4' closes; do NOT create the stop file" if (ok_a and dup_ok and ok_c) else "BRANCH F AT ONCE"))
    (HERE / "cb15_c_a4.out").write_text("\n".join(out) + "\n", encoding="ascii", errors="replace")
    print("\n".join(out[-9:]))


if __name__ == "__main__":
    main()
