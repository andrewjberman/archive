"""Read-only: in which fact_transactions partitions do rows with a given trade date appear, and how many distinct TransactionIDs (counts only)."""
import sys

sys.path.insert(0, "C:/dev/ajb_workspace/data/assets/scripts/gold/irpt_reporting/adapters")
sys.path.insert(0, "C:/dev/ajb_workspace/lib")
import boto3  # noqa: E402
import cottonwood_bd_account_return_daily as cbd  # noqa: E402

DAY = sys.argv[1]
rd = cbd.CottonwoodBlackDiamondSilverReader(boto3.client("s3", region_name="us-east-1"))
parts = [p for p in rd.list_partitions("fact_transactions") if p >= DAY]
seen_ids, total = set(), 0
out = []
for p in parts[:40]:
    d = rd.read_parquet("fact_transactions", p).to_pydict()
    n = 0
    ids = set()
    for tid, trade in zip(d["TransactionID"], d["Trade Date"]):
        if cbd.parse_trade_date(trade) == DAY:
            n += 1
            ids.add(tid)
    if n:
        out.append((p, n, len(ids), len(ids & seen_ids)))
        seen_ids |= ids
        total += n
print("trade date", DAY, "partitions >= it scanned", min(40, len(parts)))
for p, n, k, ov in out:
    print(p, "rows", n, "distinct ids", k, "already seen in an earlier partition", ov)
print("total rows over partitions", total, "distinct TransactionIDs", len(seen_ids))
