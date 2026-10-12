#!/usr/bin/env python3
"""NFRA_CTLPLN TO-CT-u-7 fence exercise tool. ASCII only.

Subcommands:
  row-create   ONE synthetic non-internal row (firm 49financial, tier advisor) by conditional put, read back.
  before       R0: the non-internal caller reads one class-(ii) route BEFORE the apply (expect 200).
  after        R1 R2 R3: non-internal and internal callers on a class-(ii) and a class-(i) route, AFTER the apply.
  row-delete   delete the synthetic row only after the last minted token's exp, read back ABSENT with a control.

The internal caller is the dormant UI walker, armed and disarmed by its own tool (arm, real /auth/login, disarm in
a finally block). The non-internal caller is the CTO half section 2 option (a): a token signed in memory with the
current key slot, at most 10 minutes, never printed, stored or sent anywhere but the one request. Every call
prints the status code, the answering hop's request id (present or absent), a short body hash and, on a 4xx, the
message or error field. No token and no password is ever printed.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

import boto3
import jwt as pyjwt
from botocore.exceptions import ClientError

HOST = "https://opalinvest.dev"
TABLE = "opal-users-v2"
EMAIL = "ctlpln-ctu7-fence-20261012@opal.invalid"
PK = "USER#" + EMAIL
NAME = "NFRA_CTLPLN CT-u-7 synthetic partner caller"
NAME_PREFIX = "NFRA_CTLPLN CT-u-7 synthetic"
FIRM = "49financial"
KEY_SECRET = "opal/auth/jwt-private-key"
TOKEN_TTL_S = 600
ROUTE_II = "/v1/health/data-availability"
ROUTE_I = "/v1/aum/metrics"
UA = "Mozilla/5.0 opal-ctu7-fence/1"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
WALKER = os.path.join(ROOT, ".claude", "skills", "ui-walk", "ui_walker_account.py")
EXP_STATE = os.environ.get("CTU7_EXP_STATE", os.path.join(HERE, ".ctu7_last_exp.txt"))


def _ddb():
    return boto3.client("dynamodb")


def _stamp(label, extra=""):
    print("%s %s %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), label, extra))


def _census():
    """Count rows whose PK holds ctlpln-ctu7, over EVERY page; returns (matches, scanned, pages)."""
    matches = scanned = pages = 0
    for page in _ddb().get_paginator("scan").paginate(
            TableName=TABLE, FilterExpression="contains(PK, :p)",
            ExpressionAttributeValues={":p": {"S": "ctlpln-ctu7"}}, ConsistentRead=True):
        matches += page["Count"]
        scanned += page["ScannedCount"]
        pages += 1
    return matches, scanned, pages


def row_create():
    item = {
        "PK": {"S": PK}, "SK": {"S": "PROFILE"}, "email": {"S": EMAIL}, "name": {"S": NAME},
        "tier": {"S": "advisor"}, "role": {"S": "user"}, "firmId": {"S": FIRM},
        "userType": {"S": "test-reader"}, "status": {"S": "active"},
        "allowedFirmIds": {"L": [{"S": FIRM}]},
        "createdAt": {"S": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())},
        "createdBy": {"S": "0.7.0_AE_CloudOps~U7 NFRA_CTLPLN CT-u-7 (CTO half section 2 option a)"},
    }
    _ddb().put_item(TableName=TABLE, Item=item, ConditionExpression="attribute_not_exists(PK)")
    got = _ddb().get_item(TableName=TABLE, Key={"PK": {"S": PK}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
    ok = bool(got)
    for k, v in item.items():
        if k == "createdAt":
            continue
        ok = ok and got.get(k) == v
    _stamp("ROW-CREATE", "PK=%s readback_fields_equal=%s allowedFirmIds_is_list=%s"
           % (PK, ok, "L" in (got or {}).get("allowedFirmIds", {})))
    m, sc, pg = _census()
    _stamp("ROW-CENSUS", "synthetic rows with ctlpln-ctu7 in PK=%d of %d scanned over %d pages" % (m, sc, pg))


def _mint():
    pem = boto3.client("secretsmanager").get_secret_value(SecretId=KEY_SECRET)["SecretString"]
    now = int(time.time())
    exp = now + TOKEN_TTL_S
    claims = {"sub": EMAIL, "name": NAME, "role": "user", "tier": "advisor", "firmId": FIRM,
              "userType": "test-reader", "iss": "opal-portal-auth", "aud": "opal-portal-api",
              "iat": now, "exp": exp}
    tok = pyjwt.encode(claims, pem, algorithm="RS256")
    del pem
    prior = 0
    if os.path.exists(EXP_STATE):
        prior = int(open(EXP_STATE).read().strip() or "0")
    with open(EXP_STATE, "w") as f:
        f.write(str(max(prior, exp)))
    _stamp("MINT", "claim_names=%s exp=%d (%s) ttl_s=%d"
           % (",".join(sorted(claims)), exp, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(exp)), TOKEN_TTL_S))
    return tok


def _get(token, path):
    req = urllib.request.Request(HOST + path, method="GET",
                                 headers={"Authorization": "Bearer " + token, "User-Agent": UA,
                                          "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read(), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def _report(label, path, code, body, hdrs):
    msg = ""
    if code >= 400:
        try:
            obj = json.loads(body.decode("utf-8", "replace"))
            if isinstance(obj, dict):
                msg = " message=%r keys=%s" % (str(obj.get("message") or obj.get("error") or "")[:120], sorted(obj))
        except ValueError:
            msg = " message=<non-json>"
    _stamp(label, "GET %s code=%d body_bytes=%d body_sha256=%s apigw_requestid=%s%s"
           % (path, code, len(body), hashlib.sha256(body).hexdigest()[:16],
              "present" if hdrs.get("apigw-requestid") else "ABSENT", msg))
    return code


def before():
    tok = _mint()
    _report("R0 class-ii partner (BEFORE)", ROUTE_II, *_get(tok, ROUTE_II))
    del tok


def _walker(cmd, *args, env=None):
    return subprocess.run([sys.executable, WALKER, cmd] + list(args), capture_output=True, text=True, env=env)


def _internal_login():
    pw = _walker("secret", env=dict(os.environ, UI_WALK_CHILD="1")).stdout
    if not pw:
        raise SystemExit("STOP: walker secret unreadable")
    data = json.dumps({"email": "opal-ui-walker@opal.test", "password": pw}).encode("ascii")
    req = urllib.request.Request(HOST + "/auth/login", data=data, method="POST",
                                 headers={"Content-Type": "application/json", "Origin": HOST, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        raise SystemExit("STOP: walker login HTTP %d" % e.code)
    finally:
        del pw
    if not isinstance(body, dict) or "accessToken" not in body:
        raise SystemExit("STOP: walker login answered without accessToken; keys=%s"
                         % (sorted(body) if isinstance(body, dict) else type(body).__name__))
    _stamp("WALKER-LOGIN", "answered 200 keys=%s" % sorted(body))
    return body["accessToken"]


def _internal(out):
    arm = _walker("arm")
    holder = ""
    for line in arm.stdout.splitlines():
        if line.startswith("HOLDER "):
            holder = line.split(" ", 1)[1].strip()
    _stamp("WALKER-ARM", "holder_present=%s rc=%d first_line=%s"
           % (bool(holder), arm.returncode, (arm.stdout.splitlines() or [arm.stderr.strip()[:80]])[0][:90]))
    if not holder:
        raise SystemExit("STOP: walker not armed: %s" % (arm.stdout + arm.stderr)[:120])
    try:
        itok = _internal_login()
        out["ii_internal"] = _report("R2 class-ii internal (AFTER)", ROUTE_II, *_get(itok, ROUTE_II))
        out["i_internal"] = _report("R3b class-i internal (AFTER)", ROUTE_I, *_get(itok, ROUTE_I))
        del itok
    finally:
        dis = _walker("disarm", holder)
        for line in (dis.stdout + dis.stderr).splitlines():
            _stamp("WALKER-DISARM", line[:160])


def internal():
    out = {}
    _internal(out)
    print("internal class-ii=%d class-i=%d" % (out.get("ii_internal", -1), out.get("i_internal", -1)))


def after():
    out = {}
    ptok = _mint()
    out["ii_partner"] = _report("R1 class-ii partner (AFTER)", ROUTE_II, *_get(ptok, ROUTE_II))
    out["i_partner"] = _report("R3 class-i partner (AFTER)", ROUTE_I, *_get(ptok, ROUTE_I))
    del ptok
    _internal(out)
    print("class-ii partner=%d internal=%d" % (out["ii_partner"], out.get("ii_internal", -1)))
    print("class-i open partner=%d internal=%d" % (out["i_partner"], out.get("i_internal", -1)))


def row_delete():
    last = int(open(EXP_STATE).read().strip()) if os.path.exists(EXP_STATE) else 0
    now = int(time.time())
    if now <= last:
        raise SystemExit("REFUSED: last token exp %d is %d s away; the row stays" % (last, last - now))
    key = {"PK": {"S": PK}, "SK": {"S": "PROFILE"}}
    _ddb().delete_item(TableName=TABLE, Key=key, ConditionExpression="begins_with(#n, :p)",
                       ExpressionAttributeNames={"#n": "name"}, ExpressionAttributeValues={":p": {"S": NAME_PREFIX}})
    _stamp("ROW-DELETE", "PK=%s deleted %d s after the last exp" % (PK, now - last))
    gone = _ddb().get_item(TableName=TABLE, Key=key, ConsistentRead=True).get("Item")
    ctl = _ddb().get_item(TableName=TABLE, Key={"PK": {"S": "USER#ctlpln-ctu7-control-never-written@opal.invalid"},
                                                "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
    m, sc, pg = _census()
    _stamp("ROW-ABSENT", "row_item_after_delete=%s never_written_control_item=%s census_matches=%d of %d scanned over %d pages"
           % ("ABSENT" if not gone else "PRESENT", "ABSENT" if not ctl else "PRESENT", m, sc, pg))


if __name__ == "__main__":
    cmds = {"row-create": row_create, "before": before, "after": after, "internal": internal, "row-delete": row_delete}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        raise SystemExit("usage: ctu7_fence_tool.py row-create|before|after|internal|row-delete")
    try:
        cmds[sys.argv[1]]()
    except ClientError as exc:
        raise SystemExit("AWS ERROR: %s" % exc.response["Error"]["Code"])
