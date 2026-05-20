<task_order>
  <metadata>
    <id>ADVI_INFALM.001</id>
    <slug>ae-inf-gold-chain-failure-cw-alarm</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18 (authored backlog) / 2026-05-19 (dispatched GO, last in 3-TO sequence)</date>
    <status>complete</status>
    <completed>2026-05-20 -- inf-gold-chain-failed alarm shipped (Option B / MDPF-mirror). orion-gold-dispatch.sh emits Inflection/GoldChain.ChainFailed; iam.tf +cloudwatch:PutMetricData (namespace-scoped); alarms.tf inf-gold-chain-failed -> opal-infrastructure-alerts SNS. Deployed inf-pipeline-v1.7.64 (commit d0a682901; 2 add / 0 change / 0 destroy; 0-diff verified). Script S3-deployed to s3://opal-data-inf/code/gold/ (SHA == committed bytes). Alarm live, State=OK. record-terraform-deploy 6b4e002be. RAVC2 to COO + CC CTO.</completed>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-19 (2.0.0_SA_COO): dispatched last in the 3-TO sequence behind SXIN_DAY1ZG.001 (rider-2 priority, deadline 2026-06-01) and ADHC_DSFLOW.007 (gate-integrity higher latent-risk). Defense-in-depth + no active INF incident keeps it bottom-of-queue but it ships in the same lane sweep so AE 0.7 closes all three rider follow-ons cleanly.</dispatch_unblock_condition>
    <project_code>ADVI_INFALM</project_code>
    <priority>P2 -- defense-in-depth observability. NOT blocking: the INF gold chain is not currently failing; this closes the unalarmed-silent-failure class, it does not fix an active fault. Real gap (the entire partner-facing INF surface depends on the chain and a hard-fail is currently unalarmed) -- CTO-endorsed, durable-tracked, dispatch-prioritized by COO/Andrew.</priority>
    <sla>0.5d wall -- a single CW alarm + SNS wiring in inf-pipeline/alarms.tf, mirroring the shipped MDPF ChainFailed/DLQ alarm pattern (tag mdpf-pipeline-v1.0.0, commit ff2368d27).</sla>
  </metadata>

  <references>
    <origin>AE 0.7.0 RAVC1 to COO 20260518T233202Z, item 1 of 2 CTO-directed backlog items. CTO cited the MDPF_ASSETS RAVC1 2026-05-18 as origin so the finding is durably tracked, not lost as a mention.</origin>
    <gap>inf-pipeline/alarms.tf has only OTP/JWT/histbf-class alarms (orion_otp_timeout, jwtres_near_expiry_spike, histbf_failure_spike -> inf_otp_alert SNS). NO alarm exists on the INF gold chain itself hard-failing: reconciliation ERROR / non-zero dispatch exit / gold/meta/pipeline-complete.json not written. Silent gold-chain failure on the partner-facing surface is unalarmed.</gap>
    <precedent>mdpf-pipeline wired its own ChainFailed + DLQ alarms -> opal-infrastructure-alerts and surfaced the INF asymmetry per the phantom-consumer-class discipline. Mirror that pattern. mdpf-pipeline codify commit ff2368d27 (module + runner + trigger + alarms), tag mdpf-pipeline-v1.0.0.</precedent>
    <sns>opal-infrastructure-alerts (the MDPF target). Do NOT reuse inf_otp_alert -- that SNS is OTP/JWT-scoped; gold-chain hard-fail is a distinct alarm class and target.</sns>
  </references>

  <context>
    The Inflection partner-facing surface (advisor summary.json, platinum/firm/leaderboard.json, NNA/GRO/New-Clients/Rank) is materialized by the INF gold chain (orion-gold-dispatch.sh + the inf-gold-trigger / inf-silver-aggregator Lambdas + the gold-layer runner). If that chain hard-fails -- a reconciliation ERROR, a non-zero dispatch exit, or pipeline-complete.json never written -- there is currently no CloudWatch alarm; the failure is silent until a human notices stale partner data. MDPF, codified this session (mdpf-pipeline-v1.0.0), did not inherit the gap (it wired ChainFailed + DLQ alarms) and flagged the asymmetry. CTO endorsed closing it as a tracked follow-on.
  </context>

  <scope>
    <step>Phase 1 -- add an inf-gold-chain-failure CloudWatch alarm in inf-pipeline/alarms.tf. Preferred signal (AE selects on inspection, mirroring the MDPF pattern): a metric-filter on the gold-dispatch failure sentinel in the runner CloudWatch log group, OR a ChainFailed custom metric emitted on non-zero dispatch / reconciliation ERROR / pipeline-complete-not-written, analogous to the mdpf-pipeline ChainFailed metric. Alarm action -> opal-infrastructure-alerts SNS (NOT inf_otp_alert). Scope precisely to a true hard-fail (avoid alarm-fatigue on transient retried steps -- JWTRES auto-recovery is a designed backstop, not a chain failure).</step>
    <step>Phase 2 -- Terraform-only deploy per CLAUDE.md Rule 1: commit -> plan -> apply -> 0-diff -> tag (inf-pipeline-v{next}; run `git tag -l "inf-pipeline-v*" | sort -V | tail -5` first) -> push --follow-tags -> record-terraform-deploy. comp-iam if any new boto3/CW permission is needed; comp-blast on the alarm target. Verify the alarm exists + is in OK (or INSUFFICIENT_DATA) state post-apply; do NOT synthetically fail the live chain to test (a controlled metric-filter test-pattern injection into a non-prod log stream, or a documented manual ALARM-state transition via put-metric-data on a test metric, is acceptable -- AE judgment).</step>
    <step>Phase 3 -- RAVC2 to COO (CC CTO, since CTO endorsed the follow-on). Record: the chosen signal, the SNS target, the alarm ARN, post-apply alarm state, the tag, and how the hard-fail-vs-transient boundary was scoped.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">An inf-gold-chain-failure CloudWatch alarm exists in inf-pipeline/alarms.tf, Terraform-managed, action -> opal-infrastructure-alerts SNS. Signal fires on a true gold-chain hard-fail (reconciliation ERROR / non-zero dispatch / pipeline-complete-not-written), scoped to avoid transient-retry alarm-fatigue.</ac>
    <ac id="AC2">Deployed Terraform-only (Rule 1): plan -> apply -> 0-diff verified -> tagged inf-pipeline-v{next} (latest-tag-checked) -> pushed --follow-tags -> record-terraform-deploy. Live alarm verified present + sane state post-apply.</ac>
    <ac id="AC3">No emoji; ds-commit-gate exit 0 on any .py touched (likely none -- pure .tf); session log with the Compiler Tools section (comp-iam if new CW/boto3 perm; comp-blast on the alarm target). RAVC2 to COO + CC CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The inf-gold-chain-failure CW alarm in inf-pipeline/alarms.tf, deployed Terraform-only + tagged.
    - Session log with the Compiler Tools section + the signal/boundary rationale. RAVC2 to COO + CC CTO.
  </deliverables>
</task_order>
