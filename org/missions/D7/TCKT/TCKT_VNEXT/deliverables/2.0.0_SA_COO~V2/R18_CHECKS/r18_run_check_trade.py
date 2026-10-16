"""TCKT_VNEXT round 18 -- R18-tf-6 ONLY (PART 2, FWD-10): the Trade Request journey on a never-pushed scratch build of DEV, re-read by an identity that did not write it.

The Meeting Request journey (FWD-11) is PART 1 and is read by r18_run_check_meeting.py. This variant is r18_run_check.py with the meeting ticket, the coordinator identity and the routing window removed; the trade ticket, the form object, the PUT origin, the placeholder and the identity row checks are identical.

Prints RUN-OK <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1). The result file is the applier's; every claim in it
that the world can contradict is re-read here: both tickets from the table, the trade form's object from S3, the synthetic identity's row.
The coordinator's act on the meeting ticket is a pre-arranged input with an owner; this check reads its trace on the ticket, never the applier's word.
"""
import json
import os
import subprocess
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r18_run/R18_RUN_P2_RESULT.json"
REC = "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~43/ATTACH_ADDRESS.json"
COORDINATOR = "jeanette@opalinvest.com"
KEYS = {"browser_origin", "put_origin_header", "identity", "firm", "tf_ticket", "tf_filer", "row_deleted_at", "token_exp",
        "row_absent_after", "form_key", "form_name", "form_version_id", "placeholder_named", "no_engine_call", "token_printed",
        "scratch_diff_lines", "scratch_removed"}
AWS = os.path.abspath(".tools/aws.cmd")


def aws(*args, empty_ok=False):
    out = subprocess.run([AWS] + list(args) + ["--region", "us-east-1", "--output", "json"],
                         capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("aws %s rc=%d" % (" ".join(args[:2]), out.returncode))
    if not out.stdout.strip():
        if empty_ok:
            return None
        raise RuntimeError("aws %s printed nothing" % " ".join(args[:2]))
    return json.loads(out.stdout)


def item(table, key):
    out = aws("dynamodb", "get-item", "--table-name", table, "--key", json.dumps(key), "--consistent-read", empty_ok=True)
    return None if out is None else out.get("Item")


def main():
    try:
        doc = json.load(open(RES, encoding="utf-8"))
        rec = json.load(open(REC, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("RUN-BAD cannot read the result file or the builder record: %s" % e)
        return 1
    missing = sorted(KEYS - set(doc))
    if missing:
        print("RUN-BAD missing key(s): %s" % missing)
        return 1
    if doc["put_origin_header"] != "http://localhost:5174":
        print("RUN-BAD the PUT Origin header is %r, not http://localhost:5174" % (doc["put_origin_header"],))
        return 1
    if doc["browser_origin"] != "http://localhost:5174":
        print("RUN-BAD the browser origin is %r, not the one DEV origin http://localhost:5174" % (doc["browser_origin"],))
        return 1
    if doc["token_printed"] is not False or doc["no_engine_call"] is not True or doc["placeholder_named"] is not True:
        print("RUN-BAD token_printed, no_engine_call or placeholder_named differs from the order")
        return 1
    if str(doc["row_deleted_at"]) <= str(doc["token_exp"]) or doc["row_absent_after"] is not True:
        print("RUN-BAD the identity row was not deleted after exp and read absent")
        return 1
    ident = doc["identity"]
    prefix = rec["key_template"].format(firm=doc["firm"])
    if not str(doc["form_key"]).startswith(prefix):
        print("RUN-BAD the form's key is not under the firm's prefix")
        return 1
    try:
        tf = item("opal-tickets", {"ticket_id": {"S": doc["tf_ticket"]}})
        if not tf or tf.get("ticket_type", {}).get("S") != "trade_request" or tf.get("status", {}).get("S") != "open":
            print("RUN-BAD the trade ticket is missing, not a trade_request, or not open")
            return 1
        att = tf.get("attachment", {}).get("M") or {}
        if att.get("key", {}).get("S") != doc["form_key"]:
            print("RUN-BAD the trade ticket's attachment key is not the recorded form key")
            return 1
        head = aws("s3api", "head-object", "--bucket", rec["buckets"][doc["firm"]], "--key", doc["form_key"])
        if int(head.get("ContentLength", 0)) < 1:
            print("RUN-BAD the form object is empty or absent")
            return 1
        if head.get("VersionId") != doc["form_version_id"]:
            print("RUN-BAD the form object's VersionId is not the recorded one")
            return 1
        row = item("opal-users-v2", {"PK": {"S": "USER#" + ident}, "SK": {"S": "PROFILE"}})
        if row is not None:
            print("RUN-BAD the identity row is still PRESENT")
            return 1
        if doc["scratch_diff_lines"] != 1 or doc["scratch_removed"] is not True:
            print("RUN-BAD the scratch build was not exactly a one-line change or was not removed")
            return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK (trade only) trade ticket open with its form object under %s; the identity row absent; the scratch build a one-line change, removed" % prefix)
    return 0


if __name__ == "__main__":
    sys.exit(main())
