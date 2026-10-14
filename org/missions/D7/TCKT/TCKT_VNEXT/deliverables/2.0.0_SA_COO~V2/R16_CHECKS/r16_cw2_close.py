"""TCKT_VNEXT round 16 -- R16-cw-2: both cottonwood test tickets read `completed` in the live store, claimed and completed by the
one crawl identity, whose row is absent after its token's exp; the mail branch and the zero-call read are in the result file.

Both tickets and the identity row are re-read here with live get-item calls, independent of the result file's claims.
Prints CW2-OK <detail> or CW2-FAIL <reason>; exit 0/1.
"""
import json
import os
import subprocess
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r16_cw2/R16_CRAWL_RESULT_20261013.json"
TICKETS = ("TCK-20261009-a1052909", "TCK-20261012-13cd3a1d")
NEVER = "TCK-20261012-c546fead"
IDENT = "tckt-r2-crawler-20261013@opal.invalid"
KEYS = {"tickets", "identity", "firm_list", "token_exp", "row_deleted_at", "row_absent_after", "mail_branch",
        "zero_call_read", "token_printed", "claim"}
MAIL_OK = {"WE_CLIENT_SEND_FAILED", "WE_CLIENT_NOT_SINGULAR"}
AWS = os.path.abspath(".tools/aws.cmd")


def get_item(table, key):
    out = subprocess.run([AWS, "dynamodb", "get-item", "--table-name", table, "--key", json.dumps(key),
                          "--consistent-read", "--region", "us-east-1", "--output", "json"],
                         capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("get-item rc=%d" % out.returncode)
    if not out.stdout.strip():
        return None
    return json.loads(out.stdout).get("Item")


def main():
    try:
        raw = open(RES, encoding="utf-8").read()
        doc = json.loads(raw)
    except (OSError, ValueError) as e:
        print("CW2-FAIL cannot read the result file: %s" % e)
        return 1
    if NEVER in raw or raw.replace(IDENT, "").count("@"):
        print("CW2-FAIL the file names the card-1 ticket or holds an address other than the identity's")
        return 1
    missing = sorted(KEYS - set(doc))
    if missing:
        print("CW2-FAIL missing key(s): %s" % missing)
        return 1
    if doc["identity"] != IDENT or doc["firm_list"] != ["cottonwood"] or doc["token_printed"] is not False:
        print("CW2-FAIL identity, firm list or token_printed differs from the pair")
        return 1
    if sorted(doc["tickets"]) != sorted(TICKETS):
        print("CW2-FAIL tickets differ from the two named in the pair: %r" % (doc["tickets"],))
        return 1
    if str(doc["row_deleted_at"]) <= str(doc["token_exp"]) or doc["row_absent_after"] is not True:
        print("CW2-FAIL the row was not deleted after exp and read absent")
        return 1
    mb = doc["mail_branch"]
    if not isinstance(mb, dict) or set(mb) != set(TICKETS) or not set(mb.values()) <= MAIL_OK:
        print("CW2-FAIL mail branch must be one OK token per ticket: %r" % (mb,))
        return 1
    zc = doc["zero_call_read"]
    if not isinstance(zc, dict) or int(zc.get("streams_searched", 0)) < 1 or zc.get("count") != 0:
        print("CW2-FAIL zero-call read VOID or non-zero: %r" % (zc,))
        return 1
    try:
        for tid in TICKETS:
            item = get_item("opal-tickets", {"ticket_id": {"S": tid}})
            if not item:
                print("CW2-FAIL live ticket %s not found" % tid)
                return 1
            st = item.get("status", {}).get("S")
            asg = item.get("assignee", {}).get("S")
            if st != "completed" or asg != IDENT:
                print("CW2-FAIL live %s: status=%s assignee-is-identity=%s" % (tid, st, asg == IDENT))
                return 1
        row = get_item("opal-users-v2", {"PK": {"S": "USER#" + IDENT}, "SK": {"S": "PROFILE"}})
        if row is not None:
            print("CW2-FAIL the identity row is still PRESENT")
            return 1
        never = get_item("opal-tickets", {"ticket_id": {"S": NEVER}})
        if not never or never.get("assignee", {}).get("S") == IDENT:
            print("CW2-FAIL the card-1 ticket is missing or was claimed by the crawl identity")
            return 1
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as e:
        print("CW2-FAIL live read failed: %s" % e)
        return 1
    print("CW2-OK two tickets completed by the identity; row absent after exp; card-1 ticket never claimed by the identity")
    return 0


if __name__ == "__main__":
    sys.exit(main())
