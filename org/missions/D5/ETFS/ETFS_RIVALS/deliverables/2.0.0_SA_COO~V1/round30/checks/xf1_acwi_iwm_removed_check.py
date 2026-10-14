"""RIV-xf-1 checks (round 30): ACWI and IWM are removed from the universe and from the holdings pull (Andrew's DEMQUE form A3, row Z4;
CTO msgs 4932 and 4969). The map file `peer_groups.json` loses the two `"leg": "pending"` entries and the budget config
`bbg_budget.json` loses their two `est_rows_per_fund_date` keys; the generic `index_control` role and its row-cap machinery stay.

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: no Excel, no vendor call. DELTA = 0 for served output: with every gate unset (today's state: `leg_gates.json` reads
ENABLE 0, D12 1, D13 0) ACWI and IWM were already absent from `universe.funds()`, so the 13-fund list below is today's list.
"""
import json

import pytest

from rivalfunds import bbg_budget as bb
from rivalfunds import collector_bloomberg as cb
from rivalfunds import universe

THIRTEEN = ["IDVZ", "TXUE", "BIDD", "CGIC", "INEQ", "SCHY", "PFOE", "WCMG", "GQGU", "TSEL", "BASG", "ETFT", "PCLG"]
GONE = {"ACWI", "IWM"}


@pytest.fixture(autouse=True)
def _gates(monkeypatch):
    for g in universe.GATES:
        monkeypatch.delenv(g, raising=False)


@pytest.mark.parametrize("gates", [(), ("RIVALFUNDS_LEG_D13",), ("RIVALFUNDS_LEG_ENABLE",), ("RIVALFUNDS_LEG_D12", "RIVALFUNDS_LEG_D13")])
def test_ac1_no_gate_state_brings_acwi_or_iwm_back(monkeypatch, gates):
    for g in gates:
        monkeypatch.setenv(g, "1")
    funds = universe.funds()
    assert not GONE & set(funds)
    assert sorted(funds) == sorted(THIRTEEN) and len(funds) == 13        # the same 13 funds as before the change
    assert not GONE & {e["fund_id"] for e in universe.entries()}
    assert not any(e.get("role") == "index_control" for e in universe.entries())


BBG_PRIMARY = ["IDVZ", "TXUE", "BIDD", "CGIC", "INEQ", "SCHY", "PFOE"]   # the holdings plan's funds with every gate on: the bloomberg_primary set


def test_ac2_the_holdings_plan_is_the_bloomberg_primary_funds_with_every_gate_on_and_one_unit(monkeypatch):
    # AMENDMENT 1 (issuer, on row ETFS_RIVALS-D1-W42-S1): `request_plan` plans the `bloomberg_primary` funds only (7 with ENABLE on; the six
    # issuer_first funds are not Bloomberg-pulled), so the prior list was these 7 plus ACWI and IWM (9); the change removes exactly the two.
    monkeypatch.setenv("RIVALFUNDS_LEG_ENABLE", "1")
    plan = cb.request_plan("2026-09-29")
    assert sorted(plan["funds"]) == sorted(BBG_PRIMARY) and plan["names"] == 7
    assert not GONE & set(plan["funds"])
    units = cb.split_units(plan["funds"])
    assert units == [(plan["funds"], cb.RIVAL_ROW_CAP)]                  # no benchmark is queried on its own any more


def test_ac3_the_budget_config_no_longer_sizes_the_two_funds():
    cfg = json.loads(bb.CONFIG_PATH.read_text(encoding="utf-8"))
    est = cfg["est_rows_per_fund_date"]
    assert not GONE & set(est) and {"IDVZ", "PFOE", "default"} <= set(est)
    assert cfg["daily_ceiling_rows"] < 175000 and 0 < cfg["production_reserve_rows"] < cfg["daily_ceiling_rows"]
