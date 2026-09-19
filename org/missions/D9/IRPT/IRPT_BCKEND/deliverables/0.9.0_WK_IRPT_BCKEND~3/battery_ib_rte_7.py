#!/usr/bin/env python3
"""battery_ib_rte_7.py -- IB-rte-7 acceptance proof: THE LGIC FIRM BUCKETS SURVIVE THE REGISTRY FLIP.

Re-derives every count from REAL `terraform plan` runs against the shared-infra root, every run --
never reads its own earlier output. NEVER `terraform apply`, NEVER a `terraform state` verb, NEVER
`-target`. Every registry edit this battery makes is LOCAL AND UNCOMMITTED and is restored to HEAD's
bytes before the battery exits (verified by `git status --porcelain -- infra/logic/registry/` reading
EMPTY), whatever the outcome.

Prints `IBR57-LGIC-FIRM-BUCKETS-SURVIVE-THE-FLIP` ONLY when every arm holds exactly as the task order's
face states it. As measured at this order's cut, one arm (PLAN-2's literal "0 to add, 0 to destroy")
does not hold, for a reason this battery isolates and prints rather than hides -- see the printed
VERDICT and row IRPT_BCKEND-W3-S45.

ASCII only. Standard library only.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

WORKER = "0.9.0_WK_IRPT_BCKEND~3"
TF_FILE_REL = "infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf"
SCOPES_REL = "infra/logic/registry/scopes.json"
EXEMPTIONS_REL = "infra/logic/registry/exemptions.json"
# The blob of s3-lgic-firm-buckets.tf as it stood at this worktree's cut commit (a57ebbe934), BEFORE
# this order's edit -- the stable "OLD selector" reference this battery diffs the new selector against,
# independent of what HEAD carries at re-run time (R-40: an identity is a content hash, not a ref).
OLD_TF_BLOB = "2f877637991cc2f83126f90b153f9567f8471fec"
MANAGED_BY_VALUE = "s3-lgic-firm-buckets.tf"

ANDREW_BERMAN_ARN = "arn:aws:iam::313476888478:user/Andrew_Berman"
ANDREW_CONSOLE_ARN = "arn:aws:iam::313476888478:user/Andrew_Berman_Console"
OPAL_TERMINAL_ARN = "arn:aws:iam::313476888478:user/Opal_Terminal"
CTO_RECORD = ("org/missions/D9/IRPT/IRPT_BCKEND/deliverables/1.0.0_SA_CTO/"
              "IRPT_BCKEND_REGISTRY_DEADLOCK_NEW_FIRM_BUCKETS_20260918.md @9eeb9a70a8")

TOKEN = "IBR57-LGIC-FIRM-BUCKETS-SURVIVE-THE-FLIP"


def repo_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


REPO = repo_root()
TF_DIR = REPO / "infra" / "aws" / "terraform" / "shared-infra"
TF_BIN = REPO / ".tools" / "terraform.exe"


def sh(args, cwd=None, timeout=600):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def git(*args, cwd=None):
    rc, out, err = sh(["git"] + list(args), cwd=cwd or REPO)
    return rc, out, err


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_object(path: Path) -> str:
    rc, out, _ = git("hash-object", "--no-filters", str(path))
    return out.strip() if rc == 0 else "(hash-object failed)"


def read_git_blob(blob_or_ref, path=None) -> str:
    if path is None:
        rc, out, err = git("cat-file", "-p", blob_or_ref)
    else:
        rc, out, err = git("show", "%s:%s" % (blob_or_ref, path))
    if rc != 0:
        raise RuntimeError("git read failed for %s: %s" % (blob_or_ref, err))
    return out


def write_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8", newline="\n")


def registry_status_empty() -> bool:
    rc, out, _ = git("status", "--porcelain", "--", "infra/logic/registry/")
    return rc == 0 and out.strip() == ""


def restore_registry():
    for rel in (SCOPES_REL, EXEMPTIONS_REL):
        write_text(REPO / rel, read_git_blob("HEAD", rel))
    git("update-index", "--really-refresh", "--", SCOPES_REL, EXEMPTIONS_REL)


def restore_tf(new_bytes: str):
    write_text(REPO / TF_FILE_REL, new_bytes)


def patch_scopes_delta():
    d = json.loads(read_git_blob("HEAD", SCOPES_REL))
    for s in d["scopes"]:
        if s.get("key") in ("inflection", "cottonwood"):
            s["bucket_provisioned"] = True
            s["bucket_managed_by"] = MANAGED_BY_VALUE
    write_text(REPO / SCOPES_REL, json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def exemption_rows(bucket):
    return [
        {"principal": "Andrew_Berman", "arn": ANDREW_BERMAN_ARN,
         "reason": ("IB-rte-7 PLAN-2 local test row (never committed): operator identity of %s. IAM_USER, "
                    "scope token none, matched and DENIED by the scope-derived Deny absent this row -- see "
                    "%s and row IRPT_BCKEND-W3-S43. Row content is this test's, not a copy of the CTO's "
                    "unwritten rows.") % (bucket, CTO_RECORD),
         "signoff_ref": "IB-rte-7 PLAN-2 local test only -- never committed"},
        {"principal": "Andrew_Berman_Console", "arn": ANDREW_CONSOLE_ARN,
         "reason": ("IB-rte-7 PLAN-2 local test row (never committed): operator identity of %s, the console "
                    "identity named for Andrew's step-4 delete-bucket-policy. IAM_USER, scope token none, "
                    "matched and DENIED absent this row.") % bucket,
         "signoff_ref": "IB-rte-7 PLAN-2 local test only -- never committed"},
        {"principal": "Opal_Terminal", "arn": OPAL_TERMINAL_ARN,
         "reason": ("IB-rte-7 PLAN-2 local test row (never committed): operator identity of %s applying this "
                    "root's plans. IAM_USER, scope token none, matched and DENIED absent this row.") % bucket,
         "signoff_ref": "IB-rte-7 PLAN-2 local test only -- never committed"},
    ]


def patch_exemptions_delta():
    d = json.loads(read_git_blob("HEAD", EXEMPTIONS_REL))
    d["exemptions"]["opal-data-inflection"] = exemption_rows("opal-data-inflection")
    d["exemptions"]["opal-data-cottonwood"] = exemption_rows("opal-data-cottonwood")
    write_text(REPO / EXEMPTIONS_REL, json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def run_validate():
    rc, out, err = sh(["py", "-3.12", "lib/opal_naming.py", "validate"], cwd=REPO, timeout=60)
    return rc, out, err


def tf_plan(label, refresh=True, out_path=None):
    args = [str(TF_BIN), "plan", "-input=false", "-no-color"]
    if not refresh:
        args.append("-refresh=false")
    if out_path:
        args += ["-out=%s" % out_path]
    rc, out, err = sh(args, cwd=TF_DIR, timeout=600)
    text = out + err
    print("---- terraform plan [%s] refresh=%s rc=%s ----" % (label, refresh, rc))
    return rc, text


def extract_summary(text):
    creates = sorted(re.findall(r"# (\S+) will be created", text))
    destroys = sorted(re.findall(r"# (\S+) will be destroyed", text))
    tainted = sorted(re.findall(r"# (\S+) is tainted, so must be replaced", text))
    plan_line_m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy\.", text)
    plan_line = plan_line_m.group(0) if plan_line_m else None
    add_n, chg_n, destroy_n = (int(x) for x in plan_line_m.groups()) if plan_line_m else (None, None, None)
    err_resources = sorted(set(re.findall(r"with (\S+),\n", text)))
    policy_arn_additions = {}
    for firm in ("inflection", "cottonwood"):
        pat = re.compile(
            r'aws_s3_bucket_policy\.lgic_firm\["%s"\].*?ArnNotLike = \{\s*~? ?"aws:PrincipalArn" = \[(.*?)\]' % firm,
            re.S)
        m = pat.search(text)
        if m:
            adds = re.findall(r'\+\s*"([^"]+)"', m.group(1))
            policy_arn_additions[firm] = adds
    return {
        "creates": creates, "destroys": destroys, "tainted": tainted, "plan_line": plan_line,
        "add": add_n, "change": chg_n, "destroy": destroy_n,
        "err_resources": err_resources, "policy_arn_additions": policy_arn_additions,
    }


def main():
    print("==== (0) WORKTREE / TREE-OK ====")
    print("REPO:", REPO)
    for p in ("org", ".tools"):
        assert (REPO / p).is_dir(), "missing %s" % p
    print("TREE-OK")

    assert TF_BIN.is_file(), "vendored terraform.exe missing at %s" % TF_BIN

    holds = {}
    diag = {}

    print("\n==== (1) TERRAFORM INIT ====")
    rc, out, err = sh([str(TF_BIN), "init", "-input=false", "-no-color"], cwd=TF_DIR, timeout=300)
    print("init rc=%s" % rc)
    if rc != 0:
        print(out[-2000:], err[-2000:])

    print("\n==== (2) THE FIELD-CLOSURE MEASUREMENT (ruling amendment: run FIRST) ====")
    try:
        patch_scopes_delta()
        vrc, vout, verr = run_validate()
        print(vout.strip().splitlines()[-1] if vout.strip() else "(no output)")
        holds["validate_accepts_field"] = (vrc == 0)
        diag["validate_rc"] = vrc
        diag["validate_last_line"] = vout.strip().splitlines()[-1] if vout.strip() else ""
    finally:
        restore_registry()
        assert registry_status_empty(), "registry not restored after arm (2)"
        print("registry restored, git status EMPTY: OK")

    if not holds["validate_accepts_field"]:
        print("\nSTOP: validate REFUSED the drafted field -- unlandable. See surprise row.")
        print("VERDICT: FAIL (arm 2)")
        return 1

    new_tf_bytes = (REPO / TF_FILE_REL).read_text(encoding="utf-8")
    old_tf_bytes = read_git_blob(OLD_TF_BLOB)

    print("\n==== (3) PLAN-1: new selector vs OLD selector, HEAD's registry ====")
    # (3a) OLD selector, HEAD registry, refresh=false (baseline, deterministic)
    restore_tf(old_tf_bytes)
    rc_old, out_old = tf_plan("PLAN-1 OLD selector (refresh=false)", refresh=False)
    s_old = extract_summary(out_old)
    # (3b) NEW selector, HEAD registry, refresh=false
    restore_tf(new_tf_bytes)
    rc_new, out_new = tf_plan("PLAN-1 NEW selector (refresh=false)", refresh=False)
    s_new = extract_summary(out_new)
    plan1_identical = (s_old["creates"] == s_new["creates"] and s_old["destroys"] == s_new["destroys"]
                        and s_old["tainted"] == s_new["tainted"] and s_old["plan_line"] == s_new["plan_line"])
    holds["plan1_zero_diff"] = plan1_identical
    diag["plan1_old"] = s_old
    diag["plan1_new"] = s_new
    print("OLD:", s_old["plan_line"], "tainted:", s_old["tainted"])
    print("NEW:", s_new["plan_line"], "tainted:", s_new["tainted"])
    print("PLAN-1 identical (0 differences):", plan1_identical)
    # also demonstrate the LIVE (refresh=true) crash is identical/orthogonal, informationally
    rc_new_live, out_new_live = tf_plan("PLAN-1 NEW selector (live refresh, informational)", refresh=True)
    s_new_live = extract_summary(out_new_live)
    diag["plan1_new_live_err_resources"] = s_new_live["err_resources"]
    diag["plan1_new_live_rc"] = rc_new_live

    print("\n==== (4) PLAN-2: new selector + registry delta, local/uncommitted ====")
    try:
        patch_scopes_delta()
        patch_exemptions_delta()
        rc2, out2 = tf_plan("PLAN-2 (refresh=false)", refresh=False)
        s2 = extract_summary(out2)
        diag["plan2"] = s2
        print("PLAN-2:", s2["plan_line"], "tainted:", s2["tainted"], "arn adds:", s2["policy_arn_additions"])
        rc2_live, out2_live = tf_plan("PLAN-2 (live refresh, informational)", refresh=True)
        diag["plan2_live_rc"] = rc2_live
        diag["plan2_live_tail"] = out2_live[-800:]
    finally:
        restore_registry()
        assert registry_status_empty(), "registry not restored after arm (4)"
        print("registry restored, git status EMPTY: OK")

    plan2_literal = (s2["add"] == 0 and s2["destroy"] == 0)
    holds["plan2_literal_zero_add_zero_destroy"] = plan2_literal
    # the isolated semantic diff: compare PLAN-2 (refresh=false) against PLAN-1 NEW (refresh=false):
    # the taint-driven tainted/destroy set must be IDENTICAL, and the only NEW content is the exemption
    # arns landing in each policy's ArnNotLike list.
    taint_isolated = (s2["tainted"] == s_new["tainted"] and s2["destroy"] == s_new["destroy"])
    arns_added = all(
        set(s2["policy_arn_additions"].get(firm, [])) == {ANDREW_BERMAN_ARN, ANDREW_CONSOLE_ARN, OPAL_TERMINAL_ARN}
        for firm in ("inflection", "cottonwood")
    )
    holds["plan2_semantic_isolated_diff_is_exactly_the_exemptions"] = (taint_isolated and arns_added)
    print("PLAN-2 literal 0/0 bound holds:", plan2_literal)
    print("PLAN-2 isolated semantic diff is exactly the 3 exemption ARNs per firm, nothing else:", taint_isolated and arns_added)

    print("\n==== (5) PLAN-3: OLD selector (mutant) + same registry delta ====")
    try:
        restore_tf(old_tf_bytes)
        patch_scopes_delta()
        patch_exemptions_delta()
        rc3, out3 = tf_plan("PLAN-3 mutant (refresh=false)", refresh=False)
        s3 = extract_summary(out3)
        diag["plan3"] = s3
        print("PLAN-3:", s3["plan_line"], "destroys:", len(s3["destroys"]))
        rc3_live, out3_live = tf_plan("PLAN-3 mutant (live refresh, informational)", refresh=True)
        diag["plan3_live_rc"] = rc3_live
        diag["plan3_live_tail"] = out3_live[-800:]
    finally:
        restore_registry()
        restore_tf(new_tf_bytes)
        assert registry_status_empty(), "registry not restored after arm (5)"
        print("registry restored, git status EMPTY: OK")
        print("tf file restored to the new selector: OK")

    plan3_holds = (s3["add"] == 0 and s3["change"] == 0 and s3["destroy"] >= 8)
    holds["plan3_mutant_destroy_ge_8"] = plan3_holds
    print("PLAN-3 destroy >= 8:", plan3_holds, "(k=%s)" % s3["destroy"])

    demo_49f_absent = all(
        not any("49financial" in x or "opal_data_49financial" in x or "opal_data_demo" in x
                for x in (s["creates"] + s["destroys"] + s["tainted"]))
        for s in (s_old, s_new, s2, s3)
    )
    holds["demo_and_49financial_absent_from_every_plan"] = demo_49f_absent
    print("demo/49financial absent from every plan's resource list:", demo_49f_absent)

    print("\n==== (6) THE DELTA FILE APPLIES CLEANLY ====")
    delta_path = Path(__file__).with_name("registry_delta_ib_rte_7.md")
    delta_text = delta_path.read_text(encoding="utf-8")
    diff_m = re.search(r"```diff\n(.*?)\n```", delta_text, re.S)
    diff_text = diff_m.group(1) + "\n"
    diff_file = Path(__file__).with_name(".tmp_delta_apply_check.diff")
    diff_file.write_text(diff_text, encoding="utf-8", newline="\n")
    rc_apply, out_apply, err_apply = git("apply", "--check", str(diff_file))
    diff_file.unlink(missing_ok=True)
    holds["delta_diff_applies_cleanly"] = (rc_apply == 0)
    print("git apply --check rc=%s" % rc_apply, out_apply, err_apply)

    print("\n==== (7) fmt/validate on the final .tf ====")
    rc_fmt, out_fmt, err_fmt = sh([str(TF_BIN), "fmt", "-check", "-diff", TF_FILE_REL], cwd=REPO, timeout=60)
    rc_val, out_val, err_val = sh([str(TF_BIN), "validate", "-no-color"], cwd=TF_DIR, timeout=60)
    holds["fmt_clean"] = (rc_fmt == 0)
    holds["validate_clean"] = (rc_val == 0)
    print("fmt -check rc=%s" % rc_fmt)
    print("validate rc=%s: %s" % (rc_val, out_val.strip()))

    print("\n==== FINAL HASHES (R-40) ====")
    tf_hash = hash_object(REPO / TF_FILE_REL)
    print("s3-lgic-firm-buckets.tf git hash-object --no-filters:", tf_hash)

    print("\n==== VERDICT ====")
    for k, v in holds.items():
        print("  %s: %s" % (k, "HOLD" if v else "FAIL"))
    every_arm = all(holds.values())
    if every_arm:
        print(TOKEN)
        return 0
    print("NOT EVERY ARM HOLDS -- token withheld.")
    print("Known unmet arm: plan2_literal_zero_add_zero_destroy (a pre-existing, already-ARMED lockout")
    print("(row IRPT_BCKEND-W3-S43) blocks a live plan from completing at all, and the state carries a")
    print("pre-existing taint on 4 resources identical with/without this order's registry delta -- see")
    print("row IRPT_BCKEND-W3-S45. The isolated semantic diff attributable to this order's own edit IS")
    print("exactly the intended exemption-arn addition, proven by arm")
    print("plan2_semantic_isolated_diff_is_exactly_the_exemptions.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
