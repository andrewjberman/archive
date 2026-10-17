"""Read-only counts of the seven Cottonwood days the re-land pair covers, from the function's own source and sink (no id printed).

For each day: fact_allocations (rows, accounts), fact_transactions (rows, or absent) through the adapter's reader class, and the gold
account_return_daily day (rows, or absent). Run before dell1's carrier lane lands a day and again after it, so the second re-land pair
is cut on measured counts (IRPT_DASHBD round 150, issuer 2.0.0_SA_COO~D2). Usage: python -I <this file> [--out <json path>]
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[8]
sys.path.insert(0, str(ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters"))
sys.path.insert(0, str(ROOT / "lib"))
import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
import cottonwood_bd_account_return_daily as cbd  # noqa: E402

DAYS = ["2026-07-22", "2026-07-27", "2026-07-29", "2026-08-03", "2026-08-19", "2026-09-24", "2026-09-25"]


def main():
    s3 = boto3.client("s3", region_name="us-east-1")
    rd = cbd.CottonwoodBlackDiamondSilverReader(s3)
    alloc, trans = set(rd.list_partitions("fact_allocations")), set(rd.list_partitions("fact_transactions"))
    gbucket, gprefix = cbd.gold_prefix()
    gold, token = set(), None
    while True:
        kw = {"Bucket": gbucket, "Prefix": gprefix, "Delimiter": "/"}
        if token:
            kw["ContinuationToken"] = token
        page = s3.list_objects_v2(**kw)
        for cp in page.get("CommonPrefixes", []):
            tail = cp["Prefix"][len(gprefix):].strip("/")
            if tail.startswith("date="):
                gold.add(tail[len("date="):])
        if not page.get("IsTruncated"):
            break
        token = page["NextContinuationToken"]
    out = {"claim": "measured", "denominators": {"fact_allocations_partitions": len(alloc), "fact_transactions_partitions": len(trans), "gold_partitions": len(gold)}, "days": {}}
    for d in DAYS:
        row = {}
        if d in alloc:
            t = rd.read_parquet("fact_allocations", d).to_pydict()
            row["allocations"] = {"rows": len(t[cbd.ACCOUNT_COLUMN]), "accounts": len({a for a in t[cbd.ACCOUNT_COLUMN] if a is not None})}
        else:
            row["allocations"] = "absent"
        if d in trans:
            row["transactions_rows"] = rd.read_parquet("fact_transactions", d).num_rows
        else:
            row["transactions_rows"] = "absent"
        if d in gold:
            body = s3.get_object(Bucket=gbucket, Key="%sdate=%s/data.parquet" % (gprefix, d))["Body"].read()
            row["gold_rows"] = pq.read_table(io.BytesIO(body)).num_rows
        else:
            row["gold_rows"] = "absent"
        out["days"][d] = row
    text = json.dumps(out, indent=1)
    if "--out" in sys.argv:
        Path(sys.argv[sys.argv.index("--out") + 1]).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
