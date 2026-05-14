<task_order>
  <metadata>
    <id>ADVI_INFINC.001</id>
    <slug>dsd-skip-gate-lib</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <redirect_history>Originally issued to DS~A 2026-05-14 13:55Z; redirected to DS~D 2026-05-14 14:00Z per Andrew direct ("DS~A midstream on more important priorities, this should be redirected to DS~C and DS~D"). DS~A stood down before code shipped. Phase 1 ownership lock: DS~D. Phase 2-6 split across DS~C + DS~D per Andrew direct.</redirect_history>
    <coordinates_with>0.6.1_AE_PartnerETL (dispatch.sh flag plumbing review + integration)</coordinates_with>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFINC</project_code>
    <priority>P1 — Phase 1 foundation; gates all Phase 2-5 per-script migrations</priority>
    <sla>~3 days wall (per AE 0.6.1 brief §5.1 sizing)</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inf-incremental-pipeline-design-20260514.md §5.1 Phase 1 + §2 architectural patterns + §4 risks + §6 open questions</ref>
    <ref type="project_json">org/projects/ADVI_INFINC.json</ref>
    <ref type="authority">Andrew direct ASK 2026-05-14 during live chain_full_20260514_131842: "make a truly incremental version of this flow rather than having to rebuild 7 years of history every single day, analyze every script in detail and write a comprehensive brief for implementation to send to COO for distribution to DS~A and DS~B." Routed via AE 0.6.1 brief 2920719f8.</ref>
    <ref type="ae_partner">0.6.1_AE_PartnerETL — co-owner of dispatch.sh flag plumbing integration; will review lib design + handle dispatch.sh edits per brief §7 AE responsibilities</ref>
  </references>

  <context>
    Foundational lib + dispatch.sh flag plumbing for the INF Incremental migration. **No production script behavior changes in this TO** — just the gate infrastructure. Subsequent phases (Phase 2 Pattern A, Phase 3 Pattern B, Phase 4 Pattern C, Phase 5 Pattern E) consume the lib to migrate individual scripts.

    **Empirical context (brief §1):** chain currently ~70 min daily; ~35-40 min waste from re-walking ~1,750 historical date partitions in B_00/B_03/C_00/C_01/A_03 + similar history-replay in D_06/D_09 + unconditional full-pull in PULL_TXN/PULL_PERF. Past partitions are deterministic functions of frozen silver inputs — rewriting them daily is pure waste.

    **The skip-gate is per-partition gating INSIDE each script's main loop** (brief Appendix B), distinct from the existing dispatch.sh `--skip-existing` per-script-execution flag. Complementary, not replacement.

    **Phase 1 deliverables per brief §5.1:**
    1. `data/orion/scripts/gold/lib/skip_gate.py` — `should_skip(script_id, partition_date, output_key, silver_input_keys)` function returning bool; reads `head_object` on output_key + each silver_input_key, compares mtime + schema version; returns False if output missing OR silver newer OR schema bump OR `--rebuild` set.
    2. `data/orion/scripts/gold/lib/empty_sentinel.py` — `mark_empty(script_id, date)` + `is_empty(script_id, date)` for signal-bounded emit (brief §4.2; preserves ADHC_DSFLOW pattern).
    3. Schema-version manifest: `gold/meta/schemas/{script_id}.json` — opt-in per-script schema version stamp; bumps documented in commit message (brief Q3 disposition: DS judgment per-script).
    4. Partition provenance: `gold/meta/partition_provenance/{script_id}/{date}.json` storage layout (brief Q4 disposition: per-partition per AE recommendation; ~1,750 small JSON × ~200 bytes = 350KB total, negligible).
    5. dispatch.sh flag plumbing: `--rebuild`, `--rebuild-start-date`, `--rebuild-end-date` wired through dispatch.sh; coord with AE 0.6.1 (brief §7).
  </context>

  <objective>
    Land Phase 1 skip-gate infrastructure: lib functions + empty-sentinel + schema-version manifest scaffolding + partition-provenance scaffolding + dispatch.sh flag plumbing. Foundational; no production script touches; reversible per-script via env flag (Phase 2+ scripts opt in to consume the lib).
  </objective>

  <scope>
    <files>
      <file action="create">data/orion/scripts/gold/lib/skip_gate.py — should_skip() + helpers</file>
      <file action="create">data/orion/scripts/gold/lib/empty_sentinel.py — mark_empty() + is_empty()</file>
      <file action="create">data/orion/scripts/gold/lib/schema_version.py (or fold into skip_gate.py — DS judgment) — schema-version stamp helpers</file>
      <file action="modify">.tools/orion-gold-dispatch.sh OR data/orion/scripts/gold/dispatch.sh (DS+AE coord per brief §7) — `--rebuild` / `--rebuild-start-date` / `--rebuild-end-date` flags plumbed through; AE 0.6.1 reviews/integrates</file>
      <file action="readonly_reference">docs/briefs/inf-incremental-pipeline-design-20260514.md §2-§5 verbatim</file>
    </files>
  </scope>

  <phase id="0" when="before write — design alignment">
    <step>
      <run>Read brief §2 architectural patterns end-to-end + §5.1 Phase 1 deliverable list</run>
      <expect>Lib signature aligned with Pattern A/B/C/D/E consumers from brief §2.</expect>
      <if_mismatch>If brief reads ambiguously on a design point, MCP AE 0.6.1 (brief author) for clarification BEFORE writing code. Better to spend 5min coord than ship a signature that requires rewrites in Phase 2.</if_mismatch>
    </step>
    <step>
      <run>Skim brief §6 open questions Q3 + Q4 + corresponding §4 risks</run>
      <expect>Q3 (schema version stamping) handled as opt-in per-script (DS judgment per AE recommendation). Q4 (partition_provenance.json layout) per-partition file (AE recommendation; ~350KB total; negligible storage cost; forensic clarity).</expect>
      <if_mismatch>If you have strong evidence-based reason to deviate from AE recommendations on Q3 or Q4, surface to COO with rationale BEFORE writing.</if_mismatch>
    </step>
    <step>
      <run>Coord MCP to AE 0.6.1 on dispatch.sh flag-plumbing approach — fold into your edits OR you author the flag-plumbing scaffolding and AE integrates into dispatch.sh as a follow-on PR</run>
      <expect>Clear ownership boundary between your lib edit + AE's dispatch.sh edit. Brief §7 puts dispatch.sh in AE lane; recommend you author flag-receiver code + AE owns dispatch.sh integration call-sites.</expect>
    </step>
  </phase>

  <phase id="1" when="before write — compiler discovery">
    <step>
      <run>ds-commit-gate.sh dry-run on a stub skip_gate.py (`python -m py_compile` + ds-precommit-check.py + ruff target=py39)</run>
      <expect>Three gates pass on stub. Confirms environment + ds-commit-gate pipeline works pre-write.</expect>
      <if_mismatch>Fix gate failures before writing real lib. Per CLAUDE.md Rule 14.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io INF_B_00 + comp-pipescript io INF_C_00 + comp-pipescript io INF_C_01</run>
      <expect>Read each Phase 2 consumer's I/O surface to confirm `should_skip` signature handles the consumer call-sites cleanly. Specifically: silver_input_keys parameter shape across the 3 worst-offender Pattern A scripts.</expect>
      <if_mismatch>Adjust signature pre-write rather than refactor in Phase 2.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>ds-commit-gate.sh on the 3 new lib files + the schema-version manifest scaffolding + the dispatch.sh edit (or stub if AE owns)</run>
      <expect>Three gates pass: py_compile + ds-precommit-check.py (incl. CLAUDE.md Rule 15 `from __future__ import annotations` first import) + ruff py39 0.15.11.</expect>
      <if_mismatch>STOP. Per CLAUDE.md Rule 14 ds-commit-gate is mandatory pre-commit gate.</if_mismatch>
    </step>
    <step>
      <run>Stub-test the lib: import + call should_skip() on a known-existing partition + assert returns True; call on a known-missing partition + assert returns False; call with --rebuild flag set + assert returns False (force-rebuild). All in a `test_skip_gate.py` under `data/orion/scripts/gold/lib/tests/`.</run>
      <expect>All stub-tests pass. Confirms the lib semantics before any production script consumes it.</expect>
      <if_mismatch>Fix lib semantics; do not commit broken foundation.</if_mismatch>
    </step>
    <step>
      <run>aws s3 head-object spot-check on `s3://opal-data-inf/code/gold/lib/skip_gate.py` post-safe-deploy.sh</run>
      <expect>S3 mirror matches commit SHA via comp-pipescript deployed gate.</expect>
      <if_mismatch>safe-deploy.sh failure; investigate before RAVC2.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>Smoke: invoke a no-op chain run via dispatch.sh with new flags (`--rebuild --rebuild-start-date 9999-12-31 --rebuild-end-date 9999-12-31`) to exercise flag parsing without actually rebuilding anything (out-of-range date → no work)</run>
      <expect>dispatch.sh accepts the flags + propagates to script invocations + scripts ignore (lib not yet consumed by any production script in Phase 1).</expect>
      <if_mismatch>Flag-plumbing bug; coord with AE 0.6.1 before declaring Phase 1 complete.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `lib/skip_gate.py` shipped with `should_skip()` + helpers; stub-tests pass; ds-commit-gate.sh pass.
    AC2: `lib/empty_sentinel.py` shipped with `mark_empty()` + `is_empty()`; stub-tests pass.
    AC3: Schema-version manifest scaffolding: `gold/meta/schemas/{script_id}.json` layout documented + helper to read/write versions; opt-in per-script bump per AE recommendation (brief Q3).
    AC4: Partition-provenance layout: `gold/meta/partition_provenance/{script_id}/{date}.json` per-partition file; helper to write provenance on partition emit; per AE recommendation (brief Q4).
    AC5: dispatch.sh flag plumbing: `--rebuild`, `--rebuild-start-date`, `--rebuild-end-date` accepted + propagated to script invocations. Coord with AE 0.6.1 on integration boundary.
    AC6: No production script touched. Foundational only.
    AC7: All new lib files start with `from __future__ import annotations` per CLAUDE.md Rule 15.
    AC8: safe-deploy.sh + comp-pipescript deployed MATCH on all new lib files.
    AC9: Session log Compiler Tools section reproduces every Phase 0/1/2/3 `<run>` with observed result + pass/fail vs. `<expect>`.
    AC10: MCP RAVC2 to COO with commit hash + AE 0.6.1 CC for dispatch.sh integration sign-off.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phases above. Auto-rule 4 trigger inverse: this TO touches `data/orion/scripts/gold/lib/**` which is silver/bronze-adjacent infrastructure — no data reprocess scope, but `comp-pipescript io` on the 3 worst-offender Phase 2 consumers (INF_B_00 / INF_C_00 / INF_C_01) at Phase 1 confirms signature alignment.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: none — foundational.

    COORD:
    - AE 0.6.1 owns dispatch.sh flag plumbing per brief §7. DS~D authors flag-receiver lib + AE integrates into dispatch.sh. Joint RAVC.
    - CTO routing on Q1 (advisor attribution lag) + Q5 (DIAGFIX banner) + Q6 (validation epsilon budget) — these inform Phase 2+ design, not Phase 1; CTO answers should land during Phase 1 wall-clock (~3d) so Phase 2 dispatch isn't blocked.
    - DS~B routing on Q2 (Orion backdate distribution empirical probe) — informs Phase 5 (PULL_TXN/PULL_PERF). Q2 doesn't block Phase 1.

    DOWNSTREAM BLOCKING: Phase 2 (.002+) per-script migrations consume `should_skip()` lib + assume schema-version manifest + partition-provenance layout. Phase 2 TOs gate on Phase 1 RAVC2 + chain #30 mode=full wrap clean (DS~A's INF_D_00c fix `fd11a33c2` production-proven).

    PARALLEL-OK: Phase 2 design discussion can begin during Phase 1 wall-clock; no code changes outside Phase 1 scope.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Phase 1 is foundational lib + dispatch.sh flag plumbing. No production script touched; no silver/bronze re-emit; no Lambda redeploy; no chain re-fire. Phase 2+ migrations will require explicit reprocess scope per script (Pattern A: existing partitions stay; new partitions go through skip-gate. Pattern B: existing blob assembled from full re-walk once, then append-only).
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `lib/skip_gate.py` + tests
    2. `lib/empty_sentinel.py` + tests
    3. Schema-version manifest scaffolding (`gold/meta/schemas/` layout + helpers)
    4. Partition-provenance scaffolding (`gold/meta/partition_provenance/` layout + helpers)
    5. dispatch.sh flag plumbing (`--rebuild` family; coord with AE 0.6.1)
    6. safe-deploy.sh + S3 MATCH evidence
    7. Session log with Compiler Tools section
    8. MCP RAVC2 to COO + AE 0.6.1 CC
  </deliverables>

  <ravc>
    DS~D RAVC2 to COO + CC AE 0.6.1 on AC1-10 PASS. COO ratifies + AE 0.6.1 confirms dispatch.sh integration sign-off. Phase 2 (.002 INF_B_00 + sibling Pattern A scripts) dispatch authorized post-RAVC2 + post chain #30 mode=full wrap clean.
  </ravc>

  <notes>
    **Phase sequencing context:** Phase 2 (~5d DS~B per AE brief §5.2) authoring begins immediately after Phase 1 RAVC2. Phase 2 ships 5 PRs serially (INF_B_00 → INF_B_03 → INF_C_00 → INF_C_01 → INF_A_03). Phase 3+4+5+6 follow per AE brief §5.

    **Q3/Q4 design decisions absorbed:** per AE recommendation. If DS~D surfaces evidence-based deviation rationale, surface to COO BEFORE writing; don't litigate post-hoc.

    **Q1/Q5/Q6 routed to CTO** in parallel; CTO answers should land during Phase 1 wall-clock so Phase 2 architectural design isn't blocked. If CTO is delayed >Phase 1 wall-clock, Phase 1 still ships standalone and Phase 2 design absorbs CTO answers when they arrive.

    **Q2 routed to DS~B** for empirical Orion backdate distribution probe. Informs Phase 5 (PULL_TXN/PULL_PERF window size); not blocking Phase 1.

    **Author identity:** `--author="0.4.0_DS_ClientPlatform~D <0.4.0_DS_ClientPlatform~D@opal.agent>"` per protocol (lane updated post-redirect 2026-05-14 14:00Z).

    **Compiler context update:**
    ```
    SERIAL=0.4.0_DS_ClientPlatform~D
    TO_ID=ADVI_INFINC.001
    ```
  </notes>
</task_order>
