"""TO-DB-b-34: build RELEASE_LOCAL_RUN.json from the two local runs of the reporting-gold handler (`--local`, one day, 20 accounts).

Usage: python build_release_record.py <returns_before.parquet> <returns_after.parquet> <class_after.parquet> <out.json> <day>

`before` is the unextended handler (git show 954983d543:<handler>); `after` is the extended handler, which also wrote the class parquet.
Reads local files only. Writes the record the criterion DB22-1-AC1 reads.
"""
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(argv):
    before, after, klass, out, day = argv[1:6]
    returns = pd.read_parquet(after)
    classes = pd.read_parquet(klass)
    measured_pairs = set(map(tuple, classes.loc[classes["coverage"] == "MEASURED", ["account_id", "business_date"]].values))
    account_days = [{"account_id": r.account_id, "business_date": r.business_date, "account_daily_return": float(r.total_return_daily)}
                    for r in returns.itertuples() if (r.account_id, r.business_date) in measured_pairs]
    total = float(classes["market_value_eod"].sum())
    unc = float(classes.loc[classes["asset_class"] == "unclassified", "market_value_eod"].sum())
    record = {
        "day": day,
        "returns_sha256_before": sha256_of(before),
        "returns_sha256_after": sha256_of(after),
        "returns_rows_before": int(len(pd.read_parquet(before))),
        "returns_rows_after": int(len(returns)),
        "account_days": account_days,
        "class_rows": [{"account_id": r.account_id, "business_date": r.business_date, "class": r.asset_class,
                        "market_value_eod": r.market_value_eod, "class_return_daily": (None if pd.isna(r.class_return_daily)
                                                                                    else float(r.class_return_daily)),
                        "coverage": r.coverage} for r in classes.itertuples()],
        "unclassified_share": {"value": (unc / total) if total else None, "numerator": round(unc, 2),
                               "denominator": round(total, 2), "denominator_unit": "USD summed class market_value_eod",
                               "basis": "market value on %s over the sample's accounts" % day},
    }
    Path(out).write_text(json.dumps(record, indent=1), encoding="utf-8")
    print("account_days=%d class_rows=%d share=%s identical=%s" % (len(account_days), len(record["class_rows"]),
                                                                  record["unclassified_share"]["value"],
                                                                  record["returns_sha256_before"] == record["returns_sha256_after"]))


if __name__ == "__main__":
    main(sys.argv)
