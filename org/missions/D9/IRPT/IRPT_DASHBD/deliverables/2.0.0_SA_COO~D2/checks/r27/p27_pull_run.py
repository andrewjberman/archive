"""IRPT_DASHBD round 27, workstream BD (issuer 2.0.0_SA_COO~D2) -- FWD-8: the split Black Diamond pull's run, made on the laptop by
0.7.0_AE_CloudOps~I (laptop CTO ruling msg 106630 via MSTR msg 1145), graded on dell2 from the returned record.

Usage: python <this file> <repo_root> <criterion_id>
  DB27-1-AC1  the returned run record deliverables/2.0.0_SA_COO~D2/relay/SPLIT_PULL_RUN.json: `aborted` null; the final denominators
              close over the plan's 2,299 (landed_before + landed_this_run + FAILED == 2,299 after the sweep, if any) with FAILED <= 105;
              no call names an account outside the plan. Base: FAIL.
  DB27-1-AC2  S3: the objects listed under the plan's pull= prefix equal the record's landed accounts, by key. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
PLAN = D + "0.9.0_WK_IRPT_DASHBD~25/SPLIT_PULL_PLAN.json"
RUN = D + "2.0.0_SA_COO~D2/relay/SPLIT_PULL_RUN.json"
SWEEP = D + "2.0.0_SA_COO~D2/relay/SPLIT_PULL_SWEEP.json"
FAILED_CAP = 105


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB27-1"))
        sys.exit(1)

    def load(rel, need=True):
        p = root / rel
        if not p.is_file():
            if need:
                fail("no %s" % rel)
            return None
        return json.loads(p.read_bytes().decode("utf-8"))

    plan = load(PLAN)
    keys = {str(r["bd_account"]): r["landing_key"] for r in plan["request_list"]}
    accts = {r["account"] for r in plan["request_list"]}
    run = load(RUN)
    sweep = load(SWEEP, need=False)
    records = list(run.get("records") or []) + list((sweep or {}).get("records") or [])
    outside = sorted({r.get("account") for r in records if r.get("account") not in accts})
    if outside:
        fail("calls name accounts outside the plan: %s" % outside[:5])
    landed = {r["account"] for r in records if r.get("status") == "LANDED" or r.get("landed") is True}
    failed = {r["account"] for r in records if r.get("status") == "FAILED"} - landed

    if cid == "DB27-1-AC1":
        last = sweep or run
        if run.get("aborted") or (sweep and sweep.get("aborted")):
            fail("aborted: run %r, sweep %r" % (run.get("aborted"), sweep and sweep.get("aborted")))
        if len(landed) + len(failed) != len(accts) or len(failed) > FAILED_CAP:
            fail("landed %d + FAILED %d against %d planned (cap %d)" % (len(landed), len(failed), len(accts), FAILED_CAP))
        print("OK: %d landed, %d FAILED of %d planned; aborted null%s" % (
            len(landed), len(failed), len(accts), "; swept once" if sweep else ""))
        _ = last
    elif cid == "DB27-1-AC2":
        import boto3
        bucket = plan["request_list"][0]["landing_key"].split("/")[2]
        prefix = "/".join(plan["request_list"][0]["landing_key"].split("/")[3:-1]) + "/"
        s3 = boto3.client("s3", region_name="us-east-1")
        listed = set()
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
            for o in page.get("Contents") or []:
                listed.add("s3://%s/%s" % (bucket, o["Key"]))
        by_acct = {r["account"]: r["landing_key"] for r in plan["request_list"]}
        want = {by_acct[a] for a in landed}
        if listed != want:
            fail("S3 lists %d keys under %s, the record lands %d (extra %d, missing %d)" % (
                len(listed), prefix, len(want), len(listed - want), len(want - listed)))
        print("OK: %d keys under s3://%s/%s equal the record's landed accounts" % (len(listed), bucket, prefix))
        _ = keys
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
