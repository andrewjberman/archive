# /verify-channel Mode A — MDPF 49F Schwab re-derive (TO-1a) — 2026-06-01T1827Z

**VERDICT: 49F-slice PASS (5/5) ; GLOBAL aggregate CONCERN — sharpest-test-binds → CONCERN gates the data-half close.**
**Requester:** DS~B `[VERIFY-CHANNEL ASK]` 1822Z (TO-1a applied; Andrew/CTO PRD; gates close w/ DE serving-harness).
**Surface:** SERVED consumer-resolved feeds `json/mdpf/{49financial,global}/aggregate-aua-timeseries.json` (FRESH: generated_at 2026-06-01T18:21:19Z, rollup re-ran). Independent checks built vs spec, not DS~B code. Verifier≠fixer satisfied.

## 49F-slice — PASS (5/5)
1. **SEAM CLOSED:** 49F 5/15→5/18 `partner_custody_total` step = **$0** ($1,648,847,957 both; was −$156M); non_model step **+$8,732,091** (~+$8.7M normal; was −$172M). ✓
2. **CUSTODY-EXACT:** 4/15 custody = **$1,556,208,376** = $1,556.2M Schwab-restricted spec anchor (NOT full-book ~$1,699M); 1/16–5/18 all Schwab-range. ✓ *(Honest-limit: confirmed served==spec-anchor + Schwab-range; did NOT independently recompute Schwab-restricted from BD silver/allocations ∩ fees crosswalk — relied on the anchor match + range-plausibility.)*
3. **IDENTITY:** total=1a+1b+1c to **$0.0000** across the re-derived range; 12/26 $43M diff is the legacy pre-1/16 region (no 1c breakout), not a defect. ✓
4. **ESTIMATE-LABELING (CTO hard-honesty gate):** per-date `cohort_provenance` flags 1/16–5/17 `sma_1c: interpolated_estimate` (`custody`+`model_1a`=measured); `meta.basis_provenance.pre_1_16 = pending_andrew_disposition`. Honest. ✓
5. **NO 12/26 regression:** 12/26 custody = $1,335,552,885 **unchanged**; pre-1/16 `cohort_provenance=null` (untouched), re-derive provenance starts exactly at the 1/16 boundary. ✓

## GLOBAL aggregate — CONCERN (re-derive NOT propagated to pre-5/18)
The Schwab re-derive landed in the 49F SLICE but the GLOBAL rollup still carries **full-book 49F** for the 1/16–5/17 range:
- 4/15: global `opal_aggregate_aua` = **$1,699,280,891** vs 49F-slice custody **$1,556,208,376** → diff **+$143,072,516 = exactly the Schwab-restriction delta** ($1,699M full-book − $1,556M Schwab). global `model_aua` == 49F `model_aua` to the dollar (so global sources 49F model fine) — it is specifically the **full-book custody/non_model** that didn't propagate; global non_model @4/15 is full-book-inflated.
- Consequence: global 5/15→5/18 shows a **−$62.4M residual step** (full-book-49F → Schwab-49F+inflection-2a transition), NOT the clean ~+$93.6M inflection-funding step a closed seam would show. Verified post-5/18 global IS correct (5/18 agg $1,742.5M = Schwab-49F $1,648.8M + inflection-2a $93.6M); the gap is the pre-5/18 (1/16–5/17) range only.
- This contradicts the full-history Schwab-canonical PRD intent (eb6abc599) and DS~B's ask point-1 "49F + global seam closes." Class = rollup/cross-slice propagation gap (the partition-vs-serving lesson at slice-vs-aggregate level): the 49F partitions re-derived, but the GLOBAL aggregate's pre-5/18 range did not re-source the re-derived 49F.

## Routing
**CONCERN → DS~B (CC COO+CTO).** 49F-slice is clean; the close is gated on GLOBAL. FIX: re-aggregate/re-derive the GLOBAL pre-5/18 (1/16–5/17) range onto Schwab-49F (same basis the slice now uses) so global custody/non_model + the trend close the seam (expected: 5/15 global ≈ Schwab-49F, 5/18 step ≈ +$93.6M inflection-funding only). Then re-verify global. DE serving-harness in parallel may corroborate. Step-3.5: Andrew reads the GLOBAL trend — the −$62M residual cliff would render as a real (false) drop.

---
## RE-VERIFY (CVO 1835Z, post DS~B aggregate-headline fix) — AXIS-1 CLEARED
DS~B fixed the TO-1a global leg (recomputed each partition's aggregate-headline from corrected partners, re-rolled). Independent re-verify of fresh served global feed (generated_at 2026-06-01T18:34:10Z):
- **4/15 global opal_aggregate_aua = $1,556,208,376 = Schwab** (was $1,699.3M full-book) — **+$143M propagation gap CLOSED**; now equals 49F-slice custody to the dollar (pre-Inflection). ✓
- **5/15→5/18 opal step = +$93,603,055** (clean Inflection-2a onboarding; was −$62M cliff) — **headline seam CLOSED**; largest 1/16–5/29 opal steps are the legit +$93.6M @5/18 + normal market moves ($34.8M/$31.8M). No headline residual cliff. ✓
- **−$89,001,092 non_model step @5/18 correctly isolated to TO-1c** (Inflection pre-5/18 backfill-vs-live re-basis) — NOT a 49F/aggregate-headline issue. Confirms the emit-gap (TO-1a, now fixed) vs Inflection-re-basis (TO-1c) separation.

**AXIS-1 (TO-1a global leg) = CLEARED.** My GLOBAL CONCERN on the headline is RESOLVED. MDPF data-half close still gated on **AXIS-2 (TO-1c Inflection re-basis, CTO authoring)** — the −$89M non_model step persists until TO-1c lands; final global re-verify (full identity + non_model continuity) fires then.
