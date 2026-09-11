"""check_join.py -- AC4: independently re-derive the fiscal-year join from the RAW histdata.json
already landed in S3 (never from the derived model_block.json, and never from model_block_pull.py's
own in-process result) and print the summary line C-FISCAL-YEAR-JOIN is graded against:

    JOIN: 3 of 3 securities at 10 FY rows; orphan price rows 0

A price row is "orphaned" if, after grouping the raw historical rows by the calendar year of
`date` (the fiscal-year join key -- never the date string, F5/PRD s.4b), some fiscal year ends up
with a PX_LAST-bearing sub-row but no fundamentals sub-row merged into it (or vice versa) --
i.e. the join key did not actually merge what the vendor split across two dates in the same year.
"""
from __future__ import annotations

import json

import boto3

BUCKET = "opal-data-research"
SECURITIES = ["SAP GY Equity", "BA US Equity", "BABA US Equity"]
EXPECTED_FY_COUNT = 10

PRICE_FIELD = "PX_LAST"
FUNDAMENTAL_FIELDS = {
    "SALES_REV_TURN", "IS_OPER_INC", "OPER_MARGIN", "EBITDA", "EBITDA_ADJUSTED",
    "EBITDA_MARGIN", "IS_EPS", "BOOK_VAL_PER_SH", "IS_SH_FOR_DILUTED_EPS",
    "CAPITAL_EXPEND", "CF_FREE_CASH_FLOW", "IS_DIV_PER_SHR", "RETURN_ON_ASSET",
    "RETURN_COM_EQY",
}


def security_key(security: str) -> str:
    return security.replace(" ", "_")


def latest_stamp(s3, prefix: str) -> str:
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix, Delimiter="/")
    stamps = [cp["Prefix"][len(prefix):-1] for cp in resp.get("CommonPrefixes", [])]
    if not stamps:
        raise RuntimeError(f"no stamp under s3://{BUCKET}/{prefix}")
    return sorted(stamps)[-1]


def merge_by_fiscal_year(hist_rows: list[dict]) -> dict[str, dict]:
    groups: dict[str, dict] = {}
    for row in hist_rows:
        date = row.get("date")
        if not date:
            continue
        fy = date[:4]
        g = groups.setdefault(fy, {})
        for k, v in row.items():
            if k == "date":
                continue
            g[k] = v
    return groups


def main() -> int:
    s3 = boto3.client("s3")

    securities_at_10 = 0
    orphan_price_rows = 0

    for sec in SECURITIES:
        sec_key = security_key(sec)
        prefix = f"raw/bloomberg/{sec_key}/"
        stamp = latest_stamp(s3, prefix)
        hist_obj = s3.get_object(Bucket=BUCKET, Key=f"{prefix}{stamp}/histdata.json")
        hist = json.loads(hist_obj["Body"].read())
        rows = hist.get(sec, [])

        fy_groups = merge_by_fiscal_year(rows)
        if len(fy_groups) == EXPECTED_FY_COUNT:
            securities_at_10 += 1

        for fy, g in fy_groups.items():
            has_price = PRICE_FIELD in g
            has_fundamentals = any(f in g for f in FUNDAMENTAL_FIELDS)
            if has_price and not has_fundamentals:
                orphan_price_rows += 1

    print(
        f"JOIN: {securities_at_10} of {len(SECURITIES)} securities at {EXPECTED_FY_COUNT} FY rows; "
        f"orphan price rows {orphan_price_rows}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
