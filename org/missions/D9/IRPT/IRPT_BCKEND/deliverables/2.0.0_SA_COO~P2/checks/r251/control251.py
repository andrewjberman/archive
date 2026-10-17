"""Positive control and negatives for p251_cells.py (run by the issuer at the cut). Usage: python control251.py <real_repo_root>

Synthetic git repos: a base commit, then ONE worker commit; a stub lib/opal_naming.py and firm registry so each arm can be made to fail.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r251/p251_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p251_cells as P  # noqa: E402

STUB = '''def address(source, scope, tier, table, partition, object=None):
    return "s3://opal-data-assets/%s/%s/%s/%s/%s" % (source, scope, tier, table, partition)
'''
REG = '{"firms": [{"firm_id": "alpha", "kind": "client"}, {"firm_id": "bravo", "kind": "client"}, {"firm_id": "charlie", "kind": "client"}, {"firm_id": "t", "kind": "test"}]}'

TF_OK = '''# header
module "irpt_hmac_list_stage_role_name" {
  source   = "../../modules/opal_name"
  system   = "irpt"
  function = "hmac-list-stage"
  kind     = "role"
}

module "irpt_hmac_list_stage_policy_name" {
  source   = "../../modules/opal_name"
  system   = "irpt"
  function = "hmac-list-stage"
  kind     = "policy"
}

locals {
  irpt_hmac_secret_name = "irpt/hmac-list/key"
  irpt_hmac_firms = [for long, short in module.irpt_scopes.scope_short : long if module.irpt_scopes.scope_class[long] == "FIRM"]
  irpt_hmac_keys = { for f in local.irpt_hmac_firms : f => "s3://opal-data-assets/globgrph/${f}/silver/account_id_list/hmac" }
}

resource "aws_secretsmanager_secret" "irpt_hmac_list_key" {
  name = local.irpt_hmac_secret_name
}

resource "aws_iam_role" "irpt_hmac_list_stage" {
  name               = module.irpt_hmac_list_stage_role_name.name
  assume_role_policy = jsonencode({ Statement = [{ Effect = "Allow", Action = "sts:AssumeRole", Principal = { AWS = local.irpt_runner_role_arn } }] })
}

resource "aws_iam_role_policy" "irpt_hmac_list_stage" {
  name = module.irpt_hmac_list_stage_policy_name.name
  role = aws_iam_role.irpt_hmac_list_stage.id
  policy = jsonencode({ Statement = [
    { Sid = "ReadTheOneHmacSecretOnly", Effect = "Allow", Action = ["secretsmanager:GetSecretValue"], Resource = [aws_secretsmanager_secret.irpt_hmac_list_key.arn] },
    { Sid = "PutTheThreeFirmListKeysOnly", Effect = "Allow", Action = ["s3:PutObject"], Resource = [for k, v in local.irpt_hmac_keys : replace(v, "s3://", "arn:aws:s3:::")] },
  ] })
}
'''
SCHED_OK = '    IRPT_HMAC_SECRET_ID = x\n    IRPT_HMAC_ROLE_ARN = y\n    IRPT_HMAC_LIST_URI_MAP = z\n'


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(tf=TF_OK, sched=SCHED_OK, stub=STUB, extra=None, drop_tf=False, drop_sched=False, extra_tf_file=None):
    root = Path(tempfile.mkdtemp(prefix="c251_"))
    (root / "lib").mkdir()
    (root / "lib" / "opal_naming.py").write_text(stub, encoding="utf-8")
    (root / "data").mkdir()
    (root / "data" / "firm_registry.json").write_text(REG, encoding="utf-8")
    (root / P.ROOTDIR).mkdir(parents=True)
    (root / P.SCHED).write_text("# schedule base\n", encoding="utf-8")
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    if not drop_tf:
        (root / P.TF).write_text(tf, encoding="utf-8")
    if not drop_sched:
        (root / P.SCHED).write_text("# schedule base\n" + sched, encoding="utf-8")
    if extra_tf_file:
        (root / P.ROOTDIR / "other.tf").write_text(extra_tf_file, encoding="utf-8")
    d = root / (P.DELIV + "note.txt")
    d.parent.mkdir(parents=True, exist_ok=True)
    d.write_text("n\n", encoding="utf-8")
    for e in extra or []:
        (root / e).parent.mkdir(parents=True, exist_ok=True)
        (root / e).write_text("x\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "worker")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-32s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IBHM8-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

CASES = [
    ("role_module_missing", "AC1", dict(tf=TF_OK.replace('kind     = "role"', 'kind     = "queue"'))),
    ("no_secret_container", "AC1", dict(tf=TF_OK.replace('resource "aws_secretsmanager_secret" "irpt_hmac_list_key"', 'resource "aws_s3_bucket" "irpt_hmac_list_key"'))),
    ("a_secret_version_present", "AC1", dict(extra_tf_file='resource "aws_secretsmanager_secret_version" "v" {}\n')),
    ("trust_not_the_host_role", "AC1", dict(tf=TF_OK.replace("local.irpt_runner_role_arn", "local.some_other_arn"))),
    ("a_service_principal", "AC1", dict(tf=TF_OK + '\n# x\nlocals { svc = "ec2.amazonaws.com" }\n')),
    ("a_wildcard", "AC1", dict(tf=TF_OK.replace("Allow", 'Allow", Principal2 = "*') if False else TF_OK + '\nlocals { w = "*" }\n')),
    ("a_third_statement", "AC1", dict(tf=TF_OK.replace("  ] })\n}\n", '    { Sid = "Extra", Effect = "Allow", Action = ["s3:PutObject"], Resource = ["x"] },\n  ] })\n}\n'))),
    ("an_extra_action", "AC1", dict(tf=TF_OK.replace('Action = ["s3:PutObject"]', 'Action = ["s3:PutObject", "s3:GetObject"]'))),
    ("an_env_key_missing", "AC1", dict(sched="    IRPT_HMAC_SECRET_ID = x\n    IRPT_HMAC_ROLE_ARN = y\n")),
    ("a_uri_differs_from_builder", "AC2", dict(tf=TF_OK.replace("account_id_list/hmac", "account_id_list/other"))),
    ("a_firm_token_typed", "AC2", dict(tf=TF_OK + '\nlocals { typed = "alpha" }\n')),
    ("a_second_assume_role", "AC1", dict(tf=TF_OK.replace('Action = ["s3:PutObject"]', 'Action = ["s3:PutObject", "sts:AssumeRole"]'))),
    ("tf_not_in_commit", "AC3", dict(drop_tf=True)),
    ("schedule_not_in_commit", "AC3", dict(drop_sched=True)),
    ("other_file_touched", "AC3", dict(extra=["lib/other_file.py"])),
]
for label, ac, kw in CASES:
    root = build(**kw)
    expect(label, "IBHM8-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c251_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBHM8-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
