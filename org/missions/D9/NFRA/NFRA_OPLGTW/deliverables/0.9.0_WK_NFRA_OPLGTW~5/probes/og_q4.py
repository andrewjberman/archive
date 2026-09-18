"""NFRA_OPLGTW TO-OG-q-4 probe -- OGQ4-AC4 (mutant control), AC5 (the surrounding modules still pass), AC6
(the R-OG-15 correction's changed lines stay inside the two granted tests) and AC7 (the module's collected
test count before/after the correction, and each corrected test's contract-clause citation).

Usage: `<python> og_q4.py AC4|AC5|AC6|AC7`. Prints its measurement with its denominator, then exactly one
line: `VERDICT: PASS-OGQ4-AC<n>` or `VERDICT: FAIL-OGQ4-AC<n> <reason>`.

AC4 (mutant control, ruling R-OG-13's standing bar): copy the worktree's opal-gateway tree (app/ + tests/,
so `test_ogq4_ac01/02/03` can run standalone against the copy) into a scratch directory under this
worktree's own `.scratch/`; in that copy ONLY, replace `app/integrations/schwab/query.py` with its own
CONTENT-PINNED pre-wiring version (see `_pre_wiring_query_bytes` below -- NOT `git show HEAD:...`: this
hand-off's first pass wrote the mutant from `HEAD` while the wiring commit was still uncommitted, so `HEAD`
correctly meant "before this cell's own call site landed" at that moment; now that 881b1a5445 is committed
and this branch has since merged CLOUD in, `HEAD` for query.py IS the wired version, and using it here would
make AC1/AC2 pass unchanged against the "mutant" -- discriminating nothing. `_pre_wiring_query_bytes` finds
the pin by CONTENT instead of by a moving ref: it walks query.py's own history oldest-to-newest and returns
the bytes of the LAST commit whose content does not yet contain `assert_quantity_sum_grouped`, with a
negative control that the pin lacks the call site while the current worktree file has it.) This removes
exactly the call site OGQ4-AC1/AC2 exercise and nothing else (verified directly: `git diff
6a4df76f02^..HEAD -- query.py` up to the query.py path is exactly the docstring update, the local
`from . import semantics as sem` and the `if agg.function == "sum": try/except` block -- nothing else in the
file changed between the pin and the wired version). semantics.py, datasets.json and every other module in
the copy are untouched, still the current worktree's bytes. Then run OGQ4-AC1, OGQ4-AC2 and OGQ4-AC3 as
separate pytest subprocesses against that copy: AC1 and AC2 must FAIL (the refusal the call site raised is
gone) while AC3 must still PASS (a legal sum was never guarded by that call site to begin with). The real,
tracked query.py is never opened for writing by this probe; a `git status --porcelain` read before and
after is printed and compared.

The mutant copy's `catalog.default_contract_path()` derives the contract path from `Path(__file__).resolve()
.parents[7]`, i.e. from catalog.py's OWN depth under the repo root (schwab/integrations/app/opal-gateway/ec2/
aws/infra/<root>, 7 levels) -- a scratch copy nested under `.scratch/<name>/opal-gateway/...` sits at a
DIFFERENT depth, so that derivation resolves to the wrong directory. **Measured 2026-09-17 by this seat: the
SAME depth fact also breaks `tests/acceptance/conftest.py` at IMPORT TIME** -- its own `_CONTRACT_PATH` is
`_GATEWAY.parents[3]` computed directly, with NO `NFRA_OPLGTW_CONTRACT_PATH` fallback at all (only
`catalog.load_contract` reads that var), so setting the env var does not help `test_schwab_wiring.py`'s
`import acceptance.conftest as h_`: at the shallow `.scratch/<name>/opal-gateway/` depth this raised
`FileNotFoundError` for the mis-derived contract path one level ABOVE the real repo root (a
`.../org/standards/NFRA_OPLGTW_CONTRACT.json` rooted at the scratch parent instead of the worktree) on
every one of AC1/AC2/AC3 against the mutant, which is a probe defect (a depth mismatch), not a finding
about the wiring. The fix is structural, not an env var: the mutant copy is nested at the SAME
relative depth as the real tree (`<scratch_root>/infra/aws/ec2/opal-gateway/...`), and the real, unmutated
contract file is mirrored at `<scratch_root>/org/standards/NFRA_OPLGTW_CONTRACT.json` -- so both
`catalog.py`'s `parents[7]` fallback and `conftest.py`'s `parents[3]` computation resolve to a real file
without either module needing to know it is running from scratch. `NFRA_OPLGTW_CONTRACT_PATH` is still set
on the mutant subprocess as a second, redundant guard for `catalog.load_contract`'s own explicit override
path; it was never sufficient on its own.

AC5: `tests/test_schwab_query.py`, `tests/test_schwab_semantics.py` and `tests/test_schwab_export.py`, one
pytest process per module (the harness's own "one module per pytest process" constraint -- BOUNDS), against
the REAL worktree (not the scratch copy) -- these are OG-q-1/q-2/q-3's own acceptance suites, run here only
to show this cell's edit did not regress them.

AC6/AC7 cut base: `_CUT_BASE` below is `d91629cfd8`, the merge-base of this branch with CLOUD's tip AT this
hand-off's starting HEAD (`2392d6f9fb`, a merge commit whose two parents are `881b1a5445` -- this seat's own
prior work -- and `d91629cfd8` -- the CLOUD tip the issuer merged in to deliver the R-OG-15 amendment). It is
PINNED to that literal hash rather than re-derived from `git merge-base HEAD CLOUD` at probe run time,
because CLOUD is a shared branch that can move independently of this worktree, and the question AC6/AC7 ask
("what did this hand-off change against the file it started from") is about that ONE historical merge, not
whatever CLOUD happens to point to when the probe next runs. `test_schwab_query.py` at that pin is the
pre-correction, OG-q-2-original file: the R-OG-15 amendment commit (`d91629cfd8`) touched only the task
order's own `.md` file, never the test file itself (verified: `git show --stat d91629cfd8` lists exactly one
changed path).
"""
from __future__ import annotations

import bisect
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

_REAL_QUERY_PY = "infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py"
_QUERY_TEST = "infra/aws/ec2/opal-gateway/tests/test_schwab_query.py"
_WIRING_TEST = "infra/aws/ec2/opal-gateway/tests/test_schwab_wiring.py"
_AC5_MODULES = (
    "infra/aws/ec2/opal-gateway/tests/test_schwab_query.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_semantics.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_export.py",
)
_CALL_SITE_MARKER = "assert_quantity_sum_grouped"
_CUT_BASE = "d91629cfd8e7693c65ac3b06d945fa584be44adf"
_CORRECTED_TESTS = ("test_ogq2_ac07", "test_ogq2_ac15")
_CLAUSE_MARKER = "Quantity sums require grouping by CUSIP and long/short indicator"


def _ws_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(Path(__file__).resolve().parent),
                         capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


def _git_status_porcelain(ws: Path) -> str:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=str(ws), capture_output=True, text=True, check=True)
    return out.stdout


def _run_pytest(python: str, ws: Path, nodeid: str, cwd: Path, extra_env: dict = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    return subprocess.run([python, "-m", "pytest", nodeid, "-q", "-p", "no:cacheprovider", "--color=no"],
                          cwd=str(cwd), capture_output=True, text=True, timeout=180, env=env)


def _outcome(cp: subprocess.CompletedProcess) -> str:
    tail = cp.stdout.strip().splitlines()
    last = tail[-1] if tail else "(no output)"
    if cp.returncode == 0 and re.search(r"^1 passed", last):
        return "PASS"
    if re.search(r"failed|error", last, re.I):
        return "FAIL"
    return "FAIL"  # any non-clean-pass outcome (timeout, collection error) counts as not-PASS


def _pre_wiring_query_bytes(ws: Path) -> "tuple[str, bytes]":
    """Content-pinned, never HEAD: walk query.py's own history oldest-to-newest and return (commit, bytes)
    for the LAST commit whose content does NOT yet contain the call site -- the version immediately before
    OG-q-4's own wiring landed, whichever commit that turns out to be. A negative control follows: the
    returned bytes must lack the marker while the CURRENT worktree file must carry it."""
    log = subprocess.run(["git", "log", "--format=%H", "--", _REAL_QUERY_PY], cwd=str(ws),
                         capture_output=True, text=True, check=True).stdout.split()
    pin, pin_bytes = None, b""
    for commit in reversed(log):  # oldest first
        content = subprocess.run(["git", "show", "%s:%s" % (commit, _REAL_QUERY_PY)], cwd=str(ws),
                                 capture_output=True, check=True).stdout
        if _CALL_SITE_MARKER.encode() in content:
            break
        pin, pin_bytes = commit, content
    current = (ws / _REAL_QUERY_PY).read_bytes()
    if pin is None:
        raise RuntimeError("no commit in %s's history lacks %r -- cannot pin a pre-wiring mutant"
                           % (_REAL_QUERY_PY, _CALL_SITE_MARKER))
    if _CALL_SITE_MARKER.encode() not in current:
        raise RuntimeError("current worktree %s lacks %r -- the call site is not even wired at HEAD"
                           % (_REAL_QUERY_PY, _CALL_SITE_MARKER))
    return pin, pin_bytes


def ac4() -> int:
    ws = _ws_root()
    python = sys.executable
    before = _git_status_porcelain(ws)
    print("AC4: git status --porcelain BEFORE (%d line(s)):\n%s" % (len(before.splitlines()), before.rstrip()))

    scratch_root = ws / ".scratch" / ("og_q4_mutant_%d" % int(time.time()))
    if scratch_root.exists():
        shutil.rmtree(scratch_root)
    src_gateway = ws / "infra" / "aws" / "ec2" / "opal-gateway"
    # mirror the REAL relative depth (repo_root/infra/aws/ec2/opal-gateway) so conftest.py's own
    # `_GATEWAY.parents[3]` and catalog.py's `parents[7]` both resolve to a real directory instead of
    # walking above a shallower scratch nesting (see module docstring, AC4 section).
    dst_gateway = scratch_root / "infra" / "aws" / "ec2" / "opal-gateway"
    shutil.copytree(src_gateway, dst_gateway, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    real_contract_src = ws / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    mirrored_contract = scratch_root / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    mirrored_contract.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(real_contract_src, mirrored_contract)
    print("AC4: copied %s -> %s (%d bytes source-side app/ dir); mirrored contract %s -> %s"
         % (src_gateway, dst_gateway, sum(f.stat().st_size for f in (src_gateway / "app").rglob("*") if f.is_file()),
            real_contract_src, mirrored_contract))

    pin, pre_wiring_bytes = _pre_wiring_query_bytes(ws)
    mutant_query_py = dst_gateway / "app" / "integrations" / "schwab" / "query.py"
    wired_bytes = mutant_query_py.read_bytes()
    mutant_query_py.write_bytes(pre_wiring_bytes)
    same = wired_bytes == pre_wiring_bytes
    print("AC4: mutant query.py written at %s (%d bytes, content-pinned at %s, verified pre-wiring); differs "
         "from the copy's wired bytes: %s" % (mutant_query_py, len(pre_wiring_bytes), pin, not same))
    if same:
        # the pin already carries the call site -- the mutant would be a no-op control, not a mutant.
        print("VERDICT: FAIL-OGQ4-AC4 pin %s is byte-identical to the worktree copy -- no call site to "
             "remove, the mutant control cannot discriminate" % pin)
        return 1

    # redundant guard on top of the depth-mirrored copy above: catalog.load_contract's own explicit
    # override still points at the REAL, unmutated contract file (see module docstring, AC4 section).
    mutant_env = {"NFRA_OPLGTW_CONTRACT_PATH": str(real_contract_src)}

    mutant_test = dst_gateway / "tests" / "test_schwab_wiring.py"
    outcomes = {}
    for name, ac_id in (("AC1", "test_ogq4_ac01"), ("AC2", "test_ogq4_ac02"), ("AC3", "test_ogq4_ac03")):
        cp = _run_pytest(python, ws, "%s::%s" % (mutant_test, ac_id), cwd=dst_gateway, extra_env=mutant_env)
        outcomes[name] = _outcome(cp)
        tail = cp.stdout.strip().splitlines()
        print("AC4: mutant run %s (%s) -> rc=%d last-line=%r outcome=%s"
             % (name, ac_id, cp.returncode, tail[-1] if tail else "", outcomes[name]))

    after = _git_status_porcelain(ws)
    print("AC4: git status --porcelain AFTER (%d line(s)):\n%s" % (len(after.splitlines()), after.rstrip()))
    porcelain_equal = before == after
    print("AC4: porcelain before == after: %s" % porcelain_equal)

    ok = outcomes["AC1"] == "FAIL" and outcomes["AC2"] == "FAIL" and outcomes["AC3"] == "PASS" and porcelain_equal
    if ok:
        print("VERDICT: PASS-OGQ4-AC4")
        return 0
    print("VERDICT: FAIL-OGQ4-AC4 outcomes=%s porcelain_equal=%s" % (outcomes, porcelain_equal))
    return 1


def ac5() -> int:
    ws = _ws_root()
    python = sys.executable
    denom = len(_AC5_MODULES)
    results = []
    for module in _AC5_MODULES:
        cp = _run_pytest(python, ws, module, cwd=ws)
        tail = cp.stdout.strip().splitlines()
        last = tail[-1] if tail else "(no output)"
        m = re.search(r"^(\d+) passed", last)
        passed_count = int(m.group(1)) if (cp.returncode == 0 and m) else 0
        ok = cp.returncode == 0 and m is not None
        results.append((module, ok, passed_count, last))
        print("AC5: %s -> rc=%d last-line=%r pass_count=%d" % (module, cp.returncode, last, passed_count))

    n_ok = sum(1 for _, ok, _, _ in results if ok)
    print("AC5: %d of %d module(s) passed" % (n_ok, denom))
    if n_ok == denom:
        print("VERDICT: PASS-OGQ4-AC5")
        return 0
    print("VERDICT: FAIL-OGQ4-AC5 %d of %d module(s) passed" % (n_ok, denom))
    return 1


_DEF_RE = re.compile(r"^def (\w+)\(", re.M)


def _function_ranges(text: str) -> dict:
    """1-based [start_line, end_line] (inclusive) for every top-level `def name(...)` in `text`, end_line
    being the line before the next top-level def or EOF."""
    lines = text.splitlines()
    line_starts = []
    pos = 0
    for ln in lines:
        line_starts.append(pos)
        pos += len(ln) + 1
    entries = []
    for m in _DEF_RE.finditer(text):
        line_no = bisect.bisect_right(line_starts, m.start())
        entries.append((line_no, m.group(1)))
    entries.sort()
    ranges = {}
    for idx, (start_line, name) in enumerate(entries):
        end_line = entries[idx + 1][0] - 1 if idx + 1 < len(entries) else len(lines)
        ranges[name] = (start_line, end_line)
    return ranges


def _function_source(text: str, name: str) -> str:
    ranges = _function_ranges(text)
    if name not in ranges:
        return ""
    start, end = ranges[name]
    lines = text.splitlines()
    return "\n".join(lines[start - 1:end])


_HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _hunks(diff_u0_text: str):
    out = []
    for line in diff_u0_text.splitlines():
        m = _HUNK_RE.match(line)
        if m:
            old_start = int(m.group(1))
            old_len = int(m.group(2)) if m.group(2) is not None else 1
            new_start = int(m.group(3))
            new_len = int(m.group(4)) if m.group(4) is not None else 1
            out.append((old_start, old_len, new_start, new_len))
    return out


def ac6() -> int:
    ws = _ws_root()
    old_text = subprocess.run(["git", "show", "%s:%s" % (_CUT_BASE, _QUERY_TEST)], cwd=str(ws),
                              capture_output=True, text=True, check=True).stdout
    new_text = (ws / _QUERY_TEST).read_text(encoding="utf-8")

    diff = subprocess.run(["git", "diff", _CUT_BASE, "--", _QUERY_TEST], cwd=str(ws),
                          capture_output=True, text=True, check=True).stdout
    diff0 = subprocess.run(["git", "diff", "-U0", _CUT_BASE, "--", _QUERY_TEST], cwd=str(ws),
                           capture_output=True, text=True, check=True).stdout
    print("AC6: diff of %s against cut base %s (%d line(s)):" % (_QUERY_TEST, _CUT_BASE, len(diff.splitlines())))
    print(diff)

    old_ranges = _function_ranges(old_text)
    new_ranges = _function_ranges(new_text)
    for name in _CORRECTED_TESTS:
        if name not in old_ranges or name not in new_ranges:
            print("VERDICT: FAIL-OGQ4-AC6 %s missing from old (%s) or new (%s) function ranges"
                 % (name, name in old_ranges, name in new_ranges))
            return 1
    print("AC6: allowed ranges old=%s new=%s" % ({n: old_ranges[n] for n in _CORRECTED_TESTS},
                                                  {n: new_ranges[n] for n in _CORRECTED_TESTS}))

    hunks = _hunks(diff0)
    bad = []
    for (old_start, old_len, new_start, new_len) in hunks:
        old_end = old_start + old_len - 1
        new_end = new_start + new_len - 1
        ok_old = (old_len == 0) or any(old_ranges[n][0] <= old_start and old_end <= old_ranges[n][1]
                                       for n in _CORRECTED_TESTS)
        ok_new = (new_len == 0) or any(new_ranges[n][0] <= new_start and new_end <= new_ranges[n][1]
                                       for n in _CORRECTED_TESTS)
        print("AC6: hunk -%d,%d +%d,%d -> old_ok=%s new_ok=%s" % (old_start, old_len, new_start, new_len,
                                                                   ok_old, ok_new))
        if not (ok_old and ok_new):
            bad.append((old_start, old_len, new_start, new_len))

    if hunks and not bad:
        print("VERDICT: PASS-OGQ4-AC6")
        return 0
    print("VERDICT: FAIL-OGQ4-AC6 %d of %d hunk(s) outside %s: %s" % (len(bad), len(hunks), _CORRECTED_TESTS, bad))
    return 1


def _collect_count(python: str, cwd: Path, nodeid: str, extra_env: dict = None):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    cp = subprocess.run([python, "-m", "pytest", "--collect-only", "-q", nodeid, "-p", "no:cacheprovider",
                        "--color=no"], cwd=str(cwd), capture_output=True, text=True, timeout=120, env=env)
    m = re.search(r"^(\d+) tests? collected", cp.stdout, re.M)
    return (int(m.group(1)) if m else -1), cp


def ac7() -> int:
    ws = _ws_root()
    python = sys.executable

    current_text = (ws / _QUERY_TEST).read_text(encoding="utf-8")
    after_count, after_cp = _collect_count(python, ws, _QUERY_TEST)
    print("AC7: collected AFTER correction -> %d (last line: %r)"
         % (after_count, after_cp.stdout.strip().splitlines()[-1] if after_cp.stdout.strip() else ""))

    old_bytes = subprocess.run(["git", "show", "%s:%s" % (_CUT_BASE, _QUERY_TEST)], cwd=str(ws),
                               capture_output=True, check=True).stdout

    scratch_root = ws / ".scratch" / ("og_q4_ac7_%d" % int(time.time()))
    if scratch_root.exists():
        shutil.rmtree(scratch_root)
    src_gateway = ws / "infra" / "aws" / "ec2" / "opal-gateway"
    dst_gateway = scratch_root / "opal-gateway"
    shutil.copytree(src_gateway, dst_gateway, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (dst_gateway / "tests" / "test_schwab_query.py").write_bytes(old_bytes)

    real_contract = ws / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    before_count, before_cp = _collect_count(python, dst_gateway, "tests/test_schwab_query.py",
                                             extra_env={"NFRA_OPLGTW_CONTRACT_PATH": str(real_contract)})
    print("AC7: collected BEFORE correction (cut base %s) -> %d (last line: %r)"
         % (_CUT_BASE, before_count, before_cp.stdout.strip().splitlines()[-1] if before_cp.stdout.strip() else ""))

    denom_ok = before_count == 25 and after_count == 25
    print("AC7: denominators -- before=%d after=%d (expected 25/25: 23 untouched + 2 corrected)"
         % (before_count, after_count))

    cite = {}
    for name in _CORRECTED_TESTS:
        src = _function_source(current_text, name)
        cite[name] = _CLAUSE_MARKER in src
        print("AC7: %s carries the contract-clause citation (%r): %s" % (name, _CLAUSE_MARKER, cite[name]))
    cite_ok = all(cite.values())

    if denom_ok and cite_ok:
        print("VERDICT: PASS-OGQ4-AC7")
        return 0
    print("VERDICT: FAIL-OGQ4-AC7 before=%d after=%d cite=%s" % (before_count, after_count, cite))
    return 1


def main() -> int:
    dispatch = {"AC4": ac4, "AC5": ac5, "AC6": ac6, "AC7": ac7}
    if len(sys.argv) != 2 or sys.argv[1] not in dispatch:
        print("usage: og_q4.py AC4|AC5|AC6|AC7")
        return 2
    return dispatch[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
