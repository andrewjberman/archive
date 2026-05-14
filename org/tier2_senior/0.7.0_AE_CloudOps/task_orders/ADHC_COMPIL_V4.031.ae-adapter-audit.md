<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.031</id>
    <slug>ae-adapter-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>Wave 1 (.027 + .028) + Wave 2 (.029a + .029b) RAVC2 PASS. May share ts-morph install setup with .026 (Wave 3 sibling) — coord at ship time.</dispatch_unblock_condition>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — Wave 3 multi-tenant readiness; Class-D pattern detection; corpus-strong empirical anchor</priority>
    <sla>~2-3 days wall per PRD §15.4 sizing (TS AST + live S3 schema inspection)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-031</ref>
    <ref type="anchor_session">Session 23 corpus — 3 same-arc adapter catches 2026-05-13: INFFIN #7 schema-drift (`32df3b85` → `cae9dcb2`); Surface #2 inverted-fallback (`d622a249`); Surface #8 (`22b7b7b4`)</ref>
    <ref type="pattern">Class-D D-1 sub-pattern (Andrew's "production-empirical-validation gate" framing)</ref>
    <ref type="cross_link">Wave 3 sibling: .026 comp-types index (shares TS AST machinery; consider ts-morph install coordination).</ref>
  </references>

  <context>
    Portal-side static adapters (e.g., `getPlatinumAdvisorSummaryStaticInflection` in `portal/src/api/endpoints/advisor-intelligence.ts`) map raw S3 envelope → typed nested shape. Every consumer-readable typed path must thread from raw, but adapter codepaths are silent-partial-success vulnerable:
    - tsc passes (types align)
    - visual logic-walk reads correct (manual review at PR time)
    - runtime smoke doesn't crash (production rendering)
    - production data subtly missing (fields silently default to undefined)

    Class-D pattern. Currently caught via empirical S3-shape inspection at adapter boundary post-ship. `comp-adapter-audit <adapter-fn>` lifts this into structural pre-commit check.

    **Three same-arc Session 23 catches (the empirical corpus):**
    1. INFFIN #7 schema-drift: `raw.book ?? raw.summary` inverted fallback → ship `32df3b85` → empirical S3 caught wrong-direction default → re-ship `cae9dcb2`
    2. Surface #2 adapter delta: `relationship_stacked_periods[]` typed-but-not-threaded → caught at empirical S3 verify pre-Lambda-deploy
    3. Surface #8 (.012): `is_fee_paying` field type-aligned but adapter missed propagation → caught at FE empirical render

    Pattern: type-system thinks adapter is correct; empirical S3 shape diff reveals missing field threading.
  </context>

  <objective>
    Land `comp-adapter-audit <adapter-fn>` subcommand. Input: adapter symbol (e.g., `getPlatinumAdvisorSummaryStaticInflection`). Output:
    - Raw envelope shape from S3 (most-recent platinum object for the adapter's data source)
    - Typed output shape (TS type the adapter returns)
    - Field-by-field threading audit: which raw fields land in output; which output fields default to undefined; which output fields lack any raw source (silent-drift candidates)
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/comp-pipescript OR new .tools/comp-adapter-audit (CLI shape choice — coord with .026 for shared TS AST setup)</file>
      <file action="create">org/modules/graph/adapter-audit/{adapter-fn}.yaml (per-adapter audit manifest)</file>
      <file action="readonly_reference">portal/src/api/endpoints/advisor-intelligence.ts (anchor adapter file)</file>
      <file action="readonly_reference">portal/src/api/endpoints/portfolio.ts (additional adapter targets)</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>grep -rn "getPlatinumAdvisorSummaryStatic\|^export.*function.*async.*get.*Static" portal/src/api/endpoints/ | head -10</run>
      <expect>Adapter function family enumerated; ≥2-3 candidates for tool validation.</expect>
      <if_mismatch>If 0 hits, adapter file structure changed; verify source paths.</if_mismatch>
    </step>
    <step>
      <run>git log --all --oneline --since="3 days ago" --grep="32df3b85\|cae9dcb2\|d622a249\|22b7b7b4" | head -10</run>
      <expect>4 anchor commits present in corpus.</expect>
      <if_mismatch>If commits absent, anchor corpus needs reverify.</if_mismatch>
    </step>
    <step>
      <run>aws s3 ls s3://opal-data-inf/platinum/advisors/ | head -5</run>
      <expect>Adapter data source S3 paths enumerable; raw envelope inspection works.</expect>
      <if_mismatch>S3 access issue or path drift; verify before proceeding.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before write">
    <step>
      <run>comp-adapter-audit getPlatinumAdvisorSummaryStaticInflection</run>
      <expect>Output: raw envelope shape + typed output shape + field-by-field threading audit. ≥3 "missing threading" flags for fields the type declares but adapter doesn't populate (silent-drift candidates).</expect>
      <if_mismatch>STOP. Tool must detect known-pattern silent-drift sites.</if_mismatch>
    </step>
    <step>
      <run>Retroactive validation: comp-adapter-audit at PRE-`cae9dcb2` checkout (the inverted-fallback bug state)</run>
      <expect>Tool flags `raw.book ?? raw.summary` inverted-direction default OR equivalent threading anomaly that 32df3b85→cae9dcb2 fixed.</expect>
      <if_mismatch>AC2 load-bearing; iterate detection logic.</if_mismatch>
    </step>
    <step>
      <run>Retroactive validation: pre-`d622a249` (Surface #2 missing `relationship_stacked_periods[]` threading)</run>
      <expect>Tool flags missing field in adapter that Surface #2 needed.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>Run on ≥3 adapter functions (Inflection + 49F + a portfolio adapter)</run>
      <expect>No crashes; consistent output structure.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `comp-adapter-audit getPlatinumAdvisorSummaryStaticInflection` returns raw-vs-typed threading audit.
    AC2: Retroactive validation detects INFFIN #7 schema-drift bug pre-`cae9dcb2` (would have flagged `raw.book ?? raw.summary` inverted fallback at PR review).
    AC3: Retroactive validation detects Surface #2 adapter delta pre-`d622a249` (would have flagged missing `relationship_stacked_periods` thread before HOLD).
    AC4: Per-adapter yaml manifest persisted under `org/modules/graph/adapter-audit/`.
    AC5: Tested on ≥3 adapters without crash.
    AC6: Session log + RAVC2 MCP to COO with retroactive validation evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: adapter enumeration + git log anchor commits + S3 access verify
    Phase 2: comp-adapter-audit + retroactive validation on cae9dcb2 + d622a249 checkouts
    Phase 3: ≥3-adapter cross-test
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: Wave 1 + Wave 2 RAVC2.

    SHARED-SETUP: .026 comp-types index uses TS AST; coord ts-morph install if separate ships.

    POST-SHIP CONSUMERS: PR-review-time pre-commit check for adapter touches; future Class-D-pattern incidents catch pre-ship.

    NO PORTAL CODE CHANGES.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Compiler-tool development with S3 read-only inspection.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `comp-adapter-audit` subcommand or binary
    2. Per-adapter manifest yaml under `org/modules/graph/adapter-audit/`
    3. Retroactive validation evidence on `cae9dcb2` + `d622a249` checkouts
    4. Session log + RAVC2 to COO
  </deliverables>

  <ravc>AE 0.7 RAVC2 to COO on AC1-6 PASS.</ravc>

  <notes>
    **AC2 + AC3 are load-bearing:** retroactive validation on the 3-catch corpus IS the value-signal. Same-arc structural pattern Class-D D-1 is what this tool detects.

    **Banking:** post-ship adapter audits should feed FIRMSEP.10 Cottonwood adapter authoring (when Cottonwood partner ships, run comp-adapter-audit on Cottonwood adapter PRE-ship; would surface partial-threading silently).

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.
  </notes>
</task_order>
