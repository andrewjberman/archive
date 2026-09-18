"""og_r1_ac11_pytest.py -- the local, pre-deploy, emulated-AWS exercise for NFRA_OPLGTW.TO-OG-r-1's OGR1-AC11.

Lives OUTSIDE infra/aws/ec2/opal-gateway/tests/ (this worker's grant does not extend there) and reuses OG-v-2's
own acceptance harness (tests/acceptance/conftest.py) exactly the way tests/test_schwab_wiring.py already does
from ITS OWN location one level above tests/acceptance/ (see that file's module docstring for why a plain
`import conftest` would collide with tests/conftest.py): both `tests/` and `tests/acceptance/` are pushed onto
sys.path and `acceptance.conftest` is imported under its own namespace-package name.

AC11 (difference, local + emulated AWS, run BEFORE the deploy): an identity carrying a predecessor's email
(the pre-rename role was person-named for `menachem@opalinvest.com`) and that email's tier, but NO tid/oid
Schwab grant, is denied on EVERY one of the five Schwab tools (app.integrations.schwab.integration.TOOL_NAMES);
the SAME identity's oid, after `og_v2_h.grant(tid, oid)`, is allowed on `schwab_get_access`. The Schwab
integration is enabled in THIS TEST PROCESS ONLY (conftest.py sets ENABLED_INTEGRATIONS=schwab before app.server
is first imported) and every AWS call in the harness is emulated (moto mock_aws) -- nothing here reaches the
host, the live account or the live state store (OGR1-AC11 / BOUNDS: "reaches neither the host nor the live
state store").

Prints the tool-by-tool denial table and the granted-arm result; asserts. Run with:
  <venv>/Scripts/python -m pytest <this file> -q
"""
from __future__ import annotations

import sys
import uuid
from pathlib import Path

_GATEWAY = Path(__file__).resolve().parents[8] / "infra" / "aws" / "ec2" / "opal-gateway"
_TESTS = _GATEWAY / "tests"
_ACCEPTANCE = _TESTS / "acceptance"
for _p in (str(_GATEWAY), str(_TESTS), str(_ACCEPTANCE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import acceptance.conftest as h_  # noqa: E402

served_app = h_.served_app
moto_world = h_.moto_world
og_v2 = h_.og_v2

from app.integrations.schwab.integration import TOOL_NAMES  # noqa: E402

PREDECESSOR_EMAIL = "menachem@opalinvest.com"   # the pre-rename person-named role's identity (OG-i-2 -> OG-i-3)

_MINIMAL_ARGS = {
    "schwab_get_access": {},
    "schwab_list_files": {"master": "x", "dataset": "y"},
    "schwab_describe_dataset": {"master": "x", "dataset": "y"},
    "schwab_query": {"query": {"master": "x", "dataset": "y", "business_date": "2024-01-01", "mode": "rows"}},
    "schwab_prepare_download": {},
}


def test_ogr1_ac11_tid_oid_authority(og_v2, capsys):
    assert set(_MINIMAL_ARGS) == set(TOOL_NAMES), (
        "OGR1-AC11 tool arg table is stale: %s vs live TOOL_NAMES %s" % (sorted(_MINIMAL_ARGS), sorted(TOOL_NAMES)))
    tid = h_.TENANT
    ungranted_oid = str(uuid.uuid4())
    session_ungranted = h_._connect(og_v2, tid=tid, oid=ungranted_oid, email=PREDECESSOR_EMAIL)

    rows = []
    for tool in sorted(TOOL_NAMES):
        r, is_error, payload = h_._tool(og_v2, session_ungranted.access, tool, _MINIMAL_ARGS[tool])
        denied = bool(is_error) and r.status_code == 200
        err = payload.get("error") if isinstance(payload, dict) else None
        code = err.get("code") if isinstance(err, dict) else (err if err is not None else payload)
        rows.append((tool, r.status_code, is_error, code, denied))

    granted_oid = str(uuid.uuid4())
    og_v2.grant(tid, granted_oid)
    session_granted = h_._connect(og_v2, tid=tid, oid=granted_oid, email=PREDECESSOR_EMAIL)
    rg, is_error_g, payload_g = h_._tool(og_v2, session_granted.access, "schwab_get_access", {})
    allowed = (rg.status_code == 200) and (is_error_g is not True)

    with capsys.disabled():
        print()
        print("OGR1-AC11: identity email=%s tid=%s oid(ungranted)=%s -- NO tid/oid grant -- per-tool denial:"
              % (PREDECESSOR_EMAIL, tid, ungranted_oid))
        for tool, status, is_err, code, denied in rows:
            print("  %s -> http=%s isError=%s code=%s DENIED=%s" % (tool, status, is_err, code, denied))
        print("DENOMINATOR: %d of %d Schwab tools denied (TOOL_NAMES live count %d)"
              % (sum(1 for *_r, d in rows if d), len(rows), len(TOOL_NAMES)))
        print("OGR1-AC11: SAME email, oid(granted)=%s, AFTER og_v2.grant(tid, oid) -- schwab_get_access -> "
              "http=%s isError=%s ALLOWED=%s" % (granted_oid, rg.status_code, is_error_g, allowed))

    assert len(rows) == len(TOOL_NAMES) == 5
    for tool, status, is_err, code, denied in rows:
        assert denied, "tool %s was NOT denied for the ungranted tid/oid identity (http=%s isError=%s code=%s)" % (
            tool, status, is_err, code)
    assert allowed, "the granted tid/oid identity was NOT allowed on schwab_get_access (http=%s isError=%s)" % (
        rg.status_code, is_error_g)
