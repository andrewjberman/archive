#!/usr/bin/env python
"""OG-ap-31 Phase B step 5: the round-39 ARMS e1 to e4 through the INSTALLED code on the gateway host (e6 is the issuer's discover_buckets_host.sh, run separately).
One file, two roles:
  python ap31_arms.py <out.json>   -> the RUNNER (repository root): uploads itself to S3, runs once over SSM (Rule 12), writes the record
  python ap31_arms.py --host       -> the HOST program (on i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python)

READ-ONLY. The audit sink is stubbed; no table or bucket is written. Counts and booleans only: no object content, account number, person's name or credential is printed.
Arms:
  e1  a master_admin stand-in asks client_get_transactions and client_get_fees for a 13-month window: partitions_read >= 2, partitions_in_window reported,
      window_partial False when partitions_in_window <= 60 else True with partitions_read 60
  e2  the allocation answer's rows carry weight_unit null with weight_unit_basis not_established; the transactions and fees answers carry currency null with
      currency_basis source_absent
  e3  the serialized holdings, allocation, transactions and fees answers: no figure as a string, no exponent in any number token, at most 6 decimals on weights and 2 on money,
      and as_of equals partition_date (the caller gave none)
  e4  data_entitlement.email_denial: the owner email with route_class internal_page and a stand-in store HOLDING a deny record -> None; alyssa against the LIVE table
      with internal_page -> 403; the owner's stand-in deny with route_class None -> 403 (no existing caller changed)"""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import re
import sys
import traceback

ROOT = "/opt/opal-gateway"
FIRM = "49financial"
OWNER = "andrew@opalinvest.com"
NON_ADMIN = "alyssa@opalinvest.com"
WINDOW_DAYS = 395          # 13 months
CAP = 60
MONEY_KEYS = {"market_value", "market_value_total", "amount", "account_market_value", "cash_market_value", "total_in_window"}
WEIGHT_KEY = re.compile(r"(^weight$|allocation$)")
IDENT_KEY = re.compile(r"(id|last4|number|ref|cusip|isin|sedol|ticker|symbol|code|zip|date|period|key|name|basis|vendor|firm|label|currency|type|class|status)", re.I)
NUMBER_STRING = re.compile(r"^\s*[-+]?(\d{1,3}(,\d{3})+|\d+)(\.\d+)?([eE][-+]?\d+)?%?\s*$")


def walk_items(obj, path=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield path + (k,), v
            yield from walk_items(v, path + (k,))
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_items(v, path)


def values_of(obj, key):
    return [v for p, v in walk_items(obj) if p and p[-1] == key]


def decimals(x):
    s = repr(float(x))
    if "e" in s.lower():
        return 99
    return len(s.split(".")[1].rstrip("0")) if "." in s else 0


def number_hygiene(ans):
    """strings that read as a figure under a figure-ish key, floats with an exponent, weight/money decimals over the bound. Names and counts only."""
    string_figures, exponents, weight_over, money_over, floats = [], 0, 0, 0, 0
    for p, v in walk_items(ans):
        key = p[-1] if p else ""
        if isinstance(v, str) and NUMBER_STRING.match(v) and not IDENT_KEY.search(str(key)):
            string_figures.append(str(key))
        if isinstance(v, float):
            floats += 1
            if "e" in repr(v).lower():
                exponents += 1
            if key in MONEY_KEYS and decimals(v) > 2:
                money_over += 1
            if WEIGHT_KEY.search(str(key)) and decimals(v) > 6:
                weight_over += 1
    blob = json.dumps(ans, default=str)
    outside_strings = re.sub(r'"(?:[^"\\]|\\.)*"', '""', blob)      # JSON string literals removed: a number TOKEN is what is left
    exp_tokens = len(re.findall(r"(?<![A-Za-z_])[-+]?\d+(?:\.\d+)?[eE][-+]?\d+", outside_strings))
    return {"string_figures": len(string_figures), "string_figure_keys": sorted(set(string_figures))[:6], "float_values": floats, "float_exponents": exponents,
            "exponent_tokens_in_text": exp_tokens, "weight_over_6": weight_over, "money_over_2": money_over}


def host() -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    out = {"arms": {}, "detail": {}}
    A, D = out["arms"], out["detail"]
    with open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)
    out["muse_env_present"] = "MUSE_CLIENT_ID" in os.environ
    import urllib.error
    import urllib.request
    from app import audit, client_core as cc, context, identity_scope, tools
    from app import data_entitlement as de
    from app import client_adapter_bd49f as bd
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    dom = identity_scope.OPAL_USERS_DOMAIN
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    if not roster:
        out["fatal"] = "no master_admin roster entry"
        return out
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ap31.master@%s" % dom)
    tools._user_token = lambda: ("ap31.master@%s" % dom, "harness-no-token")
    today = dt.datetime.now(dt.timezone.utc).date()

    def call(tool, **kw):
        context.set_current_principal(master)
        try:
            return getattr(tools, tool)(**kw)
        except Exception as exc:
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:120]), "_exc": True}

    # ---- an account the resolver returns that the four LIVE tables all hold (the OG-ap-28 method) -------------------------
    ctx = cc._new_ctx()
    bd.bind_firms()
    segment = bd._firm(ctx, FIRM)
    pre = ctx.prefix(bd.VENDOR, segment, "silver", "dim_account_xref")
    part = bd._select(ctx, pre, None)
    rows = ctx.read_rows(pre, part, columns=list(bd.DIM_COLUMNS)) if part else []
    kept, _x = bd._fence(rows, "bd_account_id")
    xr = {r.get("bd_account_id"): r.get("bd_account_number") for r in kept}
    sets = {}
    for tname in ("unrealized", "transactions", "allocations", "fees"):
        lp = bd._live_prefix(ctx, segment, tname)
        lpart = bd._select(ctx, lp, None)
        if tname in ("transactions", "fees"):
            cutoff = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
            cols = ["account_id", "trade_date"] + (list(bd.FEE_COLUMNS) if tname == "fees" else [])
            sets[tname] = {r.get("account_id") for r in ctx.read_rows(lp, lpart, columns=cols)
                           if str(r.get("trade_date") or "")[:10] >= cutoff and (tname != "fees" or any(r.get(c) not in (None, 0) for c in bd.FEE_COLUMNS))} if lpart else set()
        else:
            sets[tname] = {r.get("account_id") for r in ctx.read_rows(lp, lpart, columns=["account_id"])} if lpart else set()
    common = sorted(set.intersection(*sets.values()) & set(xr)) if all(sets.values()) else []
    D["accounts_in_all_four_live_tables"] = len(common)
    ref, tried = None, 0
    for pick in common[:60]:
        l4 = bd._last4(xr.get(pick))
        if not l4:
            continue
        tried += 1
        res = call("client_resolve_account", firm=FIRM, account_last4=l4)
        cands = [c for c in ((res or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "blackdiamond"] if isinstance(res, dict) else []
        for c in cands:
            if str(pick) in str(c.get("account_ref") or ""):
                ref = c.get("account_ref")
                break
        if ref:
            break
    D["resolver_tries"] = tried
    D["ref_resolved"] = ref is not None
    if not ref:
        out["fatal"] = "no account ref resolved"
        return out

    frm, to = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat(), today.isoformat()
    ans = {
        "holdings": call("client_get_holdings", firm=FIRM, account=ref),
        "allocation": call("client_get_allocation", firm=FIRM, account=ref),
        "transactions": call("client_get_transactions", firm=FIRM, account=ref, from_date=frm, to_date=to),
        "fees": call("client_get_fees", firm=FIRM, account=ref, from_date=frm, to_date=to),
    }
    D["answers"] = {k: {"is_dict": isinstance(v, dict), "error": (str(v.get("error", ""))[:100] if isinstance(v, dict) else None),
                        "top_keys": sorted(v)[:24] if isinstance(v, dict) else None} for k, v in ans.items()}

    # ---- e1 ---------------------------------------------------------------------------------------------------------------
    e1, e1_ok = {}, True
    for t in ("transactions", "fees"):
        a = ans[t] if isinstance(ans[t], dict) else {}
        inw, rd, partial = a.get("partitions_in_window"), a.get("partitions_read"), a.get("window_partial")
        rule = (isinstance(inw, int) and isinstance(rd, int) and rd >= 2 and
                ((inw <= CAP and partial is False and rd == inw) or (inw > CAP and partial is True and rd == CAP)))
        e1[t] = {"partitions_in_window": inw, "partitions_read": rd, "window_partial": partial, "window_days": WINDOW_DAYS, "cap": CAP, "rule_met": bool(rule),
                 "dates_listed": len(a.get("partitions_read_dates") or []), "exact_duplicates_removed": a.get("exact_duplicates_removed")}
        e1_ok = e1_ok and bool(rule)
    D["e1"] = e1
    A["e1_window_spans_partitions"] = bool(e1_ok)

    # ---- e2 ---------------------------------------------------------------------------------------------------------------
    al, tx, fe = ans["allocation"], ans["transactions"], ans["fees"]
    wu, wb = values_of(al, "weight_unit"), values_of(al, "weight_unit_basis")
    e2 = {"allocation_weight_unit_values": len(wu), "allocation_weight_unit_non_null": sum(1 for x in wu if x is not None),
          "allocation_weight_unit_basis": sorted({str(x) for x in wb})}
    cur_ok = True
    for name, a in (("transactions", tx), ("fees", fe)):
        cv, cb = values_of(a, "currency"), values_of(a, "currency_basis")
        e2[name + "_currency_values"] = len(cv)
        e2[name + "_currency_non_null"] = sum(1 for x in cv if x is not None)
        e2[name + "_currency_basis"] = sorted({str(x) for x in cb})
        cur_ok = cur_ok and len(cv) >= 1 and all(x is None for x in cv) and bool(cb) and all(x == "source_absent" for x in cb)
    unit_ok = len(wu) >= 1 and all(x is None for x in wu) and bool(wb) and all(x == "not_established" for x in wb)
    D["e2"] = e2
    A["e2_allocation_unit_and_currency"] = bool(unit_ok and cur_ok)

    # ---- e3 ---------------------------------------------------------------------------------------------------------------
    e3, e3_ok = {}, True
    for name in ("holdings", "allocation", "transactions", "fees"):
        a = ans[name] if isinstance(ans[name], dict) else {}
        h = number_hygiene(a)
        as_of, pdate = a.get("as_of"), a.get("partition_date") if a.get("partition_date") is not None else a.get("_partition_date")
        h["as_of_present"] = as_of is not None
        h["partition_date_present"] = pdate is not None
        h["as_of_equals_partition_date"] = bool(as_of is not None and pdate is not None and str(as_of)[:10] == str(pdate)[:10])
        e3[name] = h
        e3_ok = e3_ok and h["string_figures"] == 0 and h["float_exponents"] == 0 and h["exponent_tokens_in_text"] == 0 and h["weight_over_6"] == 0 and h["money_over_2"] == 0 and h["as_of_equals_partition_date"]
    D["e3"] = e3
    A["e3_numbers_and_as_of"] = bool(e3_ok)

    # ---- e4 ---------------------------------------------------------------------------------------------------------------
    class StandIn:
        """A store that HOLDS a deny record for any key and writes nothing."""
        def __init__(self):
            self.gets = 0

        def get(self, key):
            self.gets += 1
            return {"status": "active"}

    si = StandIn()
    r_owner_internal = de.email_denial(OWNER, store=si, route_class="internal_page")
    gets_after_exempt = si.gets
    r_owner_none = de.email_denial(OWNER, store=si, route_class=None)
    r_owner_consent = de.email_denial(OWNER, store=si, route_class="consent")
    try:
        r_alyssa = de.email_denial(NON_ADMIN, route_class="internal_page")
        r_alyssa_none = de.email_denial(NON_ADMIN)
    except Exception as exc:
        r_alyssa = r_alyssa_none = "RAISED:" + type(exc).__name__
    D["e4"] = {"owner_internal_page_standin_deny": r_owner_internal, "store_reads_on_the_exempt_call": gets_after_exempt, "owner_route_class_none_standin_deny": r_owner_none,
               "owner_consent_class_standin_deny": r_owner_consent, "non_admin_internal_page_live_table": r_alyssa, "non_admin_no_class_live_table": r_alyssa_none,
               "master_admin_email_roster_entries": len(getattr(get_config(), "MASTER_ADMIN_EMAILS", ()) or ())}
    A["e4_owner_browser_guard"] = bool(r_owner_internal is None and gets_after_exempt == 0 and r_owner_none == 403 and r_owner_consent == 403 and r_alyssa == 403 and r_alyssa_none == 403)

    # ---- the existing routes to NO identity (a trigger): status codes only ------------------------------------------------
    codes = {}
    for pth in ("/", "/gateway", "/api/admin/people", "/api/admin/gitstate"):
        try:
            with urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8080" + pth, method="GET"), timeout=10) as r:
                codes[pth] = r.status
        except urllib.error.HTTPError as exc:
            codes[pth] = exc.code
        except Exception as exc:
            codes[pth] = "ERR:" + type(exc).__name__
    D["no_identity_route_status"] = codes
    return out


def runner(outp: str) -> None:
    import boto3
    import time
    instance = "i-07dccb1615503ac99"
    bucket = "opal-313476888478-lambda-artifacts"
    key = "ec2/opal-gateway/ap31_arms.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap31_arms.py && aws s3 cp s3://%s/%s /tmp/ap31_arms.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ap31_arms.py --host" % (bucket, key))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=600)["Command"]["CommandId"]
    inv = None
    for _ in range(150):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    raw = outp + ".raw.txt"
    io.open(raw, "w", encoding="utf-8", newline="\n").write("status=%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n" % (inv["Status"], so, inv.get("StandardErrorContent", "")[-600:]))
    if "AP31_ARMS_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP31_ARMS_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("AP31_ARMS_JSON")
        try:
            print(json.dumps(host(), separators=(",", ":"), default=str))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-1000:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
