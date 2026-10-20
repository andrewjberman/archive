"""AR-y-478 offline check: the analysis-audit grant is ONE customer-managed policy, and the inline policy is restored.

Stdlib only, offline, no AWS, no Terraform. It reads the two Terraform files of the ycharts tree, the base commit's
resident.tf through git (680818fdb3e), and the registries through lib/opal_naming.py loaded by path.

Prints one line on stdout: AUDIT-MANAGED-OK firms=<n> prefixes=<n> builder_equal=yes put_only=yes inline_restored=yes
size=<bytes> (rc 0), or AUDIT-MANAGED-BAD <why> (rc 1). --selftest mutates the text in memory three ways and prints
CONTROL-FIRES only when all three read BAD.
"""

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
YCHARTS = ROOT / "infra" / "aws" / "terraform" / "investor-reporting" / "ycharts"
RESIDENT_TF = YCHARTS / "resident.tf"
NEW_TF = YCHARTS / "resident_audit_policy.tf"
REGISTRY = ROOT / "infra" / "logic" / "registry"
OPAL_NAMING = ROOT / "lib" / "opal_naming.py"
BASE_COMMIT = "680818fdb3e"
BASE_PATH = "infra/aws/terraform/investor-reporting/ycharts/resident.tf"
POLICY_REVISION = "irpt-anlreq-x10-v1"
FAMILY = "ANALYSIS_AUDIT"
PRODUCT_BUCKET = "opal-data-irpt"
ART_SAMPLE = "RPT-" + "a" * 32
SHA_SAMPLE = "b" * 64
SIZE_BOUND = 6144
REGION = "us-east-1"
KMS_RESOURCE = "arn:aws:kms:us-east-1:000000000000:key/00000000-0000-0000-0000-000000000000"
KMS_LINE_KEY = '"kms:EncryptionContext:aws:s3:arn"'
ARG = "local.resident_audit_write_prefixes"
SID_PUT = "WriteTheAnalysisAudit"
SID_KMS = "AuditEncryptionViaS3ForAuditPrefixesOnly"
PUT_ONLY = ["s3:PutObject"]
KMS_ACTIONS = ["kms:Decrypt", "kms:GenerateDataKey"]
KMS_RESOURCE_EXPR = "[data.terraform_remote_state.core.outputs.kms_key_arn]"
PUT_ACTION_LINE = 'Action   = ["s3:PutObject"]'


def read_text(path):
    return path.read_text(encoding="utf-8")


def strip_comments(text):
    kept = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        kept.append(line)
    return "\n".join(kept)


def top_blocks(text):
    """The brace-balanced {...} blocks at depth 0 of text, double-quoted strings respected."""
    blocks = []
    depth = 0
    start = None
    in_str = False
    for i, ch in enumerate(text):
        if in_str:
            if ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append(text[start:i + 1])
                start = None
    return blocks


def base_kms_line():
    """The KMS line of resident.tf at the base commit, read through git; None when it cannot be read."""
    proc = subprocess.run(
        ["git", "show", BASE_COMMIT + ":" + BASE_PATH],
        cwd=str(ROOT), capture_output=True,
    )
    if proc.returncode != 0:
        return None
    lines = [ln for ln in proc.stdout.decode("utf-8").splitlines() if KMS_LINE_KEY in ln]
    if len(lines) != 1:
        return None
    return lines[0].rstrip()


def check_resident(text, base_line):
    problems = []
    if base_line is None:
        problems.append("base KMS line at %s unreadable" % BASE_COMMIT)
    if SID_PUT in text:
        problems.append("resident.tf still names the statement " + SID_PUT)
    if not re.search(r"^\s*resident_audit_write_prefixes\s*=\s*\[", text, re.M):
        problems.append("resident.tf no longer defines resident_audit_write_prefixes")
    kms = [ln for ln in text.splitlines() if KMS_LINE_KEY in ln]
    if len(kms) != 1:
        problems.append("resident.tf KMS line count %d != 1" % len(kms))
    elif base_line is not None and kms[0].rstrip() != base_line:
        problems.append("resident.tf KMS line differs from its %s text" % BASE_COMMIT)
    return problems


def field_value(block, name):
    m = re.search(r"\b" + name + r"\s*=\s*([^\n]+)", block)
    if not m:
        return None
    return m.group(1).strip().rstrip(",").strip()


def quoted(value):
    return re.findall(r'"([^"]*)"', value or "")


def sid_of(block):
    m = re.search(r'\bSid\s*=\s*"([^"]+)"', block)
    return m.group(1) if m else None


def statements_of(body):
    m = re.search(r"Statement\s*=\s*\[", body)
    if not m:
        return None
    rest = body[m.end():]
    close = re.search(r"\n {4}\]\n", rest)
    list_text = rest[:close.start()] if close else rest
    return top_blocks(list_text)


def check_new(text):
    """Returns (problems, parsed) where parsed is the list of statement dicts, or None."""
    problems = []
    body = strip_comments(text)
    if "arn:aws:s3:::opal" in text:
        problems.append("the new file carries an arn:aws:s3:::opal literal")
    policies = re.findall(r'resource\s+"aws_iam_policy"\s+"([^"]+)"', body)
    if len(policies) != 1:
        problems.append("aws_iam_policy count %d != 1" % len(policies))
    attachments = re.findall(r'resource\s+"aws_iam_role_policy_attachment"\s+"([^"]+)"\s*\{([^}]*)\}', body)
    if len(attachments) != 1:
        problems.append("aws_iam_role_policy_attachment count %d != 1" % len(attachments))
    to_runner = [a for a in attachments
                 if re.search(r"role\s*=\s*aws_iam_role\.runner\.name", a[1])
                 and re.search(r"policy_arn\s*=\s*aws_iam_policy\.resident_audit_write\.arn", a[1])]
    if len(to_runner) != 1:
        problems.append("no attachment of the policy to aws_iam_role.runner")
    blocks = statements_of(body)
    if blocks is None:
        problems.append("no Statement list in the new policy")
        return problems, None
    sids = [sid_of(b) for b in blocks]
    if len(blocks) != 2 or sids != [SID_PUT, SID_KMS]:
        problems.append("statements are %s, want exactly [%s, %s]" % (sids, SID_PUT, SID_KMS))
        return problems, None
    put_block, kms_block = blocks
    put_action = quoted(field_value(put_block, "Action"))
    if put_action != PUT_ONLY:
        problems.append("put statement actions are %s, want %s" % (put_action, PUT_ONLY))
    if field_value(put_block, "Resource") != ARG:
        problems.append("put statement resource is not " + ARG)
    if "Condition" in put_block:
        problems.append("put statement carries a Condition")
    kms_action = quoted(field_value(kms_block, "Action"))
    if kms_action != KMS_ACTIONS:
        problems.append("kms statement actions are %s, want %s" % (kms_action, KMS_ACTIONS))
    if field_value(kms_block, "Resource") != KMS_RESOURCE_EXPR:
        problems.append("kms statement resource is not the core kms_key_arn")
    like = re.search(r'StringLike\s*=\s*\{\s*"kms:EncryptionContext:aws:s3:arn"\s*=\s*([^}\n]+?)\s*\}', kms_block)
    if not like or like.group(1) != ARG:
        problems.append("kms statement StringLike is not " + ARG)
    via = re.search(r'"kms:ViaService"\s*=\s*"s3\.\$\{var\.aws_region\}\.amazonaws\.com"', kms_block)
    if not via:
        problems.append("kms statement lacks the kms:ViaService s3 condition")
    parsed = [
        {"sid": SID_PUT, "action": put_action, "resource_expr": field_value(put_block, "Resource")},
        {"sid": SID_KMS, "action": kms_action, "resource_expr": field_value(kms_block, "Resource")},
    ]
    return problems, parsed


def registry_json(name):
    return json.loads(read_text(REGISTRY / name))


def load_builder():
    spec = importlib.util.spec_from_file_location("opal_naming_ar478", str(OPAL_NAMING))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate_prefixes():
    """Returns (prefixes, firm_count, problems): the derived prefixes, one per enabled client firm, sorted by key."""
    problems = []
    scopes = registry_json("scopes.json")["scopes"]
    firms = {}
    for scope in scopes:
        tenant = scope.get("tenant") or {}
        if scope.get("class") == "FIRM" and tenant.get("kind") == "client" and tenant.get("enabled") is True:
            firms[scope["key"]] = scope["long"]
    policy_rows = [p for p in registry_json("reporting_policies.json")["policies"]
                   if p.get("policy_revision") == POLICY_REVISION]
    if len(policy_rows) != 1:
        return [], len(firms), ["policy row %s count %d != 1" % (POLICY_REVISION, len(policy_rows))]
    row = policy_rows[0]
    family = row["families"][FAMILY]
    builder = load_builder()
    prefixes = []
    for key in sorted(firms):
        derived = "arn:aws:s3:::%s/%s/%s/%s/%s/*" % (
            PRODUCT_BUCKET, row["source"], firms[key], family["tier"], family["table"])
        try:
            bucket, dest_key = builder.reporting_destination(
                key, FAMILY, ART_SAMPLE, SHA_SAMPLE, policy_revision=POLICY_REVISION)
        except ValueError as exc:
            problems.append("builder refuses firm %s: %s" % (key, exc))
            continue
        # the key is <family dir>/<artifact id dir>/<sha>.json: the family directory is the prefix the grant covers
        dest_prefix = dest_key.rsplit("/", 2)[0] + "/"
        built = "arn:aws:s3:::%s/%s*" % (bucket, dest_prefix)
        if bucket != PRODUCT_BUCKET or built != derived:
            problems.append("builder differs for firm %s: %s vs %s" % (key, built, derived))
        prefixes.append(derived)
    return prefixes, len(firms), problems


def policy_size(parsed, prefixes):
    statements = []
    for stmt in parsed:
        if stmt["sid"] == SID_PUT:
            statements.append({"Sid": SID_PUT, "Effect": "Allow", "Action": stmt["action"], "Resource": prefixes})
        else:
            statements.append({
                "Sid": SID_KMS, "Effect": "Allow", "Action": stmt["action"], "Resource": [KMS_RESOURCE],
                "Condition": {
                    "StringEquals": {"kms:ViaService": "s3.%s.amazonaws.com" % REGION},
                    "StringLike": {"kms:EncryptionContext:aws:s3:arn": prefixes},
                },
            })
    doc = {"Version": "2012-10-17", "Statement": statements}
    return len(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def evaluate(resident_text, new_text, base_line):
    """Returns (ok, detail): detail is the OK line body or the list of reasons."""
    problems = check_resident(resident_text, base_line)
    new_problems, parsed = check_new(new_text)
    problems.extend(new_problems)
    prefixes, firm_count, builder_problems = evaluate_prefixes()
    problems.extend(builder_problems)
    size = None
    if parsed is not None and prefixes:
        size = policy_size(parsed, prefixes)
        if size >= SIZE_BOUND:
            problems.append("policy document is %d bytes, bound is %d" % (size, SIZE_BOUND))
    if problems:
        return False, "; ".join(problems)
    return True, ("firms=%d prefixes=%d builder_equal=yes put_only=yes inline_restored=yes size=%d"
                  % (firm_count, len(prefixes), size))


def mutate_put_list(new_text, resident_text):
    return new_text.replace(PUT_ACTION_LINE, 'Action   = ["s3:GetObject"]'), resident_text


def mutate_inline_kms(new_text, resident_text):
    lines = []
    for ln in resident_text.splitlines():
        if KMS_LINE_KEY in ln:
            ln = ln.replace("local.ycdgen_opal_report_prefixes)", "local.ycdgen_opal_report_prefixes, " + ARG + ")")
        lines.append(ln)
    return new_text, "\n".join(lines) + "\n"


def mutate_no_attachment(new_text, resident_text):
    stripped = re.sub(r'resource\s+"aws_iam_role_policy_attachment"[^{]*\{[^}]*\}\n?', "", new_text)
    return stripped, resident_text


def selftest():
    resident_text = read_text(RESIDENT_TF)
    new_text = read_text(NEW_TF)
    base_line = base_kms_line()
    ok, detail = evaluate(resident_text, new_text, base_line)
    if not ok:
        print("CONTROL-BROKEN baseline is not OK: " + detail)
        return 1
    mutants = [
        ("put-list-given-getobject", mutate_put_list),
        ("inline-kms-given-audit-argument", mutate_inline_kms),
        ("attachment-removed", mutate_no_attachment),
    ]
    all_fire = True
    for name, mutate in mutants:
        m_new, m_resident = mutate(new_text, resident_text)
        if m_new == new_text and m_resident == resident_text:
            print("CONTROL-BROKEN mutation did not change the text: " + name, file=sys.stderr)
            return 1
        m_ok, m_detail = evaluate(m_resident, m_new, base_line)
        print("mutant %s read %s: %s" % (name, "OK" if m_ok else "BAD", m_detail), file=sys.stderr)
        if m_ok:
            all_fire = False
    if all_fire:
        print("CONTROL-FIRES")
        return 0
    print("CONTROL-DID-NOT-FIRE")
    return 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    resident_text = read_text(RESIDENT_TF)
    new_text = read_text(NEW_TF)
    ok, detail = evaluate(resident_text, new_text, base_kms_line())
    if ok:
        print("AUDIT-MANAGED-OK " + detail)
        return 0
    print("AUDIT-MANAGED-BAD " + detail)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
