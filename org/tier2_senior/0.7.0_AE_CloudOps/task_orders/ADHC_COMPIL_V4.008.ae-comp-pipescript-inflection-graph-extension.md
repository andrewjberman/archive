<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.008</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-pipescript Inflection-graph extension — extend extractor path globs to data/orion/scripts/{gold,silver,bronze}/** + data/orion/manual_api/** with full I/O edges</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- SHIPPED 2026-05-08 by AE 0.7 commit `7f82ffe01` (comp-pipescript inf-manual-api coverage). 6/6 ACs PASS per AE RAVC2; scope-narrowed during AE read-through (real gap was data/orion/manual_api/* only; INF gold + silver already covered by build_inf_gold_dag + build_silver_dag). ~25min wall-clock vs 1d = 4% of budget. Drove retrospective methodology correction (§6.1 identifier-existence validation). Flipped pending→complete by 1.0.0_SA_CTO 2026-05-11 startup ground-truth pass. -->
    <priority>normal</priority>
    <estimated_effort>~1d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §12.4 TO-8 (v0.2 addendum 2026-05-08 PM)</ref>
    <ref type="parent_to">ADHC_COMPIL_V4.003 (comp-constants new tool) — TO-8 consumes constants index for bootstrap</ref>
    <ref type="extractor">org/modules/graph/extract_pipeline.py — current path globs scope data/black_diamond/scripts/**; needs Orion path additions</ref>
    <ref type="seed_inputs">org/modules/graph/comp-constants-seed-{bd,inf,multifirm}.yaml (DS~B/~C/~D SEED outputs from V4 SEED wave)</ref>
    <ref type="related">ADHC_COMPIL.001 added `--pipeline inf-gold` flag to comp-pipescript deployed; this TO extends graph extraction itself (deeper than the deployed flag).</ref>
  </references>

  <context>
    The compiler graph currently scopes `data/black_diamond/scripts/**` (BD-pipeline-shaped). Inflection scripts at `data/orion/scripts/{gold,silver,bronze}/**` and `data/orion/manual_api/**` are partial-coverage at best. 12+ NOT-INDEXED FAILs in the 2-week compiler-tools-log (INF_I_D02b, INF_I_D00b, INF_I_D00c, INF_D_07, pull_inflection_billing_dim.py, pull_inflection_performance_dim.py, etc.) all root-cause to extractor not scanning Orion paths.

    Empirical workaround pattern: agents fall back to direct S3 ls + ETag verification + manual file reads. This costs ~10-30 min per affected TO + erodes trust in the tool's coverage claims. ADHC_COMPIL.001's `--pipeline inf-gold` flag was a partial fix on the `comp-pipescript deployed` subcommand only; graph extraction itself is incomplete.

    Andrew direct 2026-05-08 PM: "comp-constants would help a lot as a precursor to a lot of this." — TO-3's marker-constants index can bootstrap "any script referencing INFLECTION_REP_IDS is Inflection-pipeline" classification, validating extractor path-glob coverage.
  </context>

  <scope>
    <step>
      <run>Read `org/modules/graph/extract_pipeline.py` (current extractor) — confirm BD path globs + AST extraction logic (S3 read/write detection via helper-function tracing per COMP_LEARNS.022 fixes).</run>
      <expect>Existing extractor has a path-glob constant or function that can be extended; AST extraction is pipeline-agnostic.</expect>
    </step>
    <step>
      <run>Add Orion path globs to extractor: `data/orion/scripts/gold/**/*.py`, `data/orion/scripts/silver/**/*.py`, `data/orion/scripts/bronze/**/*.py`, `data/orion/manual_api/**/*.py`. Register Orion script nodes with same extraction logic as BD scripts.</run>
      <expect>Path globs added; comp-build picks up Orion scripts on next rebuild.</expect>
      <if_mismatch>If Orion script structure has bronze pull/silver build/gold transform conventions different from BD, document divergence + handle in extractor (not in scope to refactor Orion script structure).</if_mismatch>
    </step>
    <step>
      <run>Bootstrap from TO-3 comp-constants output — read `comp-constants-seed-inf.yaml` + live `comp-constants check` output; identify any script referencing `INFLECTION_REP_IDS` not yet in graph; cross-validate against path-glob coverage.</run>
      <expect>Zero "constants reference but not in graph" cases post-extension. If any: extractor path globs missing.</expect>
      <if_mismatch>Add the missing path-glob; rerun comp-build; reconcile.</if_mismatch>
    </step>
    <step>
      <run>Auto-detection logic — script-name prefix `INF_D_*`/`INF_I_*` defaults to Orion-pipeline classification (no `--pipeline inf-gold` flag required for default queries). BD scripts unchanged.</run>
      <expect>`comp-pipescript io INF_D_04`, `comp-pipescript deployed INF_I_D00c`, `comp-blast INF_B_00` all return correct results with default invocation.</expect>
      <if_mismatch>If existing `--pipeline inf-gold` flag conflicts with auto-detection, prefer auto-detection + retain flag for explicit override.</if_mismatch>
    </step>
    <step>
      <run>Regression test — `comp-pipescript io D_04`, `comp-pipescript deployed B_01`, `comp-blast bd-gold-trigger` (BD cases) must continue to work unchanged.</run>
      <expect>BD case = no behavior change; Inflection case = full coverage.</expect>
    </step>
    <step>
      <run>Empirical validation against 2-week NOT-INDEXED list: rerun `comp-pipescript io <script>` for each of the 12+ scripts that FAILed in 2-week log. Document PASS rate.</run>
      <expect>PASS rate >= 11/12 (allow 1 exception if a specific script structure resists extraction; document the exception).</expect>
      <if_mismatch>If PASS rate < 11/12, surface remaining gaps; consider sub-TO for specific extraction edge cases.</if_mismatch>
    </step>
    <step>
      <run>Run comp-build full rebuild + verify Orion node count in graph stats. Ship via `.tools/safe-commit.sh` per ownership rules. RAVC2 to CTO + COO.</run>
      <expect>Graph stats show Orion nodes registered; commit clean; tag if appropriate (extension is tooling-internal; tag optional).</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">comp-pipescript graph extractor scans `data/orion/scripts/{gold,silver,bronze}/**/*.py` + `data/orion/manual_api/**/*.py` after this TO ships.</ac>
    <ac id="2">All 12+ NOT-INDEXED scripts from 2-week compiler-tools-log return PASS via `comp-pipescript io <script>` post-ship (≥11/12 with documented exceptions if any).</ac>
    <ac id="3">No `--pipeline inf-gold` flag required for default queries on Orion scripts; auto-detection works via script-name prefix or constants reference.</ac>
    <ac id="4">BD case regression-clean: `comp-pipescript io D_04` + `comp-pipescript deployed B_01` + `comp-blast bd-gold-trigger` produce same output as pre-ship.</ac>
    <ac id="5">comp-build rebuild succeeds with no stale-cache warnings + Orion node count visible in `comp-pipescript stats`.</ac>
    <ac id="6">RAVC2 to CTO + COO with sample queries (≥3 Orion + ≥3 BD) demonstrating correctness.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">
      <run>`comp-constants list --lane inf` (post TO-3 ship) + `cat comp-constants-seed-inf.yaml` — enumerate Inflection scripts that reference INFLECTION_REP_IDS as bootstrap input.</run>
      <expect>List of Inflection-pipeline scripts; cross-reference against extractor path-glob coverage.</expect>
    </phase>
    <phase id="2">
      <run>Pre-commit: `comp-build` full rebuild; verify zero stale-cache warnings + Orion node count.</run>
      <expect>Clean build; `comp-pipescript stats` shows new Orion nodes.</expect>
    </phase>
    <phase id="3">
      <run>Post-commit empirical: rerun `comp-pipescript io <script>` for the 12 NOT-INDEXED scripts from 2-week log; append rows to org/compiler-tools-log.md.</run>
      <expect>≥11/12 PASS; log rows captured.</expect>
    </phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Sample query outputs (≥3 Orion + ≥3 BD) + comp-build stats + empirical 12-script regression list</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Refactoring Orion script directory structure (data/orion/scripts/* layout stays as-is).</item>
    <item>Adding new Orion gold scripts or modifying existing ones.</item>
    <item>Extending comp-validate Orion config support — that's TO-9.</item>
    <item>Comp-iam EC2 role coverage — that's a separate gap (Group 6) not in this TO.</item>
  </out_of_scope>
</task_order>
