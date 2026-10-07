"""ETFS_RIVALS round 20 -- the CTO's term 1 (msg 30897): DELTA 0 on the served rankings (2.0.0_SA_COO~RV).

    python delta0_proof.py <code root> <page day YYYY-MM-DD> <out dir>

Builds gold holding_contribution for one real day THREE times through a read-only overlay (reads: local layer, then live
S3; every write lands in the arm's own local layer; no S3 write, no vendor call):
  A  clean                 -- the live inputs as they are;
  B  backfill-marked plant -- A plus planted G4 partitions on past trading days that hold no partition today, rows carrying
                              px_close only and as_of_source "backfill" (the shape market-range writes);
  C  control plant         -- the same partitions with as_of_source "historical" (an ordinary past-date market row).
The planted closes are the newest live close of each security moved by a different factor per day, so two consecutive
planted days imply a return the holding-implied path does not.
Prints, per fund: rows, the table's content hash in A, B and C, and whether A == B and A == C. The claim proved is
A == B for every fund (and for the whole table); the control is that C differs, so the comparison can fail."""
from __future__ import annotations

import datetime as dt
import importlib.util
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY = sys.argv[2]
OUT = pathlib.Path(sys.argv[3]).resolve()
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))

_spec = importlib.util.spec_from_file_location("r12_real_run", pathlib.Path(__file__).resolve().parent.parent / "round12" / "real_run.py")
r12 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r12)  # OverlaySink only; main() is not called

import pandas as pd  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from lib import trading_calendar as tc  # noqa: E402
from rivalfunds import enrichment_bloomberg as eb  # noqa: E402
from rivalfunds import gold_holding_contribution as hc  # noqa: E402
from rivalfunds import homes, sinks  # noqa: E402

G4 = homes.address("rivalfunds", "etfs", "gold", "security_market", "date=")
N_DAYS = 25


def plant(s_local, live, mark: str, days: list[str], base: pd.DataFrame) -> int:
    n = 0
    for i, d in enumerate(days):
        rows = []
        for r in base.itertuples():
            row = {c: None for c in eb.MARKET_COLUMNS}
            row.update({"security_id": r.security_id, "security_bloomberg": r.security_bloomberg, "date": dt.date.fromisoformat(d),
                        "px_close": float(r.px_close) * (1.0 + 0.013 * ((i % 7) - 3)), "source": eb.MARKET_SOURCE_HIST,
                        "as_of": dt.date.fromisoformat(d), "as_of_source": mark, "claim": "MEASURED",
                        "revision": "20261007T000000Z-delta0proof0", "produced_at": "2026-10-07T00:00:00Z"})
            rows.append(row)
        s_local.put(eb.market_target_uri(d, "20261007T000000Z-delta0proof0"), eb._parquet_bytes(eb._market_table(rows)))
        n += len(rows)
    return n


def run_arm(name: str, mark: str | None, days: list[str], base: pd.DataFrame) -> pd.DataFrame:
    s = r12.OverlaySink(OUT / f"layer_{name}")
    planted = plant(s.local, s.live, mark, days, base) if mark else 0
    r = hc.handler_entry({"date": DAY, "sink": s})
    uris = [u for u in s.local.list(homes.address("rivalfunds", "etfs", "gold", "holding_contribution", f"date={DAY}") + "/")
            if u.endswith(".parquet")]
    print(f"arm {name}: planted rows {planted} | handler {r.get('status')} | table objects written locally {len(uris)}")
    if not uris:
        raise SystemExit(f"arm {name}: no table written: {str(r.get('detail'))[:300]}")
    return pq.read_table(io.BytesIO(s.local.get(sorted(uris)[-1]))).to_pandas()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    live = sinks.S3Sink()
    day = dt.date.fromisoformat(DAY)
    have = sorted({u.split("date=", 1)[1][:10] for u in live.list(G4) if "date=" in u})
    newest = [d for d in have if d <= DAY][-1]
    us = sorted(u for u in live.list(G4 + newest + "/") if u.endswith(".parquet"))
    base = pq.read_table(io.BytesIO(live.get(us[-1]))).to_pandas()
    base = base[base.px_close.notna() & (base.px_close > 0)][["security_id", "security_bloomberg", "px_close"]]
    cand = [d.isoformat() for d in tc.trading_days_between(day - dt.timedelta(days=120), day - dt.timedelta(days=8))]
    days = [d for d in cand if d not in have][-N_DAYS:]
    print(f"live G4 partitions: {len(have)} ({have[0]}..{have[-1]}) | base close date {newest}, {len(base)} priced securities | "
          f"planted days: {len(days)} ({days[0]}..{days[-1]}), none holding a live partition")
    frames = {"A": run_arm("A", None, days, base), "B": run_arm("B", eb.BACKFILL_SOURCE, days, base),
              "C": run_arm("C", "historical", days, base)}
    fund_col = "fund_ticker" if "fund_ticker" in frames["A"].columns else "fund_id"
    rec = {"day": DAY, "code_root": str(ROOT), "planted_days": days, "planted_rows_per_arm": len(days) * len(base),
           "whole_table": {k: hc._content_sha(v) for k, v in frames.items()}, "rows": {k: int(len(v)) for k, v in frames.items()},
           "funds": {}}
    print(f"{'fund':<6} {'rows':>5}  {'A':<14} {'B':<14} {'C':<14} A==B  A==C")
    for f in sorted(frames["A"][fund_col].dropna().unique()):
        sha = {k: hc._content_sha(v[v[fund_col] == f].reset_index(drop=True)) for k, v in frames.items()}
        n = int((frames["A"][fund_col] == f).sum())
        rec["funds"][str(f)] = {"rows": n, **sha, "A_eq_B": sha["A"] == sha["B"], "A_eq_C": sha["A"] == sha["C"]}
        print(f"{str(f):<6} {n:>5}  {sha['A'][:12]:<14} {sha['B'][:12]:<14} {sha['C'][:12]:<14} {sha['A'] == sha['B']!s:<5} {sha['A'] == sha['C']}")
    src = {k: v["price_source"].value_counts().to_dict() if "price_source" in v.columns else {} for k, v in frames.items()}
    rec["price_source_counts"] = src
    eq_b = sum(1 for x in rec["funds"].values() if x["A_eq_B"])
    eq_c = sum(1 for x in rec["funds"].values() if x["A_eq_C"])
    rec["funds_equal_with_backfill_rows"] = f"{eq_b} of {len(rec['funds'])}"
    rec["funds_equal_with_control_rows"] = f"{eq_c} of {len(rec['funds'])}"
    rec["whole_table_A_eq_B"] = rec["whole_table"]["A"] == rec["whole_table"]["B"]
    rec["whole_table_A_eq_C"] = rec["whole_table"]["A"] == rec["whole_table"]["C"]
    print("price_source counts:", json.dumps(src))
    print(f"whole table A == B: {rec['whole_table_A_eq_B']} | funds equal with backfill-marked rows: {rec['funds_equal_with_backfill_rows']} | "
          f"control (historical-marked rows) whole table A == C: {rec['whole_table_A_eq_C']}, funds equal {rec['funds_equal_with_control_rows']}")
    (OUT / f"delta0_{DAY}.json").write_text(json.dumps(rec, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
