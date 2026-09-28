"""AC3 -- HVST-y-2: the STORED weight/score agree with the STORED tier, at both the row grain
and the (security, day) grain. READS ONLY; no write, no delete, no vendor call.
"""

import json

import _common  # bootstraps sys.path (repo root) before lib is importable

_common._ensure_repo_root_on_path()

import lib.research.harvest.publication_gold as pg  # noqa: E402


def _row_weight_check(gold_rows):
    """Per mention row: does `WEIGHTS[stored_tier]` (exactly what `assign_tier`'s own final line
    `return tier, weights[tier]` would hand back for that tier) equal the row's own carried
    `signal_weight` column. Uses ONLY stored fields -- no text/alias re-derivation needed, since
    this checks internal consistency of what is already stored, not a re-derivation from text."""
    checked = 0
    missing_weight_column = 0
    mismatches = []
    for row in gold_rows:
        stored_tier = row.get("signal_tier")
        stored_weight = row.get("signal_weight")
        if stored_weight is None:
            missing_weight_column += 1
            continue
        checked += 1
        expected_weight = pg.WEIGHTS.get(stored_tier)
        if expected_weight != stored_weight:
            mismatches.append({
                "article_key": row.get("article_key"),
                "security_key": row.get("security_key"),
                "stored_tier": stored_tier,
                "stored_weight": stored_weight,
                "assign_tier_weight_for_stored_tier": expected_weight,
            })
    return checked, missing_weight_column, mismatches


def _day_score_map(gold_rows):
    """{(security_key, day): sum(signal_weight over that day's mention rows)} -- the tier-weighted
    sum `daily_rows` itself accumulates into `mention_score` (publication_gold.py:594,626)."""
    day_score = {}
    contributors = {}
    for row in gold_rows:
        published_utc = row.get("published_utc")
        day = pg._day_of(published_utc)
        if day is None:
            continue
        security_key = row.get("security_key")
        key = (security_key, day)
        weight = row.get("signal_weight") or 0.0
        day_score[key] = day_score.get(key, 0.0) + weight
        contributors.setdefault(key, []).append({
            "article_key": row.get("article_key"),
            "signal_tier": row.get("signal_tier"),
            "signal_weight": weight,
        })
    return day_score, contributors


def _day_grain_check(mention_rows, daily_rows, tolerance=1e-9):
    day_score, contributors = _day_score_map(mention_rows)
    checked = 0
    mismatches = []
    for row in daily_rows:
        key = (row.get("security_key"), row.get("day"))
        expected = day_score.get(key, 0.0)
        stored = row.get("mention_score")
        checked += 1
        if stored is None or abs(stored - expected) > tolerance:
            mismatches.append({
                "security_key": key[0],
                "day": key[1],
                "stored_mention_score": stored,
                "expected_mention_score": expected,
                "contributing_rows": contributors.get(key, []),
            })
    return checked, mismatches


def main():
    mention_rows = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    daily_rows = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)

    row_checked, missing_weight_column, weight_mismatches = _row_weight_check(mention_rows)
    day_checked, day_mismatches = _day_grain_check(mention_rows, daily_rows)

    out = {
        "row_grain": {
            "mention_rows_total": len(mention_rows),
            "rows_checked": row_checked,
            "rows_missing_signal_weight_column": missing_weight_column,
            "weight_matches_assign_tier_for_stored_tier": len(weight_mismatches) == 0,
            "mismatch_count": len(weight_mismatches),
            "mismatches": weight_mismatches,
        },
        "day_grain": {
            "security_day_pairs_checked": day_checked,
            "chatter_daily_rows_total": len(daily_rows),
            "mention_score_reproducible": len(day_mismatches) == 0,
            "mismatch_count": len(day_mismatches),
            "one_worked_example": None,
            "disagreeing_pairs": day_mismatches,
        },
    }

    # one worked example either way (a PASS-shaped example if no mismatch, else the first
    # failing day with its arithmetic shown -- the criterion FAILS if only "consistent" is
    # printed with no example).
    if day_mismatches:
        out["day_grain"]["one_worked_example"] = day_mismatches[0]
    else:
        for row in daily_rows:
            key = (row.get("security_key"), row.get("day"))
            if row.get("mention_score"):
                day_score, contributors = _day_score_map(mention_rows)
                out["day_grain"]["one_worked_example"] = {
                    "security_key": key[0],
                    "day": key[1],
                    "stored_mention_score": row.get("mention_score"),
                    "expected_mention_score": day_score.get(key, 0.0),
                    "contributing_rows": contributors.get(key, []),
                    "arithmetic": " + ".join(
                        "%.4f" % c["signal_weight"] for c in contributors.get(key, [])
                    ) + " = %.4f" % day_score.get(key, 0.0),
                }
                break

    print(json.dumps(out, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
