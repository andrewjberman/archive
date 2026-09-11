"""check_join_fye.py -- AMGT-r-1 AC2: the readback.

Reads THE SERVED BLOCK (derive_fye_fixed.py's landed
`derived/model_block_fye/<security_key>/<stamp>/model_block_fye.json`, the LATEST stamp per
security -- never the pull log, never a re-derivation from raw here) and prints, per security
AMGT-s-1 landed, one line:

    FYE JOIN: <security> -> max fundamental-to-price gap <N> days

N is the max, across that security's fiscal years, of the gap between a fiscal-year
fundamental's period-end date and its PAIRED price's date, under the fiscal-period join
(fye_join.fiscal_period_join). For a correct join every gap is small -- SAP GY Equity and BA US
Equity (both December filers) measure 0-2 days; BABA US Equity (FYE 31 March, the security the
fix exists for) measures 0-3 days once paired against the dense DAILY price series, versus
~270-275 days under the old calendar-year grouping (test_fye_join.py's control arm, AC1).
"""
from __future__ import annotations

import json

import boto3

BUCKET = "opal-data-research"
SECURITIES = ["SAP GY Equity", "BA US Equity", "BABA US Equity"]
ENGINE = "model_block_fye"


def security_key(security: str) -> str:
    return security.replace(" ", "_")


def _latest_key_ending(s3, prefix: str, suffix: str) -> str | None:
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    keys = [o["Key"] for o in resp.get("Contents", []) if o["Key"].endswith(suffix)]
    return sorted(keys)[-1] if keys else None


def _read_json(s3, key: str):
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    return json.loads(obj["Body"].read())


def main() -> int:
    s3 = boto3.client("s3")
    for sec in SECURITIES:
        sec_key = security_key(sec)
        prefix = f"derived/{ENGINE}/{sec_key}/"
        key = _latest_key_ending(s3, prefix, "/model_block_fye.json")
        if key is None:
            print(f"FYE JOIN: {sec} -> NO SERVED BLOCK LANDED (run derive_fye_fixed.py first)")
            continue
        served = _read_json(s3, key)
        max_gap = served.get("max_gap_days")
        print(f"FYE JOIN: {sec} -> max fundamental-to-price gap {max_gap} days")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
