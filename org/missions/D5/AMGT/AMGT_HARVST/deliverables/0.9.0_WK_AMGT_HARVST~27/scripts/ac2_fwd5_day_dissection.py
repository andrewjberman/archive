"""AC2 -- FWD-5 EXERCISED ON LANDED GOLD through `timeline_api.get_timeline` /
`get_timeline_day`, fed by loaders that read the landed `chatter_daily` / `article_security_mention`
gold snapshots and the landed silver `article` rows (headline/published_precision). NO write, no
build, no vendor call, no change to `timeline_api.py`/`publication_gold.py`.
"""

import os
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.dirname(__file__))
import _gold_reader as gr  # noqa: E402

import lib.research.harvest.timeline_api as timeline_api  # noqa: E402


def _pairwise_sort_holds(rows):
    keys = [timeline_api._dissection_sort_key(r) for r in rows]
    violations = []
    for i in range(1, len(keys)):
        if keys[i - 1] > keys[i]:
            violations.append((i - 1, i, keys[i - 1], keys[i]))
    return violations


def main():
    client = gr.default_client()
    daily = gr.load_daily_rows(client=client)
    events = gr.load_event_rows(client=client)
    mention = gr.load_mention_rows(client=client)
    article_index = gr.load_article_index(client=client)

    daily_loader = gr.make_daily_loader(daily)
    event_loader = gr.make_event_loader(events)
    day_article_loader = gr.make_day_article_loader(mention, article_index)

    nonzero = sorted({r["security_key"] for r in daily if (r.get("articles_total") or 0) > 0})
    print("READ (restating AC1's cause): %d of %d landed securities carry a day with "
          "articles_total>0: %s" % (len(nonzero), len({r['security_key'] for r in daily}), nonzero))

    if not nonzero:
        print("FWD-5: UNEXERCISABLE -- restating AC1's cause: zero securities carry a day with "
              "articles_total>0 in the landed chatter_daily snapshot.")
        return 0

    lenovo = "992_HK_Equity"
    if lenovo in nonzero:
        chosen = lenovo
        print("CHOSEN SECURITY: %s (Lenovo, the spec's own acceptance security, section 8) -- "
              "confirmed exercisable by the read above, not assumed." % chosen)
    else:
        chosen = nonzero[0]
        print("CHOSEN SECURITY: %s -- NOT 992_HK_Equity (Lenovo). The spec's acceptance security "
              "(section 8) is NOT among the exercisable set this cell measured; %s is the first "
              "exercisable security in sorted order. THIS DIVERGENCE IS A FINDING, filed as a "
              "surprise row, not smoothed over." % (chosen, chosen))

    print()
    result = timeline_api.get_timeline(chosen, None, None, daily_loader, event_loader)
    if timeline_api.is_error_body(result):
        print("get_timeline returned an ERROR BODY, not data: %r" % (result,))
        return 1

    series = result["series"]
    days_in_series = [s["date"] for s in series]
    print("floor_date: %s" % result["floor_date"])
    print("series length (days returned): %d" % len(series))
    if series:
        print("first day: %s, last day: %s" % (days_in_series[0], days_in_series[-1]))

    import datetime
    first_date = datetime.date.fromisoformat(days_in_series[0]) if series else None
    last_date = datetime.date.fromisoformat(days_in_series[-1]) if series else None
    days_in_range = (last_date - first_date).days + 1 if series else 0
    print("PROOF OF NO GAP: days_in_range(first..last, inclusive) = %d ; days returned = %d ; "
          "equal = %s" % (days_in_range, len(series), days_in_range == len(series)))

    nonzero_days_in_series = [s for s in series if (s.get("articles_total") or 0) > 0]
    print("days in THIS security's own series with articles_total>0: %d of %d"
          % (len(nonzero_days_in_series), len(series)))
    if not nonzero_days_in_series:
        print("FWD-5: UNEXERCISABLE for %s specifically -- AC1 measured it nonzero over the WHOLE "
              "loaded history, but the resolved series (floor..latest landed day) carries none. "
              "This is itself a finding." % chosen)
        return 0

    # Pick the day with the MOST articles (ties broken earliest date) rather than merely the
    # first nonzero day, so the strongest-first proof below has more than one row to order.
    picked = sorted(nonzero_days_in_series, key=lambda s: (-(s.get("articles_total") or 0), s["date"]))[0]
    picked_date = picked["date"]
    print()
    print("PICKED DAY (highest articles_total among the %d nonzero days, tie-broken earliest): "
          "%s (articles_total=%s, data_status=%s)"
          % (len(nonzero_days_in_series), picked_date, picked["articles_total"], picked["data_status"]))

    day_result = timeline_api.get_timeline_day(chosen, picked_date, daily_loader, day_article_loader)
    if timeline_api.is_error_body(day_result):
        print("get_timeline_day returned an ERROR BODY, not data: %r" % (day_result,))
        return 1

    articles = day_result["articles"]
    print("data_status restated on the day route: %s" % day_result["data_status"])
    print("articles served for this day: %d" % len(articles))

    print()
    print("SERVED ARTICLE LIST, IN ORDER (the order the route actually returned):")
    for i, row in enumerate(articles):
        triple = (row["signal_tier"], row["mention_count"], row["published_utc"])
        print("  [%d] tier=%s mention_count=%s published_utc=%s | headline=%r publisher=%r "
              "mention_in_title=%r mention_in_lead=%r" % (
                  i, triple[0], triple[1], triple[2], row["headline"], row["publisher"],
                  row["mention_in_title"], row["mention_in_lead"]))

    violations = _pairwise_sort_holds(articles)
    print()
    print("STRONGEST-FIRST PROOF -- pairwise (tier_rank, -mention_count, published_utc) sort key "
          "checked across %d adjacent pairs: %d violation(s)" % (max(len(articles) - 1, 0), len(violations)))
    if violations:
        for v in violations:
            print("  VIOLATION at indices %d/%d: %r > %r" % v)
    else:
        print("  sort holds pairwise across the whole served list.")

    missing_fields = [
        f for row in articles for f in
        ("headline", "publisher", "signal_tier", "mention_in_title", "mention_in_lead", "published_utc")
        if f not in row
    ]
    print("EVERY row carries headline/publisher/tier/mention_in_title/mention_in_lead(present-even-"
          "when-false)/time: missing-field count = %d" % len(missing_fields))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
