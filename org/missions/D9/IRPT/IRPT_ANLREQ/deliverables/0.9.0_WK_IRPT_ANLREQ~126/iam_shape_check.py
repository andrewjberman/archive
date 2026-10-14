"""AR-y-316 IAM shape check (criterion AR316-y-AC3). Source only: reads Terraform text, calls nothing.

Grades infra/aws/terraform/ticket-center/main.tf (or the file named as argv[1], for the negative control) and prints
IAM-SHAPE-OK only when the statement IrptRequestsInputOwnerRead exists exactly once with:
  - Effect Allow and Action exactly ["dynamodb:GetItem"];
  - Resource exactly [data.aws_dynamodb_table.irpt_requests.arn], and that data source is named irpt-requests;
  - dynamodb:LeadingKeys equal to the three firms of the release-29 pair and no other value;
  - dynamodb:Attributes equal to INPUT_OWNER_ATTRS as lambda_function.py declares them (read from that file, never typed here);
  - ForAllValues:StringEquals wrapping both keys, and StringEqualsIfExists dynamodb:Select = SPECIFIC_ATTRIBUTES.
Otherwise it prints IAM-SHAPE-BAD <why> and exits 1.

Run:  python .../iam_shape_check.py                    (the worktree's main.tf)
      python .../iam_shape_check.py <copy-of-main.tf>  (negative control)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
MAIN_TF = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "infra" / "aws" / "terraform" / "ticket-center" / "main.tf"
LAMBDA = ROOT / "infra" / "aws" / "lambda" / "ticket_center" / "lambda_function.py"
SID = "IrptRequestsInputOwnerRead"
FIRMS = {"49financial", "inflection", "cottonwood"}


def quoted(items_text):
    return re.findall(r'"([^"]*)"', items_text)


def enclosing_block(text, pos):
    """The statement object that contains pos: scan back to the unmatched '{', then forward to its match."""
    depth = 0
    start = None
    for i in range(pos, -1, -1):
        ch = text[i]
        if ch == "}":
            depth += 1
        elif ch == "{":
            if depth == 0:
                start = i
                break
            depth -= 1
    if start is None:
        return None
    depth = 0
    for j in range(start, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[start:j + 1]
    return None


def main():
    reasons = []
    code = LAMBDA.read_text(encoding="utf-8")
    attrs_m = re.search(r"^INPUT_OWNER_ATTRS\s*=\s*\(([^)]*)\)", code, re.M)
    attrs = quoted(attrs_m.group(1)) if attrs_m else None
    if not attrs:
        print("IAM-SHAPE-BAD INPUT_OWNER_ATTRS is not declared in lambda_function.py")
        return 1

    tf = MAIN_TF.read_text(encoding="utf-8")
    data_ok = len(re.findall(r'data\s+"aws_dynamodb_table"\s+"irpt_requests"\s*\{\s*name\s*=\s*"irpt-requests"\s*\}', tf))
    if data_ok != 1:
        reasons.append("the data source aws_dynamodb_table.irpt_requests (name irpt-requests) is not declared exactly once (%d)" % data_ok)

    sids = [m.start() for m in re.finditer(r'Sid\s*=\s*"%s"' % SID, tf)]
    if len(sids) != 1:
        reasons.append("statement %s appears %d times, not once" % (SID, len(sids)))
    block = enclosing_block(tf, sids[0]) if len(sids) == 1 else None
    if len(sids) == 1 and not block:
        reasons.append("the statement block around %s does not close" % SID)
    if block:
        def one(pattern, label):
            hits = re.findall(pattern, block, re.S)
            if len(hits) != 1:
                reasons.append("%s appears %d times in the statement, not once" % (label, len(hits)))
                return None
            return hits[0]

        if not re.search(r'Effect\s*=\s*"Allow"', block):
            reasons.append("Effect is not Allow")
        action = one(r'\bAction\s*=\s*\[([^\]]*)\]', "Action")
        if action is not None and quoted(action) != ["dynamodb:GetItem"]:
            reasons.append("Action is %r, not exactly [dynamodb:GetItem]" % quoted(action))
        resource = one(r'\bResource\s*=\s*\[([^\]]*)\]', "Resource")
        if resource is not None and [x.strip() for x in resource.split(",") if x.strip()] != [
                "data.aws_dynamodb_table.irpt_requests.arn"]:
            reasons.append("Resource is %r, not exactly the irpt_requests data source ARN" % resource.strip())
        leading = one(r'"dynamodb:LeadingKeys"\s*=\s*\[([^\]]*)\]', "dynamodb:LeadingKeys")
        if leading is not None:
            keys = quoted(leading)
            if len(keys) != 3 or set(keys) != FIRMS:
                reasons.append("dynamodb:LeadingKeys is %r, not exactly the three firms %s" % (keys, sorted(FIRMS)))
        attr_list = one(r'"dynamodb:Attributes"\s*=\s*\[([^\]]*)\]', "dynamodb:Attributes")
        if attr_list is not None and quoted(attr_list) != attrs:
            reasons.append("dynamodb:Attributes is %r, not the code's INPUT_OWNER_ATTRS %r" % (quoted(attr_list), attrs))
        if not re.search(r'"ForAllValues:StringEquals"\s*=\s*\{', block):
            reasons.append("the keys are not under ForAllValues:StringEquals")
        if not re.search(r'StringEqualsIfExists\s*=\s*\{\s*"dynamodb:Select"\s*=\s*"SPECIFIC_ATTRIBUTES"\s*\}', block):
            reasons.append("StringEqualsIfExists dynamodb:Select = SPECIFIC_ATTRIBUTES is absent")

    if reasons:
        print("IAM-SHAPE-BAD " + "; ".join(reasons))
        return 1
    print("statement %s: one, Allow, dynamodb:GetItem on the irpt_requests data source; LeadingKeys = 3 firms; "
          "Attributes = %s (from lambda_function.py)" % (SID, attrs))
    print("IAM-SHAPE-OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
