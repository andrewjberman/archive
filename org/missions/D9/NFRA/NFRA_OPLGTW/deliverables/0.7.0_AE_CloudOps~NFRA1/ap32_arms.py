#!/usr/bin/env python
"""OG-ap-32 Phase B step 5: the paging arms through the INSTALLED code on the gateway host. One file, two roles:
  python ap32_arms.py <out.json>   -> the RUNNER (repository root): uploads itself to S3, runs once over SSM (Rule 12), writes the record
  python ap32_arms.py --host       -> the HOST program (on i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python), a new process
READ-ONLY. The audit sink is stubbed; nothing is written to any bucket or table. Counts, seconds, percentages and booleans only; no row content, account number
or person's name is printed (the account stays out of the record altogether).
The page chain runs strictly ONE call at a time (COO C6). Host memory is sampled every 0.25 s; the chain stops at 80 percent.
Arms:
  e1_cursor_first_page             client_get_transactions and client_get_fees for a 13-month window: partitions_read 30, window_partial true, a non-null next_cursor, wall seconds
                                   recorded (graded at 45 s, order Amendment A3 and CTO CT1; over 55 s is a trigger)
  e1_cursor_pages_to_window_start  following next_cursor as to_date until it is null reads every dated partition of the window exactly once; pages, partitions, rows, longest page
  e1_newest_first                  within each page the row dates are non-increasing, and each next page's newest date is not later than the previous page's oldest; no row repeats across pages
  e7_catalog_on_host               the installed app/refs/DATA_CATALOG.yaml md5 equals bdfee515ec348f0ea2ee716eff5acba5"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import sys
import threading
import time
import traceback

ROOT = "/opt/opal-gateway"
FIRM = "49financial"
WINDOW_DAYS = 395
STOP_PCT = 80.0
FIRST_PAGE_BOUND_S = 45.0
FIRST_PAGE_TRIGGER_S = 55.0
MAX_PAGES = 25
CATALOG_MD5 = "bdfee515ec348f0ea2ee716eff5acba5"
DATE_KEYS = ("trade_date", "date", "day", "as_of_date")


def mem_used_pct():
    d = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        d[k] = int(v.split()[0])
    return 100.0 * (1.0 - d["MemAvailable"] / d["MemTotal"])


class Sampler(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.peak = 0.0
        self.stop_flag = threading.Event()

    def run(self):
        while not self.stop_flag.is_set():
            self.peak = max(self.peak, mem_used_pct())
            time.sleep(0.25)


def rows_of(ans):
    best = []
    for k, v in ans.items():
        if isinstance(v, list) and v and isinstance(v[0], dict) and k != "candidates" and len(v) > len(best):
            best = v
    return best


def day_of(row):
    for k in DATE_KEYS:
        if row.get(k):
            return str(row[k])[:10]
    return None


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
    from app import audit, client_core as cc, context, identity_scope, tools
    from app import client_adapter_bd49f as bd
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    D["adapter_page_partitions"] = getattr(bd, "PAGE_PARTITIONS", None)
    D["adapter_read_workers"] = getattr(bd, "READ_WORKERS", None)
    D["adapter_gate_wait_seconds"] = getattr(bd, "WINDOW_GATE_WAIT_SECONDS", None)
    dom = identity_scope.OPAL_USERS_DOMAIN
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ap32.master@%s" % dom)
    tools._user_token = lambda: ("ap32.master@%s" % dom, "harness-no-token")
    today = dt.datetime.now(dt.timezone.utc).date()
    D["host_mem_used_pct_before"] = round(mem_used_pct(), 1)

    def call(tool, **kw):
        context.set_current_principal(master)
        try:
            return getattr(tools, tool)(**kw)
        except Exception as exc:
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:120]), "_exc": True}

    # ---- an account the resolver returns that the live tables hold (the OG-ap-28 method) ----------------------------------
    ctx = cc._new_ctx()
    bd.bind_firms()
    segment = bd._firm(ctx, FIRM)
    pre = ctx.prefix(bd.VENDOR, segment, "silver", "dim_account_xref")
    part = bd._select(ctx, pre, None)
    rows = ctx.read_rows(pre, part, columns=list(bd.DIM_COLUMNS)) if part else []
    kept, _x = bd._fence(rows, "bd_account_id")
    xr = {r.get("bd_account_id"): r.get("bd_account_number") for r in kept}
    sets = {}
    for tname in ("transactions", "fees"):
        lp = bd._live_prefix(ctx, segment, tname)
        lpart = bd._select(ctx, lp, None)
        cutoff = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
        cols = ["account_id", "trade_date"] + (list(bd.FEE_COLUMNS) if tname == "fees" else [])
        sets[tname] = {r.get("account_id") for r in ctx.read_rows(lp, lpart, columns=cols)
                       if str(r.get("trade_date") or "")[:10] >= cutoff and (tname != "fees" or any(r.get(c) not in (None, 0) for c in bd.FEE_COLUMNS))} if lpart else set()
    common = sorted(set.intersection(*sets.values()) & set(xr)) if all(sets.values()) else []
    ref = None
    for pick in common[:60]:
        l4 = bd._last4(xr.get(pick))
        if not l4:
            continue
        res = call("client_resolve_account", firm=FIRM, account_last4=l4)
        for c in [c for c in ((res or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "blackdiamond"]:
            if str(pick) in str(c.get("account_ref") or ""):
                ref = c.get("account_ref")
                break
        if ref:
            break
    D["ref_resolved"] = ref is not None
    if not ref:
        out["fatal"] = "no account ref resolved"
        return out
    del sets, common, xr, kept, rows

    # ---- the page chains, ONE call at a time ----------------------------------------------------------------------------------
    frm = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    sampler = Sampler()
    sampler.start()
    chains = {}
    stopped_on_memory = False
    for tool in ("client_get_transactions", "client_get_fees"):
        pages, seen_hashes, repeats, read_dates, cur = [], set(), 0, [], today.isoformat()
        total_in_window, ended_clean, stop_reason = None, False, None
        for n in range(1, MAX_PAGES + 1):
            if sampler.peak > STOP_PCT:
                stopped_on_memory = True
                stop_reason = "memory above %s percent" % STOP_PCT
                break
            sampler.peak = max(sampler.peak, mem_used_pct())
            t0 = time.monotonic()
            ans = call(tool, firm=FIRM, account=ref, from_date=frm, to_date=cur)
            wall = time.monotonic() - t0
            a = ans if isinstance(ans, dict) else {}
            reason = a.get("absent_reason") or a.get("_absent_reason")
            if a.get("error") or reason:
                stop_reason = "page %d answered %s" % (n, reason or "an error")
                pages.append({"n": n, "wall_seconds": round(wall, 2), "absent_or_error": str(reason or a.get("error"))[:60]})
                break
            rws = rows_of(a)
            days = [d for d in (day_of(r) for r in rws) if d]
            for r in rws:
                h = hashlib.sha1(json.dumps(r, sort_keys=True, default=str).encode("utf-8")).hexdigest()
                if h in seen_hashes:
                    repeats += 1
                seen_hashes.add(h)
            rd = [str(x)[:10] for x in (a.get("partitions_read_dates") or [])]
            read_dates += rd
            if total_in_window is None:
                total_in_window = a.get("partitions_in_window")
            pages.append({"n": n, "wall_seconds": round(wall, 2), "partitions_in_window": a.get("partitions_in_window"), "partitions_read": a.get("partitions_read"),
                          "window_partial": a.get("window_partial"), "next_cursor_non_null": a.get("next_cursor") is not None, "rows": len(rws),
                          "row_days_non_increasing": all(days[i] >= days[i + 1] for i in range(len(days) - 1)),
                          "newest_row_day": days[0] if days else None, "oldest_row_day": days[-1] if days else None,
                          "exact_duplicates_removed": a.get("exact_duplicates_removed"), "host_mem_used_pct_after": round(mem_used_pct(), 1)})
            if a.get("next_cursor") is None:
                ended_clean = True
                break
            cur = a["next_cursor"]
        order_ok, within_ok = True, True
        for i, p in enumerate(pages):
            within_ok = within_ok and p.get("row_days_non_increasing", False)
            if i > 0 and p.get("newest_row_day") and pages[i - 1].get("oldest_row_day"):
                order_ok = order_ok and p["newest_row_day"] <= pages[i - 1]["oldest_row_day"]
        total_read = sum(p.get("partitions_read") or 0 for p in pages)
        first = pages[0] if pages else {}
        chains[tool] = {"pages": len(pages), "total_in_window_first_page": total_in_window, "partitions_read_total": total_read, "distinct_partition_dates_read": len(set(read_dates)),
                        "partition_dates_repeated": len(read_dates) - len(set(read_dates)), "rows_total": sum(p.get("rows") or 0 for p in pages),
                        "row_repeats_across_pages": repeats, "longest_page_wall_seconds": max([p.get("wall_seconds") or 0 for p in pages] or [0]),
                        "chain_ended_with_null_cursor": ended_clean, "stop_reason": stop_reason, "within_page_non_increasing": within_ok, "page_order_ok": order_ok,
                        "first_page": {k: first.get(k) for k in ("wall_seconds", "partitions_in_window", "partitions_read", "window_partial", "next_cursor_non_null", "rows")},
                        "per_page": pages}
        if stopped_on_memory:
            break
    sampler.stop_flag.set()
    D["chains"] = chains
    D["host_mem_used_pct"] = {"before": D["host_mem_used_pct_before"], "peak_during_chains": round(sampler.peak, 1), "after": round(mem_used_pct(), 1)}
    D["stopped_on_memory"] = stopped_on_memory

    fp_ok = bool(chains) and all(
        c["first_page"].get("partitions_read") == 30 and c["first_page"].get("window_partial") is True and c["first_page"].get("next_cursor_non_null") is True
        and (c["first_page"].get("wall_seconds") or 999) <= FIRST_PAGE_BOUND_S for c in chains.values()) and len(chains) == 2
    D["first_page_over_trigger_seconds"] = any((c["first_page"].get("wall_seconds") or 0) > FIRST_PAGE_TRIGGER_S for c in chains.values())
    chain_ok = len(chains) == 2 and all(
        c["chain_ended_with_null_cursor"] and c["partition_dates_repeated"] == 0 and c["total_in_window_first_page"] == c["partitions_read_total"]
        == c["distinct_partition_dates_read"] for c in chains.values())
    nf_ok = len(chains) == 2 and all(c["within_page_non_increasing"] and c["page_order_ok"] and c["row_repeats_across_pages"] == 0 for c in chains.values())
    A["e1_cursor_first_page"] = bool(fp_ok)
    A["e1_cursor_pages_to_window_start"] = bool(chain_ok)
    A["e1_newest_first"] = bool(nf_ok)
    cat = hashlib.md5(open(os.path.join(ROOT, "app", "refs", "DATA_CATALOG.yaml"), "rb").read()).hexdigest()
    D["catalog_md5_equals_expected"] = cat == CATALOG_MD5
    A["e7_catalog_on_host"] = cat == CATALOG_MD5
    return out


def runner(outp: str) -> None:
    import boto3
    instance, bucket, key = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts", "ec2/opal-gateway/ap32_arms.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap32_arms.py && aws s3 cp s3://%s/%s /tmp/ap32_arms.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ap32_arms.py --host" % (bucket, key))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=1500)["Command"]["CommandId"]
    inv = None
    for _ in range(330):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    io.open(outp + ".raw.txt", "w", encoding="utf-8", newline="\n").write("status=%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n" % (inv["Status"], so, inv.get("StandardErrorContent", "")[-600:]))
    if "AP32_ARMS_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP32_ARMS_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({k: v for k, v in doc.items() if k != "detail"}, indent=1))
    for t, c in (doc.get("detail", {}).get("chains") or {}).items():
        print(t, {k: v for k, v in c.items() if k != "per_page"})
    print("memory", doc.get("detail", {}).get("host_mem_used_pct"))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("AP32_ARMS_JSON")
        try:
            print(json.dumps(host(), separators=(",", ":"), default=str))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-1000:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
