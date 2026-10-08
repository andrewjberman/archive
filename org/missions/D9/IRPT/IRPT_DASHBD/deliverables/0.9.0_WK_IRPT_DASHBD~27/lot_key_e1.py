"""TO-DB-b-47 measurement: the smallest column set that makes the repeated-id realized lots of 2026-10-06 unique.

Usage (from the worktree root): python <this file> <day> <out.json>
S3 reads only (the producer's own read_day). Counts only: no id, account or amount is written.
The columns tried are the realized table's own columns (the output of the producer's realized_rows, built here from the same
declared fields through the producer's own _clean/_account/_day/_num), plus the raw frame's tie columns when they are in the table.
"""
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))
import handler as h  # noqa: E402

aal, ard = h.aal, h.ard
import pandas as pd  # noqa: E402

CURRENT = ["firm", "account_id", "business_date", "lot_id"]
TABLE_COLS = ["ticker_symbol", "cusip", "quantity", "acquired_date", "holding_term", "proceeds", "cost_basis", "realized_gain",
              "custodian_cost_basis"]


def main(day, out):
    import boto3
    s3 = boto3.client("s3")
    doc = ard.load_declaration()
    src = ard.source_entry(doc, ard.declared_sources(doc)[0])
    spec = aal.lot_spec(src)["realized"]
    pad = int(src.get("account_id_zero_pad") or 0)
    frame = aal.read_day(s3, src, spec["table"], day)
    rows = []
    for _, r in frame.iterrows():
        rows.append({
            "firm": "FIRM", "account_id": aal._account(r.get(spec["account"]), pad), "business_date": aal._day(r.get(spec["closed"])),
            "lot_id": "%s/%s" % (aal._clean(r.get(spec["close_id"])), aal._clean(r.get(spec["open_id"]))),
            "ticker_symbol": aal._clean(r.get(spec["ticker"])), "cusip": aal._clean(r.get(spec["cusip"])),
            "quantity": aal._num(r.get(spec["quantity"])), "acquired_date": aal._day(r.get(spec["acquired"])) or None,
            "holding_term": aal._clean(r.get(spec["term"])), "proceeds": aal._num(r.get(spec["proceeds"])),
            "cost_basis": aal._num(r.get(spec["cost_basis"])), "realized_gain": aal._num(r.get(spec["gain"])),
            "custodian_cost_basis": aal._num(r.get(spec["cost_basis"])),
        })
    df = pd.DataFrame(rows)
    rep = df[df.duplicated("lot_id", keep=False)].reset_index(drop=True)

    def uniq(cols):
        return int(len(rep.drop_duplicates(subset=list(cols))))

    rec = {"day": day, "rows_read": int(len(rep)), "ids_repeated": int(rep["lot_id"].nunique()),
           "accounts_with_a_repeated_id": int(rep["account_id"].nunique()),
           "rows_identical_in_every_table_column": int(rep.duplicated(keep=False).sum()),
           "current_key": CURRENT, "unique_under_current_key": uniq(CURRENT),
           "columns_tried": list(CURRENT) + TABLE_COLS}
    rec["unique_under_current_key_plus_each_column"] = {c: uniq(CURRENT + [c]) for c in TABLE_COLS}
    rec["distinct_values_of_each_column_in_the_175_rows"] = {c: int(rep[c].nunique(dropna=False)) for c in rec["columns_tried"]}
    allc = rec["columns_tried"]
    found = []
    for size in range(1, 5):
        for combo in itertools.combinations(allc, size):
            if uniq(combo) == len(rep) and not any(set(f) <= set(combo) for f in found):
                found.append(combo)
        if found:
            break
    rec["smallest_sets_unique_over_all_tried_columns"] = {"size": len(found[0]) if found else None, "sets": [list(f) for f in found]}
    # the key: the current key plus the first single column (table order) that makes the 175 unique, then reduced to what is necessary
    add = [c for c in TABLE_COLS if uniq(CURRENT + [c]) == len(rep)]
    rec["single_columns_that_complete_the_current_key"] = add
    key = list(CURRENT) + ([add[0]] if add else [])
    needed = [c for c in key if uniq([k for k in key if k != c]) < len(rep)]
    rec["added_column"] = add[0] if add else None
    rec["key_columns"] = needed
    rec["unique_under_key"] = uniq(needed)
    rec["minimality"] = [{"dropped": c, "unique": uniq([k for k in key if k != c])} for c in needed]
    rec["minimality_note"] = "unique = distinct rows of the 175 under the contract primary key with that one column dropped"
    rec["columns_of_the_contract_key_each_dropped_one_at_a_time"] = {c: uniq([k for k in key if k != c]) for c in key}
    full = lambda cols: int(len(df.drop_duplicates(subset=list(cols))))  # noqa: E731
    rec["whole_day_frame"] = {
        "rows": int(len(df)), "unique_under_current_key": full(CURRENT), "unique_under_contract_primary_key": full(key),
        "contract_key_each_dropped_one_at_a_time": {c: full([k for k in key if k != c]) for c in key},
        "rows_identical_in_every_table_column": int(df.duplicated(keep=False).sum())}
    rec["current_key_columns_not_needed_within_these_rows"] = [c for c in CURRENT if c not in needed]
    rec["key_columns_meaning"] = "the columns of the contract key each necessary to separate the 175 rows"
    rec["contract_primary_key"] = key
    rec["unique_under_contract_primary_key"] = uniq(key)
    per = rep.groupby("account_id").size()
    rec["accounts_row_counts"] = sorted(int(v) for v in per.tolist())
    rec["accounts_row_counts_histogram"] = {str(k): int(v) for k, v in per.value_counts().sort_index().items()}
    rec["unrealized_contract"] = {"changed": False, "reason": "unrealized_rows sums every custodian row of one (account, lot id) into one table row, "
                                  "so the table's lot_id cannot repeat within an account and day by construction; the key stays"}
    # the producer as it now stands, over the whole day frame (no transactions; the tie is not the question here)
    rows_p, _ = aal.realized_rows(frame, None, src, "FIRM", aal.CalendarIndex(day))
    rec["producer_over_whole_day_frame"] = {"rows_in": int(len(frame)), "rows_out": len(rows_p), "refused": False,
                                           "primary_key": list(aal.PRIMARY_KEYS[aal.TABLE_REALIZED]),
                                           "repeated_primary_keys": len(aal.duplicate_keys(aal.TABLE_REALIZED, rows_p))}
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
