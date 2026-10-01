"""Round 27 AC (IB-pr-274: CTO round-26 analysis ruling 5, row S235) -- the 49 Financial Schwab silver for trading day
2026-09-29 exists for the three tables the 49F holdings producer and IRPT_DASHBD's adapter read, and the cause is recorded.

Usage: python p27_4_schwab_silver_0929.py <worktree root>
HEAD s3://opal-data-assets/schwab/08335338/silver/{dim_position,dim_balance,fact_trn}/date=2026-09-29/data.parquet (each 200), and
reads org/tier2_senior/0.6.2_AE_PartnerETL~C/deliverables/SCHWAB_SILVER_20260929_CAUSE.md (exists, names the cause in its first
heading line).
Pass line: P27-4-AC1 PASS. Base: FAIL (dim_position date=2026-09-29 absent, read at the cut).
"""
import sys
from pathlib import Path

import boto3

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def fail(msg):
    print("P27-4-AC1 FAIL: " + msg)
    sys.exit(1)


s3 = boto3.client("s3", region_name="us-east-1")
for t in ("dim_position", "dim_balance", "fact_trn"):
    key = "schwab/08335338/silver/%s/date=2026-09-29/data.parquet" % t
    try:
        h = s3.head_object(Bucket="opal-data-assets", Key=key)
    except Exception as exc:  # noqa: BLE001
        fail("%s absent (%s)" % (key, str(exc)[:80]))
    print("  %s: %d bytes at %s" % (key, h["ContentLength"], h["LastModified"].isoformat()))
cause = root / "org/tier2_senior/0.6.2_AE_PartnerETL~C/deliverables/SCHWAB_SILVER_20260929_CAUSE.md"
if not cause.exists() or not cause.read_text(encoding="utf-8").strip():
    fail("cause record absent: %s" % cause)
print("P27-4-AC1 PASS")
