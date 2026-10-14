"""MP-pd-1 run builder (run from the worktree root).

Pairs the served page rows (the SSM probe stdout, pd1_page_probe_stdout.txt) with the grant-store principals read under
the operator role (raw DynamoDB Query output in a scratch directory). The tool table and the record names are read from
the served source (infra/aws/ec2/opal-gateway/app/data_entitlement.py) by ast, never retyped. Writes the run file
pd1_run.json and the derived store detail pd1_store_read.json. No credential is read, printed or written here.

usage: python pd1_run.py <page_stdout> <raw_dir> <caller_arn> <ssm_command_id>
"""
import ast
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DE_SRC = "infra/aws/ec2/opal-gateway/app/data_entitlement.py"
WANT = ("PROFILE", "GRANT", "REVISION_DIGITS", "SCHWAB_TOOLS")


def served_constants(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in WANT:
                out[node.targets[0].id] = ast.literal_eval(node.value)
    missing = [w for w in WANT if w not in out]
    if missing:
        raise SystemExit("served constants missing: %s" % missing)
    return out


def deser(v):
    """One DynamoDB attribute value (the CLI's JSON form) -> a plain Python value."""
    if "S" in v:
        return v["S"]
    if "N" in v:
        return int(v["N"])
    if "BOOL" in v:
        return bool(v["BOOL"])
    if "NULL" in v:
        return None
    if "M" in v:
        return {k: deser(x) for k, x in v["M"].items()}
    if "L" in v:
        return [deser(x) for x in v["L"]]
    if "SS" in v:
        return list(v["SS"])
    if "NS" in v:
        return [int(x) for x in v["NS"]]
    raise ValueError("unknown attribute shape %r" % (list(v),))


def items_of(path):
    doc = json.load(open(path, encoding="utf-8"))
    return [{k: deser(v) for k, v in it.items()} for it in doc.get("Items", [])]


def store_principal(tid, oid, items, C):
    """The adapter's own rule (data_entitlement / access_state): a profile + its active grant at grant_revision."""
    prof = next((i for i in items if i.get("sk") == C["PROFILE"]), None)
    if prof is None:
        return {"tid": tid, "oid": oid, "email": "", "profile_status": None, "grant_revision": None,
                "grant_status": None, "operations": [], "masters": [], "portal_channels": [],
                "portal_only": False, "active": False, "store_tools": [], "query_items": len(items)}
    email = str(prof.get("email") or "").strip().lower()
    gr = prof.get("grant_revision")
    grant = None
    if isinstance(gr, int) and not isinstance(gr, bool):
        sk = "%s#%0*d" % (C["GRANT"], C["REVISION_DIGITS"], gr)
        grant = next((i for i in items if i.get("sk") == sk), None)
    scope = (grant or {}).get("scope") or {}
    ops = sorted(set(scope.get("operations") or []))
    masters = sorted(scope.get("masters") or [])
    pch = sorted(scope.get("portal_channels") or [])
    active = prof.get("status") == "active" and bool(grant) and grant.get("status") == "active"
    portal_only = bool(pch) and not masters
    tools = [] if (not active or portal_only) else sorted(
        t for t, op in C["SCHWAB_TOOLS"].items() if op is None or op in ops)
    return {"tid": tid, "oid": oid, "email": email, "profile_status": prof.get("status"), "grant_revision": gr,
            "grant_status": (grant or {}).get("status") if grant else None, "operations": ops, "masters": masters,
            "portal_channels": pch, "portal_only": portal_only, "active": active, "store_tools": tools,
            "query_items": len(items)}


def main():
    page_path, raw_dir, caller_arn, cid = sys.argv[1:5]
    C = served_constants(DE_SRC)   # run from the worktree root
    page_line = [ln for ln in open(page_path, encoding="utf-8").read().splitlines() if ln.startswith("PD1PAGE ")]
    if len(page_line) != 1:
        raise SystemExit("page stdout must carry exactly one PD1PAGE line, found %d" % len(page_line))
    page = json.loads(page_line[0][len("PD1PAGE "):])
    if "error" in page:
        raise SystemExit("page probe error: %s" % page["error"])
    page_rows = page["page_rows"]
    scan = [tuple(p) for p in page["scan_principals"]]

    stores, unmatched, blocking = [], [], []
    for tid, oid in scan:
        base = os.path.join(raw_dir, oid)
        rc_path = base + ".rc"
        rc = open(rc_path, encoding="utf-8").read().strip() if os.path.exists(rc_path) else "absent"
        if rc != "0":
            err = open(base + ".err", encoding="utf-8", errors="replace").read().strip()[:400] \
                if os.path.exists(base + ".err") else ""
            blocking.append({"tid": tid, "oid": oid, "rc": rc, "error": err})
            stores.append({"tid": tid, "oid": oid, "email": "", "store_tools": [], "read": "denied",
                           "reason": "operator-role Query rc=%s" % rc})
            continue
        s = store_principal(tid, oid, items_of(base + ".json"), C)
        s["read"] = "ok"
        stores.append(s)

    per, used = [], set()
    for s in stores:
        who = s["email"] or ("%s/%s" % (s["tid"], s["oid"]))
        matched = None
        for i, row in enumerate(page_rows):
            if i in used:
                continue
            if s["email"] and row["who"].strip().lower() == s["email"]:
                matched, how = i, "email"
                break
            if row["who"].strip().lower() == ("%s/%s" % (s["tid"], s["oid"])):
                matched, how = i, "tid/oid key"
                break
        if matched is None:
            unmatched.append({"side": "store_only", "who": who, "reason": "no page row with a data grant"})
            page_tools = []
            s["matched_by"] = None
        else:
            used.add(matched)
            page_tools = sorted(page_rows[matched]["page_tools"])
            s["matched_by"] = how
            who = page_rows[matched]["who"]
        per.append({"who": who, "store_tools": s["store_tools"], "page_tools": page_tools})
    for i, row in enumerate(page_rows):
        if i not in used:
            unmatched.append({"side": "page_only", "who": row["who"], "reason": "no store principal in the scan"})
            per.append({"who": row["who"], "store_tools": [], "page_tools": sorted(row["page_tools"])})

    run = {"caller_arn": caller_arn, "principals": len(per),
           "tools_compared": sum(len(r["store_tools"]) for r in per), "per_principal": per,
           "page_rows_with_grant": page["page_rows_with_grant"], "unmatched": unmatched,
           "ssm_command_id": cid}
    detail = {"served_constants_from": DE_SRC, "schwab_tools": C["SCHWAB_TOOLS"], "store_principals": stores,
              "blocking": blocking, "scan_principals": len(scan)}
    with open(os.path.join(HERE, "pd1_run.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(run, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(HERE, "pd1_store_read.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(detail, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("principals=%d tools_compared=%d page_rows_with_grant=%d unmatched=%d blocking=%d" % (
        run["principals"], run["tools_compared"], run["page_rows_with_grant"], len(unmatched), len(blocking)))


if __name__ == "__main__":
    main()
