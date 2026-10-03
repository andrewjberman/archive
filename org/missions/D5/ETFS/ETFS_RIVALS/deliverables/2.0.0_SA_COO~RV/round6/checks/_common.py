"""Shared helpers for the ETFS_RIVALS round-6 checks (issuer-written, 2.0.0_SA_COO~RV): re-exports round 5's helpers (Verdict,
guarded, the page fixture, the A1/AI fixtures). Every check runs offline on a `local:` sink unless its docstring says it reads S3
(READ-ONLY)."""
from __future__ import annotations

import importlib.util
import pathlib

_R5 = pathlib.Path(__file__).resolve().parents[2] / "round5" / "checks" / "_common.py"
_spec = importlib.util.spec_from_file_location("_rivals_r5_common", _R5)
_r5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r5)

Verdict, guarded, setup_path, tmpdir = _r5.Verdict, _r5.guarded, _r5.setup_path, _r5.tmpdir
page_fixture, ai2_tables, ai2_readings, ai2_reply, StubClient, AI_DAY = (
    _r5.page_fixture, _r5.ai2_tables, _r5.ai2_readings, _r5.ai2_reply, _r5.StubClient, _r5.AI_DAY)

ROOT = pathlib.Path(__file__).resolve().parents[9]  # the worktree the check runs in


def contribution_rows(fund: str, period: str, values: dict) -> list[dict]:
    """Security-axis holding_contribution rows in the A1 contract for one fund x period: {bucket: contribution}."""
    rows = []
    for i, (b, v) in enumerate(sorted(values.items(), key=lambda kv: -kv[1])):
        rows.append({"fund_id": fund, "role": "rival", "period": period, "period_start": "2026-01-02", "period_end": "2026-10-01",
                     "axis": "security", "bucket": b, "security_name": b, "contribution": v, "price_coverage": "full",
                     "n_days_priced": 20, "n_days_period": 20, "rank_best": i + 1, "rank_worst": len(values) - i,
                     "n_ranked": len(values), "n_missing": 0, "claim": "INFERRED", "revision": "fx"})
    return rows
