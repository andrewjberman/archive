"""ADVI_FIRMBKTS round 4 check for cells FB-g-33 and FB-g-34 (acts 4b and 4c's carrier of the ONE environment value: a Terraform
variable that is ABSENT by default, so the trunk's plan is byte-identical until the act passes it; the CTO's 4b/4c half),
issuer 2.0.0_SA_COO~B1.

--arms var --cell exec|partners [--root <tree>] [--base <ref>]  (4 arms)
  E1 the root declares `variable "platinum_mode"` with `type = string`, `default = ""` and a validation that admits exactly
     "", "legacy" and "canonical" (its error message names the three).
  E2 the Lambda's environment is the base's map UNCHANGED plus a conditional: when the variable is "" nothing is added; when
     set, exactly one key `BD_PLATINUM_MODE` = the variable. The base's keys and values are all kept, character for character.
  E3 DORMANT: every base line of the edited file is kept in order (comment lines excepted) and no other file of the root
     changes except the variable's own file when it is new.
  E4 `terraform fmt -check` reads clean on each changed file.
Plain ASCII output; the last line carries the arm count. READ-ONLY. Never edit this file.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

CELLS = {
    "exec": {"root": "infra/aws/terraform/exec-summary", "file": "main.tf", "vars": "variables.tf",
             "base_keys": ["DATA_BUCKET", "ANTHROPIC_SECRET_NAME", "MODEL", "LOG_LEVEL", "MAX_ADVISORS_HARD_CAP"]},
    "partners": {"root": "infra/aws/terraform/partners-api", "file": "lambdas.tf", "vars": "variables.tf",
                 "base_keys": ["USERS_TABLE"]},
}


def _git(root, *a):
    return subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def check(root, cell, base):
    c = CELLS[cell]
    d = c["root"]
    res = []
    vtext = ""
    for fn in sorted(os.listdir(os.path.join(root, *d.split("/")))):
        if fn.endswith(".tf"):
            t = open(os.path.join(root, *d.split("/"), fn), encoding="utf-8").read()
            if re.search(r'variable\s+"platinum_mode"', t):
                vtext += t
    m = re.search(r'variable\s+"platinum_mode"\s*\{(.*?)\n\}', vtext, re.S)
    blk = m.group(1) if m else ""
    ok1 = (m is not None and re.search(r'type\s*=\s*string', blk) is not None
           and re.search(r'default\s*=\s*""', blk) is not None and "validation" in blk
           and all(x in blk for x in ('""', '"legacy"', '"canonical"')))
    print("  E1 variable declared=%s default empty=%s validation=%s" % (
        m is not None, re.search(r'default\s*=\s*""', blk) is not None, "validation" in blk))
    res.append(("E1 the variable is declared, string, default empty, validated to the three values", ok1))

    new = open(os.path.join(root, *d.split("/"), c["file"]), encoding="utf-8").read()
    old = _git(root, "show", "%s:%s/%s" % (base, d, c["file"]))
    keys_kept = all(re.search(r'\b%s\b\s*=' % k, new) for k in c["base_keys"])
    merged = re.search(r'merge\(', new) is not None and "var.platinum_mode" in new and "BD_PLATINUM_MODE" in new
    cond = re.search(r'var\.platinum_mode\s*==\s*""\s*\?\s*\{\}\s*:\s*\{\s*BD_PLATINUM_MODE\s*=\s*var\.platinum_mode', new,
                     re.S) is not None
    # every base environment key/value text survives verbatim
    lines_old = [ln.strip() for ln in old.splitlines() if re.search(r'^\s*(%s)\s*=' % "|".join(c["base_keys"]), ln)]
    verbatim = all(any(lo == ln.strip() for ln in new.splitlines()) for lo in lines_old)
    ok2 = keys_kept and merged and cond and verbatim
    print("  E2 base keys kept=%s verbatim=%s merge=%s conditional=%s" % (keys_kept, verbatim, merged, cond))
    res.append(("E2 the environment is the base's map plus one conditional BD_PLATINUM_MODE", ok2))

    strip_o = [ln for ln in old.splitlines() if not ln.strip().startswith("#")]
    cur = [ln for ln in new.splitlines() if not ln.strip().startswith("#")]
    # a line that the edit REWRAPS (the environment block) is allowed: compare the multiset of non-env lines
    env_keys = set(c["base_keys"])
    # the environment block's own header and closing lines are rewrapped by the merge form: they are not compared
    header = re.compile(r'^\s*(environment_variables|variables)\s*=\s*(\{|merge\()|^\s*\}\s*,?\s*$|^\s*\}\)\s*$')

    def skip(ln):
        return any(re.search(r'\b%s\b' % k, ln) for k in env_keys) or header.search(ln) is not None
    keep_o = [ln for ln in strip_o if not skip(ln)]
    keep_n = [ln for ln in cur if not skip(ln)]
    i = 0
    for ln in keep_n:
        if i < len(keep_o) and ln == keep_o[i]:
            i += 1
    changed = _git(root, "diff", "--name-only", base, "HEAD", "--", d).split() + \
        _git(root, "diff", "--name-only", "HEAD", "--", d).split()
    allowed = {"%s/%s" % (d, c["file"]), "%s/%s" % (d, c["vars"])}
    others = sorted({x for x in changed if x not in allowed})
    print("  E3 base lines kept %d of %d (env block lines aside); other files changed: %s" % (i, len(keep_o), others))
    res.append(("E3 dormant: base lines kept in order and no other file of the root changes",
                i >= len(keep_o) - 2 and not others))

    tf = shutil.which("terraform")
    files = [os.path.join(root, *d.split("/"), c["file"])]
    vf = os.path.join(root, *d.split("/"), c["vars"])
    if os.path.isfile(vf):
        files.append(vf)
    rc = 0
    for f in files:
        rc |= subprocess.run([tf, "fmt", "-check", f], capture_output=True, text=True, timeout=60).returncode if tf else 1
    print("  E4 fmt rc=%d" % rc)
    res.append(("E4 terraform fmt reads clean on the changed files", rc == 0))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("var",), required=True)
    ap.add_argument("--cell", choices=("exec", "partners"), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base", default="HEAD~1")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = check(root, a.cell, a.base)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:200]))
        res = [("the root readable", False)]
    for n, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", n))
    k = sum(1 for _, ok in res if ok)
    print("ROUND 4 MODE ENV: %d of 4 arms" % k)
    sys.exit(0 if k == 4 else 1)


if __name__ == "__main__":
    main()
