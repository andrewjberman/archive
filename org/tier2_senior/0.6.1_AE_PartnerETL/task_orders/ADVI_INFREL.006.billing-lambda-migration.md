<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.006</id>
    <project>ADVI_INFREL</project>
    <title>billing Lambda migration (Phase 2 third)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>staged</status><!-- Authored sprint mode 2026-05-05T~21:15Z. Gates on TO-5 (transactions_v2) RAVC5. Pure clone+prefix substitute from TO-4 template. -->
    <priority>high</priority>
    <estimated_effort>~0.5d AE post TO-5 ship; pure clone+prefix substitute</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1; §4.4 + §6 TO-6</ref>
    <ref type="template_reference">TO-4 (unified_account_dim) + TO-5 (transactions_v2) — Phase 2 Lambda module pattern</ref>
  </references>

  <context>
    `billing` is a path-1 orchestrator-bound dim. Migration mirrors TO-4/5 pattern.

    Output paths:
    - Bronze: `bronze/orion-api-v2/{date}/billing.json`
    - Silver: `silver/api_dims/billing/{date}/data.parquet`

    EventBridge cron: 13:15 UTC.

    Naming: `inf-api-billing` Lambda + `inf-api-billing-rule` + `inf-api-billing-role`.
  </context>

  <phase id="1" when="implementation — clone TO-5 module + prefix substitute">
    <step>
      <run>Per TO-4/5 Phase 2 pattern; substitute prefix `transactions-v2` → `billing`</run>
      <expect>Per TO-4/5 Phase 2</expect>
      <if_mismatch>Per TO-4/5 Phase 2 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before terraform apply">
    <step>
      <run>Per TO-4/5 Phase 3</run>
      <expect>Per TO-4/5 Phase 3</expect>
      <if_mismatch>Per TO-4/5 Phase 3 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="terraform apply + tag + empirical">
    <step>
      <run>Per TO-4/5 Phase 4 with cron 13:15 UTC</run>
      <expect>Bronze + silver paths populated</expect>
      <if_mismatch>Per TO-4/5 Phase 4 if_mismatch</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on TO-5 RAVC5.**</coord>
    <coord>**Hardcoded mapping audit** per Risk Register.</coord>
    <coord>**Compliance-driven dim** — billing has compliance-relevance per PRD framing; verify no PII exposure post-migration via comp-pii audit.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">Per TO-5 Phase 1 mandate + comp-pii audit (compliance check)</phase>
    <phase id="2" when="before commit">Per TO-5 Phase 2 mandate</phase>
    <phase id="3" when="after deploy">Per TO-5 Phase 3 mandate; 24h empirical at 13:15 UTC</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Fresh `bronze/orion-api-v2/{D+1}/billing.json` + `silver/api_dims/billing/{D+1}/data.parquet` by 13:20 UTC daily.</criterion>
    <criterion id="AC2">CW Metric `Opal/InflectionIngestion/BillingPulled` increments daily.</criterion>
    <criterion id="AC3">CW Alarm fires on 2 consecutive failures.</criterion>
    <criterion id="AC4">orchestrator.py removed billing entry.</criterion>
    <criterion id="AC5">Silver propagates daily.</criterion>
    <criterion id="AC6">comp-iam gaps clean + comp-pii audit clean.</criterion>
    <criterion id="AC7">Tag bumped + pushed.</criterion>
    <criterion id="AC8">RAVC5 close package complete.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — gates on TO-5 RAVC5</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged`.</message>
  </go_signal>
</task_order>
