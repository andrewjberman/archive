# MX-m-1 (c): counts only, never rows. Local copies were fetched by VersionId (see MEASURE_BATCH_ROUND3.md section (c)).
import pandas as pd
import sys

B = sys.argv[1] if len(sys.argv) > 1 else ".scratch/c"
PATS = (
    "CASH",
    "MONEY",
    "MMKT",
    "SWEEP",
)  # B_01.holdings_lots.py:579 (_build_rps_context) and :925 (_build_uln_sleeve_lots)
for tag in ["0925", "0918", "0918r11"]:
    df = pd.read_parquet(
        "%s/hl_%s.parquet" % (B, tag),
        columns=["asset_name", "ticker", "cusip", "snapshot_date", "is_open"],
    )
    n = len(df)
    nul = df["cusip"].isna()
    s = df["cusip"].astype(str).str.strip()
    nul2 = nul | s.isin(["", "nan", "None"])
    name_u = df["asset_name"].fillna("").astype(str).str.upper().str.strip()
    P1 = name_u == "CASH"  # B_01.holdings_lots.py:2371 is_cash_lot
    up = df["asset_name"].fillna("").astype(str).str.upper()
    P2 = pd.Series(False, index=df.index)
    for p in PATS:
        P2 = P2 | up.str.contains(p, na=False)
    P2 = P2 & ~up.str.contains(
        "CASH COWS", na=False
    )  # B_01.holdings_lots.py:951-953 shape (uln builder)
    print(
        "==",
        tag,
        "snapshot_date distinct",
        df.snapshot_date.astype(str).unique()[:3],
        "rows",
        n,
        "null cusip",
        int(nul.sum()),
        "(also blank/nan/None strings",
        int(nul2.sum() - nul.sum()),
        ")",
    )
    print(
        " null-cusip rows with P1 (asset_name==CASH): %d of %d null (%.2f%%); non-null rows with P1: %d"
        % (
            int((nul & P1).sum()),
            int(nul.sum()),
            100 * (nul & P1).sum() / max(nul.sum(), 1),
            int((~nul & P1).sum()),
        )
    )
    print(
        " null-cusip rows with P2 (CASH|MONEY|MMKT|SWEEP, not CASH COWS): %d of %d null (%.2f%%); non-null rows with P2: %d"
        % (
            int((nul & P2).sum()),
            int(nul.sum()),
            100 * (nul & P2).sum() / max(nul.sum(), 1),
            int((~nul & P2).sum()),
        )
    )
    print(
        " null-cusip rows NOT P2: %d ; distinct asset_name among them: %d"
        % (int((nul & ~P2).sum()), df.loc[nul & ~P2, "asset_name"].nunique())
    )
    print(" total rows P1: %d  P2: %d" % (int(P1.sum()), int(P2.sum())))
    print(
        " null-cusip rows: ticker null %d, is_open True %d"
        % (
            int(df.loc[nul, "ticker"].isna().sum()),
            int(df.loc[nul, "is_open"].astype(bool).sum()),
        )
    )
