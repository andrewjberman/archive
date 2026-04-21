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
    <ref type="prd_section">docs/architecture/COMP_LEARNS_TARGET_CLOSEOUT.md v2.0 §5 — 2 hard minimums (parser-proven + gold-authorable) + 2 weights (subtype leverage + size ceiling) + 3 disqualifiers. Each maps to a named prior failure mode; content kept despite v2.0 overall trim.</ref>
  </references>

  <objective>
    Decision memo — not a build TO — selecting target 2 and scoping initial surface count + query budget.

    **Selection criteria (per COMP_LEARNS_TARGET_CLOSEOUT.md §5 v1.1 — 2 hard minimums + 2 weights):**

    **Hard minimums (pass/fail; failing any one excludes the candidate):**
    1. Parse cleanness — candidate's language has a parser ALREADY proven on at least one `comp/` codebase (Python/LibCST after `.012`; TypeScript/tree-sitter requires coverage-audit extension first). "We'll stand up a new parser" does NOT qualify — those candidates are excluded at the gate, not weight-scored.
    4. Gold-authorable — CTO writes one paragraph in the memo explicitly judging the 2-hour authoring budget feasible per the `.016` httpx precedent. Candidates where that paragraph cannot be written (specialist domain knowledge genuinely required — cryptography, compilers, ML frameworks) are excluded at the gate.

    **Weights (scored 1-5, higher is better; total is tiebreaker between qualifying candidates):**
    2. Subtype leverage — for v0.1 (same subtype as target 1, `imports`): higher score for candidates whose import patterns genuinely differ from httpx (heavier conditional dispatch, registry-based plugins). For v0.2+ (new subtype): higher for candidates exercising the subtype naturally.
    3. Size ceiling — smaller within the ≤5000 LOC range = higher score (shorter iter time, cleaner scorecard).

    **Hard disqualifiers (per TARGET_CLOSEOUT §5, any one excludes the candidate — same bar as the two hard minimums above):**
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
    2. Gate evaluation table (per v1.1 §5) — every candidate evaluated against the 5 hard bars (2 hard minimums: parser-proven + gold-authorable; 3 disqualifiers: metaprogramming / non-sonnet LLM / opal-internal). Pass/fail per bar per candidate. Excluded candidates named with one-sentence explanation; NOT scored on weights.
    3. Weight-scoring table for surviving (passes-all-gates) candidates only — 1-5 on each of the 2 weights (subtype leverage, size ceiling); total weight-score breaks ties.
    4. Estimated surface count for the chosen target (e.g., "pydantic has ~6 primary surfaces: validators, model config, fields, types, serializers, errors").
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
    2. **Gate table (per v1.1 §5):** every candidate evaluated against the five hard bars (2 hard minimums + 3 disqualifiers); pass/fail per bar; any fail = candidate excluded with one-sentence explanation. Then the surviving candidates scored 1-5 on the two weights (subtype leverage, size ceiling); total weight-score per qualifying candidate is the tiebreaker. Memo MUST present the gate evaluation BEFORE the weight scoring — excluded candidates don't get scored at all.
    3. Surface count estimate for the chosen target (e.g., "pydantic has ~6 primary surfaces: validators, model config, fields, types, serializers, errors").
    4. Query budget estimate; defensible against httpx's 24-question precedent.
    5. Repo pin sha identified (or explicit "will pin at TO-authoring time").
    6. Projected timeline with dependencies (needs PRD #2-analog authoring via SOP #008 ideally).
    7. **Gate evidence cited:** memo opens with a one-sentence citation that target 1 has reached either (a) primary_metric ≥ 0.25 at some iter (honor) or (b) ≥3 distinct mechanism-level learnings in an exhaustion close-out per TARGET_CLOSEOUT v2.0 §5. "Distinct mechanism" is CTO judgment, not a formal uniqueness rule. If neither condition holds, the TO should not have been picked up — next action is target-1 diagnostic, not target-2 authoring.
    8. Session log — CTO's decision process reproducible; Rule 7 audit.
    9. MCP COMPLETE to 2.1.0_SA_COO with commit hash.
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
