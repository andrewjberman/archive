"""IRPT_ANLREQ AR-g-90: the issuer's own tests of the resident's Opal pricing binding (run by ar_g90_checks.py).

They reuse the package fixture, the fake clients and the helpers of reports/tests/test_resident_installed.py, so they build the real
runtime. They are the check, not the worker's tests: the worker's own file cannot weaken them.
"""
# ruff: noqa: F811  (a pytest fixture is imported, then named as a test argument)
import datetime
import json
from pathlib import Path
from types import SimpleNamespace
import sys

import pytest

TESTS = Path("infra/aws/lambda/investor-reporting/reports/tests").resolve()
sys.path.insert(0, str(TESTS))
from test_resident_installed import fake_clients, opal_record, package, rewrite, ri, sha  # noqa: E402,F401

PRINCIPAL = {"firm_id": "cottonwood", "principal_id": "nobody@example.invalid"}
CLOCK = 1_800_000_000  # 2027-01-15T08:00:00Z, a Friday


def epoch(day):
    return int(datetime.datetime.fromisoformat(day + "T08:00:00+00:00").timestamp())


def assembly_of(package, pricing=None, s3=None):
    path = package.root / "overview_map.json"
    path.write_text(json.dumps({"report_type": "overview", "elements": [], "calls": []}), encoding="utf-8")
    changes = {"opal_map": {"path": "overview_map.json", "sha256": sha(path)}}
    if pricing is not None:
        changes["opal_pricing"] = pricing
    rewrite(package, **changes)
    clients = {**fake_clients(), "opal_objects": lambda firm, rid: SimpleNamespace(put_object=None),
               "opal_classifier": lambda: SimpleNamespace(get_classification=None)}
    if s3 is not None:
        clients["s3"] = s3
    return ri.build_resident_runtime(package.path, clients=clients, clock=lambda: CLOCK)["assembly"]


def stores_of(assembly):
    record = opal_record(PRINCIPAL["principal_id"])
    record["ticket_confirmed"] = True
    return assembly.opal_stores(PRINCIPAL, record)


@pytest.mark.parametrize("pricing", [None, {"enabled": False, "tiers": []}, {"enabled": False, "tiers": ["estate"]}])
def test_absent_or_disabled_binding_adds_no_pricing_keys(package, pricing):
    stores = stores_of(assembly_of(package, pricing))
    assert "pricing" not in stores and "price_readers" not in stores and "as_of" not in stores


def test_enabled_binding_adds_the_priced_run_keys(package):
    stores = stores_of(assembly_of(package, {"enabled": True, "tiers": ["estate", "yfinance"]}))
    assert stores["pricing"] is True and sorted(stores["price_readers"]) == ["estate", "yfinance"]
    assert all(callable(r) for r in stores["price_readers"].values()) and stores["as_of"] == "2027-01-14"


def test_only_the_named_tiers_are_built(package):
    stores = stores_of(assembly_of(package, {"enabled": True, "tiers": ["yfinance"]}))
    assert list(stores["price_readers"]) == ["yfinance"]


def test_t_minus_1_is_the_previous_weekday_and_never_the_run_day():
    assert [ri._t_minus_1(epoch(d)) for d in ("2026-10-12", "2026-10-13", "2026-10-10", "2026-10-11", "2026-10-16")] == [
        "2026-10-09", "2026-10-12", "2026-10-09", "2026-10-09", "2026-10-15"]


def test_estate_reader_reads_the_bbg_prefix_through_the_host_s3_client(package):
    calls = []
    s3 = SimpleNamespace(list_objects_v2=lambda **kw: calls.append(kw) or {"Contents": [], "IsTruncated": False})
    stores = stores_of(assembly_of(package, {"enabled": True, "tiers": ["estate"]}, s3=s3))
    assert stores["price_readers"]["estate"]("AAA", "2026-01-01", "2027-01-14") == []
    assert calls and calls[0].get("Bucket") == "opal-data-etfs" and calls[0].get("Prefix") == "bbg/"


@pytest.mark.parametrize("bad", [
    "yes", [], {"enabled": True}, {"enabled": True, "tiers": ["estate"], "x": 1}, {"enabled": "true", "tiers": ["estate"]},
    {"enabled": 1, "tiers": ["estate"]}, {"enabled": True, "tiers": "estate"}, {"enabled": True, "tiers": ["demque"]},
    {"enabled": True, "tiers": ["bloomberg"]}, {"enabled": True, "tiers": ["ycharts"]}, {"enabled": True, "tiers": ["estate", "estate"]},
    {"enabled": True, "tiers": []}, {"enabled": True, "tiers": [1]}, {"enabled": True, "tiers": [["estate"]]}])
def test_bad_pricing_bindings_refuse_the_load(package, bad):
    rewrite(package, opal_pricing=bad)
    with pytest.raises(ri.ResidentInstallRefused, match="^RESIDENT_PRICING_BINDINGS$"):
        ri.load_bindings(package.path)


@pytest.mark.parametrize("good", [{"enabled": True, "tiers": ["estate"]}, {"enabled": True, "tiers": ["yfinance", "estate"]},
                                  {"enabled": False, "tiers": []}])
def test_good_pricing_bindings_load(package, good):
    rewrite(package, opal_pricing=good)
    assert ri.load_bindings(package.path)["opal_pricing"] == good


def test_offline_extras_still_win_over_the_pricing_keys():
    opal_stores = ri.make_opal_stores(
        dynamodb="D", s3="S", artifacts="A", load_map=lambda *a: {}, open_objects=lambda f, r: "O", open_classifier=lambda: "C",
        clock=lambda: CLOCK, extras={"pricing": False}, pricing_extras=lambda: {"pricing": True, "as_of": "2027-01-14"})
    record = opal_record(PRINCIPAL["principal_id"])
    record["ticket_confirmed"] = True
    got = opal_stores(PRINCIPAL, record)
    assert got["pricing"] is False and got["as_of"] == "2027-01-14"
