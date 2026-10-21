"""IRPT_ANLREQ TO-AR-y-486: offline check of the resident ticket-read managed policy source.

Reads infra/aws/terraform/investor-reporting/ycharts/resident_ticket_read_policy.tf as TEXT.
Stdlib only. Offline: no AWS, no network, no terraform.

Usage:
  python -I check_ticket_read_policy.py              -> TICKET-READ-POLICY-OK ... (rc 0) or TICKET-READ-POLICY-BAD <why> (rc 1)
  python -I check_ticket_read_policy.py --selftest   -> CONTROL-FIRES (rc 0) only when all five in-memory mutants read BAD;
                                                        otherwise CONTROL-MISSED <names> (rc 1)

Stdout carries exactly one line per mode. Per-mutant detail goes to stderr.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
TF_PATH = (
    ROOT
    / "infra"
    / "aws"
    / "terraform"
    / "investor-reporting"
    / "ycharts"
    / "resident_ticket_read_policy.tf"
)

EXPECTED_ACTIONS = ["dynamodb:GetItem"]
EXPECTED_ATTRS = ["ticket_id", "ticket_type", "answers", "created_at"]
EXPECTED_RESOURCE = (
    "arn:aws:dynamodb:${var.aws_region}:${data.aws_caller_identity.current.account_id}"
    ":table/${local.resident_audit_tickets_table}"
)
EXPECTED_TABLE = "opal-tickets"
EXPECTED_OPERATORS = ["Null", "ForAllValues:StringEquals", "StringEqualsIfExists"]
FORBIDDEN_WORDS = ["Query", "Scan", "BatchGetItem", "PutItem", "UpdateItem", "DeleteItem"]
FORBIDDEN_ATTRS = ["requester", "created_by", "events", "filer_user_type", "*"]


def code_of(text):
    """Return the text with every '#' comment removed (no '#' occurs inside a string in this file)."""
    return "\n".join(re.sub(r"#.*$", "", raw) for raw in text.splitlines())


def quoted_items(body):
    return re.findall(r'"([^"]*)"', body)


def top_level_keys(body):
    """Keys of the map entries at depth zero of a body: each '"key" = {' pair found outside nested braces."""
    flat = []
    depth = 0
    for ch in body:
        if ch == "{":
            flat.append("{" if depth == 0 else " ")
            depth += 1
        elif ch == "}":
            depth -= 1
            flat.append("}" if depth == 0 else " ")
        else:
            flat.append(ch if depth == 0 else " ")
    return re.findall(r'"([^"]*)"\s*=\s*\{', "".join(flat))


def condition_body(code):
    match = re.search(r"\bCondition\s*=\s*\{", code)
    if match is None:
        return None
    depth = 1
    pos = match.end()
    start = pos
    while pos < len(code) and depth:
        if code[pos] == "{":
            depth += 1
        elif code[pos] == "}":
            depth -= 1
        pos += 1
    return code[start : pos - 1]


def validate(text):
    """Return (reasons, counts). reasons is empty only when every check holds."""
    reasons = []
    counts = {}
    non_ascii = [ch for ch in text if ord(ch) > 127]
    if non_ascii:
        reasons.append(f"non-ASCII character present ({len(non_ascii)})")
    code = code_of(text)

    action_bodies = re.findall(r"\bAction\s*=\s*\[([^\]]*)\]", code)
    if len(action_bodies) != 1 or len(re.findall(r"\bAction\b", code)) != 1:
        reasons.append(f"expected exactly one Action list, found {len(action_bodies)}")
        actions = []
    else:
        actions = quoted_items(action_bodies[0])
        if actions != EXPECTED_ACTIONS:
            reasons.append(f"Action list is {actions}, expected {EXPECTED_ACTIONS}")
    counts["actions"] = len(actions)

    resource_bodies = re.findall(r"\bResource\s*=\s*\[([^\]]*)\]", code)
    if len(resource_bodies) != 1 or len(re.findall(r"\bResource\b", code)) != 1:
        reasons.append(f"expected exactly one Resource list, found {len(resource_bodies)}")
        resources = []
    else:
        resources = quoted_items(resource_bodies[0])
        if resources != [EXPECTED_RESOURCE]:
            reasons.append("Resource is not exactly the one table/ ARN built from local.resident_audit_tickets_table")
    counts["resources"] = len(resources)

    for word in FORBIDDEN_WORDS:
        if re.search(r"\b" + word + r"\b", code):
            reasons.append(f"forbidden action word present outside comments: {word}")
    if re.search(r"index", code):
        reasons.append("the word index is present outside comments")
    if "*" in code:
        reasons.append("a wildcard * is present outside comments")
    if code.count("table/") != 1:
        reasons.append(f"expected exactly one table/ ARN, found {code.count('table/')}")

    locals_values = re.findall(r'\bresident_audit_tickets_table\s*=\s*"([^"]*)"', code)
    if locals_values != [EXPECTED_TABLE]:
        reasons.append(f"local resident_audit_tickets_table is {locals_values}, expected [{EXPECTED_TABLE}]")

    attr_match = re.search(
        r'"ForAllValues:StringEquals"\s*=\s*\{\s*"dynamodb:Attributes"\s*=\s*\[([^\]]*)\]\s*\}', code
    )
    if attr_match is None:
        reasons.append("ForAllValues:StringEquals dynamodb:Attributes list not found")
        attrs = []
    else:
        attrs = quoted_items(attr_match.group(1))
        if sorted(attrs) != sorted(EXPECTED_ATTRS) or len(attrs) != len(EXPECTED_ATTRS):
            reasons.append(f"Attributes list is {attrs}, expected exactly {EXPECTED_ATTRS}")
        for name in FORBIDDEN_ATTRS:
            if name in attrs:
                reasons.append(f"forbidden attribute {name} in the Attributes list")
    counts["attrs"] = len(attrs)

    null_guard = re.search(r'"Null"\s*=\s*\{\s*"dynamodb:Attributes"\s*=\s*"false"\s*\}', code) is not None
    if not null_guard:
        reasons.append('Null guard "dynamodb:Attributes" = "false" is missing')

    select = re.search(
        r'"StringEqualsIfExists"\s*=\s*\{\s*"dynamodb:Select"\s*=\s*"SPECIFIC_ATTRIBUTES"\s*\}', code
    ) is not None
    if not select:
        reasons.append("dynamodb:Select SPECIFIC_ATTRIBUTES guard is missing")

    body = condition_body(code)
    if body is None:
        reasons.append("no Condition block")
    else:
        keys = top_level_keys(body)
        if sorted(keys) != sorted(EXPECTED_OPERATORS):
            reasons.append(f"Condition operators are {keys}, expected exactly {EXPECTED_OPERATORS}")

    if len(re.findall(r'\bSid\s*=\s*"ReadTheFiledTicketForTheAuditOnly"', code)) != 1:
        reasons.append("expected exactly one statement with the Sid ReadTheFiledTicketForTheAuditOnly")
    if len(re.findall(r"\bEffect\s*=", code)) != 1 or not re.search(r'\bEffect\s*=\s*"Allow"', code):
        reasons.append("expected exactly one Effect, and it is Allow")

    attachments = re.findall(r'resource\s+"aws_iam_role_policy_attachment"', code)
    roles = re.findall(r"\brole\s*=\s*(\S+)", code)
    attach_ok = len(attachments) == 1 and roles == ["aws_iam_role.runner.name"]
    if not attach_ok:
        reasons.append(
            f"expected one aws_iam_role_policy_attachment naming aws_iam_role.runner.name, "
            f"found {len(attachments)} attachment(s) with roles {roles}"
        )
    if not re.search(r"\bpolicy_arn\s*=\s*aws_iam_policy\.resident_ticket_read\.arn", code):
        reasons.append("the attachment does not name aws_iam_policy.resident_ticket_read.arn")

    counts["null_guard"] = null_guard
    counts["select"] = select
    counts["attach_ok"] = attach_ok
    return reasons, counts


def mutants(text):
    """Five in-memory mutations of the policy text; each must read BAD."""
    return [
        ("add-query-action", text.replace('["dynamodb:GetItem"]', '["dynamodb:GetItem", "dynamodb:Query"]', 1)),
        ("add-requester-attr", text.replace('"created_at"]', '"created_at", "requester"]', 1)),
        ("delete-null-guard", re.sub(r'"Null"\s*=\s*\{[^}]*\}', "", text, count=1)),
        (
            "resource-index-suffix",
            text.replace('table/${local.resident_audit_tickets_table}"', 'table/${local.resident_audit_tickets_table}/index/*"', 1),
        ),
        ("local-other-table", text.replace('resident_audit_tickets_table = "opal-tickets"', 'resident_audit_tickets_table = "opal-users-v2"', 1)),
    ]


def selftest(text):
    fired = []
    missed = []
    for name, mutated in mutants(text):
        if mutated == text:
            missed.append(f"{name}(not-applied)")
            continue
        reasons, _ = validate(mutated)
        if reasons:
            fired.append(name)
            print(f"mutant {name}: BAD {reasons[0]}", file=sys.stderr)
        else:
            missed.append(name)
    if len(fired) == 5:
        print("CONTROL-FIRES")
        return 0
    print("CONTROL-MISSED " + ",".join(missed))
    return 1


def main(argv):
    if not TF_PATH.is_file():
        print(f"TICKET-READ-POLICY-BAD policy source not found at {TF_PATH}")
        return 1
    text = TF_PATH.read_text(encoding="utf-8")
    if "--selftest" in argv:
        return selftest(text)
    reasons, counts = validate(text)
    if reasons:
        print("TICKET-READ-POLICY-BAD " + "; ".join(reasons))
        return 1
    print(
        f"TICKET-READ-POLICY-OK actions={counts['actions']} resources={counts['resources']} "
        f"attrs={counts['attrs']} null_guard={'yes' if counts['null_guard'] else 'no'} "
        f"select={'yes' if counts['select'] else 'no'} "
        f"attachment_runner_only={'yes' if counts['attach_ok'] else 'no'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
