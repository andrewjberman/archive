<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.007</id>
    <project>ADVI_INFREL</project>
    <title>tax Lambda migration (Phase 2 fourth; closes Phase 2)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>staged</status><!-- Authored sprint mode 2026-05-05T~21:15Z. Gates on TO-6 (billing) RAVC5. Pure clone+prefix substitute. Closes Phase 2; unblocks TO-9 (decom). -->
    <priority>high</priority>
    <estimated_effort>~0.5d AE post TO-6 ship; pure clone+prefix substitute</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1; §4.4 + §6 TO-7</ref>
    <ref type="template_reference">TO-4/5/6 — Phase 2 Lambda module pattern</ref>
  </references>

  <context>
    `tax` is the final path-1 orchestrator-bound dim in Phase 2. Migration mirrors TO-4/5/6 pattern.

    Output paths:
    - Bronze: `bronze/orion-api-v2/{date}/tax.json`
    - Silver: `silver/api_dims/tax/{date}/data.parquet`

    EventBridge cron: 13:20 UTC.

    Naming: `inf-api-tax` Lambda + `inf-api-tax-rule` + `inf-api-tax-role`.

    **Phase 2 closer** — once TO-7 ships, all path-1 dims are Lambda-native; orchestrator.py has zero remaining dim responsibilities; TO-9 (decom) gate clears.
  </context>

  <phase id="1" when="implementation — clone TO-6 module + prefix substitute">
    <step>
      <run>Per TO-4/5/6 Phase 2 pattern; substitute prefix `billing` → `tax`</run>
      <expect>Per TO-4/5/6 Phase 2</expect>
      <if_mismatch>Per TO-4/5/6 Phase 2 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before terraform apply">
    <step>
      <run>Per TO-4/5/6 Phase 3</run>
      <expect>Per TO-4/5/6 Phase 3</expect>
      <if_mismatch>Per TO-4/5/6 Phase 3 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="terraform apply + tag + empirical">
    <step>
      <run>Per TO-4/5/6 Phase 4 with cron 13:20 UTC</run>
      <expect>Bronze + silver paths populated</expect>
      <if_mismatch>Per TO-4/5/6 Phase 4 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="Phase 2 closure validation — gates TO-9 (decom)">
    <step>
      <run>comp-blast inf-bronze-runner — verify zero remaining dim responsibilities post TO-7 ship + INFINGE Phase 1b complete</run>
      <expect>comp-blast empty (or only legacy/orphan responsibilities documented + cleared); TO-9 unblocked</expect>
      <if_mismatch>If non-zero responsibilities remain: identify + decide (migrate OR document-as-orphan); do NOT decom until clean</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on TO-6 RAVC5.** Closes Phase 2.</coord>
    <coord>**Unblocks TO-9 (decom).** Post TO-7 + INFINGE Phase 1b + 48h soak → TO-9 dispatch.</coord>
    <coord>**Hardcoded mapping audit** per Risk Register.</coord>
    <coord>**Compliance-relevant** (tax dim) — comp-pii audit pre-deploy.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">Per TO-6 Phase 1 mandate + comp-pii audit</phase>
    <phase id="2" when="before commit">Per TO-6 Phase 2 mandate</phase>
    <phase id="3" when="after deploy">Per TO-6 Phase 3 mandate; 24h empirical at 13:20 UTC</phase>
    <phase id="4" when="Phase 2 closure">comp-blast inf-bronze-runner — zero-responsibilities check</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Fresh `bronze/orion-api-v2/{D+1}/tax.json` + `silver/api_dims/tax/{D+1}/data.parquet` by 13:25 UTC daily.</criterion>
    <criterion id="AC2">CW Metric `Opal/InflectionIngestion/TaxPulled` increments daily.</criterion>
    <criterion id="AC3">CW Alarm fires on 2 consecutive failures.</criterion>
    <criterion id="AC4">orchestrator.py removed tax entry; **all path-1 dims removed; orchestrator.py zero-dim**.</criterion>
    <criterion id="AC5">Silver propagates daily.</criterion>
    <criterion id="AC6">comp-iam gaps clean + comp-pii audit clean.</criterion>
    <criterion id="AC7">Tag bumped + pushed.</criterion>
    <criterion id="AC8">comp-blast inf-bronze-runner — zero remaining responsibilities; TO-9 unblocked.</criterion>
    <criterion id="AC9">RAVC5 close package complete + Phase 2 closure RAVC.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — gates on TO-6 RAVC5</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged`. Closes Phase 2; unblocks TO-9 (decom).</message>
  </go_signal>
</task_order>
