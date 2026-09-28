"""AC4 -- HVST-y-1, JUDGMENT, PRESENTED AND NOT GRADED. `3.0.0_SA_CVO` is the oracle at L9 (task
order section 4/AC4, section 5). STATUS is always UNVERIFIABLE-BY-INSTRUMENT.

Events are computed IN MEMORY, over the newest landed `article_security_mention` gold rows, with
`publication_gold.event_rows` -- the AMENDED rule (publisher population = tier A only). This is
deliberately NOT a read of the landed `chatter_event` S3 snapshot: that snapshot was built under
the UNAMENDED rule (12 rows) and this criterion is about the SURVIVING 8, per AC2. No gold write,
no S3 delete, no vendor call.

For each of the 8 events prints: security, span, lead_headline, articles_total,
publishers_distinct, tier_a/tier_b, and the headline of every article in the span (tier +
publisher alongside). Then states, per event, whether the lead_headline names what the burst was
about -- Andrew's own standard: an event about a DIFFERENT company's product is not this
security's burst. Presents the text; records NO verdict.
"""

import os
import re
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.dirname(__file__))

import lib.research.harvest.publication_gold as pg  # noqa: E402
import _gold_reader as gr  # noqa: E402

_STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "in", "is", "it",
    "of", "on", "or", "that", "the", "this", "to", "with", "its",
})
_WORD_RE = re.compile(r"[a-z0-9']+")


def _content_words(text):
    return {w for w in _WORD_RE.findall((text or "").lower()) if w not in _STOPWORDS and len(w) > 2}


def main():
    client = gr.default_client()
    mention = gr.load_mention_rows(client=client)
    article_index = gr.load_article_index(client=client)

    headline_by_key = {key: row.get("title") for key, row in article_index.items()}
    enriched = []
    for row in mention:
        row = dict(row)
        row["title"] = headline_by_key.get(row.get("article_key"))
        enriched.append(row)

    events = pg.event_rows(enriched)
    event_article_loader = gr.make_event_article_loader(mention, article_index)

    print("STATUS: UNVERIFIABLE-BY-INSTRUMENT")
    print("status_reason: this criterion is JUDGMENT (task order section 4, AC4); the oracle is "
          "3.0.0_SA_CVO at L9. This script presents counts and text only and records no verdict.")
    print()
    print("chatter_event rows PRESENTED (computed in-memory under the AMENDED rule, no gold "
          "write): %d total" % len(events))
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
        print("  OBSERVATION (not a verdict, Andrew's standard -- an event about a DIFFERENT "
              "company's product is not this security's burst): %s" % observation)
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
