"""NFRA_OPLGTW OG-gf-1 probe (round 37): each BUILT catalog row against the REAL opal-data-etfs bucket.

Box credentials (INTERNAL_READER_ROLE_ARN unset), an Opal stand-in principal and a non-Opal stand-in principal. Read only:
no write to any bucket (the audit lake ship is replaced), no object content printed. One line per BUILT catalog row:
    probe built: <tool> [<table>] answered <True|False>; non_opal_refused <True|False>; reads_on_refusal <n>
Exit 0 only when every BUILT row answered and every tool refused the non-Opal principal with zero reads.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]                                   # the repository root (W sits under org/missions/...)
GW = ROOT / "infra/aws/ec2/opal-gateway"
TID = "00000000-0000-4000-8000-00000000b001"
OID = "00000000-0000-4000-8000-00000000b002"
OPAL_STANDIN = "probe.standin@opalinvest.com"
NON_OPAL_STANDIN = "probe.standin@example.com"

os.environ.pop("INTERNAL_READER_ROLE_ARN", None)
os.environ.setdefault("AUDIT_PATH", os.path.join(tempfile.mkdtemp(prefix="oggf1_probe_"), "audit.jsonl"))
sys.path.insert(0, str(GW))

from app import audit, context, etfs_silver as es  # noqa: E402


class _Counting:
    """Wraps the real client; counts every list and get, so a refusal's read count is measured, not assumed."""

    def __init__(self, client):
        self._client = client
        self.n = 0

    def __getattr__(self, name):
        attr = getattr(self._client, name)
        if name in ("get_object", "list_objects_v2"):
            def counted(*args, **kwargs):
                self.n += 1
                return attr(*args, **kwargs)
            return counted
        return attr


def main() -> int:
    audit._emit = lambda record: None                    # no local audit write and no S3 audit-lake put from this probe
    import boto3
    counter = _Counting(boto3.client("s3"))
    es._client = lambda: counter
    context._current_principal.set(None)
    ok_rows = []
    lines = []

    def set_principal(email):
        context.set_current_principal(context.make_principal(TID, OID, email))

    # (tool, call args, [(table label, catalog entity)], answered predicate per table)
    specs = [
        ("etfs_get_new_securities", (), [("new_securities", es.ENTITY_MDPF_NEW)]),
        ("etfs_get_fund_bloomberg_profile", ("DIVZ",),
         [("fund_daily", es.ENTITY_BBG_FUND_DAILY), ("derived_summary", es.ENTITY_BBG_SUMMARY),
          ("sector_allocation", es.ENTITY_BBG_SECTOR), ("geo_allocation", es.ENTITY_BBG_GEO)]),
        ("etfs_get_fund_snapshot", ("PFDE",), [("snapshots", es.ENTITY_SNAPSHOTS)]),
    ]
    envelope_keys = ("as_of", "source_keys", "denominator", "absent_reason")
    all_refused = True
    for tool, args, tables in specs:
        fn = getattr(es, tool)
        set_principal(OPAL_STANDIN)
        result = fn(*args)
        complete = all(k in result for k in envelope_keys)
        for label, entity in tables:
            if tool == "etfs_get_new_securities":
                section = result.get("items")
            elif tool == "etfs_get_fund_snapshot":
                section = result.get("records")
            else:
                section = result.get(label)
            absent_here = (result.get("absent_reason") or label in (result.get("section_absent_reasons") or {}))
            answered = bool(complete and ((section or []) or absent_here))
            if tool == "etfs_get_new_securities":
                answered = bool(complete and (section or result.get("absent_reason")))
            ok_rows.append(answered)
            lines.append("probe built: %s [%s] answered %s" % (tool, label, answered))
        # the non-Opal refusal, measured on the real client's counter
        set_principal(NON_OPAL_STANDIN)
        before = counter.n
        refused = fn(*args)
        reads = counter.n - before
        non_opal = refused.get("code") == "typed_opal_only" and reads == 0
        all_refused = all_refused and non_opal
        for i, (label, entity) in enumerate(tables):
            lines[len(lines) - len(tables) + i] += "; non_opal_refused %s; reads_on_refusal %d" % (non_opal, reads)
    context._current_principal.set(None)
    for line in lines:
        print(line)
    built_rows = len(ok_rows)
    print("probe denominator: %d BUILT catalog rows over %d tools; answered %d of %d; non-Opal refusals with zero reads %s" % (
        built_rows, len(specs), sum(1 for x in ok_rows if x), built_rows, all_refused))
    return 0 if (all(ok_rows) and all_refused) else 1


if __name__ == "__main__":
    sys.exit(main())
