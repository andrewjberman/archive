"""TO-DB-b-55 (E3): fold per-run records (lots_750_run.py `default` mode) into LOTS_P95_E3.json and LOTS_P95_E3.md.

Usage (worktree root): python <this file> <outdir> <default_batch_size> <size>=<rec.json> [<size>=<rec.json> ...]
The runner records batch_size 0 for a `default` run (no --batch-size argument); the size in effect for each record is the
producer's DEFAULT_BATCH_SIZE when it ran, given as <size>. p95 is over the runs at the FINAL default only. Counts only in the .md.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path

DAY = "2026-10-06"
HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py"


INTERRUPTED = [
    {"label": "run 3 (was to be at 2000)", "killed_at_utc": "2026-10-08T21:48:23Z", "elapsed_s_at_last_progress": 360.0,
     "stage": "lots", "by": "dell2 /govern process reaper (issuer ruling, 22:3xZ)", "recorded_as_timing": False},
    {"label": "run 13 (at 1500)", "killed_at_utc": "2026-10-08T22:23:31Z", "elapsed_s_at_last_progress": 630.3,
     "stage": "lots", "by": "dell2 /govern process reaper (issuer ruling, 22:3xZ)", "recorded_as_timing": False}]


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def main(outdir, size, recs):
    import psutil
    out = Path(outdir)
    runs = []
    pop = None
    for i, sp in enumerate(recs, 1):
        bs, p = sp.split("=", 1)
        r = json.loads(Path(p).read_text(encoding="utf-8"))
        pop = r.get("population_count") or pop
        runs.append({
            "order": i, "batch_size": int(bs), "batch_size_arg": None, "stopped_at_cap": r["stopped_at_cap"],
            "lots_stage_completed": bool(r["lots"].get("completed")) and r.get("lots_refused") is None,
            "lots": {"wall_seconds": r["lots"]["wall_seconds"], "peak_mb": r["lots"]["peak_mb"]},
            "total": {"wall_seconds": r["total"]["wall_seconds"], "peak_mb": r["total"]["peak_mb"]},
            "accounts_run": r.get("accounts_run")})
    ts = [x["total"]["wall_seconds"] for x in runs if x["batch_size"] == int(size) and x["lots_stage_completed"]
          and x["total"]["wall_seconds"] is not None]
    p95 = round(pct(ts, 0.95), 2) if ts else None
    root = Path(".").resolve()
    rec = {
        "task_order": "IRPT_DASHBD.TO-DB-b-55", "worker": "0.9.0_WK_IRPT_DASHBD~33", "day": DAY,
        "population_count": pop, "runs": runs, "interrupted_runs": INTERRUPTED, "runs_at_default_count": len(ts),
        "p95_total_s": p95, "p95_method": "linear interpolation over total wall_seconds of runs at default_batch_size",
        "bar_s": 750, "default_batch_size": int(size),
        "handler_sha256": hashlib.sha256((root / HANDLER).read_bytes()).hexdigest(),
        "producer_sha256": hashlib.sha256((root / PRODUCER).read_bytes()).hexdigest(),
        "machine": {"cores": psutil.cpu_count(), "ram_gb": round(psutil.virtual_memory().total / 2 ** 30, 1),
                    "handler_workers": 12, "python": platform.python_version(), "os": platform.platform(),
                    "runs_in_parallel_by_this_worker": 1},
        "other_load": "dell2 reaper killed two runs (interrupted_runs); one other worker ran a light S3 analysis on this machine concurrently (per the issuer); "
                      "no other run of this order's runner in parallel"}
    (out / "LOTS_P95_E3.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    lines = ["# LOTS_P95_E3 -- full run p95 at the producer default (counts only)", "",
             "- day %s; population %s accounts; default batch size %d (runs pass no --batch-size)" % (DAY, pop, int(size)),
             "- runs at the default: %d; p95 of total wall seconds (linear interpolation): %s; bar 750" % (len(ts), p95),
             "", "| run | batch | lots stage completed | lots s | lots MB | total s | total MB |", "|---|---|---|---|---|---|---|"]
    for x in runs:
        lines.append("| %d | %d | %s | %s | %s | %s | %s |" % (x["order"], x["batch_size"], x["lots_stage_completed"],
                     x["lots"]["wall_seconds"], x["lots"]["peak_mb"], x["total"]["wall_seconds"], x["total"]["peak_mb"]))
    lines += ["", "- interrupted by the reaper, not timings: %d runs (at 360 s and 630 s into the lots stage)" % len(INTERRUPTED),
              "- machine: %d cores, %.1f GB, 12 handler workers; one other worker ran a light S3 analysis concurrently."
              % (rec["machine"]["cores"], rec["machine"]["ram_gb"])]
    (out / "LOTS_P95_E3.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("p95", p95, "over", len(ts), "runs; totals", ts)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
