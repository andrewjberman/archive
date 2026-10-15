"""IRPT_DASHBD round 122, workstream B-49F, cell DB-b-246 (worker 0.9.0_WK_IRPT_DASHBD~200): the PEAK RESIDENT MEMORY and the
per-day time of the hop-1 filled_report_values stage on the newest landed returns day, measured LOCAL, read-only.

It imports the reporting-gold handler of THIS worktree and calls the handler's own read path for that day, as round 121 did:
  (a) the account set the scheduled run derives: population_accounts unioned with newest_accounts (account_set);
  (b) filled_inputs(s3, firm, accounts), timed (read_inputs_seconds);
  (c) filled_day_rows(inp, firm, day, accounts) for the newest returns day, timed (build_day_seconds), counting the households
      (the second value it returns) and the rows.
A daemon thread samples the process's resident set size (psutil) every SAMPLE_SECONDS for the whole measured section. Every S3
call goes through one client whose before-call hook refuses any operation but GetObject and ListObjectsV2 and counts the
calls made. The process also holds the interpreter, pandas and pyarrow; those are not subtracted.
It writes one private copy of the numbers to the directory given as its only argument, and nothing else.

Usage: python -I <this file> <private_dir>
"""
import json
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]
RED = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "reporting-gold"
sys.path.insert(0, str(RED))

import boto3  # noqa: E402
import psutil  # noqa: E402
import handler as h  # noqa: E402

FIRM = "49financial"
READ_OPS = ("GetObject", "ListObjectsV2")
SAMPLE_SECONDS = 0.25
MB = 1048576.0
COUNTS = {}


def _hook(model=None, **kwargs):
    name = model.name if model is not None else "unnamed"
    if name not in READ_OPS:
        raise SystemExit("REFUSED: S3 operation %s is not a read; this measurement reads only" % name)
    COUNTS[name] = COUNTS.get(name, 0) + 1


def _phase(name, fn):
    try:
        return fn()
    except (Exception, SystemExit) as exc:  # noqa: BLE001
        print("BLOCKED: phase %s raised %s" % (name, type(exc).__name__))
        sys.exit(2)


class Sampler(threading.Thread):
    def __init__(self, proc, first):
        threading.Thread.__init__(self)
        self.daemon = True
        self.proc = proc
        self.halt = threading.Event()
        self.lock = threading.Lock()
        self.samples = [first]

    def _take(self):
        value = self.proc.memory_info().rss
        with self.lock:
            self.samples.append(value)
        return value

    def run(self):
        while not self.halt.is_set():
            self._take()
            self.halt.wait(SAMPLE_SECONDS)

    def mark(self):
        self._take()
        with self.lock:
            return max(self.samples)

    def peak(self):
        with self.lock:
            return max(self.samples)

    def count(self):
        with self.lock:
            return len(self.samples)

    def stop(self):
        self.halt.set()
        self.join()


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: python -I <this file> <private_dir>")
    priv = Path(argv[1])
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.meta.events.register("before-call.s3", _hook)
    doc = h.ard.load_declaration()
    firm = h.ard.firm_scope(h.ard.source_entry(doc, h.ard.declared_sources(doc)[0]))
    if firm != FIRM:
        raise SystemExit("REFUSED: the declared firm is not %s" % FIRM)
    bucket, key_prefix = h._gold_location(firm)
    proc = psutil.Process()
    baseline = proc.memory_info().rss
    sampler = Sampler(proc, baseline)
    sampler.start()
    newest = _phase("newest_returns_day", lambda: h.newest_landed_day(s3, bucket, key_prefix))
    if newest is None:
        print("BLOCKED: phase newest_returns_day found no partition")
        sys.exit(2)
    pop_day, pop = _phase("population_accounts", lambda: h.population_accounts(s3, firm))
    newest_ids = _phase("newest_accounts", lambda: h.newest_accounts(s3, bucket, key_prefix, newest))
    accounts = h.account_set(pop, newest_ids)
    t0 = time.perf_counter()
    inp = _phase("filled_inputs", lambda: h.filled_inputs(s3, firm, accounts))
    read_s = time.perf_counter() - t0
    peak_after = sampler.mark()
    t1 = time.perf_counter()
    built = _phase("filled_day_rows", lambda: h.filled_day_rows(inp, firm, newest, accounts))
    build_s = time.perf_counter() - t1
    rows, households = built
    peak = max(sampler.peak(), proc.memory_info().rss)
    sampler.stop()
    measured = {
        "firm": firm,
        "day": newest,
        "population_day": pop_day,
        "population_accounts": len(pop),
        "newest_returns_accounts": len(newest_ids),
        "accounts": len(accounts),
        "households": households,
        "rows": len(rows),
        "read_inputs_seconds": round(read_s, 3),
        "build_day_seconds": round(build_s, 3),
        "day_seconds": round(read_s + build_s, 3),
        "baseline_rss_mb": round(baseline / MB, 1),
        "peak_after_inputs_mb": round(peak_after / MB, 1),
        "peak_rss_mb": round(peak / MB, 1),
        "sampler": {
            "interval_seconds": SAMPLE_SECONDS,
            "samples": sampler.count(),
            "method": "psutil.Process().memory_info().rss read by a daemon thread every 0.25 s over the measured section, "
                      "plus direct readings at the start, at the end of filled_inputs and after filled_day_rows",
        },
        "s3_calls_by_operation": dict(sorted(COUNTS.items())),
        "s3_reads": sum(COUNTS.values()),
    }
    priv.mkdir(parents=True, exist_ok=True)
    out = priv / "memory_r122.json"
    out.write_text(json.dumps(measured, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print("OK: measured %d account(s), %d household(s), %d row(s) for one day; read %.3f s, build %.3f s; baseline %.1f MB, "
          "after inputs %.1f MB, peak %.1f MB; samples %d; S3 reads %d"
          % (len(accounts), households, len(rows), read_s, build_s, baseline / MB, peak_after / MB, peak / MB,
             measured["sampler"]["samples"], sum(COUNTS.values())))
    print("OK: private copy written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
