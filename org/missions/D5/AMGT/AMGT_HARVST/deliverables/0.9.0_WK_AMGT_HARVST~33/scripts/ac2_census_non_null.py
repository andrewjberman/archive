"""AC2 -- HVST-z-2: census the newest article_security_mention gold snapshot over AC1's mapped
column set (mention_in_title, mention_in_lead, mention_count, blocks_hit, blocks_total,
co_mentioned_securities, signal_tier). Every row must carry every mapped fact.

- non-null is the test, not "plausible" -- a column present but null on a row does not carry the fact.
- a LIST column (co_mentioned_securities) carries the fact when PRESENT even if EMPTY; the
  empty-vs-null split is printed per list column so that distinction is visible, not assumed.
- a row whose article_key/security_key cannot be read at all is reported UNMEASURABLE, a third
  bucket, never folded into carried or missing.

READ-ONLY: one S3 GET of the newest gold snapshot (`_latest_gold_snapshot_rows`); no S3 write, no
delete, no vendor call.
"""

import json
import os
import sys


def _ensure_repo_root_on_path():
    here = os.path.abspath(os.path.dirname(__file__))
    path = here
    for _ in range(15):
        if os.path.isdir(os.path.join(path, "lib")) and os.path.isdir(os.path.join(path, ".tools")):
            if path not in sys.path:
                sys.path.insert(0, path)
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    raise RuntimeError("_ensure_repo_root_on_path: no ancestor of %r carries both lib/ and .tools/" % (here,))


REPO_ROOT = _ensure_repo_root_on_path()

import lib.research.harvest.publication_gold as pg  # noqa: E402

# The column set AC1 mapped clause (i)'s six ratified facts onto -- kept literal here (not
# re-imported from ac1's output) so this script's invocation stands on its own per the order's
# "each invocation LITERAL" bound; the mapping was VERIFIED against the schema object in AC1.
MAPPED_SCALAR_COLUMNS = [
    "mention_in_title",
    "mention_in_lead",
    "mention_count",
    "blocks_hit",
    "blocks_total",
    "signal_tier",
]
MAPPED_LIST_COLUMNS = ["co_mentioned_securities"]
ALL_MAPPED_COLUMNS = MAPPED_SCALAR_COLUMNS + MAPPED_LIST_COLUMNS


def main():
    schema_field_names = set(pg.GOLD_MENTION_SCHEMA.names)
    missing_from_schema = [c for c in ALL_MAPPED_COLUMNS if c not in schema_field_names]
    if missing_from_schema:
        raise RuntimeError(
            "ac2_census_non_null: mapped column(s) not present in GOLD_MENTION_SCHEMA: %r" % (missing_from_schema,)
        )

    rows = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    n_total = len(rows)

    per_column_non_null_count = {c: 0 for c in ALL_MAPPED_COLUMNS}
    per_list_column_present_empty = {c: 0 for c in MAPPED_LIST_COLUMNS}
    per_list_column_present_nonempty = {c: 0 for c in MAPPED_LIST_COLUMNS}
    per_list_column_null = {c: 0 for c in MAPPED_LIST_COLUMNS}

    unmeasurable_rows = []
    failing_rows = []

    for row in rows:
        article_key = row.get("article_key")
        security_key = row.get("security_key")

        if article_key is None or security_key is None:
            unmeasurable_rows.append({
                "article_key": article_key,
                "security_key": security_key,
                "reason": "article_key or security_key is null on this gold row; row cannot be identified",
            })
            continue

        missing_columns_this_row = []

        for c in MAPPED_SCALAR_COLUMNS:
            value = row.get(c)
            if value is not None:
                per_column_non_null_count[c] += 1
            else:
                missing_columns_this_row.append(c)

        for c in MAPPED_LIST_COLUMNS:
            value = row.get(c)
            if value is None:
                per_list_column_null[c] += 1
                missing_columns_this_row.append(c)
            else:
                per_column_non_null_count[c] += 1
                if len(value) == 0:
                    per_list_column_present_empty[c] += 1
                else:
                    per_list_column_present_nonempty[c] += 1

        if missing_columns_this_row:
            failing_rows.append({
                "article_key": article_key,
                "security_key": security_key,
                "missing_columns": missing_columns_this_row,
            })

    n_measurable = n_total - len(unmeasurable_rows)
    n_failing = len(failing_rows)
    n_met = n_measurable - n_failing

    per_column_denominator = {c: n_measurable for c in ALL_MAPPED_COLUMNS}

    list_column_split = {
        c: {
            "present_empty": per_list_column_present_empty[c],
            "present_nonempty": per_list_column_present_nonempty[c],
            "null": per_list_column_null[c],
            "denominator": n_measurable,
        }
        for c in MAPPED_LIST_COLUMNS
    }

    if n_measurable == 0:
        verdict = "clause (i) UNMEASURABLE -- 0 measurable rows out of %d total" % n_total
    elif n_failing == 0:
        verdict = "clause (i) MET over %d of %d rows" % (n_measurable, n_measurable)
    else:
        verdict = "clause (i) NOT MET, with %d of %d rows failing (named in failing_rows): %s" % (
            n_failing, n_measurable,
            ", ".join("%s/%s" % (r["article_key"], r["security_key"]) for r in failing_rows),
        )

    out = {
        "gold_rows_total_in_newest_snapshot": n_total,
        "unmeasurable_rows_count": len(unmeasurable_rows),
        "measurable_rows_count": n_measurable,
        "mapped_columns": ALL_MAPPED_COLUMNS,
        "per_column_non_null_count": per_column_non_null_count,
        "per_column_denominator": per_column_denominator,
        "list_column_empty_vs_null_split": list_column_split,
        "failing_rows_count": n_failing,
        "failing_rows": failing_rows,
        "unmeasurable_rows": unmeasurable_rows,
        "met_rows_count": n_met,
        "verdict": verdict,
    }
    print(json.dumps(out, indent=2, sort_keys=False, default=str))


if __name__ == "__main__":
    main()
