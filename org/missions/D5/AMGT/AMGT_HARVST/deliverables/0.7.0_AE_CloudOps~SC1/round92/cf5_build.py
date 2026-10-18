"""HVST-cf-5 step 0, READ ONLY, run from the pinned worktree (C:/tmp/cf5-build at 04be089e13). ASCII only.

  python -u cf5_build.py              (i) both forms built IN MEMORY, (ii) the stored research-fund-form objects, (iv) the substrate
                                      fund_form member for UNH and CPA. Writes nothing; never runs fund_form --compare or --write.
Expected (COO half): exactly two funds, PFOE 33 reports and IDVZ 82; reports_after=115 absent_after=232; stored objects are
version 1 (IDVZ, PFOE, DIVZ).
"""
from __future__ import annotations

import json
import os
import sys

WT = r"C:\tmp\cf5-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import fund_form, gold, substrate  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def build_all(client):
    items, extract_bytes = fund_form.gather_items(client=client)
    plain = fund_form._drop_extract_key(items)
    funds = fund_form.distinct_funds(plain)
    absent = fund_form.absent_fund_reports(plain)
    forms = {}
    for fund in funds:
        inputs = fund_form._inputs_for_fund(fund, items, extract_bytes)
        doc = fund_form.build_document(fund, plain, inputs)
        forms[fund] = (doc, inputs, "%s.json" % fund_form._inputs_sha16(inputs))
    return items, funds, absent, forms


def main():
    client = store._default_client()
    items, funds, absent, forms = build_all(client)
    print("BUILD items=%d funds=%s absent_fund_reports=%d" % (len(items), list(funds), absent))
    total = 0
    for fund in funds:
        doc, inputs, name = forms[fund]
        n = doc["fields"]["reports"]
        total += n
        print("FUND %s reports=%d sections=%d object=%s content_sha256=%s inputs=%d" % (
            fund, n, len(doc["fields"]["skeleton"]), name, doc["content_sha256"], len(inputs)))
    print("TOTAL reports_after=%d absent_after=%d funds=%d" % (total, absent, len(funds)))
    print("--- (ii) STORED research-fund-form objects")
    keys = gold.gold_list(fund_form.TABLE, client=client)
    for key in keys:
        body = gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, key), client=client)
        d = json.loads(body.decode("utf-8"))
        print("STORED %s method_version=%s fund=%s reports=%s inputs=%d content_sha256=%s bytes=%d" % (
            key, d.get("method_version"), d.get("subject", {}).get("fund"), d.get("fields", {}).get("reports"),
            len(d.get("inputs", [])), d.get("content_sha256"), len(body)))
    print("STORED-COUNT %d" % len(keys))
    print("--- (iv) SUBSTRATE fund_form member BEFORE")
    for sk in ("UNH_US_Equity", "CPA_US_Equity"):
        _entry, cdoc = substrate._continuation_member(sk, client)
        fv = cdoc["fields"]["fund_of_record"] if cdoc else None
        member = substrate._fund_form_member(cdoc, client)
        print("SUBSTRATE %s fund_of_record=%s fund_form=%s" % (sk, json.dumps(fv, sort_keys=True)[:120], json.dumps(member, sort_keys=True)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
