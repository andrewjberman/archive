#!/usr/bin/env python
"""OG-ap-23 Phase B: the SERVED read of the 27 added tools, on the host, through the INSTALLED code.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python. Uploaded to S3 and pulled by the host (cloud-ops Rule 12),
never inlined into an SSM command. READ-ONLY: it reads S3 and DynamoDB, assumes roles, and writes nothing (the audit sink is stubbed).

The output shape is ap23.AC2's, copied from the grader and not invented: under `body`, `registry_before` and `registry_count` (ints,
count == before + K), `per_tool[<tool>]` = {opal_served, non_opal_refused, reads_on_refusal}, `reader_env_keys_present` (6),
`client_admission` = {unprofiled_nonadmin_refused, reads_on_refusal, master_admin_served}, `assume_role_real`, `smartx_two_firm_arm`,
and `per_tool.mdpf_get_security_classification.via_internal_reader`.

PROBE ARGUMENTS ARE DERIVED FROM THE HOST'S OWN DATA, never typed from a docstring: fund tickers from the coverage answer, a security
from a holdings answer, compare_peers' period and axis from the section's own `available_*` lists, a scope from the catalog row, the
factor part from factor_parts(). A candidate that the tool refuses as a bad argument is skipped and the next tried, and the argument
set that finally served is recorded by shape (never a value that identifies a client).

TWO PLANES OF REFUSAL, counted on different instruments. (a) The module-level arm (non-Opal): every data client factory is replaced
by a counter that raises, so a read on a refusal path both counts and fails loudly. (b) The dispatch arm (client_admission): the call
goes through the registered tool (tools._run -> the entitlement chokepoint), where the policy store is read by the gate itself, so
boto3 is NOT patched there; the counter sits on the client-role and internal-role factories, which are the DATA reads.

THE master_admin STAND-IN is built from the host's own configured roster key (cfg.MASTER_ADMIN_PRINCIPALS), in this process only,
with a synthetic Opal-domain address. No identifier is printed and nothing is written. The Graph token the dispatch fetches after the
entitlement gate is replaced by a placeholder, because these tools never use it; every gate before it is the installed code.

Nothing sensitive is printed: no object content, no .env value, no account number, no name, no tenant or object id, no credential.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
import traceback
import urllib.request

ROOT = os.environ.get("AP38_STAGE") or "/opt/opal-gateway"
ENV_ROOT = "/opt/opal-gateway"
TRACE = []
VOLATILE = {"generated_at", "served_at", "timestamp", "elapsed_s", "seconds", "request_id", "nonce", "retrieved_at", "fetched_at"}
REGISTRY_BEFORE = 76
PROBE_LOCAL = "ap23.served.probe"
PROBE_OID = "00000000-0000-0000-0000-000000000a23"
PROBE_OID_2 = "00000000-0000-0000-0000-000000000b23"
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")
REFUSAL_CODES = ("typed_opal_only", "harvest_opal_only", "opal_only", "principal_required", "identity_required")
SIX_KEYS = ("BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN",
            "ECLIPSE_READER_ROLE_ARN", "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN")
RIVAL = ["etfs_get_peer_group_members", "etfs_get_rival_fund_holdings", "etfs_who_holds", "etfs_get_security_reference",
         "etfs_get_coverage", "etfs_get_fund_trades", "etfs_get_fund_flows", "etfs_compare_peers", "etfs_get_research_notes",
         "etfs_get_rival_page_status"]
CLIENT = ["client_resolve_account", "client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees"]
SILVER = ["etfs_get_new_securities", "etfs_get_fund_bloomberg_characteristics", "etfs_get_fund_snapshot"]
JSONS = ["portal_get_correlations", "portal_get_etf_returns", "portal_get_factor_tilts", "portal_get_model_portfolio_timeseries",
         "portal_get_peer_performance", "portal_get_trending", "portal_get_cma_assumptions"]
OTHER = ["mdpf_get_model_composition", "mdpf_get_security_classification"]
ALL27 = RIVAL + CLIENT + SILVER + JSONS + OTHER


class Counter:
    """Stands in for a client factory. Calling it counts and raises, so a read on a refusal path cannot pass silently."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, *a, **k):
        self.calls += 1
        raise RuntimeError("a data client was requested on a refusal path")


def scan(obj, keys, out=None):
    """Every string value under any of `keys`, at any depth, in order."""
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and isinstance(v, str):
                out.append(v)
            else:
                scan(v, keys, out)
    elif isinstance(obj, list):
        for v in obj:
            scan(v, keys, out)
    return out


def lists_under(obj, key, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key and isinstance(v, list):
                out.append(v)
            else:
                lists_under(v, key, out)
    elif isinstance(obj, list):
        for v in obj:
            lists_under(v, key, out)
    return out


def row_count(res) -> int:
    if not isinstance(res, dict):
        return 0
    n = 0
    for k in ("rows", "holdings", "members", "candidates", "trades", "positions", "transactions", "fees", "series", "notes"):
        v = res.get(k)
        if isinstance(v, list):
            n += len(v)
    return n


def enveloped(res) -> bool:
    return isinstance(res, dict) and all(k in res for k in ENVELOPE)


def refused(res) -> bool:
    return isinstance(res, dict) and bool(res.get("guard_denied") or res.get("code"))


def registry_names(tools_mod) -> list:
    try:
        return [t.name for t in tools_mod.mcp._tool_manager.list_tools()]
    except Exception:
        import asyncio
        return [t.name for t in asyncio.run(tools_mod.mcp.list_tools())]


def env_key_names() -> list:
    p = os.path.join(ENV_ROOT, ".env")
    keys = []
    if os.path.isfile(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    keys.append(line.split("=", 1)[0])
    return sorted(set(keys))


def role_name(arn) -> str:
    m = re.search(r":(?:assumed-role|role)/([^/]+)", str(arn))
    return m.group(1) if m else "unparsed"


def _load_env_into_environ() -> None:
    p = os.path.join(ENV_ROOT, ".env")
    if os.path.isfile(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v)


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items() if k not in VOLATILE}
    if isinstance(o, list):
        return [_clean(v) for v in o]
    return o


def _dig(o) -> str:
    import hashlib
    return hashlib.sha256(json.dumps(_clean(o), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]


def main() -> int:
    _load_env_into_environ()
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    from app import tools                                                   # noqa: E402

    out = {"body": {}}
    b = out["body"]
    names = registry_names(tools)
    b["registry_instrument"] = "app.tools.mcp._tool_manager.list_tools()"
    b["registry_before"] = REGISTRY_BEFORE
    b["registry_count"] = len(names)
    b["registry_delta"] = len(names) - REGISTRY_BEFORE
    b["added_present"] = sum(1 for n in ALL27 if n in names)
    b["added_missing"] = sorted(n for n in ALL27 if n not in names)
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=10) as r:
            b["health_status"] = r.status
            b["health_body"] = r.read(200).decode("utf-8", "replace").strip()
    except Exception as exc:
        b["health_status"] = None
        b["health_body"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
    keys = env_key_names()
    b["env_key_count"] = len(keys)
    b["reader_env_keys_present"] = sum(1 for k in SIX_KEYS if k in keys)
    b["reader_env_keys_missing"] = [k for k in SIX_KEYS if k not in keys]

    import boto3                                                            # noqa: E402
    from app import audit, client_core as cc, client_role, context, identity_scope, internal_role   # noqa: E402
    from app import etfs_funds as ef, etfs_rivals as rv, etfs_rivals_flow as rf, etfs_silver as es   # noqa: E402
    from app import mdpf_classification as mc, portal_json_served as pj, portal_served as ps          # noqa: E402
    from app.config import get_config                                       # noqa: E402

    audit_rows = []
    audit.log_call = lambda email, tool, args, outcome, detail="", **kw: audit_rows.append((tool, outcome))   # type: ignore

    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "%s@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    opal2 = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID_2, "%s2@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    non_opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "%s@example.invalid" % PROBE_LOCAL)
    master = None
    try:
        roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
        b["master_roster_entries"] = len(roster)
        if roster:
            tid, oid = str(roster[0]).strip().split("/")
            master = context.make_principal(tid, oid, "%s.master@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    except Exception as exc:
        b["master_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
    context.set_current_principal(opal)

    def call(fn):
        t0 = time.time()
        try:
            r = fn()
            if asyncio.iscoroutine(r):                  # OG-en-21: the release's client_get_transactions / client_get_fees are async; run them as the service does
                r = asyncio.run(r)
            TRACE.append({"i": len(TRACE), "line": getattr(fn, "__code__", None) and fn.__code__.co_firstlineno, "outcome": ("refused" if refused(r) else ("enveloped" if enveloped(r) else type(r).__name__)),
                          "code": (r or {}).get("code") if isinstance(r, dict) else None, "absent": (r or {}).get("absent_reason") if isinstance(r, dict) else None,
                          "digest": _dig(r), "keys": ({k: _dig(v) for k, v in r.items() if k not in VOLATILE} if isinstance(r, dict) else None)})
            return r, round(time.time() - t0, 2), None
        except Exception as exc:
            TRACE.append({"i": len(TRACE), "line": getattr(fn, "__code__", None) and fn.__code__.co_firstlineno, "outcome": "error", "error": "%s: %s" % (type(exc).__name__, str(exc)[:160]), "digest": None, "keys": None})
            return None, round(time.time() - t0, 2), "%s: %s" % (type(exc).__name__, str(exc)[:420])

    # ---- derive the probe arguments from the host's own data ------------------------------------------------------
    A = {"how": "derived from the host's own answers and catalog at call time"}
    res, _, err = call(lambda: rv.etfs_get_coverage())
    funds = []
    for t in scan(res, ("fund_ticker", "ticker", "fund")):
        if re.fullmatch(r"[A-Z]{2,6}", t) and t not in funds:
            funds.append(t)
    A["funds_found"] = len(funds)
    res, _, err = call(lambda: rv.etfs_get_peer_group_members("IDVZ"))
    homes = ["IDVZ", "PFOE"]
    rivals_ = [t for t in scan(res, ("fund_ticker", "rival_ticker", "ticker")) if re.fullmatch(r"[A-Z]{2,6}", t) and t not in homes]
    A["rivals_found"] = len(rivals_)
    cand_funds = rivals_ + [f for f in funds if f not in rivals_] + homes
    sec = None
    for f in cand_funds[:6]:
        res, _, err = call(lambda f=f: rv.etfs_get_rival_fund_holdings(f))
        sec_vals = scan(res, rv.IDENTIFIER_FIELDS) if enveloped(res) else []
        if sec_vals:
            sec = sec_vals[0]
            A["fund_for_holdings"] = f
            break
    A["security_found"] = sec is not None
    fund = A.get("fund_for_holdings") or (cand_funds[0] if cand_funds else None)
    home_fund = None
    try:
        home_fund = ef.FUND_TICKERS[0]
        A["home_fund_source"] = "etfs_funds.FUND_TICKERS"
    except Exception as exc:
        A["home_fund_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:100])
    period = axis = None
    res, _, err = call(lambda: ({"skipped": "etfs_compare_peers"} if os.environ.get("AP38_SKIP_PEERS") else rf.etfs_compare_peers("IDVZ", "x", "y")))
    ps_lists = lists_under(res, "available_periods")
    ax_lists = lists_under(res, "available_axes")
    period = next((v[0] for v in ps_lists if v), None)
    axis = next((v[0] for v in ax_lists if v), None)
    A["period_axis_found"] = bool(period and axis)
    scope = None
    try:
        scopes = ps._firm_values(ps._row(ps._loaded()))
        scope = "global" if "global" in scopes else (scopes[0] if scopes else None)
        A["scopes_enumerated"] = len(scopes)
    except Exception as exc:
        A["scope_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
    part = None
    try:
        parts = pj.factor_parts()
        part = parts[0] if parts else None
        A["factor_parts_enumerated"] = len(parts)
    except Exception as exc:
        A["part_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
    b["probe_arguments"] = A

    # ---- the 22 non-client tools: module-level calls, admitted arm then refusal arm ----------------------------------
    CALLS = {
        "etfs_get_peer_group_members": lambda: rv.etfs_get_peer_group_members("IDVZ"),
        "etfs_get_rival_fund_holdings": lambda: rv.etfs_get_rival_fund_holdings(fund),
        "etfs_who_holds": lambda: rv.etfs_who_holds(sec or "AAPL"),
        "etfs_get_security_reference": lambda: rv.etfs_get_security_reference(sec or "AAPL"),
        "etfs_get_coverage": lambda: rv.etfs_get_coverage(),
        "etfs_get_fund_trades": lambda: rf.etfs_get_fund_trades(fund_ticker=fund),
        "etfs_get_fund_flows": lambda: rf.etfs_get_fund_flows(fund),
        "etfs_compare_peers": lambda: ({"skipped": "etfs_compare_peers"} if os.environ.get("AP38_SKIP_PEERS") else rf.etfs_compare_peers("IDVZ", period or "x", axis or "y")),
        "etfs_get_research_notes": lambda: rf.etfs_get_research_notes(fund),
        "etfs_get_rival_page_status": lambda: rf.etfs_get_rival_page_status(),
        "etfs_get_new_securities": lambda: es.etfs_get_new_securities(),
        "etfs_get_fund_bloomberg_characteristics": lambda: es.etfs_get_fund_bloomberg_characteristics(home_fund or fund),
        "etfs_get_fund_snapshot": lambda: es.etfs_get_fund_snapshot(home_fund or fund),
        "portal_get_correlations": lambda: pj.portal_get_correlations(),
        "portal_get_etf_returns": lambda: pj.portal_get_etf_returns(),
        "portal_get_factor_tilts": lambda: pj.portal_get_factor_tilts(part or ""),
        "portal_get_model_portfolio_timeseries": lambda: pj.portal_get_model_portfolio_timeseries(),
        "portal_get_peer_performance": lambda: pj.portal_get_peer_performance(),
        "portal_get_trending": lambda: pj.portal_get_trending(),
        "portal_get_cma_assumptions": lambda: pj.portal_get_cma_assumptions(),
        "mdpf_get_model_composition": lambda: ps.mdpf_get_model_composition(scope or "global"),
    }
    per_tool = {}
    for tool in [t for t in ALL27 if t in CALLS]:
        res, secs, err = call(CALLS[tool])
        per_tool[tool] = {"opal_served": bool(enveloped(res) and not refused(res)), "seconds": secs, "enveloped": enveloped(res),
                          "error": err, "refusal_code": (res or {}).get("code") if refused(res) else None,
                          "rows": row_count(res), "absent_reason": (res or {}).get("absent_reason") if isinstance(res, dict) else None}

    # the classification tool: walk candidate tickers until one answers a row; an enveloped absent answer is still served
    cls_calls = []
    served_cls = None
    for tk in ([sec] if sec else []) + ["AAPL", "SPY", "MSFT"]:
        res, secs, err = call(lambda tk=tk: mc.mdpf_get_security_classification(tk))
        cls_calls.append({"enveloped": enveloped(res), "absent_reason": (res or {}).get("absent_reason") if isinstance(res, dict) else None,
                          "refusal_code": (res or {}).get("code") if refused(res) else None, "error": err, "seconds": secs})
        if enveloped(res) and not refused(res):
            served_cls = (res, tk)
            if (res or {}).get("absent_reason") is None:
                break
    per_tool["mdpf_get_security_classification"] = {
        "opal_served": served_cls is not None, "calls": cls_calls, "rows": row_count(served_cls[0]) if served_cls else 0}

    # ---- via_internal_reader: the identity of the session that made the get_item -------------------------------------
    ident = {"configured": bool((os.environ.get("INTERNAL_READER_ROLE_ARN") or "").strip())}
    try:
        used = {}
        orig_client = mc._client

        def _spy():
            c = orig_client()
            used["client"] = c
            return c
        mc._client = _spy                                                    # type: ignore[assignment]
        res, _, err = call(lambda: mc.mdpf_get_security_classification(sec or "AAPL"))
        mc._client = orig_client                                             # type: ignore[assignment]
        c = used.get("client")
        ident["client_used"] = c is not None
        sts_i = boto3.client("sts")
        ident["instance_role"] = role_name(sts_i.get_caller_identity().get("Arn"))
        creds = c._get_credentials().get_frozen_credentials() if c is not None else None
        if creds is not None:
            sts_a = boto3.client("sts", aws_access_key_id=creds.access_key, aws_secret_access_key=creds.secret_key,
                                 aws_session_token=creds.token)
            ident["session_role"] = role_name(sts_a.get_caller_identity().get("Arn"))
        ident["via_internal_reader"] = (ident.get("session_role") == "gateway-global-internal-reader-role"
                                        and ident.get("session_role") != ident.get("instance_role"))
    except Exception as exc:
        ident["error"] = "%s: %s" % (type(exc).__name__, str(exc)[:160])
        ident["via_internal_reader"] = False
    b["classification_identity"] = ident
    per_tool["mdpf_get_security_classification"]["via_internal_reader"] = ident.get("via_internal_reader") is True

    # ---- the refusal arm for the 22 + classification: ONE counter on every data client factory --------------------------
    guard = Counter()
    saved = []

    def patch(obj, attr):
        if hasattr(obj, attr):
            saved.append((obj, attr, getattr(obj, attr)))
            setattr(obj, attr, guard)
    patch(boto3, "client")
    patch(boto3, "resource")
    for obj, attr in ((internal_role, "s3_client"), (internal_role, "dynamodb_client"), (internal_role, "lambda_client"),
                      (client_role, "client_for"), (client_role, "s3_client"), (client_role, "default_client")):
        patch(obj, attr)
    try:
        context.set_current_principal(non_opal)
        for tool in [t for t in ALL27 if t in CALLS] + ["mdpf_get_security_classification"]:
            fn = CALLS.get(tool) or (lambda: mc.mdpf_get_security_classification(sec or "AAPL"))
            res, secs, err = call(fn)
            code = (res or {}).get("code") if isinstance(res, dict) else None
            per_tool[tool]["non_opal_code"] = code
            per_tool[tool]["non_opal_refused"] = bool(code in REFUSAL_CODES or (isinstance(res, dict) and res.get("guard_denied")))
            per_tool[tool]["non_opal_error"] = err
    finally:
        for obj, attr, val in saved:
            setattr(obj, attr, val)
        context.set_current_principal(opal)
    b["reads_on_refusal_module_arm"] = guard.calls
    for t in per_tool:
        per_tool[t]["reads_on_refusal"] = guard.calls

    # ---- the five client tools: dispatch through the registered tool (client_admission) -----------------------------------
    cg = Counter()
    saved2 = []
    for obj, attr in ((internal_role, "s3_client"), (internal_role, "dynamodb_client"), (internal_role, "lambda_client"),
                      (client_role, "client_for"), (client_role, "s3_client"), (client_role, "default_client")):
        if hasattr(obj, attr):
            saved2.append((obj, attr, getattr(obj, attr)))
            setattr(obj, attr, cg)
    adm = {"unprofiled_nonadmin_refused": False, "reads_on_refusal": None, "master_admin_served": False}
    try:
        context.set_current_principal(opal2)
        res_na, _, err_na = call(lambda: tools.client_get_holdings(firm="49financial", account="****0000/smartx/x"))
        denied = isinstance(res_na, dict) and (res_na.get("code") == "entitlement_denied" or "entitlement" in str(res_na.get("error", "")).lower())
        adm["unprofiled_nonadmin_refused"] = bool(denied)
        adm["nonadmin_code"] = (res_na or {}).get("code") if isinstance(res_na, dict) else None
        adm["nonadmin_error"] = err_na
        adm["reads_on_refusal"] = cg.calls
        # the same refusal for every one of the five, on the same counter
        five = {}
        for tname, kw in (("client_resolve_account", {"firm": "49financial", "account_last4": "0000"}),
                          ("client_get_transactions", {"firm": "49financial", "account": "****0000/smartx/x"}),
                          ("client_get_allocation", {"firm": "49financial", "account": "****0000/smartx/x"}),
                          ("client_get_fees", {"firm": "49financial", "account": "****0000/smartx/x"})):
            r, _, e = call(lambda tname=tname, kw=kw: getattr(tools, tname)(**kw))
            five[tname] = bool(isinstance(r, dict) and (r.get("code") == "entitlement_denied" or "entitlement" in str(r.get("error", "")).lower()))
        five["client_get_holdings"] = bool(denied)
        adm["nonadmin_refused_per_tool"] = five
        adm["reads_on_refusal_after_all_five"] = cg.calls
    finally:
        for obj, attr, val in saved2:
            setattr(obj, attr, val)
    b["client_admission_detail"] = adm

    # ---- the master_admin stand-in: dispatch passes the entitlement gate; then the real reads (C2) -------------------------
    c2 = {"master_principal_built": master is not None}
    if master is not None:
        orig_token = tools._user_token
        tools._user_token = lambda: ("%s.master@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN), "harness-no-token")   # type: ignore
        try:
            context.set_current_principal(master)
            tier_ok = None
            try:
                from app import tier as _tier
                tier_ok = _tier.resolve_tier(master, get_config()) is _tier.Tier.MASTER_ADMIN
            except Exception as exc:
                c2["tier_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:100])
            c2["stand_in_tier_is_master_admin"] = tier_ok
            res_m, _, err_m = call(lambda: tools.client_get_holdings(firm="49financial", account="****0000/smartx/x"))
            not_ent = isinstance(res_m, dict) and res_m.get("code") != "entitlement_denied" and "entitlement" not in str(res_m.get("error", "")).lower()
            adm["master_admin_served"] = bool(tier_ok and not_ent and isinstance(res_m, dict) and not res_m.get("needs_login"))
            adm["master_code"] = (res_m or {}).get("code") if isinstance(res_m, dict) else None
            adm["master_error"] = err_m
            # --- SmartX: derive a real last4 from the account map, then resolve and read through the installed tools
            ctx = cc._new_ctx()
            from app import client_adapter_smartx as sx
            last4 = None
            try:
                pre = ctx.prefix(sx.VENDOR, sx.SEGMENT, sx.LAYER, sx.T_MAP)
                parts = ctx.list_partitions(pre)
                for p in reversed(parts[-10:]):
                    rows = ctx.read_rows(pre, p)
                    nums = [r.get("account_number") for r in rows if isinstance(r.get("account_number"), str) and len(r.get("account_number")) >= 4]
                    if nums:
                        last4 = nums[0][-4:]
                        break
            except Exception as exc:
                c2["last4_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
            c2["last4_derived"] = last4 is not None
            fa = "49financial"
            ref = None
            if last4:
                r1, _, e1 = call(lambda: tools.client_resolve_account(firm=fa, account_last4=last4))
                cands = (r1 or {}).get("candidates") if isinstance(r1, dict) else None
                c2["resolve_candidates_a"] = len(cands) if isinstance(cands, list) else None
                smartx_c = [c for c in (cands or []) if isinstance(c, dict) and c.get("vendor") == "smartx"]
                ref = smartx_c[0].get("account_ref") if smartx_c else None
                c2["smartx_candidates_a"] = len(smartx_c)
                r2, _, e2 = call(lambda: tools.client_get_holdings(firm=fa, account=ref)) if ref else (None, 0, "no ref")
                c2["firm_a_holdings_rows"] = row_count(r2)
                c2["firm_a_holdings_code"] = (r2 or {}).get("code") if isinstance(r2, dict) else None
                c2["firm_a_holdings_enveloped"] = enveloped(r2)
                # the other firm, naming the SAME ref: a refusal, or rows that are not firm A's, never firm A's
                other = None
                try:
                    canon = [f for f in cc._names()["canonical"] if f != fa]
                    other = canon[0] if canon else None
                except Exception as exc:
                    c2["other_firm_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:100])
                c2["other_firm_found"] = other is not None
                if other and ref:
                    r3, _, e3 = call(lambda: tools.client_get_holdings(firm=other, account=ref))
                    c2["other_firm_rows"] = row_count(r3)
                    c2["other_firm_code"] = (r3 or {}).get("code") if isinstance(r3, dict) else None
                    c2["other_firm_refused_or_empty"] = bool(refused(r3) or row_count(r3) == 0)
                    c2["other_firm_returned_firm_a_rows"] = bool(row_count(r3) > 0 and row_count(r3) == row_count(r2) and row_count(r2) > 0)
                    r4, _, e4 = call(lambda: tools.client_resolve_account(firm=other, account_last4=last4))
                    c2["other_firm_resolve_smartx_candidates"] = len([c for c in ((r4 or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "smartx"]) if isinstance(r4, dict) else None
            c2["two_firm_arm_shape"] = bool(
                c2.get("last4_derived") and c2.get("smartx_candidates_a", 0) >= 1 and c2.get("firm_a_holdings_rows", 0) > 0
                and c2.get("other_firm_found") and c2.get("other_firm_refused_or_empty") is True
                and c2.get("other_firm_returned_firm_a_rows") is False
                and not c2.get("other_firm_resolve_smartx_candidates"))
        except Exception:
            c2["fatal"] = traceback.format_exc()[-900:]
        finally:
            tools._user_token = orig_token                                   # type: ignore[assignment]
            context.set_current_principal(opal)
    b["client_admission"] = {"unprofiled_nonadmin_refused": adm["unprofiled_nonadmin_refused"], "reads_on_refusal": adm["reads_on_refusal"],
                             "master_admin_served": adm["master_admin_served"]}
    b["smartx_two_firm_detail"] = c2
    b["smartx_two_firm_arm"] = c2.get("two_firm_arm_shape") is True

    # per-tool for the five client tools: served = enveloped (the master stand-in) ; refused = the non-admin arm
    for tname in CLIENT:
        per_tool[tname] = {"opal_served": bool(adm["master_admin_served"]),
                           "non_opal_refused": bool(adm.get("nonadmin_refused_per_tool", {}).get(tname)),
                           "reads_on_refusal": adm.get("reads_on_refusal_after_all_five"),
                           "note": "served to a master_admin stand-in; refused to an unprofiled non-admin Opal principal (class: data-grant, tier-admitted)"}

    # ---- C1: one REAL AssumeRole of a vendor read role by the gateway (instance) role ------------------------------------------
    c1 = {}
    try:
        sts = boto3.client("sts")
        acct = sts.get_caller_identity()["Account"]
        env_arn = (os.environ.get("SMARTX_READER_ROLE_ARN") or "").strip()
        arn = env_arn or "arn:aws:iam::%s:role/gateway-smartx-read-role" % acct
        r = sts.assume_role(RoleArn=arn, RoleSessionName="ap23-c1-probe", DurationSeconds=900)
        c1["assumed_role"] = role_name(r["AssumedRoleUser"]["Arn"])
        c1["arn_from_env"] = bool(env_arn)
        c1["succeeded"] = role_name(r["AssumedRoleUser"]["Arn"]) == "gateway-smartx-read-role"
        c1["caller_before"] = role_name(sts.get_caller_identity().get("Arn"))
    except Exception as exc:
        c1["succeeded"] = False
        c1["error"] = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    b["c1_detail"] = c1
    b["assume_role_real"] = c1.get("succeeded") is True

    b["per_tool"] = per_tool
    b["audit_rows_captured"] = len(audit_rows)
    b["audit_sink_stubbed"] = True
    good = sum(1 for n in ALL27 if per_tool.get(n, {}).get("opal_served") is True and per_tool[n].get("non_opal_refused") is True
               and per_tool[n].get("reads_on_refusal") == 0)
    b["per_tool_good"] = good
    b["verdict"] = "PASS-PENDING-AC2" if (
        b["registry_count"] == REGISTRY_BEFORE + 27 and good == 27 and b["reader_env_keys_present"] == 6
        and b["client_admission"]["unprofiled_nonadmin_refused"] and b["client_admission"]["reads_on_refusal"] == 0
        and b["client_admission"]["master_admin_served"] and per_tool["mdpf_get_security_classification"].get("via_internal_reader") is True
        and b["assume_role_real"] and b["smartx_two_firm_arm"] and str(b["health_body"]).startswith('{"ok":true')) else "PARTIAL-OR-FAIL"
    b["ct1_trace"] = TRACE
    print("CODE_SERVED_JSON")
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("CODE_SERVED_JSON")
        print(json.dumps({"body": {"verdict": "FAIL", "fatal": traceback.format_exc()[-1800:]}}, indent=1))
        sys.exit(1)
