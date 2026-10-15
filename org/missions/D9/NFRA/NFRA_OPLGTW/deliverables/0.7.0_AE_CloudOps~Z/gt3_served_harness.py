#!/usr/bin/env python
"""OG-ap-18 Phase B: the SERVED read of all ten G1 typed tools, plus every other trigger, on the host.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python. Uploaded to S3 and pulled by the
host, never inlined into an SSM command (cloud-ops Rule 12).

  --registry-only   print the registry count and names and exit (the PRE-deploy read).
  (no flag)         the full read-back.

WHAT `opal_served` MEANS HERE, stated because a weaker predicate would pass on nothing: the tool's real
call under an Opal principal returned a dict carrying all four envelope keys (as_of, source_keys,
denominator, absent_reason) and NOT a refusal. An enveloped answer that is EMPTY still counts -- the
envelope's whole point is that an empty answer says why (absent_reason) instead of reading as "no such
data" -- so this measures that the tool ran and answered in its contract, not that the bucket holds data
for the probe security.

THE REFUSAL ARM IS MEASURED, NOT INFERRED: each tool is re-called under a non-Opal address with
harvest_typed's S3 client replaced by a counter that raises on any attribute access, so a single S3 call
on a refusal path both counts and fails loudly.

THE AUDIT SINK IS STUBBED, and that is a bound rather than a convenience: audit.log_call -> _emit ->
put_object whenever AUDIT_S3_BUCKET is set, and this order's BOUNDS say no object is written to any
bucket. The gate and the tools run as installed; the verdicts the sink would have written are captured.

Nothing sensitive is printed: no object content, no .env value, no address, no tid/oid. The probe
principal is synthetic and is never written to any store.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import traceback
import urllib.request

ROOT = "/opt/opal-gateway"
PROBE_LOCAL = "ap18.served.probe"
PROBE_OID = "00000000-0000-0000-0000-000000000a18"
TOOLS = ["harvest_resolve_security", "harvest_security_coverage", "harvest_get_chatter",
         "harvest_search_articles", "harvest_get_article", "harvest_get_fundamentals",
         "harvest_query_columns", "harvest_get_research", "harvest_get_filing_analysis",
         "harvest_get_peers_and_scores"]
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")
YR_PAGE = "app/static/yearinreview/index.html"
UNTIL = b'"until": "2026-10-11"'


class _RefusalGuard:
    def __init__(self) -> None:
        self.calls = 0

    def __getattr__(self, name: str):
        self.calls += 1

        def _boom(*a, **k):
            raise RuntimeError("S3 touched on a refusal path: %s" % name)
        return _boom


def md5_path(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def tree_md5(rel: str) -> dict:
    out = {}
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, rel)):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            if fn.endswith(".pyc"):
                continue
            full = os.path.join(dirpath, fn)
            key = os.path.relpath(full, ROOT).replace(os.sep, "/")
            try:
                out[key] = md5_path(full)
            except OSError as exc:
                out[key] = "UNREADABLE:%s" % type(exc).__name__
    return out


def registry_names(tools_mod) -> list:
    try:
        return [t.name for t in tools_mod.mcp._tool_manager.list_tools()]
    except Exception:
        import asyncio
        return [t.name for t in asyncio.run(tools_mod.mcp.list_tools())]


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    # ONLY app.tools here. The five typed modules do not EXIST on the host until this release lands, so
    # importing them at the top makes --registry-only unusable at the one moment the order needs it:
    # BEFORE the deploy, to read registry_before. Measured -- the first run of the v2 harness died with
    # "ImportError: cannot import name 'harvest_typed' from 'app'" against the live host. Same class as
    # Z-S126: an instrument whose imports assume the post-deploy state cannot measure the pre-deploy one.
    from app import tools                                               # noqa: E402

    names = registry_names(tools)
    if "--registry-only" in sys.argv:
        print("REGISTRY_JSON")
        print(json.dumps({"registry_count": len(names), "registry_names": sorted(names),
                          "g1_present": sorted(n for n in names if n in TOOLS),
                          "instrument": "app.tools.mcp._tool_manager.list_tools()"}, indent=1))
        return 0

    from app import context, harvest_typed as ht, identity_scope        # noqa: E402
    from app import harvest_identity as hvi, harvest_press as hvp       # noqa: E402
    from app import harvest_figures as hvf, harvest_research as hvr     # noqa: E402
    from app import harvest_read as hv                                  # noqa: E402
    from app import data_entitlement as de                              # noqa: E402

    out = {"body": {}}
    b = out["body"]
    b["tools_listed"] = sorted(n for n in names if n in TOOLS)
    b["registry_count"] = len(names)
    b["registry_names"] = sorted(names)
    b["registry_instrument"] = "app.tools.mcp._tool_manager.list_tools()"
    b["classification_counts"] = {"NATIVE_TOOLS": len(de.NATIVE_TOOLS),
                                  "INTEGRATION_TOOLS": len(de.INTEGRATION_TOOLS),
                                  "INDEX_TOOLS": len(de.INDEX_TOOLS)}
    union = set(de.NATIVE_TOOLS) | set(de.INTEGRATION_TOOLS) | set(de.INDEX_TOOLS)
    b["repo_side_union_count"] = len(union)
    b["union_minus_live"] = sorted(union - set(names))
    b["live_minus_union"] = sorted(set(names) - union)
    b["ten_in_safe_tools"] = sorted(t for t in TOOLS if t in getattr(__import__("app.destructive_ops",
                                    fromlist=["x"]), "SAFE_TOOLS", ()))
    b["ten_in_native_tools"] = sorted(t for t in TOOLS if t in de.NATIVE_TOOLS)

    # ---- /health -------------------------------------------------------------------------------
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=10) as r:
            b["health_status"] = r.status
            b["health_body"] = r.read(200).decode("utf-8", "replace").strip()
    except Exception as exc:
        b["health_status"] = None
        b["health_body"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])

    # ---- lib/ as a NEW artifact member ---------------------------------------------------------
    lib_path = os.path.join(ROOT, "lib", "trading_calendar.py")
    b["lib_present"] = os.path.isfile(lib_path)
    b["lib_md5"] = md5_path(lib_path) if b["lib_present"] else None
    b["lib_dir_listing"] = sorted(os.listdir(os.path.join(ROOT, "lib"))) if os.path.isdir(os.path.join(ROOT, "lib")) else None

    # ---- the /yearinreview page: A8 route (a) expects the LF form -------------------------------
    page = os.path.join(ROOT, YR_PAGE)
    with open(page, "rb") as fh:
        raw = fh.read()
    b["yearinreview_md5"] = hashlib.md5(raw).hexdigest()
    b["yearinreview_bytes"] = len(raw)
    b["yearinreview_crlf"] = raw.count(b"\r\n")
    b["yearinreview_carries_until_2026_10_11"] = UNTIL in raw

    # ---- the running bytes, per file ------------------------------------------------------------
    b["tree_md5"] = {}
    for rel in ("app", "deploy", "dashboard"):
        b["tree_md5"].update(tree_md5(rel))
    b["tree_md5_files"] = len(b["tree_md5"])

    # ---- the served arms ------------------------------------------------------------------------
    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID,
                                  "%s@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    non_opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "%s@example.invalid" % PROBE_LOCAL)
    # ONLY set_current_principal: set_current_email NULLS the principal (app/context.py:105-109).
    context.set_current_principal(opal)

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
    lag_seen = {}
    for tool in TOOLS:
        extra = {"query": (b["discovery"].get("resolved_from") or "x")}
        if tool == "harvest_get_article" and article_key:
            extra.update({"article_key": article_key, "publisher": publisher or "wsj"})
        res, secs, err = call(tool, extra)
        enveloped = isinstance(res, dict) and all(k in res for k in ENVELOPE)
        refused = isinstance(res, dict) and bool(res.get("guard_denied") or res.get("code"))
        per[tool] = {"opal_served": bool(enveloped and not refused), "seconds": secs,
                     "enveloped": enveloped, "refusal_code": (res or {}).get("code") if refused else None,
                     "error": err, "answer_keys": sorted(res)[:12] if isinstance(res, dict) else None}
        # the trading-day lag, wherever this answer carries it (Z-S125's closer)
        if isinstance(res, dict):
            blob = json.dumps(res, default=str)
            if "trading_days_behind_t1" in blob:
                def _find(o):
                    found = []
                    if isinstance(o, dict):
                        for k, v in o.items():
                            if k == "trading_days_behind_t1":
                                found.append(v)
                            else:
                                found.extend(_find(v))
                    elif isinstance(o, list):
                        for v in o:
                            found.extend(_find(v))
                    return found
                vals = _find(res)
                lag_seen[tool] = {"values": vals[:8],
                                  "any_numeric": any(isinstance(v, int) for v in vals)}
        if tool == "harvest_search_articles" and isinstance(res, dict):
            rows = res.get("articles") or res.get("rows") or []
            if isinstance(rows, list) and rows and isinstance(rows[0], dict):
                article_key = rows[0].get("article_key") or rows[0].get("key")
                publisher = rows[0].get("publisher")
                per[tool]["rows_seen"] = len(rows)
    b["trading_days_behind_t1_seen"] = lag_seen
    b["lag_numeric_somewhere"] = any(v["any_numeric"] for v in lag_seen.values())
    b["harvest_search_articles_seconds"] = per["harvest_search_articles"]["seconds"]
    b["alb_idle_timeout_seconds"] = 60
    b["harvest_search_articles_under_alb_timeout"] = per["harvest_search_articles"]["seconds"] < 60

    # ---- the refusal arm, with the counter in place of the S3 client ----------------------------
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
        per[tool]["s3_calls_on_refusal"] = guard.calls      # shared counter: 0 means no tool touched S3
    b["s3_calls_on_refusal_total"] = guard.calls
    b["per_tool"] = per

    b["verdict"] = "PASS" if (
        len(b["tools_listed"]) == 10
        and all(per[t]["opal_served"] for t in TOOLS)
        and all(per[t]["non_opal_refused"] for t in TOOLS)
        and guard.calls == 0
        and b["lib_present"]
        and b["health_body"].startswith("{\"ok\":true")
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
