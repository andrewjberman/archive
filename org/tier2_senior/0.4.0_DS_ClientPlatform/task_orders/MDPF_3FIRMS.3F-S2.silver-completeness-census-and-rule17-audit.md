<task_order>
<id>MDPF_3FIRMS.3F-S2</id>
<title>Silver completeness census (denominators enumerated at run time) + Rule-17 compliance audit on the six MDPF-feeding fact tables</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-S (Silver)</workstream>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:24Z</issued_at>
<status>staged</status>
<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z -> COO decomposition.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §4 WS-S row 3F-S2; §3.2 layer contracts; §8.5</ref>
</references>

<scope>
(a) **COMPLETENESS CENSUS**: silver partition census vs bronze census, per table, for the six
    MDPF-feeding fact tables. **DENOMINATORS ENUMERATED AT RUN TIME**, never hardcoded, never inherited
    from a prior run. Convert any missing partitions via the sanctioned sweep.
(b) **RULE-17 COMPLIANCE AUDIT** on the same six tables.

**RULE 17, EXACTLY:** silver is **dedup + dtype standardization ONLY**. **NEVER** field-slimming,
**NEVER** fillna/dropna, **NEVER** business-row-filtering, **NEVER** dropping bronze columns. Anything
requiring judgment about field relevance or null meaning is GOLD-tier business logic. Legacy violators
migrate to passthrough on next touch — but **finding and itemizing them is this TO; migrating them is
not**, unless the migration is trivially passthrough.

**The six MDPF-feeding tables:** `schwab/08242234/silver/fact_rps_s2`,
`smartx/platform/silver/fact_model_aum_daily`, `orion/inflection/silver/fact_assets`,
`eclipse/inflection/silver/fact_portfolios_full`, `blackdiamond/cottonwood/silver/fact_holdings_s2`,
`blackdiamond/cottonwood/silver/fact_model_assignment`.

⚠ **STATE THE COVERAGE DENOMINATOR OF EVERY CENSUS.** "Which of the partitions does my evidence cover?"
precedes any completeness claim. A sweep that cannot find a known-present instance is a BROKEN
INSTRUMENT reporting silence — include a positive control per table.
⚠ **ENUMERATE WHAT A NUMBER IS *OF* BEFORE EXPLAINING WHY IT DIFFERS.** "Which bucket/axis?" precedes
"which vintage?" A rigorous instrument on the wrong axis survives review.
⚠ **A missing partition is only missing against the TRADING CALENDAR.** Resolve weekends + market
holidays FIRST (NEVER#1). Cottonwood additionally carries a D+1 delivery cadence (3F-B5) — a D+1 lag is
the contract, not a gap.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io on every silver converter in scope</run>
      <expect>READS/WRITES enumerated; COLUMN GAPS empty.</expect>
      <if_mismatch>Non-empty COLUMN GAPS = fix the load list first. ⚠ KNOWN GAP (filed to CTO): `comp-pipescript io` does not surface cross-bucket served imports inside helper functions — a clean manifest is not proof of no coupling. Read the source.</if_mismatch>
    </step>
    <step>
      <run>comp-freshness</run>
      <expect>All six legs resolve on freshness_basis: trading-day-frontier.</expect>
      <if_mismatch>Record any flat-hours entry as a gap; never raise staleness off it (NEVER#1).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Per-table bronze-vs-silver partition census, denominators enumerated AT RUN TIME, with a per-table POSITIVE CONTROL</run>
      <expect>For each table: "N of M expected partitions present", M derived from the trading calendar + the leg's delivery cadence. Control finds a known-present partition.</expect>
      <if_mismatch>If a control fails to find a known-present partition, the instrument is broken — fix the instrument before reporting any census result.</if_mismatch>
    </step>
    <step>
      <run>Rule-17 audit: inspect each converter for slimming / fillna / dropna / row-filtering / dropped bronze columns</run>
      <expect>A violation list — EMPTY or ITEMIZED with file:line @ commit-ish.</expect>
      <if_mismatch>An assertion of compliance without per-file evidence does not satisfy this. Cite or do not claim.</if_mismatch>
    </step>
    <step>
      <run>.tools/commit-gate.sh on any .py touched</run>
      <expect>Clean; `from __future__ import annotations` present.</expect>
      <if_mismatch>STOP.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-run the census with denominators printed</run>
      <expect>0 unexplained missing partitions per table; every remaining absence has a named cause (weekend / holiday / D+1 cadence / vendor gap).</expect>
      <if_mismatch>Surface to COO with the per-table denominator.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <reprocess_required>
    Missing-partition conversion IS a reprocess. Convert only via the sanctioned sweep path — ⛔ no
    ad-hoc gold runs, no hand-fired producers. Verify post-ingest partition mtimes via `s3api`
    (explicit-Z) exceed the sweep time. Notify 0.6.2 (3F-S1) if a reprocess overlaps his regex-fix
    reprocess so the two do not race the same objects.
  </reprocess_required>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="all six silver fact tables" shared_with="0.6.2_AE_PartnerETL~A (3F-B1/B3/B4/B5/S1)">
    0.6.2 runs leg-level censuses on the same tables and a regex-fix reprocess that CHANGES YOUR
    DENOMINATORS. Reconcile before publishing — two conflicting censuses on one surface is worse than
    one late census.
  </resource>
  <resource path="fact_holdings vs fact_holdings_s2" shared_with="0.7.0_AE_CloudOps + DS (3F-S3)">
    Which is canonical for the Cottonwood AUA total is an OPEN S4 determination (3F-S3) — do not resolve
    it silently inside this census.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency agent="0.6.2_AE_PartnerETL~A" task="MDPF_3FIRMS.3F-S1" status="staged" blocking="false">
    His regex reprocess changes denominators; sequence or re-run after.
  </dependency>
</dependencies>

<acceptance_criteria>
1. Per-table census committed with **denominators printed and enumerated at run time**, plus a per-table
   positive control that could have failed.
2. **0 unexplained missing partitions per table** — every absence carries a named cause.
3. A Rule-17 violation list: empty, or itemized with `file:line @ commit-ish`.
4. Any reprocess executed via the sanctioned sweep only, with post-ingest mtimes verified.
5. The trading calendar is resolved before any partition is called missing (NEVER#1).
6. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>Report to 2.0.0_SA_COO. Escalate any Rule-17 violation that involves fillna/dropna on a served-number path — that is silent-wrongness class.</escalation>
</task_order>
