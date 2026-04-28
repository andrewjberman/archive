<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>1.0.0_SA_CTO-2026-04-28-adhc-ownpth-008-ae-record-terraform-deploy-safe-commit</id>
  <project>ADHC_OWNPTH</project>
  <issued_by>1.0.0_SA_CTO</issued_by>
  <issued_to>0.7.0_AE_CloudOps</issued_to>
  <issued_date>2026-04-28</issued_date>
  <status>pending</status>

  <title>ADHC_OWNPTH TO 8 — migrate record-terraform-deploy.sh to safe-commit.sh (close the recurring sweep door)</title>

  <references>
    <ref type="prd">docs/architecture/ADHC_OWNPTH.md</ref>
    <ref type="rule">CLAUDE.md Rule 14a (safe-commit.sh primary commit path)</ref>
    <ref type="prior_to">ADHC_OWNPTH.007 (1998340f — safe-commit.sh wrapper shipped 2026-04-27 21:27Z)</ref>
    <ref type="script">infra/aws/lambda/ci/record-terraform-deploy.sh</ref>
    <ref type="wrapper">.tools/safe-commit.sh</ref>
    <ref type="audit">org/git-author-override-audit.log</ref>
    <ref type="memory">memory/feedback_structural_commit_hygiene.md</ref>
  </references>

  <context>
    Sweep incident on 2026-04-28: commit fe5a773f ("ci: record deploy inf-pipeline @ 04aabc29")
    swept 0.1.0_DT_MarketIntelligence's news-pipeline session log
    (org/tier2_senior/0.1.0_DT_MarketIntelligence/logs/2026-04-28/mkov_trends_topical_caps_deploy.md)
    into AE 0.7's inf-pipeline deploy commit. Both source-map.json and CHANGELOG.json
    landed correctly under fe5a773f, but the DT log file was attributed to
    "Andrew Berman &lt;andrew@opalinvest.com&gt;" instead of 0.1.0_DT_MarketIntelligence.

    Timeline that produced the sweep:
    1. DT 0.1.0 ran `git add &lt;log-file&gt;` to track new untracked log.
    2. AE 0.7's record-terraform-deploy.sh fired concurrently and ran:
       - line 268: `git add infra/aws/lambda/ci/lambda-source-map.json`
       - line 382: `git add "$CHANGELOG_PATH"`
       - line 397: `git commit -m "ci: record deploy inf-pipeline @ ..."`  &lt;-- BARE COMMIT
    3. The bare `git commit` at line 397 has no `--only` and no pathspec, so it
       picked up every file in the index — including DT's log file that was
       staged for a different commit.

    This is the **4th observed sweep incident driven by record-terraform-deploy.sh**
    in the documented pattern (CLAUDE.md Rule 14a notes three CLASS-C incidents on
    2026-04-27 with the same root cause). TO 7 shipped the wrapper; this TO migrates
    the loudest known offender to use it. Andrew flagged this directly on 2026-04-22:
    "this keeps happening — propose owned-paths pre-commit hook, not more rules."
    The hook + warn-mode + safe-commit.sh wrapper exist; the remaining gap is that
    record-terraform-deploy.sh does not call them.

    Project status note from ADHC_OWNPTH.json (2026-04-27 21:32Z):
    "Broadcast deferred — re-evaluate if 4th sweep incident occurs in next 48h."
    The 4th incident has now occurred (within 24h of that note). This TO is the
    structural close.
  </context>

  <scope>
    1. Patch `infra/aws/lambda/ci/record-terraform-deploy.sh` to commit via
       `.tools/safe-commit.sh` instead of bare `git commit`:

       a. Build the pathspec deterministically from script state:
          - Always include: `infra/aws/lambda/ci/lambda-source-map.json`
          - If CHANGELOG_WRITTEN=true: also include
            `infra/aws/terraform/${PIPELINE}/CHANGELOG.json`

       b. Replace the bare `git commit -m "..."` block (current line ~397) with:
          ```bash
          PATHSPEC=("infra/aws/lambda/ci/lambda-source-map.json")
          if [ "$CHANGELOG_WRITTEN" = true ]; then
              PATHSPEC+=("infra/aws/terraform/${PIPELINE}/CHANGELOG.json")
          fi

          # Use safe-commit.sh — aborts on index contamination per ADHC_OWNPTH.007
          AUTHOR_ARGS=()
          [ -n "$RECORD_AUTHOR" ] &amp;&amp; AUTHOR_ARGS=(--author "$RECORD_AUTHOR")

          "$WORKSPACE_ROOT/.tools/safe-commit.sh" \
              "${AUTHOR_ARGS[@]}" \
              -m "ci: record deploy ${PIPELINE} @ ${COMMIT_SHORT} [skip ci]

          Pipeline:  $PIPELINE
          Version:   $VERSION_LABEL
          Commit:    $COMMIT_SHA
          Branch:    $BRANCH
          Timestamp: $TIMESTAMP
          Recorded by: record-terraform-deploy.sh" \
              -- "${PATHSPEC[@]}"
          ```

       c. The `git add` calls at lines 268 and 382 stay (safe-commit.sh inspects
          the staged index and runs `git commit --only` — files do need to be
          staged before invocation). Do NOT pre-stash or pre-clear the index;
          safe-commit's whole point is to surface contamination, not hide it.

    2. Add a `--author` flag to record-terraform-deploy.sh argument parser:
       - Usage: `record-terraform-deploy.sh &lt;pipeline&gt; [--version &lt;tag&gt;] [--author "name &lt;email&gt;"]`
       - When provided, set `RECORD_AUTHOR="$2"` and forward to safe-commit.sh.
       - When omitted, fall through to git config identity (existing behavior).
       - Default unchanged — Andrew's manual runs and any caller without --author
         continue to work as before.

    3. Update the script's usage block (lines 53-66) to mention the new flag and
       to note "this script now uses .tools/safe-commit.sh and will abort on
       index contamination."

    4. Update CLAUDE.md after ship — append a one-paragraph note under Rule 14a:
       ```
       record-terraform-deploy.sh now invokes safe-commit.sh (ADHC_OWNPTH.008,
       2026-04-28). If you see a contamination abort during a deploy record,
       clean unrelated staged files via `git reset HEAD -- &lt;extras&gt;` and re-run.
       Concurrent agents staging files for unrelated commits will trigger this —
       this is a feature, not a bug.
       ```

    Do NOT modify safe-commit.sh itself. Do NOT modify build-and-upload.sh in this
    TO (it does not commit; it only updates source-map for a later record-deploy).
    Do NOT broadcast widely yet — Andrew will decide whether to broadcast after
    seeing TO 4 (observe-week) results next week.
  </scope>

  <dependencies>
    <dep>ADHC_OWNPTH.007 must be present at HEAD (.tools/safe-commit.sh executable, --help works). Verified at TO authoring time: file exists, 152 lines, exec bit set.</dep>
  </dependencies>

  <compiler_tools_mandate>
    <phase id="1" when="before edit">
      <step>
        <run>git diff --cached --name-only</run>
        <expect>Empty (clean index before starting work). If not empty, abort and clear the index first via `git reset HEAD -- &lt;extras&gt;` until the staged set matches your intended pathspec.</expect>
        <if_mismatch>STOP. Clean index before authoring the patch.</if_mismatch>
      </step>
      <step>
        <run>ls -la .tools/safe-commit.sh &amp;&amp; bash .tools/safe-commit.sh --help</run>
        <expect>File exists, exec bit set, --help prints usage. If not, ADHC_OWNPTH.007 has regressed and this TO blocks on its repair.</expect>
        <if_mismatch>STOP. Reopen ADHC_OWNPTH.007 first.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after edit, before commit">
      <step>
        <run>bash -n infra/aws/lambda/ci/record-terraform-deploy.sh</run>
        <expect>Exit 0 (syntax check passes).</expect>
        <if_mismatch>STOP. Fix syntax errors before proceeding.</if_mismatch>
      </step>
      <step>
        <run>Canary A (clean index): in a throwaway test repo or via test-record-deploy harness, run a record-deploy with no other staged files; expect commit to succeed and contain ONLY source-map.json + CHANGELOG.json.</run>
        <expect>Exit 0. `git show --stat HEAD` shows exactly the two expected files.</expect>
        <if_mismatch>STOP. The pathspec build logic is wrong.</if_mismatch>
      </step>
      <step>
        <run>Canary B (contaminated index): pre-stage an unrelated file (e.g., a dummy log under org/tier2_senior/0.7.0_AE_CloudOps/logs/), then run record-deploy; expect safe-commit.sh to abort with exit 1 and a list of the unrelated staged file(s). The record-deploy script must propagate the failure (exit non-zero) and NOT create any commit.</run>
        <expect>Exit non-zero. No new commit. ERROR message lists the contaminating file. The unrelated staged file remains staged (not consumed by a sweep).</expect>
        <if_mismatch>STOP. The structural fix is incomplete — script is still sweeping.</if_mismatch>
      </step>
      <step>
        <run>Canary C (--author pass-through): run record-deploy with `--author "0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;"` on a clean index; expect commit author to be the AE agent identity, not Andrew Berman.</run>
        <expect>`git log -1 --pretty=format:'%an %ae'` returns "0.7.0_AE_CloudOps 0.7.0_AE_CloudOps@opal.agent".</expect>
        <if_mismatch>STOP. --author plumbing is broken.</if_mismatch>
      </step>
      <step>
        <run>Canary D (default identity unchanged): run record-deploy without --author on a clean index; expect commit author to fall through to git config identity (existing behavior preserved).</run>
        <expect>Commit succeeds; author = whatever `git var GIT_AUTHOR_IDENT` resolves to.</expect>
        <if_mismatch>STOP. The default path regressed.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>git show --stat HEAD</run>
        <expect>Only infra/aws/lambda/ci/record-terraform-deploy.sh in the commit (and optionally CLAUDE.md if you bundled the rule note). No other files.</expect>
        <if_mismatch>STOP. The TO 8 commit itself was contaminated — escalate to CTO.</if_mismatch>
      </step>
      <step>
        <run>End-to-end self-test: run a no-op record-terraform-deploy.sh on a real pipeline (e.g., shared-infra) where source-map.json has no diff. Expected behavior is the early-exit at line 262-266 — no commit attempted. Verify the script still short-circuits correctly when there is nothing to record.</run>
        <expect>"Source map unchanged" message. Exit 0. No commit.</expect>
        <if_mismatch>STOP. Investigate; this path was working pre-patch.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <coordination agent="1.0.0_SA_CTO" note="MCP CTO on completion with commit hash + canary results. CTO closes TO 8 in ADHC_OWNPTH.json and decides on TO 4 observe-week impact (does this 4th incident shorten the observation window or trigger early flip-to-fail-closed?)."/>
    <coordination agent="2.0.0_SA_COO" note="MCP COO on completion. COO updates org-wide deployment runbook references — any agent runbook that documents the deploy sequence should mention 'record-deploy now uses safe-commit; abort on contamination is expected behavior, clean staged extras and retry.'"/>
    <coordination agent="0.1.0_DT_MarketIntelligence" note="No coordination required for this TO — DT was the victim of incident fe5a773f, not a participant in the fix. Information-only when ship completes."/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. infra/aws/lambda/ci/record-terraform-deploy.sh patched to invoke .tools/safe-commit.sh with explicit pathspec. Bare `git commit` at line 397 removed.
    2. --author flag added to argument parser, optional, defaults preserved.
    3. Canary A (clean): commit succeeds, contains only source-map.json + CHANGELOG.json.
    4. Canary B (contaminated): exit non-zero, no commit, contaminating file remains staged.
    5. Canary C (--author): commit attributed to provided agent serial.
    6. Canary D (no --author): default git identity preserved.
    7. Phase 3 self-test: early-exit short-circuit on unchanged source-map still works.
    8. Session log under org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-28/ includes all 4 canary runs with output.
    9. CLAUDE.md Rule 14a appendix note added (one paragraph; small commit, may be bundled with the script patch or separate).
    10. MCP CTO + MCP COO on completion with commit hash.
  </acceptance_criteria>

  <out_of_scope>
    - Migrating other deploy scripts (build-and-upload.sh, safe-ec2-deploy.sh, ec2 service deploy scripts) to safe-commit.sh. They will be addressed in TO 10+ as separate work items if Andrew prioritizes.
    - Broadcasting safe-commit.sh adoption org-wide. Per project status, broadcast remains deferred pending TO 4 observe-week results.
    - Retroactively fixing the author attribution on fe5a773f. Destructive git history rewrite on a shared branch is not justified by a single misattributed log file.
    - Changing the CHANGELOG.json `agent` field (currently hardcoded to 'devops_technician' at line 341). That is a separate cosmetic concern — file an issue, do not bundle here.
  </out_of_scope>
</task_order>
