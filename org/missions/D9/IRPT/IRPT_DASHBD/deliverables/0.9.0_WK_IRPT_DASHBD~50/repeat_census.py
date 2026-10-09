"""TO-DB-b-73 step 1: the rows of one day's custodian realized-lot partition that share the whole realized key, and the columns that differ.

Usage (worktree root): python <this file> <day> <out.json>
S3 reads only (the producer's own read_day). Counts and column names only; accounts are sha256-hashed (8 hex), no lot id or amount is written.
"""
import hashlib
import itertools
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
    spec = aal.lot_spec(src)["realized"]
    pad = int(src.get("account_id_zero_pad") or 0)
    frame = aal.read_day(s3, src, spec["table"], day)
    cols = [c for c in frame.columns]
    keyed = {}
    for i, (_, r) in enumerate(frame.iterrows()):
        k = (aal._account(r.get(spec["account"]), pad), aal._day(r.get(spec["closed"])),
             "%s/%s" % (aal._clean(r.get(spec["close_id"])), aal._clean(r.get(spec["open_id"]))), aal._num(r.get(spec["quantity"])))
        keyed.setdefault(k, []).append(i)
    groups = {k: v for k, v in keyed.items() if len(v) > 1}
    rec = {"day": day, "rows_read": int(len(frame)), "raw_columns": cols, "rows_in_whole_key_repeats": int(sum(len(v) for v in groups.values())),
           "pairs": len(groups), "group_sizes": dict(Counter(len(v) for v in groups.values())),
           "accounts_with_a_repeat": len({k[0] for k in groups}), "hashed_accounts": sorted(hashlib.sha256(k[0].encode()).hexdigest()[:8] for k in groups)}
    diff_count, per_group, identical = Counter(), [], 0
    for k, idx in groups.items():
        sub = frame.iloc[idx]
        d = [c for c in cols if sub[c].astype(str).nunique(dropna=False) > 1]
        per_group.append(d)
        if not d:
            identical += 1
        for c in d:
            diff_count[c] += 1
    rec["groups_identical_in_every_column"] = identical
    rec["differing_columns_union"] = sorted(diff_count)
    rec["differing_columns_groups_that_differ_in_it"] = dict(diff_count)
    rec["differing_columns_per_group_histogram"] = dict(Counter(len(d) for d in per_group))
    # smallest set of raw columns that separates every group's rows
    sep = None
    for size in range(1, 4):
        found = []
        for combo in itertools.combinations(sorted(diff_count), size):
            ok = True
            for idx in groups.values():
                vals = frame.iloc[idx][list(combo)].astype(str).apply(tuple, axis=1)
                if vals.nunique() != len(idx):
                    ok = False
                    break
            if ok:
                found.append(list(combo))
        if found:
            sep = {"size": size, "sets": found}
            break
    rec["smallest_raw_column_sets_that_separate_every_group"] = sep
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
