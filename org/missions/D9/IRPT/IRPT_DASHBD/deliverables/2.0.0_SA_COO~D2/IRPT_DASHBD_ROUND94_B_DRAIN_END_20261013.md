# IRPT_DASHBD round 94, workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~23:3xZ)

**Five cells, LOCAL or DEV-only, all `complete`;** round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 94`: orders=5, judgment=0). On the CTO's ROUND-94 ANALYSIS and msgs 7181 and 7192 (PRD v0.14, FWD-21). Round 95 (`DB-b-179`, the contract re-source) is its own drain-end:
[round 95](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/IRPT_DASHBD_ROUND95_B_DRAIN_END_20261013.md). Counts only; no client data in the repo; no served byte moved.

## What the five cells did

| cell | result |
|---|---|
| `DB-b-174` the contract (~140) | `org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json`: 117 members in the baseline's 8 sections, vendor-free, each naming its Opal gold source or ABSENT with its reason: 71 sourced, 46 ABSENT. Now version 0.2.0 (round 95). The FWD-20 figure map was found under the old FWD-9 numbering and folded in. |
| `DB-b-175` one household built from gold (~141, four seats) | One 49 Financial household of 3 accounts (from 311 eligible of 596 groups, chosen by a rule committed before any figure), 44 of 117 members filled, 73 absent (46 the contract's own). Counted proof read **30 of 30 within one dollar**: the activity ledger identity 9 of 9, activity ending value against return market value 12 of 12, activity beginning value against the previous return value 9 of 9; the window residual identity (true by construction) 16 of 16, recorded apart and not counted. 590 S3 reads, 0 writes, 0 vendor calls. **Reproduced by this seat**: the builder re-run from fresh S3 reads gave the same counts and the same sample, byte for byte, in a private folder. |
| `DB-b-176` the tab render (~142) | `PerformanceReport` renders all 117 members in the eight sections in order; an unavailable figure prints words, the fee basis is labeled; new files only; a test and a mutant; lint and typecheck 0; suite no worse. Portal branch `wk-IRPT_DASHBD-142-portal` @476736684d (local). |
| `DB-b-177` the export document (~143) | `PerformanceReportDocument` renders the same shape in the same order as 10 sheets with footers and the disclosure last, from the tab's view model; new files only. Portal branch `wk-IRPT_DASHBD-143-portal` @091ae64e95 (local). |
| `DB-b-178` the smoke fixes (~144) | YTD (and any window reaching back before the history) measured from the first measured day and labeled "YTD (from June 3rd, 2026)"; the export modal 672 to 1200 px. Re-cut as `cand/dell2/irpt-ytd-from-first-day-and-wider-export-modal` @0307376564 from origin/PROD, on origin, registered as an approval for Andrew (row `dell2-20261013T221411Z-3635` the newest; `…221352Z-cffa` is my duplicate, the CTO closes it). FDRXX is a gold-classifier matter (round 96); the export UNEXPECTED is IRPT_BCKEND's. |

## What this round did NOT do, and why

- **No hookup of the new components into the tab or the export.** Nothing serves a filled report: the sample builder writes a private file, the export bundle and the dashboard read route carry no `FilledReport`, so a mount would be a component with no data source or one fed by invented data. The hookup belongs behind a served read (a platinum report object and its route, IRPT_BCKEND's surface); this seat names that as the next enrichment rather than faking the feed. The three portal branches stay unmerged and unregistered until then.
- **Andrew's "sample display" is therefore not yet on a screen.** The way to give him that now, without client data in the repo: render the REAL private sample through the tab and export components into a local HTML/PDF kept in the private folder and show him that. This seat proposes it as a round-96 cell, with the FDRXX cell; it needs the CTO's word on the form (HTML for the tab, PDF for the export).
- **FWD-21 is not graded.** Its DONE WHEN is Andrew's own read, and it names three firms; this round built one 49 Financial household only, 44 of 117 members filled.

## What the sample cannot fill (counts and reasons)

Realized-lot members (the lot-realized table holds 4 trading days); the contributions-versus-withdrawals split and income (activity holds 4 trading days; backfill queued to `2.0.0_SA_COO~P2`); the fee-basis row (the return method table has no row for the method version the activity rows carry); every client-summary-sourced member (out of this cell's grant); the model-benchmark rows and the household return (no source). The trading calendar answered from its NYSE fallback on this box (`pandas_market_calendars` absent).

## Open

- Ledger leg L7: held on the 2026-10-14T11:41Z fire (`irpt-dashbd-thresholds-swap-20261013`); read with `checks/l5/l5b_read.py` after it.
- Round 96: FDRXX -> CASH under a never-widen pair (the CTO's order, msg 7258) and, if the CTO agrees, the private render of the real sample.
- Push state: LOCAL on box/dell2; the portal feature branch above is on origin.

-- 2.0.0_SA_COO~D2
