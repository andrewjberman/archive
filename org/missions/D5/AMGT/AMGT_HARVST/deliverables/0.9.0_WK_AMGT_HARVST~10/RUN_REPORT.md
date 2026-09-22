# AMGT_HARVST HVST-h-10 -- RUN_REPORT (Phase 1, 2026-09-22)

Issuer: `2.0.0_SA_COO~Y`. Assignee: `0.9.0_WK_AMGT_HARVST~10`. Grant: `1.0.0_SA_CTO~Z` msg 24390
(records @`c5f33fe8a3`), "one further publications run for `992_HK_Equity` covering Bloomberg.com,
FT, WSJ, Barron's, plus a Seeking Alpha pass that persists the received bytes", conditioned on the
CLI harvest wiring being fixed and verified first (done at checkpoint commit `b48efb29c6`).

## Sizing (printed before the run, item 3)

`plan.json` (S3-watermark read only, zero vendor calls): 5 publishers x 25 planned listing pages
each = **125 total planned listing pages**. Saved at `plan.json`, timestamped before item 4.

## The ONE live run (item 4)

Invocation:
```
python -m lib.opal_data_harvest run --runtime-root <main-worktree>/.runtime/opal-data-harvest \
  --publishers sa bbg ft wsj barrons --retrieval-mode backfill --floor 2026-01-01 \
  --security-json lenovo.security.json --bbg-symbol-probe --harvest-grammar --max-jobs 5
```
Run once, at 2026-09-22T23:13:55Z, NOT wrapped in `timeout`. rc=1.

**Outcome: the bbg symbol probe made a real vendor call and received a real verification
challenge from bloomberg.com (`VerificationRequired`), and that exception is UNCAUGHT in
`__main__.py`'s run handler -- it crashed the whole CLI process before `Worker.run()` was ever
reached.** Filed as row `AMGT_HARVST-Z-W10-S4` (ARMED, disarm_owner `2.0.0_SA_COO~Y`): this cell's
Phase-0 fix makes the probe run *inside* the five-publisher fetch on the probe's SUCCESS path, but
a probe FAILURE still prevents the fetch from starting at all -- a narrower echo of the original
`-S1` defect. This is the ONE authorized live vendor-call invocation (the ONE-RUN RULE); it is not
repeated. No second live vendor-call invocation was made.

Per-publisher table:

| publisher | status | planned pages | actual pages | accepted | rejected | stop reason |
|---|---|---|---|---|---|---|
| bbg | UNRESOLVED-CHALLENGED | 25 | 0 | 0 | 0 | Real vendor call (`news()` against bloomberg.com) returned a verification challenge (`transport.VerificationRequired`); the saved session is ~186h old. Consistent with the order's own SESSION STATE note. NOT retried per the ONE-RUN RULE. |
| sa | UNRESOLVED-NEVER-STARTED | 25 | 0 | 0 | 0 | The invocation crashed on the bbg probe before `Worker.run()` was reached; sa's own fetch never began. Zero http events for sa (events.jsonl unchanged, 233 before/after). |
| ft | UNRESOLVED-NEVER-STARTED | 25 | 0 | 0 | 0 | Same as sa: crashed on the bbg probe before `Worker.run()`. |
| wsj | UNRESOLVED-NEVER-STARTED | 25 | 0 | 0 | 0 | Same as sa: crashed on the bbg probe before `Worker.run()`. |
| barrons | UNRESOLVED-NEVER-STARTED | 25 | 0 | 0 | 0 | Same as sa: crashed on the bbg probe before `Worker.run()`. |

**Bloomberg symbol-probe verdict: UNRESOLVED** -- real vendor call made, real verification
challenge received, not adopted. Reason: stale (~186h) parked session, per the order's own
measured SESSION STATE note; the probe tried once, per the trial word's own cap ("Bloomberg's
per-symbol `news()` is tried once in the validation run").

`--harvest-grammar` was passed (the row `-S2` fix); the harvest_client-gated write path inside
`Worker.run()` was never reached this invocation either, because the crash happened before
`Worker` was constructed at all. This run cannot demonstrate the fix's positive case (a real
bronze/silver write) -- only that the wiring itself is present and correct in isolation, already
proven at the checkpoint by AC7/AC8 and their mutant control.

## Upload (item 5)

`upload-harvest --retrieval-mode backfill --max-objects 1000`: `{"results": [], "remaining_pending": 0}`.
Trivially satisfied -- nothing was captured to upload.

## Verify (item 6)

`bronze_reread 0 of 0 mismatch 0` -- zero bronze keys were put by this run (Worker never
constructed, harvest_raw_outbox/harvest_listing_outbox both measured 0 rows in the
2026-09-22T23:00Z+ window). `silver_article_rows 0 bronze_articles 0` (equal, trivially -- nothing
to compare). Planned-vs-actual listing pages: 25 planned / 0 actual for every one of the five
publishers (table above).

## The second same-day run, network refused (item 7)

Same command repeated with `HARVEST_REFUSE_NETWORK=1`, same UTC date (2026-09-22, both
23:13:55Z and 23:18:16Z). rc=1. The bbg probe's own `PacedSession.__init__` raised
`RuntimeError('network refused')` immediately, before any I/O -- the refuser fired correctly with
zero real network activity -- but that exception is likewise uncaught and crashed the process
before `Worker.run()` was reached, so sa/ft/wsj/barrons never got their own replay attempt either.
`http_events 0`, `network_refused_hits 1` (the probe's own refusal; not 0, because a refusal
genuinely occurred, just not from a publisher's own job). Because item 4 wrote nothing to bronze,
there was nothing for any publisher to replay from regardless -- this run confirms the refuser
itself works cleanly (zero real network I/O) but cannot demonstrate FWD-3's replay-without-network
positive case for any publisher, since none of the five ever reached their own fetch attempt in
either invocation.

## Silver prefixes written

**None.** Nothing reached bronze, so nothing reached silver either.

## Stage-9 line (verbatim, for `AMGT_RESAPP`'s driver)

**stage 9 publications for 992_HK_Equity: 0 articles in silver, run 2026-09-22T23:13:55Z**

## Bottom line

Two defects, both filed:
- `AMGT_HARVST-Z-W10-S1`/`-S2` (predecessor's, this cell's Phase-0 fix): the CLI could not wire a
  `harvest_client` and could not combine `--bbg-symbol-probe` with a live five-publisher run.
  **Fixed and verified** (checkpoint commit `b48efb29c6`, AC7/AC8 PASS, mutant control fires).
- `AMGT_HARVST-Z-W10-S4` (this run): the fixed probe branch still crashes the whole invocation on
  a probe FAILURE (as opposed to a probe replacement, the original defect), because the exception
  is uncaught. This cell's one live-run grant was spent entirely on demonstrating that gap: a real
  vendor call to bloomberg.com was made, received a genuine verification challenge, and the
  uncaught exception prevented sa/ft/wsj/barrons from ever starting their own fetch in this
  invocation.

No second live vendor-call invocation was made. The ONE-RUN RULE was honored.
