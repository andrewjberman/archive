"""HVST-cg-1 census (read-only). The silver research-report rows, the newest row per
(security_key, report_id), and the fund_relation each one carries (lib/research/corpus/fund_relation.py
classify(fund, fund_evidence)). Run from the worktree root, unbuffered, stdout to the .out:

    python -u org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~161/cg1_census.py > .../cg1_census.out

Rule for "newest": the gateway's own rule (infra/aws/ec2/opal-gateway/app/harvest_research.py,
_research_reports, lines 258-295): a row is kept when its part's object key sorts strictly higher than
the key of the part that holds the row kept so far; within one part the first row wins. Parts are read
in ascending key order, so the kept row is the one in the highest-keyed part.

typed.MISFILED_REPORTS are excluded as typed.reports_for does (typed.py), and the excluded rows are listed.

Reads ONLY: one list-objects-v2 under amgt/harvest/silver/research-report/ and one get-object per
part-*.parquet. Through lib.research.harvest.store._default_client(). Nothing is written.
Budget enforced: 200 requests (lists + gets), 300 MiB.
"""
import io
import os
import sys
from collections import Counter, defaultdict

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.corpus import fund_relation  # noqa: E402
from lib.research.corpus import typed  # noqa: E402
from lib.research.harvest import store  # noqa: E402

BUDGET_REQUESTS = 200
BUDGET_BYTES = 300 * 1024 * 1024
PROOF_SECURITIES = ("ADBE_US_Equity", "SNPS_US_Equity", "MNST_US_Equity",
                    "ML_FP_Equity", "CLX_US_Equity", "UNH_US_Equity")
NON_HOLDING = ("candidate", "initiate", "interest", "template", "unclassified")


class BudgetExceeded(RuntimeError):
    pass


class CountingReader:
    """Delegates list_objects_v2 and get_object to the real client and counts every request and byte."""

    def __init__(self, real):
        self.real = real
        self.requests = 0
        self.get_requests = 0
        self.bytes = 0

    def _spend(self):
        if self.requests + 1 > BUDGET_REQUESTS:
            raise BudgetExceeded("request budget %d exceeded" % BUDGET_REQUESTS)
        self.requests += 1

    def list_keys(self, prefix):
        keys = []
        for page in self.real.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            self._spend()
            keys.extend(obj["Key"] for obj in (page.get("Contents", []) or []))
        return keys

    def get_bytes(self, key):
        self._spend()
        self.get_requests += 1
        resp = self.real.get_object(Bucket=store.HARVEST_BUCKET, Key=key)
        body = resp["Body"]
        raw = body.read() if hasattr(body, "read") else body
        self.bytes += len(raw)
        if self.bytes > BUDGET_BYTES:
            raise BudgetExceeded("byte budget %d exceeded" % BUDGET_BYTES)
        return raw


def flat(text, n):
    if text is None:
        return "absent"
    return str(text)[:n].replace("\r", " ").replace("\n", " ").replace("\t", " ")


def main():
    prefix = store.table_prefix(typed.SOURCE, "silver", typed.TABLE)
    reader = CountingReader(store._default_client())
    keys = sorted(k for k in reader.list_keys(prefix) if k.endswith(".parquet"))

    rows_read = 0
    newest = {}  # (security_key, report_id) -> (part key, row)
    print("# PREFIX %s" % prefix)
    for key in keys:
        raw = reader.get_bytes(key)
        part_rows = pq.read_table(io.BytesIO(raw)).to_pylist()
        rows_read += len(part_rows)
        print("# PART %s rows=%d bytes=%d" % (key, len(part_rows), len(raw)))
        for row in part_rows:
            ident = (row.get("security_key"), row.get("report_id"))
            prev = newest.get(ident)
            if prev is None or key > prev[0]:
                newest[ident] = (key, row)

    excluded = {(e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS}
    kept = []
    for ident in sorted(newest, key=lambda x: (str(x[0]), str(x[1]))):
        part, row = newest[ident]
        if ident in excluded:
            print("# EXCLUDED-MISFILED %s %s part=%s" % (ident[0], ident[1], part))
            continue
        kept.append((ident, part, row))

    print("# DENOMINATOR parts=%d rows_read=%d kept_reports=%d (newest row per security_key, report_id)"
          % (len(keys), rows_read, len(kept)))
    print("# METHOD relation = fund_relation.classify(row['fund'], row['fund_evidence']) at worktree HEAD")
    print("# METHOD newest = gateway rule: highest part object key, first row within a part")
    print("# EXCLUSION typed.MISFILED_REPORTS applied as typed.reports_for does: %s"
          % ",".join("%s:%s" % (e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS))

    counts = Counter()
    securities = set()
    nonholding = set()
    by_security = defaultdict(set)
    for (sk, rid), part, row in kept:
        securities.add(sk)
        relation = fund_relation.classify(row.get("fund"), row.get("fund_evidence"))
        counts[relation] += 1
        if row.get("fund") is not None:
            print("RELATION %s %s %s fund=%s relation=%s evidence=%s"
                  % (sk, rid, row.get("report_class"), row.get("fund"), relation,
                     flat(row.get("fund_evidence"), 70)))
            by_security[sk].add(relation)
        if relation in NON_HOLDING:
            nonholding.add(sk)

    print("NONHOLDING_SECURITIES %d %s" % (len(nonholding), ",".join(sorted(nonholding)) or "none"))
    print("CENSUS-FUND-RELATION rows=%d reports=%d securities=%d holding=%d candidate=%d initiate=%d "
          "interest=%d template=%d unclassified=%d none=%d gets=%d bytes=%d"
          % (rows_read, len(kept), len(securities), counts["holding"], counts["candidate"],
             counts["initiate"], counts["interest"], counts["template"], counts["unclassified"],
             counts["none"], reader.requests, reader.bytes))
    proof = []
    for sk in PROOF_SECURITIES:
        rels = sorted(by_security.get(sk, ()))
        proof.append("%s=%s" % (sk, "+".join(rels) if rels else "none"))
    print("PROOF-NAMES " + " ".join(proof))


if __name__ == "__main__":
    main()
