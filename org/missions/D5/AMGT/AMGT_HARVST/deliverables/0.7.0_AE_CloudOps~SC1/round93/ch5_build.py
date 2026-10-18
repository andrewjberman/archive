"""HVST-ch-5 step 0, READ ONLY, run from the pinned worktree (C:/tmp/ch5-build at 2e0dc6af2e). ASCII only.

  python -u ch5_build.py     (i) the three fund forms built IN MEMORY, each compared with the stored objects by name;
                             (ii) the stored research-fund-form objects with method_version; (iv) the picker BEFORE for DIVZ.
Writes nothing. Never runs `fund_form --write`. Expected (COO half): FORM DIVZ reports=0 object=a181f84957dbb8b7.json
content_sha256=34524f75... stored=absent; IDVZ (65a5baab3afd06f0.json) and PFOE (57cee6de8b2cd85e.json) stored=equal;
11 stored objects.
"""
from __future__ import annotations

import json
import os
import sys

WT = r"C:\tmp\ch5-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import fund_form, gold, substrate  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def main():
    client = store._default_client()
    items, extract_bytes = fund_form.gather_items(client=client)
    plain = fund_form._drop_extract_key(items)
    funds = fund_form.distinct_funds(plain)
    print("BUILD items=%d stated_funds=%s FUNDS=%s absent_fund_reports=%d" % (
        len(items), list(funds), list(fund_form.FUNDS), fund_form.absent_fund_reports(plain)))
    stored_keys = gold.gold_list(fund_form.TABLE, client=client)
    stored = {}
    for key in stored_keys:
        body = gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, key), client=client)
        stored[key] = (json.loads(body.decode("utf-8")), body)
    for fund in sorted(set(funds) | set(fund_form.FUNDS)):
        inputs = fund_form._inputs_for_fund(fund, items, extract_bytes)
        doc = fund_form.build_document(fund, plain, inputs)
        name = "%s.json" % fund_form._inputs_sha16(inputs)
        key = "%s%s/%s" % (gold.table_prefix(fund_form.TABLE), "fund=%s" % fund_form._slug(fund), name)
        if key in stored:
            same = fund_form._canonical_bytes(doc) == stored[key][1]
            state = "equal" if same else "DIFFERENT"
        else:
            state = "absent"
        print("FORM %s reports=%d sections=%d object=%s content_sha256=%s inputs=%d stored=%s" % (
            fund, doc["fields"]["reports"], len(doc["fields"]["skeleton"]), name, doc["content_sha256"], len(inputs), state))
        if fund == "DIVZ":
            print("DIVZ-FIELDS %s" % json.dumps(doc["fields"], sort_keys=True))
            print("DIVZ-DOC keys=%s method_version=%s subject=%s" % (sorted(doc), doc["method_version"], doc["subject"]))
    print("--- (ii) STORED research-fund-form objects: %d" % len(stored_keys))
    for key in stored_keys:
        d, body = stored[key]
        print("STORED %s method_version=%s fund=%s reports=%s inputs=%d bytes=%d" % (
            key.split("research-fund-form/")[1], d.get("method_version"), d.get("subject", {}).get("fund"),
            d.get("fields", {}).get("reports"), len(d.get("inputs", [])), len(body)))
    print("--- (iv) PICKER BEFORE (substrate._pick_stored, fund=divz)")
    wanted = fund_form.current_inputs("DIVZ", client=client)
    doc, uri, current = substrate._pick_stored(fund_form.TABLE, "fund=divz", wanted, fund_form.METHOD_VERSION, client)
    print("PICK DIVZ wanted_inputs=%s uri=%s current=%s method_version=%s reports=%s" % (
        json.dumps(wanted), uri, current, doc and doc.get("method_version"), doc and doc.get("fields", {}).get("reports")))
    try:
        fund_form.read_latest("DIVZ", client=client)
        print("READ_LATEST DIVZ returned an object")
    except LookupError as exc:
        print("READ_LATEST DIVZ raised LookupError: %s" % exc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
