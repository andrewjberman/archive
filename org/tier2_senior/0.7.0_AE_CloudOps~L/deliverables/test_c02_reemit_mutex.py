#!/usr/bin/env python3
"""Unit arms for the C02-g-6 mutex predicate (2.0.0_SA_COO 85538, condition 3).

Required BEFORE the first write: an arm per limb, each proving the guard REFUSES in the state
it exists to refuse. A limb written for a state that is not present today is dead code that
passes by never being reached -- this fabric measured that class twice on 2026-08-30, so the
states are synthesized rather than waited for.

Run: python -m pytest test_c02_reemit_mutex.py -q   (from this directory)
"""

from __future__ import annotations

import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "drv", Path(__file__).with_name("ADVI_49F.c02-REEMIT_CAMPAIGN_DRIVER.py"))
drv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(drv)


class _Sched:
    def __init__(self, states):
        self._s = states

    def get_schedule(self, Name):  # noqa: N803 - boto3 kwarg name
        return {"State": self._s[Name], "ScheduleExpression": "cron(45 12 * * ? *)"}


class _Ssm:
    def __init__(self, commands):
        self._c = commands

    def list_commands(self, **_kw):
        return {"Commands": self._c}


@pytest.fixture(autouse=True)
def _restore():
    s, m = drv.sched, drv.ssm
    yield
    drv.sched, drv.ssm = s, m


def _wire(states, commands):
    drv.sched = lambda: _Sched(states)
    drv.ssm = lambda: _Ssm(commands)


BOTH_OFF = {"advi-49f-gold-floor": "DISABLED", "advi-49f-publisher": "DISABLED"}
FLOOR_ON = {"advi-49f-gold-floor": "ENABLED", "advi-49f-publisher": "DISABLED"}


def test_limb_i_passes_when_every_starter_is_disabled():
    """The hold form must still pass unchanged -- (b) adds a limb, it does not replace one."""
    _wire(BOTH_OFF, [])
    drv.check_mutex(projected_span_s=10 * 3600)  # span irrelevant under limb (i)


def test_limb_ii_REFUSES_inside_the_margin():
    """SYNTHETIC 30-MINUTE MARGIN: a span that does not fit before the fire must STOP.

    This is the arm that makes limb (ii) a control rather than a permission.
    """
    _wire(FLOOR_ON, [])
    now = datetime.now(timezone.utc)
    fire = drv._next_fire("cron(45 12 * * ? *)", now)
    # ask for a span that leaves only ~30 min of headroom against the real next fire
    span = (fire - now).total_seconds() - drv.MARGIN_S - 30 * 60
    with pytest.raises(SystemExit) as e:
        drv.check_mutex(projected_span_s=span + 31 * 60)
    assert "Inside the margin" in str(e.value)


def test_limb_ii_REFUSES_on_a_non_terminal_ssm_command():
    """SYNTHETIC IN-FLIGHT COMMAND: the campaign never coexists with a production run."""
    _wire(FLOOR_ON, [{"Status": "InProgress"}, {"Status": "Success"}])
    with pytest.raises(SystemExit) as e:
        drv.check_mutex(projected_span_s=60)
    assert "non-terminal SSM command" in str(e.value)


def test_limb_ii_PASSES_with_a_wide_margin_and_a_quiet_host():
    """POSITIVE CONTROL. Without this the two refusals above are satisfied by a guard that
    refuses unconditionally, which would block the campaign and look like safety."""
    _wire(FLOOR_ON, [{"Status": "Success"}, {"Status": "Cancelled"}])
    drv.check_mutex(projected_span_s=60)


def test_unparseable_cron_FAILS_CLOSED():
    """A margin computed from a misread expression is worse than no margin."""
    with pytest.raises(SystemExit) as e:
        drv._next_fire("rate(1 day)", datetime.now(timezone.utc))
    assert "cannot parse" in str(e.value)


def test_next_fire_rolls_to_tomorrow_when_todays_time_has_passed():
    """The margin must never be computed against a fire that already happened."""
    base = datetime(2026, 8, 30, 13, 0, 0, tzinfo=timezone.utc)  # after 12:45
    nxt = drv._next_fire("cron(45 12 * * ? *)", base)
    assert nxt == base.replace(hour=12, minute=45) + timedelta(days=1)
