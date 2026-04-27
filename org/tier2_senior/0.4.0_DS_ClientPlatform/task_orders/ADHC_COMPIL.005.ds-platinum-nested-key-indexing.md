<task_order>
  <metadata>
    <id>ADHC_COMPIL.005.ds-platinum-nested-key-indexing</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>staged</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>D (v2)</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V2.md §2 (commit 653b0469)</prd_ref>
    <effort>2–3 weeks</effort>
    <gates_on>ADHC_COMPIL.001 COMPLETE — multi-pipeline indexing foundation required before
    nested-key reverse-lookup across BD + INF + silver corpora is reliable</gates_on>
    <same_owner_as>ADHC_COMPIL.001 — shared graph builder codebase</same_owner_as>
  </metadata>

  <objective>
    Extend comp-platinum reverse to support nested key paths, wildcard segments,
    and dynamic parameterized keys. Currently returns EMPTY for any nested or
    dynamic key — operators fall back to manual portal grep.

    Real incident: ADVI_ROLLUP.RF01 TO authoring — COO ran
    comp-platinum reverse rfs.decomposition_max.nna → EMPTY
    comp-platinum reverse rfs.decomposition_ytd.nna → EMPTY
    Both returned nothing; COO had to manually grep portal source for consumers.
  </objective>

  <scope>
    Extend comp-platinum reverse to support:

    1. Nested key paths
       comp-platinum reverse rfs.decomposition_max.nna
       → resolves to portal hooks/components reading data?.rfs?.decomposition_max?.nna
       (or any equivalent JSON path access in consumer code)

    2. Wildcard segments
       comp-platinum reverse rfs.decomposition_*.nna
       → returns union of consumers across all matched paths
       (decomposition_max, decomposition_ytd, etc.)

    3. Dynamic keys with parameter substitution
       comp-platinum reverse role_aua.{role}.total
       → returns consumers parametrized over role with documentation note
       clarifying wildcard semantics

    Implementation approach (from PRD §2.3):
    - Graph builder already parses portal source for useQuery/useFetch calls
      and component data accesses.
    - Extend JSON-path parser to walk dot-paths into the artifact's known shape
      (sourced from the producer script's emit format).
    - Tag each access with its full JSON path.
    - Support wildcard matching at query time.
    - Producer-side: gold scripts emitting nested-shape artifacts must be
      parsed for their emit shape. Requires Theme A (multi-pipeline) as
      foundation — do NOT start before .001 is complete.
  </scope>

  <acceptance_criteria>
    1. comp-platinum reverse rfs.decomposition_max.nna returns ≥1 consumer.
       EMPTY result is a FAIL.
    2. comp-platinum reverse rfs.decomposition_*.nna returns the union of consumers
       across both decomposition_max and decomposition_ytd path matches.
    3. comp-platinum reverse role_aua.{role}.total returns consumers parametrized
       over role. Output includes documentation note on wildcard semantics.
    4. Existing flat-key behavior unchanged:
       comp-platinum reverse header_metrics.json → same output as today (no regression).
    5. ≥3 new test fixtures:
       - Nested key (rfs.decomposition_max.nna)
       - Wildcard key (rfs.decomposition_*.nna)
       - Dynamic key (role_aua.{role}.total)
       All 3 must FAIL against current implementation and PASS against new.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT start before ADHC_COMPIL.001 is complete — cross-pipeline artifact
    identity is required for reliable nested-key consumer enumeration.</rule>
    <rule>Do NOT change flat-key comp-platinum reverse behavior — additive only.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">Extended comp-platinum reverse with nested/wildcard/dynamic key support</deliverable>
    <deliverable type="code">≥3 new test fixtures</deliverable>
    <deliverable type="document">Session log with AC verification runs</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC outputs + fixture pass evidence</deliverable>
  </deliverables>
</task_order>
