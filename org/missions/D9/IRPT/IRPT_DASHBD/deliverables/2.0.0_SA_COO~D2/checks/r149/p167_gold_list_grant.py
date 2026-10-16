"""IRPT_DASHBD round 149, workstream GOLDLIST (issuer 2.0.0_SA_COO~D2) -- DB-b-299, the LISTING GRANT the 49 Financial gold function's filled-report stage lacks (row IRPT_BCKEND-D2-S219, hop 1's first scheduled fire):
the role policy's statement `ListExactlyTheSixGoldPrefixes` takes its prefix patterns from `local.irpt_rg_gold_list_pattern`, which is built from the READ prefixes only; the filled report-values prefix is in the WRITE list
(`irpt_rg_gold_write_arns`) but in no list pattern, so the catch-up listing of that prefix is denied (AccessDenied on s3:ListBucket) and the stage writes nothing. The edit is ONE expression in locals.tf: the list
pattern also takes `local.irpt_rg_gold_filled_prefix`. NO read grant is added and the write list does not change. LOCAL: one Terraform file; nothing is planned, applied or run.

  DB-b-299 (~241)   infra/aws/terraform/investor-reporting/reporting-gold/locals.tf + a facts record
                    DB167-1-AC1 (locals.tf differs from the base in exactly one expression line, plus comment lines; every other file of the root is byte-identical),
                    DB167-1-AC2 (the new expression, evaluated on the root's own declared prefixes, lists the filled prefix and every earlier pattern in the same order, and the read and write lists are untouched),
                    DB167-1-AC3 (the facts record equals the recount; the grant)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~241"
REC_REL = D + AUTHOR + "/RD_GOLD_LIST_GRANT_FACTS_R149.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-299.gold-listing-grant-for-the-filled-prefix.md"
ROOT_DIR = "infra/aws/terraform/investor-reporting/reporting-gold/"
LOCALS_REL = ROOT_DIR + "locals.tf"
OTHERS = ["iam.tf", "lambda.tf", "main.tf", "schedule.tf"]
OLD_EXPR = "[for p in local.irpt_rg_gold_read_prefixes : \"${p}*\"]"
NEW_EXPR = "[for p in concat(local.irpt_rg_gold_read_prefixes, [local.irpt_rg_gold_filled_prefix]) : \"${p}*\"]"
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    need(r.returncode == 0, "git %s: %s" % (" ".join(a[:2]), r.stderr.decode("utf-8", "replace").strip()[:200]))
    return r.stdout


def base_commit(root):
    out = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).decode().split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


def own_commits(root):
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base_commit(root) + "..HEAD").decode().split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def norm(line):
    return re.sub(r"\s+", " ", line.strip())


def check_diff(base_text, new_text):
    """locals.tf: every line of the base survives in order except the ONE list-pattern line, which becomes the new expression; other added lines are comments only."""
    bl, nl = base_text.split("\n"), new_text.split("\n")
    pat = [i for i, ln in enumerate(bl) if norm(ln).startswith("irpt_rg_gold_list_pattern =") and OLD_EXPR in ln]
    need(len(pat) == 1, "the base must hold exactly one list-pattern line with the old expression")
    j = 0
    changed = 0
    for i, ln in enumerate(bl):
        while j < len(nl) and nl[j] != ln and nl[j].strip().startswith("#"):
            j += 1  # a comment line added by the worker
        need(j < len(nl), "the new file ends before base line %d: %r" % (i + 1, ln[:60]))
        if i in pat:
            need(norm(nl[j]).startswith("irpt_rg_gold_list_pattern =") and NEW_EXPR in nl[j] and OLD_EXPR not in nl[j], "the list-pattern line must read %s" % NEW_EXPR)
            changed += 1
        else:
            need(nl[j] == ln, "base line %d changed or moved: %r became %r" % (i + 1, ln[:70], nl[j][:70]))
        j += 1
    rest = nl[j:]
    need(all(x.strip() == "" or x.strip().startswith("#") for x in rest), "lines added after the base's end must be comments or blank")
    need(changed == 1, "exactly one expression line changes")
    return True


def eval_patterns(text, expr_new):
    """The root's own declarations, read as text: the read prefixes and the filled prefix, as templates; returns the list pattern (templates) the expression yields."""
    reads = re.search(r"irpt_rg_gold_read_prefixes\s*=\s*concat\(\[([^\]]*)\],\s*local\.irpt_rg_gold_lot_prefixes\)", text)
    need(reads is not None, "locals.tf no longer declares irpt_rg_gold_read_prefixes as concat([...], local.irpt_rg_gold_lot_prefixes)")
    head = [x.strip() for x in reads.group(1).split(",") if x.strip()]
    lots = re.search(r"irpt_rg_gold_lot_prefixes\s*=\s*\[([^\]]*)\]", text)
    need(lots is not None, "locals.tf no longer declares irpt_rg_gold_lot_prefixes")
    lot = [x.strip() for x in lots.group(1).split(",") if x.strip()]
    base = head + lot
    return base + (["local.irpt_rg_gold_filled_prefix"] if "concat(local.irpt_rg_gold_read_prefixes, [local.irpt_rg_gold_filled_prefix])" in expr_new else [])


def check_semantics(base_text, new_text):
    old = eval_patterns(base_text, OLD_EXPR)
    new = eval_patterns(new_text, NEW_EXPR)
    need(new == old + ["local.irpt_rg_gold_filled_prefix"], "the list patterns must be the earlier patterns in the same order, then the filled prefix; got %s" % new)
    need("local.irpt_rg_gold_filled_prefix" not in " ".join(old), "the base must not list the filled prefix already")
    # the read and write lists are untouched
    for key in ("irpt_rg_gold_read_arns", "irpt_rg_gold_write_arns", "irpt_rg_gold_read_prefixes"):
        m1 = re.search(r"%s\s*=.*?(?=\n\s*\n|\n\s*#|\n\s*irpt_)" % key, base_text, re.S)
        m2 = re.search(r"%s\s*=.*?(?=\n\s*\n|\n\s*#|\n\s*irpt_)" % key, new_text, re.S)
        need(m1 is not None and m2 is not None and m1.group(0) == m2.group(0), "the %s declaration changed" % key)
    return True


def check_facts(rec):
    exp = {"file", "expression_old", "expression_new", "read_list_changed", "write_list_changed", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["file"] == LOCALS_REL and rec["expression_old"] == OLD_EXPR and rec["expression_new"] == NEW_EXPR and rec["read_list_changed"] is False and rec["write_list_changed"] is False, "file, expressions or the two unchanged-list statements differ")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def check_grant(changed):
    bad = [f for f in changed if f != LOCALS_REL and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(LOCALS_REL in changed, "locals.tf must change")
    return True


def run(root, cid):
    import json
    root = Path(root)
    base = base_commit(root)
    bt = git(root, "show", "%s:%s" % (base, LOCALS_REL)).decode("utf-8")
    nt = (root / LOCALS_REL).read_bytes().decode("utf-8")
    if cid == "DB167-1-AC1":
        check_diff(bt, nt)
        for f in OTHERS:
            need(git(root, "show", "%s:%s%s" % (base, ROOT_DIR, f)) == (root / ROOT_DIR / f).read_bytes(), "%s must be byte-identical to the base" % f)
        print("OK: locals.tf differs from the base in exactly the list-pattern expression (plus comments); iam.tf, lambda.tf, main.tf and schedule.tf are byte-identical")
        return True
    if cid == "DB167-1-AC2":
        check_diff(bt, nt)
        check_semantics(bt, nt)
        print("OK: the new list pattern is the earlier patterns in the same order and then the filled prefix; the read prefixes, read arns and write arns declarations are untouched; no read grant is added")
        return True
    if cid == "DB167-1-AC3":
        check_diff(bt, nt)
        check_facts(json.loads((root / REC_REL).read_bytes().decode("utf-8")))
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).decode().split())
        check_grant(changed)
        print("OK: the facts record states the two expressions and that the read and write lists are unchanged; %d files changed, all in the grant" % len(changed))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    base = ("locals {\n  # comment\n  irpt_rg_gold_lot_prefixes  = [local.a, local.b]\n  irpt_rg_gold_read_prefixes = concat([local.h, local.r, local.c], local.irpt_rg_gold_lot_prefixes)\n"
            "  irpt_rg_gold_read_arns     = [for p in local.irpt_rg_gold_read_prefixes : \"arn:${p}*\"]\n  irpt_rg_gold_list_pattern  = " + OLD_EXPR + "\n\n  irpt_rg_gold_filled_prefix = \"x/\"\n"
            "  irpt_rg_gold_write_arns = [\n    \"w\",\n  ]\n\n}\n")
    new = base.replace("irpt_rg_gold_list_pattern  = " + OLD_EXPR, "# the filled prefix is listed too (S219)\n  irpt_rg_gold_list_pattern  = " + NEW_EXPR)
    assert check_diff(base, new) and check_semantics(base, new)
    arms = (("unchanged", lambda t: t.replace(NEW_EXPR, OLD_EXPR)), ("other line changed", lambda t: t.replace('"w"', '"w2"')), ("line removed", lambda t: t.replace("  # comment\n", "")),
            ("read arns widened", lambda t: t.replace('"arn:${p}*"', '"arn2:${p}*"')), ("wrong expression", lambda t: t.replace(NEW_EXPR, "[for p in local.irpt_rg_gold_read_prefixes : \"${p}*\", local.irpt_rg_gold_filled_prefix]")),
            ("code added at the end", lambda t: t + "x = 1\n"), ("order swapped", lambda t: t.replace("concat(local.irpt_rg_gold_read_prefixes, [local.irpt_rg_gold_filled_prefix])", "concat([local.irpt_rg_gold_filled_prefix], local.irpt_rg_gold_read_prefixes)")))
    for label, fn in arms:
        t2 = fn(new)
        red(lambda: (check_diff(base, t2), check_semantics(base, t2)), label)
    rec = {"file": LOCALS_REL, "expression_old": OLD_EXPR, "expression_new": NEW_EXPR, "read_list_changed": False, "write_list_changed": False, "words": "w" * 100}
    assert check_facts(rec)
    farms = (("file", lambda r: r.update(file="x")), ("old", lambda r: r.update(expression_old="x")), ("new", lambda r: r.update(expression_new="x")), ("read", lambda r: r.update(read_list_changed=True)),
             ("write", lambda r: r.update(write_list_changed=True)), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2), label)
    assert check_grant({LOCALS_REL, D + AUTHOR + "/x.json"})
    red(lambda: check_grant({D + AUTHOR + "/x.json"}), "no locals")
    red(lambda: check_grant({LOCALS_REL, "lib/x.py"}), "outside grant")
    print("selftest: diff+semantics (%d red arms), facts (%d) and grant (2) clauses behave" % (len(arms), len(farms)))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
