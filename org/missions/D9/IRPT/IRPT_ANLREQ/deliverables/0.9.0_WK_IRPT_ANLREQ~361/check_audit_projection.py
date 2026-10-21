#!/usr/bin/env python3
"""IRPT_ANLREQ AR-y-487 check: ticket_audit_source.py reads the ticket with exactly the four-attribute projection.

Stdlib only; offline; reads the source as TEXT and parses it with ast for the PROJECTED_ATTRIBUTES constant.
Prints one line and exits:
  AUDIT-PROJECTION-OK attrs=ticket_id,ticket_type,answers,created_at projection=yes filer_user_type_read=no   (rc 0)
  AUDIT-PROJECTION-BAD <why>                                                                                  (rc 1)
--selftest mutates the text in memory four ways and prints CONTROL-FIRES (rc 0) only when all four read BAD.
AR-y-487 AMENDMENT 1: plain attribute names; the source must carry no alias argument of the second kind.
"""
import ast
import io
import re
import sys
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
SOURCE = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "generate" / "ticket_audit_source.py"
WANT = ("ticket_id", "ticket_type", "answers", "created_at")
CALL = "dynamodb.get_item("
READ_FORMS = ('found["filer_user_type"]', '"filer_user_type" in found', 'found.get("filer_user_type"')
NAMES_OUT_OF_CODE = ("requester", "created_by")


def _projected(tree):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PROJECTED_ATTRIBUTES"
                                                for t in node.targets):
            try:
                return ast.literal_eval(node.value)
            except ValueError:
                return "NOT-A-LITERAL"
    return None


def _get_item_call(text):
    start = text.find(CALL)
    if start < 0:
        return None
    depth = 0
    for index in range(start + len(CALL) - 1, len(text)):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    return None


def _code_mentions(text, tree):
    """Each NAME token, and each STRING token outside the module docstring, that spells requester or created_by."""
    doc_lines = set()
    first = tree.body[0] if tree.body else None
    if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)):
        doc_lines = set(range(first.lineno, first.end_lineno + 1))
    hits = []
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type == tokenize.NAME and tok.string in NAMES_OUT_OF_CODE:
            hits.append((tok.start[0], tok.string))
        elif tok.type == tokenize.STRING and tok.start[0] not in doc_lines:
            for name in NAMES_OUT_OF_CODE:
                if name in tok.string:
                    hits.append((tok.start[0], name))
    return hits


def judge(text):
    """None when the text passes; otherwise the first reason it does not."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return "SOURCE-DOES-NOT-PARSE"
    projected = _projected(tree)
    if projected is None:
        return "PROJECTED_ATTRIBUTES-MISSING"
    if projected != WANT:
        return "PROJECTED_ATTRIBUTES-IS-NOT-THE-FOUR-NAMES-IN-ORDER"
    if text.count(CALL) != 1:
        return "GET-ITEM-CALL-COUNT-IS-NOT-ONE"
    call = _get_item_call(text)
    if call is None or "ProjectionExpression=" not in call:
        return "NO-ProjectionExpression-IN-GET-ITEM"
    if "ExpressionAttributeNames" in text:
        return "ExpressionAttributeNames-PRESENT"
    for form in READ_FORMS:
        if form in text:
            return "FILER-USER-TYPE-READ-PRESENT"
    hits = _code_mentions(text, tree)
    if hits:
        return "requester-or-created_by-IN-CODE line %d" % hits[0][0]
    return None


def _selftest():
    base = SOURCE.read_text(encoding="utf-8")
    base_why = judge(base)
    if base_why is not None:
        print("CONTROL-SILENT base-not-clean " + base_why)
        return 1
    mutants = (
        re.sub(r",\s*ProjectionExpression=_PROJECTION", "", base, count=1),
        base.replace('"answers", "created_at")', '"answers", "created_at", "requester")', 1),
        base.replace("            written_at = datetime",
                     '            _read = found["filer_user_type"]\n            written_at = datetime', 1),
        base.replace("ProjectionExpression=_PROJECTION",
                     "ExpressionAttributeNames={}, ProjectionExpression=_PROJECTION", 1),
    )
    fired = [judge(text) is not None for text in mutants]
    if all(fired):
        print("CONTROL-FIRES")
        return 0
    print("CONTROL-SILENT fired=" + ",".join(str(flag) for flag in fired))
    return 1


def _main(argv):
    if "--selftest" in argv:
        return _selftest()
    try:
        text = SOURCE.read_text(encoding="utf-8")
    except OSError:
        print("AUDIT-PROJECTION-BAD source-unreadable")
        return 1
    why = judge(text)
    if why is not None:
        print("AUDIT-PROJECTION-BAD " + why)
        return 1
    print("AUDIT-PROJECTION-OK attrs=%s projection=yes filer_user_type_read=no" % ",".join(WANT))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
