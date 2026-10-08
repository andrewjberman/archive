"""TO-DB-b-46 diagnostic: COUNTS of the realized-lot id repeats behind the lots-stage refusal at population scale.

Usage (from the worktree root): python <this file> <day> <out.json>
Reads the realized-lot partition of <day> from S3 through the producer's own read_day (S3 reads only; nothing written but <out.json>).
The lot id is built exactly as the producer's realized_rows builds it: `<close_event_id>/<close_open_event_id>`, after the producer's _clean.
Counts only: no id, account or amount is written.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))
import handler as h  # noqa: E402

aal, ard = h.aal, h.ard


def main(day, out):
    import boto3
    from botocore.config import Config
    s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
    doc = ard.load_declaration()
    src = ard.source_entry(doc, ard.declared_sources(doc)[0])
    spec = aal.lot_spec(src)["realized"]
    pad = int(src.get("account_id_zero_pad") or 0)
    firm = ard.firm_scope(src)
    pop = set(h.population_accounts(s3, firm)[1])
    newest_day = h.newest_landed_day(s3, *h._gold_location(firm))
    acct_set = set(h.account_set(pop, h.newest_accounts(s3, *h._gold_location(firm), newest_day)))
    frame = aal.read_day(s3, src, spec["table"], day)
    rec = {"day": day, "partition_present": frame is not None}
    if frame is not None:
        accts = [aal._account(v, pad) for v in frame[spec["account"]]]
        ids = ["%s/%s" % (aal._clean(a), aal._clean(b)) for a, b in zip(frame[spec["close_id"]], frame[spec["open_id"]])]
        import pandas as pd
        df = pd.DataFrame({"id": ids, "acct": accts})
        df["in_set"] = df["acct"].isin(acct_set)
        full_dup = frame.duplicated(keep=False)
        dup_ids = df[df.duplicated("id", keep=False)]
        in_set = df[df["in_set"]]
        rec.update({
            "rows_all_accounts": int(len(df)), "distinct_ids_all_accounts": int(df["id"].nunique()),
            "ids_repeated_all_accounts": int(dup_ids["id"].nunique()), "rows_in_repeated_ids_all_accounts": int(len(dup_ids)),
            "rows_in_account_set": int(len(in_set)), "distinct_ids_in_account_set": int(in_set["id"].nunique()),
            "ids_repeated_in_account_set": int(in_set[in_set.duplicated("id", keep=False)]["id"].nunique()),
            "rows_in_repeated_ids_in_account_set": int(len(in_set[in_set.duplicated("id", keep=False)])),
            "accounts_in_set_with_a_repeated_id": int(in_set[in_set.duplicated("id", keep=False)]["acct"].nunique()),
            "repeated_ids_spanning_more_than_one_account": int((dup_ids.groupby("id")["acct"].nunique() > 1).sum()),
            "rows_that_are_exact_duplicates_of_another_row_all_columns": int(full_dup.sum()),
            "account_set_count": len(acct_set), "population_count": len(pop),
            "source_files_count": int(frame["_source_file"].nunique()) if "_source_file" in frame.columns else None,
        })
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
