"""IRPT_BCKEND workstream ~PM round 11 (issuer 2.0.0_SA_COO~P2) -- the check of one DECLARE order: the host role's identity policy gains ONE sts:AssumeRole statement on the HMAC list stage role, in infra/aws/terraform/mdpf-pipeline/iam.tf, NOT applied (CTO msg 10234; IB-hm-8 finding).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBHM10  IB-hm-10  one name module and one statement added in iam.tf
    AC1  the iam.tf diff of the worker's commit (HEAD~1..HEAD) deletes nothing and adds exactly one opal_name module block for the stage role, one statement with Sid IrptHmacListStageAssumeRole, Action sts:AssumeRole, Resource built from that module's name, no wildcard, no Principal
    AC2  the added module's inputs are exactly system irpt, function hmac-list-stage, kind role and no scope, and lib/opal_naming.py name() for those inputs returns the recorded role name (re-run now)
    AC3  the worker's ONE commit touches only iam.tf and the order's paths
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

IAM = "infra/aws/terraform/mdpf-pipeline/iam.tf"
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~"
ROLE_NAME = "irpt-hmac-list-stage-role"
MOD = "irpt_hmac_list_stage_role_name"
SID = "IrptHmacListStageAssumeRole"
fail = P6.fail


def _diff():
    g = subprocess.run(["git", "diff", "-U0", "HEAD~1", "HEAD", "--", IAM], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if g.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % g.stderr.strip()[:200])
    added, removed = [], []
    for ln in g.stdout.splitlines():
        if ln.startswith("+++") or ln.startswith("---"):
            continue
        if ln.startswith("+"):
            added.append(ln[1:])
        elif ln.startswith("-"):
            removed.append(ln[1:])
    return added, removed


def ac1(_):
    added, removed = _diff()
    if not added:
        fail("the commit adds nothing to %s" % IAM)
    if removed:
        fail("the commit deletes or rewrites %d line(s) of %s; the change is additions only" % (len(removed), IAM))
    a = "\n".join(ln for ln in added if not ln.lstrip().startswith("#"))
    if len(re.findall(r'module\s+"%s"\s*\{' % MOD, a)) != 1:
        fail("need exactly one added module block named %s" % MOD)
    if len(re.findall(r'(?i)\bsid\s*=\s*"%s"' % SID, a)) != 1:
        fail("need exactly one added statement with Sid %s" % SID)
    if len(re.findall(r'(?i)\bsid\s*=', a)) != 1:
        fail("exactly one statement may be added, found %d Sid labels" % len(re.findall(r'(?i)\bsid\s*=', a)))
    if len(re.findall(r'sts:AssumeRole', a)) != 1:
        fail("the added text must carry sts:AssumeRole exactly once")
    if "module.%s.name" % MOD not in a:
        fail("the statement's Resource must be built from module.%s.name" % MOD)
    if '"*"' in a or re.search(r'(?i)\bprincipal', a):
        fail('the added text holds a wildcard "*" or a Principal')
    print("OK: additions only, one name module, one statement Sid %s, resource built from the module, no wildcard" % SID)


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
    added, _removed = _diff()
    a = "\n".join(added)
    m = re.search(r'module\s+"%s"\s*\{(.*?)\n\}' % MOD, a, re.S)
    if not m:
        fail("no added module block %s" % MOD)
    body = m.group(1)
    attrs = dict(re.findall(r'^\s*([a-z_]+)\s*=\s*"([^"]*)"', body, re.M))
    attrs.pop("source", None)
    if attrs != {"system": "irpt", "function": "hmac-list-stage", "kind": "role"}:
        fail("the module inputs must be exactly system irpt, function hmac-list-stage, kind role and no scope; found %s" % attrs)
    got = _naming().name("irpt", None, "hmac-list-stage", "role")
    if got != ROLE_NAME:
        fail("lib/opal_naming.py name() returns %r, recorded %r" % (got, ROLE_NAME))
    print("OK: the module inputs equal the builder inputs and name() returns %s" % got)


def ac3(_):
    g = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if g.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % g.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in g.stdout.split() if x.strip()]
    if IAM not in files:
        fail("the commit must contain %s; it contains %s" % (IAM, files))
    bad = [x for x in files if x != IAM and not x.startswith(DELIV) and "INVESTIGATION_v1.md" not in x and "TO-IB-hm-10" not in x]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    print("OK: one commit, iam.tf, nothing outside the order's paths")


CHECKS = {"IBHM10-AC1": ac1, "IBHM10-AC2": ac2, "IBHM10-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p253_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
