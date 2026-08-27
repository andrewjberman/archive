"""ADVI_49F.P14-VEHICLE -- re-verification of the APPLIED entrypoint (1.0.0_SA_CTO 76738).

THIS SEAT'S NAMED STEP in ruling (i)'s execution sequence: after 0.4.0_DS_ClientPlatform~U builds
the a00 flag + local-emit + entrypoint token + three writers and PS-5 is deployed-verified,
0.7.0_AE_CloudOps~L re-runs the a00-only argv scope check and the AST auto-derive check.

SUBJECT = THE DEPLOYED BYTES, pulled from s3://opal-data-49financial/_code/ -- the object the SSM
document's `aws s3 sync` actually puts on the box. Not the working tree, not a report, not a
filename match (CLAUDE.md Rule 22a's CODE trap: running-bytes-older-than-built passes every rung).

WHAT THIS DOES *NOT* CLAIM. It verifies what the deployed bytes DO. It does NOT verify that those
bytes correspond to a committed source vintage -- that content-identity is the DS lane's deploy leg
(the LF-normalised compare against the build input, per the c02 precedent). Conflating the two would
be a claim this instrument cannot support.

WARN: WHY CHECK 3 IS AST-ONLY, BANKED BECAUSE IT BIT ME. The first run of check 3 substring-scanned the
whole file for 'epoch'/'converter' and returned FAIL on 5 hits -- every one a COMMENT or ARGPARSE
HELP STRING, including the help text that EXPLAINS the auto-derive ban. A common-noun scan over a
file that documents its own prohibition reads the documentation as the violation. Comments and
string literals are not executable; the check walks the AST and looks only at writes and compares.

EVERY CHECK CARRIES A NEGATIVE CONTROL. A check that has only ever returned PASS is
indistinguishable from a check that cannot fail.
"""
from __future__ import annotations

import ast
import sys

import boto3

BUCKET = "opal-data-49financial"
ENTRYPOINT_KEY = "_code/chain_49f_entrypoint.py"
A00_KEY = "_code/a00_runner.py"

# The entrypoint sends these to a00; a00 must accept every one or the run dies on ARGV rather than
# at the guard -- the failure mode the face names, wearing a vehicle defect's face.
A00_REQUIRED_OPTIONS = ["--date", "--upload", "--dry-run", "--local-out", "--declared-historical"]

s3 = boto3.client("s3")


def pull(key):
    o = s3.get_object(Bucket=BUCKET, Key=key)
    return o["Body"].read().decode("utf-8", errors="replace"), o["LastModified"]


def stage_argvs(source):
    """(stage_name, argv_source) for every stage in _stage_list's returned list."""
    tree = ast.parse(source)
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "_stage_list")
    ret = next(n for n in ast.walk(fn) if isinstance(n, ast.Return))
    return [(e.elts[0].value, ast.unparse(e.elts[1])) for e in ret.value.elts]


def carries(argv_src, token):
    return token in [x.strip() for x in argv_src.replace("+", " ").split()]


def flag_writes(source):
    """Every executable write to the flag identifier, and whether it derives from anything but
    the parameter. Comments/strings are invisible here by construction."""
    tree = ast.parse(source)
    problems, writes = [], []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Assign):
            continue
        for t in n.targets:
            nm = t.id if isinstance(t, ast.Name) else (
                ast.unparse(t) if isinstance(t, ast.Attribute) else None)
            if nm and ("declared_historical" in nm or nm == "dh"):
                val = ast.unparse(n.value)
                writes.append((n.lineno, nm, val))
                names = {x.id for x in ast.walk(ast.parse(val, mode="eval"))
                         if isinstance(x, ast.Name)}
                if names - {"declared_historical"}:
                    problems.append(f"line {n.lineno}: {nm} = {val} <- derives from {sorted(names)}")
    for n in ast.walk(tree):
        if isinstance(n, ast.Compare):
            for c in ast.walk(n):
                if (isinstance(c, ast.Constant) and isinstance(c.value, str)
                        and len(c.value) == 10 and c.value[4] == "-" and c.value[7] == "-"):
                    problems.append(f"line {n.lineno}: date-literal compare {ast.unparse(n)}")
    return writes, problems


def accepted_options(source):
    opts = []
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "add_argument":
            for a in n.args:
                if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.startswith("-"):
                    opts.append(a.value)
    return opts


def main():
    print("=" * 78)
    print("APPLIED-ENTRYPOINT RE-VERIFICATION -- ADVI_49F.P14-VEHICLE (CTO 76738)")
    print("=" * 78)

    ep_src, ep_lm = pull(ENTRYPOINT_KEY)
    a00_src, a00_lm = pull(A00_KEY)
    print(f"  subject {ENTRYPOINT_KEY}  LastModified {ep_lm.isoformat()}  {len(ep_src)} chars")
    print(f"  subject {A00_KEY}         LastModified {a00_lm.isoformat()}  {len(a00_src)} chars")

    stages = stage_argvs(ep_src)
    results = {}

    # ---- CHECK 1 -------------------------------------------------------------
    print("\nCHECK 1 -- a00-ONLY ARGV SCOPE for the declared-historical flag")
    print(f"  stages enumerated (DENOMINATOR): {len(stages)}")
    carriers = [n for n, a in stages if carries(a, "dh")]
    print(f"  stages carrying `dh`: {carriers}")
    c1 = carriers == ["a00_dim_account"]
    print(f"  VERDICT: {'PASS' if c1 else '*** FAIL ***'}")
    mut = ep_src.replace(
        '("a01_dim_relationship",   [sys.executable, "a01_dim_relationship.py", "--date", date] + u)',
        '("a01_dim_relationship",   [sys.executable, "a01_dim_relationship.py", "--date", date] + u + dh)')
    mcar = [n for n, a in stage_argvs(mut) if carries(a, "dh")]
    ctl1 = mcar != ["a00_dim_account"]
    print(f"  NEGATIVE CONTROL (plant dh on a01): carriers={mcar} -> "
          f"{'FIRED' if ctl1 else '*** CONTROL DEAD ***'}")
    results["CHECK1"] = c1 and ctl1

    # ---- CHECK 2 -------------------------------------------------------------
    print("\nCHECK 2 -- MIRROR MEMBERSHIP (ruling (i): a00 joins the mirror like every other stage)")
    a00_argv = dict(stages)["a00_dim_account"]
    print(f"  a00 argv: {a00_argv}")
    c2 = carries(a00_argv, "m")
    print(f"  VERDICT: {'PASS' if c2 else '*** FAIL ***'} (a00 carries `m` / --local-out)")
    ctl2 = not carries(a00_argv.replace("+ m ", "+ "), "m")
    print(f"  NEGATIVE CONTROL (strip m): -> {'FIRED' if ctl2 else '*** CONTROL DEAD ***'}")
    results["CHECK2"] = c2 and ctl2

    # ---- CHECK 3 -------------------------------------------------------------
    print("\nCHECK 3 -- NO AUTO-DERIVE of the flag in the entrypoint (BANNED, CTO 76528)")
    writes, problems = flag_writes(ep_src)
    print(f"  executable writes to the flag identifier: {len(writes)}")
    for lineno, nm, val in writes:
        print(f"    line {lineno}: {nm} = {val}")
    print(f"  problems: {len(problems)}")
    for p in problems:
        print(f"    - {p}")
    c3 = not problems
    print(f"  VERDICT: {'PASS' if c3 else '*** FAIL ***'}")
    _, pA = flag_writes(ep_src.replace(
        '    dh = ["--declared-historical"] if declared_historical else []',
        '    dh = ["--declared-historical"] if date < "2026-07-14" else []'))
    _, pB = flag_writes(ep_src.replace(
        '    u = ["--upload"] if upload else ["--dry-run"]',
        '    declared_historical = _measure_epoch() > date\n'
        '    u = ["--upload"] if upload else ["--dry-run"]'))
    ctl3 = bool(pA) and bool(pB)
    print(f"  NEGATIVE CONTROL A (epoch-literal compare): {len(pA)} problem(s)")
    print(f"  NEGATIVE CONTROL B (computed-epoch reassign): {len(pB)} problem(s)")
    print(f"  -> {'BOTH FIRED' if ctl3 else '*** A CONTROL DID NOT FIRE ***'}")
    results["CHECK3"] = c3 and ctl3

    # ---- CHECK 4 -------------------------------------------------------------
    print("\nCHECK 4 -- ARGV SURFACE AGREEMENT (a rejected flag dies on argv, not at the guard)")
    opts = accepted_options(a00_src)
    print(f"  a00_runner accepted options (DENOMINATOR {len(opts)}): {opts}")
    missing = [k for k in A00_REQUIRED_OPTIONS if k not in opts]
    for k in A00_REQUIRED_OPTIONS:
        print(f"    {k:24s} {'ACCEPTED' if k in opts else '*** NOT ACCEPTED -- ARGV DEATH ***'}")
    c4 = not missing
    print(f"  VERDICT: {'PASS' if c4 else '*** FAIL ***'}")
    ctl4 = "--no-such-option-9999" not in opts
    print(f"  NEGATIVE CONTROL (a bogus option must NOT read as accepted): "
          f"{'FIRED' if ctl4 else '*** CONTROL DEAD ***'}")
    results["CHECK4"] = c4 and ctl4

    print("\n" + "=" * 78)
    for k in sorted(results):
        print(f"  {k}: {'PASS' if results[k] else 'FAIL'}")
    allok = all(results.values())
    print(f"  OVERALL: {'PASS -- every check green AND every negative control fired' if allok else 'FAIL'}")
    print("=" * 78)
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
