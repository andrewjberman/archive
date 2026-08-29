"""G-4 acceptance evidence: the SIGNED gap from the FIXED code, on REAL partitions.

Ad-hoc QA run (permitted; never production evidence). No --upload, no emit, no serve --
the module's pure functions are called directly, so nothing can reach S3 from here.

BEFORE  = the STORED twr_daily artifact (what the pre-fix code wrote).
AFTER   = flows_from_ledger + daily_returns from the CURRENT working tree.
Both legs SIGNED. The non-fee-day equality is the negative control on both.
"""
import importlib.util
import os

import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
GOLD = "data/assets/scripts/gold/runners_49f"
PAIRS = [("2025-12-10", "2025-12-09"), ("2026-08-28", "2026-08-27")]

spec = importlib.util.spec_from_file_location("c02", os.path.join(GOLD, "c02_twr_engine.py"))
c02 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c02)
POLICY = {"policies": {"flow_timing": {"value": "EOD"}}}

tot = {"fee": 0, "pos": 0, "neg": 0, "zero": 0, "nonfee": 0, "eq": 0, "flip": 0}
print("=" * 78)
print("G-4 SIGNED GAP -- BEFORE (stored) vs AFTER (fixed code), REAL partitions")
print("=" * 78)
for d, prev in PAIRS:
    led = pd.read_parquet(f"{ROOT}/flow_ledger_{d}/data.parquet")
    cal = pd.read_parquet(f"{ROOT}/cal_{d}/data.parquet")
    prev_map = dict(zip(cal["trading_day"].astype(str), cal["prev_trading_day"].astype(str)))
    fv = pd.concat([
        pd.read_parquet(f"{ROOT}/val_{x}/data.parquet",
                        columns=["account_id", "business_date", "fair_value"])
        for x in (d, prev)], ignore_index=True)

    flows, census = c02.flows_from_ledger(led, boundary="account")
    after = c02.daily_returns(fv, flows, prev_map=prev_map, policy=POLICY)
    after = after[(after["business_date"].astype(str) == d) & (after["status"] == "OK")].copy()
    after["account_id"] = after["account_id"].astype(str)

    before = pd.read_parquet(f"{ROOT}/twr_daily_{d}/data.parquet")
    before = before[before["status"] == "OK"].copy()
    before["account_id"] = before["account_id"].astype(str)

    m = before.merge(after, on="account_id", suffixes=("_b", "_a"))
    for c in ("r_net_b", "r_gross_b", "cf_net_b", "cf_gross_b",
              "r_net_a", "r_gross_a", "cf_net_a", "cf_gross_a", "bmv_a"):
        m[c] = pd.to_numeric(m[c], errors="coerce")
    m["gap_b"] = m["r_gross_b"] - m["r_net_b"]      # SIGNED
    m["gap_a"] = m["r_gross_a"] - m["r_net_a"]      # SIGNED
    m["addback"] = -(m["cf_gross_a"] - m["cf_net_a"])   # = -fee_cf, POSITIVE for a debit

    fee = m[m["addback"] != 0.0]
    non = m[m["addback"] == 0.0]
    tot["fee"] += len(fee)
    tot["nonfee"] += len(non)
    tot["pos"] += int((fee["gap_a"] > 0).sum())
    tot["neg"] += int((fee["gap_a"] < 0).sum())
    tot["zero"] += int((fee["gap_a"] == 0).sum())
    tot["eq"] += int((non["r_net_a"] == non["r_gross_a"]).sum())
    tot["flip"] += int(((fee["gap_b"] < 0) & (fee["gap_a"] > 0)).sum())

    print(f"\n  date={d}   matched OK account-days {len(m):,}   fee-days {len(fee):,}")
    print(f"    r_net UNMOVED (SERVED leg): max |r_net_after - r_net_before| = "
          f"{(m['r_net_a'] - m['r_net_b']).abs().max():.3e}   over {len(m):,}")
    if len(fee):
        print(f"    BEFORE  SIGNED gap: min {fee['gap_b'].min():+.8f}  med {fee['gap_b'].median():+.8f}"
              f"  max {fee['gap_b'].max():+.8f}   NEG {int((fee['gap_b'] < 0).sum())}/POS "
              f"{int((fee['gap_b'] > 0).sum())} of {len(fee)}")
        print(f"    AFTER   SIGNED gap: min {fee['gap_a'].min():+.8f}  med {fee['gap_a'].median():+.8f}"
              f"  max {fee['gap_a'].max():+.8f}   NEG {int((fee['gap_a'] < 0).sum())}/POS "
              f"{int((fee['gap_a'] > 0).sum())} of {len(fee)}")
        idn = (fee["gap_a"] - fee["addback"] / fee["bmv_a"]).abs().max()
        print(f"    SPEC:81 identity AFTER -- gap == +addback/bmv : max residual {idn:.3e}")
        print(f"    sum of the two gaps (they must cancel exactly): max |gap_b + gap_a| = "
              f"{(fee['gap_b'] + fee['gap_a']).abs().max():.3e}")
    print(f"    NEGATIVE CONTROL non-fee-days {len(non):,}: r_net == r_gross EXACT AFTER on "
          f"{int((non['r_net_a'] == non['r_gross_a']).sum()):,}")

    w = fee[fee["account_id"] == "0062640151"] if d == "2025-12-10" else fee.nsmallest(1, "gap_b")
    if len(w):
        r = w.iloc[0]
        print(f"    WORKED ACCOUNT {r['account_id']}: bmv {r['bmv_a']:,.2f}  emv {r['emv_a']:,.2f}"
              f"  cf_net {r['cf_net_a']:,.2f}  addback {r['addback']:+,.2f}")
        print(f"      r_net   BEFORE {r['r_net_b']:+.8f}   AFTER {r['r_net_a']:+.8f}  (UNMOVED)")
        print(f"      r_gross BEFORE {r['r_gross_b']:+.8f}   AFTER {r['r_gross_a']:+.8f}")

print("\n" + "=" * 78)
print("TOTALS (AFTER = the fixed code)")
print("=" * 78)
print(f"  fee-days                                     : {tot['fee']:,}")
print(f"  SIGNED gap POSITIVE (r_gross > r_net)        : {tot['pos']:,} of {tot['fee']:,}")
print(f"  SIGNED gap NEGATIVE                          : {tot['neg']:,} of {tot['fee']:,}")
print(f"  SIGNED gap ZERO                              : {tot['zero']:,} of {tot['fee']:,}")
print(f"  flipped NEGATIVE(before) -> POSITIVE(after)  : {tot['flip']:,} of {tot['fee']:,}")
print(f"  NEGATIVE CONTROL non-fee-day exact equality  : {tot['eq']:,} of {tot['nonfee']:,}")
