# /verify-channel — ADVI_INFDEMO F5 data-verification (Peter Lee book), Inflection demo TODAY

**Verifier:** 3.0.0_SA_CVO (independent; empirical source read, not display). **Requested by:** COO /drive 1352Z (Andrew-direct "verify some of the data").
**Sources read (own read):** `s3://opal-data-inf/platinum/advisors/peter_lee/book.json` + `gold/canonical/holdings_2026-05-27.parquet`. **Time:** 2026-05-28T~1355Z.

## VERDICT: PASS — demo-surfaced facts are data-grounded + correct. Two non-blocking flags (1 data-side, 1 display).

### AC5.2 — headline numbers: GREEN (penny-exact vs canonical)
Independent canonical parquet read (`holdings_2026-05-27.parquet`, 30,800 rows):
- **Peter Lee AUA = $166,115,472** (canonical) == $166,115,472.09 (book.json headline) — exact.
- **Firm AUA = $205,617,542** ($205.6M) — matches Andrew ground truth ($205.53M).
- **Peter Lee distinct accounts = 611** (canonical, holdings-bearing).
- 631-vs-611 reconciled: book.json `account_count=631` (total) vs `account_count_with_perf/billing=611` (holdings-bearing). The ~20 gap = zero-holding accounts (incl. shadow household below). Demo's "611" = the canonical holdings-bearing count.
- Artifact-provenance bonus: book view reads the CORRECT canonical ($205.6M), NOT the inflated `gold/holdings/2026-05-26` ($347.9M). Clears the PRD §F4 second-artifact-divergence worry for the Peter Lee book view.
- fee-paying: 184/199 households fee-paying (15 non-fee); weighted avg fee 95.57 bps (~1.02%).

### AC5.1 — "Raeleen Tillett = newest relationship": TRUE (data-grounded), with 2 flags
- Raeleen Tillett (household_id 1352) genuinely holds the MAX `relationship_since` = 2026-04-23 across Peter Lee's 199 clients[]. NOT a sort/display artifact — the underlying data supports the claim.
- **FLAG 1 [DATA-SIDE → DS]:** "Raeleen Tillett" appears as TWO households: hh 1352 (rel 2026-04-23, $998,911 AUA, 3 accts) AND shadow hh 511 (rel 2025-09-23, **$0.01 AUA, 4 empty accts**). Duplicate-name / possible dup-household. The $0.01 shadow could surface awkwardly in a client list; it also drives part of the 631-vs-611 zero-holding-account gap. DS: investigate dup-household vs genuine namesake; decide whether zero-holding accounts belong in `account_count`.
- **FLAG 2 [DISPLAY/LABEL → RD, low-pri]:** "newest" is a TIE — "Therese & Gregory Gesell" also rel 2026-04-23. Demo picks Raeleen via sort order. Fine if the demo only needs *a* newest; flag only if it asserts "THE single newest."

## Routing
PASS → COO (requester) + CC CTO + DS base (Flag 1) . Neither flag blocks the demo: the core claim is true + the headline numbers are canonical-exact. Flag 1 is the one worth a quick DS look before/after demo (shadow household hygiene).
