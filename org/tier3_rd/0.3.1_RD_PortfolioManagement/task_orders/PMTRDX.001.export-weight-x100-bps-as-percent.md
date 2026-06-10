# TO PMTRDX.001 — Portfolio Management export → Trade Submission: weight ×100 (bps rendered as percent)

**Class:** FIX (bug — explore then fix). **Author:** 1.0.0_SA_CTO (Andrew-direct 2026-06-03 1729Z). **Receiver:** RD~B (PM/Trade-Submission domain; MSTR-spawning). **Status:** closed -- COO verified-done sweep 2026-06-10 (Andrew directive; patch 13618900 rode portal v2.1.114 promote, RAVC2'd).

> **Determination (2026-06-03):** NOT a live bad-trade — broker order is CORRECT (Vident CSV `0.200000` = 0.20% for 20bps). The ×100 is a stored-record + display unit-contract violation: PM export Lambda wrote `securities[]` weights as percent-numbers into a DynamoDB field whose canonical unit (CTO ruling) is decimal FRACTION. Brief: `docs/briefs/pm-export-trade-submission-weight-x100-determination-20260603.md`.
> **Prep delivered to AE 0.7.0** (4 patches; py_compile+ruff validated): #1 `portfolio_excel_generator/lambda_function.py` build_trade_securities ÷100 + `weight_unit` marker (Vident CSV/Excel untouched); #2 both `trade-pipeline/*/excel_generator.py` aligned to fraction; #3 `remediate_weight_unit_pmtrdx001.py` (dry-run-first, scoped, marker-idempotent, `--apply` gated); #4 `trade-submission.ts` TradeSecurity type contract note.
> **Awaiting:** AE TF-deploy (#1 portfolio-management pipeline + #2 trade-pipeline) + gated remediation run + CVO e2e served-verify. COO-ruled non-urgent (no trade exposure). CTO releases close on CVO GREEN.

## Symptom (Andrew-direct, reported by Yang)

In the **Portfolio Management** portal tool, when you **export to push a trade into Trade Submission**, the trade values are **×100 too large** — they need to be divided down. Concrete example: a **20bps** (0.20%) buy of a stock shows up in the **Trade Details as "20% buy"** (i.e. a 0.20% intended weight rendered as 20% — a ×100 error). The export→submission path is applying one too many ×100 (or treating a fraction/bps value as if it were already a percent).

## Likely mechanism (hypothesis — VERIFY, don't assume)

A unit mismatch across the export→ingest→display chain. Candidate units in play: **bps (20)** vs **percent (0.20)** vs **fraction (0.0020)**. The ×100 is one layer treating a fraction/percent as the wrong unit. Starting pointers (CTO pre-trace, portal `src/`):

- **Export payload build:** `src/pages/PortfolioManagement/components/ExportModal.tsx` — passes `finalWeight ?? optimizedWeight` (see ~L85, payload ~L125). Confirm the UNIT of `finalWeight`/`optimizedWeight` at source (fraction 0.002? percent 0.20? bps 20?).
- **Submission contract:** `src/api/endpoints/trade-submission.ts` — `current_weight` / `proposed_weight` (L41-42), `weights_as_of`. Confirm the unit the trade-submission API/ingest EXPECTS.
- **Display:** `src/pages/TradeSubmission/components/TradeDetailsModal.tsx` (+ `TradeCard.tsx`) — where "20% buy" renders. Check if the ×100 is a display-format applied on top of an already-percent value (double-percent), vs a value genuinely submitted ×100.
- Also check `src/api/endpoints/portfolio.ts` (export source) + `useTradeSubmissionState.ts` / `useTradeSubmissionActions.ts` (ingest normalization).

The fix is a single ÷100 (or unit-normalization) at the CORRECT layer — find where the unit contract breaks (export emits unit X, consumer assumes unit Y) and fix it at the boundary, NOT by blindly /100 at the display (which would mask the real submitted value — a trade submitted at 20% when 0.20% was intended is a REAL wrong order, not just a display bug; determine whether the SUBMITTED value is wrong or only the DISPLAYED value).

## Scope / acceptance

1. **EXPLORE first:** trace a single trade (e.g. 20bps buy) end-to-end — PM grid value → ExportModal payload → trade-submission API request → stored/served → TradeDetailsModal render. Identify the EXACT layer where the unit breaks. Report the trace before patching (CTO/COO awareness — is the SUBMITTED order wrong, or only the display?).
2. **FIX at the boundary** where the unit contract is violated; preserve correctness end-to-end (a 20bps intent must SUBMIT as 0.20% / 0.0020 and DISPLAY as "0.20%"/"20 bps", not 20%).
3. **REGRESSION:** verify across magnitudes (1bps, 20bps, 250bps=2.5%, 100% full-position) and both buy/sell. Confirm no OTHER consumer of the export payload relied on the (buggy) ×100 value.
4. **Quality:** tsc + eslint clean; VALGATE D-1 (check if any `api/endpoints/*.ts` adapter touched → threads adapter gate). Rule 19 (portal main tree stays DEV). Visual smoke: export a known-bps trade, confirm Trade Details shows the correct percent/bps.
5. **Verify the SUBMITTED value, not just the rendered one** — pull the actual trade-submission record/artifact (per verify-against-served-artifact discipline); a display-only fix that leaves wrong orders submitted is NOT a fix.

## Deliverable

End-to-end trace (root-cause layer named) + the boundary fix + regression matrix + RAVC2 to COO + CTO. Rides a portal promote (v2.1.114+) on COO sequencing. If the bug is also in a backend/Lambda ingest (not pure FE), flag for AE — but first determination is the FE export/display path above.
