<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.003</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-constants new tool — AST-indexer tier with check/index/new subcommands + pre-commit hook integration</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- SHIPPED 2026-05-08 by AE 0.7 commit `0eb2c8950` (comp-constants AST-indexer + drift gate; comp-constants-v1.0). 7/7 ACs PASS per AE RAVC2 20260508T~PM. ~30min wall-clock vs 1d catalog = 5% (1st instance of session under-budget pattern). Flipped pending→complete by 1.0.0_SA_CTO 2026-05-11 startup ground-truth pass. -->
    <priority>medium</priority>
    <estimated_effort>~1d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §3 row 3 + §4 TO-3</ref>
    <ref type="design_brief">docs/architecture/_drafts/ADHC_COMPIL_V4_INDEXER_BRIEF.md (DS~B authored)</ref>
    <ref type="cto_ratification">CTO ruling MCP 20260508T~PM — indexer-tier scope ACCEPTED into TO-3 (Option 1); 3-subcommand surface (check/index/new); AC #4 expanded to require both regression + value-add validation</ref>
    <ref type="seed_input_1">org/modules/graph/comp-constants-seed-bd.yaml (DS~B `290476bbf` — 12 constants, 17 sites, 1 drift FIRM_ID impl-pattern)</ref>
    <ref type="seed_input_2">org/modules/graph/comp-constants-seed-inf.yaml (DS~C `14a5474d5` — 9 constants, 33 sites, 3 drift INFLECTION_REP_IDS old-[3,11,12])</ref>
    <ref type="seed_input_3">org/modules/graph/comp-constants-seed-multifirm.yaml (DS~D `d1be50185` — 9 constants Python+JS/TS)</ref>
    <ref type="anchor_incident">INFNNA Joe Brandenburg attribution 2026-05-07 — INFLECTION_REP_IDS rep_id=6 missing from 8+ files; manual coordinated sync. PRD §5: 30+ file matches.</ref>
    <ref type="prior_art">.tools/extract_pipeline.py (existing AST-parse pattern in workspace; reuse parse infrastructure)</ref>
  </references>

  <context>
    Marker constants (`INFLECTION_REP_IDS`, `INFGRD_FIRM_AUA_LOWER/UPPER`, `FIRM_BUCKET_MAP`, `BD_FIRM_TAG`, etc.) are duplicated across 30+ files. Joe Brandenburg attribution (rep_id=6) required coordinated update across 8 sites; INFNNA UAD-CREATOR + GUARDS-AUDIT TOs were essentially "go propagate the constant change." No tool indexes the constants nor flags drift.

    **Tier-of-correctness ratified at indexer-tier (CTO ruling 2026-05-08).** SEED YAMLs (DS~B/C/D `f3f324a74`-onward) are seed inputs — T+0 snapshots that go stale on next code change. The indexer makes comp-constants self-maintaining: live AST re-scan rewrites sites; drift gate runs at pre-commit time.

    **Three-subcommand surface (per DS~B's brief):**
    - `comp-constants check` — drift gate; pre-commit hookable; exits non-zero if any constant in config has divergent values across sites
    - `comp-constants index` — live AST re-scan; rewrites the `sites` list in `comp-constants.config.yaml` to current ground truth
    - `comp-constants new` — discovery surface; surfaces ALL_UPPER_SNAKE_CASE constants found in scan but NOT yet in config; lets operator decide whether to add to allowlist

    **AST extraction pattern:** `ast.parse()` (existing prior-art in `extract_pipeline.py`) → walk Module-level `Assign` nodes → match `Name(id ALL_CAPS)` targets → extract value via `ast.literal_eval()` for str/int/float/list/set/frozenset/dict literals. For `os.environ.get(X, default)` calls, record as `env_backed: true` with the default value extracted.

    **Config source:** `comp-constants.config.yaml` (NEW) — derives initial allowlist from the 3 SEED YAMLs (merge schemas; preserve drift flags). Schema additive-compatible with seeds: lane (str), constants[] with name/type/canonical_value/sites/notes/optional drift+language fields.
  </context>

  <scope>
    <step>
      **Phase 1 — author tool skeleton + AST indexer.**

      File: `.tools/comp-constants` (Python script, executable, in PATH per workspace convention).

      Subcommand structure:
      - `comp-constants check` (default) — runs drift detection
      - `comp-constants index` — re-scan + rewrite config
      - `comp-constants new` — discover unindexed constants
      - `comp-constants list` — print current config (debug surface)

      AST extractor module:
      - Walks `search_surfaces` config glob (Python files; JS/TS deferred to v2)
      - Identifies module-level ALL_CAPS_SNAKE_CASE assignments
      - Resolves value via `ast.literal_eval` (str/int/float/list/set/frozenset/dict)
      - Identifies `os.environ.get(name, default)` patterns; records as env_backed
      - Returns site list: file:line:value:env_backed
    </step>

    <step>
      **Phase 1.5 — config bootstrap from SEED YAMLs.**

      Create initial `comp-constants.config.yaml`:
      - Source: merge `comp-constants-seed-{bd,inf,multifirm}.yaml` (already in `org/modules/graph/`)
      - Schema: preserve `lane`, `constants[]`, drift flags from SEED-INF, language flags from SEED-MULTIFIRM
      - Add `search_surfaces` per-lane:
        ```yaml
        search_surfaces:
          bd:
            - data/black_diamond/scripts/**/*.py
            - infra/aws/lambda/bd-pipeline/**/*.py
          inf:
            - data/orion/scripts/**/*.py
            - data/orion/manual_api/**/*.py
            - infra/aws/lambda/inf-pipeline/**/*.py
          multifirm:
            - infra/aws/lambda-edge/**/*.{mjs,js,ts}
            - infra/aws/lambda/shared-*/**/*.py
            - infra/aws/lambda/portal-*/**/*.py
        ```
      - Treat seeded entries as canonical for shipped scope; extend if needed.
    </step>

    <step>
      **Phase 2 — `check` subcommand (drift detection).**

      Algorithm:
      1. Load `comp-constants.config.yaml`
      2. For each constant in config: re-scan all `search_surfaces` for that constant's sites
      3. Compare current values vs canonical_value
      4. Output: list of drift sites (file:line:current_value:canonical_value); exit 1 if any drift, exit 0 if clean

      Pre-commit hook integration:
      - Add to `.tools/ds-commit-gate.sh` (CLAUDE.md Rule 14): `comp-constants check --file <staged-file>` for any staged Python file
      - Filter mode: only check constants whose sites include the staged file (don't full-repo scan on every commit; lookup index first)

      Performance gate: full-repo `comp-constants check` &lt; 10s on current state (~30 constants × ~50 sites = 1500 AST parses with file caching).
    </step>

    <step>
      **Phase 3 — `index` subcommand (live AST rewrite).**

      Algorithm:
      1. Load config
      2. For each constant: re-scan `search_surfaces`; collect new site list
      3. Detect drift; flag sites with `drift: true` if value differs from canonical_value
      4. Rewrite config in-place (preserve `notes`, `canonical_value`, but update `sites[]` from current AST scan)
      5. Commit-friendly: stable site ordering (alphabetical by file:line)

      Use case: after a coordinated rep_id change (like INFNNA.001 rep_id=6 propagation), run `comp-constants index` to refresh sites + flag any missed drift sites.
    </step>

    <step>
      **Phase 4 — `new` subcommand (discovery surface).**

      Algorithm:
      1. Walk all `search_surfaces` patterns
      2. Identify ALL_UPPER_SNAKE_CASE assignments NOT in config
      3. Filter out utility constants (BUFFER_SIZE, RETRY_LIMIT, MAX_*, DEFAULT_*) via regex blacklist
      4. Output: candidate constants + sites + values, suggesting they may be marker constants
      5. Operator reviews; manually adds chosen ones to config

      AC #4 dual-validation requirement (per CTO ruling):
      - **(a) Regression validation:** `comp-constants new` surfaces ≥ all constants found by SEED grep sessions (DS~B/C/D inventories). If any seeded constant fails to surface, AST scanner has narrower coverage than human grep — bug.
      - **(b) Value-add validation:** `comp-constants new` surfaces ≥ 1 constant the SEED grep sessions missed. Documents AST scanner's wider coverage. If value-add count is 0, AST scanner has equal-not-superior coverage; not a bug, but flag in TO-3 ship log for CTO review (may indicate undocumented cross-firm contracts).
    </step>

    <step>
      **Phase 5 — comp-tools.yaml registration.**

      Add row to `org/modules/graph/comp-tools.yaml`:
      - Tool name: `comp-constants`
      - Subcommands: `check` / `index` / `new` / `list`
      - When-to-use: pre-commit on Python edits; post-coordinated-constant-change rep_id-style propagation; pre-PRD-authoring constant discovery
      - Cost: lightweight (AST parse + file walk; cacheable)
      - Replaces: manual grep + spreadsheet drift tracking
    </step>

    <step>
      **Phase 6 — empirical validation against current state.**

      Run `comp-constants check` against current repo state. Expected:
      - Drift on `INFLECTION_REP_IDS` at 3 sites (per DS~C SEED-INF drift flags): pull_inflection_assets.py:53, create_tax_dim_queries.py:45, pull_inflection_transactions.py:49 — all on old `[3, 11, 12]`. **Tool should detect these post-config-load.**
      - Drift on `FIRM_ID` per DS~B SEED-BD finding: 4 sites with 3 divergent impl patterns (hardcoded vs env vs O6B_FIRM_ID). **Tool should detect impl-divergence.**
      - All other constants: clean (no drift).

      If tool detects different set than seeds claim → false positive/negative; debug.
    </step>

    <step>
      **Phase 7 — pre-commit hook integration ship.**

      Edit `.tools/ds-commit-gate.sh`:
      - Add `comp-constants check --file <staged-file>` post `ruff check`
      - Exit 1 on drift detection (gate), exit 0 on clean
      - Output: drift report visible to operator pre-commit

      Test fixture: stage a file with INFLECTION_REP_IDS = [3, 11, 12] (old value); commit gate should fail with drift report.
    </step>

    <step>
      Commit + push. Tag `comp-tools-v1.7.0` (or follow existing comp-* version sequence). record-terraform-deploy if applicable.
    </step>
  </scope>

  <acceptance_criteria>
    1. `.tools/comp-constants` script ships with check/index/new/list subcommands; executable; in PATH per workspace convention.
    2. `comp-constants.config.yaml` ships with merged content from 3 SEED YAMLs (≥25 constants total across bd+inf+multifirm lanes).
    3. `comp-constants check` runs in &lt; 10s full-repo; exits 1 on drift, 0 on clean. Detects all 3 INFLECTION_REP_IDS drift sites + FIRM_ID impl-divergence per SEED findings.
    4. **(Dual-validation per CTO ruling)** `comp-constants new` surfaces (a) ALL constants found by SEED grep sessions (regression validation — AST coverage ≥ human grep coverage), AND (b) ≥1 constant SEED grep sessions missed (value-add validation — empirical proof of wider AST coverage). Document (b) findings in TO-3 ship log; surface to CTO if any look like undocumented cross-firm contracts.
    5. `comp-constants index` rewrites `sites[]` in config from current AST scan; commit-friendly stable ordering; preserves `notes` + `canonical_value`.
    6. Pre-commit hook integration: `.tools/ds-commit-gate.sh` invokes `comp-constants check --file <staged>` for staged Python files; commit blocked on drift.
    7. Empirical: stage a Python file with INFLECTION_REP_IDS = `[3, 11, 12]` (old); pre-commit gate FAILS with drift report citing canonical `{3, 6, 11, 12}`.
    8. `comp-tools.yaml` row added; cross-references from `PRD_AUTHORING_PROTOCOL.md` §5 if appropriate.
    9. Session log Compiler Tools section reproduces each `<run>` from `<compiler_tools_mandate>` with observed output and pass/fail.
    10. RAVC2 to COO with: commit SHA, tool path, config path, drift detection sample output, dual-validation counts, pre-commit hook test fixture proof.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat org/modules/graph/comp-constants-seed-bd.yaml | python -c "import yaml,sys; d=yaml.safe_load(sys.stdin); print(len(d['constants']))"</run>
        <expect>≥5 BD constants present (baseline for tool to consume).</expect>
        <if_mismatch>If fewer, SEED-BD shipped incomplete. Surface to COO.</if_mismatch>
      </step>
      <step>
        <run>cat org/modules/graph/comp-constants-seed-inf.yaml | python -c "import yaml,sys; d=yaml.safe_load(sys.stdin); drift=sum(1 for c in d['constants'] for s in c['sites'] if s.get('drift')); print(f'inf consts={len(d[\"constants\"])} drift={drift}')"</run>
        <expect>≥5 INF constants; drift ≥1 (INFLECTION_REP_IDS old-[3,11,12] sites).</expect>
        <if_mismatch>If drift=0, SEED-INF didn't capture the rep_id=6 propagation gap; surface to COO.</if_mismatch>
      </step>
      <step>
        <run>ls -la .tools/extract_pipeline.py</run>
        <expect>File exists; AST-parse prior art available for pattern reuse.</expect>
        <if_mismatch>If missing, AST infrastructure is genuinely new; flag to COO + factor 0.5d into estimate.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/comp-constants check 2>&amp;1 | head -20</run>
        <expect>Exit code 1; drift report includes ≥3 INFLECTION_REP_IDS sites + FIRM_ID impl-divergence.</expect>
        <if_mismatch>If exit 0, tool isn't detecting known drift. Re-test scanner against SEED ground truth.</if_mismatch>
      </step>
      <step>
        <run>time .tools/comp-constants check 2>/dev/null</run>
        <expect>Real time &lt; 10s on full-repo scan.</expect>
        <if_mismatch>If &gt;10s, performance bottleneck; profile + fix before pre-commit hook integration.</if_mismatch>
      </step>
      <step>
        <run>.tools/comp-constants new | wc -l</run>
        <expect>≥1 candidate constant surfaced that wasn't in SEED YAMLs (value-add validation).</expect>
        <if_mismatch>If 0, AST coverage equals human grep — log in ship notes per CTO AC #4 ruling.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>git diff HEAD~1 -- .tools/ds-commit-gate.sh</run>
        <expect>Diff shows `comp-constants check --file` invocation added.</expect>
        <if_mismatch>Pre-commit integration not landed; reopen.</if_mismatch>
      </step>
      <step>
        <run>echo "INFLECTION_REP_IDS = [3, 11, 12]  # test old value" &gt;&gt; /tmp/test_drift.py; cd /tmp; .tools/comp-constants check --file test_drift.py; rm test_drift.py</run>
        <expect>Exit 1 + drift report citing canonical `{3, 6, 11, 12}` and old-value site.</expect>
        <if_mismatch>Hook not catching synthetic drift; debug.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Tool ships net-new lint/audit infrastructure; doesn't modify silver/bronze/gold scripts or S3 prefixes. No data reprocessing required.</no_reprocess_needed>
  </data_reprocess_scope>

  <dependencies>
    SEED inputs (DS~B/C/D shipped this session via `f3f324a74`/`290476bbf`/`14a5474d5`/`d1be50185`). All 3 YAMLs + dup-source baseline available at `org/modules/graph/`. TO-3 consumes; SEED outputs are canonical for shipped scope.
  </dependencies>
</task_order>
