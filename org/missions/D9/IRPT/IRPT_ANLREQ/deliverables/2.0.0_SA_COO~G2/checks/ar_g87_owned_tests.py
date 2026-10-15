"""IRPT_ANLREQ AR-g-87: the issuer's own tests of the resident installer's policy revisions (run by ar_g87_checks.py).

They reuse the package fixture and the fake clients of reports/tests/test_resident_installed.py, so they build the real
runtime. They are the check, not the worker's tests: the worker's edit of that file cannot weaken them.
"""
# ruff: noqa: F811  (a pytest fixture is imported, then named as a test argument)
from pathlib import Path
import sys
import time

TESTS = Path("infra/aws/lambda/investor-reporting/reports/tests").resolve()
sys.path.insert(0, str(TESTS))
from test_resident_installed import RESEARCH, fake_clients, package, ri  # noqa: E402,F401

COMMENTARY = "irpt-anlreq-x10-v1"


def build(package, monkeypatch):
    import composition
    asked = []
    real = composition.build_retained_repositories

    def spy(*args, **kwargs):
        asked.append(kwargs.get("additional_policy_revisions"))
        return real(*args, **kwargs)
    monkeypatch.setattr(composition, "build_retained_repositories", spy)
    return asked, ri.build_resident_runtime(package.path, clients=fake_clients(), clock=time.time)


def test_the_installer_asks_for_both_revisions_in_order(package, monkeypatch):
    asked, _ = build(package, monkeypatch)
    assert asked == [(RESEARCH, COMMENTARY)]


def test_the_constants_are_the_two_revisions(package):
    assert ri.OPAL_RESEARCH_REVISION == RESEARCH and ri.ANALYSIS_COMMENTARY_REVISION == COMMENTARY


def test_the_commentary_family_is_registered_under_its_revision_and_the_opal_family_keeps_its_own(package, monkeypatch):
    _, runtime = build(package, monkeypatch)
    artifacts = runtime["assembly"].requests.artifacts
    assert artifacts.revisions["ANALYSIS_COMMENTARY"] == COMMENTARY
    assert artifacts.revisions["YCHARTS_OPAL_REPORT"] == RESEARCH
    assert "ANALYSIS_COMMENTARY" in artifacts.families


def test_every_other_family_stays_on_the_served_revision(package, monkeypatch):
    _, runtime = build(package, monkeypatch)
    artifacts = runtime["assembly"].requests.artifacts
    assert {f for f, r in artifacts.revisions.items() if r == COMMENTARY} == {"ANALYSIS_COMMENTARY"}
    assert "ORIGINAL_VENDOR_PDF" in artifacts.families and "ORIGINAL_VENDOR_PDF" not in artifacts.revisions
