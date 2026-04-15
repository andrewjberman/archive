<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-comp-learns-010-comp-lint-decomp</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- Any DS lane; CTO flagged as "any lane" in 19:55Z punchlist. Router picks based on who's free. -->
    <date>2026-04-15</date>
    <status>staged</status><!-- Flips pending when a DS lane is free AND engineer-provided PRD doc N1 is committed to docs/architecture/. -->
    <project_code>COMP_LEARNS</project_code>
    <priority>P2 — ships last in compiler-upgrade tranche</priority>
  </metadata>

  <references>
    <ref type="cto_directive">CTO msg 19:55Z punchlist #010 — "8-category coverage-audit pass over the graph. Engineer has the edited proposal doc."</ref>
    <ref type="prd_pending">docs/architecture/COMP_LEARNS_N1_COMP_LINT.md (engineer-authored, PENDING commit — this TO instantiates it)</ref>
  </references>

  <objective>
    Decomposition TO for a new `comp-lint` tool. 8-category coverage-audit pass over the comp graph —
    surfaces drift, un-tested edges, schema holes, un-compiled entry points. Engineer has the edited
    proposal doc (CTO cites as "PRD N1"); this TO instantiates it into an implementation plan.

    Does NOT author the tool itself — that's a downstream TO post-decomposition. THIS TO produces:
    - An implementation-order plan (which of the 8 categories first, why)
    - Interface spec for `comp-lint <scope>` + subcommands
    - Test coverage target (min N cases across the 8 categories)
    - Integration points with existing comp-* tools (blast, pipescript, transform, validate)
    - Ship order (coord with ADHC_ROUTER P2 compiler-upgrade work — may share modules)
  </objective>

  <scope>
    <files>
      <file action="create">docs/architecture/COMP_LEARNS_N1_IMPLEMENTATION_PLAN.md</file>
    </files>
  </scope>

  <wire_contract>
    Implementation plan ≤ 150 lines. Enumerates 8 categories with:
    - What the category audits (concrete, e.g., "schema drift between gold_validate_config.yaml and live scripts")
    - How it detects (pattern: grep + parse + cross-reference)
    - What it emits (stdout format + exit code conventions)
    - Shared state with existing comp-* (graph reads? state writes?)

    Does NOT specify every line of code — that's for downstream TO(s).
  </wire_contract>

  <acceptance_criteria>
    1. Plan at path; ≤150 lines; 8 categories enumerated.
    2. Implementation order justified (which comes first + why; start with highest-signal lowest-cost).
    3. CLI interface spec: `comp-lint {category} [--scope X]`; exit codes match comp-* conventions (0 clean, 1 drift found, 2 error).
    4. Test-count target per category (e.g., "≥3 positive cases + ≥2 negative cases per category = ≥40 tests total").
    5. Coordination with ADHC_ROUTER P2 tranche: which compiler upgrades land first; any shared modules.
    6. Session log Compiler Tools per CTO Rule 7.
    7. MCP COMPLETE to COO with commit hash.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>ls docs/architecture/COMP_LEARNS_N1*</run>
        <expect>Engineer's proposal doc committed (PRD N1). If absent, gate on its commit — this TO decomposes that doc.</expect>
        <if_mismatch>Wait for PRD N1 commit; TO stays staged.</if_mismatch>
      </step>
      <step>
        <run>ls .tools/comp-*</run>
        <expect>Existing comp-* tools enumerated; plan identifies which share modules with comp-lint.</expect>
        <if_mismatch>n/a — baseline for integration-point mapping.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>wc -l docs/architecture/COMP_LEARNS_N1_IMPLEMENTATION_PLAN.md</run>
        <expect>≤150.</expect>
        <if_mismatch>Tighten.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>grep -cE "^## Category" docs/architecture/COMP_LEARNS_N1_IMPLEMENTATION_PLAN.md</run>
        <expect>8 — one section per category.</expect>
        <if_mismatch>Fix structure.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="engineer" task="PRD N1 COMP_LEARNS_N1_COMP_LINT.md commit" status="pending" description="source doc this TO decomposes"/>
  </dependencies>

  <next>On commit: downstream TO(s) for each compiler-upgrade category (likely 3-5 TOs across the 8 categories, grouped by integration point). Ships last in the ADHC_ROUTER P2 compiler tranche.</next>
</task_order>
