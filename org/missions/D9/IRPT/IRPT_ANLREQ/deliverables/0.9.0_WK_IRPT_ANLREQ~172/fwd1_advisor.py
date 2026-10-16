"""IRPT_ANLREQ FWD-1 window 5: mint and remove ONE synthetic partner advisor at 49financial (0.9.0_WK_IRPT_ANLREQ~172, AR-y-380).

mint    --date YYYYMMDD  Read-only pre-state first: the users row ABSENT (ConsistentRead), the email-index count 0, the
                         partner row ABSENT. Any other state prints ADVISOR-MINT-REFUSED prestate <what> and writes nothing.
                         Then ONE users row (attribute_not_exists(PK)), read back; then ONE partner row
                         (attribute_not_exists(email)), read back. Prints ADVISOR-MINT-OK <address> and
                         ADVISOR-READBACK-OK users partner. No password and no hash is written, read or printed.
remove  --date YYYYMMDD  Deletes the users row (attribute_exists(PK)) and the partner row (attribute_exists(email)), then
                         polls a ConsistentRead and the email-index GSI for up to 300 s and prints ABSENT or PRESENT lines
                         for GSI, CONSISTENT and PARTNER. Exit 1 while any row or index entry is still present.

The door (_advisor_owner in infra/aws/lambda/investor-reporting/_authz/served.py) admits an on-behalf upload only when the
partner row and an active users row for the advisor exist at the firm. The users row carries allowedFirmIds as the explicit
one-firm list, so the advisor reaches 49financial and nothing wider.

CONSTANTS ARE READ, NOT IMPORTED. Each is cited beside its value to the file and line it was read from:
  sitting_r33.py = org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r33/sitting_r33.py
  sitting_r28.py = org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/sitting_r28.py (reused by sitting_r33.py:29-30)
boto3 is imported only inside real_clients(), which only main() calls. Importing this module touches no AWS.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import time

# Address shape: the order cell (release-33 advisors were irpt-r33-<k>-<date>@opal.invalid, sitting_r33.py:169-171).
ADDRESS = "irpt-w5-advisor-%s@opal.invalid"
# The one firm: the order cell (release-33 advisors A and B used 49financial, sitting_r33.py:169-170).
FIRM = "49financial"
# Region: sitting_r28.py:32 (REGION = "us-east-1"), reached through sitting_r33.py:30 (base.REGION).
REGION = "us-east-1"
# Users table: sitting_r28.py:34 (USERS = "opal-users-v2"), reached through sitting_r33.py:194-201 (base.USERS).
USERS = "opal-users-v2"
# Partner table: sitting_r33.py:190-191 (ptable(k) = "opal-partner-" + firm).
PARTNER_PREFIX = "opal-partner-"
# Email index name: sitting_r33.py:200 (IndexName="email-index").
EMAIL_INDEX = "email-index"
# Users key shape: sitting_r33.py:184-185 (PK "USER#" + address, SK "PROFILE").
USER_PK_PREFIX = "USER#"
SK_VALUE = "PROFILE"
# Partner key shape: sitting_r33.py:187-188 (the partner table key is the email attribute alone).
PARTNER_KEY_ATTR = "email"
# Attribute values: sitting_r33.py:284-285 (tier advisor, role user) and sitting_r33.py:301-302 (advisorRole viewer, firmRole user).
TIER = "advisor"
ROLE = "user"
ADVISOR_ROLE = "viewer"
FIRM_ROLE = "user"
# Display name: the order cell. Release-33 used "IRPT_ANLREQ R33 synthetic advisor A" (sitting_r33.py:283), same shape.
NAME = "IRPT_ANLREQ FWD-1 synthetic advisor"
# Provenance stamp: the order cell says 0.7.0_AE_CloudOps~IB2. Release-33 wrote 0.7.0_AE_CloudOps~AQ2 (sitting_r33.py:286, 302);
# the order's value is used and the difference is filed as a surprise row.
CREATED_BY = "0.7.0_AE_CloudOps~IB2"
# TTL: the order cell (exp = now + 3 hours). The same 3-hour TTL is TTL_HOURS in fwd1_mint.py:28.
TTL_HOURS = 3
# Removal poll: 300 s deadline (sitting_r33.py:423) and a 10 s sleep between reads (sitting_r33.py:432).
REMOVE_WINDOW_S = 300
POLL_S = 10

DATE_RE = re.compile(r"[0-9]{8}")
CREDENTIAL_KEYS = ("passwordHash", "password", "hash")
ERR_CONDITION = "ConditionalCheckFailedException"


def parse_date(value):
    """The date is eight digits and a real calendar date. Anything else raises ValueError."""
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        raise ValueError("date must be eight digits YYYYMMDD")
    try:
        dt.datetime.strptime(value, "%Y%m%d")
    except ValueError:
        raise ValueError("date is not a calendar date") from None
    return value


def address_for(date):
    return ADDRESS % parse_date(date)


def advisor_key(date):
    return "irpt-w5-adv-" + parse_date(date)


def partner_table():
    return PARTNER_PREFIX + FIRM


def user_key(addr):
    return {"PK": {"S": USER_PK_PREFIX + addr}, "SK": {"S": SK_VALUE}}


def partner_key(addr):
    return {PARTNER_KEY_ATTR: {"S": addr}}


def iso(now):
    return dt.datetime.fromtimestamp(int(now), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def user_item(addr, now):
    """The users row: exactly thirteen attributes. allowedFirmIds is the explicit list of the one firm."""
    return {
        "PK": {"S": USER_PK_PREFIX + addr},
        "SK": {"S": SK_VALUE},
        "email": {"S": addr},
        "firmId": {"S": FIRM},
        "status": {"S": "active"},
        "name": {"S": NAME},
        "role": {"S": ROLE},
        "tier": {"S": TIER},
        "allowedFirmIds": {"L": [{"S": FIRM}]},
        "createdAt": {"S": iso(now)},
        "createdBy": {"S": CREATED_BY},
        "updatedAt": {"S": iso(now)},
        "exp": {"N": str(int(now) + TTL_HOURS * 3600)},
    }


def partner_item(addr, date, now):
    """The partner row: exactly eight attributes. No password and no hash."""
    return {
        "email": {"S": addr},
        "advisorKey": {"S": advisor_key(date)},
        "advisorName": {"S": NAME},
        "advisorRole": {"S": ADVISOR_ROLE},
        "firmRole": {"S": FIRM_ROLE},
        "createdAt": {"S": iso(now)},
        "createdBy": {"S": CREATED_BY},
        "updatedAt": {"S": iso(now)},
    }


def user_readback_ok(row, addr):
    """Pure. True only for the one-firm advisor row exactly as written: active, tier advisor, firmId 49financial,
    allowedFirmIds the explicit one-element list, and no credential key."""
    if not isinstance(row, dict):
        return False
    return (row.get("email") == {"S": addr}
            and row.get("status") == {"S": "active"}
            and row.get("firmId") == {"S": FIRM}
            and row.get("tier") == {"S": TIER}
            and row.get("role") == {"S": ROLE}
            and row.get("allowedFirmIds") == {"L": [{"S": FIRM}]}
            and not any(k in row for k in CREDENTIAL_KEYS))


def partner_readback_ok(row, addr, date):
    """Pure. True only for the partner row as written, with no credential key."""
    if not isinstance(row, dict):
        return False
    return (row.get(PARTNER_KEY_ATTR) == {"S": addr}
            and row.get("advisorKey") == {"S": advisor_key(date)}
            and row.get("advisorRole") == {"S": ADVISOR_ROLE}
            and row.get("firmRole") == {"S": FIRM_ROLE}
            and not any(k in row for k in CREDENTIAL_KEYS))


def prestate_problem(users_row, gsi_count, partner_row):
    """Pure. None when every row is ABSENT and the index holds nothing for the address; else what is present."""
    if users_row is not None:
        return "users-row-present"
    if gsi_count != 0:
        return "email-index-count=%s" % gsi_count
    if partner_row is not None:
        return "partner-row-present"
    return None


def error_code(exc):
    resp = getattr(exc, "response", None)
    if isinstance(resp, dict):
        return str((resp.get("Error") or {}).get("Code", "?"))
    return type(exc).__name__


def read_item(ddb, table, key):
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def email_count(ddb, addr):
    return ddb.query(TableName=USERS, IndexName=EMAIL_INDEX, KeyConditionExpression="email = :e",
                     ExpressionAttributeValues={":e": {"S": addr}}, Select="COUNT")["Count"]


def mint(ddb, date, now):
    """Returns (rc, output lines). Writes only after the read-only pre-state is ABSENT; never prints a credential."""
    addr = address_for(date)
    wrote_users = False
    try:
        problem = prestate_problem(read_item(ddb, USERS, user_key(addr)), email_count(ddb, addr),
                                   read_item(ddb, partner_table(), partner_key(addr)))
        if problem:
            return 1, ["ADVISOR-MINT-REFUSED prestate " + problem]
        ddb.put_item(TableName=USERS, Item=user_item(addr, now), ConditionExpression="attribute_not_exists(PK)")
        wrote_users = True
        back = read_item(ddb, USERS, user_key(addr))
        if not user_readback_ok(back, addr):
            return 1, ["ADVISOR-READBACK-BAD users (the users row is written; run remove)"]
        ddb.put_item(TableName=partner_table(), Item=partner_item(addr, date, now),
                     ConditionExpression="attribute_not_exists(email)")
        back_p = read_item(ddb, partner_table(), partner_key(addr))
        if not partner_readback_ok(back_p, addr, date):
            return 1, ["ADVISOR-READBACK-BAD partner (both rows are written; run remove)"]
    except Exception as exc:  # noqa: BLE001 -- the error code only; no item and no value is echoed
        tail = " (the users row is written; run remove)" if wrote_users else ""
        return 1, ["ADVISOR-MINT-REFUSED error " + error_code(exc) + tail]
    return 0, ["ADVISOR-MINT-OK " + addr, "ADVISOR-READBACK-OK users partner"]


def remove(ddb, date, clock=time.time, sleep=time.sleep):
    """Returns (rc, output lines). rc 1 while any of the three is still present at the deadline."""
    addr = address_for(date)
    lines = []
    deletes = (("users", USERS, user_key(addr), "attribute_exists(PK)"),
               ("partner", partner_table(), partner_key(addr), "attribute_exists(email)"))
    for label, table, key, cond in deletes:
        try:
            ddb.delete_item(TableName=table, Key=key, ConditionExpression=cond)
            lines.append("REMOVE-OK " + label)
        except Exception as exc:  # noqa: BLE001
            code = error_code(exc)
            lines.append(("REMOVE-NOOP " + label) if code == ERR_CONDITION else ("REMOVE-FAILED %s %s" % (label, code)))
    try:
        deadline = clock() + REMOVE_WINDOW_S
        while True:
            cons_absent = read_item(ddb, USERS, user_key(addr)) is None
            gsi_absent = email_count(ddb, addr) == 0
            partner_absent = read_item(ddb, partner_table(), partner_key(addr)) is None
            if (cons_absent and gsi_absent and partner_absent) or clock() >= deadline:
                break
            sleep(POLL_S)
    except Exception as exc:  # noqa: BLE001
        return 1, lines + ["REMOVE-ERROR poll " + error_code(exc)]
    lines.append(("ABSENT" if gsi_absent else "PRESENT") + " GSI " + addr)
    lines.append(("ABSENT" if cons_absent else "PRESENT") + " CONSISTENT " + addr)
    lines.append(("ABSENT" if partner_absent else "PRESENT") + " PARTNER " + addr)
    rc = 0 if (cons_absent and gsi_absent and partner_absent) else 1
    return rc, lines


def real_clients():
    """The only AWS import. Called by main() and by nothing else."""
    import boto3  # noqa: PLC0415 -- deliberately local
    return boto3.client("dynamodb", region_name=REGION)


def main(argv):
    ap = argparse.ArgumentParser(prog="fwd1_advisor.py")
    ap.add_argument("command", choices=("mint", "remove"))
    ap.add_argument("--date", required=True)
    args = ap.parse_args(argv)
    try:
        parse_date(args.date)
    except ValueError as exc:
        print("ADVISOR-REFUSED " + str(exc))
        return 2
    try:
        ddb = real_clients()
    except ImportError as exc:
        print("ADVISOR-REFUSED import " + type(exc).__name__)
        return 1
    if args.command == "mint":
        rc, lines = mint(ddb, args.date, int(time.time()))
    else:
        rc, lines = remove(ddb, args.date)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
