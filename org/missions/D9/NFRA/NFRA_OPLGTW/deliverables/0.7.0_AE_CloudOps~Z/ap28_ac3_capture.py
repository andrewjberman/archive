#!/usr/bin/env python
"""OG-ap-28 AC3 evidence (A5, COO msg 35189): six answer bodies WITHOUT scrubbing numbers or security ids, kept OUT of git.
  python ap28_ac3_capture.py <out.json>   -> the RUNNER (repository root): uploads itself to S3, runs once over SSM (Rule 12), writes <out.json> locally
  python ap28_ac3_capture.py --host       -> the HOST program (on i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python)

Six captures through the INSTALLED code as a master_admin stand-in, read-only (audit sink stubbed): the four 49F Black Diamond live tools (one account), one EMPTY-news answer
(coverage_floor), one chatter answer (trading_days_behind_t1). The ONLY masking: an account stays ****<last4> (the vendor account id part of a ref and any account-id field are
withheld), and e-mail addresses, phone numbers and person-name fields are withheld. Numbers, tickers, CUSIPs, security ids and dates are left exactly as served.
The result travels as one compressed base64 block (SSM stdout is capped near 24000 characters). One run; no retry loop."""
from __future__ import annotations

import base64
import io
import json
import os
import re
import sys
import time
import traceback
import zlib

ROOT = "/opt/opal-gateway"
FIRM = "49financial"
WINDOW_DAYS = 360
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<![\w.])(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?![\w])")
ACCT_REF = re.compile(r"\*{4}([A-Za-z0-9]{4})[|.][A-Za-z0-9._\-]+")
ACCT_ID = re.compile(r"\bz0[0-9]\w{4,}\b")
PERSON_KEY = re.compile(r"(advisor|owner|client_name|contact|email|e_mail|phone|rep_name|representative|person|first_name|last_name|full_name|"
                        r"portfolio_name|account_name|registration|holder|beneficiar|nickname|trust_name|household)", re.I)
# a value shaped like a registered name ("Surname, Given & Surname, Given"), whatever its key
NAME_SHAPE = re.compile(r"^[A-Z][A-Za-z'.-]+, [A-Z][A-Za-z'.-]+(?: [A-Z]\.?)?(?: (?:&|and) .+)?$")


def mask(obj, withheld):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(k, str) and PERSON_KEY.search(k) and v not in (None, "", [], {}):
                out[k] = "[withheld]"
                withheld["person_or_contact_fields"] += 1
            elif isinstance(k, str) and k in ("account_id", "bd_account_id", "accountid") and isinstance(v, str):
                out[k] = "[acct]"
                withheld["account_id_fields"] += 1
            else:
                out[k] = mask(v, withheld)
        return out
    if isinstance(obj, list):
        return [mask(x, withheld) for x in obj]
    if isinstance(obj, str):
        if NAME_SHAPE.match(obj.strip()):
            withheld["name_shaped_values"] += 1
            return "[withheld]"
        s, n1 = EMAIL.subn("[email]", obj)
        s, n2 = PHONE.subn("[phone]", s)
        s, n3 = ACCT_REF.subn(lambda m: "****" + m.group(1), s)
        s, n4 = ACCT_ID.subn("[acct]", s)
        withheld["emails"] += n1
        withheld["phones"] += n2
        withheld["account_ref_ids"] += n3
        withheld["bare_account_ids"] += n4
        return s
    return obj


def nrows(res):
    return sum(len(v) for k, v in res.items() if isinstance(v, list) and v and isinstance(v[0], dict) and k != "candidates") if isinstance(res, dict) else 0


def host() -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    import datetime as dt
    from app import audit, client_core as cc, context, identity_scope, tools
    from app import server  # noqa: F401 -- registers the integration tools as the running service does
    from app import client_adapter_bd49f as bd
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    dom = identity_scope.OPAL_USERS_DOMAIN
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ap28.ac3@%s" % dom)
    opal = context.make_principal(context.MOCK_TENANT_ID, "00000000-0000-0000-0000-00000000d128", "ap28.ac3.opal@%s" % dom)
    tools._user_token = lambda: ("ap28.ac3@%s" % dom, "harness-no-token")
    today = dt.datetime.now(dt.timezone.utc).date()
    withheld = {"person_or_contact_fields": 0, "account_id_fields": 0, "emails": 0, "phones": 0, "account_ref_ids": 0, "bare_account_ids": 0, "name_shaped_values": 0}

    def call(who, tool, **kw):
        context.set_current_principal(who)
        try:
            return getattr(tools, tool)(**kw)
        except Exception as exc:
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:120])}

    ctx = cc._new_ctx()
    bd.bind_firms()
    segment = bd._firm(ctx, FIRM)
    pre = ctx.prefix(bd.VENDOR, segment, "silver", "dim_account_xref")
    part = bd._select(ctx, pre, None)
    kept, _x = bd._fence(ctx.read_rows(pre, part, columns=list(bd.DIM_COLUMNS)), "bd_account_id")
    xr = {r.get("bd_account_id"): r.get("bd_account_number") for r in kept}
    cutoff = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    sets = {}
    for tname in ("unrealized", "transactions", "allocations", "fees"):
        lp = bd._live_prefix(ctx, segment, tname)
        lpart = bd._select(ctx, lp, None)
        cols = ["account_id"] + (["trade_date"] if tname in ("transactions", "fees") else []) + (list(bd.FEE_COLUMNS) if tname == "fees" else [])
        rows = ctx.read_rows(lp, lpart, columns=cols) if lpart else []
        if tname in ("transactions", "fees"):
            rows = [r for r in rows if str(r.get("trade_date") or "")[:10] >= cutoff and (tname != "fees" or any(r.get(c) not in (None, 0) for c in bd.FEE_COLUMNS))]
        sets[tname] = {r.get("account_id") for r in rows}
    common = sorted(set.intersection(*sets.values()) & set(xr))
    ref, l4_used = None, "????"
    for pick in common[:60]:
        l4 = bd._last4(xr.get(pick))
        if not l4:
            continue
        l4_used = l4
        res = call(master, "client_resolve_account", firm=FIRM, account_last4=l4)
        for c in [c for c in ((res or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "blackdiamond"]:
            if str(pick) in str(c.get("account_ref") or ""):
                ref = c.get("account_ref")
                break
        if ref:
            break
    caps = []

    def add(name, tool, kw_public, res):
        body = mask(res, withheld)
        caps.append({"capture": name, "tool": tool, "arguments": kw_public, "rows": nrows(res), "body": body})

    if ref:
        shown = "****" + l4_used
        win = {"from_date": (today - dt.timedelta(days=WINDOW_DAYS)).isoformat(), "to_date": today.isoformat()}
        add("49F BD live holdings", "client_get_holdings", {"firm": FIRM, "account": shown}, call(master, "client_get_holdings", firm=FIRM, account=ref))
        add("49F BD live transactions", "client_get_transactions", dict({"firm": FIRM, "account": shown}, **win), call(master, "client_get_transactions", firm=FIRM, account=ref, **win))
        add("49F BD live allocation", "client_get_allocation", {"firm": FIRM, "account": shown}, call(master, "client_get_allocation", firm=FIRM, account=ref))
        add("49F BD live fees", "client_get_fees", dict({"firm": FIRM, "account": shown}, **win), call(master, "client_get_fees", firm=FIRM, account=ref, **win))
    for day in ("2020-01-02", "2022-06-01", "2024-01-02", "2025-01-02"):
        r5 = call(opal, "news_search_articles", date_from=day, date_to=day, limit=5)
        if isinstance(r5, dict) and "coverage_floor" in json.dumps(r5):
            add("EMPTY news window (coverage_floor)", "news_search_articles", {"date_from": day, "date_to": day, "limit": 5}, r5)
            break
    rk = call(opal, "harvest_resolve_security", query="AAPL")
    keys = []

    def find(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "security_key" and isinstance(v, str):
                    keys.append(v)
                find(v)
        elif isinstance(o, list):
            for v in o:
                find(v)
    find(rk)
    if keys:
        kw = {"security_key": keys[0], "from_day": (today - dt.timedelta(days=14)).isoformat(), "to_day": today.isoformat()}
        add("chatter (trading_days_behind_t1)", "harvest_get_chatter", kw, call(opal, "harvest_get_chatter", **kw))
    return {"captured_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "live_release": "bf9d23b518",
            "stand_in": "master_admin stand-in for the 49F tools; an unprofiled Opal stand-in for news and chatter",
            "masking": "an account stays ****<last4>; e-mail, phone, person-name fields and the vendor account id are withheld; nothing else is changed",
            "withheld_counts": withheld, "captures": caps}


def runner(outp: str) -> None:
    import boto3
    instance = "i-07dccb1615503ac99"
    bucket = "opal-313476888478-lambda-artifacts"
    key = "ec2/opal-gateway/ap28_ac3_capture.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap28_ac3_capture.py && aws s3 cp s3://%s/%s /tmp/ap28_ac3_capture.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ap28_ac3_capture.py --host" % (bucket, key))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=600)["Command"]["CommandId"]
    inv = None
    for _ in range(150):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "AC3_B64" not in so:
        raise SystemExit("no marker; status=%s stderr=%s stdout_tail=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:], so[-200:]))
    blob = so.split("AC3_B64", 1)[1].strip().split()[0]
    doc = json.loads(zlib.decompress(base64.b64decode(blob)).decode("utf-8"))
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print("stdout chars %d (cap ~24000); wrote %s" % (len(so), outp))
    for c in doc["captures"]:
        print("  %-38s %-26s rows %d" % (c["capture"], c["tool"], c["rows"]))
    print("  withheld:", doc["withheld_counts"])


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("AC3_B64")
        try:
            print(base64.b64encode(zlib.compress(json.dumps(host(), separators=(",", ":"), default=str).encode("utf-8"), 9)).decode("ascii"))
        except Exception:
            print(base64.b64encode(zlib.compress(json.dumps({"fatal": traceback.format_exc()[-800:]}).encode("utf-8"))).decode("ascii"))
            sys.exit(1)
    else:
        runner(sys.argv[1])
