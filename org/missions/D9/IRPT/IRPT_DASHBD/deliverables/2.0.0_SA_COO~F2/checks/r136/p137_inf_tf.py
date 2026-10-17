"""IRPT_DASHBD round 137, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the INFLECTION RUNNER'S NEW SCOPED POLICY in the inf-pipeline Terraform root (cell DB-f-2501).

  The CTO's cross-adjudication XA-20261017T005839Z-a222 (RULED yes, msg 10119): ONE new scoped inline policy on the Orion gold runner's role (`aws_iam_role.inf_gold_layer`):
  (1) Get on the Orion Inflection `fact_transactions` SILVER prefix, the resource ending at that prefix's children; (2) List of the silver bucket conditioned on `s3:prefix` equal to
  that prefix and its children; (3) Put on the ONE Inflection gold prefix `irpt/<inflection>/gold/account_transaction/`. Every bucket, scope, source and prefix is DERIVED from the
  registry (the scope-feed policy's pattern), never typed; the policy name comes from the opal_name module. `iam.tf` gains the block by PURE INSERTION (the existing policies,
  statements and the role are byte-for-byte); every other file of the root is byte-identical. The grant is a never-widen pair's: this cell changes text only, nothing is planned or applied.
  DBF137-5-AC1 (the bytes and the insertion), DBF137-5-AC2 (the meaning)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

R = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/"
BASE_IAM = R + "inf_iam_base.tf.txt"
MANIFEST = R + "inf_pipeline_base_manifest.json"
RESOURCE_LABEL = "inf_gold_layer_account_transaction"
SIDS = ("S1ReadOrionInflectionTransactionsSilverOnly", "S2ListOrionInflectionTransactionsSilverOnly", "S3PutInflectionAccountTransactionGoldOnly")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def insertion_problems(base, new):
    removed, added = [], []
    for d in difflib.unified_diff(base.splitlines(), new.splitlines(), lineterm="", n=0):
        if d.startswith("---") or d.startswith("+++") or d.startswith("@@"):
            continue
        (removed if d.startswith("-") else added).append(d[1:])
    pr = []
    if removed:
        pr.append("a base line was removed or changed: %r" % removed[0][:100])
    if any(not a.isascii() for a in added):
        pr.append("an added line is not ASCII")
    return pr


def added_text(base, new):
    return chr(10).join(d[1:] for d in difflib.unified_diff(base.splitlines(), new.splitlines(), lineterm="", n=0)
                        if d.startswith("+") and not d.startswith("+++"))


def block_of(text, label):
    """The text of `resource "aws_iam_role_policy" "<label>" { ... }` with balanced braces, or None."""
    m = re.search(r'resource\s+"aws_iam_role_policy"\s+"%s"\s*\{' % re.escape(label), text)
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


def statement_text(blk, sid):
    """The `{ ... }` object of a statement whose Sid is `sid` inside the policy's jsonencode, or None."""
    m = re.search(r'Sid\s*=\s*"%s"' % re.escape(sid), blk)
    if not m:
        return None
    start = blk.rfind("{", 0, m.start())
    depth = 0
    for j in range(start, len(blk)):
        if blk[j] == "{":
            depth += 1
        elif blk[j] == "}":
            depth -= 1
            if depth == 0:
                return blk[start:j + 1]
    return None


def semantic_problems(base, new):
    pr = []
    blk = block_of(new, RESOURCE_LABEL)
    if blk is None:
        return ['iam.tf must carry resource "aws_iam_role_policy" "%s"' % RESOURCE_LABEL]
    if block_of(base, RESOURCE_LABEL) is not None:
        pr.append("the resource already exists in the base")
    if not re.search(r"role\s*=\s*aws_iam_role\.inf_gold_layer\.id", blk):
        pr.append("the policy must attach to the runner's role aws_iam_role.inf_gold_layer")
    if not re.search(r"name\s*=\s*module\.[A-Za-z0-9_]+\.name", blk):
        pr.append("the policy's name must come from an opal_name module (name = module.<x>.name)")
    mods = re.findall(r'module\s+"([A-Za-z0-9_]+)"\s*\{[^{}]*source\s*=\s*"\.\./modules/opal_name"[^{}]*kind\s*=\s*"policy"[^{}]*\}', new, re.S)
    nm = re.search(r"name\s*=\s*module\.([A-Za-z0-9_]+)\.name", blk)
    if nm and nm.group(1) not in mods:
        pr.append("module.%s must be an opal_name module with kind = \"policy\"" % nm.group(1))
    for sid in SIDS:
        if len(re.findall(r'Sid\s*=\s*"%s"' % sid, blk)) != 1:
            pr.append("the policy must carry the statement %s exactly once" % sid)
    s1, s2, s3 = (statement_text(blk, s) for s in SIDS)
    if s1 is not None:
        if not (re.search(r'Effect\s*=\s*"Allow"', s1) and re.search(r"Action\s*=\s*\[\s*\"s3:GetObject\"\s*\]", s1) and "Condition" not in s1):
            pr.append("S1 must be Allow, Action exactly [\"s3:GetObject\"], no condition")
    if s2 is not None:
        if not (re.search(r'Effect\s*=\s*"Allow"', s2) and re.search(r"Action\s*=\s*\[\s*\"s3:ListBucket\"\s*\]", s2) and "s3:prefix" in s2 and "StringLike" in s2):
            pr.append("S2 must be Allow, Action exactly [\"s3:ListBucket\"], conditioned by StringLike on s3:prefix")
    if s3 is not None:
        if not (re.search(r'Effect\s*=\s*"Allow"', s3) and re.search(r"Action\s*=\s*\[\s*\"s3:PutObject\"\s*\]", s3) and "Condition" not in s3):
            pr.append("S3 must be Allow, Action exactly [\"s3:PutObject\"], no condition")
    allact = re.findall(r'"([a-z0-9]+:[A-Za-z*]+)"', blk)
    if sorted(set(allact) - {"s3:prefix"}) != ["s3:GetObject", "s3:ListBucket", "s3:PutObject"]:
        pr.append("the policy's actions must be exactly s3:GetObject, s3:ListBucket and s3:PutObject: %r" % sorted(set(allact)))
    added = added_text(base, new)
    for needle in ("fact_transactions", "account_transaction", "silver", "gold"):
        if needle not in added:
            pr.append("the inserted text must name %r (the prefixes are built from the registry lookups and these table and layer words)" % needle)
    if "opal-data-" in blk or "opal-data-" in added:
        pr.append("no bucket name may be typed (opal-data-...): buckets come from the registry lookups")
    if re.search(r'Resource\s*=\s*"\*"|Resource\s*=\s*\[\s*"\*"\s*\]', blk) or re.search(r'Action\s*=\s*"?\*"?', blk):
        pr.append("no wildcard resource or action")
    return pr


def read(root, rel):
    p = Path(root, rel)
    need(p.is_file(), "missing " + rel)
    return p.read_bytes().decode("utf-8")


def ac1(root):
    man = json.loads(read(root, MANIFEST))
    D = man["root"] + "/"
    bad = []
    for f, want in man["others"].items():
        p = Path(root, D + f)
        if not (p.is_file() and sha(p.read_bytes()) == want):
            bad.append(f)
    need(not bad, "files of the root must be byte-identical to the base: %s" % ", ".join(bad[:5]))
    base = read(root, BASE_IAM)
    need(sha(base.encode("utf-8")) == man["iam_tf_sha256"], "the pinned iam.tf base copy is not the base the order names (sha256)")
    new = read(root, D + "iam.tf")
    need(new != base, "iam.tf is unchanged from the base")
    pr = insertion_problems(base, new)
    need(not pr, "; ".join(pr))
    need("\r" not in new or "\r" in base, "iam.tf must keep LF line endings")


def ac2(root):
    man = json.loads(read(root, MANIFEST))
    pr = semantic_problems(read(root, BASE_IAM), read(root, man["root"] + "/iam.tf"))
    need(not pr, "; ".join(pr))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    good = ('module "txn_policy_name" {\n  source = "../modules/opal_name"\n  system = "orion"\n  kind = "policy"\n}\n'
            'resource "aws_iam_role_policy" "%s" {\n  name = module.txn_policy_name.name\n  role = aws_iam_role.inf_gold_layer.id\n  policy = jsonencode({\n    Statement = [\n'
            '      {\n        Sid = "%s"\n        Effect = "Allow"\n        Action = ["s3:GetObject"]\n        Resource = local.txn_silver_object_arns\n      },\n'
            '      {\n        Sid = "%s"\n        Effect = "Allow"\n        Action = ["s3:ListBucket"]\n        Resource = local.txn_silver_bucket_arn\n        Condition = {\n          StringLike = { "s3:prefix" = local.txn_silver_list_prefixes }\n        }\n      },\n'
            '      {\n        Sid = "%s"\n        Effect = "Allow"\n        Action = ["s3:PutObject"]\n        Resource = local.account_transaction_gold_arns\n      }\n    ]\n  })\n}\n') % ((RESOURCE_LABEL,) + SIDS)
    base = "# base\n"
    good = 'locals {\n  txn_silver_key = "${x}/silver/fact_transactions"\n  txn_gold_key = "irpt/${y}/gold/account_transaction"\n}\n' + good
    arm("semantic-green", semantic_problems(base, base + good), [])
    arm("insertion-green", insertion_problems(base, base + good), [])
    arm("insertion-removed", len(insertion_problems(base, "x\n")), 1)
    arm("resource-missing", len(semantic_problems(base, base)), 1)
    arm("extra-action-red", len(semantic_problems(base, base + good.replace('["s3:PutObject"]', '["s3:PutObject", "s3:DeleteObject"]'))) >= 1, True)
    arm("typed-bucket-red", len(semantic_problems(base, base + good.replace("local.account_transaction_gold_arns", '"arn:aws:s3:::opal-data-inflection/x/*"'))) >= 1, True)
    arm("wildcard-red", len(semantic_problems(base, base + good.replace("local.account_transaction_gold_arns", '"*"'))) >= 1, True)
    arm("list-without-condition-red", len(semantic_problems(base, base + good.replace('Condition = {\n          StringLike = { "s3:prefix" = local.txn_silver_list_prefixes }\n        }', 'X = 1'))) >= 1, True)
    arm("wrong-role-red", len(semantic_problems(base, base + good.replace("aws_iam_role.inf_gold_layer.id", "aws_iam_role.other.id"))) >= 1, True)
    arm("name-not-from-module-red", len(semantic_problems(base, base + good.replace("module.txn_policy_name.name", '"typed-name"'))) >= 1, True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF137-5-AC1": ac1, "DBF137-5-AC2": ac2}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
