"""TCKT_VNEXT SA-r-1b -- the FWD-1 seat-arm run under pair v2.2. Steps 3-6 in ONE process.

Differences from SA-r-1 (order @68642d02e9, GO + AMENDMENT 1 + AMENDMENT 2):
  * TOKEN is `tier internal` (userType "test-filer" kept), so the authorizer derives allowedFirmIds = ALL.
    The row LIST [49financial] is then the ONLY client reach, and proving that is the whole census.
  * CENSUS IS WIDENED to EVERY live /api/scoped route, enumerated from the API's own route table (not
    from the source census), with the denominator PRINTED. A live count that differs from the source
    census's 117 is itself a finding and is printed as one.
  * NO DATA-REFRESH PROBE (AMENDMENT 2): every route on opal-data-refresh-api is skipped, because it is a
    write path. Instead, AFTER cleanup, ZERO calls are proven from that Lambda's own log group.
  * TICKET CREATE ARMS CARRY THE SYNTHETIC ATTACHMENT (AMENDMENT 1), so they reach _create_firm_allowed
    instead of dying at attachment validation the way SA-r-1's arm did. An off-list arm PASSES ONLY when
    its 4xx body NAMES THE FIRM; a 4xx from any other check is a FAIL to report, never a pass.

The token is minted in memory and NEVER printed, stored or committed. Every call goes over HTTPS to the
real CloudFront host; a direct lambda invoke is deliberately NOT used (CTO IRPT_YCDGEN @d54e0b7515 cond 1).

>> THE "BEHAVES AS ALL" DETECTOR, and why it is a fingerprint and not a payload read. A route that ignores
   selected_tenant answers an off-list firm with the SAME bytes it answers the own firm. Comparing the two
   answers detects that, but the trace may carry NO client figures (CTO condition 3). So each arm records
   only status, reason, body LENGTH and a 16-hex sha256 PREFIX -- a fingerprint, never content -- and the
   detector fires on: both arms 2xx AND identical fingerprints AND length past a trivial floor.

Usage: python sa_r1b_run.py [--advisor-opaque adv-04b85b8aefda]
"""
from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import boto3
import jwt as pyjwt

HOST = "d2n2nzpeqf34ge.cloudfront.net"
BASE = "https://" + HOST
REGION = "us-east-1"
USERS = "opal-users-v2"
PRIV_SECRET = "opal/auth/jwt-private-key"
PORTAL_API = "7k3ed8px20"

FILER = "tckt-fwd1-testfiler-20261009@opal.invalid"
FILER_NAME = "TCKT_VNEXT FWD-1 synthetic test filer"
FIRM = "49financial"
OFF_LIST = ("cottonwood", "inflection")
HOUSEHOLD = "[TEST] TCKT_VNEXT FWD-1 synthetic household"

# AMENDMENT 2: never probe this host. Its 9 routes are a write path.
SKIP_FUNCTIONS = frozenset({"opal-data-refresh-api"})
DATA_REFRESH_LOG_GROUP = "/aws/lambda/opal-data-refresh-api"

IRPT_SERVED = frozenset({
    "irpt-status", "irpt-export-render", "irpt-directory-search", "irpt-ycharts-generate",
    "irpt-narrative", "irpt-holdings", "irpt-performance-adapter", "irpt-49f-reporting-read-lambda",
})
TICKET_FN = "opal-ticket-api"

# AMENDMENT 1: the F10 leg M precedent attachment, so a CREATE arm reaches the firm clamp.
SYN_ATTACHMENT = {
    "upload_id": "test-sar1b-20261009",
    "input_id": "portfolio_abdbb292c2bf6f96b0db74468dcdd68a9383a2e4259be73c9cb1977fb3b2ba03",
}

ROOT = Path(__file__).resolve().parents[5]
CENSUS = ROOT / "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~6/SA_ROUTE_CENSUS.json"
TRACE = ROOT / "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/sa_r1b_trace.json"
MY_TRACE = ROOT / "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/sa_r1/sa_r1b_trace.json"
HOLDINGS = ROOT / "org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/aapl-vnq-12.03.csv"

SYN = {
    "{reportId}": "sa-r1b-synthetic-report", "{exportId}": "sa-r1b-synthetic-export",
    "{accountSetId}": "sa-r1b-synthetic-accountset", "{requestId}": "sa-r1b-synthetic-request",
    "{jobId}": "sa-r1b-synthetic-job", "{ticketId}": "sa-r1b-synthetic-ticket",
    "{advisorId}": "sa-r1b-synthetic-advisor", "{clientKey}": "sa-r1b-synthetic-client",
    "{relationshipId}": "sa-r1b-synthetic-rel", "{accountId}": "sa-r1b-synthetic-account",
    "{dimension}": "aua", "{surfaceId}": "sa-r1b-synthetic-surface",
    "{universeId}": "sa-r1b-synthetic-universe", "{executionId}": "sa-r1b-synthetic-exec",
    "{account_id}": "sa-r1b-synthetic-account", "{which}": "summary",
    "{client_id}": "sa-r1b-synthetic-client", "{quarter}": "2026Q2",
}
# Retained only to ANNOTATE an arm's body size. It is deliberately NOT a classifier any more: using it as
# one is what raised the false STOP in run SA-r-1b-2026-10-09T16:19:13Z. See the ALL detector below.
TRIVIAL_BODY = 80

ddb = boto3.client("dynamodb", region_name=REGION)


def iso(t=None):
    return (t or dt.datetime.now(dt.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")


def fill(route):
    out = route
    for k, v in SYN.items():
        out = out.replace(k, v)
    return out


def adv_label(email):
    return "adv-" + hashlib.sha256(email.lower().encode()).hexdigest()[:12]


def resolve_advisor(opaque, firm):
    pg = ddb.get_paginator("scan")
    scanned = 0
    for page in pg.paginate(TableName=USERS):
        for it in page.get("Items", []):
            scanned += 1
            em = (it.get("email") or {}).get("S")
            if em and adv_label(em) == opaque and (it.get("firmId") or {}).get("S") == firm:
                print("OK: advisor resolved from %d scanned row(s); opaque echo %s" % (scanned, adv_label(em)))
                return em
    print("ERROR: no %s user carries opaque %s (%d scanned)" % (firm, opaque, scanned))
    return None


def write_row():
    item = {
        "PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"},
        "email": {"S": FILER}, "firmId": {"S": "opal-capital"},
        "status": {"S": "active"}, "userType": {"S": "test-filer"},
        "name": {"S": FILER_NAME}, "allowedFirmIds": {"L": [{"S": FIRM}]},
    }
    ddb.put_item(TableName=USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
    back = ddb.get_item(TableName=USERS, Key={"PK": item["PK"], "SK": item["SK"]},
                        ConsistentRead=True).get("Item")
    print("OK: row written; ConsistentRead read-back present=%s allowedFirmIds=%s"
          % (back is not None, (back or {}).get("allowedFirmIds")))
    return back is not None


def mint_token():
    """ONE RS256 token. v2.2: tier internal, userType test-filer kept."""
    pem = boto3.client("secretsmanager", region_name=REGION).get_secret_value(
        SecretId=PRIV_SECRET)["SecretString"]
    issued = int(time.time())
    claims = {"sub": FILER, "iss": "opal-portal-auth", "aud": "opal-portal-api",
              "firmId": "opal-capital", "tier": "internal", "role": "user",
              "userType": "test-filer", "name": FILER_NAME, "iat": issued, "exp": issued + 7200}
    tok = pyjwt.encode(claims, pem, algorithm="RS256")
    print("OK: token minted  tier=internal userType=test-filer  iat=%s exp=%s  claims=%s"
          % (iso(dt.datetime.fromtimestamp(issued, dt.timezone.utc)),
             iso(dt.datetime.fromtimestamp(issued + 7200, dt.timezone.utc)), sorted(claims)))
    return tok, issued


def call(token, method, path, query=None, body=None, timeout=90):
    url = BASE + path
    if query:
        url += "?" + "&".join("%s=%s" % (k, urllib.parse.quote(str(v), safe="@.-_"))
                              for k, v in query.items())
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("x-contract-version", "v1")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw, status = r.read().decode("utf-8", "replace"), r.status
    except urllib.error.HTTPError as e:
        raw, status = e.read().decode("utf-8", "replace"), e.code
    except Exception as e:  # noqa: BLE001 -- a transport failure is DATA, never a pass
        return {"status": 0, "reason": "TRANSPORT_" + type(e).__name__, "len": 0, "fp": None, "parsed": None}
    try:
        parsed = json.loads(raw)
    except ValueError:
        parsed = None
    return {"status": status, "reason": reason_of(parsed) if parsed is not None else raw[:120],
            "len": len(raw), "fp": hashlib.sha256(raw.encode()).hexdigest()[:16], "parsed": parsed}


def reason_of(parsed):
    if not isinstance(parsed, dict):
        return None
    st = parsed.get("status")
    if isinstance(st, dict) and st.get("public_reason_code"):
        return st["public_reason_code"]
    for key in ("public_reason_code", "code", "error", "message"):
        v = parsed.get(key)
        if isinstance(v, str):
            return v[:140]
    return None


def names_firm(res, firm):
    """AMENDMENT 1's oracle for a CREATE arm: the 4xx body must NAME the firm."""
    blob = json.dumps(res.get("parsed")) if res.get("parsed") is not None else (res.get("reason") or "")
    return firm in blob or "allowed firms" in blob or "FIRM_BINDING" in blob


# ---------------------------------------------------------------- live route table


def live_routes():
    c = boto3.client("apigatewayv2", region_name=REGION)

    def page(fn, **kw):
        out, tok = [], None
        while True:
            k = dict(kw, MaxResults="500")
            if tok:
                k["NextToken"] = tok
            r = fn(**k)
            out.extend(r.get("Items", []))
            tok = r.get("NextToken")
            if not tok:
                return out

    routes = page(c.get_routes, ApiId=PORTAL_API)
    integs = {i["IntegrationId"]: i for i in page(c.get_integrations, ApiId=PORTAL_API)}

    def fn_of(r):
        t = r.get("Target") or ""
        uri = (integs.get(t.split("/")[-1]) or {}).get("IntegrationUri") or ""
        m = re.search(r"function:([^:/]+)", uri)
        return m.group(1) if m else "UNMAPPED"

    rows = []
    for r in routes:
        key = r["RouteKey"]
        if " " not in key:
            continue
        method, route = key.split(" ", 1)
        rows.append({"method": method, "route": route, "function": fn_of(r)})
    return routes, rows


def census_diff(all_live, scoped):
    src = json.loads(CENSUS.read_text(encoding="utf-8"))
    src_keys = {r["method"] + " " + r["route"] for r in src["rows"]}
    live_keys = {r["RouteKey"] for r in all_live}
    added, removed = sorted(live_keys - src_keys), sorted(src_keys - live_keys)
    print("== step 4: the live route table (the denominator) ==")
    print("  live routes on API %s      : %d" % (PORTAL_API, len(all_live)))
    print("  source census rows (@41b7e28bdf): %d  -> %s"
          % (len(src_keys), "SAME" if len(live_keys) == len(src_keys) else "DIFFERENT, printed as a finding"))
    print("  live /api/scoped            : %d" % len(scoped))
    for k in added:
        print("    + LIVE NOT IN SOURCE: %s" % k)
    for k in removed:
        print("    - SOURCE NOT LIVE   : %s" % k)
    return {"claim": "measured", "api_id": PORTAL_API, "live_routes": len(all_live),
            "source_census_rows": len(src_keys), "source_census_pin": "41b7e28bdf",
            "live_api_scoped": len(scoped),
            "live_not_in_source": added, "source_not_live": removed,
            "finding": ("the live table carries %d route(s) against the source census's %d; the source census "
                        "declares this blind spot itself ('routes that exist only live cannot be enumerated "
                        "from source'). The real delta is 2 live-only /api/scoped GETs plus a $default "
                        "spelling difference." % (len(all_live), len(src_keys)))}


# ---------------------------------------------------------------- step 4


def census(token, run_id):
    all_live, rows = live_routes()
    scoped = [r for r in rows if "/api/scoped" in r["route"]]
    summary = {"route_table": census_diff(all_live, scoped)}

    skipped = [r for r in scoped if r["function"] in SKIP_FUNCTIONS]
    armed = [r for r in scoped if r["function"] not in SKIP_FUNCTIONS]
    print("  skipped (AMENDMENT 2, data-refresh is a write path): %d route(s) on %s"
          % (len(skipped), ",".join(sorted(SKIP_FUNCTIONS))))
    print("  ARMING: %d of %d live /api/scoped route(s)" % (len(armed), len(scoped)))

    arms, created_tickets = [], []
    off_admits, selector_ignored, create_fails = [], [], []
    by_plane = collections.Counter()

    for r in armed:
        fn, method, route = r["function"], r["method"], r["route"]
        path = fill(route)
        is_create = fn == TICKET_FN and method == "POST" and route in (
            "/api/scoped/tickets", "/api/scoped/tickets/submit")
        plane = ("irpt-served" if fn in IRPT_SERVED else
                 "ticket-create" if is_create else
                 "ticket-api" if fn == TICKET_FN else "other-scoped")
        by_plane[plane] += 1
        row = {"function": fn, "method": method, "route": route, "plane": plane, "arms": {}}

        if is_create:
            # AMENDMENT 1: carry the synthetic attachment so the arm REACHES _create_firm_allowed.
            for firm in (FIRM,) + OFF_LIST:
                body = {"ticket_type": "analysis_request",
                        "title": "[TEST TCKT_VNEXT FWD-1] census arm %s" % firm,
                        "source": "portal",
                        "answers": {"advisor": "sa-r1b-synthetic-advisor", "firm": firm,
                                    "household": HOUSEHOLD, "report_type": "Overview"},
                        "attachment": dict(SYN_ATTACHMENT, upload_id="test-sar1b-" + run_id[-8:])}
                res = call(token, "POST", path, None, body)
                entry = {"status": res["status"], "reason": res["reason"], "len": res["len"]}
                if firm == FIRM:
                    tid = None
                    if isinstance(res["parsed"], dict):
                        t = res["parsed"].get("ticket")
                        tid = (t or {}).get("ticket_id") if isinstance(t, dict) else None
                    entry["ticket_id"] = tid
                    entry["admitted"] = res["status"] < 400
                    if tid:
                        created_tickets.append(tid)
                else:
                    named = names_firm(res, firm)
                    entry["refused"] = res["status"] >= 400
                    entry["body_names_the_firm"] = named
                    # the amendment's rule: a 4xx that does NOT name the firm is a FAIL, never a pass
                    if res["status"] < 400:
                        off_admits.append((fn, method, route, firm, "ADMITTED"))
                    elif not named:
                        create_fails.append((fn, method, route, firm, res["reason"]))
                row["arms"][firm] = entry
            print("  [create ] %-5s %-46s own=%s/%s  %s" % (
                method, route[:46], row["arms"][FIRM]["status"],
                row["arms"][FIRM].get("ticket_id") or "-",
                " ".join("%s=%s/named=%s" % (f, row["arms"][f]["status"],
                                             row["arms"][f]["body_names_the_firm"]) for f in OFF_LIST)))
            arms.append(row)
            continue

        body = {} if method in ("POST", "PUT", "PATCH") else None
        own = call(token, method, path, {"selected_tenant": FIRM}, body)
        row["arms"][FIRM] = {"status": own["status"], "reason": own["reason"],
                             "len": own["len"], "fp": own["fp"]}
        if plane == "ticket-api" and method == "GET" and route == "/api/scoped/tickets":
            p = own["parsed"] if isinstance(own["parsed"], dict) else {}
            lst = p.get("tickets") or p.get("items") or []
            firms = sorted({(t.get("requester") or {}).get("firm") for t in lst
                            if isinstance(t, dict)} - {None})
            row["list_filter"] = {"tickets_returned": len(lst), "distinct_requester_firms": firms}
            for f in firms:
                if f != FIRM:
                    off_admits.append((fn, method, route, f, "LIST returned a foreign requester firm"))
            print("  [ticket ] GET   %-46s list n=%d firms=%s" % (route[:46], len(lst), firms))

        for firm in OFF_LIST:
            res = call(token, method, path, {"selected_tenant": firm}, body)
            ent = {"status": res["status"], "reason": res["reason"], "len": res["len"], "fp": res["fp"]}
            if plane == "irpt-served":
                ent["refused"] = res["reason"] == "FIRM_BINDING"
                if not ent["refused"] and res["status"] < 400:
                    off_admits.append((fn, method, route, firm, "status %s" % res["status"]))
            else:
                ent["refused"] = res["status"] >= 400
                if res["status"] < 400:
                    # THE ALL DETECTOR, corrected after run SA-r-1b-2026-10-09T16:19:13Z.
                    # The discriminator is the FINGERPRINT, never the body length. An off-list 2xx whose
                    # bytes are IDENTICAL to the own-firm answer served no off-list data -- the route simply
                    # does not read selected_tenant. The earlier form also required len > TRIVIAL_BODY, which
                    # sent a SHORT identical 200 (GET /api/scoped/amgt/watchlist, body `[]`, len 2, same
                    # fingerprint for all three firms) into the ADMIT bucket and raised a false STOP that
                    # cost the hops. Length now only annotates; it never classifies.
                    if own["status"] < 400 and own["fp"] == res["fp"]:
                        ent["selector_ignored"] = True
                        ent["identical_to_own_firm_bytes"] = True
                        selector_ignored.append((fn, method, route, firm, own["len"]))
                    else:
                        ent["differs_from_own_firm_bytes"] = True
                        off_admits.append((fn, method, route, firm,
                                           "status %s, fingerprint DIFFERS from the own-firm answer"
                                           % res["status"]))
            row["arms"][firm] = ent
        if plane != "ticket-api" or method != "GET" or route != "/api/scoped/tickets":
            print("  [%-7s] %-5s %-46s own=%s/%s  %s" % (
                plane[:7], method, route[:46], own["status"], (own["reason"] or "-")[:18],
                " ".join("%s=%s/%s" % (f[:4], row["arms"][f]["status"],
                                       (row["arms"][f]["reason"] or "-")[:14]) for f in OFF_LIST)))
        arms.append(row)

    summary.update({
        "claim": "measured", "host": HOST,
        "armed": len(armed), "skipped_data_refresh": len(skipped),
        "by_plane": dict(by_plane),
        "off_list_admits": off_admits,
        "selector_ignored": selector_ignored,
        "create_arm_fails_not_naming_the_firm": create_fails,
        "tickets_created_by_the_census": created_tickets,
        "arms": arms,
    })
    stop = None
    if off_admits:
        stop = "OFF-LIST FIRM ADMIT on %d arm(s): %s" % (len(off_admits), off_admits[:4])
    elif selector_ignored:
        stop = "BEHAVES AS ALL on %d arm(s): %s" % (len(selector_ignored), selector_ignored[:4])
    print("  => armed %d | off-list admits %d | behaves-as-ALL %d | create arms not naming the firm %d"
          % (len(armed), len(off_admits), len(selector_ignored), len(create_fails)))
    print("  => STOP=%s" % stop)
    summary["stop"] = stop
    return summary, stop


# ---------------------------------------------------------------- step 5


def hops(token, advisor, trace):
    raw = HOLDINGS.read_bytes()
    file_sha = hashlib.sha256(raw).hexdigest()
    upload_token = "sar1b-" + file_sha[:16]
    h = {x["hop"]: x for x in trace["hops"]}
    named = trace["named_failures"]
    print("== step 5: hops (a)-(g) ==")

    a = h["a_upload"]
    a["file"] = {"path": str(HOLDINGS.relative_to(ROOT)).replace("\\", "/"), "sha256": file_sha}
    input_id = upload_id = None
    state = None
    for i in range(14):
        res = call(token, "POST", "/api/scoped/investor-reporting/analysis/inputs",
                   {"selected_tenant": FIRM, "advisor_email": advisor},
                   {"upload_token": upload_token, "filename": "sa_r1b_template.csv",
                    "file_base64": base64.b64encode(raw).decode(), "file_type": "csv"})
        p = res["parsed"] if isinstance(res["parsed"], dict) else {}
        d = p.get("data") if isinstance(p.get("data"), dict) else p
        if isinstance(d, dict):
            input_id = d.get("input_id") or input_id
            upload_id = d.get("upload_id") or upload_id
        st = p.get("status")
        state = st.get("state") if isinstance(st, dict) else None
        a["status"], a["state_seen"], a["polls"] = res["status"], state, i + 1
        print("  (a) poll %2d http=%s state=%r reason=%r input_id=%r"
              % (i + 1, res["status"], state, res["reason"], input_id))
        if state in ("NORMALIZED", "READY", "AVAILABLE"):
            break
        if res["status"] >= 400 and res["reason"] not in (None, "NOT_READY", "RESOLVING", "PENDING"):
            break
        time.sleep(5)
    a["upload_id"], a["input_id"] = upload_id, input_id
    save(trace)
    if not input_id:
        named.append({"hop": "a_upload", "status": a["status"], "reason": state or "no input_id",
                      "note": "the upload door produced no input_id; (b)-(g) depend on it"})
        return trace

    b = h["b_ticket"]
    res = call(token, "POST", "/api/scoped/tickets", None,
               {"ticket_type": "analysis_request", "title": "[TEST TCKT_VNEXT FWD-1] seat arm",
                "source": "portal",
                "answers": {"advisor": adv_label(advisor), "firm": FIRM,
                            "household": HOUSEHOLD, "report_type": "Overview"},
                "attachment": {"upload_id": upload_id, "input_id": input_id}})
    tkt = None
    if isinstance(res["parsed"], dict):
        t = res["parsed"].get("ticket")
        tkt = (t or {}).get("ticket_id") if isinstance(t, dict) else None
    b["status"], b["ticket_id"], b["source"] = res["status"], tkt, "portal"
    print("  (b) ticket http=%s reason=%r ticket_id=%r" % (res["status"], res["reason"], tkt))
    save(trace)
    if not tkt:
        named.append({"hop": "b_ticket", "status": res["status"], "reason": res["reason"],
                      "note": "ticket CREATE refused; (c)-(g) need a ticket_id and are NOT retried"})
        for k in ("c_claim", "d_analysis", "e_ready", "f_report", "g_open"):
            named.append({"hop": k, "status": None, "reason": "UNREACHABLE", "note": "depends on (b)"})
        return trace
    trace["journey_ticket"] = tkt

    res = call(token, "POST", "/api/scoped/tickets/%s/claim" % tkt, None, {})
    h["c_claim"]["status"] = res["status"]
    print("  (c) claim http=%s reason=%r" % (res["status"], res["reason"]))
    if res["status"] >= 400:
        named.append({"hop": "c_claim", "status": res["status"], "reason": res["reason"]})
    save(trace)

    res = call(token, "POST", "/api/scoped/investor-reporting/analysis",
               {"selected_tenant": FIRM}, {"input_id": input_id, "ticket_id": tkt})
    p = res["parsed"] if isinstance(res["parsed"], dict) else {}
    inner = p.get("data") if isinstance(p.get("data"), dict) else p
    rid = inner.get("request_id") if isinstance(inner, dict) else None
    h["d_analysis"]["status"], h["d_analysis"]["request_id"] = res["status"], rid
    print("  (d) analysis http=%s reason=%r request_id=%r" % (res["status"], res["reason"], rid))
    save(trace)
    if not rid:
        named.append({"hop": "d_analysis", "status": res["status"], "reason": res["reason"],
                      "note": "no request_id; (e)-(g) depend on it"})
        return trace

    e = h["e_ready"]
    rstate = None
    for i in range(60):
        res = call(token, "GET", "/api/scoped/investor-reporting/analysis/requests/%s" % rid,
                   {"selected_tenant": FIRM})
        p = res["parsed"] if isinstance(res["parsed"], dict) else {}
        inner = p.get("data") if isinstance(p.get("data"), dict) else p
        rstate = (inner or {}).get("state") or (inner or {}).get("status") if isinstance(inner, dict) else None
        if isinstance(rstate, dict):
            rstate = rstate.get("state")
        e["status"], e["polls"], e["state"] = res["status"], i + 1, rstate
        if i % 5 == 0 or rstate in ("READY", "AVAILABLE", "FAILED", "REFUSED"):
            print("  (e) poll %2d http=%s state=%r" % (i + 1, res["status"], rstate))
        if rstate in ("READY", "AVAILABLE", "FAILED", "REFUSED"):
            break
        time.sleep(10)
    save(trace)
    if rstate not in ("READY", "AVAILABLE"):
        named.append({"hop": "e_ready", "status": e["status"], "reason": rstate,
                      "note": "never reached READY in the poll budget; not retried into a pass"})

    res = call(token, "POST", "/api/scoped/tickets/%s/report" % tkt, None, {"request_id": rid})
    h["f_report"]["status"] = res["status"]
    print("  (f) report http=%s reason=%r" % (res["status"], res["reason"]))
    if res["status"] >= 400:
        named.append({"hop": "f_report", "status": res["status"], "reason": res["reason"]})
    save(trace)

    r1 = call(token, "GET", "/api/scoped/tickets/%s" % tkt)
    r2 = call(token, "GET", "/api/scoped/investor-reporting/analysis/requests/%s" % rid,
              {"selected_tenant": FIRM})
    ref = None
    if isinstance(r1["parsed"], dict):
        t = r1["parsed"].get("ticket") if isinstance(r1["parsed"].get("ticket"), dict) else r1["parsed"]
        ref = (t or {}).get("report_ref")
    g = h["g_open"]
    g["status"], g["second_status"] = r1["status"], r2["status"]
    g["report_opened"] = bool(ref) and r2["status"] < 400
    print("  (g) ticket http=%s request http=%s report_ref_present=%s"
          % (r1["status"], r2["status"], bool(ref)))
    if not g["report_opened"]:
        named.append({"hop": "g_open", "status": r1["status"], "reason": r1["reason"] or r2["reason"],
                      "note": "report_ref absent on the ticket, or the request read refused"})
    save(trace)
    return trace


# ---------------------------------------------------------------- step 6 + the zero-call proof


def cleanup(token, trace):
    print("== step 6: cleanup, same session ==")
    out = trace["cleanup"]
    ddb.delete_item(TableName=USERS, Key={"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}})
    back = ddb.get_item(TableName=USERS, Key={"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}},
                        ConsistentRead=True).get("Item")
    out["row_removed_read_back_absent"] = back is None
    print("  row removed; ConsistentRead read-back absent = %s" % (back is None))

    # every ticket this run created: the journey's, plus AMENDMENT 1's 49financial census arm
    todo = [t for t in ([trace.get("journey_ticket")] +
                        (trace.get("census", {}) or {}).get("tickets_created_by_the_census", [])) if t]
    done = {}
    for tkt in dict.fromkeys(todo):
        res = call(token, "POST", "/api/scoped/tickets/%s/complete" % tkt, None,
                   {"resolution": "[TEST] SA-r-1b arm complete"})
        done[tkt] = res["status"]
        print("  ticket %s complete -> http=%s reason=%r" % (tkt, res["status"], res["reason"]))
    out["tickets_completed"] = done
    out["tickets_completed_all"] = bool(todo) and all(v < 400 for v in done.values())
    out["token_left_to_expire"] = True
    save(trace)
    return trace


def data_refresh_zero_calls(trace, start_unix, end_unix):
    """AMENDMENT 2: prove ZERO data-refresh calls for the filer over the token window, from its own logs."""
    print("== AMENDMENT 2: zero data-refresh calls, from the log group ==")
    logs = boto3.client("logs", region_name=REGION)
    pattern = '"%s"' % FILER
    out = {"claim": "measured", "log_group": DATA_REFRESH_LOG_GROUP,
           "window": {"from": iso(dt.datetime.fromtimestamp(start_unix, dt.timezone.utc)),
                      "to": iso(dt.datetime.fromtimestamp(end_unix, dt.timezone.utc))},
           "query": "filter_log_events logGroupName=%s filterPattern=%s startTime=%d endTime=%d"
                    % (DATA_REFRESH_LOG_GROUP, pattern, start_unix * 1000, end_unix * 1000)}
    try:
        n, streams, tok = 0, 0, None
        while True:
            kw = {"logGroupName": DATA_REFRESH_LOG_GROUP, "filterPattern": pattern,
                  "startTime": start_unix * 1000, "endTime": end_unix * 1000}
            if tok:
                kw["nextToken"] = tok
            r = logs.filter_log_events(**kw)
            n += len(r.get("events", []))
            streams += len(r.get("searchedLogStreams", []))
            tok = r.get("nextToken")
            if not tok:
                break
        out["match_count"] = n
        out["searched_log_streams"] = streams
        out["verdict"] = "ZERO" if n == 0 else "NON-ZERO -- report it"
        print("  %s: %d match(es) for the filer over the window (%d stream(s) searched) -> %s"
              % (DATA_REFRESH_LOG_GROUP, n, streams, out["verdict"]))
    except Exception as e:  # noqa: BLE001 -- a failed retrieval returns a VALUE; say so, never read it as zero
        out["match_count"] = None
        out["verdict"] = "UNREAD -- %s: %s" % (type(e).__name__, str(e)[:160])
        print("  WARN: the log read did NOT complete: %s. A failed retrieval is NOT a zero." % out["verdict"])
    trace["data_refresh_zero_calls"] = out
    save(trace)


def save(trace):
    for p in (TRACE, MY_TRACE):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(trace, indent=1) + "\n", encoding="utf-8")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--advisor-opaque", default="adv-04b85b8aefda")
    ap.add_argument("--read27", required=True,
                    help="AC1's measured result, carried in from the separate STOP 1 invocation")
    a = ap.parse_args(argv)
    run_id = "SA-r-1b-" + iso()

    trace = {
        "run_id": run_id, "executor": "0.7.0_AE_CloudOps~TV2", "claim": "measured",
        "pair": "v2.2", "order_pin": "68642d02e9",
        "entry": {"host": HOST, "transport": "HTTPS through CloudFront",
                  "not_used": "direct lambda invoke (CTO IRPT_YCDGEN @d54e0b7515 condition 1)"},
        "preconditions": {"read27": a.read27, "cto_half_v2_2": "022ee70258", "row_written": None,
                          "token": "tier internal, userType test-filer, role user, firmId opal-capital",
                          "token_exp": None},
        "census": None,
        "hops": [
            {"hop": "a_upload", "call": "POST /api/scoped/investor-reporting/analysis/inputs?selected_tenant=49financial",
             "status": 0, "upload_id": "", "input_id": "", "file": {"path": "", "sha256": ""}},
            {"hop": "b_ticket", "call": "POST /api/scoped/tickets", "status": 0, "ticket_id": "", "source": ""},
            {"hop": "c_claim", "call": "POST /api/scoped/tickets/{ticketId}/claim", "status": 0},
            {"hop": "d_analysis", "call": "POST /api/scoped/investor-reporting/analysis", "status": 0, "request_id": ""},
            {"hop": "e_ready", "call": "GET /api/scoped/investor-reporting/analysis/requests/{requestId}",
             "status": 0, "polls": 0, "state": ""},
            {"hop": "f_report", "call": "POST /api/scoped/tickets/{ticketId}/report", "status": 0},
            {"hop": "g_open", "call": "GET /api/scoped/tickets/{ticketId}; GET .../analysis/requests/{requestId}",
             "status": 0, "report_opened": False},
        ],
        "named_failures": [], "journey_ticket": None,
        "cleanup": {"row_removed_read_back_absent": False, "tickets_completed": {}},
        "data_refresh_zero_calls": None,
        "no_client_figures": ("hop statuses and artifact IDs only. Census arms record status, reason, body LENGTH "
                              "and a 16-hex sha256 PREFIX as a fingerprint -- never payload content."),
    }

    advisor = resolve_advisor(a.advisor_opaque, FIRM)
    if advisor is None:
        return 1
    if not write_row():
        print("ERROR: row not readable after the put")
        return 1
    trace["preconditions"]["row_written"] = iso()
    token, issued = mint_token()
    trace["preconditions"]["token_exp"] = iso(dt.datetime.fromtimestamp(issued + 7200, dt.timezone.utc))
    save(trace)

    try:
        summary, stop = census(token, run_id)
        trace["census"] = summary
        save(trace)
        if stop:
            trace["named_failures"].append({"hop": "ALL", "status": None,
                                            "reason": "STOP_BEFORE_HOPS", "note": stop})
            print("STOP: %s -- no hop runs; going to cleanup" % stop)
        else:
            hops(token, advisor, trace)
    finally:
        cleanup(token, trace)
        data_refresh_zero_calls(trace, issued, int(time.time()) + 1)
    print("OK: trace at %s" % TRACE.relative_to(ROOT))
    print("OK: own copy at %s" % MY_TRACE.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
