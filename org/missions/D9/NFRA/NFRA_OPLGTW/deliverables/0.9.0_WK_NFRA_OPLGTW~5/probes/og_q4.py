"""NFRA_OPLGTW TO-OG-q-4 probe -- OGQ4-AC4 (mutant control) and OGQ4-AC5 (the surrounding modules still pass).

Usage: `<python> og_q4.py AC4` or `<python> og_q4.py AC5`. Prints its measurement with its denominator, then
exactly one line: `VERDICT: PASS-OGQ4-AC<n>` or `VERDICT: FAIL-OGQ4-AC<n> <reason>`.

AC4 (mutant control, ruling R-OG-13's standing bar): copy the worktree's opal-gateway tree (app/ + tests/,
so `test_ogq4_ac01/02/03` can run standalone against the copy) into a scratch directory under this
worktree's own `.scratch/`; in that copy ONLY, replace `app/integrations/schwab/query.py` with the
`git show HEAD:...` version -- HEAD is this cell's OWN starting point, i.e. the version of query.py before
this order wired semantics.py in, so restoring it removes exactly the call site OGQ4-AC1/AC2 exercise and
nothing else (semantics.py, datasets.json and every other module in the copy are untouched, still the
current worktree's bytes). Then run OGQ4-AC1, OGQ4-AC2 and OGQ4-AC3 as separate pytest subprocesses against
that copy: AC1 and AC2 must FAIL (the refusal the call site raised is gone) while AC3 must still PASS (a
legal sum was never guarded by that call site to begin with). The real, tracked query.py is never opened
for writing by this probe; a `git status --porcelain` read before and after is printed and compared.

The mutant copy's `catalog.default_contract_path()` derives the contract path from `Path(__file__).resolve()
.parents[7]`, i.e. from catalog.py's OWN depth under the repo root (schwab/integrations/app/opal-gateway/ec2/
aws/infra/<root>, 7 levels) -- a scratch copy nested under `.scratch/<name>/opal-gateway/...` sits at a
DIFFERENT depth, so that derivation resolves to the wrong directory. This is a path-depth fact about the
scratch copy's location, not a call-site change, so the mutant subprocess is launched with
`NFRA_OPLGTW_CONTRACT_PATH` set to the REAL, unmutated contract file's absolute path (catalog.py's own
documented override: "the explicit path, then NFRA_OPLGTW_CONTRACT_PATH, then the repository layout").

AC5: `tests/test_schwab_query.py`, `tests/test_schwab_semantics.py` and `tests/test_schwab_export.py`, one
pytest process per module (the harness's own "one module per pytest process" constraint -- BOUNDS), against
the REAL worktree (not the scratch copy) -- these are OG-q-1/q-2/q-3's own acceptance suites, run here only
to show this cell's edit did not regress them.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

_REAL_QUERY_PY = "infra/aws/ec2/opal-gateway/app/integrations/schwab/query.py"
_WIRING_TEST = "infra/aws/ec2/opal-gateway/tests/test_schwab_wiring.py"
_AC5_MODULES = (
    "infra/aws/ec2/opal-gateway/tests/test_schwab_query.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_semantics.py",
    "infra/aws/ec2/opal-gateway/tests/test_schwab_export.py",
)


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


def ac4() -> int:
    ws = _ws_root()
    python = sys.executable
    before = _git_status_porcelain(ws)
    print("AC4: git status --porcelain BEFORE (%d line(s)):\n%s" % (len(before.splitlines()), before.rstrip()))

    scratch_root = ws / ".scratch" / ("og_q4_mutant_%d" % int(time.time()))
    if scratch_root.exists():
        shutil.rmtree(scratch_root)
    src_gateway = ws / "infra" / "aws" / "ec2" / "opal-gateway"
    dst_gateway = scratch_root / "opal-gateway"
    shutil.copytree(src_gateway, dst_gateway, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print("AC4: copied %s -> %s (%d bytes source-side app/ dir)"
         % (src_gateway, dst_gateway, sum(f.stat().st_size for f in (src_gateway / "app").rglob("*") if f.is_file())))

    pre_wiring = subprocess.run(["git", "show", "HEAD:%s" % _REAL_QUERY_PY], cwd=str(ws),
                                capture_output=True, check=True)
    mutant_query_py = dst_gateway / "app" / "integrations" / "schwab" / "query.py"
    wired_bytes = mutant_query_py.read_bytes()
    mutant_query_py.write_bytes(pre_wiring.stdout)
    same = wired_bytes == pre_wiring.stdout
    print("AC4: mutant query.py written at %s (%d bytes, HEAD:%s); differs from the copy's wired bytes: %s"
         % (mutant_query_py, len(pre_wiring.stdout), _REAL_QUERY_PY, not same))
    if same:
        # HEAD already carries no call site to remove -- the mutant would be a no-op control, not a mutant.
        print("VERDICT: FAIL-OGQ4-AC4 HEAD:%s is byte-identical to the worktree copy -- no call site to "
             "remove, the mutant control cannot discriminate" % _REAL_QUERY_PY)
        return 1

    # scratch-depth fact (see module docstring): point the copy's contract loader at the REAL, unmutated
    # contract file rather than let default_contract_path() mis-derive the root from the copy's own depth.
    real_contract = ws / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
    mutant_env = {"NFRA_OPLGTW_CONTRACT_PATH": str(real_contract)}

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


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in ("AC4", "AC5"):
        print("usage: og_q4.py AC4|AC5")
        return 2
    return {"AC4": ac4, "AC5": ac5}[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
