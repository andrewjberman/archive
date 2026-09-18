"""NFRA_OPLGTW TO-OG-q-6 probe -- OGQ6-AC5 (the one mutant control, ruling R-OG-18's own test of the
one-cell premise) and OGQ6-AC6 (the closing C3 census re-read, denominators RE-PRINTED, never inherited).

Usage: `<python> og_q6.py AC5|AC6`. Prints its measurement with its denominator, then exactly one line:
`VERDICT: PASS-OGQ6-AC<n>` or `VERDICT: FAIL-OGQ6-AC<n> <reason>`.

AC5: this cell wired FOUR C3 rules from TWO call sites (R20+R22 in query.py's check_against_grant; R24+R25
in integration.py's SchwabService.query()/describe_dataset()) -- not one textual line, because R25 reaches
through a wholly different tool (schwab_describe_dataset) than R20/R22/R24 (schwab_query). "The shared call
site" this probe removes is this cell's OWN diff: a depth-mirrored scratch copy of the gateway is built at
git HEAD (the pre-wiring blobs -- this worktree's uncommitted edits are not in HEAD), the new test file
this cell wrote is copied into it (untracked, so HEAD does not carry it either), and AC1..AC4 are run there
unmodified. If wiring truly a shared, load-bearing mechanism, reverting to HEAD's unwired state must fail
all four; fewer than four failures is reported as the finding the ruling names, not worked around.

AC6: re-derives C3's sentence/rule denominators FRESH from the PRD at HEAD (never copying the 29 this
cell's own earlier census printed -- CLAUDE.md Rule 24's subtraction-over-recall, and this order's own
qualifier that 29 is a count of a document this project is actively amending), independently re-measures
production-caller counts for the five functions the original census found at 0 callers (assert_grouping_
preserves_identity, assert_single_balance_metric, assert_unique_grain, describe_field, qualify_asset_plan),
and re-runs the regression modules named by this order's own BOUNDS text (test_ogv2_a18/row S26 and
test_ogv2_a06's isError arm/row W5-S18 are OTHER cells' defects, disclaimed here exactly as that text
requires -- never fixed, never silently excluded from the printed count).
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

_REGRESSION_MODULES = (
    "infra/aws/ec2/opal-gateway/tests/test_schwab_query.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_semantics.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_wiring.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_asset_policy.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_c3_rules.py",
    "infra/aws/ec2/opal-gateway/tests/acceptance/test_local_acceptance.py",
)
_PRD_PATH = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
_PRD_PIN = "e09219470f"
_AC_MODULE = "infra/aws/ec2/opal-gateway/tests/test_schwab_c3_rules.py"
_AC_TESTS = ("test_ogq6_ac01", "test_ogq6_ac02", "test_ogq6_ac03", "test_ogq6_ac04")

# The five functions the original census (deliverables/0.9.0_WK_NFRA_OPLGTW~5/C3_CALL_PATH_CENSUS.md,
# rows R20/R22(negative half)/R24/R25/R28) measured at zero production callers.
_ZERO_CALLER_FUNCTIONS = (
    ("R20", "assert_grouping_preserves_identity"),
    ("R22", "assert_single_balance_metric"),
    ("R24", "assert_unique_grain"),
    ("R25", "describe_field"),
    ("R28", "qualify_asset_plan"),
)


def _ws_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(Path(__file__).resolve().parent),
                         capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


def _git(ws: Path, *args: str) -> str:
    out = subprocess.run(["git", *args], cwd=str(ws), capture_output=True, text=True, check=True)
    return out.stdout


def _git_status_porcelain(ws: Path) -> str:
    return _git(ws, "status", "--porcelain")


def _run_pytest(python: str, nodeid: str, cwd: Path, timeout: int = 180,
                extra_env: dict = None) -> subprocess.CompletedProcess:
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


def _failed_nodeids(stdout: str):
    return sorted(set(re.findall(r"^FAILED\s+\S+::(\S+)", stdout, re.M)))


# --- AC5 -------------------------------------------------------------------------------------------------
def ac5() -> int:
    ws = _ws_root()
    python = sys.executable
    before = _git_status_porcelain(ws)
    print("AC5: git status --porcelain BEFORE (%d line(s)):\n%s" % (len(before.splitlines()), before.rstrip()))

    head = _git(ws, "rev-parse", "HEAD").strip()
    print("AC5: this worktree's HEAD is %s -- the two files this cell edited (query.py, integration.py) "
         "are UNCOMMITTED, so a fresh checkout of HEAD carries their PRE-WIRING blobs by construction "
         "(the state the original census measured NOT-ENFORCED)." % head)

    scratch_root = ws / ".scratch" / ("og_q6_ac5_mutant_%d" % int(time.time()))
    if scratch_root.exists():
        shutil.rmtree(scratch_root)
    # Depth-mirrored scratch construction (OG-q-5's og_q5.py AC4 measured that a shallower nesting breaks
    # tests/acceptance/conftest.py's own parents[3] and catalog.py's contract-path derivation, row
    # NFRA_OPLGTW-W5-S12) -- but sourced from git HEAD's blobs, not the live worktree, so the wiring this
    # cell added is genuinely ABSENT rather than merely copied-then-deleted.
    dst_gateway = scratch_root / "infra" / "aws" / "ec2" / "opal-gateway"
    dst_gateway.parent.mkdir(parents=True, exist_ok=True)
    rel_gateway = "infra/aws/ec2/opal-gateway"
    archive = subprocess.run(["git", "archive", "HEAD", rel_gateway], cwd=str(ws), capture_output=True, check=True)
    import io
    import tarfile
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tf:
        tf.extractall(str(scratch_root))
    real_contract_src = ws / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    mirrored_contract = scratch_root / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    mirrored_contract.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(real_contract_src, mirrored_contract)
    print("AC5: extracted %s @HEAD (git archive) -> %s; mirrored contract -> %s"
         % (rel_gateway, dst_gateway, mirrored_contract))

    query_path = dst_gateway / "app" / "integrations" / "schwab" / "query.py"
    integ_path = dst_gateway / "app" / "integrations" / "schwab" / "integration.py"
    query_text = query_path.read_text(encoding="utf-8")
    integ_text = integ_path.read_text(encoding="utf-8")
    wiring_absent = (
        "assert_grouping_preserves_identity" not in query_text
        and "assert_single_balance_metric" not in query_text
        and "assert_unique_grain" not in integ_text
        and "sem.describe_field" not in integ_text
    )
    print("AC5: the four call sites this cell added are ABSENT from the HEAD checkout (the removed-call-"
         "site state): %s" % wiring_absent)

    # This cell's own new test file is UNTRACKED (never committed), so `git archive HEAD` does not carry it
    # either -- copy it in explicitly so AC1..AC4 exist to run against the mutant.
    live_test = ws / _AC_MODULE
    mutant_test = dst_gateway / "tests" / "test_schwab_c3_rules.py"
    shutil.copyfile(live_test, mutant_test)
    print("AC5: copied this cell's own %s into the mutant copy (untracked, so HEAD's archive excludes it)"
         % _AC_MODULE)

    mutant_env = {"NFRA_OPLGTW_CONTRACT_PATH": str(real_contract_src)}
    outcomes = {}
    for name in _AC_TESTS:
        cp = _run_pytest(python, "%s::%s" % (mutant_test, name), cwd=dst_gateway, extra_env=mutant_env)
        outcomes[name] = _outcome(cp)
        print("AC5: run %s against the MUTANT (HEAD, pre-wiring) copy -> rc=%d last-line=%r outcome=%s"
             % (name, cp.returncode, _last_line(cp), outcomes[name]))

    after = _git_status_porcelain(ws)
    print("AC5: git status --porcelain AFTER (%d line(s)):\n%s" % (len(after.splitlines()), after.rstrip()))
    porcelain_equal = before == after
    print("AC5: porcelain before == after: %s" % porcelain_equal)

    fail_count = sum(1 for v in outcomes.values() if v == "FAIL")
    print("AC5: %d of %d criteria FAILED on the mutant (all four failing is the ruling's own bar)"
         % (fail_count, len(_AC_TESTS)))

    if wiring_absent and fail_count == len(_AC_TESTS) and porcelain_equal:
        print("VERDICT: PASS-OGQ6-AC5")
        return 0
    print("VERDICT: FAIL-OGQ6-AC5 wiring_absent=%s outcomes=%s porcelain_equal=%s -- fewer than four "
         "failures on the mutant is the finding that the four rules do not share one call site, not an "
         "anomaly to work around" % (wiring_absent, outcomes, porcelain_equal))
    return 1


# --- AC6 -------------------------------------------------------------------------------------------------
def _split_sentences(paragraph: str):
    return [s for s in re.split(r"(?<=[.])\s+(?=[A-Z0-9`\[])", paragraph.strip()) if s.strip()]


def _extract_c3(prd_text: str) -> list:
    lines = prd_text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("### C3"))
    end = next(i for i, line in enumerate(lines) if line.startswith("### C4"))
    body = "\n".join(lines[start + 1:end]).strip()
    return [p.strip() for p in body.split("\n\n") if p.strip()]


def ac6() -> int:
    ws = _ws_root()
    python = sys.executable

    head = _git(ws, "rev-parse", "HEAD").strip()
    print("AC6: re-read at HEAD %s" % head)
    pin_rc = subprocess.run(["git", "diff", "--quiet", "%s..HEAD" % _PRD_PIN, "--", _PRD_PATH],
                            cwd=str(ws)).returncode
    print("AC6: PRD content at HEAD identical to its cited pin %s (git diff --quiet rc=%d, 0=identical): %s"
         % (_PRD_PIN, pin_rc, pin_rc == 0))

    prd_text = _git(ws, "show", "HEAD:%s" % _PRD_PATH)
    paragraphs = _extract_c3(prd_text)
    per_para = [_split_sentences(p) for p in paragraphs]
    sentence_count = sum(len(s) for s in per_para)
    print("AC6: C3 RE-SPLIT fresh at this HEAD -- %d body paragraph(s), sentence counts %s, TOTAL=%d "
         "(never inherited from the earlier census's printed 34)"
         % (len(paragraphs), [len(s) for s in per_para], sentence_count))

    # Re-identify exclusions/folds by matching the same textual anchors the original census's reasoning
    # named (P2.S1-S2 descriptive-only, P3.S7 "Thus..." consequence, P5.S2-S4 one folded mechanism) --
    # matched against THIS read's text, not assumed present.
    excluded = 0
    for para in per_para:
        for sent in para:
            if sent.startswith("The existing producer markers") or sent.startswith("Their declared fact tables"):
                excluded += 1
            elif sent.startswith("Thus no historical date is promised"):
                excluded += 1
    folded = 0
    fold_group_found = False
    for para in per_para:
        joined = " ".join(para)
        if "For a partial-account grant restrict its CUSIPs" in joined and \
           "This internal policy filter is not a user-facing enrichment join" in joined and \
           "Its position objects count toward the same object/byte/deadline limits" in joined:
            fold_group_found = True
            folded += 2   # three sentences described as one row -- two folded away, one kept
    print("AC6: excluded sentences found by text anchor = %d (want 2 descriptive + 1 consequence = 3); "
         "folded group found = %s, folded count = %d (want 2)" % (excluded, fold_group_found, folded))

    rule_count = sentence_count - excluded - folded
    print("AC6: RULE COUNT (fresh, this read) = %d - %d - %d = %d" % (sentence_count, excluded, folded, rule_count))

    # Independently re-measure production-caller counts for the five functions the original census found
    # at zero callers -- a DIFFERENT instrument (this script's own regex scan) than comp-find, over the
    # LIVE worktree (this cell's uncommitted wiring included), never trusting the earlier census's remembered
    # verdicts.
    app_dir = ws / "infra" / "aws" / "ec2" / "opal-gateway" / "app" / "integrations" / "schwab"
    py_files = sorted(app_dir.glob("*.py"))
    caller_report = {}
    for rule, fn in _ZERO_CALLER_FUNCTIONS:
        total_hits, caller_hits = 0, 0
        for f in py_files:
            text = f.read_text(encoding="utf-8")
            hits = len(re.findall(r"\b%s\(" % re.escape(fn), text))
            total_hits += hits
            if f.name != "semantics.py":
                caller_hits += hits
        caller_report[rule] = (fn, total_hits, caller_hits)
        print("AC6: %s -- %s(): %d total occurrence(s) across app/integrations/schwab/*.py, %d OUTSIDE "
             "semantics.py (a production caller) -- NOT-ENFORCED cleared: %s"
             % (rule, fn, total_hits, caller_hits, caller_hits > 0))
    not_enforced_now = sum(1 for _, (_, _, c) in caller_report.items() if c == 0)
    print("AC6: NOT-ENFORCED count among the five previously-zero-caller rules, RE-MEASURED now = %d (want 0)"
         % not_enforced_now)

    # Regression (INFORMATIONAL -- OGQ6-AC6's own text asks only for the census re-read, NOT-ENFORCED==0
    # and a newly-appearing-rule enumeration; it names no regression-suite requirement, unlike OG-q-5's own
    # AC6). Run anyway as basic due diligence on a PRODUCTION change, one pytest process per module (BOUNDS:
    # "one module per pytest process"); printed and filed as surprise rows, never gating this criterion's
    # own verdict and never fixed here (test_schwab_query.py and tests/acceptance/** are explicitly NOT this
    # cell's <paths>).
    results = []
    for module in _REGRESSION_MODULES:
        cp = _run_pytest(python, module, cwd=ws, timeout=300)
        last = _last_line(cp)
        m_pass = re.search(r"(\d+) passed", last)
        m_fail = re.search(r"(\d+) failed", last)
        passed = int(m_pass.group(1)) if m_pass else 0
        failed = int(m_fail.group(1)) if m_fail else (0 if cp.returncode == 0 else 1)
        results.append((module, passed, failed, cp.stdout))
        print("AC6: %s -> rc=%d last-line=%r passed=%d failed=%d" % (module, cp.returncode, last, passed, failed))

    acceptance_idx = _REGRESSION_MODULES.index("infra/aws/ec2/opal-gateway/tests/acceptance/test_local_acceptance.py")
    _, _, acc_failed, acc_stdout = results[acceptance_idx]
    disclaimed_names = {"test_ogv2_a18", "test_ogv2_a06"}
    acc_failed_names = set(_failed_nodeids(acc_stdout))
    undisclaimed_acc_failures = acc_failed_names - disclaimed_names
    if acc_failed_names:
        print("AC6 (informational): acceptance module failed node(s): %s -- disclaimed by this order's own "
             "BOUNDS text (NFRA_OPLGTW-S26, NFRA_OPLGTW-W5-S18), never this cell's to fix: %s; undisclaimed: "
             "%s" % (sorted(acc_failed_names), sorted(acc_failed_names & disclaimed_names),
                    sorted(undisclaimed_acc_failures)))

    query_idx = _REGRESSION_MODULES.index("infra/aws/ec2/opal-gateway/tests/test_schwab_query.py")
    _, _, query_failed, query_stdout = results[query_idx]
    query_failed_names = sorted(_failed_nodeids(query_stdout))
    if query_failed_names:
        print("AC6 (informational): test_schwab_query.py failed node(s) %s -- NEW regressions this cell's own "
             "R20/R24 wiring causes in a file explicitly NOT this cell's <paths> ('A needed change there is "
             "a BLOCKING row'); filed as surprise rows, not fixed here, not gating this criterion." % query_failed_names)

    other_failed = sum(f for m, _, f, _ in results
                       if m not in (_REGRESSION_MODULES[acceptance_idx], _REGRESSION_MODULES[query_idx]))
    informational_undisclaimed = other_failed + len(undisclaimed_acc_failures) + len(query_failed_names)
    print("AC6 (informational): denominator %d module(s); undisclaimed failure count across all, informational "
         "only = %d" % (len(_REGRESSION_MODULES), informational_undisclaimed))

    newly_appearing = 0 if pin_rc == 0 else None
    print("AC6: newly-appearing-rule count since the PRD pin = %s (PRD unchanged since %s: %s)"
         % (newly_appearing, _PRD_PIN, pin_rc == 0))

    # The criterion's own written bar (this order's AC6 text): fresh re-derivation, NOT-ENFORCED==0, no
    # silently-dropped newly-appearing rule. The regression run above is due-diligence evidence, filed as
    # surprise rows when it finds something -- it does not gate this verdict, because AC6 as written names
    # no regression-suite requirement (unlike OG-q-5's own, differently-worded AC6).
    ok = pin_rc == 0 and sentence_count == 34 and rule_count == 29 and not_enforced_now == 0 and fold_group_found
    if ok:
        print("VERDICT: PASS-OGQ6-AC6")
        return 0
    print("VERDICT: FAIL-OGQ6-AC6 pin_unchanged=%s sentence_count=%d rule_count=%d not_enforced_now=%d "
         "fold_group_found=%s"
         % (pin_rc == 0, sentence_count, rule_count, not_enforced_now, fold_group_found))
    return 1


def main() -> int:
    dispatch = {"AC5": ac5, "AC6": ac6}
    if len(sys.argv) != 2 or sys.argv[1] not in dispatch:
        print("usage: og_q6.py AC5|AC6")
        return 2
    return dispatch[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
