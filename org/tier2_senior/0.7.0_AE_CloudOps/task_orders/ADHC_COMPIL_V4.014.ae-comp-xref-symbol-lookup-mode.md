<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.014</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-xref `&lt;symbol&gt;` lookup mode — dual-purpose tool: graph-diff (existing) + symbol cross-reference (NEW)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status><!-- Authored by CTO direct per Andrew 2026-05-08 PM "full 5-item, run it" post-retrospective. PRD v0.3 addendum §13.4 TO-14. -->
    <priority>normal</priority>
    <estimated_effort>~0.75d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §13.4 TO-14 (v0.3 addendum 2026-05-08 PM)</ref>
    <ref type="retrospective">docs/architecture/ADHC_COMPIL_FULL_CORPUS_RETROSPECTIVE.md §6.9 + §7 Item A</ref>
    <ref type="anchor_cluster">2026-04-21 COMP_LEARNS dyad: 17/25 = 68% raw FAIL rate on `comp-xref &lt;module-path&gt;` and `comp-xref &lt;module-name&gt;` invocations. Tool is graph-diff; agents thought it was symbol lookup.</ref>
    <ref type="v3_deferred">v3 PRD §1: "COMP_LEARNS-corpus indexing for comp-xref... separate concern, COMP_LEARNS-internal, not biting production." — Now revisiting per full-corpus retrospective.</ref>
  </references>

  <context>
    `comp-xref` currently has graph-state-diff modes only (no-arg = diff vs baseline; `--save` to set baseline; `--ref HEAD~3`; `--json`). 17 FAILs on 2026-04-21 (single-day cluster) all from agents passing positional args (`comp-xref comp/framework/...`, `comp-xref harness`, `comp-xref comp.bench.mutations`) thinking the tool is a cross-reference lookup. v3 deferred as COMP_LEARNS-internal but the UX confusion is real and recurrent.

    Fix: dual-purpose tool. Preserve existing diff modes; add `<symbol>` lookup mode when positional arg provided + isn't a flag.
  </context>

  <scope>
    <step>
      <run>Read `comp-xref` source. Confirm current arg-parsing logic + how positional arg is handled (currently rejected/ignored).</run>
      <expect>Argparse layer identifiable; positional arg can be added without breaking flag-only invocations.</expect>
    </step>
    <step>
      <run>Add `comp-xref &lt;symbol&gt;` mode: when positional arg provided AND isn't a recognized flag, switch to symbol-lookup mode — return all graph nodes/edges that reference the symbol. Symbol disambiguation: function name, S3 key prefix, Lambda name, component name, EC2 role, etc. (same input-shape as `comp-blast` query).</run>
      <expect>Two modes coexist cleanly: no-arg = diff; arg-present = lookup.</expect>
    </step>
    <step>
      <run>Output for symbol mode: structured cross-reference (symbol → list of nodes/edges referencing it). Format consistent with comp-blast output (agents already know that shape).</run>
      <expect>Output is consumable + agent-recognizable.</expect>
    </step>
    <step>
      <run>Update `comp-xref --help` to clarify dual-purpose semantics: "no args = graph state diff vs baseline; positional arg = symbol cross-reference lookup."</run>
      <expect>Help text disambiguates modes; agents stop confusing the two.</expect>
    </step>
    <step>
      <run>Update `org/modules/graph/comp-tools.yaml` comp-xref entry: add the symbol-lookup mode + updated `when` examples.</run>
      <expect>Catalog reflects dual-purpose semantics.</expect>
    </step>
    <step>
      <run>Empirical test — re-run 5 representative queries from 2026-04-21 cluster (e.g., `comp-xref comp/framework/compiler_contract.py`, `comp-xref harness`, `comp-xref comp.bench.mutations`); expect each to return cross-reference results post-ship.</run>
      <expect>5/5 PASS (return cross-references); diff-mode (no-arg) regression-clean.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO.</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">`comp-xref &lt;symbol&gt;` returns cross-reference results when positional arg provided.</ac>
    <ac id="2">`comp-xref` (no-arg) preserves existing graph-diff behavior — regression-clean.</ac>
    <ac id="3">`comp-xref --save`, `--ref HEAD~3`, `--json` all preserved; no flag conflict.</ac>
    <ac id="4">Help text updated to clarify dual-purpose modes.</ac>
    <ac id="5">5 representative queries from 2026-04-21 cluster return PASS post-ship.</ac>
    <ac id="6">comp-tools.yaml entry updated.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read comp-xref source + current argparse logic.</phase>
    <phase id="2">Pre-commit: 7-cell test matrix — 5 cluster queries (lookup mode) + 1 diff-mode no-arg + 1 --save flag.</phase>
    <phase id="3">Post-commit empirical: rerun cluster queries; append to compiler-tools-log.md.</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>7-cell test matrix + cluster regression evidence</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Renaming the tool (preserve `comp-xref` entry-point; just add mode).</item>
    <item>Indexing comp/ tree itself (separate scope; COMP_LEARNS-side; not in v0.3).</item>
  </out_of_scope>
</task_order>
