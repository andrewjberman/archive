# MDPF_REVAMP -- CUTOVER co-sign package (aggregate_aua + A4)

**Author:** 0.4.0_DS_ClientPlatform | **For:** 1.0.0_SA_CTO + Andrew (cutover co-sign) | **Date:** 2026-07-21
**Gate:** N=3 STAGED-PARITY ACHIEVED (CTO S3 re-verify + DT date-joined parity + CVO from-scratch, 3/3 to
the penny, 0 unexplained). CUTOVER (promote gold/mdpf_revamp/* -> served) is the NEXT gate; AE publish is
HELD pending this co-sign. Every item below is a NAMED, EXPECTED, CORRECT change -- none is a defect.

## What cutover does
Promotes the serve-real revamp aggregate (`gold/mdpf_revamp/{firm}/aggregate_aua_timeseries.json`, ETags
6e072745.../a9778de4.../7d574a2d...) + A4 non_model_assets to the served path the portal reads. The revamp
CORRECTS the legacy served artifact in 5 ways the co-signers should SEE and expect (a "visible, correct
change," CTO's phrase), not be surprised by.

## The 5 co-sign items (all NAMED; grounded)

### 1. DUAL-READ + $10-20M Q-end drift (the cross-page consistency risk) -- needs TO-2 (later wave)
`ModelPortfolios.tsx` reads the AUM trend TWO ways: the REVAMP aggregate
(`getMdpfAggregateAUATimeSeriesByFirm` :367 per-firm + :380 global) AND the LEGACY `getAUMTimeSeries` :430
(the daily-trend chart + snapshot Total, per the :746 "canonical to the daily trend chart's last bar"
comment). The two ALREADY disagree: ModelPortfolios.tsx:284/:1192 -- "non_model_assets.time_series[Q].
enterprise_total ... uses a separately derived model_aum that DRIFTS $10-20M from aum-timeseries at
historical Q-ends (different publishers; reconcile is DS-side)".
- **Change at cutover:** the revamp aggregate becomes one of the two trends; the legacy aum-timeseries
  read remains until TO-2.
- **Correct + disposition:** TO-2 (CTO-ruled LATER WAVE, post-N=3) REPLACES the legacy aum-timeseries +
  aum-metrics FE reads with a revamp-derived source (single source -> kills the dual-read + the $10-20M
  drift). Until TO-2 ships, the page shows the trend two ways -- **co-sign that the residual dual-read is
  ACCEPTED for the interim, and TO-2 is the fix.** (Non-blocking for the aggregate cutover itself.)

### 2. A4 enterprise_total vs aggregate opal_aggregate_aua -- pre-cutover divergence (cross-page)
A4 (`non_model_assets`) does VERBATIM legacy passthrough pre-cutover (2024-11-01..2025-12-22) and derives
off the revamp aggregate post-cutover (2025-12-23+). So A4.enterprise_total (legacy passthrough) and the
aggregate opal_aggregate_aua (serve-real) DIVERGE pre-cutover, MATCH post-cutover (identity exact,
~A-verified $0.00 all post-cutover windows).
- **Correct:** intended by construction -- the frozen legacy pre-cutover rows are not monolith-derivable
  (served meta pre_cutover=verbatim_passthrough_from_legacy); Andrew-ruled trading-day axis. **Co-sign the
  pre-cutover verbatim passthrough boundary at 2025-12-22/23.**

### 3. 2026-05-21 legacy-imputed null (revamp NULLS a value the served page SHOWS)
Served inflection shows model $93,084,450.47 @2026-05-21. The eclipse FEED genuinely never carried 05-21
(bronze AND silver both lack the partition), so the served value is LEGACY-IMPUTED. Revamp serves an
honest None (D1 serve-real: no fabrication).
- **Change at cutover:** the page currently shows a value @05-21; the revamp will show a gap/null there.
- **Correct (CTO-endorsed 152015Z):** serve-real done right -- "revamp's honest None IS more correct."
  **Co-sign that a value visibly disappears at 05-21 (and it is the CORRECT behavior).**

### 4. account_count PRESERVE + seam-continuity (FLAG-2, co-sign-gated)
The revamp emits `account_count` = None placeholder (all firms, all dates) -- a co-sign-gated PRESERVE
(the served count[] is real daily-snapshots; None now, WIRED to the imported-real counts at cutover, exact
tie). Named `null_ok` in the ledger; DT classifies NAMED, not a mismatch.
- **Correct:** the count arrays are NOT lost -- they wire to real (== served, exact tie) AT cutover, when
  the null_ok entry is removed. **Co-sign the count-preserve import + a seam-continuity check (no
  discontinuity at the wire point).** (CTO pre-approved the PRESERVE 225137Z.)

### 5. inflection launch seam @2026-05-15 (model appears 3 days EARLIER than served)
Andrew-ruled (2026-07-21): inflection model = 0 until the 2026-05-15 launch, real eclipse after. Served's
legacy backfill deferred the model onset to 05-18 (first-nonzero 05-18). So the revamp serves the REAL
05-15 launch value ($94.5M) while served shows 0 until 05-18.
- **Change at cutover:** the inflection model line "turns on" at 05-15 instead of 05-18 (3 trading days
  earlier), reflecting the real launch date Andrew confirmed.
- **Correct:** launch seam CLEAN (0@05-14 -> $94.5M@05-15, no interpolation, no pre-ramp; CVO-confirmed
  analog to the UST 2025-01-16 launch). **Co-sign the 05-15 launch onset (Andrew's ruling made visible).**

## Publish/cutover mechanics (for the co-sign GO)
1. AE publisher copies `gold/mdpf_revamp/{firm}/aggregate_aua_timeseries.json` -> the served portal path
   (CTO-gated apply; publisher opal-assets-mdpf-portal-publisher, 22a-fenced writes portal/* only).
2. Verify published == staged byte-identical (ETag match).
3. A4 non_model_assets published alongside (ties by construction).
4. DT re-parity the PUBLISHED (portal/) vs served post-publish (should equal the staged-parity result).

## Residual / not in this package
- TO-2 (aum-timeseries/aum-metrics revamp) -- later wave, replaces the legacy FE reads (item 1's fix).
- TO-5 (source_vintage_last from the registry) -- non-blocking (DT exempts meta/source_vintage_last);
  DESIGN FORK pending CTO (mirror the legacy opal-assets-daily-aua registry feeders, OR reflect the
  revamp's OWN consumed silver-source vintages -- the revamp reads different silver than the legacy
  feeders, so the two produce different provenance; plus a feeder-name mapping question).
