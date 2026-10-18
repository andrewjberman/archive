"""AMGT_HARVST HVST-cf-5, issuer's own read-back of the research-fund-form objects (2.0.0_SA_COO~W1). READ ONLY.

Lists every object under amgt/harvest/gold/research-fund-form/, and for each prints fund, method_version, reports, number of
inputs, and whether the stored content_sha256 equals the sha256 of the canonical JSON of the document without that key (the rule of
lib/research/corpus/fund_form.py::build_document). Then, for each fund with a method_version "2" object, runs
fund_form.read_latest(fund) and prints the key it returns. Run from the repo root:  python -u <this file>
"""
import hashlib
import json
import sys

sys.path.insert(0, ".")
from lib.research.corpus import fund_form, gold          # noqa: E402
from lib.research.harvest import store                    # noqa: E402

client = store._default_client()
keys = gold.gold_list(fund_form.TABLE, client=client)
by_fund = {}
for key in sorted(keys):
    uri = "s3://%s/%s" % (gold.HARVEST_BUCKET, key)
    raw = gold.gold_get(uri, client=client)
    doc = json.loads(raw.decode("utf-8"))
    body = {k: v for k, v in doc.items() if k != "content_sha256"}
    recomputed = hashlib.sha256(fund_form._canonical_bytes(body)).hexdigest()
    fund = doc.get("subject", {}).get("fund")
    print("OBJECT %s fund=%s method_version=%s reports=%s inputs=%d content_sha256_equal=%s bytes=%d"
          % (key.split("research-fund-form/")[-1], fund, doc.get("method_version"), doc.get("fields", {}).get("reports"),
             len(doc.get("inputs") or []), recomputed == doc.get("content_sha256"), len(raw)))
    by_fund.setdefault(fund, []).append(doc.get("method_version"))

for fund in sorted(by_fund):
    if "2" not in by_fund[fund]:
        print("READ_LATEST %s: no method_version 2 object stored" % fund)
        continue
    try:
        doc = fund_form.read_latest(fund, client=client)
        print("READ_LATEST %s -> method_version=%s reports=%s" % (fund, doc.get("method_version"), doc["fields"]["reports"]))
    except LookupError as exc:
        print("READ_LATEST %s -> LookupError %s" % (fund, str(exc)[:120]))
print("VERIFY objects=%d funds=%d" % (len(keys), len(by_fund)))
