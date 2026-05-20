"""MDPF_ASSETS.019 -- reconcile-block sentinels acceptance probe.

Exercises the three MDPF_ASSETS.019 sentinels in reconcile() from
data/mdpf/scripts/gold/mdpf_aggregate_aua.py, in isolation.

AC1 -- SENTINEL 1 (day-over-day Cohort 0): synthetic >50% move -> ERROR;
       clean small move -> quiet.
AC2 -- SENTINEL 2 (partners-present): replay the 5/19 missing-partner state
       -> ERROR ("inflection ... MISSING"); both partners present -> quiet;
       pre-onboard date with 49F-only -> quiet (no .016-backfill false-trip).
AC3 -- SENTINEL 3 (2nd-producer cross-validation): inject a 5% divergence
       between WS-A opal_aggregate_aua and the feeder-direct recompute
       -> ERROR; matched -> quiet.

Run:  python org/tier2_senior/0.4.0_DS_ClientPlatform/probes/mdpf_assets_019_sentinels_probe.py
"""
from __future__ import annotations

import os
import sys

_GOLD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))))),
    "data", "mdpf", "scripts", "gold")
sys.path.insert(0, _GOLD_DIR)

import pandas as pd  # noqa: E402

from mdpf_aggregate_aua import (  # noqa: E402
    COHORT0_DOD_THRESHOLD,
    FEEDER_COLUMNS,
    XPROD_DIVERGENCE_TOLERANCE,
    reconcile,
)

_passed = 0
_failed = 0


def _empty(artifact: str) -> pd.DataFrame:
    return pd.DataFrame(columns=FEEDER_COLUMNS[artifact])


def _partner(firm_id: str, model: float = 0.0, sma: float = 0.0,
             non_model: float = 0.0) -> dict:
    return {
        "firm_id": firm_id, "partner_name": firm_id,
        "model_aua": model, "sma_aua": sma, "non_model_aua": non_model,
        "total_aua": round(model + sma + non_model, 2),
        "partner_custody_total": 0.0, "by_model": [],
    }


def _check(label: str, got: str, expected: str, detail: str = "") -> None:
    global _passed, _failed
    ok = got == expected
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {label}: status={got} (expected {expected})"
          + (f" -- {detail}" if detail else ""))
    if ok:
        _passed += 1
    else:
        _failed += 1


def main() -> int:
    print("=" * 72)
    print("MDPF_ASSETS.019 reconcile-block sentinels acceptance probe")
    print(f"  COHORT0_DOD_THRESHOLD      = {COHORT0_DOD_THRESHOLD * 100:.0f}%")
    print(f"  XPROD_DIVERGENCE_TOLERANCE = "
          f"{XPROD_DIVERGENCE_TOLERANCE * 100:.0f}%")
    print("=" * 72)

    # ---- AC1: SENTINEL 1 -- day-over-day Cohort 0 plausibility ----
    print("\n--- AC1: sentinel 1 (DoD Cohort 0) ---")
    # Catastrophic move: today $40M vs prior $91.31M = -56% (> 50%).
    agg_drop = {"opal_aggregate_aua": 0.0, "etf_public_residual_total": 40_000_000.0}
    r = reconcile([], [], _empty("model_aua_positions"),
                  _empty("non_model_aua"), agg_drop, "2026-06-01",
                  prior_cohort0=91_310_000.0)
    _check("AC1 catastrophic -56% Cohort 0 move",
           r["sentinel_1_cohort0_dod"]["status"], "ERROR",
           r["sentinel_1_cohort0_dod"]["detail"])
    # Clean move: today $92.4M vs prior $91.31M = +1.2%.
    agg_ok = {"opal_aggregate_aua": 0.0, "etf_public_residual_total": 92_400_000.0}
    r = reconcile([], [], _empty("model_aua_positions"),
                  _empty("non_model_aua"), agg_ok, "2026-06-01",
                  prior_cohort0=91_310_000.0)
    _check("AC1 clean +1.2% Cohort 0 move",
           r["sentinel_1_cohort0_dod"]["status"], "PASS",
           r["sentinel_1_cohort0_dod"]["detail"])
    # Zero/absent prior: DoD not meaningful -> SKIP (the .016 backfill 0->real
    # transition + first-date + local-fixture cases).
    r = reconcile([], [], _empty("model_aua_positions"),
                  _empty("non_model_aua"), agg_ok, "2026-06-01",
                  prior_cohort0=None)
    _check("AC1 absent prior -> SKIP (backfill/first-date safety)",
           r["sentinel_1_cohort0_dod"]["status"], "SKIP")

    # ---- AC2: SENTINEL 2 -- expected partners present ----
    print("\n--- AC2: sentinel 2 (partners-present) ---")
    agg0 = {"opal_aggregate_aua": 0.0, "etf_public_residual_total": None}
    # Replay the 2026-05-19 incident: 49F-only partition on a >=05-18 date.
    r = reconcile([_partner("49financial", 1_340_000_000.0)], [],
                  _empty("model_aua_positions"), _empty("non_model_aua"),
                  agg0, "2026-05-19")
    _check("AC2 replay 5/19 (49F-only, inflection missing)",
           r["sentinel_2_partners_present"]["status"], "ERROR",
           r["sentinel_2_partners_present"]["detail"])
    # Clean: both expected partners present.
    r = reconcile([_partner("49financial", 1_340_000_000.0),
                   _partner("inflection", 93_000_000.0)], [],
                  _empty("model_aua_positions"), _empty("non_model_aua"),
                  agg0, "2026-05-19")
    _check("AC2 clean (both partners present)",
           r["sentinel_2_partners_present"]["status"], "PASS",
           r["sentinel_2_partners_present"]["detail"])
    # Pre-onboard date: 49F-only is correct -> no false-trip on .016 backfill.
    r = reconcile([_partner("49financial", 1_200_000_000.0)], [],
                  _empty("model_aua_positions"), _empty("non_model_aua"),
                  agg0, "2026-03-15")
    _check("AC2 pre-onboard 2026-03-15 (49F-only, backfill-safe)",
           r["sentinel_2_partners_present"]["status"], "PASS",
           r["sentinel_2_partners_present"]["detail"])

    # ---- AC3: SENTINEL 3 -- 2nd-producer cross-validation ----
    print("\n--- AC3: sentinel 3 (cross-validation) ---")
    # Feeders: positions model_value 100M + 60M (both cohort='model'),
    # non_model 25M + 15M -> independent recompute = 160M + 40M = 200M.
    pos = pd.DataFrame([
        ["49financial", "opal_intermediate", "model", "a1", 100_000_000.0],
        ["inflection", "opal_intermediate", "model", "a2", 60_000_000.0],
    ], columns=["firm_id", "model_key", "cohort_class", "account_id",
                "model_value"])
    nm = pd.DataFrame([
        ["49financial", 25_000_000.0],
        ["inflection", 15_000_000.0],
    ], columns=["firm_id", "non_model_aua"])
    # Matched: WS-A opal_aggregate_aua == 200M independent recompute.
    agg_match = {"opal_aggregate_aua": 200_000_000.0,
                 "etf_public_residual_total": None}
    r = reconcile([], [], pos, nm, agg_match, "2026-05-19")
    _check("AC3 matched (WS-A == feeder-direct $200M)",
           r["sentinel_3_cross_validation"]["status"], "PASS",
           r["sentinel_3_cross_validation"]["detail"])
    # Injected 5% divergence: WS-A claims 210M vs 200M independent.
    agg_div = {"opal_aggregate_aua": 210_000_000.0,
               "etf_public_residual_total": None}
    r = reconcile([], [], pos, nm, agg_div, "2026-05-19")
    _check("AC3 injected +5% divergence (WS-A $210M vs $200M)",
           r["sentinel_3_cross_validation"]["status"], "ERROR",
           r["sentinel_3_cross_validation"]["detail"])

    print("\n" + "=" * 72)
    print(f"RESULT: {_passed} passed, {_failed} failed")
    print("=" * 72)
    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
