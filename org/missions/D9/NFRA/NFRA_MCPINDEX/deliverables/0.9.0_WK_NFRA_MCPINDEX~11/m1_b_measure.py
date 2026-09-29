# MX-m-1 (b): reads ONLY local copies fetched by VersionId (see MEASURE_BATCH_ROUND3.md section (b)). Prints counts, never rows.
import pandas as pd
import sys

B = sys.argv[1] if len(sys.argv) > 1 else ".scratch/b"


def dim(n):
    d = pd.read_parquet("%s/dim_%s.parquet" % (B, n), columns=["asset_id", "cusip"])
    d["asset_id"] = d["asset_id"].astype(str)
    print(n, "rows", len(d), "unique asset_ids", d.asset_id.nunique())
    return d.drop_duplicates("asset_id", keep="last").set_index("asset_id")["cusip"]


D = {
    n: dim(n)
    for n in ["V0_4dfw", "V1_pdoQ", "V2_Pa4q", "V3_bSQW", "V4_kitt", "V5_qcSd"]
}
V0, V1 = D["V0_4dfw"], D["V1_pdoQ"]
common = V0.index.intersection(V1.index)
a, b = V0.loc[common], V1.loc[common]
chg = common[((a != b) & ~(a.isna() & b.isna())).values]
print(
    "V0->V1: common asset_ids",
    len(common),
    "changed cusip",
    len(chg),
    "(null->value",
    int((V0.loc[chg].isna() & V1.loc[chg].notna()).sum()),
    " value->null",
    int((V0.loc[chg].notna() & V1.loc[chg].isna()).sum()),
    " value->other value",
    int((V0.loc[chg].notna() & V1.loc[chg].notna()).sum()),
    ")",
)
print(
    "V0->V1: asset_ids only in V1",
    len(V1.index.difference(V0.index)),
    " only in V0",
    len(V0.index.difference(V1.index)),
)
tx = pd.read_parquet("%s/tx_0928.parquet" % B)
tx["asset_id"] = tx["asset_id"].astype(str)
print(
    "silver tx 2026-09-28 rows",
    len(tx),
    "cols",
    len(tx.columns),
    "has cusip",
    ("cusip" in tx.columns),
)
if len(tx) == 0:
    print(
        "RESULT: the only silver/transactions object written after V1 has 0 rows; rows carrying a cusip differing from the predecessor dim = 0 of 0; rows among the 42 asset_ids = 0 of 0"
    )
    sys.exit(0)
c = tx["cusip"]
print("rows with cusip null", int(c.isna().sum()))


def cnt(name, dimser):
    exp = tx["asset_id"].map(dimser)
    diff = ~((c == exp) | (c.isna() & exp.isna()))
    return diff


for n in D:
    d = cnt(n, D[n])
    print("rows whose cusip != %s lookup: %d of %d" % (n, int(d.sum()), len(tx)))
d0 = cnt("V0_4dfw", V0)
inchg = tx["asset_id"].isin(set(chg))
print(
    "rows whose asset_id is among the %d changed: %d of %d; of those, cusip differs from V0 (predecessor) lookup: %d ; differs from V1: %d ; differs from V4: %d"
    % (
        len(chg),
        int(inchg.sum()),
        len(tx),
        int((d0 & inchg).sum()),
        int((cnt("V1", D["V1_pdoQ"]) & inchg).sum()),
        int((cnt("V4", D["V4_kitt"]) & inchg).sum()),
    )
)
print("rows differing from V0 lookup, OUTSIDE the 42:", int((d0 & ~inchg).sum()))
print(
    "distinct asset_ids among the 42 present in the file:",
    tx.loc[inchg, "asset_id"].nunique(),
)
print("distinct asset_ids differing from V0 lookup:", tx.loc[d0, "asset_id"].nunique())
# what is V0 vs V1 vs V4 asset set of file
print(
    "file asset_ids",
    tx.asset_id.nunique(),
    " in V0",
    int(tx.asset_id.drop_duplicates().isin(V0.index).sum()),
    " in V1",
    int(tx.asset_id.drop_duplicates().isin(V1.index).sum()),
    " in V4",
    int(tx.asset_id.drop_duplicates().isin(D["V4_kitt"].index).sum()),
)
