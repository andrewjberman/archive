"""Reproduce I4 offline examples using existing corpus writers, never AWS.

Run from the repository root with python <this file>.
"""
from pathlib import Path
import datetime
import hashlib
import json
import socket
import subprocess
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[7]))

import boto3
import pyarrow as pa

from lib.research.corpus import substrate, continuation, sector_template, fund_form, typecast
from lib.research.corpus.tests.test_substrate import _seed_docx_report, _seed_xlsx_sector_report

OUT = Path(__file__).resolve().parent / "evidence"


def refuse(*args, **kwargs):
    raise RuntimeError("OFFLINE EXAMPLE: external transport refused")


def retained_bytes(result, stub):
    out = {}
    for member in substrate.DERIVED_MEMBERS:
        entry = result[member]
        if "absent" in entry:
            out[member] = {"absent": entry["absent"]}
            continue
        bucket, key = substrate._split_uri(entry["uri"])
        raw = stub.get_object(Bucket=bucket, Key=key)["Body"].read()
        doc = json.loads(raw)
        out[member] = {"uri": entry["uri"], "retained_byte_sha256": hashlib.sha256(raw).hexdigest(),
                       "artifact_content_sha256": doc["content_sha256"],
                       "inputs": doc["inputs"], "document": doc}
    return out


def main():
    pa.Table.from_pylist([{"warm": 1}])
    with patch.object(boto3, "client", refuse), patch.object(boto3, "resource", refuse), \
            patch.object(boto3.session.Session, "client", refuse), \
            patch.object(socket, "create_connection", refuse), \
            patch.object(subprocess, "run", refuse), patch.object(subprocess, "Popen", refuse):
        try:
            boto3.client("s3")
        except RuntimeError:
            poison_control = True
        else:
            raise AssertionError("network poison not armed")
        stub = substrate.StubS3Client()
        security = "ACME_US_Equity"
        _seed_docx_report(stub, security, "i4-report", [
            ("RECOMMENDATION: Maintain 1% position in IDVZ", True),
            ("Investment Thesis", True), ("Durable demand and disciplined capital allocation.", False),
        ])
        _seed_xlsx_sector_report(stub, security, "i4-workbook", "Health Care")
        continuation.write_one(security, client=stub)
        sector_template._run_write(client=stub)
        # No invented derived rows: these are the real writers over the fixture.
        fund_form._run_write(client=stub)
        typecast.write(client=stub)
        positive = substrate.substrate(security, client=stub)
        positive_documents = retained_bytes(positive, stub)
        absent = substrate.substrate("ABSENT_US_Equity", client=stub)
        substrate._add_synthetic_report(security, stub)
        stale = substrate.substrate(security, client=stub)
        continuation.write_one(security, client=stub)
        changed = substrate.substrate(security, client=stub)
        before_hashes = substrate._hashes_of(positive)
        after_hashes = substrate._hashes_of(changed)
        changed_members = sorted(k for k in before_hashes if before_hashes[k] != after_hashes[k])
        assert stale["continuation"]["current"] is False
        assert changed["continuation"]["current"] is True
        assert changed_members == sorted(substrate.EXPECTED_CHANGED_SET)
        broken = substrate.StubS3Client()
        broken._objects = dict(stub._objects)
        extract_key = next(k for k in broken._objects if "/research-report-extract/" in k)
        # Fixture-only removal is a failed-read control, never a cloud deletion.
        broken._objects.pop(extract_key)
        try:
            substrate.substrate(security, client=broken)
        except KeyError as exc:
            failed = {"state": "FAILED", "exception": type(exc).__name__, "missing_key": extract_key}
        else:
            raise AssertionError("missing retained extraction became successful absence")
        document = {
            "interface": "I4", "example_version": "1", "evidence_level": "offline exercise",
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "source_population": "synthetic, two initial reports; not the live library",
            "network_poison_positive_control": poison_control,
            "positive": positive, "positive_referenced_documents": positive_documents,
            "absent_security": absent, "changed_input_before_rebuild": stale,
            "changed_input_after_rebuild": changed, "changed_members": changed_members,
            "after_rebuild_referenced_documents": retained_bytes(changed, stub),
            "failed_read": failed,
            "semantics": {
                "prior_reports.sha256": "SHA-256 of the referenced extraction JSON bytes, NOT bronze bytes",
                "content_sha256": "producer-defined semantic hash; not necessarily SHA-256 of stored JSON bytes",
                "retained_byte_sha256": "SHA-256 of exactly the retained JSON bytes returned by get_object",
                "inputs": "load from referenced derived document; substrate inline response only has inputs_count",
                "absent_security": "global typecast may still be present; absence is per member",
                "failed_read": "an exception is not absence; preserve previous accepted report in R",
            },
        }
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "I4_EXAMPLES_v1.json"
    target.write_text(json.dumps(document, indent=2, ensure_ascii=True) + "\n", encoding="ascii")
    print("I4 examples PASS; changed_members=%s; poison=True; %s" % (changed_members, target))


if __name__ == "__main__":
    main()
