<task_order>
  <metadata>
    <id>0.1.0_DS_CompLearns-2026-04-15-comp-learns-008-bench-sop</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_CompLearns</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- Flips pending when ~A closes PRD #1 follow-ups. Transferability lever — 4-6 CTO hours per target → DS-runnable under spot-check. -->
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — transferability unlock</priority>
  </metadata>

  <references>
    <ref type="doctrine">docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md (CTO's 7-step construction protocol + 5 query dimensions + 6 Goodhart failure modes)</ref>
    <ref type="precedent">docs/architecture/COMP_LEARNS_HTTPX_TARGET.md (CTO-authored target #1; SOP distills this pattern)</ref>
  </references>

  <objective>
    Turn CTO's qualitative framework 7-step protocol into a DS-runnable checklist + 4 template files.
    Without this, every target is 4-6 CTO hours; with it, DS lanes can author target harnesses under
    CTO spot-check only. This is the transferability lever for scaling COMP_LEARNS to multiple targets.

    Scope: framework doc + template files under `comp/framework/templates/`. Does NOT author queries
    for any target — that's per-target TO.
  </objective>

  <scope>
    <files>
      <file action="create">docs/architecture/COMP_LEARNS_BENCHMARK_AUTHORING_SOP.md</file>
      <file action="create">comp/framework/templates/SURFACE_INVENTORY.md.template</file>
      <file action="create">comp/framework/templates/EDGE_TYPES.md.template</file>
      <file action="create">comp/framework/templates/QUERY_MATRIX.yaml.template</file>
      <file action="create">comp/framework/templates/VERIFIABILITY_AUDIT_CHECKLIST.md.template</file>
    </files>
  </scope>

  <wire_contract>
    SOP is LLM+human-readable. Each of the 7 CTO-protocol steps has:
    - What DS does (procedural)
    - Template file to fill
    - Verifiability check (how CTO spot-checks without re-authoring)
    - Goodhart guard — which of the 6 failure modes this step addresses

    Templates are fill-in-the-blank Markdown/YAML skeletons DS copy into `comp/targets/{name}/`.
    Framework validator (`comp.framework.query_schema`) accepts the populated template at `load_queries`.

    5 query dimensions (simple_fact / single_hop / cross_surface / compound_hard / counterfactual)
    have explicit quota guidance in the SOP — DS lane sees target tag distribution goals upfront.
  </wire_contract>

  <acceptance_criteria>
    1. SOP at `docs/architecture/COMP_LEARNS_BENCHMARK_AUTHORING_SOP.md` ≤200 lines; maps CTO's 7 steps 1:1.
    2. 4 templates live under `comp/framework/templates/`.
    3. Goodhart-guard callouts present at each relevant step — minimum 3 of 6 failure modes addressed explicitly.
    4. 5-dimension quota guidance (e.g., "~30% simple_fact, ~30% single_hop, ~20% cross_surface, ~10% compound_hard, ~10% counterfactual" — adjust per target).
    5. CTO spot-check checklist at end: 7 items that let CTO verify a DS-authored benchmark without re-authoring queries.
    6. `query_schema.py validate_queries_file()` accepts populated QUERY_MATRIX template (pytest test case).
    7. Session log Compiler Tools per Rule 7.
    8. MCP COMPLETE to COO with commit hash + SOP path.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md | head -100</run>
        <expect>7-step protocol readable; 5 dims + 6 Goodhart modes identified.</expect>
        <if_mismatch>Escalate — framework missing.</if_mismatch>
      </step>
      <step>
        <run>cat docs/architecture/COMP_LEARNS_HTTPX_TARGET.md | head -60</run>
        <expect>PRD #2 pattern visible; SOP distills this.</expect>
        <if_mismatch>Reconcile.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -c "from comp.framework.query_schema import validate_queries_file; validate_queries_file('comp/framework/templates/QUERY_MATRIX.yaml.template')"</run>
        <expect>Template validates OR raises expected-missing-required-fields (valid skeleton vs valid queries).</expect>
        <if_mismatch>Align template with schema validator expectations.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>ls comp/framework/templates/</run>
        <expect>4 template files listed.</expect>
        <if_mismatch>Missing files; fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.1.0_DS_CompLearns" task="COMP_LEARNS.001" status="complete" description="query_schema.py needed for template validation"/>
    <dependency agent="1.0.0_SA_CTO" task="COMP_LEARNS_QUALITATIVE_FRAMEWORK authoring" status="complete" description="7-step protocol is source material"/>
  </dependencies>

  <next>On commit: DS lanes can author future target harnesses under CTO spot-check (4-6 CTO hrs → <1 CTO hr per target). Unlocks PRD #2-style work for targets 2, 3, N.</next>
</task_order>
