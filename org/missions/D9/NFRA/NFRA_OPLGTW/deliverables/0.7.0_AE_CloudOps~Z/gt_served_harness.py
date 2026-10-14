#!/usr/bin/env python
"""OG-ap-18 step 5: the SERVED read of all ten G1 typed tools, through the INSTALLED code.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python. Uploaded to S3 and pulled by the
host, never inlined into an SSM command (cloud-ops Rule 12).

  --registry-only   print the registry count and exit. Run BEFORE the deploy to get registry_before.
  (no flag)         the full served read.

WHAT `opal_served` MEANS HERE, stated because a weaker predicate would pass on nothing: the tool's real
call under an Opal principal returned a dict carrying all four envelope keys (as_of, source_keys,
denominator, absent_reason) and NOT a refusal. An enveloped answer that is EMPTY still counts -- the
envelope's whole point is that an empty answer says why (absent_reason) instead of reading as "no such
data" -- so this measures that the tool ran and answered in its contract, not that the bucket holds
data for the probe security.

THE REFUSAL ARM IS MEASURED, NOT INFERRED: each tool is re-called under a non-Opal address with
harvest_typed's S3 client replaced by a counter that raises on any attribute access, so a single S3
call on a refusal path both counts and fails loudly.

Nothing sensitive is printed: no object content, no .env value, no address, no tid/oid. The probe
principal is synthetic and is never written to any store.
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback

ROOT = "/opt/opal-gateway"
PROBE_LOCAL = "ap18.served.probe"
PROBE_OID = "00000000-0000-0000-0000-000000000a18"
TOOLS = ["harvest_resolve_security", "harvest_security_coverage", "harvest_get_chatter",
         "harvest_search_articles", "harvest_get_article", "harvest_get_fundamentals",
         "harvest_query_columns", "harvest_get_research", "harvest_get_filing_analysis",
         "harvest_get_peers_and_scores"]
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")


class _RefusalGuard:
    def __init__(self) -> None:
        self.calls = 0

    def __getattr__(self, name: str):
        self.calls += 1

        def _boom(*a, **k):
            raise RuntimeError("S3 touched on a refusal path: %s" % name)
        return _boom


def registry_names(tools_mod) -> list:
    try:
        return [t.name for t in tools_mod.mcp._tool_manager.list_tools()]
    except Exception:
        import asyncio
        return [t.name for t in asyncio.run(tools_mod.mcp.list_tools())]


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    from app import context, harvest_typed as ht, identity_scope, tools  # noqa: E402
    from app import harvest_identity as hvi, harvest_press as hvp       # noqa: E402
    from app import harvest_figures as hvf, harvest_research as hvr     # noqa: E402
    from app import harvest_read as hv                                  # noqa: E402

    names = registry_names(tools)
    if "--registry-only" in sys.argv:
        print("REGISTRY_JSON")
        print(json.dumps({"registry_count": len(names),
                          "g1_present": sorted(n for n in names if n in TOOLS),
                          "instrument": "app.tools.mcp._tool_manager.list_tools()"}, indent=1))
        return 0

    out = {"body": {}}
    b = out["body"]
    b["tools_listed"] = sorted(n for n in names if n in TOOLS)
    b["registry_count"] = len(names)
    b["registry_instrument"] = "app.tools.mcp._tool_manager.list_tools()"

    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID,
                                  "%s@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    non_opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "%s@example.invalid" % PROBE_LOCAL)
    # ONLY set_current_principal: set_current_email NULLS the principal (app/context.py:105-109).
    context.set_current_principal(opal)

    # --- discover a real security from the bucket rather than hardcoding one -------------------
    probe, disco = None, {}
    try:
        listing = hv.harvest_list("packs/")
        pres = [p.rstrip("/").split("/")[-1] for p in (listing.get("common_prefixes") or [])]
        disco = {"packs_prefixes_seen": len(pres)}
        if pres:
            r = hvi.harvest_resolve_security(pres[0])
            cands = r.get("matches") or r.get("securities") or []
            probe = (cands[0].get("security_key") if isinstance(cands, list) and cands and isinstance(cands[0], dict)
                     else r.get("security_key"))
            disco["resolved_from"] = pres[0]
    except Exception as exc:
        disco["discovery_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
    probe = probe or "UNRESOLVED"
    disco["probe_security_key_resolved"] = probe != "UNRESOLVED"
    b["discovery"] = disco

    def call(tool: str, extra: dict):
        fn = {"harvest_resolve_security": lambda: hvi.harvest_resolve_security(extra.get("query", "")),
              "harvest_security_coverage": lambda: hvi.harvest_security_coverage(probe),
              "harvest_get_chatter": lambda: hvp.harvest_get_chatter(probe, "2026-10-01", "2026-10-14"),
              "harvest_search_articles": lambda: hvp.harvest_search_articles(probe),
              "harvest_get_article": lambda: hvp.harvest_get_article(extra.get("article_key", "none"),
                                                                     extra.get("publisher", "wsj")),
              "harvest_get_fundamentals": lambda: hvf.harvest_get_fundamentals(probe, "reference"),
              "harvest_query_columns": lambda: hvf.harvest_query_columns("chatter_daily", ["security_key"],
                                                                         security_keys=[probe]),
              "harvest_get_research": lambda: hvr.harvest_get_research(probe),
              "harvest_get_filing_analysis": lambda: hvr.harvest_get_filing_analysis(probe),
              "harvest_get_peers_and_scores": lambda: hvr.harvest_get_peers_and_scores(probe)}[tool]
        t0 = time.time()
        try:
            res = fn()
            return res, round(time.time() - t0, 2), None
        except Exception as exc:
            return None, round(time.time() - t0, 2), "%s: %s" % (type(exc).__name__, str(exc)[:160])

    per = {}
    article_key, publisher = None, None
    for tool in TOOLS:
        extra = {"query": (b["discovery"].get("resolved_from") or "x")}
        if tool == "harvest_get_article" and article_key:
            extra.update({"article_key": article_key, "publisher": publisher or "wsj"})
        res, secs, err = call(tool, extra)
        enveloped = isinstance(res, dict) and all(k in res for k in ENVELOPE)
        refused = isinstance(res, dict) and bool(res.get("guard_denied") or res.get("code"))
        per[tool] = {"opal_served": bool(enveloped and not refused), "seconds": secs,
                     "enveloped": enveloped, "refusal_code": (res or {}).get("code") if refused else None,
                     "error": err, "answer_keys": sorted(res)[:10] if isinstance(res, dict) else None}
        if tool == "harvest_search_articles" and isinstance(res, dict):
            rows = res.get("articles") or res.get("rows") or []
            if isinstance(rows, list) and rows and isinstance(rows[0], dict):
                article_key = rows[0].get("article_key") or rows[0].get("key")
                publisher = rows[0].get("publisher")
                per[tool]["rows_seen"] = len(rows)

    # --- the refusal arm, with the counter in place of the S3 client --------------------------
    guard = _RefusalGuard()
    real = ht._client if hasattr(ht, "_client") else None
    if real is not None:
        ht._client = lambda: guard
    try:
        context.set_current_principal(non_opal)
        for tool in TOOLS:
            res, secs, err = call(tool, {"query": "x", "article_key": "none", "publisher": "wsj"})
            code = (res or {}).get("code") if isinstance(res, dict) else None
            per[tool]["non_opal_refused"] = (code == "harvest_opal_only")
            per[tool]["non_opal_code"] = code
            per[tool]["non_opal_error"] = err
    finally:
        if real is not None:
            ht._client = real
        context.set_current_principal(opal)
    for tool in TOOLS:
        per[tool]["s3_calls_on_refusal"] = guard.calls      # the counter is shared: 0 means no tool touched S3
    b["s3_calls_on_refusal_total"] = guard.calls
    b["per_tool"] = per

    b["verdict"] = "PASS" if (
        len(b["tools_listed"]) == 10
        and all(per[t]["opal_served"] for t in TOOLS)
        and all(per[t]["non_opal_refused"] for t in TOOLS)
        and guard.calls == 0
    ) else "PARTIAL-OR-FAIL"
    print("GT_SERVED_JSON")
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("GT_SERVED_JSON")
        print(json.dumps({"body": {"verdict": "FAIL", "fatal": traceback.format_exc()[-1500:]}}, indent=1))
        sys.exit(1)
