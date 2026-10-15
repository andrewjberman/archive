"""IRPT_DASHBD round 133, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-265, the COTTONWOOD REPORT-BUILD TERRAFORM ROOT and its source-map entry (CTO decision msg 8348; the handler is
round 131's DB-b-263). A NEW root `infra/aws/terraform/investor-reporting/reporting-gold-iso/` that declares, in its own state, the firm-isolated function that runs the handler: one yang-lambda
module (handler.lambda_handler, python3.12, timeout 900, memory 1024 from the issuer's local measurement, NO reserved concurrency because the chain invokes itself, the EXISTING native pyarrow
layer through a read-only data source), an execution role and policy that read ONLY the two Cottonwood gold inputs, the one served model-series object and read back / write ONLY Cottonwood's
filled_report_values prefix and invoke only the function itself, a scheduler role and policy, and ONE schedule created DISABLED. Every name from the builder, every firm-scoped value derived, never
typed. LOCAL: nothing is planned, applied, uploaded or deployed (the box has no terraform); the applier's plan must read 7 add / 0 change / 0 destroy.

  DB-b-265 (~216)   the new root's five .tf files, the source-map entry `irpt-cot-reporting-gold-lambda` (pinned), a facts record
                    DB133-1-AC1 (the HCL: resources, statements, derivations, no typed name, the layer, the schedule),
                    DB133-1-AC2 (the REAL naming gate in plan mode on the six named resources; the import check against the layer; the build-only package equals its sources),
                    DB133-1-AC3 (the source-map entry: 18 members pinned and hashed, tf fields, nothing else moved; the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~216/RD_COT_REPORT_ROOT_FACTS_R133.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-265.cottonwood-report-build-terraform-root-and-source-map-entry.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~216"
ROOT_DIR = "infra/aws/terraform/investor-reporting/reporting-gold-iso/"
STATE_KEY = "investor-reporting/reporting-gold-iso/tfstate"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
ENTRY_KEY = "irpt-cot-reporting-gold-lambda"
SOURCE_DIR = "infra/aws/lambda/investor-reporting/reporting-gold-cot"
LANDING_REL = D + "0.9.0_WK_IRPT_DASHBD~195/RD_CW_LANDING_FACTS_R120.json"
GATE = ".tools/naming-apply-gate.py"
LAYER_NAME, DATA_NAME = "irpt-performance-native-layer", "irpt_performance_native"
CRON, ZONE = "cron(15 9 ? * MON-FRI *)", "America/New_York"
HANDLER = "handler.lambda_handler"
# the bundle (shared with the handler's checker): the handler is the bundle root, the rest are staged_from members at their repo paths
CLOSURE = ["data/assets/scripts/gold/irpt_reporting/filled_report_values.py", "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_report_reader.py",
           "data/assets/scripts/gold/irpt_reporting/adapters/model_series_windows.py", "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json", "lib/opal_naming.py", "lib/trading_calendar.py",
           "org/standards/NAMING_SCHEMA.json"] + ["infra/logic/registry/%s.json" % n for n in (
               "systems", "scopes", "tiers", "exemptions", "remediations", "resources", "reporting_policies", "legacy_addresses", "feeds", "platinum_destinations", "firm_pages")]
EXEC_SIDS = ["ListCottonwoodGoldInputsAndFilledOnly", "ReadCottonwoodGoldInputsOnly", "WriteTheFilledReportValuesPrefixOnly", "ReadBackTheFilledPrefixOnly",
             "ReadTheServedModelSeriesObjectOnly", "InvokeOwnFunctionOnly", "OwnLogStreamOnly"]
OTHER_SIDS = ["ExecutionRoleAssumedByLambdaService", "SchedulerRoleAssumedBySchedulerService", "InvokeTheReportFunctionOnly"]
ALLOWED_ACTIONS = {"s3:GetObject", "s3:ListBucket", "s3:PutObject", "logs:CreateLogStream", "logs:PutLogEvents", "sts:AssumeRole", "lambda:InvokeFunction"}
TYPE_COUNTS = {"aws_iam_role": 2, "aws_iam_role_policy": 2, "aws_scheduler_schedule": 1}
SERVED_KEY = "json/benchmarks/model_portfolio_timeseries.json"
EDITABLE_ENTRY_KEYS = {"staged_from", "tf_file", "tf_resource", "iam_role", "_tf_note", "_staged_from_note"}
HEX40, HEX64 = re.compile(r"[0-9a-f]{40}$"), re.compile(r"[0-9a-f]{64}$")
LONG_DIGITS = re.compile(r"\d{8,}")
RUNTIME_PROVIDED = {"boto3", "botocore"}


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout.decode("utf-8", "replace"), r.returncode


def sha(b):
    return hashlib.sha256(b).hexdigest()


def base_commit(root):
    out, _ = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(out.split(), "the order's first commit is not in this history")
    return out.split()[-1]


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
def check_hcl(files, typed_names):
    need(files, "the root holds no .tf file")
    t = uncommented("\n".join(files[k] for k in sorted(files)))
    types = re.findall(r'^\s*resource\s+"([a-z0-9_]+)"\s+"[^"]+"', t, re.M)
    for ty, n in TYPE_COUNTS.items():
        need(types.count(ty) == n, "the root must declare %d resource(s) of type %s, found %d" % (n, ty, types.count(ty)))
    need(set(types) <= set(TYPE_COUNTS), "the root declares resources of other types: %s" % sorted(set(types) - set(TYPE_COUNTS)))
    mods = re.findall(r'module\s+"([^"]+)"\s*\{(.*?)\n\}', t, re.S)
    lam = [m for m in mods if "yang-lambda" in m[1]]
    need(len(lam) == 1, "exactly one module of source yang-lambda is required, found %d" % len(lam))
    need(sum(1 for m in mods if "opal_name" in m[1]) == 6, "exactly six opal_name module calls are required (function, execution role and policy, scheduler role and policy, schedule)")
    body = lam[0][1]
    need(HANDLER in body and re.search(r"\btimeout\s*=\s*900\b", body) and re.search(r"\bmemory_size\s*=\s*1024\b", body), "the lambda module call needs handler %s, timeout 900 and memory_size 1024" % HANDLER)
    need("reserved_concurrent_executions" not in body, "no reserved concurrency: the chain invokes the function while it still runs")
    need(re.search(r"layers\s*=\s*\[\s*data\.aws_lambda_layer_version\.%s\.arn\s*\]" % DATA_NAME, body), "the module call must attach the native layer through the read-only data source")
    need(re.search(r'data\s+"aws_lambda_layer_version"\s+"%s"\s*\{\s*layer_name\s*=\s*"%s"\s*\}' % (DATA_NAME, re.escape(LAYER_NAME)), t), "the read-only layer data source is missing")
    need("environment_variables" not in body or re.search(r"environment_variables\s*=\s*\{\s*\}", body), "no environment variable may carry a firm token")
    need("lambda-source-map.json" in t and ENTRY_KEY not in t.replace("module.", ""), "the artifact key must be read from the source map by the module's builder name, never typed")
    sch = re.search(r'resource\s+"aws_scheduler_schedule"\s+"[^"]+"\s*\{(.*?)\n\}', t, re.S)
    need(sch is not None and re.search(r'state\s*=\s*"DISABLED"', sch.group(1)), "the schedule must be created with state = \"DISABLED\"")
    need(CRON in sch.group(1) and ZONE in sch.group(1), "the schedule must carry %s in %s" % (CRON, ZONE))
    st = statements(t)
    need(sorted(st) == sorted(EXEC_SIDS + OTHER_SIDS), "the statement ids must be exactly %s; read %s" % (sorted(EXEC_SIDS + OTHER_SIDS), sorted(st)))
    puts = [s for s, b in st.items() if "s3:PutObject" in actions_of(b)]
    need(puts == ["WriteTheFilledReportValuesPrefixOnly"] and "filled_report_values" in st[puts[0]], "exactly one PutObject statement, on the filled_report_values prefix")
    need(sorted(s for s, b in st.items() if "lambda:InvokeFunction" in actions_of(b)) == ["InvokeOwnFunctionOnly", "InvokeTheReportFunctionOnly"], "exactly two lambda:InvokeFunction statements: the function's own and the scheduler's")
    for s, b in st.items():
        acts = actions_of(b)
        need(acts and all("*" not in a for a in acts) and set(acts) <= ALLOWED_ACTIONS, "statement %s: explicit allowed actions only, found %s" % (s, acts))
        need('resources = ["*"]' not in b and '"arn:aws:s3:::*' not in b, "statement %s grants all resources" % s)
    reads = st["ReadCottonwoodGoldInputsOnly"] + st["ListCottonwoodGoldInputsAndFilledOnly"]
    need("account_dim" in reads and "account_return_daily" in reads, "the read statements must name account_dim and account_return_daily")
    for other in ("holdings_performance", "account_activity", "account_lot", "account_class", "household_crosswalk", "49financial"):
        need(other not in "\n".join(st[s] for s in EXEC_SIDS), "an execution statement names %s, a table this handler never reads" % other)
    sv = st["ReadTheServedModelSeriesObjectOnly"]
    need((SERVED_KEY in sv and sv.count("arn:aws:s3:::") == 1) or re.search(r"resources\s*=\s*\[\s*local\.\w*served_object_arn\s*\]", sv), "the served series statement names the one object (its ARN, or a local derived from the adapter's constants named ..served_object_arn)")
    for nm in typed_names:
        need(('"%s"' % nm) not in t, "the builder name %s is typed in the Terraform; take it from the opal_name module" % nm)
    need(re.search(r'key\s*=\s*"%s"' % re.escape(STATE_KEY), t), "the backend state key must be %s" % STATE_KEY)
    return True


OPTIONAL_IMPORTS = {"opal_naming_rootcheck", "pandas_market_calendars"}  # a CLI-only path in opal_naming and a guarded fallback in trading_calendar: never required at run time


def third_party(sources, bundle_modules):
    """Every top-level module any statement of the bundle's python files imports (function-level imports count: pyarrow is imported lazily), minus the stdlib, the bundle's own modules and the two known optional ones."""
    std = set(sys.stdlib_module_names)
    found = set()
    for name, src in sources.items():
        for node in ast.walk(ast.parse(src, filename=name)):
            if isinstance(node, ast.Import):
                found |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                found.add(node.module.split(".")[0])
    return sorted(m for m in found if m not in std and m not in bundle_modules and m != "__future__" and m not in OPTIONAL_IMPORTS)


def check_imports(tp, layer_has):
    need(set(tp) - RUNTIME_PROVIDED == {"pyarrow"}, "the bundle's third-party imports (any statement, besides boto3/botocore) must be exactly pyarrow, read %s" % sorted(set(tp) - RUNTIME_PROVIDED))
    need(layer_has("python/pyarrow/__init__.py"), "the layer zip does not hold python/pyarrow/__init__.py")
    return True


def check_gate_output(out):
    need("NAMING-PLAN:" in out and "REFUSE" not in out.split("NAMING-PLAN:")[1], "the naming gate refused: %s" % out.strip().splitlines()[-1:])
    need(out.count("NAMING CONFORMANT") == 6 and "NAMING REFUSE" not in out, "expected 6 CONFORMANT and no REFUSE lines, read %d CONFORMANT" % out.count("NAMING CONFORMANT"))
    return True


def check_package(names_in_zip, expected, bytes_of_zip, bytes_expected):
    need(sorted(names_in_zip) == sorted(expected), "zip members differ: extra %s missing %s" % (sorted(set(names_in_zip) - set(expected))[:3], sorted(set(expected) - set(names_in_zip))[:3]))
    for m in expected:
        need(bytes_of_zip(m) == bytes_expected(m), "zip member %s differs from its source" % m)
    return True


def check_entry(base_map, new_map, head_blob, pin_blob, pin_ok, expect_role):
    need(ENTRY_KEY in new_map["functions"] and ENTRY_KEY not in base_map["functions"], "the entry %s must be NEW" % ENTRY_KEY)
    for k, v in base_map["functions"].items():
        need(new_map["functions"].get(k) == v, "another entry changed: %s" % k)
    for k in base_map:
        if k != "functions":
            need(new_map.get(k) == base_map[k], "a top-level key changed: %s" % k)
    e = new_map["functions"][ENTRY_KEY]
    need(e.get("pipeline") == "investor-reporting" and e.get("source_dir") == SOURCE_DIR and e.get("artifact_s3_key") == "investor-reporting/irpt-cot-reporting-gold-lambda.zip", "pipeline, source_dir or artifact_s3_key")
    need(e.get("files") == ["handler.py"] + CLOSURE, "files must be handler.py then the 18 closure members in the checker's order")
    need(e.get("tf_file") == ROOT_DIR + "lambda.tf" and e.get("tf_resource") == "module.irpt_reporting_gold_iso.aws_lambda_function.this" and e.get("iam_role") == expect_role, "tf_file, tf_resource or iam_role")
    sf = e.get("staged_from")
    need(isinstance(sf, list) and [s["repo_path"] for s in sf] == CLOSURE, "staged_from must list exactly the closure members in order")
    for s in sf:
        need(set(s) == {"repo_path", "pin", "packaged_as", "sha256"} and s["packaged_as"] == s["repo_path"], "member form: %s" % s.get("repo_path"))
        need(isinstance(s["pin"], str) and HEX40.match(s["pin"]) and isinstance(s["sha256"], str) and HEX64.match(s["sha256"]), "pin or sha256 form: %s" % s["repo_path"])
        need(pin_ok(s["pin"]), "pin of %s is not an ancestor commit" % s["repo_path"])
        need(sha(pin_blob(s["pin"], s["repo_path"])) == s["sha256"] == sha(head_blob(s["repo_path"])), "sha256 of %s differs from git show pin:path or HEAD" % s["repo_path"])
    return True


def check_facts(rec, names, peak_note_ok=True):
    exp = {"root", "names", "resources", "expected_plan", "schedule", "memory", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["root"] == ROOT_DIR and rec["names"] == names, "root or names differ from the builder recount")
    need(isinstance(rec["resources"], list) and len(rec["resources"]) == 7, "resources: the seven addresses the plan will add")
    need(rec["expected_plan"] == {"add": 7, "change": 0, "destroy": 0, "claim": "inferred"}, "expected_plan must be 7/0/0 claimed inferred")
    need(rec["schedule"] == {"cron": CRON, "zone": ZONE, "state": "DISABLED"}, "schedule block")
    need(rec["memory"] == {"memory_mb": 1024, "basis": "issuer local measurement, peak 408 MB, 70 percent rule", "claim": "inferred"}, "memory block must carry the issuer's measurement and claim inferred")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


# ------------------------------------------------------------------------------------------------ the live run
def module_blocks(text):
    out = {}
    for m in re.finditer(r'module\s+"([^"]+)"\s*\{(.*?)\n\}', text, re.S):
        blk = m.group(2)
        if "opal_name" not in blk:
            continue
        g = {k: re.search(r'^\s*%s\s*=\s*"([^"]*)"' % k, blk, re.M) for k in ("system", "function", "kind", "qualifier")}
        out[m.group(1)] = {k: (v.group(1) if v else None) for k, v in g.items()}
    return out


def builder_names(root, text):
    sys.path.insert(0, str(root))
    from lib import opal_naming
    land = json.loads((Path(root) / LANDING_REL).read_text(encoding="utf-8"))
    scope = land["names"][0]["builder_args"]["scope"]
    mods = module_blocks(text)
    want = [("lambda", None), ("role", "execution"), ("policy", "execution"), ("policy", "scheduler"), ("role", "scheduler"), ("daily", None)]
    out = []
    for kind, qual in want:
        hit = [v for v in mods.values() if v["kind"] == kind and v["qualifier"] == qual]
        need(len(hit) == 1 and hit[0]["system"] == "irpt" and hit[0]["function"] == "reporting-gold", "exactly one opal_name module for irpt / reporting-gold / %s / %s" % (kind, qual))
        kw = {"qualifier": qual} if qual else {}
        out.append(opal_naming.name("irpt", scope, "reporting-gold", kind, **kw))
    return out


def run_gate(root, names):
    kinds = [("aws_lambda_function", "this"), ("aws_iam_role", "irpt_reporting_gold_iso_execution"), ("aws_iam_role_policy", "irpt_reporting_gold_iso_execution"),
             ("aws_iam_role_policy", "irpt_reporting_gold_iso_scheduler"), ("aws_iam_role", "irpt_reporting_gold_iso_scheduler"), ("aws_scheduler_schedule", "irpt_reporting_gold_iso")]
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


def layer_names(version):
    import boto3
    lam = boto3.client("lambda", region_name="us-east-1")
    url = lam.get_layer_version(LayerName=LAYER_NAME, VersionNumber=version)["Content"]["Location"]
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "layer.zip"
        urllib.request.urlretrieve(url, str(p))
        with zipfile.ZipFile(p) as z:
            return set(z.namelist())


def latest_layer_version():
    import boto3
    lam = boto3.client("lambda", region_name="us-east-1")
    return max(v["Version"] for v in lam.list_layer_versions(LayerName=LAYER_NAME)["LayerVersions"])


def run(root, cid):
    root = Path(root)
    d = root / ROOT_DIR
    need(d.is_dir(), "no %s" % ROOT_DIR)
    files = {p.name: p.read_text(encoding="utf-8") for p in sorted(d.glob("*.tf"))}
    alltext = "\n".join(files[k] for k in sorted(files))
    names = builder_names(root, alltext)
    if cid == "DB133-1-AC1":
        check_hcl(files, names)
        print("OK: root HCL: 5 resource blocks, one yang-lambda module (1024 MB, 900 s, no reserved concurrency, the native layer), six opal_name calls, a DISABLED %s schedule, exactly the %d expected statements with explicit actions, one PutObject on filled_report_values, no typed builder name" % (CRON, len(EXEC_SIDS + OTHER_SIDS)))
        return True
    if cid == "DB133-1-AC2":
        out = run_gate(root, names)
        check_gate_output(out)
        sm = json.loads((root / SOURCE_MAP_REL).read_text(encoding="utf-8"))["functions"][ENTRY_KEY]
        sources = {}
        for f in sm["files"]:
            if f.endswith(".py"):
                sources[f] = (root / ((SOURCE_DIR + "/" + f) if f == "handler.py" else f)).read_text(encoding="utf-8")
        mods = {Path(f).stem for f in sources} | {"lib"}
        check_imports(third_party(sources, mods), lambda n: n in layer_names(latest_layer_version()))
        env = dict(os.environ, BUILD_ONLY="1")
        r = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", ENTRY_KEY], cwd=str(root), env=env, capture_output=True, text=True, timeout=300)
        m = re.search(r"BUILD_ONLY:\s*(\S+)\s+sha256=(\S+)", r.stdout + r.stderr)
        need(r.returncode == 0 and m is not None, "the build-only run failed (rc %s): %s" % (r.returncode, (r.stdout + r.stderr)[-300:].replace("\n", " | ")))
        zpath = m.group(1)
        if zpath.startswith("/"):
            cp = subprocess.run(["cygpath", "-w", zpath], capture_output=True, text=True)
            need(cp.returncode == 0, "cygpath could not resolve %s" % zpath)
            zpath = cp.stdout.strip()
        with zipfile.ZipFile(zpath) as z:
            check_package([n for n in z.namelist() if not n.endswith("/")], sm["files"], lambda mem: z.read(mem),
                          lambda mem: (root / ((SOURCE_DIR + "/" + mem) if mem == "handler.py" else mem)).read_bytes())
        print("OK: the real naming gate grades the six named resources CONFORMANT; the bundle's third-party imports are pyarrow plus the runtime's and the layer holds it; the build-only package of %d members equals its sources byte for byte" % len(sm["files"]))
        return True
    if cid == "DB133-1-AC3":
        base = base_commit(root)
        bm = json.loads(git(root, "show", "%s:%s" % (base, SOURCE_MAP_REL))[0])
        nm = json.loads((root / SOURCE_MAP_REL).read_text(encoding="utf-8"))
        def head_blob(p):
            return (root / p).read_bytes()

        def pin_blob(pin, p):
            r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (pin, p)], capture_output=True)
            need(r.returncode == 0, "git show %s:%s failed" % (pin[:10], p))
            return r.stdout

        def pin_ok(pin):
            return subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", pin, "HEAD"], capture_output=True).returncode == 0
        check_entry(bm, nm, head_blob, pin_blob, pin_ok, names[1])
        rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
        check_facts(rec, names)
        print("OK: source-map entry %s is NEW with %d members pinned to ancestor commits with matching sha256, tf fields filled, no other entry moved; the facts record equals the builder recount" % (ENTRY_KEY, len(CLOSURE)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy

    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)

    def stmt(sid, actions, resources, extra=""):
        return 'statement {\n  sid = "%s"\n  effect = "Allow"\n  actions = [%s]\n  resources = [%s]\n%s}\n' % (
            sid, ", ".join('"%s"' % a for a in actions), ", ".join('"%s"' % r for r in resources), extra)
    g = "arn:aws:s3:::gold/irpt/x/gold/"
    sts = "".join([
        stmt("ListCottonwoodGoldInputsAndFilledOnly", ["s3:ListBucket"], ["arn:aws:s3:::gold"], '  values = ["irpt/x/gold/account_dim/*", "irpt/x/gold/account_return_daily/*", "irpt/x/gold/filled_report_values/*"]\n'),
        stmt("ReadCottonwoodGoldInputsOnly", ["s3:GetObject"], [g + "account_dim/*", g + "account_return_daily/*"]),
        stmt("WriteTheFilledReportValuesPrefixOnly", ["s3:PutObject"], [g + "filled_report_values/*"]), stmt("ReadBackTheFilledPrefixOnly", ["s3:GetObject"], [g + "filled_report_values/*"]),
        stmt("ReadTheServedModelSeriesObjectOnly", ["s3:GetObject"], ["arn:aws:s3:::opal-data-portal-v2/" + SERVED_KEY]), stmt("InvokeOwnFunctionOnly", ["lambda:InvokeFunction"], ["arn:aws:lambda:x"]),
        stmt("OwnLogStreamOnly", ["logs:CreateLogStream", "logs:PutLogEvents"], ["arn:aws:logs:x"]),
        stmt("ExecutionRoleAssumedByLambdaService", ["sts:AssumeRole"], ["arn:aws:iam:x"]), stmt("SchedulerRoleAssumedBySchedulerService", ["sts:AssumeRole"], ["arn:aws:iam:y"]),
        stmt("InvokeTheReportFunctionOnly", ["lambda:InvokeFunction"], ["arn:aws:lambda:x"])])
    mods = "".join('module "m%d" {\n  source = "../../modules/opal_name"\n}\n' % i for i in range(6))
    lam = ('module "irpt_reporting_gold_iso" {\n  source = "../../modules/yang-lambda"\n  handler = "handler.lambda_handler"\n  timeout = 900\n  memory_size = 1024\n'
           '  layers = [data.aws_lambda_layer_version.%s.arn]\n  artifact_key = file("lambda-source-map.json")\n}\n' % DATA_NAME)
    data = 'data "aws_lambda_layer_version" "%s" {\n  layer_name = "%s"\n}\n' % (DATA_NAME, LAYER_NAME)
    res = ('resource "aws_iam_role" "a" {}\nresource "aws_iam_role" "b" {}\nresource "aws_iam_role_policy" "c" {}\nresource "aws_iam_role_policy" "d" {}\n'
           'resource "aws_scheduler_schedule" "s" {\n  state = "DISABLED"\n  schedule_expression = "%s"\n  schedule_expression_timezone = "%s"\n}\n' % (CRON, ZONE))
    back = 'terraform {\n  backend "s3" {\n    key = "%s"\n  }\n}\n' % STATE_KEY
    good = {"main.tf": back + data + mods + lam + res + sts}
    assert check_hcl(good, ["irpt-cot-x"])
    base = good["main.tf"]
    arms = (("memory", base.replace("memory_size = 1024", "memory_size = 2048")), ("reserved", base.replace("timeout = 900", "timeout = 900\n  reserved_concurrent_executions = 1")),
            ("no layer", base.replace("layers = [data.aws_lambda_layer_version.%s.arn]" % DATA_NAME, "layers = []")), ("enabled", base.replace('state = "DISABLED"', 'state = "ENABLED"')),
            ("cron", base.replace(CRON, "cron(0 1 ? * * *)")), ("typed name", base + '\nresource "x" "y" { name = "irpt-cot-x" }\n'), ("extra table", base.replace("ReadBackTheFilledPrefixOnly", "ReadBackTheFilledPrefixOnly") + '\n# x\nstatement {\n  sid = "Z"\n}\n'),
            ("wildcard", base.replace('actions = ["logs:CreateLogStream", "logs:PutLogEvents"]', 'actions = ["logs:*"]')), ("second put", base.replace('sid = "ReadBackTheFilledPrefixOnly"\n  effect = "Allow"\n  actions = ["s3:GetObject"]', 'sid = "ReadBackTheFilledPrefixOnly"\n  effect = "Allow"\n  actions = ["s3:PutObject"]')),
            ("state key", base.replace(STATE_KEY, "investor-reporting/other/tfstate")), ("holdings table", base.replace(g + "account_dim/*", g + "holdings_performance_daily/*")),
            ("five opal modules", base.replace('module "m5" {\n  source = "../../modules/opal_name"\n}\n', "")))
    for label, txt in arms:
        red(lambda: check_hcl({"main.tf": txt}, ["irpt-cot-x"]), label)
    red(lambda: check_hcl({}, []), "no files")
    src = {"handler.py": "import json\nimport pyarrow as pa\nimport opal_naming\n"}
    assert check_imports(third_party(src, {"handler", "opal_naming"}), lambda n: True)
    red(lambda: check_imports(["pyarrow", "pandas"], lambda n: True), "extra third party")
    red(lambda: check_imports(["pyarrow"], lambda n: False), "layer lacks pyarrow")
    ok = "NAMING CONFORMANT x\n" * 6 + "NAMING-PLAN: PASS 6 graded\n"
    assert check_gate_output(ok)
    red(lambda: check_gate_output(ok.replace("PASS 6 graded", "REFUSE 6 graded")), "refuse")
    red(lambda: check_gate_output("NAMING CONFORMANT x\n" * 5 + "NAMING-PLAN: PASS 5 graded\n"), "five")
    members = ["handler.py", "a.py"]
    srcb = {"handler.py": b"h", "a.py": b"a"}
    assert check_package(members, members, lambda m: srcb[m], lambda m: srcb[m])
    red(lambda: check_package(members + ["x"], members, lambda m: srcb.get(m, b""), lambda m: srcb[m]), "extra member")
    red(lambda: check_package(members, members, lambda m: b"z", lambda m: srcb[m]), "bytes")
    # the entry
    contents = {f: f.encode() * 2 for f in CLOSURE}
    pins = {f: "%040x" % (i + 1) for i, f in enumerate(CLOSURE)}
    staged = [{"repo_path": f, "pin": pins[f], "packaged_as": f, "sha256": sha(contents[f])} for f in CLOSURE]
    bmap = {"functions": {"other": {"x": 1}}}
    entry = {"pipeline": "investor-reporting", "source_dir": SOURCE_DIR, "artifact_s3_key": "investor-reporting/irpt-cot-reporting-gold-lambda.zip", "files": ["handler.py"] + CLOSURE,
             "tf_file": ROOT_DIR + "lambda.tf", "tf_resource": "module.irpt_reporting_gold_iso.aws_lambda_function.this", "iam_role": "irpt-cot-reporting-gold-execution-role", "staged_from": staged}
    nmap = {"functions": {"other": {"x": 1}, ENTRY_KEY: entry}}

    def go(m, **kw):
        return check_entry(bmap, m, kw.get("head", lambda p: contents[p]), kw.get("pb", lambda pin, p: contents[p]), kw.get("ok", lambda pin: True), "irpt-cot-reporting-gold-execution-role")
    assert go(nmap)
    red(lambda: go(nmap, ok=lambda pin: False), "pin ancestry")
    red(lambda: go(nmap, pb=lambda pin, p: b"drift"), "pin content")
    red(lambda: go(nmap, head=lambda p: b"moved"), "head differs")
    for label, fn in (("other entry", lambda m: m["functions"]["other"].update(x=2)), ("files", lambda m: m["functions"][ENTRY_KEY].update(files=["handler.py"])),
                      ("tf_file", lambda m: m["functions"][ENTRY_KEY].update(tf_file="x")), ("iam_role", lambda m: m["functions"][ENTRY_KEY].update(iam_role="x")),
                      ("member lost", lambda m: m["functions"][ENTRY_KEY]["staged_from"].pop()), ("null pin", lambda m: m["functions"][ENTRY_KEY]["staged_from"][0].update(pin=None)),
                      ("source_dir", lambda m: m["functions"][ENTRY_KEY].update(source_dir="x")), ("existing", lambda m: None)):
        m2 = copy.deepcopy(nmap)
        fn(m2)
        if label == "existing":
            red(lambda: check_entry({"functions": {ENTRY_KEY: entry}}, m2, lambda p: contents[p], lambda pin, p: contents[p], lambda pin: True, "irpt-cot-reporting-gold-execution-role"), label)
        else:
            red(lambda: go(m2), label)
    rec = {"root": ROOT_DIR, "names": ["a", "b", "c", "d", "e", "f"], "resources": ["r"] * 7, "expected_plan": {"add": 7, "change": 0, "destroy": 0, "claim": "inferred"},
           "schedule": {"cron": CRON, "zone": ZONE, "state": "DISABLED"}, "memory": {"memory_mb": 1024, "basis": "issuer local measurement, peak 408 MB, 70 percent rule", "claim": "inferred"}, "words": "w" * 100}
    assert check_facts(rec, ["a", "b", "c", "d", "e", "f"])
    for label, fn in (("names", lambda r: r.update(names=["x"])), ("resources", lambda r: r.update(resources=["r"])), ("plan", lambda r: r["expected_plan"].update(add=6)),
                      ("schedule", lambda r: r["schedule"].update(state="ENABLED")), ("memory", lambda r: r["memory"].update(memory_mb=2048)), ("words", lambda r: r.update(words="short")),
                      ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, ["a", "b", "c", "d", "e", "f"]), label)
    print("selftest: hcl (%d red arms), imports, gate, package, entry (12 red arms) and facts (8 red arms) clauses behave" % (len(arms) + 1))
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
