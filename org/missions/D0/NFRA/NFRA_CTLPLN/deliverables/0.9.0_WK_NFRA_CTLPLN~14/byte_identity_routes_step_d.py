"""CT-a-1 AMENDMENT 15 (step D): the module's rendered documents are byte-identical before and after the routes-host removal.

Renders modules/routes_policy twice with `terraform console` in a provider-less scratch root (no AWS call, nothing applied): once from the module and the three data files
as committed at --base (default: the trunk commit this pass was cut from), once from the working tree. Prints one line per output document with a sha256 prefix.
Usage: python byte_identity_routes_step_d.py [--base <rev>]    (run from anywhere inside the worktree)
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT_REL = "infra/aws/terraform/nfra-ctlpln-identity"
FILES = [ROOT_REL + "/modules", ROOT_REL + "/tests/reached_roles_census.json", ROOT_REL + "/tests/vendor_secrets_census.json", ROOT_REL + "/dell_respol_policy.json"]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=110, **kw)


def render(base_dir):
    base = Path(base_dir) / ROOT_REL
    tmp = Path(tempfile.mkdtemp(prefix="bi-"))
    try:
        (tmp / "main.tf").write_text('module "routes" {\n  source = "%s"\n  census = jsondecode(file("%s"))\n  vendor_census = jsondecode(file("%s"))\n  respol_data = jsondecode(file("%s"))\n}\n' % (
            (base / "modules/routes_policy").as_posix(), (base / "tests/reached_roles_census.json").as_posix(),
            (base / "tests/vendor_secrets_census.json").as_posix(), (base / "dell_respol_policy.json").as_posix()), encoding="utf-8", newline="\n")
        r = run(["terraform", "-chdir=%s" % tmp, "init", "-backend=false", "-input=false", "-no-color"])
        assert r.returncode == 0, r.stdout[-300:] + r.stderr[-300:]
        r = run(["terraform", "-chdir=%s" % tmp, "console", "-no-color"], input="jsonencode(module.routes)\n")
        assert r.returncode == 0, r.stdout[-300:] + r.stderr[-300:]
        return json.loads(json.loads(r.stdout.strip().splitlines()[-1]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    base_rev = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "c9d8210b3e"
    top = run(["git", "rev-parse", "--show-toplevel"]).stdout.strip()
    tmp = Path(tempfile.mkdtemp(prefix="bi-head-"))
    try:
        arc = subprocess.run(["git", "-C", top, "archive", base_rev, *FILES], capture_output=True, timeout=110)
        assert arc.returncode == 0, arc.stderr[-300:]
        subprocess.run(["tar", "-x", "-C", str(tmp)], input=arc.stdout, check=True, timeout=110)
        before = render(tmp)
        after = render(top)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    same = True
    for k in ("vendor_policy_json", "platform_policy_json", "respol_policy_json", "functions_policy_json", "hosts_policy_json"):
        h, n = before[k] or "", after[k] or ""
        same = same and h == n
        print("BYTES %-22s base sha256=%s now sha256=%s len=%d/%d %s" % (k, hashlib.sha256(h.encode()).hexdigest()[:16], hashlib.sha256(n.encode()).hexdigest()[:16], len(h), len(n),
                                                                        "IDENTICAL" if h == n else "DIFFERENT"))
    print("BYTE-IDENTITY base=%s whole_module_output_identical=%s keys=%d ok=%s" % (base_rev, before == after, len(after), same and before == after))
    return 0 if same and before == after else 1


if __name__ == "__main__":
    sys.exit(main())
