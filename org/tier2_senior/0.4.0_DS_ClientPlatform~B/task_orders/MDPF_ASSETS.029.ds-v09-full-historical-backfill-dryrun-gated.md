<task_order>
  <metadata>
    <id>MDPF_ASSETS.029</id>
    <slug>ds-v09-full-historical-backfill-dryrun-gated</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-20 (authored on .028 RAVC-accept + CTO~B .029-scoping directive)</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>PHASE 0 + PHASE 1 BOTH GO'd. Phase 0 GO'd 2026-05-20 (COO~B) -- dry-run COMPLETE, brief e8d176d8f. PHASE 1 GO'd 2026-05-21 by 2.0.0_SA_COO~B on ANDREW SIGN-OFF ("GO 97 + probe 2024 depth", relayed via CTO~B who reviewed + accepted the Phase-0 brief, no redline). The Phase-1 authoritative scope is in the <phase1_go> block below -- it supersedes the original speculative Phase-1 <scope> step.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF critical path. The .016-equivalent historical backfill, re-scoped to PRD v0.9. Brings the full aggregate_aua_timeseries historical series onto the v0.9 full-Schwab-49F basis. SUPERSEDES the .016 Option-(a) split-basis (which split at 2026-03-11 only because certified_aua's earliest partition was 03-11 -- moot under v0.9, since Schwab + SmartX both have daily data back to 2024 per Andrew 2026-05-20).</priority>
    <sla>Phase 0: ~1h DS wall -- a non-mutating dry-run + a small scratch-location sample validation + the findings brief. [SLA CORRECTED 2026-05-20 by 2.0.0_SA_COO~B, from a wildly over-padded "~3-5h" -- a padded SLA suppresses stall-detection: .029 sat un-picked-up ~2h under cover of the inflated number. Track this TO by its work ARTIFACT (the .029 session log + commits + brief on origin), NOT by an elapsed-SLA clock; if 30-40min pass post-session-engagement with no .029 log appearing, escalate to CTO~B.] Phase 1 (Andrew-gated, NOT on this GO): ~2-3h -- the partition rewrite + verification.</sla>
    <deadline>Phase 0 prompt -- it gates the Andrew go/no-go. Phase 1 has no date; it ships when Andrew signs off.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md PRD v0.9 (8951ce8f0) -- §3.4 + §3.0.1 the formula of record. 49F = full Schwab 49F book; 1b = Schwab_49F_whole - 1a - 1c (SMA-exclusive); aggregator 3-term.</prd>
    <origin>CTO~B .029-scoping directive 2026-05-20, on the .028 RAVC-accept. Andrew 2026-05-20: Schwab + SmartX both have daily data back to 2024 -> the WHOLE historical series can backfill accurately on v0.9, superseding the .016 split-basis. Andrew constraint, verbatim intent: "be ginger / nondestructive until we know for sure how we're gonna do it."</origin>
    <predecessor>.028 (v0.9 49F re-scope, COMPLETE 2026-05-20, commit dd3cd4d22) shipped the v0.9 daily-forward methodology -- WS-E 1b SMA-exclusive residual + aggregator 3-term. .029 applies that same v0.9 methodology to the HISTORICAL series. .016 (the v0.7/v0.8-era backfill) stays closed as historical record; .029 is a fresh TO.</predecessor>
    <hard_constraint>Andrew "be ginger / nondestructive." The historical aggregate_aua_timeseries partitions are NOT to be rewritten until the v0.9 backfill methodology is proven on a dry-run and Andrew has explicitly signed off. Phase 0 is non-mutating by construction; Phase 1 is the gated rewrite.</hard_constraint>
    <pipeline_rule>Rule 13/14/15 apply to any Phase-1 code. Phase 0 is non-mutating (no commit, no deploy, no partition write).</pipeline_rule>
  </references>

  <context>
    .028 put v0.9 live daily-forward. The historical aggregate_aua_timeseries series is still on the older bases (the .016 backfill was v0.7/v0.8-era, with the Option-(a) 2026-03-11 split forced by certified_aua's start date). Under v0.9 the 49F basis is the full Schwab book, and Schwab + SmartX both have daily data to 2024 -- so the whole series CAN be re-materialized on one consistent v0.9 methodology, no split. But rewriting historical partitions is destructive; per Andrew's "be ginger" directive this TO proves the methodology on a non-mutating dry-run FIRST, and the actual rewrite is a separate Andrew-gated step.
  </context>

  <scope>
    <step>PHASE 0 -- DRY-RUN + MECHANISM VALIDATION (this GO; NON-MUTATING). No partition is written, no artifact mutated, no S3 object overwritten. Produce:
      (a) BACKFILL MECHANISM -- how the v0.9 historical series is re-materialized: the per-date inputs (Schwab 49F whole via the crosswalk + SmartX 1a/1c), the date range (target: full series to 2024), the script/path plan.
      (b) PARTITION-WRITE PLAN -- exactly which aggregate_aua_timeseries partitions/objects Phase 1 would rewrite, and how (overwrite-in-place vs versioned vs side-by-side), with the blast radius (downstream consumers of the historical series).
      (c) SAMPLE VALIDATION -- re-materialize a SMALL sample of historical dates v0.9-style IN A SCRATCH LOCATION (not the live series), and validate them: at least one sample date cross-checked against the live .028 v0.9 daily-forward run for an overlapping date (must reconcile), plus plausibility on older dates (no $0 1a, day-over-day within market bounds).
      (d) RISK / blast radius -- what breaks if the rewrite is wrong; the rollback story.</step>
    <step>PHASE 0 deliverable -- a dry-run findings brief at docs/briefs/, routed to 1.0.0_SA_CTO~B (CC 2.0.0_SA_COO~B). HARD STOP here. Do NOT proceed to Phase 1. CTO~B reviews the brief + carries a go/no-go-to-rewrite recommendation to Andrew.</step>
    <step>PHASE 1 -- HISTORICAL PARTITION REWRITE. DISPATCH-HELD / EXPLICITLY ANDREW-GATED. Does NOT execute on this TO's initial GO. Only after Andrew signs off the rewrite (via CTO~B) does COO~B flip the Phase-1 gate. Phase 1 then: re-materialize the historical aggregate_aua_timeseries on the v0.9 methodology per the approved plan; per-date methodology_version=v0_9; preserve a rollback path; Rule 13 commit + deploy; verify the rewritten series reconciles + the daily-forward/.028 boundary is clean.</step>
    <step>PHASE 1 deliverable (post-Andrew-gate) -- RAVC2 to COO~B CC CTO~B: the rewrite transcript, the full-series reconciliation, the boundary check, deployed commit + S3 MATCH.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC0">PHASE 0 is fully non-mutating -- no partition write, no artifact mutation, no S3 overwrite, no commit. [If any mutation is needed to validate, it goes to a scratch location, never the live series.]</ac>
    <ac id="AC1">Phase-0 brief delivers (a) mechanism, (b) partition-write plan + blast radius, (c) a sample-date validation incl. at least one overlapping-date cross-check vs the .028 v0.9 daily-forward run, (d) risk/rollback. Routed to CTO~B CC COO~B.</ac>
    <ac id="AC2">HARD STOP after Phase 0 -- Phase 1 does NOT execute on this GO. The TO records that the rewrite is gated on an explicit Andrew sign-off relayed via CTO~B.</ac>
    <ac id="AC3">[Phase 1, post-Andrew-gate only] Historical aggregate_aua_timeseries re-materialized on v0.9; per-date methodology_version=v0_9; the daily-forward boundary with .028 reconciles; rollback path preserved; Rule 13 deploy; RAVC2.</ac>
  </acceptance_criteria>

  <out_of_scope>
    The legacy-emit re-scope (build_legacy_compat_emit.py -> v0.9) -- separate TO MDPF_ASSETS.030, gates on this TO. Re-opening .016 (closed, historical record). The daily-forward v0.9 methodology (.028, already live). Any partition rewrite WITHOUT the explicit Andrew sign-off -- structurally forbidden by AC2.
  </out_of_scope>

  <deliverables>
    - Phase 0: a non-mutating dry-run + mechanism-validation brief (docs/briefs/), routed to CTO~B CC COO~B. HARD STOP. -- DONE 2026-05-20, brief e8d176d8f.
    - Phase 1 (post-Andrew-gate): the v0.9 historical re-materialization + RAVC2. -- GO'd 2026-05-21, scope below.
  </deliverables>

  <phase1_go date="2026-05-21" by="2.0.0_SA_COO~B" authority="Andrew sign-off via CTO~B">
    PHASE 1 GATE FLIPPED -- ANDREW SIGNED OFF on the Phase-0 brief: "GO 97 + probe 2024 depth." CTO~B reviewed + accepted the Phase-0 brief (mechanism proven bit-identical, non-destructive plan sound, no redline) and carried the go/no-go to Andrew. This block is the AUTHORITATIVE Phase-1 scope; it supersedes the original speculative Phase-1 <scope> step.

    PHASE 1 SCOPE:
    1. Backfill the 97 existing pre-v0.9 partitions: aggregate_aua/2025-12-23.json ... 2026-05-19.json -> v0.9 (2026-05-20 is already v0.9, no-op). Then rebuild aggregate_aua_timeseries.json from the 98 now-v0.9 partitions.
    2. ADD a 2024-DEPTH PROBE to Phase 1's opening probe step: characterize whether the raw/bronze Schwab + SmartX daily data reaches back to 2024, and at what per-date completeness (the existing partitions floor at 2025-12-23; Andrew wants the series toward 2024). Fold it into the same feeder-coverage probe pass. The 2024-depth finding routes to CTO~B -- CTO~B carries the scoped to-2024 extension decision to Andrew. Phase 1 itself does NOT materialize pre-2025-12-23 dates; that is a separate Andrew decision off the probe.
    3. STAGED EXECUTION (do NOT jump straight to the 97-sweep): (a) opening probe = feeder-output coverage+basis for the 97 dates + the 2024-depth characterization; (b) a 3-date scratch batch validated before the full sweep; (c) the full 97-date sweep; (d) the rollup rebuild.

    HARD GUARDRAILS:
    - NON-DESTRUCTIVE: versioned bucket, overwrite-in-place, a local pre-write backup of all 98 objects before any write. No object deleted.
    - NEVER run mdpf_aggregate_aua.py against stale v0.8 feeder rows -- that silently emits a v0.8 number stamped v0_9 (the brief's High-severity risk). Per date, re-run WS-E v0.9 (1b = Schwab_49F_whole - 1a - 1c, the .028 crosswalk source) + WS-B FIRST, THEN the aggregator.
    - .029 and .030's historical phases must NOT interleave: complete all 97 writes + the rollup rebuild + verification, THEN .030's historical phase.

    DELIVERABLE: Phase-1 RAVC2 to 2.0.0_SA_COO~B CC 1.0.0_SA_CTO~B -- the 97-partition rewrite transcript, full-series reconciliation, the v0.8/v0.9 boundary check (the -$100.8M cliff should be GONE post-backfill), the 2024-depth probe finding, deployed verification.
  </phase1_go>

  <phase1_checkpoint1 date="2026-05-21" note="MECHANISM CORRECTION -- supersedes the phase1_go guardrail">
    Checkpoint 1 (opening probe) COMPLETE -- brief 07b7f7687. ANDREW CORRECTED THE MECHANISM mid-probe: the phase1_go guardrail's literal "re-run WS-E v0.9 + WS-B per date FIRST" is NOT EXECUTABLE for the historical series -- WS-B's SmartX call is current-state-only, and silver/allocations floors at 2026-01-16. CORRECTED MECHANISM (Andrew-direct, authoritative; detail in brief 07b7f7687): re-materialize each date's v0.9 49F from THREE EXISTING daily artifacts -- 1a from aum-timeseries.json (the portal Daily AUA panel series), Schwab-whole from schwab/silver/rps, 1c from the SmartX SMA daily mechanism. The non-destructive + no-interleave guardrails STAND; only the per-date feeder-recompute mechanism is replaced. 2024-depth: the series can reach 2024-11-01 -- routed to CTO~B for the to-Andrew extension decision (Phase 1 still does only the 97 dates 2025-12-23..2026-05-19 on this GO). ~$56M RPS-vs-crosswalk basis-seam -- RULED 2026-05-21 by CTO~B: HYBRID Schwab-whole source. Crosswalk NATIVE for 2026-01-16..2026-05-19 (~73 dates -- crosswalk is computable wherever BD silver/allocations reaches, which floors at 2026-01-16; this is also .028 daily-forward's source, so NO seam at the 2026-05-20 boundary). RPS CALIBRATED-onto-crosswalk-basis for 2025-12-23..2026-01-15 (~24 dates -- the deep tail the crosswalk cannot reach; RPS confined to the depth it alone provides). Checkpoint 2 (3-date scratch batch) ALSO measures the RPS-vs-crosswalk delta across the full 2026-01-16..2026-05-19 overlap to characterize the calibration ($ vs % vs drift); HARD STOP after Checkpoint 2 -> the offset characterization routes to CTO~B -> CTO~B ratifies the calibration form -> THEN the 97-sweep (Checkpoint 3).
  </phase1_checkpoint1>

  <phase1_checkpoint2 date="2026-05-21">
    Checkpoint 2 (3-date scratch batch) COMPLETE -- brief 3d1d14fd8. The corrected mechanism is VALIDATED: 3 historical dates re-materialized v0.9-style, identity 49F = 1a+1c+1b = Schwab_whole(RPS) holds, aum-timeseries 1a matches the v0.8 partitions' model_aua to the cent, v0.9 1b lands $204M-$251M historically (plausible track to .028's $280M). The staged-execution gate worked -- the scratch batch caught a real data-quality issue before it could touch 97 live partitions. CTO~B ruled the 2 hard-stop items 2026-05-21:
    (1) 1a-SERIES ANOMALY -- aum-timeseries.json carries a ~$80-100M spike across 2026-05-15..05-19 (a 4-day round-trip to trend = data artifact, correlated to the known 05-15 silver/transactions event). RULED: linear-interpolate (smooth) 05-15..05-19 + carry-forward the 12-25 holiday; 01-14 / 04-02 kept as real only on a cheap corroboration check; ALL smoothed points carry an explicit marker field (estimation must be VISIBLE, never silent).
    (2) RPS-vs-crosswalk seam -- the hybrid ruling (phase1_checkpoint1) STANDS; checkpoint 2's measurement used the wrong comparator (the v0.8 full-BD-book total), so there is no new finding -- the hybrid source dissolves it.
    CHECKPOINT 3 STAGED 3a/3b: 3a = crosswalk-native sweep of 2026-01-16..2026-05-19 (73 dates) -- DS~B starts NOW, no ruling needed; it produces those partitions AND measures the RPS-vs-crosswalk overlap delta as a byproduct. HARD STOP -> DS~B routes the delta characterization to CTO~B -> CTO~B ratifies the calibration form -> 3b = RPS-calibrated sweep of the 24-date deep tail (2025-12-23..2026-01-15) -> rollup rebuild (Checkpoint 4). Non-destructive throughout; nothing written to live S3 pre-sweep.
  </phase1_checkpoint2>

  <phase1_seam_resolved date="2026-05-21" authority="Andrew ruling via CTO~B">
    SUPERSEDES the phase1_checkpoint1 hybrid ruling AND the phase1_checkpoint2 "3a/3b crosswalk-native" staging -- both WITHDRAWN. Sequence of record:
    - DS~B's checkpoint-2 calibration brief (325aaeb81) measured the RPS-vs-crosswalk delta as a ~linear DRIFT ($16.6M/1.18% Jan -> $56.2M/3.41% May), not a stable offset -- AND flagged that the HYBRID's crosswalk-native stage reintroduces silver/allocations for ~73 of 97 CEO-facing partitions, contradicting Andrew's emphatic verbatim 2026-05-20 directive against silver/allocations ("we're using rps").
    - CTO~B agreed the flag was correct, WITHDREW the HYBRID ruling, and took the seam decision to Andrew (the directive vs the validated $1,748M headline vs a continuous series could not all three hold = a genuine Andrew call).
    - ANDREW RULED OPTION B: RPS stays the sole historical data source; the RPS history gets a calibration lift onto the crosswalk basis -- NO new crosswalk run, ZERO silver/allocations operations. Preserves the validated $1,748M headline + a continuous series + honors the no-silver/allocations directive.
    - CALIBRATION FORM RATIFIED (CTO~B 2026-05-21, refined from DS~B's checkpoint-2 drift measurement 325aaeb81): the RPS-vs-crosswalk gap DRIFTS ~linearly (~1.2% Dec/Jan -> ~3.4% May) -- a flat multiplicative K is wrong. RATIFIED form = a LINEAR-IN-TIME delta-$ FIT (intercept $14.8M @ 2026-01-16, slope +$343k/day, R2=0.854), applied as a 2-PARAMETER MODEL to RPS for all 97 dates. The backfill runs purely on RPS + those 2 fit parameters -- NO per-date crosswalk values baked in (that would be the hybrid). Fit parameters recorded in partition metadata. CTO~B sent Andrew a transparency note (the form is a linear fit, not the flat ~3.4% the Option-B framing implied).
    REVISED CHECKPOINT-3 SEQUENCE (no crosswalk-native stage, no separate calibration hard-stop -- the calibration is ratified): RULING #1 1a-series smoothing + the K-calibration -> calibrated 3-date validation (+ the residual-seam measurement) -> the 97-date sweep -> rollup rebuild (Checkpoint 4) -> Checkpoint-3 RAVC2 to COO~B CC CTO~B. OPEN VERIFY DS~B will surface: RPS floors at 2026-05-15 but the range runs to 05-19 -- a 4-date coverage gap, DS~B flags it with a proposed handling if real. All within .029 Phase 1 scope -- no TO re-author.
  </phase1_seam_resolved>
</task_order>
