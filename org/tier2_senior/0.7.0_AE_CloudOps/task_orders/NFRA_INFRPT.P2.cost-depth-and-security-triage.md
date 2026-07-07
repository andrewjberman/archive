<to_id>NFRA_INFRPT.P2</to_id>
<project>NFRA_INFRPT</project>
<title>MONEY depth (per-pipeline attribution + trend/forecast + biggest-movers + EC2 right-size) + SECURITY triage (trend/top-N-new/Claude briefing)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<co_assignees>none (AE-lane: Cost Explorer + security sweep + the Lambda)</co_assignees>
<issued_by>2.0.0_SA_COO (NFRA_INFRPT decomposition 2026-06-16; CVO proposal 6d5954360 §A/§4 + §G/§5)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>complete -- shipped 2026-07-07 (3 increments: cost-depth/security-trend + snapshot-reaper; COO commit "NFRA_INFRPT.P2 complete", CI artifacts uploaded for opal-infrastructure-monitor). Status backfilled by COO~B 2026-07-07 dedup -- worker-dir copy was stale-open; the COO-dir NFRA_INFRPT.P2.cost-depth-reaper is the completed reaper sub-slice of this same P2.</status>
<priority>HIGH — cost is the section Andrew VALUES + the biggest enhancement lever. Lands after P1. Gate: P0/P1 landed + AE capacity.</priority>

<references>
  <ref type="proposal">docs/briefs/infra-report-revamp-proposal-20260616.md §4/§A (cost) + §5/§G (security)</ref>
  <ref type="cost-context">The c6i.16xlarge bd-gold runner ~34% of the monthly bill is the known cost lever; no cost-allocation tags exist today (name-prefix heuristic).</ref>
</references>

<scope>
**(A) MONEY depth** — the Lambda already holds ce:GetCostAndUsage. Enhance the existing top-10-by-service:
- TREND: MTD vs same-day-last-month + month-end FORECAST (is $293 high?).
- BIGGEST MOVERS: day-over-day / week-over-week deltas per service (catch a spike the day it lands).
- PER-PIPELINE attribution: the firm thinks in pipelines (bd/inf/cot/yang/smartx/news), not AWS services. Start with a resource-NAME-PREFIX heuristic (`bd-*`, `inf-*`, `yang-*`, `smartx-*`, `news-*`) since NO cost-allocation tags exist (add tags later as a follow-on). Surface the known levers (e.g. the bd-gold c6i.16xlarge runner share).
- EC2 RIGHT-SIZE watch: the c6i.16xlarge runner hours + any instance running OUTSIDE its expected window. (Respect the purpose-kept bd-gold-qa-runner — do NOT flag a PROD-isolation-kept stopped box as decommissionable.)
- Bedrock spend (from P0's triage re-home) shows here too — self-consistent.
**(G) SECURITY triage** — replace bare counts (CRITICAL 0 / HIGH 116 / ...) with: trend (new today / resolved today / chronic-accepted), top-N NEW actionable findings, suppress the chronic-accepted baseline, + the Claude briefing (Bedrock, per P0's re-home).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-iam service opal-infrastructure-monitor</run>
      <expect>ce:GetCostAndUsage already present (cost). The security sweep + Claude briefing reuse existing perms + Bedrock (from P0). No new IAM expected.</expect>
      <if_mismatch>Add any new perm via Terraform + comp-iam gaps.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before deploy">
    <step>
      <run>comp-iam gaps (if iam.tf changed)</run>
      <expect>No new gap.</expect>
      <if_mismatch>Resolve before apply (Terraform-only).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>Trigger a report + sanity-check the cost numbers (per-pipeline attribution sums to ~the service totals; forecast is plausible vs MTD; movers match a known recent change)</run>
      <expect>Per-pipeline attribution reconciles to the AWS-service totals (no double-count / no gap); forecast magnitude-plausible; security trend distinguishes new-vs-chronic. EC2 right-size flags exclude the purpose-kept boxes.</expect>
      <if_mismatch>Reconcile (a per-pipeline total that doesn't sum to the service total is a wrong attribution).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- Cost attribution is a HEURISTIC (name-prefix) until cost-allocation tags exist — label it as such in the report (don't present a heuristic as exact). Adding tags = a follow-on (coordinate with NFRA_COSTAWS).
- Security briefing uses the same Bedrock path as P0's triage re-home (no second mechanism).
- Magnitude-sanity: any cost number the section surfaces gets a plausibility check (the /govern magnitude heuristic) before it ships.
</cross_domain_coordination>

<acceptance_criteria>
- MONEY: MTD-vs-last-month + month-end forecast + per-service biggest-movers + per-pipeline (name-prefix, labeled heuristic) attribution + EC2 right-size flags (purpose-kept boxes excluded).
- SECURITY: trend (new/resolved/chronic) + top-N new + Claude (Bedrock) briefing; chronic-accepted baseline suppressed.
- Phase-3: per-pipeline attribution reconciles to service totals; forecast plausible; no double-count.
- Deployed via Terraform; comp-iam gaps clean if iam.tf changed.
- Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Report-generator logic only; reads Cost Explorer + the security sweep live each run.</no_reprocess_needed></data_reprocess_scope>
