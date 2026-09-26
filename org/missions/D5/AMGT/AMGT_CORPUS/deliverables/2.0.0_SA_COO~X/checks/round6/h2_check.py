"""AMGT_CORPUS round 6 -- the issuer's check for CRPS-h-2 (read-only). Three modes, one line each.

--shape        the evidence JSON covers every key holding a served Model block (counted HERE, independently), its bins
               sum to that count, and every workbook row carries a sheet and a cell coordinate.
--determinism  the worker's producer run twice into two temp files writes identical bytes.
--floor        the side-by-side names at least one London, one US and one Asian key (R-1), and every key whose served
               Base case is REFUSED (counted HERE, independently) appears in the ratio census.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

import boto3

W2 = "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~2"
EVIDENCE = W2 + "/CASE_EVIDENCE_ROUND6.json"
PRODUCER = W2 + "/case_evidence.py"
BUCKET = os.environ.get("HARVEST_BUCKET", "opal-data-harvest")
PREFIX = "derived/model_block/"
ASIA = {"JP", "HK", "TT", "KS", "CH", "C1", "C2", "IN", "IB", "SP", "IJ", "TB", "MK", "PM"}


def served_blocks():
    """{security_key dir: newest block document}, newest by stamp directory name."""
    s3 = boto3.client("s3", region_name="us-east-1")
    newest = {}
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []) or []:
            parts = obj["Key"].split("/")
            if len(parts) == 5 and parts[4] == "model_block.json":
                if parts[2] not in newest or parts[3] > newest[parts[2]].split("/")[3]:
                    newest[parts[2]] = obj["Key"]
    return {k: json.loads(s3.get_object(Bucket=BUCKET, Key=v)["Body"].read()) for k, v in newest.items()}


def venue(security_key):
    tokens = security_key.replace("-SLASH-", "/").split("_")
    return tokens[-2] if len(tokens) >= 3 else ""


def load():
    with open(EVIDENCE, encoding="utf-8") as fh:
        return json.load(fh)


def shape():
    doc = load()
    keys = len(served_blocks())
    rows = doc["ratio_census"]["rows"]
    bins_sum = sum(doc["ratio_census"]["bins"].values())
    wb_rows = doc["workbook"]["rows"]
    names = len({r["security_key"] for r in wb_rows})
    no_coord = sum(1 for r in wb_rows if not r.get("sheet") or not r.get("cell"))
    ok = len(rows) == bins_sum == keys and names > 0 and no_coord == 0
    print("h2 %s census_rows %d bins_sum %d keys_with_block %d workbook_names %d rows_without_coord %d"
          % ("OK" if ok else "FAIL", len(rows), bins_sum, keys, names, no_coord))


def determinism():
    digests = []
    with tempfile.TemporaryDirectory() as tmp:
        for i in (1, 2):
            out = os.path.join(tmp, "run%d.json" % i)
            subprocess.run([sys.executable, PRODUCER, "--out-json", out], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(out, "rb") as fh:
                digests.append(hashlib.sha256(fh.read()).hexdigest())
    print("h2 determinism %s sha %s" % ("identical" if digests[0] == digests[1] else "differs", digests[0][:12]))


def floor():
    doc = load()
    wb_keys = {r["security_key"] for r in doc["workbook"]["rows"]}
    counts = {"LN": 0, "US": 0, "ASIA": 0}
    for key in wb_keys:
        v = venue(key)
        if v in ("LN", "US"):
            counts[v] += 1
        elif v in ASIA:
            counts["ASIA"] += 1
    refused = {k for k, d in served_blocks().items()
               if (d.get("cases") or {}).get("base", {}).get("status") == "ABSENT"
               and (d.get("cases") or {}).get("base", {}).get("cause")}
    census = {r["security_key"] for r in doc["ratio_census"]["rows"]}
    print("h2 floor LN %d US %d ASIA %d refused_in_census %d of %d"
          % (counts["LN"], counts["US"], counts["ASIA"], len(refused & census), len(refused)))


if __name__ == "__main__":
    {"--shape": shape, "--determinism": determinism, "--floor": floor}[sys.argv[1]]()
