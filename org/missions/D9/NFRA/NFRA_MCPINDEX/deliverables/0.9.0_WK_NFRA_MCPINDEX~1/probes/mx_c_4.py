#!/usr/bin/env python3
"""NFRA_MCPINDEX MX-c-4 probe -- MXC4-AC1 .. AC12 (AC8 is judgment; no probe call for it).

Run from <WS> (the invocation always `cd`s there first): `py -3.12 <this> AC<n>`.
Every mechanical criterion prints its measurement (instrument, denominator where the criterion
names one) and ends with exactly one `VERDICT: PASS-MXC4-AC<n>` or `VERDICT: FAIL-MXC4-AC<n> <reason>`
line. AC1-AC4, AC9's plant, AC12 reuse `tests/test_tool_classification_composition.py`'s planted
builders (imported, never duplicated) by running its pytest node directly -- one source of truth for
the planted-spec evidence. AC5, AC6, AC9's real half and AC11 measure the REAL registered population;
AC10 measures the Gateway suite's scoped subset (see SCOPE_NOTE for the exact denominator and why).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WS = Path.cwd()
GW = WS / "infra" / "aws" / "ec2" / "opal-gateway"
PY = sys.executable
CATALOG = GW / "app" / "refs" / "DATA_CATALOG.yaml"


def _verdict(ok: bool, ac: str, reason: str = "") -> None:
    if ok:
        print("VERDICT: PASS-MXC4-%s" % ac)
    else:
        print(("VERDICT: FAIL-MXC4-%s %s" % (ac, reason)).rstrip())


def _run(cmd, cwd, timeout=100):
    t0 = time.time()
    res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
    dt = time.time() - t0
    print("$ %s   (cwd=%s, %.2fs, rc=%d)" % (" ".join(cmd), cwd, dt, res.returncode))
    if res.stdout:
        print(res.stdout)
    if res.returncode != 0 and res.stderr.strip():
        print("--- stderr (rc!=0) ---")
        print(res.stderr[-4000:])
    return res


def _pytest_node(node):
    res = _run([PY, "-m", "pytest", "-q", "-s", node], cwd=GW, timeout=90)
    return res.returncode


# --- AC1 .. AC4: reuse the planted pytest nodes directly (one source of truth) --------------------

def ac1():
    rc = _pytest_node("tests/test_tool_classification_composition.py::test_mxc4_ac1")
    _verdict(rc == 0, "AC1", "pytest rc=%d" % rc)


def ac2():
    rc = _pytest_node("tests/test_tool_classification_composition.py::test_mxc4_ac2")
    _verdict(rc == 0, "AC2", "pytest rc=%d" % rc)


def ac3():
    rc = _pytest_node("tests/test_tool_classification_composition.py::test_mxc4_ac3")
    _verdict(rc == 0, "AC3", "pytest rc=%d" % rc)


def ac4():
    rc = _pytest_node("tests/test_tool_classification_composition.py::test_mxc4_ac4")
    _verdict(rc == 0, "AC4", "pytest rc=%d" % rc)


# --- shared: a faithful BEFORE snapshot (this worktree's cut commit, HEAD -- never inferred) -------

_TOUCHED = (
    "app/destructive_ops.py", "app/data_entitlement.py",
    "app/integrations/base.py", "app/integrations/registry.py",
)


def _snapshot_before(tmp_root: Path) -> Path:
    """A copy of the live gateway tree with exactly the files this cell writes reverted to their
    HEAD (pre-edit) bytes via `git show` -- everything else (the four real integrations' own
    directories included) is untouched, so a difference below is attributable to THIS cell's diff
    and nothing else."""
    dest = tmp_root / "opal-gateway"
    shutil.copytree(GW, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for rel in _TOUCHED:
        blob = subprocess.run(
            ["git", "show", "HEAD:infra/aws/ec2/opal-gateway/%s" % rel],
            cwd=str(WS), capture_output=True, text=True, check=True,
        ).stdout
        (dest / rel).write_text(blob, encoding="utf-8")
    new_test = dest / "tests" / "test_tool_classification_composition.py"
    if new_test.exists():
        new_test.unlink()   # did not exist at HEAD
    return dest


_REG_SNIPPET = r"""
import sys, json
sys.path.insert(0, ".")
from app.integrations import registry as _r
class _M:
    def __init__(self):
        self.names = []
    def tool(self, *a, **k):
        def d(fn):
            self.names.append(fn.__name__)
            return fn
        return d
out = {}
for iid in ["ycharts", "opal_portal", "globgrph", "schwab"]:
    f = _r._FACTORIES.get(iid)
    if f is None:
        out[iid] = None
        continue
    m = _M()
    f().register(m)
    out[iid] = sorted(m.names)
print(json.dumps(out))
"""


def _register_names(gw_root: Path) -> dict:
    res = subprocess.run([PY, "-c", _REG_SNIPPET], cwd=str(gw_root),
                         capture_output=True, text=True, timeout=60)
    if res.returncode != 0:
        raise RuntimeError("register snippet failed rc=%d stderr=%s" % (res.returncode, res.stderr[-2000:]))
    return json.loads(res.stdout.strip().splitlines()[-1])


def ac5():
    with tempfile.TemporaryDirectory(prefix="mxc4_before_") as td:
        before_root = _snapshot_before(Path(td))
        before = _register_names(before_root)
    after = _register_names(GW)
    print("BEFORE (HEAD %s, pre-edit):" % _head_short())
    print(json.dumps(before, indent=2, sort_keys=True))
    print("AFTER  (this worktree):")
    print(json.dumps(after, indent=2, sort_keys=True))
    ids_ok = set(before) == set(after) == {"ycharts", "opal_portal", "globgrph", "schwab"}
    names_ok = all(before[i] == after[i] and before[i] for i in before)
    ok = ids_ok and names_ok
    _verdict(ok, "AC5", "" if ok else "before/after id set or name set differs (printed above)")


def _head_short() -> str:
    return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(WS),
                          capture_output=True, text=True, check=True).stdout.strip()


# --- AC6: 49-name classification stability, before vs after ----------------------------------------

_CLASSIFY_SNIPPET = r"""
import sys, json
sys.path.insert(0, ".")
from app import destructive_ops as dop
from app import data_entitlement as de
names = sorted(de.NATIVE_TOOLS | de.INTEGRATION_TOOLS | frozenset(de.SCHWAB_TOOLS))
out = {}
for n in names:
    tag = dop.classify(n)
    out[n] = {"dop_class": tag["class"].value, "dop_unclassified": bool(tag.get("unclassified")),
             "de_class": de.classify(n)}
print(json.dumps({"names": names, "by_name": out}))
"""


def _classify_all(gw_root: Path) -> dict:
    res = subprocess.run([PY, "-c", _CLASSIFY_SNIPPET], cwd=str(gw_root),
                         capture_output=True, text=True, timeout=60)
    if res.returncode != 0:
        raise RuntimeError("classify snippet failed rc=%d stderr=%s" % (res.returncode, res.stderr[-2000:]))
    return json.loads(res.stdout.strip().splitlines()[-1])


def ac6():
    with tempfile.TemporaryDirectory(prefix="mxc4_before_") as td:
        before_root = _snapshot_before(Path(td))
        before = _classify_all(before_root)
    after = _classify_all(GW)
    names = sorted(set(before["names"]) | set(after["names"]))
    diffs = []
    for n in names:
        b, a = before["by_name"].get(n), after["by_name"].get(n)
        if b != a:
            diffs.append({"tool": n, "before": b, "after": a})
    ac7_owned = {"read_teams_attachment"}   # this cell's OWN deliberate change, graded by AC7/AC8
    unexpected = [d for d in diffs if d["tool"] not in ac7_owned]
    print("DENOMINATOR %d tool name(s) (union of before/after NATIVE_TOOLS|INTEGRATION_TOOLS|SCHWAB_TOOLS)"
         % len(names))
    print("all differences (%d): %s" % (len(diffs), json.dumps(diffs, indent=2)))
    print("differences EXCLUDING AC7's own read_teams_attachment change (%d): %s"
         % (len(unexpected), json.dumps(unexpected, indent=2)))
    ok = len(names) == 49 and not unexpected
    _verdict(ok, "AC6", "" if ok else "collateral difference(s) beyond AC7's own change, or denominator != 49")


# --- AC7: read_teams_attachment classified, no longer fail-closed-denied ---------------------------

def ac7():
    sys.path.insert(0, str(GW))
    from app import destructive_ops as dop     # noqa: E402
    from app import data_entitlement as de     # noqa: E402
    tag = dop.classify("read_teams_attachment")
    de_cls = de.classify("read_teams_attachment")
    print("destructive_ops.classify('read_teams_attachment') = %r" % tag)
    print("data_entitlement.classify('read_teams_attachment') = %r" % de_cls)
    print("'read_teams_attachment' in destructive_ops.SAFE_TOOLS = %r"
         % ("read_teams_attachment" in dop.SAFE_TOOLS))
    ok = (tag.get("unclassified") is not True) and (tag["class"] is dop.OpClass.SAFE) and (de_cls is not None)
    _verdict(ok, "AC7", "" if ok else "still fail-closed-denied or data_entitlement lost its classification")


# --- AC9: the planted difference (pytest) + the REAL population's derived pin, replayed here since
# test_entitlement_admin.py cannot collect on this box (moto missing, MEASURED once below) -----------

_PIN_SNIPPET = r"""
import sys, json
sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from app.integrations import registry as _r
from app import data_entitlement as de
import test_tool_classification_composition as tccomp
pinned = {
    "ycharts": ["ycharts_freshness", "ycharts_snapshot_metrics", "ycharts_time_series",
               "ycharts_fund_series", "ycharts_risk_return_scatter", "ycharts_search"],
    "opal_portal": ["opal_data_refresh_upload"],
    "globgrph": ["graph_cypher", "graph_status"],
    "schwab": ["schwab_get_access", "schwab_list_files", "schwab_describe_dataset",
              "schwab_query", "schwab_prepare_download"],
}
pinned = {k: frozenset(v) for k, v in pinned.items()}
actual = {}
for iid in _r.available_ids():
    actual[iid] = frozenset(_r._FACTORIES[iid]().register(tccomp.FakeMCP()))
mism = tccomp.diff_against_pin(pinned, actual)
registered = de.NATIVE_TOOLS | de.INTEGRATION_TOOLS
derived = len(de.NATIVE_TOOLS) + sum(len(v) for k, v in actual.items() if k != "schwab")
print(json.dumps({"mismatches": mism, "registered_len": len(registered), "derived_len": derived,
                  "actual": {k: sorted(v) for k, v in actual.items()}}))
"""


def ac9():
    rc = _pytest_node("tests/test_tool_classification_composition.py::test_mxc4_ac9_diff")
    res = subprocess.run([PY, "-c", _PIN_SNIPPET], cwd=str(GW), capture_output=True, text=True, timeout=60)
    print("$ real-population pin replay   (cwd=%s, rc=%d)" % (GW, res.returncode))
    if res.stdout:
        print(res.stdout)
    if res.returncode != 0:
        print(res.stderr[-2000:])
        _verdict(False, "AC9", "pin-replay snippet rc=%d" % res.returncode)
        return
    data = json.loads(res.stdout.strip().splitlines()[-1])
    real_ok = data["mismatches"] == [] and data["registered_len"] == data["derived_len"] == 44
    print("REAL POPULATION: mismatches=%r registered_len=%d derived_len=%d"
         % (data["mismatches"], data["registered_len"], data["derived_len"]))
    print("NOTE: tests/test_entitlement_admin.py:332's own assertion runs this identical composition "
         "in-file; it cannot be collected on this box today (see AC10's SCOPE_NOTE, moto missing, "
         "MEASURED, pre-existing) -- this replay is the same code path, run directly.")
    ok = (rc == 0) and real_ok
    _verdict(ok, "AC9", "" if ok else "planted diff test rc=%d or real pin mismatch=%r" % (rc, data["mismatches"]))


# --- AC10: Gateway suite counts, before vs after, over the scoped terminating subset ----------------

SCOPED_FILES = [
    "tests/test_attachment_tools.py", "tests/test_identity_scope.py", "tests/test_min_tier_gate.py",
    "tests/test_ratelimit.py", "tests/test_schwab_query.py", "tests/test_schwab_semantics.py",
    "tests/test_sprint_view.py", "tests/test_ssavail_contract.py", "tests/test_taxsma_workbook.py",
    "tests/test_teams_format.py",
]
# MEASURED 2026-09-21 (this cell's cut, before any MX-c-4 edit): `py -3.12 -m pytest <SCOPED_FILES> -q`.
BEFORE_SUMMARY = {"passed": 130, "failed": 1, "raw": "1 failed, 130 passed, 55 warnings, 34 subtests passed in 12.99s",
                 "failed_nodeids": ["tests/test_identity_scope.py::test_scoped_deny_by_default"]}
SCOPE_NOTE = (
    "SCOPE (denominator over the tracked Gateway test tree, 163 files, decomp s.7): this cell's own "
    "invocation budget (timeout 120) cannot run the FULL suite once -- MEASURED: `py -3.12 -m pytest "
    "tests -q --continue-on-collection-errors` did not finish inside 280s locally. Two exclusions, "
    "both MEASURED and pre-existing (present before this cell touched anything):\n"
    "  (a) 14 collection units (tests/acceptance/ + 13 tests/test_*.py files) fail to COLLECT with "
    "`ModuleNotFoundError: No module named 'moto'` on this box -- bound 14 ('a missing instrument is "
    "a refusal, never an install') forbids installing it here; --collect-only confirms 150 tests "
    "collected, 14 errors, in 1.13s.\n"
    "  (b) tests/test_schwab_engine.py (spawns a child job-runner process) did not terminate within "
    "100s locally and is excluded per bound 11 (every invocation terminates).\n"
    "The remaining 10 files (+ this cell's own new tests/test_tool_classification_composition.py, "
    "run separately by AC1-AC4/AC9) are exercised in full below."
)


def _parse_pytest_summary(stdout: str):
    failed_nodeids = sorted(set(re.findall(r"^FAILED (\S+)", stdout, re.M)))
    m = re.search(r"(\d+) failed", stdout)
    failed_n = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) passed", stdout)
    passed_n = int(m.group(1)) if m else 0
    return failed_n, passed_n, [f.replace("\\", "/") for f in failed_nodeids]


def ac10():
    print(SCOPE_NOTE)
    files = SCOPED_FILES + ["tests/test_tool_classification_composition.py"]
    res = _run([PY, "-m", "pytest", "-q", "--color=no"] + files, cwd=GW, timeout=100)
    failed_n, passed_n, failed_nodeids = _parse_pytest_summary(res.stdout)
    print("BEFORE (the %d pre-existing files only): %s" % (len(SCOPED_FILES), json.dumps(BEFORE_SUMMARY)))
    print("AFTER  (the same %d files + this cell's own new test file): failed=%d passed=%d nodeids=%r"
         % (len(files), failed_n, passed_n, failed_nodeids))
    before_failed = set(BEFORE_SUMMARY["failed_nodeids"])
    after_failed = set(failed_nodeids)
    newly_failing = after_failed - before_failed
    still_failing_same = after_failed & before_failed
    print("newly-failing (passed before, fails after): %r" % sorted(newly_failing))
    print("still-failing, SAME pre-existing test (not this cell's to fix, bound 17): %r"
         % sorted(still_failing_same))
    ok = res.returncode in (0, 1) and not newly_failing
    _verdict(ok, "AC10", "" if ok else "a test that passed before now fails, or pytest itself errored")


# --- AC11: C2's bar, exercised over the real registered population ---------------------------------

def _catalog_tool_refs() -> set:
    import yaml
    doc = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    refs: set = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ("tools", "tool_refs", "tool_ref"):
                    if isinstance(v, (list, tuple, set)):
                        refs.update(str(x) for x in v)
                    elif isinstance(v, str):
                        refs.add(v)
                walk(v)
        elif isinstance(node, (list, tuple)):
            for x in node:
                walk(x)

    walk(doc)
    return refs


def ac11():
    sys.path.insert(0, str(GW))
    from app import destructive_ops as dop     # noqa: E402
    from app import data_entitlement as de     # noqa: E402
    tools = sorted(de.NATIVE_TOOLS | de.INTEGRATION_TOOLS | frozenset(de.SCHWAB_TOOLS))
    catalog_refs = _catalog_tool_refs()
    print("CAT tool-reference fields found across the catalog (denominator of tool-naming fields "
         "'tools'/'tool_ref'/'tool_refs' anywhere in the parsed YAML): %d -> %r"
         % (len(catalog_refs), sorted(catalog_refs)))
    fail_dop, fail_de, fail_cat = [], [], []
    for t in tools:
        tag = dop.classify(t)
        if tag.get("unclassified"):
            fail_dop.append(t)
        if de.classify(t) is None:
            fail_de.append(t)
        if t not in catalog_refs:
            fail_cat.append(t)
    print("DENOMINATOR %d registered tool name(s) (NATIVE_TOOLS | INTEGRATION_TOOLS | SCHWAB_TOOLS)"
         % len(tools))
    print("fails destructive_ops.classify (no declared class): %d -> %r" % (len(fail_dop), fail_dop))
    print("fails data_entitlement.classify (returns None): %d -> %r" % (len(fail_de), fail_de))
    print("fails catalog-entry-reference resolution: %d -> %r" % (len(fail_cat), fail_cat))
    zero_fail = not fail_dop and not fail_de and not fail_cat
    _verdict(zero_fail, "AC11",
             "%d of %d tool(s) fail >=1 of the three axes (dop=%d de=%d catalog=%d); "
             "DATA_CATALOG.yaml carries 0 tool-reference fields today (MX-c-2/other cells' scope, "
             "not this cell's <paths>) so the catalog axis fails for every registered tool -- "
             "REFUSED per bound 9, measured above"
             % (len({*fail_dop, *fail_de, *fail_cat}), len(tools), len(fail_dop), len(fail_de), len(fail_cat)))


# --- AC12 -------------------------------------------------------------------------------------------

def ac12():
    rc = _pytest_node("tests/test_tool_classification_composition.py::test_mxc4_ac12")
    _verdict(rc == 0, "AC12", "pytest rc=%d" % rc)


_DISPATCH = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6, "AC7": ac7,
            "AC9": ac9, "AC10": ac10, "AC11": ac11, "AC12": ac12}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in _DISPATCH:
        print("usage: mx_c_4.py AC{1,2,3,4,5,6,7,9,10,11,12}   (AC8 is judgment, no probe call)")
        return 2
    _DISPATCH[sys.argv[1]]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
