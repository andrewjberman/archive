#!/usr/bin/env python3
"""NFRA_CTLPLN TO-CT-w-3 exercise: reuses ctu7_fence_tool.py with its own synthetic identity. ASCII only.

Subcommands: row-create | after | row-delete   (the same rules as the CT-u-7 tool: tokens in memory, 600 s,
never printed; the internal caller is the UI walker armed and disarmed by its own tool).
after: R1 partner GET /aum/metrics; R3 partner GET one class-(ii) route; R2 internal GET /aum/metrics and
POST /sentiment/keyword-intelligence (a fixed one-keyword body, read-only on the deployed handler).
R4 (a caller of a firm NOT in the set) is NOT exercised here: no credential is minted for it.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ctu7_fence_tool as t  # noqa: E402

t.EMAIL = "ctlpln-ctw3-firmcheck-20261012@opal.invalid"
t.PK = "USER#" + t.EMAIL
t.NAME = "NFRA_CTLPLN CT-w-3 synthetic partner caller"
t.NAME_PREFIX = "NFRA_CTLPLN CT-w-3 synthetic"
t.CENSUS_TOKEN = "ctlpln-ctw3"
t.CREATED_BY = "0.7.0_AE_CloudOps~U7 NFRA_CTLPLN CT-w-3 (first pair CTO half section 2 option a)"
POST_ROUTE = "/v1/sentiment/keyword-intelligence"
POST_BODY = json.dumps({"keyword": "inflation"}).encode("ascii")


def _post(token, path):
    req = urllib.request.Request(t.HOST + path, data=POST_BODY, method="POST",
                                 headers={"Authorization": "Bearer " + token, "User-Agent": t.UA,
                                          "Accept": "application/json", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.read(), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def after():
    out = {}
    ptok = t._mint()
    out["i_partner"] = t._report("R1 class-i partner admitted-firm (AFTER)", t.ROUTE_I, *t._get(ptok, t.ROUTE_I))
    out["ii_partner"] = t._report("R3 class-ii partner (AFTER)", t.ROUTE_II, *t._get(ptok, t.ROUTE_II))
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
        out["i_internal"] = t._report("R2a class-i internal GET (AFTER)", t.ROUTE_I, *t._get(itok, t.ROUTE_I))
        out["i_internal_post"] = t._report("R2b class-i internal POST (AFTER)", POST_ROUTE, *_post(itok, POST_ROUTE))
        del itok
    finally:
        dis = t._walker("disarm", holder)
        for line in (dis.stdout + dis.stderr).splitlines():
            t._stamp("WALKER-DISARM", line[:160])
    print("class-i admitted-firm=%d internal=%d" % (out["i_partner"], out.get("i_internal", -1)))
    print("internal POST keyword-intelligence=%d" % out.get("i_internal_post", -1))
    print("class-ii partner=%d" % out["ii_partner"])


if __name__ == "__main__":
    cmds = {"row-create": t.row_create, "after": after, "row-delete": t.row_delete}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        raise SystemExit("usage: ctw3_firm_check_tool.py row-create|after|row-delete")
    try:
        cmds[sys.argv[1]]()
    except t.ClientError as exc:
        raise SystemExit("AWS ERROR: %s" % exc.response["Error"]["Code"])
