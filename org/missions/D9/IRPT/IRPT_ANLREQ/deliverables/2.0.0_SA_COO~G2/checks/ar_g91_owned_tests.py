"""IRPT_ANLREQ AR-g-91: the issuer's own tests of the resident release's source (run by ar_g91_checks.py).

They run the tracked builder as a subprocess over this repository's own HEAD (git show; no AWS or vendor call), extract the tarball
it writes into a throwaway host root, and check the shipped bindings against the shipped files. They are the check, not the worker's
tests: the worker's own file cannot weaken them.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

import pytest

ROOT = Path.cwd().resolve()
PKG = ROOT / "infra/aws/lambda/investor-reporting"
for rel in ("reports", "ycharts/generate", "ycharts/session", "ycharts/extract", "_scope", "_ids", "_keys", "_authz", "intake", "ops"):
    sys.path.insert(0, str(PKG / rel))
sys.path.insert(0, str(ROOT / "lib"))
import resident_installed as ri  # noqa: E402
import resident_worker  # noqa: E402

MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"
OVERVIEW_SHA = "21a8f6d690bbd28cf7eedfc979c3edcfa8d8a156336d9de779e8438c4913310f"
ADDRESS = "fwd1-staff-r41b@opal.invalid"
MODULES = ["price_source", "swap_replacement", "portfolio_series", "tr_level", "price_adapter_bbg", "price_adapter_demque",
           "price_adapter_yfinance", "price_adapter_ycharts", "opal_producer", "layout_overview"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build(out_dir, host_root, name="t.tar.gz"):
    pin = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    digest = "a" * 64
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    proc = subprocess.run([sys.executable, str(PKG / "reports/build_resident_package.py"), str(ROOT), str(Path(out_dir) / name), pin,
                           host_root, "4242", digest, digest], capture_output=True, text=True, env=env, timeout=300)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout), Path(out_dir) / name


def member_hashes(tar_path):
    with tarfile.open(tar_path) as tar:
        return {m.name: hashlib.sha256(tar.extractfile(m).read()).hexdigest() for m in tar.getmembers() if m.isfile()}


@pytest.fixture(scope="module")
def release(tmp_path_factory):
    out = tmp_path_factory.mktemp("r32_build")
    host = (out / "host").as_posix()
    manifest, tar_path = build(out, host)
    with tarfile.open(tar_path) as tar:
        names = tar.getnames()
        tar.extractall(host)
    return {"manifest": manifest, "bindings": manifest["bindings"], "names": names, "host": host, "out": out}


def test_the_two_other_maps_are_pinned_by_content_beside_the_overview(release):
    b, host = release["bindings"], release["host"]
    assert b["opal_map"]["sha256"] == OVERVIEW_SHA
    for key, name in (("opal_map_comparison", "comparison_map.json"), ("opal_map_multicomp", "multi_map.json")):
        assert b[key] == {"path": host + "/ycharts/research/" + name, "sha256": sha(MAPS / name)}


def test_every_shipped_pin_verifies_against_the_shipped_file_and_loads_its_own_report_type(release):
    load = ri._opal_map_loader(release["bindings"], release["host"])
    got = {v: load(v)["report_type"] for v in ("overview", "comparison", "multicomp")}
    assert got == {"overview": "OVERVIEW", "comparison": "COMPARISON", "multicomp": "MULTI"}


def test_pricing_is_shipped_off_and_the_bindings_load(release):
    assert release["bindings"]["opal_pricing"] == {"enabled": False, "tiers": ["estate", "yfinance"]}
    path = release["out"] / "bindings.json"
    path.write_text(json.dumps(release["bindings"]), encoding="utf-8")
    assert ri.load_bindings(path)["opal_pricing"]["enabled"] is False


def test_the_tarball_carries_the_price_modules_the_adapters_and_the_three_maps_and_no_test_or_fixture(release):
    names = set(release["names"])
    for module in MODULES:
        assert "ycharts/research/%s.py" % module in names, module
    for name in ("overview_map.json", "comparison_map.json", "multi_map.json"):
        assert "ycharts/research/" + name in names
    assert not [n for n in names if "/tests/" in n or "/fixtures/" in n or n.endswith(".pyc")]


def test_the_build_is_stated_by_this_seat_and_is_reproducible(release, tmp_path):
    assert release["bindings"]["pin"]["built_by"] == "2.0.0_SA_COO~G2"
    again, again_tar = build(tmp_path, release["host"])
    assert again["bindings"] == release["bindings"] and again["members"] == release["manifest"]["members"]
    assert member_hashes(again_tar) == member_hashes(release["out"] / "t.tar.gz")  # the gzip header time differs; the members do not


def test_the_producer_list_is_andrew_and_run_3s_address_and_nobody_else():
    assert resident_worker.OPAL_PRODUCER_PRINCIPALS == ("andrew@opalinvest.com", ADDRESS)
    for who, want in (("andrew@opalinvest.com", "OPAL"), (ADDRESS, "OPAL"), ("fwd1-staff-r41a@opal.invalid", "YCHARTS"),
                      ("FWD1-STAFF-R41B@opal.invalid", "YCHARTS"), (" " + ADDRESS, "YCHARTS"), ("fwd1-staff-r42a@opal.invalid", "YCHARTS"),
                      ("someone@opalinvest.com", "YCHARTS")):
        assert resident_worker.producer_for({"owner": {"principal_id": who}}) == want, who
