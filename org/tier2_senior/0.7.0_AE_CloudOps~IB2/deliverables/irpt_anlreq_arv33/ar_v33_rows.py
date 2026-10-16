"""IRPT_ANLREQ TO-RUN-AR-v33 (0.7.0_AE_CloudOps~IB2): the table reads and the one fixture attribute of sitting 2.

  python ar_v33_rows.py pre        READ ONLY: lines B2 (ticket TCK-20261015-944c84f8 and its PRE hash), A1 (the job row's hop_failure), B3 (the packaged
                                   ticket), and the users-row-ABSENT line. Writes the PRE hash beside this file's out dir argument.
  python ar_v33_rows.py fixture    ONE update-item on opal-tickets: SET report_ref with attribute_not_exists(report_ref); reads it back; prints F1.
  python ar_v33_rows.py unfixture  ONE update-item REMOVE report_ref with the condition recorded_by = :fixture; reads it back ABSENT; prints R3.
  python ar_v33_rows.py state      READ ONLY: the arm-A ticket item hash and whether report_ref is present (no write).

The item hash is sha256 over json.dumps(Item, sort_keys=True, separators=(",", ":")) of a consistent get-item. No credential, password, token or hash of a
credential is read or printed; ticket text is never printed.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import boto3

REGION = "us-east-1"
TICKETS = "opal-tickets"
JOBS = "irpt-jobs"
USERS = "opal-users-v2"
TICKET_A = "TCK-20261015-944c84f8"
TICKET_B = "TCK-20261014-2965a5e0"
REQ_A = "REQ-d47252fe74634d0c5cdd8067"
EMAIL = "fwd1-staff-r41b@opal.invalid"
OUT = Path(__file__).resolve().parent
PRE_FILE = OUT / "pre_hash.txt"
d = boto3.client("dynamodb", region_name=REGION)


def item(table, key):
    return d.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def ihash(it):
    return hashlib.sha256(json.dumps(it, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def cmd_pre():
    a = item(TICKETS, {"ticket_id": {"S": TICKET_A}})
    if not a:
        print("STOP ticket A absent")
        return 2
    h = ihash(a)
    PRE_FILE.write_text(h, encoding="ascii")
    st = (a.get("status") or {}).get("S")
    ttype = (a.get("ticket_type") or {}).get("S")
    pkg = "PRESENT" if "package" in a else "ABSENT"
    rr = "PRESENT" if "report_ref" in a else "ABSENT"
    print("B2 ticket=%s type=%s status=%s package=%s report_ref=%s item_sha256=%s" % (TICKET_A, ttype, st, pkg, rr, h))
    j = item(JOBS, {"tenant": {"S": "49financial"}, "job": {"S": REQ_A}})
    if not j:
        print("STOP job row absent")
        return 2
    hf = (j.get("hop_failure") or {}).get("M")
    state = (j.get("state") or j.get("status") or {}).get("S")
    if hf:
        print("A1 job=%s state=%s hop_failure=PRESENT hop=%s code=%s at=%s" % (REQ_A, state, hf["hop"]["S"], hf["code"]["S"], hf["at"]["S"]))
    else:
        print("A1 job=%s state=%s hop_failure=ABSENT" % (REQ_A, state))
    b = item(TICKETS, {"ticket_id": {"S": TICKET_B}})
    if not b:
        print("STOP ticket B absent")
        return 2
    print("B3 ticket=%s type=%s status=%s package=%s report_ref=%s" % (TICKET_B, (b.get("ticket_type") or {}).get("S"), (b.get("status") or {}).get("S"),
                                                                       "PRESENT" if "package" in b else "ABSENT", "PRESENT" if "report_ref" in b else "ABSENT"))
    u = item(USERS, {"PK": {"S": "USER#" + EMAIL}, "SK": {"S": "PROFILE"}})
    print("USERS row for the synthetic staff user: %s (consistent get)" % ("PRESENT" if u else "ABSENT"))
    return 0 if (not u and "package" not in a and "report_ref" not in a and hf and hf["code"]["S"] == "COMMENTARY_DRAFT_REFUSED" and "package" in b) else 3


def cmd_fixture():
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ref = {"M": {"request_id": {"S": REQ_A}, "revision": {"S": "1"}, "recorded_by": {"S": "fixture:AR-v-32-s2"}, "recorded_at": {"S": now}}}
    d.update_item(TableName=TICKETS, Key={"ticket_id": {"S": TICKET_A}}, UpdateExpression="SET report_ref = :ref",
                  ConditionExpression="attribute_not_exists(report_ref)", ExpressionAttributeValues={":ref": ref})
    a = item(TICKETS, {"ticket_id": {"S": TICKET_A}})
    rr = (a.get("report_ref") or {}).get("M") or {}
    ok = rr.get("request_id", {}).get("S") == REQ_A and rr.get("recorded_by", {}).get("S", "").startswith("fixture:")
    print("F1 fixture ticket=%s request_id=%s written=%s recorded_by=%s" % (TICKET_A, REQ_A, "YES" if ok else "NO", rr.get("recorded_by", {}).get("S")))
    return 0 if ok else 3


def cmd_unfixture():
    d.update_item(TableName=TICKETS, Key={"ticket_id": {"S": TICKET_A}}, UpdateExpression="REMOVE report_ref",
                  ConditionExpression="report_ref.recorded_by = :fixture", ExpressionAttributeValues={":fixture": {"S": "fixture:AR-v-32-s2"}})
    a = item(TICKETS, {"ticket_id": {"S": TICKET_A}})
    pre = PRE_FILE.read_text(encoding="ascii").strip()
    absent = "report_ref" not in a
    eq = ihash(a) == pre
    print("R3 ticket %s report_ref=%s item_hash_equals_pre=%s" % (TICKET_A, "ABSENT" if absent else "PRESENT", "YES" if eq else "NO"))
    return 0 if (absent and eq) else 3


def cmd_state():
    a = item(TICKETS, {"ticket_id": {"S": TICKET_A}})
    print("STATE ticket=%s report_ref=%s hash_equals_pre=%s" % (TICKET_A, "PRESENT" if "report_ref" in a else "ABSENT",
                                                                 "YES" if ihash(a) == PRE_FILE.read_text(encoding="ascii").strip() else "NO"))
    return 0


if __name__ == "__main__":
    sys.exit({"pre": cmd_pre, "fixture": cmd_fixture, "unfixture": cmd_unfixture, "state": cmd_state}[sys.argv[1]]())
