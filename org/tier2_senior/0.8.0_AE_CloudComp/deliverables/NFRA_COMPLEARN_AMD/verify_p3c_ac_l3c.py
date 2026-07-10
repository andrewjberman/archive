"""
verify_p3c_ac_l3c -- NFRA_COMPLEARN AMD-P3c LANDING VERIFICATION (AC-L3c) against the LIVE module.

This is the exercise-gate for the P3c enforcer LAND. It imports the LIVE
org/modules/graph/comp_log_auto.py and forces each drop condition:

    RED   until the disclosure patch (P3c_comp_log_auto_disclosure.patch) lands -- the live module still
          swallows drops silently, so _disclose_drop is absent and CHECK 2-6 fail (BY DESIGN: this documents
          the pre-land state; a passing assertion never mutated has never been tested).
    GREEN after the patch lands -- every forced drop is DISCLOSED (count/marker/stderr); a normal run is
          untouched; the disclosure never disrupts the caller.

Run at LAND time (from workspace root):  python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_COMPLEARN_AMD/verify_p3c_ac_l3c.py
The identical pre-land GREEN proof (vs the staged copy) is .runtmp/p3c_comp_log_auto_disclosure/exercise_p3c.py.
ASCII-only, deterministic.  Author: 0.8.0_AE_CloudComp~E (NFRA_COMPLEARN AMD-P3c). 2026-07-10.
"""

from __future__ import annotations

import io
import os
import sys
import tempfile
from pathlib import Path

_WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", ".."))
_GRAPH = os.path.join(_WS, "org", "modules", "graph")
if _GRAPH not in sys.path:
    sys.path.insert(0, _GRAPH)
import comp_log_auto as cla  # noqa: E402 -- the LIVE module under verification

_DROPS = os.path.join(".comp-graph", ".comp_log_drops")


def _mk_ws() -> Path:
    ws = Path(tempfile.mkdtemp(prefix="p3c_verify_"))
    (ws / ".comp-graph").mkdir(parents=True, exist_ok=True)
    (ws / "org").mkdir(parents=True, exist_ok=True)
    return ws


def _drop_lines(ws: Path) -> list:
    f = ws / _DROPS
    return [ln for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()] if f.exists() else []


def run() -> tuple[bool, list]:
    checks: list = []

    def ck(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        return ok

    has_disclose = hasattr(cla, "_disclose_drop")
    ck("disclosure_present_in_live_module", has_disclose,
       "live comp_log_auto exposes _disclose_drop" if has_disclose
       else "NOT YET LANDED -- live module still swallows drops (expected pre-land)")
    if not has_disclose:
        # Pre-land: the remaining checks cannot exercise disclosure that does not exist. Record + stop.
        return False, checks

    # CHECK 1 -- normal run: writable log -> row appends, no false drop.
    ws1 = _mk_ws()
    (ws1 / "org" / "compiler-tools-log.md").write_text("| DATE |\n", encoding="utf-8")
    cla._append_log(ws1, "comp-grep", "pat path", 0, "0.8.0_AE_CloudComp~E", "NFRA_COMPLEARN.AMD-P3c")
    ck("normal_run_no_false_drop",
       "comp-grep" in (ws1 / "org" / "compiler-tools-log.md").read_text(encoding="utf-8") and not _drop_lines(ws1))

    # CHECK 2 -- log absent -> 'log-file-absent' disclosed.
    ws2 = _mk_ws()
    cla._append_log(ws2, "comp-blast", "fn", 0, "s", "t")
    d2 = _drop_lines(ws2)
    ck("drop_disclosed_log_absent", len(d2) == 1 and "log-file-absent" in d2[0] and "comp-blast" in d2[0], f"{d2}")

    # CHECK 3 -- append fails (log is a dir) -> 'append-failed' disclosed.
    ws3 = _mk_ws()
    (ws3 / "org" / "compiler-tools-log.md").mkdir()
    cla._append_log(ws3, "comp-iam", "service x", 0, "s", "t")
    d3 = _drop_lines(ws3)
    ck("drop_disclosed_append_fail", len(d3) == 1 and "append-failed" in d3[0], f"{d3}")

    # CHECK 4 -- count accrues.
    ws4 = _mk_ws()
    for i in range(3):
        cla._append_log(ws4, f"comp-t-{i}", "a", 0, "s", "t")
    ck("count_accrues", len(_drop_lines(ws4)) == 3, f"lines={len(_drop_lines(ws4))}")

    # CHECK 5 -- stderr last resort (workspace=None).
    cap, old = io.StringIO(), sys.stderr
    sys.stderr = cap
    try:
        cla._disclose_drop(None, "comp-freshness", "main-exception: RuntimeError")
    finally:
        sys.stderr = old
    ck("stderr_last_resort", "COMP_LOG_AUTO_DROP" in cap.getvalue() and "comp-freshness" in cap.getvalue())

    # CHECK 6 -- never raises (unwritable marker + closed stderr).
    import shutil
    ws6 = _mk_ws()
    shutil.rmtree(ws6 / ".comp-graph")
    (ws6 / ".comp-graph").write_text("not-a-dir", encoding="utf-8")
    closed, old2 = io.StringIO(), sys.stderr
    closed.close()
    sys.stderr = closed
    raised = None
    try:
        cla._disclose_drop(ws6, "comp-x", "append-failed: OSError")
    except Exception as e:  # noqa: BLE001
        raised = e
    finally:
        sys.stderr = old2
    ck("disclosure_never_raises", raised is None, f"raised={raised!r}")

    for ws in (ws1, ws2, ws3, ws4, ws6):
        import shutil as _sh
        _sh.rmtree(ws, ignore_errors=True)
    return all(c["pass"] for c in checks), checks


def main() -> int:
    ok, checks = run()
    print("=== verify_p3c_ac_l3c -- AC-L3c LANDING VERIFICATION (vs LIVE comp_log_auto) ===")
    for c in checks:
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['check']}" + (f"   ({c['detail']})" if c.get("detail") else ""))
    print("\n" + ("OK: AC-L3c holds against the LIVE module -- the disclosure has landed and works"
                  if ok else "PENDING/FAIL: disclosure not yet landed OR a check failed (RED pre-land is BY DESIGN)"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
