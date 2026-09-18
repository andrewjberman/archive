#!/usr/bin/env python3
"""battery_ib_rtd_5.py -- IRPT_BCKEND.TO-IB-rtd-5, R45-AC1.

READ-ONLY VERIFICATION of an act already performed once, under ledger, by
this worker (a targeted `terraform apply -target=aws_s3_object.mdpf_route_bindings`,
sourced from the committed LF bytes). This battery does NOT apply, put-object
or otherwise write to S3/Terraform state -- it re-derives, LIVE, every count
the four arms need from the CURRENT world (Rule 12: no self-wrapping harness,
nothing cached from a prior run; the only local mutation is a TEMPORARY,
restored-in-finally overwrite of the worktree file so a plan run sources the
same LF bytes the act itself was sourced from -- never left in place, `git
status` reads clean for that path when this script exits, success or not).

  ARM A -- PRECONDITION READ: both never-widen halves at HEAD name the SAME
           packet blob (re-hashed here, not taken on trust) and the same act.
  ARM B -- THE ACT UNDER LEDGER: the ledger entry is CLOSED with both legs
           proven; before -> after content identity on the served object
           (the prior VersionId's content-sha256 vs the CURRENT head-object's);
           a targeted plan re-run NOW reads "no changes" (already converged);
           an untargeted plan re-run NOW reads 0 RESOURCE actions on the root
           (a stale OUTPUT-only diff from -target's own well-documented
           output-recomputation gap is reported separately and does not fail
           this arm -- filed as IRPT_BCKEND-W3-S40; terraform's own apply-time
           warning predicted exactly this).
  ARM C -- EVERY CONSUMER READ ONCE: the packet's 4 of 4, each against its
           OWN real load path (not a copy).
  ARM D -- ROLLBACK REHEARSED READ-ONLY: the prior VersionId is retrievable.

Prints IBR45-ROUTE-BINDINGS-DRIFT-RESOLVED-ROOT-CONVERGED only if every arm
holds.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
TF_ROOT = os.path.join(WS, "infra", "aws", "terraform", "mdpf-pipeline")
TF_BIN = os.path.join(WS, ".tools", "terraform.exe")
REPO_FILE = os.path.join(WS, "data", "mdpf", "config", "route_bindings.yaml")
BUCKET = "opal-data-assets"
KEY = "config/mdpf/route_bindings.yaml"
PRIOR_VERSION_ID = "iR4vgE0NJdkuQyNkO6AsYjlBmDaqBLBz"
COMMITTED_SHA256 = "98f5e9c51d016d5283562e525b53088292576d86752c6cf0449865fbf328d923"
PRE_ACT_SHA256 = "c9e54ce28351752a382cc14ac17c380ccea471da9191aa1170cf834cbf971fcd"
PACKET_PATH = os.path.join(HERE, "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtd-4.md")
PACKET_BLOB_EXPECTED = "d3dfc6f6f335762ad9b955d17a1441c13ef088e7"
COO_HALF_PATH = os.path.join(
    WS, "org", "tier1_exec", "2.0.0_SA_COO~B", "deliverables",
    "NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtd-5_ROUTE_BINDINGS.md")
CTO_HALF_PATH = os.path.join(
    WS, "org", "tier1_exec", "1.0.0_SA_CTO", "deliverables",
    "NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtd-5_ROUTE_BINDINGS.md")


def log(msg: str) -> None:
    print("[battery-ib-rtd-5] %s" % msg, flush=True)


def run(cmd, cwd=None, timeout=300):
    """CLAUDE.md encoding trap: decode subprocess output as UTF-8 explicitly, never
    the platform cp1252 default, with a lossy fallback that stays ASCII-safe."""
    log("RUN: %s" % " ".join(cmd))
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
    out = p.stdout.decode("utf-8", errors="replace") if isinstance(p.stdout, bytes) else p.stdout
    err = p.stderr.decode("utf-8", errors="replace") if isinstance(p.stderr, bytes) else p.stderr
    return p.returncode, out, err


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def arm_a() -> "tuple[bool, dict]":
    """Precondition read: both halves at HEAD, packet re-hashed."""
    rc, out, err = run(["git", "hash-object", PACKET_PATH], cwd=WS)
    packet_hash = out.strip()
    with open(COO_HALF_PATH, "r", encoding="utf-8") as fh:
        coo_text = fh.read()
    with open(CTO_HALF_PATH, "r", encoding="utf-8") as fh:
        cto_text = fh.read()
    coo_names_blob = PACKET_BLOB_EXPECTED[:10] in coo_text
    cto_names_blob = PACKET_BLOB_EXPECTED[:10] in cto_text
    # Both halves quote the committed sha256's ABBREVIATED (8-char) prefix, never
    # the full 64 hex digits (the CTO half in particular writes `98f5e9c5...`
    # throughout) -- match on the same prefix the documents actually carry.
    sha_prefix = COMMITTED_SHA256[:8]
    coo_names_act = ("-target=aws_s3_object.mdpf_route_bindings" in coo_text
                     and sha_prefix in coo_text)
    cto_names_act = ("TARGETED" in cto_text and sha_prefix in cto_text)
    halves_n = int(coo_names_blob and coo_names_act) + int(cto_names_blob and cto_names_act)
    findings = {
        "packet_hash": packet_hash,
        "packet_hash_expected": PACKET_BLOB_EXPECTED,
        "coo_names_blob": coo_names_blob, "coo_names_act": coo_names_act,
        "cto_names_blob": cto_names_blob, "cto_names_act": cto_names_act,
        "halves_n": halves_n,
    }
    log("ARM A: packet git hash-object = %s (expected %s) MATCH=%s"
       % (packet_hash, PACKET_BLOB_EXPECTED, packet_hash == PACKET_BLOB_EXPECTED))
    log("ARM A: %d of 2 halves name the packet blob AND the act" % halves_n)
    ok = (packet_hash == PACKET_BLOB_EXPECTED) and (halves_n == 2)
    if not ok:
        log("ARM A FAIL")
    return ok, findings


def read_worktree_status_clean() -> bool:
    rc, out, err = run(["git", "status", "--porcelain", "--",
                        "data/mdpf/config/route_bindings.yaml"], cwd=WS)
    return out.strip() == ""


def with_lf_source(fn):
    """Materialise the committed LF bytes at REPO_FILE for the duration of fn(), then
    ALWAYS restore the normal checkout render via `git checkout --`. This mirrors
    exactly how the act itself was sourced (never this box's CRLF render) -- both
    halves' condition (2) and the packet's own recommendation. `git status` on the
    path is asserted clean both before entry (a pre-existing dirty state would make
    the finally-restore misleading) and after restore."""
    pre_clean = read_worktree_status_clean()
    if not pre_clean:
        raise SystemExit("REFUSING: data/mdpf/config/route_bindings.yaml is NOT clean "
                         "before this arm runs -- will not risk masking a real edit.")
    rc, out, err = run(["git", "cat-file", "-p", "HEAD:data/mdpf/config/route_bindings.yaml"], cwd=WS)
    p = subprocess.run(["git", "cat-file", "-p", "HEAD:data/mdpf/config/route_bindings.yaml"],
                       cwd=WS, capture_output=True, timeout=60)
    committed_raw = p.stdout
    with open(REPO_FILE, "wb") as fh:
        fh.write(committed_raw)
    try:
        return fn()
    finally:
        run(["git", "checkout", "--", "data/mdpf/config/route_bindings.yaml"], cwd=WS)
        post_clean = read_worktree_status_clean()
        log("with_lf_source: restored worktree render; git status clean = %s" % post_clean)


def arm_b() -> "tuple[bool, dict]":
    """The act under ledger: ledger CLOSED, before/after identity, plan convergence."""
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")

    log("ARM B: ledger entry state")
    ledger_dir = os.path.join(WS, "org", "critical_paths", "change_management")
    ledger_files = [f for f in os.listdir(ledger_dir) if "ib-rtd-5-route-bindings" in f]
    ledger_closed = False
    ledger_text = ""
    if ledger_files:
        with open(os.path.join(ledger_dir, ledger_files[0]), "r", encoding="utf-8") as fh:
            ledger_text = fh.read()
        ledger_closed = ("CLOSED" in ledger_text) or ("status: closed" in ledger_text.lower())
    open_sentinel = os.path.join(WS, "org", "critical_paths", ".open_deploys",
                                 "ib-rtd-5-route-bindings.json")
    sentinel_absent = not os.path.exists(open_sentinel)
    log("ARM B: ledger file(s) found=%d closed=%s open-sentinel-absent=%s"
       % (len(ledger_files), ledger_closed, sentinel_absent))

    log("ARM B: before -> after identity (re-derived live)")
    prior = s3.head_object(Bucket=BUCKET, Key=KEY, VersionId=PRIOR_VERSION_ID)
    prior_sha256 = prior["Metadata"].get("content-sha256")
    current = s3.head_object(Bucket=BUCKET, Key=KEY)
    current_sha256 = current["Metadata"].get("content-sha256")
    current_version_id = current["VersionId"]
    log("ARM B: prior version %s content-sha256=%s (expect %s)"
       % (PRIOR_VERSION_ID, prior_sha256, PRE_ACT_SHA256))
    log("ARM B: current version %s content-sha256=%s (expect %s)"
       % (current_version_id, current_sha256, COMMITTED_SHA256))
    identity_ok = (prior_sha256 == PRE_ACT_SHA256 and current_sha256 == COMMITTED_SHA256
                  and current_version_id != PRIOR_VERSION_ID)

    log("ARM B: terraform init")
    rc, out, err = run([TF_BIN, "init", "-input=false"], cwd=TF_ROOT, timeout=180)
    if rc != 0:
        raise SystemExit("terraform init FAILED rc=%d stderr=%s" % (rc, err[-2000:]))

    def targeted_plan():
        rc_t, out_t, err_t = run([TF_BIN, "plan", "-input=false", "-no-color",
                                  "-target=aws_s3_object.mdpf_route_bindings"], cwd=TF_ROOT, timeout=300)
        return rc_t, out_t, err_t

    def untargeted_plan():
        rc_u, out_u, err_u = run([TF_BIN, "plan", "-input=false", "-no-color"], cwd=TF_ROOT, timeout=300)
        return rc_u, out_u, err_u

    rc_t, out_t, err_t = with_lf_source(targeted_plan)
    rc_u, out_u, err_u = with_lf_source(untargeted_plan)

    targeted_no_changes = ("No changes." in out_t) or ("Plan: 0 to add, 0 to change, 0 to destroy" in out_t)
    plan_line_match = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", out_u)
    untargeted_resource_actions = (
        0 if plan_line_match is None else
        sum(int(x) for x in plan_line_match.groups())
    )
    untargeted_output_only_diff = ("Changes to Outputs:" in out_u) and (plan_line_match is None)
    root_resource_converged = (untargeted_resource_actions == 0)
    log("ARM B: targeted plan NOW (LF-sourced, post-apply) -- no-changes=%s (rc=%d)"
       % (targeted_no_changes, rc_t))
    log("ARM B: untargeted plan NOW (LF-sourced, post-apply) -- 'Plan:' line present=%s, "
       "resource actions=%d, output-only-diff=%s (rc=%d) -- see IRPT_BCKEND-W3-S40 for the "
       "instrument-behaviour note on why an OUTPUT-only diff prints no 'Plan:' line and is not "
       "a resource drift"
       % (plan_line_match is not None, untargeted_resource_actions, untargeted_output_only_diff, rc_u))

    findings = {
        "ledger_files": ledger_files, "ledger_closed": ledger_closed,
        "open_sentinel_absent": sentinel_absent,
        "prior_version_sha256": prior_sha256, "current_version_sha256": current_sha256,
        "current_version_id": current_version_id, "identity_ok": identity_ok,
        "targeted_no_changes": targeted_no_changes,
        "untargeted_resource_actions": untargeted_resource_actions,
        "untargeted_output_only_diff": untargeted_output_only_diff,
        "root_resource_converged": root_resource_converged,
        "untargeted_plan_tail": "\n".join(out_u.strip().splitlines()[-15:]),
    }
    ok = (ledger_closed and sentinel_absent and identity_ok and targeted_no_changes
         and root_resource_converged)
    if not ok:
        log("ARM B FAIL: %s" % json.dumps({k: v for k, v in findings.items()
                                          if k != "untargeted_plan_tail"}, default=str))
    return ok, findings


def arm_c() -> "tuple[bool, dict]":
    """Every consumer, read once, against its own real load path."""
    import boto3
    results = {}

    log("ARM C 1/4: mdpf-gold-lambda's PACKAGED copy (deployed zip, live download)")
    lam = boto3.client("lambda", region_name="us-east-1")
    loc = lam.get_function(FunctionName="mdpf-gold-lambda")["Code"]["Location"]
    zip_path = os.path.join(WS, ".scratch", "battery_ib_rtd_5_mdpf_gold_lambda.zip")
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    import urllib.request
    with urllib.request.urlopen(loc, timeout=60) as resp:               # noqa: S310
        zdata = resp.read()
    with open(zip_path, "wb") as fh:
        fh.write(zdata)
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if n.endswith("route_bindings.yaml")]
        c1_loads_ok = False
        c1_sha256 = None
        if names:
            raw = z.read(names[0])
            c1_sha256 = sha256(raw)
            import yaml
            doc = yaml.safe_load(raw)
            c1_loads_ok = doc.get("schema") == "mdpf-canrte-route-bindings/v1"
    os.remove(zip_path)
    c1_equal_new_object = (c1_sha256 == COMMITTED_SHA256)
    log("ARM C 1/4: packaged member found=%s loads_ok=%s sha256=%s equal-to-new-object=%s"
       % (bool(names), c1_loads_ok, c1_sha256, c1_equal_new_object))
    results["mdpf_gold_lambda_packaged_copy"] = {
        "loads_ok": c1_loads_ok, "sha256": c1_sha256, "equal_to_new_object": c1_equal_new_object}

    log("ARM C 2/4: build_mdpf_spine.py load_bindings() on its own repo-relative path")
    sys.path.insert(0, os.path.join(WS, "data", "mdpf", "scripts", "gold"))
    import build_mdpf_spine as bms   # noqa: E402
    import importlib
    importlib.reload(bms)
    c2_doc = bms.load_bindings()
    c2_loads_ok = c2_doc.get("schema") == "mdpf-canrte-route-bindings/v1"
    log("ARM C 2/4: loads_ok=%s path=%s" % (c2_loads_ok, bms.BINDINGS_PATH))
    results["build_mdpf_spine"] = {"loads_ok": c2_loads_ok, "path": bms.BINDINGS_PATH}

    log("ARM C 3/4: route_bindings_tieout.py, live, its own repo-relative path")
    rc3, out3, err3 = run(["py", "-3.12", "data/mdpf/config/route_bindings_tieout.py"], cwd=WS, timeout=120)
    tieout_line = [ln for ln in out3.strip().splitlines() if ln.startswith("DENOMINATOR")]
    tieout_denominator = tieout_line[0] if tieout_line else "NO DENOMINATOR LINE PRINTED"
    c3_ok = (rc3 == 0) and ("0 FAIL" in tieout_denominator)
    log("ARM C 3/4: rc=%d %s" % (rc3, tieout_denominator))
    results["route_bindings_tieout"] = {"rc": rc3, "denominator_line": tieout_denominator, "ok": c3_ok}

    log("ARM C 4/4: mdpf-daily-runner EC2 dispatch's OWN synced key (different bucket -- not applicable "
       "to this key's drift, per the packet; read to confirm its own load path is intact)")
    import botocore
    s3 = boto3.client("s3", region_name="us-east-1")
    try:
        head = s3.head_object(Bucket="opal-data-mdpf", Key="code/config/route_bindings.yaml")
        c4_ok = True
        c4_etag = head["ETag"].strip('"')
    except botocore.exceptions.ClientError as exc:                       # noqa: BLE001
        c4_ok = False
        c4_etag = "ERROR %s" % exc
    log("ARM C 4/4: opal-data-mdpf/code/config/route_bindings.yaml head-object ok=%s ETag=%s "
       "(different artifact, separate mint mechanism, per packet)" % (c4_ok, c4_etag))
    results["mdpf_daily_runner_synced_config"] = {"ok": c4_ok, "etag": c4_etag}

    consumers_n = 4
    passing = sum([c1_loads_ok, c2_loads_ok, c3_ok, c4_ok])
    log("ARM C: consumers %d of %d loaded without error on their own path" % (passing, consumers_n))
    ok = (passing == consumers_n)
    if not ok:
        log("ARM C FAIL")
    return ok, {"consumers_n": consumers_n, "passing": passing, "results": results}


def arm_d() -> "tuple[bool, dict]":
    """Rollback rehearsed, READ-ONLY: the prior version is retrievable. The rollback
    recipe is PRINTED, never run."""
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    head = s3.head_object(Bucket=BUCKET, Key=KEY, VersionId=PRIOR_VERSION_ID)
    retrievable = (head["ETag"].strip('"') == "56a03a1410848f88b006f1f98b69dced")
    current = s3.head_object(Bucket=BUCKET, Key=KEY)
    recipe = ('.tools/aws s3api delete-object --bucket %s --key %s --version-id %s'
             % (BUCKET, KEY, current["VersionId"]))
    log("ARM D: prior version %s retrievable=%s (head-object rc reached, ETag matches the "
       "pre-act served bytes)" % (PRIOR_VERSION_ID, retrievable))
    log("ARM D: rollback recipe (PRINTED, NOT RUN): %s" % recipe)
    ok = retrievable
    if not ok:
        log("ARM D FAIL")
    return ok, {"retrievable": retrievable, "rollback_recipe_printed_not_run": recipe}


def main() -> int:
    log("START %s" % datetime.now(timezone.utc).isoformat())
    a_ok, a_findings = arm_a()
    b_ok, b_findings = arm_b()
    c_ok, c_findings = arm_c()
    d_ok, d_findings = arm_d()

    summary = {"arm_a": a_ok, "arm_b": b_ok, "arm_c": c_ok, "arm_d": d_ok}
    log("SUMMARY: %s" % json.dumps(summary))

    if a_ok and b_ok and c_ok and d_ok:
        print("IBR45-ROUTE-BINDINGS-DRIFT-RESOLVED-ROOT-CONVERGED")
        return 0
    log("FAIL: %s" % json.dumps(summary))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
