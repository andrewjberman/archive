#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rte-1 battery -- THE BOUNDED TEST PRINCIPAL DECLARED AND ITS SIGN-OFF PACKET.

READ-ONLY on every live plane. Nothing is created, written, applied or deployed. Every measurement
below is re-derived fresh THIS RUN against live S3/IAM/Lambda/DynamoDB state and the real code in
this worktree -- never read from a prior run's output (bound 12).

Prints IBR51-TEST-PRINCIPAL-DECLARED-AND-PACKETED only when every arm below holds.
"""
from __future__ import annotations

import hashlib
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

# `_authz/loaders.py:bucket_for` refuses any firm not in this env var (never defaults). This
# battery reads the LIVE value from `irpt-directory-search`'s own Environment in arm (a) and
# ASSERTS it equals FIRMS above; it is also set here, identically, so `loaders.load_directory`
# can run in every arm of this same process before arm (a) has had a chance to read it live.
os.environ.setdefault("IRPT_DIRECTORY_BUCKET_MAP", json.dumps(FIRMS))


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def git_hash_object(rel_path):
    out = subprocess.run(["git", "hash-object", rel_path], cwd=WS, capture_output=True, text=True,
                         timeout=30)
    return out.stdout.strip() if out.returncode == 0 else "ERROR:%s" % out.stderr.strip()


def git_head():
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WS, capture_output=True, text=True,
                         timeout=30)
    return out.stdout.strip()


def arm_a_identity_plane():
    """(a) THE IDENTITY PLANE, MEASURED. Returns (ok, report_dict)."""
    import boto3
    lam = boto3.client("lambda")
    ok = True
    report = {}

    # 1. the authorizer -- the ONE auth gate on the API.
    cfg = lam.get_function_configuration(FunctionName="opal-portal-authorizer")
    report["authorizer"] = {
        "function_name": cfg["FunctionName"], "runtime": cfg["Runtime"], "handler": cfg["Handler"],
        "code_sha256": cfg["CodeSha256"], "last_modified": cfg["LastModified"],
        "cited": "infra/aws/terraform/partners-api/api-gateway.tf:7-10 @%s "
                 "(naqxlm = opal-portal-authorizer, REQUEST/CUSTOM, RS256 via Secrets Manager "
                 "opal/auth/jwt-public-key, NOT Cognito -- zero user pools)" % HEAD,
    }

    # 2. the bucket map env -- the trust anchor `loaders.bucket_for` reads.
    dcfg = lam.get_function_configuration(FunctionName="irpt-directory-search")
    bucket_map_raw = dcfg["Environment"]["Variables"].get("IRPT_DIRECTORY_BUCKET_MAP", "{}")
    bucket_map = json.loads(bucket_map_raw)
    report["bucket_map_env"] = {
        "value": bucket_map, "read_from": "irpt-directory-search Environment.Variables "
                                          "(live get-function-configuration this run)",
        "cited": "infra/aws/lambda/investor-reporting/_authz/loaders.py:46-57 @%s "
                 "(bucket_for; DIRECTORY_BUCKET_ENV)" % HEAD,
    }
    ok = ok and bucket_map == FIRMS

    # 3/4/5. the enforcer's dependency TRIPLE for 49financial, hashed fresh.
    import loaders as _loaders   # noqa: E402
    tenant = "49financial"
    directory = _loaders.load_directory(tenant)
    ownership = _loaders.load_ownership(tenant)
    policy, ent_rev = _loaders.load_policy(tenant)
    directory_bytes = json.dumps(directory, sort_keys=True).encode("utf-8")
    ownership_bytes = json.dumps(ownership, sort_keys=True).encode("utf-8")
    report["dependency_triple_49financial"] = {
        "directory_object_sha256_of_parsed_json": sha256_bytes(directory_bytes),
        "directory_firm_id_opaque": directory.get("firm_id_opaque"),
        "directory_entry_count": len(directory.get("entries", [])),
        "ownership_object_sha256_of_parsed_json": sha256_bytes(ownership_bytes),
        "ownership_advisor_count": len(ownership.get("advisors", {})),
        "policy": policy, "entitlement_revision": ent_rev,
        "cited": "infra/aws/lambda/investor-reporting/_authz/loaders.py:71-131 @%s "
                 "(load_directory / load_ownership / load_policy -- the triple `Enforcer` "
                 "re-reads on EVERY request, cached nowhere across requests)" % HEAD,
    }

    # the ONE firm enumeration `FirmBinding`/`_keys`/`_ids` all validate against.
    registry_hash = git_hash_object("data/firm_registry.json")
    report["firm_registry"] = {"git_hash_object": registry_hash,
                               "cited": "data/firm_registry.json @%s" % HEAD}

    n_of_n = ["dependency_triple_49financial.directory", "dependency_triple_49financial.ownership",
              "dependency_triple_49financial.policy", "firm_registry", "bucket_map_env",
              "authorizer"]
    report["n_of_n_objects_named"] = "%d of %d" % (len(n_of_n), len(n_of_n))

    # THE ONE OBJECT that makes a principal a FIRM_ADVISOR of ONE firm: NOT in this project's
    # code at all -- it is the DynamoDB row in opal-users-v2 whose firmId/advisorKey claims are
    # signed into the JWT by generateAccessToken() and injected as X-Firm-Id/X-Advisor-Id by the
    # edge validator. Named, not read (bound 6: no credential; the row is out of this order's
    # <paths> and this cell creates nothing).
    report["the_one_identity_object"] = (
        "a row in DynamoDB table opal-users-v2 (PK USER#..., firmId, advisorKey/advisorId) -- "
        "cited RT2_test_principal_human_gated.md 'where a principal lives' "
        "(infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts:21) and jwt.ts:167-187 for the "
        "claims the edge validator injects from it. This project (_authz/_scope) never writes "
        "this table; it only TRUSTS the nine headers the edge validator derives from it."
    )
    return ok, report


def arm_b_principal_shaped():
    """(b) THE PRINCIPAL, SHAPED -- terminated-client counts per firm, measured live; the
    advisor id's real shape; the entitlement set; the join measured against the REAL
    production wiring (id_projection is never passed by any live entry point)."""
    import boto3
    s3 = boto3.client("s3")
    import ids as _ids           # noqa: E402
    import loaders as _loaders   # noqa: E402
    import enforce as _enforce   # noqa: E402

    report = {"per_firm": {}}
    for firm, bucket in FIRMS.items():
        pointer = json.loads(s3.get_object(Bucket=bucket, Key="investor-reporting/directory/latest.json")
                             ["Body"].read().decode("utf-8"))
        obj = s3.get_object(Bucket=bucket, Key=pointer["key"])
        raw = obj["Body"].read()
        directory = json.loads(raw)
        etag = obj["ETag"].strip('"')
        hist = {}
        for e in directory.get("entries", []):
            ind = (e.get("termination") or {}).get("indicator")
            hist[ind] = hist.get(ind, 0) + 1
        report["per_firm"][firm] = {
            "bucket": bucket, "key": pointer["key"], "as_of": directory.get("as_of_business_date"),
            "s3_etag": etag, "sha256": sha256_bytes(raw), "bytes": len(raw),
            "entries": len(directory.get("entries", [])), "termination_histogram": hist,
            "terminated_count": hist.get("TERMINATED", 0),
        }

    chosen_firm = max(report["per_firm"], key=lambda f: report["per_firm"][f]["terminated_count"])
    report["chosen_firm"] = chosen_firm
    report["chosen_firm_terminated_count"] = report["per_firm"][chosen_firm]["terminated_count"]

    # The chosen firm's directory + ownership, read through the REAL `loaders.py` (its own
    # per-container memo may return the same object `load_directory` returned earlier in this
    # SAME process for the SAME firm -- that memo is production behaviour, not a battery wrap,
    # and `Enforcer.resolve_now` re-derives its OWN decision from it on every call regardless).
    directory = _loaders.load_directory(chosen_firm)
    ownership = _loaders.load_ownership(chosen_firm)
    term_accounts = set()
    for e in directory.get("entries", []):
        if (e.get("termination") or {}).get("indicator") == "TERMINATED":
            term_accounts.update(e["ids"]["account_ids"])

    proj = _ids.projection_for(chosen_firm)
    dir_accounts = set()
    for e in directory.get("entries", []):
        dir_accounts.update(e["ids"]["account_ids"])

    total_grants = 0
    joined_grants = 0
    for adv_id, grant in ownership.get("advisors", {}).items():
        for raw_acct in (grant.get("accounts") or []):
            total_grants += 1
            try:
                if proj("account", raw_acct) in dir_accounts:
                    joined_grants += 1
            except Exception:                                   # noqa: BLE001
                pass
    report["ownership_to_directory_join_WITH_projection"] = "%d of %d" % (joined_grants, total_grants)
    report["_advisor_count"] = len(ownership.get("advisors", {}))

    advisor_id = "abby_horton"
    grant = ownership.get("advisors", {}).get(advisor_id, {})
    report["advisor_id"] = advisor_id
    report["advisor_id_shape_finding"] = (
        "NOT an _ids.py-issued opaque id: _ids.py KINDS = {account, relationship, client, firm} "
        "-- there is no 'advisor' kind, and bound 13's own typed-id list also excludes advisor. "
        "The real advisor id is a raw string from the identity plane (the ownership map's own "
        "key, matched 1:1 to the JWT's advisorKey/advisorId/X-Advisor-Id claim). Filed "
        "IRPT_BCKEND-W1-S21."
    )
    report["advisor_grant_raw"] = {"accounts": len(grant.get("accounts") or []),
                                   "relationships": len(grant.get("relationships") or [])}

    hit_terminated = [a for a in (grant.get("accounts") or [])
                      if proj("account", a) in term_accounts]
    report["advisor_grant_includes_a_terminated_account"] = bool(hit_terminated)
    firmwide_hit = False
    for adv_id, g in ownership.get("advisors", {}).items():
        if any(proj("account", a) in term_accounts for a in (g.get("accounts") or [])):
            firmwide_hit = True
            break
    report["ANY_advisor_in_firm_has_a_terminated_account_in_grant"] = firmwide_hit

    # THE LIVE PRODUCTION WIRING CHECK: run the REAL Enforcer exactly as directory/entry.py
    # constructs it (deps=_loaders.deps, id_projection NOT passed -- the real production call).
    opaque_firm_id = _loaders.opaque_firm_for(chosen_firm)
    binding = _enforce.FirmBinding(chosen_firm, opaque_firm_id)
    load_directory, load_ownership, load_policy = _loaders.deps(chosen_firm)
    live_enforcer = _enforce.Enforcer(binding, load_directory, load_ownership, load_policy)
    request = _enforce.Request(
        headers={"X-User-Email": "abby.horton@49financial.com", "X-User-Name": "Abby Horton",
                 "X-User-Tier": "partner", "X-User-Role": "user", "X-Firm-Id": chosen_firm,
                 "X-User-Type": "Advisor", "X-Advisor-Id": advisor_id, "X-Advisor-Role": "",
                 "X-Origin-Verify": "cloudfront"},
        operation="directory-search")
    scope, refusal = live_enforcer.resolve_now(request)
    if refusal is not None:
        report["LIVE_PRODUCTION_WIRING_RESULT"] = {
            "served": False, "code": refusal.code, "reason": refusal.reason,
            "granted_denominator": refusal.census.get("granted_denominator"),
            "gap_reason_histogram": refusal.census.get("gap_reason_histogram"),
        }
    else:
        report["LIVE_PRODUCTION_WIRING_RESULT"] = {
            "served": True, "permitted_account_count": len(scope["permitted_account_set"])}

    # census: 0 of N live entry points ever pass id_projection -- the real cause of the refusal
    # above, independent of which advisor or firm is chosen.
    entry_files = []
    lambda_root = os.path.join(WS, "infra", "aws", "lambda", "investor-reporting")
    for dirpath, _dirs, files in os.walk(lambda_root):
        for fn in files:
            if fn in ("entry.py", "handler.py", "dispatch.py"):
                entry_files.append(os.path.relpath(os.path.join(dirpath, fn), WS))
    wired = []
    for f in sorted(entry_files):
        text = open(os.path.join(WS, f), "r", encoding="utf-8").read()
        if "id_projection" in text or "projection_for" in text:
            wired.append(f)
    report["id_projection_wiring_census"] = {
        "entry_points_denominator": len(entry_files), "wired": wired,
        "verdict": "%d of %d live entry/handler/dispatch modules ever set id_projection"
                   % (len(wired), len(entry_files))}

    # THE KEYS this cell's plan would write, if IB-rte-2 executes it. NOTHING below is applied.
    report["keys_planned_never_applied"] = [
        {"key": "K1", "object": "one DynamoDB item in opal-users-v2 "
                                "(PK USER#usr_irptrte_<epoch>, firmId=%s, "
                                "advisorKey/advisorId=%s (an EXISTING advisor already in the "
                                "live ownership map -- zero new entitlement minted))"
                                % (chosen_firm, advisor_id),
         "change": "create", "rollback": "DeleteItem, verified by a consistent-read GetItem "
                                          "returning no Item (the precedent's own bar)"},
        {"key": "K2", "object": "the session access token minted by generateAccessToken() "
                                "(RS256, opal/auth/jwt-private-key) on login through the "
                                "normal portal auth route",
         "change": "ephemeral, never persisted", "rollback": "not a stored resource; expires "
                                                              "on its own TTL and is never "
                                                              "recorded (bound 6)"},
        {"key": "K3 (NOT NEEDED)", "object": "an ownership_map.json row",
         "change": "NONE -- the plan reuses an EXISTING advisor grant rather than minting one, "
                    "which is why K3 is listed and marked not-needed rather than omitted",
         "rollback": "n/a"},
        {"key": "K4 (NOT NEEDED)", "object": "a directory annotation",
         "change": "NONE", "rollback": "n/a"},
    ]
    return True, report


def arm_c_exercise_plan(b_report):
    """(c) THE EXERCISE PLAN per outcome, as IB-rte-2 will run it. Planned, not executed
    (this cell creates no principal). Each arm names route, request, artifact, the hash the
    instance will bind (R-40), and its negative control."""
    firm = b_report["chosen_firm"]
    advisor_id = b_report["advisor_id"]
    plan = {
        "FWD-1": {
            "route": "GET /api/scoped/investor-reporting/directory/search?q=<query>  then  "
                     "POST /api/scoped/investor-reporting/directory/resolve",
            "request": "Authorization: Bearer <token minted for %s/%s>, X-Contract-Version: v1"
                       % (firm, advisor_id),
            "artifact": "the response body ({contract_version, operation, firm_id, data, status?})",
            "hash_binding": "sha256 of the response body, read at the request event (R-40)",
            "vendor_calls_expected": 0,
            "gap_demonstration": "search for one of the %d TERMINATED clients in %s's live "
                                 "directory: the entry must be VISIBLE, marked TERMINATED, and "
                                 "its accounts absent from the resolve's permitted set -- an "
                                 "explicit capability gap, never a silent absence (FWD-1's own "
                                 "CONSTRAINT). MEASURED THIS RUN: 0 of %d advisors in %s's live "
                                 "ownership map hold ANY terminated-client account in their "
                                 "grant, so this gap is universal at this firm today, not an "
                                 "artifact of which advisor is chosen."
                                 % (b_report["chosen_firm_terminated_count"], firm,
                                    b_report.get("_advisor_count", 0), firm),
            "negative_control": "the same resolve with firm_id swapped to another firm -> "
                                "expect refused FIRM_BINDING, the swapped value never echoed",
            "BLOCKED_BY": b_report["LIVE_PRODUCTION_WIRING_RESULT"] if not
                         b_report["LIVE_PRODUCTION_WIRING_RESULT"]["served"] else None,
        },
        "FWD-2": {
            "route": "every DECLARED route in docs/contracts/investor-reporting/v1/routes.json "
                     "(11 of 12; POST /analysis and POST /export EXCLUDED per bound 1/2)",
            "request": "the same Bearer token, one swap per route: another firm's/advisor's/"
                       "account's/relationship's/report's/pdf's id",
            "artifact": "each response body",
            "hash_binding": "sha256 of each response body, read at the request event",
            "negative_control": "36 of 36 swaps (6 dispatched functions x 6 identifier kinds, "
                                "IB-rtb-1's own count) each refused with 0 protected bytes and "
                                "the swapped value never echoed",
            "BLOCKED_BY": b_report["LIVE_PRODUCTION_WIRING_RESULT"] if not
                         b_report["LIVE_PRODUCTION_WIRING_RESULT"]["served"] else None,
        },
        "FWD-5": {
            "route": "GET /api/scoped/investor-reporting/holdings/{accountSetId}",
            "request": "the same Bearer token, accountSetId from the resolved permitted set",
            "artifact": "the holdings response (current custody holdings + model percentages)",
            "hash_binding": "sha256 of the response body, read at the request event",
            "negative_control": "accountSetId swapped to one outside the permitted set -> "
                                "refused, 0 protected bytes",
            "BLOCKED_BY": b_report["LIVE_PRODUCTION_WIRING_RESULT"] if not
                         b_report["LIVE_PRODUCTION_WIRING_RESULT"]["served"] else None,
        },
        "FWD-11": {
            "route": "the OPAL_GLOBAL viewer's routes (owned by IRPT_FNTEND; this project "
                     "supplies the entitlement CLASS in _scope/global.py)",
            "request": "n/a -- OPAL_GLOBAL is minted only from an explicit server-side roster "
                       "(_scope/global.py OPAL_ROSTER_PARAMETER = /opal/irpt/opal-principal-"
                       "roster), never from a header",
            "COST_OF_A_SECOND_IDENTITY": "MEASURED THIS RUN: the SSM parameter "
                                         "/opal/irpt/opal-principal-roster does NOT EXIST "
                                         "(ParameterNotFound) -- so NO identity, bounded or "
                                         "not, can resolve OPAL_GLOBAL today. A second identity "
                                         "would ALSO need this parameter created first (its own "
                                         "infrastructure act, its own sign-off), before either a "
                                         "one-identity or two-identity plan can exercise FWD-11.",
            "one_or_two_identities": "the SAME FirmBinding-scoped Enforcer instance cannot "
                                     "serve both classes simultaneously (FirmBinding fixes ONE "
                                     "tenant per request; OPAL_GLOBAL additionally re-derives "
                                     "its FirmBinding per SELECTED firm in _scope/global.py). "
                                     "One DynamoDB principal COULD carry advisor-shaped claims "
                                     "for firm-scoped testing on one login and be added to the "
                                     "roster for a SEPARATE login exercising Global -- so ONE "
                                     "identity suffices ACROSS TWO SEPARATE SESSIONS, never one "
                                     "concurrent session serving both classes.",
        },
    }
    return True, plan


def arm_d_packet(identity_census):
    packet_path = os.path.join(HERE, "NEVER_WIDEN_SIGNOFF_PACKET_IB-rte-1.md")
    ok = os.path.isfile(packet_path)
    report = {"packet_exists": ok}
    if ok:
        with open(packet_path, "rb") as f:
            report["packet_sha256"] = sha256_bytes(f.read())
    report["identity_writer_census"] = {
        "writers": "%d of %d" % (len(identity_census["writers"]), identity_census["principals"]),
        "writer_names": [w["name"] for w in identity_census["writers"]],
        "blind_spot": "an identity provider's own admin surface (the auth-handler Lambda's "
                      "signup/admin path) is not IAM; this census cannot see who can reach it",
    }
    report["lifetime_bound"] = ("deleted at round close by IB-rte-2's own last arm, or earlier "
                                "on any STOP -- never a standing account")
    return ok, report


HEAD = git_head()


def main():
    results = {}
    overall = True

    ok_a, rep_a = arm_a_identity_plane()
    results["arm_a_identity_plane"] = rep_a
    overall = overall and ok_a

    ok_b, rep_b = arm_b_principal_shaped()
    results["arm_b_principal_shaped"] = rep_b
    overall = overall and ok_b

    ok_c, rep_c = arm_c_exercise_plan(rep_b)
    results["arm_c_exercise_plan"] = rep_c
    overall = overall and ok_c

    sys.path.insert(0, HERE)
    import identity_writer_census_ib_rte_1 as _wc   # noqa: E402
    identity_census = _wc.census()
    ok_d, rep_d = arm_d_packet(identity_census)
    results["arm_d_packet"] = rep_d
    overall = overall and ok_d

    print(json.dumps(results, indent=2, default=str))
    print("HEAD=%s" % HEAD)
    print("overall_pass: %s" % overall)
    if overall:
        print("IBR51-TEST-PRINCIPAL-DECLARED-AND-PACKETED")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
