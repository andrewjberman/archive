<task_order>
  <metadata>
    <id>MDPF_ASSETS.031</id>
    <slug>ds-v09-2024-depth-backfill</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-21 (authored on Andrew 2024-depth = YES ruling, relayed by CTO~B)</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO'd 2026-05-21 by 2.0.0_SA_COO~B on the CTO~B relay of Andrew's 2024-depth ruling (YES -- extend to 2024-11-01). The .029 v0.9 backfill mechanism is RAVC-accepted + proven; .030 landed the legacy emitter on v0.9. .031 is the final MDPF TO -- on .031 land MDPF_ASSETS 3-step-closes. ONE internal checkpoint: the fresh calibration is derived + sample-validated + CTO~B-ratified BEFORE the ~290-date full sweep (see <calibration_checkpoint>).</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P2 -- the 2024-depth extension. Final MDPF TO; on land MDPF_ASSETS closes.</priority>
    <sla>~4-6h DS wall -- a proven-mechanism backfill (.029 replay) over ~290 partitions + a fresh calibration derivation/validation. No new methodology; no Phase-0 dry-run re-prove.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md PRD v0.9 (8951ce8f0). 49F = full Schwab 49F book; 1b = Schwab_49F_whole - 1a - 1c (SMA-exclusive); aggregator/headline 3-term.</prd>
    <origin>Andrew ruled 2024-depth = YES (extend the v0.9 historical series back to 2024-11-01), relayed by 1.0.0_SA_CTO~B 2026-05-21. The 2024-depth extension was the sole remaining MDPF_ASSETS open item after the .028+.029+.030 v0.9 line landed.</origin>
    <predecessor_029>MDPF_ASSETS.029 -- the v0.9 historical aggregate backfill 2025-12-23 ... 2026-05-19 (97 partitions). RAVC-accepted, proven. .031 REPLAYS .029's exact mechanism over the earlier range; .029's session log + briefs are the reference implementation. The .029 partitions are the structural template -- .031 partitions MUST be byte-structurally identical in shape (see AC1).</predecessor_029>
    <predecessor_030>MDPF_ASSETS.030 -- legacy emitter (build_legacy_compat_emit.py) on v0.9; non_model_assets.json already continuous 2024-11-01 -> 2026-05-20 in the live artifact (the .030 close confirmed the series renders back to 2024-11-01). .031 materializes the v0.9 aggregate_aua/{date}.json partitions that underpin that range so every layer is v0.9-consistent, not just the legacy overlay.</predecessor_030>
    <pipeline_rule>Rule 13 (DS commit + S3 deploy cycle). Rule 14 (ds-commit-gate). Rule 15 (`from __future__ import annotations`). Rule 17 (silver no field-slimming -- N/A here, gold/platinum work). Non-destructive guardrail per AC4.</pipeline_rule>
  </references>

  <context>
    The v0.9 historical series (.029) currently floors at 2025-12-23. Pre-2025-12-23 dates are still pre-v0.9. Andrew ruled YES on extending the v0.9 basis back to 2024-11-01 -- ~14 months / ~290 daily partitions. The mechanism is the .029 mechanism, unchanged: RPS Schwab-whole + 1a (model) from aum-timeseries.json + 1c (SMA) ratio-estimate -> 1b residual, with a calibration lift onto the crosswalk basis. The mechanism is PROVEN (.029 RAVC-accepted) -- so there is NO Phase-0 dry-run re-prove. The ONE genuinely new thing .031 introduces is a FRESH calibration: the .029 linear-$ fit does not extrapolate ~14 months back (it goes negative -- structurally impossible, RPS cannot exceed the crosswalk). .031 derives a fresh calibration valid for the 2024-11..2025-12 range, CTO~B-ratified before the full sweep.
  </context>

  <scope>
    <step>Phase 1 -- FRESH CALIBRATION. Derive a calibration valid across 2024-11-01..2025-12-22. The .029 linear-$ fit extrapolates negative over ~14 months -- do NOT reuse it. Pick a calibration form that holds physically across the range (RPS <= crosswalk at every date; no negative 1b). Validate it on a SAMPLE of dates spanning the range (early-2024-11, mid-2025, late-2025-12) before any full sweep. Route the calibration form + the sample-validation evidence to CTO~B for ratification. HARD CHECKPOINT -- see <calibration_checkpoint>.</step>
    <step>Phase 2 -- THE SWEEP (only after CTO~B ratifies the calibration). Replay the .029 mechanism over 2024-11-01..2025-12-22: for each business day, RPS Schwab-whole + daily-per-model 1a from aum-timeseries.json + 1c ratio-estimate -> 1b residual, calibration-lifted. Write each date's v0.9 aggregate_aua/{date}.json partition in the IDENTICAL structure as the .029 partitions (AC1). ~290 partitions; year-end / non-business-day gaps handled exactly as .029 handled them (honest gaps, no synthetic fill).</step>
    <step>Phase 3 -- ROLLUP + VERIFICATION. Rebuild aggregate_aua_timeseries.json to span the extended range; verify the series is continuous across the 2024-11-01 .. 2026-05-20 full span with NO step at the 2025-12-22/23 boundary (the .031/.029 seam) and NO step at the .029/.030-era seams. Per-component series-walk (1a / 1c / 1b / 2a) for day-over-day plausibility -- the identity gate alone is insufficient (a residual 1b absorbs leakage; walk the components, do not trust aggregate==sum). Confirm the 1a layer is daily-per-model at every date (AC1 verification).</step>
    <step>Phase 4 -- RAVC2 to COO~B CC CTO~B: the calibration form + ratification reference, the sweep transcript (partition count, gap list), the rollup verification (continuity + per-component series-walk), the AC1 granularity proof. On accept, MDPF_ASSETS 3-step-closes.</step>
  </scope>

  <calibration_checkpoint date="2026-05-21" by="2.0.0_SA_COO~B" authority="CTO~B relay of Andrew ruling">
    Phase 1 ends at a HARD CHECKPOINT. DS~B derives the fresh calibration + validates it on a sample, then routes the calibration FORM (the functional shape + parameters) + the sample-validation evidence to 1.0.0_SA_CTO~B. CTO~B ratifies the calibration form before the ~290-date full sweep -- the SAME checkpoint discipline as .029's calibration-ratification. Phase 2 does NOT begin until CTO~B's ratification lands. COO~B routes DS~B's calibration to CTO~B and relays the ratification verdict back. If the sample validation surfaces a date where the calibration produces a negative 1b or RPS > crosswalk -> HARD STOP, the calibration form is wrong, re-derive before routing. Rationale: the calibration is the one new thing in .031; the mechanism is proven, the calibration is not -- it is ratified before it touches 290 partitions, not after.
  </calibration_checkpoint>

  <data_reprocess_scope>
    Materializes ~290 NEW v0.9 aggregate_aua/{date}.json partitions for 2024-11-01..2025-12-22 + rebuilds aggregate_aua_timeseries.json to span the extended range. No producer script logic changes beyond the calibration. Non-destructive -- see AC4.
  </data_reprocess_scope>

  <acceptance_criteria>
    <ac id="AC1" priority="HARD -- Andrew explicit, non-negotiable">
      DAILY PER-MODEL 1a GRANULARITY -- preserved across the ENTIRE 2024-11-01..2025-12-22 range. The 1a model series MUST be daily per-model: every business day, every model in the by_model breakdown, as a distinct daily point. aum-timeseries.json carries the daily per-model data back to 2024-11-01 -- read it at FULL GRAIN. The .031 partitions MUST carry the IDENTICAL daily-per-model structure as the .029 partitions.
      FORBIDDEN (any one of these = AC1 FAIL): monthly (or any sub-daily-coarser) downsampling of the 1a series; collapsing / flattening the by_model split into a single aggregate; any aggregate-then-interpolate step that loses the daily OR the per-model resolution. Andrew flagged this directly as a destroy-granularity risk. Phase 3 verification MUST prove, per partition, that 1a is daily-per-model -- not assert it.
    </ac>
    <ac id="AC2">FRESH CALIBRATION -- a calibration valid across the full 2024-11..2025-12 range (NOT the .029 linear-$ fit, which extrapolates negative). Physically sound at every date: RPS <= crosswalk, no negative 1b. CTO~B-ratified per <calibration_checkpoint> before the full sweep; sample-validated on dates spanning the range.</ac>
    <ac id="AC3">THE SWEEP -- ~290 v0.9 aggregate_aua/{date}.json partitions materialized for 2024-11-01..2025-12-22 via the proven .029 mechanism; aggregate_aua_timeseries.json rebuilt to span 2024-11-01 .. present. Series continuous with NO step at the 2025-12-22/23 .031/.029 seam; per-component series-walk (1a/1c/1b/2a) day-over-day plausible. Honest gaps for non-business / year-end dates -- no synthetic fill.</ac>
    <ac id="AC4">NON-DESTRUCTIVE -- versioned bucket, overwrite-in-place / new-key writes only, pre-write backup; no object deleted. Same guardrail class as .029 Phase 1 / .030 Phase 5.</ac>
    <ac id="AC5">Rule 13 deploy cycle (ds-commit-gate -> safe-commit --author -> push CLOUD -> aws s3 cp -> deployed MATCH) for any script change. Rule 14/15. No emoji. Session log with the Compiler Tools section. RAVC2 to COO~B CC CTO~B.</ac>
  </acceptance_criteria>

  <out_of_scope>
    Re-deciding the v0.9 methodology (Andrew-ruled). The .029 range (2025-12-23 forward -- already v0.9). The legacy emitter / non_model_assets.json (.030 -- closed; its series already renders to 2024-11-01). Any new portal/WS-F work. Pre-2024-11-01 depth (Andrew ruled the floor at 2024-11-01).
  </out_of_scope>

  <deliverables>
    - ~290 v0.9 aggregate_aua/{date}.json partitions for 2024-11-01..2025-12-22; aggregate_aua_timeseries.json rebuilt to the extended span.
    - The fresh calibration (form + parameters + sample-validation evidence), CTO~B-ratified.
    - Phase 3 verification: continuity proof + per-component series-walk + the AC1 daily-per-model granularity proof.
    - Session log with the Compiler Tools section. RAVC2 to COO~B CC CTO~B.
  </deliverables>

  <amendment id="A1" date="2026-05-21" by="2.0.0_SA_COO~B" authority="CTO~B method ruling (125643Z) + CTO~B release on Andrew informed-YES">
    METHOD RULED -- OPTION A. The DS~B Phase-0 probe (fb5c4f556) established there is NO calibration anchor anywhere in the .031 range (the crosswalk floors at 2026-01-16; the whole 2024-11-01..2025-12-22 span is out-of-sample). CTO~B ruled: any fitted lift (DS~B's clamped-linear candidate, or a saturating Option B) is FALSE PRECISION -- every parameter is itself unanchored. The honest method is OPTION A: RPS uncalibrated, NO lift, across the ENTIRE .031 range. The understatement is known, bounded (<=~1.13% at the 2026-01-16 edge, shrinking toward 0 going back as the missing-account set scales with book size), and CONSERVATIVE (understates, never overstates).

    ANDREW INFORMED-YES: the best-estimate caveat (deep tail NOT reconciled-to-the-cent, RPS-based, marked-estimate, <=~1.13%-declining conservative understatement) was put to Andrew explicitly. Andrew confirmed -- verbatim "proceed, RPS is acceptable for this purpose." The .031 YES now stands on complete information.

    SUPERSEDES:
    - <calibration_checkpoint> -- VOID. Option A has no calibration to derive and nothing to ratify; the method ruling IS the checkpoint and it is ruled. There is NO calibration-ratification round-trip. DS~B's clamped-linear candidate (from its ACK) is superseded -- use RPS raw, lift=0, whole range.
    - <scope> Phase 1 "FRESH CALIBRATION" -- VOID. There is no calibration phase. The build is: sweep -> rollup -> verification -> RAVC2.
    - AC2 -- REPLACED (see AC2-A1 below).
    - AC3 seam clause -- AMENDED (see AC3-A1 below).
    - <deliverables> "The fresh calibration (form + parameters + sample-validation evidence), CTO~B-ratified" -- VOID; replaced by "the estimated-segment marking (per-partition + chart-surfaced)".

    AC2-A1 (replaces AC2): OPTION A -- the emitter uses RPS uncalibrated, NO lift, for the entire 2024-11-01..2025-12-22 range. 1b = RPS_Schwab_whole - 1a - 1c with calibrated_Schwab == RPS. The deep-tail segment is a BEST-ESTIMATE, not a reconciled-to-the-cent series. It MUST be marked: (i) per-partition -- a field on each .031 aggregate_aua/{date}.json partition flagging it as estimated/RPS-uncalibrated (distinct from the .029 reconciled partitions); (ii) chart-surfaced -- the marking propagates so the Daily AUA chart itself visibly flags the estimated segment; a reader must be able to see where the .029 reconciled series ends and the .031 marked-estimate begins.

    AC3-A1 (amends AC3): under Option A the .031/.029 seam (2025-12-22 -> 2025-12-23) is EXPECTED to show a small step -- .029's 2025-12-23 partition carries the linear lift (~$6.56M, ~0.4% of headline) while .031's 2025-12-22 is uncalibrated (lift=0). That step is the HONEST reconciled/estimated boundary and is exactly what the AC2-A1 markers flag -- it is NOT a defect and NOT a v0.8/v0.9-class cliff. AC3's continuity requirement applies WITHIN the .031 estimated segment (no spurious internal steps; per-component series-walk plausible); the .031/.029 seam is permitted the lift-difference step and MUST be marked, not smoothed away.

    1c (SMA): per DS~B's parallel SMA-start-date probe (TO item d) -- if the SMA program was not live in 2024-11, 1c=0 for those early .031 dates (correct, not a defect); if it was live, ratio-estimate as .029 did (1.85% of 1a). DS~B applies per the probe finding.

    2a (Inflection): MOOT for the whole range -- Inflection data starts ~2026-05-15, so the entire .031 span is 49F-only (1a+1b+1c, no synthesized 2a). Correct, consistent with .029's pre-2026-05-15 handling.

    AC1 -- UNCHANGED. The HARD daily-per-model 1a granularity requirement holds in full. It remains the priority AC; Phase 3 PROVES it per-partition.

    RELEASE: the sweep is GO'd 2026-05-21 (COO~B, on CTO~B's release). DS~B builds sweep -> rollup -> RAVC2 to COO~B CC CTO~B. CTO~B output-validates the RAVC2 -- the AC1 per-partition granularity proof + the estimated-segment marking are the key checks. On .031 RAVC-accept, MDPF_ASSETS 3-step-closes -- the final TO. If at RAVC the marking or the granularity fails, .031 does not close.
  </amendment>

  <amendment id="A2" date="2026-05-21" by="2.0.0_SA_COO~B" authority="CTO~B calibration ratification (130657Z) + CTO~B RESOLVE directive superseding AC3-A1">
    A1's AC3 framing is REVERSED by CTO~B. The reversal rests on a NEW artifact -- DS~B's Phase-1 commit 8a11acbed (the clamped-linear-delta-$ derivation + 3-date sample validation), which was not in hand when A1's Option A was framed off the probe (fb5c4f556). CTO~B reviewed + RATIFIED the clamped fit (130657Z) and issued the RESOLVE directive: the clamped fit governs; A1's "accept the ~$6.56M seam" is the wrong call. COO~B concurs on the merits -- a bare ~$6.56M step at the 2025-12-22/23 boundary is a methodology-APPLICATION artifact (the calibration applied to 12-23 but not 12-22), not an honest economic boundary; "marked-not-smoothed" does not fix an artifactual overnight jump. The clamped fit eliminates it correctly.

    THE RATIFIED CALIBRATION (.031's calibration of record): the clamped linear delta-$ fit --
        lift(d) = max(0, 14,796,793 + 343,246 x days_since(2026-01-16))
        calibrated_Schwab(d) = RPS_whole(d) + lift(d)
    It is the ALREADY-RATIFIED .029 linear delta-$ fit + a physical floor (max with 0). Behavior across the .031 range:
    - 2024-11-01..~2025-12-03 (~265 days, the genuinely-unanchored deep tail): clamps to lift=0 -- RPS uncalibrated. This IS Option A. Marked best-estimate (AC2).
    - ~2025-12-04..2025-12-22 (the ~19-day strip): carries a positive lift that is the .029 ratified line tapering from ~$6.22M (12-22) down to $0 (~12-04). It is a 19-day continuation of an already-ratified fit -- NOT a fabricated/unanchored calibration -- and it makes the .031/.029 join seamless (12-22 lift ~$6.22M joins .029's 12-23 lift ~$6.56M one slope-step apart -- zero boundary step, the same line).

    SUPERSEDES (within A1):
    - <calibration_checkpoint> "VOID" -- REVERSED. The checkpoint produced the clamped fit and CTO~B ratified it (130657Z). The .031 calibration of record = the clamped linear delta-$ fit above.
    - AC2-A1 "RPS uncalibrated, NO lift, entire range" -- CORRECTED to: RPS uncalibrated (lift=0) for the ~265-day deep tail; the .029-line taper for the ~19-day strip. AC2 stays Option-A-in-substance: the genuinely-unanchored deep tail is RPS-uncalibrated, marked best-estimate. Andrew's informed-YES is fully honored -- the deep tail is exactly the RPS-uncalibrated marked-estimate he approved; the 19-day strip uses the .029 calibration he already has, tapering. No Andrew re-surface needed (CTO~B's call).
    - AC3-A1 "the .031/.029 seam carries an expected ~$6.56M step, marked not smoothed" -- DELETED. AC3-A2: the clamped fit produces NO boundary step; the .031/.029 join is seamless by construction (same line). AC3's within-segment continuity + per-component series-walk still hold.
    - DS~B's calibration-derivation STOP (COO~B 130722Z message) -- LIFTED. DS~B's clamped-linear fit (8a11acbed) is correct and IS the calibration used.

    MARKING (AC2 clarification): the per-partition + chart-surfaced "estimated" marker flags the lift=0 deep-tail segment (2024-11-01..~2025-12-03) -- that is the RPS-uncalibrated best-estimate a reader must be able to see. The ~19-day taper strip is .029-line-calibrated, not in the same "unanchored estimate" class. DS~B sets the precise marker boundary at the lift=0 cutover (~2025-12-04) and surfaces it for CTO~B output-validation at RAVC.

    1c (SMA) -- RESOLVED by DS~B's item-(d) probe (commit 265a3f04f, brief docs/briefs/mdpf-assets-031-item-d-1c-sma-and-gaps-20260521.md): 1c = $0 at EVERY .031 date. The 2 SMA-type models (opal_growth_sma, opal_div_sma) are entirely absent from the SmartX consolidated allocations store across the whole .031 span -- the SMA program had no book footprint in 2024-11..2025-12. The .029 ratio-estimate (1c = 1.85% x 1a) MUST NOT be carried into .031 -- it would fabricate a non-existent SMA layer. .031 per-date formula: 1a daily-per-model from aum-timeseries.json at full grain; calibrated_Schwab = RPS + clamped-lift; 1c = 0; 1b = calibrated_Schwab - 1a.

    GAP HANDLING -- per DS~B item-(d): identical to .029 (a partition only for a business day with both RPS + a 1a point; weekends/holidays/year-end get no partition + no synthetic fill; rollup connects across).

    AC1 -- UNCHANGED. The HARD daily-per-model 1a granularity requirement holds in full; Phase 3 PROVES it per-partition.

    NET: the sweep proceeds on the clamped fit + 1c=0. DS~B builds sweep -> rollup -> RAVC2 to COO~B CC CTO~B. The A1 RELEASE clause stands. This A2 is the FINAL calibration ruling.
  </amendment>
</task_order>
