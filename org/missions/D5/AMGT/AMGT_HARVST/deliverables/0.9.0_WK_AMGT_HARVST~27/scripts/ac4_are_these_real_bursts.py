"""AC4 -- JUDGMENT, PRESENTED AND NOT GRADED. `3.0.0_SA_CVO` is the oracle at L9 (task order
section 5 / bounds). This script PRESENTS every landed `chatter_event` row (span, lead_headline,
articles_total, publishers_distinct, plus the headlines of every article in the span) and offers
a plain-English observation of whether the lead headline plausibly names what the burst was
about -- an OBSERVATION for the oracle to weigh, never a PASS/FAIL this cell records. If no
`chatter_event` row exists at all, this falls back to the day-level question the criterion names
as its alternate arm. No S3 write, no build, no vendor call, no change to any producer module.
"""

import os
import re
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.dirname(__file__))
import _gold_reader as gr  # noqa: E402

# A tiny stopword set for the OBSERVATION'S word-overlap heuristic ONLY -- excluded so a shared
# "for"/"the"/"a" does not read as topical overlap it is not. Never used anywhere the criteria
# grade; this script records no verdict regardless.
_STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "in", "is", "it",
    "of", "on", "or", "that", "the", "this", "to", "with", "its",
})
_WORD_RE = re.compile(r"[a-z0-9']+")


def _content_words(text):
    return {w for w in _WORD_RE.findall((text or "").lower()) if w not in _STOPWORDS and len(w) > 2}


def main():
    client = gr.default_client()
    daily = gr.load_daily_rows(client=client)
    events = gr.load_event_rows(client=client)
    mention = gr.load_mention_rows(client=client)
    article_index = gr.load_article_index(client=client)

    event_article_loader = gr.make_event_article_loader(mention, article_index)

    print("STATUS: UNVERIFIABLE-BY-INSTRUMENT")
    print("status_reason: this criterion is JUDGMENT (task order section 5, AC4); the oracle is "
          "3.0.0_SA_CVO at L9. This script presents counts and text only and records no verdict.")
    print()

    if not events:
        denom = len({r["security_key"] for r in daily})
        print("chatter_event holds ZERO rows for every security (denominator: %d landed securities)."
              % denom)
        print("CAUSE, restated from AC1: no (security, day) has ever reached "
              "EVENT_MIN_PUBLISHERS=%d distinct publishers on tier A/B coverage." % gr.pg.EVENT_MIN_PUBLISHERS)
        print()
        print("FALLING BACK TO THE DAY-LEVEL QUESTION the criterion names as its alternate arm: "
              "do the highest mention_score days correspond to a day a reader would call a burst?")
        top_days = sorted(daily, key=lambda r: -(r.get("mention_score") or 0.0))[:10]
        for row in top_days:
            print("  security=%s day=%s mention_score=%.3f articles_total=%s tier_a=%s tier_b=%s "
                  "tier_c=%s tier_d=%s publishers_distinct=%s data_status=%s" % (
                      row["security_key"], row["day"], row.get("mention_score") or 0.0,
                      row.get("articles_total"), row.get("tier_a"), row.get("tier_b"),
                      row.get("tier_c"), row.get("tier_d"), row.get("publishers_distinct"),
                      row.get("data_status")))
        return 0

    print("chatter_event ROWS PRESENTED: %d total" % len(events))
    print()

    for e in sorted(events, key=lambda r: (r["security_key"], r["first_day"])):
        articles = event_article_loader(e["security_key"], e)
        headlines = [(a["signal_tier"], a["publisher"], a["headline"]) for a in articles]
        print("EVENT security=%s span=[%s .. %s] days_span=%s" % (
            e["security_key"], e["first_day"], e["last_day"], e["days_span"]))
        print("  articles_total=%s tier_a=%s tier_b=%s publishers_distinct=%s"
              % (e["articles_total"], e["tier_a"], e["tier_b"], e["publishers_distinct"]))
        print("  lead_headline: %r (lead_article_key=%s)" % (e["lead_headline"], e["lead_article_key"]))
        print("  ARTICLES IN SPAN (%d):" % len(headlines))
        for tier, publisher, headline in headlines:
            print("    tier=%s publisher=%s headline=%r" % (tier, publisher, headline))

        lead_words = _content_words(e["lead_headline"])
        other_headline_words = set()
        for _tier, _publisher, headline in headlines[1:]:
            other_headline_words |= _content_words(headline)
        shared = lead_words & other_headline_words
        if len(articles) <= 1:
            observation = ("only one article in this span (the lead itself); no co-article to "
                            "compare the lead headline against")
        elif shared:
            observation = ("the lead headline shares word(s) %r with at least one other article "
                            "in the span -- plausibly the same underlying topic" % (sorted(shared)[:6],))
        else:
            observation = ("the lead headline shares NO word with the other article(s) in the span "
                            "(e.g. a co-mentioned article about a different company/topic) -- the "
                            "span may be a shared industry item rather than news specific to %s"
                            % e["security_key"])
        print("  OBSERVATION (not a verdict): %s" % observation)
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
