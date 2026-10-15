"""IRPT_DASHBD round 121, workstream B-49F, cell DB-b-242 (worker 0.9.0_WK_IRPT_DASHBD~196): the measured run of the hop-1
filled_report_values stage of the 49 Financial reporting gold, LOCAL, read-only.

It imports the reporting-gold handler of THIS worktree and calls the handler's own read path:
  (a) the account set the scheduled run derives for its newest landed returns day: run()'s account_set of population_accounts
      (the newest holdings partition) and newest_accounts (the accounts of the newest account_return_daily partition);
  (b) filled_inputs(s3, firm, accounts), timed (read_inputs_seconds, every S3 read it makes);
  (c) filled_day_rows(inp, firm, day, accounts) for the newest returns day, timed (build_day_seconds), counting the households
      (the second value it returns) and the rows.
Every S3 call goes through one client whose before-call hook refuses any operation but GetObject and ListObjectsV2 and counts
the rest of the calls. No writing function of the handler is called. It writes one private counts copy, to the directory given
as its only argument, and nothing else.

Usage: python -I <this file> <private_dir>
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]
RED = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "reporting-gold"
sys.path.insert(0, str(RED))

import boto3  # noqa: E402
import handler as h  # noqa: E402

FIRM = "49financial"
READ_OPS = ("GetObject", "ListObjectsV2")
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
    t1 = time.perf_counter()
    built = _phase("filled_day_rows", lambda: h.filled_day_rows(inp, firm, newest, accounts))
    build_s = time.perf_counter() - t1
    rows, households = built
    days_built = 1
    max_days = h.MAX_DAYS_PER_FIRE
    est = read_s + max_days * build_s / days_built
    measured = {
        "firm": firm,
        "day": newest,
        "population_day": pop_day,
        "population_accounts": len(pop),
        "newest_returns_accounts": len(newest_ids),
        "accounts": len(accounts),
        "households": households,
        "rows": len(rows),
        "days_built": days_built,
        "max_days_per_fire": max_days,
        "read_inputs_seconds": round(read_s, 3),
        "build_day_seconds": round(build_s, 3),
        "fire_estimate_seconds": round(est, 3),
        "s3_calls_by_operation": dict(sorted(COUNTS.items())),
        "s3_reads": sum(COUNTS.values()),
    }
    priv.mkdir(parents=True, exist_ok=True)
    out = priv / "counts_r121.json"
    out.write_text(json.dumps(measured, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print("OK: measured %d account(s), %d household(s), %d row(s) for one day; read %.3f s, build %.3f s, estimate %.3f s; S3 reads %d"
          % (len(accounts), households, len(rows), read_s, build_s, est, sum(COUNTS.values())))
    print("OK: private counts copy written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
