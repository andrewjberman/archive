"""OG-q-2 probes (NFRA_OPLGTW, TO-OG-q-2, worker 0.9.0_WK_NFRA_OPLGTW~5).

    python og_q2.py AC26
    python og_q2.py AC27
    python og_q2.py AC29

AC26 (re-cut on R-OG-11, discriminating): app/data_entitlement.py at HEAD must be byte-identical to its blob at
d88cd32d0c (OG-z-1's commit, which already classifies the five tools with schwab_get_access as None). Reads both
blob ids from git (never from this worker's account of what it changed) and compares them.

AC27: org/standards/NFRA_OPLGTW_CONTRACT.json carries the key tool_operations, whose keys are exactly the
contract's tools (denominator 5 printed) and whose values are each a member of operations or JSON null, with null
on schwab_get_access only; operations and disabled_operations equal their blobs at the cut base.

AC29 (mutant control): runs tests/test_schwab_query.py::test_ogq2_ac28 three times as a real pytest subprocess --
once unmutated (must PASS), once with one value of integrations.schwab.integration.TOOL_OPERATION changed in the
child process only (must FAIL), once with one value of data_entitlement.SCHWAB_TOOLS changed in the child process
only (must FAIL). Neither source file is written to disk; the mutation is injected via a sitecustomize-style
PYTHONPATH shim so the on-disk modules are untouched.

Exit 0 on PASS, 1 on FAIL, for each subcommand.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[8]
GATEWAY = ROOT / "infra" / "aws" / "ec2" / "opal-gateway"
TARGET = "infra/aws/ec2/opal-gateway/app/data_entitlement.py"
CONTRACT_PATH = ROOT / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
CONTRACT_REL = "org/standards/NFRA_OPLGTW_CONTRACT.json"
AC26_BASE = "d88cd32d0c"
CUT_BASE = "0fc7c71160"


def _git(*args):
    out = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, encoding="utf-8")
    return out.returncode, out.stdout.strip(), out.stderr.strip()


def ac26() -> int:
    rc_head, head_blob, err_head = _git("rev-parse", "HEAD:%s" % TARGET)
    rc_base, base_blob, err_base = _git("rev-parse", "%s:%s" % (AC26_BASE, TARGET))
    print("HEAD blob:      %s%s" % (head_blob, (" (git rc=%d: %s)" % (rc_head, err_head)) if rc_head else ""))
    print("%s blob: %s%s" % (AC26_BASE, base_blob, (" (git rc=%d: %s)" % (rc_base, err_base)) if rc_base else ""))
    if rc_head != 0 or rc_base != 0:
        print("VERDICT: FAIL-OGQ2-AC26 could not read one or both blobs from git")
        return 1
    if head_blob != base_blob:
        print("VERDICT: FAIL-OGQ2-AC26 HEAD blob %s differs from %s's blob %s"
              % (head_blob, AC26_BASE, base_blob))
        return 1
    print("VERDICT: PASS-OGQ2-AC26")
    return 0


def ac27() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    tools = contract.get("tools")
    operations = contract.get("operations")
    tool_operations = contract.get("tool_operations")
    reasons = []
    if not isinstance(tools, list):
        print("VERDICT: FAIL-OGQ2-AC27 contract has no tools list")
        return 1
    denom = len(tools)
    print("denominator: %d contract tools" % denom)
    if tool_operations is None:
        print("VERDICT: FAIL-OGQ2-AC27 contract carries no tool_operations key")
        return 1
    print("tool_operations: %s" % json.dumps(tool_operations, sort_keys=True))
    if set(tool_operations) != set(tools):
        reasons.append("tool_operations keys %s != contract tools %s" % (sorted(tool_operations), sorted(tools)))
    for tool, op in tool_operations.items():
        print("  %-26s -> %r" % (tool, op))
        if op is not None and op not in operations:
            reasons.append("tool_operations[%r] = %r is not a member of operations and not null" % (tool, op))
    null_tools = sorted(t for t, op in tool_operations.items() if op is None)
    if null_tools != ["schwab_get_access"]:
        reasons.append("null on %s, expected null on schwab_get_access only" % (null_tools,))
    # operations and disabled_operations equal their blobs at the cut base: compare via git diff on those two
    # JSON sub-trees the only faithful way available without a repo-wide parse -- read the base file, parse it,
    # and compare the two keys' values directly.
    rc_base, base_text, err_base = _git("show", "%s:%s" % (CUT_BASE, CONTRACT_REL))
    if rc_base != 0:
        reasons.append("could not read the contract at the cut base %s (%s)" % (CUT_BASE, err_base))
    else:
        base_contract = json.loads(base_text)
        for key in ("operations", "disabled_operations"):
            if contract.get(key) != base_contract.get(key):
                reasons.append("contract[%r] changed from the cut base %s" % (key, CUT_BASE))
            else:
                print("%s unchanged from cut base %s: %s" % (key, CUT_BASE, contract.get(key)))
    if reasons:
        print("VERDICT: FAIL-OGQ2-AC27 %s" % "; ".join(reasons))
        return 1
    print("VERDICT: PASS-OGQ2-AC27")
    return 0


_MUTATE_INTEGRATION = """
import app.integrations.schwab.integration as _integ
_keys = list(_integ.TOOL_OPERATION)
_integ.TOOL_OPERATION[_keys[0]] = "__mutated__"
"""

_MUTATE_ENTITLEMENT = """
import app.data_entitlement as _de
_keys = list(_de.SCHWAB_TOOLS)
_de.SCHWAB_TOOLS[_keys[0]] = "__mutated__"
"""

_CONFTEST_TEMPLATE = """
def pytest_configure(config):
%s
"""


def _run_ac28(mutation_body: str, tmpdir: Path) -> "tuple[int, str]":
    # Inject the mutation as a pytest plugin loaded via -p, so it runs (pytest_configure) before the target test
    # module executes, WITHOUT writing to any file this order grants for editing -- the plugin file itself lives
    # only in a throwaway temp directory.
    plugin_path = tmpdir / ("mutplug_%d.py" % abs(hash(mutation_body)))
    if mutation_body:
        indented = "\n".join(("    " + ln if ln.strip() else ln) for ln in mutation_body.strip("\n").splitlines())
        plugin_path.write_text(_CONFTEST_TEMPLATE % indented, encoding="utf-8")
    else:
        plugin_path.write_text("def pytest_configure(config):\n    pass\n", encoding="utf-8")
    args = [sys.executable, "-m", "pytest",
            "tests/test_schwab_query.py::test_ogq2_ac28",
            "-q", "-p", "no:cacheprovider", "--color=no", "-s",
            "-p", plugin_path.stem]
    import os
    full_env = dict(os.environ)
    full_env["PYTHONPATH"] = str(plugin_path.parent) + (os.pathsep + full_env["PYTHONPATH"]
                                                          if full_env.get("PYTHONPATH") else "")
    out = subprocess.run(args, cwd=str(GATEWAY), capture_output=True, text=True, env=full_env, timeout=120)
    return out.returncode, (out.stdout + out.stderr)


def ac29() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        rc_clean, text_clean = _run_ac28("", tmpdir)
        rc_integ, text_integ = _run_ac28(_MUTATE_INTEGRATION, tmpdir)
        rc_ent, text_ent = _run_ac28(_MUTATE_ENTITLEMENT, tmpdir)
    print("run 1 (unmutated):                        rc=%d, %s" % (rc_clean, _last_line(text_clean)))
    print("run 2 (TOOL_OPERATION mutated in child):   rc=%d, %s" % (rc_integ, _last_line(text_integ)))
    print("run 3 (SCHWAB_TOOLS mutated in child):     rc=%d, %s" % (rc_ent, _last_line(text_ent)))
    reasons = []
    if rc_clean != 0:
        reasons.append("the unmutated run did not pass (rc=%d)" % rc_clean)
    if rc_integ == 0:
        reasons.append("the TOOL_OPERATION-mutated run did not fail (rc=0)")
    if rc_ent == 0:
        reasons.append("the SCHWAB_TOOLS-mutated run did not fail (rc=0)")
    if reasons:
        print("VERDICT: FAIL-OGQ2-AC29 %s" % "; ".join(reasons))
        return 1
    print("VERDICT: PASS-OGQ2-AC29")
    return 0


def _last_line(text: str) -> str:
    lines = [ln for ln in text.strip().splitlines() if ln.strip()]
    return lines[-1] if lines else "<no output>"


def main(argv) -> int:
    if len(argv) < 2 or argv[1] not in ("AC26", "AC27", "AC29"):
        print("usage: og_q2.py AC26|AC27|AC29")
        return 2
    return {"AC26": ac26, "AC27": ac27, "AC29": ac29}[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
