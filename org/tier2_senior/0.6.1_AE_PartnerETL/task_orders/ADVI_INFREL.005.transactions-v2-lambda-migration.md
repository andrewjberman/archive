<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.005</id>
    <project>ADVI_INFREL</project>
    <title>transactions_v2 Lambda migration (conditional on INFINGE TO-5a TXN rate-empirical)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>staged</status><!-- SUPERSEDED BY ADVI_INFINGE.005b 2026-05-06. CTO Q-A/Q-B rulings (session 10) changed path schema (bronze/orion-api/{date}/transactions.csv, silver/api_dims/transactions) and confirmed Custom Reports _v2.py path. INFINGE.005b covers bronze pull Lambda + silver builder. This TO's scope (transactions_v2 Lambda, orion-api-v2 paths, _v2 suffix silver) is stale. DO NOT EXECUTE. -->
    <priority>high</priority>
    <estimated_effort>~0.5d AE post TO-4 ship (pure clone+prefix substitute); CONDITIONAL on rate-empirical</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1; §4.4 + §6 TO-5</ref>
    <ref type="template_reference">TO-4 (unified_account_dim) — Phase 2 Lambda module pattern</ref>
    <ref type="conditional_gate">INFINGE TO-5a (TXN rate-empirical) — if 2+ RPS not sustainable for transactions, transactions_v2 likely shares constraint; investigate before TO-5 ship</ref>
  </references>

  <context>
    `transactions_v2` is a path-1 orchestrator-bound dim. Migration mirrors TO-4 pattern with prefix substitution.

    Output paths:
    - Bronze: `bronze/orion-api-v2/{date}/transactions_v2.json`
    - Silver: `silver/api_dims/transactions_v2/{date}/data.parquet`

    EventBridge cron: 13:10 UTC (5min after TO-4 unified_account_dim 13:05 UTC).

    Naming: `inf-api-transactions-v2` Lambda + `inf-api-transactions-v2-rule` + `inf-api-transactions-v2-role`.

    **Conditional:** if INFINGE TO-5a (TXN rate-empirical) reveals 2+ RPS NOT sustainable for `transactions` dim, `transactions_v2` may share constraint. Pre-flight check: run rate test on transactions_v2 standalone; if rate-bound, fold into Phase 2.5 OR stay on orchestrator.
  </context>

  <phase id="0" when="Phase 0 — rate-empirical pre-flight (gates on INFINGE TO-5a)">
    <step>
      <run>Verify INFINGE TO-5a (TXN rate-empirical) ship + RAVC5. Read empirical findings.</run>
      <expect>Findings clear: transactions dim sustains 2+ RPS YES/NO. If YES, transactions_v2 likely also fits; proceed to Phase 1. If NO, scope TO-5 conservatively (longer wall + smaller batch).</expect>
      <if_mismatch>If TO-5a not yet shipped: hold TO-5; rate-empirical determines path.</if_mismatch>
    </step>
    <step>
      <run>Standalone rate-empirical for transactions_v2: invoke pull script with timer; measure wall + memory + API call count + RPS.</run>
      <expect>Lambda-fits decision: wall &lt;15min, memory &lt;3GB, RPS sustainable.</expect>
      <if_mismatch>If transactions_v2 NOT Lambda-fit: surface to me + CTO; consider keeping on orchestrator or splitting into multi-invocation pattern.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="implementation — same shape as TO-4">
    <step>
      <run>Per TO-4 Phase 2 pattern; substitute prefix `unified-account-dim` → `transactions-v2`</run>
      <expect>Per TO-4 Phase 2</expect>
      <if_mismatch>Per TO-4 Phase 2 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before terraform apply">
    <step>
      <run>Per TO-4 Phase 3</run>
      <expect>Per TO-4 Phase 3</expect>
      <if_mismatch>Per TO-4 Phase 3 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="terraform apply + tag + empirical">
    <step>
      <run>Per TO-4 Phase 4 with cron 13:10 UTC</run>
      <expect>Bronze + silver paths populated</expect>
      <if_mismatch>Per TO-4 Phase 4 if_mismatch</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on TO-4 + INFINGE TO-5a.** Both must close clean.</coord>
    <coord>**Conditional ship.** If rate-bound: stay on orchestrator until empirical resolves; do NOT force-ship.</coord>
    <coord>**Hardcoded mapping audit** per Risk Register (ADVISOR_KEY_TO_REP_ID-style search in transactions_v2 script).</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">Per TO-4 Phase 1 mandate; substitute `inf-api-transactions-v2` for `inf-api-unified-account-dim`</phase>
    <phase id="2" when="before commit">Per TO-4 Phase 2 mandate</phase>
    <phase id="3" when="after deploy">Per TO-4 Phase 3 mandate; 24h empirical at 13:10 UTC</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Fresh `bronze/orion-api-v2/{D+1}/transactions_v2.json` + `silver/api_dims/transactions_v2/{D+1}/data.parquet` by 13:15 UTC daily.</criterion>
    <criterion id="AC2">CW Metric `Opal/InflectionIngestion/TransactionsV2Pulled` increments daily.</criterion>
    <criterion id="AC3">CW Alarm fires on 2 consecutive failures.</criterion>
    <criterion id="AC4">orchestrator.py removed transactions_v2 entry.</criterion>
    <criterion id="AC5">Silver propagates daily.</criterion>
    <criterion id="AC6">comp-iam gaps clean.</criterion>
    <criterion id="AC7">Tag bumped + pushed.</criterion>
    <criterion id="AC8">RAVC5 close package complete.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — gates on TO-4 RAVC5 + INFINGE TO-5a rate-empirical resolution</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged`. Conditional on rate-empirical.</message>
  </go_signal>
</task_order>
