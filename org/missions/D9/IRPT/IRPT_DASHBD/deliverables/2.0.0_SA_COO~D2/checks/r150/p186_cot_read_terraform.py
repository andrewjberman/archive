"""IRPT_DASHBD round 150, workstream COTTF (issuer 2.0.0_SA_COO~D2) -- DB-b-320, C2 of the Cottonwood Performance read path: the TERRAFORM. A NEW root
`infra/aws/terraform/investor-reporting/reporting-read-iso/` (four .tf files) declaring the Cottonwood read function, its execution role and its two policies; and, in the
`reporting-read` root, a new `forward.tf` plus ONE environment line in `lambda.tf`: the forward target's name (builder output) and ONE `lambda:InvokeFunction` statement on that
one function. No route, no S3 grant on the 49 Financial role, no schedule. LOCAL: nothing is planned or applied (the box has no terraform); the applier's plan reads the rest.

  DB186-1-AC1   the iso root's HCL: resources, modules, environment keys, statements and actions, no typed firm token, no forward variable, no API wiring
  DB186-1-AC2   the forward half: forward.tf and the one lambda.tf line; the changed-file set is exactly the agreed set
  DB186-1-AC3   the builder recount of the five names, the REAL naming gate in plan mode on the named resources, and the facts record

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>     green on a reference tree, red on single-fault mutants
"""
import difflib
import glob
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-320.cottonwood-read-path-c2-terraform.md"
ISO = "infra/aws/terraform/investor-reporting/reporting-read-iso/"
READ = "infra/aws/terraform/investor-reporting/reporting-read/"
STATE_KEY = "investor-reporting/reporting-read-iso/tfstate"
MODULE = "irpt_reporting_read_iso"
GATE = ".tools/naming-apply-gate.py"
ISO_FILES = ["iam.tf", "lambda.tf", "locals.tf", "main.tf"]
ISO_SIDS = ["ListExactlyThePlatinumReportingPrefix", "ReadThePlatinumReportingPrefixOnly", "ReadCurrentScopeDependencies", "OwnLogStreamOnly"]
SP_SIDS = ["ReadServiceProfileByEmailIndex", "ReadServiceProfileRow", "DecryptUsersTableViaDynamoOnly"]
ALLOWED_ACTIONS = {"s3:GetObject", "s3:GetObjectVersion", "s3:ListBucket", "logs:CreateLogStream", "logs:PutLogEvents", "sts:AssumeRole", "dynamodb:Query", "dynamodb:GetItem", "kms:Decrypt"}
ENV_KEYS = {"IRPT_DIRECTORY_BUCKET_MAP", "IRPT_FIRM_REGISTRY"}
FWD_ENV = "IRPT_FORWARD_COTTONWOOD_FUNCTION"
FWD_LINE = FWD_ENV + " = module.irpt_reporting_read_forward_target_name.name"
LONG_DIGITS = re.compile(r"\d{8,}")
ISO_RESOURCES = ["module.%s.aws_lambda_function.this" % MODULE, "module.%s.aws_cloudwatch_log_group.lambda" % MODULE, "aws_iam_role.%s" % MODULE,
                 "aws_iam_role_policy.%s" % MODULE, "aws_iam_role_policy.%s_service_profile" % MODULE]


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout.decode("utf-8", "replace"), r.returncode


def uncommented(text):
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))


def blocks(text, opener):
    """Brace-balanced blocks that start with the regex `opener` (which must end just before the opening brace)."""
    out = []
    for m in re.finditer(opener + r"\s*\{", text):
        depth, i = 1, m.end()
        while depth and i < len(text):
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        out.append(text[m.start():i])
    return out


def sids_hcl(text):
    return [re.search(r'sid\s*=\s*"([^"]+)"', b).group(1) for b in blocks(text, r"statement") if re.search(r'sid\s*=\s*"([^"]+)"', b)]


def sids_json(text):
    return re.findall(r'\bSid\s*=\s*"([^"]+)"', text)


def actions_all(text):
    acts = []
    for m in re.finditer(r"\b(?:actions|Action)\s*=\s*\[([^\]]*)\]", text):
        acts += re.findall(r'"([^"]+)"', m.group(1))
    return acts


def modules(text):
    return {m.group(1): m.group(2) for m in re.finditer(r'module\s+"([^"]+)"\s*\{(.*?)\n\}', text, re.S)}


def opal_calls(text):
    out = []
    for name, body in modules(text).items():
        if "opal_name" in body:
            g = {k: re.search(r'^\s*%s\s*=\s*(.+?)\s*$' % k, body, re.M) for k in ("system", "scope", "function", "kind", "qualifier")}
            out.append((name, {k: (v.group(1).strip('"') if v else None) for k, v in g.items()}))
    return out


def resource_types(text):
    return re.findall(r'^\s*resource\s+"([a-z0-9_]+)"\s+"[^"]+"', text, re.M)


# ------------------------------------------------------------------------------------------------ AC1 (pure)
def check_iso(files):
    need(sorted(files) == ISO_FILES, "the root must hold exactly %s, found %s" % (ISO_FILES, sorted(files)))
    t = uncommented("\n".join(files[k] for k in sorted(files)))
    types = resource_types(t)
    need(sorted(types) == ["aws_iam_role", "aws_iam_role_policy", "aws_iam_role_policy"], "the root declares exactly one role and two role policies and nothing else (no API, permission, schedule, topic or mail resource); read %s" % sorted(types))
    mods = modules(t)
    lam = [(n, b) for n, b in mods.items() if "yang-lambda" in b]
    need(len(lam) == 1 and lam[0][0] == MODULE, "exactly one yang-lambda module, named %s" % MODULE)
    body = lam[0][1]
    need(re.search(r'handler\s*=\s*"entry\.lambda_handler"', body) and re.search(r"\btimeout\s*=\s*29\b", body) and re.search(r"\bmemory_size\s*=\s*512\b", body), "handler entry.lambda_handler, timeout 29 and memory_size 512")
    need("reserved_concurrent_executions" not in body and "layers" not in body, "no reserved concurrency and no layer")
    need(re.search(r"artifact_key\s*=\s*local\.irpt_rri_artifact_key", body), "the artifact key is read through the function-map local")
    need("function-map" in t and "lambda-source-map" not in t, "the artifact key is read from the function map, never the retired source map")
    env = re.search(r"environment_variables\s*=\s*\{(.*?)\n  \}", body, re.S)
    need(env is not None and set(re.findall(r"^\s*(IRPT_[A-Z_]+)\s*=", env.group(1), re.M)) == ENV_KEYS, "environment keys must be exactly %s" % sorted(ENV_KEYS))
    need(FWD_ENV not in t and "IRPT_EVIDENCE_BUCKET" not in t, "this function never carries the forward variable or the evidence bucket")
    calls = opal_calls(t)
    kinds = sorted((c[1]["kind"], c[1]["qualifier"] or "") for c in calls)
    need(kinds == [("lambda", ""), ("policy", ""), ("policy", "service-profile"), ("role", "")], "four opal_name calls: lambda, role, policy, policy service-profile; read %s" % kinds)
    for n, c in calls:
        need(c["system"] == "irpt" and c["function"] == "reporting-read" and c["scope"] == "local.irpt_rri_firm", "opal_name %s: system irpt, function reporting-read, scope local.irpt_rri_firm" % n)
    need(not re.search(r'"(cottonwood|cot|49financial|49f)"|opal-data-', t), "a firm token or bucket is typed in the Terraform; every one is derived")
    need(re.search(r'key\s*=\s*"%s"' % re.escape(STATE_KEY), t), "the backend state key must be %s" % STATE_KEY)
    need(sorted(sids_hcl(t)) == sorted(ISO_SIDS) and sorted(sids_json(t)) == sorted(SP_SIDS), "statement ids must be exactly %s and %s" % (ISO_SIDS, SP_SIDS))
    acts = actions_all(t)
    need(acts and set(acts) <= ALLOWED_ACTIONS and all("*" not in a for a in acts), "explicit allowed actions only: read %s" % sorted(set(acts) - ALLOWED_ACTIONS))
    need('resources = ["*"]' not in t and 'Resource = ["*"]' not in t and '"arn:aws:s3:::*' not in t, "no statement grants all resources")
    need("irpt_rri_platinum_read_arns" in t and "platinum/reporting/" in t and re.search(r'"irpt/\$\{local\.irpt_rri_firm\}/platinum/reporting/"', t), "the product read is the platinum reporting prefix of the derived firm")
    need("irpt_rri_scope_dependency_arns" in t, "the scope-dependency read grant is present")
    return True


# ------------------------------------------------------------------------------------------------ AC2 (pure)
def check_forward(forward_tf, lambda_old, lambda_new):
    t = uncommented(forward_tf)
    need(resource_types(t) == ["aws_iam_role_policy"], "forward.tf declares exactly one aws_iam_role_policy and nothing else")
    calls = opal_calls(t)
    kinds = sorted((c[1]["kind"], c[1]["qualifier"] or "") for c in calls)
    need(kinds == [("lambda", ""), ("policy", "forward")], "two opal_name calls: the target lambda and the forward policy; read %s" % kinds)
    tgt = [c for n, c in calls if n == "irpt_reporting_read_forward_target_name"]
    need(len(tgt) == 1 and tgt[0]["system"] == "irpt" and tgt[0]["function"] == "reporting-read" and tgt[0]["scope"] == "local.irpt_rr_fwd_firm", "the target name module: irpt / reporting-read / lambda, scope local.irpt_rr_fwd_firm")
    pol = [c for n, c in calls if n == "irpt_reporting_read_forward_policy_name"]
    need(len(pol) == 1 and pol[0]["scope"] == "local.irpt_rr_firm", "the policy name module carries this root's own scope local.irpt_rr_firm")
    need(sids_json(t) == ["InvokeTheCottonwoodReadFunctionOnly"], "exactly one statement id InvokeTheCottonwoodReadFunctionOnly")
    need(actions_all(t) == ["lambda:InvokeFunction"], "the one action is lambda:InvokeFunction")
    need(re.search(r"Resource\s*=\s*\[\s*\"arn:aws:lambda:\$\{data\.aws_region\.current\.name\}:\$\{data\.aws_caller_identity\.current\.account_id\}:function:\$\{module\.irpt_reporting_read_forward_target_name\.name\}\"\s*\]", t),
         "the one resource is the ARN of the one target function, built from the builder-named module")
    need(re.search(r"role\s*=\s*aws_iam_role\.irpt_reporting_read\.id", t), "the policy attaches to the 49 Financial read role")
    need("s3:" not in t and '"*"' not in t and not re.search(r'"(cottonwood|cot|49financial|49f)"|opal-data-', t), "no S3 action, no wildcard, no typed firm token")
    removed = [ln for ln in difflib.unified_diff(lambda_old.splitlines(), lambda_new.splitlines(), lineterm="", n=0) if ln.startswith("-") and not ln.startswith("---")]
    added = [ln for ln in difflib.unified_diff(lambda_old.splitlines(), lambda_new.splitlines(), lineterm="", n=0) if ln.startswith("+") and not ln.startswith("+++")]
    need(not removed and len(added) <= 8, "lambda.tf may only gain lines (at most 8, none removed): removed %d, added %d" % (len(removed), len(added)))
    need(any(FWD_LINE in ln for ln in added), "lambda.tf must gain the line `%s`" % FWD_LINE)
    need(not [ln for ln in added if ln.strip() and not ln.lstrip("+").strip().startswith("#") and FWD_ENV not in ln and ln.strip() != "+"], "the only non-comment line lambda.tf gains is the forward variable")
    return True


def check_changed_set(changed, worker_dir):
    allowed_files = {ISO + f for f in ISO_FILES} | {READ + "forward.tf", READ + "lambda.tf", ORDER_REL}
    extra = [f for f in changed if f not in allowed_files and not f.startswith(worker_dir) and not f.startswith("org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/")]
    need(not extra, "files outside the agreed set changed: %s" % sorted(extra)[:4])
    need(all((ISO + f) in changed for f in ISO_FILES) and (READ + "forward.tf") in changed and (READ + "lambda.tf") in changed, "the four iso files, forward.tf and lambda.tf must all be in the change")
    return True


# ------------------------------------------------------------------------------------------------ AC3 (pure)
def check_facts(rec, names):
    exp = {"iso_root", "names", "iso_resources", "iso_plan", "read_root_plan", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["iso_root"] == ISO and rec["names"] == names, "iso_root or names differ from the builder recount")
    need(rec["iso_resources"] == ISO_RESOURCES, "iso_resources must be the five addresses %s" % ISO_RESOURCES)
    need(rec["iso_plan"] == {"add": 5, "change": 0, "destroy": 0, "claim": "inferred"}, "iso_plan must be 5/0/0 claimed inferred")
    need(isinstance(rec["read_root_plan"], dict) and {k: rec["read_root_plan"].get(k) for k in ("add", "change", "destroy", "claim")} == {"add": 1, "change": 1, "destroy": 0, "claim": "inferred"}
         and isinstance(rec["read_root_plan"].get("change_is"), str) and rec["read_root_plan"]["change_is"].strip(), "read_root_plan: add 1, change 1 (the function), destroy 0, claim inferred, change_is in words")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def check_gate_output(out, n):
    need("NAMING-PLAN:" in out and "REFUSE" not in out.split("NAMING-PLAN:")[1], "the naming gate refused: %s" % out.strip().splitlines()[-1:])
    need(out.count("NAMING CONFORMANT") == n and "NAMING REFUSE" not in out, "expected %d CONFORMANT and no REFUSE lines, read %d CONFORMANT" % (n, out.count("NAMING CONFORMANT")))
    return True


# ------------------------------------------------------------------------------------------------ the live run
def builder_names(root):
    sys.path.insert(0, str(root))
    from lib import opal_naming
    sc = {s["key"]: s for s in json.loads((Path(root) / "infra/logic/registry/scopes.json").read_text(encoding="utf-8"))["scopes"]}
    src = json.loads((Path(root) / "data/assets/scripts/gold/irpt_holdings_performance/sources.json").read_text(encoding="utf-8"))
    firm = sc[src["blackdiamond_z09"]["registry_key"]]["firm"]
    decl = json.loads((Path(root) / "data/assets/scripts/gold/irpt_reporting/sources.json").read_text(encoding="utf-8"))
    firms = {sc[v["registry_key"]]["firm"] for k, v in decl.items() if not k.startswith("_") and isinstance(v, dict) and v.get("registry_key")}
    need(len(firms) == 1, "the 49 Financial read root's declaration must resolve to exactly one firm")
    other = firms.pop()
    nm = opal_naming.name
    return [nm("irpt", firm, "reporting-read", "lambda"), nm("irpt", firm, "reporting-read", "role"), nm("irpt", firm, "reporting-read", "policy"),
            nm("irpt", firm, "reporting-read", "policy", qualifier="service-profile"), nm("irpt", other, "reporting-read", "policy", qualifier="forward")]


def run_gate(root, kinds, names, root_dir):
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
        r = subprocess.run([sys.executable, GATE, "--plan-json", str(p), "--root", root_dir.rstrip("/")], cwd=str(root), capture_output=True, text=True)
    return r.stdout + r.stderr


def worker_commit_files(root, serial):
    out, _ = git(root, "log", "--author=" + serial, "--name-only", "--format=")
    return {x for x in out.splitlines() if x.strip()}


def worker_base(root, serial, rel):
    out, _ = git(root, "log", "--author=" + serial, "--format=%H", "--", rel)
    commits = out.split()
    if commits:
        return commits[-1] + "^"
    return "HEAD"


def issued_to(root):
    m = re.search(r"<issued_to>([^<]+)</issued_to>", (Path(root) / ORDER_REL).read_text(encoding="utf-8"))
    need(m is not None, "the order has no issued_to")
    return m.group(1).strip()


def run(root, cid):
    root = Path(root)
    serial = issued_to(root)
    worker_dir = D + serial + "/"
    if cid == "DB186-1-AC1":
        d = root / ISO
        need(d.is_dir(), "no %s" % ISO)
        check_iso({p.name: p.read_text(encoding="utf-8") for p in sorted(d.glob("*.tf"))})
        print("OK: iso root: one role, two role policies, one yang-lambda module (29 s, 512 MB, no layer, no reserved concurrency), exactly the two environment keys and not the forward variable, four builder-named resources, exactly the expected statement ids and explicit allowed actions, no typed firm token, no API or schedule resource")
        return True
    if cid == "DB186-1-AC2":
        wf = worker_commit_files(root, serial)
        wt = {x for x in (git(root, "diff", "--name-only", "HEAD")[0] + git(root, "ls-files", "--others", "--exclude-standard")[0]).splitlines() if x.strip() and x.strip() != "portal"}  # the nested portal checkout is the provisioner's, never a worker's write
        check_changed_set(wf | wt, worker_dir)
        old = git(root, "show", "%s:%s" % (worker_base(root, serial, READ + "lambda.tf"), READ + "lambda.tf"))[0]
        check_forward((root / (READ + "forward.tf")).read_text(encoding="utf-8"), old, (root / (READ + "lambda.tf")).read_text(encoding="utf-8"))
        print("OK: the change touches only the iso root, forward.tf, lambda.tf and the worker's own folder; forward.tf holds one role policy with one lambda:InvokeFunction statement on the one builder-named target; lambda.tf only gained the forward variable")
        return True
    if cid == "DB186-1-AC3":
        names = builder_names(root)
        out1 = run_gate(root, [("aws_lambda_function", "this"), ("aws_iam_role", MODULE), ("aws_iam_role_policy", MODULE), ("aws_iam_role_policy", MODULE + "_service_profile")], names[:4], ISO)
        check_gate_output(out1, 4)
        out2 = run_gate(root, [("aws_iam_role_policy", "irpt_reporting_read_forward")], names[4:], READ)
        check_gate_output(out2, 1)
        recs = sorted(glob.glob(str(root / (D + serial) / "RD_COT_READ_ISO_FACTS_R150.json")))
        need(len(recs) == 1, "the facts record RD_COT_READ_ISO_FACTS_R150.json is missing from %s" % worker_dir)
        check_facts(json.loads(Path(recs[0]).read_text(encoding="utf-8")), names)
        print("OK: the real naming gate grades the four iso resources and the forward policy CONFORMANT; the five names equal the builder recount; the facts record is complete")
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest(ref_root):
    ref = Path(ref_root)
    serial = issued_to(ref) if (ref / ORDER_REL).exists() else "0.9.0_WK_IRPT_DASHBD~SELFTEST"
    names = builder_names(ref)
    wdir = ref / (D + serial)
    wdir.mkdir(parents=True, exist_ok=True)
    rec = {"iso_root": ISO, "names": names, "iso_resources": ISO_RESOURCES, "iso_plan": {"add": 5, "change": 0, "destroy": 0, "claim": "inferred"},
           "read_root_plan": {"add": 1, "change": 1, "destroy": 0, "claim": "inferred", "change_is": "the function environment gains the forward variable"}, "words": "w" * 100}
    (wdir / "RD_COT_READ_ISO_FACTS_R150.json").write_text(json.dumps(rec), encoding="utf-8")
    files = {p.name: p.read_text(encoding="utf-8") for p in sorted((ref / ISO).glob("*.tf"))}
    fwd = (ref / (READ + "forward.tf")).read_text(encoding="utf-8")
    lam_new = (ref / (READ + "lambda.tf")).read_text(encoding="utf-8")
    try:
        for fn in (lambda: check_iso(files), lambda: check_facts(rec, names)):
            fn()
        # lambda_old: the new text without the lines the order adds (everything from the DB-b-320 comment to the variable)
        i = lam_new.index("    # DB-b-320")
        j = lam_new.index(FWD_LINE) + len(FWD_LINE) + 1
        lam_old = lam_new[:i].rstrip("\n") + "\n" + lam_new[j:]
        need(lam_new != lam_old, "selftest: the reference lambda.tf lacks the added block")
        check_forward(fwd, lam_old, lam_new)
        n = 0

        def red(fn, label):
            nonlocal n
            try:
                fn()
            except Fail:
                n += 1
                return
            raise AssertionError("mutant passed: " + label)
        allf = lambda **kw: dict(files, **kw)  # noqa: E731
        iam, lam, loc, mn = files["iam.tf"], files["lambda.tf"], files["locals.tf"], files["main.tf"]

        def sub(text, a, b):
            assert a in text, "selftest: anchor missing: %s" % a[:50]
            return text.replace(a, b, 1)
        red(lambda: check_iso(allf(**{"lambda.tf": sub(lam, "memory_size = 512", "memory_size = 1024")})), "memory")
        red(lambda: check_iso(allf(**{"lambda.tf": sub(lam, "    IRPT_FIRM_REGISTRY", "    " + FWD_ENV + ' = "x"\n    IRPT_FIRM_REGISTRY')})), "forward variable set on the target")
        red(lambda: check_iso(allf(**{"lambda.tf": sub(lam, "  log_retention_days = 14", "  reserved_concurrent_executions = 1\n  log_retention_days = 14")})), "reserved concurrency")
        red(lambda: check_iso(allf(**{"iam.tf": iam + '\nresource "aws_lambda_permission" "x" {}\n'})), "extra resource type")
        red(lambda: check_iso(allf(**{"iam.tf": sub(iam, 'actions   = ["s3:GetObject", "s3:GetObjectVersion"]', 'actions   = ["s3:GetObject", "s3:PutObject"]')})), "put action")
        red(lambda: check_iso(allf(**{"iam.tf": sub(iam, 'actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]', 'actions   = ["logs:*"]')})), "wildcard action")
        red(lambda: check_iso(allf(**{"iam.tf": sub(iam, 'sid       = "ReadCurrentScopeDependencies"', 'sid       = "ReadMore"')})), "statement id")
        red(lambda: check_iso(allf(**{"iam.tf": sub(iam, "resources = local.irpt_rri_platinum_read_arns", 'resources = ["*"]')})), "resource star")
        red(lambda: check_iso(allf(**{"locals.tf": loc + '\n  # x\nlocals {\n  typed = "cottonwood"\n}\n'})), "typed firm token")
        red(lambda: check_iso(allf(**{"main.tf": sub(mn, 'key    = "%s"' % STATE_KEY, 'key    = "investor-reporting/other/tfstate"')})), "state key")
        red(lambda: check_iso(allf(**{"lambda.tf": sub(lam, "    IRPT_FIRM_REGISTRY = \"/var/task/firm_registry.json\"\n", "")})), "env key lost")
        red(lambda: check_iso(allf(**{"iam.tf": sub(iam, 'scope    = local.irpt_rri_firm\n  function = "reporting-read"\n  kind     = "role"', 'scope    = "x"\n  function = "reporting-read"\n  kind     = "role"')})), "role scope typed")
        red(lambda: check_iso({k: v for k, v in files.items() if k != "main.tf"}), "file missing")
        red(lambda: check_iso(allf(**{"locals.tf": loc.replace("function-map", "lambda-source-map")})), "retired source map")
        red(lambda: check_forward(sub(fwd, 'Action   = ["lambda:InvokeFunction"]', 'Action   = ["lambda:*"]'), lam_old, lam_new), "lambda star")
        red(lambda: check_forward(fwd + '\nresource "aws_lambda_permission" "x" {}\n', lam_old, lam_new), "extra resource in forward.tf")
        red(lambda: check_forward(sub(fwd, "function:${module.irpt_reporting_read_forward_target_name.name}", "function:*"), lam_old, lam_new), "resource not the one function")
        red(lambda: check_forward(sub(fwd, "InvokeTheCottonwoodReadFunctionOnly", "Other"), lam_old, lam_new), "forward sid")
        red(lambda: check_forward(sub(fwd, 'Action   = ["lambda:InvokeFunction"]', 'Action   = ["lambda:InvokeFunction", "s3:GetObject"]'), lam_old, lam_new), "s3 action")
        red(lambda: check_forward(fwd, lam_old, lam_new.replace(FWD_LINE, FWD_ENV + ' = "typed"')), "typed target")
        red(lambda: check_forward(fwd, lam_old + "# extra\n", lam_new), "a line removed from lambda.tf")
        red(lambda: check_forward(fwd, lam_old, lam_new + "\n".join("  x%d = 1" % k for k in range(10))), "too many lines")
        red(lambda: check_changed_set({ISO + f for f in ISO_FILES} | {READ + "forward.tf", READ + "lambda.tf", "infra/aws/lambda/ci/function-map/x.json"}, D + serial + "/"), "function-map file touched")
        red(lambda: check_changed_set({ISO + f for f in ISO_FILES}, D + serial + "/"), "forward files missing")
        red(lambda: check_facts(dict(rec, names=["x"]), names), "names")
        red(lambda: check_facts(dict(rec, iso_plan={"add": 4, "change": 0, "destroy": 0, "claim": "inferred"}), names), "plan")
        red(lambda: check_facts(dict(rec, words="short"), names), "words")
        red(lambda: check_facts(dict(rec, read_root_plan={"add": 1, "change": 1, "destroy": 0, "claim": "inferred", "change_is": ""}), names), "change_is")
        red(lambda: check_gate_output("NAMING CONFORMANT x\n" * 3 + "NAMING-PLAN: PASS 3 graded\n", 4), "gate count")
        red(lambda: check_gate_output("NAMING CONFORMANT x\nNAMING-PLAN: REFUSE 1\n", 1), "gate refuse")
    finally:
        try:
            (wdir / "RD_COT_READ_ISO_FACTS_R150.json").unlink()
            if serial.endswith("SELFTEST"):
                wdir.rmdir()
        except OSError:
            pass
    print("selftest: green on the reference and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2])
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or build is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
