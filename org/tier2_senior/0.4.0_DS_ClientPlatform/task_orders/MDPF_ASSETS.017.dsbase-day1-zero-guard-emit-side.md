<task_order>
  <metadata>
    <id>MDPF_ASSETS.017</id>
    <slug>dsbase-day1-zero-guard-emit-side</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>MDPF_ASSETS</project_code>
    <supersedes>SXIN_DAY1ZG.001 (closed-as-superseded-by-redirect 2026-05-19 per CTO PATH (a) disposition on AE 0.7 smartx-v1.0.1 RAVC1; the in-Lambda placement of the day-1-zero guard inside append_non_model_today.py became scope-orphaned under v1.0.1 Opt A neutralization; guard migrates to DS Base's build_legacy_compat_emit.py producer step where the methodology computation lives)</supersedes>
    <priority>P1 -- TIME-PRESSURED. Closes the SmartX day-1-of-period zero-emission masking class (today's 4-anchor #3, `memory/feedback_identity1_masks_absolute_value_class.md`) at the new SoT producer step BEFORE the next at-risk live run 2026-06-01 (Mon, first first-trading-day-of-month after smartx-pipeline-v1.0.1 ships with the Lambda neutralized). Empirical anchor: DS 0.4 root-caused SmartX upstream emits EndMarketVal = $0.00 across all model CSVs on each reporting-period day-1; under the v1.0.1 producer-consumer split where build_legacy_compat_emit.py is sole SoT for non_model_assets.json, the day-1-zero defense MUST live at THIS producer step or the masking class re-opens.</priority>
    <sla>~0.5d wall -- defensive guard inside build_legacy_compat_emit.py at the broader-1b compute step OR the write step (DS Base picks the structurally cleanest placement; equivalent for the guard purpose). No new infra, no new IAM, no shared-state coordination beyond the existing DS Base lane.</sla>
    <deadline>2026-06-01 14:00 UTC (first at-risk live emit for first trading day of June 2026; assumes smartx-v1.0.1 lands tomorrow 2026-05-20 14:00 UTC + the DS emit schedule is in place by then -- if DS emit is still manual-only via CTO rider-1 schedule answer, the deadline pressure transfers to manual-run discipline). Original SXIN_DAY1ZG.001 deadline preserved verbatim.</deadline>
  </metadata>

  <references>
    <origin>1.0.0_SA_CTO MCP to 2.0.0_SA_COO 2026-05-19 ~15:5XZ ("ACK -- you caught a scope-collision I missed; disposition is (a) STAND-DOWN + migrate guard to DS lane"). CTO PATH (a) disposition on AE 0.7 v1.0.1 RAVC1 (CEO-direct methodology pivot via DS Base; broader-1b + Cohort-0-IN supersedes Schwab-only v1.0.0). Original rider-2 sketch from 1.0.0_SA_CTO 2026-05-19 ~13:23Z (canonical guard recipe).</origin>
    <superseded_to>SXIN_DAY1ZG.001 (originally authored + dispatched to AE 0.7.0 at 15:09Z then stood down at 15:27Z when the in-Lambda placement was scope-orphaned by v1.0.1 Opt A neutralization). Same guard recipe, migrated to the new SoT producer step.</superseded_to>
    <ds_fixes>Two-layer DS 0.4 fix shipped 2026-05-19 on the MDPF aggregate + legacy aum-timeseries paths: fb9a910b8 (drop SmartX zero-emission rows + null 1b on partial-1a coverage) + e0f22b108 (legacy-compat smooth 1/16+1/19 + skip post-cutover SmartX zero-emission dates). This TO extends the same drop-rather-than-fabricate philosophy to the write step in build_legacy_compat_emit.py -- belt-and-suspenders defense layer covering the new producer role.</ds_fixes>
    <new_methodology>CEO-direct methodology pivot via DS Base (broader-1b + Cohort-0-IN) supersedes the Schwab-only v1.0.0 (de03b497a). Under the new methodology, DS Base's build_legacy_compat_emit.py is the sole SoT for non_model_assets.json. AE 0.7 smartx-v1.0.1 RAVC1 to CTO (15:27Z) confirms Opt A NEUTRALIZE the append_non_model_today Lambda step under this architecture; CTO ratified PATH (a) (stand-down + migrate) at ~15:5XZ.</new_methodology>
    <emit_script>data/mdpf/scripts/backfill/build_legacy_compat_emit.py (commit 225df40bc 2026-05-19; the new SoT producer for non_model_assets.json under the broader-1b + Cohort-0-IN methodology).</emit_script>
    <empirical_anchor>memory/feedback_identity1_masks_absolute_value_class.md anchor #3 (SmartX day-1-of-period zero emission). 7 known 2026 zero-dates: 2026-01-02, 2026-01-03, 2026-01-04, 2026-02-02, 2026-03-02, 2026-04-01, 2026-05-01 (next at-risk: 2026-06-01).</empirical_anchor>
    <pipeline_rule>Rule 13 -- DS owns the full commit -> QA-deploy cycle for data/*/scripts/* including aws s3 cp for any S3-side artifact involved. Rule 14 -- .tools/ds-commit-gate.sh on every .py edit (note: gate is currently MSYS-mangled on Windows Git Bash per ADHC_DSFLOW.007 PENDING; run the 3 checks by hand if .007 hasn't shipped before this TO runs). Rule 15 -- `from __future__ import annotations` first import statement.</pipeline_rule>
    <related_open>CTO rider-1 to AE 0.7 (verify build_legacy_compat_emit.py schedule -- is it manual-only or cron-fired?) is MORE critical post-migration; this TO's deadline-pressure depends on knowing when DS emit runs. If still manual-only post v1.0.1, the day-1-zero gate window depends on manual-run cadence (DS Base discipline), not automated cron. CTO Opt C follow-on (productionize emit as scheduled Lambda/SSM) is the long-term cleanup but NOT in this TO's scope.</related_open>
  </references>

  <context>
    Under the smartx-v1.0.1 producer-consumer split (Lambda neutralized + DS Base's build_legacy_compat_emit.py as sole SoT), the day-1-of-period zero-emission masking class re-opens unless defended at the new producer step. The empirical defect class: SmartX upstream emits EndMarketVal = $0.00 across all model CSVs on each reporting-period day-1; without a guard, build_legacy_compat_emit.py computes broader-1b non_model_aum = partner_custody_total - model_aum with model_aum = $0 and writes a structurally wrong emit (non_model materially over-stated). identity_1 STILL PASSES on the wrong emit (the residual absorbs the leak) -- exactly the absolute-value masking class anchor #3 documents. This TO ports the same canonical guard recipe DS 0.4 already shipped on the consumer side (fb9a910b8 + e0f22b108) to the new producer side, completing belt-and-suspenders defense across the methodology.
  </context>

  <scope>
    <step>Phase 1 -- defensive guard inside build_legacy_compat_emit.py at the broader-1b compute step OR the write step (DS Base picks structurally cleanest placement; structurally equivalent for the guard purpose). Per the CTO ratified recipe + DS 0.4 canonical pattern: before computing or writing `non_model_aum`, assert `model_aum > MIN_PLAUSIBLE_THRESHOLD` (~$100M for 49F; DS Base right-sizes per observed model_aum distribution on Schwab-clean dates) AND/OR `model_aum within +/-15% of prior business day`. Failure: raise + do NOT write the new artifact + preserve prior non_model_assets.json emit + log clearly (CloudWatch / runtime log). Same drop-rather-than-fabricate philosophy as fb9a910b8 + e0f22b108. Structure as a small `assert_model_aum_plausible(today, prior)` helper so threshold + tolerance are visible + testable in isolation.</step>
    <step>Phase 2 -- DS commit + QA-deploy cycle per Rule 13: `.tools/ds-commit-gate.sh` on the edit (or run-by-hand 3 checks if ADHC_DSFLOW.007 MSYS fix has not shipped) -> safe-commit.sh with agent --author (ADHC_OWNPTH.007) -> push to CLOUD -> aws s3 cp the updated script to wherever the canonical s3:// path lives (DS Base verifies; if it's a runtime artifact location, source-map check first) -> comp-pipescript deployed MATCH verification.</step>
    <step>Phase 3 -- acceptance verification (run BEFORE RAVC2 close):
      AC1 anchor-reproduction: force-set today's model_aum to $0.00 in a probe input -> guard raises + no write + prior non_model_assets.json preserved.
      AC2 false-positive smoke: run on a real Schwab-clean date (today's emit or any non-day-1 date) -> normal emit + non_model_pct in expected range (10-15% empirical band for 49F under the new broader-1b methodology -- DS Base confirms expected range).
      AC3 cross-empirical 7 fixtures: re-run as fixtures against each 2026 zero-date (2026-01-02, 2026-01-03, 2026-01-04, 2026-02-02, 2026-03-02, 2026-04-01, 2026-05-01) -> guard raises on each.
      Capture all 9 transcripts in the session log.</step>
    <step>Phase 4 -- RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO. Record: chosen MIN_PLAUSIBLE_THRESHOLD + tolerance + DS Base rationale (observed model_aum distribution + min day-to-day swing on real Schwab-clean dates under the new methodology); the placement decision (compute step vs write step + why); the commit SHA + S3 destination + comp-pipescript MATCH verification; AC1/AC2/AC3 transcripts; the hard-fail-vs-transient boundary scoping (avoid alarm-fatigue on legitimate small-firm-low-AUM situations -- the threshold must distinguish "zero" from "legitimately small"). On RAVC2-accept, MDPF_ASSETS phase narrative updated with .017 closure entry.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Anchor-reproduction: forced today-model_aum=$0.00 input -> guard raises + no write to non_model_assets.json + prior emit preserved. Transcript captured.</ac>
    <ac id="AC2">False-positive smoke: real-input run on a Schwab-clean date -> normal emit + non_model_pct in expected range per DS Base's empirical band. Transcript captured.</ac>
    <ac id="AC3">Cross-empirical 7 fixtures: re-run as fixtures against each 2026 zero-date (2026-01-02/03/04, 02-02, 03-02, 04-01, 05-01) -> guard raises on each. All 7 transcripts captured.</ac>
    <ac id="AC4">DS commit + S3 deploy cycle per Rule 13: safe-commit.sh with agent --author -> push to CLOUD -> aws s3 cp to canonical s3:// path -> comp-pipescript deployed MATCH (or, if the script runs from local DS Base machine only, document that path explicitly + cross-reference CTO rider-1 schedule answer).</ac>
    <ac id="AC5">No emoji in code or logs (ASCII only per CLAUDE.md). Pre-commit gate (.tools/ds-commit-gate.sh) exit 0 -- run by hand if ADHC_DSFLOW.007 MSYS fix has not shipped. `from __future__ import annotations` first import statement per Rule 15. Session log under `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/` with the Compiler Tools section.</ac>
    <ac id="AC6">Compiler-tools: `comp-pipescript io build_legacy_compat_emit` (likely empty per the data/mdpf/scripts/ comp-graph gap DS~B re-flagged this morning; document the gap as separate ADHC follow-up, not blocking this TO) + `comp-blast build_legacy_compat_emit` (consumer-side blast for any downstream consumers of non_model_assets.json) + direct file-read of build_legacy_compat_emit.py for placement context.</ac>
    <ac id="AC7">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO with: chosen MIN_PLAUSIBLE_THRESHOLD + tolerance + DS Base rationale; placement decision (compute vs write step + why); commit SHA + S3 destination + MATCH verification; AC1/AC2/AC3 transcripts; hard-fail-vs-transient boundary explanation. On accept, MDPF_ASSETS.json phase narrative updated with .017 closure entry + this TO status -> complete.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      `comp-pipescript io build_legacy_compat_emit` (expect empty per data/mdpf/scripts/ comp-graph gap; document as separate ADHC follow-up, not blocking).
      `comp-blast build_legacy_compat_emit` (consumer-side blast for downstream non_model_assets.json consumers).
      Direct file-read of `data/mdpf/scripts/backfill/build_legacy_compat_emit.py` for placement context.
    </before_write>
    <before_commit>
      `.tools/ds-commit-gate.sh build_legacy_compat_emit.py` exit 0 (Rule 14; run-by-hand 3 checks if ADHC_DSFLOW.007 MSYS fix has not shipped).
    </before_commit>
    <after_commit>
      `comp-pipescript deployed` MATCH if applicable to the S3-deployed runtime (post-aws-s3-cp). If the script runs only from DS Base local, document that explicitly + cross-reference CTO rider-1 schedule answer.
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    None blocking. build_legacy_compat_emit.py is DS Base-owned per CEO-direct methodology pivot. CTO rider-1 to AE 0.7 (verify build_legacy_compat_emit.py schedule) is in flight + relevant to this TO's runtime placement context but does NOT gate this TO's authoring (the guard ships regardless of schedule; CTO Opt C follow-on TO productionizes the schedule separately, downstream).
  </cross_domain_coordination>

  <out_of_scope>
    Opt C productionization of build_legacy_compat_emit.py as a scheduled Lambda/SSM (CTO follow-on, AE lane, gated on this TO + rider-1 schedule answer + v1.0.1 ship). Cleanup of the now-dead append_non_model_today step in the Lambda (AE 0.7 v1.0.1 scope). IAM grant removal for the now-dead Lambda cache path (AE follow-on TO candidate). 2nd-producer cross-validation gate against DS_aggregate emit (CTO masking-class memory rider 2 follow-on).
  </out_of_scope>

  <deliverables>
    - build_legacy_compat_emit.py with the day-1-zero guard (assert + helper + raise-don't-write + preserve-prior-emit logic).
    - Commit on CLOUD via safe-commit.sh + S3 deploy per Rule 13 + comp-pipescript MATCH verification (or document local-only runtime).
    - Session log under org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/ with: chosen MIN_PLAUSIBLE_THRESHOLD + tolerance + DS Base rationale; AC1/AC2/AC3 transcripts (1 + 1 + 7); placement decision + hard-fail-vs-transient boundary justification; comp-tools row.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO. MDPF_ASSETS.json phase narrative updated with .017 closure entry on RAVC2-accept.
  </deliverables>
</task_order>
