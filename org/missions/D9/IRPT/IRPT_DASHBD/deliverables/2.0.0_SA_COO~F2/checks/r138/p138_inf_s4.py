"""IRPT_DASHBD round 138, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the Inflection runner policy gains S4: ListBucket on the Inflection GOLD prefix (cell DB-f-2603).

  The CTO's ruling on the bounded default (msg 10145, item 4 B) makes the launcher read the newest written day at the gold prefix, and his msg 10239: "s3:ListBucket on
  opal-data-inflection, conditioned on s3:prefix equal to irpt/inflection/gold/account_transaction/ and its children (address() output); no GetObject on gold; XA-a222
  condition 2's form applies". The policy block of cell DB-f-2501 (resource inf_gold_layer_account_transaction, merged at 3e5d4896e2) is the base: this cell is a PURE INSERTION
  into it (a statement S4 placed between S2 and S3, and the two gold list locals beside the existing gold locals); S1 to S3 stay byte-for-byte.

  DBF138-3-AC1  the root's 46 other files are byte-identical and iam.tf is a pure insertion of ASCII lines against the pinned base (sha256 31e06b5e051e..)
  DBF138-3-AC2  the meaning: the policy carries S1..S4, S1 to S3 unchanged, S4 Allow s3:ListBucket on the gold bucket conditioned by StringLike on s3:prefix over the gold key and its children,
                no gold GetObject, nothing typed, no wildcard

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

R136 = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/"
R138 = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r138/"
BASE_IAM = R138 + "inf_iam_r138_base.tf.txt"
MANIFEST = R136 + "inf_pipeline_base_manifest.json"
BASE_SHA256 = "31e06b5e051ef3bc0457127bba1e22f0dd5c0cabe58c14858c3518bedb8ccc77"
RESOURCE_LABEL = "inf_gold_layer_account_transaction"
S123 = ("S1ReadOrionInflectionTransactionsSilverOnly", "S2ListOrionInflectionTransactionsSilverOnly", "S3PutInflectionAccountTransactionGoldOnly")
S4 = "S4ListInflectionAccountTransactionGoldOnly"


def _load_base(root_hint):
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("p137_inf_tf_for_s4", str(here.parent / "r136" / "p137_inf_tf.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = _load_base(None)
Fail, need, sha, read = B.Fail, B.need, B.sha, B.read


def semantic_problems(base, new):
    pr = []
    blk, bblk = B.block_of(new, RESOURCE_LABEL), B.block_of(base, RESOURCE_LABEL)
    if blk is None or bblk is None:
        return ['the base and the new iam.tf must both carry resource "aws_iam_role_policy" "%s"' % RESOURCE_LABEL]
    for sid in S123:
        a, b = B.statement_text(bblk, sid), B.statement_text(blk, sid)
        if a is None or b is None or a != b:
            pr.append("statement %s must be present and byte-for-byte unchanged" % sid)
    if len(re.findall(r'Sid\s*=\s*"%s"' % S4, blk)) != 1:
        pr.append("the policy must carry the statement %s exactly once" % S4)
    s4 = B.statement_text(blk, S4)
    if s4 is not None:
        if not re.search(r'Effect\s*=\s*"Allow"', s4):
            pr.append("S4 must be Allow")
        if not re.search(r"Action\s*=\s*\[\s*\"s3:ListBucket\"\s*\]", s4):
            pr.append("S4 Action must be exactly [\"s3:ListBucket\"]")
        if "s3:GetObject" in s4 or "s3:PutObject" in s4:
            pr.append("S4 must not carry GetObject or PutObject")
        if not (re.search(r"Resource\s*=", s4) and "txn_gold" in s4.split("Condition")[0] and "silver" not in s4):
            pr.append("S4 Resource must be the gold bucket (a txn_gold local) and must not name the silver bucket")
        if not ("Condition" in s4 and "StringLike" in s4 and "s3:prefix" in s4 and "txn_gold" in s4.split("Condition", 1)[1]):
            pr.append("S4 must be conditioned by StringLike on s3:prefix over the gold key and its children (a txn_gold local)")
    if "opal-data-" in blk:
        pr.append("no bucket name may be typed (opal-data-...)")
    if re.search(r'Resource\s*=\s*"\*"|Resource\s*=\s*\[\s*"\*"\s*\]', blk) or re.search(r'Action\s*=\s*"?\*"?', blk):
        pr.append("no wildcard resource or action")
    acts = sorted(set(re.findall(r'"([a-z0-9]+:[A-Za-z*]+)"', blk)) - {"s3:prefix"})
    if acts != ["s3:GetObject", "s3:ListBucket", "s3:PutObject"]:
        pr.append("the policy's actions must stay exactly s3:GetObject, s3:ListBucket and s3:PutObject: %r" % acts)
    added = B.added_text(base, new)
    if "txn_gold" not in added:
        pr.append("the inserted text must use the txn_gold locals")
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
    pr = B.insertion_problems(base, new)
    need(not pr, "; ".join(pr))
    need("\r" not in new, "iam.tf must keep LF line endings")


def ac2(root):
    pr = semantic_problems(read(root, BASE_IAM), read(root, "infra/aws/terraform/inf-pipeline/iam.tf"))
    need(not pr, "; ".join(pr))


def _reference(base):
    """A reference insertion for the selftest and the positive control: S4 between S2 and S3, and two gold locals."""
    s4 = ('      {\n        Sid      = "%s"\n        Effect   = "Allow"\n        Action   = ["s3:ListBucket"]\n        Resource = [local.txn_gold_bucket_arn]\n'
          '        Condition = {\n          StringLike = { "s3:prefix" = local.txn_gold_list_prefixes }\n        }\n      },\n') % S4
    anchor = '      {\n        Sid      = "S3PutInflectionAccountTransactionGoldOnly"'
    assert base.count(anchor) == 1
    out = base.replace(anchor, s4 + anchor)
    loc = ('  txn_gold_bucket_arn     = "arn:aws:s3:::${local.txn_gold_bucket}"\n'
           '  txn_gold_list_prefixes  = [local.txn_gold_key, "${local.txn_gold_key}/*"]\n')
    la = '  txn_gold_object_arns  = ["arn:aws:s3:::${local.txn_gold_bucket}/${local.txn_gold_key}/*"]\n'
    assert out.count(la) == 1
    return out.replace(la, la + loc)


def selftest(root):
    bad = count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    base = read(root, BASE_IAM)
    good = _reference(base)
    arm("reference-semantic-green", semantic_problems(base, good), [])
    arm("reference-insertion-green", B.insertion_problems(base, good), [])
    arm("unchanged-red", len(semantic_problems(base, base)) >= 1, True)
    arm("s4-getobject-red", len(semantic_problems(base, good.replace('Action   = ["s3:ListBucket"]\n        Resource = [local.txn_gold_bucket_arn]', 'Action   = ["s3:ListBucket", "s3:GetObject"]\n        Resource = [local.txn_gold_bucket_arn]'))) >= 1, True)
    arm("s4-silver-bucket-red", len(semantic_problems(base, good.replace("[local.txn_gold_bucket_arn]", "[local.txn_silver_bucket_arn]"))) >= 1, True)
    arm("s4-no-condition-red", len(semantic_problems(base, good.replace('        Condition = {\n          StringLike = { "s3:prefix" = local.txn_gold_list_prefixes }\n        }\n', ''))) >= 1, True)
    arm("s4-typed-bucket-red", len(semantic_problems(base, good.replace("[local.txn_gold_bucket_arn]", '["arn:aws:s3:::opal-data-inflection"]'))) >= 1, True)
    arm("s3-changed-red", len(semantic_problems(base, good.replace('Action   = ["s3:PutObject"]\n        Resource = local.txn_gold_object_arns', 'Action   = ["s3:PutObject"]\n        Resource = ["*"]'))) >= 1, True)
    arm("s4-twice-red", len(semantic_problems(base, good.replace('      {\n        Sid      = "S3Put', '      {\n        Sid      = "%s"\n        Effect   = "Allow"\n        Action   = ["s3:ListBucket"]\n        Resource = [local.txn_gold_bucket_arn]\n        Condition = {\n          StringLike = { "s3:prefix" = local.txn_gold_list_prefixes }\n        }\n      },\n      {\n        Sid      = "S3Put' % S4))) >= 1, True)
    arm("insertion-removed-red", len(B.insertion_problems(base, good.replace("# =====", "# ---", 1))) >= 1, True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 3 and argv[1] == "--selftest":
        return selftest(argv[2])
    if len(argv) != 3 or argv[2] not in ("DBF138-3-AC1", "DBF138-3-AC2"):
        print("usage: p138_inf_s4.py <repo_root> DBF138-3-AC1|AC2 | --selftest <repo_root>")
        return 2
    try:
        {"DBF138-3-AC1": ac1, "DBF138-3-AC2": ac2}[argv[2]](argv[1])
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
