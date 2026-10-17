"""HVST-ce-1 measurement harness (read-only). Runs the PURE derivation in lib/research/corpus/continuation.py
on the documents fetched read-only from opal-data-harvest. Nothing is written to S3; no product file is edited.
Run from the worktree root: python .scratch/ce1/repro.py
"""
import io
import json
import os
import sys

ROOT = os.getcwd()
sys.path.insert(0, ROOT)
HERE = os.path.join(ROOT, ".scratch", "ce1")

import pyarrow.parquet as pq  # noqa: E402
from botocore.exceptions import ClientError  # noqa: E402,F401

from lib.research.corpus import continuation, typed  # noqa: E402

SK = "UNH_US_Equity"
REPORT = "48d81f053e5076e8"

# --- the silver rows: the five parquet parts, read whole (no S3 access here)
silver_rows = []
for name in sorted(os.listdir(os.path.join(HERE, "silver"))):
    if name.startswith("part_") and name.endswith(".parquet"):
        for r in pq.read_table(os.path.join(HERE, "silver", name)).to_pylist():
            silver_rows.append(r)

# typed.reports_for is replaced by the same call with the silver rows handed in (store.silver_latest is an S3 read)
def _reports_for(security_key, client=None):
    rows = [r for r in silver_rows if r.get("security_key") == security_key]
    return typed._order_reports(rows)

typed.reports_for = _reports_for

# --- the extraction bytes: v2 is the object the stored continuation read (sha 117e704b8346), v1 the sibling
V2_KEY = "amgt/harvest/bronze/research-report-extract/security_key=UNH_US_Equity/48d81f053e5076e8/extract.v2.json"
V1_KEY = "amgt/harvest/bronze/research-report-extract/security_key=UNH_US_Equity/48d81f053e5076e8/extract.json"
BYTES = {
    V2_KEY: open(os.path.join(HERE, "ext_extract.v2.json"), "rb").read(),
    V1_KEY: open(os.path.join(HERE, "ext_extract.json"), "rb").read(),
}


class _StubClient:
    """Serves only the two bytes above. Any other key raises the same KeyError the offline stub uses."""

    def get_object(self, Bucket, Key):
        if Key not in BYTES:
            raise KeyError(Key)
        return {"Body": io.BytesIO(BYTES[Key])}


# the KPI lexicon file is absent from this sparse checkout; the copy from HEAD goes to scratch and the path is pointed there
lex_src = os.path.join(HERE, "research_docx_kpi_census.json")
if not os.path.exists(lex_src):
    import subprocess
    data = subprocess.run(["git", "show", "HEAD:" + continuation.KPI_LEXICON_PATH.replace(os.sep, "/")],
                          capture_output=True, check=True).stdout
    open(lex_src, "wb").write(data)
continuation.KPI_LEXICON_PATH = lex_src

client = _StubClient()
items_raw = continuation._read_reports_with_bytes(SK, client=client)
print("ITEMS_BUILT rows=%d (silver rows for %s; security rows listed=%d of %d silver rows)"
      % (len(items_raw), SK, sum(1 for r in silver_rows if r.get("security_key") == SK), len(silver_rows)))
for row, raw, doc, read_key in items_raw:
    print("  item report_id=%s class=%s period=%s read_key=%s raw_sha=%s pages=%d" % (
        row.get("report_id"), row.get("report_class"), row.get("period"), read_key.rsplit("/", 1)[-1],
        __import__("hashlib").sha256(raw).hexdigest()[:12], len(doc.get("pages") or [])))

items = [(row, document) for row, _raw, document, _rk in items_raw]

# --- step e: the pure derivation on items as the caller builds them
fund_field, position_field = continuation._resolve_fund_and_position(items)
print("RESOLVE fund_of_record=%s" % json.dumps(fund_field, sort_keys=True))
print("RESOLVE last_stated_position=%s" % json.dumps(position_field, sort_keys=True))
cands = continuation._recommendation_candidates(items)
print("RESOLVE candidates=%d" % len(cands))

# --- compare with the stored continuation object (newest by LastModified, method v3)
stored = json.load(open(os.path.join(HERE, "obj_28404359eb0645c4.json"), encoding="utf-8"))
inputs = continuation.current_inputs(SK, items=items_raw)
lex = continuation.kpi_lexicon()
doc = continuation.build_document(SK, items, inputs, lex)
for name in ("fund_of_record", "last_stated_position", "thesis_pillars", "thesis_summary", "kpi_set"):
    same = json.dumps(doc["fields"][name], sort_keys=True) == json.dumps(stored["fields"][name], sort_keys=True)
    print("STORED_VS_TODAY field=%s equal=%s" % (name, same))
print("STORED_VS_TODAY stored_method=%s today_method=%s" % (stored.get("method_version"), doc.get("method_version")))
print("STORED_VS_TODAY stored_inputs_sha_v2=%s today_v2=%s" % (
    [i["sha256"][:12] for i in stored["inputs"] if "extract.v2" in i["key"]],
    [i["sha256"][:12] for i in inputs if "extract.v2" in i["key"]]))

# --- counterfactual diagnostic ONLY (not a product change): the same label, read per LINE of each page
import re  # noqa: E402
label_line = re.compile(r"(?im)^\s*recommendation\s*:?\s*(.*)$")
for row, document in items:
    for i, page in enumerate(document.get("pages") or []):
        for m in label_line.finditer(page or ""):
            print("COUNTERFACTUAL line-anchored label hit report=%s page=%d content=%r" % (
                row.get("report_id"), i, m.group(1).strip()[:120]))
