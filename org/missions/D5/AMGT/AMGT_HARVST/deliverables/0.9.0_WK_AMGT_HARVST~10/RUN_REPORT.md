# HVST-h-10 RUN REPORT -- the ONE Lenovo harvester trial run

**Security:** `992_HK_Equity` (Lenovo Group; sa_symbol `LNVGY`, the US ADR line -- fallback file, since
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/universe.json` carries a Lenovo record
keyed by folder `"Lenovo 992 HK"` / `bloomberg_ticker.value "992 HK"` with `sa_symbol.status UNRESOLVED`, not
a `992_HK_Equity`-keyed record with a usable flat `sa_symbol` in the `--security-json` shape).

**Bottom line, stated first:** this cell's live run was interrupted by this worker's own error (an
erroneous `timeout 590` applied to item 4, which the task order's section 5 preamble explicitly names as
NOT a bounded criterion invocation), after real vendor calls to Seeking Alpha had already begun. Separately
and independently, **harvest_grammar mode -- the mechanism item 5's bronze/silver write depends on -- is
structurally unreachable from this cell's CLI** regardless of how the run is invoked or bounded: see row
`AMGT_HARVST-Z-W10-S2`. So even a correctly-bounded run of item 4 could never have produced a non-empty
`upload-harvest` receipt. No second live vendor-call invocation was made (the ONE-RUN RULE: real vendor
calls having occurred, re-spending the word is the issuer's/Andrew's call, not this worker's).

## Per-publisher

| publisher | status | planned_listing_pages | actual pages | stop reason | articles accepted | articles rejected (mention floor) | bronze/silver counts |
|---|---|---|---|---|---|---|---|
| sa | interrupted, job status `running` (never finalized) | 25 | >=2 listing pages fetched (27 HTTP calls: 2x account/info, 2x symbols/lnvgy/news, 23x article GETs) | killed mid-job by this worker's own `timeout 590` (row -S2) | 21 (locally captured: `.runtime/opal-data-harvest/runs/20260922T195934Z-sa-592d7d85bf.json` and per-article files under `publications/v1/sa/`) | 6 | bronze 0, silver 0 -- harvest_grammar mode never engaged (row -S2), so nothing reached `harvest_raw_outbox`/`harvest_listing_outbox` for `upload-harvest` to find, live run or not |
| bbg | UNRESOLVED, never started | 25 | 0 | live run invocation terminated before reaching this publisher (0 http events for bbg in the event ledger) | 0 | 0 | bronze 0, silver 0 |
| ft | UNRESOLVED, never started | 25 | 0 | live run invocation terminated before reaching this publisher (0 http events for ft) | 0 | 0 | bronze 0, silver 0 |
| wsj | UNRESOLVED, never started | 25 | 0 | live run invocation terminated before reaching this publisher (0 http events for wsj) | 0 | 0 | bronze 0, silver 0 |
| barrons | UNRESOLVED, never started | 25 | 0 | live run invocation terminated before reaching this publisher (0 http events for barrons) | 0 | 0 | bronze 0, silver 0 |

**Auth verdicts** (recorded in `first_run.summary.json.auth_verdicts`, before any listing/article call each
publisher would have made): sa AUTHENTICATED (confirmed live, 27 real 200 responses); bbg/ft/wsj/barrons
UNTESTED (the interrupted run never reached them, so their ~7.6-day-old sessions were never exercised).

## Bloomberg's per-symbol probe

**Verdict: UNRESOLVED.** `--bbg-symbol-probe` cannot be combined with a full five-publisher `run` in one
invocation: the built CLI's `run` handler branches on the flag BEFORE `Worker.run()` and, when set, probes
bbg only for every named security while ignoring `--publishers` entirely and never running the other four
publishers' fetch at all (`__main__.py:139-150`; HVST-h-3's own proof-of-spec artifact description says the
same thing verbatim: "in place of the normal fetch"). Trying it as a genuine live attempt would need a
SECOND live vendor-call invocation, exceeding the ONE-RUN RULE and the trial's "1 run for Lenovo" cap. Not
attempted. Row `AMGT_HARVST-Z-W10-S1`.

## Silver prefixes written

**None.** `upload-harvest --retrieval-mode backfill` (item 5) returned `{"results": [], "remaining_pending":
0}` -- nothing was pending, because nothing reached `harvest_raw_outbox`/`harvest_listing_outbox` (row
`AMGT_HARVST-Z-W10-S2`).

## Second same-day, network-refused run (item 7)

Run at `2026-09-22T20:27:02Z` (same UTC date as item 4's `2026-09-22T19:58:10Z` start). Result: all five
publishers raised `RuntimeError("network refused")` before any I/O (`http_events 0`, confirmed via the
event ledger: 0 new `"event": "http"` lines since the pre-run baseline) -- because nothing is held locally
in bronze/listing form for ANY of the five publishers (sa's 21 articles were captured to a local per-job
JSON cache and per-article files, never to bronze). `network_refused_hits 5` (not 0). This is the honest,
correctly-measured consequence of item 4's interruption plus the harvest_grammar wiring gap -- not a defect
in the network refuser or the paging/dedupe logic itself.

## The stage-9 line

`AMGT_RESAPP` stage 9 publications for 992_HK_Equity: **0** articles in silver, run 2026-09-22T19:58:10Z
(interrupted; see rows AMGT_HARVST-Z-W10-S1 and AMGT_HARVST-Z-W10-S2 for why, and for the 21 Seeking Alpha
articles genuinely fetched but not yet reachable by the bronze/silver write path).
