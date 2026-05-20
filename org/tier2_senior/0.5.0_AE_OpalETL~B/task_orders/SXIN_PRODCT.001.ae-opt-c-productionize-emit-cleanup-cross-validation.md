<task_order>
  <metadata>
    <id>SXIN_PRODCT.001</id>
    <slug>ae-opt-c-productionize-emit-cleanup-cross-validation</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL~B</issued_to>
    <date>2026-05-19 (authored ~16:09Z; SCOPE-REDUCED ~17:1XZ per CTO re-disposition -- 2nd-producer cross-validation gate moved to MDPF_ASSETS.019 DS-lane; this TO now ships 2 items not 3; DEMOTED from FIRST to SECOND in AE 0.7 post-v1.0.1 queue behind MDPF_ASSETS.018 chain integration)</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <completion_note>COMPLETE 2026-05-20 (0.5.0_AE_OpalETL~B). Phase-2-only per the 2026-05-20 Option-A amendment (Phase 1 split to SXIN_PRODCT.002). Shipped smartx-pipeline-v1.0.2 -- dead append_non_model_today Lambda step + file + 2 dead IAM statements retired; commit ccf3a79c2; terraform 0-diff verified. Session log: org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-05-20/sxin_prodct_001_phase2_smartx_dead_lambda_cleanup.md. RAVC-ACCEPTED by 2.0.0_SA_COO~B 2026-05-20 (validated off git ground truth + this completion_note; formal RAVC2 MCP was not sent -- COO~B closed directly, no rework). TO CLOSED.</completion_note>
    <scope_reduction_note>SCOPE-REDUCED 2026-05-19 ~17:1XZ (2.0.0_SA_COO per 1.0.0_SA_CTO re-disposition on the 5/19 Cohort 0 incident follow-up). The 2nd-producer cross-validation gate (originally Phase 3 + AC3 in this TO) MOVES TO MDPF_ASSETS.019 (DS Base lane) per CTO architectural placement reasoning: "cross-validation lives where reconcile lives (WS-A side, DS lane), adjacent to the partners-present sentinel that .019 also adds". This TO now ships 2 items not 3: (1) productionize DS emit as scheduled + (2) dead-Lambda cleanup. AC structure reduced accordingly. Queue position: DEMOTED from FIRST to SECOND in AE 0.7 post-v1.0.1 queue per CTO empirical-driven re-sequencing -- MDPF_ASSETS.018 (chain integration, prevent-class for the 5/19 partner-absence defect) preempts because "scheduled emit value depends on platinum being correct; fix the source-of-truth first; then schedule the refresh". No wasted work -- this TO not yet started by AE 0.7. SLA + deadline unchanged.</scope_reduction_note>
    <project_code>SXIN_PRODCT</project_code>
    <priority>P1 -- ACTIVE-STALENESS WINDOW. Under v1.0.1 Opt A Lambda neutralization + manual-only DS emit, the legacy non_model_assets.json file goes stale daily without an interim daily-fire mechanism. CTO disposition 2026-05-19: compound (a) DS Base interim manual daily-fire bridges the 1-2d gap + (b) THIS TO closes the gap permanently within ~0.5d wall post-v1.0.1. Re-sequenced FIRST in AE 0.7 post-v1.0.1 queue (ahead of ADHC_DSFLOW.007 + ADVI_INFALM.001) per CTO's "active-staleness beats preventive-defense" reasoning. ADHC_DSFLOW.007 + ADVI_INFALM.001 push by ~0.5d, no broken dependencies (both independent infrastructure on different pipelines).</priority>
    <sla>~0.5d wall per CTO sizing. Bundles 3 items: scheduled-emit infrastructure + dead-Lambda cleanup + 2nd-producer cross-validation gate. Single tag bump smartx-pipeline-v1.0.2 (or v1.1.0 per AE convention).</sla>
    <deadline>2026-05-22 -- 2-day window post-v1.0.1 (tomorrow 2026-05-20 14:00 UTC) to close the daily-fire gap. DS Base interim daily-fire bridges the gap; this TO ends the bridge dependency.</deadline>
  </metadata>

  <amendment id="2026-05-20-sxin-option-a-split">
    AMENDMENT 2026-05-20 (COO~B, from CTO~B's SXIN architecture ruling -- Option A). This TO's PHASE 1 (productionize / schedule the legacy non_model_assets.json emit) is SPLIT OUT to a new TO -- SXIN_PRODCT.002 (issued_to 0.7.0_AE_CloudOps~B). Reason: CTO~B ruled the emit must be an IN-CHAIN step appended to mdpf-daily-dispatch.sh (NOT a separately-scheduled trigger -- the fixed-offset cadence-race anti-pattern MDPF has paid for repeatedly); that chain script is also edited by MDPF_ASSETS.023, so both edits consolidate on the single agent 0.7.0_AE_CloudOps~B.
    THIS TO (SXIN_PRODCT.001) is now SCOPED TO PHASE 2 ONLY: the dead-Lambda cleanup -- remove lambda_function.py STEP 6 + its import, git rm append_non_model_today.py, drop the 2 dead IAM statements in smartx-pipeline/iam.tf, remove the source-map files[] entry. Phase 2 is off-script, unambiguously the 0.5.0_AE_OpalETL~B lane, and ships independently -> smartx-pipeline-v1.0.2. The Phase-1 scope/ACs in the body below are SUPERSEDED by SXIN_PRODCT.002 -- read this TO as Phase-2-only. The earlier 2-module/2-tag question is resolved: this TO = smartx-pipeline-v1.0.2; SXIN_PRODCT.002 is a script edit + S3 upload only (no Terraform, no tag).
  </amendment>

  <references>
    <origin>1.0.0_SA_CTO MCP to 2.0.0_SA_COO 2026-05-19 ~16:0XZ ("Dispositions: Phase 1B = (a) hardening TO; interim daily-fire = (a)+(b) compound; rider-1 = manual-only confirmed"). CTO disposition compound (a)+(b) on the interim-fire fork; this TO is the (b) Opt C v1.0.2 acceleration.</origin>
    <upstream_pivot>AE 0.7 smartx-pipeline-v1.0.1 RAVC1 2026-05-19 ~15:27Z (Opt A NEUTRALIZE the append_non_model_today step under the CEO-direct broader-1b + Cohort-0-IN methodology pivot via DS Base). v1.0.1 makes DS Base's build_legacy_compat_emit.py (225df40bc) sole SoT for non_model_assets.json but leaves dead Lambda code + IAM dangling + producer manual-only.</upstream_pivot>
    <ds_producer>data/mdpf/scripts/backfill/build_legacy_compat_emit.py (DS Base-owned per CEO-direct methodology pivot). MDPF_ASSETS.017 (dispatched 2026-05-19 ~15:58Z, DS Base lane, deadline 2026-06-01) ships the day-1-zero guard INSIDE this script; SXIN_PRODCT.001 wraps the scheduling infrastructure AROUND it. Both TOs touch the same file but in non-overlapping ways.</ds_producer>
    <rider_1_answer>Per CTO disposition relayed: rider-1 schedule answer = MANUAL-ONLY confirmed (DS Base verbatim "currently it's manual-only"). This TO eliminates the manual-only constraint.</rider_1_answer>
    <masking_class_memory>memory/feedback_identity1_masks_absolute_value_class.md -- the 2nd-producer cross-validation gate (item 3 of scope) is the structural defense against the masking class: single-producer's identity_1 PASSES while cohort values are wrong; second-producer cross-check catches the divergence at a different code path. Rider 2 framing.</masking_class_memory>
    <pipeline_rule>Rule 1 (Terraform-only Lambda + EventBridge deploy). Rule 13 (DS owns scripts, AE owns infrastructure -- this TO is pure infrastructure around DS Base's script).</pipeline_rule>
    <related_pushed>This TO's acceleration pushes by ~0.5d: ADHC_DSFLOW.007 (ds-commit-gate MSYS path-mangle fix) + ADVI_INFALM.001 (INF gold-chain CW alarm). No broken dependencies. CTO is relaying the re-sequencing to AE 0.7 separately in this turn.</related_pushed>
  </references>

  <context>
    Post v1.0.1 (CEO-direct methodology pivot tomorrow 2026-05-20 14:00 UTC), the smartx-pipeline architecture transitions from "Lambda computes + writes non_model_assets.json" to "DS Base's build_legacy_compat_emit.py is sole SoT + Lambda is no-op-but-deployed". The transition leaves 3 cleanup gaps: (1) DS emit runs manual-only (legacy file goes stale daily without daily-fire), (2) Lambda code + IAM are dead but still deployed (dangling state), (3) single-producer architecture re-opens masking-class risk (without a 2nd-producer cross-validation gate, the new SoT's identity_1 PASSES on wrong cohort values just like the old Lambda's would). This TO closes all 3 gaps in one bundle, ending the DS Base interim manual daily-fire dependency permanently.
  </context>

  <scope>
    <step>Phase 1 -- SCHEDULED-EMIT INFRASTRUCTURE (item 1 of 3). Productionize DS Base's build_legacy_compat_emit.py as a daily-scheduled mechanism. AE picks architecture per the cleanest fit:
      - (a) Lambda + EventBridge cron (zip the script + dependencies as a Lambda; EventBridge cron rule fires daily; ARN pattern same as the mdpf-daily-runner trigger pattern).
      - (b) SSM RunDocument + EventBridge cron (run the script on the existing mdpf-daily-runner EC2 instance via SSM; EventBridge cron fires the SSM dispatch).
      - (c) Other (AE judgment if a cleaner option exists post-inspection).
      Schedule: ALIGN with the existing mdpf-pipeline-v1.0.0 daily refresh schedule (cron(0 15 * * ? *) per the mdpf-pipeline runner -- AE verifies + matches). Output destination preserved: same s3:// path build_legacy_compat_emit.py currently writes to (DS Base confirms).</step>
    <step>Phase 2 -- DEAD-LAMBDA CLEANUP (item 2 of 3). Remove the now-neutered append_non_model_today step from the Lambda code (or the entire Lambda if the rest is also dead post-v1.0.1; AE judgment). Retire unused IAM permissions (the SmartX cache IAM grant per AE 0.7's prior CC noting "Cache IAM grant becomes dead-but-harmless"). comp-iam gaps verification post-edit. If the Lambda itself is removable, remove via Terraform per Rule 1 (terraform plan -> apply -> 0-diff verified). If only the step is removed (Lambda kept for some other function), the code edit goes through standard Lambda deploy pattern.</step>
    <step>(Phase 3 REMOVED per scope reduction 2026-05-19 ~17:1XZ -- 2nd-producer cross-validation gate moved to MDPF_ASSETS.019.)</step>
    <step>Phase 4 -- Terraform-only deploy per CLAUDE.md Rule 1: commit via .tools/safe-commit.sh --author per ADHC_OWNPTH.007 -> push CLOUD -> build/upload Lambda zip (if Phase 1 is Lambda) or update SSM document (if Phase 1 is SSM) per pipeline pattern -> plan -> apply -> verify 0-diff -> tag smartx-pipeline-v1.0.2 (run `git tag -l "smartx-pipeline-v*" | sort -V | tail -5` first to confirm; v1.0.0 + v1.0.1 already shipped) -> push --follow-tags -> record-terraform-deploy.sh.</step>
    <step>Phase 5 -- empirical verification:
      AC1 (scheduled-emit): trigger the scheduled mechanism manually (cron-fire equivalent) + verify the artifact writes correctly + the timestamp matches the schedule expected; verify the next-cron-window fires automatically (e.g. wait until next cron tick + verify).
      AC2 (cleanup): comp-iam gaps shows no orphan IAM perms post-edit + comp-blast on the removed Lambda step shows no remaining downstream references; if Lambda fully removed, comp-blast on the function name returns empty + Terraform state confirms removal.
      AC3 (cross-validation gate): inject a synthetic divergence (e.g. mock-set the reference scalar 5% off) + verify the gate fires the alert; verify on a real clean date the gate stays quiet.
      Capture transcripts.</step>
    <step>Phase 6 -- RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform (DS Base is the SoT producer owner; must verify the productionization preserves their methodology). Record: the chosen architecture for each of the 3 items (with rationale per AE judgment + post-inspection findings); the deployed commit SHA + tag + apply timestamp; AC1/AC2/AC3 transcripts; the 2nd-producer cross-validation reference path choice (a/b/c) + sensitivity threshold + rationale; DS Base interim daily-fire mechanism can stand down on RAVC2-accept (you confirm in the RAVC2 + DS Base ACKs back).</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Scheduled-emit infrastructure live + verified: scheduled mechanism (Lambda+EventBridge OR SSM-scheduled OR equivalent) fires daily + writes the artifact to the canonical s3:// path; cron schedule matches mdpf-pipeline daily refresh window (cron(0 15 * * ? *) or equivalent per AE verification). Manual trigger + auto-cron-fire both verified post-deploy. Transcript captured.</ac>
    <ac id="AC2">Dead-Lambda cleanup verified: append_non_model_today step (or full Lambda) removed via Terraform; comp-iam gaps shows no orphan IAM perms; comp-blast on removed code shows no remaining downstream refs. Transcript captured.</ac>
    <ac id="AC3">(REMOVED per scope reduction 2026-05-19 ~17:1XZ -- moved to MDPF_ASSETS.019 AC3.)</ac>
    <ac id="AC4">Terraform-only deploy per Rule 1: commit -> plan -> apply -> 0-diff verified -> tagged smartx-pipeline-v1.0.2 -> pushed --follow-tags -> record-terraform-deploy. No console-side shortcuts.</ac>
    <ac id="AC5">No emoji (ASCII only per CLAUDE.md). Pre-commit gate (.tools/ds-commit-gate.sh) exit 0 on any .py touched (or by-hand 3 checks if ADHC_DSFLOW.007 hasn't shipped). Session log with Compiler Tools section.</ac>
    <ac id="AC6">Compiler-tools: comp-iam gaps (orphan IAM check post-cleanup) + comp-blast on removed code (downstream-reference check) + comp-pipescript deployed smartx-pipeline MATCH post-apply + comp-iam service for any new boto3 surface in the scheduled-emit infrastructure.</ac>
    <ac id="AC7">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform with: chosen architecture for each of the 3 items + rationale; deployed commit SHA + tag + apply timestamp; AC1/AC2/AC3 transcripts; 2nd-producer reference path choice + sensitivity threshold; DS Base interim daily-fire stand-down confirmation. On RAVC2-accept: SXIN_PRODCT.json status -> complete; REGISTRY row moves to Completed (3-step atomic).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      comp-iam service opal-smartx-ingestion-pipeline (pre-cleanup IAM baseline for comparison).
      comp-blast append_non_model_today (pre-cleanup downstream-reference baseline).
      Direct file-read of data/mdpf/scripts/backfill/build_legacy_compat_emit.py for productionization context (DS Base-owned; AE inspects the script for scheduled-runtime constraints).
    </before_write>
    <before_commit>
      .tools/ds-commit-gate.sh on any .py edits (Rule 14; by-hand 3 checks if ADHC_DSFLOW.007 hasn't shipped).
    </before_commit>
    <after_commit>
      comp-iam gaps (orphan IAM check post-cleanup).
      comp-blast on removed code (downstream-reference check; expect empty).
      comp-pipescript deployed smartx-pipeline MATCH post-apply.
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Coordinates with MDPF_ASSETS.017 (DS Base day-1-zero guard inside build_legacy_compat_emit.py; same file, non-overlapping scopes -- .017 is the guard LOGIC, this TO is the scheduling INFRASTRUCTURE AROUND it). Sequencing: .017 GO is independent (DS Base can start anytime; tomorrow morning default per their ACK); this TO gates on AE 0.7's v1.0.1 ship landing. Both can complete in parallel; both touch the same script but at different layers. RAVC2 CC to DS Base on this TO + DS Base owns the methodology-preservation verification.
  </cross_domain_coordination>

  <out_of_scope>
    Phase 1B (WS-A + WS-E canonical alignment to broader-1b methodology) -- per CTO disposition (a), tracked as known-deferred MDPF_ASSETS Phase-2.5 hardening item; COO authors when DS Base bandwidth opens. Not in this TO. Platinum partitions remain Schwab-only-emit until Phase 1B lands; non-load-bearing for partner-facing page (which reads the legacy file this TO productionizes).
  </out_of_scope>

  <deliverables>
    - Scheduled-emit infrastructure for build_legacy_compat_emit.py (Lambda+EventBridge OR SSM-scheduled OR equivalent; AE picks).
    - Dead-Lambda cleanup (append_non_model_today step or full Lambda removed; orphan IAM retired).
    - 2nd-producer cross-validation gate live + tested (reference path AE-chosen + documented).
    - smartx-pipeline-v1.0.2 tag + Terraform 0-diff apply + record-terraform-deploy.
    - Session log under org/tier2_senior/0.7.0_AE_CloudOps/logs/YYYY-MM-DD/ with: 3-item architecture choices + rationale; AC1/AC2/AC3 transcripts; cross-validation reference + sensitivity; DS Base interim daily-fire stand-down confirmation; comp-tools row.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform.
  </deliverables>
</task_order>
