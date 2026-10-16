"""OG-sv-1 probe: each BUILT json-served tool against the REAL portal-v2 bucket, with the box's own credentials.

For each tool: an Opal stand-in principal calls it; the envelope must be complete and carry a non-empty body (or a stated
absent_reason) with the object's own as-of date; a non-Opal stand-in calls it again and must be refused with zero S3 reads.
Prints ONE line per tool and no object content: counts, booleans and dates only. The audit sink is a no-op, so the probe
writes nothing into the repository.

Run from anywhere: python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~113/probe_sv1.py
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

OPAL_STANDIN = "sv1.probe@opalinvest.com"       # stand-in; never printed
OUTSIDER_STANDIN = "sv1.probe@example.com"      # stand-in; never printed
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")
META = ("columns_dropped", "freshness", "stale")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


def _answered(out: dict) -> bool:
    if not all(k in out for k in ENVELOPE):
        return False
    body = [k for k in out if k not in ENVELOPE and k not in META]
    if body and isinstance(out.get("as_of"), str) and DATE.match(out["as_of"]):
        return True
    return bool(out.get("absent_reason"))


def main() -> int:
    if os.environ.get("INTERNAL_READER_ROLE_ARN"):
        print("probe sv1: refused to run, INTERNAL_READER_ROLE_ARN is set")
        return 1
    print("probe sv1: box credentials, INTERNAL_READER_ROLE_ARN unset")
    real = boto3.client("s3")
    counter = _Counting(real)
    state = {"principal": SimpleNamespace(email=OPAL_STANDIN, tid="0", oid="0")}
    audited = []
    audit.log_call = lambda *a, **kw: audited.append(1)
    hr.get_current_principal = lambda: state["principal"]
    internal_role.s3_client = lambda *a, **kw: None
    pjs._client = lambda: counter
    outsider = SimpleNamespace(email=OUTSIDER_STANDIN, tid="0", oid="0")

    def non_opal_refused(call) -> tuple:
        """(refused, reads) of a call made as the non-Opal stand-in."""
        state["principal"] = outsider
        before = counter.reads
        out = call()
        state["principal"] = SimpleNamespace(email=OPAL_STANDIN, tid="0", oid="0")
        refused = out.get("code") == "typed_opal_only" and out.get("guard_denied") is True
        return refused, counter.reads - before

    ok_all = True
    # correlations: the default answer names the window keys; one of them is then read by name
    default = pjs.portal_get_correlations()
    windows = default.get("windows_available") or []
    by_window = pjs.portal_get_correlations(window=windows[0]) if windows else {}
    refused_c, reads_c = non_opal_refused(lambda: pjs.portal_get_correlations())
    line_ok = _answered(default) and _answered(by_window) and refused_c and reads_c == 0
    ok_all &= line_ok
    print("probe sv: portal_get_correlations answered %s as_of %s non_opal_refused %s reads_on_refusal %d"
          % (_answered(default) and _answered(by_window), default.get("as_of"), refused_c, reads_c))

    single = [
        ("portal_get_etf_returns", lambda: pjs.portal_get_etf_returns()),
        ("portal_get_model_portfolio_timeseries", lambda: pjs.portal_get_model_portfolio_timeseries()),
        ("portal_get_peer_performance", lambda: pjs.portal_get_peer_performance()),
        ("portal_get_trending", lambda: pjs.portal_get_trending()),
    ]
    for name, call in single:
        out = call()
        refused, reads = non_opal_refused(call)
        ok = _answered(out) and refused and reads == 0
        ok_all &= ok
        print("probe sv: %s answered %s as_of %s non_opal_refused %s reads_on_refusal %d"
              % (name, _answered(out), out.get("as_of"), refused, reads))

    parts = pjs.factor_parts()
    first, answered, refused_all, reads_all = None, True, True, 0
    for part in parts:
        out = pjs.portal_get_factor_tilts(part)
        first = out if first is None else first
        answered &= _answered(out)
        refused, reads = non_opal_refused(lambda p=part: pjs.portal_get_factor_tilts(p))
        refused_all &= refused
        reads_all += reads
    answered = bool(parts) and answered
    ok_all &= answered and refused_all and reads_all == 0
    print("probe sv: portal_get_factor_tilts answered %s as_of %s non_opal_refused %s reads_on_refusal %d"
          % (answered, (first or {}).get("as_of"), refused_all, reads_all))

    print("probe sv1: tools 6 answered-all %s audit rows %d reads %d" % (ok_all, len(audited), counter.reads))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
