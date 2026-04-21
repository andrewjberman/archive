<task_order>
  <metadata>
    <id>1.1.0_SA_CTO-2026-04-15-comp-learns-009-target-2-selection</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.1.0_SA_CTO</issued_to><!-- Transferred 2026-04-21 from 1.0.0_SA_CTO per COMP_LEARNS_TARGET_CLOSEOUT.md §7.2. Scope amended same commit per §8.4 — selection criteria now anchored in TARGET_CLOSEOUT §5 (weights-not-filters + hard disqualifiers) + gate tightened per §5 evidence bar. Original authorship date + issuer preserved. -->
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
    <ref type="prd_section">docs/architecture/COMP_LEARNS_TARGET_CLOSEOUT.md §5 — selection criteria (weights-not-filters) + hard disqualifiers + gate evidence bar</ref>
  </references>

  <objective>
    Decision memo — not a build TO — selecting target 2 and scoping initial surface count + query budget.

    **Selection criteria (per COMP_LEARNS_TARGET_CLOSEOUT.md §5, weights-not-filters, score each candidate 1-5):**
    1. Parse cleanness — Python (LibCST, shipped) default; TypeScript / Go acceptable v0.1+ with coverage audit. Lua / Rust / Haskell / anything without a proven extractor is rejected.
    2. Subtype leverage — v0.1 uses same subtype (`imports`) as target 1 to test cross-target generalization; v0.2+ may introduce a new subtype.
    3. Size ceiling — ≤ 5000 LOC for v0.1; larger targets deferred to v0.3+ once the loop runs unattended.
    4. Gold-authorable — plain-English ground-truth within a 2-hour CTO authoring budget per the `.016` precedent.

    **Hard disqualifiers (per TARGET_CLOSEOUT §5, any one excludes the candidate):**
    - Extensive metaprogramming (`exec`, `eval`, import-time codegen, runtime class synthesis).
    - Dependency on an LLM beyond `claude-sonnet-4-6`.
    - Opal-internal code.

    **Gate for when this TO becomes pickup-ready (per TARGET_CLOSEOUT §5):** target 1 has reached either PLATEAU_WITH_HONOR (primary_metric ≥ 0.25) OR PLATEAU_BY_EXHAUSTION with ≥ 3 promoted learnings in `program.md`. If neither holds, this TO stays staged and the next action is a target-1 diagnostic audit, not target-2 authoring.

    Candidates CTO weighs (illustrative — full scoring in the memo):
    - `pydantic` (validation + schema; different surface than HTTP; widely-used but core is tight)
    - `sqlalchemy` core (ORM/expression language; cross-surface: dialects + engine + core)
    - `starlette` (ASGI toolkit; closer to httpx, might be too similar)
    - `click` (CLI toolkit; small core, structurally different from HTTP)
    - other OSS

    Output: decision memo at `docs/architecture/COMP_LEARNS_TARGET_2_SELECTION.md` with:
    1. Chosen target + rationale.
    2. Per-candidate scoring table (1-5 on each of the four §5 criteria).
    3. Explicit disqualifier check per candidate (pass/fail on each of the three hard disqualifiers).
    4. Estimated surface count (from `comp-pipescript`-equivalent passes if CTO wants).
    5. Estimated query budget (tighter than httpx's 24 if using SOP to delegate authoring).
    6. Repo pin sha identified.
    7. Projected Phase 1 completion timeline.
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
    2. **Scoring table:** every candidate scored 1-5 on each of the four TARGET_CLOSEOUT §5 criteria; total score per candidate visible.
    3. **Disqualifier check table:** every candidate evaluated against all three hard disqualifiers; pass/fail per disqualifier; any fail = candidate excluded with one-sentence explanation.
    4. Surface count estimate for the chosen target (e.g., "pydantic has ~6 primary surfaces: validators, model config, fields, types, serializers, errors").
    5. Query budget estimate; defensible against httpx's 24-question precedent.
    6. Repo pin sha identified (or explicit "will pin at TO-authoring time").
    7. Projected timeline with dependencies (needs PRD #2-analog authoring via SOP #008 ideally).
    8. **Gate evidence cited:** memo opens with a one-sentence citation that target 1 has reached either PLATEAU_WITH_HONOR or PLATEAU_BY_EXHAUSTION-with-3-promoted-learnings per TARGET_CLOSEOUT §5. If neither holds, the TO should not have been picked up.
    9. Session log — CTO's decision process reproducible; Rule 7 audit.
    10. MCP COMPLETE to 2.1.0_SA_COO with commit hash.
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
