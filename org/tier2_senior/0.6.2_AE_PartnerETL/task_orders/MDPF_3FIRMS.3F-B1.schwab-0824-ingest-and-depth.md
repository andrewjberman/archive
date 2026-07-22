<task_order>
<id>MDPF_3FIRMS.3F-B1</id>
<title>49F/Schwab 0824 bronze leg — verify the 2x-daily pull fire history + silver-sweep coupling; document vendor depth vs silver floor</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-B (Bronze)</workstream>
<issued_to>0.6.2_AE_PartnerETL~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:23Z</issued_at>
<status>staged</status>
<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z -> COO decomposition.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §2.2 (49F-AUA row); §4 WS-B row 3F-B1; §5 ruling 2</ref>
</references>

<scope>
Verify the ingestion mechanism and backfill completeness of the 49 Financial AUA leg
(`schwab/08242234`, the **0824 Model Portfolios master**, basis `schwab-rps`).

Three deliverables:
(a) **Fire history** of `canonical-schwab-si2-08242234-daily-pull` (cron(15 10,22 UTC), 2x/day) over a
    30-day window — evidence, not configuration.
(b) **Silver-sweep coupling**: `opal-assets-silver-schwab-sweep-daily` (cron(15 12)) — show the pull ->
    sweep -> `fact_rps_s2` partition chain actually completes, not merely that both rules exist.
(c) **Depth statement with vendor citation**: silver reaches `date=2024-05-24`; the gold spec cites 427
    dates from 2024-11-01. Reconcile the two floors. Andrew's standing read is that this leg "seems in
    good condition on backfill" — CONFIRM OR REFUTE it with evidence rather than inheriting it.

⛔ **TWO STANDING PROHIBITIONS BIND THIS LEG AND THEY ARE SEPARATE:** the 0824 and 0833 Schwab buckets
are **NEVER SUMMED** *and* **NEVER SUBSTITUTED** for one another (0833 = Advisor Intelligence master;
0824 = Model Portfolios master — a business-purpose split). **A law about addition cannot license a
selection.** Never blended-preferred in place of schwab-rps. Every artifact carries `basis: schwab-rps`.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-freshness</run>
      <expect>The 49F leg resolves on freshness_basis: trading-day-frontier; CURRENT at T-1.</expect>
      <if_mismatch>A flat-hours entry WILL false-alarm every Monday. Record the gap; do not raise it as staleness (NEVER#1).</if_mismatch>
    </step>
    <step>
      <run># rail-checked: EventBridge applied truth is not comp-modeled
aws events describe-rule --name canonical-schwab-si2-08242234-daily-pull
aws events describe-rule --name opal-assets-silver-schwab-sweep-daily</run>
      <expect>Both ENABLED; crons cron(15 10,22 * * ? *) and cron(15 12 * * ? *). Cite verbatim.</expect>
      <if_mismatch>STOP and report — a DISABLED rule on the 49F leg is a P1, this is the fee-basis-full firm.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>30-day invocation evidence for both rules (CloudWatch metrics / invocation logs), denominator printed</run>
      <expect>Expected fire count met (2/day pull), with the trading calendar resolved first for any gap interpretation.</expect>
      <if_mismatch>A missed fire is a finding; a weekend/holiday is NOT. Resolve the calendar before calling any absence a miss.</if_mismatch>
    </step>
    <step>
      <run>aws s3api list-objects-v2 --bucket opal-data-assets --prefix schwab/08242234/silver/fact_rps_s2/ (explicit-Z)</run>
      <expect>Floor date=2024-05-24, frontier date=2026-07-21; zero missing TRADING days in a 30-day census with denominator printed.</expect>
      <if_mismatch>⛔ never bare `aws s3 ls` for a load-bearing time. Report gaps with "N of M expected trading days".</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-run the partition census with denominators printed</run>
      <expect>Unchanged.</expect>
      <if_mismatch>Surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Verification only; no script patched.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="schwab/08242234/silver/fact_rps_s2/" shared_with="0.4.0_DS_ClientPlatform (3F-S2)">
    Shared census surface — reconcile denominators with DS before publishing.
  </resource>
</cross_domain_coordination>

<dependencies><dependency type="none">Independent.</dependency></dependencies>

<acceptance_criteria>
1. 30-day fire evidence for BOTH rules (rule name + state + cron cited verbatim + invocation evidence).
2. A depth statement with vendor citation reconciling the 2024-05-24 silver floor against the gold
   spec's 427-dates-from-2024-11-01.
3. Zero missing TRADING days in a 30-day partition census, denominator printed.
4. Andrew's "good condition on backfill" read explicitly CONFIRMED or REFUTED with evidence.
5. Basis discipline restated in the deliverable: 0824 never summed with and never substituted for 0833.
6. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>Report to 2.0.0_SA_COO. A disabled rule or a mid-series trading-day gap on this leg is P1 — escalate immediately.</escalation>
</task_order>
