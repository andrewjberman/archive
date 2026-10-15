"""Count-only: rows per fact_allocations partition across all partitions, and the empty ones."""
import sys
from pathlib import Path

ROOT = Path("C:/dev/wk-irpt-dashbd-188")
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import cottonwood_bd_account_return_daily as ad  # noqa: E402

reader = ad.CottonwoodBlackDiamondSilverReader()
parts = reader.list_partitions("fact_allocations")
empty = []
nonempty = []
for p in parts:
    t = reader.read_parquet("fact_allocations", p).to_pydict()
    n = len(t["AccountID"])
    (empty if n == 0 else nonempty).append((p, n))
print("partitions:", len(parts), "first", parts[0], "last", parts[-1])
print("empty partitions:", len(empty), "first empty", empty[0][0] if empty else None, "last empty", empty[-1][0] if empty else None)
print("nonempty partitions:", len(nonempty), "first nonempty", nonempty[0][0], "last nonempty", nonempty[-1][0])
print("empty partitions before 2026-06-22:", sum(1 for p, _ in empty if p < "2026-06-22"))
print("nonempty partitions before 2026-06-22:", sum(1 for p, _ in nonempty if p < "2026-06-22"))
print("S3 reads:", reader.reads)
