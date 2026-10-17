"""IRPT_DASHBD round 139, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the Inflection transaction policy moves to a NEW narrow role the runner assumes (cell DB-f-2704).

  The CTO's ruling (msg 10542, route B): opal-data-inflection's DenyForeignFirmPrincipals does not admit `inf-gold-layer-ec2-role`, so the four-statement policy of DB-f-2501 and DB-f-2603
  moves to a NEW role whose builder-made name matches role/*-inf-* (opal_naming.name("orion", "inflection", "account-transaction", "role") = orion-inf-account-transaction-role);
  the runner role gets ONE sts:AssumeRole on it; the launcher assumes it (cell DB-f-2705). The cross-firm fence and the registry are not touched.
  `iam.tf` of the inf-pipeline root changes as follows against the pinned base (the trunk's iam.tf after DB-f-2603):
    - a module for the role name (kind role) and one for the assume policy's name (kind policy), both from ../modules/opal_name; a local for the fixed session name and one for the role ARN;
    - `aws_iam_role.inf_account_transaction`: trust = the runner role (`aws_iam_role.inf_gold_layer.arn`) ONLY, `sts:AssumeRole`, conditioned on the fixed session name;
    - the existing `aws_iam_role_policy.inf_gold_layer_account_transaction` keeps its four statements BYTE FOR BYTE and its name, and its `role` line points at the NEW role;
    - `aws_iam_role_policy` on the runner role with ONE statement, `sts:AssumeRole` on the new role's ARN, and nothing else.
  The plan this makes: 3 to add (the role, its policy, the runner's assume policy), 0 to change, 0 to destroy. Every other file of the root is byte-identical. Nothing is planned or applied here.

  DBF139-4-AC1  the root's 46 other files are byte-identical; iam.tf differs from the pinned base only by additions plus the changes inside the 1b region (the removed lines all lie in it)
  DBF139-4-AC2  the new role: builder names (kind role / policy), the trust (the runner role only, the fixed session name), the existing policy now on the new role with S1..S4 unchanged
  DBF139-4-AC3  the runner role's assume policy: exactly one statement, sts:AssumeRole, on the new role's ARN only; no data action; no wildcard; no typed name

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <repo_root>           the pure helpers on synthetic arms
"""
import difflib
import importlib.util
import json
import re
import sys
from pathlib import Path

R136 = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/"
R139 = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r139/"
BASE_IAM = R139 + "inf_iam_r139_base.tf.txt"
BASE_SHA256 = "89e061e51fba303150e44b26ea3ffe766bdd151bd33a4507d865b30e089d5e61"
MANIFEST = R136 + "inf_pipeline_base_manifest.json"
SESSION_NAME = "inf-g-01-account-transaction"
POLICY_RESOURCE = "inf_gold_layer_account_transaction"
SIDS = ["S1ReadOrionInflectionTransactionsSilverOnly", "S2ListOrionInflectionTransactionsSilverOnly", "S3PutInflectionAccountTransactionGoldOnly",
        "S4ListInflectionAccountTransactionGoldOnly"]
REGION_START = "# 1b. Inflection account_transaction gold step"
REGION_END_RE = re.compile(r'^resource "aws_iam_role_policy" "inf_gold_layer_runner_shared" \{', re.M)


def _load_base():
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("p137_inf_tf_for_role", str(here.parent / "r136" / "p137_inf_tf.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = _load_base()
Fail, need, sha, read = B.Fail, B.need, B.sha, B.read


def region_lines(text):
    """(first, last) 1-based line numbers of the 1b region: from its header comment through the line before the next resource (the runner_shared policy)."""
    lines = text.splitlines()
    start = next((i + 1 for i, ln in enumerate(lines) if ln.startswith(REGION_START)), None)
    m = REGION_END_RE.search(text)
    end = text[:m.start()].count("\n") if m else None
    return start, end


def removed_outside_region(base, new):
    """Base lines that were removed or changed and lie OUTSIDE the 1b region of the base: must be none."""
    first, last = region_lines(base)
    if first is None or last is None:
        return ["the 1b region cannot be found in the base"]
    out = []
    sm = difflib.SequenceMatcher(None, base.splitlines(), new.splitlines(), autojunk=False)
    for tag, i1, i2, _j1, _j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            for k in range(i1, i2):
                if not (first - 1 <= k + 0 <= last):
                    out.append("base line %d outside the 1b region was removed or changed" % (k + 1))
    return out


def resource_block(text, rtype, label):
    m = re.search(r'resource\s+"%s"\s+"%s"\s*\{' % (re.escape(rtype), re.escape(label)), text)
    if not m:
        return None
    depth, i = 0, m.end() - 1
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[m.start():j + 1]
    return None


def module_ok(text, kind):
    """A module from ../modules/opal_name with system orion, scope inflection, function account-transaction[-assume] and the kind; returns the module's label or None."""
    for m in re.finditer(r'module\s+"([A-Za-z0-9_]+)"\s*\{([^{}]*)\}', text, re.S):
        body = m.group(2)
        if "../modules/opal_name" in body and re.search(r'kind\s*=\s*"%s"' % kind, body) and re.search(r'system\s*=\s*"orion"', body) \
                and re.search(r'scope\s*=\s*"inflection"', body) and re.search(r'function\s*=\s*"account-transaction(-assume)?"', body):
            yield m.group(1), body


def semantic_problems(base, new):
    pr = []
    roles = [(lab, b) for lab, b in module_ok(new, "role")]
    pols = [(lab, b) for lab, b in module_ok(new, "policy") if "account-transaction-assume" in b]
    if len(roles) != 1:
        pr.append("exactly one opal_name module of kind role for the account-transaction role is required (orion, inflection, account-transaction)")
    if len(pols) != 1:
        pr.append("exactly one opal_name module of kind policy for the assume policy (function account-transaction-assume) is required")
    if not re.search(r'txn_session_name\s*=\s*"%s"' % re.escape(SESSION_NAME), new):
        pr.append('a local txn_session_name = "%s" is required (the launcher\'s fixed session name)' % SESSION_NAME)
    if not re.search(r'txn_role_arn\s*=\s*"arn:aws:iam::\$\{local\.account_id\}:role/\$\{module\.[A-Za-z0-9_]+\.name\}"', new):
        pr.append("a local txn_role_arn built from local.account_id and the role module's name is required")
    role = resource_block(new, "aws_iam_role", "inf_account_transaction")
    if role is None:
        pr.append('resource "aws_iam_role" "inf_account_transaction" is required')
    else:
        if roles and not re.search(r"name\s*=\s*module\.%s\.name" % re.escape(roles[0][0]), role):
            pr.append("the role's name must be module.<role module>.name")
        if "aws_iam_role.inf_gold_layer.arn" not in role or '"*"' in role or "Service" in role:
            pr.append("the trust must name aws_iam_role.inf_gold_layer.arn ONLY (no wildcard, no service principal)")
        if role.count("sts:AssumeRole") != 1 or "sts:RoleSessionName" not in role or "local.txn_session_name" not in role:
            pr.append("the trust must be one sts:AssumeRole conditioned on sts:RoleSessionName = local.txn_session_name")
    pol_new = resource_block(new, "aws_iam_role_policy", POLICY_RESOURCE)
    pol_old = resource_block(base, "aws_iam_role_policy", POLICY_RESOURCE)
    if pol_new is None or pol_old is None:
        pr.append("the existing policy resource %s must be present in the base and in the new file" % POLICY_RESOURCE)
    else:
        if not re.search(r"role\s*=\s*aws_iam_role\.inf_account_transaction\.id", pol_new):
            pr.append("the existing policy's role line must point at aws_iam_role.inf_account_transaction.id")
        for sid in SIDS:
            a, b = B.statement_text(pol_old, sid), B.statement_text(pol_new, sid)
            if a is None or b is None or a != b:
                pr.append("statement %s must be present and byte-for-byte unchanged" % sid)
        if re.search(r"name\s*=\s*module\.account_transaction_policy_name\.name", pol_new) is None:
            pr.append("the existing policy keeps name = module.account_transaction_policy_name.name")
    assume = None
    for m in re.finditer(r'resource\s+"aws_iam_role_policy"\s+"([A-Za-z0-9_]+)"', new):
        if m.group(1) not in (POLICY_RESOURCE, "inf_gold_layer_runner_shared") and "txn_role_arn" in (resource_block(new, "aws_iam_role_policy", m.group(1)) or ""):
            assume = resource_block(new, "aws_iam_role_policy", m.group(1))
    if assume is None:
        pr.append("a runner-role aws_iam_role_policy carrying local.txn_role_arn (the assume policy) is required")
    else:
        if not re.search(r"role\s*=\s*aws_iam_role\.inf_gold_layer\.id", assume):
            pr.append("the assume policy must attach to the runner role aws_iam_role.inf_gold_layer")
        if pols and not re.search(r"name\s*=\s*module\.%s\.name" % re.escape(pols[0][0]), assume):
            pr.append("the assume policy's name must be module.<assume module>.name")
        acts = re.findall(r'"([a-z0-9]+:[A-Za-z*]+)"', assume)
        if acts != ["sts:AssumeRole"]:
            pr.append("the assume policy must carry exactly the action sts:AssumeRole: %r" % acts)
        if assume.count("Sid") != 1 or re.search(r'Resource\s*=\s*"?\*"?|Resource\s*=\s*\[\s*"\*"\s*\]', assume) or "opal-data-" in assume:
            pr.append("the assume policy must carry ONE statement on local.txn_role_arn, no wildcard, no typed bucket")
        if "local.txn_role_arn" not in assume:
            pr.append("the assume policy's Resource must be local.txn_role_arn")
    return pr


def ac1(root):
    man = json.loads(read(root, MANIFEST))
    D = man["root"] + "/"
    bad = [f for f, want in man["others"].items() if not (Path(root, D + f).is_file() and sha(Path(root, D + f).read_bytes()) == want)]
    need(not bad, "files of the root must be byte-identical to the base: %s" % ", ".join(bad[:5]))
    base = read(root, BASE_IAM)
    need(sha(base.encode("utf-8")) == BASE_SHA256, "the pinned iam.tf base copy is not the base the order names (sha256)")
    new = read(root, D + "iam.tf")
    need(new != base, "iam.tf is unchanged from the base")
    added = [ln[1:] for ln in difflib.unified_diff(base.splitlines(), new.splitlines(), lineterm="", n=0) if ln.startswith("+") and not ln.startswith("+++")]
    need(all(x.isascii() for x in added), "every line this cell adds must be ASCII")
    need("\r" not in new, "iam.tf must keep LF line endings")
    pr = removed_outside_region(base, new)
    need(not pr, "; ".join(pr[:4]))


def ac2(root):
    pr = [p for p in semantic_problems(read(root, BASE_IAM), read(root, "infra/aws/terraform/inf-pipeline/iam.tf")) if "assume policy" not in p and "runner-role aws_iam_role_policy" not in p]
    need(not pr, "; ".join(pr))


def ac3(root):
    pr = [p for p in semantic_problems(read(root, BASE_IAM), read(root, "infra/aws/terraform/inf-pipeline/iam.tf"))
          if "assume policy" in p or "runner-role aws_iam_role_policy" in p or "txn_role_arn" in p]
    need(not pr, "; ".join(pr))


def reference(base):
    """A reference edit for the selftest and the positive control."""
    out = base
    mods = ('module "account_transaction_role_name" {\n  source   = "../modules/opal_name"\n  system   = "orion"\n  scope    = "inflection"\n  function = "account-transaction"\n  kind     = "role"\n}\n\n'
            'module "account_transaction_assume_policy_name" {\n  source   = "../modules/opal_name"\n  system   = "orion"\n  scope    = "inflection"\n  function = "account-transaction-assume"\n  kind     = "policy"\n}\n\n')
    anchor = 'module "account_transaction_policy_name" {'
    assert out.count(anchor) == 1
    out = out.replace(anchor, mods + anchor)
    la = '  txn_gold_list_prefixes  = [local.txn_gold_key, "${local.txn_gold_key}/*"]\n'
    assert out.count(la) == 1
    out = out.replace(la, la + '\n  txn_session_name = "%s"\n  txn_role_arn     = "arn:aws:iam::${local.account_id}:role/${module.account_transaction_role_name.name}"\n' % SESSION_NAME)
    role = ('resource "aws_iam_role" "inf_account_transaction" {\n  name = module.account_transaction_role_name.name\n  assume_role_policy = jsonencode({\n    Version = "2012-10-17"\n    Statement = [{\n'
            '      Effect    = "Allow"\n      Principal = { AWS = aws_iam_role.inf_gold_layer.arn }\n      Action    = "sts:AssumeRole"\n'
            '      Condition = { StringEquals = { "sts:RoleSessionName" = local.txn_session_name } }\n    }]\n  })\n}\n\n')
    ra = 'resource "aws_iam_role_policy" "inf_gold_layer_account_transaction" {\n  name = module.account_transaction_policy_name.name\n  role = aws_iam_role.inf_gold_layer.id\n'
    assert out.count(ra) == 1
    out = out.replace(ra, role + ra.replace("aws_iam_role.inf_gold_layer.id", "aws_iam_role.inf_account_transaction.id"))
    assume = ('resource "aws_iam_role_policy" "inf_gold_layer_assume_account_transaction" {\n  name = module.account_transaction_assume_policy_name.name\n  role = aws_iam_role.inf_gold_layer.id\n'
              '  policy = jsonencode({\n    Version = "2012-10-17"\n    Statement = [{\n      Sid      = "AssumeTheAccountTransactionRoleOnly"\n      Effect   = "Allow"\n'
              '      Action   = ["sts:AssumeRole"]\n      Resource = [local.txn_role_arn]\n    }]\n  })\n}\n\n')
    rs = 'resource "aws_iam_role_policy" "inf_gold_layer_runner_shared" {'
    assert out.count(rs) == 1
    return out.replace(rs, assume + rs)


def selftest(root):
    bad = count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    base = read(root, BASE_IAM)
    good = reference(base)
    arm("reference-semantic-green", semantic_problems(base, good), [])
    arm("reference-removed-outside", removed_outside_region(base, good), [])
    arm("unchanged-red", len(semantic_problems(base, base)) >= 1, True)
    arm("trust-wildcard-red", len(semantic_problems(base, good.replace("Principal = { AWS = aws_iam_role.inf_gold_layer.arn }", 'Principal = { AWS = "*" }'))) >= 1, True)
    arm("no-session-condition-red", len(semantic_problems(base, good.replace('      Condition = { StringEquals = { "sts:RoleSessionName" = local.txn_session_name } }\n', ""))) >= 1, True)
    arm("policy-still-on-runner-red", len(semantic_problems(base, good.replace("role = aws_iam_role.inf_account_transaction.id", "role = aws_iam_role.inf_gold_layer.id"))) >= 1, True)
    arm("assume-extra-action-red", len(semantic_problems(base, good.replace('Action   = ["sts:AssumeRole"]\n      Resource = [local.txn_role_arn]', 'Action   = ["sts:AssumeRole", "s3:GetObject"]\n      Resource = [local.txn_role_arn]'))) >= 1, True)
    arm("assume-wildcard-red", len(semantic_problems(base, good.replace("Resource = [local.txn_role_arn]", 'Resource = ["*"]'))) >= 1, True)
    arm("s2-changed-red", len(semantic_problems(base, good.replace('Action   = ["s3:ListBucket"]\n        Resource = [local.txn_silver_bucket_arn]', 'Action   = ["s3:ListBucket", "s3:GetObject"]\n        Resource = [local.txn_silver_bucket_arn]'))) >= 1, True)
    arm("session-name-differs-red", len(semantic_problems(base, good.replace(SESSION_NAME, "other-session"))) >= 1, True)
    arm("edit-outside-region-red", len(removed_outside_region(base, good.replace('resource "aws_iam_role_policy" "inf_gold_layer_runner_shared" {\n  name = "runner-shared-read"', 'resource "aws_iam_role_policy" "inf_gold_layer_runner_shared" {\n  name = "runner-shared-reads"'))) >= 1, True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 3 and argv[1] == "--selftest":
        return selftest(argv[2])
    if len(argv) != 3 or argv[2] not in ("DBF139-4-AC1", "DBF139-4-AC2", "DBF139-4-AC3"):
        print("usage: p139_inf_role.py <repo_root> DBF139-4-AC1|AC2|AC3 | --selftest <repo_root>")
        return 2
    try:
        {"DBF139-4-AC1": ac1, "DBF139-4-AC2": ac2, "DBF139-4-AC3": ac3}[argv[2]](argv[1])
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % argv[2])
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % argv[2])
        return 1
    print("%s PASS" % argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
