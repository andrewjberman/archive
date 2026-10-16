#!/usr/bin/env python
"""OG-ev-1 discovery pass (READ-ONLY, on the host, through the installed code).

Not the record. It calls a broad set of candidate arguments per marker and prints only SHAPES: top-level keys, which marker words occur
in the serialised answer, a few short scalar fields, row counts. No account number, no name and no object content is printed; the
output is read by the author to choose the arguments of the final harness. usage: python ev1_discover.py   (on the host)
"""
from __future__ import annotations

import json
import os
import sys
import traceback

ROOT = "/opt/opal-gateway"
PROBE_OID = "00000000-0000-0000-0000-000000000e41"
WORDS = ("data_status", "not_held", "trading_days", "truncated", "projected", "50", "14", "pct", "percent", "fraction", "unit", "newest",
         "as_of", "absent_reason", "denominator", "coverage", "csv", "master", "currency", "capped", "cap", "window")


def short(v, n=140):
    s = v if isinstance(v, str) else json.dumps(v, default=str)
    return s[:n]


def summarize(res):
    if not isinstance(res, dict):
        return {"type": type(res).__name__, "value": short(res)}
    txt = json.dumps(res, default=str)
    out = {"keys": sorted(res)[:30], "bytes": len(txt), "words": [w for w in WORDS if w in txt]}
    for k in ("as_of", "absent_reason", "data_status", "code", "error", "denominator", "projected", "truncated", "unit", "units", "coverage",
              "window_days", "cap", "capped"):
        if k in res:
            out[k] = short(res[k])
    for k, v in res.items():
        if isinstance(v, list):
            out["len_" + k] = len(v)
            if v and isinstance(v[0], dict):
                out["row0_keys_" + k] = sorted(v[0])[:24]
        elif isinstance(v, dict) and k not in ("denominator",):
            out["sub_" + k] = sorted(v)[:16]
    return out


def find_vals(obj, keys, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and isinstance(v, (str, int)):
                out.append(v)
            else:
                find_vals(v, keys, out)
    elif isinstance(obj, list):
        for v in obj:
            find_vals(v, keys, out)
    return out


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    from app import tools                                                    # noqa: E402
    from app import audit, client_core as cc, context, identity_scope        # noqa: E402
    from app.config import get_config                                        # noqa: E402

    audit.log_call = lambda *a, **k: None                                    # type: ignore
    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "ev1.probe@%s" % identity_scope.OPAL_USERS_DOMAIN)
    master = None
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    if roster:
        tid, oid = str(roster[0]).strip().split("/")
        master = context.make_principal(tid, oid, "ev1.master@%s" % identity_scope.OPAL_USERS_DOMAIN)
    tools._user_token = lambda: ("ev1.probe@%s" % identity_scope.OPAL_USERS_DOMAIN, "no-token")   # type: ignore

    log = []
    only = tuple(a for a in sys.argv[1:] if not a.startswith("-"))

    def call(tag, tool, who="opal", **kw):
        if only and not (tag.startswith(only) or tag == "18.resolve.ticker"):
            return None
        context.set_current_principal(master if who == "master" else opal)
        try:
            res = getattr(tools, tool)(**kw)
            log.append({"tag": tag, "tool": tool, "args": {k: short(v, 60) for k, v in kw.items()}, "sum": summarize(res)})
            return res
        except Exception as exc:
            log.append({"tag": tag, "tool": tool, "args": {k: short(v, 60) for k, v in kw.items()},
                        "exc": "%s: %s" % (type(exc).__name__, str(exc)[:200])})
            return None

    # ---- ap-18 typed harvest -----------------------------------------------------------------------------------
    r = call("18.resolve.ticker", "harvest_resolve_security", query="AAPL")
    key = (find_vals(r, ("security_key",)) or [None])[0]
    call("18.resolve.fakecusip", "harvest_resolve_security", query="999999AA9")
    call("18.resolve.fakecusip2", "harvest_resolve_security", query="00000X000")
    if key:
        call("18.coverage", "harvest_security_coverage", security_key=key)
        call("18.chatter.recent", "harvest_get_chatter", security_key=key, from_day="2026-10-01", to_day="2026-10-15")
        call("18.chatter.old", "harvest_get_chatter", security_key=key, from_day="2025-01-02", to_day="2025-01-09")
        call("18.articles", "harvest_search_articles", security_key=key, limit=3)
        call("18.research", "harvest_get_research", security_key=key)
        call("18.peers", "harvest_get_peers_and_scores", security_key=key)
        call("18.filing", "harvest_get_filing_analysis", security_key=key)
        call("18.fundamentals", "harvest_get_fundamentals", security_key=key, kind="annual")
    for q in ("ZZZZ", "BRK.B"):
        rr = call("18.resolve." + q, "harvest_resolve_security", query=q)
        k2 = (find_vals(rr, ("security_key",)) or [None])[0]
        if k2:
            call("18.chatter.quiet." + q, "harvest_get_chatter", security_key=k2, from_day="2026-10-01", to_day="2026-10-15")
            call("18.coverage." + q, "harvest_security_coverage", security_key=k2)
    # ---- ap-19 portal + news ----------------------------------------------------------------------------------
    call("19.freshness", "portal_get_pipeline_freshness")
    call("19.returns", "portal_get_market_returns")
    call("19.regime", "portal_get_market_regime")
    call("19.macro", "portal_get_macro")
    call("19.valuation", "portal_get_valuation")
    call("19.model_pos", "portal_get_model_positioning")
    call("19.model_attr", "portal_get_model_attribution")
    call("19.mood", "news_market_mood")
    call("19.trending", "news_trending_topics")
    call("19.trending.quietday", "news_trending_topics", date="2026-10-10")
    call("19.keyword", "news_keyword_intelligence", keyword="inflation")
    call("19.search", "news_search_articles", limit=3)
    call("19.for_security.cap", "news_for_security", ticker="AAPL", window_days=999)
    call("19.for_security.14", "news_for_security", ticker="AAPL", window_days=14)
    # ---- ap-20 etfs ---------------------------------------------------------------------------------------------
    call("20.holdings", "etfs_get_fund_holdings", fund_ticker="IDVZ")
    call("20.partner", "etfs_get_partner_ownership")
    call("20.rollup", "etfs_get_ownership_rollup")
    call("20.monthly", "etfs_get_monthly_report")
    call("20.nav", "etfs_get_fund_nav_history", fund_ticker="IDVZ")
    call("20.catviews", "mdpf_get_category_views", scope="global")
    # ---- ap-21 published analysis -----------------------------------------------------------------------------------
    if key:
        for sec in ("overlay", "thesis", "peers", "ledger", "versions", "timeline"):
            call("21." + sec, "harvest_get_published_analysis", security_key=key, sections=sec)
    # ---- ap-23 client + rival ----------------------------------------------------------------------------------------
    call("23.rival.holdings", "etfs_get_rival_fund_holdings", fund_ticker="BASG")
    call("23.rival.coverage", "etfs_get_coverage")
    call("23.rival.page", "etfs_get_rival_page_status")
    call("23.rival.peers", "etfs_get_peer_group_members", home_ticker="IDVZ")
    ctx = cc._new_ctx()
    from app import client_adapter_smartx as sx                              # noqa: E402
    last4s = {}
    try:
        pre = ctx.prefix(sx.VENDOR, sx.SEGMENT, sx.LAYER, sx.T_MAP)
        for p in reversed(ctx.list_partitions(pre)[-10:]):
            rows = ctx.read_rows(pre, p)
            nums = [m.get("account_number") for m in rows if isinstance(m.get("account_number"), str) and len(m.get("account_number")) >= 4]
            if nums:
                last4s["smartx"] = nums[0][-4:]
                break
    except Exception as exc:
        last4s["smartx_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:100])
    cn = cc._names()
    log.append({"tag": "23.firms", "canonical": list(cn.get("canonical", ())), "vendors": list(cc.registered_vendors())})
    if last4s.get("smartx"):
        for fa in list(cn.get("canonical", ()))[:3]:
            r = call("23.resolve." + fa, "client_resolve_account", who="master", firm=fa, account_last4=last4s["smartx"])
            cands = (r or {}).get("candidates") if isinstance(r, dict) else None
            if isinstance(cands, list) and cands:
                vend = {}
                for c in cands:
                    if isinstance(c, dict):
                        vend[c.get("vendor")] = vend.get(c.get("vendor"), 0) + 1
                log.append({"tag": "23.cand_vendors." + fa, "vendors": vend, "cand0_keys": sorted(cands[0])[:20]})
                ref = cands[0].get("account_ref")
                if ref:
                    call("23.holdings." + fa, "client_get_holdings", who="master", firm=fa, account=ref)
                    call("23.allocation." + fa, "client_get_allocation", who="master", firm=fa, account=ref)
                    call("23.fees." + fa, "client_get_fees", who="master", firm=fa, account=ref,
                         from_date="2026-01-01", to_date="2026-03-31")
    print("EV1_DISCOVER_JSON")
    print(json.dumps(log, separators=(",", ":"), default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("EV1_DISCOVER_JSON")
        print(json.dumps([{"fatal": traceback.format_exc()[-1500:]}]))
        sys.exit(1)
