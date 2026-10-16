"""IRPT_ANLREQ FWD-1 synthetic staff user: mint and remove (0.9.0_WK_IRPT_ANLREQ~149, AR-y-345).

mint    reads ONE JSON object {"password": "..."} on STDIN (never argv, a file or the environment), hashes it with
        bcrypt at cost 12 and writes ONE users row with ConditionExpression attribute_not_exists(PK). Stdout carries
        only MINT-OK READBACK-OK (then one SCOPE line: the firm list and the absent markers, never the hash),
        MINT-OK READBACK-BAD or MINT-REFUSED <word>.
remove  deletes that row (attribute_exists(PK)), then polls a ConsistentRead get_item and the email-index GSI for up
        to 300 s and prints ABSENT/PRESENT GSI and CONSISTENT lines; exit 1 while either is still present.

Neither subcommand prints, logs or returns the password or the hash. boto3 and bcrypt are imported inside the
functions, so importing this module touches no AWS. Table, region, key shape, conditional write, removal and ABSENT
polling follow the release-29/30 sittings (org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r29 and
irpt_anlreq_r30); their constants are read there, not imported.
"""
from __future__ import annotations

import json
import sys
import time

REGION = "us-east-1"
TABLE = "opal-users-v2"
EMAIL = "fwd1-staff-r41b@opal.invalid"
PK = "USER#" + EMAIL
SK = "PROFILE"
FIRM = "opal-capital"
RUN_FIRM = "49financial"  # AR-y-373: the one firm the run files under; the row's allowedFirmIds list holds exactly this
TTL_HOURS = 3
COST = 12
MIN_PW = 24
MAX_PW = 72
REMOVE_WINDOW_S = 300
POLL_S = 10


def hash_password(pw):
    """bcrypt at cost 12 ($2b$12$ prefix). Returns str. Shared by mint and by hash_check.py; no AWS here."""
    import bcrypt  # local import: importing this module needs no bcrypt either

    if not isinstance(pw, str):
        raise ValueError("password is not a string")
    raw = pw.encode("utf-8")
    if not (MIN_PW <= len(raw) <= MAX_PW):
        raise ValueError("password length outside 24..72 bytes")
    return bcrypt.hashpw(raw, bcrypt.gensalt(COST)).decode("ascii")


def read_password():
    """The one JSON object on stdin; the caller never echoes what this returns."""
    obj = json.loads(sys.stdin.read())
    pw = obj.get("password") if isinstance(obj, dict) else None
    if not isinstance(pw, str):
        raise ValueError("stdin carries no password field")
    return pw


def item_for(hashed):
    return {
        "PK": {"S": PK},
        "SK": {"S": SK},
        "email": {"S": EMAIL},
        "passwordHash": {"S": hashed},
        "status": {"S": "active"},
        "firmId": {"S": FIRM},
        "allowedFirmIds": {"L": [{"S": RUN_FIRM}]},
        "role": {"S": "user"},
        "userType": {"S": "test-filer"},
        "name": {"S": "IRPT_ANLREQ FWD-1 synthetic staff"},
        "exp": {"N": str(int(time.time()) + TTL_HOURS * 3600)},
    }


def readback_ok(row):
    """Pure, no AWS. True only for the one-firm scope shape the FWD-1 ticket reader admits: status exactly active,
    firmId exactly opal-capital, a passwordHash present, allowedFirmIds exactly a DynamoDB list (L) of ONE string
    member RUN_FIRM, and none of mfaEnabled, mfaChannel or the global marker scope_all_firms present."""
    if not isinstance(row, dict):
        return False
    return (row.get("status") == {"S": "active"}
            and row.get("firmId") == {"S": FIRM}
            and "passwordHash" in row
            and row.get("allowedFirmIds") == {"L": [{"S": RUN_FIRM}]}
            and not any(k in row for k in ("mfaEnabled", "mfaChannel", "scope_all_firms")))


def cmd_mint():
    try:
        pw = read_password()
        hashed = hash_password(pw)
        pw = None
    except Exception as e:  # noqa: BLE001 -- the type name only; no message can carry the input
        print("MINT-REFUSED input " + type(e).__name__)
        return 1
    try:
        import boto3
        from botocore.exceptions import ClientError
    except Exception as e:  # noqa: BLE001
        print("MINT-REFUSED import " + type(e).__name__)
        return 1
    ddb = boto3.client("dynamodb", region_name=REGION)
    try:
        ddb.put_item(TableName=TABLE, Item=item_for(hashed), ConditionExpression="attribute_not_exists(PK)")
    except ClientError as e:
        print("MINT-REFUSED " + str(e.response.get("Error", {}).get("Code", "?")))
        return 1
    except Exception as e:  # noqa: BLE001
        print("MINT-REFUSED " + type(e).__name__)
        return 1
    key = {"PK": {"S": PK}, "SK": {"S": SK}}
    try:
        row = ddb.get_item(TableName=TABLE, Key=key, ConsistentRead=True).get("Item") or {}
    except Exception as e:  # noqa: BLE001
        print("MINT-OK READBACK-BAD read " + type(e).__name__)
        return 1
    if not readback_ok(row):
        print("MINT-OK READBACK-BAD shape")
        return 1
    print("MINT-OK READBACK-OK")
    members = [m.get("S", "?") for m in row["allowedFirmIds"]["L"]]
    print("SCOPE allowedFirmIds=" + ",".join(members)
          + " scope_all_firms=" + ("present" if "scope_all_firms" in row else "absent")
          + " mfa=" + ("present" if any(k in row for k in ("mfaEnabled", "mfaChannel")) else "absent"))
    return 0


def cmd_remove():
    try:
        import boto3
        from botocore.exceptions import ClientError
    except Exception as e:  # noqa: BLE001
        print("REMOVE-ERROR import " + type(e).__name__)
        return 1
    ddb = boto3.client("dynamodb", region_name=REGION)
    key = {"PK": {"S": PK}, "SK": {"S": SK}}
    try:
        ddb.delete_item(TableName=TABLE, Key=key, ConditionExpression="attribute_exists(PK)")
        print("REMOVE-OK deleted")
    except ClientError as e:
        code = str(e.response.get("Error", {}).get("Code", "?"))
        print("REMOVE-NOOP " + code if code == "ConditionalCheckFailedException" else "REMOVE-FAILED " + code)
    except Exception as e:  # noqa: BLE001
        print("REMOVE-FAILED " + type(e).__name__)
    try:
        deadline = time.time() + REMOVE_WINDOW_S
        while True:
            cons_absent = ddb.get_item(TableName=TABLE, Key=key, ConsistentRead=True).get("Item") is None
            gsi_count = ddb.query(TableName=TABLE, IndexName="email-index", KeyConditionExpression="email = :e",
                                  ExpressionAttributeValues={":e": {"S": EMAIL}}, Select="COUNT")["Count"]
            gsi_absent = gsi_count == 0
            if (cons_absent and gsi_absent) or time.time() >= deadline:
                break
            time.sleep(POLL_S)
    except Exception as e:  # noqa: BLE001
        print("REMOVE-ERROR poll " + type(e).__name__)
        return 1
    print(("ABSENT" if gsi_absent else "PRESENT") + " GSI " + EMAIL)
    print(("ABSENT" if cons_absent else "PRESENT") + " CONSISTENT " + EMAIL)
    return 0 if (gsi_absent and cons_absent) else 1


def main(argv):
    if len(argv) != 2 or argv[1] not in ("mint", "remove"):
        print("USAGE fwd1_mint.py mint|remove  (mint reads one JSON object on stdin)")
        return 2
    return cmd_mint() if argv[1] == "mint" else cmd_remove()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
