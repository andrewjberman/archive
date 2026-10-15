"""IRPT_BCKEND workstream ~PO round 8 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD cell: the Scope feed IAM resource, rewritten to pass the commit-time naming gate.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB234-1  IB-pr-603  aws_iam_role_policy.inf_gold_layer_scope_feed in infra/aws/terraform/inf-pipeline/iam.tf: the packet's two statements, every scope and name read from the registry
    AC1  the resource in the file: two statements (Put/Get on the two feed prefixes; ListBucket under an s3:prefix condition), no Delete, no KMS, no hand-typed firm scope or bucket literal in it
    AC2  the record: the diff bounded to iam.tf, the commit accepted by the naming gate, the evaluated prefixes equal to address() output
    AC3  notes and the six counters 0, no long digit run
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for sub in ("r196", "r200"):
    sys.path.insert(0, str(HERE.parent / sub))
import p196_cells as P6  # noqa: E402
import p200_cells as P0  # noqa: E402

TF = "infra/aws/terraform/inf-pipeline/iam.tf"
SLOT = 439
REC = P6.D + "0.9.0_WK_IRPT_BCKEND~%d/IB234-1_scope_feed_iam_hcl.json" % SLOT
ADDRESS = "inf_gold_layer_scope_feed"
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits
ALLOWED = (TF, "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-603.scope-feed-iam-hcl.md")


def resource_block(src):
    m = re.search(r'resource\s+"aws_iam_role_policy"\s+"%s"\s*\{' % ADDRESS, src)
    if not m:
        return None
    depth, i = 1, m.end()
    while i < len(src) and depth:
        depth += {"{": 1, "}": -1}.get(src[i], 0)
        i += 1
    return src[m.start():i] if depth == 0 else None


def ac1():
    f = P6.ROOT / TF
    if not f.is_file():
        fail("no %s" % TF)
    src = f.read_text(encoding="utf-8")
    b = resource_block(src)
    if b is None:
        fail("%s has no resource aws_iam_role_policy.%s" % (TF, ADDRESS))
    if len(re.findall(r"\bSid\s*=", b)) != 2:
        fail("the resource must hold exactly two statements (Sid count)")
    for need in ("s3:PutObject", "s3:GetObject", "s3:ListBucket", "s3:prefix", "aws_iam_role.inf_gold_layer.id"):
        if need not in b:
            fail("the resource must carry %s" % need)
    for banned in ("s3:DeleteObject", "s3:*", "kms:", '"*"'):
        if banned in b:
            fail("the resource must not carry %s" % banned)
    stripped = re.sub(r"\b(?:lookup|jsondecode|file)\([^)]*\)", "", b)
    for lit in ("inflection", "opal-data-assets", "orion", "scope_account_returns"):
        if re.search(r'"[^"]*%s[^"]*"' % re.escape(lit), stripped.replace('"s3:prefix"', "")):
            fail("a hand-typed %r literal in the resource: it must come through lookup() over a registry-fed local or the opal_name module" % lit)
    if "logic/registry/" not in src:
        fail("%s must feed a local from jsondecode(file(.../logic/registry/<name>.json))" % TF)
    print("OK: the resource holds two statements, no Delete, no KMS, no hand-typed scope or bucket literal")


def expected_arns():
    sys.path.insert(0, str(P6.ROOT / "lib"))
    import importlib
    mod = importlib.import_module("opal_naming")
    out = []
    for layer in ("bronze", "silver"):
        a = mod.address("orion", "inflection", layer, "scope_account_returns", "date=2000-01-01", "x")
        out.append(re.sub(r"^s3://", "arn:aws:s3:::", a).replace("date=2000-01-01/x", "*"))
    return sorted(out)


def ac2():
    r = load(REC)
    base = r.get("base_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        fail("base_commit must be 40 hex")
    c = {"slot": SLOT}
    changed = P0.own_changes(c, base)
    if sorted(r.get("changed_paths", [])) != changed:
        fail("changed_paths differs from the worker's own commits since base")
    stray = [x for x in changed if x not in ALLOWED]
    if stray:
        fail("paths outside the grant: %r" % stray[:4])
    if TF not in changed:
        fail("%s must change" % TF)
    ng = r.get("naming_gate") or {}
    if ng.get("commit_accepted") is not True or ng.get("refused") != 0 or not (is_int(ng.get("literals_graded")) and ng["literals_graded"] >= 1):
        fail("naming_gate must read commit_accepted true, refused 0 and literals_graded >= 1 (the worker's own commit passed the gate)")
    if ng.get("policy_name_source") not in ("name()", "registered"):
        fail("naming_gate.policy_name_source must read name() or registered")
    ev = r.get("evaluated_prefixes")
    if not isinstance(ev, list) or sorted(ev) != expected_arns():
        fail("evaluated_prefixes must equal the address() output for the two layers (as ARN prefixes ending /*), character for character")
    if r.get("evaluated_by") not in ("terraform console", "registry reading"):
        fail("evaluated_by must read terraform console or registry reading")
    print("OK: diff bounded to iam.tf; naming gate accepted; the prefixes equal address() output")


def ac3():
    r = load(REC)
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 2 or any(not isinstance(n, str) or len(n) < 30 for n in notes):
        fail("notes needs at least two lines of 30+ characters")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: notes, counters, no long digit run")


CHECKS = {"IB234-1-AC1": ac1, "IB234-1-AC2": ac2, "IB234-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p234_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
