#!/usr/bin/env python3
"""IRPT_ANLREQ AR-y-468: the resident role's put-only grant on the analysis audit record.

Stdlib only, offline, no AWS call (git is read for the trunk base only). Checks over this worktree:
  (a) the HCL text of infra/aws/terraform/investor-reporting/ycharts/resident.tf: the list local
      resident_audit_write_prefixes is built from resident_scopes and the policy row selected by
      irpt-anlreq-x10-v1 (no arn:aws:s3:::opal literal), and the statement WriteTheAnalysisAudit has
      Effect Allow, Action exactly ["s3:PutObject"], Resource local.resident_audit_write_prefixes, and sits
      right after ReadTheAnalysisCommentaryDraft inside aws_iam_role_policy.runner_resident.
  (b) AMENDMENT 1 (TO-AR-y-468, trunk a71b17d96d): for each enabled client firm the Terraform prefix
      "arn:aws:s3:::BUCKET/<source>/<firm>/<tier>/<table>/*" (BUCKET stands for local.resident_bucket, remote
      state, not read here) is compared with lib/opal_naming.py reporting_destination(firm, ANALYSIS_AUDIT,
      ART_SAMPLE, SHA_SAMPLE, policy_revision=irpt-anlreq-x10-v1) (loaded BY PATH): the key minus its last
      two parts (artifact id and sha256 file) plus /*. The writer's bucket must equal the product scope's
      bucket in scopes.json (the product_scope of the policy row), which is the bucket the reporting
      bucket is derived from (core/reporting_storage.tf). The firm buckets are not compared.
      The family row must exist in the policy row; if it is absent the report says so.
  (c) AMENDMENT 2 (trunk 00f56f44ba): the KMS statement ReportEncryptionViaS3ForResidentFamiliesOnly
      carries local.resident_audit_write_prefixes as the fourth argument of its encryption-context concat,
      after the three existing arguments, and no other statement's text differs from the trunk base
      5143b9b2565 except that one added argument. WriteTheAnalysisAudit is the only added statement.

Usage: python -I check_audit_write_grant.py [--selftest]
  --selftest mutates in memory (A) the table name of the family, compared with the writer, (B) the statement
  Action by adding s3:GetObject, and (C) the KMS concat by dropping the audit prefixes. It prints
  CONTROL-FIRES only when all three read BAD, each for its own reason. ASCII only.
"""

import argparse
import copy
import importlib.util
import json
import os
import re
import subprocess
import sys

POLICY_REVISION = "irpt-anlreq-x10-v1"
FAMILY = "ANALYSIS_AUDIT"
EXPECT_TIER = "platinum"
SID = "WriteTheAnalysisAudit"
PREV_SID = "ReadTheAnalysisCommentaryDraft"
KMS_SID = "ReportEncryptionViaS3ForResidentFamiliesOnly"
TRUNK_BASE = "5143b9b2565"
BUCKET = "BUCKET"
ART_SAMPLE = "ART-" + "a" * 64
SHA_SAMPLE = "b" * 64
TF_REL = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"
SCOPES_REL = "infra/logic/registry/scopes.json"
POLICIES_REL = "infra/logic/registry/reporting_policies.json"
NAMING_REL = "lib/opal_naming.py"
EXPECT_KEYS = ["Sid", "Effect", "Action", "Resource"]
AUDIT_ARG = "local.resident_audit_write_prefixes"
KMS_ARGS = [
    "local.resident_write_prefixes",
    "local.resident_read_prefixes",
    "local.ycdgen_opal_report_prefixes",
    AUDIT_ARG,
]
POLICY_LINE = (
    'resident_commentary_policy = one([for p in jsondecode(file("${path.module}/../../../../logic/registry/'
    'reporting_policies.json")).policies : p if p.policy_revision == "irpt-anlreq-x10-v1"])'
)
LIST_HEAD = "resident_audit_write_prefixes = ["
LIST_BODY = (
    'for scope_key in keys(local.resident_scopes) : '
    '"arn:aws:s3:::${local.resident_bucket}/${local.resident_commentary_policy.source}/'
    '${local.resident_scopes[scope_key].long}/'
    '${local.resident_commentary_policy.families["ANALYSIS_AUDIT"].tier}/'
    '${local.resident_commentary_policy.families["ANALYSIS_AUDIT"].table}/*"'
)
KMS_CONCAT = re.compile(r'StringLike\s*=\s*\{\s*"kms:EncryptionContext:aws:s3:arn"\s*=\s*concat\(([^)]*)\)\s*\}')
REASON_TABLE = "differs from builder"
REASON_ACTION = "Action is not exactly"
REASON_KMS = "does not include local.resident_audit_write_prefixes"


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


def trunk_base_text(root):
    proc = subprocess.run(["git", "show", "%s:%s" % (TRUNK_BASE, TF_REL)], cwd=root,
                          capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit("AUDIT-WRITE-GRANT-BAD trunk base %s unreadable: rc=%d" % (TRUNK_BASE, proc.returncode))
    return proc.stdout


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


def kms_reasons(text):
    found = KMS_CONCAT.search(text)
    if not found:
        return ["KMS statement %s encryption-context concat not found" % KMS_SID]
    args = [part.strip() for part in found.group(1).split(",")]
    if AUDIT_ARG not in args:
        return ["KMS encryption-context concat %s" % REASON_KMS]
    if args != KMS_ARGS:
        return ["KMS encryption-context concat differs from the expected four arguments"]
    sid_pos = text.find('Sid      = "%s"' % KMS_SID)
    if sid_pos < 0 or not (sid_pos < found.start() < text.index("\n      }", sid_pos)):
        return ["KMS encryption-context concat is not inside statement %s" % KMS_SID]
    return []


def statements(text):
    out = {}
    for match in re.finditer(r'Sid\s*=\s*"([^"]+)"', text):
        pos = match.start()
        bstart = text.rfind("{", 0, pos)
        bend = text.find("\n      }", pos)
        if bend < 0:
            continue
        out[match.group(1)] = norm(text[bstart:bend])
    return out


def statement_reasons(text, base_text):
    why = []
    head = statements(text)
    base = statements(base_text)
    for sid in sorted(set(base) - set(head)):
        why.append("statement %s removed since the trunk base" % sid)
    extra = sorted(set(head) - set(base) - {SID})
    if extra:
        why.append("statement(s) added beyond %s: %s" % (SID, ", ".join(extra)))
    for sid in sorted(set(base) & set(head)):
        if sid == KMS_SID:
            if norm(head[sid]).replace(norm(", " + AUDIT_ARG), "") != base[sid]:
                why.append("statement %s changed by more than the audit argument" % sid)
        elif head[sid] != base[sid]:
            why.append("statement %s text changed since the trunk base" % sid)
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


def tf_prefix(policy, scope):
    # The Terraform bucket is local.resident_bucket (remote state), so its side carries the placeholder BUCKET.
    fam = policy["families"].get(FAMILY)
    if fam is None:
        return None
    return "arn:aws:s3:::%s/%s/%s/%s/%s/*" % (BUCKET, policy["source"], scope["long"], fam["tier"], fam["table"])


def product_bucket(scopes_doc, policy):
    rows = [r for r in scopes_doc["scopes"] if r.get("key") == policy["product_scope"]]
    if len(rows) != 1:
        raise SystemExit("AUDIT-WRITE-GRANT-BAD product scope %s found %d times" % (policy["product_scope"], len(rows)))
    return rows[0]["bucket"]


def builder_prefix(naming, firm):
    # AMENDMENT 1 (TO-AR-y-468): the writer's own destination. reporting_destination returns the bucket and the
    # key of one object; the prefix is the key minus its last two parts (the artifact id and the sha256 file),
    # plus /*. The bucket is returned too and is compared with the product scope bucket by the caller.
    bucket, path = naming.reporting_destination(firm, FAMILY, ART_SAMPLE, SHA_SAMPLE, policy_revision=POLICY_REVISION)
    parts = path.split("/")
    prefix_key = "/".join(parts[:-2])
    return bucket, "arn:aws:s3:::%s/%s/*" % (BUCKET, prefix_key)


def grant_reasons(naming, scopes, tf_policy, scopes_doc):
    why = []
    if not scopes:
        why.append("no FIRM client enabled scope in scopes.json")
    if FAMILY not in tf_policy["families"]:
        why.append("family %s absent from policy %s in reporting_policies.json at this HEAD" % (FAMILY, POLICY_REVISION))
    expect_bucket = product_bucket(scopes_doc, tf_policy)
    tf_map = {}
    for key in sorted(scopes):
        got = tf_prefix(tf_policy, scopes[key])
        if got is None:
            got = "(no family row)"
        built_bucket, want = builder_prefix(naming, key)
        tf_map[key] = got
        if built_bucket != expect_bucket:
            why.append("firm %s: writer bucket %s is not the product bucket %s" % (key, built_bucket, expect_bucket))
        if got != want:
            why.append("firm %s: prefix %s %s; reporting_destination gives %s" % (key, got, REASON_TABLE, want))
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
    base_text = trunk_base_text(root)
    scopes_doc = load_json(root, SCOPES_REL)
    scopes = firm_scopes(scopes_doc)
    disk_policy = policy_row(load_json(root, POLICIES_REL))
    if args.selftest:
        mutant_a = copy.deepcopy(disk_policy)
        mutant_a["families"][FAMILY] = {"tier": EXPECT_TIER, "table": "analysis_audit_x", "extension": "json",
                                        "unreferenced_days": None, "accepted_ceiling_days": 2555}
        why_a, _, _ = grant_reasons(naming, scopes, mutant_a, scopes_doc)
        mutant_b = re.sub(r'(Sid\s*=\s*"%s".*?Action\s*=\s*)\["s3:PutObject"\]' % SID,
                          r'\1["s3:PutObject", "s3:GetObject"]', text, count=1, flags=re.S)
        why_b = hcl_reasons(mutant_b) if mutant_b != text else []
        mutant_c = text.replace(", %s)" % AUDIT_ARG, ")", 1)
        why_c = kms_reasons(mutant_c) if mutant_c != text else []
        fires_a = any(REASON_TABLE in reason for reason in why_a)
        fires_b = any(REASON_ACTION in reason for reason in why_b)
        fires_c = any(REASON_KMS in reason for reason in why_c)
        if fires_a and fires_b and fires_c:
            print("CONTROL-FIRES")
            return 0
        print("CONTROL-DID-NOT-FIRE a=%s b=%s c=%s" % (fires_a, fires_b, fires_c))
        return 1
    why = hcl_reasons(text) + kms_reasons(text) + statement_reasons(text, base_text)
    grant_why, firms, prefixes = grant_reasons(naming, scopes, disk_policy, scopes_doc)
    why = why + grant_why
    if why:
        print("AUDIT-WRITE-GRANT-BAD " + "; ".join(why))
        return 1
    print("AUDIT-WRITE-GRANT-OK firms=%d prefixes=%d builder_equal=yes put_only=yes" % (firms, prefixes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
