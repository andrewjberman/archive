"""NFRA_OPLGTW TO-OG-z-4 probe -- OGZ4-AC3 (mutant control) and OGZ4-AC5 (docstring/code agreement).

Usage: `<python> og_z4.py AC3|AC5`. Prints its measurement with its denominator, then exactly one line:
`VERDICT: PASS-OGZ4-AC<n>` or `VERDICT: FAIL-OGZ4-AC<n> <reason>`.

AC3 (mutant control, the same depth-mirrored-scratch-copy shape TO-OG-q-5's own og_q5.py AC4 uses, to
avoid that same probe's own conftest.py-depth defect -- tests/acceptance/conftest.py's `parents[3]` and
app/integrations/schwab/catalog.py's `parents[7]` repository-layout derivations both need the copy at the
real relative depth `<scratch_root>/infra/aws/ec2/opal-gateway`): copies the whole `infra/aws/ec2/opal-
gateway` tree into a scratch root, MUTATES the scratch copy's `app/tools.py` by removing the
`isError=True` flag-setting line this cell adds (restoring the pre-fix `return denial` shape), then runs
OGZ4-AC1 and OGZ4-AC2 against that MUTATED copy. Passes only if AC1 FAILS there (the flag no longer set)
while AC2 still PASSES (a permitted call was never touched by the mutation) -- both outcomes printed. Ends
by asserting `git status --porcelain` before and after are equal (no tracked file left modified).

AC5: reads `app/tools.py` at this HEAD (the real worktree copy, not the mutant), extracts
`_PolicyGuardedMCP`'s own docstring and `call_tool`'s source, prints the docstring's denial sentence and
the lines that build the returned denial result, and passes only if the docstring's "a terminal tool
error" claim and the code AGREE: either the docstring makes that claim AND the denial branch sets the MCP
protocol's `isError` flag True, or the docstring no longer makes that claim.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

_TOOLS_REL = "infra/aws/ec2/opal-gateway/app/tools.py"


def _ws_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(Path(__file__).resolve().parent),
                         capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


def _git_status_porcelain(ws: Path) -> str:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=str(ws), capture_output=True, text=True, check=True)
    return out.stdout


def _run_pytest(python: str, cwd: Path, nodeid: str, extra_env: dict = None,
                timeout: int = 180) -> subprocess.CompletedProcess:
    import os
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    return subprocess.run([python, "-m", "pytest", nodeid, "-q", "-p", "no:cacheprovider", "--color=no"],
                          cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)


def _last_line(cp: subprocess.CompletedProcess) -> str:
    tail = cp.stdout.strip().splitlines()
    return tail[-1] if tail else "(no output)"


def _outcome(cp: subprocess.CompletedProcess) -> str:
    last = _last_line(cp)
    if cp.returncode == 0 and re.search(r"^1 passed", last):
        return "PASS"
    return "FAIL"


def ac3() -> int:
    ws = _ws_root()
    python = sys.executable
    before = _git_status_porcelain(ws)
    print("AC3: git status --porcelain BEFORE (%d line(s)):\n%s" % (len(before.splitlines()), before.rstrip()))

    scratch_root = ws / ".scratch" / ("og_z4_mutant_%d" % int(time.time()))
    if scratch_root.exists():
        shutil.rmtree(scratch_root)
    src_gateway = ws / "infra" / "aws" / "ec2" / "opal-gateway"
    # Mirror the real relative depth (repo_root/infra/aws/ec2/opal-gateway) -- og_q5.py's own AC4 probe
    # measured that a shallower scratch nesting breaks tests/acceptance/conftest.py's parents[3] and
    # catalog.py's parents[7] repository-layout derivations at import time (NFRA_OPLGTW-W5-S12).
    dst_gateway = scratch_root / "infra" / "aws" / "ec2" / "opal-gateway"
    shutil.copytree(src_gateway, dst_gateway, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    real_contract_src = ws / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    mirrored_contract = scratch_root / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    mirrored_contract.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(real_contract_src, mirrored_contract)
    print("AC3: copied %s -> %s; mirrored contract %s -> %s" % (src_gateway, dst_gateway, real_contract_src,
                                                                 mirrored_contract))

    tools_path = dst_gateway / "app" / "tools.py"
    tools_text = tools_path.read_text(encoding="utf-8")
    marker = (
        "            return CallToolResult(\n"
        "                content=[TextContent(type=\"text\", text=json.dumps(denial, indent=2))],\n"
        "                structuredContent=denial,\n"
        "                isError=True,\n"
        "            )\n"
    )
    flag_line_present = marker in tools_text
    print("AC3: the scratch copy's app/tools.py carries the isError=True flag-setting return before "
         "mutation: %s" % flag_line_present)
    if flag_line_present:
        mutated_text = tools_text.replace(marker, "            return denial\n", 1)
        tools_path.write_text(mutated_text, encoding="utf-8")
        print("AC3: mutated -- the denial branch now returns the plain dict again (the pre-fix shape), so "
             "the MCP low-level server's `dict` branch renders isError=False unconditionally.")

    mutant_env = {"NFRA_OPLGTW_CONTRACT_PATH": str(real_contract_src)}
    outcomes = {}
    for name, ac_id in (("AC1", "test_ogz4_ac01"), ("AC2", "test_ogz4_ac02")):
        test_path = dst_gateway / "tests" / "test_schwab_denial_envelope.py"
        cp = _run_pytest(python, dst_gateway, "%s::%s" % (test_path, ac_id), extra_env=mutant_env)
        outcomes[name] = _outcome(cp)
        print("AC3: run %s (%s) against the MUTATED scratch copy -> rc=%d last-line=%r outcome=%s"
             % (name, ac_id, cp.returncode, _last_line(cp), outcomes[name]))

    after = _git_status_porcelain(ws)
    print("AC3: git status --porcelain AFTER (%d line(s)):\n%s" % (len(after.splitlines()), after.rstrip()))
    porcelain_equal = before == after
    print("AC3: porcelain before == after: %s" % porcelain_equal)

    # The criterion's own bar: AC1 must FAIL on the mutant (the flag no longer set) while AC2 still PASSES
    # (a permitted call's flag was never touched by removing the denial branch's isError line).
    discriminates = outcomes.get("AC1") == "FAIL" and outcomes.get("AC2") == "PASS"
    if flag_line_present and discriminates and porcelain_equal:
        print("VERDICT: PASS-OGZ4-AC3")
        return 0
    print("VERDICT: FAIL-OGZ4-AC3 flag_line_present=%s outcomes=%s porcelain_equal=%s"
         % (flag_line_present, outcomes, porcelain_equal))
    return 1


def ac5() -> int:
    ws = _ws_root()
    sys.path.insert(0, str((ws / "infra" / "aws" / "ec2" / "opal-gateway")))
    import importlib
    import inspect
    tools = importlib.import_module("app.tools")
    importlib.reload(tools)  # this HEAD's bytes on disk, not a stale cached import

    cls_doc = inspect.getdoc(tools._PolicyGuardedMCP) or ""
    call_tool_src = inspect.getsource(tools._PolicyGuardedMCP.call_tool)

    print("AC5: %s :: _PolicyGuardedMCP docstring (%d line(s)):" % (_TOOLS_REL, len(cls_doc.splitlines())))
    for line in cls_doc.splitlines():
        print("AC5:   %s" % line)

    claims_terminal_error = "terminal tool error" in cls_doc
    print("AC5: docstring claims 'a terminal tool error': %s" % claims_terminal_error)

    denial_branch_match = re.search(r"if denial:\n(.*?)\n        token = data_entitlement\.remember_allowed",
                                    call_tool_src, re.S)
    denial_branch = denial_branch_match.group(1) if denial_branch_match else ""
    print("AC5: call_tool's denial branch (%d line(s)):" % len(denial_branch.splitlines()))
    for line in denial_branch.splitlines():
        print("AC5:   %s" % line)

    sets_error_flag = bool(denial_branch) and "isError=True" in denial_branch
    print("AC5: the denial branch sets the MCP protocol's isError flag True: %s" % sets_error_flag)

    # Agreement: either the docstring's claim is TRUE of the code (sets the flag), or the docstring makes
    # no such claim at all -- disagreement is the ONLY failing case.
    agrees = (claims_terminal_error and sets_error_flag) or (not claims_terminal_error)
    print("AC5: docstring and code agree: %s" % agrees)
    if agrees:
        print("VERDICT: PASS-OGZ4-AC5")
        return 0
    print("VERDICT: FAIL-OGZ4-AC5 claims_terminal_error=%s sets_error_flag=%s"
         % (claims_terminal_error, sets_error_flag))
    return 1


def main() -> int:
    dispatch = {"AC3": ac3, "AC5": ac5}
    if len(sys.argv) != 2 or sys.argv[1] not in dispatch:
        print("usage: og_z4.py AC3|AC5")
        return 2
    return dispatch[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
