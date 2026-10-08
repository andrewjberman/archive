"""TO-DB-b-41: the primary-key uniqueness of the three tables over a WINDOW (the one-day release run has 0 realized rows).

Usage (worktree root): python <this file> <start> <end> <out.json>
Runs the producer's own compute_local over the trading days of [start, end] for the same 20 accounts as release_local_run.py, then
emit_day(upload=False) on every (table, day) so the producer's own refusals (a repeated key, a row off the day) are exercised.
Reads S3 only; writes one local JSON.
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
import account_activity_lots as aal  # noqa: E402
import release_local_run as rlr  # noqa: E402


def main(start, end, out):
    import boto3
    from botocore.config import Config
    s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
    days = [str(d)[:10] for d in aal.tc.trading_days_between(start, end)]
    accts = rlr.accounts()
    tables, run = aal.compute_local(s3, days, accts)
    res = {"window": [days[0], days[-1]], "trading_days": len(days), "accounts": len(accts), "tables": {}}
    for t in aal.TABLES:
        rows = tables[t]
        dup = aal.duplicate_keys(t, rows)
        by_day = Counter(r["business_date"] for r in rows)
        dry = {"days_emitted_dry": 0, "days_refused": []}
        for d in sorted(by_day):
            try:
                aal.emit_day(None, t, [r for r in rows if r["business_date"] == d], run["firm"], d, upload=False)
                dry["days_emitted_dry"] += 1
            except SystemExit as exc:
                dry["days_refused"].append({"day": d, "reason": str(exc)[:200]})
        outside = sum(1 for r in rows if r["business_date"] not in set(days))
        res["tables"][t] = {"primary_key": list(aal.PRIMARY_KEYS[t]), "rows": len(rows), "days_with_rows": len(by_day),
                            "distinct_keys": len(rows) - len(dup), "duplicate_keys": len(dup), "unique": not dup,
                            "rows_outside_the_window_days": outside, "dry_emit": dry,
                            "basis_source_census": dict(sorted(Counter(r.get("basis_source") for r in rows).items(), key=str))
                            if t != aal.TABLE_ACTIVITY else None}
    Path(out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({t: {k: v for k, v in x.items() if k in ("rows", "duplicate_keys", "unique", "rows_outside_the_window_days")}
                      for t, x in res["tables"].items()}))


if __name__ == "__main__":
    main(*sys.argv[1:4])
