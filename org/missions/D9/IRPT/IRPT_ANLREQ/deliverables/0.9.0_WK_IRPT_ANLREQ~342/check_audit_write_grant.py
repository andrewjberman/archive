#!/usr/bin/env python3
"""IRPT_ANLREQ AR-y-468: the resident role's put-only grant on the analysis audit record.

Stdlib only, offline, no AWS call. Three checks over this worktree:
  (a) the HCL text of infra/aws/terraform/investor-reporting/ycharts/resident.tf: the list local
      resident_audit_write_prefixes is built from resident_scopes and the policy row selected by
      irpt-anlreq-x10-v1 (no arn:aws:s3:::opal literal), and the statement WriteTheAnalysisAudit has
      Effect Allow, Action exactly ["s3:PutObject"], Resource local.resident_audit_write_prefixes, and sits
      right after ReadTheAnalysisCommentaryDraft inside aws_iam_role_policy.runner_resident.
  (b) the prefixes are evaluated in Python from scopes.json and reporting_policies.json (family
      ANALYSIS_AUDIT of irpt-anlreq-x10-v1). For each enabled client firm the Terraform prefix is compared
      with lib/opal_naming.py address() (loaded BY PATH) by EXACT string equality of the whole bucket and
      key: "arn:aws:s3:::" + the bucket of address() + "/" + the key of address() without its partition
      segment + "/*". The partition is the placeholder PARTITION on the builder side (the key grammar
      takes any partition token; the prefix ends before it).
  (c) the family row must exist in the policy row; if it is absent the prefixes are evaluated with the
      tier and table the cell names (platinum, analysis_audit) and the check reports the absence.

Usage: python -I check_audit_write_grant.py [--selftest]
  --selftest mutates in memory (A) the table name of the family, compared with the builder, and (B) the
  statement Action by adding s3:GetObject. It prints CONTROL-FIRES only when both read BAD, each for
  its own reason. ASCII only.
"""

import argparse
import copy
import importlib.util
import json
import os
import re
import sys

POLICY_REVISION = "irpt-anlreq-x10-v1"
FAMILY = "ANALYSIS_AUDIT"
EXPECT_TIER = "platinum"
EXPECT_TABLE = "analysis_audit"
SID = "WriteTheAnalysisAudit"
PREV_SID = "ReadTheAnalysisCommentaryDraft"
PARTITION = "PARTITION"
TF_REL = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"
SCOPES_REL = "infra/logic/registry/scopes.json"
POLICIES_REL = "infra/logic/registry/reporting_policies.json"
NAMING_REL = "lib/opal_naming.py"
EXPECT_KEYS = ["Sid", "Effect", "Action", "Resource"]
POLICY_LINE = (
    'resident_commentary_policy = one([for p in jsondecode(file("${path.module}/../../../../logic/registry/'
    'reporting_policies.json")).policies : p if p.policy_revision == "irpt-anlreq-x10-v1"])'
)
LIST_HEAD = "resident_audit_write_prefixes = ["
LIST_BODY = (
    'for scope_key in keys(local.resident_scopes) : '
    '"arn:aws:s3:::${local.resident_scopes[scope_key].bucket}/${local.resident_commentary_policy.source}/'
    '${local.resident_scopes[scope_key].long}/'
    '${local.resident_commentary_policy.families["ANALYSIS_AUDIT"].tier}/'
    '${local.resident_commentary_policy.families["ANALYSIS_AUDIT"].table}/*"'
)
REASON_TABLE = "differs from builder"
REASON_ACTION = "Action is not exactly"


def find_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(cur, NAMING_REL)) and os.path.isdir(os.path.join(cur, "infra")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("AUDIT-WRITE-GRANT-BAD no worktree root above %s" % start)
        cur = parent


def load_naming(root):
    spec = importlib.util.spec_from_file_location("opal_naming_by_path", os.path.join(root, NAMING_REL))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as handle:
        return json.load(handle)


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def hcl_reasons(text):
    why = []
    if norm(POLICY_LINE) not in norm(text):
        why.append("policy selector for %s absent or changed" % POLICY_REVISION)
    if text.count(LIST_HEAD) != 1:
        why.append("list local resident_audit_write_prefixes not found exactly once")
    else:
        start = text.index(LIST_HEAD)
        end = text.index("\n  ]", start)
        body = text[start + len(LIST_HEAD):end]
        if norm(body) != norm(LIST_BODY):
            why.append("list local body is not the registry-built formula over resident_scopes")
        if "arn:aws:s3:::opal" in text[start:end]:
            why.append("list local holds a typed arn:aws:s3:::opal literal")
    sids = [m.start() for m in re.finditer(r'Sid\s*=\s*"%s"' % SID, text)]
    if len(sids) != 1:
        why.append("statement %s found %d times, expected once" % (SID, len(sids)))
        return why
    pos = sids[0]
    bstart = text.rfind("{", 0, pos)
    bend = text.index("\n      }", pos)
    block = text[bstart:bend]
    if sorted(re.findall(r"^\s*([A-Za-z]+)\s*=", block, re.M)) != sorted(EXPECT_KEYS):
        why.append("statement %s carries keys other than Sid, Effect, Action, Resource" % SID)
    if not re.search(r'^\s*Effect\s*=\s*"Allow"\s*$', block, re.M):
        why.append("statement %s Effect is not Allow" % SID)
    if not re.search(r'^\s*Action\s*=\s*\[\s*"s3:PutObject"\s*\]\s*$', block, re.M):
        why.append("statement %s %s s3:PutObject" % (SID, REASON_ACTION))
    if not re.search(r"^\s*Resource\s*=\s*local\.resident_audit_write_prefixes\s*$", block, re.M):
        why.append("statement %s Resource is not local.resident_audit_write_prefixes" % SID)
    prior = re.findall(r'Sid\s*=\s*"([^"]+)"', text[:pos])
    if not prior or prior[-1] != PREV_SID:
        why.append("statement %s is not placed right after %s" % (SID, PREV_SID))
    rr = text.find('resource "aws_iam_role_policy" "runner_resident"')
    rr_end = text.find("\n}\n", rr)
    if not (0 <= rr < pos < rr_end):
        why.append("statement %s is not inside aws_iam_role_policy.runner_resident" % SID)
    return why


def firm_scopes(scopes_doc):
    out = {}
    for row in scopes_doc["scopes"]:
        tenant = row.get("tenant") or {}
        if row.get("class") == "FIRM" and tenant.get("kind") == "client" and tenant.get("enabled") is True:
            out[row["key"]] = row
    return out


def policy_row(policies_doc):
    rows = [p for p in policies_doc["policies"] if p.get("policy_revision") == POLICY_REVISION]
    if len(rows) != 1:
        raise SystemExit("AUDIT-WRITE-GRANT-BAD policy revision %s found %d times" % (POLICY_REVISION, len(rows)))
    return rows[0]


def family_tier_table(policy):
    fam = policy["families"].get(FAMILY)
    if fam is None:
        return EXPECT_TIER, EXPECT_TABLE
    return fam["tier"], fam["table"]


def tf_prefix(policy, scope):
    fam = policy["families"].get(FAMILY)
    if fam is None:
        return None
    return "arn:aws:s3:::%s/%s/%s/%s/%s/*" % (scope["bucket"], policy["source"], scope["long"],
                                              fam["tier"], fam["table"])


def builder_prefix(naming, policy, scope):
    tier, table = family_tier_table(policy)
    addr = naming.address(policy["source"], scope["long"], tier, table, PARTITION)
    if not addr.startswith("s3://"):
        raise SystemExit("AUDIT-WRITE-GRANT-BAD address() returned %r" % addr)
    return "arn:aws:s3:::%s/*" % addr[len("s3://"):].rsplit("/", 1)[0]


def grant_reasons(naming, scopes, builder_policy, tf_policy):
    why = []
    if not scopes:
        why.append("no FIRM client enabled scope in scopes.json")
    if FAMILY not in tf_policy["families"]:
        why.append("family %s absent from policy %s in reporting_policies.json at this HEAD" % (FAMILY, POLICY_REVISION))
    tf_map = {}
    for key in sorted(scopes):
        scope = scopes[key]
        got = tf_prefix(tf_policy, scope)
        if got is None:
            got = "(no family row)"
        want = builder_prefix(naming, builder_policy, scope)
        tf_map[key] = got
        if got != want:
            why.append("firm %s: prefix %s %s; builder address gives %s" % (key, got, REASON_TABLE, want))
    return why, len(scopes), len(tf_map)


def main(argv=None):
    sys.dont_write_bytecode = True
    parser = argparse.ArgumentParser(description="AR-y-468 resident analysis audit put grant check")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    root = find_root(os.path.dirname(os.path.abspath(__file__)))
    naming = load_naming(root)
    with open(os.path.join(root, TF_REL), encoding="utf-8") as handle:
        text = handle.read()
    scopes = firm_scopes(load_json(root, SCOPES_REL))
    disk_policy = policy_row(load_json(root, POLICIES_REL))
    if args.selftest:
        mutant_a = copy.deepcopy(disk_policy)
        mutant_a["families"][FAMILY] = {"tier": EXPECT_TIER, "table": "analysis_audit_x", "extension": "json",
                                        "unreferenced_days": None, "accepted_ceiling_days": 2555}
        why_a, _, _ = grant_reasons(naming, scopes, disk_policy, mutant_a)
        mutant_b = re.sub(r'(Sid\s*=\s*"%s".*?Action\s*=\s*)\["s3:PutObject"\]' % SID,
                          r'\1["s3:PutObject", "s3:GetObject"]', text, count=1, flags=re.S)
        why_b = hcl_reasons(mutant_b) if mutant_b != text else []
        fires_a = any(REASON_TABLE in reason for reason in why_a)
        fires_b = any(REASON_ACTION in reason for reason in why_b)
        if fires_a and fires_b:
            print("CONTROL-FIRES")
            return 0
        print("CONTROL-DID-NOT-FIRE a=%s b=%s" % (fires_a, fires_b))
        return 1
    why = hcl_reasons(text)
    grant_why, firms, prefixes = grant_reasons(naming, scopes, disk_policy, disk_policy)
    why = why + grant_why
    if why:
        print("AUDIT-WRITE-GRANT-BAD " + "; ".join(why))
        return 1
    print("AUDIT-WRITE-GRANT-OK firms=%d prefixes=%d builder_equal=yes put_only=yes" % (firms, prefixes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
