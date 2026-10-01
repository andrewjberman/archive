#!/usr/bin/env python3
"""IB-yr-303 AC4 -- routes.json no longer says "NO CONSUMER OPERATION" of three routes the consumer names
(row IRPT_BCKEND-W91-S1), and NOTHING ELSE in the route table moved.

Reads docs/contracts/investor-reporting/v1/routes.json and checks:
  (a) for status-summary, status-job and export-download: `consumer_operation` equals the row's own `operation`
      (the convention of the 14 rows that already name one) and the row carries no
      `consumer_operation_absent_reason` key;
  (b) comparison-catalogue is untouched: `consumer_operation` null and its absent reason still present (the
      remedy names three routes, not four);
  (c) CONTROL: the route table Terraform derives resources from did not move -- sha256 over every row's
      (route_key, handler, status, operation, response_schema) plus `_denominator` equals the pin taken at the
      base, and there are still 18 rows.
PASS iff (a) 3 of 3, (b) and (c).
Base run (before the cut): FAIL -- 0 of 3 notes corrected; (b) and (c) hold.
Issuer 2.0.0_SA_COO~Y, round 30. ASCII only.
"""
import hashlib
import json
import os
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R30_checks; the repo root is parents[8]
ROUTES = os.path.join(ROOT, "docs", "contracts", "investor-reporting", "v1", "routes.json")
PIN = "cc6e5acac5ce51419882116c3b0e15f9e4be0ab90df9ca8401b3d2e6b474ae1a"
NAMED = ("status-summary", "status-job", "export-download")
KEYS = ("route_key", "handler", "status", "operation", "response_schema")


def main():
    with open(ROUTES, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    rows = {row["operation"]: row for row in doc["routes"]}
    corrected = sum(1 for op in NAMED
                    if rows[op].get("consumer_operation") == op and "consumer_operation_absent_reason" not in rows[op])
    cat = rows["comparison-catalogue"]
    untouched = cat.get("consumer_operation") is None and bool(cat.get("consumer_operation_absent_reason"))
    table = sorted(json.dumps([row.get(k) for k in KEYS]) for row in doc["routes"])
    pin = hashlib.sha256(json.dumps([table, doc["_denominator"]], sort_keys=True).encode()).hexdigest()
    control = pin == PIN and len(doc["routes"]) == 18
    if corrected == 3 and untouched and control:
        print("PASS: 3 of 3 consumer notes corrected and the route table is unmoved")
        return 0
    print("FAIL: %d of 3 consumer notes corrected; comparison-catalogue untouched %s; route table unmoved %s"
          % (corrected, untouched, control))
    return 1


if __name__ == "__main__":
    sys.exit(main())
