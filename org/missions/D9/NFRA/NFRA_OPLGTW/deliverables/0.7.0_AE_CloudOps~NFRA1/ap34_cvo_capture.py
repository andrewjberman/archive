#!/usr/bin/env python
"""OG-ap-34 Phase C (Amendment A1, COO msg 35396): for the CVO's AC3 judgment, the BODIES of one page chain, WITHOUT scrubbing numbers or security ids, kept OUT of git.
  python ap34_cvo_capture.py <out.json>   -> the RUNNER (run from the repository root): uploads itself to S3, runs once over SSM (Rule 12), writes <out.json> locally
  python ap34_cvo_capture.py --host       -> the HOST program (on i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python), a NEW process through the INSTALLED code

For the one test account, 13-month window, ONE call at a time, the transactions chain and the fees chain are each walked to the null cursor; the bodies of the FIRST TWO pages and the
LAST page of each chain are kept (the masked body as served; the other pages are counted and dropped). The ONLY masking is the one of ap31_ac3_capture.py: an account stays ****<last4>
(the vendor account id part of a ref and any account-id field are withheld), and e-mail addresses, phone numbers and person-name fields are withheld. Numbers, tickers, CUSIPs,
security ids and dates are left exactly as served. The chain stops at 80 percent host memory. Audit sink stubbed; nothing is written to any bucket or table. One run; no retry loop.
The result travels as one compressed base64 block (SSM stdout is capped near 24000 characters); a cut block fails loudly at the decode."""
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
WINDOW_DAYS = 395
MAX_PAGES = 25
STOP_PCT = 80.0
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<![\w.])(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?![\w])")
ACCT_REF = re.compile(r"\*{4}([A-Za-z0-9]{4})[|.][A-Za-z0-9._\-]+")
ACCT_ID = re.compile(r"\bz0[0-9]\w{4,}\b")
PERSON_KEY = re.compile(r"(advisor|owner|client_name|contact|email|e_mail|phone|rep_name|representative|person|first_name|last_name|full_name|"
                        r"portfolio_name|account_name|registration|holder|beneficiar|nickname|trust_name|household)", re.I)
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


def mem_used_pct():
    d = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        d[k] = int(v.split()[0])
    return 100.0 * (1.0 - d["MemAvailable"] / d["MemTotal"])


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
    master = context.make_principal(tid, oid, "ap34.ac3@%s" % dom)
    tools._user_token = lambda: ("ap34.ac3@%s" % dom, "harness-no-token")
    today = dt.datetime.now(dt.timezone.utc).date()
    withheld = {"person_or_contact_fields": 0, "account_id_fields": 0, "emails": 0, "phones": 0, "account_ref_ids": 0, "bare_account_ids": 0, "name_shaped_values": 0}

    def call(tool, **kw):
        context.set_current_principal(master)
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
    for tname in ("transactions", "fees"):
        lp = bd._live_prefix(ctx, segment, tname)
        lpart = bd._select(ctx, lp, None)
        cols = ["account_id", "trade_date"] + (list(bd.FEE_COLUMNS) if tname == "fees" else [])
        rows = ctx.read_rows(lp, lpart, columns=cols) if lpart else []
        rows = [r for r in rows if str(r.get("trade_date") or "")[:10] >= cutoff and (tname != "fees" or any(r.get(c) not in (None, 0) for c in bd.FEE_COLUMNS))]
        sets[tname] = {r.get("account_id") for r in rows}
    common = sorted(set.intersection(*sets.values()) & set(xr))
    ref, l4_used = None, "????"
    for pick in common[:60]:
        l4 = bd._last4(xr.get(pick))
        if not l4:
            continue
        l4_used = l4
        res = call("client_resolve_account", firm=FIRM, account_last4=l4)
        for c in [c for c in ((res or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "blackdiamond"]:
            if str(pick) in str(c.get("account_ref") or ""):
                ref = c.get("account_ref")
                break
        if ref:
            break
    out = {"captured_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "live_release": "9d5b712557",
           "stand_in": "master_admin stand-in through the installed code in a new process (audit sink stubbed)",
           "masking": "an account stays ****<last4>; e-mail, phone, person-name fields and the vendor account id are withheld; nothing else is changed",
           "kept_pages": "the first two pages and the last page of each chain; the other pages are counted and dropped", "chains": {}, "withheld_counts": withheld,
           "ref_resolved": ref is not None, "stopped_on_memory": False}
    if not ref:
        return out
    shown = "****" + l4_used
    frm = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    for tool in ("client_get_transactions", "client_get_fees"):
        cur, pages, kept_pages, total_rows, last = today.isoformat(), 0, [], 0, None
        ended = False
        for n in range(1, MAX_PAGES + 1):
            if mem_used_pct() > STOP_PCT:
                out["stopped_on_memory"] = True
                break
            res = call(tool, firm=FIRM, account=ref, from_date=frm, to_date=cur)
            pages += 1
            total_rows += nrows(res)
            last = res
            if n <= 2:
                kept_pages.append({"page": n, "arguments": {"firm": FIRM, "account": shown, "from_date": frm, "to_date": cur}, "rows": nrows(res), "body": mask(res, withheld)})
            nxt = res.get("next_cursor") if isinstance(res, dict) else None
            if not isinstance(res, dict) or res.get("error") or nxt is None:
                ended = isinstance(res, dict) and not res.get("error") and nxt is None
                break
            cur = nxt
            del res
        if pages > 2 and last is not None:
            kept_pages.append({"page": pages, "arguments": {"firm": FIRM, "account": shown, "from_date": frm, "to_date": cur}, "rows": nrows(last), "body": mask(last, withheld)})
        out["chains"][tool] = {"pages": pages, "rows_total": total_rows, "ended_with_null_cursor": ended, "kept": kept_pages}
        if out["stopped_on_memory"]:
            break
    return out


def runner(outp: str) -> None:
    import boto3
    instance = "i-07dccb1615503ac99"
    bucket = "opal-313476888478-lambda-artifacts"
    key = "ec2/opal-gateway/ap34_cvo_capture.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap34_cvo_capture.py && aws s3 cp s3://%s/%s /tmp/ap34_cvo_capture.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ap34_cvo_capture.py --host; rm -f /tmp/ap34_cvo_capture.py" % (bucket, key))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=1800)["Command"]["CommandId"]
    inv = None
    for _ in range(420):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "AC3_B64" not in so:
        raise SystemExit("no marker; status=%s stderr=%s stdout_chars=%d" % (inv["Status"], inv.get("StandardErrorContent", "")[-200:], len(so)))
    blob = so.split("AC3_B64", 1)[1].strip().split()[0]
    doc = json.loads(zlib.decompress(base64.b64decode(blob)).decode("utf-8"))
    io.open(outp, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(doc, indent=1) + chr(10))
    print("stdout chars %d (cap ~24000); wrote the capture" % len(so))
    for t, c in doc.get("chains", {}).items():
        print("  %-26s pages %d rows_total %d null_cursor %s kept %d" % (t, c["pages"], c["rows_total"], c["ended_with_null_cursor"], len(c["kept"])))
    print("  withheld:", doc["withheld_counts"], "stopped_on_memory", doc["stopped_on_memory"], "ref_resolved", doc["ref_resolved"])


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
