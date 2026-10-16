"""Planted defect for OG-en-14's mutant control (deliverable-only; the committed tree is NOT changed).

The mutant makes data_entitlement.email_denial IGNORE route_class, so a master admin with a deny record is refused on the
browser routes again -- the exact defect the order fixes. Loaded with `python -m pytest -p og_en14_mutant_ignores_class`
(PYTHONPATH = this folder), run from the gateway directory. The patch is applied per test SETUP, not at plugin import,
because importing the gateway at plugin load runs before the test module sets its environment.
Expected: test_ogen14_ac01 and test_ogen14_ac03 FAIL (both assert the admin passes the internal_page class);
test_ogen14_ac02 PASSES (a non-admin is refused either way).
"""
import pytest

_PATCHED = []


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if _PATCHED:
        return
    import app.data_entitlement as _de

    original = _de.email_denial

    def _mutant_email_denial(email, store=None, route_class=None):
        return original(email, store)   # route_class dropped: the browser exemption never applies

    _de.email_denial = _mutant_email_denial
    _PATCHED.append(original)
