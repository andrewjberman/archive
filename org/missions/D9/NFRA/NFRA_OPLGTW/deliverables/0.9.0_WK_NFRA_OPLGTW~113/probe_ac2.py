"""OG-ac-2 probe: mdpf_get_security_classification against the REAL etf-classifications table, with the box's own credentials.

(a) Find ONE ticker that has a row, with at most three get_item calls (SPY, then AGG, then QQQ). Call the tool as an Opal
    stand-in: the envelope must be complete, the body non-empty and as_of a date. Call it again as a non-Opal stand-in and
    assert the refusal with zero table reads.
(b) Call the tool on ZZNOSUCHKEY9 and assert the absent answer.

Prints two lines and no row content: booleans, counts and the row's own as-of date. The audit sink is a no-op, so the probe
writes nothing into the repository.

Run from anywhere: python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~113/probe_ac2.py
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[7]
GW = REPO / "infra" / "aws" / "ec2" / "opal-gateway"
sys.path.insert(0, str(GW))

import boto3  # noqa: E402

from app import audit, harvest_read as hr, internal_role, mdpf_classification as mc  # noqa: E402

OPAL_STANDIN = "ac2.probe@opalinvest.com"       # stand-in; never printed
OUTSIDER_STANDIN = "ac2.probe@example.com"      # stand-in; never printed
SEARCH = ("SPY", "AGG", "QQQ")                  # at most three get_item calls to find a row
ABSENT = "ZZNOSUCHKEY9"
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class _Counting:
    """Wraps the real DynamoDB client, counts get_item calls, and refuses any other method (the module makes none)."""

    def __init__(self, real):
        self.real = real
        self.reads = 0

    def get_item(self, **kw):
        self.reads += 1
        return self.real.get_item(**kw)

    def __getattr__(self, name):
        raise AssertionError("the module called %s, which is not a read of this tool" % name)


def _answered_row(out: dict) -> bool:
    if not all(k in out for k in ENVELOPE):
        return False
    body = [k for k in out if k not in ENVELOPE and k not in ("freshness", "stale")]
    return bool(body) and isinstance(out.get("as_of"), str) and bool(DATE.match(out["as_of"]))


def main() -> int:
    if os.environ.get("INTERNAL_READER_ROLE_ARN"):
        return 1
    counter = _Counting(boto3.client("dynamodb", region_name=mc.REGION))
    state = {"principal": SimpleNamespace(email=OPAL_STANDIN, tid="0", oid="0")}
    audit.log_call = lambda *a, **kw: None
    hr.get_current_principal = lambda: state["principal"]
    internal_role.dynamodb_client = lambda *a, **kw: None
    mc._client = lambda: counter

    found, out = None, {}
    for ticker in SEARCH:
        out = mc.mdpf_get_security_classification(ticker)
        if _answered_row(out):
            found = ticker
            break
    if found is None:
        print("probe cls: mdpf_get_security_classification answered False as_of None non_opal_refused False reads_on_refusal 0")
        return 1

    state["principal"] = SimpleNamespace(email=OUTSIDER_STANDIN, tid="0", oid="0")
    before = counter.reads
    refused_out = mc.mdpf_get_security_classification(found)
    reads = counter.reads - before
    refused = refused_out.get("code") == "typed_opal_only" and refused_out.get("guard_denied") is True
    state["principal"] = SimpleNamespace(email=OPAL_STANDIN, tid="0", oid="0")
    print("probe cls: mdpf_get_security_classification answered %s as_of %s non_opal_refused %s reads_on_refusal %d"
          % (_answered_row(out), out.get("as_of"), refused, reads))

    absent = mc.mdpf_get_security_classification(ABSENT)
    print("probe cls: absent_ticker answered %s absent_reason set %s"
          % (all(k in absent for k in ENVELOPE), bool(absent.get("absent_reason"))))
    ok = _answered_row(out) and refused and reads == 0 and bool(absent.get("absent_reason"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
