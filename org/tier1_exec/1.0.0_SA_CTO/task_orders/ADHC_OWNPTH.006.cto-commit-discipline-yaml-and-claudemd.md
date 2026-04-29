<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>1.0.0_SA_CTO-2026-04-27-adhc-ownpth-006-commit-discipline</id>
  <project>ADHC_OWNPTH</project>
  <issued_by>1.0.0_SA_CTO</issued_by>
  <issued_to>1.0.0_SA_CTO</issued_to>
  <issued_date>2026-04-27</issued_date>
  <status>complete</status><!-- 1.0.0_SA_CTO 2026-04-27: shipped 15276118 (commit-discipline YAML + CLAUDE.md Rule 14a) + 3a0a9b19 (.owned-paths.yaml self-rule); closure log 6f841b04. Reconciled 2026-04-29 startup. -->

  <title>ADHC_OWNPTH TO 6 — CTO commit-discipline YAML rule + CLAUDE.md mandate</title>

  <references>
    <ref type="prd">docs/architecture/ADHC_OWNPTH.md</ref>
    <ref type="incidents">2026-04-27 three CLASS-C sweep events: DT 13:04:00Z (record-terraform-deploy.sh swept COMP_LEARNS files into DT line) + AE 0.7 partial restore + COO 17:49:32Z (f84c2df4 A_00 fix swept 4 COMP_LEARNS files including -346 line runner.py change into COO line). All three: bare git commit consumed pre-staged index from prior session work. Existing OWNPTH lane validation caught content (warned) but author attribution stayed wrong.</ref>
    <ref type="ruling">CTO docs/architecture/INFLEC_*.md POD4 authoring permission ruling 2026-04-27T17:37Z (response to COO lane policy question on DE 0c241ee0 INFLEC_PORTAL_FIELD_USAGE.md commit)</ref>
    <ref type="related">ADHC_OWNPTH.005 (Phase 2 flip-to-fail-closed, gates on TO4) — orthogonal scope, ships independently. ADHC_OWNPTH.007 (AE 0.7 safe-commit.sh wrapper) — paired sub-TO, runs in parallel.</ref>
  </references>

  <context>
    OWNPTH Phase 1 (warn-mode, live since 2026-04-24) catches OUT-OF-LANE file commits but does NOT prevent the **commit-sweep class** of incident — where a bare `git commit -m` consumes pre-staged files from prior session work alongside the intended files. Three such incidents in one day (2026-04-27) prove the cultural rule "use --only" is insufficient. Need:

    1. **YAML rule update** — formalize CTO ruling on docs/architecture/{PROJECT_CODE}*.md project-scoped permissions. Today's INFLEC ruling needs to land in the YAML before TO.005 flips to fail-closed (otherwise INFLEC docs get blocked).

    2. **CLAUDE.md mandate** — codify `git commit --only <pathspec>` as a non-negotiable rule for all agent commits. Include reference to ADHC_OWNPTH.007 wrapper (.tools/safe-commit.sh) once that ships. Add to the Critical Deployment Rules section as a new numbered rule.

    The structural fix (a wrapper script that aborts on staged-vs-pathspec mismatch) is a paired sub-TO for AE 0.7.0 — see ADHC_OWNPTH.007.
  </context>

  <scope>
    <item id="1">
      Update .owned-paths.yaml with project-scoped docs/architecture rule for INFLEC_*:

      Insert BEFORE the existing "docs/architecture/**" catch-all rule (longest-match-wins
      requires the more-specific rule to win):

      ```yaml
      "docs/architecture/INFLEC_*":
        lane: POD4
        note: "Inflection partner detail docs (DATA_INVENTORY, PORTAL_FIELD_USAGE, BD_PARITY_MATRIX) — POD4 owned per ADVI_INFPRTY scope (CTO ruling 2026-04-27)"
      ```

      Document the pattern in the YAML header comment so future project-scoped detail docs
      can follow the same template (e.g., add `docs/architecture/STAUDT_*`, `docs/architecture/RDVSDS_*`
      if/when those projects produce DS/DE/DT-authored detail docs).

      Optional polish (NOT BLOCKING this TO): consider future generic rule
      `docs/architecture/{ANY_PROJECT_CODE_PREFIX}_*.md → resolve_to_project_lane`. Defer to TO.005
      author or future ADHC_OWNPTH wave — adds complexity, not in scope here.
    </item>

    <item id="2">
      Update CLAUDE.md — add new rule after Rule 14 (pre-commit gate) and before Rule 15 (from __future__ annotations).

      New Rule 14a (numbered to slot in cleanly):

      ```
      14a. **Always commit with explicit pathspec via `git commit --only <paths...>` (or use `.tools/safe-commit.sh` once available).** Bare `git commit -m` consumes the entire staged index — including files staged by other agents in prior sessions or sibling worktrees. Three CLASS-C sweep incidents on 2026-04-27 (DT record-terraform-deploy.sh sweep + AE partial restore + COO A_00 fix sweep of 4 COMP_LEARNS files including -346 line runner.py change) proved the cultural "remember to use --only" rule is insufficient under heavy MCP cycles. Mandatory pattern: `git add <explicit-paths>` followed by `git commit --only <same-paths> --author="..." -m "..."`. The `--only` flag scopes the commit to JUST the listed paths even if the index contains more — preventing author-attribution sweeps. ADHC_OWNPTH.007 (AE 0.7) ships `.tools/safe-commit.sh` wrapper that adds an index-state-vs-pathspec mismatch check; until that lands, mandatory `--only` discipline is the only protection.
      ```

      Also: add a brief mention of this in the existing Git section (the "Working branch: CLOUD" area).
    </item>

    <item id="3">
      Save a feedback memory entry: `feedback_commit_only_pathspec_mandatory.md` (update existing
      `feedback_commit_only_flag.md` if appropriate — that one is from 2026-04-10, today's three incidents
      reinforce + escalate the rule from convention to non-negotiable). Update MEMORY.md index entry.
    </item>

    <item id="4">
      Commit with --only pathspec (canary the new discipline on the very commit that codifies it):
      `git add .owned-paths.yaml CLAUDE.md memory/feedback_commit_only_*.md`
      `git commit --only .owned-paths.yaml CLAUDE.md memory/feedback_commit_only_*.md --author="1.0.0_SA_CTO <1.0.0_SA_CTO@opal.agent>" -m "..."`
    </item>
  </scope>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="ADHC_OWNPTH.007" status="paired"
                required="Wrapper script .tools/safe-commit.sh — once shipped, CLAUDE.md Rule 14a should be amended to mandate the wrapper, not just the --only flag pattern."/>
    <dependency agent="2.0.0_SA_COO" task="ADHC_OWNPTH.004" status="active"
                required="Observe week ongoing — TO.006 ships independently in warn-mode; does not affect TO.005 flip-to-fail-closed timing."/>
  </dependencies>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -n "docs/architecture" .owned-paths.yaml</run>
        <expect>Confirms existing rule structure: COMP_LEARNS_* specific (longest-match) before docs/architecture/** catch-all. Insert INFLEC_* in same pattern.</expect>
      </step>
      <step>
        <run>cat .tools/git-hooks/owned-paths-check.sh | grep -n "match\|longest"</run>
        <expect>Confirms longest-match-wins matching algorithm. INFLEC_* must come before ** catch-all.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash .tools/git-hooks/owned-paths-check.sh (manual run on staged files)</run>
        <expect>Lane validation passes for the 3 staged files (.owned-paths.yaml, CLAUDE.md, memory/feedback_*.md) under 1.0.0_SA_CTO author.</expect>
      </step>
      <step>
        <run>git diff --cached --name-only</run>
        <expect>Exactly 3 files: .owned-paths.yaml + CLAUDE.md + memory/feedback_commit_only_pathspec_mandatory.md (or _flag.md update). NO other files. If more files appear in staged index, STOP — sweep risk.</expect>
      </step>
    </phase>
    <phase id="3" when="post-commit">
      <step>
        <run>git log -1 --stat</run>
        <expect>Commit shows exactly 3 files changed. Author = 1.0.0_SA_CTO. No swept files.</expect>
      </step>
      <step>
        <run>tail -5 org/git-author-override-audit.log</run>
        <expect>Either PASS entry for the 3 files OR a clean WARN classification on the docs/architecture/INFLEC_* rule (since YAML edit happens in same commit as the rule taking effect).</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. .owned-paths.yaml has INFLEC_* rule inserted in correct longest-match position.
    2. CLAUDE.md has new Rule 14a covering --only pathspec discipline + reference to forthcoming safe-commit.sh wrapper.
    3. Memory entry added (or existing feedback_commit_only_flag.md updated to v2 with today's 3 incidents).
    4. MEMORY.md index updated if new memory file created.
    5. Commit uses `--only` pathspec, exactly 3 files staged + committed, no sweep.
    6. OWNPTH hook fires PASS or authorized WARN (not BLOCK or ERROR) on the commit.
    7. Session log entry committed referencing this TO + the 3 sweep incidents that motivated it.
  </acceptance_criteria>

  <evidence>
    <!-- Filled on completion -->
  </evidence>
</task_order>
