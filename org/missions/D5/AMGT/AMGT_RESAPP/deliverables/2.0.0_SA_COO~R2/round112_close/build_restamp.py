"""build_restamp.py -- build the 95 re-stamped AI fill documents of the HELD to CLEARED write (CTO ruling cc02, msg 6898).

READ-ONLY on S3 (get_object on the 95 current keys) and a LOCAL write under live95/. It changes ONLY each block's `validation` dict:
the verdict of every block is the producer's own rule (contract.validate_block on the block without its validation key, exactly as
lib.research.aifill.validation.stamp_validation computes it), a PASS block becomes CLEARED, a block that is not PASS stays as stamped.
For the all-PASS case the result is cross-checked equal to stamp_validation(doc, now, state="CLEARED") of the library.

  PYTHONPATH=. python build_restamp.py            -> live95/stamped/*.json, changed.json, stamped_sha256_changed.json, build_report.json

Every stamped file is document_bytes(doc) plus one trailing newline (the form store.write_document stores). Prints the denominators
(documents, blocks, PASS by the rule, REFUSED by the rule) and the proof that only `validation` differs.
"""
import datetime
import hashlib
import json
import os
import sys

import boto3

from lib.research.aifill import contract, store, validation
from lib.research.api import scoped_amgt as served

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "round110_close", "live95", "stamped")  # names the 95 keys; the CONTENT is read from S3
OUT = os.path.join(HERE, "live95")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def keys():
    out = []
    for name in sorted(os.listdir(SRC)):
        with open(os.path.join(SRC, name), "rb") as handle:
            out.append(json.loads(handle.read().decode("utf-8"))["security_key"])
    return sorted(out)


def strip_validation(doc):
    copy = json.loads(json.dumps(doc))
    for block in copy["blocks"].values():
        block.pop(contract.VALIDATION_KEY, None)
    return copy


def main():
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    s3 = boto3.client("s3", region_name=store.REGION)
    os.makedirs(os.path.join(OUT, "stamped"), exist_ok=True)
    changed, manifest = {}, {}
    n_docs = n_blocks = n_pass = n_refused = n_cleared_now = 0
    problems = []
    for key in keys():
        bucket, objkey = store._split(store.address_for(key))
        old_raw = s3.get_object(Bucket=bucket, Key=objkey)["Body"].read()
        old = json.loads(old_raw.decode("utf-8"))
        held = validation.stamp_validation(old, now, state="HELD")  # verdicts by the producer's rule
        new = json.loads(json.dumps(held))
        refused = []
        for block_id, block in new["blocks"].items():
            n_blocks += 1
            if block[contract.VALIDATION_KEY]["verdict"] == "PASS":
                block[contract.VALIDATION_KEY]["state"] = "CLEARED"
                n_pass += 1
            else:
                refused.append(block_id)
                n_refused += 1
            if old["blocks"][block_id].get(contract.VALIDATION_KEY, {}).get("state") == "CLEARED":
                n_cleared_now += 1
        if not refused:  # the library's own CLEARED stamp must give the same document
            if validation.stamp_validation(old, now, state="CLEARED") != new:
                problems.append("%s: library CLEARED stamp differs from the per-block result" % key)
        if strip_validation(old) != strip_validation(new):
            problems.append("%s: something other than validation differs" % key)
        doc_problems = contract.validate_document(new)
        if doc_problems:
            problems.append("%s: contract.validate_document: %s" % (key, doc_problems[:2]))
        if not served._validate_ai_fill_document(new, key)[0]:
            problems.append("%s: the serve's own rules refuse the re-stamped document" % key)
        raw = store.document_bytes(new) + b"\n"
        name = key.replace("/", "-SLASH-").replace("*", "-STAR-") + ".json"
        with open(os.path.join(OUT, "stamped", name), "wb") as handle:
            handle.write(raw)
        changed[key] = {"file": name}
        manifest[name] = sha(raw)
        n_docs += 1
    report = {"built_at": now.isoformat(), "documents": n_docs, "blocks": n_blocks, "pass_by_producer_rule": n_pass,
              "refused_by_producer_rule": n_refused, "blocks_already_cleared_before": n_cleared_now, "problems": problems}
    with open(os.path.join(OUT, "changed.json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(changed, handle, indent=1, sort_keys=True)
        handle.write("\n")
    with open(os.path.join(OUT, "stamped_sha256_changed.json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, indent=1, sort_keys=True)
        handle.write("\n")
    with open(os.path.join(OUT, "build_report.json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=1, sort_keys=True)
        handle.write("\n")
    print("BUILD: documents %d, blocks %d, PASS by the producer's rule %d, REFUSED %d, already CLEARED before %d, problems %d"
          % (n_docs, n_blocks, n_pass, n_refused, n_cleared_now, len(problems)))
    for p in problems[:10]:
        print("  PROBLEM", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
