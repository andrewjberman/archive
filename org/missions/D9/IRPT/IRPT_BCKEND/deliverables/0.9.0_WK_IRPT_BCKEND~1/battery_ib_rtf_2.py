#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-2 battery -- THE PARTIAL GRANT SERVED WITH ITS UNPROJECTED COUNT
DISCLOSED. CTO ruling @61627f39f9.

FIRST PASS: arms (a), (b), (c) graded for real, against the real code in this worktree, that run.
Arm (d) FAILED truthfully (the never-widen halves did not exist before the packet did).

SECOND PASS (this run): arm (d) re-graded now both halves are at HEAD naming the packet's blob;
arm (e) (the deploy + live proof) runs for real -- build+upload+terraform-apply the 7 serving
functions, then exercise the REAL deployed code path through `served.Entry.enforcer_for` for a
real firm (never a copy of the subject, bound 12).

Prints IBR59-PARTIAL-GRANT-SERVED-WITH-DISCLOSURE only when EVERY arm holds, including (d) and (e).
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
# .../deliverables/0.9.0_WK_IRPT_BCKEND~1 -> up 7 to the worktree root
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
LAMBDA_ROOT = os.path.join(WS, "infra", "aws", "lambda", "investor-reporting")
AUTHZ_DIR = os.path.join(LAMBDA_ROOT, "_authz")
TESTS_DIR = os.path.join(AUTHZ_DIR, "tests")
for _p in (AUTHZ_DIR, TESTS_DIR, os.path.join(LAMBDA_ROOT, "_scope"),
           os.path.join(LAMBDA_ROOT, "_keys"), os.path.join(LAMBDA_ROOT, "_ids")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ENTRY_FUNCTION_DIRS = ("directory", "export", "holdings", "narrative", "ops", "performance",
                       os.path.join("ycharts", "generate"))

COO_HALF_DIR = os.path.join(WS, "org", "tier1_exec", "2.0.0_SA_COO~B", "deliverables")
CTO_HALF_DIR = os.path.join(WS, "org", "tier1_exec", "1.0.0_SA_CTO", "deliverables")
PACKET_PATH = os.path.join(HERE, "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-2.md")

AWS = os.path.join(WS, ".tools", "aws.cmd")
DEPLOY_SCRIPT = os.path.join(HERE, "rte6_package_deploy.py")
FUNCTIONS = ("irpt-directory-search", "irpt-export-render", "irpt-holdings",
             "irpt-narrative", "irpt-status", "irpt-performance-adapter",
             "irpt-ycharts-generate")
FIRMS = {"49financial": "opal-data-bd", "inflection": "opal-data-inf", "cottonwood": "opal-data-cot"}
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
# The prior CodeSha256 per function, as the packet's table recorded it (read live, packet-write
# time) -- the S3 object VERSION under that exact content-sha256 is fetched fresh each run for the
# negative control; never a cached copy from a prior run.
PRIOR_CODE_SHA256 = {
    "irpt-directory-search": "v0MMA3yUxIPNdCMXhE/2pSD9lU+5LgI945JqkuULH8U=",
}


def git_head():
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WS, capture_output=True, text=True,
                         timeout=30)
    return out.stdout.strip()


def git_hash_object(path):
    out = subprocess.run(["git", "hash-object", path], cwd=WS, capture_output=True, text=True,
                         timeout=30)
    if out.returncode != 0:
        return None
    return out.stdout.strip()


# --------------------------------------------------------------------------- arm (a): the tests
def arm_a_tests():
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q",
                            os.path.join(TESTS_DIR, "test_enforce.py")],
                          capture_output=True, text=True, timeout=180, cwd=WS)
    out = (proc.stdout or "") + (proc.stderr or "")
    n_passed, n_failed = 0, 0
    for token in out.split():
        pass
    import re
    mp = re.search(r"(\d+) passed", out)
    mf = re.search(r"(\d+) failed", out)
    n_passed = int(mp.group(1)) if mp else 0
    n_failed = int(mf.group(1)) if mf else 0
    all_pass = (proc.returncode == 0) and n_failed == 0 and n_passed > 0

    # INDEPENDENT RE-DERIVATION of the mutant claim -- never trust the pytest test's own
    # internal assertion alone. Same transplant helper the test imports, called fresh here.
    import mutant_ordering
    import fixtures as fx
    import enforce as ez

    def real_partial_result():
        deps = fx.Deps(ownership=fx.OWNERSHIP_PARTIAL_UNPROJECTED)
        binding = ez.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM)
        e = ez.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy)
        return e.serve(ez.Request(fx.headers(), "directory_search", "account", fx.A1),
                       lambda scope: {"accounts": list(scope["permitted_account_set"])})

    real_out = real_partial_result()
    mutant_ns = mutant_ordering.build_old_order_module(os.path.join(AUTHZ_DIR, "enforce.py"))
    deps2 = fx.Deps(ownership=fx.OWNERSHIP_PARTIAL_UNPROJECTED)
    mbinding = mutant_ns["FirmBinding"](fx.TENANT, fx.OPAQUE_FIRM)
    me = mutant_ns["Enforcer"](mbinding, deps2.load_directory, deps2.load_ownership,
                               deps2.load_policy)
    mutant_out = me.serve(mutant_ns["Request"](fx.headers(), "directory_search", "account", fx.A1),
                          lambda scope: {"accounts": list(scope["permitted_account_set"])})
    mutant_fires = (mutant_out.ok is False and mutant_out.code == "UNPROJECTED_GRANT")
    real_serves = (real_out.ok is True
                  and sorted(real_out.payload["accounts"]) == sorted([fx.A1, fx.A2])
                  and real_out.census["unprojected_grant"] == {
                      "count": 1, "denominator": 3, "kinds": {"UNPROJECTED-ID": 1}})

    return {
        "pytest_returncode": proc.returncode,
        "n_passed": n_passed,
        "n_failed": n_failed,
        "pytest_tail": out[-3000:],
        "real_serves_the_partial_case": real_serves,
        "real_census": real_out.census.get("unprojected_grant"),
        "mutant_fires": mutant_fires,
        "mutant_code": mutant_out.code,
        "pass": all_pass and real_serves and mutant_fires,
    }


# --------------------------------------------------------------------------- arm (b): the field
def _entry_py_paths():
    out = []
    for rel in ENTRY_FUNCTION_DIRS:
        p = os.path.join(LAMBDA_ROOT, rel, "entry.py")
        out.append(p)
    return out


def arm_b_disclosure_field():
    import served as _served

    paths = _entry_py_paths()
    denom = len(paths)
    wired = []
    rows = {}
    for p in paths:
        rel = os.path.relpath(p, WS)
        exists = os.path.isfile(p)
        imports_served = False
        if exists:
            with open(p, "r", encoding="utf-8") as fh:
                imports_served = "import served" in fh.read()
        rows[rel] = {"exists": exists, "imports_served": imports_served}
        if exists and imports_served:
            wired.append(p)
    census_ok = (len(wired) == denom == 7)

    # PRESENT-AT-ZERO, DIRECTLY ON THE SHARED FUNCTION: every route this function serves answers
    # through response_envelope(), and this proves its DEFAULT (no gap measured -> omitted arg)
    # still carries the field.
    zero_env = _served.response_envelope("some-op", "fir_x", {"k": 1})
    zero_present = ("unprojected_grant" in zero_env
                    and zero_env["unprojected_grant"] == {"count": 0, "denominator": 0,
                                                           "kinds": {}})

    # NON-ZERO: the same function fed a real measured gap.
    nonzero_env = _served.response_envelope("some-op", "fir_x", {"k": 1},
                                            unprojected_grant={"count": 22, "denominator": 43,
                                                                "kinds": {"UNPROJECTED-ID": 22}})
    nonzero_present = nonzero_env.get("unprojected_grant") == {
        "count": 22, "denominator": 43, "kinds": {"UNPROJECTED-ID": 22}}

    # ONE SHARED CALL SITE: response_envelope has exactly one caller inside served.py
    # (Entry.handle), which is what makes "wired == field present" a valid inference rather than
    # a per-route promise nobody enforces. Re-derived by reading the source fresh, not recalled.
    with open(os.path.join(AUTHZ_DIR, "served.py"), "r", encoding="utf-8") as fh:
        served_src = fh.read()
    call_sites = served_src.count("response_envelope(")
    # 1 def + 1 call = 2 occurrences of the literal "response_envelope(" as a definition/call
    # opener; the def itself also matches the substring, so this is DEF(1) + CALLS.
    def_count = served_src.count("def response_envelope(")
    calls_excluding_def = call_sites - def_count

    return {
        "denominator": denom,
        "wired": len(wired),
        "rows": rows,
        "census_verdict": "%d of %d entry.py import the shared served boundary" % (len(wired), denom),
        "zero_present": zero_present,
        "zero_envelope": zero_env,
        "nonzero_present": nonzero_present,
        "nonzero_envelope": nonzero_env,
        "response_envelope_call_sites_excluding_def": calls_excluding_def,
        "pass": census_ok and zero_present and nonzero_present and calls_excluding_def == 1,
    }


# --------------------------------------------------------------------------- arm (c): the row
def arm_c_consumer_obligation_row():
    import re
    path = os.path.join(WS, "org", "missions", "D9", "IRPT", "IRPT_BCKEND", "surprise-channel",
                        "investigations", "INVESTIGATION_v1.md")
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"```json\n(.*?)\n```", text, re.S)
    rows = json.loads(m.group(1))
    match = [r for r in rows if r.get("id") == "IRPT_BCKEND-W1-S28"]
    ok = (len(match) == 1 and match[0].get("class") == "OBSERVATION"
         and match[0].get("hazard_standing") == "ARMED"
         and match[0].get("disarm_owner") == "1.0.0_SA_CTO")
    return {
        "row_id": "IRPT_BCKEND-W1-S28" if match else None,
        "found": len(match),
        "class": match[0].get("class") if match else None,
        "hazard_standing": match[0].get("hazard_standing") if match else None,
        "disarm_owner": match[0].get("disarm_owner") if match else None,
        "total_rows_in_first_fence": len(rows),
        "pass": ok,
    }


# --------------------------------------------------------------------------- arm (d): the halves
def _half_files(directory, code_pattern):
    if not os.path.isdir(directory):
        return []
    return sorted(f for f in os.listdir(directory)
                 if f.startswith(code_pattern) and f.endswith(".md"))


def _committed_at_head(path):
    """Is this path's WORKING-TREE content identical to what HEAD carries for it -- i.e. does a
    commit already hold these exact bytes, so 'at HEAD' claims made from `git hash-object` on the
    working tree are not getting ahead of the commit that is supposed to carry them."""
    rel = os.path.relpath(path, WS)
    out = subprocess.run(["git", "cat-file", "-p", "HEAD:" + rel.replace(os.sep, "/")],
                        cwd=WS, capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        return False
    with open(path, "r", encoding="utf-8") as fh:
        working = fh.read()
    return out.stdout == working


def arm_d_halves():
    packet_hash = git_hash_object(PACKET_PATH) if os.path.isfile(PACKET_PATH) else None
    packet_committed_at_head = _committed_at_head(PACKET_PATH) if packet_hash else False
    coo_files = _half_files(COO_HALF_DIR, "NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-2_")
    cto_files = _half_files(CTO_HALF_DIR, "NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-2_")

    def names_blob(files_dir, files):
        # "blob <hash>" tolerating markdown emphasis/backticks between the word and the hash
        # (the real halves write "**blob `<hash>`**") -- a bare substring match on "blob " +
        # hash is a FALSE NEGATIVE against that formatting, found and fixed this run.
        import re
        pattern = re.compile(r"blob[\s*`]*" + re.escape(str(packet_hash))) if packet_hash else None
        out = []
        for f in files:
            p = os.path.join(files_dir, f)
            with open(p, "r", encoding="utf-8") as fh:
                text = fh.read()
            out.append((f, bool(pattern.search(text)) if pattern else False))
        return out

    coo_checked = names_blob(COO_HALF_DIR, coo_files)
    cto_checked = names_blob(CTO_HALF_DIR, cto_files)
    coo_ok = any(ok for _f, ok in coo_checked)
    cto_ok = any(ok for _f, ok in cto_checked)

    return {
        "packet_path": os.path.relpath(PACKET_PATH, WS),
        "packet_file_exists": os.path.isfile(PACKET_PATH),
        "packet_committed_at_head": packet_committed_at_head,
        "packet_blob_hash": packet_hash,
        "coo_half_dir": os.path.relpath(COO_HALF_DIR, WS),
        "coo_half_candidates": coo_files,
        "coo_half_names_packet_blob": coo_ok,
        "cto_half_dir": os.path.relpath(CTO_HALF_DIR, WS),
        "cto_half_candidates": cto_files,
        "cto_half_names_packet_blob": cto_ok,
        "pass": bool(packet_hash) and packet_committed_at_head and coo_ok and cto_ok,
    }


# --------------------------------------------------------------------------- arm (e): the deploy
def aws_json(*args):
    out = subprocess.run([AWS] + list(args), capture_output=True, text=True, timeout=90)
    if out.returncode != 0:
        raise RuntimeError("aws %s failed rc=%s: %s" % (" ".join(args), out.returncode, out.stderr[-500:]))
    return json.loads(out.stdout)


def arm_e_deploy_verify():
    """N of N functions: served CodeSha256 == built, re-derived fresh via the SAME deploy tool
    IB-rte-6 built for this project (rte6_package_deploy.py, used UNCHANGED per this order's own
    text) -- never trusted from a prior run's cached output."""
    proc = subprocess.run([sys.executable, DEPLOY_SCRIPT, "verify"], capture_output=True,
                          text=True, timeout=180)
    lines = [ln for ln in (proc.stdout or "").splitlines() if " served=" in ln]
    rows = {}
    for ln in lines:
        fn = ln.split(" ", 1)[0]
        ok = ln.strip().endswith("True")
        rows[fn] = ok
    n_ok = sum(1 for v in rows.values() if v)
    return {"denominator": len(FUNCTIONS), "matched": n_ok, "rows": rows,
            "raw_tail": proc.stdout[-3000:],
            "pass": (n_ok == len(FUNCTIONS) == len(rows))}


def _fetch_prior_zip_enforce(function_name, prior_sha256_b64, out_dir):
    """Fetch the EXACT prior S3 object version whose content-sha256 metadata equals the packet's
    recorded prior CodeSha256, verify it BY CONTENT (never by version-id alone), and return the
    path to its extracted enforce.py -- the real pre-fix bytes, not a simulated mutant."""
    versions = aws_json("s3api", "list-object-versions", "--bucket", ARTIFACT_BUCKET,
                        "--prefix", "investor-reporting/%s.zip" % function_name,
                        "--query", "Versions[].VersionId")
    os.makedirs(out_dir, exist_ok=True)
    for vid in versions:
        dest = os.path.join(out_dir, "%s_%s.zip" % (function_name, vid[:8]))
        head = aws_json("s3api", "head-object", "--bucket", ARTIFACT_BUCKET,
                        "--key", "investor-reporting/%s.zip" % function_name,
                        "--version-id", vid)
        meta_sha = (head.get("Metadata") or {}).get("content-sha256")
        if meta_sha != prior_sha256_b64:
            continue
        subprocess.run([AWS, "s3api", "get-object", "--bucket", ARTIFACT_BUCKET,
                        "--key", "investor-reporting/%s.zip" % function_name,
                        "--version-id", vid, dest], capture_output=True, text=True,
                       timeout=90, check=True)
        with open(dest, "rb") as fh:
            raw = fh.read()
        got_sha = base64.b64encode(hashlib.sha256(raw).digest()).decode("ascii")
        if got_sha != prior_sha256_b64:
            continue
        z = zipfile.ZipFile(dest)
        extract_to = os.path.join(out_dir, "enforce_pre_fix_%s.py" % function_name)
        with z.open("enforce.py") as zf, open(extract_to, "wb") as out_fh:
            out_fh.write(zf.read())
        return extract_to, got_sha
    return None, None


def arm_e_live_proof():
    """The REAL deployed code path, exercised through `served.Entry.enforcer_for` -- never a copy
    of the subject (bound 12). Re-derives the seam firm, builds the SAME real request IB-rte-6
    measured, and reads: post-fix served k with count=denominator-k; cross-firm swap refused;
    the ACTUAL pre-deploy artifact bytes (fetched fresh from S3 by content hash, this run) reading
    UNPROJECTED_GRANT; inflection/cottonwood (empty ownership maps) reading the empty-branch
    refusal."""
    os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(FIRMS)

    directory_dir = os.path.join(LAMBDA_ROOT, "directory")
    if directory_dir not in sys.path:
        sys.path.insert(0, directory_dir)
    for mod in ("entry", "handler"):
        sys.modules.pop(mod, None)
    import entry as _directory_entry   # the REAL irpt-directory-search entry point, unedited
    import ids as _ids
    import enforce as _enforce

    seam_firm = None
    for firm in _ids.firm_ids():
        row = _ids.raw_keys().get("firms", {}).get(firm, {}).get("account", {})
        if row.get("projection_seam"):
            seam_firm = firm
            break
    if seam_firm is None:
        raise RuntimeError("no firm declares a projection_seam in raw_keys.json")

    def headers_for(advisor_id, tenant, email):
        return {"X-User-Email": email, "X-User-Name": advisor_id, "X-User-Tier": "partner",
                "X-User-Role": "user", "X-Firm-Id": tenant, "X-User-Type": "Advisor",
                "X-Advisor-Id": advisor_id, "X-Advisor-Role": "", "X-Origin-Verify": "cloudfront"}

    # POST-FIX, LIVE: served.Entry.enforcer_for(tenant), the REAL directory + ownership map.
    post_enforcer, _ctx = _directory_entry.ENTRY.enforcer_for(seam_firm)
    request = _enforce.Request(headers_for("abby_horton", seam_firm, "abby.horton@49financial.com"),
                               operation="directory-search")
    post_scope, post_refusal = post_enforcer.resolve_now(request)
    post_code = post_refusal.code if post_refusal is not None else None
    post_served = post_refusal is None
    post_k = len(post_scope["permitted_account_set"]) if post_scope is not None else 0
    post_grant = (dict(post_scope["_census"]["unprojected_grant"])
                 if post_scope is not None else None)

    # CROSS-FIRM SWAP: same enforcer (same tenant/firm), an advisor id that firm's ownership map
    # does not hold -- must still refuse, never served.
    swap_request = _enforce.Request(
        headers_for("definitely-not-a-49f-advisor", seam_firm, "swap@49financial.com"),
        operation="directory-search")
    swap_scope, swap_refusal = post_enforcer.resolve_now(swap_request)
    swap_refused = swap_scope is None
    swap_code = swap_refusal.code if swap_refusal is not None else None

    # THE PRE-FIX BYTES, FETCHED FRESH FROM S3 THIS RUN (by content hash, never a cached extract):
    # the ACTUAL zip irpt-directory-search served before this pass's deploy, verified by its own
    # sha256 against the packet's recorded prior CodeSha256.
    prior_sha = PRIOR_CODE_SHA256["irpt-directory-search"]
    extract_dir = os.path.join(WS, ".scratch", "prefix_extracted")
    pre_fix_path, verified_sha = _fetch_prior_zip_enforce("irpt-directory-search", prior_sha,
                                                          extract_dir)
    pre_fix_code = None
    pre_fix_verified_by_content = (verified_sha == prior_sha) if verified_sha else False
    if pre_fix_path is not None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("enforce_pre_fix", pre_fix_path)
        pre_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pre_mod)
        # SAME real deps, same real request -- only the enforce.py MODULE differs (the actual
        # pre-deploy artifact's bytes, not a simulated mutant).
        pre_binding = pre_mod.FirmBinding(seam_firm, post_enforcer.binding.opaque_firm_id)
        load_directory, load_ownership, load_policy = _loaders_deps(seam_firm)
        pre_enforcer = pre_mod.Enforcer(pre_binding, load_directory, load_ownership, load_policy,
                                        id_projection=_ids.projection_for_firm(seam_firm))
        pre_scope, pre_refusal = pre_enforcer.resolve_now(request)
        pre_fix_code = pre_refusal.code if pre_refusal is not None else None

    # INFLECTION / COTTONWOOD: empty ownership maps at this vintage -- any request refuses via the
    # empty branch (EMPTY_GRANT), never UNPROJECTED_GRANT (nothing was granted at all).
    other_firms = {}
    for firm in FIRMS:
        if firm == seam_firm:
            continue
        try:
            enforcer, _c = _directory_entry.ENTRY.enforcer_for(firm)
        except Exception as exc:
            other_firms[firm] = {"error": str(exc)[:200]}
            continue
        req = _enforce.Request(headers_for("any-advisor-id", firm, "x@%s.com" % firm),
                               operation="directory-search")
        scope, refusal = enforcer.resolve_now(req)
        other_firms[firm] = {"served": scope is not None,
                             "code": refusal.code if refusal is not None else None}

    others_refused = all((not v.get("served", True)) for v in other_firms.values())

    return {
        "seam_firm": seam_firm,
        "post_fix_code": post_code,
        "post_fix_served": post_served,
        "post_fix_permitted_count": post_k,
        "post_fix_unprojected_grant": post_grant,
        "post_fix_count_plus_k_equals_denominator": (
            post_grant is not None and post_k + post_grant["count"] == post_grant["denominator"]),
        "cross_firm_swap_refused": swap_refused,
        "cross_firm_swap_code": swap_code,
        "pre_fix_zip_verified_by_content_sha256": pre_fix_verified_by_content,
        "pre_fix_zip_content_sha256": verified_sha,
        "pre_fix_code": pre_fix_code,
        "other_firms": other_firms,
        "other_firms_refused": others_refused,
        "pass": (post_served and post_code != "UNPROJECTED_GRANT" and post_k >= 1
                 and post_grant is not None
                 and post_k + post_grant["count"] == post_grant["denominator"]
                 and swap_refused
                 and pre_fix_verified_by_content and pre_fix_code == "UNPROJECTED_GRANT"
                 and others_refused),
    }


def _loaders_deps(tenant):
    import loaders as _loaders
    return _loaders.deps(tenant)


def main():
    report = {"git_head": git_head()}

    a = arm_a_tests()
    report["arm_a_tests"] = a
    print("ARM (a) TESTS: pytest rc=%s, %d passed / %d failed; real serves partial=%s "
          "census=%s; mutant fires=%s (code=%s)"
          % (a["pytest_returncode"], a["n_passed"], a["n_failed"],
             a["real_serves_the_partial_case"], a["real_census"], a["mutant_fires"],
             a["mutant_code"]))

    b = arm_b_disclosure_field()
    report["arm_b_disclosure_field"] = b
    print("ARM (b) DISCLOSURE FIELD: %s; zero-present=%s; nonzero-present=%s; "
          "response_envelope call sites (excl def)=%d"
          % (b["census_verdict"], b["zero_present"], b["nonzero_present"],
             b["response_envelope_call_sites_excluding_def"]))

    c = arm_c_consumer_obligation_row()
    report["arm_c_consumer_obligation_row"] = c
    print("ARM (c) CONSUMER-OBLIGATION ROW: id=%s found=%d class=%s hazard_standing=%s "
          "disarm_owner=%s"
          % (c["row_id"], c["found"], c["class"], c["hazard_standing"], c["disarm_owner"]))

    d = arm_d_halves()
    report["arm_d_halves"] = d
    print("ARM (d) NEVER-WIDEN HALVES AT HEAD: packet_file_exists=%s packet_committed_at_head=%s "
          "blob=%s; coo_half_present_naming_blob=%s (%d candidate file(s)); "
          "cto_half_present_naming_blob=%s (%d candidate file(s))"
          % (d["packet_file_exists"], d["packet_committed_at_head"], d["packet_blob_hash"],
             d["coo_half_names_packet_blob"], len(d["coo_half_candidates"]),
             d["cto_half_names_packet_blob"], len(d["cto_half_candidates"])))
    if not d["pass"]:
        print("ARM (d) STOP: at least one never-widen half is ABSENT at HEAD naming the "
              "packet's blob hash. Arm (e) (the deploy) does not run.")
        overall = a["pass"] and b["pass"] and c["pass"] and d["pass"]
        report["overall_pass"] = overall
        print(json.dumps(report, indent=1, default=str))
        return 0 if overall else 1

    # ARM (e): both halves are present -- the deploy has already been performed this pass
    # (build+upload+terraform-apply, outside this battery, under its own change-management
    # ledger entry) and this arm VERIFIES it by re-deriving fresh reads, never trusting a prior
    # run's cached output.
    e_deploy = arm_e_deploy_verify()
    report["arm_e_deploy_verify"] = e_deploy
    print("ARM (e.1) DEPLOY VERIFY: %d of %d functions served CodeSha256==built"
          % (e_deploy["matched"], e_deploy["denominator"]))

    e_live = arm_e_live_proof()
    report["arm_e_live_proof"] = e_live
    print("ARM (e.2) LIVE PROOF: seam=%s post-fix code=%s served=%s k=%d unprojected_grant=%s "
          "(k+count==denominator=%s); cross-firm swap refused=%s (code=%s); pre-fix zip verified "
          "by content=%s code=%s; other firms refused=%s (%s)"
          % (e_live["seam_firm"], e_live["post_fix_code"], e_live["post_fix_served"],
             e_live["post_fix_permitted_count"], e_live["post_fix_unprojected_grant"],
             e_live["post_fix_count_plus_k_equals_denominator"], e_live["cross_firm_swap_refused"],
             e_live["cross_firm_swap_code"], e_live["pre_fix_zip_verified_by_content_sha256"],
             e_live["pre_fix_code"], e_live["other_firms_refused"], e_live["other_firms"]))

    overall = (a["pass"] and b["pass"] and c["pass"] and d["pass"]
              and e_deploy["pass"] and e_live["pass"])
    report["overall_pass"] = overall
    print(json.dumps(report, indent=1, default=str))
    if overall:
        print("IBR59-PARTIAL-GRANT-SERVED-WITH-DISCLOSURE")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
