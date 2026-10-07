"""AMGT_RESAPP round 77 -- AMGT-ba-2 checks (the /freshness body: attribute, then trim; CTO round-76 ruling 3).

  python r77_ba2.py --crit AC1|AC2|AC3 [--where local|deployed]

AC1 (build, the measurement): `deliverables/0.9.0_WK_AMGT_RESAPP~268/BODY_ATTRIBUTION.json` exists and attributes the body:
    total bytes, bytes per top-level key (summing to the total within 1%), bytes per row field, rows total and covered.
AC2 (build, the trim): `lib.research.freshness.page_body.page_view(view)` on the /freshness view the function serves keeps
    only the covered rows, drops the `reads` records, keeps every kept field's value EQUAL to the source row, and encodes
    within the bar (default 150,000 bytes).
AC3 (bound): the route's DEFAULT /freshness body is unchanged in shape: it still carries `reads` and every row (the r75 c59
    pin and /overlay's input_provenance read it).

Prints PASS/FAIL clause lines and `R77 BA2 <CRIT> SERVED: YES|NO`; exit 0 on YES.
"""
import argparse
import importlib
import json
import os
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
ATTRIBUTION = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~268/BODY_ATTRIBUTION.json"
PAGE_FIELDS = ("covered", "name", "security_key", "last_refreshed", "per_input", "pack")


def _event(path, query=None):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": query}


def _raw(where, path, query=None):
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        return json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(_event(path, query)).encode())["Payload"].read())
    from lib.research.api import scoped_amgt

    return scoped_amgt.handler(_event(path, query))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    ap.add_argument("--bar", type=int, default=150000)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("{0} {1} {2}".format("PASS" if cond else "FAIL", name, detail))

    def verdict():
        yes = bool(ok) and all(ok)
        print("R77 BA2 {0} SERVED: {1}".format(a.crit, "YES" if yes else "NO"))
        return 0 if yes else 1

    if a.crit == "AC1":
        if not os.path.isfile(ATTRIBUTION):
            clause("C0 the attribution file exists", False, ATTRIBUTION)
            return verdict()
        with open(ATTRIBUTION, encoding="utf-8") as fh:
            doc = json.load(fh)
        total = doc.get("total_bytes")
        top = doc.get("by_top_level") or {}
        fields = doc.get("by_row_field") or {}
        summed = sum(v for v in top.values() if isinstance(v, int))
        largest = max(top, key=top.get) if top else None
        print("   total {0} B; top-level keys {1}, summing to {2} B; largest {3} {4} B; row fields {5}; rows {6}, covered "
              "{7}".format(total, len(top), summed, largest, top.get(largest), len(fields), doc.get("rows_total"),
                           doc.get("rows_covered")))
        clause("C1 the total and the per-key bytes are stated and agree within 1%", isinstance(total, int) and total > 0
               and top and abs(summed - total) <= total * 0.01, "{0} vs {1}".format(summed, total))
        clause("C2 the row fields and both row counts are stated", len(fields) >= 5
               and isinstance(doc.get("rows_total"), int) and isinstance(doc.get("rows_covered"), int)
               and 0 < doc.get("rows_covered") <= doc.get("rows_total"))
        clause("C3 the body measured is named (function hash or `local`, and when)", bool(doc.get("measured_on"))
               and bool(doc.get("measured_at")))
        return verdict()

    r = _raw(a.where, PREFIX + "/freshness")
    raw_body = r.get("body") or ""
    try:
        view = json.loads(raw_body)
    except ValueError:
        view = {}
    rows = view.get("rows") or []
    covered = [x for x in rows if x.get("covered")]

    if a.crit == "AC3":
        print("   default /freshness: status {0}; {1} B; rows {2}; covered {3}; reads keys {4}".format(
            r.get("statusCode"), len(raw_body.encode("utf-8")), len(rows), len(covered), len(view.get("reads") or {})))
        clause("C1 the default body still carries the read records and every row", r.get("statusCode") == 200
               and isinstance(view.get("reads"), dict) and view.get("reads") and len(rows) > len(covered) > 0,
               "{0} rows".format(len(rows)))
        return verdict()

    try:
        page_body = importlib.import_module("lib.research.freshness.page_body")
    except Exception as err:  # noqa: BLE001 -- absent at the base: the build check FAILS here
        clause("C0 lib.research.freshness.page_body imports", False, "{0}: {1}".format(type(err).__name__, err))
        return verdict()
    page = page_body.page_view(view)
    out_rows = page.get("rows") or []
    size = len(json.dumps(page).encode("utf-8"))
    by_key = {x.get("security_key"): x for x in covered}
    same = 0
    for x in out_rows:
        src = by_key.get(x.get("security_key")) or {}
        if all(x.get(f) == src.get(f) for f in PAGE_FIELDS):
            same += 1
    print("   {0} view: full {1} B, {2} rows ({3} covered); page view {4} B, {5} rows; kept-field values EQUAL {6} of "
          "{7}; bar {8} B".format(a.where, len(raw_body.encode("utf-8")), len(rows), len(covered), size, len(out_rows),
                                  same, len(out_rows), a.bar))
    clause("C1 the page view holds exactly the covered rows", covered and len(out_rows) == len(covered)
           and {x.get("security_key") for x in out_rows} == set(by_key), "{0} of {1}".format(len(out_rows), len(covered)))
    clause("C2 the read records are not in the page view", "reads" not in page)
    clause("C3 every kept field equals its source row", out_rows and same == len(out_rows),
           "{0} of {1}".format(same, len(out_rows)))
    clause("C4 the page view encodes within the bar", 0 < size <= a.bar, "{0} B".format(size))
    clause("C5 the page view still says when the view was made", bool(page.get("generated_at")))
    return verdict()


if __name__ == "__main__":
    sys.exit(main())
