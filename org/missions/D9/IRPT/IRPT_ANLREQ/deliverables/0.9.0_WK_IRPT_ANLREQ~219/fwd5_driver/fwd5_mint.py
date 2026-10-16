"""IRPT_ANLREQ FWD-5 scoped cross-firm principal: mint and remove (0.9.0_WK_IRPT_ANLREQ~219, AR-ty-56).

mint    --email <addr> --firm <firm> --allowed-firm-ids <id1,id2,...>
        reads ONE JSON object {"password": "..."} on STDIN (never argv, a file or the environment), hashes it with
        bcrypt at cost 12 and writes ONE users row with ConditionExpression attribute_not_exists(PK). The row is the
        FWD-1 synthetic item with firmId set from --firm and one more attribute allowedFirmIds, written as a DynamoDB
        list of strings ({"L": [{"S": ...}, ...]}): infra/aws/lambda/ticket_center/lambda_function.py reads it as a
        Python list (_profile_scope), and a boto3 resource returns a set for an SS value, which that reader refuses.
        Stdout carries only MINT-OK READBACK-OK, MINT-OK READBACK-BAD <word>, MINT-REFUSED <word>, and after a
        READBACK-OK the scope line MINT-SCOPE allowedFirmIds=<ids> entitlement_rows=<n> (AR-tz-69): the ids are
        firm identifiers; the rows count the partition's items whose SK is not PROFILE and must be zero.
remove  --email <addr>
        deletes that row (attribute_exists(PK)), then polls a ConsistentRead get_item and the email-index GSI for up
        to 300 s and prints ABSENT/PRESENT GSI and CONSISTENT lines; exit 1 while either is still present.

The email must end in @opal.invalid and must not be the FWD-1 helper's address (fwd1-staff-r41b@opal.invalid); both
subcommands refuse it before any client is built. mint refuses a missing or empty --firm or --allowed-firm-ids with
MINT-REFUSED args and returns 1 before any AWS import. Neither subcommand prints, logs or returns the password or the
hash. boto3 and bcrypt are imported inside the functions, so importing this module touches no AWS and no bcrypt.
Region, table, key shape, conditional write, removal and ABSENT polling follow fwd1_mint.py (read, not imported).
"""
from __future__ import annotations

import json
import sys
import time

REGION = "us-east-1"
TABLE = "opal-users-v2"
FWD1_EMAIL = "fwd1-staff-r41b@opal.invalid"
EMAIL_SUFFIX = "@opal.invalid"
SK = "PROFILE"
TTL_HOURS = 3
COST = 12
MIN_PW = 24
MAX_PW = 72
REMOVE_WINDOW_S = 300
POLL_S = 10
MINT_FLAGS = ("--email", "--firm", "--allowed-firm-ids")


def hash_password(pw):
    """bcrypt at cost 12 ($2b$12$ prefix). Returns str. No AWS here."""
    import bcrypt  # local import: importing this module needs no bcrypt either

    if not isinstance(pw, str):
        raise ValueError("password is not a string")
    raw = pw.encode("utf-8")
    if not (MIN_PW <= len(raw) <= MAX_PW):
        raise ValueError("password length outside 24..72 bytes")
    return bcrypt.hashpw(raw, bcrypt.gensalt(COST)).decode("ascii")


def read_password(text=None):
    """The one JSON object on stdin (or the given text in tests); the caller never echoes what this returns."""
    raw = sys.stdin.read() if text is None else text
    obj = json.loads(raw)
    pw = obj.get("password") if isinstance(obj, dict) else None
    if not isinstance(pw, str):
        raise ValueError("stdin carries no password field")
    return pw


def valid_email(email):
    """A non-empty local part, no whitespace or comma, the suffix @opal.invalid, and not the FWD-1 address.
    The checks run on the lower-cased form so a case variant of the FWD-1 address is refused too."""
    if not isinstance(email, str) or any(c.isspace() or c == "," for c in email):
        return False
    low = email.lower()
    if not low.endswith(EMAIL_SUFFIX) or len(low) == len(EMAIL_SUFFIX):
        return False
    return low != FWD1_EMAIL


def parse_ids(text):
    """'a,b,c' -> ['a', 'b', 'c']. An empty list, an empty item or an item with whitespace is None (refused)."""
    if not isinstance(text, str):
        return None
    parts = [p.strip() for p in text.split(",")]
    if any((not p) or any(c.isspace() for c in p) for p in parts):
        return None
    return parts


def parse_mint_args(args):
    """{'email', 'firm', 'ids'} for a well-formed mint command line, else None. Each flag appears once, with a value."""
    opts = {}
    i = 0
    while i < len(args):
        flag = args[i]
        if flag not in MINT_FLAGS or i + 1 >= len(args) or flag in opts:
            return None
        opts[flag] = args[i + 1]
        i += 2
    if set(opts) != set(MINT_FLAGS):
        return None
    email = opts["--email"]
    firm = opts["--firm"]
    ids = parse_ids(opts["--allowed-firm-ids"])
    if not valid_email(email) or not firm or any(c.isspace() for c in firm) or ids is None:
        return None
    return {"email": email, "firm": firm, "ids": ids}


def parse_remove_args(args):
    """The email for a well-formed remove command line, else None."""
    if len(args) != 2 or args[0] != "--email" or not valid_email(args[1]):
        return None
    return args[1]


def item_for(email, firm, ids, hashed):
    """The FWD-1 item with firmId from the parameter, the key and email from --email, and allowedFirmIds as an L."""
    return {
        "PK": {"S": "USER#" + email},
        "SK": {"S": SK},
        "email": {"S": email},
        "passwordHash": {"S": hashed},
        "status": {"S": "active"},
        "firmId": {"S": firm},
        "role": {"S": "user"},
        "userType": {"S": "test-filer"},
        "name": {"S": "IRPT_ANLREQ FWD-5 synthetic cross-firm principal"},
        "exp": {"N": str(int(time.time()) + TTL_HOURS * 3600)},
        "allowedFirmIds": {"L": [{"S": i} for i in ids]},
    }


def ids_of_attr(attr):
    """The Python list of ids a raw DynamoDB L of S attribute holds, or None when absent or of another shape."""
    if not isinstance(attr, dict) or set(attr) != {"L"} or not isinstance(attr["L"], list):
        return None
    out = []
    for el in attr["L"]:
        if not (isinstance(el, dict) and set(el) == {"S"} and isinstance(el["S"], str)):
            return None
        out.append(el["S"])
    return out


def readback_ok(row, firm, ids):
    """READBACK-OK needs allowedFirmIds PRESENT and equal to the ids given; absent is BAD, never 'no scope'."""
    got = ids_of_attr(row.get("allowedFirmIds"))
    return bool(row.get("status", {}).get("S") == "active"
                and row.get("firmId", {}).get("S") == firm
                and "passwordHash" in row
                and not any(k in row for k in ("mfaEnabled", "mfaChannel"))
                and got is not None and got == ids)


def entitlement_rows(resp):
    """Items under the principal's PK whose SK is not PROFILE; a response with no Items key holds none. The query
    projects SK, so every returned item carries it; an item with no SK string is counted, never waved through."""
    items = resp.get("Items") or []
    return sum(1 for it in items if (it.get("SK") or {}).get("S") != SK)


def _refused_word(e):
    resp = getattr(e, "response", None)
    if isinstance(resp, dict):
        return str((resp.get("Error") or {}).get("Code", "?"))
    return type(e).__name__


def cmd_mint(args, stdin_text=None, ddb=None, hasher=None):
    parsed = parse_mint_args(args)
    if parsed is None:
        print("MINT-REFUSED args")
        return 1
    try:
        pw = read_password(stdin_text)
        hashed = (hasher or hash_password)(pw)
        pw = None
    except Exception as e:  # noqa: BLE001 -- the type name only; no message can carry the input
        print("MINT-REFUSED input " + type(e).__name__)
        return 1
    if ddb is None:
        try:
            import boto3
        except Exception as e:  # noqa: BLE001
            print("MINT-REFUSED import " + type(e).__name__)
            return 1
        ddb = boto3.client("dynamodb", region_name=REGION)
    item = item_for(parsed["email"], parsed["firm"], parsed["ids"], hashed)
    try:
        ddb.put_item(TableName=TABLE, Item=item, ConditionExpression="attribute_not_exists(PK)")
    except Exception as e:  # noqa: BLE001
        print("MINT-REFUSED " + _refused_word(e))
        return 1
    key = {"PK": item["PK"], "SK": {"S": SK}}
    try:
        row = ddb.get_item(TableName=TABLE, Key=key, ConsistentRead=True).get("Item") or {}
    except Exception as e:  # noqa: BLE001
        print("MINT-OK READBACK-BAD read " + type(e).__name__)
        return 1
    if not readback_ok(row, parsed["firm"], parsed["ids"]):
        print("MINT-OK READBACK-BAD shape")
        return 1
    try:
        rows = entitlement_rows(ddb.query(TableName=TABLE, KeyConditionExpression="PK = :p",
                                          ExpressionAttributeValues={":p": {"S": "USER#" + parsed["email"]}},
                                          ConsistentRead=True, ProjectionExpression="SK"))
    except Exception as e:  # noqa: BLE001
        print("MINT-OK READBACK-BAD query " + type(e).__name__)
        return 1
    scope = ("MINT-SCOPE allowedFirmIds=" + ",".join(parsed["ids"]) + " entitlement_rows=" + str(rows))
    if rows:
        print("MINT-OK READBACK-BAD entitlement")
        print(scope)
        return 1
    print("MINT-OK READBACK-OK")
    print(scope)
    return 0


def cmd_remove(args, ddb=None):
    email = parse_remove_args(args)
    if email is None:
        print("REMOVE-REFUSED args")
        return 1
    if ddb is None:
        try:
            import boto3
        except Exception as e:  # noqa: BLE001
            print("REMOVE-ERROR import " + type(e).__name__)
            return 1
        ddb = boto3.client("dynamodb", region_name=REGION)
    pk = "USER#" + email
    key = {"PK": {"S": pk}, "SK": {"S": SK}}
    try:
        ddb.delete_item(TableName=TABLE, Key=key, ConditionExpression="attribute_exists(PK)")
        print("REMOVE-OK deleted")
    except Exception as e:  # noqa: BLE001
        code = _refused_word(e)
        print("REMOVE-NOOP " + code if code == "ConditionalCheckFailedException" else "REMOVE-FAILED " + code)
    try:
        deadline = time.time() + REMOVE_WINDOW_S
        while True:
            cons_absent = ddb.get_item(TableName=TABLE, Key=key, ConsistentRead=True).get("Item") is None
            gsi_count = ddb.query(TableName=TABLE, IndexName="email-index", KeyConditionExpression="email = :e",
                                  ExpressionAttributeValues={":e": {"S": email}}, Select="COUNT")["Count"]
            gsi_absent = gsi_count == 0
            if (cons_absent and gsi_absent) or time.time() >= deadline:
                break
            time.sleep(POLL_S)
    except Exception as e:  # noqa: BLE001
        print("REMOVE-ERROR poll " + type(e).__name__)
        return 1
    print(("ABSENT" if gsi_absent else "PRESENT") + " GSI " + email)
    print(("ABSENT" if cons_absent else "PRESENT") + " CONSISTENT " + email)
    return 0 if (gsi_absent and cons_absent) else 1


def main(argv):
    if len(argv) < 2 or argv[1] not in ("mint", "remove"):
        print("USAGE fwd5_mint.py mint --email A --firm F --allowed-firm-ids I1,I2 | remove --email A "
              "(mint reads one JSON object on stdin)")
        return 2
    return cmd_mint(argv[2:]) if argv[1] == "mint" else cmd_remove(argv[2:])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
