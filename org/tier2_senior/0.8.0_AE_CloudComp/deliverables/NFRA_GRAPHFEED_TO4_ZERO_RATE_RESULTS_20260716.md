# TO-4 measurement follow-up -- ZERO-RESULT RATE, both eras under ONE construct (CLOSED)

**Author:** 0.8.0_AE_CloudComp~Z · **Date:** 2026-07-16 ~14:05Z · **Method authority:** CTO ruling
(the cohort-R construct was never durably recorded at row grain; "define YOUR construct, print it,
re-derive BOTH sides under it"). Harness: deliverables/comp_which_zero_rate_harness.py @ 818ae80d8.

## The construct (printed verbatim from the run)

> Replay every DISTINCT logged routing query through ONE FIXED ranker -- `.tools/comp-which
> --json` at blob 266f205a094d. A routed outcome is ZERO-RESULT iff the ranker returns
> routed == [] (kind=fallback/abstain: comp-which serves no candidate and hands off to a search
> primitive). Era zero-rate = occurrences-weighted zero queries / era routing decisions.

## The numbers (100% coverage both eras; 0 timeouts, 0 unparseable)

| Era | Routing decisions | ZERO | SERVED | Zero-rate |
|---|---|---|---|---|
| PRE (< 2026-07-13T22:07Z, before c52f83612) | 8,114 | 172 | 7,942 | **2.12%** |
| POST (>= cut) | 2,105 | 13 | 2,092 | **0.62%** |

Replay: 876 distinct queries (805 pre / 130 post / 56 overlap), 2026-07-16 13:35:29Z ->
14:03:48Z. **POLLUTION WINDOW: rail-log rows appended in that window are replay artifacts --
exclude the window from future tallies** (the probe set is drawn from the log itself; a replayed
q is byte-identical to an agent asking it -- the routing-test's own control note).

## What this measures -- and what it does not (stated before anyone quotes it)

- It measures: of the questions agents ACTUALLY ASKED in each era, the fraction TODAY'S
  catalog+ranker serves NOTHING for (hard abstain). One instrument, both populations --
  the comparison measures the QUERY POPULATIONS against one catalog, per the CTO ruling's
  "one construct applied to both sides measures the build" discipline taken to its honest
  limit: era-2 questions were asked WITH the build live, so no log-only construct can
  isolate the build's causal effect; this one does not pretend to.
- It does NOT reproduce the SS0-errata **34.0%**: that was cohort-R's CONTENT-level
  adjudication (was the routed answer decision-USEFUL) under its own filter -- a strictly
  richer bar than serves-nothing. Both can be true at once: comp-which rarely serves NOTHING
  (0.6-2.1% here) while a larger share of routings may fail a usefulness bar. **34.0% stays
  cited as a prior measurement with its own filter -- history, never row-compared.**
- The PRE->POST drop (2.12% -> 0.62%) is CONSISTENT WITH (not proof of) the c52f83612-era
  improvements: the post-era question population resolves against the current catalog almost
  everywhere, and the 13 post-era ZEROs include the deliberate gibberish-control rows (the
  programmatic abstain working as designed on questions DESIGNED to have no answer).

## Disposition

TO-4's last open measurement cell is CLOSED. If a decision-useful-ness bar is wanted (the
cohort-R construct's true successor), that is a CONTENT-adjudication build -- new scope, its
own TO, not smuggled into this number.
