<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.009</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-validate Orion config support — `--config &lt;path&gt;` flag + script-name auto-resolver + INFLECTION_REP_IDS symbolic-rule integration</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status><!-- Authored by CTO direct per Andrew 2026-05-08 PM "distribute the Task orders" delegation. PRD v0.2 addendum §12.4 TO-9. Sequencing: gates on TO-3 comp-constants for symbolic-rule resolution. -->
    <priority>normal</priority>
    <estimated_effort>~0.75d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §12.4 TO-9 (v0.2 addendum 2026-05-08 PM)</ref>
    <ref type="parent_to">ADHC_COMPIL_V4.003 (comp-constants) — TO-9 consumes constants index for symbolic-rule resolution</ref>
    <ref type="bd_config">data/black_diamond/scripts/gold/gold_validate_config.yaml — current default config (BD-only)</ref>
    <ref type="orion_config">data/orion/scripts/gold/gold_validate_config.yaml — exists per ADHC_COMPIL.006 + .012 ship; needs `--config` flag to be loadable</ref>
    <ref type="anchor_incident">INFLFE.006-data 2026-05-06: "comp-validate NO_CONFIG applicable — tool resolves INF_D_04 to BD leaderboard checks; false ERRORs. Manual artifact spot-check performed instead."</ref>
  </references>

  <context>
    `comp-validate &lt;script&gt;` resolves to `data/black_diamond/scripts/gold/gold_validate_config.yaml` only. Running on Inflection scripts produces false ERRORs (BD leaderboard checks emit on INF_D_04 partner_analytics) or NO_CONFIG-skip (no rules match Inflection-specific publishers). 4+ TOs in 2-week window flagged this:
    - INFLFE.006-data (DS~A 2026-05-06): NO_CONFIG applicable + false ERRORs.
    - ADVI_INFPRTY (DS~A 2026-04-27): "No `gold_validate_config.yaml` rules currently match these specific publishers for INFLEC. Spot-checked output schema directly."
    - ADVI_INFLV2.005 + 2 others.

    The Orion config exists but has no CLI flag to load it. Also: script-name prefix `INF_D_*`/`INF_I_*` should auto-resolve to Orion config (no flag required for default queries) — same auto-detection pattern as TO-8.

    Andrew direct 2026-05-08 PM identified comp-constants as precursor — symbolic rules (e.g., "expect: households filtered to INFLECTION_REP_IDS") let Orion config reference canonical constants without hardcoding values; tool resolves at validate time.
  </context>

  <scope>
    <step>
      <run>Read existing `comp-validate` CLI implementation. Locate config-resolution logic (currently hardcoded BD path).</run>
      <expect>Single hardcoded-path location to extend; clean refactor target.</expect>
    </step>
    <step>
      <run>Add `--config &lt;path&gt;` flag. When provided, override default config-resolution. When omitted, fall through to auto-resolver (next step).</run>
      <expect>Flag plumbing: `comp-validate D_04 --config data/orion/scripts/gold/gold_validate_config.yaml` loads explicit Orion config.</expect>
    </step>
    <step>
      <run>Auto-resolver — script-name prefix `INF_D_*`/`INF_I_*` defaults to Orion config; otherwise default to BD config. Override via explicit `--config` flag stays available.</run>
      <expect>`comp-validate INF_D_04` auto-loads Orion config; `comp-validate D_04` auto-loads BD config; both with no flag.</expect>
      <if_mismatch>If script-name prefix is ambiguous (some Orion scripts may not start with `INF_`), document edge cases + add fallback logic.</if_mismatch>
    </step>
    <step>
      <run>Symbolic-rule integration with TO-3 comp-constants — Orion config rules can reference symbolic names (e.g., `expect: "households filtered to INFLECTION_REP_IDS"`); tool resolves to canonical value at validate time via `comp-constants check` output.</run>
      <expect>Symbolic resolution works: rule with `INFLECTION_REP_IDS` literal in expect-string passes when artifact contains all 4 of {3,6,11,12}; FAILs if rep_id=6 missing (regression to pre-INFNNA Joe Brandenburg state).</expect>
      <if_mismatch>If TO-3 not yet shipped, this sub-step gates; ship the basic flag-plumbing portion first, return for symbolic resolution post-TO-3.</if_mismatch>
    </step>
    <step>
      <run>Empirical validation — rerun INFLFE.006-data case: `comp-validate INF_D_04 --artifact &lt;inflection_partner_analytics_quarterly.json&gt;` produces correct validation (no false ERRORs about leaderboard).</run>
      <expect>Inflection case validates against Orion config; results meaningful + actionable.</expect>
    </step>
    <step>
      <run>BD regression — `comp-validate D_04 --artifact &lt;BD leaderboard.json&gt;` produces same output as pre-ship.</run>
      <expect>BD case unchanged.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO with sample Inflection + BD validation outputs.</run>
      <expect>Clean ship; both cases empirically demonstrated.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">`--config &lt;path&gt;` flag works on `comp-validate &lt;script&gt;` invocation; explicit config override loads any specified yaml.</ac>
    <ac id="2">Auto-resolver: `comp-validate INF_D_*` defaults to Orion config; `comp-validate &lt;BD_script&gt;` defaults to BD config; both without `--config` flag.</ac>
    <ac id="3">Symbolic-rule resolution via TO-3 comp-constants: Orion config rules reference `INFLECTION_REP_IDS`; tool resolves to canonical {3,6,11,12} at validate time.</ac>
    <ac id="4">INFLFE.006-data class regression-validates correctly post-ship: `comp-validate INF_D_04 --artifact &lt;inflection_artifact&gt;` produces correct result (no false BD ERRORs).</ac>
    <ac id="5">BD case regression-clean: `comp-validate D_04 --artifact &lt;BD_artifact&gt;` produces same output as pre-ship.</ac>
    <ac id="6">RAVC2 to CTO + COO with sample outputs from both Inflection + BD cases.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">
      <run>`comp-constants check INFLECTION_REP_IDS` (post TO-3 ship) — confirm symbolic resolution data source available.</run>
      <expect>Drift-clean; canonical {3,6,11,12} returned.</expect>
    </phase>
    <phase id="2">
      <run>Pre-commit: synthetic test against both Orion + BD configs with known-good + known-bad artifacts.</run>
      <expect>4-cell matrix all PASS expected outcomes.</expect>
    </phase>
    <phase id="3">
      <run>Post-commit empirical: rerun INFLFE.006-data + 1 BD regression case; append rows to org/compiler-tools-log.md.</run>
      <expect>Both correct; log rows captured.</expect>
    </phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>4-cell matrix sample (Orion-config × Inflection-artifact / BD-config × BD-artifact / explicit-flag override / auto-resolver default) + symbolic-resolution proof</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Authoring new validation rules in either Orion or BD config (those are gold-script-author scope when emitting new fields).</item>
    <item>Extending the Orion config schema (rule format stays YAML; symbolic-name references are textual).</item>
    <item>Cross-firm config (Cottonwood) — not in scope until FIRMSEP.10 ships; can be added as future TO when that lands.</item>
  </out_of_scope>
</task_order>
