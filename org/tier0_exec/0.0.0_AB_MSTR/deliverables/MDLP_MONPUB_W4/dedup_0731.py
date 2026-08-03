"""MDLP_MONPUB.W4 -- produce the corrected 2026-07-31 data.pkl by removing the
month-end double-append rows, restoring exactly the shape Yang's own 13:08Z guard
would have produced. Deterministic; every drop is asserted. ASCII-only.

Dedup semantics (why not a naive drop_duplicates):
- price_monthly: dup pairs are fully value-identical -> drop either (asserted identical first).
- return_monthly: dup pairs DIFFER -- the monthly-sourced row carries monthly fields
  (dy/eps/pe/... and a MONTHLY 'return'); the appended daily row carries NaNs there and a
  1-DAY 'return'. Keep the monthly-sourced row WHOLE; drop the daily row entirely.
  (combine_first or .last() would splice/keep 1-day returns into a monthly frame.)
- return_daily: untouched (0 dups).
"""
import hashlib
import pickle
import sys

import pandas as pd

SRC = r"C:\Users\Opal Bloomberg\OneDrive - Opal Capital\Shared - Documents\OCIO Models\Dashboard\202511 Model Portfolio Exposure\output\data 20260731 v1 bkp.pkl"
DST = r"C:\Users\OPALBL~1\AppData\Local\Temp\claude\C--Users-Opal-Bloomberg-Desktop-ajb-workspace\d6886795-b5fb-491b-bec0-9948fe43d03e\scratchpad\data 20260731 v1 DEDUPED.pkl"
REF0727 = r"C:\Users\Opal Bloomberg\OneDrive - Opal Capital\Shared - Documents\OCIO Models\Dashboard\202511 Model Portfolio Exposure\output\data 20260727 v1.pkl"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("SOURCE:", SRC)
    print("  md5:", md5(SRC), " sha256:", sha256(SRC)[:16] + "...")
    with open(SRC, "rb") as f:
        d = pickle.load(f)

    # ---- price_monthly: identical-pair dedup ----
    pm = d["price_monthly"]
    n0 = len(pm)
    dup_mask = pm.duplicated(subset=["index_name", "date"], keep=False)
    full_dup_mask = pm.duplicated(keep=False)
    assert dup_mask.sum() == 60, f"expected 60 dup rows, got {dup_mask.sum()}"
    assert (dup_mask == full_dup_mask).all(), "price_monthly dup pairs are NOT fully identical; abort"
    pm2 = pm.drop_duplicates(subset=["index_name", "date"], keep="first").reset_index(drop=True)
    assert len(pm2) == n0 - 30, (n0, len(pm2))
    d["price_monthly"] = pm2
    print(f"price_monthly: {n0} -> {len(pm2)} rows (dropped 30 identical month-end dupes)")

    # ---- return_monthly: keep the field-bearing (monthly-sourced) row whole ----
    rm = d["return_monthly"]
    n0 = len(rm)
    dm = rm.duplicated(subset=["index_name", "date"], keep=False)
    assert dm.sum() == 168, f"expected 168 dup rows, got {dm.sum()}"
    dups = rm[dm]
    keep_idx = []
    conflict_cols = {}
    tie_cases = 0
    for (nm, dt_), grp in dups.groupby(["index_name", "date"]):
        assert len(grp) == 2, (nm, dt_, len(grp))
        # record which columns conflict (info only -- periodicity-dependent fields
        # like return/rsi legitimately differ between a monthly and a daily row)
        for col in grp.columns:
            a, b = grp[col].iloc[0], grp[col].iloc[1]
            if pd.notna(a) and pd.notna(b) and a != b:
                conflict_cols[col] = conflict_cols.get(col, 0) + 1
        nn = grp.notna().sum(axis=1)
        if nn.iloc[0] != nn.iloc[1]:
            best = nn.idxmax()  # monthly-sourced row carries the valuation fields
        else:
            # tie (e.g. crypto: no valuation fields either way) -> semantic test:
            # the monthly row's 'return' fits the frame's own month-over-month price move.
            tie_cases += 1
            hist = rm[(rm["index_name"] == nm) & (rm["date"] < dt_) & ~rm.index.isin(grp.index)]
            assert len(hist), f"no prior history for {nm}; cannot discriminate tie; abort"
            prev_px = float(hist.sort_values("date")["price"].iloc[-1])
            fits = {}
            for idx in grp.index:
                px = float(grp.loc[idx, "price"])
                exp_ret = (px / prev_px - 1.0) * 100.0
                fits[idx] = abs(float(grp.loc[idx, "return"]) - exp_ret)
            best, worst = sorted(fits, key=fits.get)
            assert fits[best] < 0.2 * max(fits[worst], 1e-12) or fits[best] < 1e-6, (
                f"ambiguous monthly-return fit for {nm} {dt_}: {fits}; abort")
        keep_idx.append(best)
    drop_idx = dups.index.difference(pd.Index(keep_idx))
    rm2 = rm.drop(index=drop_idx).reset_index(drop=True)
    assert len(rm2) == n0 - 84, (n0, len(rm2))
    assert not rm2.duplicated(subset=["index_name", "date"]).any()
    d["return_monthly"] = rm2
    print(f"return_monthly: {n0} -> {len(rm2)} rows (dropped 84 daily-append rows; monthly rows kept whole; {tie_cases} tie(s) resolved by monthly-return fit)")
    print(f"  conflicting columns across the 84 pairs (periodicity-dependent, monthly wins): {conflict_cols}")

    # ---- return_daily untouched, assert clean ----
    rd = d["return_daily"]
    assert not rd.duplicated(subset=["index_name", "date"]).any(), "return_daily has dups?!"
    print(f"return_daily: {len(rd)} rows untouched, 0 dups")

    # ---- verification suite ----
    print()
    print("VERIFICATION:")
    # V1: the exact Lambda precondition -- per index_name, date index unique in price_monthly
    bad = [nm for nm, g in d["price_monthly"].groupby("index_name") if not g.set_index("date").index.is_unique]
    assert not bad, f"non-unique date index remains for: {bad}"
    print("  V1 PASS: price_monthly date-index unique for all", d["price_monthly"]["index_name"].nunique(), "index_names (build_rfr_daily reindex precondition)")
    # V1b: simulate the crash line for every index_name
    for nm, g in d["price_monthly"].groupby("index_name"):
        s = g.set_index("date")["price"]
        daily_index = pd.date_range(s.index.min(), s.index.max(), freq="D")
        s.reindex(daily_index)  # raises ValueError on dup labels
    print("  V1b PASS: reindex(daily_index) executes clean for every index_name")
    # V2: ST series integrity vs verified-clean 0727
    with open(REF0727, "rb") as f:
        ref = pickle.load(f)
    for key in ("return_daily", "price_monthly", "return_monthly"):
        a = ref[key]
        b = d[key]
        probe = "Short Term" if (a["index_name"] == "Short Term").any() and (b["index_name"] == "Short Term").any() else "10Y"
        sa = a[a["index_name"] == probe].set_index("date")
        sb = b[b["index_name"] == probe].set_index("date")
        common = sa.index.intersection(sb.index)
        cols = [c for c in ("price", "return") if c in sa.columns and c in sb.columns]
        diff = (sa.loc[common, cols].astype(float) - sb.loc[common, cols].astype(float)).abs()
        mx = float(diff.max().max()) if len(common) else float("nan")
        assert len(common) > 0 and mx < 1e-9, (key, probe, len(common), mx)
        print(f"  V2 PASS: {key} {probe!r} identical to 0727 on {len(common)} shared dates (max diff {mx:.1e})")
    # V3: ST terminal cross-check values (live pull earlier this session)
    st = d["return_daily"]
    st = st[st["bbg_ticker"] == ".ST Index"].set_index("date")
    v = float(st.loc[pd.Timestamp("2026-07-31"), "price"])
    assert abs(v - 112.503) < 1e-3, v
    print(f"  V3 PASS: .ST Index 2026-07-31 price {v} == live-terminal 112.503")
    # V4: frontier
    print("  V4: max dates:", {k: str(d[k]["date"].max().date()) for k in ("return_daily", "return_monthly", "price_monthly")})

    with open(DST, "wb") as f:
        pickle.dump(d, f)
    print()
    print("WROTE:", DST)
    print("  md5:", md5(DST), " sha256:", sha256(DST))
    return 0


if __name__ == "__main__":
    sys.exit(main())
