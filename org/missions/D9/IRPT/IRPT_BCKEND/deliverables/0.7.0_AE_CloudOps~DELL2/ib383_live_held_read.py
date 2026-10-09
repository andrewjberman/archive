"""IB-pr-383, the CTO-corrected gate: read LIVE held_in_source for ALL THREE firms off the ratified bundle.

AWS READS ONLY. `upload=False` and `local_out=None`, so nothing is put to S3 and nothing is written
locally. That choice is deliberate and not incidental: the IB-pr-384 runner RAISES its
BUILD_DROPS_SOURCE_ENTRY refusal when `upload or local_out` is truthy, and merely RECORDS it in
`carried_forward.refused` otherwise. I want the verdict observable, not an exception, so neither is set.

The issuer's harness (deliverables/0.9.0_WK_IRPT_BCKEND~189/replay/replay_runner.py) covers
inflection and cottonwood only; the corrected ruling asks for all three, and that harness is
another seat's file, so this driver is this seat's own rather than an edit to theirs.

Usage: python -I ib383_live_held_read.py <extracted_bundle_dir> <out.json>
"""
import datetime as dt
import io
import json
import os
import sys

tree, out_path = sys.argv[1:3]
sys.path.insert(0, os.path.join(tree, "data", "assets", "scripts", "gold", "investor_reporting"))
import boto3  # noqa: E402
import directory_runner as dr  # noqa: E402

assert os.path.abspath(dr.__file__).startswith(os.path.abspath(tree)), "runner resolved outside the bundle"

S3 = boto3.client("s3", region_name="us-east-1")
BUCKETS = dr.firm_bucket_map()
TODAY = dt.date.today()

# The packet's per-firm seeding keys. 49financial is NOT seeded, so it has no previous-key arm.
PREVIOUS_KEY = {
    "inflection": "investor-reporting/directory/2026-09-25/directory.json",
    "cottonwood": "investor-reporting/directory/2026-10-05/directory.json",
    "49financial": None,
}


def loader(bucket, prefix, explicit_key):
    return dr.read_previous_served(bucket, prefix, explicit_key, s3=S3)


def arm(firm, previous_key):
    """One read. Returns the counts that decide the gate, or the error type if the firm refuses."""
    try:
        res = dr.run_firm({"firm_id": firm}, BUCKETS, qa=False, upload=False, local_out=None,
                          explicit=None, now=TODAY, previous_loader=loader, previous_key=previous_key)
    except Exception as exc:  # noqa: BLE001 -- the error TYPE is the recorded evidence (CTO condition 4)
        return {"ok": False, "error_type": type(exc).__name__, "error": str(exc)[:300]}
    cf = res["carried_forward"]
    return {"ok": True,
            "business_date": res["business_date"],
            "entry_count": res["entry_count"],
            "held_in_source": cf["held_in_source"],
            "carried_terminated_keys": cf["terminated"],
            "previous_as_of": cf["previous_as_of"],
            "previous_directory_key": cf["previous_directory_key"],
            "refused": cf.get("refused"),
            "validation_errors": len(res["validation_errors"])}


def main():
    out = {"bundle_dir": tree, "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "today": TODAY.isoformat(), "firms": {}}
    for firm in ("inflection", "cottonwood", "49financial"):
        pk = PREVIOUS_KEY[firm]
        out["firms"][firm] = {"seeded_arm_previous_key": pk,
                              "served": arm(firm, None),
                              "seeded": arm(firm, pk) if pk else None}
        s = out["firms"][firm]
        for name in ("served", "seeded"):
            a = s[name]
            if a is None:
                print("  %-12s %-7s not applicable (no previous-key arm)" % (firm, name))
            elif a["ok"]:
                print("  %-12s %-7s held_in_source=%s carried=%s refused=%s" %
                      (firm, name, a["held_in_source"], a["carried_terminated_keys"],
                       (a["refused"] or "none")[:40] if a["refused"] else "none"))
            else:
                print("  %-12s %-7s REFUSED %s" % (firm, name, a["error_type"]))
    with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print()
    print("wrote", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
