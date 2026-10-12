"""count_internal_callers.py -- a READ-ONLY census for IRPT_ANLREQ round 17, workstream Y, cell AR-y-173.

Part (a): one SCAN of the users table (opal-users-v2), PROFILE rows only. An INTERNAL row is one whose firmId is
'opal-capital' or whose userType is 'Dev' or 'service'. Counted by firmId, userType and status (the status string as it
is, 'absent' when the attribute is missing), and the number of rows whose status is exactly 'active'.
Part (b): NOT_AVAILABLE. The investor-reporting request log lines do not carry the caller's identity (LOG_EVIDENCE), so no
count of distinct internal callers can be read from them. The script says so and prints no number for it, never a zero.

The only AWS call in this file is dynamodb scan, a read. Nothing here changes state anywhere.

Live use (a seat that holds the read):
  python count_internal_callers.py --region <R> [--table opal-users-v2] [--out <file>]
Offline proof (no AWS, no network, no boto3 client):
  python count_internal_callers.py --self-test

Exit: 0 counted; 2 usage; 3 the scan failed (its error code is printed on stderr and nothing is counted).
The LAST stdout line is ONE JSON object of counts. It carries no address, name, id, account or raw attribute value: the
firmId, userType and status buckets are the table's own short letter tokens, and any other value is bucketed as
'other-string'. An unreadable row (a malformed attribute or a non-dict item) is counted as unreadable and is never
counted as active or as an internal caller.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

CELL = "AR-y-173"
TABLE = "opal-users-v2"
PROFILE_SK = "PROFILE"
INTERNAL_FIRM = "opal-capital"
INTERNAL_TYPES = ("Dev", "service")
ACTIVE = "active"
TOKEN = re.compile(r"[A-Za-z][A-Za-z_-]{0,23}\Z")
KINDS = ("S", "N", "BOOL", "NULL", "M", "L", "SS", "NS", "BS", "B")
LOG_EVIDENCE = (
    "infra/aws/lambda/investor-reporting/_authz/served.py:81-86 (_internal_sink prints the internal record: "
    "correlation_id, operation, exception_type, exception_text, component, reason, developer_detail, extra)",
    "infra/aws/lambda/investor-reporting/_authz/served.py:89-108 (_record prints the public line)",
    "infra/aws/lambda/investor-reporting/_authz/errors.py:146-167 (public_line writes event, operation, "
    "public_reason_code and correlation_id only)",
    "infra/aws/lambda/investor-reporting/_scope/ has no print or log call that writes a caller's email, firmId or userType",
)
PART_B_REASON = ("the request log lines carry a correlation id and an operation, not the caller's identity (no email, firmId "
                 "or userType is written); a count of distinct internal callers cannot be made from them, so no part (b) "
                 "number is printed")


class ScanFailed(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def safe_code(exc):
    """The error's code, restricted to a short token (an AWS error code, or the exception class name)."""
    response = getattr(exc, "response", None)
    code = response.get("Error", {}).get("Code") if isinstance(response, dict) else None
    code = code or type(exc).__name__
    return re.sub(r"[^A-Za-z0-9_.:-]", "_", str(code))[:48] or "ERROR"


def scan_profiles(ddb, table):
    """Every PROFILE row of the table, read by SCAN pages. Returns (rows, items_scanned). Raises ScanFailed."""
    rows, scanned, start = [], 0, None
    while True:
        args = {"TableName": table, "ConsistentRead": True,
                "FilterExpression": "#sk = :p", "ExpressionAttributeNames": {"#sk": "SK", "#f": "firmId",
                                                                              "#u": "userType", "#s": "status"},
                "ExpressionAttributeValues": {":p": {"S": PROFILE_SK}},
                "ProjectionExpression": "#f, #u, #s"}
        if start:
            args["ExclusiveStartKey"] = start
        try:
            got = ddb.scan(**args)
        except Exception as exc:
            raise ScanFailed(safe_code(exc)) from None
        if not isinstance(got, dict) or not isinstance(got.get("Items"), list) or not isinstance(got.get("ScannedCount"), int):
            raise ScanFailed("SCAN_REPLY_SHAPE")
        scanned += got["ScannedCount"]
        rows.extend(got["Items"])
        start = got.get("LastEvaluatedKey")
        if not start:
            return rows, scanned


def typed_text(attr):
    """(kind, text). kind is 'absent', 'S' (text is the string), 'OTHER' (a non-string type) or 'MALFORMED'."""
    if attr is None:
        return "absent", None
    if not isinstance(attr, dict) or len(attr) != 1:
        return "MALFORMED", None
    (kind, inner), = attr.items()
    if kind not in KINDS:
        return "MALFORMED", None
    if kind == "S" and isinstance(inner, str):
        return "S", inner
    return "OTHER", None


def bucket(kind, text):
    """The printed bucket of one field: the table's own token, or a word that names its kind. Never a raw value."""
    if kind == "absent":
        return "absent"
    if kind == "S":
        return text if TOKEN.match(text) else "other-string"
    return "non-string"


def census(rows, scanned):
    internal, by_key, external, unreadable, active = 0, {}, 0, 0, 0
    for row in rows:
        if not isinstance(row, dict):
            unreadable += 1
            continue
        parts = {name: typed_text(row.get(name)) for name in ("firmId", "userType", "status")}
        if any(kind == "MALFORMED" for kind, _ in parts.values()):
            unreadable += 1
            continue
        firm_kind, firm = parts["firmId"]
        type_kind, user_type = parts["userType"]
        status_kind, status = parts["status"]
        is_internal = (firm_kind == "S" and firm == INTERNAL_FIRM) or (type_kind == "S" and user_type in INTERNAL_TYPES)
        if not is_internal:
            external += 1
            continue
        internal += 1
        key = (bucket(firm_kind, firm), bucket(type_kind, user_type), bucket(status_kind, status))
        by_key[key] = by_key.get(key, 0) + 1
        if status_kind == "S" and status == ACTIVE:
            active += 1
    cross = [{"firmId": k[0], "userType": k[1], "status": k[2], "rows": n} for k, n in sorted(by_key.items())]
    return {"table": TABLE, "items_scanned": scanned, "profile_rows": len(rows), "internal_rows": internal,
            "internal_active": active, "internal_by_firmId_userType_status": cross, "external_rows": external,
            "unreadable_rows": unreadable, "denominator_check": internal + external + unreadable == len(rows)}


def part_b():
    """Part (b) reads the logs only if they carry the caller. They do not (LOG_EVIDENCE), so it is not run."""
    return {"part_b": "NOT_AVAILABLE", "reason": PART_B_REASON, "evidence": list(LOG_EVIDENCE)}


def run(ddb, table=TABLE):
    """(rc, out, code). Shared by the live path and the self-test; the one JSON object is out, code names a failed scan."""
    try:
        rows, scanned = scan_profiles(ddb, table)
    except ScanFailed as exc:
        return 3, None, exc.code
    return 0, {"cell": CELL, "part_a": census(rows, scanned), "part_b": part_b()}, None


# ----------------------------------------------------------------------------------------------------------------------
# the offline proof: in-memory fakes holding SYNTHETIC rows (no boto3 client is created here)
# ----------------------------------------------------------------------------------------------------------------------

class FakeClientError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.response = {"Error": {"Code": code}}


class FakeDdb:
    PAGE = 4

    def __init__(self, rows):
        self.rows, self.deny, self.bad_reply, self.log = rows, False, False, {}

    def scan(self, **args):
        self.log["scan"] = self.log.get("scan", 0) + 1
        if self.deny:
            raise FakeClientError("AccessDeniedException")
        if args.get("ProjectionExpression") is None or args.get("ConsistentRead") is not True:
            raise FakeClientError("ValidationException")
        begin = args.get("ExclusiveStartKey", {}).get("n", 0) if args.get("ExclusiveStartKey") else 0
        page = self.rows[begin:begin + self.PAGE]
        keep = ("firmId", "userType", "status")
        items = []
        for row in page:
            if row.get("SK", {}).get("S") == args["ExpressionAttributeValues"][":p"]["S"]:
                items.append({k: v for k, v in row.items() if k in keep})
        got = {"Items": items}
        if not self.bad_reply:
            got["ScannedCount"] = len(page)
        if begin + self.PAGE < len(self.rows):
            got["LastEvaluatedKey"] = {"n": begin + self.PAGE}
        return got


def fake_row(sk="PROFILE", firm=None, user_type=None, status="absent", email="person.one@example.test"):
    row = {"PK": {"S": "USER#" + email}, "SK": {"S": sk}, "email": {"S": email}}
    if firm is not None:
        row["firmId"] = {"S": firm}
    if user_type is not None:
        row["userType"] = {"S": user_type}
    if status == "absent":
        pass
    elif isinstance(status, dict):
        row["status"] = status
    else:
        row["status"] = {"S": status}
    return row


def synthetic_rows():
    """Nine rows: eight PROFILE, one ROLE row (not a user row), one malformed status. Each shape is named."""
    return [
        fake_row(firm="opal-capital", user_type="Dev", status="active"),          # internal, active
        fake_row(firm="opal-capital", user_type="Dev", status="disabled"),        # internal, disabled
        fake_row(firm="inflection", user_type="service", status="absent"),        # internal (service), no status
        fake_row(firm="opal-capital", user_type="Dev", status="Active"),          # internal, wrong case
        fake_row(firm="opal-capital", user_type="Dev", status="ACTIVE"),          # internal, wrong case
        fake_row(firm="opal-capital", user_type="Dev", status={"N": "1"}),        # internal, wrong type
        fake_row(firm="inflection", user_type="client", status="active"),         # external
        fake_row(sk="ROLE#x", firm="opal-capital", user_type="Dev", status="active"),  # not a PROFILE row
        fake_row(firm="opal-capital", user_type="Dev", status={"S": "active", "N": "1"}),  # malformed: unreadable
    ]


EXPECTED_KEYS = [
    {"firmId": "inflection", "userType": "service", "status": "absent", "rows": 1},
    {"firmId": "opal-capital", "userType": "Dev", "status": "ACTIVE", "rows": 1},
    {"firmId": "opal-capital", "userType": "Dev", "status": "Active", "rows": 1},
    {"firmId": "opal-capital", "userType": "Dev", "status": "active", "rows": 1},
    {"firmId": "opal-capital", "userType": "Dev", "status": "disabled", "rows": 1},
    {"firmId": "opal-capital", "userType": "Dev", "status": "non-string", "rows": 1},
]


def self_test():
    problems = []
    ddb = FakeDdb(synthetic_rows())
    rc, out, code = run(ddb, TABLE)
    if rc != 0 or out is None:
        problems.append("the synthetic census did not count (rc=%s code=%s)" % (rc, code))
    else:
        a = out["part_a"]
        want = {"items_scanned": 9, "profile_rows": 8, "internal_rows": 6, "internal_active": 1, "external_rows": 1,
                "unreadable_rows": 1, "denominator_check": True}
        for key, value in want.items():
            if a.get(key) != value:
                problems.append("%s: expected %r got %r" % (key, value, a.get(key)))
        if a.get("internal_by_firmId_userType_status") != EXPECTED_KEYS:
            problems.append("the status buckets differ: %r" % a.get("internal_by_firmId_userType_status"))
        if out["part_b"].get("part_b") != "NOT_AVAILABLE" or not out["part_b"].get("reason"):
            problems.append("part (b) is not NOT_AVAILABLE with a reason")
        text = json.dumps(out["part_a"], sort_keys=True)
        for banned in ("@", "person", "example", "USER#", "ROLE#"):
            if banned in text:
                problems.append("the output carries %r" % banned)
        if set(ddb.log) != {"scan"}:
            problems.append("a call other than scan reached the fake: %r" % sorted(ddb.log))
    denied = FakeDdb(synthetic_rows())
    denied.deny = True
    rc, out, code = run(denied, TABLE)
    if rc != 3 or out is not None or code != "AccessDeniedException":
        problems.append("a denied scan was not reported as its code and exit 3 (rc=%s code=%s)" % (rc, code))
    shaped = FakeDdb(synthetic_rows())
    shaped.bad_reply = True
    rc, out, code = run(shaped, TABLE)
    if rc != 3 or code != "SCAN_REPLY_SHAPE":
        problems.append("a reply without ScannedCount was counted (rc=%s code=%s)" % (rc, code))
    if census([], 0)["internal_active"] != 0 or census([{"firmId": {"S": "opal-capital"}}], 1)["internal_active"] != 0:
        problems.append("a row with no status was counted as active")
    for line in problems:
        print("SELF-TEST FAIL: " + line, file=sys.stderr)
    if problems:
        return 1
    print("self-test: 9 synthetic rows (8 PROFILE), 6 status shapes, scan pages %d, denied scan -> AccessDeniedException, "
          "reply shape -> SCAN_REPLY_SHAPE" % ddb.log.get("scan", 0), file=sys.stderr)
    print("CENSUS-SELFTEST-OK")
    return 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--region")
    parser.add_argument("--table", default=TABLE)
    parser.add_argument("--out", help="also write the one JSON object to this file")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.region:
        parser.error("--region is required for a live run")
    print("part_b: NOT_AVAILABLE -- " + PART_B_REASON, file=sys.stderr)
    import boto3  # only a live run needs it
    ddb = boto3.client("dynamodb", region_name=args.region)
    rc, out, code = run(ddb, args.table)
    if rc != 0:
        print("SCAN_FAILED %s" % code, file=sys.stderr)
        return rc
    line = json.dumps(out, sort_keys=True)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(line + "\n")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
