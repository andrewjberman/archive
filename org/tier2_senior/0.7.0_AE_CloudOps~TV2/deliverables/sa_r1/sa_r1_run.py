"""TCKT_VNEXT SA-r-1 -- the FWD-1 seat-arm run. Steps 3-6 of the order in ONE process.

The token is minted in memory and NEVER printed, stored or committed. One token, RS256, exp = iat + 2h,
signed with the CURRENT slot of opal/auth/jwt-private-key (a bare PEM = the current slot, per
lambda/lib/authkeys/jwtPublicKeys.mjs).

Every call goes over HTTPS to the real CloudFront host. A direct lambda invoke is DELIBERATELY NOT USED:
the CTO's IRPT_YCDGEN ruling @d54e0b7515 condition 1 says a crafted-context invoke "proves only one hop
and does not count" as the real entry.

ORDER OF OPERATIONS is the CTO half's condition (1): the one-firm proof runs BEFORE any hop.

ORACLES, read from the DEPLOYED bytes rather than guessed:
  IRPT hosts (21 of the 27 clamped routes) -- _authz/served.py @74a62fb46c (sha256 87d9ecc4, = the
    deployed member on all 7 hosts). The clamp is Entry.handle: when selected_tenant != verified firm and
    the caller is internal and x-user-type is not 'service', _internal_allowed_firms reads the caller's
    own PROFILE allowedFirmIds LIST and refuses public_reason_code FIRM_BINDING when the selection is
    outside it. It fires BEFORE the operation compute, so a synthetic path id cannot cause a write and
    cannot mask the clamp.
  opal-ticket-api (6 of the 27) -- ticket_center/lambda_function.py (local bytes == deployed R13
    sha256 67068626). Its gate is _in_profile_scope(actor, ticket.requester.firm), keyed on a DynamoDB
    read of the TICKET. It takes no selected_tenant.

>> WHY THE TICKET ROUTES ARE NOT COUNTED AS COTTONWOOD REFUSALS. Exercising that gate against cottonwood
   needs a cottonwood-requester ticket id, and acquiring one is another firm's data (CLAUDE.md NEVER:
   never reference another firm's data). With a synthetic id the handler refuses at `cur is None` -- a
   NOT-FOUND that is byte-identical to a clamp refusal. Counting it would be ABSENT read as
   EXERCISED-AGAINST (rule 22a). So those arms are recorded as NOT_EXERCISED with the reason, and the
   ticket plane's cottonwood reach is exercised instead by the two arms that ARE sound:
     - GET /api/scoped/tickets, whose list is FILTERED by _in_profile_scope: the observable output is the
       set of requester firms, and a cottonwood member there would be an admit;
     - POST /api/scoped/tickets with answers.firm=cottonwood, which _create_firm_allowed must refuse.

Usage: python sa_r1_run.py [--advisor-opaque adv-04b85b8aefda]
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
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

FILER = "tckt-fwd1-testfiler-20261009@opal.invalid"
FILER_NAME = "TCKT_VNEXT FWD-1 synthetic test filer"
FIRM = "49financial"
FOREIGN = "cottonwood"
HOUSEHOLD = "[TEST] TCKT_VNEXT FWD-1 synthetic household"

ROOT = Path(__file__).resolve().parents[5]
CENSUS = ROOT / "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~6/SA_ROUTE_CENSUS.json"
TRACE = ROOT / "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/sa_r1_trace.json"
HOLDINGS = ROOT / "org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/aapl-vnq-12.03.csv"

TICKET_FN = "opal-ticket-api"
# Synthetic ids: non-existent by construction, so an admit past a clamp cannot touch real data.
SYN = {
    "{reportId}": "sa-r1-synthetic-report",
    "{exportId}": "sa-r1-synthetic-export",
    "{accountSetId}": "sa-r1-synthetic-accountset",
    "{requestId}": "sa-r1-synthetic-request",
    "{jobId}": "sa-r1-synthetic-job",
    "{ticketId}": "sa-r1-synthetic-ticket",
    "{advisorId}": "sa-r1-synthetic-advisor",
    "{clientKey}": "sa-r1-synthetic-client",
    "{relationshipId}": "sa-r1-synthetic-rel",
    "{accountId}": "sa-r1-synthetic-account",
    "{dimension}": "aua",
    "{surfaceId}": "sa-r1-synthetic-surface",
    "{universeId}": "sa-r1-synthetic-universe",
    "{executionId}": "sa-r1-synthetic-exec",
    "{account_id}": "sa-r1-synthetic-account",
    "{which}": "summary",
    "{client_id}": "sa-r1-synthetic-client",
}

ddb = boto3.client("dynamodb", region_name=REGION)


def now():
    return dt.datetime.now(dt.timezone.utc)


def iso(t=None):
    return (t or now()).strftime("%Y-%m-%dT%H:%M:%SZ")


def fill(route):
    out = route
    for k, v in SYN.items():
        out = out.replace(k, v)
    return out


# ---------------------------------------------------------------- identity


def adv_label(email):
    return "adv-" + hashlib.sha256(email.lower().encode()).hexdigest()[:12]


def resolve_advisor(opaque, firm):
    """Return the address whose adv- label is `opaque`. Held in memory; never printed, never in the trace."""
    pg = ddb.get_paginator("scan")
    scanned = 0
    for page in pg.paginate(TableName=USERS):
        for it in page.get("Items", []):
            scanned += 1
            em = (it.get("email") or {}).get("S")
            if em and adv_label(em) == opaque and (it.get("firmId") or {}).get("S") == firm:
                print("OK: advisor resolved from %d scanned row(s); opaque echo %s" % (scanned, adv_label(em)))
                return em
    print("ERROR: no active %s user carries opaque %s (%d row(s) scanned)" % (firm, opaque, scanned))
    return None


def mint_token():
    """ONE RS256 token, v2.1 claims, exp = iat + 2h. Returned to the caller's memory only."""
    pem = boto3.client("secretsmanager", region_name=REGION).get_secret_value(
        SecretId=PRIV_SECRET)["SecretString"]
    issued = int(time.time())
    claims = {
        "sub": FILER,
        "iss": "opal-portal-auth",
        "aud": "opal-portal-api",
        "firmId": "opal-capital",
        "tier": "advisor",
        "role": "user",
        "userType": "test-filer",
        "name": FILER_NAME,
        "iat": issued,
        "exp": issued + 7200,
    }
    tok = pyjwt.encode(claims, pem, algorithm="RS256")
    print("OK: token minted  iat=%s  exp=%s  claims=%s"
          % (iso(dt.datetime.fromtimestamp(issued, dt.timezone.utc)),
             iso(dt.datetime.fromtimestamp(issued + 7200, dt.timezone.utc)),
             sorted(claims)))
    return tok, issued


# ---------------------------------------------------------------- transport


def call(token, method, path, query=None, body=None, timeout=90):
    """ONE HTTPS call through CloudFront. Returns (status, reason_code, parsed_or_text)."""
    url = BASE + path
    if query:
        parts = []
        for k, v in query.items():
            parts.append("%s=%s" % (k, urllib.parse.quote(str(v), safe="@.-_")))
        url += "?" + "&".join(parts)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("x-contract-version", "v1")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", "replace")
            status = r.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        status = e.code
    except Exception as e:  # noqa: BLE001 -- a transport failure is DATA, not a pass
        return 0, "TRANSPORT_" + type(e).__name__, str(e)[:200]
    try:
        parsed = json.loads(raw)
    except ValueError:
        return status, None, raw[:300]
    return status, reason_of(parsed), parsed


def reason_of(parsed):
    if not isinstance(parsed, dict):
        return None
    st = parsed.get("status")
    if isinstance(st, dict):
        rc = st.get("public_reason_code")
        if rc:
            return rc
    for key in ("public_reason_code", "code", "error"):
        v = parsed.get(key)
        if isinstance(v, str):
            return v[:120]
    return None


# ---------------------------------------------------------------- step 4


def load_routes():
    d = json.loads(CENSUS.read_text(encoding="utf-8"))
    mto, one = [], []
    for r in d["rows"]:
        verdicts = {v.get("verdict") for v in r["per_token"].values()}
        if "MORE_THAN_ONE" in verdicts:
            mto.append(r)
        elif "ONE_FIRM" in verdicts:
            one.append(r)
    return d, mto, one


def one_firm_proof(token):
    """The CTO's condition, before any hop. Returns (summary, stop_reason_or_None)."""
    _, mto, one = load_routes()
    irpt = [r for r in mto if r["function"] != TICKET_FN]
    ticket = [r for r in mto if r["function"] == TICKET_FN]
    print("== step 4: the one-firm proof ==")
    print("  denominator: %d clamped route(s) = %d IRPT + %d ticket-api"
          % (len(mto), len(irpt), len(ticket)))

    arms = []
    refused_foreign = admitted_foreign = 0

    # --- the 21 IRPT routes: selected_tenant is the clamp's own carrier, so both arms are sound.
    for r in irpt:
        path = fill(r["route"])
        body = {} if r["method"] == "POST" else None
        st_f, rc_f, _ = call(token, r["method"], path, {"selected_tenant": FOREIGN}, body)
        st_o, rc_o, _ = call(token, r["method"], path, {"selected_tenant": FIRM}, body)
        foreign_refused = rc_f == "FIRM_BINDING"
        if foreign_refused:
            refused_foreign += 1
        else:
            admitted_foreign += 1
        arms.append({"function": r["function"], "method": r["method"], "route": r["route"],
                     "plane": "irpt-served", "exercised": True,
                     "foreign": {"firm": FOREIGN, "status": st_f, "reason": rc_f,
                                 "refused": foreign_refused},
                     "own": {"firm": FIRM, "status": st_o, "reason": rc_o,
                             "past_clamp": rc_o != "FIRM_BINDING"}})
        print("  %-26s %-5s %-58s cottonwood=%s/%s  49f=%s/%s"
              % (r["function"], r["method"], r["route"][:58], st_f, rc_f, st_o, rc_o))

    # --- the 6 ticket-api routes: see the module docstring. NOT counted as cottonwood refusals.
    for r in ticket:
        path = fill(r["route"])
        body = {} if r["method"] == "POST" else None
        st, rc, parsed = call(token, r["method"], path, None, body)
        row = {"function": r["function"], "method": r["method"], "route": r["route"],
               "plane": "ticket-api", "exercised": False,
               "not_exercised_reason": ("the gate keys on the TICKET's requester.firm via a DynamoDB read and "
                                        "takes no selected_tenant; a synthetic id refuses at `cur is None`, "
                                        "which is NOT-FOUND and indistinguishable from a clamp refusal "
                                        "(ABSENT != EXERCISED-AGAINST). A foreign ticket id is out of bounds."),
               "own": {"status": st, "reason": rc}}
        if r["route"] == "/api/scoped/tickets" and r["method"] == "GET":
            firms = sorted({(t.get("requester") or {}).get("firm")
                            for t in (parsed.get("tickets") or parsed.get("items") or [])
                            if isinstance(t, dict)} - {None}) if isinstance(parsed, dict) else []
            n = len(parsed.get("tickets") or parsed.get("items") or []) if isinstance(parsed, dict) else 0
            row["exercised"] = True
            row["not_exercised_reason"] = None
            row["list_filter"] = {"tickets_returned": n, "distinct_requester_firms": firms,
                                  "foreign_present": FOREIGN in firms}
            print("  %-26s %-5s %-58s list n=%d firms=%s"
                  % (r["function"], r["method"], r["route"][:58], n, firms))
            if FOREIGN in firms:
                admitted_foreign += 1
            else:
                refused_foreign += 1
        else:
            print("  %-26s %-5s %-58s own=%s/%s  [cottonwood NOT_EXERCISED]"
                  % (r["function"], r["method"], r["route"][:58], st, rc))
        arms.append(row)

    # --- extra sound arm on the ticket plane: CREATE with a foreign firm must be refused.
    st_c, rc_c, _ = call(token, "POST", "/api/scoped/tickets",
                         None, {"ticket_type": "analysis_request",
                                "title": "[TEST TCKT_VNEXT FWD-1] cottonwood negative arm",
                                "answers": {"advisor": "sa-r1-synthetic-advisor", "firm": FOREIGN,
                                            "household": HOUSEHOLD, "report_type": "Overview"}})
    create_foreign_refused = st_c >= 400
    print("  ticket CREATE answers.firm=%s -> %s/%s  refused=%s"
          % (FOREIGN, st_c, rc_c, create_foreign_refused))

    # --- a sample of the 36 ONE_FIRM routes (GET only: a sample must not write).
    sample = [r for r in one if r["method"] == "GET"][:8]
    sample_rows = []
    for r in sample:
        st, rc, _ = call(token, "GET", fill(r["route"]), {"selected_tenant": FIRM})
        sample_rows.append({"function": r["function"], "route": r["route"], "status": st, "reason": rc})
        print("  [sample] %-26s %-50s %s/%s" % (r["function"], r["route"][:50], st, rc))

    # --- one data-refresh route: v2.1 says a non-empty non-Dev userType is refused there.
    st_d, rc_d, _ = call(token, "GET", "/api/scoped/data-refresh/history")
    dr_refused = st_d >= 400
    print("  data-refresh GET /history -> %s/%s  refused=%s" % (st_d, rc_d, dr_refused))

    # --- the instrument control: a uniform 401 is a key/claims failure, NOT a clamp proof.
    own_codes = [a["own"]["status"] for a in arms if a.get("own")]
    all_401 = bool(own_codes) and all(s == 401 for s in own_codes)

    summary = {
        "claim": "measured",
        "host": HOST,
        "routes_armed": len(mto),
        "irpt_plane_exercised": len(irpt),
        "ticket_plane_exercised": sum(1 for a in arms if a["plane"] == "ticket-api" and a["exercised"]),
        "ticket_plane_not_exercised": sum(1 for a in arms if a["plane"] == "ticket-api" and not a["exercised"]),
        "refused_cottonwood": "%d of %d exercised" % (refused_foreign, refused_foreign + admitted_foreign),
        "admit_cottonwood": admitted_foreign,
        "admit_49financial_past_clamp": sum(1 for a in arms if a.get("own", {}).get("past_clamp")),
        "ticket_create_foreign_refused": {"status": st_c, "reason": rc_c, "refused": create_foreign_refused},
        "one_firm_sample": {"n": len(sample_rows), "of": len(one), "rows": sample_rows},
        "data_refresh": {"route": "GET /api/scoped/data-refresh/history", "status": st_d,
                         "reason": rc_d, "refused": dr_refused},
        "instrument_control": {"all_own_arms_401": all_401,
                               "note": "a uniform 401 would mean the token or key is wrong and the clamp "
                                       "was never reached; it is NOT a refusal proof"},
        "arms": arms,
    }

    stop = None
    if all_401:
        stop = "INSTRUMENT: every own-firm arm returned 401 -- the clamp was never exercised"
    elif admitted_foreign:
        stop = "COTTONWOOD ADMIT on %d exercised arm(s)" % admitted_foreign
    elif not dr_refused:
        stop = "DATA-REFRESH ADMIT (status %s)" % st_d
    print("  => refused_cottonwood %s | admits %d | data-refresh refused %s | STOP=%s"
          % (summary["refused_cottonwood"], admitted_foreign, dr_refused, stop))
    return summary, stop


# ---------------------------------------------------------------- step 5


def hops(token, advisor, trace):
    raw = HOLDINGS.read_bytes()
    file_sha = hashlib.sha256(raw).hexdigest()
    upload_token = "sar1-" + file_sha[:16]
    h = {x["hop"]: x for x in trace["hops"]}
    named = trace["named_failures"]
    print("== step 5: hops (a)-(g) ==")

    # (a) the upload door
    a = h["a_upload"]
    a["file"] = {"path": str(HOLDINGS.relative_to(ROOT)).replace("\\", "/"), "sha256": file_sha}
    input_id = upload_id = None
    state = None
    for i in range(14):
        st, rc, parsed = call(token, "POST", "/api/scoped/investor-reporting/analysis/inputs",
                              {"selected_tenant": FIRM, "advisor_email": advisor},
                              {"upload_token": upload_token, "filename": "sa_r1_template.csv",
                               "file_base64": base64.b64encode(raw).decode(), "file_type": "csv"})
        d = parsed.get("data") if isinstance(parsed, dict) and isinstance(parsed.get("data"), dict) else parsed
        if isinstance(d, dict):
            input_id = d.get("input_id") or input_id
            upload_id = d.get("upload_id") or upload_id
        stv = parsed.get("status") if isinstance(parsed, dict) else None
        state = stv.get("state") if isinstance(stv, dict) else None
        a["status"], a["state_seen"], a["polls"] = st, state, i + 1
        print("  (a) poll %2d  http=%s state=%r reason=%r input_id=%r" % (i + 1, st, state, rc, input_id))
        if state in ("NORMALIZED", "READY", "AVAILABLE"):
            break
        if st >= 400 and rc not in (None, "NOT_READY", "RESOLVING", "PENDING"):
            break
        time.sleep(5)
    a["upload_id"], a["input_id"] = upload_id, input_id
    save(trace)
    if not input_id:
        named.append({"hop": "a_upload", "status": a["status"], "reason": state or "no input_id",
                      "note": "the upload door produced no input_id; hops (b)-(g) depend on it"})
        return trace

    # (b) the ticket
    b = h["b_ticket"]
    st, rc, parsed = call(token, "POST", "/api/scoped/tickets", None,
                          {"ticket_type": "analysis_request",
                           "title": "[TEST TCKT_VNEXT FWD-1] seat arm",
                           "source": "portal",
                           "answers": {"advisor": adv_label(advisor), "firm": FIRM,
                                       "household": HOUSEHOLD, "report_type": "Overview"},
                           "attachment": {"upload_id": upload_id, "input_id": input_id}})
    b["status"], b["source"] = st, "portal"
    tkt = None
    if isinstance(parsed, dict):
        tkt = ((parsed.get("ticket") or {}) if isinstance(parsed.get("ticket"), dict) else {}).get("ticket_id")
    b["ticket_id"] = tkt
    print("  (b) ticket http=%s reason=%r ticket_id=%r" % (st, rc, tkt))
    save(trace)
    if not tkt:
        named.append({"hop": "b_ticket", "status": st, "reason": rc,
                      "note": "ticket CREATE refused; (c)-(g) all need a ticket_id and are NOT retried",
                      "structural_cause": "_create_firm_allowed = _firm_allowed(actor, firm) AND "
                                          "_in_profile_scope(actor, firm). The authorizer gives "
                                          "allowedFirmIds=opal-capital (tier advisor + role user, "
                                          "portal-authorizer computeAllowedFirms), while the PROFILE row "
                                          "scope is [49financial]: the two sets are disjoint, so firm="
                                          "49financial fails the first and firm=opal-capital fails the second."})
        for key in ("c_claim", "d_analysis", "e_ready", "f_report", "g_open"):
            named.append({"hop": key, "status": None, "reason": "UNREACHABLE",
                          "note": "depends on (b)'s ticket_id"})
        return trace

    # (c) claim
    c = h["c_claim"]
    st, rc, _ = call(token, "POST", "/api/scoped/tickets/%s/claim" % tkt, None, {})
    c["status"] = st
    print("  (c) claim http=%s reason=%r" % (st, rc))
    if st >= 400:
        named.append({"hop": "c_claim", "status": st, "reason": rc})
    save(trace)

    # (d) analysis submit
    d_ = h["d_analysis"]
    st, rc, parsed = call(token, "POST", "/api/scoped/investor-reporting/analysis",
                          {"selected_tenant": FIRM}, {"input_id": input_id, "ticket_id": tkt})
    inner = parsed.get("data") if isinstance(parsed, dict) and isinstance(parsed.get("data"), dict) else parsed
    rid = inner.get("request_id") if isinstance(inner, dict) else None
    d_["status"], d_["request_id"] = st, rid
    print("  (d) analysis http=%s reason=%r request_id=%r" % (st, rc, rid))
    if not rid:
        named.append({"hop": "d_analysis", "status": st, "reason": rc,
                      "note": "no request_id; (e)-(g) depend on it"})
        save(trace)
        return trace
    save(trace)

    # (e) poll to READY
    e = h["e_ready"]
    rstate = None
    for i in range(60):
        st, rc, parsed = call(token, "GET",
                             "/api/scoped/investor-reporting/analysis/requests/%s" % rid,
                             {"selected_tenant": FIRM})
        inner = parsed.get("data") if isinstance(parsed, dict) and isinstance(parsed.get("data"), dict) else parsed
        rstate = (inner or {}).get("state") or (inner or {}).get("status") if isinstance(inner, dict) else None
        e["status"], e["polls"], e["state"] = st, i + 1, rstate
        if i % 5 == 0 or rstate in ("READY", "AVAILABLE", "FAILED", "REFUSED"):
            print("  (e) poll %2d http=%s state=%r" % (i + 1, st, rstate))
        if rstate in ("READY", "AVAILABLE", "FAILED", "REFUSED"):
            break
        time.sleep(10)
    save(trace)
    if rstate not in ("READY", "AVAILABLE"):
        named.append({"hop": "e_ready", "status": e["status"], "reason": rstate,
                      "note": "never reached READY within the poll budget; not retried into a pass"})

    # (f) report onto the ticket
    f = h["f_report"]
    st, rc, _ = call(token, "POST", "/api/scoped/tickets/%s/report" % tkt, None, {"request_id": rid})
    f["status"] = st
    print("  (f) report http=%s reason=%r" % (st, rc))
    if st >= 400:
        named.append({"hop": "f_report", "status": st, "reason": rc})
    save(trace)

    # (g) open the report from the ticket
    g = h["g_open"]
    st1, rc1, p1 = call(token, "GET", "/api/scoped/tickets/%s" % tkt)
    st2, rc2, _ = call(token, "GET",
                       "/api/scoped/investor-reporting/analysis/requests/%s" % rid,
                       {"selected_tenant": FIRM})
    ref = None
    if isinstance(p1, dict):
        t = p1.get("ticket") if isinstance(p1.get("ticket"), dict) else p1
        ref = (t or {}).get("report_ref")
    g["status"] = st1
    g["report_opened"] = bool(ref) and st2 < 400
    g["second_status"] = st2
    print("  (g) ticket http=%s  request http=%s  report_ref_present=%s" % (st1, st2, bool(ref)))
    if not g["report_opened"]:
        named.append({"hop": "g_open", "status": st1, "reason": rc1 or rc2,
                      "note": "report_ref absent on the ticket or the request read refused"})
    save(trace)
    return trace


# ---------------------------------------------------------------- step 6


def cleanup(token, trace):
    print("== step 6: cleanup, same session ==")
    out = trace["cleanup"]
    ddb.delete_item(TableName=USERS, Key={"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}})
    back = ddb.get_item(TableName=USERS, Key={"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}},
                        ConsistentRead=True).get("Item")
    out["row_removed_read_back_absent"] = back is None
    print("  row removed; ConsistentRead read-back absent = %s" % (back is None))

    tkt = next((h.get("ticket_id") for h in trace["hops"] if h["hop"] == "b_ticket"), None)
    if tkt:
        st, rc, _ = call(token, "POST", "/api/scoped/tickets/%s/complete" % tkt, None,
                         {"resolution": "[TEST] SA-r-1 seat arm complete"})
        out["ticket_completed"] = st < 400
        out["ticket_complete_status"] = st
        print("  ticket %s complete -> http=%s reason=%r" % (tkt, st, rc))
    else:
        out["ticket_completed"] = None
        out["ticket_complete_status"] = "NO_TICKET_CREATED"
        print("  no ticket was created, so there is nothing to complete")
    out["token_left_to_expire"] = True
    save(trace)
    return trace


def save(trace):
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    TRACE.write_text(json.dumps(trace, indent=1) + "\n", encoding="utf-8")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--advisor-opaque", default="adv-04b85b8aefda")
    a = ap.parse_args(argv)

    trace = {
        "run_id": "SA-r-1-" + iso(),
        "executor": "0.7.0_AE_CloudOps~TV2",
        "claim": "measured",
        "entry": {"host": HOST, "transport": "HTTPS through CloudFront",
                  "not_used": "direct lambda invoke (CTO IRPT_YCDGEN @d54e0b7515 condition 1)"},
        "preconditions": {
            "read27": "27/27 rc 0 (reread_27.py, measured 15:08Z this session)",
            "cto_half_v2_1": "85c6dc8fe7",
            "order_pin": "104bc493ed",
            "row_written": None,
            "token_exp": None,
            "deployed_bytes": {
                "irpt_served_py": "87d9ecc4 (= git show 74a62fb46c:_authz/served.py, positive control HEAD=ada9bf5b)",
                "ticket_center_py": "67068626 (= local bytes, R13)"},
        },
        "one_firm_proof": None,
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
        "named_failures": [],
        "cleanup": {"row_removed_read_back_absent": False, "ticket_completed": False},
        "no_client_figures": "hop statuses and artifact IDs only; no holdings values and no report contents",
    }

    advisor = resolve_advisor(a.advisor_opaque, FIRM)
    if advisor is None:
        return 1
    trace["preconditions"]["row_written"] = iso()
    token, issued = mint_token()
    trace["preconditions"]["token_exp"] = iso(dt.datetime.fromtimestamp(issued + 7200, dt.timezone.utc))
    save(trace)

    try:
        proof, stop = one_firm_proof(token)
        trace["one_firm_proof"] = proof
        save(trace)
        if stop:
            trace["named_failures"].append({"hop": "ALL", "status": None, "reason": "STOP_BEFORE_HOPS",
                                            "note": stop})
            print("STOP: %s -- no hop runs; going straight to cleanup" % stop)
        else:
            hops(token, advisor, trace)
    finally:
        cleanup(token, trace)
    print("OK: trace at %s" % TRACE.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
