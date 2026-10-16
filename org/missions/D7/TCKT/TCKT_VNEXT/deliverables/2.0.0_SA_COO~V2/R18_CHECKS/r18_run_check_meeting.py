"""TCKT_VNEXT round 18 -- R18-mt-5 ONLY (PART 1, FWD-11): the Meeting Request journey on DEV, re-read by an identity that did not write it.

The Trade Request option is hidden in the DEV new-ticket list by Andrew's word of 2026-10-13 (hide 4d601023), so FWD-10's journey is PART 2 and is not read here. This variant is r18_run_check.py with the trade ticket, the form object, the form key and the placeholder
claims removed; everything else is identical.

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
KEYS = {"browser_origin", "identity", "coordinator_identity", "mt_confirmed_time", "routing_before", "routing_during", "routing_after",
        "firm", "mt_ticket", "mt_filer", "row_deleted_at", "token_exp",
        "row_absent_after", "no_engine_call", "token_printed"}
FUNCTION = "opal-ticket-api"
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
    except (OSError, ValueError) as e:
        print("RUN-BAD cannot read the result file: %s" % e)
        return 1
    missing = sorted(KEYS - set(doc))
    if missing:
        print("RUN-BAD missing key(s): %s" % missing)
        return 1
    if doc["browser_origin"] != "http://localhost:5174":
        print("RUN-BAD the browser origin is %r, not the one DEV origin http://localhost:5174" % (doc["browser_origin"],))
        return 1
    if doc["token_printed"] is not False or doc["no_engine_call"] is not True:
        print("RUN-BAD token_printed or no_engine_call differs from the order")
        return 1
    if str(doc["row_deleted_at"]) <= str(doc["token_exp"]) or doc["row_absent_after"] is not True:
        print("RUN-BAD the identity row was not deleted after exp and read absent")
        return 1
    ident = doc["identity"]
    try:
        mt = item("opal-tickets", {"ticket_id": {"S": doc["mt_ticket"]}})
        if not mt or mt.get("ticket_type", {}).get("S") != "meeting_request":
            print("RUN-BAD the meeting ticket is missing or not a meeting_request")
            return 1
        meeting = mt.get("meeting", {}).get("M")
        coord = doc["coordinator_identity"]
        if (not meeting or meeting.get("status", {}).get("S") != "confirmed" or meeting.get("by", {}).get("S") != coord
                or meeting.get("time", {}).get("S") != doc["mt_confirmed_time"]):
            print("RUN-BAD the meeting ticket carries no confirmation by the recorded coordinator identity")
            return 1
        if mt.get("status", {}).get("S") == "completed":
            print("RUN-BAD the meeting ticket was completed; the outcome must not complete it")
            return 1
        for who in (ident, coord):
            row = item("opal-users-v2", {"PK": {"S": "USER#" + who}, "SK": {"S": "PROFILE"}})
            if row is not None:
                print("RUN-BAD an identity row is still PRESENT")
                return 1
        cfg = aws("lambda", "get-function-configuration", "--function-name", FUNCTION)
        matrix = json.loads(((cfg.get("Environment") or {}).get("Variables") or {}).get("ROUTING_MATRIX") or "{}")
        if (matrix.get("meeting_request") or {}).get("primary") != [COORDINATOR]:
            print("RUN-BAD the live meeting_request routing primary is not restored to exactly the coordinator")
            return 1
        if (doc["routing_during"].get("primary") if isinstance(doc["routing_during"], dict) else None) != [coord]:
            print("RUN-BAD the recorded routing window did not name the synthetic coordinator as the sole primary")
            return 1
        if (doc["routing_before"].get("primary") if isinstance(doc["routing_before"], dict) else None) != [COORDINATOR] \
                or (doc["routing_after"].get("primary") if isinstance(doc["routing_after"], dict) else None) != [COORDINATOR]:
            print("RUN-BAD the recorded routing before or after the window is not the coordinator alone")
            return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK (meeting only) meeting confirmed by the synthetic coordinator inside a routing window now restored; both identity rows absent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
