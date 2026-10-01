"""RIV-d-5 AC2 (live, READ-ONLY) -- the SERVED trade schedule pairs each fund with its OWN prior report date (row W1-S27):
for TSEL and WCMG (the two funds whose windows the global-prior pairing dropped), every served G5 window ending in the act's
replay window starts on that fund's previous served G1 report date.

Reads d5_live.json `replay_window` {start, end}; then the newest served G1 and G5 object per date under
rivalfunds/etfs/gold/{canonical_shape,trade_schedule}/."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _live as L  # noqa: E402


def newest_per_date(table, lo, hi):
    per = {}
    for k in L.keys(f"rivalfunds/etfs/gold/{table}/"):
        if k.endswith(".parquet"):
            d = k.split("date=")[1][:10]
            if lo <= d <= hi:
                per[d] = max(per.get(d, ""), k)
    return per


def run(v):
    w = L.record().get("replay_window") or {}
    lo, hi = w.get("start"), w.get("end")
    g1 = newest_per_date("canonical_shape", "0000", hi)
    g5 = newest_per_date("trade_schedule", lo, hi)
    for fund in ("TSEL", "WCMG"):
        dates = sorted(d for d, k in g1.items()
                       if fund in set(L.parquet(k)["fund_ticker"].astype(str).str.strip()))
        prev = {d: dates[i - 1] for i, d in enumerate(dates) if i > 0}
        bad, n = [], 0
        for d, k in sorted(g5.items()):
            df = L.parquet(k)
            t = df[df["fund_id"].astype(str) == fund]
            for s in set(t["window_start"].astype(str).str[:10]):
                n += 1
                if prev.get(d) != s:
                    bad.append((d, s, prev.get(d)))
        print(f"{fund}: {n} served windows in {lo}..{hi}; mismatched {bad[:3]}")
        v.check(n > 0 and not bad, f"{fund}: every served window starts on its own prior report date")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
