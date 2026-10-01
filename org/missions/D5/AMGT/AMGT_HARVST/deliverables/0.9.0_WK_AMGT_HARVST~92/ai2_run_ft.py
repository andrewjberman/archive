"""HVST-ai-2 run: the real collector on ft names in backfill-driver order, one job per name, mirroring
`backfill_driver.Collector.run_job` (same arguments, `--no-sign-in` included, cwd = this worktree), until the jobs span
`--span-minutes` (default 122) or a hard cap (`--cap-minutes`, default 178). A job whose status is a driver STOP status
ends the run (the driver would stop the ft leg). No upload is made. After every job the collected run records are written
to ai2_ft_longevity.json = {"run_records": [<each job's run record, verbatim>]}.

  OPAL_HARVEST_PROFILE_ROOT=<main>/.runtime/opal-data-harvest/browser-profiles \
  python ai2_run_ft.py --runtime-root <main>/.runtime/opal-data-harvest --workdir <dir> --out ai2_ft_longevity.json
"""
import argparse
import datetime as dt
import json
import os
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")
from lib.opal_data_harvest.__main__ import universe  # noqa: E402
from lib.opal_data_harvest.backfill_driver import STOP_STATUSES  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--runtime-root", required=True)
ap.add_argument("--workdir", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--span-minutes", type=float, default=122)
ap.add_argument("--cap-minutes", type=float, default=178)
ap.add_argument("--floor", default="2026-01-01")
ap.add_argument("--skip", nargs="*", default=[], help="universe keys to leave out")
args = ap.parse_args()

config = json.loads(Path("lib/opal_data_harvest/config.json").read_text(encoding="utf-8"))
rows = [r for r in universe(config) if r["key"] not in set(args.skip)]
runtime = Path(args.runtime_root).resolve()
workdir = Path(args.workdir)
(workdir / "securities").mkdir(parents=True, exist_ok=True)
started = time.time()
records, jobs = [], []


def stamp():
    return dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%S")


def cooldown_until():
    db = sqlite3.connect(str(runtime / "progress.sqlite3"), timeout=30)
    try:
        row = db.execute("SELECT until FROM cooldown WHERE publisher='ft'").fetchone()
    except sqlite3.OperationalError:
        return None
    finally:
        db.close()
    return float(row[0]) if row else None


def ts(x):
    return dt.datetime.fromisoformat(str(x).replace("Z", "+00:00"))


def span_minutes():
    starts = [ts(r["started_at"]) for r in records if r.get("started_at")]
    ends = [ts(r["finished_at"]) for r in records if r.get("finished_at")]
    return (max(ends) - min(starts)).total_seconds() / 60 if starts and ends else 0.0


def write_out():
    tmp = Path(args.out + ".tmp")
    tmp.write_text(json.dumps({"run_records": records}, indent=1), encoding="utf-8")
    os.replace(tmp, args.out)


for sec in rows:
    if span_minutes() >= args.span_minutes:
        print("%s DONE: span %.1f min >= %.0f" % (stamp(), span_minutes(), args.span_minutes), flush=True)
        break
    until = cooldown_until()
    if until and until > time.time():
        print("%s COOLDOWN ft: waiting %d s" % (stamp(), int(until - time.time()) + 1), flush=True)
        time.sleep(until - time.time() + 1)
    remaining = args.cap_minutes * 60 - (time.time() - started)
    if remaining < 120:
        print("%s CAP reached before the next job" % stamp(), flush=True)
        break
    sec_file = workdir / "securities" / (sec["key"] + ".json")
    sec_file.write_text(json.dumps(sec, indent=2), encoding="utf-8")
    cmd = [sys.executable, "-m", "lib.opal_data_harvest", "--runtime-root", str(runtime), "run", "--harvest-grammar",
           "--retrieval-mode", "backfill", "--floor", args.floor, "--new-only", "--no-sign-in", "--security-json", str(sec_file),
           "--publishers", "ft", "--max-jobs", "1"]
    print("%s JOB START ft %s (%s) cap-remaining %.0f min" % (stamp(), sec["key"], sec["company"], remaining / 60), flush=True)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=remaining)
        out, rc = proc.stdout or "", proc.returncode
    except subprocess.TimeoutExpired as exc:
        out, rc = (exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else exc.stdout) or "", "TIMEOUT"
    path = None
    for line in out.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("event") == "job_finished":
            path = event.get("result")
    if not path or not Path(path).exists():
        print("%s JOB ft %s: no run record (rc=%s)" % (stamp(), sec["key"], rc), flush=True)
        break
    record = json.loads(Path(path).read_text(encoding="utf-8"))
    records.append(record)
    write_out()
    status = record.get("status")
    stored = sum(1 for o in (record.get("fetch_outcomes") or {}).values() if o.get("outcome") == "stored")
    print("%s JOB END ft %s status=%s stored=%d fetched=%d auth_refreshes=%s record=%s span=%.1f min"
          % (stamp(), sec["key"], status, stored, len(record.get("fetched_keys") or []), record.get("auth_refreshes"),
             Path(path).name, span_minutes()), flush=True)
    if status in STOP_STATUSES or status in {"auth_failed_after_refresh", "auth_expired", "session_expired"}:
        print("%s STOP: status %s ends the ft leg" % (stamp(), status), flush=True)
        break
print("%s RUN END: %d job(s), span %.1f min" % (stamp(), len(records), span_minutes()), flush=True)
