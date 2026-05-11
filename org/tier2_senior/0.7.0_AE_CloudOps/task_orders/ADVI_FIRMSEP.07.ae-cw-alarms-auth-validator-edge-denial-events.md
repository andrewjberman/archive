<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.07</id>
    <project>ADVI_FIRMSEP</project>
    <title>CW alarms on auth-validator-edge denial events — defense-in-depth observability</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-11</completed_date>
    <completed_commit><!-- already deployed pre-2026-05-11; 0-diff plan confirmed --></completed_commit>
    <priority>medium</priority>
    <estimated_effort>~0.25d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.7 + §6 Phase 2</ref>
    <ref type="sns_topic">opal-infrastructure-alerts (existing)</ref>
    <ref type="log_group">/aws/lambda/us-east-1.auth-validator-edge (Lambda@Edge logs land per-region; us-east-1 is the primary)</ref>
  </references>

  <context>
    Lambda@Edge runs across all CloudFront edge regions; logs land in each region's
    /aws/lambda/{region}.{function-name} log group. Most denial-event traffic concentrates in
    us-east-1; broader coverage may need cross-region metric filters in a future iteration.

    Phase 1 ships a clean baseline; Phase 2 alarms on top of that baseline. Alarms surface any
    cross-firm scoping attempt (legitimate or not) — and any sudden uptick is signal for
    either a deploy regression or a reconnaissance attempt.

    Ships AFTER Phase 1 (.01-.05) so the baseline is clean.
  </context>

  <scope>
    <step>
      In portal-auth Terraform — add 4 CW Logs metric filters on the us-east-1
      auth-validator-edge log group (additional regions deferred to Phase 4 carry-over):

      Filter 1 — advisor_scoping_denied:
        pattern: "advisor_scoping_denied"
        metric_namespace: "opal/firmsep"
        metric_name: "AuthValidatorAdvisorScopingDenied"

      Filter 2 — tier_denied:
        pattern: "tier_denied"
        metric_name: "AuthValidatorTierDenied"

      Filter 3 — ownership_map_fetch_failed:
        pattern: "ownership_map_fetch_failed"
        metric_name: "AuthValidatorOwnershipMapFetchFailed"

      Filter 4 — ownership_map_schema_mismatch:
        pattern: "ownership_map_schema_mismatch"
        metric_name: "AuthValidatorOwnershipMapSchemaMismatch"

      (Verify exact log line patterns in auth-validator-edge/index.mjs source first; the PRD
      cites these names but the code may use slightly different casing/structure.)
    </step>
    <step>
      Add 4 CW alarms in portal-auth/cloudwatch-alarms.tf (or analogous):

      Alarm 1: advisor_scoping_denied > 5/min for 1 datapoint → opal-infrastructure-alerts SNS.
      Alarm 2: tier_denied > 5/min for 1 datapoint → SNS.
      Alarm 3: ownership_map_fetch_failed > 1/min for 1 datapoint → SNS (fail-closed surface).
      Alarm 4: ownership_map_schema_mismatch > 0 for 1 datapoint (stop-the-line — any > 0 is bad) → SNS.
    </step>
    <step>
      terraform plan — should show ADD of 4 metric filters + 4 alarms only.
    </step>
    <step>
      apply.
    </step>
    <step>
      Empirical: synthesize one denial event (curl portal with intentionally-mismatched JWT
      claim → expect 403 + log line). Within 2-3min, verify CW metric updates. Don't trip the
      alarm threshold (single event << 5/min); just confirm metric flow works.
    </step>
    <step>
      Tag bump portal-auth-v1.X.Y. Push --follow-tags. record-terraform-deploy.sh.
    </step>
    <step>
      RAVC2 to COO with plan/apply, log-line pattern verification (grep auth-validator-edge
      source for the 4 patterns), single-event synthesis evidence, tag.
    </step>
  </scope>

  <compiler_mandate>
    <tool>terraform plan — ADD 4 filters + 4 alarms only</tool>
    <tool>grep auth-validator-edge source for actual log emit patterns — confirm match</tool>
    <tool>CW metric flow synthesis (single denial event → metric tick)</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">4 CW Logs metric filters land on us-east-1 auth-validator-edge log group.</criterion>
    <criterion id="AC2">4 CW alarms wired to opal-infrastructure-alerts SNS.</criterion>
    <criterion id="AC3">terraform plan/apply 0-diff post; portal smoke unaffected.</criterion>
    <criterion id="AC4">Empirical: single synthetic denial event → metric updates in CW within 2-3min.</criterion>
    <criterion id="AC5">Tag bump + push --follow-tags + record-terraform-deploy.sh.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>Phase 1 ships (.01-.05) for clean baseline.</upstream>
    <downstream>None.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Phase 2 ships post Phase 1 baseline. us-east-1 only this iteration; cross-region deferred to Phase 4 carry-over.</message>
  </go_signal>
</task_order>
