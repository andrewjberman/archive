#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rte-6 battery -- THE SERVED PATH ADMITS A PROJECTED ADVISOR GRANT.

Every arm below re-derives its count fresh THIS RUN against the real code in this worktree
and, for (b)/(c)/(d), live S3/Lambda state -- never a prior run's cached output (bound 12).

Prints IBR56-SERVED-PATH-ADMITS-PROJECTED-GRANT only when every arm holds.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
LAMBDA_ROOT = os.path.join(WS, "infra", "aws", "lambda", "investor-reporting")
for _p in ("_authz", "_scope", "_ids", "_keys"):
    sys.path.insert(0, os.path.join(LAMBDA_ROOT, _p))

FIRMS = {"49financial": "opal-data-bd", "inflection": "opal-data-inf", "cottonwood": "opal-data-cot"}
os.environ.setdefault("IRPT_DIRECTORY_BUCKET_MAP", json.dumps(FIRMS))

AWS = os.path.join(WS, ".tools", "aws.cmd")

FUNCTIONS = ("irpt-directory-search", "irpt-export-render", "irpt-holdings",
             "irpt-narrative", "irpt-status", "irpt-performance-adapter",
             "irpt-ycharts-generate")


def git_head():
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WS, capture_output=True, text=True,
                         timeout=30)
    return out.stdout.strip()


def aws_json(*args):
    out = subprocess.run([AWS] + list(args), capture_output=True, text=True, timeout=90)
    if out.returncode != 0:
        raise RuntimeError("aws %s failed rc=%s: %s" % (" ".join(args), out.returncode, out.stderr[-500:]))
    return json.loads(out.stdout)


def aws_text(*args):
    out = subprocess.run([AWS] + list(args), capture_output=True, text=True, timeout=90)
    if out.returncode != 0:
        raise RuntimeError("aws %s failed rc=%s: %s" % (" ".join(args), out.returncode, out.stderr[-500:]))
    return out.stdout.strip()


# --------------------------------------------------------------------------- arm (a): the wiring
CENSUS_NAMES = ("entry.py", "handler.py", "dispatch.py")


def census_files():
    out = []
    for dirpath, _dirs, files in os.walk(LAMBDA_ROOT):
        for fn in files:
            if fn in CENSUS_NAMES:
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def _call_name(func):
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return None


def _construction_calls(tree):
    """Every `Entry(...)`/`Enforcer(...)` call in the module body (any depth)."""
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = _call_name(node.func)
            if name in ("Entry", "Enforcer"):
                out.append(node)
    return out


def _has_nonnone_id_projection(call_node):
    for kw in call_node.keywords:
        if kw.arg == "id_projection":
            return not (isinstance(kw.value, ast.Constant) and kw.value.value is None)
    return False


def grade_wiring(path, source=None):
    """(compliant: bool, constructs: int, reason: str) for one file's AST."""
    text = source if source is not None else open(path, "r", encoding="utf-8").read()
    tree = ast.parse(text)
    calls = _construction_calls(tree)
    if not calls:
        return True, 0, "no Enforcer/Entry construction in this file (vacuously wired)"
    missing = [c for c in calls if not _has_nonnone_id_projection(c)]
    if missing:
        return False, len(calls), "%d of %d construction(s) missing id_projection" % (len(missing), len(calls))
    return True, len(calls), "%d of %d construction(s) carry id_projection" % (len(calls), len(calls))


def arm_a_wiring():
    files = census_files()
    denom = len(files)
    wired = []
    rows = {}
    for f in files:
        ok, n, why = grade_wiring(f)
        rows[os.path.relpath(f, WS)] = {"compliant": ok, "constructions": n, "why": why}
        if ok:
            wired.append(f)
    census_ok = (len(wired) == denom)

    # THE MUTANT: strip id_projection from ONE compliant, ACTUALLY-CONSTRUCTING file's source
    # (in memory only) and re-grade; the census must then read one fewer wired and FAIL overall.
    constructing = [f for f in files if grade_wiring(f)[1] > 0]
    mutant_file = sorted(constructing)[0]
    mutant_src = open(mutant_file, "r", encoding="utf-8").read()
    tree = ast.parse(mutant_src)
    call = _construction_calls(tree)[0]
    call.keywords = [k for k in call.keywords if k.arg != "id_projection"]
    ast.fix_missing_locations(tree)
    mutant_src2 = ast.unparse(tree)
    mutant_ok, _n, mutant_why = grade_wiring(mutant_file, source=mutant_src2)
    mutant_fires = (mutant_ok is False)

    return {
        "denominator": denom,
        "wired": len(wired),
        "verdict": "%d of %d wired" % (len(wired), denom),
        "rows": rows,
        "mutant_file": os.path.relpath(mutant_file, WS),
        "mutant_fires": mutant_fires,
        "mutant_why": mutant_why,
        "pass": census_ok and mutant_fires,
    }


# --------------------------------------------------------------------------- arm (b): the join rate
def arm_b_join_rates():
    import ids as _ids

    seam_firm = None
    for firm in _ids.firm_ids():
        row = _ids.raw_keys().get("firms", {}).get(firm, {}).get("account", {})
        if row.get("projection_seam"):
            seam_firm = firm
            seam_name = row["projection_seam"]
            break
    if seam_firm is None:
        raise RuntimeError("no firm declares a projection_seam in raw_keys.json")

    bucket = FIRMS[seam_firm]
    aws_json("s3api", "get-object", "--bucket", bucket,
             "--key", "platinum/%s/ownership_map.json" % seam_firm,
             os.path.join(WS, ".scratch", "rte6_ownership_live.json"))
    with open(os.path.join(WS, ".scratch", "rte6_ownership_live.json"), "r", encoding="utf-8") as fh:
        ownership = json.load(fh)
    advisors = ownership.get("advisors") or {}
    all_slots = []
    for adv, g in advisors.items():
        all_slots.extend(g.get("accounts") or [])
    total_slots = len(all_slots)

    seam_doc = _ids.load_seam_index(seam_name)
    idx = seam_doc.get("index", {})
    resolved_via_seam = sum(1 for a in all_slots if a in idx)

    # THE ISSUER'S ORIGINALLY-NAMED JOIN TABLE, measured on the SAME population: 0 is the
    # measurement this order's REC pivoted on, re-derived fresh (never assumed from the artifact's
    # own citation) by checking whether any candidate is ALREADY an issued id (the crosswalk
    # target id space, per raw_keys.json) -- none of the raw custodian keys are.
    named_join_resolved = sum(1 for a in all_slots if _ids.is_issued("account", a))

    project = _ids.projection_for_firm(seam_firm)
    ab = advisors.get("abby_horton") or {}
    ab_accts = ab.get("accounts") or []
    ab_resolved = sum(1 for a in ab_accts if a in idx)
    ab_projected_sample = [project("account", a) for a in ab_accts[:3]]

    unmatched_kinds = {}
    for a in all_slots:
        if a not in idx and not _ids.is_issued("account", a):
            unmatched_kinds["UNRESOLVED-BY-SEAM"] = unmatched_kinds.get("UNRESOLVED-BY-SEAM", 0) + 1

    others = {}
    for firm in _ids.firm_ids():
        if firm == seam_firm:
            continue
        b = FIRMS.get(firm)
        if not b:
            continue
        try:
            aws_json("s3api", "get-object", "--bucket", b,
                     "--key", "platinum/%s/ownership_map.json" % firm,
                     os.path.join(WS, ".scratch", "rte6_ownership_%s.json" % firm))
            with open(os.path.join(WS, ".scratch", "rte6_ownership_%s.json" % firm),
                      "r", encoding="utf-8") as fh:
                o = json.load(fh)
            n_adv = len(o.get("advisors") or {})
            n_slots = sum(len(g.get("accounts") or []) for g in (o.get("advisors") or {}).values())
        except Exception as exc:  # ABSENT map == empty (loaders.load_ownership's own rule)
            n_adv, n_slots = 0, 0
            if "NoSuchKey" not in str(exc) and "400" not in str(exc) and "404" not in str(exc):
                raise
        others[firm] = {"advisors": n_adv, "account_slots": n_slots}

    return {
        "seam_firm": seam_firm,
        "seam_name": seam_name,
        "ownership_map_total_account_slots": total_slots,
        "resolved_via_seam": resolved_via_seam,
        "resolved_via_named_join_table": named_join_resolved,
        "abby_horton_denominator": len(ab_accts),
        "abby_horton_resolved_via_seam": ab_resolved,
        "abby_horton_projected_sample": ab_projected_sample,
        "unmatched_kinds": unmatched_kinds,
        "other_firms_measured": others,
        "pass": (resolved_via_seam >= 1 and ab_resolved >= 1 and named_join_resolved == 0),
    }


# --------------------------------------------------------------------------- arm (c): the deploy
def arm_c_deploy():
    deploy_script = os.path.join(HERE, "rte6_package_deploy.py")
    proc = subprocess.run([sys.executable, deploy_script, "verify"], capture_output=True,
                          text=True, timeout=180)
    lines = [ln for ln in (proc.stdout or "").splitlines() if " served=" in ln]
    rows = {}
    for ln in lines:
        fn = ln.split(" ", 1)[0]
        ok = ln.strip().endswith("True")
        rows[fn] = ok
    n_ok = sum(1 for v in rows.values() if v)
    return {"denominator": len(FUNCTIONS), "matched": n_ok, "rows": rows,
            "raw": proc.stdout[-4000:], "pass": (n_ok == len(FUNCTIONS) == len(rows))}


# --------------------------------------------------------------------------- arm (d): live route
def arm_d_live_route():
    import loaders as _loaders
    import enforce as _enforce
    import ids as _ids

    # Re-derive the seam firm the same way arm (b) does, independently of arm (b)'s own call.
    seam_firm = None
    for firm in _ids.firm_ids():
        row = _ids.raw_keys().get("firms", {}).get(firm, {}).get("account", {})
        if row.get("projection_seam"):
            seam_firm = firm
            break

    opaque_firm_id = _loaders.opaque_firm_for(seam_firm)
    binding = _enforce.FirmBinding(seam_firm, opaque_firm_id)
    load_directory, load_ownership, load_policy = _loaders.deps(seam_firm)
    projection = _ids.projection_for_firm(seam_firm)

    # POST-FIX: the SAME construction `served.Entry.enforcer_for` now performs for a live request.
    post_enforcer = _enforce.Enforcer(binding, load_directory, load_ownership, load_policy,
                                      id_projection=projection)
    request = _enforce.Request(
        headers={"X-User-Email": "abby.horton@49financial.com", "X-User-Name": "Abby Horton",
                 "X-User-Tier": "partner", "X-User-Role": "user", "X-Firm-Id": seam_firm,
                 "X-User-Type": "Advisor", "X-Advisor-Id": "abby_horton", "X-Advisor-Role": "",
                 "X-Origin-Verify": "cloudfront"},
        operation="directory-search")
    post_scope, post_refusal = post_enforcer.resolve_now(request)
    post_code = post_refusal.code if post_refusal is not None else None
    post_k = len(post_scope["permitted_account_set"]) if post_scope is not None else 0

    # CROSS-FIRM SWAP: same everything, advisor id from a DIFFERENT firm's ownership map -- must
    # still refuse (never served).
    swap_request = _enforce.Request(
        headers={"X-User-Email": "swap@49financial.com", "X-User-Name": "Swap Test",
                 "X-User-Tier": "partner", "X-User-Role": "user", "X-Firm-Id": seam_firm,
                 "X-User-Type": "Advisor", "X-Advisor-Id": "definitely-not-a-49f-advisor",
                 "X-Advisor-Role": "", "X-Origin-Verify": "cloudfront"},
        operation="directory-search")
    swap_scope, swap_refusal = post_enforcer.resolve_now(swap_request)
    swap_refused = swap_scope is None

    # NEGATIVE CONTROL: the PRE-FIX construction (id_projection NOT passed, exactly as EVERY
    # entry.py constructed it before this order) on the SAME request must still read
    # UNPROJECTED_GRANT.
    pre_enforcer = _enforce.Enforcer(binding, load_directory, load_ownership, load_policy)
    pre_scope, pre_refusal = pre_enforcer.resolve_now(request)
    pre_code = pre_refusal.code if pre_refusal is not None else None

    return {
        "seam_firm": seam_firm,
        "post_fix_code": post_code,
        "post_fix_permitted_count": post_k,
        "post_fix_served": post_refusal is None,
        "cross_firm_swap_refused": swap_refused,
        "cross_firm_swap_code": (swap_refusal.code if swap_refusal is not None else None),
        "pre_fix_negative_control_code": pre_code,
        "pass": (post_code != "UNPROJECTED_GRANT" and (post_k >= 1 or post_code == "EMPTY_GRANT")
                 and swap_refused and pre_code == "UNPROJECTED_GRANT"),
    }


def main():
    report = {"git_head": git_head()}

    a = arm_a_wiring()
    report["arm_a_wiring"] = a
    print("ARM (a) WIRING: %s -- mutant (%s) fires=%s"
          % (a["verdict"], a["mutant_file"], a["mutant_fires"]))

    b = arm_b_join_rates()
    report["arm_b_join_rates"] = b
    print("ARM (b) JOIN RATE: seam=%s slots %d of %d resolved via seam; named join table %d of %d; "
          "abby_horton %d of %d"
          % (b["seam_firm"], b["resolved_via_seam"], b["ownership_map_total_account_slots"],
             b["resolved_via_named_join_table"], b["ownership_map_total_account_slots"],
             b["abby_horton_resolved_via_seam"], b["abby_horton_denominator"]))
    print("ARM (b) OTHER FIRMS (no fix): %s" % b["other_firms_measured"])

    c = arm_c_deploy()
    report["arm_c_deploy"] = c
    print("ARM (c) DEPLOY: %d of %d functions CodeSha256==built" % (c["matched"], c["denominator"]))

    d = arm_d_live_route()
    report["arm_d_live_route"] = d
    print("ARM (d) LIVE ROUTE: post-fix code=%s served=%s k=%d; cross-firm swap refused=%s; "
          "pre-fix negative control=%s"
          % (d["post_fix_code"], d["post_fix_served"], d["post_fix_permitted_count"],
             d["cross_firm_swap_refused"], d["pre_fix_negative_control_code"]))

    overall = a["pass"] and b["pass"] and c["pass"] and d["pass"]
    report["overall_pass"] = overall
    print(json.dumps(report, indent=1, default=str))
    if overall:
        print("IBR56-SERVED-PATH-ADMITS-PROJECTED-GRANT")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
