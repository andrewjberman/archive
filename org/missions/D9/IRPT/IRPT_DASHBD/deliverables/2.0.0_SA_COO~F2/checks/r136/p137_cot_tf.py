"""IRPT_DASHBD round 137, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the COTTONWOOD TRANSACTION WRITE STATEMENT in the account-return-daily Terraform root (cell DB-f-2302).

  The CTO's ruling (XA-20261016T224156Z-3c21, msg 10002; reply 9979): the host is the landing function; the write grant is a NEW statement of its own (the existing
  `WriteTheOneAccountReturnDailyGoldPrefixOnly` is named for exactly one prefix, so a second resource would make its name false); any READ grant would be scoped to
  Cottonwood's own prefix by address() output (the sizing read found none needed, so none is added).
  `locals.tf` gains, by PURE INSERTION, the table constant `irpt_arc_gold_table_transaction`; `iam.tf` gains, by PURE INSERTION, ONE new statement
  `WriteTheAccountTransactionGoldPrefixOnly`: effect Allow, action `s3:PutObject` only, ONE resource built from the gold-bucket local, the firm local and the table
  constant, no condition. Every existing statement, `lambda.tf`, `main.tf` and `schedule.tf` are byte-identical. No plan is run here.
  DBF137-3-AC1 (the bytes and the insertions), DBF137-3-AC2 (the meaning)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import difflib
import hashlib
import re
import sys
from pathlib import Path

ROOT_DIR = "infra/aws/terraform/investor-reporting/account-return-daily/"
R = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/"
BASES = {"iam.tf": (R + "cot_iam_base.tf.txt", "be6fe3f38597c4acb36afe9da66b7d3f2a4883deb365e25c3f6482912a3662b8"),
         "locals.tf": (R + "cot_locals_base.tf.txt", "8414bb4980d4773eb6c717ab26e655cafc65b8dc1ae1e87ff53695859d215746")}
UNCHANGED = {"lambda.tf": "736826f6e6d8e711d94cb18c3d487ccfcd7bb2447655b2860e6c276dbcd749e8",
             "main.tf": "72245428da82e06843715f89dee62536c952792af136891e7c764d24e0ab381b",
             "schedule.tf": "8bcf2a5295a5f55ff6991dbeee07ddaf030e4d7381e537a606dc23b7d23f82de"}
SID = "WriteTheAccountTransactionGoldPrefixOnly"
OLD_SID = "WriteTheOneAccountReturnDailyGoldPrefixOnly"
TABLE_RE = re.compile(r'^\s*irpt_arc_gold_table_transaction\s*=\s*"account_transaction"\s*$', re.M)
RESOURCE = '"arn:aws:s3:::${local.irpt_arc_gold_bucket}/irpt/${local.irpt_arc_firm}/gold/${local.irpt_arc_gold_table_transaction}/*"'


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


def statement_block(text, sid):
    """The text of the `statement { ... }` block whose sid is `sid` (braces balanced), or None."""
    m = re.search(r'statement\s*\{[^{}]*?sid\s*=\s*"%s"' % re.escape(sid), text, re.S)
    if not m:
        return None
    start = text.rfind("statement", 0, m.end())
    i = text.index("{", start)
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[start:j + 1]
    return None


def semantic_problems(base_iam, new_iam, base_locals, new_locals):
    pr = []
    if not TABLE_RE.search(new_locals):
        pr.append('locals.tf must declare irpt_arc_gold_table_transaction = "account_transaction"')
    blk = statement_block(new_iam, SID)
    if blk is None:
        return pr + ["iam.tf must carry the new statement with sid %s" % SID]
    if len(re.findall(r'\bsid\s*=\s*"%s"' % SID, new_iam)) != 1:
        pr.append("the sid %s must appear exactly once" % SID)
    if not re.search(r'effect\s*=\s*"Allow"', blk):
        pr.append("the new statement's effect must be Allow")
    acts = re.search(r"actions\s*=\s*\[([^\]]*)\]", blk)
    if not acts or [a.strip() for a in acts.group(1).split(",") if a.strip()] != ['"s3:PutObject"']:
        pr.append('the new statement\'s actions must be exactly ["s3:PutObject"]')
    res = re.search(r"resources\s*=\s*\[([^\]]*)\]", blk, re.S)
    got = [x.strip() for x in res.group(1).split(",") if x.strip()] if res else None
    if got != [RESOURCE]:
        pr.append("the new statement's resources must be exactly [%s]" % RESOURCE)
    if re.search(r"\bcondition\s*\{", blk):
        pr.append("the new statement must carry no condition")
    if statement_block(base_iam, OLD_SID) != statement_block(new_iam, OLD_SID) or statement_block(new_iam, OLD_SID) is None:
        pr.append("the existing write statement %s must be unchanged" % OLD_SID)
    nbase = len(re.findall(r"\n\s*statement\s*\{", base_iam))
    nnew = len(re.findall(r"\n\s*statement\s*\{", new_iam))
    if nnew != nbase + 1:
        pr.append("iam.tf must hold exactly one more statement block than the base (%d), found %d" % (nbase, nnew))
    if "s3:GetObject" in blk or "s3:ListBucket" in blk:
        pr.append("the new statement grants no read or list")
    return pr


def read(root, rel):
    p = Path(root, rel)
    need(p.is_file(), "missing " + rel)
    return p.read_bytes().decode("utf-8")


def load_base(root, name):
    rel, want = BASES[name]
    b = Path(root, rel)
    need(b.is_file(), "missing the pinned base copy " + rel)
    data = b.read_bytes()
    need(sha(data) == want, "the pinned base copy of %s is not the base the order names (sha256)" % name)
    return data.decode("utf-8")


def ac1(root):
    for name, want in UNCHANGED.items():
        p = Path(root, ROOT_DIR + name)
        need(p.is_file() and sha(p.read_bytes()) == want, "%s must be byte-identical to the base (sha256 differs or the file is missing)" % name)
    pr = []
    for name in BASES:
        base, new = load_base(root, name), read(root, ROOT_DIR + name)
        pr += ["%s: %s" % (name, x) for x in insertion_problems(base, new)]
        if new == base:
            pr.append("%s is unchanged from the base" % name)
    need(not pr, "; ".join(pr))


def ac2(root):
    pr = semantic_problems(load_base(root, "iam.tf"), read(root, ROOT_DIR + "iam.tf"), load_base(root, "locals.tf"), read(root, ROOT_DIR + "locals.tf"))
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

    old = 'statement {\n  sid = "%s"\n  effect = "Allow"\n  actions = ["s3:PutObject"]\n  resources = ["arn:x"]\n}\n' % OLD_SID
    new_stmt = ('statement {\n  sid = "%s"\n  effect = "Allow"\n  actions = ["s3:PutObject"]\n  resources = [%s]\n}\n' % (SID, RESOURCE))
    base_iam = "\n" + old
    new_iam = "\n" + old + "\n" + new_stmt
    loc_b = "a = 1\n"
    loc_n = 'a = 1\nirpt_arc_gold_table_transaction = "account_transaction"\n'
    arm("semantic-green", semantic_problems(base_iam, new_iam, loc_b, loc_n), [])
    arm("insertion-green", insertion_problems(base_iam, new_iam), [])
    arm("insertion-removed", len(insertion_problems(base_iam, "x\n")), 1)
    arm("no-new-statement", len(semantic_problems(base_iam, base_iam, loc_b, loc_n)) >= 1, True)
    arm("second-resource-in-old-red", len(semantic_problems(base_iam, new_iam.replace('resources = ["arn:x"]', 'resources = ["arn:x", "arn:y"]'), loc_b, loc_n)) >= 1, True)
    arm("read-action-red", len(semantic_problems(base_iam, new_iam.replace('actions = ["s3:PutObject"]\n  resources = [%s]' % RESOURCE, 'actions = ["s3:PutObject", "s3:GetObject"]\n  resources = [%s]' % RESOURCE), loc_b, loc_n)) >= 1, True)
    arm("typed-resource-red", len(semantic_problems(base_iam, new_iam.replace(RESOURCE, '"arn:aws:s3:::opal-data-cottonwood/x/*"'), loc_b, loc_n)) >= 1, True)
    arm("missing-table-red", len(semantic_problems(base_iam, new_iam, loc_b, loc_b)), 1)
    arm("block-extraction", statement_block(new_iam, SID) is not None and SID in statement_block(new_iam, SID), True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF137-3-AC1": ac1, "DBF137-3-AC2": ac2}
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
