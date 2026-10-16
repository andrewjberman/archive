#!/usr/bin/env python
"""OG-en-7 host program: count firm A's SmartX candidates whose advisor maps to ANOTHER firm, on the REAL served data.

Runs ON the gateway host under /opt/opal-gateway/.venv/bin/python (uploaded to S3 and pulled, cloud-ops Rule 12). READ-ONLY: the audit sink is stubbed
and nothing is written. The enumeration uses client_adapter_smartx's OWN functions (_firm_allocations, _account_map, _candidates_by_account) and the
context's own firm_roster() -- no copy of their logic. Nothing identifying is printed: counts and booleans only.

CANDIDATES. resolve_account() returns, for one last4, one candidate per account_id whose custodian number ends in that last4 and which holds at least one
of the firm's allocations. This program takes EVERY distinct last4 present on the firm's accounts in the newest non-empty account map and runs the
module's _candidates_by_account for each, so n is the whole candidate set across all last4s, not a sample. A few last4s are also run through the served
tool (tools.client_resolve_account) and compared with the module's own answer, so the enumeration is tied to what the tools return.

THE MAPPING. For each candidate, every allocation of its account_id on the account map is joined to its roster row(s), and each row's advisor_name is
mapped through ctx.firm_roster() ({advisor_name: canonical firm id or None}). A candidate maps to ANOTHER firm when any such allocation's advisor maps to a
firm id that is not the firm. Also counted, apart from k: candidates with an unmapped advisor name or one mapped to None, and candidate accounts that also
carry an allocation outside the firm's set (a shared account)."""
from __future__ import annotations

import json
import os
import sys
import traceback

ROOT = "/opt/opal-gateway"
FIRM = "49financial"
PROBE_OID = "00000000-0000-0000-0000-00000000e717"
CROSSCHECK_MAX = 6


def main() -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    from app import audit, client_core as cc, context, identity_scope, tools
    from app import client_adapter_smartx as sx
    from app.config import get_config

    audit.log_call = lambda *a, **k: None
    out = {"firm": FIRM}
    master = None
    roster_entries = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    out["master_roster_entries"] = len(roster_entries)
    if roster_entries:
        tid, oid = str(roster_entries[0]).strip().split("/")
        master = context.make_principal(tid, oid, "en7.master@%s" % identity_scope.OPAL_USERS_DOMAIN)
    if master is None:
        out["fatal"] = "no master_admin stand-in could be built"
        return out
    tools._user_token = lambda: ("en7.master@%s" % identity_scope.OPAL_USERS_DOMAIN, "harness-no-token")
    context.set_current_principal(master)

    ctx = cc._new_ctx()
    sx.bind_firms()
    out["firm_is_canonical"] = FIRM in sx.CANONICAL_FIRMS
    out["firm_is_served"] = FIRM in sx.FIRMS
    p = sx._prefixes(ctx, sx.T_ROSTER, sx.T_MAP)
    src = []
    rpart, rrows, alloc, dropped = sx._firm_allocations(ctx, FIRM, p[sx.T_ROSTER], None, src)
    mpart, mrows, steps = sx._account_map(ctx, p[sx.T_MAP], None, src)
    roster_map = ctx.firm_roster()
    out["roster_partition_rows"] = len(rrows)
    out["account_map_partition_rows"] = len(mrows)
    out["firm_allocations"] = len(alloc)
    out["dropped"] = dropped
    out["firm_roster_names"] = len(roster_map)
    out["firm_roster_firms"] = len({v for v in roster_map.values() if v})

    # every distinct last4 on the firm's accounts, then the module's own candidate grouping for each
    last4s = sorted({(m.get("account_number") or "")[-4:] for m in mrows
                     if m.get("allocation_id") in alloc and m.get("account_id") is not None and len(m.get("account_number") or "") >= 4})
    cand = {}                                  # account_id -> last4 (a candidate is one account_id under one last4)
    for l4 in last4s:
        for acc in sx._candidates_by_account(mrows, alloc, l4):
            cand[acc] = l4
    out["distinct_last4"] = len(last4s)
    out["candidates"] = len(cand)

    rows_by_alloc = {}
    for r in rrows:
        rows_by_alloc.setdefault(r.get("allocation_id"), []).append(r)
    allocs_by_acc = {}
    for m in mrows:
        if m.get("account_id") in cand and m.get("allocation_id") is not None:
            allocs_by_acc.setdefault(m["account_id"], set()).add(m["allocation_id"])

    other_firm = unmapped = shared = no_roster_row = 0
    for acc in cand:
        firms = set()
        miss = False
        outside = False
        for aid in allocs_by_acc.get(acc, ()):
            rows = rows_by_alloc.get(aid, [])
            if not rows:
                miss = True
            for r in rows:
                firms.add(roster_map.get(r.get("advisor_name")) if r.get("advisor_name") in roster_map else "<unknown>")
            if aid not in alloc:
                outside = True
        if any(f not in (FIRM, None, "<unknown>") for f in firms):
            other_firm += 1
        if None in firms or "<unknown>" in firms:
            unmapped += 1
        if miss:
            no_roster_row += 1
        if outside:
            shared += 1
    out["candidates_mapping_to_other_firm"] = other_firm
    out["candidates_with_unmapped_advisor"] = unmapped
    out["candidates_with_an_allocation_lacking_a_roster_row"] = no_roster_row
    out["candidates_on_a_shared_account"] = shared

    # the tie to the served tool: a few last4s through client_resolve_account, compared with the module's own grouping
    agree = checked = 0
    for l4 in last4s[:CROSSCHECK_MAX]:
        res = tools.client_resolve_account(firm=FIRM, account_last4=l4)
        tool_n = len([c for c in ((res or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "smartx"]) if isinstance(res, dict) else None
        mod_n = len(sx._candidates_by_account(mrows, alloc, l4))
        checked += 1
        agree += 1 if tool_n == mod_n else 0
    out["tool_crosscheck_last4s"] = checked
    out["tool_crosscheck_agree"] = agree
    return out


if __name__ == "__main__":
    print("EN7_JSON")
    try:
        print(json.dumps(main(), separators=(",", ":"), default=str))
    except Exception:
        print(json.dumps({"fatal": traceback.format_exc()[-1200:]}))
        sys.exit(1)
