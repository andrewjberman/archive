"""Probe: count GetObject attempts on an ai_fill key, per test, and block each one.

Loaded with `python -m pytest -p probe_aifill_gets`. Every attempted GetObject whose
Key contains "ai_fill" is recorded against the running test's nodeid and raised
(never sent), so the probe reaches no network. PROBE_UNSET=1 removes the
AMGT_AIFILL_ROOT variable at the start of each test body (after the autouse
fixtures have set it), which reproduces the pre-line state as a negative control.
"""
import json
import os

from botocore import client as _bc

_CUR = {"nodeid": None}
_HITS = []
_ORIG = _bc.BaseClient._make_api_call
_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "probe_out_%s.json" % ("unset" if os.environ.get("PROBE_UNSET") == "1" else "with_line"))


def _probe(self, operation_name, api_params):
    if operation_name == "GetObject" and "ai_fill" in str(api_params.get("Key", "")):
        _HITS.append({"test": _CUR["nodeid"], "bucket": api_params.get("Bucket"), "key": api_params.get("Key")})
        raise RuntimeError("probe: ai_fill GET counted and blocked, not sent")
    return _ORIG(self, operation_name, api_params)


_bc.BaseClient._make_api_call = _probe


def pytest_runtest_setup(item):
    _CUR["nodeid"] = item.nodeid


def pytest_runtest_call(item):
    if os.environ.get("PROBE_UNSET") == "1":
        os.environ.pop("AMGT_AIFILL_ROOT", None)


def pytest_sessionfinish(session, exitstatus):
    tests = sorted({h["test"] for h in _HITS})
    with open(_OUT, "w") as fh:
        json.dump({"gets": len(_HITS), "tests_with_get": len(tests), "tests": tests,
                   "first_hits": _HITS[:5]}, fh, indent=1)
