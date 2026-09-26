"""AMGT_CORPUS round 7 act A -- the issuer's content verification after the 94-key re-derive (read-only).

Reads the before-state rows (key, stamp, status, cause, value, ratio, has_band, has_currencies) from the path given as
argv[1] and the served newest block per key now. Prints the three stop limbs of the CTO half @8b27c6f2cc:
  1. band_basis on exactly the SERVED + outside_band keys of the 94, and on none of the rest;
  2. no disposition and no served ratio moves on any of the 94;
  3. the three excluded keys keep their newest stamp.
"""
import json
import sys

import boto3

BUCKET = "opal-data-harvest"
EXCLUDED = {"6861_JP_Equity", "CSL_AU_Equity", "NVDA_US_Equity"}


def newest_blocks(s3):
    newest = {}
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="derived/model_block/"):
        for obj in page.get("Contents", []) or []:
            k = obj["Key"].split("/")
            if len(k) == 5 and k[4] == "model_block.json" and (k[2] not in newest or k[3] > newest[k[2]]):
                newest[k[2]] = k[3]
    return newest


def main():
    before = {r[0]: r for r in json.load(open(sys.argv[1], encoding="utf-8"))}
    s3 = boto3.client("s3", region_name="us-east-1")
    newest = newest_blocks(s3)
    act = sorted(k for k in before if k not in EXCLUDED)
    carry = without = should_carry = 0
    moves, restamped, wrong_field = [], [], []
    for key in act:
        doc = json.loads(s3.get_object(Bucket=BUCKET, Key="derived/model_block/%s/%s/model_block.json"
                                       % (key, newest[key]))["Body"].read())
        base = (doc.get("cases") or {}).get("base") or {}
        _k, b_stamp, b_status, b_cause, _b_value, b_ratio, _hb, _hc = before[key]
        if newest[key] != b_stamp:
            restamped.append(key)
        if (base.get("status"), base.get("cause")) != (b_status, b_cause):
            moves.append("%s %s/%s -> %s/%s" % (key, b_status, b_cause, base.get("status"), base.get("cause")))
        elif b_status == "SERVED" and b_ratio is not None and abs((base.get("ratio_to_px_last") or 0) - b_ratio) > 1e-9:
            moves.append("%s ratio %s -> %s" % (key, b_ratio, base.get("ratio_to_px_last")))
        expect = base.get("status") == "SERVED" or base.get("cause") == "outside_band"
        should_carry += int(expect)
        if "band_basis" in base:
            carry += 1
            if not expect:
                wrong_field.append(key)
        else:
            without += 1
            if expect:
                wrong_field.append(key)
    cat_doc = json.loads(s3.get_object(Bucket=BUCKET, Key="derived/model_block/CAT_US_Equity/%s/model_block.json"
                                       % newest["CAT_US_Equity"])["Body"].read())
    cat_base = cat_doc["cases"]["base"]
    excluded_same = sum(1 for k in EXCLUDED if newest[k] == before[k][1])
    print("act keys %d restamped %d" % (len(act), len(restamped)))
    print("limb1 band_basis carry %d without %d should_carry %d wrong_field %d" % (carry, without, should_carry, len(wrong_field)))
    print("limb2 disposition_or_ratio_moves %d" % len(moves))
    for m in moves:
        print("  move %s" % m)
    print("limb3 excluded_same_stamp %d of 3" % excluded_same)
    print("CAT_US status %s ratio %s band %s currencies %s band_basis %s" % (
        cat_base.get("status"), cat_base.get("ratio_to_px_last"), cat_base.get("band"), "currencies" in cat_doc,
        "band_basis" in cat_base))


if __name__ == "__main__":
    main()
