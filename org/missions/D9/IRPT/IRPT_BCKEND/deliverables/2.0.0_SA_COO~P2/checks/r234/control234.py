"""Positive control and negatives for p234_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control234.py <real_repo_root>
Builds temp git roots holding the real lib/opal_naming*.py and registry, a stub iam.tf at the base, a worker commit by slot 438, and a synthetic record;
runs every criterion expecting PASS, then each mutation expecting the NAMED criterion to FAIL. The temp roots are removed.
"""
import copy
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r234/p234_cells.py"
for sub in ("r196", "r200", "r234"):
    sys.path.insert(0, str(CHECK.parent.parent / sub))
import p234_cells as P  # noqa: E402

GOOD_TF = '''locals {
  scope_feed_registry = jsondecode(file("${path.module}/../../../logic/registry/scopes.json"))
  scope_feed_scope    = lookup(local.scope_feed_registry, "feed_scope")
}

resource "aws_iam_role_policy" "inf_gold_layer_scope_feed" {
  name = module.scope_feed_name.name
  role = aws_iam_role.inf_gold_layer.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Sid = "S1PutAndReadFeedKeysOnly", Effect = "Allow", Action = ["s3:PutObject", "s3:GetObject"], Resource = local.scope_feed_object_arns },
      { Sid = "S2ListFeedPrefixesOnly", Effect = "Allow", Action = ["s3:ListBucket"], Resource = [local.scope_feed_bucket_arn],
        Condition = { StringLike = { "s3:prefix" = local.scope_feed_list_prefixes } } }
    ]
  })
}
'''


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def expected(root):
    sys.path.insert(0, str(root / "lib"))
    for k in [k for k in sys.modules if k.startswith("opal_naming")]:
        del sys.modules[k]
    P6 = P.P6
    old = P6.ROOT
    P6.ROOT = root
    try:
        return P.expected_arns()
    finally:
        P6.ROOT = old
        sys.path.remove(str(root / "lib"))


def build(tf=GOOD_TF, mutate=None):
    root = Path(tempfile.mkdtemp(prefix="c234_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    (root / "lib").mkdir()
    for f in glob.glob(str(REAL / "lib" / "opal_naming*.py")) + [str(REAL / "lib" / "trading_calendar.py")]:
        shutil.copy(f, root / "lib" / Path(f).name)
    shutil.copytree(REAL / "infra/logic/registry", root / "infra/logic/registry")
    (root / "org/standards").mkdir(parents=True)
    shutil.copy(REAL / "org/standards/NAMING_SCHEMA.json", root / "org/standards/NAMING_SCHEMA.json")
    tf_path = root / P.TF
    tf_path.parent.mkdir(parents=True, exist_ok=True)
    tf_path.write_text("# stub\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    base = git(root, "rev-parse", "HEAD")
    tf_path.write_text(tf, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "worker", "--author", "0.9.0_WK_IRPT_BCKEND~%d <w@x>" % P.SLOT)
    rec = {"base_commit": base, "changed_paths": [P.TF], "naming_gate": {"commit_accepted": True, "refused": 0, "literals_graded": 6, "policy_name_source": "name()"},
           "evaluated_prefixes": expected(root), "evaluated_by": "registry reading",
           "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
           "notes": ["the policy name is the opal_name module output, graded by the gate at commit", "the prefixes were read from the registry by the same lookups the HCL makes"]}
    if mutate:
        rec = mutate(rec)
    f = root / P.REC
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(rec), encoding="utf-8")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


def rm(rec, *path, value=None):
    rec = copy.deepcopy(rec)
    cur = rec
    for k in path[:-1]:
        cur = cur[k]
    cur[path[-1]] = value
    return rec


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-28s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB234-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
TF_NEGS = [
    ("delete_action", GOOD_TF.replace('"s3:GetObject"]', '"s3:GetObject", "s3:DeleteObject"]')),
    ("kms_action", GOOD_TF.replace('"s3:GetObject"]', '"s3:GetObject", "kms:Decrypt"]')),
    ("typed_scope", GOOD_TF.replace("local.scope_feed_list_prefixes", '["orion/inflection/silver/x/*"]')),
    ("no_prefix_condition", GOOD_TF.replace('"s3:prefix"', '"s3:max-keys"')),
    ("one_statement", GOOD_TF.replace('Sid = "S2ListFeedPrefixesOnly"', 'Zid = "S2"')),
    ("no_registry_local", GOOD_TF.replace("logic/registry/", "logic/other/")),
    ("wrong_role", GOOD_TF.replace("aws_iam_role.inf_gold_layer.id", "aws_iam_role.other.id")),
]
for label, tf in TF_NEGS:
    root = build(tf)
    expect(label, "IB234-1-AC1", root, False)
    shutil.rmtree(root, ignore_errors=True)
REC_NEGS = [
    ("gate_not_accepted", lambda r: rm(r, "naming_gate", "commit_accepted", value=False)),
    ("gate_refused", lambda r: rm(r, "naming_gate", "refused", value=2)),
    ("prefix_differs", lambda r: rm(r, "evaluated_prefixes", value=["arn:aws:s3:::x/y/*"])),
    ("changed_paths_wrong", lambda r: rm(r, "changed_paths", value=[P.TF, "extra.tf"])),
    ("evaluated_by_missing", lambda r: rm(r, "evaluated_by", value="guess")),
]
for label, fn in REC_NEGS:
    root = build(mutate=fn)
    expect(label, "IB234-1-AC2", root, False)
    shutil.rmtree(root, ignore_errors=True)
for label, fn in (("counter_nonzero", lambda r: rm(r, "aws_writes_made", value=1)), ("short_notes", lambda r: rm(r, "notes", value=["a"]))):
    root = build(mutate=fn)
    expect(label, "IB234-1-AC3", root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c234_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_input", "IB234-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
