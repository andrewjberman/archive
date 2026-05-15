<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.025</id>
    <slug>ae-skipgate</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>active</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED — Wave 3 RAVC2 received (890f8d2fe). Wave 4 dispatched 2026-05-15.</dispatch_unblock_condition>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — Wave 4 incremental architecture enabler; makes ADVI_INFINC Phase 2-6 migrations diagnostic-ready</priority>
    <sla>~2-3 days wall per PRD §15.4 sizing</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-025</ref>
    <ref type="anchor">AE 0.6.1 ADVI_INFINC brief `2920719f8` + DS~D Phase 1 lib `d88b7a7a4` (skip_gate / empty_sentinel / schema_version / partition_provenance)</ref>
    <ref type="upstream_dep">ADVI_INFINC Phase 1 LIB ALREADY SHIPPED. This tool reads the manifests the lib emits.</ref>
    <ref type="cross_link">Wave 4 sibling: .030 stale-marker (related but different concern — markers vs partition-coverage). .032 vectorize-audit also Wave 4.</ref>
  </references>

  <context>
    ADVI_INFINC introduces per-partition skip-gate via `INFINC_PHASE1=1` env-var. Phase 2 migration touches 5 Pattern A scripts (INF_B_00, INF_B_03, INF_A_03, INF_C_00, INF_C_01) + 2 Pattern B scripts (INF_C_02, INF_C_03); each gets opt-in skip behavior.

    Need single-invocation diagnostic showing "for `INF_B_00`, which partitions would skip on next run, which compute" — currently requires manual S3 enumeration of `gold/meta/partition_provenance/{script_id}/{date}.json` + `gold/meta/empty/{script_id}/{date}.empty` + env-var contract reading.

    Tool reads:
    - DS~D's lib manifests (`partition_provenance` + `empty_sentinel`)
    - Env-var contract (INFINC_REBUILD family)
    - Current input-partition S3 listing
    - Cross-references all to produce per-partition skip/compute decision preview
  </context>

  <objective>
    Land `comp-pipescript skipgate <script>` subcommand. Per-partition table showing date / status (SKIP/COMPUTE/MISSING-INPUT) / reason. `--rebuild-window <start>:<end>` preview. `--manifest-fresh-only` filter.
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/comp-pipescript (add `skipgate` subcommand)</file>
      <file action="readonly_reference">data/orion/scripts/gold/lib/skip_gate.py + partition_provenance.py + empty_sentinel.py (DS~D Phase 1 lib)</file>
      <file action="readonly_reference">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-025</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>aws s3 ls s3://opal-data-inf/gold/meta/partition_provenance/ | head -5</run>
      <expect>Manifest directory exists (DS~D Phase 1 ship). Per-script subdirectories appearing as ADVI_INFINC Phase 2 progresses.</expect>
      <if_mismatch>If empty, DS~D Phase 1 lib not yet emitting; verify with DS~D.</if_mismatch>
    </step>
    <step>
      <run>cat data/orion/scripts/gold/lib/skip_gate.py | head -30</run>
      <expect>should_skip signature + helpers per DS~D `d88b7a7a4` — informs tool's manifest-read contract.</expect>
      <if_mismatch>If file missing, fetch from origin.</if_mismatch>
    </step>
    <step>
      <run>aws s3 ls s3://opal-data-inf/gold/canonical/holdings_ | head -5</run>
      <expect>Date-partitioned input-side listing for INF_B_00 readable.</expect>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>comp-pipescript skipgate INF_B_00</run>
      <expect>Per-partition table for ~2,500 date partitions in <30s. Status SKIP if manifest fresh + COMPUTE if missing + MISSING-INPUT if upstream missing.</expect>
      <if_mismatch>STOP. AC1 load-bearing.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript skipgate INF_B_00 --rebuild-window 2026-05-01:2026-05-14</run>
      <expect>In-window partitions flip to COMPUTE; out-of-window remain SKIP.</expect>
    </step>
    <step>
      <run>comp-pipescript skipgate INF_B_00 --manifest-fresh-only</run>
      <expect>Filtered to partitions where input mtime > last skip-gate emit.</expect>
    </step>
    <step>
      <run>Schema-version-mismatch detection: simulate manifest schema_version < current → mark COMPUTE</run>
      <expect>AC3 detection works.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>Test on ≥3 Pattern A scripts (INF_B_00, INF_C_00, INF_C_01)</run>
      <expect>Consistent output structure; no crashes.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `comp-pipescript skipgate INF_B_00` returns per-partition table for ~2,500 date partitions in <30s wall.
    AC2: `--rebuild-window 2026-05-01:2026-05-14` correctly forces COMPUTE on in-window partitions.
    AC3: Schema-version-mismatch detection: skip-gate manifest schema_version < current → mark COMPUTE.
    AC4: `--manifest-fresh-only` filter works.
    AC5: Tested on ≥3 Pattern A scripts.
    AC6: Session log + RAVC2 MCP to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: S3 manifest verify + lib code read + S3 input listing baseline
    Phase 2: skipgate + --rebuild-window + --manifest-fresh-only + schema-mismatch
    Phase 3: ≥3-script cross-test
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: DS~D Phase 1 lib SHIPPED (`d88b7a7a4`) — already done.

    PARALLEL-OK: Wave 4 siblings .030 stale-marker + .032 vectorize-audit.

    DOWNSTREAM CONSUMERS: ADVI_INFINC Phase 2-6 dispatch + RAVC2 — `comp-pipescript skipgate` is the per-phase migration diagnostic gate.

    NO PORTAL CHANGES.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Compiler-tool development; reads from existing manifests + S3.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `comp-pipescript skipgate` subcommand
    2. Per-script invocation demo on ≥3 Pattern A scripts
    3. Session log + RAVC2
  </deliverables>

  <ravc>AE 0.7 RAVC2 to COO on AC1-6 PASS.</ravc>

  <notes>
    **AC1 wall-time (<30s for 2500 partitions)** is load-bearing for usability. If hitting >30s, optimize S3 list batching + manifest parse.

    **ADVI_INFINC Phase 2-6 enablement** — this tool becomes the standard diagnostic for every Pattern A/B/C migration's pre-flight + post-flight verify.

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.
  </notes>
</task_order>
