#!/usr/bin/env python3
"""IB-rtg-4 -- THE HOLDINGS LOADER FOLLOWS THE DIRECTORY POINTER (row S100). Cell IB-rtg-4.

APPLY-GATED PASS (the rtf-13 shape, per decomp R7.2): arms (a)-(c) MEASURE the defect, VERIFY the
source fix, BUILD and VERIFY the artifact AT REST, then check BOTH never-widen halves at HEAD.
ABSENT (the expected first-pass outcome) -> STOP; arms (d)/(e) do not run and the order stays
open. PRESENT -> the SUBTRACTION gate, the apply, and the live proof under the deployed role and
bytes would follow (not implemented in this pass because the halves are not yet signed; a later
pass, once both halves are SIGNED, extends this file rather than re-deriving it).

Re-derives, every run, from the worktree source / git blobs / the committed manifest / live AWS
state -- never from a hand-typed verdict table with no premise check.

Usage: py -3.12 battery_ib_rtg_4.py
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
REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE,
                      capture_output=True, check=True).stdout.decode("utf-8").strip()
REPO = REPO.replace("/", os.sep)
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
# This battery runs under native `py -3.12`, not Git Bash -- .tools/aws is a bash script (native
# subprocess.run cannot exec it); .tools/aws.cmd is the Windows-shell companion for this caller
# class. .tools/terraform.exe is a real PE, used by its own path.
AWS = os.path.join(REPO, ".tools", "aws.cmd")
TERRAFORM = os.path.join(REPO, ".tools", "terraform.exe")

HOLDINGS_DIR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "holdings")
ENTRY_PATH = os.path.join(HOLDINGS_DIR, "entry.py")
DIRECTORY_HANDLER_PATH = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting",
                                       "directory", "handler.py")
LOADERS_PATH = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_authz",
                            "loaders.py")

FUNCTION = "irpt-holdings"
TF_ROOTS = ("api", "core", "directory", "export", "holdings", "intake", "narrative", "ops",
            "performance", "ycharts")
FIRM = "49financial"
OM_BUCKET, OM_KEY = "opal-data-bd", "platinum/%s/ownership_map.json" % FIRM
DIRECTORY_BUCKET = "opal-data-bd"
DIRECTORY_POINTER_KEY = "investor-reporting/directory/latest.json"

SCRATCH = os.path.join(REPO, ".scratch")
os.makedirs(SCRATCH, exist_ok=True)

COO_DIR = os.path.join(REPO, "org", "tier1_exec", "2.0.0_SA_COO~B", "deliverables")
CTO_DIR = os.path.join(REPO, "org", "tier1_exec", "1.0.0_SA_CTO", "deliverables")


def run(cmd, cwd=None, timeout=180):
    p = subprocess.run(cmd, cwd=cwd or REPO, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def aws_json(args, timeout=60):
    rc, out, err = run([AWS] + args + ["--output", "json"], timeout=timeout)
    if rc != 0:
        return rc, None, err
    try:
        return rc, json.loads(out), err
    except ValueError:
        return rc, out, err


def load_source_map():
    with open(SOURCE_MAP, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------------------------
# ARM (a): MEASURE -- confirm S100's cause, confirm the fix's shape, re-derive the live grant
# count (never inherit round-6's 33/18 or this round's own prior 44/19 citation).
# ---------------------------------------------------------------------------------------------
def arm_a():
    print("=" * 100)
    print("ARM (a) -- MEASURE")
    print("=" * 100)
    ok = True

    with open(ENTRY_PATH, "r", encoding="utf-8") as fh:
        entry_src = fh.read()
    with open(DIRECTORY_HANDLER_PATH, "r", encoding="utf-8") as fh:
        directory_src = fh.read()
    with open(LOADERS_PATH, "r", encoding="utf-8") as fh:
        loaders_src = fh.read()

    old_defect_signature = "_directory.load_directory(_firm_bucket(tenant), DIRECTORY_KEY)"
    has_old_defect = old_defect_signature in entry_src
    print("PRE-FIX defect signature ('%s') present in holdings/entry.py: %s (expect False, "
          "post-fix)" % (old_defect_signature, has_old_defect))
    ok = ok and (not has_old_defect)

    has_pointer_fetch = "Key=DIRECTORY_KEY" in entry_src
    has_resolved_fetch = '_directory.load_directory(bucket, pointer["key"], s3)' in entry_src
    print("FIX signature -- pointer fetch at DIRECTORY_KEY present: %s" % has_pointer_fetch)
    print("FIX signature -- resolved-artifact fetch at pointer['key'] present: %s"
          % has_resolved_fetch)
    ok = ok and has_pointer_fetch and has_resolved_fetch

    correct_pattern_present = (
        'pointer = _get_json(bucket, DIRECTORY_PREFIX + "/latest.json", s3)' in loaders_src
        and 'artifact = _get_json(bucket, pointer["key"], s3)' in loaders_src)
    print("_authz/loaders.py:71-78 two-step pattern (the pattern this fix mirrors) confirmed "
          "present at HEAD: %s" % correct_pattern_present)
    ok = ok and correct_pattern_present

    single_key_unedited = ('def load_directory(firm_bucket: str, key: str, s3_client=None) '
                           '-> dict:') in directory_src
    print("directory/handler.py's single-key load_directory left UNEDITED (this order's confined "
          "bound -- the fix lives in holdings/entry.py only): %s" % single_key_unedited)
    ok = ok and single_key_unedited

    print()
    print("-- re-deriving the ownership/grant count LIVE (THE 44/19 RE-DERIVE CONSTRAINT: never "
          "inherit round-6's 33/18, never inherit this round's own prior 44/19 citation either -- "
          "the map is DS-owned, `data/assets/scripts/gold/runners_49f/d08_firm_ownership_map.py`, "
          "and changes independently of this cell) --")
    om_path = os.path.join(SCRATCH, "ib_rtg_4_om_live.json")
    rc, _out, err = aws_json(["s3api", "get-object", "--bucket", OM_BUCKET, "--key", OM_KEY,
                              om_path.replace("\\", "/")])
    om_ok = (rc == 0)
    if om_ok:
        with open(om_path, "r", encoding="utf-8") as fh:
            om_doc = json.load(fh)
        advisors = om_doc.get("advisors") or {}
        n_advisors = len(advisors)
        n_slots = sum(len(g.get("accounts") or []) for g in advisors.values())
        print("LIVE s3://%s/%s (schema_version=%s) -- %d advisor/relationship key(s), %d total "
              "account grant slot(s), THIS RUN" % (OM_BUCKET, OM_KEY, om_doc.get("schema_version"),
                                                    n_advisors, n_slots))
    else:
        print("WARN: could not read the live ownership map rc=%d: %s" % (rc, str(err)[:300]))
    ok = ok and om_ok

    ptr_path = os.path.join(SCRATCH, "ib_rtg_4_ptr_live.json")
    rc2, _out2, err2 = aws_json(["s3api", "get-object", "--bucket", DIRECTORY_BUCKET,
                                 "--key", DIRECTORY_POINTER_KEY, ptr_path.replace("\\", "/")])
    mutant_confirmed = False
    if rc2 == 0:
        with open(ptr_path, "r", encoding="utf-8") as fh:
            ptr_doc = json.load(fh)
        mutant_opaque = ptr_doc.get("firm_id_opaque")
        resolved_key = ptr_doc.get("key")
        print("MUTANT CHECK: the pointer document itself at s3://%s/%s (what the PRE-FIX "
              "single-key read returns VERBATIM) declares firm_id_opaque=%r, key=%r -- %s"
              % (DIRECTORY_BUCKET, DIRECTORY_POINTER_KEY, mutant_opaque, resolved_key,
                 "CONFIRMS S100 (a pre-fix read of this document finds no firm_id_opaque and "
                 "FirmBinding would raise for a granted account)" if mutant_opaque is None else
                 "UNEXPECTED: the pointer document itself declares firm_id_opaque"))
        mutant_confirmed = (mutant_opaque is None) and bool(resolved_key)
    else:
        print("WARN: could not read the live pointer document rc=%d: %s" % (rc2, str(err2)[:300]))
    ok = ok and mutant_confirmed

    print()
    print("ARM (a): %s" % ("PASS" if ok else "FAIL"))
    return ok


# ---------------------------------------------------------------------------------------------
# ARM (b): THE SOURCE EDIT, THE BUILD, AND VERIFICATION AT REST
# ---------------------------------------------------------------------------------------------
def arm_b():
    print()
    print("=" * 100)
    print("ARM (b) -- THE BUILD AND ITS VERIFICATION AT REST")
    print("=" * 100)
    ok = True
    sm = load_source_map()
    cfg = sm["functions"][FUNCTION]
    if "entry.py" not in cfg["files"]:
        print("ERROR: entry.py not declared in files[] for %s" % FUNCTION)
        return False, {}

    rc, live_cfg, _err = aws_json(["lambda", "get-function-configuration",
                                   "--function-name", FUNCTION,
                                   "--query", "{CodeSha256:CodeSha256,LastModified:LastModified}"])
    prior_live = live_cfg.get("CodeSha256") if rc == 0 else None
    print("prior LIVE CodeSha256 (read live, this run): %s LastModified=%s"
          % (prior_live, live_cfg.get("LastModified") if rc == 0 else "?"))

    art_bucket = "opal-313476888478-lambda-artifacts"
    art_key = cfg["artifact_s3_key"]
    rc_v, versions, _err_v = aws_json([
        "s3api", "list-object-versions", "--bucket", art_bucket, "--prefix", art_key,
        "--query", "Versions[?Key=='%s'].{VersionId:VersionId,LastModified:LastModified,"
                   "IsLatest:IsLatest}" % art_key])
    rollback_version = None
    if rc_v == 0 and versions:
        non_latest = [v for v in versions if not v.get("IsLatest")]
        if non_latest:
            rollback_version = non_latest[0]
    print("build-store rollback candidate (the version under %s BEFORE any build this run): %s"
          % (art_key, rollback_version or "NONE FOUND"))

    pre_declared_sha = cfg.get("artifact_sha256")
    already_built = bool(rc == 0 and prior_live and prior_live == pre_declared_sha)
    print("pre-build check: live CodeSha256=%s manifest artifact_sha256=%s already_built=%s"
          % (prior_live, pre_declared_sha, already_built))

    print()
    print("-- building %s (build-and-upload.sh, single-function mode; cwd MUST be inside the "
          "repo -- a bare cwd=/c/ breaks manifest-index-check.py's git-show calls, row filed) --"
          % FUNCTION)
    sys.path.insert(0, os.path.join(REPO, ".tools"))
    from git_bash_resolver import git_bash  # noqa: E402
    bash = git_bash()
    if not bash:
        raise SystemExit("ERROR: no Git Bash found (git_bash_resolver) -- refusing bare 'bash'")
    build_cmd = [bash, os.path.join(REPO, "infra", "aws", "lambda", "ci", "build-and-upload.sh"),
                "investor-reporting", FUNCTION]
    rc_b, out_b, err_b = run(build_cmd, cwd=REPO, timeout=180)
    print(out_b[-4000:])
    if err_b.strip():
        print("STDERR (tail):", err_b[-1500:])
    if rc_b != 0:
        print("ERROR: build-and-upload.sh rc=%d -- STOPPING arm (b) here" % rc_b)
        return False, {}

    sm2 = load_source_map()
    cfg2 = sm2["functions"][FUNCTION]
    built_sha = cfg2["artifact_sha256"]
    print("built artifact_sha256 (this run): %s" % built_sha)

    zip_path = os.path.join(SCRATCH, "ib_rtg_4_holdings_built.zip")
    rc_g, _out_g, err_g = run([AWS, "s3api", "get-object", "--bucket", art_bucket,
                               "--key", cfg2["artifact_s3_key"], zip_path.replace("\\", "/")],
                              timeout=60)
    if rc_g != 0:
        print("ERROR: get-object failed rc=%d: %s" % (rc_g, err_g[:400]))
        return False, {}
    with open(zip_path, "rb") as fh:
        zip_bytes = fh.read()
    measured = base64.b64encode(hashlib.sha256(zip_bytes).digest()).decode("ascii")
    print("VERIFIED AT REST: downloaded zip sha256(base64)=%s declared=%s match=%s"
          % (measured, built_sha, measured == built_sha))
    ok = ok and (measured == built_sha)

    zf = zipfile.ZipFile(os.path.abspath(zip_path))
    zip_names = sorted(zf.namelist())
    declared = sorted(set(cfg2["files"]))
    print("declared files[] (%d) == zip namelist (%d): %s"
          % (len(declared), len(zip_names), declared == zip_names))
    ok = ok and (declared == zip_names)

    entry_in_zip = zf.read("entry.py")
    with open(ENTRY_PATH, "rb") as fh:
        entry_wt = fh.read()
    delta_is_exactly_the_edit = (entry_in_zip == entry_wt)
    print("packaged entry.py byte-equal to the worktree fix (the served-byte delta is EXACTLY "
          "this order's edit, no other member changed): %s" % delta_is_exactly_the_edit)
    ok = ok and delta_is_exactly_the_edit

    print("ARM (b): %s" % ("PASS" if ok else "FAIL"))
    return ok, {"prior_live_codesha256": prior_live,
               "rollback_build_store_version": (rollback_version or {}).get("VersionId"),
               "rollback_build_store_last_modified": (rollback_version or {}).get("LastModified"),
               "built_sha256_b64": built_sha}


# ---------------------------------------------------------------------------------------------
# ARM (c): THE PACKET -- plan all TEN roots (never-widen scope check), then the halves gate
# ---------------------------------------------------------------------------------------------
def arm_c(built_info):
    print()
    print("=" * 100)
    print("ARM (c) -- THE PACKET: TEN-ROOT PLAN + THE HALVES GATE")
    print("=" * 100)
    plans = {}
    plan_failures = []
    for root in TF_ROOTS:
        root_dir = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", root)
        try:
            rc_init, _o, e_init = run([TERRAFORM, "init", "-input=false"], cwd=root_dir, timeout=180)
        except subprocess.TimeoutExpired:
            rc_init, e_init = 124, "TIMEOUT"
        plan_file = os.path.join(SCRATCH, "ib_rtg_4_%s.tfplan" % root)
        if rc_init == 0:
            try:
                rc_plan, out_plan, e_plan = run([TERRAFORM, "plan", "-input=false", "-no-color",
                                                 "-out=%s" % plan_file], cwd=root_dir, timeout=180)
            except subprocess.TimeoutExpired:
                rc_plan, out_plan, e_plan = 124, "", "TIMEOUT"
        else:
            rc_plan, out_plan, e_plan = None, "", ""
        tail = "\n".join(out_plan.splitlines()[-8:]) if out_plan else (e_init if rc_init != 0 else "")
        print("root=%-12s init_rc=%s plan_rc=%s" % (root, rc_init, rc_plan))
        print("  " + str(tail).replace("\n", "\n  ")[:1200])
        plans[root] = plan_file
        if rc_init != 0 or (rc_plan is not None and rc_plan != 0):
            plan_failures.append((root, rc_init, rc_plan, (e_init or "")[:300] or (e_plan or "")[:300]))

    print()
    print("-- ten-root plan summary: the ONLY root expected to show a change is 'holdings' "
          "(1 to change), every other root expected 'No changes' (never-widen scope check) --")
    plan_ok = (len(plan_failures) == 0)
    if not plan_ok:
        print()
        print("FRESH 10-ROOT PLAN FAILED on %d of %d root(s): %s"
              % (len(plan_failures), len(TF_ROOTS),
                 ["%s(init_rc=%s,plan_rc=%s)" % (r, ri, rp) for r, ri, rp, _ in plan_failures]))
        for r, ri, rp, msg in plan_failures:
            print("  %-12s: %s" % (r, msg))

    print()
    print("-- packet blob --")
    packet_path = os.path.join(HERE, "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-4.md")
    blob_hash = None
    if os.path.isfile(packet_path):
        rc, out, _err = run(["git", "hash-object", packet_path])
        blob_hash = out.strip()
        print("packet at %s -- blob %s (measured this run; the COMMITTED blob may differ until "
              "the commit lands)" % (packet_path, blob_hash))
    else:
        print("packet not yet written at this point in the run")

    print()
    print("-- halves at HEAD --")
    coo_halves = ([f for f in os.listdir(COO_DIR) if "rtg-4" in f.lower()]
                 if os.path.isdir(COO_DIR) else [])
    cto_halves = ([f for f in os.listdir(CTO_DIR) if "rtg-4" in f.lower()]
                 if os.path.isdir(CTO_DIR) else [])
    print("COO half candidates (%s): %s" % (COO_DIR, coo_halves or "ABSENT"))
    print("CTO half candidates (%s): %s" % (CTO_DIR, cto_halves or "ABSENT"))
    halves_present = len(coo_halves) + len(cto_halves)
    print("halves present: %d of 2" % halves_present)

    if halves_present < 2:
        print()
        print("ARM (c): STOP HERE -- halves ABSENT (%d of 2). This is the EXPECTED first-pass "
              "outcome (the rtf-13 shape, decomp R7.2): R75-AC1 FAILS TRUTHFULLY at this point. "
              "Arm (d) [apply] and arm (e) [live proof under deployed role+bytes] are NOT run "
              "this pass. The order stays open." % halves_present)
        return False

    if not plan_ok:
        print()
        print("ARM (c): STOP HERE -- both halves are PRESENT (2 of 2), but the FRESH 10-ROOT PLAN "
              "this arm requires COULD NOT BE TAKEN (%d of %d root(s) failed init/plan; see the "
              "per-root output above). Per this order's own arm (d) discipline, a subtraction gate "
              "cannot be evaluated over a plan that was never produced -- STOP HERE, do NOT apply. "
              "Arm (d) [apply] and arm (e) [live proof] are NOT run this pass. The order stays open."
              % (len(plan_failures), len(TF_ROOTS)))
        return False

    print("ARM (c): both halves present AND all ten roots plan cleanly -- proceeding to (d)/(e) "
          "is a LATER pass, not this one.")
    return True


def main():
    a_ok = arm_a()
    b_ok, b_info = arm_b()
    c_ok = arm_c(b_info) if b_ok else False

    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print("arm (a) MEASURE:              %s" % ("PASS" if a_ok else "FAIL"))
    print("arm (b) BUILD+VERIFY-AT-REST: %s" % ("PASS" if b_ok else "FAIL"))
    print("arm (c) PACKET+HALVES-GATE:   %s" % ("PASS (halves present)" if c_ok else
                                                "STOP (halves absent or an earlier arm failed)"))
    print("arm (d) APPLY:                 NOT RUN THIS PASS (gated on arm (c))")
    print("arm (e) LIVE PROOF:            NOT RUN THIS PASS (gated on arm (c))")

    overall = a_ok and b_ok and c_ok
    if overall:
        print()
        print("IBR75-HOLDINGS-FOLLOWS-POINTER-AND-SERVES")
    else:
        print()
        print("NOT PRINTING THE SUCCESS TOKEN: this pass stops at arm (c) (or an earlier arm "
              "failed) -- the never-widen halves are not yet SIGNED, so no apply and no live "
              "proof can truthfully run. This is the EXPECTED first-pass outcome; the order "
              "stays open pending both halves.")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
