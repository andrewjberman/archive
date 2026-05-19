<task_order>
  <metadata>
    <id>MDPF_ASSETS.019</id>
    <slug>dsbase-cohort0-sentinels-and-2nd-producer-cross-validation</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- DETECT-CLASS DEFENSE LAYER. Sister to MDPF_ASSETS.018 (AE 0.7 chain integration, prevent-class). §7 identity_1 PASSED on the 5/19 missing-partner partition that emitted Cohort 0 understated by $17.80M (19% of value, page-visible) -- exact same masking class as anchors 1-5 in `feedback_identity1_masks_absolute_value_class.md`, now 6th anchor today. Two reconcile-block sentinels (DoD plausibility + partners-present-vs-expected) catch the partner-absence class even if .018 chain integration regresses or a new partner-emission failure mode surfaces. Plus 2nd-producer cross-validation gate (moved here from SXIN_PRODCT.001 per CTO architectural placement -- cross-validation lives where reconcile lives) catches cohort-level methodology divergence between independent code paths.</priority>
    <sla>~2-3h wall per CTO sizing. Three additions to WS-A reconcile block in gold/mdpf_aggregate_aua.py: sentinel 1 (DoD), sentinel 2 (partners-present), 2nd-producer cross-validation gate.</sla>
    <deadline>Co-ship with MDPF_ASSETS.018 (this turn dispatch + tomorrow-AM DS Base pickup co-ship with .017). Ideally lands within 24-48h to close the detect-class gap concurrent with .018 closing the prevent-class gap.</deadline>
  </metadata>

  <references>
    <origin>1.0.0_SA_CTO MCP to 2.0.0_SA_COO 2026-05-19 ~17:0XZ (architectural dispositions on the 5/19 Cohort 0 incident follow-up). DS Base brief at `docs/briefs/mdpf-cohort-0-5-19-race-and-structural-followups-20260519.md` (2026-05-19) authored the empirical-grounded 3-TO proposal; CTO ratified .018/.019/.020 sequencing + .019 scope expansion to absorb the 2nd-producer cross-validation gate originally in SXIN_PRODCT.001.</origin>
    <live_incident>2026-05-19 Cohort 0 5/19 understated $17.80M (19% of value): chain ordering race -- WS-C feeder ran AFTER MDPF chain, platinum 5/19 emitted with 49F-only partners. Re-fire complete this session: Cohort 0 now $91.31M correct. .018 prevents recurrence (chain integration); this TO (.019) detects ANY similar partner-absence or absolute-scale anomaly even if .018 regresses.</live_incident>
    <masking_class_memory>memory/feedback_identity1_masks_absolute_value_class.md -- the 5/19 chain-ordering-race is the 6TH anchor (joining PFOE over-attribution, Spread-2 partner-feeder vintage spread, SmartX day-1-of-period zero emission, INFGRO Finding A/B). Same masking class: §7 identity_1 PASSED on the missing-partner partition. The detect-class series-walk + day-over-day plausibility caught all prior 5 incidents post-hoc; THIS TO bakes the detect-class into the reconcile block STRUCTURALLY so future anchors fire LOUD at emit time, not require human-driven post-hoc audits.</masking_class_memory>
    <reconcile_script>data/mdpf/scripts/gold/mdpf_aggregate_aua.py (DS Base-owned per CEO-direct methodology pivot + per existing MDPF_ASSETS lineage). WS-A reconcile block is the canonical placement for absolute-scale + cross-row sentinels.</reconcile_script>
    <sister_to>MDPF_ASSETS.018 (AE 0.7 chain integration, dispatched parallel this turn; prevent-class). MDPF_ASSETS.017 (DS Base day-1-zero guard at producer step, dispatched 2026-05-19 15:58Z; orthogonal class -- .017 catches day-1-zero at producer, .019 catches partner-absence + DoD + cross-producer at reconcile). DS Base's tomorrow-AM pickup window can co-ship .017 + .019 if both ready (same DS-lane reconcile/script work).</sister_to>
    <ds_proxy_draft_offer>DS Base offered to proxy-draft .019 body in their 2026-05-19 ~17:0XZ brief. CTO disposition expanded .019 scope (added the 2nd-producer cross-validation gate from SXIN_PRODCT.001). COO authored directly here rather than wait for re-draft; DS Base can amend in-line during pickup if the placement choices need refinement.</ds_proxy_draft_offer>
    <sxin_prodct_scope_reduction>The 2nd-producer cross-validation gate was originally in SXIN_PRODCT.001 (Opt C v1.0.2 rider per CTO 2026-05-19 ~16:0XZ disposition). CTO 2026-05-19 ~17:0XZ re-disposition moves it HERE per architectural placement reasoning: "cross-validation lives where reconcile lives (WS-A side, DS lane), adjacent to the partners-present sentinel". SXIN_PRODCT.001 scope-reduced to (a) productionize DS emit as scheduled + (b) dead-Lambda cleanup; this TO absorbs the gate.</sxin_prodct_scope_reduction>
    <pipeline_rule>Rule 13 (DS owns the commit + S3 deploy cycle for data/*/scripts/gold/*.py). Rule 14 (.tools/ds-commit-gate.sh on every .py edit -- run by-hand 3 checks if ADHC_DSFLOW.007 MSYS fix has not shipped yet). Rule 15 (from __future__ import annotations first import statement).</pipeline_rule>
  </references>

  <context>
    The 5/19 Cohort 0 incident exposed two structural gaps in the WS-A reconcile block: (1) day-over-day Cohort 0 swung from ~$91M to ~$74M (-19%) without any reconcile error fired (the partition was internally consistent on the 49F-only partner set -- §7 identity_1 PASSED); (2) the reconcile block doesn't check WHICH partners are present, only whether the partners-it-sees-internally reconcile. Both gaps fit the canonical masking class: identity_1 passes on internally-consistent partial data. This TO adds three structural defense layers at reconcile time: (1) DoD Cohort 0 plausibility (>50% move = ERROR -- catches large jumps either direction); (2) partners-present vs expected (config-driven expected_partners_for_date check; ERROR on missing partner); (3) 2nd-producer cross-validation (independent reference path; fail-LOUD on divergence). Sister to .018 (chain integration prevent-class); together prevent + detect close the class.
  </context>

  <scope>
    <step>Phase 1 -- SENTINEL 1: Day-over-day Cohort 0 plausibility gate. In gold/mdpf_aggregate_aua.py WS-A reconcile block: compare today's Cohort 0 value vs prior-business-day's Cohort 0 value (read prior from the most-recent prior platinum emit). If `abs(today - prior) / prior > 0.50` (50% threshold; DS Base right-sizes per observed market-stress-day distribution), raise reconcile ERROR with the diff + both values + a "Cohort 0 plausibility check failed" message. Failure semantic: ERROR (don't write platinum + DLQ alert + last_emit preserved). Mirrors the day-1-zero guard's drop-rather-than-fabricate philosophy (.017 / fb9a910b8 / e0f22b108).</step>
    <step>Phase 2 -- SENTINEL 2: Partners-present vs expected. In gold/mdpf_aggregate_aua.py WS-A reconcile block: add a config-driven `EXPECTED_PARTNERS_FOR_DATE` map (DS Base picks placement -- inline constant OR external JSON OR YAML; per current MDPF convention). For each date being processed, check that all expected partners are present in the cohort decomposition. If any expected partner is MISSING from the cohort decomposition (e.g. Inflection partition empty as today's 5/19 incident), raise reconcile ERROR with the missing partner + date + a "partner partition missing" message. Failure semantic: ERROR (don't write platinum + DLQ alert + last_emit preserved). Initial config: {expected_partners: ["49financial", "inflection"]} for all dates >= 2026-05-18 (DS Base confirms or refines per Inflection onboarding date).</step>
    <step>Phase 3 -- 2ND-PRODUCER CROSS-VALIDATION GATE. In gold/mdpf_aggregate_aua.py WS-A reconcile block: cross-validate the WS-A aggregator output against an independent reference computation, fail-LOUD on divergence. Reference path DS Base picks per cleanest fit:
      - (a) Cross-validate vs SXIN_PRODCT.001 productionized emit (DS Base build_legacy_compat_emit.py output) -- both compute from same upstream feeds via different code paths; divergence catches methodology bugs or upstream-feed defects. Note: SXIN_PRODCT.001 schedules the emit; this gate cross-checks AGAINST that emit OR vice-versa.
      - (b) Cross-validate vs a fresh independent computation (separate function in mdpf_aggregate_aua.py that computes the same scalar via a non-WS-A code path).
      - (c) Cross-validate vs the prior business day's emit + an expected-DoD-bound (lower defense quality than (a)/(b) but cheapest).
      DS Base picks + documents the choice in RAVC2 with rationale. Sensitivity: tolerance threshold that catches cohort-level error (~1%+ divergence) without alarm-fatigue on minor vintage-window noise. Failure: ERROR + DLQ alert + don't write platinum (or AE-style WARN-not-block if DS Base judges the gate too aggressive -- DS Base call, document in RAVC2).</step>
    <step>Phase 4 -- DS commit + S3 deploy cycle per Rule 13: .tools/ds-commit-gate.sh (or by-hand 3 checks if ADHC_DSFLOW.007 not shipped) -> safe-commit.sh with agent --author -> push CLOUD -> aws s3 cp the updated script to the canonical s3:// path (comp-pipescript MATCH precondition) -> comp-pipescript deployed MATCH verification.</step>
    <step>Phase 5 -- empirical verification:
      AC1 (DoD sentinel): replay the 5/19 missing-partner partition state (Cohort 0 = $74M, partition emits 49F-only) → sentinel 1 fires ERROR (DoD 91→74 = -19% < 50% threshold so this one PASSES sentinel 1 -- DS Base may need a tighter threshold OR sentinel 1 catches a 5/19-class via combined-sentinels-2-required; document the tuning). Cross-validate on a clean date → sentinel 1 stays quiet.
      AC2 (partners-present sentinel): replay the 5/19 missing-partner state → sentinel 2 fires ERROR ("inflection partition missing"). Clean date with both partners → sentinel 2 stays quiet.
      AC3 (2nd-producer gate): inject a synthetic 5% divergence between WS-A aggregator and the chosen reference path → gate fires. Clean clean-date run → gate stays quiet.
      Capture all transcripts.</step>
    <step>Phase 6 -- RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO. Record: chosen DoD threshold + partners-present config + 2nd-producer reference path (a/b/c) + sensitivity threshold; AC1/AC2/AC3 transcripts; the DoD-sentinel-tuning note (if 50% threshold misses 5/19's -19% then explain combined-sentinel coverage OR tighter threshold); commit SHA + S3 destination + MATCH verification. On RAVC2-accept: MDPF_ASSETS.json phase narrative updated with .019 closure entry; this TO status -> complete.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">DoD Cohort 0 plausibility sentinel: synthetic large-move test (>50% threshold OR DS Base's tuned threshold) → reconcile ERROR fires + DLQ alert + last_emit preserved. Clean DoD-move test → sentinel stays quiet. Transcript captured.</ac>
    <ac id="AC2">Partners-present vs expected sentinel: replay 5/19 missing-partner state → reconcile ERROR fires ("inflection partition missing") + DLQ alert + last_emit preserved. Clean date with both expected partners → sentinel stays quiet. Transcript captured.</ac>
    <ac id="AC3">2nd-producer cross-validation gate: synthetic 5% divergence injection → gate fires (ERROR or WARN per DS Base call). Clean date → gate stays quiet. Reference path (a/b/c) documented + sensitivity threshold tested. Transcript captured.</ac>
    <ac id="AC4">DS commit + S3 deploy per Rule 13: safe-commit.sh with agent --author -> push CLOUD -> aws s3 cp to canonical path -> comp-pipescript deployed MATCH. No console-side shortcuts.</ac>
    <ac id="AC5">No emoji (ASCII only per CLAUDE.md). Pre-commit gate (.tools/ds-commit-gate.sh) exit 0 -- by-hand 3 checks if ADHC_DSFLOW.007 not shipped. `from __future__ import annotations` first import statement per Rule 15. Session log under `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/` with Compiler Tools section.</ac>
    <ac id="AC6">Compiler-tools: comp-pipescript io mdpf_aggregate_aua (likely empty per data/mdpf/scripts/ comp-graph gap -- document not blocking) + comp-blast mdpf_aggregate_aua (consumer-side blast for downstream platinum consumers) + direct file-read of mdpf_aggregate_aua.py for placement context.</ac>
    <ac id="AC7">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO with: 3 chosen thresholds/configs + rationale; AC1/AC2/AC3 transcripts; sister coordination note (.018 prevents + this .019 detects partner-absence class). On accept: MDPF_ASSETS.json phase narrative updated with .019 closure entry; project stays active pending .017 + .018 closures + SXIN_PRODCT.001 close.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      comp-pipescript io mdpf_aggregate_aua (expect empty per data/mdpf/scripts/ comp-graph gap; document as separate ADHC follow-up, not blocking).
      comp-blast mdpf_aggregate_aua (consumer-side blast for downstream platinum consumers).
      Direct file-read of `data/mdpf/scripts/gold/mdpf_aggregate_aua.py` for WS-A reconcile block placement context.
    </before_write>
    <before_commit>
      .tools/ds-commit-gate.sh mdpf_aggregate_aua.py exit 0 (Rule 14; by-hand 3 checks if ADHC_DSFLOW.007 not shipped).
    </before_commit>
    <after_commit>
      comp-pipescript deployed MATCH post-aws-s3-cp (verify runtime has the new code).
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Sister to MDPF_ASSETS.018 (AE 0.7 chain integration, dispatched parallel this turn; ships together as prevent + detect pair). Co-ship candidate with MDPF_ASSETS.017 (DS Base day-1-zero guard, also DS-lane reconcile/script work; same tomorrow-AM pickup window per DS Base bandwidth ACK). Coordinates with SXIN_PRODCT.001 scope reduction (the 2nd-producer cross-validation gate moves HERE from SXIN_PRODCT.001; SXIN_PRODCT.001 retains only the productionize + dead-Lambda cleanup scope per CTO 2026-05-19 ~17:0XZ disposition).
  </cross_domain_coordination>

  <out_of_scope>
    MDPF_ASSETS.020 strict Cohort 0 formula (Andrew CEO-directive) -- deferred under existing TO #27 Phase 3 per CTO disposition. Phase 1B WS-A + WS-E canonical alignment to broader-1b methodology -- tracked as Phase-2.5 hardening known-deferred item per CTO disposition (a). Chain integration architecture (.018 scope) -- AE 0.7 lane, prevent-class sister; this TO is detect-class only.
  </out_of_scope>

  <deliverables>
    - 3 reconcile-block additions in `gold/mdpf_aggregate_aua.py`: DoD sentinel + partners-present sentinel + 2nd-producer cross-validation gate.
    - Commit on CLOUD via safe-commit.sh + S3 deploy per Rule 13 + comp-pipescript MATCH verification.
    - Session log under org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/ with: 3 chosen thresholds/configs + rationale; AC1/AC2/AC3 transcripts; comp-tools row.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO. MDPF_ASSETS.json phase narrative updated with .019 closure entry on RAVC2-accept.
  </deliverables>
</task_order>
