"""AMGT_CORPUS round 9 act k-2 -- the SERVED model-block state, read-only.

For every key under s3://opal-data-harvest/derived/model_block/, reads the NEWEST stamp's model_block.json (the object the
readers serve) and prints its Base case: `block <key> stamp <stamp> base <status> ratio <ratio>`. With argv[1] = a
cases-report log, also compares each key's served Base status/ratio against the rule's expected line and prints
`match` / `mismatch` counts -- the verify limb after the re-derive. Writes nothing.
"""
import json
import re
import sys

import boto3

BUCKET = "opal-data-harvest"
LINE = re.compile(r"^cases (\S+) base (\S+) ratio (\S+) ")


def newest_blocks(s3):
    newest = {}
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="derived/model_block/"):
        for obj in page.get("Contents", []) or []:
            k = obj["Key"].split("/")
            if len(k) == 5 and k[4] == "model_block.json" and (k[2] not in newest or k[3] > newest[k[2]]):
                newest[k[2]] = k[3]
    return newest


def main():
    s3 = boto3.client("s3", region_name="us-east-1")
    newest = newest_blocks(s3)
    rows = {}
    for key, stamp in sorted(newest.items()):
        body = s3.get_object(Bucket=BUCKET, Key="derived/model_block/%s/%s/model_block.json" % (key, stamp))["Body"].read()
        block = json.loads(body.decode("utf-8"))
        base = (block.get("cases") or {}).get("base")
        status = base.get("status") if isinstance(base, dict) else "NOCASES"
        ratio = base.get("ratio_to_px_last") if isinstance(base, dict) else None
        rows[key] = (status, "none" if ratio is None else repr(ratio))
        print("block %s stamp %s base %s ratio %s" % (key, stamp, status, rows[key][1]))
    served = sum(1 for s, _ in rows.values() if s == "SERVED")
    nocases = sum(1 for s, _ in rows.values() if s == "NOCASES")
    print("blocks keys %d served %d absent %d nocases %d" % (len(rows), served, len(rows) - served - nocases, nocases))
    if len(sys.argv) > 1:
        want = {}
        for line in open(sys.argv[1], encoding="utf-8"):
            m = LINE.match(line.strip())
            if m:
                want[m.group(1)] = (m.group(2), m.group(3))
        match = [k for k in want if k in rows and rows[k][0] == want[k][0]
                 and (want[k][0] != "SERVED" or abs(float(rows[k][1]) - float(want[k][1])) < 1e-9)]
        miss = sorted(set(want) - set(match))
        for k in miss:
            print("mismatch %s served %s expected %s" % (k, rows.get(k), want[k]))
        print("verify keys %d match %d mismatch %d" % (len(want), len(match), len(miss)))


if __name__ == "__main__":
    main()
