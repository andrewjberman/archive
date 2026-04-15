<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-15-comp-learns-009-target-2-selection</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO</issued_to><!-- CTO-execution TO per CTO 19:55Z punchlist — decision authority on target 2 candidate + initial scope -->
    <date>2026-04-15</date>
    <status>staged</status><!-- Gate: worktree fix landed (done 2cb83eb6) + target 1 Phase 1 passes. -->
    <project_code>COMP_LEARNS</project_code>
    <priority>P2 — post target-1 Phase 1 success</priority>
  </metadata>

  <references>
    <ref type="cto_directive">CTO msg 19:55Z punchlist #009 — candidates: pydantic / sqlalchemy core / starlette / small internal service. Must NOT be opal-capital.</ref>
    <ref type="precedent">docs/architecture/COMP_LEARNS_HTTPX_TARGET.md (PRD #2 shape — repo pin + ~50 queries + harness + answers)</ref>
    <ref type="doctrine">docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md</ref>
    <ref type="sop">docs/architecture/COMP_LEARNS_BENCHMARK_AUTHORING_SOP.md (shipping via #008; reduces target-2 authoring time)</ref>
  </references>

  <objective>
    Decision memo — not a build TO — selecting target 2 and scoping initial surface count + query budget.

    Decision drivers (per qualitative framework):
    - Different surface area from httpx (avoid overfit to HTTP-client patterns)
    - Unfamiliar to agents (no training-data memorization shortcut)
    - Similar scale (~5-15K LOC) so authoring stays tractable
    - Python-first (reuses PRD #1 framework subprocess contract)

    Candidates CTO weighs:
    - `pydantic` (validation + schema; different surface than HTTP; widely-used but core is tight)
    - `sqlalchemy` core (ORM/expression language; cross-surface: dialects + engine + core)
    - `starlette` (ASGI toolkit; closer to httpx, might be too similar)
    - small internal service (TF + Python) — Opal-agnostic only if truly shareable
    - other OSS

    Output: decision memo at `docs/architecture/COMP_LEARNS_TARGET_2_SELECTION.md` with:
    1. Chosen target + rationale
    2. Estimated surface count (from `comp-pipescript`-equivalent passes if CTO wants)
    3. Estimated query budget (tighter than httpx's 50 if using SOP to delegate authoring)
    4. Repo pin strategy
    5. Projected Phase 1 completion timeline
  </objective>

  <scope>
    <files>
      <file action="create">docs/architecture/COMP_LEARNS_TARGET_2_SELECTION.md</file>
    </files>
  </scope>

  <wire_contract>
    Decision memo is informational; commits the target-2 scope so downstream PRDs (analogous to PRDs #1-#5 but for target 2) can be authored.

    Not a PRD itself — scopes the decision, PRDs follow.
  </wire_contract>

  <acceptance_criteria>
    1. Memo at path; ≤150 lines; explicit decision with rationale.
    2. Surface count estimate (e.g., "pydantic has ~6 primary surfaces: validators, model config, fields, types, serializers, errors").
    3. Query budget estimate; must be defensible against httpx's 50-query precedent.
    4. Repo pin sha identified (or explicit "will pin at TO-authoring time").
    5. Projected timeline with dependencies (needs PRD #2-analog authoring via SOP #008 ideally).
    6. Session log — CTO's decision process reproducible; Rule 7 audit.
    7. MCP COMPLETE to COO with commit hash.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md | grep -E "target|surface"</run>
        <expect>Qualitative framework surface-dimensionality criteria visible.</expect>
        <if_mismatch>Re-read.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>wc -l docs/architecture/COMP_LEARNS_TARGET_2_SELECTION.md</run>
        <expect>≤150 lines.</expect>
        <if_mismatch>Tighten.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>grep -E "^\- " docs/architecture/COMP_LEARNS_TARGET_2_SELECTION.md</run>
        <expect>5 acceptance fields enumerated.</expect>
        <if_mismatch>Structural gap — fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="target-1-phase-1" task="target 1 (httpx) passes Phase 1 iteration loop" status="pending" description="gates target-2 PRD authoring, not the decision memo"/>
  </dependencies>

  <next>On commit: COO authors target-2 harness PRD analog (via SOP #008 if shipped) → DS lane (via SOP #008) or CTO-solo (per httpx precedent if SOP not yet available).</next>
</task_order>
