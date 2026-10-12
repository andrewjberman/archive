"""pick_request_id.py -- READ-ONLY: name ONE accepted analysis request id for crossbox CALL XB-20261012T204548Z-706d.

Same scan, same reserved-domain rule and same composition read as count_f2.py (imported, not copied). A request qualifies when
its owner address is on a reserved domain, its owner class is OPAL_GLOBAL, and its composition document is retained and reads at
the recorded version with its digest equal. Tenant = the one with the most qualifying requests (ties: first in alphabetical
order); request = the qualifying id that sorts first within it. Writes ONE result file; no address, input id or text is kept.
"""
import datetime
import importlib.util
import json
import os
import re
import sys
from collections import Counter

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("count_f2", os.path.join(here, "count_f2.py"))
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)

REQ_ID = re.compile(r"analysis#(REQ-[0-9a-f]{24})#\d+\Z")


def main(out_path):
    qualifying, scanned, checked, not_qualifying, unreadable = {}, 0, 0, Counter(), Counter()
    start = None
    while True:
        args = {"TableName": f2.TABLE, "ConsistentRead": True, "FilterExpression": "begins_with(#r, :p)",
                "ExpressionAttributeNames": {"#r": "request_revision", "#t": "tenant", "#c": "record"},
                "ExpressionAttributeValues": {":p": {"S": "analysis#"}}, "ProjectionExpression": "#t, #r, #c"}
        if start:
            args["ExclusiveStartKey"] = start
        try:
            page = f2.ddb.scan(**args)
        except Exception as exc:
            print("SCAN_FAILED " + f2.code_of(exc), file=sys.stderr)
            return 3
        scanned += page.get("ScannedCount", 0)
        for item in page.get("Items", []):
            tenant, revision = item["tenant"]["S"], item["request_revision"]["S"]
            match = REQ_ID.match(revision)
            try:
                rec = json.loads(item["record"]["S"])
                owner = rec["owner"]
                address = owner.get(f2.OWNER_ADDRESS_MEMBER)
            except Exception:
                unreadable["RECORD_SHAPE"] += 1
                continue
            if not match or not isinstance(address, str) or "@" not in address or not f2.is_reserved(address) \
                    or owner.get(f2.OWNER_CLASS_MEMBER) != "OPAL_GLOBAL":
                not_qualifying["owner_or_id"] += 1
                continue
            checked += 1
            try:
                f2.composition_input_ids(tenant, (rec.get("composition_ref") or {}).get("artifact_id"))
            except LookupError as exc:
                not_qualifying["composition:" + str(exc)] += 1
                continue
            except Exception as exc:
                not_qualifying["composition:" + f2.code_of(exc)] += 1
                continue
            qualifying.setdefault(tenant, set()).add(match.group(1))
        start = page.get("LastEvaluatedKey")
        if not start:
            break
    counts = {t: len(ids) for t, ids in sorted(qualifying.items())}
    result = {"read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "items_scanned": scanned, "reserved_opal_global_checked_for_composition": checked,
              "qualifying_by_tenant": counts, "unreadable": dict(unreadable),
              "not_qualifying": dict(sorted(not_qualifying.items()))}
    if counts:
        best = sorted(counts, key=lambda t: (-counts[t], t))[0]
        result.update(tenant=best, request_id=sorted(qualifying[best])[0], composition_retained=True,
                      how_tied=("the record's composition_ref names an ARTIFACT# row; that row's blob member gives bucket, key and "
                                "version; the document was read at that version and its sha256 equalled the row's recorded digest; "
                                "the id is the REQ- part of the item's request_revision key; tenant chosen by most qualifying "
                                "requests (ties alphabetical); within it the id that sorts first"),
                      owner_class="OPAL_GLOBAL", owner_reserved_domain=True,
                      original_retained="not re-read here; the earlier count (F2_synthetic_owner_count.json at commit b9cb3e0ff8) found a retained original for all 33 reserved-domain requests")
    result.update(writes_made=[], claim="measured", not_read=[])
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "@" in text:
        print("REFUSED: output carries an at-sign", file=sys.stderr)
        return 4
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    print(json.dumps({k: result[k] for k in ("items_scanned", "qualifying_by_tenant", "unreadable", "not_qualifying")}, sort_keys=True))
    print("tenant=%s" % result.get("tenant"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
