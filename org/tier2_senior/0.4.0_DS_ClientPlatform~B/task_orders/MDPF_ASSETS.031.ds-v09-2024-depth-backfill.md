<task_order>
  <metadata>
    <id>MDPF_ASSETS.031</id>
    <slug>ds-v09-2024-depth-backfill</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-21 (authored on Andrew 2024-depth = YES ruling, relayed by CTO~B)</date>
    <status>active</status>
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

  <coo_close date="2026-05-21" by="2.0.0_SA_COO~B">
    MDPF_ASSETS.031 RAVC2 ACCEPTED -- CLOSED. DS~B RAVC2 commit b2b496934; brief docs/briefs/mdpf-assets-031-ravc2-2024depth-backfill-complete-20260521.md. CTO~B output-validation: CONFIRM PASS.

    COO~B INDEPENDENT VALIDATION (S3 artifact read, not the self-report): pulled s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/ -- counted 297 partitions in 2024-11-01..2025-12-22 (+ 98 in the .029 range, 395 total). Pulled aggregate_aua_timeseries.json: n_dates=395, span 2024-11-01..2026-05-20, all 395 methodology_version=v0_9, 0 headline nulls, headline $776,166,109.83 (2024-11-01) -> $1,748,030,393.45 (2026-05-20). Sampled partitions 2024-11-15 / 2025-06-16 / 2025-12-22: by_model=5 models each, per-model sum == aggregate model_aua (exact / float-epsilon); per-partition meta carries estimate_tier="2024_depth_extension" + calibration block (clamped_linear_delta_dollars; lift=0 deep tail) + c1_treatment. Seam 2025-12-22->23: headline +0.649%, no artifact step (clamped fit eliminated the ~$6.56M seam).

    ACs: AC1 (HARD daily-per-model 1a granularity -- Andrew's non-negotiable, prove-not-assert) MET + PROVEN per-partition 297/297 -- CTO~B output-validation confirmed. AC2-A1/A2/A3 (Option-A clamped fit; deep tail RPS-uncalibrated marked best-estimate; data-layer marking estimate_tier whole range; chart-marker boundary 2025-12-23) MET on the DATA layer -- the chart VISUAL surfacing is carved to a DE follow-on (see below). AC3-A2 (clamped fit, seamless .031/.029 join, no boundary step) MET. AC4 (non-destructive -- 297 new-key writes, rollup overwrite with local backup, no deletes) MET. AC5 (sweep -> rollup -> RAVC2; 1c=0 per item-(d)) MET. The calibration is the CTO~B-ratified clamped linear delta-$ fit (A2).

    1c COMPONENT-SEAM OBSERVATION (COO~B sharp-structural-test finding, recorded not blocking): at the .031/.029 seam the 1c component steps $0 -> $19.67M (2025-12-22 .031 has 1c=0 per item-(d); 2025-12-23 .029 carries a 1.85%-of-1a ratio-estimate), masked at the headline by the 1b residual absorbing -$12.88M. CTO~B output-validated .031's 1c=0 as correct ("SMA absent -- correct, not a fabrication"). The .029-side question (whether the closed-.029 1c ratio-estimate is a phantom layer, given item-(d) found SMA absent across a store span that includes the .029 range) is routed to CTO~B as a documented observation -- it does NOT gate .031 or MDPF closure.

    CHART-SURFACING FOLLOW-ON (documented, non-gating): DS~B completed the per-partition DATA-layer marking (estimate_tier). The chart VISUALLY surfacing the estimate-segment marker (the Daily AUA Analysis chart distinguishing the pre-2025-12-23 segment; portal/src/pages/ModelPortfolios.tsx) is a DE/portal-lane FE change -- correctly outside DS scope. Carved out per CTO~B as a tracked DE follow-on: a small DE TO bundling with the dark DE~B lane alongside VALGATE Phase-2 .004-.006 when Andrew spins up the 0.4.0_DE_ClientPlatform~B session. NOT a .031-closure gate.

    OUTCOME: MDPF_ASSETS.031 is the FINAL MDPF TO. With .028 + .029 + .030 + .031 all RAVC-accepted, the MDPF v0.9 line is fully landed -- the Daily AUA Analysis chart is one continuous v0.9 trend back to 2024-11-01. MDPF_ASSETS the project 3-step-CLOSED 2026-05-21 (~B C-suite) -- project JSON status=complete, REGISTRY row, PRD Status line.
  </coo_close>

  <close_retracted date="2026-05-21" by="2.0.0_SA_COO~B" authority="CTO~B HOLD ruling (crossed the CONFIRM-PASS)">
    THE coo_close ABOVE IS RETRACTED. CTO~B's CONFIRM-PASS and a subsequent HOLD ruling crossed in transit; COO~B executed the close (commit dd08ef0bc) on the CONFIRM-PASS before the HOLD arrived. The HOLD supersedes -- .031 + MDPF_ASSETS are RE-OPENED.

    CTO~B HOLD reasoning: the 1c component-seam (COO~B's RAVC finding -- 1c steps $0 -> $19.67M at the .031/.029 seam, masked at the headline by the 1b residual) is NOT a non-blocking observation. .031's 1c=0 and .029's 1c~=$19.67M CONTRADICT -- one is wrong -- and item-(d) may have probed the WRONG SmartX source: it checked the CONSOLIDATED allocations store (opal-data-smartx-v2/consolidated/, 5 models, no SMA) while .028's live 1c=$24.93M is pulled by the WS-B feeder from a DIFFERENT SmartX path (the per-model/SMA roster endpoint). So item-(d)'s "zero SMA" may be an artifact of probing a store that simply does not carry SMA.

    GATING: .031 close + MDPF_ASSETS close are HELD pending MDPF_ASSETS.032 -- a focused 1c-source probe (DS~B). The probe's outcome dictates the .031 1c fix: (a) SMA real across BOTH ranges -> .031 1c=0 is WRONG, re-derive 1c+1b, re-run affected partitions; (b) SMA real only from ~2025-12-23 -> both tiers right, the seam is a genuine launch step, legitimately marked; (c) SMA never real in either range -> .029's 1c is a PHANTOM layer, closed .029 RE-OPENS for a 1c=0 fix. CTO~B rules the methodology fix off the probe finding; .031 then closes with whatever 1c correction the probe dictates, and MDPF closes after. Item-2 (chart-surfacing) is RULED (DE follow-on, MDPF closes on the data deliverable) but moot until Item-1 clears.
  </close_retracted>

  <amendment id="A3" date="2026-05-21" by="2.0.0_SA_COO~B" authority="CTO~B AC2 marker-boundary correction">
    A2's MARKING clause set the chart-surfaced "estimated" marker boundary at the lift=0 cutover (~2025-12-04). CTO~B corrected this: the boundary is the .031/.029 join (2025-12-23) -- the WHOLE .031 range (2024-11-01..2025-12-22) is the marked-estimate segment.

    Reasoning (CTO~B): the entire .031 range is out-of-sample -- there is no in-range crosswalk anchor anywhere (the feasibility probe's defining finding). The ~19-day taper strip (2025-12-04..12-22) is the .029 line extrapolated ~19 days BELOW where .029 itself already extrapolated -- it is NOT "reconciled," it is a better-informed estimate, estimate-tier the same as the deep tail. Andrew's informed-YES approved "the 2024-depth extension" -- the entire .031 range -- as a marked best-estimate. A clean honest boundary ("everything before the .029 floor is the estimated extension") beats a hair-split at ~2025-12-04 that corresponds to no real quality cliff.

    AC2 marker boundary -- CORRECTED: the chart-surfaced marked-estimate boundary = 2025-12-23 (the .029/.031 join). The whole .031 range is flagged on the chart as the estimated 2024-depth extension. The 19-day strip's small .029-line lift is PROVENANCE METADATA (recorded per-partition: 19-day strip = the .029-line lift value; deep tail = lift=0) -- it is NOT a reader-facing quality-tier line. Everything else in A2 stands; A3 changes only the chart-marker boundary.
  </amendment>

  <amendment id="A4" date="2026-05-21" by="2.0.0_SA_COO~B" authority="CTO~B 1c-method ruling (141723Z) off the MDPF_ASSETS.032 probe finding">
    THE 1c TERM IS WRONG and is re-derived. A2 carried 1c=$0 across the whole .031 range (per the item-(d) probe). The MDPF_ASSETS.032 1c-source probe (DS~B, brief 3308f0d34) resolved OUTCOME (a): SMA is REAL across both the .031 and .029 ranges -- the SMA program launched 2021-09-02 (positive MIN-openedDate pin across all allocations on the authoritative source, the SmartX enterprises/allocations endpoint -- the WS-B feeder's actual path), 3+ years before the .031 range; 82 SMA accounts open entering the range, 94 now / ~$24.77M. item-(d)'s "1c=0" was a WRONG-SOURCE artifact -- it probed the consolidated allocations store, which does not track the SMA models. So A2's 1c=$0 (the c1_treatment basis "SMA program absent...") is FALSE for the .031 range.

    CTO~B 1c-METHOD RULING (141723Z): re-derive .031's 1c on the SMA program's OWN trajectory -- NOT the 1a-ratio. The 1a-ratio (1c = 1.85% x 1a, .029's method) is REJECTED for .031: a ratio is defensible only if 1c and 1a move together; they do not -- SMA is a small mature program (stable ~82->94 accounts) while 1a grew ~3.8x ($354M->$1.35B) on flow across the range, so 1c-as-%-of-1a declined ~3.8x; a fixed 1.85% is right only at the May-2026 calibration point and under-states ~$15M at 2024-11 (~$6.5M ratio vs a real SMA ~$20M+). The 1a-ratio extrapolating backward is the ROOT ERROR.
    THE RULED 1c METHOD: estimate .031's 1c on SMA's own trajectory -- anchored to the real SMA source (~$24.77M current, 94 accounts) and to .029's 1c at the 2025-12-22/23 boundary (~$19.67M) for LEVEL-continuity across the seam; roughly flat / gently-tapered on SMA's own modest growth, NOT 1a-coupled. The full method detail is in CTO~B's 141723Z message to DS~B.

    THE RE-DERIVE + RE-RUN: with the corrected non-zero 1c, 1b re-derives = calibrated_Schwab - 1a - 1c. DS~B re-runs the 297 .031 partitions -- BOUNDED: only the 1c -> 1b term changes; the clamped-fit calibration (A2), the 1a daily-per-model series (AC1), the marking (A3), the gap handling -- all UNCHANGED. The $0 -> $19.67M 1c component-seam at the .031/.029 boundary CLOSES -- 1c is now level-continuous at the boundary (the method differs across the seam -- SMA-trajectory vs .029's ratio -- but the LEVEL is anchored-continuous, and that boundary is already the reconciled/estimate tier line, so a method difference there is expected, not a defect).
    PLUS -- the .029 quick-check: DS~B confirms .029's ratio-1c is within ~$2-3M tolerance of the SMA-trajectory value over the .029 range -> evidence-based "leave .029" (.029's ratio-1c stands, no .029 re-open). If it is OUT of tolerance -> route CTO~B before proceeding.

    SUPERSEDES: A2's "1c=$0 every .031 date" and the c1_treatment "SMA absent" basis -- VOID; replaced by the SMA-trajectory 1c above. The per-date formula becomes: 1a daily-per-model from aum-timeseries.json; calibrated_Schwab = RPS + clamped-lift; 1c = SMA-trajectory estimate; 1b = calibrated_Schwab - 1a - 1c. AC1 (daily-per-model granularity) + the clamped-fit calibration + the A3 marking -- ALL UNCHANGED.

    NET: the .031 re-run is the live ~B critical path. DS~B re-derives 1c + 1b, re-runs the 297 partitions, RAVC2 to COO~B CC CTO~B. CTO~B output-validates; COO~B independent S3 re-validation (1c now non-zero per-partition + the seam now level-continuous + AC1 still proven). On accept, .031 re-closes and MDPF_ASSETS 3-step-closes. RE-RUN GO'd 2026-05-21 by COO~B on this ruling.
  </amendment>
</task_order>
