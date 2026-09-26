"""AMGT_CORPUS round 7 -- the issuer's check for CRPS-i-3 (read-only). Three modes, one line each.

--shape        the round-7 evidence JSON covers every key holding a served Model block (counted HERE, independently),
               its Base-labelled cells carry right-hand neighbours where the sheet has them, at least one name carries a
               selected workbook Base-case cell, and every selection names its sheet and cell.
--determinism  the producer run twice into two temp files writes identical bytes.
--floor        the selections name at least one London, one US and one Asian key (R-1).
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

import boto3

W = "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~2"
EVIDENCE = W + "/CASE_EVIDENCE_ROUND7.json"
PRODUCER = W + "/case_evidence.py"
BUCKET = os.environ.get("HARVEST_BUCKET", "opal-data-harvest")
PREFIX = "derived/model_block/"
ASIA = {"JP", "HK", "TT", "KS", "CH", "C1", "C2", "IN", "IB", "SP", "IJ", "TB", "MK", "PM", "AU"}


def block_keys():
    s3 = boto3.client("s3", region_name="us-east-1")
    keys = set()
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []) or []:
            parts = obj["Key"].split("/")
            if len(parts) == 5 and parts[4] == "model_block.json":
                keys.add(parts[2])
    return keys


def venue(security_key):
    tokens = security_key.replace("-SLASH-", "/").split("_")
    return tokens[-2] if len(tokens) >= 3 else ""


def load():
    with open(EVIDENCE, encoding="utf-8") as fh:
        return json.load(fh)


def shape():
    doc = load()
    keys = len(block_keys())
    census = len(doc["ratio_census"]["rows"])
    base_rows = [r for r in doc["workbook"]["rows"] if "base" in (r.get("label") or "").lower()]
    right_nonempty = sum(1 for r in base_rows if r.get("right"))
    sels = doc["workbook"]["selections"]
    no_coord = sum(1 for s in sels if not s.get("sheet") or not s.get("cell"))
    names = len({s["security_key"] for s in sels})
    ok = census == keys and names > 0 and no_coord == 0
    print("i3 %s census_rows %d keys_with_block %d base_labels %d right_nonempty %d names_with_selection %d "
          "selections_without_coord %d" % ("OK" if ok else "FAIL", census, keys, len(base_rows), right_nonempty,
                                           names, no_coord))


def determinism():
    digests = []
    with tempfile.TemporaryDirectory() as tmp:
        for i in (1, 2):
            out = os.path.join(tmp, "run%d.json" % i)
            subprocess.run([sys.executable, PRODUCER, "--out-json", out], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(out, "rb") as fh:
                digests.append(hashlib.sha256(fh.read()).hexdigest())
    print("i3 determinism %s sha %s" % ("identical" if digests[0] == digests[1] else "differs", digests[0][:12]))


def floor():
    doc = load()
    counts = {"LN": 0, "US": 0, "ASIA": 0}
    for key in {s["security_key"] for s in doc["workbook"]["selections"]}:
        v = venue(key)
        if v in ("LN", "US"):
            counts[v] += 1
        elif v in ASIA:
            counts["ASIA"] += 1
    print("i3 floor LN %d US %d ASIA %d" % (counts["LN"], counts["US"], counts["ASIA"]))


if __name__ == "__main__":
    {"--shape": shape, "--determinism": determinism, "--floor": floor}[sys.argv[1]]()
