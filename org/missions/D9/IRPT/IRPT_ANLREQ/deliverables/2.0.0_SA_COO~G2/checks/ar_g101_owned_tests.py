"""IRPT_ANLREQ AR-g-101: the issuer's own tests of the resident's swap-pool binding (run by ar_g101_checks.py).

They reuse the package fixture, the fake clients and the helpers of reports/tests/test_resident_installed.py, so they build the real
runtime. They are the check, not the worker's tests: the worker's own file cannot weaken them.
"""
# ruff: noqa: F811  (a pytest fixture is imported, then named as a test argument)
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import sys

import pytest

TESTS = Path("infra/aws/lambda/investor-reporting/reports/tests").resolve()
sys.path.insert(0, str(TESTS))
from test_resident_installed import fake_clients, opal_record, package, rewrite, ri, sha  # noqa: E402,F401

PRINCIPAL = {"firm_id": "cottonwood", "principal_id": "nobody@example.invalid"}
CLOCK = 1_800_000_000  # 2027-01-15T08:00:00Z
ROWS = [{"ticker": t, "asset_class": "equity", "sub_asset_class": "USLargeCap"} for t in ("AAA", "BBB")]


def write_pool(root, as_of="2026-12-20", claim="held", name="swap_pool.json"):
    path = root / name
    path.write_text(json.dumps({"schema": "irpt-swap-pool.v1", "pool_as_of": as_of, "pool_claim": claim, "rows": ROWS}), encoding="utf-8")
    return path


def assembly_of(package, pool=None, pricing=None, s3=None, **pool_changes):
    path = package.root / "overview_map.json"
    path.write_text(json.dumps({"report_type": "overview", "elements": [], "calls": []}), encoding="utf-8")
    changes = {"opal_map": {"path": "overview_map.json", "sha256": sha(path)}}
    if pool is not False:
        pool_path = write_pool(package.root, **pool_changes)
        changes["opal_swap_pool"] = pool if pool is not None else {"path": "swap_pool.json", "sha256": sha(pool_path)}
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


def test_absent_binding_adds_no_swap_store(package):
    assert "swap" not in stores_of(assembly_of(package, pool=False))


def test_binding_supplies_the_pool_and_a_batched_history_port(package):
    stores = stores_of(assembly_of(package))
    swap = stores["swap"]
    assert set(swap) == {"pool", "history_days"}
    assert (swap["pool"]["pool_as_of"], swap["pool"]["pool_claim"], swap["pool"]["rows_count"]) == ("2026-12-20", "held", 2)
    assert callable(swap["history_days"]) and callable(swap["history_days"].prefetch) and swap["history_days"].calls == 0


def test_the_run_date_is_the_clocks_utc_date_so_an_old_pool_loads_and_is_stale(package):
    swap = stores_of(assembly_of(package, as_of="2026-12-01"))["swap"]
    assert swap["pool"]["stale_days"] == 45 and swap["pool"]["stale"] is True
    fresh = stores_of(assembly_of(package, as_of="2027-01-15"))["swap"]
    assert fresh["pool"]["stale_days"] == 0 and fresh["pool"]["stale"] is False


def test_a_changed_pool_file_refuses_the_job_naming_the_binding(package):
    assembly = assembly_of(package)
    (package.root / "swap_pool.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ri.ResidentInstallRefused, match="^PINNED_FILE_DIFFERS:opal_swap_pool$"):
        stores_of(assembly)


def test_an_absent_pool_file_refuses_the_job_naming_the_binding(package):
    assembly = assembly_of(package)
    (package.root / "swap_pool.json").unlink()
    with pytest.raises(ri.ResidentInstallRefused, match="^PINNED_FILE_ABSENT:opal_swap_pool$"):
        stores_of(assembly)


@pytest.mark.parametrize("changes,code", [({"claim": "measured"}, "POOL_CLAIM_NOT_HELD"), ({"as_of": "2027-02-01"}, "POOL_DATED_IN_FUTURE"),
                                          ({"as_of": "not a date"}, "POOL_AS_OF_INVALID")])
def test_a_pool_that_does_not_load_refuses_the_job_with_the_pools_own_code(package, changes, code):
    assembly = assembly_of(package, **changes)
    with pytest.raises(Exception, match=code):
        stores_of(assembly)


@pytest.mark.parametrize("bad", [
    "yes", [], {}, {"path": "p"}, {"sha256": "a" * 64}, {"path": "p", "sha256": "a" * 64, "x": 1}, {"path": "", "sha256": "a" * 64},
    {"path": "  ", "sha256": "a" * 64}, {"path": 5, "sha256": "a" * 64}, {"path": "p", "sha256": "A" * 64}, {"path": "p", "sha256": "a" * 63},
    {"path": "p", "sha256": "a" * 65}, {"path": "p", "sha256": 5}, {"path": "p", "sha256": "g" * 64}, None])
def test_bad_swap_pool_bindings_refuse_the_load(package, bad):
    rewrite(package, opal_swap_pool=bad)
    with pytest.raises(ri.ResidentInstallRefused, match="^RESIDENT_SWAP_POOL_BINDINGS$"):
        ri.load_bindings(package.path)


@pytest.mark.parametrize("good", [{"path": "p.json", "sha256": "a" * 64}, {"path": "/opt/x/ycharts/research/swap_pool.json", "sha256": "0123456789abcdef" * 4}])
def test_good_swap_pool_bindings_load(package, good):
    rewrite(package, opal_swap_pool=good)
    assert ri.load_bindings(package.path)["opal_swap_pool"] == good


def test_pricing_and_swap_extras_are_both_supplied(package):
    stores = stores_of(assembly_of(package, pricing={"enabled": True, "tiers": ["yfinance"]}))
    assert stores["pricing"] is True and "swap" in stores and sorted(stores["price_readers"]) == ["yfinance"]


def test_offline_extras_still_win_over_the_swap_keys():
    opal_stores = ri.make_opal_stores(
        dynamodb="D", s3="S", artifacts="A", load_map=lambda *a: {}, open_objects=lambda f, r: "O", open_classifier=lambda: "C",
        clock=lambda: CLOCK, extras={"swap": "OFFLINE"}, swap_extras=lambda: {"swap": {"pool": "P", "history_days": "H"}})
    record = opal_record(PRINCIPAL["principal_id"])
    record["ticket_confirmed"] = True
    assert opal_stores(PRINCIPAL, record)["swap"] == "OFFLINE"


def test_the_pin_is_read_per_job_not_at_install(package):
    assembly = assembly_of(package)
    (package.root / "swap_pool.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ri.ResidentInstallRefused):
        stores_of(assembly)       # the pin is read when a listed principal's job asks for stores


def test_the_pool_binding_is_read_from_the_bindings_and_not_hard_coded(package):
    path = write_pool(package.root, name="other_pool.json", as_of="2027-01-10")
    assembly = assembly_of(package, pool={"path": "other_pool.json", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    assert stores_of(assembly)["swap"]["pool"]["pool_as_of"] == "2027-01-10"
