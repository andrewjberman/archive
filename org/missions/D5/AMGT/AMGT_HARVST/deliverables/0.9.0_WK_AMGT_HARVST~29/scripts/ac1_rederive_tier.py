"""AC1 -- HVST-y-2: match the STORED signal_tier against a re-derivation from the STORED silver
text, with a printed denominator. READS ONLY (gold article_security_mention snapshot + silver
article text + live universe alias read); no write, no delete, no vendor call.

Which of the four `assign_tier` inputs were recomputed from stored TEXT, and which could not be:
ALL FOUR -- mention_in_title, mention_in_lead, mention_count, share -- are produced by
`publication_gold._security_mentions(article_row, security)`, which reads only the silver
article's own `title` and `text_blocks` fields against the security's alias list; none of the
four is read off the gold row's own stored booleans/count (that readback is the tautology BOUNDS
clause 2 names). A row is UNMEASURABLE, never a match or a mismatch, when its silver text or its
security's alias entry cannot be found -- see _common.rederive_row.
"""

import json

from _common import load_context, rederive_all


def main():
    gold_rows, articles_by_key, securities_by_key, universe_summary = load_context()
    total_in_newest_snapshot = len(gold_rows)
    examined = total_in_newest_snapshot  # every row of the newest snapshot is examined below

    agree, disagree, unmeasurable_text, unmeasurable_security = rederive_all(
        gold_rows, articles_by_key, securities_by_key
    )
    measurable = len(agree) + len(disagree)
    unmeasurable = len(unmeasurable_text) + len(unmeasurable_security)

    out = {
        "gold_rows_total_in_newest_snapshot": total_in_newest_snapshot,
        "gold_rows_examined": examined,
        "silver_text_available_count": total_in_newest_snapshot - len(unmeasurable_text),
        "measurable_rows_count": measurable,
        "unmeasurable_rows_count": unmeasurable,
        "unmeasurable_text_count": len(unmeasurable_text),
        "unmeasurable_security_alias_count": len(unmeasurable_security),
        "agree_count": len(agree),
        "disagree_count": len(disagree),
        "inputs_recomputed_from_text": [
            "mention_in_title", "mention_in_lead", "mention_count", "share",
        ],
        "inputs_not_recomputable": [],
        "universe_alias_source": universe_summary.get("universe"),
        "disagreeing_rows": disagree,
        "unmeasurable_text_rows": unmeasurable_text,
        "unmeasurable_security_rows": unmeasurable_security,
    }
    print(json.dumps(out, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
