#!/usr/bin/env python
"""OG-ap-20 Phase B: the SERVED read of the six G5 wave A / category-views tools, on the host.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python. Uploaded to S3 and pulled by the
host, never inlined into an SSM command (cloud-ops Rule 12). WRITTEN DURING PHASE A, before the GO, so
the instrument is settled before the window rather than during it; it reads and never applies.

  --registry-only   the registry count and names, then exit (the PRE-deploy read).
  (no flag)         the full read-back.

THE OUTPUT SHAPE IS NOT MINE TO CHOOSE. ap20.AC2 reads, under `body`: `registry_before` and
`registry_count` as INTS with count == before + 6; `policies_live` exactly True; and per tool in
`per_tool`, `opal_served` True, `non_opal_refused` True, `reads_on_refusal` == 0. Those names are
copied from the grader, not invented here -- on OG-ap-18 I measured the right facts under my own names
and they graded as ABSENT. `policies_live` is left None for the CALLER to fill from the IAM read-back,
because a host-side script cannot see IAM and must not pretend to.

FIVE OF THE SIX TOOLS REQUIRE ARGUMENTS, and that is this release's version of a trap OG-ap-19 already
paid for: a no-argument probe passes the Opal admission and is then correctly refused on the contract,
so `opal_served` reads False for a tool working exactly as written. Worse, the valid values are NOT
constants here -- `firm` comes from the catalog row's own partner key segments (`_firms`) and `scope`
from the row's `fork_keys.firm.values` (`_scopes`), both read at call time. So the probe arguments are
DERIVED FROM THE SAME SOURCE THE PREDICATE USES, never typed from a docstring. Only FUND_TICKERS is a
module constant, and even that is read from the module rather than retyped.

THE REFUSAL CODE IS DIFFERENT FROM OG-ap-19'S. These tools admit through typed_scope, whose non-Opal
code is `typed_opal_only`; harvest's is `harvest_opal_only`. Carrying ap-19's accepted-code list over
would have read `non_opal_refused` False for all six while every refusal was working. The detection
therefore accepts the `guard_denied` flag that every refusal dict carries AND records the code, so a
code I did not anticipate shows up as data instead of as a false negative.

ONE READ PLANE. G5 reads S3 only, so there is ONE counter -- but it is installed on typed_scope's
client factory AND on each etfs/mdpf module's own, because each builds its Scope with its own
`_client`. A guard on typed_scope alone would have left three modules unguarded while reporting a
clean zero.

THE AUDIT SINK IS STUBBED, a bound rather than a convenience: audit.log_call -> _emit -> put_object
whenever AUDIT_S3_BUCKET is set, and this order's BOUNDS forbid writing any object.

Nothing sensitive is printed: no object content, no .env value, no address, no tenant or object id. The
probe principal is synthetic and is never written to any store.
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
PROBE_LOCAL = "ap20.served.probe"
PROBE_OID = "00000000-0000-0000-0000-000000000a20"
ROOTS = ("app", "deploy", "dashboard", "lib")
REGISTRY_BEFORE = 69               # the live count at the base 1b18b94979, measured, not assumed

ETFS = ["etfs_get_partner_ownership", "etfs_get_ownership_rollup", "etfs_get_monthly_report",
        "etfs_get_fund_nav_history", "etfs_get_fund_holdings"]
SIX = ETFS + ["mdpf_get_category_views"]
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")
REFUSAL_CODES = ("typed_opal_only", "harvest_opal_only", "opal_only", "principal_required")


class _ReadGuard:
    """Stands in for a client factory's product. Any attribute access counts; calling it raises."""

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


def tree_md5():
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


def _lag_values(res) -> list:
    """Every trading_days_behind_t1 value at any depth, so a nested envelope is not missed."""
    found = []
    if isinstance(res, dict):
        for k, v in res.items():
            found.append(v) if k == "trading_days_behind_t1" else found.extend(_lag_values(v))
    elif isinstance(res, list):
        for v in res:
            found.extend(_lag_values(v))
    return found


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    from app import tools                                              # noqa: E402

    names = registry_names(tools)
    if "--registry-only" in sys.argv:
        print("REGISTRY_JSON")
        print(json.dumps({"registry_count": len(names), "registry_names": sorted(names),
                          "six_present": sorted(n for n in names if n in SIX),
                          "instrument": "app.tools.mcp._tool_manager.list_tools()"}, indent=1))
        return 0

    from app import context, identity_scope                            # noqa: E402
    from app import data_entitlement as de                             # noqa: E402
    from app import etfs_ownership as eto, etfs_funds as etf, portal_mdpf as mdc   # noqa: E402
    from app import typed_scope as ts                                  # noqa: E402

    out = {"body": {}}
    b = out["body"]

    # ---- the registry, on ONE named instrument ------------------------------------------------
    b["registry_instrument"] = "app.tools.mcp._tool_manager.list_tools()"
    b["registry_before"] = REGISTRY_BEFORE
    b["registry_count"] = len(names)
    b["registry_delta"] = len(names) - REGISTRY_BEFORE
    b["six_present"] = sorted(n for n in names if n in SIX)
    b["six_missing"] = sorted(n for n in SIX if n not in names)
    b["repo_side_pin_instrument"] = "tests/test_entitlement_admin.py registered_tool_names = NATIVE|INTEGRATION|INDEX"
    b["repo_side_pin_before_after"] = [88, 94]
    union = set(de.NATIVE_TOOLS) | set(de.INTEGRATION_TOOLS) | set(de.INDEX_TOOLS)
    b["repo_side_union_on_host"] = len(union)
    b["union_minus_live"] = sorted(union - set(names))
    b["live_minus_union"] = sorted(set(names) - union)
    b["six_in_native"] = sorted(t for t in SIX if t in de.NATIVE_TOOLS)
    try:
        from app import destructive_ops as do
        b["six_in_safe"] = sorted(t for t in SIX if t in getattr(do, "SAFE_TOOLS", ()))
    except Exception as exc:
        b["six_in_safe"] = "%s: %s" % (type(exc).__name__, str(exc)[:80])

    # ---- /health ------------------------------------------------------------------------------
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=10) as r:
            b["health_status"] = r.status
            b["health_body"] = r.read(200).decode("utf-8", "replace").strip()
    except Exception as exc:
        b["health_status"] = None
        b["health_body"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])

    # ---- the seams and the running bytes ------------------------------------------------------
    for seam in ("typed_scope.py", "harvest_typed.py", "harvest_read.py"):
        p = os.path.join(ROOT, "app", seam)
        b["seam_" + seam.replace(".py", "")] = md5_path(p) if os.path.isfile(p) else None
    b["catalog_md5"] = (md5_path(os.path.join(ROOT, "app", "refs", "DATA_CATALOG.yaml"))
                        if os.path.isfile(os.path.join(ROOT, "app", "refs", "DATA_CATALOG.yaml")) else None)
    tm, per, absent = tree_md5()
    b["tree_md5"] = tm
    b["tree_md5_files"] = len(tm)
    b["tree_per_root"] = per
    b["tree_absent_roots"] = absent

    # ---- the .env key NAMES (names only, never a value); this release adds none ---------------
    env = os.path.join(ROOT, ".env")
    if os.path.isfile(env):
        keys = []
        with open(env, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    keys.append(line.split("=", 1)[0])
        b["env_key_count"] = len(set(keys))
        b["env_key_names"] = sorted(set(keys))
    else:
        b["env_key_count"] = None

    # ---- the probe arguments, DERIVED from the host's own catalog ------------------------------
    audit_rows = []

    def _recorder(email, tool, args, outcome, detail="", **kw):
        audit_rows.append((tool, outcome, detail))

    for mod in (eto, etf, mdc):
        if hasattr(mod, "audit"):
            mod.audit.log_call = _recorder            # type: ignore[assignment]

    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID,
                                  "%s@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    non_opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "%s@example.invalid" % PROBE_LOCAL)
    context.set_current_principal(opal)

    args = {"firm": None, "fund_ticker": None, "scope_global": None, "scope_firm": None,
            "how": "read from the catalog row at call time, never typed"}
    try:
        resolved = eto._resolve()
        row, why = resolved[eto.GOLD_ENTITY]
        firms = eto._firms(row) if row is not None else ()
        args["firms_enumerated"] = list(firms)
        args["firm"] = firms[0] if firms else None
        args["firm_absent_reason"] = None if row is not None else why
    except Exception as exc:
        args["firm_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    try:
        args["fund_tickers_enumerated"] = list(etf.FUND_TICKERS)
        args["fund_ticker"] = etf.FUND_TICKERS[0]
    except Exception as exc:
        args["fund_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    try:
        # _row takes the LOADED catalog: `_row(loaded)`, not `_row()`. Checked against the release
        # source rather than guessed -- a wrong signature here would fail inside the ledger window.
        mrow = mdc._row(mdc._loaded())
        scopes = mdc._scopes(mrow) if mrow is not None else ()
        args["scopes_enumerated"] = list(scopes)
        args["scope_global"] = "global" if "global" in scopes else (scopes[0] if scopes else None)
        args["scope_firm"] = next((s for s in scopes if s != "global"), None)
    except Exception as exc:
        args["scope_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    b["probe_arguments"] = args

    CALLS = {
        "etfs_get_partner_ownership": lambda: eto.etfs_get_partner_ownership(firm=args["firm"]),
        "etfs_get_ownership_rollup": lambda: eto.etfs_get_ownership_rollup(),
        "etfs_get_monthly_report": lambda: eto.etfs_get_monthly_report(),
        "etfs_get_fund_nav_history": lambda: etf.etfs_get_fund_nav_history(fund_ticker=args["fund_ticker"]),
        "etfs_get_fund_holdings": lambda: etf.etfs_get_fund_holdings(fund_ticker=args["fund_ticker"]),
        "mdpf_get_category_views": lambda: mdc.mdpf_get_category_views(scope=args["scope_global"]),
    }

    def call(fn):
        t0 = time.time()
        try:
            return fn(), round(time.time() - t0, 2), None
        except Exception as exc:
            return None, round(time.time() - t0, 2), "%s: %s" % (type(exc).__name__, str(exc)[:160])

    per_tool, lag = {}, {}
    for tool in SIX:
        res, secs, err = call(CALLS[tool])
        enveloped = isinstance(res, dict) and all(k in res for k in ENVELOPE)
        refused = isinstance(res, dict) and bool(res.get("guard_denied") or res.get("code"))
        per_tool[tool] = {"opal_served": bool(enveloped and not refused), "seconds": secs,
                          "enveloped": enveloped, "error": err,
                          "refusal_code": (res or {}).get("code") if refused else None,
                          "answer_keys": sorted(res)[:12] if isinstance(res, dict) else None}
        vals = _lag_values(res)
        if vals:
            lag[tool] = {"values": vals[:8],
                         "any_numeric": any(isinstance(v, (int, float)) and not isinstance(v, bool) for v in vals)}
    b["trading_days_behind_t1_seen"] = lag
    b["trading_days_behind_t1_numeric"] = bool(lag) and all(v["any_numeric"] for v in lag.values())

    # ---- C5's extra arm: mdpf_get_category_views on global AND on one firm scope --------------
    extra = {}
    for label, sc in (("global", args.get("scope_global")), ("one_firm", args.get("scope_firm"))):
        if not sc:
            extra[label] = {"scope": None, "skipped": "the catalog row enumerated no such scope"}
            continue
        res, secs, err = call(lambda sc=sc: mdc.mdpf_get_category_views(scope=sc))
        extra[label] = {"scope": sc, "seconds": secs, "error": err,
                        "enveloped": isinstance(res, dict) and all(k in res for k in ENVELOPE),
                        "refusal_code": (res or {}).get("code") if isinstance(res, dict) else None,
                        "answer_keys": sorted(res)[:12] if isinstance(res, dict) else None}
    b["category_views_scope_arms"] = extra

    # ---- the refusal arm: ONE plane, but a guard on EVERY module's own client ------------------
    s3_guard = _ReadGuard("S3")
    saved = {}
    for mod in (ts, eto, etf, mdc):
        for attr in ("_client", "_s3", "_s3_client"):
            if hasattr(mod, attr):
                saved[(mod.__name__, attr)] = getattr(mod, attr)
                setattr(mod, attr, (lambda g: (lambda *a, **k: g))(s3_guard))
    b["refusal_guards_installed"] = sorted("%s.%s" % k for k in saved)
    try:
        context.set_current_principal(non_opal)
        for tool in SIX:
            res, secs, err = call(CALLS[tool])
            code = (res or {}).get("code") if isinstance(res, dict) else None
            per_tool[tool]["non_opal_code"] = code
            per_tool[tool]["non_opal_refused"] = bool(
                code in REFUSAL_CODES or (isinstance(res, dict) and res.get("guard_denied")))
            per_tool[tool]["non_opal_error"] = err
    finally:
        for (modname, attr), val in saved.items():
            for mod in (ts, eto, etf, mdc):
                if mod.__name__ == modname:
                    setattr(mod, attr, val)
        context.set_current_principal(opal)

    b["reads_on_refusal"] = s3_guard.calls
    for tool in SIX:
        per_tool[tool]["reads_on_refusal"] = s3_guard.calls
    b["per_tool"] = per_tool
    b["audit_rows_captured"] = len(audit_rows)
    b["audit_sink_stubbed"] = True

    b["policies_live"] = None          # the CALLER fills this from the IAM read-back; a host script cannot see IAM
    b["verdict"] = "PASS-PENDING-IAM" if (
        len(b["six_present"]) == 6
        and b["registry_count"] == REGISTRY_BEFORE + 6
        and all(per_tool[t]["opal_served"] for t in SIX)
        and all(per_tool[t]["non_opal_refused"] for t in SIX)
        and b["reads_on_refusal"] == 0
        and str(b["health_body"]).startswith('{"ok":true')
    ) else "PARTIAL-OR-FAIL"
    print("G5A_SERVED_JSON")
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("G5A_SERVED_JSON")
        print(json.dumps({"body": {"verdict": "FAIL", "fatal": traceback.format_exc()[-1800:]}}, indent=1))
        sys.exit(1)
