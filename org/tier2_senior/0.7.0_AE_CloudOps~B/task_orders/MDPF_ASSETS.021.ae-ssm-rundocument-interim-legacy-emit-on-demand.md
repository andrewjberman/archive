<task_order>
  <metadata>
    <id>MDPF_ASSETS.021</id>
    <slug>ae-ssm-rundocument-interim-legacy-emit-on-demand</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- GAP-WINDOW INTERIM-BRIDGE INFRASTRUCTURE. Closes CTO compound (a) disposition (DS Base interim daily-fire mechanism choice = SSM RunDocument). The gap window opens NOW (v1.0.1 SHIPPED 17:09Z, Lambda neutralized, legacy file goes stale daily without DS-side daily-fire). DS Base needs a workstation-triggerable handle by tomorrow AM ~13:00 UTC for ongoing-days coverage until SXIN_PRODCT.001 productionization lands the scheduled-firing version. Small parallel sister-TO to MDPF_ASSETS.018 (chain integration); ships in the SAME AE 0.7 session since both touch `mdpf-daily-runner` EC2 instance + adjacent Terraform module. Becomes load-bearing infra that SXIN_PRODCT.001 EXTENDS (productionization just adds EventBridge cron firing the same SSM doc; not throwaway wiring).</priority>
    <sla>~30min wall per DS Base sizing -- bundled into AE's .018 session (same EC2 touch + adjacent TF module). Single SSM document + ResourceGroup + IAM-perm review.</sla>
    <deadline>Bundled with .018 close (when Andrew GO's chain-into-.018-now post v1.0.1 RAVC2 OR next AE session pickup). Tomorrow-AM DS Base AM-session ~13:00 UTC depends on this SSM doc being live; DS Base falls back to manual-on-demand .017+.019+emit run if .021 hasn't landed by then (acceptable one-day-only bridge per CTO compound (a) framing -- DS Base owns the bridge mechanism choice + DS-Base's manual run tomorrow covers that one day).</deadline>
  </metadata>

  <references>
    <origin>0.4.0_DS_ClientPlatform MCP to 2.0.0_SA_COO 2026-05-19 ~17:1XZ ("ACK .019 + path-corrections + interim daily-fire MECHANISM: SSM RunDocument bundled into AE 0.7 .018 work; tomorrow AM emit run confirmed"). CTO compound (a)+(b) disposition earlier this turn -- DS Base owns the bridge mechanism choice + COO routes the operational TO authoring.</origin>
    <chosen_mechanism>(a) SSM RunDocument per DS Base's structural reasoning: (b) workstation cron rejected as fragile under Windows-Git-Bash for any window >24h; (c) manual-on-demand-ping rejected as durable bridge (works one day, breaks any day Andrew steps away). (a) SSM RunDocument is right shape because AE already touching the EC2 instance + Terraform + the document becomes load-bearing infra SXIN_PRODCT.001 EXTENDS via EventBridge cron.</chosen_mechanism>
    <upstream_pivot>v1.0.1 SHIPPED 17:09Z + CTO RAVC2-accepted (CEO-direct methodology pivot via DS Base; broader-1b + Cohort-0-IN supersedes Schwab-only v1.0.0). Lambda `append_non_model_today` Opt-A-neutralized; DS Base's `build_legacy_compat_emit.py` is sole SoT for `non_model_assets.json`.</upstream_pivot>
    <sister_to>MDPF_ASSETS.018 (AE 0.7 chain integration, dispatched 2026-05-19 ~17:1XZ; same EC2 instance + adjacent TF module; sister session-window). MDPF_ASSETS.017 (DS Base day-1-zero guard, tomorrow-AM pickup co-shipping with .019). MDPF_ASSETS.019 (DS Base sentinels + 2nd-producer gate + WS-C --bronze-date enhancement, tomorrow-AM co-ship).</sister_to>
    <future_extension>SXIN_PRODCT.001 (AE 0.7 Opt C v1.0.2 productionization, SECOND in AE 0.7 post-v1.0.1 queue) will EXTEND this SSM RunDocument via EventBridge cron rule firing the document on schedule. The interim manual-trigger (this TO) is the same artifact at the manual-lifecycle stage; SXIN_PRODCT.001 adds the schedule-firing layer. Not throwaway wiring -- continuous infrastructure evolution.</future_extension>
    <ds_workstation_iam>DS Base's workstation IAM role already has execution perms on `mdpf-daily-runner` EC2 instance per their 5/19 re-fire runs today. AE verifies the IAM grants `ssm:SendCommand` on the new doc ARN; likely a small policy-attachment addition (NOT a new role).</ds_workstation_iam>
    <pipeline_rule>Rule 1 (Terraform-only for SSM document + ResourceGroup creation). Rule 13 (AE owns EC2 infrastructure + SSM documents; DS owns the script the document invokes, but the document itself = AE lane).</pipeline_rule>
  </references>

  <context>
    Under v1.0.1 Opt A Lambda neutralization, DS Base's `build_legacy_compat_emit.py` is the sole SoT for `non_model_assets.json`. The script currently runs manual-only on DS Base's workstation OR via manual SSH/SSM on the `mdpf-daily-runner` EC2. The gap window (until SXIN_PRODCT.001 scheduled-firing version lands) needs a durable workstation-triggerable handle for DS Base to fire the daily refresh without machine-cron fragility or per-day Andrew-coordination overhead. This TO ships that handle as an SSM RunDocument that DS Base invokes via `aws ssm send-command` from any host with their workstation IAM role; AE 0.7 ships it as a small rider on the .018 session since both touch the same EC2 instance + adjacent TF module. SXIN_PRODCT.001 productionization later wires an EventBridge cron rule firing the same SSM doc -- the document becomes the load-bearing artifact across the manual-bridge + scheduled-production lifecycle stages.
  </context>

  <scope>
    <step>Phase 1 -- SSM document spec per DS Base sketch:
      - Doc name: `mdpf-legacy-emit-on-demand` (or AE-preferred naming convention).
      - Target: `mdpf-daily-runner` instance via tag-based ResourceGroup (`Service=mdpf-daily-runner` or AE-equivalent existing tag).
      - Script: pulls `build_legacy_compat_emit.py` from `s3://opal-data-mdpf/code/scripts/backfill/` (DS Base confirms canonical S3 path -- this is the same path mdpf-daily-runner already syncs from; reuse existing IAM grants for the EC2 instance profile).
      - Invocation: Python on the EC2 (existing Python runtime; no new layer/venv).
      - Args: `--date $(date -u +%Y-%m-%d) --upload` (latest-business-day auto-resolve; AE may add `--bronze-date` auto-resolve too if DS Base's WS-C enhancement pattern from .019 generalizes -- AE picks).
      - Exit-code check: SSM-doc fails LOUD on non-zero exit; reports stderr.
      - Telemetry: writes execution result to `s3://opal-data-mdpf/telemetry/mdpf-daily-runner/legacy-emit-runs/{run_id}.json` (or AE-equivalent per opal-runner-shared schema) with last-emit-timestamp + Cohort 0 value + headline figure + exit code.</step>
    <step>Phase 2 -- ResourceGroup (if not already existing) + IAM policy addition for DS Base workstation role: grant `ssm:SendCommand` on the new doc ARN + `ssm:DescribeAutomationExecutions` for visibility. AE verifies DS Base's existing IAM role identity (confirm with DS Base if uncertain) + scopes the new policy attachment narrowly to this doc.</step>
    <step>Phase 3 -- Terraform-only deploy per CLAUDE.md Rule 1: place the new SSM doc + IAM policy in `infra/aws/terraform/mdpf-pipeline/` (or adjacent module per AE convention) -> commit via .tools/safe-commit.sh --author -> push CLOUD -> plan -> apply -> verify 0-diff -> tag in the same `mdpf-pipeline-v{next}` tag as the .018 cron shift (single tag covers both .018 + .021 work since same TF module) -> push --follow-tags -> record-terraform-deploy.</step>
    <step>Phase 4 -- empirical verification:
      AC1 SSM doc invocation: AE invokes the doc once (`aws ssm send-command --document-name mdpf-legacy-emit-on-demand --targets Key=tag:Service,Values=mdpf-daily-runner`) + verifies execution succeeds + telemetry artifact written to S3.
      AC2 DS Base workstation invocation: AE coordinates with DS Base for them to invoke the doc once from their workstation + verify their IAM role works. (Cross-agent verification step -- AE confirms with DS Base via MCP that their invocation succeeded.)
      AC3 telemetry shape: verify the S3 telemetry artifact has the schema spec'd (last-emit-timestamp + Cohort 0 + headline figure + exit code).
      Capture transcripts.</step>
    <step>Phase 5 -- RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform (DS Base is the consumer of the workstation-trigger handle; must confirm AC2 invocation works). Record: SSM doc ARN + IAM policy addition + tag + apply timestamp; AC1/AC2/AC3 transcripts; DS Base invocation confirmation. On RAVC2-accept: MDPF_ASSETS.json phase narrative updated with .021 closure entry; this TO status -> complete. DS Base interim daily-fire mechanism is LIVE.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">SSM doc `mdpf-legacy-emit-on-demand` (or AE-name) live; AE invocation from any-host-with-AE-role succeeds + telemetry artifact written to `s3://opal-data-mdpf/telemetry/...` with spec'd schema (last-emit-timestamp + Cohort 0 + headline + exit code). Transcript captured.</ac>
    <ac id="AC2">DS Base workstation invocation succeeds (coordinated with DS Base via MCP); confirms DS Base's IAM role has the needed perms post-policy-attachment. DS Base ACKs success in MCP back to AE.</ac>
    <ac id="AC3">Telemetry artifact schema verified: spec'd fields present + parseable. SSM execution history visible via `aws ssm list-command-invocations` for the doc.</ac>
    <ac id="AC4">Terraform-only deploy per Rule 1: commit via safe-commit.sh -> push CLOUD -> plan -> apply -> 0-diff verified -> tagged `mdpf-pipeline-v{next}` (single tag covers .018 + .021 since same TF module; or AE picks per convention) -> pushed --follow-tags -> record-terraform-deploy.</ac>
    <ac id="AC5">No emoji (ASCII only per CLAUDE.md). Pre-commit gate on any .py touched (likely none -- pure SSM doc YAML + Terraform). Session log under `org/tier2_senior/0.7.0_AE_CloudOps/logs/YYYY-MM-DD/` with Compiler Tools section.</ac>
    <ac id="AC6">Compiler-tools: comp-iam service for the new SSM doc IAM scope (verify scoped narrowly to the doc ARN; no broad ssm:* grants) + comp-blast on the SSM doc name (downstream-consumer check; SXIN_PRODCT.001 will be a consumer when productionization adds EventBridge cron firing).</ac>
    <ac id="AC7">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform with: SSM doc ARN + IAM addition diff + tag + apply timestamp; AC1/AC2/AC3 transcripts; DS Base AC2 confirmation. On accept: MDPF_ASSETS.json phase narrative updated; this TO status -> complete; DS Base interim mechanism LIVE.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      Direct file-read of `infra/aws/terraform/mdpf-pipeline/` for the SSM doc + IAM policy placement context.
      DS Base confirmation of canonical `build_legacy_compat_emit.py` S3 path (`s3://opal-data-mdpf/code/scripts/backfill/` per DS Base sketch -- verify before doc reference).
      DS Base IAM role identity confirmation (channel-push if uncertain).
    </before_write>
    <before_commit>
      comp-iam service for any new IAM scope (verify SSM doc grants are scoped narrowly).
    </before_commit>
    <after_commit>
      comp-blast on the SSM doc name (post-apply; future SXIN_PRODCT.001 consumer check).
      Direct verification of the SSM doc state post-apply (`aws ssm describe-document --name`).
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Sister-bundles with MDPF_ASSETS.018 (same AE 0.7 session, same EC2 instance, adjacent TF module). DS Base consumer: AC2 requires DS Base workstation invocation verification (cross-agent confirmation via MCP). SXIN_PRODCT.001 future-extension: productionization will fire this SSM doc via EventBridge cron; this TO is the foundation, .001 is the scheduled-trigger layer.
  </cross_domain_coordination>

  <out_of_scope>
    EventBridge cron firing the SSM doc (that's SXIN_PRODCT.001 scope -- "productionize DS emit as scheduled" maps to wiring the cron rule firing this SSM doc). The SSM doc itself ships here; the scheduling lands in SXIN_PRODCT.001.
  </out_of_scope>

  <deliverables>
    - SSM RunDocument `mdpf-legacy-emit-on-demand` (or AE-name) live in mdpf-pipeline TF module.
    - IAM policy attachment for DS Base workstation role granting `ssm:SendCommand` on the doc ARN.
    - Telemetry schema (last-emit-timestamp + Cohort 0 + headline + exit code) written to `s3://opal-data-mdpf/telemetry/...` on each invocation.
    - `mdpf-pipeline-v{next}` tag (single tag with .018 cron shift, or AE picks separation).
    - Session log under org/tier2_senior/0.7.0_AE_CloudOps/logs/YYYY-MM-DD/ with: SSM doc YAML + IAM diff; AC1/AC2/AC3 transcripts; comp-tools row.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform.
  </deliverables>
</task_order>
