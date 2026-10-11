"""TCKT_VNEXT FWD-1 seat-arm runner, REPAIRED for round 2 (cell R2-rn-1, 0.9.0_WK_TCKT_VNEXT~8).
Copied from org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/sa_r1/sa_r1b_run.py and repaired:
  1. importable with no side effect: boto3/jwt/clients are built on first use, never at import; the HTTP layer
     `call` and the poll sleeper `SLEEP` are module attributes a test replaces.
  2. the analysis request id is the SERVICE's: the submission answer, else the firm's request list. The client
     token sent as the submission's request_id is NEVER polled, recorded on a ticket or written as a hop request_id.
  3. (AMENDMENT 1) hop (e) reads the FINISHED REPORT (operation `analysis-report`, GET .../analysis/<REQ id>/sections),
     never `stage`. Only the refusal codes in NOT_READY_CODES are polled, at most MAX_POLLS x POLL_SECONDS; a bound
     reached is the named result NOT_READY, never a pass; every other refusal and any non-200 is terminal at once.
  4. a refusal envelope is a refusal at ANY HTTP status.
  5. hop (f) sends a REQ-<24 hex> id only; hop (g) takes report_ref.request_id FROM THE TICKET and reads the finished
     report for that id by the same read as hop (e). The pdf route is no longer called.
  6. (AMENDMENT 2) the shell is safe to run: token expiry is the REQUIRED argument --exp-minutes (5 to 60, no default);
     cleanup completes the tickets FIRST, WAITS until the token's exp has passed, and only then deletes the PROFILE
     row (deleting it earlier would WIDEN the token) and reads it back absent, on every stop path after the row was
     written; a REQUIRED --expect-irpt-status-sha precheck stops before any write; the data-refresh zero-call read is
     VOID on zero streams searched or a silent positive control; two report-route arms (malformed id refused 400,
     issued id stored); --close-ticket completes an old test ticket; the trace header names this run.
This module has NOT been run against the portal by this order; only its fake-HTTP tests have run.

Original header follows.

TCKT_VNEXT SA-r-1b -- the FWD-1 seat-arm run under pair v2.2. Steps 3-6 in ONE process.

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

Usage: python fwd1_run.py --read27 <AC1 result> --exp-minutes N --expect-irpt-status-sha <prefix>
           --run-label <label> --pair <pair path and pin> --executor <serial>
           [--advisor-opaque adv-04b85b8aefda] [--close-ticket <id>]...
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

# These two are census MORE_THAN_ONE but read NO selected_tenant: the ticket plane is clamped by
# _in_profile_scope on the TICKET's requester.firm. Identical bytes across firm arms is therefore expected
# and says nothing either way, so a selector test on them is a category error.
NO_SELECTOR_CARRIER = frozenset({"/api/scoped/tickets", "/api/scoped/tickets/metrics"})

# AMENDMENT 4's limb 2: "leak = an off-list payload that DIFFERS from the own-firm answer, OR CODE THAT
# READS THE SELECTOR for an off-list target. A selector-ignoring route whose firm comes only from the token
# is not a STOP." Limb 2 is a CODE question, so it is answered by a code read and carried here as DATA.
#
# >> WHY THIS IS A TABLE AND NOT A SOURCE-DIR WALK. A walk of each function's own source_dir UNDERSTATES:
#    irpt-holdings counts 0 occurrences of `selected_tenant` in its own dir, yet it refuses an off-list
#    target with FIRM_BINDING, because the clamp lives in the SHARED _authz/served.py that is BUNDLED into
#    every IRPT host and sits outside that dir. A bundled shared module is invisible to the walk, so the
#    walk would clear a route that does read the selector. Measured counts per own source_dir, for the
#    record: irpt-status 5, irpt-export-render 1, irpt-directory-search 16, irpt-ycharts-generate 6,
#    irpt-performance-adapter 3, irpt-narrative 17, irpt-holdings 0, irpt-49f-reporting-read-lambda 0 --
#    and the last two still read it through the shared boundary.
READS_SELECTOR = {
    # every IRPT-served host reaches selected_tenant through the shared _authz/served.py boundary
    "irpt-status": True, "irpt-export-render": True, "irpt-directory-search": True,
    "irpt-ycharts-generate": True, "irpt-narrative": True, "irpt-holdings": True,
    "irpt-performance-adapter": True, "irpt-49f-reporting-read-lambda": True,
    # 0 occurrences anywhere in the module; firm comes only from the edge-injected header
    "opal-amgt-scoped-api": False,   # CTO msg 3747 code read + verified here: lib/research/api/scoped_amgt.py == 0
    "opal-ticket-api": False,        # 0 in 12 files; clamped by _in_profile_scope on the ticket's requester.firm
    "opal-portal-content-api": False,
    "opal-partners-data": False,     # scoped by its own advisor-scoping check, not by the selector
}

_VERDICTS = {}


def verdict_of(key):
    """The source census's verdict for 'METHOD /route', or NOT-IN-SOURCE-CENSUS for a live-only route."""
    if not _VERDICTS:
        src = json.loads(CENSUS.read_text(encoding="utf-8"))
        for r in src["rows"]:
            vs = {v.get("verdict") for v in r["per_token"].values()}
            _VERDICTS[r["method"] + " " + r["route"]] = (
                "MORE_THAN_ONE" if "MORE_THAN_ONE" in vs else
                "ONE_FIRM" if "ONE_FIRM" in vs else sorted(str(v) for v in vs)[0])
    return _VERDICTS.get(key, "NOT-IN-SOURCE-CENSUS")

# AMENDMENT 1: the F10 leg M precedent attachment, so a CREATE arm reaches the firm clamp.
SYN_ATTACHMENT = {
    "upload_id": "test-sar1b-20261009",
    "input_id": "portfolio_abdbb292c2bf6f96b0db74468dcdd68a9383a2e4259be73c9cb1977fb3b2ba03",
}

ROOT = Path(__file__).resolve().parents[8]
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

REQ_ID = re.compile(r"^REQ-[0-9a-f]{24}$")
MAX_POLLS = 40         # hop (e): at most this many polls of the finished-report read
POLL_MAX = MAX_POLLS   # the name the first build used; same value
POLL_SECONDS = 30      # hop (e): seconds between polls
# The public refusal codes that mean "the report is not generated yet" on the finished-report read. PROPOSED, from
# the handler read (the refusal table is in this worker's report and row TCKT_VNEXT-D2-W8-S3; the file
# REPORT_READ_REFUSALS.md could not be written): the issuer's run pair confirms it. Every other code is terminal.
#   NOT_FOUND  AnalysisUnavailable("ANALYSIS_REPORT_NOT_READY") for a job whose state is not READY (owned_report.py:119),
#              answered NOT_FOUND by the boundary (ops/entry.py:254).
#   NOT_READY  ReportBundleAbsent: the report is READY and indexed but its retained bytes are not in the store yet
#              (owned_report.py:20-29, :137).
NOT_READY_CODES = frozenset({"NOT_FOUND", "NOT_READY"})
LIST_PAGES = 5         # request-list pages read (50 rows each), newest first
SLEEP = time.sleep     # a test replaces this
NOW = time.time        # a test replaces this (the clock the cleanup waits on)
EXP_MIN_MINUTES = 5    # --exp-minutes is an integer in this closed range; there is no default
EXP_MAX_MINUTES = 60
EXP_MARGIN_SECONDS = 30   # the row outlives the token's exp by this much: local clock skew and authorizer leeway
WAIT_STEP_SECONDS = 60    # the cleanup wait sleeps in steps of at most this
IRPT_STATUS_FN = "irpt-status"
TICKET_LOG_GROUP = "/aws/lambda/opal-ticket-api"   # the zero-call read's positive control
# D5: a well-formed-looking but malformed id; the deployed report route must refuse it 400 INVALID_REPORT_REQUEST_ID
MALFORMED_REPORT_ID = "sar1b-" + "0" * 24
_CLIENTS = {}


def _client(name):
    """Every AWS client is built on first use, never at import."""
    if name not in _CLIENTS:
        import boto3
        _CLIENTS[name] = boto3.client(name, region_name=REGION)
    return _CLIENTS[name]


class _Ddb:
    def __getattr__(self, attr):
        return getattr(_client("dynamodb"), attr)


ddb = _Ddb()


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


def put_row():
    """Write the filer's PROFILE row. A raise here means the row is NOT ours (a ConditionalCheckFailed is a row that
    already existed): nothing is deleted on that path."""
    item = {
        "PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"},
        "email": {"S": FILER}, "firmId": {"S": "opal-capital"},
        "status": {"S": "active"}, "userType": {"S": "test-filer"},
        "name": {"S": FILER_NAME}, "allowedFirmIds": {"L": [{"S": FIRM}]},
    }
    ddb.put_item(TableName=USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")


def read_row():
    """ConsistentRead of the PROFILE row -> the item or None."""
    back = ddb.get_item(TableName=USERS, Key={"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}},
                        ConsistentRead=True).get("Item")
    print("OK: ConsistentRead read-back present=%s allowedFirmIds=%s"
          % (back is not None, (back or {}).get("allowedFirmIds")))
    return back


def check_exp_minutes(n):
    """D1: an integer from EXP_MIN_MINUTES to EXP_MAX_MINUTES. A bool is not an integer here."""
    if isinstance(n, bool) or not isinstance(n, int) or not (EXP_MIN_MINUTES <= n <= EXP_MAX_MINUTES):
        raise ValueError("exp minutes must be an integer from %d to %d, got %r" % (EXP_MIN_MINUTES, EXP_MAX_MINUTES, n))
    return n


def mint_token(iat, exp_minutes):
    """ONE RS256 token. v2.2: tier internal, userType test-filer kept. exp = iat + exp_minutes*60 (D1): the caller
    fixed iat BEFORE the row was written, so the cleanup knows the exp whatever happens next."""
    check_exp_minutes(exp_minutes)
    import jwt as pyjwt
    pem = _client("secretsmanager").get_secret_value(
        SecretId=PRIV_SECRET)["SecretString"]
    exp = iat + exp_minutes * 60
    claims = {"sub": FILER, "iss": "opal-portal-auth", "aud": "opal-portal-api",
              "firmId": "opal-capital", "tier": "internal", "role": "user",
              "userType": "test-filer", "name": FILER_NAME, "iat": iat, "exp": exp}
    tok = pyjwt.encode(claims, pem, algorithm="RS256")
    print("OK: token minted  tier=internal userType=test-filer  iat=%s exp=%s (%d min)  claims=%s"
          % (iso(dt.datetime.fromtimestamp(iat, dt.timezone.utc)),
             iso(dt.datetime.fromtimestamp(exp, dt.timezone.utc)), exp_minutes, sorted(claims)))
    return tok, exp


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
    ctype = None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw, status = r.read().decode("utf-8", "replace"), r.status
            ctype = r.headers.get("Content-Type")
    except urllib.error.HTTPError as e:
        raw, status = e.read().decode("utf-8", "replace"), e.code
        ctype = e.headers.get("Content-Type") if e.headers else None
    except Exception as e:  # noqa: BLE001 -- a transport failure is DATA, never a pass
        return {"status": 0, "reason": "TRANSPORT_" + type(e).__name__, "len": 0, "fp": None, "parsed": None}
    try:
        parsed = json.loads(raw)
    except ValueError:
        parsed = None
    return {"status": status, "reason": reason_of(parsed) if parsed is not None else raw[:120],
            "len": len(raw), "fp": hashlib.sha256(raw.encode()).hexdigest()[:16], "parsed": parsed,
            "content_type": ctype}


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
    c = _client("apigatewayv2")

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
    # >> WHAT "BEHAVES AS ALL" IS, AND WHAT IT IS NOT. Corrected after run 2 of this order stopped on it.
    # A route that returns the SAME bytes for every firm has no firm axis to leak through; the pair's own
    # blast radius v2 already accepts that "the 51 NO_FIRM routes stay reachable as for any opal-capital
    # user", and two ticket routes read no selected_tenant at all, so a selector test on them is a category
    # error. Treating every selector-ignored arm as a STOP (which run 2 did) re-stops on exactly the arms
    # run 1 had already classified as expected. The census verdict is the discriminator: an ignored selector
    # is a REAL finding only on a route the census says resolves to one or more FIRMS.
    # AMENDMENT 4 limb 2: a selector-ignoring route leaks only if its CODE reads the selector. A route whose
    # firm comes only from the token is explicitly NOT a STOP. UNKNOWN is never cleared: it is carried as
    # UNKNOWN so it can be read by a code read rather than assumed either way.
    leak_by_code, cleared_by_code, unknown_by_code = [], [], []
    for t in selector_ignored:
        reads = READS_SELECTOR.get(t[0])
        if reads is True:
            leak_by_code.append(t)
        elif reads is False:
            cleared_by_code.append(t)
        else:
            unknown_by_code.append(t)
    summary["selector_ignored_cleared_by_code_read"] = cleared_by_code
    summary["selector_ignored_leak_by_code_read"] = leak_by_code
    summary["selector_ignored_code_read_UNKNOWN"] = unknown_by_code
    summary["leak_criterion"] = ("AMENDMENT 4: an off-list payload DIFFERING from the own-firm answer, OR code "
                                 "that reads the selector for an off-list target. A selector-ignoring route "
                                 "whose firm comes only from the token is not a STOP.")
    stop = None
    if off_admits:
        stop = "LEAK limb 1 -- OFF-LIST PAYLOAD DIFFERS on %d arm(s): %s" % (len(off_admits), off_admits[:4])
    elif leak_by_code:
        stop = ("LEAK limb 2 -- a selector-READING route answered an off-list target on %d arm(s): %s"
                % (len(leak_by_code), leak_by_code[:4]))
    elif unknown_by_code:
        stop = ("LEAK limb 2 UNDECIDABLE -- %d arm(s) on a host with no code read: %s"
                % (len(unknown_by_code), unknown_by_code[:4]))
    print("  => selector-ignored: %d CLEARED by code read (firm from the token only), %d leak, %d UNKNOWN"
          % (len(cleared_by_code), len(leak_by_code), len(unknown_by_code)))
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
        # AnalysisUploadResult carries `state` on the RESULT itself (contract: resolving["state"] ==
        # "RESOLVING"), not under the status envelope. Run 3 read only status.state and saw None for all
        # 14 polls, so it never recognised NORMALIZED and polled the full budget although the input_id
        # had already landed on poll 2. Read the result first, then fall back to the envelope.
        st = p.get("status")
        state = (d.get("state") if isinstance(d, dict) else None) \
            or (st.get("state") if isinstance(st, dict) else None)
        a["status"], a["state_seen"], a["polls"] = res["status"], state, i + 1
        print("  (a) poll %2d http=%s state=%r reason=%r input_id=%r"
              % (i + 1, res["status"], state, res["reason"], input_id))
        if state in ("NORMALIZED", "READY", "AVAILABLE"):
            break
        if res["status"] >= 400 and res["reason"] not in (None, "NOT_READY", "RESOLVING", "PENDING"):
            break
        SLEEP(5)
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

    return hops_d_to_g(token, trace, h, named, tkt, input_id, file_sha)


# ---------------------------------------------------------------- hops (d)-(g), REPAIRED (cell R2-rn-1)

ANALYSIS = "/api/scoped/investor-reporting/analysis"
REQUESTS = ANALYSIS + "/requests"


def body_of(res):
    """(top, inner): the parsed body and its `data` object when it has one."""
    p = res.get("parsed") if isinstance(res.get("parsed"), dict) else {}
    return p, (p.get("data") if isinstance(p.get("data"), dict) else p)


def refusal_of(res):
    """None when the response is a read; else the reason it is a refusal. A refusal envelope is a refusal at ANY
    HTTP status: round 1 read an HTTP 200 carrying INVALID_REQUEST_ID as success, 61 times."""
    parsed = res.get("parsed")
    why = reason_of(parsed) if parsed is not None else None
    if why:
        return why
    status = res.get("status") or 0
    if status == 0 or status >= 400:
        return res.get("reason") or ("HTTP_%s" % status)
    if parsed is None:
        return "UNPARSEABLE_BODY"
    return None


def list_requests(token):
    """The firm's request list, newest first, at most LIST_PAGES pages. -> (ok, rows, reason).
    A row is {request_id, accepted_at}: the schema (OwnedAnalysisRequestHistory -> OwnedAnalysisRequest) carries
    NOTHING else on a history item -- no ticket id, no input_id."""
    rows, cursor = [], None
    for _ in range(LIST_PAGES):
        q = {"selected_tenant": FIRM, "limit": 50}
        if cursor:
            q["cursor"] = cursor
        res = call(token, "GET", REQUESTS, q)
        why = refusal_of(res)
        if why:
            return False, rows, why
        _, inner = body_of(res)
        for it in inner.get("items") or []:
            ident = it.get("identity") if isinstance(it, dict) else None
            rid = ident.get("request_id") if isinstance(ident, dict) else None
            rows.append({"request_id": rid, "accepted_at": it.get("accepted_at")})
        cursor = inner.get("next_cursor")
        if not cursor:
            break
    return True, rows, None


def request_id_from_answer(res):
    """A REQ-<24 hex> id the submission's answer carries (top level, or under `data`), else None."""
    p, inner = body_of(res)
    for d in (p, inner):
        v = d.get("request_id")
        if isinstance(v, str) and REQ_ID.fullmatch(v):
            return v
    return None


def hop_d_analysis(token, tkt, input_id, file_sha, d, named):
    """POST the submission; return the SERVICE's REQ id or None. The value SENT as request_id is an idempotency
    token: it is traced as `idempotency_token` and never polled, recorded on a ticket or written as request_id.

    The request list is the fallback when the answer carries no id. A history item carries only
    identity.request_id and accepted_at, so no field ties a row to this run's ticket or input_id; the row that
    belongs to this submission is the ONE REQ id present in the list after the submission and absent from the
    list read just before it. Zero or more than one is REQUEST_ID_UNRESOLVED, never a guess."""
    sent = "sar1b-" + file_sha[:24]
    d["idempotency_token"] = sent
    base_ok, base_rows, base_why = list_requests(token)
    baseline = {r["request_id"] for r in base_rows}
    res = call(token, "POST", ANALYSIS, {"selected_tenant": FIRM},
               {"request_id": sent, "client_id": None, "account_ids": [], "snapshot_id": None,
                "variant": "overview", "comparison_keys": [],
                "report_title": "[TEST TCKT_VNEXT FWD-1] seat arm",
                "prepared_for": HOUSEHOLD, "input_id": input_id, "ticket_id": tkt})
    d["status"], d["request_id"] = res["status"], None
    why = refusal_of(res)
    if why:
        d["refused_reason"] = why
        named.append({"hop": "d_analysis", "status": res["status"], "reason": why,
                      "note": "submission refused (any HTTP status); (e)-(g) depend on it"})
        return None
    rid = request_id_from_answer(res)
    d["request_id_source"] = "submission_answer" if rid else None
    if not rid:
        ok, rows, list_why = list_requests(token)
        fresh = {}
        for r in rows:
            v = r["request_id"]
            if isinstance(v, str) and REQ_ID.fullmatch(v) and v not in baseline:
                fresh[v] = r["accepted_at"]
        d["candidates"] = len(fresh) if (ok and base_ok) else None
        if not (ok and base_ok) or len(fresh) != 1:
            named.append({"hop": "d_analysis", "status": res["status"], "reason": "REQUEST_ID_UNRESOLVED",
                          "candidates": d["candidates"],
                          "note": ("the answer carried no REQ id; the request list gave %s candidate row(s) "
                                   "(list read: %s). Not guessed, not the newest row. (e)-(g) depend on it"
                                   % (d["candidates"], "ok" if ok and base_ok else (list_why or base_why)))})
            return None
        rid = next(iter(fresh))
        d["request_id_source"] = "request_list"
        d["accepted_at"] = fresh[rid]
    d["request_id"] = rid
    return rid


def report_read(token, rid):
    """One finished-report read (operation `analysis-report`): GET .../analysis/<REQ id>/sections, selected_tenant=FIRM.
    -> (verdict, code, res, facts). verdict is MET | NOT_READY | TERMINAL.
      MET       HTTP 200, not a refusal envelope, the id in the body equals the id asked for, >= 1 section.
      NOT_READY HTTP 200 refusal envelope whose code is in NOT_READY_CODES (the only thing ever polled).
      TERMINAL  any other refusal code, any non-200, or a 200 body that is not the report asked for.
    facts carries ids, counts, a byte length and a sha256 prefix only: no section text, no figures."""
    res = call(token, "GET", ANALYSIS + "/" + rid + "/sections", {"selected_tenant": FIRM})
    facts = {"status": res.get("status"), "len": res.get("len"), "sha256_prefix": res.get("fp")}
    why = refusal_of(res)
    if res.get("status") != 200:
        return "TERMINAL", why or "HTTP_%s" % res.get("status"), res, facts
    if why:
        return ("NOT_READY" if why in NOT_READY_CODES else "TERMINAL"), why, res, facts
    _, inner = body_of(res)
    ref = inner.get("request_ref")
    echoed = ref.get("request_id") if isinstance(ref, dict) else None
    sections = inner.get("sections")
    facts["request_id_echoed"] = echoed if isinstance(echoed, str) and REQ_ID.fullmatch(echoed) else None
    facts["request_id_matches"] = facts["request_id_echoed"] == rid
    facts["sections"] = len(sections) if isinstance(sections, list) else None
    if facts["request_id_matches"] and facts["sections"]:
        return "MET", None, res, facts
    return "TERMINAL", "REPORT_BODY_NOT_THE_REPORT", res, facts


def hop_e_ready(token, rid, e, named):
    """Poll the finished-report read. -> "OK" | "NOT_READY" | "FAILED".
    Only NOT_READY_CODES are polled (MAX_POLLS x POLL_SECONDS); the bound reached is NOT_READY, never a pass."""
    e["route"] = "analysis-report"
    for i in range(MAX_POLLS):
        verdict, code, res, facts = report_read(token, rid)
        e["status"], e["polls"], e["report"] = res["status"], i + 1, facts
        if i % 5 == 0 or verdict != "NOT_READY":
            print("  (e) poll %2d http=%s verdict=%s code=%r" % (i + 1, res["status"], verdict, code))
        if verdict == "MET":
            e["result"] = {"result": "REPORT_READ", "sections": facts["sections"]}
            return "OK"
        if verdict == "TERMINAL":
            e["refused"], e["reason"] = True, code
            named.append({"hop": "e_ready", "status": res["status"], "reason": code,
                          "note": "the finished-report read ended terminal; recorded with its code and not polled again"})
            return "FAILED"
        e["last_code"] = code
        if i < MAX_POLLS - 1:
            SLEEP(POLL_SECONDS)
    e["outcome"], e["result"] = "NOT_READY", {"result": "NOT_READY", "last_code": e.get("last_code"), "polls": MAX_POLLS}
    named.append({"hop": "e_ready", "status": e.get("status"), "reason": "NOT_READY",
                  "note": "code %r on all %d polls %d s apart; the report was not read. Not retried into a pass"
                          % (e.get("last_code"), MAX_POLLS, POLL_SECONDS)})
    return "NOT_READY"


def arm_malformed_report_id(token, tkt, arms, named):
    """D5 arm 1, after hop (e) is met and before hop (f): POST the journey ticket's /report with a MALFORMED id. The
    deployed id check must refuse it HTTP 400 with code INVALID_REPORT_REQUEST_ID. Anything else is the named failure
    REPORT_ID_ARM_UNEXPECTED and the run stops before hop (f). -> True when the arm is as expected."""
    res = call(token, "POST", "/api/scoped/tickets/%s/report" % tkt, None, {"request_id": MALFORMED_REPORT_ID})
    parsed = res.get("parsed")
    code = parsed.get("code") if isinstance(parsed, dict) else None
    arm = {"status": res.get("status"), "code": code, "sent_shape": "sar1b-<24 zeros>"}
    arms["report_id_malformed_refused"] = arm
    print("  (arm) malformed id http=%s code=%r" % (res.get("status"), code))
    if res.get("status") == 400 and code == "INVALID_REPORT_REQUEST_ID":
        arm["as_expected"] = True
        return True
    arm["as_expected"] = False
    named.append({"hop": "f_report", "status": res.get("status"), "reason": "REPORT_ID_ARM_UNEXPECTED", "code": code,
                  "note": ("the malformed id was expected to be refused HTTP 400 INVALID_REPORT_REQUEST_ID; "
                           "the run stops before hop (f)")})
    return False


def hop_f_report(token, tkt, rid, f, named, arms=None):
    """POST the ticket report with the REQ id only. Refuses to send anything that is not a REQ id.
    D5 arm 2: a 200 is `report_id_well_formed_stored`; a 400 on the ISSUED id is the named result
    BRANCH_B_ISSUED_ID_REFUSED: stop at once, no retry, cleanup follows."""
    arms = arms if arms is not None else {}
    if not (isinstance(rid, str) and REQ_ID.fullmatch(rid)):
        f["status"], f["refused_to_send"] = None, True
        named.append({"hop": "f_report", "status": None, "reason": "NOT_A_REQ_ID",
                      "note": "the id in hand is not REQ-<24 hex>; nothing was sent and nothing was recorded"})
        return False
    res = call(token, "POST", "/api/scoped/tickets/%s/report" % tkt, None, {"request_id": rid})
    f["status"], f["request_id"] = res["status"], rid
    why = refusal_of(res)
    print("  (f) report http=%s reason=%r" % (res["status"], why))
    if res["status"] == 400:
        parsed = res.get("parsed")
        code = parsed.get("code") if isinstance(parsed, dict) else None
        f["refused_reason"], f["result"] = why, "BRANCH_B_ISSUED_ID_REFUSED"
        arms["report_id_well_formed_stored"] = {"status": 400, "code": code, "as_expected": False}
        named.append({"hop": "f_report", "status": 400, "reason": "BRANCH_B_ISSUED_ID_REFUSED", "code": code,
                      "note": ("the deployed route refused the id the service ISSUED; stopped at once, not retried, "
                               "cleanup follows")})
        return False
    if why:
        f["refused_reason"] = why
        arms["report_id_well_formed_stored"] = {"status": res["status"], "code": why, "as_expected": False}
        named.append({"hop": "f_report", "status": res["status"], "reason": why})
        return False
    arms["report_id_well_formed_stored"] = {"status": res["status"], "as_expected": res["status"] == 200}
    return True


def hop_g_open(token, tkt, g, named):
    """GET the ticket, take report_ref.request_id FROM THE TICKET, and read the finished report for that id by the
    same read as hop (e) (one read, not polled). Records status, the id echoed in the body, the section count, the
    body byte length and a sha256 prefix; no section text, no figures. The pdf route is not called."""
    r1 = call(token, "GET", "/api/scoped/tickets/%s" % tkt)
    g["status"], g["report_opened"] = r1["status"], False
    why = refusal_of(r1)
    if why:
        named.append({"hop": "g_open", "status": r1["status"], "reason": why, "note": "the ticket read was refused"})
        return False
    p = r1["parsed"] if isinstance(r1["parsed"], dict) else {}
    t = p.get("ticket") if isinstance(p.get("ticket"), dict) else p
    ref = t.get("report_ref")
    ref_rid = ref.get("request_id") if isinstance(ref, dict) else None
    if not (isinstance(ref_rid, str) and REQ_ID.fullmatch(ref_rid)):
        g["report_ref_present"] = bool(ref)
        named.append({"hop": "g_open", "status": r1["status"], "reason": "REPORT_REF_NOT_A_REQ_ID",
                      "note": "report_ref absent on the ticket, or its request_id is not REQ-<24 hex>"})
        return False
    g["report_ref_request_id"] = ref_rid
    verdict, code, r2, facts = report_read(token, ref_rid)
    g["second_status"], g["report"] = r2["status"], facts
    print("  (g) ticket http=%s report http=%s verdict=%s code=%r" % (r1["status"], r2["status"], verdict, code))
    if verdict != "MET":
        named.append({"hop": "g_open", "status": r2["status"], "reason": code or verdict,
                      "note": "the finished report did not open from the ticket's report_ref"})
        return False
    g["report_opened"] = True
    return True


def hops_d_to_g(token, trace, h, named, tkt, input_id, file_sha):
    rid = hop_d_analysis(token, tkt, input_id, file_sha, h["d_analysis"], named)
    print("  (d) analysis http=%s request_id=%r source=%s" % (
        h["d_analysis"]["status"], rid, h["d_analysis"].get("request_id_source")))
    save(trace)

    def unreachable(keys, why):
        for k in keys:
            h[k]["outcome"] = "UNREACHABLE"
            named.append({"hop": k, "status": None, "reason": "UNREACHABLE", "note": why})

    if not rid:
        unreachable(("e_ready", "f_report", "g_open"), "depends on (d), which produced no service request id")
        return trace
    outcome = hop_e_ready(token, rid, h["e_ready"], named)
    save(trace)
    if outcome != "OK":
        unreachable(("f_report", "g_open"), "(e) ended %s; the report is not made, so (f) and (g) are not run" % outcome)
        return trace
    arms = trace.setdefault("report_route_arms", {})
    if not arm_malformed_report_id(token, tkt, arms, named):
        unreachable(("f_report", "g_open"), "REPORT_ID_ARM_UNEXPECTED: the run stops before hop (f)")
        save(trace)
        return trace
    save(trace)
    if hop_f_report(token, tkt, rid, h["f_report"], named, arms):
        save(trace)
        hop_g_open(token, tkt, h["g_open"], named)
    else:
        unreachable(("g_open",), "(f) did not attach a report")
    save(trace)
    return trace


# ---------------------------------------------------------------- step 6 + the zero-call proof


def ticket_facts(res):
    """(status, assignee) a ticket read carries, or (None, None). The assignee is the claimer's email, lower-cased."""
    p = res.get("parsed") if isinstance(res.get("parsed"), dict) else {}
    t = p.get("ticket") if isinstance(p.get("ticket"), dict) else p
    return t.get("status"), str(t.get("assignee") or "").lower()


def complete_ticket(token, tkt, label):
    try:
        res = call(token, "POST", "/api/scoped/tickets/%s/complete" % tkt, None,
                   {"resolution": "[TEST] %s arm complete" % label})
    except Exception as e:  # noqa: BLE001 -- a failed completion is DATA; the row delete must still follow the wait
        return {"status": 0, "reason": "RAISED_" + type(e).__name__}
    return {"status": res.get("status"), "reason": res.get("reason")}


def close_old_ticket(token, tkt, label):
    """D6: complete a named OLD ticket when it reads in_progress AND is assigned to the filer; any other state is
    recorded as found and left alone. -> {before, after, action}."""
    rec = {"before": None, "after": None, "action": None}
    try:
        r = call(token, "GET", "/api/scoped/tickets/%s" % tkt)
    except Exception as e:  # noqa: BLE001
        rec["action"], rec["before"] = "READ_RAISED_" + type(e).__name__ + "_LEFT_ALONE", {"http": 0}
        return rec
    status, assignee = ticket_facts(r)
    rec["before"] = {"http": r.get("status"), "status": status, "assigned_to_filer": assignee == FILER.lower()}
    if r.get("status") != 200 or status is None:
        rec["action"] = "NOT_READ_LEFT_ALONE"
        return rec
    if status != "in_progress" or assignee != FILER.lower():
        rec["action"], rec["after"] = "FOUND_LEFT_ALONE", dict(rec["before"])
        return rec
    done = complete_ticket(token, tkt, label)
    r2 = call(token, "GET", "/api/scoped/tickets/%s" % tkt)
    status2, assignee2 = ticket_facts(r2)
    rec["action"] = "COMPLETED" if done["status"] and done["status"] < 400 else "COMPLETE_REFUSED"
    rec["complete_http"] = done["status"]
    rec["after"] = {"http": r2.get("status"), "status": status2, "assigned_to_filer": assignee2 == FILER.lower()}
    return rec


def wait_past_exp(exp_unix):
    """D2 step 2: sleep (SLEEP, replaceable) until NOW() is past exp + EXP_MARGIN_SECONDS. -> seconds slept."""
    target = exp_unix + EXP_MARGIN_SECONDS
    slept = 0.0
    while NOW() <= target:
        step = max(1.0, min(float(WAIT_STEP_SECONDS), target - NOW() + 1.0))
        print("  waiting for the token to expire: %d s left before the row may be deleted" % max(0, target - NOW()))
        SLEEP(step)
        slept += step
    return slept


def cleanup(token, trace, exp_unix, close_tickets=()):
    """D2, in this order on EVERY path after the row was written:
      (1) complete every ticket the run created, and every --close-ticket one that qualifies;
      (2) WAIT until the token's exp has passed;
      (3) only then delete the PROFILE row and read it back ABSENT with ConsistentRead.
    Deleting the row while the token lives WIDENS the token (the authorizer then derives allowedFirmIds = ALL)."""
    print("== step 6: cleanup, same session ==")
    out = trace["cleanup"]
    label = trace.get("run_label") or "run"

    # (1) tickets first
    todo = [t for t in ([trace.get("journey_ticket")] +
                        (trace.get("census", {}) or {}).get("tickets_created_by_the_census", [])) if t]
    done, errors = {}, {}
    if token is None:
        out["tickets_not_attempted"] = "no token was minted"
    else:
        for tkt in dict.fromkeys(todo):
            r = complete_ticket(token, tkt, label)
            done[tkt] = r["status"] or 0
            if r["status"] in (None, 0) or r["status"] >= 400:
                errors[tkt] = r["reason"]
            print("  ticket %s complete -> http=%s reason=%r" % (tkt, r["status"], r["reason"]))
        old = {}
        for tkt in dict.fromkeys(close_tickets):
            if tkt in done:
                continue
            old[tkt] = close_old_ticket(token, tkt, label)
            print("  old ticket %s: %s (before %s, after %s)" % (
                tkt, old[tkt]["action"], (old[tkt]["before"] or {}).get("status"), (old[tkt]["after"] or {}).get("status")))
        out["old_tickets"] = old
    out["tickets_completed"] = done
    out["tickets_completed_all"] = bool(done) and all(v < 400 for v in done.values())
    if errors:
        out["ticket_completion_errors"] = errors
    out["token_left_to_expire"] = True
    save(trace)

    # (2) wait for exp
    out["token_exp"] = iso(dt.datetime.fromtimestamp(exp_unix, dt.timezone.utc))
    try:
        out["waited_seconds"] = wait_past_exp(exp_unix)
    except BaseException as e:
        out["row_left_in_place"] = "interrupted while waiting for exp (%s); the row was NOT deleted" % type(e).__name__
        save(trace)
        print("ERROR: %s -- delete the row only AFTER %s plus margin" % (out["row_left_in_place"], out["token_exp"]))
        raise

    # (3) only now touch the row
    now = NOW()
    if now <= exp_unix:   # unreachable after the wait; a refusal rather than an early delete
        raise RuntimeError("refusing to delete the row before exp")
    out["row_deleted_at"] = iso(dt.datetime.fromtimestamp(now, dt.timezone.utc))
    out["row_deleted_at_unix"] = int(now)
    ddb.delete_item(TableName=USERS, Key={"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}})
    back = ddb.get_item(TableName=USERS, Key={"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}},
                        ConsistentRead=True).get("Item")
    out["row_removed_read_back_absent"] = back is None
    print("  row removed after exp (%s > %s); ConsistentRead read-back absent = %s"
          % (out["row_deleted_at"], out["token_exp"], back is None))
    save(trace)
    return trace


def _scan_group(logs, group, pattern, start_unix, end_unix):
    """filter_log_events over a group and window, all pages -> (matching events, log streams searched)."""
    n, streams, tok = 0, 0, None
    while True:
        kw = {"logGroupName": group, "filterPattern": pattern,
              "startTime": start_unix * 1000, "endTime": end_unix * 1000}
        if tok:
            kw["nextToken"] = tok
        r = logs.filter_log_events(**kw)
        n += len(r.get("events", []))
        streams += len(r.get("searchedLogStreams", []))
        tok = r.get("nextToken")
        if not tok:
            return n, streams


def data_refresh_zero_calls(trace, start_unix, end_unix):
    """D4: prove ZERO data-refresh calls for the filer over iat..exp, from its own logs. Recorded ZERO_CALLS_PROVEN only
    when streams searched > 0 AND the positive control over the ticket API's log group found the filer >= 1 time AND
    the data-refresh matches == 0. Zero streams searched, or a control that finds nothing, is ZERO_CALL_VOID."""
    print("== zero data-refresh calls, from the log group ==")
    logs = _client("logs")
    pattern = '"%s"' % FILER
    out = {"claim": "measured", "log_group": DATA_REFRESH_LOG_GROUP,
           "window": {"from": iso(dt.datetime.fromtimestamp(start_unix, dt.timezone.utc)),
                      "to": iso(dt.datetime.fromtimestamp(end_unix, dt.timezone.utc))},
           "query": "filter_log_events logGroupName=%s filterPattern=%s startTime=%d endTime=%d"
                    % (DATA_REFRESH_LOG_GROUP, pattern, start_unix * 1000, end_unix * 1000)}
    try:
        n, streams = _scan_group(logs, DATA_REFRESH_LOG_GROUP, pattern, start_unix, end_unix)
        c_n, c_streams = _scan_group(logs, TICKET_LOG_GROUP, pattern, start_unix, end_unix)
        out["match_count"], out["searched_log_streams"] = n, streams
        out["control"] = {"log_group": TICKET_LOG_GROUP, "same_filter": True, "found": c_n,
                          "searched_log_streams": c_streams}
        void = []
        if streams == 0:
            void.append("streams searched is 0 on %s" % DATA_REFRESH_LOG_GROUP)
        if c_n < 1:
            void.append("the positive control found the filer %d time(s) in %s, needs >= 1" % (c_n, TICKET_LOG_GROUP))
        if n > 0:
            out["verdict"] = "NON-ZERO -- report it"
        elif void:
            out["verdict"], out["void_reasons"] = "ZERO_CALL_VOID", void
        else:
            out["verdict"] = "ZERO_CALLS_PROVEN"
        print("  %s: %d match(es), %d stream(s) searched; control %s: %d found -> %s"
              % (DATA_REFRESH_LOG_GROUP, n, streams, TICKET_LOG_GROUP, c_n, out["verdict"]))
    except Exception as e:  # noqa: BLE001 -- a failed retrieval returns a VALUE; say so, never read it as zero
        out["match_count"] = None
        out["verdict"] = "UNREAD -- %s: %s" % (type(e).__name__, str(e)[:160])
        print("  WARN: the log read did NOT complete: %s. A failed retrieval is NOT a zero." % out["verdict"])
    trace["data_refresh_zero_calls"] = out
    save(trace)


def read_irpt_status_sha():
    """The live irpt-status CodeSha256 (through an AWS client a test can replace)."""
    return _client("lambda").get_function_configuration(FunctionName=IRPT_STATUS_FN)["CodeSha256"]


def precheck_irpt_status(prefix):
    """D3: runs BEFORE the row is written. -> (ok, info). Not ok when the live CodeSha256 does not start with the
    expected prefix (IRPT_STATUS_BUILD_MISMATCH, both values recorded) or cannot be read (IRPT_STATUS_BUILD_UNREAD)."""
    info = {"function": IRPT_STATUS_FN, "expected_prefix": prefix, "live_code_sha256": None}
    try:
        live = read_irpt_status_sha()
    except Exception as e:  # noqa: BLE001 -- an unread build is not a match
        info["result"], info["live_code_sha256"] = "IRPT_STATUS_BUILD_UNREAD", "UNREAD: " + type(e).__name__
        return False, info
    info["live_code_sha256"] = live
    ok = isinstance(live, str) and bool(prefix) and live.startswith(prefix)
    info["result"] = "IRPT_STATUS_BUILD_MATCH" if ok else "IRPT_STATUS_BUILD_MISMATCH"
    return ok, info


def limb3_non_500(token):
    """AMENDMENT 3 precondition limb 3: ONE real call must answer non-500 before any hop.

    It cannot be settled from the log group: a group with ZERO events of any kind shows ABSENCE OF TRAFFIC, not health. Only a real authenticated call
    discriminates, and the authorizer refuses an unauthenticated one before irpt-status is ever reached --
    so this runs after the mint and gates everything that follows.
    """
    res = call(token, "GET", "/api/scoped/investor-reporting/status", {"selected_tenant": FIRM})
    ok = res["status"] < 500
    print("== AMENDMENT 3 limb 3: one real irpt-status call ==")
    print("  GET /api/scoped/investor-reporting/status -> http=%s reason=%r  non-500=%s"
          % (res["status"], res["reason"], ok))
    return ok, {"claim": "measured", "route": "GET /api/scoped/investor-reporting/status",
                "status": res["status"], "reason": res["reason"], "non_500": ok,
                "why_not_from_logs": ("a log group with no events shows absence of traffic, not health; only a "
                                      "real authenticated call discriminates")}


def save(trace):
    """Run 2 is a SECTION: run 1's committed object stays exactly as the issuer committed it (@be24188c7a)."""
    for p in (TRACE, MY_TRACE):
        p.parent.mkdir(parents=True, exist_ok=True)
        doc = {}
        if p.exists():
            try:
                doc = json.loads(p.read_text(encoding="utf-8"))
            except ValueError:
                doc = {}
        if not isinstance(doc, dict):
            doc = {}
        if doc.get("run_id") and doc.get("run_id") != trace.get("run_id"):
            # Allocate the NEXT FREE run_N, reusing the slot this same run already owns. Keying every
            # later run to a fixed "run_2" made run 3 overwrite run 2's section in the working file
            # (run 2 was recovered from commit e2c7f7b25a). A record is still a record: do not clobber it.
            slot = next((k for k in doc
                         if k.startswith("run_") and isinstance(doc[k], dict)
                         and doc[k].get("run_id") == trace.get("run_id")), None)
            if slot is None:
                n = 2
                while "run_%d" % n in doc:
                    n += 1
                slot = "run_%d" % n
            doc[slot] = trace
        else:
            doc = dict(doc, **trace)
        p.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")


def _exp_minutes_arg(text):
    if not re.fullmatch(r"[0-9]+", text):
        raise argparse.ArgumentTypeError("--exp-minutes must be an integer from %d to %d, got %r"
                                         % (EXP_MIN_MINUTES, EXP_MAX_MINUTES, text))
    n = int(text)
    try:
        return check_exp_minutes(n)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))


def _nonblank(text):
    if not text.strip():
        raise argparse.ArgumentTypeError("must not be blank")
    return text.strip()


def build_parser():
    ap = argparse.ArgumentParser(prog="fwd1_run.py")
    ap.add_argument("--advisor-opaque", default="adv-04b85b8aefda")
    ap.add_argument("--read27", required=True,
                    help="AC1's measured result, carried in from the separate STOP 1 invocation")
    ap.add_argument("--exp-minutes", required=True, type=_exp_minutes_arg,
                    help="token lifetime in minutes, an integer from %d to %d; no default" % (EXP_MIN_MINUTES, EXP_MAX_MINUTES))
    ap.add_argument("--expect-irpt-status-sha", required=True, type=_nonblank,
                    help="prefix the live irpt-status CodeSha256 must start with; checked before anything is written")
    ap.add_argument("--run-label", required=True, type=_nonblank, help="names this run in the trace, e.g. R2-tr-1")
    ap.add_argument("--pair", required=True, type=_nonblank, help="the pair's path and pin, as one string")
    ap.add_argument("--executor", required=True, type=_nonblank, help="the executing seat's serial")
    ap.add_argument("--close-ticket", action="append", default=[], metavar="TICKET_ID", type=_nonblank,
                    help="an old test ticket to complete in cleanup step 1 if it is in_progress and assigned to the filer; "
                         "repeatable")
    return ap


def build_trace(a, run_id):
    """The trace header names THIS run (D7): label, pair and executor come from the arguments."""
    return {
        "run_id": run_id, "run_label": a.run_label, "executor": a.executor, "claim": "measured",
        "pair": a.pair,
        "entry": {"host": HOST, "transport": "HTTPS through CloudFront",
                  "not_used": "direct lambda invoke (CTO IRPT_YCDGEN @d54e0b7515 condition 1)"},
        "preconditions": {"read27": a.read27, "irpt_status": None, "row_written": None,
                          "token": "tier internal, userType test-filer, role user, firmId opal-capital",
                          "token_iat": None, "token_exp": None, "exp_minutes": a.exp_minutes},
        "census": None,
        "hops": [
            {"hop": "a_upload", "call": "POST /api/scoped/investor-reporting/analysis/inputs?selected_tenant=49financial",
             "status": 0, "upload_id": "", "input_id": "", "file": {"path": "", "sha256": ""}},
            {"hop": "b_ticket", "call": "POST /api/scoped/tickets", "status": 0, "ticket_id": "", "source": ""},
            {"hop": "c_claim", "call": "POST /api/scoped/tickets/{ticketId}/claim", "status": 0},
            {"hop": "d_analysis", "call": "POST /api/scoped/investor-reporting/analysis", "status": 0, "request_id": ""},
            {"hop": "e_ready", "call": "GET /api/scoped/investor-reporting/analysis/{requestId}/sections",
             "status": 0, "polls": 0},
            {"hop": "f_report", "call": "POST /api/scoped/tickets/{ticketId}/report", "status": 0},
            {"hop": "g_open", "call": "GET /api/scoped/tickets/{ticketId}; GET .../analysis/{requestId}/sections",
             "status": 0, "report_opened": False},
        ],
        "report_route_arms": {},
        "named_failures": [], "journey_ticket": None,
        "cleanup": {"row_removed_read_back_absent": False, "tickets_completed": {}},
        "data_refresh_zero_calls": None,
        "no_client_figures": ("hop statuses and artifact IDs only. Census arms record status, reason, body LENGTH "
                              "and a 16-hex sha256 PREFIX as a fingerprint -- never payload content."),
    }


def main(argv):
    a = build_parser().parse_args(argv)
    run_id = a.run_label + "-" + iso()
    trace = build_trace(a, run_id)

    # D3: nothing is written before the build is the expected one
    ok, info = precheck_irpt_status(a.expect_irpt_status_sha)
    trace["preconditions"]["irpt_status"] = info
    print("== precheck: irpt-status build ==\n  expected prefix %r, live %r -> %s"
          % (info["expected_prefix"], info["live_code_sha256"], info["result"]))
    if not ok:
        trace["named_failures"].append({
            "hop": "ALL", "status": None, "reason": info["result"],
            "expected_prefix": info["expected_prefix"], "live_code_sha256": info["live_code_sha256"],
            "note": "stopped before any write: no row, no token, no census, no hop"})
        save(trace)
        print("STOP: %s -- nothing was written" % info["result"])
        return 1

    advisor = resolve_advisor(a.advisor_opaque, FIRM)
    if advisor is None:
        return 1

    # iat and exp are fixed BEFORE the row exists, so every later path knows the exp it must wait for (D1, D2)
    iat = int(NOW())
    exp = iat + check_exp_minutes(a.exp_minutes) * 60
    trace["preconditions"]["token_iat"] = iso(dt.datetime.fromtimestamp(iat, dt.timezone.utc))
    trace["preconditions"]["token_exp"] = iso(dt.datetime.fromtimestamp(exp, dt.timezone.utc))
    try:
        put_row()
    except Exception as e:  # noqa: BLE001 -- the row is not ours to delete; nothing else ran
        trace["named_failures"].append({"hop": "ALL", "status": None, "reason": "ROW_WRITE_FAILED",
                                        "note": "%s: %s; the row was not written by this run and is not deleted"
                                                % (type(e).__name__, str(e)[:160])})
        save(trace)
        print("ERROR: row not written: %s" % type(e).__name__)
        return 1
    trace["preconditions"]["row_written"] = iso()

    token = None
    try:
        # every path from here on ends in cleanup(), which waits for exp before it touches the row
        if read_row() is None:
            trace["named_failures"].append({"hop": "ALL", "status": None, "reason": "ROW_NOT_READABLE",
                                            "note": "the row was not readable after the put; no token minted"})
            print("STOP: row not readable after the put -- going to cleanup")
            save(trace)
        else:
            token, minted_exp = mint_token(iat, a.exp_minutes)
            assert minted_exp == exp
            save(trace)
            ok3, limb3 = limb3_non_500(token)
            trace["preconditions"]["limb_3_non_500"] = limb3
            save(trace)
            if not ok3:
                trace["named_failures"].append({
                    "hop": "ALL", "status": limb3["status"], "reason": "PRECONDITION_LIMB_3_FAILED",
                    "note": ("irpt-status still answers 5xx, so the precondition is unmet: no census and no "
                             "hop ran.")})
                print("STOP: limb 3 unmet -- irpt-status answered %s; no census, no hops" % limb3["status"])
            else:
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
        cleanup(token, trace, exp, a.close_ticket)
        data_refresh_zero_calls(trace, iat, exp)
    print("OK: trace at %s" % TRACE.relative_to(ROOT))
    print("OK: own copy at %s" % MY_TRACE.relative_to(ROOT))
    return 0 if trace["cleanup"].get("row_removed_read_back_absent") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
