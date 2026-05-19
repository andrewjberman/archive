<task_order>
  <metadata>
    <id>MDPF_ASSETS.018</id>
    <slug>ae-wsc-chain-integration-stage1-parallel</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P0 -- RECURRING DAILY DEFECT. The 5/19 Cohort 0 incident ($17.80M understated, 19% of value, page-visible) is structural: WS-C Inflection feeder runs on a separate ~10am cadence; mdpf-daily-dispatch.sh fires 11:02Z and reads empty Inflection partitions on early-fire days. This recurs daily until fixed -- not a one-off. CTO ratified Option A (chain integration over WS-A reconcile gate) per 2026-05-19 architectural disposition: chain as source-of-truth is the structurally correct path; .019 reconcile sentinels are the parallel defense layer (detect-class), this TO is the prevent-class. Preempts SXIN_PRODCT.001 in AE 0.7 post-v1.0.1 queue per CTO empirical-driven re-sequencing -- platinum must be correct BEFORE Opt C productionizes the refresh, or scheduled emit emits broken platinum daily-productionized.</priority>
    <sla>~1-1.5h wall per CTO sizing. Single chain dispatch script edit + single EventBridge cron time shift + verification.</sla>
    <deadline>Tomorrow's chain fire (next daily mdpf-pipeline cron run; AE picks the cleanest verification window). Ship ASAP post-v1.0.1 lands.</deadline>
  </metadata>

  <references>
    <origin>1.0.0_SA_CTO MCP to 2.0.0_SA_COO 2026-05-19 ~17:0XZ ("5/19 Cohort 0 dispositions: 3 new TOs (.018/.019/.020); AE 0.7 queue re-sequence (.018 now first-after-v1.0.1); SXIN_PRODCT.001 scope reduction"). CTO architectural disposition: Option A (chain integration) over Option B (WS-A reconcile gate). DS Base brief at `docs/briefs/mdpf-cohort-0-5-19-race-and-structural-followups-20260519.md` (2026-05-19) is the empirical anchor.</origin>
    <live_incident>2026-05-19 Cohort 0 5/19 understated $17.80M (19% of value): chain ordering race -- WS-C feeder ran AFTER MDPF chain, platinum 5/19 emitted with 49F-only partners. Re-fire complete this session: Cohort 0 now $91.31M correct. This TO prevents the recurrence; .019 sentinels detect any similar future class.</live_incident>
    <masking_class_memory>memory/feedback_identity1_masks_absolute_value_class.md -- the 5/19 chain-ordering-race is the 6TH anchor (joining the prior 5: PFOE over-attribution, Spread-2 partner-feeder vintage spread, SmartX day-1-of-period zero emission, INFGRO Finding A/B, and now this). Same masking class: §7 identity_1 PASSED on the missing-partner partition.</masking_class_memory>
    <chain_script>data/mdpf/scripts/mdpf-daily-dispatch.sh (AE 0.7-owned per Rule 13 chain dispatch infrastructure). Currently fires 11:02Z UTC via EventBridge cron. WS-C feeder script: `build_mdpf_wsc_inflection_feeder.py` (or equivalent per AE inspection -- DS Base owns the producer + can confirm the canonical path).</chain_script>
    <ws_c_cadence>WS-C Inflection feeder currently runs on a separate ~10am-ish cadence (DS Base confirms; Eclipse-upload-dependent). The 11:02Z mdpf chain fires before WS-C consistently lands on Eclipse-upload-late days, causing the partition-empty read. Mitigation: pull WS-C into chain Stage 1 parallel (so chain owns the dependency + ensures partition presence before WS-A aggregator runs); shift cron 11:02Z → 11:30Z (28-min buffer for Eclipse upload variance).</ws_c_cadence>
    <sister_to>MDPF_ASSETS.019 (DS Base, dispatched parallel this turn -- sentinels + 2nd-producer cross-validation gate; ships together with .018 as prevent + detect pair). Sister to MDPF_ASSETS.017 (DS Base day-1-zero guard at producer step, dispatched 2026-05-19 15:58Z; orthogonal scope -- .017 catches day-1-zero, .019 catches partner-absence, .018 prevents partner-absence).</sister_to>
    <queue_resequence>AE 0.7 post-v1.0.1 queue re-sequenced per CTO empirical-driven 2nd disposition this turn: (1) v1.0.1 OPT A (in flight) -> (2) THIS TO MDPF_ASSETS.018 (first-after-v1.0.1, preempts SXIN_PRODCT.001) -> (3) SXIN_PRODCT.001 (demoted to second; scope REDUCED -- 2nd-producer gate moved to .019) -> (4) ADHC_DSFLOW.007 -> (5) ADVI_INFALM.001. Reasoning: scheduled emit (Opt C) value depends on platinum being correct first; fixing the source-of-truth gates the productionization.</queue_resequence>
    <pipeline_rule>Rule 1 (Terraform-only for any EventBridge cron rule change). Rule 13 (AE owns chain dispatch infrastructure; DS owns the WS-C feeder script -- AE invokes, doesn't author the WS-C script).</pipeline_rule>
  </references>

  <context>
    The 11:02Z mdpf-daily-dispatch.sh fires Stage 1 (feeders) → Stage 2 (aggregator) → Stage 3 (legacy emit). Currently Stage 1 includes the 49F SmartX feeder but NOT the WS-C Inflection feeder (which runs on a separate ~10am cadence dependent on Eclipse upload completion). On days where Eclipse upload arrives close to 11:02Z, WS-C feeder hasn't landed → mdpf chain's Stage 2 aggregator reads an empty Inflection partition → emits 49F-only partner data → page shows $17.80M understated Cohort 0 (today's 5/19 incident). The fix: pull WS-C feeder INTO chain Stage 1 (chain owns the dependency + ensures partition presence) + shift cron 11:02Z → 11:30Z to give Eclipse upload a 28-min buffer. CTO ratified Option A architecturally; this TO implements.
  </context>

  <scope>
    <step>Phase 1 -- inspect data/mdpf/scripts/mdpf-daily-dispatch.sh + identify Stage 1 invocation block. Confirm the canonical WS-C feeder script path (likely `data/mdpf/scripts/feeders/wsc_inflection_eclipse_model_aua.py` or similar -- DS Base owns; AE inspects + verifies the exact path). Add WS-C feeder invocation to Stage 1 in parallel with the existing 49F feeder (background invoke + wait, mirroring the current Stage 1 parallel pattern; AE picks the cleanest bash idiom). On WS-C failure, FAIL CHAIN (chain integrity must hold -- empty Inflection partition is exactly what we're preventing).</step>
    <step>Phase 2 -- shift the EventBridge cron rule that fires mdpf-daily-dispatch.sh from 11:02Z to 11:30Z UTC (28-min buffer for Eclipse upload variance). Terraform-only per Rule 1: locate the cron rule in infra/aws/terraform/mdpf-pipeline/ (or wherever the trigger is defined per AE inspection) + edit the cron expression + plan -> apply -> verify 0-diff -> tag mdpf-pipeline-v{next} (current is mdpf-pipeline-v1.0.0; likely v1.0.1 OR v1.1.0 per AE convention) -> push --follow-tags -> record-terraform-deploy.</step>
    <step>Phase 3 -- empirical verification. Trigger the chain manually post-deploy (via SSM RunDocument equivalent OR the existing manual-trigger path AE uses) + verify WS-C feeder invocation lands in Stage 1 + WS-A aggregator reads populated Inflection partition + platinum emit includes both partners (49F + Inflection). Cross-check Cohort 0 value vs expected (~$91M for clean dates per DS Base's empirical baseline). Capture transcript.</step>
    <step>Phase 4 -- AC verification: AC1 chain integrity (WS-C failure -> chain fails LOUD, no partial emit); AC2 happy-path verification (clean Eclipse-uploaded date -> chain runs end-to-end + platinum has both partners + Cohort 0 ≈ $91M); AC3 cron timing verification (next-day scheduled fire at 11:30Z lands successfully, not 11:02Z). Wait for the next daily scheduled fire OR document AE-side justification for skipping the wait-for-cron AC.</step>
    <step>Phase 5 -- RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform (DS Base owns the producer + must verify the chain integration preserves their methodology). Record: chain script edit diff; cron rule diff; mdpf-pipeline-v{next} tag + commit SHA + apply timestamp; AC1/AC2/AC3 transcripts; the post-shift cron fire transcript (or AE justification if waiting for next-day-cron is unjustified). On RAVC2-accept: MDPF_ASSETS.json phase narrative updated with .018 closure entry; this TO status -> complete.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Chain integrity: WS-C feeder invocation added to Stage 1 in parallel with 49F feeder; WS-C failure (forced via fixture OR mocked) causes chain FAIL LOUD with no partial emit (no Stage 2 aggregator run, no Stage 3 legacy emit). Transcript captured.</ac>
    <ac id="AC2">Happy-path verification: post-deploy manual chain trigger on a clean Eclipse-uploaded date → WS-C feeder lands → WS-A aggregator reads populated Inflection partition → platinum emit includes both 49F + Inflection partners → Cohort 0 value ≈ $91M (per DS Base's empirical baseline; AE confirms exact expected value). Transcript captured.</ac>
    <ac id="AC3">Cron timing verification: EventBridge cron rule shifted from cron(2 11 * * ? *) to cron(30 11 * * ? *); next daily scheduled fire lands at 11:30Z (NOT 11:02Z) successfully. AE waits for the next-day natural cron fire OR documents justification + uses manual trigger as proxy.</ac>
    <ac id="AC4">Terraform-only deploy per Rule 1: commit via safe-commit.sh with agent --author -> push CLOUD -> plan -> apply -> 0-diff verified -> tagged mdpf-pipeline-v{next} (latest-tag-checked) -> pushed --follow-tags -> record-terraform-deploy.</ac>
    <ac id="AC5">No emoji (ASCII only per CLAUDE.md). Pre-commit gate (.tools/ds-commit-gate.sh) exit 0 on any .py touched (likely none -- this is .sh + .tf). Session log with Compiler Tools section.</ac>
    <ac id="AC6">Compiler-tools: comp-pipescript io mdpf-daily-dispatch (or direct file-read if not in graph -- document gap as separate ADHC follow-up; the data/mdpf/scripts/ comp-graph gap is known) + comp-iam service for any IAM changes (likely none -- WS-C feeder invocation reuses existing chain IAM) + comp-blast on mdpf-pipeline trigger (downstream consumer check).</ac>
    <ac id="AC7">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform with: chain script edit diff; cron rule diff + tag; AC1/AC2/AC3 transcripts; sentinels coordination note (sister .019 ships together; both prevent + detect the partner-absence class). On accept: MDPF_ASSETS.json phase narrative updated with .018 closure entry; project stays active pending .019 + .017 closures.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      Direct file-read of `data/mdpf/scripts/mdpf-daily-dispatch.sh` for Stage 1 invocation pattern context.
      Direct file-read of `infra/aws/terraform/mdpf-pipeline/` for the EventBridge cron rule location (likely `eventbridge.tf` or `trigger.tf`).
      DS Base confirmation of the canonical WS-C feeder script path (channel-push or check brief).
    </before_write>
    <before_commit>
      .tools/ds-commit-gate.sh on any .py edits (Rule 14; likely none for this TO).
      comp-iam service on any IAM changes (likely none).
    </before_commit>
    <after_commit>
      comp-pipescript deployed mdpf-pipeline MATCH post-apply (verify the chain runner has the new code).
      Direct verification of the EventBridge cron rule state post-apply.
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Sister to MDPF_ASSETS.019 (DS Base lane, sentinels + 2nd-producer gate; ships together as prevent + detect pair). Coordinates with v1.0.1 ship (this TO gates on v1.0.1 landing tomorrow 14:00 UTC; CEO-direct deadline). Coordinates with SXIN_PRODCT.001 (demoted to second-after-v1.0.1 post this TO -- the productionization of DS emit gates on platinum being correct first per CTO sequencing). DS Base CC on RAVC2 -- they own the WS-C producer + must verify the chain integration preserves methodology.
  </cross_domain_coordination>

  <out_of_scope>
    MDPF_ASSETS.020 strict Cohort 0 formula (Andrew CEO-directive: NAV - Opal ETFs in (1a + 1c + 2a) only) -- deferred under existing TO #27 Phase 3 per CTO disposition. Phase 1B WS-A + WS-E canonical alignment to broader-1b methodology -- tracked as Phase-2.5 hardening known-deferred item per CTO disposition (a). Both surface naturally after this TO + .019 + .017 + SXIN_PRODCT.001 close.
  </out_of_scope>

  <deliverables>
    - Chain script edit: WS-C feeder invocation in Stage 1 parallel.
    - EventBridge cron shift: 11:02Z → 11:30Z (28-min Eclipse buffer).
    - mdpf-pipeline-v{next} tag + Terraform 0-diff apply + record-terraform-deploy.
    - Session log under org/tier2_senior/0.7.0_AE_CloudOps/logs/YYYY-MM-DD/ with: chain script + cron edit diffs; AC1/AC2/AC3 transcripts; comp-tools row.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform.
  </deliverables>
</task_order>
