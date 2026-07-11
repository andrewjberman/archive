"""NFRA_TOOLPASS C0 (census reader #7, the comp-incrparity WRAPPER loop CTO asked to close): the
agent-facing comp-incrparity CLI (incrparity_cli.py) reads the opal-data-bd DATA bucket on every path
(core.fetch_bytes(core.S3_BUCKET, ...), S3_BUCKET hardcoded 'opal-data-bd') with NO guard -- the census
audited the ENGINE (incrparity_core, out-of-scope designed-bd) but not this CLI. FIX (comp-xray pattern):
guard the AGENT ENTRY -- skip for an agent by default (rc 3 = HELD-blocked), COMP_INCRPARITY_INCLUDE_HELD=1
re-enables for the DS/pipeline parity path.

bd-SAFE + hermetic: STUBS _make_s3 to raise before any AWS call, so the test NEVER touches opal-data-bd.
Non-vacuous: default -> rc 3 and _make_s3 is never reached (blocked before any read); override -> the
guard passes and _make_s3 IS reached (rc != 3).

# rail-checked: assurance oracle for comp-incrparity CLI under test (NFRA_TOOLPASS sec.6)
Author: 3.0.0_SA_CVO~B.
"""

import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(_HERE))))
_MODULE = os.path.join(_WS, "org", "modules", "graph", "incrparity_cli.py")

_spec = importlib.util.spec_from_file_location("incrparity_cli_undertest", _MODULE)
cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cli)


def _run(include_held: bool):
    calls = []

    def _stub_make_s3():
        calls.append(1)
        raise RuntimeError("stub: no real AWS/opal-data-bd in test")

    saved = cli._make_s3
    cli._make_s3 = _stub_make_s3
    if include_held:
        os.environ["COMP_INCRPARITY_INCLUDE_HELD"] = "1"
    else:
        os.environ.pop("COMP_INCRPARITY_INCLUDE_HELD", None)
    try:
        rc = cli.main(["C_06"])
    finally:
        cli._make_s3 = saved
        os.environ.pop("COMP_INCRPARITY_INCLUDE_HELD", None)
    return rc, calls


def test_bd_blocked_for_agent_by_default():
    rc, calls = _run(include_held=False)
    assert rc == 3, f"comp-incrparity must be HELD-blocked (rc 3) for an agent by default; got {rc}"
    assert not calls, "the guard must block BEFORE _make_s3 -- no bd read is even attempted"


def test_override_gets_past_the_guard_nonvacuous():
    rc, calls = _run(include_held=True)
    assert calls, "COMP_INCRPARITY_INCLUDE_HELD=1 must let the CLI proceed to _make_s3 (non-vacuous)"
    assert rc != 3, f"under the override the CLI must NOT return the HELD-blocked code; got {rc}"


if __name__ == "__main__":
    test_bd_blocked_for_agent_by_default()
    print("PASS: comp-incrparity HELD-blocked (rc 3) for an agent by default, no bd read attempted")
    test_override_gets_past_the_guard_nonvacuous()
    print("PASS: COMP_INCRPARITY_INCLUDE_HELD=1 proceeds past the guard (non-vacuous)")
    print("=== comp-incrparity CLI bd-hold: ALL PASS ===")
