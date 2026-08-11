"""The cross-account pair-matching engine for the CONDITIONAL-BY-COUNTERPARTY family.

Classifies boundary-conditional transactions (journals, account transfers, in-kind moves)
per event, per the GIPS standard's sec4 rule: internal iff BOTH legs are inside the
performance-portfolio boundary, external otherwise.

CASH legs (tr_cd=FC): matched on (business_date, |gross_amount|) across DIFFERENT accounts
with OPPOSITE debit_credit. Matched pairs -> INTERNAL; unmatched -> EXTERNAL-BY-DEFAULT.

IN-KIND legs (tr_cd=IC): debit_credit carries LONG/SHORT (position side, NOT direction) and
quantities are unsigned -- measured 2026-08-11; a direction-based matcher structurally
cannot fire on these rows. Matching key = (business_date, cusip, |quantity|) across
different accounts; single-account groups are structurally one-sided in-book.
Direction resolution for one-sided in-kind events (receive vs deliver) is NOT derivable
from this table alone -- corroborate via next-day position delta (dim_position) or
fact_trn's fuller fields at build.

PII discipline: aggregate counts, values, and rates only.
"""
import glob
import os

import pandas as pd

CASH_CODES = {"$JNL", "$TYPE", "JNL", "JRNL", "TOA"}
INKIND_CODES = {"TOA", "T/A", "TYP", "DEL", "REC"}
COLS = ["account_id", "business_date", "tran_srcde", "tr_cd", "debit_credit",
        "gross_amount", "quantity", "cusip", "price"]


def load_series(partition_dir):
    frames = []
    for f in sorted(glob.glob(os.path.join(partition_dir, "date=*", "data.parquet"))):
        frames.append(pd.read_parquet(f, columns=COLS))
    t = pd.concat(frames, ignore_index=True)
    for c in ["account_id", "tran_srcde", "tr_cd", "debit_credit", "cusip"]:
        t[c] = t[c].astype(str).str.strip()
    for c in ["gross_amount", "quantity", "price"]:
        t[c] = pd.to_numeric(t[c], errors="coerce").fillna(0.0)
    return t


def match_cash(t):
    cash = t[(t["tran_srcde"].isin(CASH_CODES)) & (t["tr_cd"] == "FC") & (t["gross_amount"] != 0)].copy()
    cash["absv"] = cash["gross_amount"].abs()
    cash["is_debit"] = cash["debit_credit"].str.upper().str.startswith("D")
    matched_idx = []
    for _, g in cash.groupby(["business_date", "absv"]):
        if g["account_id"].nunique() >= 2 and g["is_debit"].nunique() >= 2:
            d = g[g["is_debit"]]
            c = g[~g["is_debit"]]
            n = min(len(d), len(c))
            matched_idx += list(d.index[:n]) + list(c.index[:n])
    matched = cash.loc[matched_idx]
    unmatched = cash.drop(index=matched_idx)
    return cash, matched, unmatched


def census_inkind(t):
    ink = t[(t["tran_srcde"].isin(INKIND_CODES)) & (t["tr_cd"] == "IC") & (t["quantity"] != 0)].copy()
    ink["absq"] = ink["quantity"].abs()
    ink["value"] = ink["absq"] * ink["price"].abs()
    groups = ink.groupby(["business_date", "cusip", "absq"])
    solo = 0
    multi_rows = 0
    for _, g in groups:
        if g["account_id"].nunique() == 1:
            solo += 1
        else:
            multi_rows += len(g)
    return ink, groups.ngroups, solo, multi_rows


def main():
    scratch = os.environ.get(
        "TRN_PARTITION_DIR",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "trn_full"),
    )
    t = load_series(scratch)
    cash, m, u = match_cash(t)
    print(f"CASH conditional rows={len(cash)} value=${cash['absv'].sum():,.2f}")
    print(f"  MATCHED (INTERNAL, both legs in-book): rows={len(m)} ({len(m)/max(len(cash),1)*100:.1f}%) "
          f"value=${m['absv'].sum():,.2f} ({m['absv'].sum()/max(cash['absv'].sum(),1)*100:.1f}% by value)")
    print(f"  UNMATCHED (EXTERNAL-BY-DEFAULT): rows={len(u)} value=${u['absv'].sum():,.2f}")
    ink, ngroups, solo, multi_rows = census_inkind(t)
    print(f"IN-KIND conditional rows={len(ink)} value=${ink['value'].sum():,.2f}")
    print(f"  one-sided-in-book groups: {solo}/{ngroups} ({solo/max(ngroups,1)*100:.1f}%) -> EXTERNAL-dominant")
    print(f"  rows in multi-account groups (pairable candidates): {multi_rows}")
    print("  direction resolution for one-sided events: position-delta corroboration at build (see docstring)")


if __name__ == "__main__":
    main()
