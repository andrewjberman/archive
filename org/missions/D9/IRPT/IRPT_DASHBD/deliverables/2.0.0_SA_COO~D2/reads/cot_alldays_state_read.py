"""Read-only census of the Cottonwood days an all-days rewrite from the claim floor would touch (IRPT_DASHBD round 150, issuer 2.0.0_SA_COO~D2).

Prints counts and ISO dates only: the fact_allocations partitions on or after the floor, the landed gold days on or after the floor, the landed days with no allocations partition
(a rewrite refuses them), the allocations days with no gold day (a rewrite never lands them), and the landed days split into rewrite events of at most 25 days.
Usage: python -I <this file> [--floor 2026-07-10] [--out <json path>]
"""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[8]
sys.path.insert(0, str(ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters"))
sys.path.insert(0, str(ROOT / "lib"))
import boto3  # noqa: E402
import cottonwood_bd_account_return_daily as cbd  # noqa: E402
import trading_calendar as tc  # noqa: E402

EVENT_MAX = 25


def chunks(days, n):
    return [days[i:i + n] for i in range(0, len(days), n)]


def runs_of_landed(gold):
    """Maximal runs of consecutive TRADING days that are all landed (a rewrite range must hold landed trading days only)."""
    if not gold:
        return []
    landed, runs, cur = set(gold), [], []
    for d in tc.trading_days_between(datetime.date.fromisoformat(gold[0]), datetime.date.fromisoformat(gold[-1])):
        iso = d.isoformat()
        if iso in landed:
            cur.append(iso)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def main():
    floor = sys.argv[sys.argv.index("--floor") + 1] if "--floor" in sys.argv else "2026-07-10"
    s3 = boto3.client("s3", region_name="us-east-1")
    rd = cbd.CottonwoodBlackDiamondSilverReader(s3)
    alloc = sorted(p for p in rd.list_partitions("fact_allocations") if p >= floor)
    gbucket, gprefix = cbd.gold_prefix()
    gold, token = [], None
    while True:
        kw = {"Bucket": gbucket, "Prefix": gprefix, "Delimiter": "/"}
        if token:
            kw["ContinuationToken"] = token
        page = s3.list_objects_v2(**kw)
        for cp in page.get("CommonPrefixes", []):
            tail = cp["Prefix"][len(gprefix):].strip("/")
            if tail.startswith("date=") and tail[len("date="):] >= floor:
                gold.append(tail[len("date="):])
        if not page.get("IsTruncated"):
            break
        token = page["NextContinuationToken"]
    gold = sorted(gold)
    out = {"claim": "measured", "floor": floor, "denominators": {"allocations_partitions_from_floor": len(alloc), "gold_days_from_floor": len(gold)},
           "landed_without_allocations": [d for d in gold if d not in set(alloc)], "allocations_without_gold": [d for d in alloc if d not in set(gold)],
           "events": [{"first": c[0], "last": c[-1], "days": len(c)} for r in runs_of_landed(gold) for c in chunks(r, EVENT_MAX)]}
    text = json.dumps(out, indent=1)
    if "--out" in sys.argv:
        Path(sys.argv[sys.argv.index("--out") + 1]).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
