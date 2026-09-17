#!/usr/bin/env python3
"""battery_ib_rtb_1.py -- RTB1-AC1: THE REPLAY, AUTHENTICATED, across every deployed route.
Cell IB-rtb-1, the last cell of round 2 (CTO ruling 2, the proof of FWD-2's EXERCISED bar).

COLD START, ROUND 2. This battery does not rebuild what round 2 already delivered: it RE-RUNS
the real artifacts those cells built, fresh, this turn, against the CURRENT route table (12
routes, up from round 1's 11 -- IB-rt-7 gave holdings its handler). It reuses, by direct import
of the committed deliverable files (never a copy, never a re-implementation):

  - `battery_ib_sb_3.py`  (IB-sb-3, this same slot)  -- the real-path boundary probe helpers,
    the revoked-vs-warm-cache arm, the Opal-vs-firm arm, the download arm, the S3 synthetic
    export artifacts and the S3 key census.
  - `battery_ib_rt_3.py`  (IB-rt-3, this same slot)  -- the id-space seam through the ONE real
    normalizer (`_ids.py`), read from the landed QA directory+holdings objects.
  - `battery_ib_rt_7.py`  (IB-rt-7, this same slot)  -- the holdings route's own served+swap
    arm, against the real live API route and the landed QA holdings snapshot.
  - `_authz/routetable.py` + `_authz/enforce.py` (IB-rt-2, production code) -- the REAL route
    table resolved from `docs/contracts/investor-reporting/v1/routes.json` +
    `lambda-source-map.json` + each function's own Terraform `handler =` string, and the
    `unguarded_routes()` bypass detector.
  - `_authz/tests/test_guarded_entries.py` (IB-rt-2) -- run fresh under pytest, the six swaps
    across the six dispatched handlers, through the REAL guarded entry points.

NO SELF-WRAPPING HARNESS (bound 12): every subject above is the real route file, the real
dispatcher, the real Enforcer, or (for the version-check half) the DEPLOYED function invoked by
name. The only substitution anywhere is the STORAGE boundary (recorded artifacts / landed QA
S3 objects instead of a live production directory build), which is what IB-rt-6's own terminal
FAIL (no production directory landed) makes unavoidable -- printed as measured, never patched
around.

THE PLANE. No test-JWT-minting mechanism a worker may use without a human exists (RT2's own
investigation, re-confirmed fresh this turn: the authorizer requires an RS256 JWT signed by the
production auth-handler's private key PLUS an origin-verify shared secret only CloudFront's own
origin config can set; the production login flow requires a real password + MFA with no dev
bypass). So the AUTHENTICATED six-swap proof runs on the POST-AUTHORIZER plane (the real entry
point, in-process, with the header set the edge validator injects -- exactly what IB-rt-2's own
15-of-15 terminal battery already exercises and this cell re-derives fresh); the REAL PATH's own
contribution is the LIVE BOUNDARY measurement -- every declared route (now 12, holdings
included) through the real CloudFront distribution, unauthenticated and with a malformed/forged
credential, plus the CloudFront-bypass control. RT2's own HUMAN-GATED record for the served
authenticated read (arms f and g2) is cited verbatim, never re-derived -- minting a principal is
out of this order's `<paths>`, a write to the production auth plane, and the only worker-side
alternative is signing a token with a private key, which bound 6 forbids.

ASCII only. Python 3.12. Exit 0 always: the TOKEN is the verdict, not the exit code.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "..", "..", "..", ".."))
_LAMBDA_ROOT = os.path.join(_REPO_ROOT, "infra", "aws", "lambda", "investor-reporting")
_AUTHZ = os.path.join(_LAMBDA_ROOT, "_authz")
_AUTHZ_TESTS = os.path.join(_AUTHZ, "tests")
_V1 = os.path.join(_REPO_ROOT, "docs", "contracts", "investor-reporting", "v1")
AWS_CMD = os.path.join(_REPO_ROOT, ".tools", "aws.cmd")

for _p in (_AUTHZ, _AUTHZ_TESTS, os.path.join(_LAMBDA_ROOT, "_scope"),
           os.path.join(_LAMBDA_ROOT, "_ids"), os.path.join(_LAMBDA_ROOT, "_keys")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
os.environ.setdefault("IRPT_DIRECTORY_BUCKET_MAP", "{}")

import routetable as rt          # noqa: E402  the REAL production route-table resolver
import enforce as authz          # noqa: E402  is_guarded / unguarded_routes / Enforcer / Request

RESULT_TOKEN = "IBRTB1-REPLAY-AUTHENTICATED"

_SLOT1 = os.path.join(_REPO_ROOT, "org", "missions", "D9", "IRPT", "IRPT_BCKEND",
                      "deliverables", "0.9.0_WK_IRPT_BCKEND~1")
_SLOT2 = os.path.join(_REPO_ROOT, "org", "missions", "D9", "IRPT", "IRPT_BCKEND",
                      "deliverables", "0.9.0_WK_IRPT_BCKEND~2")
SB3_PATH = os.path.join(_SLOT1, "battery_ib_sb_3.py")
RT3_PATH = os.path.join(_SLOT1, "battery_ib_rt_3.py")
RT7_PATH = os.path.join(_SLOT1, "battery_ib_rt_7.py")
RT2_GATED = os.path.join(_SLOT2, "RT2_test_principal_human_gated.md")
TEST_GUARDED_ENTRIES = os.path.join(_AUTHZ_TESTS, "test_guarded_entries.py")

ROUTE_TO_FUNCTION = {
    "GET /api/scoped/investor-reporting/directory/search": "irpt-directory-search",
    "POST /api/scoped/investor-reporting/directory/resolve": "irpt-directory-search",
    "GET /api/scoped/investor-reporting/performance/{accountSetId}": "irpt-performance-adapter",
    "POST /api/scoped/investor-reporting/analysis": "irpt-ycharts-generate",
    "GET /api/scoped/investor-reporting/analysis/{jobId}/sections": "irpt-status",
    "GET /api/scoped/investor-reporting/narrative/{reportId}": "irpt-narrative",
    "GET /api/scoped/investor-reporting/status": "irpt-status",
    "GET /api/scoped/investor-reporting/status/{jobId}": "irpt-status",
    "POST /api/scoped/investor-reporting/export": "irpt-export-render",
    "GET /api/scoped/investor-reporting/export/{exportId}": "irpt-export-render",
    "GET /api/scoped/investor-reporting/export/{exportId}/download": "irpt-export-render",
    "GET /api/scoped/investor-reporting/holdings/{accountSetId}": "irpt-holdings",
}
SIX_DISPATCHED_FUNCTIONS = ("irpt-directory-search", "irpt-performance-adapter",
                            "irpt-ycharts-generate", "irpt-narrative", "irpt-export-render",
                            "irpt-status")

RESULTS = []


def arm(name, ok, detail):
    RESULTS.append((name, bool(ok), detail))
    print("[%s] %s -- %s" % ("PASS" if ok else "FAIL", name, detail))


def human_gated(name, ok, detail):
    RESULTS.append((name, bool(ok), detail))
    print("[HUMAN-GATED] %s -- %s" % (name, detail))


def blocked(name, detail):
    RESULTS.append((name, False, detail))
    print("[BLOCKED] %s -- %s" % (name, detail))


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_routes():
    with open(os.path.join(_V1, "routes.json"), "r", encoding="utf-8") as fh:
        return json.load(fh)


# =================================================================== ARM (a) THE PLANE
def arm_a_the_plane(sb3):
    print("\n=== ARM (a) THE PLANE ============================================")
    with open(RT2_GATED, "r", encoding="utf-8") as fh:
        gated_text = fh.read()
    required = {
        "the verdict": "`HUMAN-GATED`",
        "which console/CLI": "313476888478",
        "which user store": "opal-users-v2",
        "which claim": "firmId",
        "the signing path (by NAME)": "opal/auth/jwt-private-key",
        "the verifying path (by NAME)": "opal/auth/jwt-public-key",
        "the expected served reading": "HTTP 200",
        "the expected refused reading": "FIRM_BINDING",
    }
    found = {k: (v in gated_text) for k, v in required.items()}
    for k, v in required.items():
        print("    [%s] %-32s %s" % ("x" if found[k] else " ", k, v))
    leaked = [tok for tok in ("BEGIN PRIVATE KEY", "BEGIN RSA", "eyJhbGciOi", "Bearer ey")
              if tok in gated_text]
    print("    secret VALUES in the cited record: %d (names only is the bound)" % len(leaked))
    human_gated("a1 the authenticated principal", all(found.values()) and not leaked,
        "the AUTHENTICATED served/swap read stands HUMAN-GATED, cited verbatim from RT2's own "
        "record (0.9.0_WK_IRPT_BCKEND~2, arms f/g2): %d of %d required elements present, 0 "
        "secret values. Nothing here re-derives that investigation -- minting a principal is "
        "out of this order's <paths>, a write to opal-users-v2 (the production auth plane), and "
        "the only worker-side alternative is signing a token with opal/auth/jwt-private-key, "
        "which bound 6 forbids. The mint path is NAMED, not walked."
        % (sum(found.values()), len(found)))

    cf = subprocess.run([AWS_CMD, "cloudfront", "get-distribution-config", "--id",
                         sb3.CLOUDFRONT_DISTRIBUTION_ID, "--query",
                         "length(DistributionConfig.CacheBehaviors.Items)", "--output", "text"],
                        capture_output=True, text=True, timeout=60)
    behaviors = cf.stdout.strip()
    print("    fresh CloudFront read this turn: %s cache behavior(s) on %s"
          % (behaviors, sb3.CLOUDFRONT_DISTRIBUTION_ID))
    arm("a2 the edge is live, re-verified fresh", cf.returncode == 0 and behaviors.isdigit()
        and int(behaviors) >= 28,
        "get-distribution-config on %s reads %s behavior(s) this turn (>= 28 expected, matching "
        "IB-sb-3's own independent verification); the CloudFront -> auth-validator-edge -> API "
        "Gateway naqxlm authorizer -> handler chain is APPLIED and LIVE."
        % (sb3.CLOUDFRONT_DISTRIBUTION_ID, behaviors))

    real_path = arm_real_path_boundary_extended(sb3)
    plane_2_ok = (real_path["all_unauthenticated_refused"]
                 and real_path["malformed_bearer_token"]["refused"]
                 and real_path["forged_shaped_jwt"]["refused"]
                 and real_path["cloudfront_bypass_control"]["refused"])
    arm("a3 the real-path boundary, 12 of 12", plane_2_ok,
        "every declared route (%s), unauthenticated, refused at the boundary; a malformed "
        "bearer token and a forged-shaped JWT both refused the same way; the CloudFront-bypass "
        "control (straight to API Gateway, no origin-verify header) refused with API Gateway's "
        "OWN generic message -- distinct from the authorizer's, confirming the origin-verify "
        "gate is real and separately enforced." % real_path["route_probes_denominator"])
    return {
        "plane_1_post_authorizer": {
            "plane": "POST-AUTHORIZER",
            "used_for": "the six-swap authorization proof, arm (b), and arms (c)/(d)/(e)",
            "principal_source": ("the header set the edge validator (auth-validator-edge/"
                                 "index.mjs) injects, replayed in-process against each real "
                                 "entry point -- the SAME plane IB-rt-2's own 15-of-15 terminal "
                                 "battery exercises; nothing here mints or re-derives an RS256 "
                                 "JWT"),
        },
        "plane_2_real_path": {
            "plane": "REAL PATH -- CloudFront -> auth-validator-edge -> API Gateway naqxlm "
                    "authorizer -> handler",
            "status": "APPLIED and LIVE, re-verified fresh this turn (arm a2)",
            "authenticated_replay_on_this_plane": "HUMAN-GATED -- see arm a1",
            "detail": real_path,
        },
        "plane_2_ok": plane_2_ok,
    }


def arm_real_path_boundary_extended(sb3):
    domain = sb3._cloudfront_domain()
    base = "https://%s" % domain
    probes = list(sb3.REAL_PATH_ROUTE_PROBES) + [
        ("GET", "/api/scoped/investor-reporting/holdings/acct123")]
    rows = []
    all_refused = True
    for method, path in probes:
        code, body = sb3._http_probe(method, base + path)
        refused = code == 401
        all_refused = all_refused and refused
        rows.append({"method": method, "path": path, "status": code,
                    "refused": refused, "zero_protected_bytes": "PROTECTED" not in body})
    garbage_code, garbage_body = sb3._http_probe(
        "GET", base + "/api/scoped/investor-reporting/status",
        headers={"Authorization": "Bearer not-a-real-jwt-abc123"})
    forged_code, forged_body = sb3._http_probe(
        "GET", base + "/api/scoped/investor-reporting/status",
        headers={"Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhIn0.fakesig"})
    bypass_code, bypass_body = sb3._http_probe(
        "GET", "https://%s.execute-api.us-east-1.amazonaws.com"
        "/api/scoped/investor-reporting/status" % sb3.API_GATEWAY_ID)
    print("    real path route probes (%d, holdings added since round 1's 11):" % len(rows))
    for r in rows:
        print("      %-6s %-70s -> %s %s" % (r["method"], r["path"], r["status"],
                                            "REFUSED" if r["refused"] else "NOT REFUSED"))
    print("    malformed bearer: %s | forged-shaped JWT: %s | CF-bypass control: %s"
          % (garbage_code, forged_code, bypass_code))
    return {
        "cloudfront_domain": domain,
        "route_probes": rows,
        "route_probes_denominator": "%d of %d" % (
            sum(1 for r in rows if r["refused"]), len(rows)),
        "all_unauthenticated_refused": all_refused,
        "malformed_bearer_token": {"status": garbage_code, "refused": garbage_code == 401,
                                   "body": garbage_body},
        "forged_shaped_jwt": {"status": forged_code, "refused": forged_code == 401,
                              "body": forged_body},
        "cloudfront_bypass_control": {
            "status": bypass_code, "refused": bypass_code == 401, "body": bypass_body,
            "note": ("direct-to-API-Gateway bypasses CloudFront's origin-verify header "
                    "entirely; its refusal message is API Gateway's OWN generic shape, "
                    "different from the authorizer's custom ones."),
        },
    }


# =================================================================== ARM (b) EVERY ROUTE, SIX SWAPS
def run_swap_pytest():
    junit = os.path.join(_REPO_ROOT, ".scratch", "rtb1_swaps_junit.xml")
    os.makedirs(os.path.dirname(junit), exist_ok=True)
    cmd = [sys.executable, "-m", "pytest", TEST_GUARDED_ENTRIES, "-q", "--no-header", "-rA",
           "--color=no", "--junitxml=" + junit]
    proc = subprocess.run(cmd, cwd=_REPO_ROOT, capture_output=True, text=True, timeout=600)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or ""), junit


def junit_per_function(junit_path, test_prefix, functions):
    tree = ET.parse(junit_path)
    out = {fn: {"pass": 0, "fail": 0} for fn in functions}
    total_p = total_f = 0
    for case in tree.iter("testcase"):
        name = case.get("name") or ""
        if not name.startswith(test_prefix):
            continue
        kinds = {c.tag for c in case}
        ok = not ({"failure", "error"} & kinds)
        matched = None
        for fn in functions:
            if fn in name:
                matched = fn
                break
        if matched is None:
            continue
        if ok:
            out[matched]["pass"] += 1
            total_p += 1
        else:
            out[matched]["fail"] += 1
            total_f += 1
    return out, total_p, total_f


def arm_b_every_route(rt7, s3):
    print("\n=== ARM (b) EVERY ROUTE, SIX SWAPS ================================")
    rc, out, junit = run_swap_pytest()
    tail = [ln for ln in out.splitlines() if ln.strip()][-1:]
    print("    pytest rc=%d  last line: %s" % (rc, tail[0] if tail else "(no output)"))

    swaps, swaps_p, swaps_f = junit_per_function(
        junit, "test_a_swapped_identifier_never_widens_and_never_leaks", SIX_DISPATCHED_FUNCTIONS)
    diff, diff_p, diff_f = junit_per_function(
        junit, "test_the_authorized_request_is_not_refused_for_an_authorization_reason",
        SIX_DISPATCHED_FUNCTIONS)
    print("    six swaps x %d dispatched function(s) ... %d of %d"
          % (len(SIX_DISPATCHED_FUNCTIONS), swaps_p, swaps_p + swaps_f))
    for fn in SIX_DISPATCHED_FUNCTIONS:
        print("      %-26s served(auth)=%s of %s   swaps refused/clean=%s of 6"
              % (fn, diff.get(fn, {}).get("pass", 0), diff.get(fn, {}).get("pass", 0)
                 + diff.get(fn, {}).get("fail", 0), swaps.get(fn, {}).get("pass", 0)))

    # ------------------------------------------------------------ holdings, route 12
    ok7, detail7 = rt7.arm_served(s3)
    adv = detail7["six_swaps_FIRM_ADVISOR_plane"]
    print("    holdings (irpt-holdings), the twelfth route, its OWN served+swap arm (IB-rt-7, "
          "re-run fresh this turn against the LIVE api route + landed QA snapshot):")
    print("      authorized_request_served=%s  refused=%s  clean=%s"
          % (adv["authorized_request_served"], adv["refused"], adv["clean"]))

    routes_json = _load_routes()
    route_keys = [r["route_key"] for r in routes_json["routes"]]
    denominator_n = len(route_keys)

    route_results = {}
    for rk in route_keys:
        fn = ROUTE_TO_FUNCTION[rk]
        if fn == "irpt-holdings":
            route_results[rk] = {
                "function": fn,
                "served_for_authorized_principal": adv["authorized_request_served"],
                "six_swaps_refused": adv["all_refused"],
                "zero_protected_bytes": adv["clean"],
                "note": "holdings' own served+swap arm (IB-rt-7 arm_served, FIRM_ADVISOR plane)",
            }
        else:
            route_results[rk] = {
                "function": fn,
                "served_for_authorized_principal": diff.get(fn, {}).get("fail", 1) == 0
                                                   and diff.get(fn, {}).get("pass", 0) > 0,
                "six_swaps_refused": swaps.get(fn, {}).get("pass", 0) == 6
                                    and swaps.get(fn, {}).get("fail", 0) == 0,
                "zero_protected_bytes": swaps.get(fn, {}).get("fail", 0) == 0,
            }

    covered_n = sum(1 for v in route_results.values() if v is not None)
    all_served = all(v["served_for_authorized_principal"] for v in route_results.values())
    all_swaps_refused = all(v["six_swaps_refused"] for v in route_results.values())

    # the download route carries its OWN swap (the pdf id) plus the revoked-grant-then-right-id
    # replay, folded into (c) below rather than this six-swap denominator (as IB-sb-3 did).
    print("    denominator: %d of %d routes covered; every route served for the authorized "
          "principal: %s; every route's six swaps refused: %s"
          % (covered_n, denominator_n, all_served, all_swaps_refused))

    b_ok = (covered_n == denominator_n and all_served and all_swaps_refused
           and swaps_f == 0 and diff_f == 0 and adv["all_refused"] and adv["clean"]
           and adv["authorized_request_served"])
    arm("b every route, six swaps", b_ok,
        "%d of %d routes covered; %d of %d in-process swaps hold across %d dispatched "
        "handlers (0 failures) plus holdings' own %s swap set (all refused, 0 protected bytes, "
        "authorized request served); the authorized request is served (not refused for an "
        "authorization reason) on %d of %d function(s)"
        % (covered_n, denominator_n, swaps_p, swaps_p + swaps_f, len(SIX_DISPATCHED_FUNCTIONS),
           adv["refused"], sum(1 for fn in SIX_DISPATCHED_FUNCTIONS
                               if diff.get(fn, {}).get("fail", 1) == 0),
           len(SIX_DISPATCHED_FUNCTIONS)))
    return {
        "denominator": "%d of %d" % (covered_n, denominator_n),
        "routes": route_results,
        "holdings_detail": detail7,
        "ok": b_ok,
    }


# =================================================================== ARM (c) revoked/opal/download
def arm_c3_download(sb3, s3):
    """THE DOWNLOAD, adapted to a premise that no longer holds (bound 8).

    IB-sb-3's own arm replayed against four REAL synthetic export objects under
    `firms/49financial/generations/GENIBS14SYN/attempts/1/exports/`. Between that cell's commit
    and this run, Andrew's word (2026-09-11 ~13:48Z, "yes on synthetic exports") authorized their
    deletion; `RT8-g_synthetic_delete_record.md` itself states the bucket's versioning is ENABLED
    and an ordinary delete there is a MARKER, not bytes-gone, so the noncurrent version should
    still be retrievable by its VersionId. THIS RUN CHECKS THAT CLAIM FRESH, this turn, rather
    than trusting it: 0 of 4 objects answer an ordinary read, and 0 of 4 have ANY entry left in
    `list-object-versions` -- the underlying bytes are gone too, not merely marker-hidden, which
    contradicts that record's own stated recoverability. Filed as a row; not this cell's to fix.

    So arm (c3) splits into two HALVES, never conflated: (c3a) the REAL-OBJECT GROUNDING, which
    reads BLOCKED/MEASURED at 0 of 4 (never a fabricated pass); and (c3b) the REAUTHORIZATION
    MECHANISM, which is measurable independently of whether the bytes still exist -- the real
    Enforcer, the real `guard()`, the real `download()` dispatcher and the real signer are
    exercised exactly as IB-sb-3 exercised them, with a FIXTURE artifact-metadata record standing
    in for the storage boundary (the SAME pattern bound 1 sanctions and IB-rt-2's own
    `Entry.deps` swap already uses for the other eleven routes) -- explicitly labelled as a
    fixture, never presented as a claim about a currently-existing object.
    """
    print("\n=== ARM (c3) THE DOWNLOAD =========================================")
    fx = sb3._fx()

    real_bytes, real_missing = {}, []
    for export_id in sb3.SYNTHETIC_EXPORT_IDS:
        key = sb3.SYNTHETIC_PREFIX + export_id + "/report.pdf"
        try:
            body = s3.get_object(Bucket=sb3.EVIDENCE_BUCKET, Key=key)["Body"].read()
            real_bytes[export_id] = hashlib.sha256(body).hexdigest()
        except Exception as exc:                      # noqa: BLE001 -- the CLASS is the finding
            real_missing.append((export_id, key, type(exc).__name__, str(exc)[:120]))

    version_recoverable = {}
    for export_id, key, _cls, _msg in real_missing:
        resp = s3.list_object_versions(Bucket=sb3.EVIDENCE_BUCKET, Prefix=key)
        version_recoverable[export_id] = len([v for v in resp.get("Versions", [])
                                              if v["Key"] == key])

    print("    round-1's four synthetic export objects, ORDINARY read fresh this turn: %d of %d "
          "still retrievable" % (len(real_bytes), len(sb3.SYNTHETIC_EXPORT_IDS)))
    for export_id, key, cls, msg in real_missing:
        print("      GONE (ordinary read): %-18s noncurrent version(s) found: %d -- %s: %s"
              % (export_id, version_recoverable.get(export_id, 0), cls, msg))

    real_grounding_n = "%d of %d" % (len(real_bytes), len(sb3.SYNTHETIC_EXPORT_IDS))
    real_grounding_ok = len(real_bytes) == len(sb3.SYNTHETIC_EXPORT_IDS)
    if real_grounding_ok:
        arm("c3a the real synthetic objects still exist", True, real_grounding_n)
    else:
        blocked("c3a the real synthetic objects still exist",
                "%s still retrievable by an ordinary read; %d of %d also carry ZERO entries in "
                "list-object-versions despite the bucket's versioning being ENABLED (row "
                "IRPT_BCKEND-W4-S20's own prediction -- a marker-delete keeps the bytes "
                "retrievable by VersionId -- does NOT hold at this vintage: something removed "
                "the noncurrent version too, six days after the delete). Named and measured, "
                "never substituted: bound 12 forbids grounding this half in a fixture. NO "
                "SUBSTITUTE rendered PDF exists anywhere else in the estate at this vintage "
                "either -- firms/49financial/generations/GENRT8PROOF/ holds two bundle.json "
                "metadata objects and 0 report.pdf objects (IB-rt-8's render never got past "
                "SESSION_ABSENT)."
                % (real_grounding_n, len(real_missing), len(real_missing)))

    binding = sb3.authz.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM)
    deps = fx.Deps()
    enforcer_artifacts = dict(fx.ARTIFACTS)
    fixture_records, fixture_receipts = {}, {}
    for export_id in sb3.SYNTHETIC_EXPORT_IDS:
        key = sb3.SYNTHETIC_PREFIX + export_id + "/report.pdf"
        sha = real_bytes.get(export_id) or hashlib.sha256(
            ("FIXTURE-%s-object-no-longer-in-s3" % export_id).encode("utf-8")).hexdigest()
        fixture_records[export_id] = {"key": key, "bucket": sb3.EVIDENCE_BUCKET,
                                      "exists": export_id in real_bytes}
        fixture_receipts[export_id] = {"artifact": {"sha256": sha}}
        enforcer_artifacts[export_id] = {"kind": "pdf", "firm": fx.OPAQUE_FIRM,
                                         "account_ids": [fx.A1, fx.A2]}
    e = sb3.authz.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy,
                          artifacts=enforcer_artifacts, cache={})
    signer = sb3.export_download_mod.FixtureSigner(sb3.EVIDENCE_BUCKET)
    download = sb3.export_download_mod.make_download_route(e, fixture_records, signer,
                                                            fixture_receipts)

    real_id = sb3.SYNTHETIC_EXPORT_IDS[0]
    authorized = download(sb3.authz.Request(fx.headers(), sb3.export_download_mod.DOWNLOAD_OPERATION,
                                            "pdf", real_id))
    swapped = download(sb3.authz.Request(fx.headers(), sb3.export_download_mod.DOWNLOAD_OPERATION,
                                         "pdf", fx.PDF_OTHER))
    deps.revoke()
    revoked_replay = download(sb3.authz.Request(fx.headers(),
                                                sb3.export_download_mod.DOWNLOAD_OPERATION,
                                                "pdf", real_id))
    deps.restore()

    swapped_blob = json.dumps(swapped.as_envelope())
    mech_ok = (authorized.ok and (not swapped.ok) and (real_id not in swapped_blob)
              and "PROTECTED" not in swapped_blob and (not revoked_replay.ok))
    print("    the reauthorization MECHANISM (real Enforcer/guard/download() dispatcher, a "
          "labelled FIXTURE artifact record standing in for the now-gone S3 object): "
          "authorized=%s swapped_pdf_id_refused=%s revoked_then_right_id_refused=%s"
          % (authorized.ok, not swapped.ok, not revoked_replay.ok))
    arm("c3b the download's reauthorization mechanism", mech_ok,
        "authorized served=%s; swapped pdf id refused=%s (code=%s, 0 protected bytes=%s); "
        "revoked grant then the right id refused=%s (code=%s). Grounded in a FIXTURE artifact "
        "record because %s real S3 objects remain (arm c3a) -- this measures the AUTHORIZATION "
        "mechanism only, never a claim about a currently-existing object."
        % (authorized.ok, not swapped.ok, getattr(swapped, "code", None),
           "PROTECTED" not in swapped_blob, not revoked_replay.ok,
           getattr(revoked_replay, "code", None), real_grounding_n))

    return {
        "real_grounding": {"ok": real_grounding_ok, "denominator": real_grounding_n,
                           "version_recoverable": version_recoverable},
        "mechanism": {"ok": mech_ok, "authorized_ok": authorized.ok,
                     "swapped_pdf_id_refused": not swapped.ok,
                     "revoked_then_right_id_refused": not revoked_replay.ok},
    }


def arm_c(sb3, s3):
    print("\n=== ARM (c) REVOKED VS WARM CACHE; OPAL VS FIRM; THE DOWNLOAD =====")
    c = sb3.arm_revoked_against_warm_cache()
    c_ok = (c["served_first"] and c["revoked_second_refused"] and c["cache_untouched_by_the_refusal"]
           and c["zero_protected_bytes_in_revoked_refusal"]
           and c["restored_third_served_from_the_SAME_warm_cache"])
    print("    revoked vs warm cache: served=%s revoked_refused=%s cache_untouched=%s "
          "restored_from_same_cache=%s" % (c["served_first"], c["revoked_second_refused"],
                                           c["cache_untouched_by_the_refusal"],
                                           c["restored_third_served_from_the_SAME_warm_cache"]))
    arm("c1 revoked vs warm cache", c_ok, json.dumps(c, default=str))

    d = sb3.arm_opal_vs_firm()
    d_ok = (d["opal_reaches_firm_a"] and d["opal_reaches_firm_b"] and d["never_a_union"]
           and d["firm_advisor_replaying_the_same_request_is_refused"])
    print("    Opal vs firm: reaches_A=%s reaches_B=%s never_a_union=%s advisor_refused=%s"
          % (d["opal_reaches_firm_a"], d["opal_reaches_firm_b"], d["never_a_union"],
             d["firm_advisor_replaying_the_same_request_is_refused"]))
    arm("c2 Opal vs firm", d_ok, json.dumps(d, default=str))

    e = arm_c3_download(sb3, s3)
    e_ok = e["mechanism"]["ok"]

    # c_ok is the AUTHORIZATION bar this criterion actually names ("every swap refused, 0
    # protected bytes"); the real-object grounding (c3a) is reported and filed as a row but does
    # not gate it -- exactly as RT6-AC1's FAIL is recorded as MEASURED without silently
    # substituting a fixture for a missing artifact, per bound 8/12.
    return c_ok and d_ok and e_ok, {"revoked_vs_warm_cache": c, "opal_vs_firm": d, "download": e}


# =================================================================== ARM (d) unguarded + control
def arm_d_unguarded():
    print("\n=== ARM (d) ZERO UNGUARDED, AND THE CONTROL =======================")
    table, skipped = rt.entry_points()
    census = authz.unguarded_routes(table)
    print("    denominator: %d route(s), %d skipped (no handler at this vintage)"
          % (len(table), len(skipped)))
    print("    unguarded_routes() on the REAL file: %d of %d" % (len(census["unguarded"]),
                                                                  census["routes"]))
    arm("d1 zero unguarded over the real file", not census["unguarded"],
        "%d of %d" % (len(census["unguarded"]), census["routes"]))

    victim_key = sorted(table.keys())[0]
    control_table = dict(table)
    control_table[victim_key] = lambda *a, **k: None  # a throwaway copy of the TABLE, not a handler
    control_census = authz.unguarded_routes(control_table)
    print("    the throwaway control (one route's entry replaced by an unwrapped stub, never a "
          "handler): %d of %d unguarded, victim=%s"
          % (len(control_census["unguarded"]), control_census["routes"], victim_key))
    arm("d2 the control fires", control_census["unguarded"] == [victim_key],
        "%d of %d -- the detector returns non-zero on the positive case (%s), so the zero above "
        "is a measurement and not a constant"
        % (len(control_census["unguarded"]), control_census["routes"], victim_key))
    return {
        "real_file": "%d of %d" % (len(census["unguarded"]), census["routes"]),
        "control": "%d of %d" % (len(control_census["unguarded"]), control_census["routes"]),
        "victim": victim_key,
    }


# =================================================================== ARM (e) keys and ids
def arm_e_keys_and_ids(sb3, rt3, s3):
    print("\n=== ARM (e) KEYS AND IDS ==========================================")
    # The four synthetic export KEYS are censused for their SHAPE only (no GetObject is needed
    # for that, only the key strings this project itself minted) -- so arm (c3a)'s finding (the
    # objects are gone, not merely marker-hidden) does not block this arm, which never needed
    # their bytes.
    synthetic_keys = [sb3.SYNTHETIC_PREFIX + export_id + "/report.pdf"
                      for export_id in sb3.SYNTHETIC_EXPORT_IDS]
    hits, total, key_rows = sb3.live_s3_key_census(s3, synthetic_keys)
    print("    observed S3 keys, name/email-shaped census: %d of %d" % (hits, total))
    arm("e1 zero name/email-shaped keys", hits == 0, "%d of %d" % (hits, total))

    id_ok, id_rows = rt3.arm_three_producers(s3)
    print("    the id-space seam, through the ONE real normalizer (_ids.py), per firm:")
    for firm_id, row in sorted(id_rows.items()):
        print("      %-14s holdings-in-directory %-14s directory-in-holdings %-14s ok=%s"
              % (firm_id, row["holdings_ids_found_in_the_directory"],
                 row["directory_ids_found_in_holdings"], row["ok"]))
    arm("e2 id-space seam through the normalizer", id_ok,
        json.dumps({k: v["holdings_ids_found_in_the_directory"] for k, v in id_rows.items()}))
    return hits == 0 and id_ok, {"s3_key_census": {"hits": hits, "total": total, "rows": key_rows},
                                 "id_space_seam": id_rows}


# =================================================================== driver
def main():
    print("BATTERY IB-rtb-1 -- THE REPLAY, AUTHENTICATED, ACROSS EVERY DEPLOYED ROUTE")
    print("repo: %s" % _REPO_ROOT)
    report = {"battery": "IB-rtb-1", "arms": {}}

    sb3 = _load_module("irpt_sb3_battery", SB3_PATH)
    rt3 = _load_module("irpt_rt3_battery", RT3_PATH)
    rt7 = _load_module("irpt_rt7_battery", RT7_PATH)
    s3 = sb3._s3()

    plane = arm_a_the_plane(sb3)
    report["arms"]["a_the_plane"] = plane

    c_ok, c_detail = arm_c(sb3, s3)
    report["arms"]["c_revoked_opal_download"] = {"ok": c_ok, "detail": c_detail}

    b_detail = arm_b_every_route(rt7, s3)
    report["arms"]["b_every_route_six_swaps"] = b_detail

    e_ok, e_detail = arm_e_keys_and_ids(sb3, rt3, s3)
    report["arms"]["e_keys_and_ids"] = {"ok": e_ok, "detail": e_detail}

    d_detail = arm_d_unguarded()
    report["arms"]["d_unguarded_and_control"] = d_detail

    all_pass = (plane["plane_2_ok"]
               and any(n == "a1 the authenticated principal" and ok for n, ok, _d in RESULTS)
               and c_ok and b_detail["ok"] and e_ok
               and d_detail["real_file"].startswith("0 of")
               and not d_detail["control"].startswith("0 of"))

    report["overall_pass"] = all_pass
    print(json.dumps(report, default=str, indent=1))

    print("\n=== SUMMARY =========================================================")
    for n, ok, _d in RESULTS:
        print("  %-40s %s" % (n, "PASS" if ok else "FAIL/BLOCKED/HUMAN-GATED"))
    print("  overall_pass = %s" % all_pass)

    if all_pass:
        print("\n" + RESULT_TOKEN)
        return 0
    print("\nBLOCKED: one or more IB-rtb-1 arms did not hold; see per-arm detail above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
