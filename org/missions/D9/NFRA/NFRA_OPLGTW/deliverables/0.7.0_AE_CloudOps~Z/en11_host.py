#!/usr/bin/env python
"""OG-en-11 host program: which bucket does each of the four 49F Black Diamond client tools read, on the live host?

Runs ON the gateway host under /opt/opal-gateway/.venv/bin/python (uploaded to S3 and pulled, cloud-ops Rule 12). READ-ONLY: the audit sink is stubbed and
nothing is written. It calls the installed registered tools (client_resolve_account, then client_get_holdings, _transactions, _allocation, _fees for ONE
Black Diamond account of firm 49financial) as a master_admin stand-in built in-process from the host's roster key.

Two independent instruments for the bucket, both recorded: (a) the catalog row the context resolves for the answer's FIRST source key (the bucket the code
would read), and (b) the bucket the S3 helpers of typed_scope were actually handed during that call (wrapped, recording only the bucket and key prefix).
The session role is the STS caller identity of the very client the adapter used (the role name only, never a credential). No account number, name or
e-mail address is returned: the account reference is dropped and only its masked form is used inside this process."""
from __future__ import annotations

import json
import os
import re
import sys
import traceback

ROOT = "/opt/opal-gateway"
FIRM = "49financial"
TOOLS = ("client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees")


def role_name(arn) -> str:
    m = re.search(r":(?:assumed-role|role)/([^/]+)", str(arn))
    return m.group(1) if m else "unparsed"


def main() -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    import boto3
    from app import audit, client_core as cc, client_role, context, identity_scope, tools, typed_scope
    from app import client_adapter_bd49f as bd
    from app.config import get_config

    audit.log_call = lambda *a, **k: None
    out = {"firm": FIRM, "tools": []}
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    if not roster:
        out["fatal"] = "no master_admin roster entry"
        return out
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "en11.master@%s" % identity_scope.OPAL_USERS_DOMAIN)
    tools._user_token = lambda: ("en11.master@%s" % identity_scope.OPAL_USERS_DOMAIN, "harness-no-token")
    context.set_current_principal(master)

    seen_buckets = []          # (bucket, key-or-prefix) handed to typed_scope's S3 helpers
    seen_clients = []

    def wrap(name):
        orig = getattr(typed_scope, name)

        def w(scope, *a, **k):
            seen_buckets.append((scope.bucket, str(a[0]) if a else ""))
            return orig(scope, *a, **k)
        setattr(typed_scope, name, w)
    for n in ("list_keys", "newest_part", "read_parquet"):
        wrap(n)
    orig_cf = client_role.client_for

    def cf(key):
        c = orig_cf(key)
        seen_clients.append((key, c))
        return c
    client_role.client_for = cf

    ctx = cc._new_ctx()
    bd.bind_firms()
    segment = bd._firm(ctx, FIRM)
    out["segment_is_firm_keyed"] = bool(segment)

    # one Black Diamond account the resolver returns: derive a last4 from the firm's account xref, as the resolver reads it
    prefix = ctx.prefix(bd.VENDOR, segment, "silver", "dim_account_xref")
    part = bd._select(ctx, prefix, None)
    rows = ctx.read_rows(prefix, part, columns=list(bd.DIM_COLUMNS)) if part else []
    kept, _ex = bd._fence(rows, "bd_account_id")
    l4 = None
    for r in kept:
        cand4 = bd._last4(r.get("bd_account_number"))
        if cand4:
            l4 = cand4
            break
    out["xref_rows"] = len(rows)
    out["last4_derived"] = l4 is not None
    if not l4:
        out["finding_hint"] = "no 49F Black Diamond account could be derived from the xref"
        return out
    res = tools.client_resolve_account(firm=FIRM, account_last4=l4)
    cands = [c for c in ((res or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "blackdiamond"] if isinstance(res, dict) else []
    out["resolver_blackdiamond_candidates"] = len(cands)
    if not cands:
        out["finding_hint"] = "the resolver returned no Black Diamond candidate for firm 49financial"
        return out
    ref = cands[0].get("account_ref")
    sts_default = boto3.client("sts")
    out["instance_role"] = role_name(sts_default.get_caller_identity().get("Arn"))

    for tname in TOOLS:
        del seen_buckets[:]
        del seen_clients[:]
        entry = {"tool": tname}
        try:
            kw = {"firm": FIRM, "account": ref}
            if tname in ("client_get_transactions", "client_get_fees"):
                # the first run omitted the window these two tools require (absent_reason window_required); a 30-day window supplies it
                import datetime as _dt
                _today = _dt.datetime.now(_dt.timezone.utc).date()
                kw.update({"from_date": (_today - _dt.timedelta(days=30)).isoformat(), "to_date": _today.isoformat()})
            res = getattr(tools, tname)(**kw)
        except Exception as exc:
            entry["error"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
            out["tools"].append(entry)
            continue
        if not isinstance(res, dict):
            entry["error"] = "non-dict answer"
            out["tools"].append(entry)
            continue
        keys = res.get("_source_keys") or res.get("source_keys") or []
        entry["source_keys_n"] = len(keys)
        entry["code"] = res.get("code")
        entry["absent_reason"] = res.get("absent_reason") or res.get("_absent_reason")
        entry["partition_date"] = res.get("_partition_date") or res.get("partition_date")
        entry["as_of"] = res.get("_as_of") or res.get("as_of")
        entry["rows"] = sum(len(v) for k, v in res.items() if isinstance(v, list) and v and isinstance(v[0], dict) and k != "candidates")
        if keys:
            first = str(keys[0])
            tprefix = first.rsplit("/", 1)[0] + "/"
            entry["source_prefix"] = tprefix
            try:
                entry["catalog_bucket"] = ctx._row(tprefix)["bucket"]
            except Exception as exc:
                entry["catalog_bucket"] = None
                entry["catalog_error"] = type(exc).__name__
            entry["observed_buckets"] = sorted({b for b, k in seen_buckets if k.startswith(tprefix)})
        entry["observed_buckets_all"] = sorted({b for b, _k in seen_buckets})
        roles = set()
        for key, c in seen_clients:
            try:
                creds = c._get_credentials().get_frozen_credentials()
                sts_a = boto3.client("sts", aws_access_key_id=creds.access_key, aws_secret_access_key=creds.secret_key, aws_session_token=creds.token)
                roles.add(role_name(sts_a.get_caller_identity().get("Arn")))
            except Exception as exc:
                roles.add("unread:" + type(exc).__name__)
        entry["session_roles"] = sorted(roles)
        entry["client_keys"] = sorted({k for k, _c in seen_clients})
        out["tools"].append(entry)
    return out


if __name__ == "__main__":
    print("EN11_JSON")
    try:
        print(json.dumps(main(), separators=(",", ":"), default=str))
    except Exception:
        print(json.dumps({"fatal": traceback.format_exc()[-1200:]}))
        sys.exit(1)
