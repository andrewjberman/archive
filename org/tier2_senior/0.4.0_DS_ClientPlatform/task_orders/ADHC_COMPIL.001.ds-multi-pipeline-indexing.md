<task_order>
  <metadata>
    <id>ADHC_COMPIL.001.ds-multi-pipeline-indexing</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>A</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL.md §4 (commit 172470a8)</prd_ref>
    <effort>3–4 weeks</effort>
    <gates_on>None — parallelizable with ADHC_COMPIL.002 and .003</gates_on>
    <gates_for>ADHC_COMPIL.005 (Theme D nested-key indexing)</gates_for>
  </metadata>

  <objective>
    Extend comp-pipescript (and the underlying graph builder) to index the
    Inflection gold corpus, BD silver, INF silver, and bronze layers.
    Currently comp-pipescript only indexes BD gold scripts — operators cannot
    run comp-pipescript io/deployed/postdeps against any INF script or any
    silver/bronze script. This is the foundational gap that blocked ADVI_RDVSDS
    root-cause analysis and blocks Theme D (comp-platinum reverse nested keys).
  </objective>

  <scope>
    Extend comp-pipescript graph indexing to cover:

    1. INF gold scripts: data/orion/scripts/gold/
       Full corpus: D_00c, D_02, D_04, I_D00, I_D00b, I_D03, I_09, and all
       I_A*, I_B*, I_C*, I_D* files. Post-ORNREN.001 naming (A_*/B_*/C_*/D_*/09
       convention).

    2. BD silver scripts: data/black_diamond/scripts/silver/ (full set)

    3. INF silver scripts: data/orion/scripts/silver/
       (convert_orion_to_silver.py and any siblings)

    4. Bronze layer: index when scripts exist. Currently empty for INF —
       index the directory, emit no nodes if empty, ready for future addition.

    Required operations on any indexed script:
    - comp-pipescript io <script>  → READS / WRITES / FUNC-key writes
    - comp-pipescript deployed <script>  → MATCH/STALE/MISSING vs appropriate EC2
      - INF gold: inf-gold-layer-runner (i-0ed5afded2ebd4ed4)
      - BD silver: bd-silver-runner (check EC2_MANIFEST.json for correct ID)
    - comp-pipescript postdeps <script>  → downstream chain steps
    - comp-blast <script or artifact>  → cross-layer, cross-pipeline impact

    Cross-pipeline edges: a silver script writing s3://opal-data-inf/silver/transactions/
    must appear as a producer for any INF gold script reading that prefix.

    Pipeline labeling: all comp-pipescript io and comp-blast output must label
    nodes with their pipeline. Format: [bd-gold], [bd-silver], [inf-gold],
    [inf-silver], [bronze]. A BD gold change must not silently affect INF
    impact analysis.

    Implementation note: INF scripts hardcode S3_BUCKET = 'opal-data-inf'
    (not imported from lib.config like BD). The AST walker must handle both
    patterns. Check ORNREN.001 commit 889acba2 for renamed file list and any
    dispatch-script CATALOG references that may inform the graph seed.
  </scope>

  <acceptance_criteria>
    1. comp-pipescript io data/orion/scripts/gold/D_04.client_portal_summary.py
       returns READS / WRITES / FUNC-key writes in same shape as BD equivalent.
    2. comp-pipescript io data/black_diamond/scripts/silver/<any>.py returns
       silver script READS + WRITES.
    3. comp-blast canonical_lots_realized_key (BD) and comp-blast leaderboard.json
       (INF) both return downstream consumers correctly, with pipeline labels.
    4. Pipeline labeling ([bd-gold], [inf-gold], etc.) visible in comp-pipescript io
       and comp-blast output.
    5. comp-pipescript deployed <any INF gold script> returns MATCH/STALE/MISSING
       against inf-gold-layer-runner EC2.
    6. Existing BD-gold behavior unchanged — no regressions on 75+ existing tests.
    7. ≥5 new test fixtures covering:
       - INF gold script (io + READS/WRITES)
       - BD silver script (io)
       - INF silver script (io)
       - Cross-pipeline edge (silver producer → gold consumer)
       - Pipeline labeling correctness
       All 5 must FAIL against current implementation and PASS against new.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT modify existing BD-gold indexing behavior — additive only.</rule>
    <rule>Do NOT hardcode INF EC2 instance ID — read from EC2_MANIFEST.json.</rule>
    <rule>Do NOT skip the pipeline-label requirement — unlabeled output breaks
    cross-pipeline blast analysis.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">Extended graph builder with INF gold + BD/INF silver + bronze indexing</deliverable>
    <deliverable type="code">≥5 new test fixtures</deliverable>
    <deliverable type="document">Session log with AC verification runs</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC exit codes, sample
    io output for INF gold + BD silver, cross-pipeline blast sample</deliverable>
  </deliverables>
</task_order>
