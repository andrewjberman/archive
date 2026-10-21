#!/usr/bin/env python3
# AR-y-485 check: the audit reporting policy row is ACTIVE and cites the commit that records the applied audit policy.
# Stdlib only. Offline: local git reads (HEAD, the pre-flip base, the cited commit) and an in-process import of
# lib/opal_naming.py by path. No network, no AWS.
import copy
import importlib.util
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True

AUDIT_REVISION = "irpt-anlreq-audit-x10-v1"
BASE_COMMIT = "382ebe4a5a9a"
ENFORCEMENT_REF = "e3788d3f8a359b0253f45137f8ff3b1cfa075c2d"
RECEIPT_PATH = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_auditpolicy/A_AFTER_AUDITPOLICY.txt"
REGISTER_COMMIT = "705dae3202cac873a133825bee9d0381c7dd6b7f"
RULING_COMMIT = "88ae0673276c9c9b0ce068c0273c6ebf25de5a48"
REGISTRY_PATH = "infra/logic/registry/reporting_policies.json"
EDITED_KEYS = {"state", "enforcement_ref"}
HEX40 = re.compile(r"[0-9a-f]{40}")
HEX64 = re.compile(r"[0-9a-f]{64}")


def find_repo():
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(cur, "lib", "opal_naming.py")) and os.path.isdir(os.path.join(cur, ".tools")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


REPO = find_repo()


def git_run(args):
    proc = subprocess.run(["git", "-C", REPO] + args, capture_output=True)
    return proc.returncode, proc.stdout.decode("utf-8", errors="replace")


def load_doc(spec):
    rc, out = git_run(["show", spec])
    if rc != 0:
        raise RuntimeError("git show failed for " + spec)
    return json.loads(out)


def rev_of(row):
    return row.get("policy_revision") if isinstance(row, dict) else None


def audit_row(doc):
    rows = [r for r in doc["policies"] if rev_of(r) == AUDIT_REVISION]
    return rows[0] if len(rows) == 1 else None


def verify_docs(head, base):
    """Doc-level rules. Returns (why, changed_key_count); why is None when every rule holds."""
    if not isinstance(head, dict) or not isinstance(base, dict):
        return "registry is not a JSON object", 0
    if set(head) != set(base):
        return "top-level key set differs from base", 0
    for key in head:
        if key != "policies" and head[key] != base[key]:
            return "top-level key " + key + " changed", 0
    head_rows = head.get("policies")
    base_rows = base.get("policies")
    if not isinstance(head_rows, list) or not isinstance(base_rows, list):
        return "policies is not a list", 0
    if [rev_of(r) for r in head_rows] != [rev_of(r) for r in base_rows]:
        return "policy row order or revision set differs from base", 0
    audit_seen = 0
    changed_count = 0
    for hrow, brow in zip(head_rows, base_rows):
        if not isinstance(hrow, dict) or not isinstance(brow, dict):
            return "a policy row is not an object", 0
        if rev_of(brow) != AUDIT_REVISION:
            if hrow != brow:
                return "other row " + str(rev_of(brow)) + " differs from base", 0
            continue
        audit_seen += 1
        keys = set(hrow) | set(brow)
        changed = sorted(k for k in keys if (k in hrow) != (k in brow) or hrow.get(k) != brow.get(k))
        if set(changed) != EDITED_KEYS:
            return "audit row changed keys " + ",".join(changed) + " (must be exactly state,enforcement_ref)", 0
        if hrow["state"] != "ACTIVE":
            return "audit row state is " + repr(hrow["state"]), 0
        ref = hrow["enforcement_ref"]
        if not isinstance(ref, str) or not HEX40.fullmatch(ref):
            return "audit row enforcement_ref is not 40 lowercase hex", 0
        if ref != ENFORCEMENT_REF:
            return "audit row enforcement_ref is not the applied-policy commit", 0
        if hrow.get("register_commit") != brow.get("register_commit") or hrow.get("register_commit") != REGISTER_COMMIT:
            return "audit row register_commit moved", 0
        if hrow.get("ruling_commit") != brow.get("ruling_commit") or hrow.get("ruling_commit") != RULING_COMMIT:
            return "audit row ruling_commit moved", 0
        changed_count = len(changed)
    if audit_seen != 1:
        return "audit row count is " + str(audit_seen), 0
    return None, changed_count


def verify_ref():
    rc, out = git_run(["cat-file", "-t", ENFORCEMENT_REF])
    if rc != 0 or out.strip() != "commit":
        return "enforcement_ref does not resolve to a commit"
    rc, _ = git_run(["cat-file", "-e", ENFORCEMENT_REF + ":" + RECEIPT_PATH])
    if rc != 0:
        return "enforcement_ref commit does not contain the applied-policy receipt"
    return None


def verify_builder(head):
    path = os.path.join(REPO, "lib", "opal_naming.py")
    with open(os.path.join(REPO, *REGISTRY_PATH.split("/")), encoding="utf-8") as fh:
        working = json.load(fh)
    if working != head:
        return "working-tree registry differs from HEAD"
    try:
        spec = importlib.util.spec_from_file_location("opal_naming_ar485", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        policy = module.reporting_policy(AUDIT_REVISION)
    except Exception as exc:  # the builder's refusal is the verdict, whatever its type
        return "builder raised " + type(exc).__name__ + ": " + str(exc)
    if not isinstance(policy, dict):
        return "builder returned no dict"
    if policy.get("state") != "ACTIVE":
        return "builder state is " + repr(policy.get("state"))
    digest = policy.get("policy_sha256")
    if not isinstance(digest, str) or not HEX64.fullmatch(digest):
        return "builder policy_sha256 is not 64 lowercase hex"
    return None


def run_real():
    """Returns (stdout_line, ok)."""
    head = load_doc("HEAD:" + REGISTRY_PATH)
    base = load_doc(BASE_COMMIT + ":" + REGISTRY_PATH)
    base_audit = audit_row(base)
    if base_audit is None or base_audit.get("state") != "PENDING_ENFORCEMENT" or base_audit.get("enforcement_ref") is not None:
        return "AUDIT-ACTIVE-BAD base commit is not the pre-flip registry", False
    why, changed = verify_docs(head, base)
    if why is None:
        why = verify_ref()
    if why is None:
        why = verify_builder(head)
    if why is not None:
        return "AUDIT-ACTIVE-BAD " + why, False
    line = ("AUDIT-ACTIVE-OK state=ACTIVE enforcement_ref=" + ENFORCEMENT_REF[:10]
            + " other_rows_unchanged=yes audit_row_keys_changed=" + str(changed) + " builder_accepts=yes")
    return line, True


def run_selftest():
    head = load_doc("HEAD:" + REGISTRY_PATH)
    base = load_doc(BASE_COMMIT + ":" + REGISTRY_PATH)
    baseline, _ = verify_docs(head, base)
    if baseline:
        sys.stderr.write("baseline read BAD: " + baseline + "\n")
        print("CONTROL-DOES-NOT-FIRE baseline")
        return 1
    m1 = copy.deepcopy(head)
    audit_row(m1)["state"] = "ACTIVE"
    audit_row(m1)["enforcement_ref"] = None
    m2 = copy.deepcopy(head)
    audit_row(m2)["enforcement_ref"] = ENFORCEMENT_REF[:39]
    m3 = copy.deepcopy(head)
    other = [r for r in m3["policies"] if rev_of(r) != AUDIT_REVISION][0]
    other["state"] = "DISABLED" if other.get("state") != "DISABLED" else "ACTIVE"
    reasons = []
    for label, mutant in (("audit-active-null-ref", m1), ("ref-39-hex", m2), ("other-row-state", m3)):
        why, _ = verify_docs(mutant, base)
        sys.stderr.write("mutant " + label + ": " + (why or "READ OK") + "\n")
        reasons.append(why)
    if all(reasons):
        print("CONTROL-FIRES")
        return 0
    print("CONTROL-DOES-NOT-FIRE " + ",".join(str(i) for i, w in enumerate(reasons) if not w))
    return 1


def main(argv):
    if REPO is None:
        print("AUDIT-ACTIVE-BAD repository root not found from " + os.path.abspath(__file__))
        return 1
    if "--selftest" in argv:
        return run_selftest()
    line, ok = run_real()
    print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
