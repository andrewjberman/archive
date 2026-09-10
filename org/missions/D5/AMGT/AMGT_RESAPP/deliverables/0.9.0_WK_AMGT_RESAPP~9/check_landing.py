#!/usr/bin/env python3
"""AC1 -- reads back the actual landed state from S3 and sa_ids.json, never from the fetcher's own
log. Prints exactly one line of the shape:
  SA LANDING: tickers <n>; raw objects <n> across <n> keys; symbol+report present for <a> of <b>; sa_ids MEASURED <c>
"""
import json
import os

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    with open(os.path.join(HERE, "run_manifest.json"), encoding="utf-8") as fh:
        manifest = json.load(fh)
    tickers = manifest["tickers"]

    with open(os.path.join(HERE, "sa_ids.json"), encoding="utf-8") as fh:
        sa_ids = json.load(fh)

    # Read the vendor + bucket names from the module's own config.json rather than hardcoding here.
    repo_root = HERE
    while not os.path.isdir(os.path.join(repo_root, "integrations", "seekingalpha")):
        parent = os.path.dirname(repo_root)
        if parent == repo_root:
            raise RuntimeError("could not locate integrations/seekingalpha/ from %s" % HERE)
        repo_root = parent
    with open(
        os.path.join(repo_root, "integrations", "seekingalpha", "config.json"), encoding="utf-8"
    ) as fh:
        config = json.load(fh)

    s3 = boto3.client("s3", region_name=config["region"])
    bucket = config["store_bucket"]
    vendor = config["vendor"]

    total_raw_objects = 0
    symbol_and_report_count = 0
    for t in tickers:
        prefix = "raw/%s/%s/" % (vendor, t["security_key"])
        keys = []
        continuation = None
        while True:
            kwargs = {"Bucket": bucket, "Prefix": prefix}
            if continuation:
                kwargs["ContinuationToken"] = continuation
            resp = s3.list_objects_v2(**kwargs)
            for obj in resp.get("Contents", []):
                keys.append(obj["Key"])
            if resp.get("IsTruncated"):
                continuation = resp.get("NextContinuationToken")
            else:
                break
        total_raw_objects += len(keys)
        has_symbol = any(k.endswith("/symbol.json") for k in keys)
        has_report = any(k.endswith("/report.json") for k in keys)
        if has_symbol and has_report:
            symbol_and_report_count += 1

    measured = sum(1 for v in sa_ids.values() if v.get("status") == "MEASURED")

    print(
        "SA LANDING: tickers %d; raw objects %d across %d keys; symbol+report present for %d of %d; sa_ids MEASURED %d"
        % (
            len(tickers),
            total_raw_objects,
            len(tickers),
            symbol_and_report_count,
            len(tickers),
            measured,
        )
    )


if __name__ == "__main__":
    main()
