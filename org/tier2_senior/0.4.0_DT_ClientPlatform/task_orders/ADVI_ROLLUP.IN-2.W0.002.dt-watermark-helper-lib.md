<task_order>
  <metadata>
    <id>ADVI_ROLLUP.IN-2.W0.002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>7 — IN (Incremental runs) Wave 0 Foundation</wave>
    <priority>P1 (foundational — all future IN waves consume this helper lib)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/INCREMENTAL_RUNS_DESIGN.md §3 (watermark contract) + §4 (atomic write rule) + §7 Wave 0</ref>
    <ref type="prd_commit">916a3a4f</ref>
    <ref type="parent_analysis">docs/analysis/2026-04-15_incremental_runs_feasibility.md (IN-1, commit 196e8e53)</ref>
  </references>

  <objective>
    Ship the two helper modules that every IN Wave 1-5 per-script conversion will consume:

    **Module 1: `data/black_diamond/scripts/gold/_lib/watermark.py`** — single-writer-pattern per PRD §3.

    API:
    ```python
    def load_watermark(script_id: str) -> Watermark | None: ...
    def save_watermark(script_id: str, **fields) -> None: ...
    def upstream_changed(script_id: str, my_inputs: list[str]) -> bool: ...
    ```

    Watermark schema per PRD §3:
    - `script_id`, `max_partition_date`, `max_input_ingest_ts`, `computed_at`
    - `input_hashes`: dict of upstream_script_id → sha256 of that upstream's watermark JSON (transitive close)
    - `run_mode`: "full" | "incremental"
    - `skipped`: bool
    - `rebuild_reason`: null | "weekly_parity_check" | "manual_full_chain" | "input_hash_mismatch" | "first_run_post_promotion"

    Storage: `s3://opal-data-bd/gold/meta/{script_id}_watermark.json` — one file per script.

    `upstream_changed()` returns True if any of `my_inputs` (list of upstream script_ids) has a watermark with a hash different from what our own last watermark recorded. Cheap transitive-close hash compare.

    **Module 2: `data/black_diamond/scripts/gold/_lib/atomic_write.py`** — atomic write rule per PRD §4.

    API:
    ```python
    def atomic_s3_write(bucket: str, key: str, body: bytes | str) -> None:
        """Write to {key}.staging then atomic rename to final. Prevents partial-state visibility."""
    ```

    **Migration compat:** read old `CANONICAL_HOLDINGS_WATERMARK` + `CLIENT_TIMESERIES_WATERMARK` formats for one transition cycle (emit deprecation warning on read). Writes always use new format. Old formats removed in Wave 5 cleanup.

    **Unit tests (mandatory):**
    - `load_watermark` on missing file returns None.
    - `save_watermark` round-trips all fields.
    - `upstream_changed` returns False when all upstream hashes match; True when any differ.
    - `atomic_s3_write` uses `.staging` intermediate (mock S3).
    - Old-format readers for CANONICAL_HOLDINGS_WATERMARK + CLIENT_TIMESERIES_WATERMARK return valid Watermark objects.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/gold/_lib/__init__.py</file>
      <file action="create">data/black_diamond/scripts/gold/_lib/watermark.py</file>
      <file action="create">data/black_diamond/scripts/gold/_lib/atomic_write.py</file>
      <file action="create">tests/gold_lib/test_watermark.py</file>
      <file action="create">tests/gold_lib/test_atomic_write.py</file>
    </files>
  </scope>

  <wire_contract>
    Single canonical watermark convention ratified in PRD §3. Every IN Wave 1-5 TO imports from this lib. No per-script watermark reinvention allowed (PRD §8 coordination row).
  </wire_contract>

  <acceptance_criteria>
    1. Both modules exist with API exactly matching PRD §3 + §4 spec.
    2. Unit test coverage: all API functions + migration-compat readers; pytest PASS.
    3. Watermark schema JSON-schema compliant (all required fields present on write).
    4. `atomic_s3_write` uses `{key}.staging` intermediate; atomic rename via `CopyObject` + `DeleteObject` (S3 doesn't have native rename).
    5. Migration readers emit `DeprecationWarning` when reading old formats.
    6. Documented in `docs/data/watermark_contract.md` (short reference for Wave 1-5 TOs).
    7. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    8. MCP COMPLETE to COO + CTO with module paths, test pass count, docs path.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -rn 'CANONICAL_HOLDINGS_WATERMARK\|CLIENT_TIMESERIES_WATERMARK' data/black_diamond/scripts/gold/</run>
        <expect>Existing usage sites enumerated (B_00, C_06 per IN-1 memo). Informs migration-compat reader surface.</expect>
        <if_mismatch>Re-baseline migration scope.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io C_06</run>
        <expect>C_06 already uses CLIENT_TIMESERIES_WATERMARK — confirms one reference implementation for the migration reader.</expect>
        <if_mismatch>Locate any already-watermarked scripts for reference.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>pytest tests/gold_lib/ -v</run>
        <expect>All cases PASS.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/_lib/watermark.py data/black_diamond/scripts/gold/_lib/atomic_write.py</run>
        <expect>PY_COMPILE_OK both modules.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Single-writer of `_lib/watermark.py` + `_lib/atomic_write.py`. All IN Wave 1-5 scripts READ these; no modification outside W0/W5.
    - Output contract ratified in PRD §3; any schema change after W0 requires new CTO PRD.
  </cross_domain_coordination>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    W0.002 close → W0.003 (comp-incrparity tool) can validate against the helper lib; IN-2.W2+ per-script TOs can consume.
  </next>
</task_order>
