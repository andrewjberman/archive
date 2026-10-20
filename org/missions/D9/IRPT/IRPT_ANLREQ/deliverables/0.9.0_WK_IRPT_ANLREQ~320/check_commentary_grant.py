#!/usr/bin/env python3
"""IRPT_ANLREQ AR-y-445: the resident role's read grant on the ANALYSIS_COMMENTARY draft.

Stdlib only, offline, no AWS call. Three checks over this worktree:
  (a) the HCL text of infra/aws/terraform/investor-reporting/ycharts/resident.tf: the policy selector, the
      prefix list and the statement ReadTheAnalysisCommentaryDraft have the shape the cell names;
  (b) the prefix formula is evaluated in Python from the registry (scopes.json, reporting_policies.json),
      and each firm's prefix is compared with the naming builder's key (lib/opal_naming.py key(), loaded
      BY PATH). The Terraform bucket is local.resident_bucket (remote state), not typed in the file, so the
      comparison is made with a BUCKET placeholder on both sides;
  (c) run 6's real commentary prefix lies under one of the evaluated prefixes.

Usage: python -I check_commentary_grant.py [--selftest]
  --selftest re-evaluates (b) with the table name changed in memory to analysis_commentary and prints
  CONTROL-FIRES only when that variant is BAD.
ASCII only.
"""

import argparse
import copy
import importlib.util
import json
import os
import re
import sys

POLICY_REVISION = "irpt-anlreq-x10-v1"
FAMILY = "ANALYSIS_COMMENTARY"
SID = "ReadTheAnalysisCommentaryDraft"
PREV_SID = "ReadFrozenCompositionAndNormalizedInput"
RUN6_PREFIX = "irpt/49financial/state/analysis_commentaries/"
PARTITION = "PARTITION"
BUCKET = "BUCKET"
TF_REL = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"
SCOPES_REL = "infra/logic/registry/scopes.json"
POLICIES_REL = "infra/logic/registry/reporting_policies.json"
NAMING_REL = "lib/opal_naming.py"
EXPECT_ACTIONS = ["s3:GetObject", "s3:GetObjectVersion"]
EXPECT_KEYS = ["Sid", "Effect", "Action", "Resource"]
POLICY_LINE = (
    'resident_commentary_policy = one([for p in jsondecode(file("${path.module}/../../../../logic/registry/'
    'reporting_policies.json")).policies : p if p.policy_revision == "irpt-anlreq-x10-v1"])'
)
LIST_HEAD = "resident_commentary_read_prefixes = ["
LIST_BODY = (
    'for scope_key in keys(local.resident_scopes) : '
    '"arn:aws:s3:::${local.resident_bucket}/${local.resident_commentary_policy.source}/'
    '${local.resident_scopes[scope_key].long}/'
    '${local.resident_commentary_policy.families["ANALYSIS_COMMENTARY"].tier}/'
    '${local.resident_commentary_policy.families["ANALYSIS_COMMENTARY"].table}/*"'
)


def find_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(cur, NAMING_REL)) and os.path.isdir(os.path.join(cur, "infra")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("COMMENTARY-GRANT-BAD no worktree root above %s" % start)
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
        why.append("list local resident_commentary_read_prefixes not found exactly once")
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
    if not re.search(r'^\s*Action\s*=\s*\[\s*"s3:GetObject"\s*,\s*"s3:GetObjectVersion"\s*\]\s*$', block, re.M):
        why.append("statement %s Action is not exactly s3:GetObject and s3:GetObjectVersion" % SID)
    if not re.search(r"^\s*Resource\s*=\s*local\.resident_commentary_read_prefixes\s*$", block, re.M):
        why.append("statement %s Resource is not local.resident_commentary_read_prefixes" % SID)
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
        raise SystemExit("COMMENTARY-GRANT-BAD policy revision %s found %d times" % (POLICY_REVISION, len(rows)))
    return rows[0]


def tf_prefix(policy, scope_long):
    fam = policy["families"][FAMILY]
    return "arn:aws:s3:::%s/%s/%s/%s/%s/*" % (BUCKET, policy["source"], scope_long, fam["tier"], fam["table"])


def builder_prefix(naming, policy, scope_long):
    fam = policy["families"][FAMILY]
    built = naming.key(policy["source"], scope_long, fam["tier"], fam["table"], PARTITION)
    return "arn:aws:s3:::%s/%s/*" % (BUCKET, built.rsplit("/", 1)[0])


def grant_reasons(naming, scopes, disk_policy, tf_policy):
    why = []
    if not scopes:
        why.append("no FIRM client enabled scope in scopes.json")
    tf_map = {}
    for key in sorted(scopes):
        long_name = scopes[key]["long"]
        got = tf_prefix(tf_policy, long_name)
        want = builder_prefix(naming, disk_policy, long_name)
        tf_map[key] = got
        if got != want:
            why.append("firm %s: formula %s differs from builder %s" % (key, got, want))
    run6 = "arn:aws:s3:::%s/%s" % (BUCKET, RUN6_PREFIX)
    if not any(run6.startswith(prefix[:-1]) for prefix in tf_map.values()):
        why.append("run 6 commentary prefix %s is under no evaluated prefix" % RUN6_PREFIX)
    return why, len(scopes), len(tf_map)


def main(argv=None):
    sys.dont_write_bytecode = True
    parser = argparse.ArgumentParser(description="AR-y-445 resident commentary read grant check")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    root = find_root(os.path.dirname(os.path.abspath(__file__)))
    naming = load_naming(root)
    with open(os.path.join(root, TF_REL), encoding="utf-8") as handle:
        text = handle.read()
    scopes = firm_scopes(load_json(root, SCOPES_REL))
    disk_policy = policy_row(load_json(root, POLICIES_REL))
    if args.selftest:
        variant = copy.deepcopy(disk_policy)
        variant["families"][FAMILY]["table"] = "analysis_commentary"
        why, _, _ = grant_reasons(naming, scopes, disk_policy, variant)
        if why:
            print("CONTROL-FIRES")
            return 0
        print("CONTROL-DID-NOT-FIRE")
        return 1
    why = hcl_reasons(text)
    grant_why, firms, prefixes = grant_reasons(naming, scopes, disk_policy, disk_policy)
    why = why + grant_why
    if why:
        print("COMMENTARY-GRANT-BAD " + "; ".join(why))
        return 1
    print("COMMENTARY-GRANT-OK firms=%d prefixes=%d builder_equal=yes" % (firms, prefixes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
