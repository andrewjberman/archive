"""MDPF_ASSETS.017 -- day-1-zero guard acceptance probe.

Exercises assert_model_aum_plausible() from
data/mdpf/scripts/backfill/build_legacy_compat_emit.py in isolation.

AC1 -- anchor reproduction: forced today model_aum=$0.00 -> guard raises.
AC2 -- false-positive smoke: real Schwab-clean 49F 1a -> guard does NOT raise.
AC3 -- cross-empirical: each of the 7 known 2026 SmartX zero-dates as a
       fixture (model_aum=$0.00) -> guard raises on every one.
Bonus -- DoD-band check: a 30% single-day collapse (above floor) -> guard
       raises on the day-over-day tolerance, not the absolute floor.

Run:  python org/tier2_senior/0.4.0_DS_ClientPlatform/probes/mdpf_assets_017_day1_zero_guard_probe.py
"""
from __future__ import annotations

import os
import sys

_BACKFILL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))))),
    "data", "mdpf", "scripts", "backfill")
sys.path.insert(0, _BACKFILL_DIR)

from build_legacy_compat_emit import (  # noqa: E402
    MIN_PLAUSIBLE_49F_MODEL_AUM,
    MODEL_AUM_DOD_TOLERANCE,
    Day1ZeroGuardError,
    assert_model_aum_plausible,
)

# Representative real 49F 1a model_aum on a Schwab-clean date
# (2026-05-18 platinum partition: partner 49financial model_aua).
REAL_49F_MODEL_AUM = 1_340_415_278.02

# The 7 known 2026 SmartX day-1-of-period zero-emission dates.
ZERO_DATES = [
    "2026-01-02", "2026-01-03", "2026-01-04",
    "2026-02-02", "2026-03-02", "2026-04-01", "2026-05-01",
]

_passed = 0
_failed = 0


def _expect_raise(label: str, period: str, model_aum, prior) -> None:
    global _passed, _failed
    try:
        assert_model_aum_plausible(period, model_aum, prior)
    except Day1ZeroGuardError as exc:
        print(f"  PASS [{label}] {period}: guard RAISED -- {exc}")
        _passed += 1
    else:
        print(f"  FAIL [{label}] {period}: guard did NOT raise "
              f"(model_aum={model_aum}, prior={prior})")
        _failed += 1


def _expect_clean(label: str, period: str, model_aum, prior) -> None:
    global _passed, _failed
    try:
        assert_model_aum_plausible(period, model_aum, prior)
    except Day1ZeroGuardError as exc:
        print(f"  FAIL [{label}] {period}: guard RAISED on a clean input "
              f"-- {exc}")
        _failed += 1
    else:
        print(f"  PASS [{label}] {period}: guard quiet "
              f"(model_aum=${model_aum:,.2f}, prior="
              f"${prior:,.2f})" if prior is not None else
              f"  PASS [{label}] {period}: guard quiet "
              f"(model_aum=${model_aum:,.2f}, prior=None)")
        _passed += 1


def main() -> int:
    print("=" * 70)
    print("MDPF_ASSETS.017 day-1-zero guard acceptance probe")
    print(f"  MIN_PLAUSIBLE_49F_MODEL_AUM = ${MIN_PLAUSIBLE_49F_MODEL_AUM:,.2f}")
    print(f"  MODEL_AUM_DOD_TOLERANCE     = {MODEL_AUM_DOD_TOLERANCE * 100:.0f}%")
    print("=" * 70)

    print("\n--- AC1: anchor reproduction (forced today model_aum=$0.00) ---")
    _expect_raise("AC1", "2026-06-01", 0.0, REAL_49F_MODEL_AUM)

    print("\n--- AC2: false-positive smoke (real Schwab-clean 49F 1a) ---")
    _expect_clean("AC2", "2026-05-19", REAL_49F_MODEL_AUM, REAL_49F_MODEL_AUM)

    print("\n--- AC3: cross-empirical 7 zero-date fixtures (model_aum=$0.00) ---")
    for zd in ZERO_DATES:
        _expect_raise("AC3", zd, 0.0, REAL_49F_MODEL_AUM)

    print("\n--- Bonus: DoD-band check (30% collapse, above $500M floor) ---")
    # 0.70 * REAL = $938.3M -- above the $500M floor, but a 30% DoD swing,
    # so the day-over-day tolerance gate (not the floor) must catch it.
    _expect_raise("DoD", "2026-06-01", REAL_49F_MODEL_AUM * 0.70,
                  REAL_49F_MODEL_AUM)
    # And a within-band 5% move stays quiet.
    _expect_clean("DoD", "2026-05-19", REAL_49F_MODEL_AUM * 0.95,
                  REAL_49F_MODEL_AUM)

    print("\n" + "=" * 70)
    print(f"RESULT: {_passed} passed, {_failed} failed")
    print("=" * 70)
    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
