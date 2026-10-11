"""Y5 after-reads helpers. READ-ONLY: scan, get_item, lambda invoke of irpt-status. ASCII only.
Prints ids, keys, counts and codes only; never an email, link, name or document body."""
import json
import re

import boto3

FN = "irpt-status"
RB = "GET /api/scoped/investor-reporting/analysis/"
R_SECTIONS = RB + "{jobId}/sections"
R_HISTORY = RB + "requests"
R_JOB = "GET /api/scoped/investor-reporting/status/{jobId}"
lam = boto3.client("lambda", region_name="us-east-1")
ddb = boto3.client("dynamodb", region_name="us-east-1")
SK = re.compile(r"^analysis#(REQ-[0-9a-f]{24})#1$")


def config():
    c = lam.get_function_configuration(FunctionName=FN)
    return {"code_sha256": c["CodeSha256"], "last_modified": c["LastModified"]}


def requests_all():
    """Every analysis#REQ-<24hex>#1 record in irpt-requests, all pages, consistent read."""
    out, pages, items = [], 0, 0
    for pg in ddb.get_paginator("scan").paginate(TableName="irpt-requests", ConsistentRead=True):
        pages += 1
        for it in pg.get("Items", []):
            items += 1
            m = SK.match(it.get("request_revision", {}).get("S", ""))
            if m and "record" in it:
                out.append((it["tenant"]["S"], m.group(1), json.loads(it["record"]["S"])))
    return out, {"items_scanned": items, "pages": pages}


_ROLE = {}


def _roles():
    if not _ROLE:
        for pg in ddb.get_paginator("scan").paginate(TableName="opal-users-v2", ProjectionExpression="#sk,email,#r",
                                                      ExpressionAttributeNames={"#sk": "SK", "#r": "role"}):
            for it in pg.get("Items", []):
                if it.get("SK", {}).get("S") == "PROFILE" and it.get("role", {}).get("S"):
                    _ROLE[it["email"]["S"].lower()] = it["role"]["S"].lower()
    return _ROLE


def owner_headers(rec):
    o = rec["owner"]
    role = _roles().get(o["principal_id"].lower(), "user")
    return {"X-Contract-Version": "v1", "x-origin-verify": "cloudfront", "x-user-email": o["principal_id"],
            "x-firm-id": o["home_firm_id"], "x-user-name": "owner", "x-user-role": role}


def invoke(route, headers, path=None, query=None):
    ev = {"routeKey": route, "headers": headers}
    if path:
        ev["pathParameters"] = path
    if query:
        ev["queryStringParameters"] = query
    r = lam.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())
    return json.loads(r["Payload"].read().decode())


def code(b):
    return (b.get("status") or {}).get("public_reason_code") if isinstance(b, dict) else None


def shape(o, depth=0):
    """Key structure only, no values."""
    if isinstance(o, dict):
        return {k: (shape(v, depth + 1) if depth < 2 else type(v).__name__) for k, v in o.items()}
    if isinstance(o, list):
        return ["list[%d]" % len(o)] + ([shape(o[0], depth + 1)] if o and depth < 2 else [])
    return type(o).__name__
