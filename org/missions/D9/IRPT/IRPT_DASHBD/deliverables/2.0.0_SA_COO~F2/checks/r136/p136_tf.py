"""IRPT_DASHBD round 136, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the 49 FINANCIAL TRANSACTION WRITE PREFIX in the reporting-gold Terraform root (W2).

  DB-f-2202 (~2202) `infra/aws/terraform/investor-reporting/reporting-gold/locals.tf` gains, by PURE INSERTION, the table constant `irpt_rg_gold_table_transaction`, the prefix
                    `irpt_rg_gold_transaction_prefix` (built from the firm and the table constant, never typed) and ONE more element, LAST, in `irpt_rg_gold_write_arns`.
                    The read prefixes, the read arns and the list pattern do not change (no read or list grant); `iam.tf`, `lambda.tf`, `main.tf` and `schedule.tf` are byte-identical
                    (the PutObject statement takes the write list; its sid is kept). No plan is run here: the plan gate is the applier's, under a later signed pair.
                    DBF136-2-AC1 (the bytes and the insertion), DBF136-2-AC2 (the meaning)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import difflib
import hashlib
import re
import sys
from pathlib import Path

ROOT_DIR = "infra/aws/terraform/investor-reporting/reporting-gold/"
BASE = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/locals_base.tf.txt"
BASE_SHA256 = "1063ebb77489c7a273a125592e64ec15f9b112731d3e76ef154d5e55a8f71835"
UNCHANGED = {"iam.tf": "a9b82429beeb0b5386b2ea53cb33de8b9f713c527e299de5fb9295b92fb1fb0b",
             "lambda.tf": "a20ea4a0a21c3a899d09a964f379f7f1d5ff13274e80960d40fc254fe369bf46",
             "main.tf": "782bb13480997ac1cab4a39e69569be4fc24205b7a46c0eda74fe9fbb798037e",
             "schedule.tf": "6f92147a2a184cd6c1472f4707399b3d4062ef12cfac586bfe5203fd289cf225"}
NEW_ARN = '"arn:aws:s3:::${local.irpt_rg_gold_bucket}/${local.irpt_rg_gold_transaction_prefix}*",'
TABLE_RE = re.compile(r'^\s*irpt_rg_gold_table_transaction\s*=\s*"account_transaction"\s*$', re.M)
PREFIX_RE = re.compile(r'^\s*irpt_rg_gold_transaction_prefix\s*=\s*"irpt/\$\{local\.irpt_rg_firm\}/gold/\$\{local\.irpt_rg_gold_table_transaction\}/"\s*$', re.M)


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def insertion_problems(base, new):
    """Every base line survives in order (a pure insertion); the added lines are ASCII."""
    pr = []
    removed, added = [], []
    for d in difflib.unified_diff(base.splitlines(), new.splitlines(), lineterm="", n=0):
        if d.startswith("---") or d.startswith("+++") or d.startswith("@@"):
            continue
        (removed if d.startswith("-") else added).append(d[1:])
    if removed:
        pr.append("a base line was removed or changed: %r" % removed[0][:100])
    if any(not a.isascii() for a in added):
        pr.append("an added line is not ASCII")
    return pr


def write_elements(text):
    m = re.search(r"irpt_rg_gold_write_arns\s*=\s*\[(.*?)\n\s*\]", text, re.S)
    if not m:
        return None
    return [ln.strip() for ln in m.group(1).splitlines() if ln.strip().startswith('"arn:')]


def semantic_problems(base, new):
    pr = []
    if not TABLE_RE.search(new):
        pr.append('locals.tf must declare irpt_rg_gold_table_transaction = "account_transaction"')
    if not PREFIX_RE.search(new):
        pr.append("locals.tf must declare irpt_rg_gold_transaction_prefix from the firm and the table constant (irpt/${local.irpt_rg_firm}/gold/${local.irpt_rg_gold_table_transaction}/)")
    b, n = write_elements(base), write_elements(new)
    if b is None or n is None:
        pr.append("the write list irpt_rg_gold_write_arns could not be read")
    elif n != b + [NEW_ARN]:
        pr.append("irpt_rg_gold_write_arns must be the base's %d elements and then exactly %s as the LAST element" % (len(b), NEW_ARN))
    for name in ("irpt_rg_gold_read_prefixes", "irpt_rg_gold_read_arns", "irpt_rg_gold_list_pattern"):
        bl = [ln for ln in base.splitlines() if re.match(r"\s*%s\s*=" % name, ln)]
        nl = [ln for ln in new.splitlines() if re.match(r"\s*%s\s*=" % name, ln)]
        if bl != nl or not nl:
            pr.append("%s must be unchanged (the transaction prefix is written, never read or listed here)" % name)
        elif "transaction" in nl[0]:
            pr.append("%s must not name the transaction prefix" % name)
    return pr


def load(root):
    p = Path(root, ROOT_DIR + "locals.tf")
    need(p.is_file(), "missing " + ROOT_DIR + "locals.tf")
    bp = Path(root, BASE)
    need(bp.is_file(), "missing the pinned base copy " + BASE)
    base_bytes = bp.read_bytes()
    need(sha(base_bytes) == BASE_SHA256, "the pinned base copy is not the base the order names (sha256)")
    return base_bytes.decode("utf-8"), p.read_bytes().decode("utf-8")


def ac1(root):
    for name, want in UNCHANGED.items():
        p = Path(root, ROOT_DIR + name)
        need(p.is_file() and sha(p.read_bytes()) == want, "%s must be byte-identical to the base (sha256 differs or the file is missing)" % name)
    base, new = load(root)
    pr = insertion_problems(base, new)
    need(not pr, "; ".join(pr))
    need(new != base, "locals.tf is unchanged from the base")
    need(b"\r" not in Path(root, ROOT_DIR + "locals.tf").read_bytes() or b"\r" in base.encode("utf-8"), "locals.tf must keep LF line endings")


def ac2(root):
    base, new = load(root)
    pr = semantic_problems(base, new)
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

    reads = 'irpt_rg_gold_read_prefixes = [1]\nirpt_rg_gold_read_arns = [2]\nirpt_rg_gold_list_pattern = [3]\n'
    b = 'x = 1\n' + reads + 'irpt_rg_gold_write_arns = [\n  "arn:aws:s3:::${local.irpt_rg_gold_bucket}/${local.a}*",\n]\n'
    n = ('x = 1\n' + reads + 'irpt_rg_gold_table_transaction = "account_transaction"\n'
         'irpt_rg_gold_transaction_prefix = "irpt/${local.irpt_rg_firm}/gold/${local.irpt_rg_gold_table_transaction}/"\n'
         'irpt_rg_gold_write_arns = [\n  "arn:aws:s3:::${local.irpt_rg_gold_bucket}/${local.a}*",\n  ' + NEW_ARN + '\n]\n')
    arm("insertion-green", insertion_problems(b, n), [])
    arm("insertion-removed", len(insertion_problems(b, "x = 2\n")), 1)
    arm("write-elements", write_elements(b), ['"arn:aws:s3:::${local.irpt_rg_gold_bucket}/${local.a}*",'])
    arm("semantic-green", semantic_problems(b, n), [])
    first = '  "arn:aws:s3:::${local.irpt_rg_gold_bucket}/${local.a}*",\n'
    arm("semantic-not-last", len(semantic_problems(b, n.replace(first + "  " + NEW_ARN + "\n", "  " + NEW_ARN + "\n" + first))), 1)
    arm("semantic-missing-table", len(semantic_problems(b, b)) >= 3, True)
    arm("hashes-are-sha256", all(len(v) == 64 for v in UNCHANGED.values()) and len(BASE_SHA256) == 64, True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF136-2-AC1": ac1, "DBF136-2-AC2": ac2}
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
