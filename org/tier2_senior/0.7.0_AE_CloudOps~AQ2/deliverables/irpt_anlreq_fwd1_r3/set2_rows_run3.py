"""IRPT_ANLREQ TO-RUN-FWD1 window 3, AMENDMENT 5 ADDENDUM (1) (0.7.0_AE_CloudOps~AQ2): READ the five SET 2 uploads' NORMALIZATION rows.

  python set2_rows_run3.py <out-file>

A read-only paginated scan of irpt-requests filtered on owner.principal_id = the SET 2 viewer; no write, no vendor call. The upload rows (filename,
identity) tie each NORMALIZATION row (by upload_id) to its candidate. Per candidate it writes ONLY: the upload id, the row's state, its final reason,
resolved_at, findings_total, and per finding: code, severity, the typed value (the symbol), the suggestion field (present or absent, and its symbol and
source), the actions list. No holdings amount, no description text, no provider receipt hash.
"""
from __future__ import annotations

import sys

from boto3.dynamodb.types import TypeDeserializer

ADDR = "irpt-r3q-iv-20261016@opal.invalid"
TENANT = "49financial"


def main(argv):
    import boto3
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    de = TypeDeserializer()
    kw = dict(TableName="irpt-requests", FilterExpression="#o.#p = :a", ExpressionAttributeNames={"#o": "owner", "#p": "principal_id"},
              ExpressionAttributeValues={":a": {"S": ADDR}})
    items = []
    while True:
        r = ddb.scan(**kw)
        items += [{k: de.deserialize(v) for k, v in it.items()} for it in r.get("Items", [])]
        if "LastEvaluatedKey" not in r:
            break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    uploads = [i for i in items if "filename" in i and "identity" in i]
    norms = [i for i in items if "findings" in i and "upload_id" in i]
    lines = ["SET 2 rows read at irpt-requests, tenant %s, owner.principal_id %s: %d rows matched (%d upload rows, %d NORMALIZATION rows); read only" % (TENANT, ADDR, len(items), len(uploads), len(norms))]
    by_up = {}
    for u in uploads:
        by_up[str(u["identity"])] = u["filename"]
    lines.append("upload rows (identity is the upload id): %s" % {v: k for k, v in by_up.items()})
    for n in sorted(norms, key=lambda x: str(by_up.get(str(x["upload_id"]), x["upload_id"]))):
        fn = by_up.get(str(n["upload_id"]), "UNMATCHED")
        cand = fn.split("-")[-1].split(".")[0].upper() if fn != "UNMATCHED" else "UNMATCHED"
        lines.append("CANDIDATE %s file %s upload_id %s state %s reason %s findings_total %s resolved_at %s" % (cand, fn, n["upload_id"], n.get("state"), n.get("reason"), n.get("findings_total"), n.get("resolved_at")))
        for f in n.get("findings") or []:
            sug = f.get("suggestion")
            sugtxt = "ABSENT" if not sug else "PRESENT symbol=%s source=%s" % ((sug or {}).get("symbol"), (sug or {}).get("source"))
            lines.append("  FINDING code %s severity %s value %s suggestion %s actions %s" % (f.get("code"), f.get("severity"), f.get("value"), sugtxt, ",".join(str(a) for a in (f.get("actions") or []))))
    open(argv[0], "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
