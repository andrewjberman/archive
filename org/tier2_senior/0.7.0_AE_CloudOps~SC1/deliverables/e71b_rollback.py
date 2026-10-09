"""e71b ROLLBACK -- put the 15 snapshot items back on etf-classifications (us-east-1).

Named in ledger slug secclass-e71-seed-names-sc1-20261009, leg W, as the per-key rollback:
each snapshot item is put back under ConditionExpression updated_by = 'seed-script', so a
rollback cannot clobber a later legitimate writer. A ConditionalCheckFailedException is a
SKIP (the row moved on after the act), never a failure of this script.

Default is DRY RUN. The write needs --confirm.

  python org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/e71b_rollback.py
  python org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/e71b_rollback.py --confirm
"""
import json
import sys

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

SNAPSHOT = "org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E71_SEED_ROWS_SNAPSHOT_20261009.json"
TABLE = "etf-classifications"
REGION = "us-east-1"
GUARD = "seed-script"


def main() -> int:
    confirm = "--confirm" in sys.argv[1:]
    with open(SNAPSHOT, encoding="utf-8") as fh:
        snap = json.load(fh)
    rows = snap["rows"]
    keys = sorted(rows)
    print("E71B-ROLLBACK table=%s region=%s snapshot_rows=%d mode=%s"
          % (TABLE, REGION, len(keys), "WRITE" if confirm else "DRY-RUN"))
    print("GUARD: ConditionExpression updated_by = '%s'" % GUARD)

    if not confirm:
        for k in keys:
            r = rows[k]
            print("  WOULD-PUT %-6s name=%r updated_by=%r low_confidence=%r"
                  % (k, r.get("name"), r.get("updated_by"), r.get("low_confidence")))
        print("DRY-RUN: 0 of %d written. Re-run with --confirm to roll back." % len(keys))
        return 0

    table = boto3.resource("dynamodb", region_name=REGION).Table(TABLE)
    put = skipped = failed = 0
    for k in keys:
        item = dict(rows[k])
        try:
            table.put_item(Item=item, ConditionExpression=Attr("updated_by").eq(GUARD))
            put += 1
            print("  OK: %-6s restored" % k)
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code == "ConditionalCheckFailedException":
                skipped += 1
                print("  SKIP: %-6s updated_by is not %r -- a later writer owns this row" % (k, GUARD))
            else:
                failed += 1
                print("  ERROR: %-6s %s" % (k, code))
    print("E71B-ROLLBACK DONE denominator=%d restored=%d skipped=%d errors=%d"
          % (len(keys), put, skipped, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
