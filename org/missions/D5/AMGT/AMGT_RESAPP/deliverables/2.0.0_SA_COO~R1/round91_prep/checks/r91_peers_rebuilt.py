"""AMGT_RESAPP round-91 PREP -- AMGT-pp-3: the peers objects are rebuilt against the current scanner, and nothing prior is overwritten.

  PYTHONPATH=<repo root> python r91_peers_rebuilt.py [--expect <PEERS_REBUILD_DRYRUN_20261011.json>]

Reads (GET and LIST only) the LATEST `peers/v1/<slash-safe key>/` object of each of the 243 keyed crosswalk names and compares it with
the in-memory dry run the never-widen COO half cites (`round91_prep/PEERS_REBUILD_DRYRUN_20261011.json`: the producer's own
`engine.peers` over the fresh scanner universe).
    P1 every name's latest object sits in a partition that sorts AFTER `2026-09-24T2252Z` (a NEW dated object).
    P2 all names share ONE write partition (the batch's `write_as_of`).
    P3 every name's basis equals the dry run's.
    P4 every name's member ticker list equals the dry run's, in order.
    P5 every scanner-sourced member's cap_vintage is the scanner's asOf (2026-10-02); the one model-block-only candidate is named.
    P6 control: each name's PRIOR object (the dry run's `old_key`) is still in place -- nothing was overwritten or deleted.
Verdict: R91 PEERS REBUILT: YES|NO (exit 0|1). At the base (2026-10-11) P1-P5 FAIL, P6 PASSes.
"""
import argparse
import collections
import json
import os
import sys

import boto3

from lib.research.identity import crosswalk

BUCKET = "opal-data-harvest"
OLD_FLOOR = "2026-09-24T2252Z"
SCANNER_ASOF = "2026-10-02"
DEFAULT = os.path.join("org", "missions", "D5", "AMGT", "AMGT_RESAPP", "deliverables", "2.0.0_SA_COO~R1", "round91_prep",
                       "PEERS_REBUILD_DRYRUN_20261011.json")


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect", default=DEFAULT)
    args = ap.parse_args()
    rows = json.load(open(args.expect))
    s3 = boto3.client("s3", region_name="us-east-1")
    partitions = collections.Counter()
    new_ok = basis_ok = members_ok = cap_ok = prior_ok = 0
    cap_exceptions = []
    bad = collections.defaultdict(list)
    for r in rows:
        key = r["key"]
        prefix = "peers/v1/%s/" % crosswalk.slash_safe_key(key)
        listed = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix).get("Contents", [])
        keys = sorted(o["Key"] for o in listed)
        latest = keys[-1] if keys else None
        part = latest.rsplit("/", 1)[-1][: -len(".json")] if latest else None
        partitions[part] += 1
        if part and part > OLD_FLOOR:
            new_ok += 1
        else:
            bad["P1"].append(key)
        if r.get("old_key") is None or r["old_key"] in keys:
            prior_ok += 1
        else:
            bad["P6"].append(key)
        obj = json.loads(s3.get_object(Bucket=BUCKET, Key=latest)["Body"].read()) if latest else {}
        if obj.get("basis") == r["new_basis"]:
            basis_ok += 1
        else:
            bad["P3"].append(key)
        tickers = [m.get("ticker") for m in obj.get("members", [])]
        if tickers == r["new_members"]:
            members_ok += 1
        else:
            bad["P4"].append(key)
        vint = {m.get("cap_vintage") for m in obj.get("members", []) if m.get("cap_vintage")}
        extra = sorted(v for v in vint if v != SCANNER_ASOF)
        expected_extra = sorted(v for v in r["new_cap_vintages"] if v != SCANNER_ASOF)
        if extra == expected_extra:
            cap_ok += 1
            if extra:
                cap_exceptions.append((key, extra))
        else:
            bad["P5"].append(key)
    n = len(rows)
    res = [
        say(new_ok == n, "P1 every latest object is a NEW dated object (after %s)" % OLD_FLOOR, "%d of %d" % (new_ok, n)),
        say(len([p for p in partitions if p]) == 1 and None not in partitions,
            "P2 one write partition for all names", json.dumps(dict(partitions))[:160]),
        say(basis_ok == n, "P3 basis equals the dry run's", "%d of %d" % (basis_ok, n)),
        say(members_ok == n, "P4 member tickers equal the dry run's, in order", "%d of %d" % (members_ok, n)),
        say(cap_ok == n, "P5 every scanner-sourced member cap_vintage is %s" % SCANNER_ASOF,
            "%d of %d; exception(s): %s" % (cap_ok, n, cap_exceptions)),
        say(prior_ok == n, "P6 control: every prior object is still in place", "%d of %d" % (prior_ok, n)),
    ]
    for k, v in bad.items():
        print("   %s first failing names: %s" % (k, v[:5]))
    ok = all(res)
    print("R91 PEERS REBUILT: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
