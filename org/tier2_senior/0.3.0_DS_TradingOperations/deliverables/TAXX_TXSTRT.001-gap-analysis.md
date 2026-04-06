# TAXX_TXSTRT.001 — Gap Analysis & Phase 1 Recommendations

**Agent:** 0.3.0_DS_TradingOperations
**Date:** 2026-04-06
**System Under Review:** `models/tax_strategy/trade_allocator.py` (1,632 lines)

---

## 1. System Overview

The Tax SMA Trade Allocator is a single-file Python CLI that processes Axioma optimizer output for 3 long/short SMA accounts ($3.7M combined AUM). It applies a 6-stage constraint cascade and produces Schwab-ready upload CSVs, per-security audit ledgers, run reports, and an LLM-generated executive summary.

### Data Flow (Current — Fully Manual)

```
Andrew manually:
  1. Runs Axioma optimizer per account -> exports Acct-N.xlsx workbooks
  2. Downloads Schwab SSAVAIL2.ASC (borrow availability, daily SOD file)
  3. Places files in models/tax_strategy/Trade/Trade YYYYMMDD/
  4. Runs: python trade_allocator.py "Trade/Trade YYYYMMDD" "Tax SMA Accounts (1).xlsx" "Trade/Trade YYYYMMDD/SSAVAIL2.ASC"
  5. Reviews console output + exec summary for cascade violations
  6. Manually uploads schwab_upload_acctN_*.csv files to Schwab platform
```

### Constraint Cascade (6 stages + budget cap)

| Stage | Type | Description |
|-------|------|-------------|
| 3a excludedSecurities | HARD | Remove divested tickers from account manifest |
| 3b htbValidate | HARD | Shorts must have borrow in SSAVAIL2.ASC; partial fills allowed |
| 3c maxWeight | HARD | No single position >1% long or <-1% short |
| 3d sectorBand | SOFT+HARD | Net sector active weight within band; long sector cap (15% SMA200, 7.5% SMA145) |
| 3e roundLot | HARD | Implicit — `math.floor()` throughout |
| 3f budgetCap | HARD | Each side <= strategy budget (100% SMA200, 45% SMA145) |
| 3X emhBand | HARD | Long vs short gross within 2% of each other |

Freed weight is redistributed via a two-pass reallocation: same-sector first (preserve neutrality), then cross-sector spillover ranked by alpha.

### Accounts

| # | Name | Strategy | Leverage | AUM | Divest |
|---|------|----------|----------|-----|--------|
| 1 | Chiles | SMA 200 | 1.0x | $1.0M | HD, NFLX |
| 2 | Nixon | SMA 200 | 1.0x | $750K | AAPL |
| 3 | Bump | SMA 145 | 0.45x | $1.95M | VIGAX, VMGM, VSGAX |

---

## 2. Code Quality Assessment

### Strengths

1. **Comprehensive audit trail.** Every constraint mutation is recorded in a SecurityLedger with full before/after state. Three output formats (mutations-only, full, event-level) give different views.
2. **Cascade-introduced vs optimizer-original violation classification.** The system correctly differentiates between sector violations that existed in the Axioma output and those created by the constraint cascade. This is critical for human review.
3. **LLM exec summary.** Calls Claude API via AWS Secrets Manager to generate natural language risk summaries — good for compliance records.
4. **Dual-key borrow lookup.** SSAVAIL2 is indexed by both CUSIP and ticker, handling FactSet security ID mismatches from Axioma.
5. **Budget cap with priority trimming.** Trims lowest-alpha longs / highest-alpha shorts first (correct alpha-preservation priority).

### Issues & Risks

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| 1 | HIGH | **No position reconciliation.** Allocator produces net-new trade lists. No comparison against current holdings — if run twice on the same day, it would double positions. No concept of "current portfolio state." | Missing entirely |
| 2 | HIGH | **No idempotency / run locking.** Output directory is overwritten on every run. No run ID, no historical tracking. Previous run outputs are destroyed. | `main()` L1584-1585 |
| 3 | HIGH | **SSAVAIL2.ASC parser is incomplete and fragile.** The current `parse_ssavail()` extracts only 3 fields (symbol, CUSIP, total_avail_qty) from a 200-char-wide record that contains 7 fields (prelim qty, locates qty, BTC qty, total qty, market value, short sale rate). It also skips header/trailer validation entirely — no client number check, no batch date extraction, no record count verification. Yang has already built a complete parser (provided separately) that extracts all fields, validates header/trailer, and reports record count mismatches. **Current parser also misreports "avail=0" when a security is absent from the file entirely** (e.g., WAT CUSIP 941848103 has no SSAVAIL2 record at all — it's not that borrow is zero, the security simply isn't listed). This distinction matters for compliance reporting. | `parse_ssavail()` L358-383 |
| 4 | MEDIUM | **Negative-alpha longs are not caught.** The reallocation spillover can assign freed weight to negative-alpha long positions (see Nixon FRMI incident). The sort rank places negative-alpha positions last but doesn't exclude them. | `_reallocate_to_survivors()` L548-551 |
| 5 | MEDIUM | **Sector weight tracking is mutable dict passed by reference.** `sector_long_wt` and `sector_short_wt` are modified in-place during reallocation. If the function were called twice or order changed, accumulated state would be wrong. | `_reallocate_to_survivors()` L612-617 |
| 6 | MEDIUM | **Budget cap trim sort is destructive.** `valid_longs.sort()` sorts in-place before trimming. If budget trim is close to zero, the re-ordering still changes position order for downstream stages. | L958, L997 |
| 7 | MEDIUM | **No validation of Trade List vs Workspace universe.** The system takes whatever the optimizer produces. If Axioma includes a security not in the expected universe, it passes through silently. | `build_securities_from_trade_list()` L443-491 |
| 8 | LOW | **Hardcoded constants.** MAX_LONG_WEIGHT_PCT (1.0%), SECTOR_BAND_TOLERANCE_PCT (0.1%), EMH_BAND_PCT (2.0%) are module-level constants. These should be strategy-specific — SMA 200 and SMA 145 may need different tolerances as AUM grows. | L39-42 |
| 9 | LOW | **No input validation on manifest.** If a row has unexpected types (string AUM, missing leverage), the script crashes with an unhelpful error. | `parse_manifest()` L331-355 |
| 10 | LOW | **exec_summary failed silently.** The 155814 run produced an empty file — the `except Exception` catch-all returns "" without surfacing the error to the operator. | `generate_exec_summary()` L1559-1561 |
| 11 | LOW | **openpyxl read_only mode memory.** Large Axioma workbooks (~4MB each) are loaded in read_only mode (good) but `wb.close()` is only called in main, not in error paths. | `main()` L1600, 1621 |

### SSAVAIL2 Parser: Current vs Yang's Parser

The SSAVAIL2.ASC file is a 60,383-line fixed-width file (200 chars/record) from Schwab's SOD short-sale availability feed. Batch date: 2026-03-31. Client: 0164.

**Current trade_allocator.py `parse_ssavail()`** extracts only:
- symbol (pos 1-10), cusip (pos 11-20), total_avail_qty (sign@78, qty@79-96)
- Returns two flat dicts (by_cusip, by_symbol) of `SsavailRecord` dataclass
- No header/trailer parsing, no validation, no rate data

**Yang's `parse_ssavail.py`** (provided by Andrew) extracts all 7 detail fields:
- prelim_ss_avail_qty, locates_qty, btc_qty, total_ss_avail_qty, total_market_value, short_sale_rate_pct
- Validates header (client_no, batch_date) and trailer (record_count cross-check)
- Returns structured (header, records, trailer) tuple — much richer for audit trail
- Has CSV export and CLI usage built in

**Recommendation:** Replace the inline `parse_ssavail()` in trade_allocator.py with an import of Yang's parser. The additional fields (especially `short_sale_rate_pct` and `total_market_value`) are valuable for:
1. Rate-aware borrow decisions (some borrows are uneconomical even if available)
2. Market value cross-check against AUM allocation
3. Distinguishing "not in file" from "in file with 0 availability" for compliance
4. Audit completeness — the current parser discards 80% of the available data

---

## 3. 04-02 Run Anomalies (Nixon Account)

The task order specifically flags the Nixon account cascade-introduced violations. Analysis from the run report:

1. **Business Services net +0.6927% vs +/-0.6% band (CASCADE BREACH).**
   - Root cause: PLTR (Business Services short, alpha +7.92 — *positive* alpha on a short) was the lowest-priority short. Budget trim removed 9 of 11 shares (-0.1717%), shrinking the short side of Business Services. EXLS long was reallocated +1 share (+0.004%). Combined effect: net shifted from +0.5214% to +0.6927%.
   - PLTR has *positive* alpha (+7.92), meaning it's a poor short candidate the optimizer included. Trimming it is correct behavior, but the cascade doesn't compensate for the sector imbalance this creates.

2. **Non-Energy Materials net -0.6501% vs +/-0.6% band (CASCADE BREACH).**
   - Root cause: GPK (Non-Energy Materials long, alpha -6.06 — *negative* alpha on a long) was budget-trimmed from 0.2117% to 0.0603% (-0.1514%). Short-side reallocations into AMCR (+0.0051%) and IP (+0.0047%) increased short weight. Combined: net went from -0.4989% to -0.6501%.

3. **FRMI negative-alpha long spillover.** Alpha = -2.65, received +1 share via spillover. The code sorts by alpha DESC for longs, so FRMI should be last in line — it only received spillover because higher-alpha candidates in other sectors were at their weight or sector caps.

**Pattern:** Budget cap (3f) and EMH trim (3X) run AFTER sector reallocation (3d) and don't re-check sector bands. The cascade is one-pass — there's no feedback loop to re-validate earlier constraints after later stages modify positions.

### Cross-Account Observations From Output Review

**Multiple exec summaries (5 files from 04-02):** The output/ directory contains exec summaries from at least 4 successful runs on the same day (134642, 135234, 161216, 162614) plus one failed/empty (155814). This confirms no run isolation — each re-run overwrites the CSVs and ledgers, only exec summaries accumulate because they're timestamped. The 4 successful summaries are substantively identical (same constraint actions, same violations), meaning the Axioma inputs didn't change between runs. The runs were likely iterative testing of the script itself.

**Schwab upload CSV format vs template divergence:** The Schwab upload template (from `Trade/schwab upload template.csv`) has no header row and uses format: `account_number,side,shares,ticker`. The generated CSVs match this format exactly — `2726-5115,B,77,A`. However, the template has account numbers as pure digits (`23772796`) while the generated files use formatted account numbers with dash (`2726-5115`). This suggests the manifest stores a display format, not the raw Schwab account number. This may or may not be correct for actual Schwab upload — needs confirmation.

**Acct-3 (Bump) is nearly untouched:** The SMA 145 account at 0.45x leverage had only 4 mutations total: WAT HTB block, SMMT same-sector replacement, and two minor budget trims (IT long, MTSI short). Every other position (309 of 313) passed through the cascade unchanged. This makes sense — at 0.45x leverage, individual position weights are well below the 1% cap, so the weight cap stage has nothing to do.

**WAT is truly absent from SSAVAIL2, not zero-availability:** Grepped the 60K-line file — no record for CUSIP `941848103` or symbol `WAT`. The closest match is `WATT` (CUSIP `29272C301`), a different security. The current audit log says "avail=0" which is misleading — the security simply isn't in Schwab's borrow universe.

**AVTR (replacement security) has ample borrow:** AVTR shows total_ss_avail_qty of 5,841,913,898 shares and market value $458M. The cascade allocated 789-1,158 shares depending on account — well within availability. Good replacement choice.

**Alpha preservation is measurable:** Every run report includes an AGGREGATE ALPHA section showing optimizer vs final. Across all 3 accounts, total alpha *increased* slightly post-cascade (Chiles: 14.070 -> 14.104, Nixon: 14.080 -> 14.131, Bump: 7.337 -> 7.365). This is because the cascade preferentially trims low-alpha positions and reallocates to high-alpha survivors. The alpha-preservation logic is working correctly.

**PLTR is a problematic position across accounts:** PLTR appears as a short in all accounts but has *positive* alpha (+7.92). It's consistently the first position budget-trimmed because shorts are trimmed in descending alpha order (worst shorts first). PLTR being positive-alpha means the optimizer included it for reasons other than alpha (risk/factor exposure). The budget trim aggressively cuts it (Nixon: 0.21% -> 0.04%), which is fine for alpha preservation but suggests the optimizer's PLTR allocation may not survive the constraint cascade well.

**GPK mirrors PLTR on the long side:** GPK has *negative* alpha (-6.06) but is allocated as a long. It's the first long position budget-trimmed. Combined with PLTR, these two "wrong-sign alpha" positions absorb essentially all the budget trim capacity across accounts.

---

## 4. What Is Currently Manual

| Step | Manual Action | Frequency | Time Estimate |
|------|--------------|-----------|---------------|
| 1 | Run Axioma optimizer per account (3 workbooks) | Weekly/biweekly | 15-30 min |
| 2 | Export optimizer results to Excel | Per run | 5 min |
| 3 | Download SSAVAIL2.ASC from Schwab | Daily (SOD) | 2 min |
| 4 | Place files in correct Trade/ folder | Per run | 2 min |
| 5 | Run `python trade_allocator.py` | Per run | <1 min |
| 6 | Review exec summary + risk notes | Per run | 10-20 min |
| 7 | Upload Schwab CSVs to platform | Per run | 5-10 min |
| 8 | Confirm execution / reconcile fills | Post-trade | 15-30 min |

**Total manual time per run: ~55-95 minutes.** Steps 1-2 depend on Axioma access (not automatable without Axioma API). Steps 3-7 are automatable.

---

## 5. What Could Be Automated

### Fully Automatable (no external dependencies)

| Component | Approach |
|-----------|----------|
| SSAVAIL2.ASC retrieval | SFTP pull from Schwab (if API/SFTP credentials available) |
| Run execution | Lambda or EC2 cron job triggered by S3 upload of Axioma files |
| Output archival | S3 versioned storage with run ID timestamps |
| Historical run tracking | DynamoDB table keyed by run timestamp + account |
| Pre-execution validation | Lambda that compares new allocations against current holdings |
| Schwab CSV upload | Schwab API (if available) or staged for manual upload |

### Partially Automatable (requires external access)

| Component | Blocker |
|-----------|---------|
| Axioma optimization | Requires Axioma API access or RPA |
| Post-trade reconciliation | Requires Schwab positions API |
| Real-time borrow monitoring | Requires intraday SSAVAIL feed |

---

## 6. Missing Features

| Feature | Impact | Complexity |
|---------|--------|------------|
| **Position reconciliation** | Cannot detect double-execution or partial fills | HIGH — needs current holdings feed |
| **Run history / versioning** | Previous outputs destroyed on re-run | LOW — S3 prefix by run timestamp |
| **Feedback loop in cascade** | Budget cap can break sector bands (Nixon incident) | MEDIUM — add sector re-validation pass after 3f/3X |
| **Negative-alpha guard** | Spillover can allocate to wrong-sign alpha positions | LOW — add alpha sign check in reallocation |
| **Strategy-specific parameters** | SMA 200 and SMA 145 share identical constraint constants | LOW — move to manifest or config |
| **P&L attribution** | No tracking of alpha impact from constraint mutations | MEDIUM — extend run report with realized alpha cost |
| **Multi-day position tracking** | No concept of trades vs. existing holdings | HIGH — needs position database |
| **Risk monitoring dashboard** | No real-time view of portfolio exposure | HIGH — portal page + Lambda API |

---

## 7. Phase 1 Recommendations (Minimum Viable Automation)

**Goal:** Make the existing workflow safer and more efficient without building new infrastructure. All changes are to the existing `trade_allocator.py` and local workflow.

### P1.1 — Run Isolation & History (Priority: CRITICAL)

**Problem:** Outputs overwrite on every run. No run ID. No history.
**Fix:** Generate a run ID (`{YYYYMMDD}_{HHMMSS}_{strategy}`) and write outputs to `output/{run_id}/`. Add a `runs.json` manifest at the output root tracking every run with metadata (accounts, timestamp, total positions, violations).
**Effort:** ~2 hours code change. No infrastructure.

### P1.2 — Cascade Feedback Loop (Priority: HIGH)

**Problem:** Budget cap and EMH trim break sector bands (Nixon incident).
**Fix:** After stages 3f and 3X, re-run sector band validation. If new breaches are found, apply targeted trimming to the breaching sector (lowest-priority positions first). Add a `3Y_postValidation` stage to the audit log.
**Effort:** ~4 hours code change. Requires careful testing against all 3 accounts.

### P1.3 — Negative-Alpha Spillover Guard (Priority: HIGH)

**Problem:** Reallocation can assign weight to wrong-sign alpha positions.
**Fix:** In `_reallocate_to_survivors()`, skip positions where alpha sign doesn't match side (negative alpha on longs, positive alpha on shorts). Log as `REALLOC_SKIPPED_ALPHA`.
**Effort:** ~1 hour code change.

### P1.4 — Input Validation (Priority: MEDIUM)

**Problem:** Bad input silently produces wrong output.
**Fix:** Add validation at the top of `main()`: check manifest column count/types, verify SSAVAIL2 has header/trailer records, verify each Acct-N.xlsx has "Trade List" and "General Constraints" sheets with expected headers. Fail fast with clear error messages.
**Effort:** ~2 hours code change.

### P1.5 — S3 Archival (Priority: MEDIUM)

**Problem:** Outputs exist only on local disk. No backup, no sharing.
**Fix:** After run completes, upload entire `output/{run_id}/` to `s3://opal-data-portal-v2/tax-sma/runs/{run_id}/`. Add `--upload` CLI flag. Use existing boto3 patterns from workspace.
**Effort:** ~2 hours code change. Uses existing S3 infrastructure.

### P1.6 — Adopt Yang's SSAVAIL2 Parser (Priority: MEDIUM)

**Problem:** Current `parse_ssavail()` extracts 3 of 7 fields, skips header/trailer validation, and conflates "absent from file" with "zero availability."
**Fix:** Add Yang's `parse_ssavail.py` to `models/tax_strategy/`. Refactor trade_allocator.py to import from it. Update `lookup_ssavail()` to return richer data (short_sale_rate, market_value) and distinguish absent vs zero. Update HTB audit logging to report "NOT IN SSAVAIL" vs "AVAIL=0."
**Benefit:** Enables rate-aware borrow decisions in Phase 2. Immediately improves audit accuracy. Batch date from header can be validated against trade date for staleness detection.
**Effort:** ~2 hours (parser already written, just integration + audit log updates).

### P1.7 — Exec Summary Error Handling (Priority: LOW)

**Problem:** LLM exec summary fails silently (see 155814 empty file).
**Fix:** Log the actual exception. If API call fails, write a structured text summary from the audit data instead (no LLM needed — just template the key numbers).
**Effort:** ~1 hour code change.

### P1.8 — Schwab Account Number Verification (Priority: LOW)

**Problem:** Generated Schwab CSVs use dash-formatted account numbers from the manifest (e.g., `2726-5115`) while the Schwab upload template uses raw digits (e.g., `23772796`). If the format matters for Schwab upload acceptance, this would cause upload rejection.
**Fix:** Verify with Andrew which format Schwab expects. If raw digits, strip dashes in `write_schwab_csv()`. If dash format is correct, document it.
**Effort:** ~15 minutes once confirmed.

### Phase 1 Priority Order

1. P1.1 Run Isolation (unblocks everything else — can't safely iterate without history)
2. P1.2 Cascade Feedback Loop (fixes the known Nixon violation pattern)
3. P1.3 Negative-Alpha Guard (prevents misallocation)
4. P1.4 Input Validation (prevents silent failures)
5. P1.5 S3 Archival (operational resilience)
6. P1.6 Yang's SSAVAIL2 Parser (richer borrow data, audit accuracy)
7. P1.7 Exec Summary Fallback (polish)
8. P1.8 Account Number Format (verify with Andrew)

**Total Phase 1 effort: ~15 hours of code changes.** All local, no Terraform, no Lambda, no infrastructure.

---

## 8. Phase 2+ Outlook (Not In Scope)

For future planning:

- **Phase 2:** Lambda-ify the allocator. S3 trigger on Axioma file upload -> Step Function -> constraint cascade -> output to S3 -> SNS notification with exec summary. Portal page for viewing run history and approving trades.
- **Phase 3:** Position reconciliation. Integrate Schwab positions feed. Track holdings state in DynamoDB. Compute incremental trades (new allocation minus current holdings).
- **Phase 4:** Real-time borrow monitoring. Intraday SSAVAIL feed -> Lambda -> alert if any held short loses borrow availability.
