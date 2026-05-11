<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.ID-DTYPE-ENFORCEMENT</id>
    <project>ADVI_INFNNA</project>
    <title>Pre-commit gate enforcement — extend .tools/ds-precommit-check.py to detect silver builders missing canonical ID dtype coerce; going-forward rigidity</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>staged</status>
    <priority>medium</priority>
    <estimated_effort>~1-2h</estimated_effort>
    <authorized_by>Andrew direct 2026-05-11 ("we need to be rigid on it moving forward")</authorized_by>
  </metadata>

  <references>
    <ref type="parent_to_1">ADVI_INFNNA.SILVER-ID-DTYPE-UNIFY `81c9212d0` — establishes Int64 canonical convention in silver builders</ref>
    <ref type="parent_to_2">ADVI_INFNNA.ACCOUNT-ID-COERCE `5287179fb` — gold-side belt-and-suspenders coerce_id_columns helper</ref>
    <ref type="enforcement_tooling">.tools/ds-precommit-check.py — existing AST-based undefined-name scanner per CLAUDE.md rule 14 (`b6e0c154` + `7b7381ac`)</ref>
    <ref type="bash_compat_constraint">CLAUDE.md rule 16 — Git Bash 3.6.7 available utilities only</ref>
  </references>

  <context>
    Once SILVER-ID-DTYPE-UNIFY establishes the Int64 canonical convention, the system needs **structural enforcement** so future silver builders can't accidentally re-introduce dtype drift. Cultural rules are insufficient (proven by the 3-class commit-sweep incidents 2026-04-27 that drove safe-commit.sh).

    **Enforcement mechanism:** AST-based pre-commit check. Extend `.tools/ds-precommit-check.py` to:
    1. Detect Python files under `data/*/scripts/silver/` modified in commit
    2. For each `build_*` function, scan for `coerce_silver_ids(...)` call before `return df[cols]`
    3. If `build_*` function returns a DataFrame without calling `coerce_silver_ids`, ERROR with file:line:reason
    4. Also detect: explicit `.astype(str)` calls on any column named `*_id` (regression check — the old accounts_v2 pattern shouldn't reappear)

    This makes the convention **structurally impossible to violate** without explicitly bypassing the gate (which leaves an audit trail via `GIT_COMMIT_AUTHOR_OVERRIDE=ANY_EXEC` per existing escape hatch).

    Same category as CLAUDE.md rule 14's existing py_compile + undefined-name + ruff stack. This adds a domain-specific check on top.
  </context>

  <scope>
    <step>
      **Read existing precommit-check architecture.** `.tools/ds-precommit-check.py` is AST-based per `b6e0c154`. Understand current scanner pattern, error format, exit-code convention.
    </step>

    <step>
      **Design the new check.** AST visitor that:
      - Visits all `FunctionDef` nodes matching `^build_.*` in scripts under `data/*/scripts/silver/`
      - For each, walks the function body
      - Tracks whether any `Call` node matches `coerce_silver_ids(...)` (or whatever final naming SILVER-ID-DTYPE-UNIFY commits to)
      - Tracks whether function returns a DataFrame (heuristic: `return <expr>` where expr is df-shaped — accept loose heuristic + document edge cases)
      - If function returns DataFrame but never calls coerce helper: ERROR

      Separate check: visits all `Call` nodes matching `.astype('str')` or `.astype(str)` where the object being cast appears to be a column ending in `_id`. Heuristic, may have false positives — surface those for manual confirmation rather than hard-block.
    </step>

    <step>
      **Implement + test.** Write the check code. Build 3 synthetic test fixtures:
      - **PASS:** build_x function that calls coerce_silver_ids before return
      - **FAIL (missing coerce):** build_x function that returns df without coerce
      - **FAIL (regression astype):** build_x function with `df['account_id'] = df['account_id'].astype(str)`

      Fixtures live at `.tools/test_fixtures/ds-precommit-check/` or similar canonical path. Run via `.tools/test_ds_precommit_check.py` (parallel to the existing tool itself).
    </step>

    <step>
      **Update CLAUDE.md rule 14 reference.** Add a sentence to rule 14 noting that ds-precommit-check now includes silver-canonical-ID enforcement (rule 17 candidate or sub-rule of 14). Keep edit minimal — just one sentence.

      Coordinate with CTO before editing CLAUDE.md (it's a high-bar workspace file).
    </step>

    <step>
      **Validate against current codebase.** Run the enhanced check across all existing silver builders (post SILVER-ID-DTYPE-UNIFY landing). Should be 100% PASS.

      If any existing builder fails: surface to COO — likely a missed builder in SILVER-ID-DTYPE-UNIFY's coverage.
    </step>

    <step>
      **Bash compat verification.** Per CLAUDE.md rule 16, the local-runtime script must rely only on Git Bash 3.6.7 utilities. Python-based AST check is fine (Python is in the "present" column). No pgrep/pkill/etc dependencies expected.
    </step>

    <step>
      **Memory entry.** Author `feedback_silver_id_dtype_enforcement_gate.md` documenting the gate behavior, the bypass escape hatch, and the rationale.
    </step>

    <step>
      **Commit + push + RAVC.** Bundle:
      - Updated `.tools/ds-precommit-check.py`
      - Test fixtures + test runner
      - Memory entry
      - (Coordinated) CLAUDE.md rule 14 edit
      - Author: `0.4.0_DS_ClientPlatform~B`

      RAVC payload:
      - 100% PASS confirmation against current silver builders
      - 3-fixture test result (PASS/FAIL/FAIL as expected)
      - CLAUDE.md edit coordination outcome with CTO
      - Memory entry path
    </step>
  </scope>

  <acceptance_criteria>
    1. **AST check** implemented in `.tools/ds-precommit-check.py`.
    2. **3 synthetic fixtures** in canonical path; runner script PASS/FAIL/FAIL as expected.
    3. **100% PASS** validation against current silver builders (post SILVER-ID-DTYPE-UNIFY).
    4. **CLAUDE.md rule 14** updated with reference to canonical ID enforcement (CTO-coordinated).
    5. **Bash 3.6.7 compat** verified (Python + stdlib only; no missing utility dependencies).
    6. **Memory entry** drafted.
    7. **RAVC delivered** with fixture test results + CLAUDE.md edit outcome.
  </acceptance_criteria>

  <blocking>
    **Blocked by:** ADVI_INFNNA.SILVER-ID-DTYPE-UNIFY `81c9212d0` completion. Need a clean post-unification silver corpus + finalized coerce helper naming before pre-commit gate can lock against it.

    Adjacent: A-GROUP-AUDIT can run in parallel (orthogonal scope). DS~B picks up A-GROUP-AUDIT first; this TO is the second DS~B pickup.
  </blocking>

  <notes>
    **Going-forward rigidity:** This TO is the structural enforcement that makes the canonical Int64 convention non-bypassable without explicit audit-logged override. Same defense pattern as safe-commit.sh's `--force` escape hatch.

    **Tooling owner = DS~B going forward:** if DS~B builds this gate, they become the natural owner for future enhancements (e.g., extending to non-ID column type conventions, etc.). Reasonable lane fit.

    **CLAUDE.md edit coordination is the only cross-lane element** — `1.0.0_SA_CTO` should ratify the rule-14 wording. Send a draft to CTO before committing; expect minor wording tweaks.
  </notes>
</task_order>
