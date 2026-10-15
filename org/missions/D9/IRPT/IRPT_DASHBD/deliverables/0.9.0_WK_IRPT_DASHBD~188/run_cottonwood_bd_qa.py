"""One LOCAL derivation run for IRPT_DASHBD TO-DB-b-234 (round 119, worker 0.9.0_WK_IRPT_DASHBD~188).

Selects the 25 lowest sha256 keys of AccountID among the accounts that are BOTH in the household frame and in the newest
fact_allocations partition; derives the account return rows from the link base to the newest partition through the
adapter's GET-only reader; writes the private parquet and the private counts file. Prints COUNTS only: no account id.

Usage: python -I run_cottonwood_bd_qa.py <repo_root>
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pyarrow.parquet as pq

FRAME = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~161/account_dim_dry_run.parquet")
PRIV = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~188")
LINK_BASE = "2026-06-22"
N_ACCOUNTS = 25


def load_adapter(root):
    path = root / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters" / "cottonwood_bd_account_return_daily.py"
    spec = importlib.util.spec_from_file_location("cottonwood_bd_account_return_daily", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    root = Path(sys.argv[1]).resolve()
    ad = load_adapter(root)
    PRIV.mkdir(parents=True, exist_ok=True)
    frame = set(v for v in pq.read_table(str(FRAME), columns=["account_id"]).to_pydict()["account_id"] if v)
    reader = ad.CottonwoodBlackDiamondSilverReader()
    newest = reader.list_partitions("fact_allocations")[-1]
    newest_accounts = ad.accounts_in_partition(reader, newest)
    both = sorted(frame & newest_accounts, key=ad.account_hash_key)
    chosen = both[:N_ACCOUNTS]
    rows, summary = ad.derive(reader, chosen, LINK_BASE, newest)
    table = ad.to_table(rows)
    out = PRIV / "cottonwood_bd_account_return_qa.parquet"
    pq.write_table(table, str(out))
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    derived = set(chosen)
    overlap = len(derived & frame)
    keys = [(r["account_id"], r["business_date"]) for r in rows]
    dup = len(keys) - len(set(keys))
    window = sorted(set(r["business_date"] for r in rows))
    counts = {
        "frame_accounts": len(frame), "newest_partition": newest, "newest_partition_accounts": len(newest_accounts),
        "frame_and_newest": len(both), "accounts": len(chosen), "derived_accounts": len(derived),
        "overlap": overlap, "rows": len(rows), "duplicate_keys": dup,
        "window_first": window[0] if window else None, "window_last": window[-1] if window else None,
        "by_day_quality": dict(sorted(summary["by_day_quality"].items())), "summary": summary,
        "private_parquet": str(out), "sha256": sha, "reads": reader.reads,
    }
    (PRIV / "derivation_counts.json").write_text(json.dumps(counts, indent=1, sort_keys=True), encoding="ascii")
    public = {k: v for k, v in counts.items() if k not in ("summary", "private_parquet")}
    public["flow_counts"] = summary["flow_counts"]
    public["census_rows"] = summary["census"]["rows"]
    public["census_partitions"] = summary["census"]["partitions"]
    print(json.dumps(public, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
