<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.019</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-pipescript BLOCKING bug fixes — deployed UnboundLocalError + chain --pipeline silently ignored</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- Closed 2026-05-08T~PM by AE 0.7.0. Both bugs fixed in single pipeline_cli.py edit. Bug 1.1: skip_gold init at top of cmd_deployed + inf-gold branch sets to False with filter-check. Bug 1.2: cmd_chain reads args.pipeline + passes to _build_dag(); explicit error if chain not registered (replaces silent BD return). Empirical evidence: pre-fix UnboundLocalError reproduced; post-fix renders INF deployment status cleanly. INF chains DO exist (full/incremental/label/silver_prep) — chain --pipeline inf-gold full returns 47 scripts. BD regression-clean (default chain downstream + deployed D_00c + bd-silver all unchanged). -->
    <priority>high</priority>
    <estimated_effort>~0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md (V4 family)</ref>
    <ref type="ops_briefing">AE 0.7 OPS triage briefing 20260508T~PM Cat 1 (BLOCKING)</ref>
    <ref type="ops_matrix">docs/architecture/ADHC_COMPIL_V4_017_TEST_MATRIX.md (full evidence)</ref>
  </references>

  <context>
    Two BLOCKING bugs surfaced empirically via TO-017 OPS test matrix. Both in `comp-pipescript`. One crash; one silent-wrong (worse — agent reads BD output thinking it's INF, makes wrong decisions).
  </context>

  <scope>
    <step>
      <run>**Bug 1.1 (crash):** `comp-pipescript deployed --pipeline inf-gold INF_D_04` raises `UnboundLocalError: cannot access local variable 'skip_gold' where it is not associated with a value` at `org/modules/graph/pipeline_cli.py:1004`. Root cause: silver branch initializes `skip_gold`; gold-only path references it without init. Fix: initialize `skip_gold = True` (or False, depending on default semantics) at top of `cmd_deployed` before the silver-completion check.</run>
      <expect>Empirical: `comp-pipescript deployed --pipeline inf-gold INF_D_04` returns deployment status without crash. Same invocation regression-clean for BD case.</expect>
    </step>
    <step>
      <run>**Bug 1.2 (silent-wrong):** `comp-pipescript chain downstream --pipeline inf-gold` silently returns BD chain (12 scripts) instead of INF chain. Root cause: `--pipeline` flag parsed by argparse but not consumed by `chain` subcommand resolver. Fix: wire `--pipeline` through `cmd_chain`. May need INF chain config additions if `gold_pipeline_deps.yaml` lacks INF entries — surface via RAVC1 if scope expands.</run>
      <expect>Empirical: `comp-pipescript chain downstream --pipeline inf-gold` returns INF chain (or explicit "INF chain config not registered" error if INF entries absent). BD case unchanged.</expect>
      <if_mismatch>If INF chain config doesn't exist + extending it requires PRD-level scope: surface via RAVC1; defer chain config to follow-on TO; ship the flag-consumption fix only.</if_mismatch>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO with empirical pre/post evidence per bug.</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">Bug 1.1 fixed: `comp-pipescript deployed --pipeline inf-gold INF_D_04` returns valid output (not UnboundLocalError).</ac>
    <ac id="2">Bug 1.2 fixed: `comp-pipescript chain downstream --pipeline inf-gold` returns INF chain (or explicit error if INF chain config not registered — NOT silent BD chain).</ac>
    <ac id="3">BD case regression-clean: `comp-pipescript deployed` (default) + `comp-pipescript chain downstream` (default) both unchanged.</ac>
    <ac id="4">Empirical evidence in RAVC2: pre-ship error captures + post-ship valid output per bug.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read pipeline_cli.py — locate `cmd_deployed` + `cmd_chain` resolver paths.</phase>
    <phase id="2">Pre-commit: 4-cell test matrix (2 bugs × pre-ship vs post-ship).</phase>
    <phase id="3">Post-commit empirical: append rows to org/compiler-tools-log.md.</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Pre/post empirical per bug + BD regression test</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>INF chain config authoring (if 1.2 RAVC1 surfaces this; defer to follow-on).</item>
    <item>Other BLOCKING bugs not in Cat 1 of OPS briefing.</item>
  </out_of_scope>
</task_order>
