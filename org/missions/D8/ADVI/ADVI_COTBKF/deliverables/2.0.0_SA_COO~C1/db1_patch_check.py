"""ADVI_COTBKF TO-CB-db-1 (issuer's check): is the proposed ssm.tf patch the one non-gating account_attributes step, and does Terraform plan it as ONE in-place change?

Takes the patch file the worker wrote (a unified diff of infra/aws/terraform/cot-pipeline/ssm.tf, path relative to the repo root). Read-only against AWS and git:
nothing is applied, and the shared tree is not edited (the patch is applied to a throwaway sibling copy that is deleted afterwards).
  python db1_patch_check.py shape <patch>
    PATCH-SHAPE files=<n> removed=<n> added=<n> table_line=<bool> nongating=<bool> before_finalize=<bool> applies=<bool>
  python db1_patch_check.py plan <patch>
    PATCH-PLAN add=<n> change=<n> destroy=<n> address=<resource address changed, or none>
Rules: shape reads the diff: files = distinct paths in '+++' lines (expect exactly infra/aws/terraform/cot-pipeline/ssm.tf); removed = '-' lines other than the header
(expect 0); added = '+' lines other than the header; table_line = an added line holds '--table account_attributes'; nongating = that line sits inside a brace group that
ends in '|| echo' and '; } &&' (the holdings step's shape); before_finalize = the added lines come before the '--finalize' line in the patched text; applies = 'git apply
--check' passes on HEAD. plan copies the *.tf files of the root to a sibling directory, applies the patch there, points TF_DATA_DIR at the initialised .terraform of the
real root, runs 'terraform plan -lock=false -input=false' and reads the 'Plan:' line and the one 'will be updated in-place' address.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()).resolve()
ROOT_REL = "infra/aws/terraform/cot-pipeline"
SSM_REL = ROOT_REL + "/ssm.tf"
TF = str(REPO / ".tools" / "terraform.exe")

mode, patch_rel = sys.argv[1], sys.argv[2]
patch = (REPO / patch_rel).read_text(encoding="utf-8")
lines = patch.splitlines()
added = [ln[1:] for ln in lines if ln.startswith("+") and not ln.startswith("+++")]
removed = [ln for ln in lines if ln.startswith("-") and not ln.startswith("---")]

if mode == "shape":
    files = {re.sub(r"^[ab]/", "", ln[4:].split("\t")[0].strip()) for ln in lines if ln.startswith("+++ ")}
    table = any("--table account_attributes" in a for a in added)
    block = "\n".join(added)
    nongating = bool(re.search(r"\{\s*python3\.11 /tmp/cot_silver_merge\.py --table account_attributes[^\n]*\|\| echo[^\n]*;\s*\}\s*&&", block))
    chk = subprocess.run(["git", "apply", "--check", str(REPO / patch_rel)], capture_output=True, text=True, cwd=str(REPO))
    before = False
    if chk.returncode == 0:
        tmp = REPO / (ROOT_REL + "_r105_shape_tmp")
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir()
        shutil.copy(REPO / SSM_REL, tmp / "ssm.tf")
        r = subprocess.run(["git", "apply", "--directory", tmp.relative_to(REPO).as_posix(), "-p5", str(REPO / patch_rel)],
                           capture_output=True, text=True, cwd=str(REPO))
        text = (tmp / "ssm.tf").read_text(encoding="utf-8") if r.returncode == 0 else ""
        shutil.rmtree(tmp, ignore_errors=True)
        i, j = text.find("cot_silver_merge.py --table account_attributes"), text.find("cot_silver_merge.py --finalize")
        before = 0 <= i < j
    print("PATCH-SHAPE files=%d removed=%d added=%d table_line=%s nongating=%s before_finalize=%s applies=%s"
          % (len(files), len(removed), len(added), table, nongating, before, chk.returncode == 0))
    raise SystemExit(0)

src = REPO / ROOT_REL
tmp = REPO / (ROOT_REL + "_r105_plan_tmp")
shutil.rmtree(tmp, ignore_errors=True)
try:
    tmp.mkdir()
    for f in src.glob("*.tf"):
        shutil.copy(f, tmp / f.name)
    for extra in (".terraform.lock.hcl",):
        if (src / extra).exists():
            shutil.copy(src / extra, tmp / extra)
    r = subprocess.run(["git", "apply", "--directory", tmp.relative_to(REPO).as_posix(), "-p5", str(REPO / patch_rel)], capture_output=True, text=True, cwd=str(REPO))
    if r.returncode != 0:
        print("PATCH-PLAN add=-1 change=-1 destroy=-1 address=patch-did-not-apply")
        raise SystemExit(0)
    env = dict(os.environ, TF_DATA_DIR=str(src / ".terraform"), TF_IN_AUTOMATION="1")
    out = subprocess.run([TF, "-chdir=" + str(tmp), "plan", "-lock=false", "-input=false", "-no-color"], capture_output=True, text=True, env=env).stdout
    m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", out)
    n = re.search(r"No changes", out)
    addr = re.findall(r"# (\S+) will be updated in-place", out)
    a, c, d = (m.groups() if m else (("0", "0", "0") if n else ("-1", "-1", "-1")))
    print("PATCH-PLAN add=%s change=%s destroy=%s address=%s" % (a, c, d, ",".join(addr) if addr else "none"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
