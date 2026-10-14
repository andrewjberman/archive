"""TCKT_VNEXT round 18 -- R18-mt-5 / R18-tf-6: ONE live run of each journey on DEV, re-read by an identity that did not write them.

Prints RUN-OK <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1). The result file is the applier's; every claim in it
that the world can contradict is re-read here: both tickets from the table, the trade form's object from S3, the synthetic identity's row.
The coordinator's act on the meeting ticket is a pre-arranged input with an owner; this check reads its trace on the ticket, never the applier's word.
"""
import json
import os
import subprocess
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r18_run/R18_RUN_RESULT.json"
REC = "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~43/ATTACH_ADDRESS.json"
COORDINATOR = "jeanette@opalinvest.com"
KEYS = {"identity", "firm", "mt_ticket", "tf_ticket", "mt_filer", "tf_filer", "row_deleted_at", "token_exp",
        "row_absent_after", "form_key", "form_name", "placeholder_named", "no_engine_call", "token_printed"}
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
        head = aws("s3api", "head-object", "--bucket", rec["bucket"], "--key", doc["form_key"])
        if int(head.get("ContentLength", 0)) < 1:
            print("RUN-BAD the form object is empty or absent")
            return 1
        mt = item("opal-tickets", {"ticket_id": {"S": doc["mt_ticket"]}})
        if not mt or mt.get("ticket_type", {}).get("S") != "meeting_request":
            print("RUN-BAD the meeting ticket is missing or not a meeting_request")
            return 1
        meeting = mt.get("meeting", {}).get("M")
        if not meeting or meeting.get("status", {}).get("S") not in ("confirmed", "rescheduled") or meeting.get("by", {}).get("S") != COORDINATOR:
            print("RUN-BAD the meeting ticket carries no outcome recorded by the coordinator")
            return 1
        if mt.get("status", {}).get("S") == "completed":
            print("RUN-BAD the meeting ticket was completed; the outcome must not complete it")
            return 1
        row = item("opal-users-v2", {"PK": {"S": "USER#" + ident}, "SK": {"S": "PROFILE"}})
        if row is not None:
            print("RUN-BAD the identity row is still PRESENT")
            return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK trade ticket open with its form object under %s; meeting outcome %s by the coordinator; identity row absent" % (prefix, meeting["status"]["S"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
