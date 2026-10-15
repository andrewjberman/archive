"""IRPT_DASHBD round 129, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-261, the COTTONWOOD LANDING ROOT's SCHEDULER POLICY NAME. The AE applier's safe-apply of the signed pair was
REFUSED by the naming-plan gate (rc 7, nothing written): `aws_iam_role_policy.irpt_account_return_daily_scheduler` takes its `name` from the scheduler ROLE's name module, so it is named
`irpt-cot-account-return-daily-scheduler-role`, a role name on a policy; the builder's policy name is `irpt-cot-account-return-daily-scheduler-policy`. The execution policy already uses its
own policy-name module. This cell gives the scheduler policy its own builder name and changes nothing else. LOCAL: nothing is planned, applied or deployed.

  DB-b-261 (~213)   iam.tf: one `opal_name` module (kind policy, qualifier scheduler) and the scheduler policy's `name` pointing at it; a facts record
                    DB129-1-AC1 (the HCL: only that module and that one attribute change, every other root file byte-equal),
                    DB129-1-AC2 (the REAL naming gate, run in plan mode on a synthetic plan holding the six named resources with names built from the root's own module arguments: no REFUSE),
                    DB129-1-AC3 (the facts record: six builder names, equal to the recount, and the gate's verdict line)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~213/RD_COT_NAMES_FACTS_R129.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-261.cottonwood-landing-root-scheduler-policy-builder-name.md"
ROOT_DIR = "infra/aws/terraform/investor-reporting/account-return-daily/"
IAM_TF = ROOT_DIR + "iam.tf"
GATE = ".tools/naming-apply-gate.py"
MODULE_NAME = "irpt_account_return_daily_scheduler_policy_name"
EXPECT_SCHEDULER_POLICY = "irpt-cot-account-return-daily-scheduler-policy"
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout.decode("utf-8", "replace"), r.returncode


def base_commit(root):
    out, _ = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(out.split(), "the order's first commit is not in this history")
    return out.split()[-1]


def norm_code(text):
    return [" ".join(ln.split()) for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


MODULE_BLOCK = re.compile(r'module\s+"%s"\s*\{(.*?)\n\}' % MODULE_NAME, re.S)


def module_args(text):
    m = MODULE_BLOCK.search(text)
    need(m is not None, "iam.tf must hold the module %s" % MODULE_NAME)
    blk = m.group(1)
    out = {}
    for k in ("source", "system", "function", "kind", "qualifier"):
        mm = re.search(r'^\s*%s\s*=\s*"([^"]*)"' % k, blk, re.M)
        need(mm is not None, "module %s lacks %s" % (MODULE_NAME, k))
        out[k] = mm.group(1)
    sc = re.search(r"^\s*scope\s*=\s*local\.(\w+)\s*$", blk, re.M)
    need(sc is not None, "module %s must take its scope from a local, never a typed firm" % MODULE_NAME)
    out["scope_local"] = sc.group(1)
    return out


# ------------------------------------------------------------------------------------------------ pure clauses
def check_hcl(base_text, new_text):
    a = module_args(new_text)
    need(a["source"] == "../../modules/opal_name" and a["system"] == "irpt" and a["function"] == "account-return-daily" and a["kind"] == "policy" and a["qualifier"] == "scheduler",
         "module %s must be opal_name for irpt / account-return-daily / policy / scheduler: %s" % (MODULE_NAME, a))
    sibling = re.search(r'module\s+"irpt_account_return_daily_scheduler_role_name"\s*\{.*?scope\s*=\s*local\.(\w+)', new_text, re.S)
    need(sibling is not None and sibling.group(1) == a["scope_local"], "the new module must take the same scope local as the scheduler role's module")
    stripped = MODULE_BLOCK.sub("", new_text)
    old_attr = "name = module.irpt_account_return_daily_scheduler_role_name.name"
    new_attr = "name = module.%s.name" % MODULE_NAME
    lines = norm_code(stripped)
    base = norm_code(base_text)
    need(lines.count(new_attr) == 1, "the scheduler policy's name must be exactly `%s`" % new_attr)
    swapped = [new_attr if ln == new_attr else ln for ln in lines]
    # the base holds the attribute pointing at the role-name module once for the role and once for the policy; the new file keeps it once (the role)
    need(base.count(old_attr) == 2 and swapped.count(old_attr) == 1, "the role must keep its own name module and only the policy's attribute may move")
    rebuilt = list(swapped)
    rebuilt[rebuilt.index(new_attr)] = old_attr
    need(rebuilt == base, "anything beyond the new module and the one attribute changed in the code (comments excluded, spacing normalised)")
    return True


def graded_names(builder_names, expect):
    need(len(builder_names) == 6 and builder_names[3] == expect, "the six builder names must include the scheduler policy %s: %s" % (expect, builder_names))
    return True


def check_gate_output(out):
    need("NAMING-PLAN:" in out and "REFUSE" not in out.split("NAMING-PLAN:")[1], "the naming gate refused: %s" % out.strip().splitlines()[-1:])
    need(out.count("NAMING CONFORMANT") == 6, "expected 6 CONFORMANT lines, read %d" % out.count("NAMING CONFORMANT"))
    need("NAMING REFUSE" not in out, "a NAMING REFUSE line is present")
    return True


def check_facts(rec, names, gate_line):
    exp = {"names", "scheduler_policy", "gate_verdict", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["names"] == names and rec["scheduler_policy"] == EXPECT_SCHEDULER_POLICY, "names or scheduler_policy differ from the builder recount")
    need(isinstance(rec["gate_verdict"], str) and rec["gate_verdict"].strip() == gate_line.strip(), "gate_verdict must be the gate's own last line as the checker reads it")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1500 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1500 characters with no long digit run")
    return True


# ------------------------------------------------------------------------------------------------ the live run
def build_names(root):
    sys.path.insert(0, str(root))
    from lib import opal_naming
    a = module_args((Path(root) / IAM_TF).read_text(encoding="utf-8"))
    land = json.loads((Path(root) / (D + "0.9.0_WK_IRPT_DASHBD~195/RD_CW_LANDING_FACTS_R120.json")).read_text(encoding="utf-8"))
    five = []
    for x in land["names"]:
        b = x["builder_args"]
        kw = {"qualifier": b["qualifier"]} if b.get("qualifier") else {}
        five.append(opal_naming.name(b["system"], b["scope"], b["function"], b["kind"], **kw))
    sched_policy = opal_naming.name(a["system"], land["names"][0]["builder_args"]["scope"], a["function"], a["kind"], qualifier=a["qualifier"])
    # order: function, execution role, execution policy, scheduler policy, scheduler role, schedule
    return [five[0], five[1], five[2], sched_policy, five[3], five[4]]


def run_gate(root, names):
    kinds = [("aws_lambda_function", "this"), ("aws_iam_role", "irpt_account_return_daily_execution"), ("aws_iam_role_policy", "irpt_account_return_daily_execution"),
             ("aws_iam_role_policy", "irpt_account_return_daily_scheduler"), ("aws_iam_role", "irpt_account_return_daily_scheduler"), ("aws_scheduler_schedule", "irpt_account_return_daily")]
    changes = []
    for (t, n), nm in zip(kinds, names):
        key = "function_name" if t == "aws_lambda_function" else "name"
        after = {key: nm}
        if t == "aws_iam_role_policy":
            after.update({"role": "r", "policy": "{}"})
        changes.append({"address": "%s.%s" % (t, n), "mode": "managed", "type": t, "name": n, "change": {"actions": ["create"], "after": after}})
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "plan.json"
        p.write_text(json.dumps({"format_version": "1.2", "resource_changes": changes}), encoding="utf-8")
        r = subprocess.run([sys.executable, GATE, "--plan-json", str(p), "--root", ROOT_DIR.rstrip("/")], cwd=str(root), capture_output=True, text=True)
    return r.stdout + r.stderr


def run(root, cid):
    root = Path(root)
    base = base_commit(root)
    if cid == "DB129-1-AC1":
        bt, rc = git(root, "show", "%s:%s" % (base, IAM_TF))
        need(rc == 0, "cannot read the base iam.tf")
        check_hcl(bt, (root / IAM_TF).read_text(encoding="utf-8"))
        others, _ = git(root, "ls-tree", "-r", "--name-only", "HEAD", "--", ROOT_DIR)
        n = 0
        for f in others.split():
            if f != IAM_TF:
                need(git(root, "show", "HEAD:" + f)[0] == git(root, "show", "%s:%s" % (base, f))[0], "another root file changed: %s" % f)
                n += 1
        print("OK: iam.tf gains the opal_name module %s (policy / scheduler, scope from the same local as the role's) and the scheduler policy's name points at it; nothing else in the code moves; %d other root files byte-equal" % (MODULE_NAME, n))
        return True
    names = build_names(root)
    graded_names(names, EXPECT_SCHEDULER_POLICY)
    out = run_gate(root, names)
    if cid == "DB129-1-AC2":
        check_gate_output(out)
        print("OK: the real naming gate in plan mode grades the six named resources of the root, all CONFORMANT, no REFUSE (%s)" % out.strip().splitlines()[-1])
        return True
    if cid == "DB129-1-AC3":
        check_gate_output(out)
        rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
        check_facts(rec, names, out.strip().splitlines()[-1])
        print("OK: facts record: six builder names incl. %s, the gate's verdict line equal" % EXPECT_SCHEDULER_POLICY)
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    base = ('module "irpt_account_return_daily_scheduler_role_name" {\n  source    = "../../modules/opal_name"\n  system    = "irpt"\n  scope     = local.irpt_arc_firm\n  function  = "account-return-daily"\n'
            '  kind      = "role"\n  qualifier = "scheduler"\n}\n\nresource "aws_iam_role" "r" {\n  name = module.irpt_account_return_daily_scheduler_role_name.name\n}\n\n'
            'resource "aws_iam_role_policy" "p" {\n  name   = module.irpt_account_return_daily_scheduler_role_name.name\n  role   = aws_iam_role.r.id\n}\n')
    new = base.replace('resource "aws_iam_role" "r"', 'module "%s" {\n  source    = "../../modules/opal_name"\n  system    = "irpt"\n  scope     = local.irpt_arc_firm\n  function  = "account-return-daily"\n  kind      = "policy"\n  qualifier = "scheduler"\n}\n\nresource "aws_iam_role" "r"' % MODULE_NAME)
    new = new.replace("  name   = module.irpt_account_return_daily_scheduler_role_name.name\n  role", "  name   = module.%s.name\n  role" % MODULE_NAME)
    assert check_hcl(base, new)
    red(lambda: check_hcl(base, base), "no module")
    red(lambda: check_hcl(base, new.replace('kind      = "policy"', 'kind      = "role"')), "wrong kind")
    red(lambda: check_hcl(base, new.replace('qualifier = "scheduler"\n}\n\nresource "aws_iam_role" "r"', 'qualifier = "execution"\n}\n\nresource "aws_iam_role" "r"')), "wrong qualifier")
    red(lambda: check_hcl(base, new.replace("scope     = local.irpt_arc_firm\n  function  = \"account-return-daily\"\n  kind      = \"policy\"", "scope     = \"cottonwood\"\n  function  = \"account-return-daily\"\n  kind      = \"policy\"")), "typed firm")
    red(lambda: check_hcl(base, new.replace("module.%s.name\n  role" % MODULE_NAME, "module.irpt_account_return_daily_scheduler_role_name.name\n  role")), "attribute not moved")
    red(lambda: check_hcl(base, new + 'resource "x" "y" {}\n'), "extra code")
    red(lambda: check_hcl(base, new.replace('resource "aws_iam_role" "r" {\n  name = module.irpt_account_return_daily_scheduler_role_name.name', 'resource "aws_iam_role" "r" {\n  name = module.%s.name' % MODULE_NAME)), "role moved")
    names = ["f", "er", "ep", EXPECT_SCHEDULER_POLICY, "sr", "sc"]
    assert graded_names(names, EXPECT_SCHEDULER_POLICY)
    red(lambda: graded_names(names[:5], EXPECT_SCHEDULER_POLICY), "five names")
    red(lambda: graded_names(["f", "er", "ep", "irpt-cot-account-return-daily-scheduler-role", "sr", "sc"], EXPECT_SCHEDULER_POLICY), "role name on the policy")
    ok = "NAMING CONFORMANT x\n" * 6 + "NAMING-PLAN-DENOM: 6\nNAMING-PLAN: CONFORMANT 6 graded\n"
    assert check_gate_output(ok)
    red(lambda: check_gate_output(ok.replace("NAMING-PLAN: CONFORMANT 6 graded", "NAMING-PLAN: REFUSE 6 graded")), "refuse line")
    red(lambda: check_gate_output(ok.replace("NAMING CONFORMANT x\n", "NAMING REFUSE y\n", 1)), "a refuse")
    red(lambda: check_gate_output("NAMING CONFORMANT x\n" * 5 + "NAMING-PLAN: CONFORMANT 5 graded\n"), "five graded")
    rec = {"names": names, "scheduler_policy": EXPECT_SCHEDULER_POLICY, "gate_verdict": "NAMING-PLAN: CONFORMANT 6 graded", "words": "w" * 100}
    assert check_facts(rec, names, "NAMING-PLAN: CONFORMANT 6 graded")
    for label, fn in (("names", lambda r: r.update(names=["x"])), ("policy", lambda r: r.update(scheduler_policy="x")), ("verdict", lambda r: r.update(gate_verdict="other")),
                      ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2, names, "NAMING-PLAN: CONFORMANT 6 graded"), label)
    print("selftest: hcl (8 red arms), gate output (3 red arms), names and facts (8 red arms) clauses behave")
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
