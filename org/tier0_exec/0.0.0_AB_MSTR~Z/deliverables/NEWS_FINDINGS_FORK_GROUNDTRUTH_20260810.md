# News-findings ground-truth — MSTR~Z fork verdict (2026-08-10 ~2200Z)

Context: Andrew challenged the TO-4d News census frozen-findings (verbatim @d2f2e01d9: "They're
looking in the wrong place then because that pipeline operates twice a day every day and its
August 2026") and ordered an in-session fork to track it down. Fork ran read-only, ~2152-2158Z.

## VERDICT: SPLIT — Andrew right about the pipeline; census right about one dead side-leg;
## the load-bearing finding (i) is REFUTED on mechanism.

**(i) "keyword drilldown chain FROZEN / modal serves EMPTY / newest item 2026-02-23" — REFUTED.**
- keyword-intelligence-generator RAN TODAY (log events 2026-08-10 ~11:22Z, ~7 min after the
  11:15Z trending cron): "COMPLETE: 20 written, 0 skipped, 0 errors / 20 total".
- Complete scan of opal-keyword-intelligence: 2,892/2,892 items, 20 items written EVERY day
  through 2026-08-10. **2026-02-23 is the table's OLDEST date (23 items), not its newest — the
  census read the wrong end of the sort.**
- The census's 2/2 empty probes: GPT-normalization + MAX_KEYWORDS=20 means only 5/44 cloud
  keywords matched exactly tonight ("fund commentaries" vs stored "fund commentary") — both
  probes fell in the non-overlap. Real gap, wrong mechanism attributed.
- Modal route (portal_data_proxy/lambda_function.py:1439+): cache-first, then 7-day partition
  fallback, then a designed _evolving_keyword_card (sentiment + up to 50 articles +
  analysis_pending) — structurally cannot serve "empty intelligence". (Source+data grounded;
  POST not exercised by fork or census.)

**(ii) "720 keyword-history keys frozen since 04-07, orphaned at HEAD" — CONFIRMED.**
360 keyword-history-summary/ keys newest 2026-04-07T14:40:49Z; opal-keyword-drilldown-generator
last log ~2026-04-07. Genuinely dead — but it is the HISTORY side-leg the modal no longer calls.
Dead AND unused: ~zero user impact.

**(iii) "trending/latest.json producer INFERRED-only" — freshness LIVE; hygiene nit stands.**
latest.json written today 21:17:21Z, 1s after layer3 DDB writes; crons 11:15/21:15Z ENABLED —
Andrew's "twice a day" exactly. Producer attribution remains timing-inferred (stale in-code
comment names the disabled publisher).

**Residual worth keeping:** per-day exact-match coverage of clickable cloud keywords is thin
(5/44 tonight before the 7-day fallback widens it) — a keyword-normalization/coverage tuning
question, NOT an outage.

**Disposition:** census F1/F2/F3 rows to be corrected on 0.5.0_AE~Z's lane before the semantic
pass consumes the News vertical (sequenced behind the Andrew-directed artifact-design work).
No fixes/monitors/commits made by the fork — read-only throughout.
