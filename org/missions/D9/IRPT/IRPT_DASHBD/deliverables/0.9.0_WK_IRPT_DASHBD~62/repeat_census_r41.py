"""TO-DB-b-87 step 1: the rows of the 2026-10-08 custodian realized-lot partition that share the WHOLE current realized key
(account, closing date, lot id, quantity, proceeds), over the population accounts, and the columns that differ within each pair.

Usage (worktree root, kit venv python): python <this file> <day> <out.json>
S3 reads only (the producer's own read_day and the handler's own population). Counts and column names only; accounts are sha256-hashed
(8 hex); no lot id or amount is written.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))
import handler as h  # noqa: E402

aal, ard = h.aal, h.ard


def main(day, out):
    import boto3
    s3 = boto3.client("s3")
    doc = ard.load_declaration()
    src = ard.source_entry(doc, ard.declared_sources(doc)[0])
    firm = ard.firm_scope(src)
    bucket, key_prefix = h._gold_location(firm)
    population = h.population_accounts(s3, firm)[1]
    accounts = set(h.account_set(population, h.newest_accounts(s3, bucket, key_prefix, h.newest_landed_day(s3, bucket, key_prefix))))
    spec = aal.lot_spec(src)["realized"]
    pad = int(src.get("account_id_zero_pad") or 0)
    frame = aal.read_day(s3, src, spec["table"], day)
    cols = list(frame.columns)
    rows_all = int(len(frame))
    frame = frame[frame[spec["account"]].map(lambda v: aal._account(v, pad)).isin(accounts)].reset_index(drop=True)
    keyed = {}
    for i, (_, r) in enumerate(frame.iterrows()):
        k = (aal._account(r.get(spec["account"]), pad), aal._day(r.get(spec["closed"])),
             "%s/%s" % (aal._clean(r.get(spec["close_id"])), aal._clean(r.get(spec["open_id"]))), aal._num(r.get(spec["quantity"])),
             aal._num(r.get(spec["proceeds"])))
        keyed.setdefault(k, []).append(i)
    groups = {k: v for k, v in keyed.items() if len(v) > 1}
    diff_count, per_pair, identical = Counter(), [], 0
    for k, idx in sorted(groups.items()):
        sub = frame.iloc[idx]
        d = [c for c in cols if sub[c].astype(str).nunique(dropna=False) > 1]
        per_pair.append({"account_hash": hashlib.sha256(k[0].encode()).hexdigest()[:8], "rows": len(idx), "differing_columns": d})
        if not d:
            identical += 1
        for c in d:
            diff_count[c] += 1
    rec = {"day": day, "population_accounts": len(accounts), "rows_all_accounts": rows_all, "rows_read": int(len(frame)),
           "pairs": len(groups), "group_sizes": dict(Counter(len(v) for v in groups.values())),
           "accounts_with_a_repeat": len({k[0] for k in groups}), "groups_identical_in_every_column": identical,
           "differing_columns_union": sorted(diff_count), "per_pair": per_pair, "raw_columns": cols}
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in rec.items() if k != "raw_columns"}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
