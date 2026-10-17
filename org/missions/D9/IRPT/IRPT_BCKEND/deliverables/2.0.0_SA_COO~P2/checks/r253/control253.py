"""Positive control and negatives for p253_cells.py (run by the issuer at the cut). Usage: python control253.py <real_repo_root>

Synthetic git repos: a base commit holding a stub iam.tf, then ONE worker commit; a stub lib/opal_naming.py so each arm can be made to fail.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r253/p253_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p253_cells as P  # noqa: E402

STUB = '''def name(system, scope, function, kind, qualifier=None, fifo=False):
    return "%s-%s-%s" % (system, function, kind)
'''
BASE_IAM = '''resource "aws_iam_role_policy" "mdpf_runner" {
  policy = jsonencode({
    Statement = [
      {
        Sid      = "IrptDirectory49fAssumeSourcePrincipal"
        Effect   = "Allow"
        Action   = "sts:AssumeRole"
        Resource = "arn:aws:iam::${local.account_id}:role/${module.irpt_49f_directory_read_role_name.name}"
      },
    ]
  })
}

module "irpt_49f_directory_read_role_name" {
  source   = "../modules/opal_name"
  system   = "irpt"
  scope    = "49financial"
  function = "directory-read"
  kind     = "role"
}
'''
STATEMENT = '''      {
        Sid      = "IrptHmacListStageAssumeRole"
        Effect   = "Allow"
        Action   = "sts:AssumeRole"
        Resource = "arn:aws:iam::${local.account_id}:role/${module.irpt_hmac_list_stage_role_name.name}"
      },
'''
MODULE = '''
module "irpt_hmac_list_stage_role_name" {
  source   = "../modules/opal_name"
  system   = "irpt"
  function = "hmac-list-stage"
  kind     = "role"
}
'''


def good(statement=STATEMENT, module=MODULE):
    marker = "    ]\n  })\n}\n"
    return BASE_IAM.replace(marker, statement + marker, 1) + module


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(iam=None, stub=STUB, extra=None, drop_iam=False):
    root = Path(tempfile.mkdtemp(prefix="c253_"))
    (root / "lib").mkdir()
    (root / "lib" / "opal_naming.py").write_text(stub, encoding="utf-8")
    (root / "infra/aws/terraform/mdpf-pipeline").mkdir(parents=True)
    (root / P.IAM).write_text(BASE_IAM, encoding="utf-8")
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    if not drop_iam:
        (root / P.IAM).write_text(good() if iam is None else iam, encoding="utf-8")
    d = root / (P.DELIV + "454/note.txt")
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
    expect("clean", "IBHM10-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

CASES = [
    ("no_name_module", "AC1", dict(iam=good(module=""))),
    ("no_statement", "AC1", dict(iam=good(statement=""))),
    ("a_wildcard_resource", "AC1", dict(iam=good(statement=STATEMENT.replace('Resource = "arn:aws:iam::${local.account_id}:role/${module.irpt_hmac_list_stage_role_name.name}"', 'Resource = "*"')))),
    ("resource_not_from_module", "AC1", dict(iam=good(statement=STATEMENT.replace("${module.irpt_hmac_list_stage_role_name.name}", "irpt-hmac-list-stage-role")))),
    ("a_principal", "AC1", dict(iam=good(statement=STATEMENT.replace('Effect   = "Allow"', 'Effect   = "Allow"\n        Principal = "x"')))),
    ("two_statements", "AC1", dict(iam=good(statement=STATEMENT + STATEMENT.replace("IrptHmacListStageAssumeRole", "Second")))),
    ("a_line_rewritten", "AC1", dict(iam=good().replace('system   = "irpt"\n  scope', 'system   = "irpt "\n  scope'))),
    ("a_scope_on_the_module", "AC2", dict(iam=good(module=MODULE.replace('function = "hmac-list-stage"', 'scope    = "x"\n  function = "hmac-list-stage"')))),
    ("wrong_function", "AC2", dict(iam=good(module=MODULE.replace("hmac-list-stage", "hmac-stage")))),
    ("builder_returns_other_name", "AC2", dict(stub=STUB.replace('"%s-%s-%s" % (system, function, kind)', '"other"'))),
    ("iam_not_in_commit", "AC3", dict(drop_iam=True)),
    ("other_file_touched", "AC3", dict(extra=["lib/other_file.py"])),
]
for label, ac, kw in CASES:
    root = build(**kw)
    expect(label, "IBHM10-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c253_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBHM10-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
