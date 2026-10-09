"""TO-DB-b-69 (S32): classify_and_sum on named custodian transaction partitions, in ONE process, under whichever interpreter runs it.

Usage (worktree root): <python> <this file> <out.json> <day>[,<day>...]
Reads S3 only. The days' partitions are read through the producer's own FlowCache (so in-kind closes and the account filter are the
production path), with the account set the handler's --local mode uses (the declared population unioned with the newest reporting
partition's accounts). Writes the per-day output (flow, income, unvalued, cash_unknown, census) and this process's runtime versions.
The output file holds account ids and stays in .scratch; the committed record holds counts and numbers only.
"""
import json
import platform
import sys
from pathlib import Path

import numpy
import pandas
import pyarrow

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))


def main(out, days):
    import boto3
    from botocore.config import Config
    import handler as h
    ard = h.ard
    rt = {"python": platform.python_version(), "pandas": pandas.__version__, "numpy": numpy.__version__,
          "pyarrow": pyarrow.__version__}
    print("RUNTIME " + json.dumps(rt), flush=True)
    s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
    doc = ard.load_declaration()
    src = ard.source_entry(doc, ard.declared_sources(doc)[0])
    firm = ard.firm_scope(src)
    bucket, key_prefix = h._gold_location(firm)
    accounts = h.account_set(h.population_accounts(s3, firm)[1],
                             h.newest_accounts(s3, bucket, key_prefix, h.newest_landed_day(s3, bucket, key_prefix)))
    table, keycols = ard.load_classification(src)
    flows = ard.FlowCache(s3, src, table, keycols, accounts)
    res = {"runtime": rt, "n_accounts": len(accounts), "days": {}}
    for day in days:
        flow, income, unvalued, cash_unknown, absent = flows.get(day)
        res["days"][day] = {"flow": flow, "income": income, "unvalued": unvalued, "cash_unknown": cash_unknown,
                            "partition_absent": bool(absent), "census": flows.census.get(day)}
        print("DAY %s flow=%d income=%d unvalued=%d cash_unknown=%d" % (day, len(flow), len(income), len(unvalued), len(cash_unknown)), flush=True)
    Path(out).write_text(json.dumps(res, sort_keys=True, default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2].split(","))
