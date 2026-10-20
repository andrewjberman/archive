"""IRPT_ANLREQ TO-READ-PAGEFILED (applier 0.7.0_AE_CloudOps~IB2): READ ONLY.

  python pagefiled.py     prints the lines and writes A_PAGEFILED.txt beside this file

One paginated scan of the tickets table with a SERVER-SIDE filter (ticket_type = analysis_request, created_at at or after the v0.24 live minute) and a projection of four
members, so no other item is returned. The denominator is the sum of ScannedCount. Only ids, counts, times and closed words are printed; a creator is classed by the
domain of its address and never printed. The record never holds a title, name, email or value. Andrew's ticket (filed before the window) is a STOP if it comes back.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
TABLE = "opal-tickets"
SINCE = "2026-10-20T09:28:44"
ANDREWS = "TCK-20261017-5af976ff"
ID_SHAPE = re.compile(r"^TCK-\d{8}-[0-9a-f]{8}$")

ddb = boto3.client("dynamodb", region_name="us-east-1")
def scan():
    out, seen, count = [], 0, 0
    kwargs = {
        "TableName": TABLE,
        "FilterExpression": "ticket_type = :t AND created_at >= :c",
        "ExpressionAttributeValues": {":t": {"S": "analysis_request"}, ":c": {"S": SINCE}},
        "ProjectionExpression": "ticket_id, created_at, created_by, report_ref",
        "ConsistentRead": True,
    }
    while True:
        page = ddb.scan(**kwargs)
        count += 1
        seen += page["ScannedCount"]
        out.extend(page["Items"])
        if "LastEvaluatedKey" not in page:
            return out, seen, count
        kwargs["ExclusiveStartKey"] = page["LastEvaluatedKey"]


items, scanned, pages = scan()
read_at = datetime.now(timezone.utc).strftime("%H:%M:%S") + "Z"
ids = sorted(i["ticket_id"]["S"] for i in items)
if ANDREWS in ids:
    raise SystemExit("STOP: Andrew's ticket falls in the window; nothing written")
bad = [i for i in ids if not ID_SHAPE.match(i)]
held = sorted(i["ticket_id"]["S"] for i in items if "report_ref" in i)
syn = staff = other = 0
for i in items:
    domain = i.get("created_by", {}).get("S", "").rsplit("@", 1)[-1].lower()
    if domain == "opal.invalid":
        syn += 1
    elif domain == "opalinvest.com":
        staff += 1
    else:
        other += 1
lines = [
    "T1 count=%d since=09:28:44Z read_at=%s scanned=%d (pages=%d, consistent read, server-side filter)" % (len(ids), read_at, scanned, pages),
    "T2 ids=%s" % (",".join(ids) or "none"),
    "T3 report_ref_held=%d not_held=%d" % (len(held), len(ids) - len(held)),
    "T3b held_ids=%s" % (",".join(held) or "none"),
    "T4 creators synthetic=%d staff=%d other=%d" % (syn, staff, other),
    "READS-DONE 4 of 4 answered",
]
if bad:
    lines.append("NOTE-IDS %d id(s) not of the shape TCK-YYYYMMDD-8hex" % len(bad))
text = "\n".join(lines) + "\n"
(HERE / "A_PAGEFILED.txt").write_text(text, encoding="ascii", errors="replace", newline="\n")
print(text)
