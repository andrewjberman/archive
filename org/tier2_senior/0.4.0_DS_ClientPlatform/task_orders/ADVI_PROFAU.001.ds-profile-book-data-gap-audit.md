<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-13-profau-001</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>pending</status>
    <project_code>ADVI_PROFAU</project_code>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/advi-profau-ds-audit-brief.md</ref>
    <ref type="audit">docs/audits/advisor-profile-book-input-mapping-2026-04-13.md</ref>
    <ref type="project">org/projects/ADVI_PROFAU.json (CTO registering)</ref>
  </references>

  <objective>
    Produce a single structured audit response covering 7 backend data gaps surfaced from today's advisor-profile/book number-tie audit. For each gap: label (LIVE / MISSING-COLUMN / MISSING-ROLL-UP / MISSING-ARTIFACT / DEPRECATED), canonical-source recommendation, proposed chain insertion point, and follow-up TO hooks. No implementation in this TO — pure audit output. DS then spawns follow-up TOs per confirmed gap under `ADVI_PROFAU.002+`.
  </objective>

  <context>
    DE 0.4.0's audit doc at `docs/audits/advisor-profile-book-input-mapping-2026-04-13.md` (CLOUD c2efa4a7) has the DE column complete — every rendered field on `AdvisorPublicProfile` / `AdvisorBookView` L2/L3/L4 / shared panels is mapped to its source artifact and status. RD column is in flight but orthogonal; do NOT wait for it.

    The 7 questions are in the brief at `docs/briefs/advi-profau-ds-audit-brief.md`. Q1-Q6 are verbatim DE findings; Q7 is the `fee_earning_aua` vs `sum(role.fee_paying.aua)` canonical-source pick explicitly tied to the W6-002 allChecked fix + the in-flight D_00c 3-case split-allocation rule (DE's informal "W6-005" work).
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing audit):
    - `comp-pipescript io D_00c` — what D_00c currently produces/consumes.
    - `comp-pipescript io D_04` — which artifacts D_04 emits to platinum.
    - `comp-trace employee_leaderboard --direction both --all` — full chain for leaderboard fee fields.
    - `comp-transform schema-check AdvisorBookView` — current prop shape contract.
    - `comp-transform schema-check AdvisorPublicProfile` — current prop shape contract.
    - Grep `fee_summary`, `total_market_value`, `PlatinumAdvisorSummary`, `role_breakdown`, `capital_gains_ttm`, `cost_basis_by_year`, `top_gain_positions`, `is_fee_paying` across `portal/src/pages/AdvisorIntelligence/` + `data/black_diamond/scripts/gold/` to seed the LIVE/MISSING labels.

    Phase 2 (before committing response doc):
    - For each LIVE claim: cite grep or line reference proving emission.
    - For each MISSING claim: cite a compiler/grep run proving absence.
    - Re-run `comp-transform schema-check` on both components to confirm the Q6 type-drift diagnosis.

    Phase 3 (after commit):
    - Append one line per compiler run to `org/compiler-tools-log.md`.
    - MCP-message 0.4.0_DE_ClientPlatform with the response doc path so DE can pre-spec wiring TOs in parallel.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <!-- Pure DS audit. No shared-file writes. DE is the downstream consumer but only of the response doc — not of code. Parallel with RD's audit-doc column. -->
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Single response doc at `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/profaup_gap_audit_response.md` covering all 7 questions (path per CTO scoping — do NOT rename).
    2. Each gap carries: LIVE / MISSING-COLUMN / MISSING-ROLL-UP / MISSING-ARTIFACT / DEPRECATED label + evidence line (grep or compiler ref).
    3. Each gap carries: canonical-source recommendation (gold script + field name) when LIVE; proposed chain insertion point (which script, column name or new artifact path) when MISSING.
    4. Each gap identifies whether follow-up work is one-liner column-add, multi-script work, or deprecation removal — this drives `.002+` TO granularity.
    5. Q7 explicitly names which field (`fee_earning_aua` or `sum(role_breakdown[role].fee_paying.aua)`) should be canonical at the advisor-profile headline and whether the non-canonical should be deprecated anywhere on the platinum surface.
    6. Compiler Tools section in the response doc logs every Phase 1 + Phase 2 run with pass/fail + output summary.
    7. MCP signal sent to 0.4.0_DE_ClientPlatform on doc commit so they can begin parallel wiring-TO pre-spec.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/profaup_gap_audit_response.md</file>
    </files>
  </scope>

  <requirements>
    - Pure audit; no gold-script edits, no platinum re-emits, no schema changes in this TO.
    - If an in-flight change (D_00c 3-case split-allocation) affects a gap's answer, note the dependency and what the post-landing answer becomes.
    - Follow the brief's question ordering Q1-Q7 so downstream TOs map 1:1.
  </requirements>

  <deliverables>
    - Commit to CLOUD with `--author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>"`.
    - Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-13/profau_001_data_gap_audit.md` with Compiler Tools section.
    - `org/compiler-tools-log.md` entries.
    - MCP message to 0.4.0_DE with doc path on commit.
    - Flip `<status>pending</status>` -> `complete` after acceptance criteria 1-7 validated.
  </deliverables>

  <do_not>
    - Do NOT implement any schema change in this TO. All follow-ups become `ADVI_PROFAU.002+`.
    - Do NOT wait for the RD column on the audit doc — orthogonal.
    - Do NOT reopen ADVI_PROFIL or ADVI_REBORN — both closed; this is a clean-start project.
    - Do NOT skip Q7 because the fix is in-flight — note the dependency explicitly.
  </do_not>
</task_order>
