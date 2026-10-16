"""IRPT_DASHBD round 148, workstream PUBWRITE (issuer 2.0.0_SA_COO~D2) -- DB-b-288, the DAILY SCHEDULE of the Cottonwood series publish, created DISABLED (the CTO's condition on the publish pair, msg 9021:
"2.0.0_SA_COO~D2 owes the daily schedule, in its own pair, before any page reads this prefix as served"). Three NEW resources are appended to the existing `reporting-publish-iso` root: a scheduler role, its policy
(lambda:InvokeFunction on the one function) and one schedule `cron(30 9 ? * MON-FRI *)` America/New_York, state DISABLED, input {"upload": true}. The function, its role and policy, the locals, the main file and the
source-map entry stay byte-identical. Enabling it is the CTO's separate word (a later one-line change, its own pair). LOCAL: Terraform files only; nothing is planned, applied or deployed.

  DB-b-288 (~232)   infra/aws/terraform/investor-reporting/reporting-publish-iso/{schedule.tf (new), iam.tf (append only)} + a facts record
                    DB156-1-AC1 (the HCL: the base files byte-identical, the three new resources, the schedule's fields, the statements),
                    DB156-1-AC2 (the REAL naming gate in plan mode on the three new names),
                    DB156-1-AC3 (the facts record equals the checker's recount)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~232"
REC_REL = D + AUTHOR + "/RD_PUBLISH_SCHEDULE_FACTS_R148.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-288.publish-daily-schedule-created-disabled.md"
ROOT_DIR = "infra/aws/terraform/investor-reporting/reporting-publish-iso/"
LANDING_REL = D + "0.9.0_WK_IRPT_DASHBD~195/RD_CW_LANDING_FACTS_R120.json"
GATE = ".tools/naming-apply-gate.py"
MODULE = "irpt_reporting_publish_iso"
CRON, ZONE = "cron(30 9 ? * MON-FRI *)", "America/New_York"
BASE_SIDS = ["ListGoldReturnsAndPlatinumReportingOnly", "ReadGoldReturnsOnly", "WriteThePlatinumReportingPrefixOnly", "ReadBackThePlatinumReportingPrefixOnly", "OwnLogStreamOnly", "ExecutionRoleAssumedByLambdaService"]
NEW_SIDS = ["SchedulerRoleAssumedBySchedulerService", "InvokeThePublishFunctionOnly"]
TYPE_COUNTS = {"aws_iam_role": 2, "aws_iam_role_policy": 2, "aws_scheduler_schedule": 1}
UNCHANGED_FILES = ("main.tf", "locals.tf", "lambda.tf")
NEW_ADDRESSES = ["aws_iam_role.%s_scheduler" % MODULE, "aws_iam_role_policy.%s_scheduler" % MODULE, "aws_scheduler_schedule.%s" % MODULE]
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def p149():
    spec = importlib.util.spec_from_file_location("p149_helper", str(HERE.parent / "r147" / "p149_pubroot.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["p149_helper"] = mod
    spec.loader.exec_module(mod)
    return mod


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    need(r.returncode == 0, "git %s: %s" % (" ".join(a[:2]), r.stderr.decode("utf-8", "replace").strip()[:200]))
    return r.stdout.decode("utf-8", "replace")


def base_commit(root):
    out = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_unchanged(base_files, files):
    for n in UNCHANGED_FILES:
        need(n in files and files[n] == base_files[n], "%s must stay byte-identical to the base" % n)
    need(files["iam.tf"].startswith(base_files["iam.tf"]) and len(files["iam.tf"]) > len(base_files["iam.tf"]), "iam.tf must keep the base text as an unchanged prefix and only APPEND the scheduler block")
    need("schedule.tf" in files, "schedule.tf (new) is missing")
    return True


def check_hcl(files, new_names, h):
    t = h.uncommented("\n".join(files[k] for k in sorted(files)))
    types = re.findall(r'^\s*resource\s+"([a-z0-9_]+)"\s+"[^"]+"', t, re.M)
    for ty, n in TYPE_COUNTS.items():
        need(types.count(ty) == n, "the root must declare %d resource(s) of type %s, found %d" % (n, ty, types.count(ty)))
    need(set(types) <= set(TYPE_COUNTS), "the root declares resources of other types: %s" % sorted(set(types) - set(TYPE_COUNTS)))
    mods = re.findall(r'module\s+"([^"]+)"\s*\{(.*?)\n\}', t, re.S)
    need(sum(1 for m in mods if "opal_name" in m[1]) == 6, "exactly six opal_name module calls are required (function, execution role and policy, scheduler role and policy, schedule)")
    need(sum(1 for m in mods if "yang-lambda" in m[1]) == 1, "exactly one yang-lambda module")
    sch = re.search(r'resource\s+"aws_scheduler_schedule"\s+"[^"]+"\s*\{(.*?)\n\}', t, re.S)
    need(sch is not None, "no aws_scheduler_schedule")
    body = sch.group(1)
    need(re.search(r'state\s*=\s*"DISABLED"', body), 'the schedule must be created with state = "DISABLED"')
    need(CRON in body and ZONE in body, "the schedule must carry %s in %s" % (CRON, ZONE))
    need(re.search(r'mode\s*=\s*"OFF"', body), 'flexible_time_window must be mode = "OFF"')
    need("function_arn" in body and MODULE in body, "the schedule's target must be the module's function_arn")
    need(re.search(r"input\s*=\s*jsonencode\(\s*\{\s*upload\s*=\s*true\s*\}\s*\)", body) or re.search(r'input\s*=\s*"\{\\"upload\\":\s*true\}"', body), 'the schedule input must be exactly {"upload": true}')
    st = h.statements(t)
    need(sorted(st) == sorted(BASE_SIDS + NEW_SIDS), "the statement ids must be exactly %s; read %s" % (sorted(BASE_SIDS + NEW_SIDS), sorted(st)))
    inv = [s for s, b in st.items() if "lambda:InvokeFunction" in h.actions_of(b)]
    need(inv == ["InvokeThePublishFunctionOnly"], "exactly one lambda:InvokeFunction statement, the scheduler's: %s" % inv)
    need("function_arn" in st["InvokeThePublishFunctionOnly"] and 'resources = ["*"]' not in st["InvokeThePublishFunctionOnly"], "the scheduler policy names the one function ARN only")
    need(h.actions_of(st["InvokeThePublishFunctionOnly"]) == ["lambda:InvokeFunction"], "the scheduler policy holds ONLY lambda:InvokeFunction")
    puts = [s for s, b in st.items() if "s3:PutObject" in h.actions_of(b)]
    need(puts == ["WriteThePlatinumReportingPrefixOnly"], "the one PutObject statement is unchanged")
    for nm in new_names:
        need(('"%s"' % nm) not in t, "the builder name %s is typed in the Terraform; take it from the opal_name module" % nm)
    return True


def check_gate_output(out):
    need("NAMING-PLAN:" in out and "REFUSE" not in out.split("NAMING-PLAN:")[1], "the naming gate refused: %s" % out.strip().splitlines()[-1:])
    need(out.count("NAMING CONFORMANT") == 3 and "NAMING REFUSE" not in out, "expected 3 CONFORMANT and no REFUSE lines, read %d" % out.count("NAMING CONFORMANT"))
    return True


def check_facts(rec, names):
    exp = {"root", "new_names", "new_resources", "expected_plan", "schedule", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["root"] == ROOT_DIR and rec["new_names"] == names, "root or new_names differ from the builder recount")
    need(rec["new_resources"] == ["%s.%s" % (a.split(".")[0], a.split(".")[1]) for a in NEW_ADDRESSES] or sorted(rec["new_resources"]) == sorted(NEW_ADDRESSES), "new_resources must be the three addresses %s" % NEW_ADDRESSES)
    need(rec["expected_plan"] == {"add": 3, "change": 0, "destroy": 0, "claim": "inferred"}, "expected_plan must be 3/0/0 claimed inferred")
    need(rec["schedule"] == {"cron": CRON, "zone": ZONE, "state": "DISABLED", "input": {"upload": True}}, "schedule block")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def module_names(root, files, h):
    sys.path.insert(0, str(root))
    from lib import opal_naming
    land = json.loads((Path(root) / LANDING_REL).read_text(encoding="utf-8"))
    scope = land["names"][0]["builder_args"]["scope"]
    mods = h.module_blocks(h.uncommented("\n".join(files[k] for k in sorted(files))))
    out = []
    for kind, qual in (("role", "scheduler"), ("policy", "scheduler"), ("daily", None)):
        hit = [v for v in mods.values() if v["kind"] == kind and v["qualifier"] == qual]
        need(len(hit) == 1 and hit[0]["system"] == "irpt" and hit[0]["function"] == "reporting-publish", "exactly one opal_name module for irpt / reporting-publish / %s / %s" % (kind, qual))
        out.append(opal_naming.name("irpt", scope, "reporting-publish", kind, **({"qualifier": qual} if qual else {})))
    return out


def run_gate(root, names):
    kinds = [("aws_iam_role", MODULE + "_scheduler"), ("aws_iam_role_policy", MODULE + "_scheduler"), ("aws_scheduler_schedule", MODULE)]
    changes = []
    for (t, n), nm in zip(kinds, names):
        after = {"name": nm}
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
    h = p149()
    d = root / ROOT_DIR
    need(d.is_dir(), "no %s" % ROOT_DIR)
    files = {p.name: p.read_text(encoding="utf-8") for p in sorted(d.glob("*.tf"))}
    base = base_commit(root)
    if cid == "DB156-1-AC1":
        base_files = {n: git(root, "show", "%s:%s%s" % (base, ROOT_DIR, n)) for n in UNCHANGED_FILES + ("iam.tf",)}
        check_unchanged(base_files, files)
        names = module_names(root, files, h)
        check_hcl(files, names, h)
        print("OK: root HCL: main, locals and lambda byte-identical to the base, iam.tf append-only; 3 new resources (scheduler role, its policy, one schedule created DISABLED at %s %s with input {upload: true}); six opal_name calls; the scheduler policy holds only lambda:InvokeFunction on the one function ARN; the execution statements unchanged; no typed builder name" % (CRON, ZONE))
        return True
    if cid == "DB156-1-AC2":
        names = module_names(root, files, h)
        check_gate_output(run_gate(root, names))
        print("OK: the real naming gate grades the three new names CONFORMANT (%s)" % ", ".join(names))
        return True
    if cid == "DB156-1-AC3":
        names = module_names(root, files, h)
        check_facts(json.loads((root / REC_REL).read_text(encoding="utf-8")), names)
        print("OK: the facts record equals the builder recount")
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    h = p149()

    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)

    def stmt(sid, actions, resources, extra=""):
        return 'statement {\n  sid = "%s"\n  effect = "Allow"\n  actions = [%s]\n  resources = [%s]\n%s}\n' % (sid, ", ".join('"%s"' % a for a in actions), ", ".join(resources), extra)
    sts = "".join([stmt("ListGoldReturnsAndPlatinumReportingOnly", ["s3:ListBucket"], ['"arn:x"']), stmt("ReadGoldReturnsOnly", ["s3:GetObject"], ['"arn:g"']),
                   stmt("WriteThePlatinumReportingPrefixOnly", ["s3:PutObject"], ['"arn:p"']), stmt("ReadBackThePlatinumReportingPrefixOnly", ["s3:GetObject"], ['"arn:p"']),
                   stmt("OwnLogStreamOnly", ["logs:PutLogEvents"], ['"arn:l"']), stmt("ExecutionRoleAssumedByLambdaService", ["sts:AssumeRole"], ['"arn:r"']),
                   stmt("SchedulerRoleAssumedBySchedulerService", ["sts:AssumeRole"], ['"arn:s"']), stmt("InvokeThePublishFunctionOnly", ["lambda:InvokeFunction"], ["module.%s.function_arn" % MODULE])])
    mods = "".join('module "m%d" {\n  source = "../../modules/opal_name"\n}\n' % i for i in range(6)) + 'module "%s" {\n  source = "../../modules/yang-lambda"\n}\n' % MODULE
    res = ('resource "aws_iam_role" "a" {}\nresource "aws_iam_role" "b" {}\nresource "aws_iam_role_policy" "c" {}\nresource "aws_iam_role_policy" "d" {}\n'
           'resource "aws_scheduler_schedule" "s" {\n  state = "DISABLED"\n  schedule_expression = "%s"\n  schedule_expression_timezone = "%s"\n  flexible_time_window {\n    mode = "OFF"\n  }\n'
           '  target {\n    arn = module.%s.function_arn\n    input = jsonencode({ upload = true })\n  }\n}\n' % (CRON, ZONE, MODULE))
    good = {"main.tf": mods + res + sts}
    assert check_hcl(good, ["irpt-cot-x"], h)
    base = good["main.tf"]
    arms = (("enabled", base.replace('state = "DISABLED"', 'state = "ENABLED"')), ("cron", base.replace(CRON, "cron(0 1 ? * * *)")), ("input", base.replace("jsonencode({ upload = true })", "jsonencode({ upload = false })")),
            ("no input", base.replace("    input = jsonencode({ upload = true })\n", "")), ("flex", base.replace('mode = "OFF"', 'mode = "FLEXIBLE"')), ("zone", base.replace(ZONE, "UTC")),
            ("target", base.replace("module.%s.function_arn" % MODULE, '"arn:aws:lambda:x"')), ("typed", base + '\nresource "x" "y" { name = "irpt-cot-x" }\n'),
            ("two invoke", base.replace('actions = ["logs:PutLogEvents"]', 'actions = ["lambda:InvokeFunction"]')), ("wildcard invoke", base.replace("module.%s.function_arn" % MODULE, '"*"', 1).replace('resources = ["*"]', 'resources = ["*"]')),
            ("extra action", base.replace('actions = ["lambda:InvokeFunction"]', 'actions = ["lambda:InvokeFunction", "lambda:GetFunction"]')), ("sid", base.replace("InvokeThePublishFunctionOnly", "Other")),
            ("five opal", base.replace('module "m5" {\n  source = "../../modules/opal_name"\n}\n', "")), ("extra resource", base + '\nresource "aws_sns_topic" "t" {}\n'))
    for label, txt in arms:
        red(lambda: check_hcl({"main.tf": txt}, ["irpt-cot-x"], h), label)
    bf = {"main.tf": "a", "locals.tf": "b", "lambda.tf": "c", "iam.tf": "base"}
    gf = {"main.tf": "a", "locals.tf": "b", "lambda.tf": "c", "iam.tf": "base + more", "schedule.tf": "s"}
    assert check_unchanged(bf, gf)
    for label, fn in (("main", lambda x: x.update(**{"main.tf": "z"})), ("lambda", lambda x: x.update(**{"lambda.tf": "z"})), ("iam prefix", lambda x: x.update(**{"iam.tf": "other"})), ("iam same", lambda x: x.update(**{"iam.tf": "base"})), ("no schedule", lambda x: x.pop("schedule.tf"))):
        x = dict(gf)
        fn(x)
        red(lambda: check_unchanged(bf, x), label)
    ok = "NAMING CONFORMANT x\n" * 3 + "NAMING-PLAN: PASS 3 graded\n"
    assert check_gate_output(ok)
    red(lambda: check_gate_output(ok.replace("PASS 3 graded", "REFUSE 3 graded")), "refuse")
    red(lambda: check_gate_output("NAMING CONFORMANT x\n" * 2 + "NAMING-PLAN: PASS 2 graded\n"), "two")
    rec = {"root": ROOT_DIR, "new_names": ["a", "b", "c"], "new_resources": list(NEW_ADDRESSES), "expected_plan": {"add": 3, "change": 0, "destroy": 0, "claim": "inferred"},
           "schedule": {"cron": CRON, "zone": ZONE, "state": "DISABLED", "input": {"upload": True}}, "words": "w" * 100}
    assert check_facts(rec, ["a", "b", "c"])
    for label, fn in (("names", lambda r: r.update(new_names=["x"])), ("resources", lambda r: r.update(new_resources=["r"])), ("plan", lambda r: r["expected_plan"].update(add=4)), ("state", lambda r: r["schedule"].update(state="ENABLED")),
                      ("input", lambda r: r["schedule"].update(input={"upload": False})), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, ["a", "b", "c"]), label)
    print("selftest: hcl (%d red arms), unchanged (5), gate (2) and facts (8) clauses behave" % len(arms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or build is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
