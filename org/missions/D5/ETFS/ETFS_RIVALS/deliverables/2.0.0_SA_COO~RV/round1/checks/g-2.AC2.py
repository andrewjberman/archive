"""RIV-g-2 AC2 -- the flow control (FWD-5 ACCEPT: the fund growing or shrinking never shows as a trade).

Difference control on real data: one real canonical_shape day, and a second day that is the same book with every
quantity and value scaled by 1.037 (a pure inflow). infer_trades() must return ZERO rows for that pair. The positive
arm moves one position by +5% on top of the flow and must return exactly one 'add' for that position."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    import pandas as pd
    from rivalfunds.gold_trade_schedule import infer_trades

    files = c.archive_files(1)
    sink = c.tmpdir("rv_g2b_")
    c.run_chain(sink, files, through="canonical")
    d = c.archive_meta(files[0])["requested_date"]
    day1, _ = c.read_parquets(c.local_path(sink, c.address("rivalfunds", "etfs", "gold", "canonical_shape", f"date={d}")))
    v.check(len(day1) > 0, f"a real canonical day ({len(day1)} rows)")
    if not len(day1):
        return
    nxt = (pd.Timestamp(d) + pd.offsets.BDay(1)).date().isoformat()

    def shifted(scale_one=None):
        day2 = day1.copy()
        day2["report_date"] = nxt
        day2["snapshot_id"] = day2["snapshot_id"].astype(str) + "-t"
        noncash = day2["position_type"].astype(str).str.lower() != "cash"
        for col in ("quantity", "market_value"):
            day2.loc[noncash, col] = day2.loc[noncash, col] * 1.037
        if scale_one is not None:
            for col in ("quantity", "market_value"):
                day2.loc[scale_one, col] = day2.loc[scale_one, col] * 1.05
        return pd.concat([day1, day2], ignore_index=True)

    neg = infer_trades(shifted())
    v.check(len(neg) == 0, f"pure 3.7% inflow -> 0 trades (got {len(neg)})")
    noncash_idx = day1.index[(day1["position_type"].astype(str).str.lower() != "cash") & (day1["quantity"] > 0)]
    target = noncash_idx[0]
    pos = infer_trades(shifted(scale_one=target))
    v.check(len(pos) == 1 and set(pos["action"]) == {"add"}, f"one position +5% on top of the flow -> exactly one 'add' (got {len(pos)}: {list(pos.get('action', []))})")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
