"""HVST-cb-10 read: how many S3 GETs does ONE collector job make, counted inside the job's own process?

Runs exactly the argument list `backfill_driver.Collector.run_job` spawns for one pair (same flags, a copy of the
security file the driver wrote), in THIS process so `store.get_stats_snapshot()` can be read at the end, against a
scratch runtime root so the production runner's progress database and sessions are not touched. It uploads nothing:
the `run` command writes local files only (the uploader is the separate `upload-harvest` command).

Usage: python cb10_job_get_probe.py <publisher> <security.json> [<floor>]
Prints one line: PROBE publisher=.. get_count=.. get_bytes=.. status=..
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, r"C:\dev\ajb_workspace")
from lib.opal_data_harvest import __main__ as collector  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def main():
    publisher, security_file = sys.argv[1], sys.argv[2]
    floor = sys.argv[3] if len(sys.argv) > 3 else "2026-10-14"
    scratch = Path(tempfile.mkdtemp(prefix="cb10-probe-"))
    store.get_stats_reset()
    sys.argv = ["lib.opal_data_harvest", "run", "--runtime-root", str(scratch), "--harvest-grammar",
                "--retrieval-mode", "backfill", "--floor", floor, "--new-only", "--no-sign-in",
                "--security-json", security_file, "--publishers", publisher, "--max-jobs", "1"]
    status = None
    try:
        collector.main()
    except SystemExit:
        pass
    finally:
        snap = store.get_stats_snapshot()
        records = sorted((scratch / "run_records").glob("*.json"))
        keys = ""
        if records:
            record = json.loads(records[-1].read_text(encoding="utf-8"))
            jobs = record.get("jobs") or [{}]
            status = jobs[0].get("status")
            # HVST-cb-10 puts the process's own counters on the run record: the probe prints them beside its own.
            keys = " record_get_count=%s record_get_bytes=%s" % (record.get("s3_get_count"), record.get("s3_get_bytes"))
        ledger = scratch / "s3_get_ledger.jsonl"
        lines = len(ledger.read_text(encoding="utf-8").splitlines()) if ledger.exists() else 0
        print("PROBE publisher=%s get_count=%d get_bytes=%d status=%s%s ledger_lines=%d" % (
            publisher, snap["get_count"], snap["get_bytes"], status, keys, lines))


if __name__ == "__main__":
    main()
