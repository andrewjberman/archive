<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.08</id>
    <project>ADVI_FIRMSEP</project>
    <title>CW alarm on shared-advisor-router 400/401 — defense-in-depth observability</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-11</completed_date>
    <completed_commit><!-- already deployed pre-2026-05-11; 0-diff plan confirmed --></completed_commit>
    <priority>medium</priority>
    <estimated_effort>~0.15d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.7 + §6 Phase 2</ref>
    <ref type="sns_topic">opal-infrastructure-alerts</ref>
    <ref type="log_group">/aws/lambda/us-east-1.shared-advisor-router</ref>
    <ref type="sibling_to">TO-FIRMSEP.07 — same pattern, applied to shared-advisor-router</ref>
  </references>

  <context>
    shared-advisor-router emits 400 (missing X-Firm-Id, missing ?firm= for opal-capital staff)
    and 401 (defense-in-depth tier/scope re-check failures) responses. A spike is either
    benign (bot scanning) or signal (router regression after a deploy / unauthorized
    enumeration attempt).

    Sibling to TO-FIRMSEP.07 — same pattern, single function. Smaller TO because there's only
    one alarm (combined 400/401) rather than 4 distinct denial-event types.
  </context>

  <scope>
    <step>
      In portal-auth Terraform — add CW Logs metric filter on us-east-1 shared-advisor-router
      log group.
        Filter pattern: matches both 400 and 401 status emissions.
        Inspect shared-advisor-router/index.mjs to find the actual response emit pattern
        (likely `console.log` with a `status: 400` or `status: 401` field, or HTTP response
        construction). Match accordingly.
        metric_namespace: "opal/firmsep"
        metric_name: "SharedAdvisorRouterDenied"
    </step>
    <step>
      Add CW alarm:
        threshold: > 5/min for 1 datapoint
        action: opal-infrastructure-alerts SNS
    </step>
    <step>
      terraform plan — ADD 1 metric filter + 1 alarm only.
    </step>
    <step>
      apply.
    </step>
    <step>
      Empirical: synthesize a 400 (curl /api/scoped/advisor-intelligence/* with no
      X-Firm-Id header through CF) → confirm metric tick.
    </step>
    <step>
      Tag bump + push --follow-tags + record-terraform-deploy.sh.
    </step>
    <step>
      RAVC2 to COO.
    </step>
  </scope>

  <compiler_mandate>
    <tool>terraform plan — ADD 1 + 1</tool>
    <tool>grep shared-advisor-router source for response emit patterns — confirm filter match</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">CW Logs metric filter on us-east-1 shared-advisor-router log group lands.</criterion>
    <criterion id="AC2">CW alarm > 5/min wired to SNS.</criterion>
    <criterion id="AC3">terraform 0-diff post-apply; portal smoke unaffected.</criterion>
    <criterion id="AC4">Empirical synthetic denial → metric updates in CW.</criterion>
    <criterion id="AC5">Tag bump + push --follow-tags.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>Phase 1 ships (clean baseline).</upstream>
    <downstream>None.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Sibling to FIRMSEP.07; same Phase 2 timing.</message>
  </go_signal>
</task_order>
