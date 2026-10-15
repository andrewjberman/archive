"""IRPT_DASHBD round 123, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the Cottonwood account_dim PACKAGE (source-map entry + package test) and TERRAFORM root.

  DBC123-1-AC1 the source-map entry for the account_dim function: exact members, every pin resolves to its recorded sha256, shared members carry the holdings function's pins, nothing else in the file changed
  DBC123-1-AC2 the package test passes with the staged pins and FAILS with the old scopes pin (planted control)
  DBC123-2-AC1 the Terraform root's structure (builder names, DISABLED schedule in America/New_York, closed action set, no foreign-firm token) and two planted mutations the structure check must refuse
  DBC123-2-AC2 terraform fmt -check and validate pass in the new root

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = (HERE / "BASE_R123.txt").read_text(encoding="ascii").strip()
SM = "infra/aws/lambda/ci/lambda-source-map.json"
HOLD_KEY = "irpt-holdings-performance-lambda"
SRC_DIR = "infra/aws/lambda/investor-reporting/account-dim-cot"
ADAPTER = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_account_dim.py"
PKG_TEST = SRC_DIR + "/tests/test_package_resolves.py"
PKG_TEST_NAME = "test_package_resolves_silver_locations_and_target_day"
OLD_SCOPES_PIN = "14b52ca13a467e4be0e47231fb6840611bbb134a"
SHARED = ("data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py",
          "data/assets/scripts/gold/irpt_holdings_performance/sources.json",
          "data/assets/scripts/lib/stream_parquet.py", "lib/opal_naming.py", "lib/trading_calendar.py",
          "org/standards/NAMING_SCHEMA.json",
          "infra/logic/registry/systems.json", "infra/logic/registry/scopes.json", "infra/logic/registry/tiers.json",
          "infra/logic/registry/exemptions.json", "infra/logic/registry/remediations.json",
          "infra/logic/registry/resources.json", "infra/logic/registry/reporting_policies.json")
EXPECT_FILES = {"lambda_function.py", ADAPTER} | set(SHARED)
TF_ROOT = "infra/aws/terraform/investor-reporting/account-dim"
TF_FILES = ("main.tf", "locals.tf", "lambda.tf", "iam.tf", "schedule.tf")
ALLOWED_ACTIONS = {"s3:GetObject", "s3:ListBucket", "s3:PutObject", "logs:CreateLogStream", "logs:PutLogEvents",
                   "logs:CreateLogGroup", "lambda:InvokeFunction", "sts:AssumeRole"}
FOREIGN = ("49financial", "inflection", "orion", "schwab", "08335338")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True, timeout=60)
    need(r.returncode == 0, "git %s failed rc=%s: %s" % (args[0], r.returncode, r.stderr.strip()[:200]))
    return r.stdout


def git_bytes(root, spec):
    r = subprocess.run(["git", "-C", str(root), "show", spec], capture_output=True, timeout=60)
    need(r.returncode == 0, "git show %s failed" % spec)
    return r.stdout


def builder_name(root):
    spec = importlib.util.spec_from_file_location("opal_naming_p123", str(Path(root) / "lib" / "opal_naming.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.name("irpt", "cottonwood", "account-dim", "lambda")


def ac_1_1(root):
    root = Path(root)
    key = builder_name(root)
    need(key == "irpt-cot-account-dim-lambda", "builder name unexpected: " + key)
    now = json.loads((root / SM).read_text(encoding="utf-8"))["functions"]
    old = json.loads(git(root, "show", "%s:%s" % (BASE, SM)))["functions"]
    need(key in now, "source-map entry absent: " + key)
    need(set(now) - set(old) == {key}, "functions added are not exactly the one new entry")
    need(all(now[k] == old[k] for k in old), "an existing function entry changed")
    e, h = now[key], now[HOLD_KEY]
    need(e["source_dir"] == SRC_DIR, "source_dir wrong")
    need(set(e["files"]) == EXPECT_FILES and len(e["files"]) == len(EXPECT_FILES), "files are not exactly the expected set")
    staged = {s["repo_path"]: s for s in e["staged_from"]}
    need(set(staged) == EXPECT_FILES - {"lambda_function.py"} and len(e["staged_from"]) == len(staged), "staged_from members wrong")
    for rp, s in staged.items():
        need(s["packaged_as"] == rp, "packaged_as differs from repo_path: " + rp)
        blob = git_bytes(root, "%s:%s" % (s["pin"], rp))
        need(hashlib.sha256(blob).hexdigest() == s["sha256"], "sha256 does not match the pinned blob: " + rp)
    for rp in SHARED:
        hs = {s["repo_path"]: s for s in h["staged_from"]}[rp]
        need((staged[rp]["pin"], staged[rp]["sha256"]) == (hs["pin"], hs["sha256"]), "shared member drifted from the holdings entry: " + rp)
    need(staged[ADAPTER]["sha256"] == hashlib.sha256((root / ADAPTER).read_bytes()).hexdigest(), "adapter pin is not the working bytes")
    need((root / SRC_DIR / "lambda_function.py").is_file(), "lambda_function.py absent in source_dir")
    need(e["tf_file"] == TF_ROOT + "/lambda.tf" and e["tf_resource"] == "module.irpt_account_dim.aws_lambda_function.this" and e["iam_role"] == "irpt-cot-account-dim-role" and e["pipeline"] == "investor-reporting",
         "tf_file, iam_role or pipeline wrong")
    need(not any(k in e for k in ("artifact_s3_key", "artifact_sha256", "last_deployed_commit", "last_deployed_at", "deployed_code_sha256")), "a deploy field or artifact_s3_key is present: nothing is built, and the key stays out until the CVO rules (CTO msg 8187)")


def pytest(root, args, env_extra=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + args, cwd=str(root), capture_output=True,
                       text=True, timeout=110, env=env)
    return r.returncode, (r.stdout + r.stderr)[-500:]


def ac_1_2(root):
    p = Path(root) / PKG_TEST
    need(p.is_file(), "package test file absent")
    need(re.search(r"^def %s\(" % PKG_TEST_NAME, p.read_text(encoding="utf-8"), re.M) is not None, "named test absent")
    rc, tail = pytest(root, [PKG_TEST])
    need(rc == 0, "package test failed with the staged pins: " + tail.replace("\n", " | ")[-300:])
    rc, tail = pytest(root, [PKG_TEST], {"ADCOT_SCOPES_PIN": OLD_SCOPES_PIN})
    need(rc != 0, "the planted control (old scopes pin) did not make the package test fail")


def tf_text(root):
    d = Path(root) / TF_ROOT
    for f in TF_FILES:
        need((d / f).is_file(), "terraform file absent: " + f)
    return "\n".join((d / f).read_text(encoding="utf-8") for f in TF_FILES)


def structure(text):
    need(re.search(r'key\s*=\s*"investor-reporting/account-dim/tfstate"', text) is not None, "backend state key wrong")
    for m in re.finditer(r'"(irpt-[a-z0-9-]+)"', text):
        need("irpt-performance-native" in m.group(1), "a typed irpt- name (names come from the opal_name module): " + m.group(1))
    need(len(re.findall(r'source\s*=\s*"\.\./\.\./modules/opal_name"', text)) >= 5, "fewer than five opal_name builder modules")
    blocks = [blk for blk in re.split(r'(?m)^module\s+"', text)[1:] if re.search(r'source\s*=\s*"\.\./\.\./modules/opal_name"', blk)]
    for blk in blocks:
        need(re.search(r'scope\s*=', blk) is not None, "an opal_name module without scope: " + blk.split('"')[0])
    for lab in re.findall(r'(?m)^(?:module|resource\s+"[a-z_]+"|data\s+"[a-z_]+")\s+"?([A-Za-z0-9_]+)"', text):
        need("cot" not in lab.split("_"), "a block label carries the firm token: " + lab)
    need(re.search(r'function\s*=\s*"account-dim"', text) is not None, "builder modules do not name the function account-dim")
    need(re.search(r'handler\s*=\s*"lambda_function\.lambda_handler"', text) is not None, "handler wrong")
    need(re.search(r'runtime\s*=\s*"python3\.12"', text) is not None, "runtime wrong")
    need(re.search(r'artifact_key\s*=\s*"investor-reporting/\$\{module\.[a-z0-9_]+\.name\}\.zip"', text) is not None, "artifact_key wrong")
    need(re.search(r'state\s*=\s*"DISABLED"', text) is not None and "ENABLED" not in text.replace("DISABLED", ""), "the schedule is not created DISABLED")
    need(re.search(r'schedule_expression_timezone\s*=\s*"America/New_York"', text) is not None, "schedule zone wrong")
    need(re.search(r'cron\([^)]*MON-FRI[^)]*\)', text) is not None, "schedule cadence is not trading weekdays")
    actions = set()
    for m in re.finditer(r'actions\s*=\s*\[([^\]]*)\]', text):
        actions |= set(re.findall(r'"([^"]+)"', m.group(1)))
    need(actions and actions <= ALLOWED_ACTIONS, "actions outside the closed set: " + ", ".join(sorted(actions - ALLOWED_ACTIONS)))
    need(re.search(r'resources\s*=\s*\[\s*"\*"', text) is None, "a wildcard resource")
    need("account_dim" in text, "the account_dim gold table is not named")
    low = text.lower()
    for tok in FOREIGN:
        need(tok not in low, "a foreign-firm token: " + tok)


def ac_2_1(root):
    text = tf_text(root)
    structure(text)
    muts = (text + '\nactions = ["s3:DeleteObject"]\n', text.replace('"DISABLED"', '"ENABLED"', 1))
    for i, m in enumerate(muts):
        need(m != text, "mutation %d could not be planted" % i)
        try:
            structure(m)
        except Fail:
            continue
        raise Fail("the structure check accepted planted mutation %d" % i)


def terraform(root, *args):
    exe = Path(root) / ".tools" / "terraform.exe"
    if not exe.is_file():  # a worker worktree has no gitignored binary: use the base checkout's (the repo's common git dir parent)
        common = Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())
        exe = common.parent / ".tools" / "terraform.exe"
    need(exe.is_file(), "terraform.exe absent")
    r = subprocess.run([str(exe), "-chdir=" + str(Path(root) / TF_ROOT)] + list(args), capture_output=True, text=True, timeout=600)
    return r.returncode, r.stdout + r.stderr


def ac_2_2(root):
    tf_text(root)
    rc, out = terraform(root, "fmt", "-check", "-recursive", "-no-color")
    need(rc == 0, "terraform fmt -check: " + out.replace("\n", " | ")[:300])
    if not (Path(root) / TF_ROOT / ".terraform").is_dir():
        rc, out = terraform(root, "init", "-backend=false", "-input=false", "-no-color")
        need(rc == 0, "terraform init -backend=false: " + out.replace("\n", " | ")[-300:])
    rc, out = terraform(root, "validate", "-no-color")
    need(rc == 0 and "valid" in out.lower(), "terraform validate: " + out.replace("\n", " | ")[:400])


ARMS = {"DBC123-1-AC1": ac_1_1, "DBC123-1-AC2": ac_1_2, "DBC123-2-AC1": ac_2_1, "DBC123-2-AC2": ac_2_2}


def main(argv):
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
