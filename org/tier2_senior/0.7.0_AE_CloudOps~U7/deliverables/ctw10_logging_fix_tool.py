#!/usr/bin/env python3
"""NFRA_CTLPLN TO-CT-w-10 exercise tool: reuses ctu7_fence_tool.py with its own synthetic identity. ASCII only.

Subcommands:
  row-create | row-delete   the same rules as the CT-u-7 tool (token in memory, 600 s, never printed).
  after                     partner GET /aum/metrics, partner GET one class-(ii) route, internal (walker) GET /aum/metrics.
  logread <apply_epoch>     read ONLY the log events written after the apply time: counts of events, JWT-shaped
                            strings, Bearer, and cookie/authorization words, plus one redacted example line.
  identities                digests ONLY of the identities behind the refresh_token lines aged 7 days or less.
No token, cookie or identity value is printed or stored by any subcommand.
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import re
import sys
import time

import boto3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ctu7_fence_tool as t  # noqa: E402

t.EMAIL = "ctlpln-ctw10-logfix-20261012@opal.invalid"
t.PK = "USER#" + t.EMAIL
t.NAME = "NFRA_CTLPLN CT-w-10 synthetic partner caller"
t.NAME_PREFIX = "NFRA_CTLPLN CT-w-10 synthetic"
t.CENSUS_TOKEN = "ctlpln-ctw10"
t.CREATED_BY = "0.7.0_AE_CloudOps~U7 NFRA_CTLPLN CT-w-10 (first pair CTO half section 2 option a)"
GROUP = "/aws/lambda/opal-portal-data-proxy"
JWT = re.compile(r"eyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]*")


def after():
    out = {}
    ptok = t._mint()
    out["i_partner"] = t._report("R1a class-i partner admitted-firm (AFTER)", t.ROUTE_I, *t._get(ptok, t.ROUTE_I))
    out["ii_partner"] = t._report("R2 class-ii partner (AFTER)", t.ROUTE_II, *t._get(ptok, t.ROUTE_II))
    del ptok
    arm = t._walker("arm")
    holder = ""
    for line in arm.stdout.splitlines():
        if line.startswith("HOLDER "):
            holder = line.split(" ", 1)[1].strip()
    t._stamp("WALKER-ARM", "holder_present=%s rc=%d" % (bool(holder), arm.returncode))
    if not holder:
        raise SystemExit("STOP: walker not armed: %s" % (arm.stdout + arm.stderr)[:120])
    try:
        itok = t._internal_login()
        out["i_internal"] = t._report("R1b class-i internal (AFTER)", t.ROUTE_I, *t._get(itok, t.ROUTE_I))
        del itok
    finally:
        dis = t._walker("disarm", holder)
        for line in (dis.stdout + dis.stderr).splitlines():
            t._stamp("WALKER-DISARM", line[:160])
    print("class-i admitted-firm=%d internal=%d" % (out["i_partner"], out.get("i_internal", -1)))
    print("class-ii partner=%d" % out["ii_partner"])


def _events(start_ms, pattern=None):
    logs = boto3.client("logs")
    kw = {"logGroupName": GROUP, "startTime": start_ms}
    if pattern:
        kw["filterPattern"] = pattern
    for page in logs.get_paginator("filter_log_events").paginate(**kw):
        for e in page["events"]:
            yield e


def logread(apply_epoch):
    start_ms = int(apply_epoch) * 1000
    ev = list(_events(start_ms))
    jwt = sum(1 for e in ev if JWT.search(e["message"]))
    bearer = sum(1 for e in ev if "bearer" in e["message"].lower())
    cookie = sum(1 for e in ev if re.search(r"cookie|refresh_token|device_trust|authorization", e["message"], re.I))
    kinds = collections.Counter(e["message"].split(":", 1)[0][:14] if ":" in e["message"][:30] else e["message"][:10].strip()
                                for e in ev)
    ex = ""
    for e in ev:
        m = re.match(r"Request: method=(\w+), path=(\S+), request_id=", e["message"])
        if m:
            ex = "Request: method=%s, path=%s, request_id=<redacted>" % (m.group(1), m.group(2).rstrip(","))
            break
    t._stamp("LOGREAD", "events written after %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(apply_epoch))))
    print("line-prefix census of those events:", dict(kinds.most_common(12)))
    print("lines with cookie/refresh_token/device_trust/authorization words:", cookie)
    print("example line (every value other than method and path redacted):", ex or "<no Request line found>")
    print("POST-APPLY events=%d jwt_shaped=%d bearer=%d" % (len(ev), jwt, bearer))


def identities():
    now = time.time()
    digs = []
    lines = 0
    for e in _events(int((now - 14 * 86400) * 1000), '"Event:"'):
        m = e["message"]
        i = m.find("Event: ")
        try:
            o = json.loads(m[i + 7:])
        except ValueError:
            continue
        if "refresh_token" not in [str(c).split("=", 1)[0] for c in (o.get("cookies") or [])]:
            continue
        if (now - e["timestamp"] / 1000.0) > 7 * 86400:
            continue
        lines += 1
        ac = (o.get("requestContext") or {}).get("authorizer") or {}
        em = str((ac.get("lambda") if isinstance(ac.get("lambda"), dict) else ac).get("email") or "").strip().lower()
        digs.append(hashlib.sha256(em.encode("utf-8")).hexdigest() if em else "<no-identity-in-context>")
    uniq = sorted(set(digs))
    # mapping control: hash the users table's emails the same way and COUNT the matches (never print an identity)
    ddb = boto3.client("dynamodb")
    table = collections.Counter()
    rows = 0
    for pg in ddb.get_paginator("scan").paginate(TableName=t.TABLE, ProjectionExpression="SK, email", ConsistentRead=True):
        for it in pg["Items"]:
            if it.get("SK", {}).get("S") == "PROFILE" and it.get("email", {}).get("S"):
                rows += 1
                table[hashlib.sha256(it["email"]["S"].strip().lower().encode("utf-8")).hexdigest()] += 1
    mapped = sum(1 for d in uniq if table.get(d, 0) == 1)
    ambiguous = sum(1 for d in uniq if table.get(d, 0) > 1)
    print("refresh_token lines aged 7 days or less: %d" % lines)
    print("distinct identity digests (sha256 of the lower-cased email): %d" % len(uniq))
    print("mapping control against the users table (%d PROFILE rows hashed the same way): %d digests map to exactly one account, %d to several, %d to none"
          % (rows, mapped, ambiguous, len(uniq) - mapped - ambiguous))
    for d in uniq:
        print(d)


if __name__ == "__main__":
    cmds = {"row-create": t.row_create, "after": after, "row-delete": t.row_delete, "identities": identities}
    if len(sys.argv) == 3 and sys.argv[1] == "logread":
        logread(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] in cmds:
        cmds[sys.argv[1]]()
    else:
        raise SystemExit("usage: ctw10_logging_fix_tool.py row-create|after|identities|row-delete | logread <apply_epoch>")
