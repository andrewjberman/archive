"""IRPT_BCKEND workstream ~PM round 10 (issuer 2.0.0_SA_COO~P2) -- the check of one DECLARE order: the narrow HMAC list stage role, its policy, the secret container and the Lambda environment, in Terraform, NOT applied (CTO msgs 10203 and 10234).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBHM8  IB-hm-8  declared in hmac_list_stage.tf plus three additive environment keys in schedule.tf
    AC1  static markers: the two name modules, one secret container and NO secret version in the root, the role's trust names the host role local only, the policy has exactly the two statements and the two actions, no wildcard resource, the three environment keys
    AC2  the list-key URIs in the file equal what lib/opal_naming.py address() returns for the three firm tokens (re-run now)
    AC3  the worker's ONE commit (HEAD~1..HEAD) touches only the new .tf, schedule.tf and the order's paths, and both .tf files are in it
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

ROOTDIR = "infra/aws/terraform/investor-reporting/directory"
TF = ROOTDIR + "/hmac_list_stage.tf"
SCHED = ROOTDIR + "/schedule.tf"
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~454/"
ENV_KEYS = ("IRPT_HMAC_SECRET_ID", "IRPT_HMAC_ROLE_ARN", "IRPT_HMAC_LIST_URI_MAP")
SIDS = ("ReadTheOneHmacSecretOnly", "PutTheThreeFirmListKeysOnly")
ACTIONS = {"secretsmanager:GetSecretValue", "s3:PutObject"}
fail = P6.fail


def _text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def _code(rel):
    """The file with full-line comments removed."""
    return "\n".join(ln for ln in _text(rel).splitlines() if not ln.lstrip().startswith("#"))


def ac1(_):
    t = _code(TF)
    mods = re.findall(r'module\s+"[^"]+"\s*\{[^}]*\}', t, re.S)
    named = [m for m in mods if "../../modules/opal_name" in m and re.search(r'function\s*=\s*"hmac-list-stage"', m) and re.search(r'system\s*=\s*"irpt"', m)]
    kinds = sorted(re.search(r'kind\s*=\s*"([a-z]+)"', m).group(1) for m in named if re.search(r'kind\s*=\s*"([a-z]+)"', m))
    if kinds != ["policy", "role"]:
        fail("need exactly two opal_name modules (system irpt, function hmac-list-stage) of kind role and policy; found kinds %s" % kinds)
    if len(re.findall(r'resource\s+"aws_secretsmanager_secret"\s+"', t)) != 1:
        fail("need exactly one aws_secretsmanager_secret container")
    for f in sorted((P6.ROOT / ROOTDIR).glob("*.tf")):
        if "aws_secretsmanager_secret_version" in "\n".join(ln for ln in f.read_text(encoding="utf-8").splitlines() if not ln.lstrip().startswith("#")):
            fail("aws_secretsmanager_secret_version appears in %s: no secret value belongs in Terraform" % f.name)
    if len(re.findall(r'resource\s+"aws_iam_role"\s+"', t)) != 1 or len(re.findall(r'resource\s+"aws_iam_role_policy"\s+"', t)) != 1:
        fail("need exactly one aws_iam_role and one aws_iam_role_policy")
    if "local.irpt_runner_role_arn" not in t or re.search(r"(ec2|lambda|sts|events|scheduler)\.amazonaws\.com", t):
        fail("the trust must name local.irpt_runner_role_arn and no service principal")
    if '"*"' in t:
        fail('a wildcard "*" appears in the file (no wildcard resource, action or principal)')
    sids = re.findall(r'(?i)sid\s*=\s*"([^"]+)"', t) or re.findall(r'"Sid"\s*:\s*"([^"]+)"', t)
    if sorted(sids) != sorted(SIDS):
        fail("the policy statements must be exactly %s, found %s" % (list(SIDS), sids))
    acts = set(re.findall(r'"((?:secretsmanager|s3|sts|iam|kms|ec2|lambda|logs):[A-Za-z*]+)"', t))
    if t.count("sts:AssumeRole") > 1:
        fail("sts:AssumeRole may appear once only (the trust document)")
    if acts - {"sts:AssumeRole"} != ACTIONS:
        fail("the policy actions must be exactly %s, found %s" % (sorted(ACTIONS), sorted(acts - {"sts:AssumeRole"})))
    s = _text(SCHED)
    missing = [k for k in ENV_KEYS if k not in s]
    if missing:
        fail("schedule.tf lacks the environment keys: %s" % ", ".join(missing))
    print("OK: names, one secret container and no version, host-role trust only, two statements and two actions, no wildcard, three environment keys")


def _naming():
    f = P6.ROOT / "lib" / "opal_naming.py"
    if not f.is_file():
        fail("no lib/opal_naming.py")
    sys.path.insert(0, str(P6.ROOT / "lib"))
    spec = importlib.util.spec_from_file_location("opal_naming_under_test", str(f))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ac2(_):
    reg = json.loads(_text("data/firm_registry.json"))
    firms = [x["firm_id"] for x in (reg.get("firms") if isinstance(reg, dict) else reg) if x.get("kind") == "client"]
    if len(firms) != 3:
        fail("the firm registry must hold three client firms, read %d" % len(firms))
    mod = _naming()
    want = {mod.address("globgrph", f, "silver", "account_id_list", "hmac") for f in firms}
    t = _code(TF)
    typed = [f for f in firms if '"%s"' % f in t]
    if typed:
        fail("a firm token is typed as a literal in the file (derive firms from the registry): %s" % typed)
    got = set()
    for lit in re.findall(r'"(s3://opal-data-assets/[^"]+)"', t):
        if "${" in lit:
            for f in firms:
                got.add(re.sub(r"\$\{[^}]+\}", f, lit))
        else:
            got.add(lit)
    if got != want:
        fail("the list-key URIs in the file %s differ from the builder results %s" % (sorted(got), sorted(want)))
    print("OK: the three list-key URIs equal the builder results")


def ac3(_):
    g = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if g.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % g.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in g.stdout.split() if x.strip()]
    if TF not in files or SCHED not in files:
        fail("the commit must contain both %s and %s; it contains %s" % (TF, SCHED, files))
    bad = [x for x in files if x not in (TF, SCHED) and not x.startswith(DELIV) and "INVESTIGATION_v1.md" not in x and "TO-IB-hm-8" not in x]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    print("OK: one commit, the new .tf and schedule.tf, nothing outside the order's paths")


CHECKS = {"IBHM8-AC1": ac1, "IBHM8-AC2": ac2, "IBHM8-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p251_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
