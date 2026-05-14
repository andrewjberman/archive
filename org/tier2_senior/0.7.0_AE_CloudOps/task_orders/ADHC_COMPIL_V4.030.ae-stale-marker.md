<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.030</id>
    <slug>ae-stale-marker</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>Wave 1+2+3 RAVC2 PASS. AE 0.6.1's ADHC_TRIGMRK standalone TO authoring may absorb related work; coord at dispatch time.</dispatch_unblock_condition>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — Wave 4 incremental architecture enabler; ADHC_TRIGMRK compiler-side companion</priority>
    <sla>~1 day wall per PRD §15.4 sizing</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-030</ref>
    <ref type="anchor_incidents">AE 0.6.1 stale-marker race incidents (chain_full_20260514_141419 + earlier same-day incident). Trigger-marker race banked as 6-candidate corpus signal.</ref>
    <ref type="related">AE 0.6.1 ADHC_TRIGMRK standalone TO (in AE queue post brief expansions) — operational/Lambda+dispatcher fix; THIS TO is the compiler-side diagnostic.</ref>
    <ref type="cross_link">Wave 4 sibling: .025 skipgate + .032 vectorize-audit. Related-but-orthogonal-concern to .025 — markers vs partition-coverage.</ref>
  </references>

  <context>
    S3 markers carry freshness contracts:
    - `gold/meta/empty/{script_id}/{date}.empty` (signal-bounded emit sentinel)
    - `gold/meta/skip-coverage/{script_id}.json` (per-script skip-coverage manifest)
    - `pipeline-complete.json` (chain wrap sentinel)
    - `chain-trigger.json` (chain re-fire marker)
    - `gold/meta/schemas/{script_id}.json` (schema version)
    - `gold/meta/partition_provenance/{script_id}/{date}.json`

    Stale markers cause: (a) skip-gate firing when it shouldn't, (b) chain re-fires on stale sentinels, (c) auto-fired Lambdas overwriting fresh data. Today's stale-marker race incidents at AE 0.6.1's chain operations were empirical anchors.

    Compiler doesn't currently model marker-freshness invariants. `comp-pipescript stale-marker` enumerates every S3 marker path written by gold scripts + every consumer that reads it. Flags asymmetries: writer present, reader absent; reader assumes freshness invariant writer doesn't enforce.
  </context>

  <objective>
    Land `comp-pipescript stale-marker` subcommand. Enumerate marker writer/reader pairs across INF + BD pipelines. Flag freshness-invariant mismatches. `--pipeline inf` pipeline-scoped output.
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/comp-pipescript (add `stale-marker` subcommand)</file>
      <file action="create">org/modules/graph/stale-marker/{pipeline}.yaml (per-pipeline manifest-pair map)</file>
      <file action="readonly_reference">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-030</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>grep -rn "gold/meta/\|pipeline-complete\.json\|chain-trigger\.json" data/orion/scripts/gold/ | head -20</run>
      <expect>≥5 marker writer/reader call sites enumerated.</expect>
      <if_mismatch>If 0 hits, marker pattern not yet shipped; verify.</if_mismatch>
    </step>
    <step>
      <run>aws s3 ls s3://opal-data-inf/gold/meta/ | head -10</run>
      <expect>Marker directories exist; manifest-pair baseline established.</expect>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>comp-pipescript stale-marker</run>
      <expect>≥5 marker invariant pairs enumerated. Flag any writer-reader asymmetry.</expect>
      <if_mismatch>STOP. AC1 load-bearing.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript stale-marker --pipeline inf</run>
      <expect>Pipeline-scoped output: only INF-side markers.</expect>
    </step>
    <step>
      <run>Validate against AE 0.6.1's stale-marker race incidents</run>
      <expect>Tool flags the marker pair(s) that raced.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>Run on BD pipeline scope</run>
      <expect>No crashes; BD-specific markers enumerated.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Detects 5+ marker invariant pairs in INF chain (skip-coverage, empty-sentinel, pipeline-complete, chain-trigger, schema-version).
    AC2: Flags AE 0.6.1's prior stale-marker race incidents post-hoc (validation against real corpus).
    AC3: `--pipeline inf` and `--pipeline bd` modes both functional.
    AC4: Per-pipeline yaml manifest persisted.
    AC5: Session log + RAVC2 MCP to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: marker writer/reader grep + S3 manifest verify
    Phase 2: stale-marker + --pipeline modes + retroactive validation on AE race incidents
    Phase 3: cross-pipeline (BD) test
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: Wave 1+2+3 RAVC2.

    COORDINATES WITH: AE 0.6.1's ADHC_TRIGMRK TO (operational/Lambda+dispatcher fix). This compiler-side tool is the structural-diagnostic companion. Coord at dispatch time on overlap.

    NO PORTAL CHANGES.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Compiler-tool development.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `comp-pipescript stale-marker` subcommand
    2. Per-pipeline yaml manifests
    3. Retroactive validation on AE 0.6.1 race incidents
    4. Session log + RAVC2
  </deliverables>

  <ravc>AE 0.7 RAVC2 to COO on AC1-5 PASS.</ravc>

  <notes>
    **Coord with AE 0.6.1's ADHC_TRIGMRK:** their fix is operational (Lambda + dispatcher checks); this is diagnostic. Complementary not duplicate. Coord at ship time.

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.
  </notes>
</task_order>
