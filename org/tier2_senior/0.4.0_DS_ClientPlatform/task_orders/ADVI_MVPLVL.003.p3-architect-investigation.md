```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-13-p3-architect-investigation</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-13</date>
    <status>pending</status>
    <thread_serial>ADVI_MVPLVL-003</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-003-p3-advisors-tab-alignment/</thread_ref>
  </metadata>

  <objective>
    Investigate portfolio_group and architect data quality in the gold layer to
    determine whether the Advisors Tab can support a group-by hierarchy (Portfolio
    Group -> Architect -> Implementor) or must remain flat. Produce a written
    artifact with findings and a recommendation.

    Background: 49 Financial has 53 architect entries but likely fewer than 15 true
    architects. The thread confirmed portfolio_group is raw/unnormalized free-text
    from transaction data. This investigation resolves whether it can be cleaned or
    if an alternative grouping dimension is needed.
  </objective>

  <scope>
    <files>
      <file action="read">data/black_diamond/scripts/gold/00_build_accounts_dimension.py</file>
      <file action="read">data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Portfolio group field analysis. Query gold/accounts_dimension_latest.parquet:
      - Distinct portfolio_group values + counts (all, not just top 10)
      - Null/blank rate
      - Qualitative assessment: do values look like teams/offices or person names?
    </requirement>

    <requirement id="2">
      Architect AUA distribution. Query gold/views/nna_aua_by_advisor.parquet (latest date):
      - Top 20 architects by AUA with dollar amounts
      - Count of architects above $25M, $10M, $5M thresholds
      - Long tail analysis: how many architects have material AUA vs negligible
    </requirement>

    <requirement id="3">
      Portfolio group to architect alignment. For each architect:
      - What portfolio_group(s) do their accounts fall into?
      - Concentration metric: % of accounts in their top portfolio_group
      - Does portfolio_group behave like a stable team assignment or is it many-to-many?
    </requirement>

    <requirement id="4">
      Recommendation. Based on findings:
      - If portfolio_group is clean: recommend it as the default group-by dimension
        and specify any cleanup needed (normalize nulls, merge duplicates, etc.)
      - If portfolio_group is noisy: propose an alternative grouping dimension from
        accounts_dimension (local_relationship, manager, or a curated mapping table)
      - Provide a concrete "is_true_architect" filtering recommendation (AUA threshold +
        account count + activity recency)
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Written artifact produced with all 4 requirement sections answered</criterion>
    <criterion id="2">Portfolio group cardinality + examples documented</criterion>
    <criterion id="3">Architect AUA distribution documented with thresholds</criterion>
    <criterion id="4">Clear recommendation: group-by dimension + true architect filter</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This is a research/investigation task — no code changes to gold scripts</constraint>
    <constraint>Queries require reading actual parquet data from S3 — use Python + pandas locally or on EC2</constraint>
    <constraint>Deliverable is a written artifact (session log or brief), not code</constraint>
  </constraints>

  <references>
    <ref type="prd">docs/architecture/ADVI_MVPLVL_PRD.md (Part 3, item 3a)</ref>
    <ref type="thread">org/threads/ADVI_MVPLVL-003-p3-advisors-tab-alignment/</ref>
  </references>

  <deliverables>
    <deliverable type="document">DS session log or brief with portfolio_group analysis, architect AUA distribution, alignment metric, and grouping recommendation</deliverable>
  </deliverables>
</task_order>
```
