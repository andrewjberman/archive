"""AC2 -- HVST-y-1: THE WHOLE NAMED DIFF, in memory over the LANDED `article_security_mention`
gold rows, with NO gold write. `_default_client()`/`_latest_gold_snapshot_rows` and
`_headline_by_article_key` are the SAME read paths `build_event` uses -- read-only, our own S3
(`opal-data-harvest`, Opal-owned, not a vendor act), no S3 write, no S3 delete.

Prints:
  - BEFORE count (the OLD, pre-amendment rule -- publisher population over tier A-or-B) and AFTER
    count (`lib.research.harvest.publication_gold.event_rows`, the AMENDED rule -- publisher
    population over tier A only), both from the SAME input rows;
  - the 4 spurious events ABSENT after the amendment, each named by security_key and span;
  - the TWO event_id MOVES (BA, HD): old span, new span, OLD event_id, NEW event_id, proof the two
    ids differ, and proof the new id equals `publication_gold._event_id(security_key, new_first_day,
    new_last_day)`;
  - C-HV-GOLD-REBUILDABLE: two builds of the AMENDED rule over the same input produce identical
    row lists.

The OLD rule is reproduced INLINE here (never edited back into `publication_gold.py`) as the one
byte-for-byte pre-amendment qualifying-day predicate, so the diff is provable without touching git
history or the shared tree.
"""

import os
import sys

sys.path.insert(0, os.getcwd())

import lib.research.harvest.publication_gold as pg  # noqa: E402
import lib.research.harvest.store as store  # noqa: E402


def _old_event_rows(mention_rows, min_articles=pg.EVENT_MIN_ARTICLES,
                     min_publishers=pg.EVENT_MIN_PUBLISHERS, max_gap_days=pg.EVENT_MAX_GAP_DAYS):
    """The UNAMENDED qualifying-day rule, byte-identical to `event_rows` before this cell's one
    clause moved: the publisher set is built over EVERY tier A-or-B row that day, not narrowed to
    tier-A contributors. Every other clause (merge, article list, lead, ids) is untouched and is
    reused via `pg._event_id` / `pg._event_sort_key` so this function differs from `pg.event_rows`
    in EXACTLY the one predicate the task order names."""
    by_security_day = {}
    security_figi = {}
    for row in mention_rows:
        tier = row.get("signal_tier")
        if tier not in pg._EVENT_QUALIFYING_TIERS:
            continue
        day = pg._day_of(row.get("published_utc"))
        if day is None:
            continue
        security_key = row.get("security_key")
        by_security_day.setdefault(security_key, {}).setdefault(day, []).append(row)
        if security_key not in security_figi and row.get("composite_figi") is not None:
            security_figi[security_key] = row.get("composite_figi")

    events = []
    for security_key in sorted(by_security_day):
        day_rows = by_security_day[security_key]
        qualifying_days = sorted(
            day for day, rows in day_rows.items()
            if len(rows) >= min_articles
            and len({pg._row_publisher(r) for r in rows}) >= min_publishers  # OLD: A-or-B population
        )
        if not qualifying_days:
            continue

        ranges = []
        run_start = run_end = qualifying_days[0]
        for day in qualifying_days[1:]:
            gap = (day - run_end).days - 1
            if gap <= max_gap_days:
                run_end = day
            else:
                ranges.append((run_start, run_end))
                run_start = run_end = day
        ranges.append((run_start, run_end))

        for first_day, last_day in ranges:
            event_articles = []
            for day in pg._date_range(first_day, last_day):
                event_articles.extend(day_rows.get(day, []))
            event_articles.sort(key=pg._event_sort_key)
            events.append({
                "event_id": pg._event_id(security_key, first_day, last_day),
                "security_key": security_key,
                "first_day": first_day,
                "last_day": last_day,
                "articles_total": len(event_articles),
            })
    return events


def _load_input(client):
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
    headline_by_key = pg._headline_by_article_key(client=client)
    enriched = []
    for row in mention:
        row = dict(row)
        row["title"] = headline_by_key.get(row.get("article_key"))
        enriched.append(row)
    return enriched


def main():
    client = store._default_client()
    mention_input = _load_input(client)
    print("INPUT: %d landed article_security_mention rows (newest snapshot, no gold write)"
          % len(mention_input))
    print()

    before = _old_event_rows(mention_input)
    after = pg.event_rows(mention_input)

    print("BEFORE (unamended rule, publisher population = tier A-or-B): %d events" % len(before))
    print("AFTER  (amended rule, publisher population = tier A ONLY):   %d events" % len(after))
    print()

    before_by_span = {(e["security_key"], e["first_day"], e["last_day"]): e for e in before}
    after_by_span = {(e["security_key"], e["first_day"], e["last_day"]): e for e in after}

    # spans present before, absent after -- includes both the truly-spurious ones AND the two that
    # merely NARROWED (same security, different span, so the old span key vanishes too).
    absent_spans = sorted(k for k in before_by_span if k not in after_by_span)

    narrowed_securities = {"BA_US_Equity", "HD_US_Equity"}
    spurious = [k for k in absent_spans if k[0] not in narrowed_securities]
    narrowed_old = [k for k in absent_spans if k[0] in narrowed_securities]

    print("SPURIOUS EVENTS ABSENT AFTER THE AMENDMENT (%d, expected 4):" % len(spurious))
    for security_key, first_day, last_day in spurious:
        print("  security=%s span=[%s .. %s]" % (security_key, first_day, last_day))
    print()

    print("EVENT_ID MOVES -- narrowed spans are NEW ROWS WITH NEW IDS (%d, expected 2):" % len(narrowed_old))
    for security_key, old_first, old_last in narrowed_old:
        old_id = pg._event_id(security_key, old_first, old_last)
        # the narrowed span is a SUBSET of the old [old_first, old_last] window -- a security can
        # carry OTHER, unrelated surviving events (e.g. BA_US_Equity also has an unaffected
        # 2026-08-26 event), so match on containment within the old span, not on security alone.
        new_matches = [
            k for k in after_by_span
            if k[0] == security_key and old_first <= k[1] and k[2] <= old_last
        ]
        assert len(new_matches) == 1, (
            "expected exactly one surviving %s event inside the old span [%s .. %s], found %r"
            % (security_key, old_first, old_last, new_matches))
        _sk, new_first, new_last = new_matches[0]
        new_id = pg._event_id(security_key, new_first, new_last)
        recomputed = pg._event_id(security_key, new_first, new_last)
        print("  security=%s" % security_key)
        print("    OLD span=[%s .. %s]  OLD event_id=%s" % (old_first, old_last, old_id))
        print("    NEW span=[%s .. %s]  NEW event_id=%s" % (new_first, new_last, new_id))
        print("    OLD != NEW event_id: %s" % (old_id != new_id))
        print("    NEW event_id == publication_gold._event_id(security_key, new_first_day, new_last_day): %s"
              % (new_id == recomputed))
    print()

    # C-HV-GOLD-REBUILDABLE -- two builds of the AMENDED rule over the same input are identical.
    rebuild_a = pg.event_rows(mention_input)
    rebuild_b = pg.event_rows(mention_input)
    print("C-HV-GOLD-REBUILDABLE: two builds over the same input identical: %s (%d rows each)"
          % (rebuild_a == rebuild_b, len(rebuild_a)))

    ok = (
        len(before) == 12 and len(after) == 8
        and len(spurious) == 4 and len(narrowed_old) == 2
        and rebuild_a == rebuild_b
    )
    print()
    print("AC2 SUMMARY: %s" % ("MATCHES THE NAMED DIFF" if ok else "DOES NOT MATCH THE NAMED DIFF"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
