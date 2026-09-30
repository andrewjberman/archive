"""Before/after read for ledger irpt-holdings-contract-category-20260929 (CRO half condition 1, CTO 102767 (a)).

Each firm's latest served Holdings snapshot is assembled by the SERVED irpt-holdings code
(`publication.HoldingsPublication.capture`, all accounts, read-only S3), then validated with jsonschema Draft 2020-12
under the `contracts/HoldingsSnapshot.schema.json` packaged in each zip named on the command line.

Usage: python holdings_contract_three_firm_validate.py <holdings zip whose publication.py assembles> <zip> [<zip> ...]
Prints per firm: revision, parts, nodes, node kinds; per zip: schema sha256[:8] and VALID or the error count.
Exit 0 iff every firm is VALID under the LAST zip named.
"""
import collections
import hashlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path

import boto3
from jsonschema import Draft202012Validator, FormatChecker

FIRMS = ("49financial", "cottonwood", "inflection")
assembler, zips = sys.argv[1], sys.argv[2:]
work = Path(tempfile.mkdtemp(prefix="hc3f_"))
zipfile.ZipFile(assembler).extractall(work)
sys.path[:0] = [str(work), str(work / "lib")]
import publication  # noqa: E402

# The served read bounds a SELECTED read; this census reads every account, so the bounds are lifted here only.
for name in ("MAX_SELECTED_PART_READS", "MAX_SELECTED_READ_BYTES", "MAX_JSON_BYTES"):
    setattr(publication, name, 10 ** 12)

schemas = []
for z in zips:
    body = zipfile.ZipFile(z).read("contracts/HoldingsSnapshot.schema.json")
    schema = json.loads(body)
    Draft202012Validator.check_schema(schema)
    schemas.append((Path(z).name, hashlib.sha256(body).hexdigest()[:8],
                    Draft202012Validator(schema, format_checker=FormatChecker())))

s3 = boto3.client("s3", region_name="us-east-1")
last_ok = True
for firm in FIRMS:
    document, manifest, receipt = publication.HoldingsPublication(s3, firm).capture()
    kinds = collections.Counter(n.get("node_kind") for n in document["nodes"])
    print("%s revision %s date %s parts %d nodes %d kinds %s" % (
        firm, manifest["revision"][:10], receipt["business_date"], len(manifest.get("partitions") or []),
        len(document["nodes"]), dict(sorted(kinds.items(), key=lambda kv: str(kv[0])))))
    for number, (name, sha, validator) in enumerate(schemas):
        errors = sum(1 for _ in validator.iter_errors(document))
        print("  under %s (schema %s): %s" % (name, sha, "VALID" if errors == 0 else "INVALID, %d errors" % errors))
        if number == len(schemas) - 1:
            last_ok = last_ok and errors == 0
print("ALL FIRMS VALID UNDER %s: %s" % (schemas[-1][0], last_ok))
sys.exit(0 if last_ok else 1)
