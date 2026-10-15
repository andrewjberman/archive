#!/usr/bin/env python
"""OG-ap-19 Phase B: the SERVED read of all thirteen G3/G6 tools, plus every trigger, on the host.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python. Uploaded to S3 and pulled by the
host, never inlined into an SSM command (cloud-ops Rule 12).

  --registry-only   the registry count and names, then exit (the PRE-deploy read).
  (no flag)         the full read-back.

ONE INSTRUMENT FOR THE REGISTRY DELTA, as the GO requires: app.tools.mcp._tool_manager.list_tools().
The repo-side pin (tests/test_entitlement_admin.py, 75 -> 88) is a DIFFERENT instrument counting a
DIFFERENT population -- the union of NATIVE | INTEGRATION | INDEX -- and both are reported here with
their names so neither is mistaken for the other. OG-ap-18's STEP 0 established that the live registry
holds NATIVE tools only and that the gap to the repo-side union is exactly INTEGRATION | INDEX; this
run re-checks that identity rather than assuming it survived.

THE REFUSAL ARM IS MEASURED, NOT INFERRED: each tool is re-called under a non-Opal address with the
scope seam's S3 client AND the news path's DynamoDB client replaced by counters that raise on any
attribute access, so a single read on a refusal path both counts and fails loudly. G3 reads S3 and G6
reads DynamoDB, so there are TWO counters and `reads_on_refusal` is their sum -- one counter would have
left the five news tools unguarded while reporting a clean zero.

THE AUDIT SINK IS STUBBED, and that is a bound rather than a convenience: audit.log_call -> _emit ->
put_object whenever AUDIT_S3_BUCKET is set, and this order's BOUNDS forbid writing any object.

Nothing sensitive is printed: no object content, no .env value, no address, no tenant or object id.
The probe principal is synthetic and is never written to any store.
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
PROBE_LOCAL = "ap19.served.probe"
PROBE_OID = "00000000-0000-0000-0000-000000000a19"
ROOTS = ("app", "deploy", "dashboard", "lib")
NEWS_KEYS = ("NEWS_ARTICLES_TABLE", "NEWS_TRENDING_TABLE", "NEWS_KEYWORD_TABLE")

G3 = ["portal_get_model_positioning", "portal_get_model_attribution", "portal_get_market_returns",
      "portal_get_market_regime", "portal_get_macro", "portal_get_valuation",
      "portal_get_security_scan", "portal_get_pipeline_freshness"]
G6 = ["news_search_articles", "news_trending_topics", "news_keyword_intelligence",
      "news_market_mood", "news_for_security"]
THIRTEEN = G3 + G6
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")


class _ReadGuard:
    """Stands in for a client. Any attribute access counts; calling it raises."""

    def __init__(self, label: str) -> None:
        self.calls = 0
        self.label = label

    def __getattr__(self, name: str):
        self.calls += 1

        def _boom(*a, **k):
            raise RuntimeError("%s touched on a refusal path: %s" % (self.label, name))
        return _boom


def md5_path(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def tree_md5() -> dict:
    out, per, absent = {}, {}, []
    for rel in ROOTS:
        base = os.path.join(ROOT, rel)
        if not os.path.isdir(base):
            absent.append(rel)
            per[rel] = None               # None, never 0: absent is not empty
            continue
        n = 0
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in filenames:
                if fn.endswith(".pyc"):
                    continue
                full = os.path.join(dirpath, fn)
                out[os.path.relpath(full, ROOT).replace(os.sep, "/")] = md5_path(full)
                n += 1
        per[rel] = n
    return out, per, absent


def registry_names(tools_mod) -> list:
    try:
        return [t.name for t in tools_mod.mcp._tool_manager.list_tools()]
    except Exception:
        import asyncio
        return [t.name for t in asyncio.run(tools_mod.mcp.list_tools())]


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    from app import tools                                              # noqa: E402

    names = registry_names(tools)
    if "--registry-only" in sys.argv:
        print("REGISTRY_JSON")
        print(json.dumps({"registry_count": len(names), "registry_names": sorted(names),
                          "thirteen_present": sorted(n for n in names if n in THIRTEEN),
                          "instrument": "app.tools.mcp._tool_manager.list_tools()"}, indent=1))
        return 0

    from app import context, identity_scope                            # noqa: E402
    from app import data_entitlement as de                             # noqa: E402
    from app import portal_models as pm, portal_macro as mc, news_typed as nw   # noqa: E402
    from app import typed_scope as ts                                  # noqa: E402

    out = {"body": {}}
    b = out["body"]

    # ---- the registry, on ONE named instrument -----------------------------------------------
    b["registry_instrument"] = "app.tools.mcp._tool_manager.list_tools()"
    b["registry_before"] = 56
    b["registry_count"] = len(names)
    b["registry_delta"] = len(names) - 56
    b["thirteen_present"] = sorted(n for n in names if n in THIRTEEN)
    b["thirteen_missing"] = sorted(n for n in THIRTEEN if n not in names)
    b["repo_side_pin_instrument"] = "tests/test_entitlement_admin.py registered_tool_names = NATIVE|INTEGRATION|INDEX"
    b["repo_side_pin_before_after"] = [75, 88]
    union = set(de.NATIVE_TOOLS) | set(de.INTEGRATION_TOOLS) | set(de.INDEX_TOOLS)
    b["repo_side_union_on_host"] = len(union)
    b["union_minus_live"] = sorted(union - set(names))
    b["live_minus_union"] = sorted(set(names) - union)
    b["classification_counts"] = {"NATIVE_TOOLS": len(de.NATIVE_TOOLS),
                                  "INTEGRATION_TOOLS": len(de.INTEGRATION_TOOLS),
                                  "INDEX_TOOLS": len(de.INDEX_TOOLS)}
    b["thirteen_in_native"] = sorted(t for t in THIRTEEN if t in de.NATIVE_TOOLS)
    try:
        from app import destructive_ops as do
        b["thirteen_in_safe"] = sorted(t for t in THIRTEEN if t in getattr(do, "SAFE_TOOLS", ()))
    except Exception as exc:
        b["thirteen_in_safe"] = "%s: %s" % (type(exc).__name__, str(exc)[:80])

    # ---- /health ------------------------------------------------------------------------------
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=10) as r:
            b["health_status"] = r.status
            b["health_body"] = r.read(200).decode("utf-8", "replace").strip()
    except Exception as exc:
        b["health_status"] = None
        b["health_body"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])

    # ---- the seam, and the running bytes ------------------------------------------------------
    b["typed_scope_on_host"] = os.path.isfile(os.path.join(ROOT, "app", "typed_scope.py"))
    b["typed_scope_md5"] = (md5_path(os.path.join(ROOT, "app", "typed_scope.py"))
                            if b["typed_scope_on_host"] else None)
    tm, per, absent = tree_md5()
    b["tree_md5"] = tm
    b["tree_md5_files"] = len(tm)
    b["tree_per_root"] = per
    b["tree_absent_roots"] = absent

    # ---- the three NEWS_* key NAMES (names only, never a value) -------------------------------
    env = os.path.join(ROOT, ".env")
    if os.path.isfile(env):
        keys = []
        with open(env, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    keys.append(line.split("=", 1)[0])
        b["env_key_count"] = len(set(keys))
        b["news_keys_present"] = sorted(k for k in set(keys) if k in NEWS_KEYS)
        b["env_key_names_present"] = sorted(b["news_keys_present"]) == sorted(NEWS_KEYS)
    else:
        b["env_key_names_present"] = None

    # ---- the served arms ----------------------------------------------------------------------
    audit_rows = []

    def _recorder(email, tool, args, outcome, detail="", **kw):
        audit_rows.append((tool, outcome, detail))

    for mod in (pm, mc, nw):
        if hasattr(mod, "audit"):
            mod.audit.log_call = _recorder            # type: ignore[assignment]

    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID,
                                  "%s@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    non_opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "%s@example.invalid" % PROBE_LOCAL)
    context.set_current_principal(opal)

    CALLS = {
        "portal_get_model_positioning": lambda: pm.portal_get_model_positioning(),
        "portal_get_model_attribution": lambda: pm.portal_get_model_attribution(),
        "portal_get_market_returns": lambda: pm.portal_get_market_returns(),
        "portal_get_market_regime": lambda: pm.portal_get_market_regime(),
        "portal_get_macro": lambda: mc.portal_get_macro(),
        "portal_get_valuation": lambda: mc.portal_get_valuation(),
        "portal_get_security_scan": lambda: mc.portal_get_security_scan("sp500"),
        "portal_get_pipeline_freshness": lambda: mc.portal_get_pipeline_freshness(),
        # These two REQUIRE arguments and refuse harvest_bad_argument without them -- measured: a
        # no-argument probe passes the Opal admission and is then correctly refused on the contract, so
        # `opal_served` read False for a tool that was working exactly as written. A wrong-shape call
        # against a real parser returns a real-looking refusal; the arguments below are the shape the
        # module's own guards demand (a dated window inside WINDOW_CAP_DAYS, and a keyword).
        "news_search_articles": lambda: nw.news_search_articles(date_from="2026-10-08", date_to="2026-10-14"),
        "news_trending_topics": lambda: nw.news_trending_topics(),
        "news_keyword_intelligence": lambda: nw.news_keyword_intelligence(keyword="inflation"),
        "news_market_mood": lambda: nw.news_market_mood(),
        "news_for_security": lambda: nw.news_for_security(ticker="AAPL"),
    }

    def call(tool):
        t0 = time.time()
        try:
            res = CALLS[tool]()
            return res, round(time.time() - t0, 2), None
        except Exception as exc:
            return None, round(time.time() - t0, 2), "%s: %s" % (type(exc).__name__, str(exc)[:160])

    per_tool, lag = {}, {}
    for tool in THIRTEEN:
        res, secs, err = call(tool)
        enveloped = isinstance(res, dict) and all(k in res for k in ENVELOPE)
        refused = isinstance(res, dict) and bool(res.get("guard_denied") or res.get("code"))
        per_tool[tool] = {"opal_served": bool(enveloped and not refused), "seconds": secs,
                          "enveloped": enveloped, "error": err,
                          "refusal_code": (res or {}).get("code") if refused else None,
                          "answer_keys": sorted(res)[:12] if isinstance(res, dict) else None}
        if isinstance(res, dict) and "trading_days_behind_t1" in json.dumps(res, default=str):
            def _find(o):
                f = []
                if isinstance(o, dict):
                    for k, v in o.items():
                        f.append(v) if k == "trading_days_behind_t1" else f.extend(_find(v))
                elif isinstance(o, list):
                    for v in o:
                        f.extend(_find(v))
                return f
            vals = _find(res)
            lag[tool] = {"values": vals[:8], "any_numeric": any(isinstance(v, int) for v in vals)}
    b["trading_days_behind_t1_seen"] = lag
    b["trading_days_behind_t1_numeric"] = bool(lag) and any(v["any_numeric"] for v in lag.values())

    # ---- the refusal arm: TWO counters, S3 for G3 and DynamoDB for G6 -------------------------
    s3_guard = _ReadGuard("S3")
    ddb_guard = _ReadGuard("DynamoDB")
    saved = {}
    for mod, attr, guard in ((ts, "_client", s3_guard), (pm, "_client", s3_guard),
                             (mc, "_client", s3_guard), (nw, "_client", ddb_guard),
                             (nw, "_table", ddb_guard), (nw, "_ddb", ddb_guard)):
        if hasattr(mod, attr):
            saved[(mod.__name__, attr)] = getattr(mod, attr)
            setattr(mod, attr, (lambda g: (lambda *a, **k: g))(guard))
    b["refusal_guards_installed"] = sorted("%s.%s" % k for k in saved)
    try:
        context.set_current_principal(non_opal)
        for tool in THIRTEEN:
            res, secs, err = call(tool)
            code = (res or {}).get("code") if isinstance(res, dict) else None
            per_tool[tool]["non_opal_code"] = code
            per_tool[tool]["non_opal_refused"] = bool(
                code in ("harvest_opal_only", "opal_only", "principal_required")
                or (isinstance(res, dict) and res.get("guard_denied")))
            per_tool[tool]["non_opal_error"] = err
    finally:
        for (modname, attr), val in saved.items():
            for mod in (ts, pm, mc, nw):
                if mod.__name__ == modname:
                    setattr(mod, attr, val)
        context.set_current_principal(opal)

    b["reads_on_refusal"] = s3_guard.calls + ddb_guard.calls
    b["reads_on_refusal_s3"] = s3_guard.calls
    b["reads_on_refusal_dynamodb"] = ddb_guard.calls
    for tool in THIRTEEN:
        per_tool[tool]["reads_on_refusal"] = b["reads_on_refusal"]
    b["per_tool"] = per_tool
    b["audit_rows_captured"] = len(audit_rows)
    b["audit_sink_stubbed"] = True

    b["policies_live"] = None          # filled by the caller from the IAM read-backs
    b["verdict"] = "PASS" if (
        len(b["thirteen_present"]) == 13
        and b["registry_count"] == 69
        and all(per_tool[t]["opal_served"] for t in THIRTEEN)
        and all(per_tool[t]["non_opal_refused"] for t in THIRTEEN)
        and b["reads_on_refusal"] == 0
        and b["typed_scope_on_host"]
        and b["env_key_names_present"]
        and str(b["health_body"]).startswith('{"ok":true')
    ) else "PARTIAL-OR-FAIL"
    print("G36_SERVED_JSON")
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("G36_SERVED_JSON")
        print(json.dumps({"body": {"verdict": "FAIL", "fatal": traceback.format_exc()[-1800:]}}, indent=1))
        sys.exit(1)
