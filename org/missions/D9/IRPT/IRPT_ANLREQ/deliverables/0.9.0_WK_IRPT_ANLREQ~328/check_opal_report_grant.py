#!/usr/bin/env python3
"""IRPT_ANLREQ AR-y-463: the irpt-status role's read grant on the Opal report PDF family.

Stdlib only, offline, no AWS call. Three checks over this worktree:
  (a) the HCL text of infra/aws/terraform/investor-reporting/ops/iam.tf: the policy selector of
      local.irpt_ycdgen_research_policy (the row revision irpt-ycdgen-research-v1), the local opal_report_family
      built from its YCHARTS_OPAL_REPORT row, the statement ReadRetainedAnalysisFamiliesUnderThePolicyPrefixesOnly
      taking that local in its family list, its actions exactly the two read actions, and no literal
      ycharts_opal_reports anywhere in the file. The cell named irpt-x10-v1 as the row; that premise does not hold
      (lib/tests/test_irpt_destination.py: no OPAL_REPORT_PDF family on irpt-x10-v1), so the check asserts the row
      the registry holds;
  (b) the prefixes are evaluated in Python from the registries (the enabled client firms of data/firm_registry.json,
      the irpt PRODUCT bucket of infra/logic/registry/scopes.json, the policy row) as
      arn:aws:s3:::<bucket>/irpt/<firm_id>/<tier>/<table>/*, and each is compared, firm by firm, with the key that
      lib/opal_naming.py key() builds for the firm's long scope (the key with its partition segment removed).
      The comparison is the one the naming builder gives: the bucket is the same registry value on both sides and
      key() is the builder whose output the prefix must equal. lib/opal_naming.py is loaded BY PATH;
  (c) a real report-PDF key, read from the IRPT_ANLREQ-D2-S224 row of the surprise investigation file, matches
      exactly one computed prefix by fnmatch.

Usage: python -I check_opal_report_grant.py [--selftest]
  --selftest makes two in-memory mutants: (1) the table name of the computed family is changed, (2) a
  s3:PutObject action is added to the statement text. It prints CONTROL-FIRES only when BOTH mutants read BAD.
ASCII only.
"""

import argparse
import copy
import fnmatch
import importlib.util
import json
import os
import re
import sys

REVISION = "irpt-ycdgen-research-v1"
FAMILY = "YCHARTS_OPAL_REPORT"
SID = "ReadRetainedAnalysisFamiliesUnderThePolicyPrefixesOnly"
LOCAL = "opal_report_family"
EXPECT_ACTIONS = ["s3:GetObject", "s3:GetObjectVersion"]
PRODUCT = "irpt"
PARTITION = "PARTITION"
ROW_ID = "IRPT_ANLREQ-D2-S224"
TF_REL = "infra/aws/terraform/investor-reporting/ops/iam.tf"
FIRMS_REL = "data/firm_registry.json"
SCOPES_REL = "infra/logic/registry/scopes.json"
POLICIES_REL = "infra/logic/registry/reporting_policies.json"
NAMING_REL = "lib/opal_naming.py"
INVESTIGATION_REL = "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md"
POLICY_LINE = (
    'irpt_ycdgen_research_policy = one([for p in jsondecode(file("${path.module}/../../../../../infra/logic/'
    'registry/reporting_policies.json")).policies : p if p.policy_revision == "irpt-ycdgen-research-v1"])'
)
LOCAL_LINE = (
    'opal_report_family = "${local.irpt_ycdgen_research_policy.families["YCHARTS_OPAL_REPORT"].tier}/'
    '${local.irpt_ycdgen_research_policy.families["YCHARTS_OPAL_REPORT"].table}"'
)
REAL_KEY_RE = r"irpt/[A-Za-z0-9_.-]+/state/ycharts_opal_reports/ART-[0-9a-f]+/[0-9a-f]+\.pdf"


def find_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(cur, NAMING_REL)) and os.path.isdir(os.path.join(cur, "infra")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("OPAL-REPORT-GRANT-BAD no worktree root above %s" % start)
        cur = parent


def load_naming(root):
    spec = importlib.util.spec_from_file_location("opal_naming_by_path", os.path.join(root, NAMING_REL))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_text(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as handle:
        return handle.read()


def load_json(root, rel):
    return json.loads(read_text(root, rel))


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def sid_positions(text):
    return [m.start() for m in re.finditer(r'\bsid\s*=\s*"%s"' % SID, text)]


def statement_block(text):
    found = sid_positions(text)
    if len(found) != 1:
        return None, -1
    pos = found[0]
    bstart = text.rfind("statement {", 0, pos)
    bend = text.index("\n  }", pos)
    return text[bstart:bend], pos


def hcl_reasons(text):
    why = []
    if norm(POLICY_LINE) not in norm(text):
        why.append("policy selector for %s absent or changed" % REVISION)
    if norm(LOCAL_LINE) not in norm(text):
        why.append("local %s is not built from the %s row of local.irpt_ycdgen_research_policy" % (LOCAL, FAMILY))
    if "ycharts_opal_reports" in text:
        why.append("file holds a literal ycharts_opal_reports")
    block, _ = statement_block(text)
    if block is None:
        why.append("statement %s not found exactly once" % SID)
        return why
    if "opal-data" in block:
        why.append("statement %s holds a typed opal-data literal" % SID)
    if not re.search(r'^\s*actions\s*=\s*\[\s*"s3:GetObject"\s*,\s*"s3:GetObjectVersion"\s*\]\s*$', block, re.M):
        why.append("statement %s actions are not exactly s3:GetObject and s3:GetObjectVersion" % SID)
    concat = re.search(r"concat\(\[[^\]]*\],\s*\[([^\]]*)\]\)", block)
    if concat is None:
        why.append("statement %s family list is not a concat of two lists" % SID)
    else:
        members = [item.strip() for item in concat.group(1).split(",")]
        if "local.%s" % LOCAL not in members:
            why.append("statement %s family list does not include local.%s" % (SID, LOCAL))
    return why


def firm_ids(firms_doc):
    return [row["firm_id"] for row in firms_doc["firms"] if row.get("kind") == "client" and row.get("enabled") is True]


def product_bucket(scopes_doc):
    rows = [row for row in scopes_doc["scopes"] if row.get("key") == PRODUCT and row.get("class") == "PRODUCT"]
    if len(rows) != 1:
        raise SystemExit("OPAL-REPORT-GRANT-BAD product scope %s found %d times" % (PRODUCT, len(rows)))
    return rows[0]["bucket"]


def long_scope(scopes_doc, firm_id):
    rows = [row for row in scopes_doc["scopes"] if row.get("key") == firm_id]
    if len(rows) != 1:
        raise SystemExit("OPAL-REPORT-GRANT-BAD scope row %s found %d times" % (firm_id, len(rows)))
    return rows[0]["long"]


def policy_row(policies_doc):
    rows = [p for p in policies_doc["policies"] if p.get("policy_revision") == REVISION]
    if len(rows) != 1:
        raise SystemExit("OPAL-REPORT-GRANT-BAD policy revision %s found %d times" % (REVISION, len(rows)))
    return rows[0]


def tf_prefix(bucket, firm_id, policy):
    fam = policy["families"][FAMILY]
    return "arn:aws:s3:::%s/%s/%s/%s/%s/*" % (bucket, PRODUCT, firm_id, fam["tier"], fam["table"])


def builder_prefix(naming, bucket, scope_long, policy):
    fam = policy["families"][FAMILY]
    built = naming.key(policy["source"], scope_long, fam["tier"], fam["table"], PARTITION)
    return "arn:aws:s3:::%s/%s/*" % (bucket, built.rsplit("/", 1)[0])


def real_key(root):
    section = read_text(root, INVESTIGATION_REL)
    start = section.find("## %s -- " % ROW_ID)
    if start < 0:
        return None
    nxt = section.find("\n## ", start + 1)
    body = section[start: nxt if nxt > 0 else len(section)]
    match = re.search(REAL_KEY_RE, body)
    return match.group(0) if match else None


def grant_reasons(naming, firms_doc, scopes_doc, policies_doc, tf_policy, key):
    why = []
    bucket = product_bucket(scopes_doc)
    ids = firm_ids(firms_doc)
    if not ids:
        why.append("no enabled client firm in data/firm_registry.json")
    disk = policy_row(policies_doc)
    prefixes = {}
    for firm_id in ids:
        scope_long = long_scope(scopes_doc, firm_id)
        got = tf_prefix(bucket, firm_id, tf_policy)
        want = builder_prefix(naming, bucket, scope_long, disk)
        prefixes[firm_id] = got
        if got != want:
            why.append("firm %s: computed prefix %s differs from builder %s" % (firm_id, got, want))
    if key is None:
        why.append("no real %s key in row %s" % (FAMILY, ROW_ID))
    else:
        real_arn = "arn:aws:s3:::%s/%s" % (bucket, key)
        hits = [p for p in prefixes.values() if fnmatch.fnmatchcase(real_arn, p)]
        if len(hits) != 1:
            why.append("real key %s matches %d computed prefixes, expected 1" % (key, len(hits)))
    return why, len(ids), len(prefixes)


def selftest(root, naming, firms_doc, scopes_doc, policies_doc, text, key):
    mutant_table = copy.deepcopy(policy_row(policies_doc))
    mutant_table["families"][FAMILY]["table"] = "ycharts_opal_reports_mutant"
    table_why, _, _ = grant_reasons(naming, firms_doc, scopes_doc, policies_doc, mutant_table, key)
    found = sid_positions(text)
    if len(found) != 1:
        return False
    act = text.index("actions = [", found[0])
    line_end = text.index("\n", act)
    put_text = text[:act] + 'actions = ["s3:GetObject", "s3:GetObjectVersion", "s3:PutObject"]' + text[line_end:]
    put_why = hcl_reasons(put_text)
    return bool(table_why) and bool(put_why)


def main(argv=None):
    sys.dont_write_bytecode = True
    parser = argparse.ArgumentParser(description="AR-y-463 status role Opal report grant check")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    root = find_root(os.path.dirname(os.path.abspath(__file__)))
    naming = load_naming(root)
    text = read_text(root, TF_REL)
    firms_doc = load_json(root, FIRMS_REL)
    scopes_doc = load_json(root, SCOPES_REL)
    policies_doc = load_json(root, POLICIES_REL)
    key = real_key(root)
    if args.selftest:
        if selftest(root, naming, firms_doc, scopes_doc, policies_doc, text, key):
            print("CONTROL-FIRES")
            return 0
        print("CONTROL-DID-NOT-FIRE")
        return 1
    why = hcl_reasons(text)
    grant_why, firms, prefixes = grant_reasons(
        naming, firms_doc, scopes_doc, policies_doc, policy_row(policies_doc), key
    )
    why = why + grant_why
    if why:
        print("OPAL-REPORT-GRANT-BAD " + "; ".join(why))
        return 1
    print("OPAL-REPORT-GRANT-OK firms=%d prefixes=%d builder_equal=yes real_key_covered=yes" % (firms, prefixes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
