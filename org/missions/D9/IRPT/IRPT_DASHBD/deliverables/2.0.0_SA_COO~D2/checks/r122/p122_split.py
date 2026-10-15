"""IRPT_DASHBD round 122, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-247, the PER-DAY SELF-INVOKE SPLIT of the hop-1 `filled_report_values` stage (CTO analysis @e690365741
ruling 1, shape B): the scheduled fire runs the earlier stages and the OLDEST owed filled day, then asynchronously invokes ITSELF with {"day": <next owed day>} until none is owed;
an invocation carrying a "day" runs exactly that day (a day already landed is a no-op, so a duplicated chain link writes nothing) and then chains the next. The function's role gains
`lambda:InvokeFunction` on its OWN ARN only. LOCAL build: nothing is planned, applied or deployed.

  DB-b-247 (~201) handler.py gains owed_filled_days, run_filled_day, invoke_next_day, filled_day_event and filled_population, the scheduled `run` stops calling the shared
                  `filled_stage`, `lambda_handler` takes the day event; iam.tf (and locals.tf) gain the one invoke statement.
                                                                                           DB122-2-AC1 (handler and tests), AC2 (the Terraform), AC3 (the facts and the change)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the HCL and record clauses on synthetic arms
"""
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~201/RD_SPLIT_FACTS_R122.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-247.per-day-self-invoke-split-of-the-hop-1-filled-stage.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~201"
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
TESTS_DIR = "infra/aws/lambda/investor-reporting/reporting-gold/tests"
NEW_TEST_REL = TESTS_DIR + "/test_filled_per_day.py"
TF_DIR = "infra/aws/terraform/investor-reporting/reporting-gold/"
IAM_REL = TF_DIR + "iam.tf"
LOC_REL = TF_DIR + "locals.tf"
BASE_TESTS = 105
MIN_NEW_TESTS = 8
FUNCS = ("owed_filled_days", "run_filled_day", "invoke_next_day", "filled_day_event", "filled_population")
TEST_WORDS = (("landed", "noop"), ("none_owed", "chain_stops", "no_next"), ("event",), ("payload",))
PLAN_RESOURCES = ["aws_iam_role_policy.irpt_reporting_gold", "module.irpt_reporting_gold.aws_lambda_function.this"]
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "resources")
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


def own_numstat(root, commits, rel):
    add = dele = 0
    for c in commits:
        for ln in git(root, "show", "--numstat", "--format=", c, "--", rel).strip().splitlines():
            p = ln.split("\t")
            if len(p) >= 2 and p[0].isdigit() and p[1].isdigit():
                add += int(p[0])
                dele += int(p[1])
    return add, dele


def own_files(root, commits):
    names = set()
    for c in commits:
        names |= set(git(root, "show", "--name-only", "--format=", c).split())
    return names


def strip_comments(text):
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
        if s:
            out[s.group(1)] = blk
    return out


def actions_of(blk):
    m = re.search(r"actions\s*=\s*\[([^\]]*)\]", blk)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []


# ------------------------------------------------------------------------------------------------ the clauses (pure)
def check_handler_source(src):
    tree = ast.parse(src)
    funcs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    miss = [f for f in FUNCS if f not in funcs]
    need(not miss, "the handler lacks functions: %s" % miss)
    run = funcs.get("run")
    need(run is not None, "no run()")
    called = {c.func.id for c in ast.walk(run) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)}
    need("filled_stage" not in called, "run() must no longer call the shared filled_stage")
    need({"owed_filled_days", "run_filled_day"} <= called, "run() must call owed_filled_days and run_filled_day (the oldest owed day)")
    inv = ast.get_source_segment(src, funcs["invoke_next_day"]) or ""
    need('InvocationType="Event"' in inv.replace(" ", "") or "InvocationType='Event'" in inv.replace(" ", ""), "invoke_next_day must invoke with InvocationType Event")
    need("FunctionName" in inv and '"day"' in inv.replace("'", '"'), "invoke_next_day must pass FunctionName and a payload with the day key")
    lh = funcs.get("lambda_handler")
    need(lh is not None and "filled_day_event" in (ast.get_source_segment(src, lh) or ""), "lambda_handler must read the day event through filled_day_event")
    return True


def check_tests_names(names):
    need(len(names) >= MIN_NEW_TESTS, "the new test file needs at least %d tests, found %d" % (MIN_NEW_TESTS, len(names)))
    low = [n.lower() for n in names]
    for group in TEST_WORDS:
        need(any(any(w in n for w in group) for n in low), "no test name mentions any of %s" % (group,))
    return True


def check_hcl(iam, loc, base_iam):
    ic, lc = strip_comments(iam), strip_comments(loc)
    st, base_st = statements(ic), statements(strip_comments(base_iam))
    new = sorted(set(st) - set(base_st))
    inv = [s for s in new if "lambda:InvokeFunction" in actions_of(st[s])]
    need(len(inv) == 1, "iam.tf must gain exactly one statement with lambda:InvokeFunction, found %s" % inv)
    blk = st[inv[0]]
    need(actions_of(blk) == ["lambda:InvokeFunction"], "the invoke statement's actions must be exactly lambda:InvokeFunction")
    need("*" not in blk.replace("*/", ""), "the invoke statement holds a wildcard")
    need(len([s for s, b in st.items() if any(a.startswith("lambda:") for a in actions_of(b))]) == 1, "exactly one statement may carry lambda actions")
    need("module.irpt_reporting_gold_lambda_name" in (ic + lc), "the function ARN must be built from the builder-derived function name (module.irpt_reporting_gold_lambda_name), never typed")
    need(re.search(r"arn:aws:lambda:[^\"]*:function:", ic + lc) is not None, "no function ARN is built")
    return inv[0]


def check_facts(rec, sha_of, file_exists, has_line):
    exp = {"handler", "behavior", "iam", "expected_plan", "tests", "files_changed", "words", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(nes(rec["words"]) and rec["claim"] in CLAIMS, "words or claim")
    h = rec["handler"]
    need(isinstance(h, dict) and set(h) == {"file", "functions_added", "event_key", "invocation_type", "words"} and h["file"] == HANDLER_REL and set(FUNCS) <= set(h["functions_added"])
         and h["event_key"] == "day" and h["invocation_type"] == "Event" and nes(h["words"]), "handler block")
    for fn in FUNCS:
        need(has_line(HANDLER_REL, "def " + fn), "the handler has no function %s" % fn)
    b = rec["behavior"]
    keys = {"oldest_first", "noop_when_landed", "chain_stops_when_none_owed", "scheduled_runs_earlier_stages", "day_event_skips_earlier_stages", "words"}
    need(isinstance(b, dict) and set(b) == keys and all(b[k] is True for k in keys - {"words"}) and nes(b["words"]), "behavior block (all five must be true, with words)")
    i = rec["iam"]
    need(isinstance(i, dict) and set(i) == {"file", "statement_id", "action", "resource_form", "words"} and i["file"] == IAM_REL and i["action"] == "lambda:InvokeFunction"
         and nes(i["statement_id"]) and nes(i["resource_form"]) and nes(i["words"]), "iam block")
    ep = rec["expected_plan"]
    need(isinstance(ep, dict) and set(ep) == {"to_add", "to_change", "to_destroy", "resources", "words"} and ep["to_add"] == 0 and ep["to_change"] == 2 and ep["to_destroy"] == 0
         and sorted(ep["resources"]) == PLAN_RESOURCES and nes(ep["words"]), "expected_plan must stay 0 add / 2 change / 0 destroy on the two named resources")
    t = rec["tests"]
    need(isinstance(t, dict) and set(t) == {"file", "new_tests", "dir_total"} and t["file"] == NEW_TEST_REL and is_int(t["new_tests"]) and t["new_tests"] >= MIN_NEW_TESTS
         and is_int(t["dir_total"]) and t["dir_total"] >= BASE_TESTS + MIN_NEW_TESTS, "tests block")
    fc = rec["files_changed"]
    need(isinstance(fc, list) and {f.get("file") for f in fc} >= {HANDLER_REL, NEW_TEST_REL, IAM_REL}, "files_changed must name the handler, the test file and iam.tf")
    for f in fc:
        need(set(f) == {"file", "sha256", "kind"} and nes(f["kind"]) and file_exists(f["file"]) and HEX64.match(str(f["sha256"])) and sha_of(f["file"]) == f["sha256"],
             "files_changed entry %s: hash or form" % f.get("file"))
        need(f["file"] in (HANDLER_REL, NEW_TEST_REL, IAM_REL, LOC_REL), "a changed file outside the grant: %s" % f["file"])
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def run(root, cid):
    root = Path(root)
    if cid == "DB122-2-AC1":
        src = (root / HANDLER_REL).read_text(encoding="utf-8")
        check_handler_source(src)
        tp = root / NEW_TEST_REL
        need(tp.is_file(), "no new test file")
        names = re.findall(r"^def (test_\w+)", tp.read_text(encoding="utf-8"), re.M)
        check_tests_names(names)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(root / TESTS_DIR)], cwd=str(root), capture_output=True, text=True, timeout=250)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= BASE_TESTS + MIN_NEW_TESTS and "failed" not in r.stdout,
             "pytest on the handler's tests: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: the handler has the five functions, run() runs the oldest owed day and no longer calls filled_stage, the invoke is async with a day payload; %s tests pass (%d earlier, %d new)" %
              (m.group(1), BASE_TESTS, len(names)))
        return True
    if cid == "DB122-2-AC2":
        cs = own_commits(root)
        base_iam = git(root, "show", "%s~1:%s" % (cs[0], IAM_REL))
        need(base_iam.strip(), "base iam.tf unreadable")
        sid = check_hcl((root / IAM_REL).read_text(encoding="utf-8"), (root / LOC_REL).read_text(encoding="utf-8"), base_iam)
        ga, la = own_numstat(root, cs, IAM_REL)
        need(ga >= 8 and la <= 2, "iam.tf gains %d loses %d (needs gain >= 8, lose <= 2)" % (ga, la))
        other = sorted(f for f in own_files(root, cs) if f.startswith("infra/aws/terraform/") and f not in (IAM_REL, LOC_REL))
        need(not other, "this worker's commits changed other Terraform files: %s" % other)
        print("OK: iam.tf gains the one lambda:InvokeFunction statement %s (iam.tf +%d/-%d), the ARN is built from the builder-derived function name, no wildcard, no other Terraform file" % (sid, ga, la))
        return True
    if cid == "DB122-2-AC3":
        rec = load(root, REC_REL)
        check_facts(rec, lambda rel: hashlib.sha256((root / rel).read_bytes()).hexdigest(), lambda rel: (root / rel).is_file(),
                    lambda rel, token: token in (root / rel).read_text(encoding="utf-8"))
        cs = own_commits(root)
        add, dele = own_numstat(root, cs, HANDLER_REL)
        need(add >= 60 and dele <= 10, "the handler change must be additive in the worker's own commits: %d added, %d deleted (needs >= 60 and <= 10)" % (add, dele))
        stray = sorted(f for f in own_files(root, cs) if f.startswith(("infra/", "data/", "lib/", "org/standards/")) and f not in (HANDLER_REL, NEW_TEST_REL, IAM_REL, LOC_REL))
        need(not stray, "this worker's commits changed files outside the grant: %s" % stray[:3])
        print("OK: facts record valid, files hashed; the handler gains %d lines and loses %d in the worker's own commits; nothing else under infra/, data/, lib/ or org/standards/" % (add, dele))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    src = ('def owed_filled_days(a):\n    return []\n\ndef run_filled_day(a):\n    return {}\n\ndef filled_day_event(e):\n    return None\n\ndef filled_population(s):\n    return []\n\n'
           'def invoke_next_day(c, arn, day):\n    return c.invoke(FunctionName=arn, InvocationType="Event", Payload=json.dumps({"day": day}))\n\n'
           'def run(s3):\n    owed_filled_days(s3)\n    run_filled_day(s3)\n\ndef lambda_handler(e, c=None):\n    return filled_day_event(e)\n')
    assert check_handler_source(src)

    def bad_src(s):
        try:
            check_handler_source(s)
            return False
        except Fail:
            return True
    assert bad_src(src.replace("run_filled_day(s3)", "filled_stage(s3)"))
    assert bad_src(src.replace('InvocationType="Event"', 'InvocationType="RequestResponse"'))
    assert bad_src(src.replace("def filled_population", "def other"))
    assert bad_src(src.replace("return filled_day_event(e)", "return 1"))
    assert check_tests_names(["test_landed_day_is_noop", "test_chain_stops_when_none_owed", "test_event_day", "test_payload_has_day", "test_a", "test_b", "test_c", "test_d"])
    try:
        check_tests_names(["test_a"] * 8)
        raise AssertionError("names arm")
    except Fail:
        pass
    base_iam = 'data "x" "y" {\n statement {\n sid = "A"\n actions = ["s3:GetObject"]\n resources = local.r\n }\n}\n'
    iam = base_iam + 'statement {\n sid = "InvokeOwn"\n actions = ["lambda:InvokeFunction"]\n resources = ["arn:aws:lambda:us-east-1:${data.aws_caller_identity.current.account_id}:function:${module.irpt_reporting_gold_lambda_name.name}"]\n}\n'
    assert check_hcl(iam, "locals {}", base_iam) == "InvokeOwn"
    for i2 in (iam.replace("lambda:InvokeFunction", "lambda:*"), iam.replace("module.irpt_reporting_gold_lambda_name.name", "typed-name"), base_iam,
               iam.replace('"lambda:InvokeFunction"]', '"lambda:InvokeFunction", "lambda:GetFunction"]')):
        try:
            check_hcl(i2, "locals {}", base_iam)
            raise AssertionError("a red HCL arm passed")
        except Fail:
            pass
    fc = [{"file": f, "sha256": "ab" * 32, "kind": "k"} for f in (HANDLER_REL, NEW_TEST_REL, IAM_REL)]
    good = {"handler": {"file": HANDLER_REL, "functions_added": list(FUNCS), "event_key": "day", "invocation_type": "Event", "words": "w"},
            "behavior": {"oldest_first": True, "noop_when_landed": True, "chain_stops_when_none_owed": True, "scheduled_runs_earlier_stages": True, "day_event_skips_earlier_stages": True, "words": "w"},
            "iam": {"file": IAM_REL, "statement_id": "InvokeOwn", "action": "lambda:InvokeFunction", "resource_form": "own ARN", "words": "w"},
            "expected_plan": {"to_add": 0, "to_change": 2, "to_destroy": 0, "resources": PLAN_RESOURCES, "words": "w"}, "tests": {"file": NEW_TEST_REL, "new_tests": 9, "dir_total": 114},
            "files_changed": fc, "words": "w", "claim": "inferred", "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(r, sha="ab" * 32):
        try:
            return check_facts(r, lambda rel: sha, lambda rel: True, lambda rel, t: True)
        except Fail:
            return False
    assert grade(copy.deepcopy(good)) is True
    for f in (lambda r: r["behavior"].update(noop_when_landed=False), lambda r: r["expected_plan"].update(to_change=3), lambda r: r["handler"].update(invocation_type="RequestResponse"),
              lambda r: r["tests"].update(new_tests=2), lambda r: r.update(deployed=True), lambda r: r["files_changed"].pop(), lambda r: r["iam"].update(action="lambda:*"),
              lambda r: r.update(words="id 1234567890")):
        r = copy.deepcopy(good)
        f(r)
        assert grade(r) is False
    assert grade(copy.deepcopy(good), sha="cd" * 32) is False
    print("selftest: the AST arms, the test-name arms, the HCL arms and the facts arms behave")


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
