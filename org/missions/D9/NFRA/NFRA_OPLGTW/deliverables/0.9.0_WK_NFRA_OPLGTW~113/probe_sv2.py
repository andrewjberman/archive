"""OG-sv-2 probe: portal_get_cma_assumptions against the REAL portal-v2 bucket, with the box's own credentials.

An Opal stand-in principal calls the tool: the envelope must be complete, the body non-empty, and the as_of the edition year.
A non-Opal stand-in calls it again and must be refused with zero S3 reads. Prints ONE line and no object content. The audit
sink is a no-op, so the probe writes nothing into the repository.

Run from anywhere: python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~113/probe_sv2.py
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

from app import audit, harvest_read as hr, internal_role, portal_json_served as pjs  # noqa: E402

OPAL_STANDIN = "sv2.probe@opalinvest.com"       # stand-in; never printed
OUTSIDER_STANDIN = "sv2.probe@example.com"      # stand-in; never printed
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")
YEAR = re.compile(r"^\d{4}$")


class _Counting:
    """Wraps the real S3 client and counts every read call."""

    def __init__(self, real):
        self.real = real
        self.reads = 0

    def get_object(self, **kw):
        self.reads += 1
        return self.real.get_object(**kw)

    def list_objects_v2(self, **kw):
        self.reads += 1
        return self.real.list_objects_v2(**kw)


def main() -> int:
    if os.environ.get("INTERNAL_READER_ROLE_ARN"):
        return 1
    counter = _Counting(boto3.client("s3"))
    state = {"principal": SimpleNamespace(email=OPAL_STANDIN, tid="0", oid="0")}
    audit.log_call = lambda *a, **kw: None
    hr.get_current_principal = lambda: state["principal"]
    internal_role.s3_client = lambda *a, **kw: None
    pjs._client = lambda: counter

    out = pjs.portal_get_cma_assumptions()
    body = [k for k in out if k not in ENVELOPE and k not in ("columns_dropped", "freshness", "stale")]
    answered = all(k in out for k in ENVELOPE) and bool(body) and bool(YEAR.match(str(out.get("as_of") or "")))

    state["principal"] = SimpleNamespace(email=OUTSIDER_STANDIN, tid="0", oid="0")
    before = counter.reads
    refused_out = pjs.portal_get_cma_assumptions()
    reads = counter.reads - before
    refused = refused_out.get("code") == "typed_opal_only" and refused_out.get("guard_denied") is True

    print("probe sv2: portal_get_cma_assumptions answered %s as_of %s non_opal_refused %s reads_on_refusal %d"
          % (answered, out.get("as_of"), refused, reads))
    return 0 if (answered and refused and reads == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
