<task_order>
  <metadata>
    <id>MDPF_ASSETS.022</id>
    <slug>dsbase-phase1b-wsa-wse-canonical-alignment-broader-1b</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-19 (pre-authored under Andrew "drive everything" 17:48Z directive; queued for DS Base bandwidth opening post-.017 + .019 close)</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED for DS Base bandwidth window post MDPF_ASSETS.017 + .019 RAVC2-accept. Pre-authored per CTO PATH (a) disposition 2026-05-19 ("Phase 1B = (a) hardening TO when bandwidth surfaces; concur with COO lean"). Andrew "drive everything" directive 17:48Z covers pre-authoring + queueing; actual dispatch unblock = DS Base channel-push signaling bandwidth available after .017 + .019 ship (likely tomorrow PM or next-day-AM per their /loop cadence). NOT deadline-pressured: known-deferred Phase-2.5 hardening item; SXIN_PRODCT.001 + .018 + .019 + .021 close the partner-facing-page-not-load-bearing path first.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P2 -- KNOWN-DEFERRED PHASE-2.5 HARDENING. Closes the canonical-vs-served SoT divergence that v1.0.1 Opt A neutralization created: under the new architecture, DS Base's build_legacy_compat_emit.py emits the legacy non_model_assets.json file using broader-1b + Cohort-0-IN methodology (CEO-direct pivot), BUT the WS-A canonical aggregator (mdpf_aggregate_aua.py) + WS-E feeder still emit the Schwab-only methodology to platinum partitions. Any future consumer reading PLATINUM (vs LEGACY) gets the wrong methodology -- same masking-class risk in a different shape (SoT divergence between consumed-state and canonical-state; future-trap framing per CTO 2026-05-19 disposition). Non-load-bearing for the partner-facing page (which reads the legacy file), but load-bearing for canonical correctness + any future platinum-consumer use case.</priority>
    <sla>~3-5h DS wall estimate (refines on DS Base inspection): WS-A aggregator update + WS-E feeder methodology shift + reconciliation fixture re-baseline + AC verification on both legacy + platinum paths. Possibly bundled with .017 + .019 if DS Base prefers single-session-across-MDPF + the bandwidth window accommodates ~6-8h total.</sla>
    <deadline>None hard. Known-deferred; surface naturally on DS Base bandwidth opening. Andrew "drive everything" intent doesn't override "known-deferred" framing -- this TO ships when DS Base bandwidth opens, not on a forced timeline.</deadline>
  </metadata>

  <references>
    <origin>1.0.0_SA_CTO disposition 2026-05-19 ~16:0XZ ("Phase 1B = (a) hardening TO when bandwidth surfaces") on the 5/19 Cohort 0 incident follow-up architecture. Phase 1B was identified as a structural follow-on to v1.0.1 Opt A Lambda neutralization but de-prioritized vs the prevent + detect + bridge work (.018 + .019 + .021) per CTO empirical-driven re-sequencing. Pre-authored under Andrew "drive everything" 2026-05-19 ~17:48Z directive.</origin>
    <upstream_pivot>v1.0.1 SHIPPED 17:09Z + CTO RAVC2-accepted (CEO-direct broader-1b + Cohort-0-IN methodology pivot via DS Base; Lambda Opt-A-neutralized; DS Base's build_legacy_compat_emit.py sole SoT for non_model_assets.json LEGACY file). PLATINUM partitions still emit the Schwab-only methodology because the WS-A canonical aggregator + WS-E feeder weren't updated to broader-1b.</upstream_pivot>
    <divergence_class>SoT divergence: LEGACY non_model_assets.json (DS Base emit, broader-1b methodology) vs PLATINUM partitions (WS-A aggregator + WS-E feeder, Schwab-only methodology). Partner-facing page reads LEGACY -- not load-bearing now. ANY future platinum-consumer (refactor, new dashboard, downstream pipeline, audit) reads PLATINUM -- gets the wrong methodology. Future-trap class.</divergence_class>
    <sister_to>MDPF_ASSETS.017 (DS Base day-1-zero guard at producer step). MDPF_ASSETS.019 (DS Base reconcile sentinels + 2nd-producer cross-validation gate). MDPF_ASSETS.018 (AE 0.7 chain integration prevent-class). MDPF_ASSETS.021 (AE 0.7 SSM RunDocument interim bridge). SXIN_PRODCT.001 (AE 0.7 productionize DS emit as scheduled). Together with this Phase 1B, the architectural transition from v1.0.0 Schwab-only Lambda-as-producer to v1.0.1 broader-1b DS-as-producer closes end-to-end across PRODUCER + RECONCILE + CANONICAL + LEGACY paths.</sister_to>
    <future_trap_framing>CTO 2026-05-19 disposition (a) rationale: "(b) folding into Opt C is scope creep (Opt C should stay lean: productionize emit + clean dead Lambda code + cross-validate methodology; adding WS-A/WS-E canonical alignment doubles the scope). (c) defer-indefinitely is unsafe -- the platinum-canonical-vs-legacy-served divergence creates a future-trap: any future platinum consumer (or anyone refactoring to read platinum) gets the wrong methodology. That's the same masking-class risk in a different shape (SoT divergence between consumed-state and canonical-state). (a) tracks the work without forcing it onto a critical path. Track as a known-deferred Phase-2.5 hardening item in MDPF_ASSETS.json; surface for sequencing when DS Base bandwidth opens. You author the TO when ready."</future_trap_framing>
    <pipeline_rule>Rule 13 (DS owns commit + S3 deploy cycle for data/*/scripts/gold/*.py + data/*/scripts/feeders/*.py). Rule 14 (.tools/ds-commit-gate.sh on every .py edit; ADHC_DSFLOW.007 MSYS fix may or may not have shipped by .022 pickup; by-hand 3 checks fallback). Rule 15 (`from __future__ import annotations` first import statement).</pipeline_rule>
  </references>

  <context>
    Under v1.0.1 Opt A Lambda neutralization (CEO-direct methodology pivot via DS Base 2026-05-19), the producer-consumer architecture transitioned from "Lambda computes broader-1b methodology + writes legacy file" to "DS Base's build_legacy_compat_emit.py computes broader-1b methodology + writes legacy file". The PLATINUM artifacts (WS-A aggregator output + WS-E feeder output to opal-data-mdpf) still encode the Schwab-only methodology because the v1.0.1 pivot only updated the LEGACY-file emit path -- not the CANONICAL platinum-emit path. The partner-facing Model Portfolios page reads the LEGACY file, so the page is correct. But any future platinum-consumer (downstream dashboard, audit script, refactored portal page, new pipeline) reads PLATINUM + gets the OLD Schwab-only methodology silently. This TO updates WS-A aggregator + WS-E feeder to align canonical platinum with the new broader-1b methodology, eliminating the SoT divergence + future-trap class.
  </context>

  <scope>
    <step>Phase 1 -- DS Base inspection of WS-A aggregator (`data/mdpf/scripts/gold/mdpf_aggregate_aua.py`) + WS-E feeder (`data/mdpf/scripts/feeders/wse_49f_non_model_residual.py` or canonical name per DS Base inspection) to identify the Schwab-only-vs-broader-1b methodology divergence points. Methodology delta per DS Base's 2026-05-19 CEO-direct pivot:
      - Schwab-only methodology (current platinum): partner_custody_total = Schwab-only book (~$1,655M for 49F); non_model_aua = partner_custody_total - model_aua - sma_aua = strict Schwab subtraction
      - Broader-1b + Cohort-0-IN methodology (current LEGACY via build_legacy_compat_emit.py): broader_custody_total includes non-Schwab custodians + Cohort 0 (Opal-ETF public residual $91.31M); non_model_aua computed against the broader basis
      DS Base picks the cleanest placement (in-line WS-A aggregator function update vs methodology-flag config vs separate broader-1b code path with a config switch).</step>
    <step>Phase 2 -- update WS-A aggregator + WS-E feeder to emit broader-1b + Cohort-0-IN methodology to PLATINUM partitions. Preserve a methodology-version field in the emitted artifact (e.g., `methodology_version: "broader_1b_cohort0_in_v1_0_1"`) so downstream consumers can detect + handle methodology pivots cleanly. Keep the §7 reconcile sentinels (.019's DoD + partners-present + 2nd-producer gate) compatible -- they should fire on broader-1b output the same way they fire on Schwab-only.</step>
    <step>Phase 3 -- reconciliation fixture re-baseline. The 4-5 fixture tests in mdpf_aggregate_aua's reconciliation suite were authored under Schwab-only methodology baselines (per .013 ship history). Update fixture expected values to broader-1b baselines + add a fixture for the new methodology_version field. Cross-validate against DS Base's build_legacy_compat_emit.py outputs for the same date -- platinum + legacy should reconcile to-the-cent under the same methodology now.</step>
    <step>Phase 4 -- empirical verification:
      - AC1 PLATINUM emit cross-validation: WS-A aggregator on a real production date produces platinum artifacts whose totals reconcile to-the-cent against the LEGACY file's totals for the same date (verifies platinum + legacy now agree under broader-1b methodology).
      - AC2 reconciliation fixture pass: all 4-5 fixtures pass under broader-1b baseline.
      - AC3 §7 reconcile sentinels still fire correctly on broader-1b output (DoD + partners-present + 2nd-producer gate from .019 still gate appropriately).
      - AC4 NO regression on the LEGACY emit (DS Base's build_legacy_compat_emit.py output unchanged byte-for-byte; this TO only touches platinum).
      - AC5 methodology_version field present in PLATINUM artifacts; downstream consumers can detect + handle.</step>
    <step>Phase 5 -- DS commit + S3 deploy cycle per Rule 13: .tools/ds-commit-gate.sh (or by-hand 3 checks per ADHC_DSFLOW.007 state) -> safe-commit.sh with agent --author -> push CLOUD -> aws s3 cp the updated scripts to the canonical s3:// paths (mdpf-daily-runner pulls from same prefix; comp-pipescript deployed MATCH verification). Tag if pipeline-naming convention applies (mdpf doesn't currently tag the DS scripts but DS Base picks per convention).</step>
    <step>Phase 6 -- RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.7.0_AE_CloudOps (AE may want to verify SXIN_PRODCT.001's productionization + .021 SSM doc reference the same canonical methodology now, no divergence). Record: chosen placement (in-line vs config-flag vs separate path); methodology delta + fixture re-baseline + methodology_version field naming; AC1/AC2/AC3/AC4/AC5 transcripts; deployed commit SHA + S3 destination + MATCH verification. On RAVC2-accept: MDPF_ASSETS.json phase narrative updated with .022 closure + the Phase 1B architectural transition closure narrative; project moves CLOSER to completion-status (still has .016 Cohort-0 historical backfill pending + maybe other open items).</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">PLATINUM emit cross-validation: WS-A aggregator on a real production date produces platinum totals that reconcile TO-THE-CENT against DS Base's LEGACY file totals for the same date (broader-1b methodology, both paths). Transcript captured.</ac>
    <ac id="AC2">All 4-5 reconciliation fixtures pass under broader-1b baseline (re-baselined from Schwab-only).</ac>
    <ac id="AC3">§7 reconcile sentinels from .019 (DoD + partners-present + 2nd-producer gate) still fire correctly on broader-1b output. No false-positives on clean dates; fire on synthetic injection per the original .019 ACs.</ac>
    <ac id="AC4">NO regression on LEGACY emit: DS Base's build_legacy_compat_emit.py output unchanged byte-for-byte for the same date (this TO only touches platinum-emit path).</ac>
    <ac id="AC5">methodology_version field present in PLATINUM artifacts (e.g., `methodology_version: "broader_1b_cohort0_in_v1_0_1"` or DS Base naming choice). Field documented in the artifact schema.</ac>
    <ac id="AC6">DS commit + S3 deploy per Rule 13: safe-commit.sh with agent --author -> push CLOUD -> aws s3 cp to canonical s3:// paths -> comp-pipescript deployed MATCH. No console-side shortcuts.</ac>
    <ac id="AC7">No emoji (ASCII only per CLAUDE.md). Pre-commit gate per Rule 14. `from __future__ import annotations` per Rule 15. Session log with Compiler Tools section.</ac>
    <ac id="AC8">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.7.0_AE_CloudOps with: placement choice + methodology delta + fixture re-baseline + methodology_version naming + AC1-AC5 transcripts + commit SHA + S3 destination + MATCH verification.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      comp-pipescript io mdpf_aggregate_aua (likely empty per known data/mdpf/ comp-graph gap; document not blocking).
      comp-pipescript io wse_49f_non_model_residual (or canonical WS-E feeder name per DS Base inspection; same comp-graph gap likely).
      comp-blast mdpf_aggregate_aua (downstream platinum-consumer enumeration; check for any current platinum consumers that would see the methodology pivot first).
      Direct file-read of mdpf_aggregate_aua.py + WS-E feeder + build_legacy_compat_emit.py for methodology-delta identification.
    </before_write>
    <before_commit>
      .tools/ds-commit-gate.sh per Rule 14 (by-hand fallback if ADHC_DSFLOW.007 MSYS fix not shipped).
    </before_commit>
    <after_commit>
      comp-pipescript deployed MATCH post-aws-s3-cp (verify runtime has new methodology code).
      comp-blast for any downstream consumers of methodology_version field (forward-looking).
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Coordinates with MDPF_ASSETS.017 + .019 (DS Base lane; same gold/script scope; .022 must NOT regress .017 day-1-zero guard or .019 sentinels). Coordinates with SXIN_PRODCT.001 (AE 0.7; productionized DS emit must reference the same canonical methodology post-.022; CC AE 0.7 on RAVC2). DS Base owns the methodology choice end-to-end -- AE consumers (SXIN_PRODCT.001 productionized cron, .021 SSM doc, .018 chain integration) all read the post-.022 broader-1b methodology canonical artifacts without code change.
  </cross_domain_coordination>

  <out_of_scope>
    MDPF_ASSETS.016 Cohort-0 historical backfill (already in DS Base queue; independent scope -- historical date-range backfill, not methodology-update). MDPF_ASSETS.020 strict Cohort 0 formula (Phase 3, deferred under existing TO #27; methodology-refinement of Cohort 0 calculation, not the platinum-emit alignment). Lambda re-activation under broader-1b (Lambda stays neutralized per v1.0.1; this TO is canonical-side only, not Lambda-side).
  </out_of_scope>

  <deliverables>
    - WS-A aggregator (mdpf_aggregate_aua.py) + WS-E feeder updated to emit broader-1b + Cohort-0-IN methodology to PLATINUM partitions.
    - methodology_version field added to platinum artifact schema.
    - Reconciliation fixtures re-baselined (Schwab-only -> broader-1b).
    - Commit on CLOUD via safe-commit.sh + S3 deploy per Rule 13 + comp-pipescript MATCH.
    - Session log under org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/ with: placement choice + methodology delta + fixture re-baseline + AC1-AC5 transcripts + comp-tools row.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.7.0_AE_CloudOps.
  </deliverables>
</task_order>
