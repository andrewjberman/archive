"""IB-pr-381 offline replay of the BUILT runner bundle, on the real inputs. AWS READS ONLY. Run with python -I.

Usage (from anywhere; the bundle is the extracted investor-reporting.tar.gz that BUILD_ONLY produced):
  python -I replay_runner.py <extracted_bundle_dir> <scratch_dir> <now YYYY-MM-DD>

It drives the BUNDLE'S OWN `directory_runner.run_firm` (upload=False: nothing is put to S3) for inflection and cottonwood, three arms each,
on the firm's real source snapshot (the runner's own source adapter reads the silver planes) and the real previous directories:
  * served   -- previous = the SERVED directory (what a scheduled run reads). The entry the vendor removed is already gone from it.
  * seeded   -- previous = the last accounted-completion build (`--previous-key`, from prev_keys.json written by replay_refresh.py prev):
                the one-time reconciling run. The entry is carried TERMINATED into the landed directory.
  * negative -- the seeded run with the dropped key put back into the SOURCE snapshot only: the entry stays missing from the build and
                must NOT be carried.
Each arm's landed directory.json/latest.json is written under <scratch>/landed_<arm>/ (CLIENT ENTRIES: scratch only, never committed).
Output <scratch>/runner_result.json carries counts and booleans only: no id, no name.
"""
import datetime as dt
import json
import os
import sys

tree, scratch, now = sys.argv[1:4]
sys.path.insert(0, os.path.join(tree, "data", "assets", "scripts", "gold", "investor_reporting"))
import boto3  # noqa: E402
import directory_runner as dr  # noqa: E402

assert os.path.abspath(dr.__file__).startswith(os.path.abspath(tree)), "runner resolved outside the bundle"
S3 = boto3.client("s3", region_name="us-east-1")
BUCKETS = dr.firm_bucket_map()
FIRMS = ("inflection", "cottonwood")
PREV = json.load(open(os.path.join(scratch, "prev_keys.json"), encoding="utf-8"))
ORIG_SOURCE_IDS = dr.source_client_ids


def loader(bucket, prefix, explicit_key):
    return dr.read_previous_served(bucket, prefix, explicit_key, s3=S3)


def marked(entries):
    return [e for e in entries if (e.get("termination") or {}).get("indicator") == "TERMINATED" and dr._source_removed_on_of(e)]


def run(firm, arm, previous_key, extra_source_ids=()):
    if extra_source_ids:
        dr.source_client_ids = lambda f, d: sorted(set(ORIG_SOURCE_IDS(f, d)) | set(extra_source_ids))
    try:
        out = os.path.join(scratch, "landed_" + arm)
        res = dr.run_firm({"firm_id": firm}, BUCKETS, qa=False, upload=False, local_out=out, explicit=None,
                          now=dt.date.fromisoformat(now), previous_loader=loader, previous_key=previous_key)
    finally:
        dr.source_client_ids = ORIG_SOURCE_IDS
    p = res["payload"]
    cf = res["carried_forward"]
    return res, {"business_date": res["business_date"], "entry_count": res["entry_count"], "entries_valid": res["entries_valid"],
                 "validation_errors": len(res["validation_errors"]), "source_client_ids": len(p["source_client_ids"]),
                 "previous_directory_key": cf["previous_directory_key"], "previous_as_of": cf["previous_as_of"],
                 "carried_terminated_keys": cf["terminated"], "held_in_source": cf["held_in_source"],
                 "carried_in_landed": len(marked(p["entries"])) > 0, "landed_marked_entries": len(marked(p["entries"])),
                 "landed_key": res["landed"]["key"], "note": cf["note"]}


result = {"now": now, "runner_file": os.path.relpath(dr.__file__, tree).replace("\\", "/"), "firms": {}}
for firm in FIRMS:
    served = loader(BUCKETS[firm], dr.PROD_PREFIX, None)
    arms = {"served_directory_read": {"key": served["key"], "as_of": served["payload"].get("as_of_business_date"),
                                      "entry_count": len(served["payload"]["entries"]),
                                      "marked_entries": len(marked(served["payload"]["entries"])),
                                      "states_source_client_ids": "source_client_ids" in served["payload"]}}
    r_served, arms["served"] = run(firm, "served", None)
    r_seeded, arms["seeded"] = run(firm, "seeded", PREV[firm]["fire_20261008"]["key"])
    dropped = [dr.entry_key(e) for e in marked(r_seeded["payload"]["entries"])]
    r_neg, arms["negative"] = run(firm, "negative", PREV[firm]["fire_20261008"]["key"], extra_source_ids=dropped)
    arms["dropped_keys"] = len(set(dropped))
    result["firms"][firm] = arms
with open(os.path.join(scratch, "runner_result.json"), "w", encoding="utf-8") as fh:
    json.dump(result, fh, indent=1, sort_keys=True)
print(json.dumps({f: {a: (v["carried_terminated_keys"], v["held_in_source"], v["carried_in_landed"]) for a, v in r.items()
                      if isinstance(v, dict) and "carried_terminated_keys" in v} for f, r in result["firms"].items()}))
