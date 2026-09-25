#!/usr/bin/env python3
"""NFRA_MCPINDEX MX-c-4 probe -- MXC4-AC1 .. AC12 (AC8 is judgment; no probe call for it).

Run from <WS> (the invocation always `cd`s there first): `python <this> AC<n>` (device-neutral
interpreter, row W1-S6; MX-c-5 conformed AC6, AC10 and AC11 to the CTO's ruling R-1 @9c70622d13).
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
# MX-c-5 conform: BEFORE is the MX-c-5 cell's BASE commit (below), the WHOLE gateway app/ tree at that
# commit's bytes (so the three integration directories this cell edits are reverted too -- the MX-c-4
# snapshot reverted only its own 4 files, which at this base are HEAD's bytes, so it compared the tree
# with itself). Both sides register the DEPLOYED enabled set first: destructive_ops.classify composes an
# integration's declared class only through a spec that register_enabled made active.

MXC5_BASE = "97f1aad836"   # issue-carry of NFRA_MCPINDEX.TO-MX-c-5 onto wk-nfra_mcpindex-1-1d (MX-c-4 build)
DEPLOY_SCRIPT = GW / "deploy-to-ec2.sh"

# The reason for each class MX-c-5 declares, as STATED by 0.9.0_WK_NFRA_MCPINDEX~1 (claim: held -- the
# worker's reading of each tool's code, graded at L9 as MXC5-AC4; the probe prints it, never grades it).
MXC5_REASONS = {
    "ycharts_freshness": "one GET /indices/table_data liveness read; no YCharts state mutated",
    "ycharts_snapshot_metrics": "one GET /indices/table_data; snapshot values read",
    "ycharts_time_series": "one GET /charts/general_data.json; history series read",
    "ycharts_fund_series": "one GET /charts/fund_data.json; daily series read",
    "ycharts_risk_return_scatter": "one POST /charts/scatter_plot_data.json carrying only security ids "
                                   "and two metric names; a query-POST returning computed chart data, "
                                   "nothing saved or changed",
    "ycharts_search": "one GET /search/suggest/main; name/ticker resolution",
    "graph_cypher": "statement proxied verbatim to the projection service, which opens Kuzu "
                    "read_only=True (projection_server.py KuzuAdapter.open_read_only); a write is "
                    "refused by the engine",
    "graph_status": "one GET /health on the projection service",
    "opal_data_refresh_upload": "a WRITE: PUTs 2 PKLs to presigned S3 URLs and POSTs /trigger, firing "
                                "the live yang-pipeline (unrecallable); dry_run still writes pending/. "
                                "IRREVERSIBLE_SEND = same class and flags as the fail-closed default",
}


def deployed_enabled_ids() -> list:
    """ENABLED_INTEGRATIONS as the deploy writes it into the box's .env (deploy-to-ec2.sh); the
    gateway's own config default (env, empty on this box) is printed beside it, never substituted."""
    text = DEPLOY_SCRIPT.read_text(encoding="utf-8")
    hits = re.findall(r"ENABLED_INTEGRATIONS=([A-Za-z0-9_ ,]+?)(?:\\n|['\"\n])", text)
    if len(hits) != 1:
        raise RuntimeError("expected exactly 1 ENABLED_INTEGRATIONS= value in %s, found %d: %r"
                           % (DEPLOY_SCRIPT, len(hits), hits))
    return [s for s in hits[0].replace(",", " ").split() if s]


_CLASSIFY_SNIPPET = r"""
import sys, json
sys.path.insert(0, ".")
enabled = json.loads(sys.argv[1])
from app import destructive_ops as dop
from app import data_entitlement as de
from app import config as _cfg
from app.integrations import registry as _r
class _M:
    def tool(self, *a, **k):
        return lambda fn: fn
report = _r.register_enabled(_M(), enabled)
registered = {iid: sorted(_r._FACTORIES[iid]().register(_M())) for iid in _r.available_ids()}
names = sorted(de.NATIVE_TOOLS | de.INTEGRATION_TOOLS | frozenset(de.SCHWAB_TOOLS))
out = {}
for n in names:
    tag = dop.classify(n)
    out[n] = {"dop_class": tag["class"].value, "dop_unclassified": bool(tag.get("unclassified")),
             "de_class": de.classify(n)}
env_enabled = list(_cfg.get_config().ENABLED_INTEGRATIONS) if hasattr(_cfg, "get_config") else None
print(json.dumps({"names": names, "by_name": out, "registered": registered,
                  "report": {k: sorted(v.get("tools", [])) for k, v in report.items()},
                  "env_enabled": env_enabled}))
"""


def _classify_all(gw_root: Path, enabled: list) -> dict:
    res = subprocess.run([PY, "-c", _CLASSIFY_SNIPPET, json.dumps(enabled)], cwd=str(gw_root),
                         capture_output=True, text=True, timeout=60)
    if res.returncode != 0:
        raise RuntimeError("classify snippet failed rc=%d stderr=%s" % (res.returncode, res.stderr[-2000:]))
    return json.loads(res.stdout.strip().splitlines()[-1])


def _snapshot_base(tmp_root: Path) -> Path:
    """The gateway tree with every tracked app/ file set to MXC5_BASE's bytes (binary, via git show)."""
    dest = tmp_root / "opal-gateway"
    shutil.copytree(GW, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.rmtree(dest / "app")
    prefix = "infra/aws/ec2/opal-gateway/"
    listing = subprocess.run(["git", "ls-tree", "-r", "--name-only", MXC5_BASE, "--", prefix + "app"],
                             cwd=str(WS), capture_output=True, text=True, check=True).stdout.split("\n")
    files = [p for p in listing if p]
    if not files:
        raise RuntimeError("git ls-tree returned 0 files for %s at %s" % (prefix + "app", MXC5_BASE))
    for p in files:
        blob = subprocess.run(["git", "show", "%s:%s" % (MXC5_BASE, p)], cwd=str(WS),
                              capture_output=True, check=True).stdout
        out = dest / p[len(prefix):]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(blob)
    print("BASE snapshot: %d tracked app/ file(s) at %s" % (len(files), MXC5_BASE))
    return dest


def ac6():
    enabled = deployed_enabled_ids()
    print("ENABLED_INTEGRATIONS (deployed, %s): %r" % (DEPLOY_SCRIPT.relative_to(WS).as_posix(), enabled))
    with tempfile.TemporaryDirectory(prefix="mxc5_base_") as td:
        before = _classify_all(_snapshot_base(Path(td)), enabled)
    after = _classify_all(GW, enabled)
    print("ENABLED_INTEGRATIONS (gateway config default on this box, env): %r" % after["env_enabled"])
    names = sorted(set(before["names"]) | set(after["names"]))
    enabled_tools = {t for iid in enabled for t in after["registered"].get(iid, [])}
    expected_new = sorted(n for n in names if before["by_name"][n]["dop_unclassified"] and n in enabled_tools)
    diffs = {n: (before["by_name"].get(n), after["by_name"].get(n)) for n in names
             if before["by_name"].get(n) != after["by_name"].get(n)}
    kept = [n for n in names if n not in expected_new]
    kept_changed = sorted(n for n in kept if n in diffs)
    print("DENOMINATOR %d tool name(s) (union of before/after NATIVE_TOOLS|INTEGRATION_TOOLS|SCHWAB_TOOLS)"
          % len(names))
    print("KEEP: %d tool(s) outside the newly-classified set; %d changed class -> %r"
          % (len(kept), len(kept_changed), kept_changed))
    for n in kept_changed:
        print("  CHANGED %s before=%s after=%s" % (n, json.dumps(diffs[n][0]), json.dumps(diffs[n][1])))
    print("NEWLY CLASSIFIED: %d tool(s) unclassified at %s whose integration is enabled:" % (len(expected_new), MXC5_BASE))
    not_classified = []
    for n in expected_new:
        a = after["by_name"][n]
        if a["dop_unclassified"]:
            not_classified.append(n)
        print("  %-28s %s -> %s%s   reason: %s"
              % (n, before["by_name"][n]["dop_class"] + "(unclassified)", a["dop_class"],
                 "(unclassified)" if a["dop_unclassified"] else "", MXC5_REASONS.get(n, "NO REASON STATED")))
    missing_reason = [n for n in expected_new if n not in MXC5_REASONS]
    ok = (len(names) == 49 and len(kept) == 40 and not kept_changed and len(expected_new) == 9
          and not not_classified and not missing_reason)
    _verdict(ok, "AC6", "" if ok else
             "denominator=%d kept=%d kept_changed=%d newly=%d still_unclassified=%r missing_reason=%r"
             % (len(names), len(kept), len(kept_changed), len(expected_new), not_classified, missing_reason))


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
# MX-c-4's cut (2026-09-21, before any MX-c-4 edit, `py -3.12`, the 10 SCOPED_FILES): 1 failed, 130 passed.
# MX-c-5 conform: BEFORE is re-MEASURED at THIS cell's base -- 2026-09-25, worktree at 97f1aad836 with no
# MX-c-5 edit, `python` 3.11.9, via this function over the same 11 files the AFTER run uses (the 10
# SCOPED_FILES + tests/test_tool_classification_composition.py, which exists at this base).
BEFORE_SUMMARY = {"passed": 137, "failed": 1,
                 "raw": "1 failed, 137 passed, 56 warnings, 34 subtests passed in 14.64s",
                 "base": "97f1aad836", "interpreter": "python 3.11.9",
                 "failed_nodeids": ["tests/test_identity_scope.py::test_scoped_deny_by_default"]}
SCOPE_NOTE = (
    "[Carried from MX-c-4's cut (2026-09-21, py -3.12); not re-measured by MX-c-5 except that "
    "`moto` is still absent under `python` 3.11.9.]\n"
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
    print("BEFORE (the same %d files at this cell's base): %s" % (len(files), json.dumps(BEFORE_SUMMARY)))
    print("AFTER  (the same %d files, this worktree): failed=%d passed=%d nodeids=%r"
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


# --- AC11: C2's bar, exercised over the real registered population -----------------------------------
# AMENDED (issuer commit 0bec07601a, per the CTO's ruling @5f3b4a20c6): AC11 grades exactly the two
# registry limbs -- destructive_ops.classify and data_entitlement -- by name, over every registered
# tool. The catalog-entry limb is struck from this criterion; it is graded on each tool's own shipping
# cell (MX-t-1 .. MX-t-7).

# MX-c-5 conform (CTO ruling R-1 @9c70622d13, item 3): the denominator stays 49 and is graded as
# 44 classified + 5 HELD (G-OPLGTW). A HELD name is a schwab tool that is registered (the schwab
# factory's register() returns it) but whose integration is absent from ENABLED_INTEGRATIONS as
# deployed. Classification is read after register_enabled(<deployed set>), the only route by which an
# integration's declared class becomes visible to destructive_ops.classify. PASS only when the
# unclassified set IS the HELD set, exactly 5, and every tool clears data_entitlement.

def ac11():
    enabled = deployed_enabled_ids()
    after = _classify_all(GW, enabled)
    tools = after["names"]
    schwab_registered = set(after["registered"].get("schwab", []))
    held = sorted(t for t in schwab_registered if "schwab" not in enabled and t in tools)
    fail_dop = sorted(t for t in tools if after["by_name"][t]["dop_unclassified"])
    fail_de = sorted(t for t in tools if after["by_name"][t]["de_class"] is None)
    classified = [t for t in tools if t not in fail_dop]
    unheld_unclassified = sorted(set(fail_dop) - set(held))
    held_but_classified = sorted(set(held) - set(fail_dop))
    print("ENABLED_INTEGRATIONS (deployed, %s): %r" % (DEPLOY_SCRIPT.relative_to(WS).as_posix(), enabled))
    print("ENABLED_INTEGRATIONS (gateway config default on this box, env): %r" % after["env_enabled"])
    print("registered by integration: %s" % json.dumps(after["registered"], sort_keys=True))
    print("DENOMINATOR %d registered tool name(s) (NATIVE_TOOLS | INTEGRATION_TOOLS | SCHWAB_TOOLS)"
          % len(tools))
    print("%d = %d classified + %d HELD (G-OPLGTW)" % (len(tools), len(classified), len(held)))
    print("HELD (schwab, registered, not in ENABLED_INTEGRATIONS): %d -> %r" % (len(held), held))
    print("fails destructive_ops.classify (no declared class): %d -> %r" % (len(fail_dop), fail_dop))
    print("  of which NOT held: %d -> %r" % (len(unheld_unclassified), unheld_unclassified))
    print("  held but classified: %d -> %r" % (len(held_but_classified), held_but_classified))
    print("fails data_entitlement.classify (returns None): %d -> %r" % (len(fail_de), fail_de))
    ok = (len(tools) == 49 and len(held) == 5 and len(classified) == 44
          and not unheld_unclassified and not held_but_classified and not fail_de)
    _verdict(ok, "AC11",
             "%d = %d classified + %d HELD; unheld unclassified=%r; held but classified=%r; de fails=%r"
             % (len(tools), len(classified), len(held), unheld_unclassified, held_but_classified, fail_de))


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
