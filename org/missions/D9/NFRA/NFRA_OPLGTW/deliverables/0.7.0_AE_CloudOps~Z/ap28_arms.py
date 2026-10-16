#!/usr/bin/env python
"""OG-ap-28 Phase B step 5: the seven round-38 ARMS through the INSTALLED code on the gateway host. One file, two roles:
  python ap28_arms.py <out.json>   -> the RUNNER (repository root): uploads itself to S3, runs once over SSM (Rule 12), writes the record
  python ap28_arms.py --host       -> the HOST program (on i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python)

READ-ONLY. The audit sink is stubbed (log_call) and the 429 arm captures the row at the writer's emit seam instead of writing it (no object or item is written anywhere).
Counts and booleans only: no object content, account number, person's name or credential is printed; role NAMES only.

Honest limits, stated here and in the record:
  * A real bearer for e10 cannot be minted without writing to the access-state table (a refresh family), which the order forbids. So the arm drives the REAL installed
    GuardMiddleware and the REAL ratelimit/audit code in-process with the bearer lookup stubbed to ONE synthetic stand-in principal and the live limit (120 per 60 s)
    unchanged. The live service's own limiter is not touched.
  * The 429 row is captured at audit._emit, the writer's last seam, not read back from the lake.
  * e8's tools_list is the master_admin stand-in's (the measure used for tools_list_before); /teams/poll is a real GET to the running service.
Arms:
  e4  a client position answer carries weight_unit in {fraction, percent} and a currency (tried on the 49F Black Diamond holdings, then SmartX; orion's unit stays null)
  e5  an empty news_search_articles window carries coverage_floor
  e6  a chatter answer carries an integer trading_days_behind_t1
  e8  MUSE_CLIENT_ID is not set, tools_list equals tools_list_before, GET /teams/poll answers any status but 404
  e9  gateway_query_catalog on a key with no catalog row answers http_status 404
  e10 130 POSTs through GuardMiddleware as one stand-in: the first 120 are not 429, the 121st onward are 429, one gw_ratelimit row with hashed by_client and no email
  e12 (a) the four 49F Black Diamond -live tools, master_admin: enveloped, rows above 0, first source key in opal-data-bd, as_of the newest dated file, assumed role
      gateway-49f-blackdiamond-live-read-role; (b) one unprofiled non-admin call is refused with 0 S3 client requests"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import time
import traceback

ROOT = "/opt/opal-gateway"
FIRM = "49financial"
PROBE_OID = "00000000-0000-0000-0000-00000000a128"
PROBE_OID_2 = "00000000-0000-0000-0000-00000000b128"
LIVE_ROLE = "gateway-49f-blackdiamond-live-read-role"
WINDOW_DAYS = 360
TOOLS4 = ("client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees")


class Counter:
    def __init__(self):
        self.calls = 0

    def __call__(self, *a, **k):
        self.calls += 1
        raise RuntimeError("a data client was requested on a refusal path")


def walk(obj, key, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                out.append(v)
            walk(v, key, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, key, out)
    return out


def role_name(arn):
    m = re.search(r":(?:assumed-role|role)/([^/]+)", str(arn))
    return m.group(1) if m else "unparsed"


def load_env():
    n = 0
    with open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)
                n += 1
    return n


def host() -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    out = {"arms": {}, "detail": {}}
    A, D = out["arms"], out["detail"]
    D["env_lines_loaded"] = load_env()
    import asyncio
    import datetime as dt
    import urllib.error
    import urllib.request
    import boto3
    from app import audit, client_core as cc, client_role, context, identity_scope, internal_role, tools
    from app import server  # importing it registers the integration tools (gateway_query_catalog); the e10 arm reuses it
    from app import client_adapter_bd49f as bd
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    dom = identity_scope.OPAL_USERS_DOMAIN
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    if not roster:
        out["fatal"] = "no master_admin roster entry"
        return out
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ap28.master@%s" % dom)
    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "ap28.opal@%s" % dom)
    opal2 = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID_2, "ap28.opal2@%s" % dom)
    tools._user_token = lambda: ("ap28.master@%s" % dom, "harness-no-token")
    today = dt.datetime.now(dt.timezone.utc).date()

    def call(who, tool, **kw):
        context.set_current_principal(who)
        try:
            return getattr(tools, tool)(**kw)
        except Exception as exc:
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:120]), "_exc": True}

    # ---- the clients the adapter uses, for the role name (names only) --------------------------------------------------
    seen_clients = []
    orig_cf = client_role.client_for

    def cf(key, *a, **k):
        c = orig_cf(key, *a, **k)
        seen_clients.append((key, c))
        return c
    client_role.client_for = cf

    def roles_of(clients):
        roles = set()
        for _k, c in clients:
            try:
                cr = c._get_credentials().get_frozen_credentials()
                s = boto3.client("sts", aws_access_key_id=cr.access_key, aws_secret_access_key=cr.secret_key, aws_session_token=cr.token)
                roles.add(role_name(s.get_caller_identity().get("Arn")))
            except Exception as exc:
                roles.add("unread:" + type(exc).__name__)
        return sorted(roles)

    # ---- e12 (a) and the account ref ---------------------------------------------------------------------------------
    ctx = cc._new_ctx()
    bd.bind_firms()
    segment = bd._firm(ctx, FIRM)
    pre = ctx.prefix(bd.VENDOR, segment, "silver", "dim_account_xref")
    part = bd._select(ctx, pre, None)
    rows = ctx.read_rows(pre, part, columns=list(bd.DIM_COLUMNS)) if part else []
    kept, _x = bd._fence(rows, "bd_account_id")
    # an account the resolver returns that the four LIVE tables all hold: intersect the account ids of the newest live partition of each table
    xr = {r.get("bd_account_id"): r.get("bd_account_number") for r in kept}
    sets, live_parts = {}, {}
    for tname in ("unrealized", "transactions", "allocations", "fees"):
        lp = bd._live_prefix(ctx, segment, tname)
        lpart = bd._select(ctx, lp, None)
        live_parts[tname] = lpart
        if tname in ("transactions", "fees"):      # only accounts with a row inside the window the call will ask for
            cutoff = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
            sets[tname] = {r.get("account_id") for r in ctx.read_rows(lp, lpart, columns=["account_id", "trade_date"] + (list(bd.FEE_COLUMNS) if tname == "fees" else []))
                                if str(r.get("trade_date") or "")[:10] >= cutoff and (tname != "fees" or any(r.get(c) not in (None, 0) for c in bd.FEE_COLUMNS))} if lpart else set()
        else:
            sets[tname] = {r.get("account_id") for r in ctx.read_rows(lp, lpart, columns=["account_id"])} if lpart else set()
    try:
        sample = ctx.read_rows(bd._live_prefix(ctx, segment, "unrealized"), live_parts["unrealized"])[:1]
        D["e4_bd_unrealized_currency_like_columns"] = sorted(c for c in (sample[0].keys() if sample else []) if "curr" in c.lower() or "ccy" in c.lower())
    except Exception as exc:
        D["e4_bd_unrealized_columns_error"] = type(exc).__name__
    D["e12_live_partition_account_counts"] = {k: len(v) for k, v in sets.items()}
    common = sorted(set.intersection(*sets.values()) & set(xr)) if all(sets.values()) else []
    D["e12_accounts_in_all_four_live_tables"] = len(common)
    ref, l4, tried_accounts = None, None, 0
    D["e12_resolver_blackdiamond_candidates"] = 0
    for pick in common[:60]:
        l4 = bd._last4(xr.get(pick))
        if not l4:
            continue
        tried_accounts += 1
        res = call(master, "client_resolve_account", firm=FIRM, account_last4=l4)
        cands = [c for c in ((res or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "blackdiamond"] if isinstance(res, dict) else []
        D["e12_resolver_blackdiamond_candidates"] = max(D["e12_resolver_blackdiamond_candidates"], len(cands))
        if tried_accounts <= 3:
            allc = (res or {}).get("candidates") if isinstance(res, dict) else None
            D.setdefault("e12_dbg", []).append({"top_keys": sorted(res)[:10] if isinstance(res, dict) else None, "error": str((res or {}).get("error", ""))[:100] if isinstance(res, dict) else None,
                                                "absent_reason": (res or {}).get("absent_reason") if isinstance(res, dict) else None,
                                                "n_candidates_all": len(allc) if isinstance(allc, list) else None,
                                                "vendors": sorted({str(c.get("vendor")) for c in (allc or []) if isinstance(c, dict)}),
                                                "pick_in_xref": pick in xr, "pick_prefix_ok": str(pick).startswith(bd.ACCOUNT_PREFIX)})
        for c in cands:
            if str(pick) in str(c.get("account_ref") or ""):    # the served tool's ref carries the vendor id (protocol form)
                ref = c.get("account_ref")
                break
        if ref:
            break
    D["e12_resolver_tries"] = tried_accounts
    D["e12_ref_is_a_resolver_candidate"] = ref is not None
    per, ok_all, bd_holdings = {}, bool(ref), None
    for t in TOOLS4:
        del seen_clients[:]
        kw = {"firm": FIRM, "account": ref}
        if t in ("client_get_transactions", "client_get_fees"):
            kw.update({"from_date": (today - dt.timedelta(days=WINDOW_DAYS)).isoformat(), "to_date": today.isoformat()})
        res = call(master, t, **kw) if ref else {"error": "no ref"}
        keys = (res.get("_source_keys") or res.get("source_keys") or []) if isinstance(res, dict) else []
        nrows = sum(len(v) for k, v in res.items() if isinstance(v, list) and v and isinstance(v[0], dict) and k != "candidates") if isinstance(res, dict) else 0
        bucket_ok = newest_ok = False
        braw = berr = None
        if keys:
            first = str(keys[0])
            tprefix = first.rsplit("/", 1)[0] + "/"
            try:
                row = ctx._row_for(tprefix)
                braw = row.get("bucket")
                bucket_ok = (braw == "opal-data-bd")
                pdate = (res.get("_partition_date") or res.get("partition_date") or "")
                newest_ok = bool(pdate) and pdate == ctx.newest_partition(tprefix)
            except Exception as exc:
                berr = type(exc).__name__
        roles = roles_of(seen_clients)
        per[t] = {"enveloped": bool(isinstance(res, dict) and (res.get("_source_keys") is not None or res.get("source_keys") is not None)),
                  "absent_reason": (res.get("absent_reason") or res.get("_absent_reason")) if isinstance(res, dict) else None,
                  "top_keys": sorted(res)[:14] if isinstance(res, dict) else None, "code": res.get("code") if isinstance(res, dict) else None,
                  "error": str(res.get("error", ""))[:110] if isinstance(res, dict) else None,
                  "rows": nrows, "bucket_is_opal_data_bd": bucket_ok, "as_of_is_newest_dated_file": newest_ok, "session_roles": roles,
                  "role_ok": LIVE_ROLE in roles, "catalog_bucket": re.sub(r"[0-9]{12}", "<acct>", str(braw)), "bucket_lookup_error": berr,
                  "newest_partition_in_bucket": (ctx.newest_partition(tprefix) if (keys and not berr) else None), "answer_partition_date": (res.get("_partition_date") or res.get("partition_date")) if isinstance(res, dict) else None, "first_source_prefix": (str(keys[0]).rsplit("/", 1)[0] + "/") if keys else None,
                  "catalog_bucket_class": ("opal-data-bd" if bucket_ok else "other") if keys else "none", "partition_date_present": bool((res.get("_partition_date") or res.get("partition_date")) if isinstance(res, dict) else False)}
        ok_all = ok_all and per[t]["rows"] > 0 and bucket_ok and newest_ok and per[t]["role_ok"] and per[t]["enveloped"]
        if t == "client_get_holdings":
            bd_holdings = res
    D["e12_a_per_tool"] = per
    # ---- e12 (b): one unprofiled non-admin call, zero S3 client requests -------------------------------------------------
    guard = Counter()
    saved = []
    for obj, attr in ((internal_role, "s3_client"), (internal_role, "dynamodb_client"), (internal_role, "lambda_client"),
                      (client_role, "client_for"), (client_role, "s3_client"), (client_role, "default_client")):
        if hasattr(obj, attr):
            saved.append((obj, attr, getattr(obj, attr)))
            setattr(obj, attr, guard)
    try:
        r2 = call(opal2, "client_get_holdings", firm=FIRM, account=ref or "****0000|x")
    finally:
        for obj, attr, val in saved:
            setattr(obj, attr, val)
    denied = isinstance(r2, dict) and (r2.get("code") == "entitlement_denied" or "entitlement" in str(r2.get("error", "")).lower())
    D["e12_b"] = {"refused": bool(denied), "s3_client_requests": guard.calls, "code": (r2 or {}).get("code") if isinstance(r2, dict) else None}
    A["e12_bd49f_live"] = bool(ok_all and denied and guard.calls == 0)
    client_role.client_for = orig_cf

    # ---- e4: weight_unit and currency -------------------------------------------------------------------------------------
    def unit_ok(res):
        units = [u for u in walk(res, "weight_unit") if u is not None]
        curr = [c for c in walk(res, "currency") if c]
        return bool(units) and all(u in ("fraction", "percent") for u in units) and bool(curr), sorted({str(u) for u in units})
    ok4, units4 = unit_ok(bd_holdings)
    D["e4_bd_currency"] = {"currency_values": len(walk(bd_holdings, "currency")), "types": sorted({type(x).__name__ for x in walk(bd_holdings, "currency")}),
                           "distinct": sorted({str(x) for x in walk(bd_holdings, "currency") if x})[:6], "basis": sorted({str(x) for x in walk(bd_holdings, "currency_basis")})[:6]}
    D["e4_bd_row_keys"] = sorted({k for x in walk(bd_holdings, "weight_unit") for k in ()} | set())
    D["e4_bd49f"] = {"ok": ok4, "units": units4}
    e4_ok, via = ok4, "blackdiamond"
    if not ok4:
        from app import client_adapter_smartx as sx
        pre2 = ctx.prefix(sx.VENDOR, sx.SEGMENT, sx.LAYER, sx.T_MAP)
        parts = ctx.list_partitions(pre2)
        l4s = None
        for p in reversed(parts[-10:]):
            rr = ctx.read_rows(pre2, p)
            nums = [r.get("account_number") for r in rr if isinstance(r.get("account_number"), str) and len(r.get("account_number")) >= 4]
            if nums:
                l4s = nums[0][-4:]
                break
        if l4s:
            rs = call(master, "client_resolve_account", firm=FIRM, account_last4=l4s)
            sc = [c for c in ((rs or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "smartx"] if isinstance(rs, dict) else []
            if sc:
                rh = call(master, "client_get_holdings", firm=FIRM, account=sc[0].get("account_ref"))
                ok_s, units_s = unit_ok(rh)
                D["e4_smartx"] = {"ok": ok_s, "units": units_s, "currency_values": len(walk(rh, "currency")), "currency_types": sorted({type(x).__name__ for x in walk(rh, "currency")}),
                                  "currency_distinct": sorted({str(x) for x in walk(rh, "currency") if x})[:6], "basis_distinct": sorted({str(x) for x in walk(rh, "currency_basis")})[:6],
                                  "currency_keys_seen": sorted({k for k in (rh.keys() if isinstance(rh, dict) else []) if "curr" in k.lower()}),
                                  "top_keys": sorted(rh)[:14] if isinstance(rh, dict) else None}
                e4_ok, via = ok_s, "smartx"
    A["e4_unit_currency"] = bool(e4_ok)
    D["e4_via"] = via

    # ---- e5: coverage_floor on an empty news window ---------------------------------------------------------------------
    e5 = False
    tried = []
    for day in ("2020-01-02", "2022-06-01", "2024-01-02", "2025-01-02"):
        r5 = call(opal, "news_search_articles", date_from=day, date_to=day, limit=5)
        has = bool(walk(r5, "coverage_floor")) if isinstance(r5, dict) else False
        tried.append({"has_floor": has, "absent_reason": (r5 or {}).get("absent_reason") if isinstance(r5, dict) else None})
        if has:
            e5 = True
            break
    D["e5_tried"] = tried
    A["e5_news_floor"] = e5

    # ---- e6: trading_days_behind_t1 on a chatter answer --------------------------------------------------------------------
    rk = call(opal, "harvest_resolve_security", query="AAPL")
    skeys = [k for k in walk(rk, "security_key") if isinstance(k, str)]
    r6 = call(opal, "harvest_get_chatter", security_key=skeys[0], from_day=(today - dt.timedelta(days=14)).isoformat(), to_day=today.isoformat()) if skeys else {}
    lags = walk(r6, "trading_days_behind_t1")
    D["e6"] = {"resolved_security": bool(skeys), "lag_values_found": len(lags), "all_int": bool(lags) and all(isinstance(x, int) and not isinstance(x, bool) for x in lags)}
    A["e6_chatter_lag"] = bool(D["e6"]["all_int"])

    # ---- e8: Muse inert ----------------------------------------------------------------------------------------------------------
    context.set_current_principal(master)
    after = len(asyncio.run(tools.mcp.list_tools()))
    out["tools_list_after"] = after
    status = None
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/teams/poll", timeout=10) as r:
            status = r.status
    except urllib.error.HTTPError as exc:
        status = exc.code
    except Exception as exc:
        D["teams_poll_error"] = type(exc).__name__
    D["teams_poll_status"] = status
    muse_env = bool((os.environ.get("MUSE_CLIENT_ID") or "").strip())
    out["muse_env_present"] = muse_env
    A["e8_muse_inert"] = bool((not muse_env) and status is not None and status != 404)   # tools_list equality is graded by the builder against tools_list_before

    # ---- e9: a key with no catalog row answers 404 -------------------------------------------------------------------------
    context.set_current_principal(master)
    try:
        r9 = tools.mcp._tool_manager.get_tool("gateway_query_catalog").fn(key="ap28-no-such-catalog-key")
    except Exception as exc:
        r9 = {"error": "%s: %s" % (type(exc).__name__, str(exc)[:110]), "_exc": True}
    D["e9"] = {"http_status": (r9 or {}).get("http_status") if isinstance(r9, dict) else None,
               "top_keys": sorted(r9)[:12] if isinstance(r9, dict) else None, "error": str(r9.get("error", ""))[:110] if isinstance(r9, dict) else None}
    A["e9_not_found_404"] = D["e9"]["http_status"] == 404

    # ---- e10: 130 POSTs through the installed GuardMiddleware as ONE stand-in --------------------------------------------------
    from app import ratelimit as rl
    records = []
    audit._emit = lambda rec: records.append(dict(rec))
    server.enforce = lambda email: None
    stand = context.make_principal(context.MOCK_TENANT_ID, "00000000-0000-0000-0000-00000000c128", "ap28.limit@%s" % dom)
    server._bearer_auth = lambda request: (stand, "ap28-standin-client")
    rl._LOGS.clear()
    rl._REFUSAL_ROWS.clear()

    async def one():
        sent = []

        async def inner(scope, receive, send):
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": b"{}"})

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(m):
            sent.append(m)
        scope = {"type": "http", "method": "POST", "path": "/mcp", "query_string": b"", "headers": [(b"authorization", b"Bearer ap28-standin")]}
        await server.GuardMiddleware(inner)(scope, receive, send)
        return sent[0]["status"]

    t0 = time.monotonic()
    codes = [asyncio.run(one()) for _ in range(130)]
    el = time.monotonic() - t0
    lim = int(getattr(rl._cfg, "RL_MCP_IDENTITY_LIMIT", 0) or 0)
    win = float(getattr(rl._cfg, "RL_MCP_IDENTITY_WINDOW", 0) or 0)
    rows429 = [r for r in records if r.get("event") == "gw_ratelimit"]
    blob = json.dumps(rows429)
    D["e10"] = {"limit": lim, "window_s": win, "elapsed_s": round(el, 2), "first_120_not_429": all(c != 429 for c in codes[:120]),
                "from_121_all_429": all(c == 429 for c in codes[120:]), "n_429": sum(1 for c in codes if c == 429), "rows": len(rows429),
                "by_client_hashed": bool(rows429) and all(re.fullmatch(r"[0-9a-f]{8}|none|other", k) for r in rows429 for k in (r.get("by_client") or {})),
                "no_email_in_row": "@" not in blob, "no_stand_in_client_id_in_row": "ap28-standin-client" not in blob}
    A["e10_429_audited"] = bool(lim == 120 and win == 60.0 and D["e10"]["first_120_not_429"] and D["e10"]["from_121_all_429"] and D["e10"]["rows"] >= 1
                                and D["e10"]["by_client_hashed"] and D["e10"]["no_email_in_row"] and D["e10"]["no_stand_in_client_id_in_row"] and el < 60)
    return out


def runner(outp: str) -> None:
    import boto3
    instance = "i-07dccb1615503ac99"
    bucket = "opal-313476888478-lambda-artifacts"
    key = "ec2/opal-gateway/ap28_arms.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap28_arms.py && aws s3 cp s3://%s/%s /tmp/ap28_arms.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ap28_arms.py --host" % (bucket, key))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=600)["Command"]["CommandId"]
    inv = None
    for _ in range(150):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "AP28_ARMS_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP28_ARMS_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("AP28_ARMS_JSON")
        try:
            print(json.dumps(host(), separators=(",", ":"), default=str))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-1000:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
