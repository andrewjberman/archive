"""IRPT_DASHBD round 123, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-252, the COTTONWOOD LANDING TERRAFORM ROOT (CTO analysis @1ffd4f5afb ruling 3): the Terraform files of the
function `irpt-cot-account-return-daily-lambda` (round 122's handler and source-map entry), written as a NEW root that changes nothing existing: one Lambda (module yang-lambda: the
function and its log group), one execution role and its policy, one scheduler role and its policy, one schedule created DISABLED. Names from the builder module, never typed. LOCAL:
nothing is planned, applied or deployed (the box has no terraform); the applier's plan must read 7 add / 0 change / 0 destroy.

  DB-b-252 (~206) infra/aws/terraform/investor-reporting/account-return-daily/*.tf (a new directory), and a facts record.
                                                                                           DB123-3-AC1 (the HCL), AC2 (additive, a new root only), AC3 (the facts)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the HCL and record clauses on synthetic arms
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~206/RD_COT_ROOT_FACTS_R123.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-252.cottonwood-landing-terraform-root-function-roles-disabled-schedule.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~206"
ROOT_DIR = "infra/aws/terraform/investor-reporting/account-return-daily/"
STATE_KEY = "investor-reporting/account-return-daily/tfstate"
LANDING_REL = D + "0.9.0_WK_IRPT_DASHBD~195/RD_CW_LANDING_FACTS_R120.json"
CRON = "cron(15 8 ? * MON-FRI *)"
ZONE = "America/New_York"
HANDLER = "handler.lambda_handler"
ENTRY_KEY = "irpt-cot-account-return-daily-lambda"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
ALLOWED_ACTIONS = {"s3:GetObject", "s3:ListBucket", "s3:PutObject", "logs:CreateLogStream", "logs:PutLogEvents", "sts:AssumeRole", "lambda:InvokeFunction"}
TYPE_COUNTS = {"aws_iam_role": 2, "aws_iam_role_policy": 2, "aws_scheduler_schedule": 1}
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "resources", "name", "arn", "arns")
HEX64 = re.compile(r"[0-9a-f]{64}$")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def git(root, *a):
    return subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True).stdout


def own_commits(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(base, "the order's first commit is not in this history")
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base[-1] + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def own_files(root, commits):
    names = set()
    for c in commits:
        names |= set(git(root, "show", "--name-only", "--format=", c).split())
    return names


def uncommented(text):
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))


def statements(text):
    out = {}
    for m in re.finditer(r"statement\s*\{", text):
        depth, i = 1, m.end()
        while depth and i < len(text):
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        blk = text[m.start():i]
        s = re.search(r'sid\s*=\s*"([^"]+)"', blk)
        out[s.group(1) if s else "statement%d" % len(out)] = blk
    return out


def actions_of(blk):
    m = re.search(r"actions\s*=\s*\[([^\]]*)\]", blk)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []


# ------------------------------------------------------------------------------------------------ the HCL clauses (pure)
def check_hcl(files, built_names, tables, artifact_key):
    """files: {filename: text}; built_names: the builder's five names; tables: the two silver tables; artifact_key: the source-map entry's key."""
    need(files, "the root holds no .tf file")
    t = uncommented("\n".join(files[k] for k in sorted(files)))
    types = re.findall(r'^\s*resource\s+"([a-z0-9_]+)"\s+"[^"]+"', t, re.M)
    for ty, n in TYPE_COUNTS.items():
        need(types.count(ty) == n, "the root must declare %d resource(s) of type %s, found %d" % (n, ty, types.count(ty)))
    need(set(types) <= set(TYPE_COUNTS), "the root declares resources of other types: %s" % sorted(set(types) - set(TYPE_COUNTS)))
    mods = re.findall(r'module\s+"([^"]+)"\s*\{(.*?)\n\}', t, re.S)
    lam = [m for m in mods if "yang-lambda" in m[1]]
    need(len(lam) == 1, "exactly one module of source yang-lambda is required, found %d" % len(lam))
    need(sum(1 for m in mods if "opal_name" in m[1]) >= 5, "at least five opal_name module calls are required (function, execution role and policy, scheduler role, schedule)")
    body = lam[0][1]
    need(HANDLER in body and re.search(r"\btimeout\s*=\s*\d+", body) and re.search(r"\bmemory_size\s*=\s*\d+", body), "the lambda module call needs handler %s, a timeout and a memory_size" % HANDLER)
    need(re.search(r"reserved_concurrent_executions\s*=\s*1\b", body), "the function must be capped at reserved_concurrent_executions = 1")
    need("environment_variables" not in body or re.search(r"environment_variables\s*=\s*\{\s*\}", body), "no environment variable may carry a firm token: leave environment_variables out")
    need(artifact_key in t or "lambda-source-map.json" in t, "the artifact key must be the source-map entry's (%s) or be read from the source map" % artifact_key)
    sch = re.search(r'resource\s+"aws_scheduler_schedule"\s+"[^"]+"\s*\{(.*?)\n\}', t, re.S)
    need(sch is not None, "no schedule resource")
    sb = sch.group(1)
    need(re.search(r'state\s*=\s*"DISABLED"', sb), "the schedule must be created with state = \"DISABLED\"")
    need(CRON in sb and ZONE in sb, "the schedule must carry %s in %s" % (CRON, ZONE))
    st = statements(t)
    need(len(st) >= 4, "at least four policy statements are required")
    puts = [s for s, b in st.items() if "s3:PutObject" in actions_of(b)]
    inv = [s for s, b in st.items() if "lambda:InvokeFunction" in actions_of(b)]
    need(len(puts) == 1 and "account_return_daily" in st[puts[0]] + t[t.find(puts[0]):t.find(puts[0]) + 1], "exactly one PutObject statement is allowed, on the account_return_daily prefix")
    need(len(inv) == 1, "exactly one lambda:InvokeFunction statement is allowed (the scheduler's)")
    need(len([x for x, b in st.items() if "s3:ListBucket" in actions_of(b)]) >= 2, "at least two s3:ListBucket statements are required: the silver tables and the gold account_return_daily prefix (the handler lists it for the newest landed day)")
    for s, b in st.items():
        acts = actions_of(b)
        need(acts and all("*" not in a for a in acts) and set(acts) <= ALLOWED_ACTIONS, "statement %s: explicit allowed actions only, found %s" % (s, acts))
        need('resources = ["*"]' not in b and '"arn:aws:s3:::*' not in b, "statement %s grants all resources" % s)
    need(all(tb in t for tb in tables), "the read statements must name both silver tables %s" % list(tables))
    for nm in built_names:
        need(('"%s"' % nm) not in t, "the builder name %s is typed in the Terraform; take it from the opal_name module" % nm)
    need(re.search(r'key\s*=\s*"%s"' % re.escape(STATE_KEY), t), "the backend state key must be %s" % STATE_KEY)
    return {"resources": types, "module": lam[0][0], "statements": sorted(st)}


# ------------------------------------------------------------------------------------------------ the recount and the record (pure)
def builder_names(root, args_list):
    sys.path.insert(0, str(root))
    from lib import opal_naming
    out = []
    for a in args_list:
        kw = {"qualifier": a["qualifier"]} if a.get("qualifier") else {}
        out.append(opal_naming.name(a["system"], a["scope"], a["function"], a["kind"], **kw))
    return out


def check_facts(rec, recount_names, sha_of, file_exists, hcl):
    exp = {"root", "files_changed", "names", "resources", "expected_plan", "schedule", "iam", "artifact", "validated", "derivations", "words", "claim", "files_in_repo",
           "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["root"] == ROOT_DIR and nes(rec["words"]) and rec["claim"] in CLAIMS, "root, words or claim")
    fc = rec["files_changed"]
    need(isinstance(fc, list) and len(fc) >= 3, "files_changed must list the root's .tf files")
    for f in fc:
        need(set(f) == {"file", "sha256", "kind"} and nes(f["kind"]) and f["file"].startswith(ROOT_DIR) and f["file"].endswith(".tf") and file_exists(f["file"]) and HEX64.match(str(f["sha256"]))
             and sha_of(f["file"]) == f["sha256"], "files_changed entry %s: path, hash or form" % f.get("file"))
    nm = rec["names"]
    need(isinstance(nm, list) and len(nm) == 5 and all(isinstance(x, dict) and set(x) == {"purpose", "builder_args", "name"} for x in nm), "names: five entries {purpose, builder_args, name}")
    need([x["name"] for x in nm] == recount_names, "names differ from the builder's output: record %s, recount %s" % ([x["name"] for x in nm], recount_names))
    rs = rec["resources"]
    need(isinstance(rs, list) and len(rs) == 7 and all(nes(x) for x in rs), "resources: the seven addresses the plan will add")
    need(sum(1 for x in rs if x.startswith("aws_iam_role.")) == 2 and sum(1 for x in rs if x.startswith("aws_iam_role_policy.")) == 2 and sum(1 for x in rs if x.startswith("aws_scheduler_schedule.")) == 1
         and any(x.startswith("module.%s.aws_lambda_function" % hcl["module"]) for x in rs) and any(x.startswith("module.%s.aws_cloudwatch_log_group" % hcl["module"]) for x in rs), "resources do not match the HCL")
    ep = rec["expected_plan"]
    need(isinstance(ep, dict) and set(ep) == {"to_add", "to_change", "to_destroy", "words"} and ep["to_add"] == 7 and ep["to_change"] == 0 and ep["to_destroy"] == 0 and nes(ep["words"]), "expected_plan must be 7 add / 0 change / 0 destroy")
    sc = rec["schedule"]
    need(isinstance(sc, dict) and set(sc) == {"cron", "zone", "state", "words"} and sc["cron"] == CRON and sc["zone"] == ZONE and sc["state"] == "DISABLED" and nes(sc["words"]), "schedule block")
    ia = rec["iam"]
    need(isinstance(ia, dict) and set(ia) == {"statement_ids", "no_wildcard", "words"} and sorted(ia["statement_ids"]) == hcl["statements"] and ia["no_wildcard"] is True and nes(ia["words"]), "iam block")
    ar = rec["artifact"]
    need(isinstance(ar, dict) and set(ar) == {"entry", "key", "words"} and ar["entry"] == ENTRY_KEY and nes(ar["key"]) and nes(ar["words"]), "artifact block")
    v = rec["validated"]
    need(isinstance(v, dict) and set(v) == {"ran", "words"} and isinstance(v["ran"], bool) and nes(v["words"]), "validated block")
    dv = rec["derivations"]
    need(isinstance(dv, dict) and set(dv) == {"scope", "buckets", "prefixes"} and all(nes(dv[k]) for k in dv), "derivations block (one sentence each: where the scope, the buckets and the prefixes come from)")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def read_root(root):
    d = Path(root) / ROOT_DIR
    need(d.is_dir(), "no %s" % ROOT_DIR)
    files = {p.name: p.read_text(encoding="utf-8") for p in sorted(d.glob("*.tf"))}
    return files


def run(root, cid):
    root = Path(root)
    landing = load(root, LANDING_REL)
    args = [x["builder_args"] for x in landing["names"]]
    names = builder_names(root, args)
    sm = load(root, SOURCE_MAP_REL)
    artifact_key = sm["functions"][ENTRY_KEY]["artifact_s3_key"]
    tables = ("fact_allocations", "fact_transactions")
    if cid == "DB123-3-AC1":
        h = check_hcl(read_root(root), names, tables, artifact_key)
        print("OK: root HCL: %d resource blocks and one yang-lambda module (%s), five opal_name calls, a DISABLED %s schedule, explicit IAM actions (%s), no builder name typed" %
              (len(h["resources"]), h["module"], CRON, ", ".join(h["statements"])))
        return True
    if cid == "DB123-3-AC2":
        cs = own_commits(root)
        stray = sorted(f for f in own_files(root, cs) if f.startswith(("infra/", "data/", "lib/", "org/standards/")) and not f.startswith(ROOT_DIR))
        need(not stray, "this worker's commits changed files outside the new root: %s" % stray[:3])
        existing = [f for f in git(root, "ls-tree", "-r", "--name-only", "%s~1" % cs[0], "--", ROOT_DIR).split()]
        need(not existing, "the root already existed before this worker: %s" % existing[:3])
        n = sum(1 for f in own_files(root, cs) if f.startswith(ROOT_DIR))
        need(n >= 3, "the worker's commits touch only %d files of the root" % n)
        print("OK: the worker's own commits touch %d files, all inside the NEW root %s; nothing else under infra/, data/, lib/ or org/standards/" % (n, ROOT_DIR))
        return True
    if cid == "DB123-3-AC3":
        rec = load(root, REC_REL)
        h = check_hcl(read_root(root), names, tables, artifact_key)
        check_facts(rec, names, lambda rel: hashlib.sha256((root / rel).read_bytes()).hexdigest(), lambda rel: (root / rel).is_file(), h)
        print("OK: root facts: five names equal the builder's, seven resources, plan 7/0/0, DISABLED schedule, statements and files hashed")
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    names = ["irpt-cot-account-return-daily-lambda", "irpt-cot-account-return-daily-execution-role", "irpt-cot-account-return-daily-execution-policy",
             "irpt-cot-account-return-daily-scheduler-role", "irpt-cot-account-return-daily-daily"]
    mod = 'module "n%d" {\n  source = "../../modules/opal_name"\n}\n'
    tf = ("terraform {\n  backend \"s3\" {\n    key = \"%s\"\n  }\n}\n" % STATE_KEY + "".join(mod % i for i in range(5)) +
          'module "fn" {\n  source = "../../modules/yang-lambda"\n  handler = "handler.lambda_handler"\n  timeout = 300\n  memory_size = 1024\n  reserved_concurrent_executions = 1\n}\n'
          'locals {\n  sm = jsondecode(file("${path.module}/lambda-source-map.json"))\n}\n'
          'resource "aws_iam_role" "a" {\n}\nresource "aws_iam_role" "b" {\n}\nresource "aws_iam_role_policy" "a" {\n}\nresource "aws_iam_role_policy" "b" {\n}\n'
          'resource "aws_scheduler_schedule" "s" {\n  state = "DISABLED"\n  schedule_expression = "%s"\n  schedule_expression_timezone = "%s"\n}\n' % (CRON, ZONE) +
          'data "aws_iam_policy_document" "p" {\n'
          '  statement {\n    sid = "R"\n    actions = ["s3:GetObject"]\n    resources = ["arn:aws:s3:::b/x/fact_allocations/*", "arn:aws:s3:::b/x/fact_transactions/*"]\n  }\n'
          '  statement {\n    sid = "L"\n    actions = ["s3:ListBucket"]\n    resources = ["arn:aws:s3:::b"]\n  }\n'
          '  statement {\n    sid = "L2"\n    actions = ["s3:ListBucket"]\n    resources = ["arn:aws:s3:::g"]\n  }\n'
          '  statement {\n    sid = "W"\n    actions = ["s3:PutObject"]\n    resources = ["arn:aws:s3:::g/irpt/f/gold/account_return_daily/*"]\n  }\n'
          '  statement {\n    sid = "G"\n    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]\n    resources = ["arn:aws:logs:x"]\n  }\n'
          '  statement {\n    sid = "I"\n    actions = ["lambda:InvokeFunction"]\n    resources = ["arn:aws:lambda:x"]\n  }\n}\n')
    h = check_hcl({"main.tf": tf}, names, ("fact_allocations", "fact_transactions"), "lambda-source-map.json")
    assert h["module"] == "fn" and len(h["statements"]) == 6

    def bad(mut):
        try:
            check_hcl({"main.tf": mut}, names, ("fact_allocations", "fact_transactions"), "lambda-source-map.json")
            return False
        except Fail:
            return True
    assert bad(tf.replace('state = "DISABLED"', 'state = "ENABLED"'))
    assert bad(tf.replace('"s3:GetObject"', '"s3:*"'))
    assert bad(tf.replace('reserved_concurrent_executions = 1', 'reserved_concurrent_executions = 5'))
    assert bad(tf + 'resource "aws_lambda_permission" "x" {\n}\n')
    assert bad(tf + 'locals {\n  n = "%s"\n}\n' % names[0])
    assert bad(tf.replace('"s3:ListBucket"', '"s3:PutObject"'))
    assert bad(tf.replace(CRON, "cron(0 0 * * ? *)"))
    assert bad(tf.replace("fact_transactions", "fact_other"))
    assert bad(tf.replace('"../../modules/opal_name"', '"../../modules/other"'))
    assert bad(tf.replace(STATE_KEY, "investor-reporting/other/tfstate"))
    fc = [{"file": ROOT_DIR + n, "sha256": "ab" * 32, "kind": "terraform"} for n in ("main.tf", "lambda.tf", "iam.tf")]
    good = {"root": ROOT_DIR, "files_changed": fc, "names": [{"purpose": "p", "builder_args": {}, "name": n} for n in names],
            "resources": ["aws_iam_role.a", "aws_iam_role.b", "aws_iam_role_policy.a", "aws_iam_role_policy.b", "aws_scheduler_schedule.s", "module.fn.aws_lambda_function.this", "module.fn.aws_cloudwatch_log_group.lambda"],
            "expected_plan": {"to_add": 7, "to_change": 0, "to_destroy": 0, "words": "w"}, "schedule": {"cron": CRON, "zone": ZONE, "state": "DISABLED", "words": "w"},
            "iam": {"statement_ids": sorted(h["statements"]), "no_wildcard": True, "words": "w"}, "artifact": {"entry": ENTRY_KEY, "key": "k", "words": "w"},
            "validated": {"ran": False, "words": "w"}, "derivations": {"scope": "s", "buckets": "b", "prefixes": "p"}, "words": "w", "claim": "inferred", "files_in_repo": False,
            "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(r, nm=names):
        try:
            return check_facts(r, nm, lambda rel: "ab" * 32, lambda rel: True, h)
        except Fail:
            return False
    assert grade(copy.deepcopy(good)) is True
    for f in (lambda r: r["expected_plan"].update(to_add=6), lambda r: r["schedule"].update(state="ENABLED"), lambda r: r["resources"].pop(), lambda r: r["names"][0].update(name="x"),
              lambda r: r.update(deployed=True), lambda r: r["iam"].update(no_wildcard=False), lambda r: r["files_changed"][0].update(file="infra/other/x.tf"), lambda r: r.update(words="id 1234567890")):
        r = copy.deepcopy(good)
        f(r)
        assert grade(r) is False
    print("selftest: eleven HCL arms and nine facts arms behave")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
