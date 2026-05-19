<task_order>
  <metadata>
    <id>SXIN_DAY1ZG.001</id>
    <slug>ae-smartx-ingestion-write-time-day1-zero-guard</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>SXIN_DAY1ZG</project_code>
    <priority>P1 -- TIME-PRESSURED. Closes the SmartX day-1-of-period zero-emission masking class (today's 4-anchor #3) BEFORE the next at-risk live run 2026-06-01 (Mon, first first-trading-day-of-month after smartx-pipeline-v1.0.0 went live 2026-05-19 14:12Z via de03b497a). Empirical anchor: DS 0.4 root-caused SmartX upstream emits EndMarketVal = $0.00 across all model CSVs on each reporting-period day-1 (Jan 2/3/4, Feb 2, Mar 2, Apr 1, May 1 in 2026); without a write-time guard the AE Lambda's model_aum-read step silently writes (model_aum=0, non_model = partner_custody_total) on those dates. 12-day runway from authoring to the at-risk gate.</priority>
    <sla>~0.5d wall -- a single Lambda code edit in append_non_model_today.py + tag bump (smartx-pipeline-v1.0.1 or v1.1.0 per AE convention). No new resources, no new IAM scope, no shared-state collision.</sla>
    <deadline>2026-06-01 14:00 UTC (chain run for first trading day of June 2026)</deadline>
  </metadata>

  <references>
    <origin>1.0.0_SA_CTO MCP to 2.0.0_SA_COO 2026-05-19 ("Queue: rider-2 follow-on TO sketch -- AE 0.7 smartx-ingestion-pipeline write-time guard before 2026-06-01"); rider-2 to smartx-pipeline-v1.0.0 RAVC2-accepted. DS 0.4 structural observation MCP 2026-05-19 ~13:23Z (the canonical guard recipe).</origin>
    <ds_fixes>Two-layer DS 0.4 fix shipped 2026-05-19 on the MDPF aggregate + legacy aum-timeseries paths: fb9a910b8 (drop SmartX zero-emission rows + null 1b on partial-1a coverage) + e0f22b108 (legacy-compat smooth 1/16+1/19 + skip post-cutover SmartX zero-emission dates). This TO ports the same drop-rather-than-fabricate philosophy to the AE Lambda's write path.</ds_fixes>
    <prior_ship>smartx-pipeline-v1.0.0 (Schwab-confirmed methodology for opal-smartx-ingestion-pipeline non-model writer; AE 0.7 commit de03b497a 2026-05-19 14:12Z, RAVC2-accepted by 1.0.0_SA_CTO). The Lambda computes non_model_aum = partner_custody_total(Schwab) - model_aum.</prior_ship>
    <empirical_anchor>memory/feedback_identity1_masks_absolute_value_class.md anchor #3 (SmartX day-1-of-period zero emission; today CTO RAVC 13:13Z). The 4-anchor cross-link establishes this TO as a structural-defense layer, not a one-off patch.</empirical_anchor>
    <prior_zero_dates_2026>Empirically observed in DS 0.4 fix scope: 2026-01-02, 2026-01-03, 2026-01-04, 2026-02-02, 2026-03-02, 2026-04-01, 2026-05-01 (next at-risk: 2026-06-01).</prior_zero_dates_2026>
    <pipeline_rule>Rule 1 (Terraform-only Lambda deploy) + Rule 13 (DS owns commit->QA-deploy cycle for gold/silver/bronze; AE owns infra-tooling Lambda code per existing precedent on opal-smartx-ingestion-pipeline). This TO is AE-lane: it modifies the Lambda code AE 0.7 already owns per source-map; no DS-lane gold script touched.</pipeline_rule>
  </references>

  <context>
    The opal-smartx-ingestion-pipeline Lambda runs daily (cron-fired) and computes non_model_aum per partner-firm by subtracting model_aum (read from the SmartX-derived MDPF feed) from partner_custody_total (read from the Schwab-confirmed source). On the first trading day of each reporting period, SmartX upstream emits EndMarketVal = $0.00 for every model CSV (roster-before-value-accrues behavior on the SmartX side). Without a guard, the Lambda reads model_aum = $0 on those days and writes non_model_aum = partner_custody_total -- a structurally wrong emit (non_model materially over-stated, model materially under-stated by the same amount). Identity_1 (aggregate = sum partner components) STILL PASSES on the wrong emit because the residual absorbs the leak -- exactly the absolute-value masking class anchor #3 documents. The DS 0.4 two-layer fix already covers the MDPF aggregator + legacy aum-timeseries consumers; this TO closes the writer-side gap so the bad emit never leaves the Lambda.
  </context>

  <scope>
    <step>Phase 1 -- add a defensive write-time sentinel inside append_non_model_today.py at the model_aum-read step. Per DS 0.4 canonical recipe: assert model_aum > MIN_PLAUSIBLE_THRESHOLD (~$100M; AE right-sizes per Lambda input distribution) AND/OR within +/-15% of prior business day's model_aum. Failure path: honest skip + DLQ alert + last_append carry-forward (NOT silent emit with zeroed model). Same drop-rather-than-fabricate philosophy as DS's fb9a910b8 + e0f22b108. Implementation note: structure as a small `assert_model_aum_plausible(today, prior)` helper so the threshold + tolerance are visible + testable in isolation.</step>
    <step>Phase 2 -- Terraform-only deploy per CLAUDE.md Rule 1: commit (via .tools/safe-commit.sh --author per ADHC_OWNPTH.007) -> push to CLOUD -> build/upload Lambda zip per smartx-pipeline build-and-upload pattern -> plan -> apply -> verify 0-diff -> tag smartx-pipeline-v{next} (run `git tag -l "smartx-pipeline-v*" | sort -V | tail -5` first to pick patch vs minor per AE judgment; v1.0.0 just shipped so v1.0.1 or v1.1.0 likely) -> push --follow-tags -> record-terraform-deploy.sh.</step>
    <step>Phase 3 -- Acceptance verification (run BEFORE RAVC2 close): AC1 anchor-reproduction (force-set today's model_aum to $0.00 via local fixture invoke; expect FAIL-LOUD raise + DLQ alert + last_append unchanged); AC2 false-positive smoke (invoke on a real Schwab-clean date e.g. today's chain output; expect normal emit + non_model_pct in expected range 10-15%); AC3 cross-empirical re-run against each of the 2026 zero-dates as fixtures (2026-01-02/03/04, 02-02, 03-02, 04-01, 05-01; expect FAIL-LOUD on each). Capture all three transcripts in the session log.</step>
    <step>Phase 4 -- RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO (CTO endorsed the rider-2). Record: the chosen MIN_PLAUSIBLE_THRESHOLD + tolerance + their AE-side justification (e.g. observed model_aum distribution + min day-to-day swing on real Schwab-clean dates); the tag + commit SHA + deploy timestamp; AC1/AC2/AC3 transcripts; the hard-fail-vs-transient boundary scoping (avoid alarm-fatigue on legitimate small-firm low-AUM situations -- the threshold must distinguish "zero" from "legitimately small," AE judgment).</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Anchor-reproduction: forced today-model_aum=$0.00 invoke -> Lambda raises (FAIL-LOUD) + DLQ alert fires + last_append on the partner-firm unchanged (no silent emit with zeroed model). Transcript captured.</ac>
    <ac id="AC2">False-positive smoke: real-input invoke on a Schwab-clean date (today's chain or any non-day-1 date) -> normal emit + non_model_pct in expected range (10-15% empirical band; AE confirms post-emit). Transcript captured.</ac>
    <ac id="AC3">Cross-empirical: re-run as fixtures against each 2026 zero-date (2026-01-02, 2026-01-03, 2026-01-04, 2026-02-02, 2026-03-02, 2026-04-01, 2026-05-01) -> FAIL-LOUD on each. All 7 transcripts captured.</ac>
    <ac id="AC4">Terraform-only deploy per Rule 1: commit via safe-commit.sh with agent --author -> plan -> apply -> 0-diff verified -> tagged smartx-pipeline-v{next} (latest-tag-checked) -> pushed --follow-tags -> record-terraform-deploy. No console-side Lambda code update, no aws lambda update-function-code shortcut.</ac>
    <ac id="AC5">No emoji in code or logs (ASCII only per CLAUDE.md). Pre-commit gate (.tools/ds-commit-gate.sh) exit 0 on any .py touched -- the gate is Rule 14, applies to all Python edits not just DS. (Note ADHC_DSFLOW.007 is the related MSYS-mangle fix on the gate wrapper itself -- if .007 ships before this, run the fixed gate; if not, run the three checks by hand as DS 0.4 did for the MDPF feeders.) Session log with the Compiler Tools section.</ac>
    <ac id="AC6">Compiler-tools: `comp-blast append_non_model_today` (likely empty if not in graph; document the gap as a separate ADHC follow-up not blocking this TO -- AE judgment) + direct iam.tf read confirming no new permissions needed (this is a code-only edit, no new boto3 surface) + `comp-pipescript deployed smartx-pipeline` MATCH post-deploy.</ac>
    <ac id="AC7">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO with: chosen MIN_PLAUSIBLE_THRESHOLD + tolerance + AE rationale; deployed commit SHA + tag + apply timestamp; AC1/AC2/AC3 transcripts; hard-fail-vs-transient boundary explanation; SXIN_DAY1ZG project record updated to status complete on receipt.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      `comp-blast append_non_model_today` (expect empty per trade-pipeline-uninstrumented pattern; document the gap as separate ADHC follow-up not blocking this TO -- AE judgment).
      Direct iam.tf read on smartx-pipeline confirming no new permissions needed (code-only edit; no new boto3 surface).
    </before_write>
    <before_commit>
      `.tools/ds-commit-gate.sh append_non_model_today.py` exit 0 (Rule 14 -- applies to all Python edits; run-by-hand the 3 checks if ADHC_DSFLOW.007 MSYS fix has not landed yet).
    </before_commit>
    <after_commit>
      `comp-pipescript deployed smartx-pipeline` MATCH post-apply (confirms the runner Lambda has the new code; rule out smartx-pipeline-v1.0.0 mid-flight stale state).
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    None -- smartx-pipeline Lambda is AE 0.7-owned per source-map; no shared S3 artifacts touched; the MDPF aggregator + legacy aum-timeseries fixes (DS 0.4 fb9a910b8 + e0f22b108) are read-only consumers of the SAME underlying SmartX data, not co-writers. The AE write-time guard is structurally independent of the DS consumer-side drops -- belt-and-suspenders defense layer.
  </cross_domain_coordination>

  <deliverables>
    - append_non_model_today.py with the write-time day-1-zero sentinel (assert + helper + DLQ wiring + last_append carry-forward path).
    - smartx-pipeline-v{next} tag + Terraform 0-diff apply + record-terraform-deploy.
    - Session log under org/tier2_senior/0.7.0_AE_CloudOps/logs/YYYY-MM-DD/ with: chosen MIN_PLAUSIBLE_THRESHOLD + tolerance + AE rationale; AC1/AC2/AC3 transcripts (1 + 1 + 7); hard-fail-vs-transient boundary justification; comp-tools row.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO; SXIN_DAY1ZG.json status -> complete on close.
  </deliverables>
</task_order>
