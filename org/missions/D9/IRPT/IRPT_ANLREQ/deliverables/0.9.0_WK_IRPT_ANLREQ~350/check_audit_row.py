"""IRPT_ANLREQ AR-y-481 (C-AUDIT-RECORD; CTO msg 11646): the restored row irpt-anlreq-x10-v1 and the audit's own row.

Offline and stdlib only: git show of blobs at HEAD and at the commit before AR-y-466, a temporary registry directory outside
the repository, no AWS, no network, no write to the repository.

  python -I check_audit_row.py              AUDIT-ROW-OK ... (rc 0) or AUDIT-ROW-BAD <why> (rc 1)
  python -I check_audit_row.py --selftest   CONTROL-FIRES (rc 0) or CONTROL-MISSED <why> (rc 1)

Each mode prints exactly one line on stdout. ASCII only.
"""
import copy
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

OLD_REV = "irpt-anlreq-x10-v1"
NEW_REV = "irpt-anlreq-audit-x10-v1"
PARENT = "1c277930e66^"
REGISTRY_REL = "infra/logic/registry"
POLICY_FILE = REGISTRY_REL + "/reporting_policies.json"
NAMING_REL = "lib/opal_naming.py"
TF_REL = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"
REGISTER_COMMIT = "705dae3202cac873a133825bee9d0381c7dd6b7f"
RULING_COMMIT = "88ae0673276c9c9b0ce068c0273c6ebf25de5a48"
FAMILY = "ANALYSIS_AUDIT"
FAMILY_TERMS = {"tier": "platinum", "table": "analysis_audit", "extension": "json",
                "unreferenced_days": None, "accepted_ceiling_days": 2555}
SHARED_FIELDS = ("register_id", "register_path", "retention_policy_id", "source", "product_scope", "firms")


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError("git %s returned rc=%d" % (" ".join(args), proc.returncode))
    return proc.stdout


def blob(repo, rev, path):
    return git(repo, "show", "%s:%s" % (rev, path))


def registry_json_names(repo, rev):
    listing = git(repo, "ls-tree", "--name-only", rev, REGISTRY_REL + "/").decode("utf-8")
    names = [line[len(REGISTRY_REL) + 1:] for line in listing.splitlines() if line.endswith(".json")]
    if "reporting_policies.json" not in names:
        raise RuntimeError("reporting_policies.json is absent at %s" % rev)
    return names


def rows_at(repo, rev):
    return json.loads(blob(repo, rev, POLICY_FILE).decode("utf-8"))["policies"]


def naming_at(repo, rev, workdir):
    """lib/opal_naming.py loaded BY PATH from the blob at rev, with REGISTRY_DIR pointed at that rev's registry blobs."""
    tag = re.sub(r"[^A-Za-z0-9]", "_", rev)
    root = os.path.join(workdir, tag)
    os.makedirs(os.path.join(root, "lib"))
    os.makedirs(os.path.join(root, "registry"))
    lib_path = os.path.join(root, "lib", "opal_naming.py")
    with open(lib_path, "wb") as handle:
        handle.write(blob(repo, rev, NAMING_REL))
    for name in registry_json_names(repo, rev):
        with open(os.path.join(root, "registry", name), "wb") as handle:
            handle.write(blob(repo, rev, REGISTRY_REL + "/" + name))
    spec = importlib.util.spec_from_file_location("opal_naming_" + tag, lib_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.REGISTRY_DIR = os.path.join(root, "registry")
    return module


def find_row(rows, revision):
    found = [row for row in rows if row.get("policy_revision") == revision]
    return found[0] if len(found) == 1 else None


def new_row_reasons(new, old_parent):
    """The CTO's terms for the new row, and the same shape as the restored row."""
    reasons = []
    if set(new) != set(old_parent):
        reasons.append("new row field set differs from %s" % OLD_REV)
    expected = {
        "policy_id": "irpt-anlreq-audit",
        "policy_revision": NEW_REV,
        "register_commit": REGISTER_COMMIT,
        "ruling_commit": RULING_COMMIT,
        "state": "PENDING_ENFORCEMENT",
        "enforcement_ref": None,
        "physical_disposal": "OPEN",
        "families": {FAMILY: FAMILY_TERMS},
    }
    for field in SHARED_FIELDS:
        expected[field] = old_parent.get(field)
    for field in sorted(expected):
        if new.get(field) != expected[field]:
            reasons.append("new row %s is not the CTO term" % field)
    return reasons


def tf_reasons(tf_text):
    reasons = []
    selectors = [line for line in tf_text.splitlines() if "resident_audit_policy = one(" in line]
    if len(selectors) != 1 or ('"%s"' % NEW_REV) not in selectors[0]:
        reasons.append("resident_audit_policy does not select %s" % NEW_REV)
    lines = tf_text.splitlines()
    start = [index for index, line in enumerate(lines) if line.startswith("  resident_audit_write_prefixes = [")]
    block = []
    if len(start) == 1:
        for line in lines[start[0] + 1:]:
            if line == "  ]":
                break
            block.append(line)
    text = "\n".join(block)
    if len(start) != 1 or "resident_audit_policy" not in text or ('"%s"' % FAMILY) not in text:
        reasons.append("resident_audit_write_prefixes does not name the new row")
    return reasons


def check(parent_rows, head_rows, parent_sha, head_sha, tf_text):
    """The list of reasons the tree is wrong; empty when every term holds."""
    reasons = []
    by_parent = {row.get("policy_revision"): row for row in parent_rows}
    by_head = {row.get("policy_revision"): row for row in head_rows}
    if len(by_head) != len(head_rows):
        reasons.append("duplicate policy_revision at HEAD")
    if parent_sha != head_sha:
        reasons.append("%s policy_sha256 differs from %s" % (OLD_REV, PARENT))
    old_parent, old_head = by_parent.get(OLD_REV), by_head.get(OLD_REV)
    if old_parent is None or old_head is None:
        reasons.append("%s row is absent" % OLD_REV)
    else:
        if old_head != old_parent:
            reasons.append("%s row is not the row at %s" % (OLD_REV, PARENT))
        if list(old_head.get("families", {})) != ["ANALYSIS_COMMENTARY"]:
            reasons.append("%s families are not ['ANALYSIS_COMMENTARY']" % OLD_REV)
    if set(by_head) != set(by_parent) | {NEW_REV}:
        reasons.append("policy revisions are not %s plus %s" % (PARENT, NEW_REV))
    for revision, row in by_parent.items():
        if revision != OLD_REV and by_head.get(revision) != row:
            reasons.append("row %s differs from %s" % (revision, PARENT))
    new = by_head.get(NEW_REV)
    if new is None:
        reasons.append("%s row is absent" % NEW_REV)
    elif old_parent is not None:
        reasons.extend(new_row_reasons(new, old_parent))
    reasons.extend(tf_reasons(tf_text))
    return reasons


def selftest(parent_rows, head_rows, parent_sha, head_sha, tf_text):
    baseline = check(parent_rows, head_rows, parent_sha, head_sha, tf_text)
    if baseline:
        return "CONTROL-MISSED baseline is not OK: " + "; ".join(baseline)
    mutants = {}
    old_again = copy.deepcopy(head_rows)
    find_row(old_again, OLD_REV)["families"][FAMILY] = dict(FAMILY_TERMS)
    mutants["old-row-given-ANALYSIS_AUDIT"] = old_again
    active = copy.deepcopy(head_rows)
    find_row(active, NEW_REV)["state"] = "ACTIVE"
    mutants["new-row-ACTIVE-with-null-enforcement"] = active
    enforced = copy.deepcopy(head_rows)
    find_row(enforced, NEW_REV)["enforcement_ref"] = "a" * 40
    mutants["new-row-with-40-hex-enforcement"] = enforced
    missed = [name for name, rows in sorted(mutants.items())
              if not check(parent_rows, rows, parent_sha, head_sha, tf_text)]
    if missed:
        return "CONTROL-MISSED " + ",".join(missed)
    return "CONTROL-FIRES"


def run(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    repo = git(here, "rev-parse", "--show-toplevel").decode("utf-8").strip()
    workdir = tempfile.mkdtemp(prefix="anlreq481_")
    try:
        parent_rev = git(repo, "rev-parse", "--verify", PARENT).decode("utf-8").strip()
        head_module = naming_at(repo, "HEAD", workdir)
        parent_module = naming_at(repo, parent_rev, workdir)
        head_sha = head_module.reporting_policy(OLD_REV)["policy_sha256"]
        parent_sha = parent_module.reporting_policy(OLD_REV)["policy_sha256"]
        parent_rows = rows_at(repo, parent_rev)
        head_rows = rows_at(repo, "HEAD")
        tf_text = blob(repo, "HEAD", TF_REL).decode("utf-8")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    if "--selftest" in argv:
        return selftest(parent_rows, head_rows, parent_sha, head_sha, tf_text)
    reasons = check(parent_rows, head_rows, parent_sha, head_sha, tf_text)
    if reasons:
        return "AUDIT-ROW-BAD " + "; ".join(reasons)
    new = find_row(head_rows, NEW_REV)
    enforcement = "null" if new["enforcement_ref"] is None else "set"
    return ("AUDIT-ROW-OK old_policy_sha_equal=yes new_row=%s enforcement_ref=%s register_commit=%s "
            "ruling_commit=%s other_rows_unchanged=yes" % (new["state"], enforcement, REGISTER_COMMIT[:8],
                                                             RULING_COMMIT[:8]))


def main(argv):
    try:
        line = run(argv)
    except Exception as exc:  # fail closed: any read or load failure is a BAD verdict, never a pass
        line = "AUDIT-ROW-BAD unreadable: %s" % type(exc).__name__
        if "--selftest" in argv:
            line = "CONTROL-MISSED unreadable: %s" % type(exc).__name__
    print(line)
    if line.startswith(("AUDIT-ROW-OK", "CONTROL-FIRES")):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
