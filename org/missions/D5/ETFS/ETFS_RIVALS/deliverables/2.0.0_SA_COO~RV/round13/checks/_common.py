"""Shared helpers for the ETFS_RIVALS round-12 checks (issuer-written, 2.0.0_SA_COO~RV): re-exports round 11's helpers
(Verdict, guarded, setup_path, tmpdir, the page fixture, offline_guards) and puts round 8's check folder on the path (its
`_ui7` renderer-fixture helpers and the fc-1 AC1 page fixture). Every round-12 check runs offline: no S3, no Lambda, no
vendor call."""
from __future__ import annotations

import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
_R11 = HERE.parents[1] / "round11" / "checks" / "_common.py"
_spec = importlib.util.spec_from_file_location("_rivals_r11_common", _R11)
_r11 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r11)

Verdict, guarded, setup_path, tmpdir, page_fixture, offline_guards = (
    _r11.Verdict, _r11.guarded, _r11.setup_path, _r11.tmpdir, _r11.page_fixture, _r11.offline_guards)
ROOT = HERE.parents[8]  # the worktree this check file lives in

R8 = HERE.parents[1] / "round8" / "checks"
if str(R8) not in sys.path:
    sys.path.insert(1, str(R8))


def load_fc1():
    """Round 8's fc-1 AC1 module with its fixture only (its own verdict never runs): IDVZ home, TXUE rival, Apple and
    Microsoft ranked and in the trend, one TXUE trade in Apple, one TXUE AI account naming AAPL_US_Equity."""
    p = R8 / "fc-1.AC1.py"
    src = p.read_text(encoding="utf-8")
    src = src[: src.index("failures = c.guarded(")]
    mod = type(sys)("fc1_ac1_fixture")
    mod.__file__ = str(p)
    exec(compile(src, str(p), "exec"), mod.__dict__)
    return mod
