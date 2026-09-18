"""NFRA_OPLGTW TO-OG-q-5 probe -- OGQ5-AC4 (mutant control), AC5 (the C3 census self-check) and AC6 (the
four named modules' failure counts).

Usage: `<python> og_q5.py AC4|AC5|AC6`. Prints its measurement with its denominator, then exactly one
line: `VERDICT: PASS-OGQ5-AC<n>` or `VERDICT: FAIL-OGQ5-AC<n> <reason>`.

AC4 (mutant control, ruling R-OG-13's standing bar, same shape as OG-q-4's own og_q4.py AC4): on the
re-hand, `app/integrations/schwab/integration.py`'s `SchwabService.query()` was granted for HALF ONE's call
site only (row NFRA_OPLGTW-W5-S13) and now calls `semantics.qualify_asset_plan()`. This probe builds the
depth-mirrored scratch copy (the same construction og_q4.py's AC4 uses, to avoid that same probe's own
conftest.py-depth defect), MUTATES it by neutering the `if q.dataset == sem.ASSET_DATASET:` branch that
wires HALF ONE (forcing it dead so `run_plan` stays the unqualified `plan`, exactly "the restriction's call
site removed"), then runs AC1/AC2/AC3 against that mutated copy and requires AC1 and AC2 to FAIL there
(the criterion's own bar; AC3's outcome is printed, not required either way).

AC5: re-reads org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/C3_CALL_PATH_CENSUS.md
and checks its own printed denominators are internally consistent: the sentence count, the rule count, and
the three verdict counts summing to the rule count.

AC6: tests/test_schwab_query.py, tests/test_schwab_semantics.py, tests/test_schwab_wiring.py and
tests/acceptance/test_local_acceptance.py, ONE pytest process per module (BOUNDS: "one module per pytest
process"), against the REAL worktree. Per this order's issuer context, test_ogv2_a18 in the acceptance
module is NOT this cell's to fix (its correction rides OG-v-2's re-hand, issuer row NFRA_OPLGTW-S26) and is
named, not counted against this cell, if it is the only acceptance-module failure; test_ogv2_a06 IS this
cell's own arm (HALF ONE) and its failure counts here exactly as measured.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

_MODULES = (
    "infra/aws/ec2/opal-gateway/tests/test_schwab_query.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_semantics.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_wiring.py",
    "infra/aws/ec2/opal-gateway/tests/acceptance/test_local_acceptance.py",
)
_A18_NODEID = "test_ogv2_a18"
_ASSET_POLICY_TESTS = ("test_ogq5_ac01", "test_ogq5_ac02", "test_ogq5_ac03")
_ASSET_POLICY_MODULE = "infra/aws/ec2/opal-gateway/tests/test_schwab_asset_policy.py"
_CENSUS_PATH = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/C3_CALL_PATH_CENSUS.md"


def _ws_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(Path(__file__).resolve().parent),
                         capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


def _git_status_porcelain(ws: Path) -> str:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=str(ws), capture_output=True, text=True, check=True)
    return out.stdout


def _run_pytest(python: str, ws: Path, nodeid: str, cwd: Path, extra_env: dict = None,
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


def ac4() -> int:
    ws = _ws_root()
    python = sys.executable
    before = _git_status_porcelain(ws)
    print("AC4: git status --porcelain BEFORE (%d line(s)):\n%s" % (len(before.splitlines()), before.rstrip()))

    scratch_root = ws / ".scratch" / ("og_q5_mutant_%d" % int(time.time()))
    if scratch_root.exists():
        shutil.rmtree(scratch_root)
    src_gateway = ws / "infra" / "aws" / "ec2" / "opal-gateway"
    # mirror the real relative depth (repo_root/infra/aws/ec2/opal-gateway) -- og_q4.py's probe measured
    # that a shallower scratch nesting breaks tests/acceptance/conftest.py's own hardcoded parents[3] and
    # catalog.py's parents[7] contract-path derivations at import time (NFRA_OPLGTW-W5-S12).
    dst_gateway = scratch_root / "infra" / "aws" / "ec2" / "opal-gateway"
    shutil.copytree(src_gateway, dst_gateway, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    real_contract_src = ws / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    mirrored_contract = scratch_root / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    mirrored_contract.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(real_contract_src, mirrored_contract)
    print("AC4: copied %s -> %s; mirrored contract %s -> %s" % (src_gateway, dst_gateway, real_contract_src,
                                                                mirrored_contract))

    # Mutate: neuter the branch that wires HALF ONE so `run_plan` never becomes the qualified plan --
    # exactly "the restriction's call site removed" for a query-time restriction that is applied by
    # branching to it, not by a single deletable line.
    integration_path = dst_gateway / "app" / "integrations" / "schwab" / "integration.py"
    integration_text = integration_path.read_text(encoding="utf-8")
    marker = "                    if q.dataset == sem.ASSET_DATASET:\n"
    call_site_present = marker in integration_text and "qualify_asset_plan" in integration_text
    print("AC4: app/integrations/schwab/integration.py in the scratch copy calls qualify_asset_plan before "
         "mutation: %s" % call_site_present)
    if call_site_present:
        mutated_text = integration_text.replace(
            marker, "                    if False and q.dataset == sem.ASSET_DATASET:  # AC4 mutant: "
                    "restriction call site removed\n", 1)
        integration_path.write_text(mutated_text, encoding="utf-8")
        print("AC4: mutated -- the HALF ONE branch is now dead code, so run_plan stays the unqualified plan.")

    mutant_env = {"NFRA_OPLGTW_CONTRACT_PATH": str(real_contract_src)}
    outcomes = {}
    for name, ac_id in (("AC1", "test_ogq5_ac01"), ("AC2", "test_ogq5_ac02"), ("AC3", "test_ogq5_ac03")):
        test_path = dst_gateway / "tests" / "test_schwab_asset_policy.py"
        cp = _run_pytest(python, ws, "%s::%s" % (test_path, ac_id), cwd=dst_gateway, extra_env=mutant_env)
        outcomes[name] = _outcome(cp)
        print("AC4: run %s (%s) against the MUTATED scratch copy -> rc=%d last-line=%r outcome=%s"
             % (name, ac_id, cp.returncode, _last_line(cp), outcomes[name]))

    after = _git_status_porcelain(ws)
    print("AC4: git status --porcelain AFTER (%d line(s)):\n%s" % (len(after.splitlines()), after.rstrip()))
    porcelain_equal = before == after
    print("AC4: porcelain before == after: %s" % porcelain_equal)

    # The criterion's own bar: AC1 and AC2 FAIL on the mutant (AC3's outcome is printed, not required).
    discriminates = outcomes.get("AC1") == "FAIL" and outcomes.get("AC2") == "FAIL"
    if call_site_present and discriminates and porcelain_equal:
        print("VERDICT: PASS-OGQ5-AC4")
        return 0
    print("VERDICT: FAIL-OGQ5-AC4 call_site_present=%s outcomes=%s porcelain_equal=%s"
         % (call_site_present, outcomes, porcelain_equal))
    return 1


def ac5() -> int:
    ws = _ws_root()
    text = (ws / _CENSUS_PATH).read_text(encoding="utf-8")

    def find_int(pattern: str) -> int:
        m = re.search(pattern, text)
        if not m:
            raise RuntimeError("census is missing the pattern %r" % pattern)
        return int(m.group(1))

    sentences = find_int(r"Sentences in PRD C3 \(v0\.9 @e09219470f\):\*\*\s*(\d+)")
    rules = find_int(r"Rules \(by subtraction:[^)]*\):\*\*\s*(\d+)")
    enforced = find_int(r"ENFORCED-ON-CALL-PATH:\*\*\s*(\d+)")
    not_enforced = find_int(r"NOT-ENFORCED:\*\*\s*(\d+)\s*\(R20")
    not_call_path = find_int(r"NOT-A-CALL-PATH-RULE:\*\*\s*(\d+)\s*\(R8")

    print("AC5: census denominators -- sentences=%d rules=%d ENFORCED=%d NOT-ENFORCED=%d "
         "NOT-A-CALL-PATH-RULE=%d" % (sentences, rules, enforced, not_enforced, not_call_path))
    verdict_sum = enforced + not_enforced + not_call_path
    print("AC5: verdict sum %d + %d + %d = %d (rule count %d)" % (enforced, not_enforced, not_call_path,
                                                                   verdict_sum, rules))

    row_ids = sorted(set(re.findall(r"^\*\*R(\d+) \[", text, re.M)), key=int)
    print("AC5: %d row id(s) found in the census body: R%s" % (len(row_ids), ", R".join(row_ids)))

    ok = (sentences > 0 and rules > 0 and verdict_sum == rules and len(row_ids) == rules
         and [int(r) for r in row_ids] == list(range(1, rules + 1)))
    if ok:
        print("VERDICT: PASS-OGQ5-AC5")
        return 0
    print("VERDICT: FAIL-OGQ5-AC5 sentences=%d rules=%d verdict_sum=%d row_ids=%d"
         % (sentences, rules, verdict_sum, len(row_ids)))
    return 1


def ac6() -> int:
    ws = _ws_root()
    python = sys.executable
    denom = len(_MODULES)
    results = []
    for module in _MODULES:
        cp = _run_pytest(python, ws, module, cwd=ws, timeout=300)
        last = _last_line(cp)
        m_pass = re.search(r"(\d+) passed", last)
        m_fail = re.search(r"(\d+) failed", last)
        passed = int(m_pass.group(1)) if m_pass else 0
        failed = int(m_fail.group(1)) if m_fail else (0 if cp.returncode == 0 else 1)
        results.append((module, passed, failed, last, cp.stdout))
        print("AC6: %s -> rc=%d last-line=%r passed=%d failed=%d" % (module, cp.returncode, last, passed, failed))

    # The acceptance module's own known, disclaimed exception (issuer context, this order's hand-off):
    # test_ogv2_a18 is NOT this cell's to fix (it rides OG-v-2's re-hand, row NFRA_OPLGTW-S26). If it is
    # the ONLY failure in that module, that is measured and reported plainly, not counted against this
    # cell's AC6, and not edited (test_local_acceptance.py is OG-v-2's <paths>, not this cell's).
    acceptance_idx = _MODULES.index("infra/aws/ec2/opal-gateway/tests/acceptance/test_local_acceptance.py")
    _, acc_passed, acc_failed, acc_last, acc_stdout = results[acceptance_idx]
    only_a18 = acc_failed == 1 and (_A18_NODEID in acc_stdout) and ("test_ogv2_a06" not in
                                                                     _failed_nodeids(acc_stdout))
    if acc_failed >= 1:
        failed_names = _failed_nodeids(acc_stdout)
        print("AC6: acceptance module failed node(s): %s" % failed_names)
        if only_a18:
            print("AC6: the acceptance module's only failure is test_ogv2_a18 -- issuer row NFRA_OPLGTW-S26 "
                 "names this as OG-v-2's own re-hand, not this cell's; reported, not fixed, not excluded "
                 "from the printed count below.")
        if "test_ogv2_a06" in failed_names:
            cusip_matched = "partial-grant-asset-cusips: got ['SYN000001', 'SYN000002']" in acc_stdout and \
                "(MATCH)" in acc_stdout
            print("AC6: test_ogv2_a06 still fails, but MEASURED at a different assertion than HALF ONE's: "
                 "its own dim_asset partial-account CUSIP assertion (line ~477) %s; the remaining failure is "
                 "the LAST assertion in that test (post-revocation guard-denial response shape, line ~488), "
                 "previously MASKED by the CUSIP assertion failing first -- a defect this cell's fix newly "
                 "exposed, not caused, in app/data_entitlement.py's guard/tests/acceptance/, neither in this "
                 "cell's <paths>; reported here, not fixed, not excluded from the count below -- see the "
                 "surprise row this cell files for it." % ("PASSES (MATCH)" if cusip_matched else
                                                            "did NOT pass -- re-check before trusting this note"))

    total_failed = sum(f for _, _, f, _, _ in results)
    print("AC6: denominator 4 modules; total failure count across all four = %d" % total_failed)
    if total_failed == 0:
        print("VERDICT: PASS-OGQ5-AC6")
        return 0
    print("VERDICT: FAIL-OGQ5-AC6 %d of %d module(s) carried a failure: %s"
         % (sum(1 for _, _, f, _, _ in results if f), denom,
            {m: f for m, _, f, _, _ in results if f}))
    return 1


def _failed_nodeids(stdout: str):
    return sorted(set(re.findall(r"^FAILED\s+\S+::(\S+)", stdout, re.M)))


def main() -> int:
    dispatch = {"AC4": ac4, "AC5": ac5, "AC6": ac6}
    if len(sys.argv) != 2 or sys.argv[1] not in dispatch:
        print("usage: og_q5.py AC4|AC5|AC6")
        return 2
    return dispatch[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
