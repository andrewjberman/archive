"""AC2 -- HVST-y-2: separate AGREEMENT from a DEGENERATE DISTRIBUTION, and prove assign_tier's
TOTALITY claim over its full 16-row truth table. READS ONLY; no write, no delete, no vendor call.
"""

import itertools
import json

from _common import load_context, rederive_all  # bootstraps sys.path before lib is importable

import lib.research.harvest.publication_gold as pg  # noqa: E402


def _tier_distribution(tiers):
    counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for tier in tiers:
        counts[tier] = counts.get(tier, 0) + 1
    return counts


def _totality_truth_table():
    """Every (mention_in_title, mention_in_lead, mention_count>=2, share>=share_b) combination,
    16 rows. `mention_count` is set to 2 when the count>=2 bit is True, else 0 (both land on the
    same side of the ">= 2" boundary as the bit they represent); `share` is set to
    DEFAULT_SHARE_B when the share>=share_b bit is True, else 0.0. Each row is evaluated TWICE
    (determinism) and its tier is asserted to be one of A/B/C/D (never None, never a raise) --
    that is what TOTAL means for a first-match if/elif/elif/else partition."""
    rows = []
    seen_tiers = set()
    for title, lead, count_ge2, share_ge in itertools.product([True, False], repeat=4):
        mention_count = 2 if count_ge2 else 0
        share = pg.DEFAULT_SHARE_B if share_ge else 0.0
        tier_1, weight_1 = pg.assign_tier(title, lead, mention_count, share)
        tier_2, weight_2 = pg.assign_tier(title, lead, mention_count, share)
        deterministic = (tier_1 == tier_2) and (weight_1 == weight_2)
        defined = tier_1 in pg.WEIGHTS
        seen_tiers.add(tier_1)
        rows.append({
            "mention_in_title": title,
            "mention_in_lead": lead,
            "mention_count_ge_2": count_ge2,
            "share_ge_share_b": share_ge,
            "mention_count_used": mention_count,
            "share_used": share,
            "tier": tier_1,
            "weight": weight_1,
            "deterministic_on_replay": deterministic,
            "tier_is_defined": defined,
        })
    return rows, seen_tiers


def main():
    gold_rows, articles_by_key, securities_by_key, universe_summary = load_context()
    agree, disagree, unmeasurable_text, unmeasurable_security = rederive_all(
        gold_rows, articles_by_key, securities_by_key
    )
    measurable_rows = agree + disagree
    stored_distribution = _tier_distribution(r["stored_tier"] for r in measurable_rows)
    derived_distribution = _tier_distribution(r["derived_tier"] for r in measurable_rows)

    truth_table, seen_tiers = _totality_truth_table()
    all_defined = all(row["tier_is_defined"] for row in truth_table)
    all_deterministic = all(row["deterministic_on_replay"] for row in truth_table)
    unmapped_combinations = sum(1 for row in truth_table if not row["tier_is_defined"])

    out = {
        "measurable_rows_denominator": len(measurable_rows),
        "stored_tier_distribution": stored_distribution,
        "derived_tier_distribution": derived_distribution,
        "is_degenerate_single_tier_stored": sum(1 for v in stored_distribution.values() if v > 0) <= 1,
        "is_degenerate_single_tier_derived": sum(1 for v in derived_distribution.values() if v > 0) <= 1,
        "truth_table_row_count": len(truth_table),
        "truth_table": truth_table,
        "distinct_tiers_seen_in_truth_table": sorted(seen_tiers),
        "every_combination_mapped_to_exactly_one_tier": all_defined and all_deterministic,
        "unmapped_combination_count": unmapped_combinations,
    }
    print(json.dumps(out, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
