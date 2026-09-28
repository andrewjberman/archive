"""AC1 -- WHICH ARM IS EXERCISABLE, named BEFORE either FWD-5 or FWD-6 is exercised, with
denominators. READS the landed `chatter_daily` and `chatter_event` gold snapshots only (no
write, no build, no vendor call). A zero anywhere is reported WITH ITS CAUSE.
"""

import os
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.dirname(__file__))
import _gold_reader as gr  # noqa: E402


def main():
    client = gr.default_client()
    daily = gr.load_daily_rows(client=client)
    events = gr.load_event_rows(client=client)

    all_securities = sorted({r["security_key"] for r in daily})
    denom = len(all_securities)
    print("DENOMINATOR -- distinct securities carrying ANY chatter_daily row (the LANDED "
          "universe, measured live, not assumed): %d" % denom)
    if denom == 0:
        print("CAUSE: 0 chatter_daily rows of any kind landed -- no gold has been built yet.")

    nonzero = sorted({r["security_key"] for r in daily if (r.get("articles_total") or 0) > 0})
    print("SECURITIES with >=1 day carrying articles_total>0: %d of %d" % (len(nonzero), denom))
    print("THE SECURITY KEYS THEMSELVES (round 7 never named these): %s" % (nonzero,))

    per_security_event_count = {}
    for row in events:
        per_security_event_count[row["security_key"]] = per_security_event_count.get(row["security_key"], 0) + 1
    securities_with_events = sorted(per_security_event_count)
    print("chatter_event ROWS THAT EXIST AT ALL: %d total, spread over %d of %d securities"
          % (len(events), len(securities_with_events), denom))
    print("PER-SECURITY chatter_event row counts: %s" % (per_security_event_count,))
    if not events:
        print("CAUSE (if zero): publication_gold.EVENT_MIN_PUBLISHERS=%d and the per-security "
              "publisher coverage never reaches it." % gr.pg.EVENT_MIN_PUBLISHERS)

    max_publishers_distinct = max((r.get("publishers_distinct") or 0) for r in daily) if daily else None
    print("publishers_distinct MAXIMUM observed on any chatter_daily row: %r (EVENT_MIN_PUBLISHERS=%d)"
          % (max_publishers_distinct, gr.pg.EVENT_MIN_PUBLISHERS))
    if max_publishers_distinct is not None and max_publishers_distinct < gr.pg.EVENT_MIN_PUBLISHERS:
        print("CAUSE: no day, for any security, has ever reached EVENT_MIN_PUBLISHERS distinct "
              "publishers -- chatter_event is structurally empty for every security, not merely "
              "quiet.")

    print()
    lenovo = "992_HK_Equity"
    if nonzero:
        print("FWD-5 arm: EXERCISABLE -- %d securities carry a day with articles_total>0; "
              "%s is%s among them." % (len(nonzero), lenovo,
                                        "" if lenovo in nonzero else " NOT"))
    else:
        print("FWD-5 arm: UNEXERCISABLE -- zero securities carry a day with articles_total>0 "
              "(denominator %d); every landed day is the honest zero-articles state." % denom)

    if events:
        print("FWD-6 arm: EXERCISABLE -- %d chatter_event rows exist across %d securities; "
              "%s is%s among them." % (len(events), len(securities_with_events), lenovo,
                                        "" if lenovo in securities_with_events else " NOT"))
    else:
        print("FWD-6 arm: UNEXERCISABLE -- zero chatter_event rows exist for any security "
              "(denominator %d); max publishers_distinct observed is %r against "
              "EVENT_MIN_PUBLISHERS=%d." % (denom, max_publishers_distinct, gr.pg.EVENT_MIN_PUBLISHERS))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
