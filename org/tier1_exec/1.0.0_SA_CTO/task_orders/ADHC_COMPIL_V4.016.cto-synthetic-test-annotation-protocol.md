<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.016</id>
    <project>ADHC_COMPIL_V4</project>
    <title>compiler-tools-log synthetic-test annotation protocol — convention + 3-place documentation</title>
    <issued_to>1.0.0_SA_CTO</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status><!-- Self-issued by CTO per PRD v0.3 addendum §13.4 TO-16. CTO direct ship; no AE involvement. -->
    <priority>normal</priority>
    <estimated_effort>~0.25d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §13.4 TO-16 (v0.3 addendum 2026-05-08 PM)</ref>
    <ref type="retrospective">docs/architecture/ADHC_COMPIL_FULL_CORPUS_RETROSPECTIVE.md §4.2 + §6.10 + §7 Item E</ref>
    <ref type="anchor_evidence">2026-04-30 v3 testing day: ~15 of 27 comp-validate FAILs were synthetic test fixtures (`/tmp/empty_test_artifact.json`, `nonexistent_script_xyz`, `definitely_not_a_thing`, etc.). Inflated raw FAIL rate from 29% real → 36.7% raw across full corpus.</ref>
  </references>

  <context>
    Test-fixture runs (intentional FAIL/SKIPPED entries during tool-development testing) currently look identical to real failures in `compiler-tools-log.md`. This pollutes retrospective analysis — agents/CTO running aggregations cannot distinguish "tool genuinely failed for an agent" from "tool was tested with deliberately-bad input." Fix: protocol convention for annotating synthetic entries.
  </context>

  <scope>
    <step>
      <run>Update `org/compiler-tools-log.md` header section. Add a new sub-section between "Format" and existing "Results" doc explaining the synthetic-test convention:
```
**Synthetic test fixtures:**
Test-fixture runs (deliberately-failing inputs during tool-development testing) MUST include `(SYNTHETIC TEST FIXTURE) <description>` in the NOTE column. This distinguishes intentional test failures from real agent-encountered failures during retrospective analysis.

Example:
| 2026-04-30 | 0.4.0_DS~A | (no-TO) | comp-validate | comp-validate definitely_not_a_thing | FAIL | (SYNTHETIC TEST FIXTURE) ADHC_COMPIL.012 invalid-script-name regression test |
```</run>
      <expect>Header documents the convention.</expect>
    </step>
    <step>
      <run>Update `org/modules/graph/comp-tools.yaml` — add a `compiler_tools_log_conventions` top-level section (or append to existing notes section) documenting the synthetic-test annotation:
```yaml
compiler_tools_log_conventions:
  synthetic_test_marker: "(SYNTHETIC TEST FIXTURE)"
  applies_when: "Tool-development testing with deliberately-bad inputs"
  example: "comp-validate definitely_not_a_thing | FAIL | (SYNTHETIC TEST FIXTURE) ADHC_COMPIL.012 invalid-script-name regression test"
  rationale: "Distinguishes intentional test failures from real agent-encountered failures during retrospective analysis."
```</run>
      <expect>Catalog references the convention.</expect>
    </step>
    <step>
      <run>Update `docs/architecture/ADHC_COMPIL_FULL_CORPUS_RETROSPECTIVE.md` §1.4 — add footnote referencing the convention as part of methodology:
```
**Forward-only convention:** post-2026-05-08 synthetic test runs MUST use the `(SYNTHETIC TEST FIXTURE)` annotation per `compiler-tools-log.md` header. Pre-2026-05-08 entries can be retroactively annotated by their authors when next touched (no backfill required).
```</run>
      <expect>Methodology references the protocol; future retrospectives auto-discount annotated entries.</expect>
    </step>
    <step>
      <run>Optional retroactive annotation — for the 15 known synthetic entries on 2026-04-30, append annotation to existing rows. Forward-only is fine; backfill is a nice-to-have.</run>
      <expect>If time permits: 15 entries annotated. If not: skip (forward-only is the AC).</expect>
    </step>
    <step>
      <run>Commit via .tools/safe-commit.sh; CTO RAVC2 self-close (no external recipient required for CTO-direct doc-only TO).</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">`compiler-tools-log.md` header section documents the `(SYNTHETIC TEST FIXTURE)` convention with example.</ac>
    <ac id="2">`org/modules/graph/comp-tools.yaml` includes `compiler_tools_log_conventions` section referencing the protocol.</ac>
    <ac id="3">`ADHC_COMPIL_FULL_CORPUS_RETROSPECTIVE.md` §1.4 references the forward-only convention as part of methodology.</ac>
    <ac id="4">Convention is forward-only — no backfill required; pre-2026-05-08 entries may be retroactively annotated when authors next touch them.</ac>
    <ac id="5">Existing log entries unchanged unless retroactively annotated; structural change is header-only.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">N/A — doc-only TO; no compiler tools required for authoring.</phase>
    <phase id="2">Pre-commit: verify all 3 docs reference the convention consistently.</phase>
    <phase id="3">Post-commit: append a row to compiler-tools-log.md noting this TO's ship + first use of the convention (meta-example).</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>Self-RAVC (CTO) + FYI to 2.0.0_SA_COO</expected_recipient>
    <expected_evidence>Commit hash + 3-doc consistency check</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Backfilling pre-2026-05-08 synthetic entries (forward-only convention; retroactive is opt-in).</item>
    <item>Tool-side enforcement of the convention (process-only; agents annotate at log-write time).</item>
    <item>Auto-detection of synthetic patterns in existing log (separate scope; would need ML/regex heuristic).</item>
  </out_of_scope>
</task_order>
