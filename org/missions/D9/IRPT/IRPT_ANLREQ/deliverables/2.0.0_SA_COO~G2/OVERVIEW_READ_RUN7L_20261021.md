# Run 7L read: the Overview with the kept unknown ticker ZQXWVK on r34s -- 2026-10-21

**From:** `2.0.0_SA_COO~G2`. **Order:** Y2's `TO-RUN-COMMENTARY-E2E-7L` (CTO-approved, msg 11970). **Receipt (IB2):** `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7l/A_E2E7L.txt` (RUN-DONE PASS). **PDF:** `C:/dev/andrew_samples/Opal_Overview_sample_post_r34s.pdf`, 260336 bytes, sha256 `be9b2b7bc891`, 42 pages, outside the repository; the r34p sample is untouched. Claim class: MEASURED from the receipt and from `pypdf` text of the PDF (this seat read the text, not the rendered pages).

## What the run shows (S220, the live read)
| item | measured |
|---|---|
| door, Keep of the unknown ticker | `upload keep=sent reason=TICKER_NOT_FOUND:Our data provider does not recognize this ticker, so it may be a typo. ... leave it for Opal Staff, who will manage the replacement.` (9 posts; the only TICKER_NOT_FOUND was ZQXWVK; SPY, AGG, TIMXX answered TICKER_KEPT_BY_HISTORY) |
| composition and job | submit ok, variant overview, READY at 09:45:21Z; the journal has no `retained_for_retry` line; packager ATTACHED; audit AUDIT_WRITTEN |
| kept row | `ZQXWVK resolution=UNRESOLVED method=KEPT_AS_TYPED, swap NOT_ANALYSED` |
| the raw placeholder | `{portfolio_name}`: 0 of 42 pages (receipt R5, and this seat's own count over the PDF text: 0) |

**S220 as filed (run 5B: a kept-as-typed unknown row accepted by the door, then refused `CLOSED_COMPOSITION_REQUIRED`) does not recur on r34s.** The refusal is gone; the first-hop reason is shown by the door in words. My earlier inference (S220/S222 disposition note) attributed the original refusal to the S245 packaging defect cured in r34q; this run is consistent with that and does not prove the cause.

## What the run does not show, stated plainly
- **ZQXWVK does not appear anywhere in the 42 pages** (this seat searched the PDF text for the token: 0 hits). The report does not state that a kept row was left out of the analysis. Whether that is the intended presentation, or a line saying so is wanted, is the CTO's call; it is not a failure of FWD-10.
- **Unchanged from the r34p sample, not caused by this release:** page 21 (report page 7, Risk Info) prints "The kept answer is not a readable table." six times (Alpha, Beta, Sharpe, Sortino, Max Drawdown, Monthly VaR) in both the r34p and r34s samples (6 occurrences each, counted). The sections route read 29 VALUE and 89 NOT_AVAILABLE. This is an FWD-9 (Overview) matter; it is raised for the CTO's enrichment list, not changed here.
