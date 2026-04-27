<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-084-ds-path-b-candidate-survey</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.4.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — Path B target re-selection input; parallel with COO sub-PRD authoring (per CTO direction 20260427T20:50Z)</priority>
  </metadata>

  <references>
    <ref type="cto_direction">CTO MCP 20260427T20:50Z to COO -- "Deploy 1.4.0_DS for candidate survey" — explicit assignment of this lane</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §7.2 (Path B candidates) + §11.5 (HOLD release) + V1.2 ship-blocker checklist</ref>
    <ref type="closeout_brief">CTO brief-supplement (74145edc) -- sphinx q03/q05 pilot DEMOTE_CEILING + sphinx fully closed; Path B is sole path forward</ref>
    <ref type="cvo_brief">CVO Q1 V1.2 acceptance pending .083 fix; this candidate survey can run in parallel</ref>
  </references>

  <objective>
    Survey 4-6 candidate libraries for Path B target re-selection. Assess each against CTO criteria
    framework (REQUIRED + PREFERRED) and emit a structured candidate report that COO + CTO use as
    input to sub-PRD authoring + ruling.

    ## Context

    Sphinx Path A failed: exact-match grader masking semantic-prior-unparseable revealed that ~12 of
    12 questions were prior-dominated. V1.2 grader-governance fixes the masking; Path B target
    re-selection chooses a NEW target where the parametric prior is genuinely low.

    1.4.0_DS has been on standby since wave 3b. Appropriate use of capacity. This is parallel work
    with COO Path B sub-PRD authoring (which is HELD until .083 P0 bug fix lands; 1.3.0_DS in flight).

    ## Phase 0 — Read CTO selection criteria

    Read these references in full before surveying:
    - docs/architecture/COMP_LEARNS_STAGE3.md §7 (Path A/B target selection) + §11.4-§11.5 (V1.2 governance gating)
    - docs/architecture/COMP_LEARNS_PHASE2_PROTOCOL_AMENDMENT.md §1 (target criteria 1-3)
    - CTO brief in COO inbox 20260427T20:50Z (Path B sub-PRD authoring direction) — propagated below

    REQUIRED criteria (all must be satisfied jointly):
    1. **Low parametric prior** — model knowledge cutoff ~Aug 2025; targets must be either
       (a) released or substantially modified post-cutoff OR (b) low online presence
       (small Github star count, sparse Stack Overflow / blog coverage)
    2. **Cross-file semantic joins required** (Phase 2 amendment §1 criterion 2)
    3. **Named entry not adjacent to fix site** (Phase 2 amendment §1 criterion 3)
    4. **Sufficient question diversity for INCLUDE pool ≥ 5 post-triage** — pre-screen yields
       ≥ 12 candidate questions with structural variety (numeric / enumerable / set_membership /
       code-extraction). Not all set_membership.
    5. **Question types compatible with V1.2 dual-grader** — semantic_grader.py handles all 6
       R-SC-2 labels. Avoid types systematically producing semantic-ambiguous or partial-correct.

    PREFERRED (tiebreaker):
    6. Operational familiarity (existing harness patterns reusable)
    7. Curation cost low (gold key generation tractable for small team)
    8. Reasonable size: ≥ 10k LOC for cross-module joins to matter; ≤ 200k LOC for H3 baseline tractability

    OUT-OF-BOUNDS:
    - Internal/proprietary codebases (program claims of generality require public)
    - Single-file libraries (no cross-module joins)
    - Targets prior-dominated under semantic-aware triage (Path B exists to escape that)

    ## Phase 1 — Survey 4-6 candidate libraries

    For each candidate, gather and document:
    - Name + GitHub URL + stars + initial-release date + last-major-update date
    - Brief structural description (~3 sentences: domain, architecture, why cross-module joins matter)
    - Prior-strength assessment (how much pre-2025-08 online coverage exists; rough estimate of model familiarity)
    - Candidate question pool richness (could ≥ 12 measurement-room questions be authored from the codebase?)
    - Question type variety (would the pool exceed pure set_membership? would it include numeric/enumerable/code-extraction?)
    - Harness adaptation cost (rough effort to wire repo_pin + ab_questions/ab_answer_key to existing comp/targets/ infrastructure)
    - Pinned commit candidate + roughly when (within last 6 months)
    - REQUIRED criteria check: 5/5? Any not met?
    - PREFERRED criteria score: 3/3? 2/3? 1/3?
    - OUT-OF-BOUNDS check: clear?

    Suggested seeds (you may use these or substitute as you research; the goal is 4-6 strong candidates):
    - **Modern Python frameworks released post-Aug 2025** (low parametric prior by construction)
    - **Domain-specific scientific libraries** (low online presence; low parametric prior)
    - **Recently-rewritten internal-replacements that went open-source** (cross-module joins by structure)
    - Examples to consider/reject explicitly (don't just include all):
      - litellm (popular, high prior — likely OUT)
      - polars-extension libraries (recent, niche — possibly IN)
      - rio (Python web framework, post-cutoff — possibly IN)
      - any post-cutoff fork or successor of well-known libraries

    DO NOT surface candidates that are obvious priors (django, flask, fastapi, requests, click,
    sphinx, sqlalchemy, etc.). Those are already prior-dominated.

    ## Phase 2 — Emit structured candidate report

    Author at:
    ```
    comp/results/path_b_candidates/candidate_survey.md
    ```

    Structure:
    - §1 Executive summary (1 paragraph + ranked candidate list)
    - §2 Methodology (criteria framework — list, not prose)
    - §3 Candidate-by-candidate assessment (one §3.X subsection per candidate; same fields for each)
    - §4 Recommendation (1-3 candidates flagged for COO sub-PRD inclusion + 1-3 for explicit rejection with rationale)
    - §5 Open questions / asks for COO+CTO (any criteria ambiguity surfaced; any candidate that scores well on REQUIRED but fails one PREFERRED — surface, don't auto-decide)

    ## Phase 3 — Validation pass

    For each candidate, attempt to find at least 2 candidate questions you would author from the
    codebase. Sketch them in §3.X (1-2 sentences each, no formal authoring). The point is to
    convince yourself + reviewers that the question pool is plausible — not to author the actual pool.

    If you can't sketch 2 plausible candidate questions for a target, score it lower on criterion 4
    or drop it from the survey.

    ## Phase 4 — Commit and push

    Note: this is doc-only work. No Python source changes; no ds-commit-gate.sh required.

    ```bash
    mkdir -p comp/results/path_b_candidates
    git add comp/results/path_b_candidates/candidate_survey.md
    git commit --only \
      --author="1.4.0_DS_CompLearns <1.4.0_DS_CompLearns@opal.agent>" \
      -m "doc(COMP_LEARNS.084): Path B candidate survey -- N candidates assessed against V1.2 criteria" \
      -- comp/results/path_b_candidates/candidate_survey.md
    git push origin CLOUD
    ```

    ## Phase 5 — MCP

    MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with:
    - Commit sha
    - Number of candidates surveyed (4-6)
    - Top 1-3 recommended candidates (briefly)
    - Any criteria ambiguity surfaced for COO/CTO ruling
    - Estimated time spent (helps calibrate future research-survey TOs)
  </objective>

  <compiler_tools_mandate>
    <note>This TO is doc-only research. No Python edits; no ds-commit-gate.sh.
    The deliverable is a structured assessment, not code.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .083 (1.3.0_DS bug fix) and COO Path B sub-PRD authoring (HELD until .083 + V1.2→V1.3 sync).
      This survey is INPUT to the sub-PRD; COO uses it for candidate proposals to CTO.
      Do NOT pre-decide the target — surface options + assessments. CTO rules the final selection.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/results/path_b_candidates/ directory created.
    2. candidate_survey.md authored with §1-§5 structure.
    3. 4-6 candidates assessed; each with all REQUIRED + PREFERRED criteria scored.
    4. ≥ 2 plausible candidate questions sketched per surfaced candidate (Phase 3).
    5. Top 1-3 candidates flagged for COO sub-PRD inclusion.
    6. Any out-of-bounds candidates explicitly rejected with rationale.
    7. Open questions / criteria ambiguity surfaced (do NOT silently resolve).
    8. Committed --only --author=1.4.0_DS_CompLearns. Pushed to CLOUD.
    9. MCP COO + CC CTO with commit sha + candidate count + top picks.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallel with .083 (1.3.0_DS bug fix) and COO Path B sub-PRD authoring.
    - COO Path B sub-PRD consumes this survey output before dispatching to CTO.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - This is research; you may use WebFetch/WebSearch to gather GitHub star counts, release dates,
      online-presence signals. Cite sources in the survey for auditability.
    - Do NOT install or pin any candidate's repo. Just describe what would be needed.
    - Do NOT author actual ab_questions.yaml / ab_answer_key.yaml content -- only sketch candidate
      questions in 1-2 sentences (Phase 3) for convincibility.
    - You have been idle since wave 3b standby. Welcome back.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO
    - session log
  </closeout>
</task_order>
