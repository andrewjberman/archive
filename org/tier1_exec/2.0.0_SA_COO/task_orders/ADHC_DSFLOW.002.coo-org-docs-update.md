<task_order>
  <metadata>
    <id>ADHC_DSFLOW.002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>2.0.0_SA_COO</issued_to>
    <date>2026-04-21</date>
    <status>pending</status>
    <project_code>ADHC_DSFLOW</project_code>
    <priority>P1 (surfaces enforcement of §6.2 DS deploy ownership in DS startup protocol — paired with .001 tooling to give enforcement teeth)</priority>
    <sla>1h from .001 commit (ordering: .001 ships first so CLAUDE.md Rule 13 can reference a real tool, then .002 lands docs update)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_DSFLOW.md (sections 6.4 + 7 TO-2 + 10 acceptance)</ref>
    <ref type="memory_enforced">memory/feedback_ds_commits_ae_deploys.md — exists but not consistently executed (§2.2 evidence); this TO promotes to CLAUDE.md Rule 13 + org/XXX.md DS row + DS README CAN/CANNOT + DS prompt.md gate step</ref>
    <ref type="sibling">ADHC_DSFLOW.001 — the tool path `.tools/ds-commit-gate.sh` referenced in CLAUDE.md Rule 13 must exist before this TO's doc updates become actionable. Order DSFLOW.001 first.</ref>
    <ref type="project_json">org/projects/ADHC_DSFLOW.json</ref>
    <ref type="target_files">CLAUDE.md (add Rule 13), org/XXX.md (Abilities table DS row), org/tier2_senior/0.4.0_DS_ClientPlatform/README.md (CAN/CANNOT), org/tier2_senior/0.4.0_DS_ClientPlatform/prompt.md (add gate step), memory/feedback_ds_commits_ae_deploys.md (enforcement-reference note)</ref>
  </references>

  <objective>
    Update 5 org documents to enforce DS end-to-end gold-script deploy ownership + mandate the pre-commit gate from DSFLOW.001. Promotes the existing `feedback_ds_commits_ae_deploys.md` memory (which was not consistently executed, see PRD §2.2) to surface in DS startup protocol + CLAUDE.md critical deployment rules.

    Single commit under `2.0.0_SA_COO` author. All 5 doc edits atomic.
  </objective>

  <scope>
    <files>
      <file action="modify">CLAUDE.md — add Rule 13 (DS commit→QA deploy cycle ownership) under Critical EC2 Deployment Rules section</file>
      <file action="modify">org/XXX.md — Abilities by Role table DS row: change "Edit + commit locally" to reflect commit+push+S3-upload+qa-runner-dispatch per PRD §6.4</file>
      <file action="modify">org/tier2_senior/0.4.0_DS_ClientPlatform/README.md — CAN DO + CANNOT DO sections per PRD §6.4</file>
      <file action="modify">org/tier2_senior/0.4.0_DS_ClientPlatform/prompt.md — add step N-1 "Run `.tools/ds-commit-gate.sh <files>` before git commit"</file>
      <file action="modify">memory/feedback_ds_commits_ae_deploys.md — append enforcement-reference note pointing to this PRD + DSFLOW.001 tool + CLAUDE.md Rule 13</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="claude-md-rule-13">
      **CLAUDE.md — add Rule 13** after current Rule 12 (EC2 Deployment Rules section). Verbatim text from PRD §6.4:
      > **13. DS owns gold-script commit→QA deploy cycle.** DS uploads committed gold-script code to S3 directly via `git show {sha}:{path} | aws s3 cp -`, verifies via `comp-pipescript deployed`, and dispatches QA runner or hands RAVC2 ACK to AE. DT/AE step in only for infrastructure, PROD, or multi-pipeline coordination — not as the default upload path.

      Position: after Rule 12 "S3 is the artifact store for all EC2 code." Before the "Agent Autonomy Rules" section.
    </deliverable>
    <deliverable id="xxx-md-abilities-row">
      **org/XXX.md Abilities by Role table — DS row change.** PRD §6.4 text:

      FROM:
      | DS | Edit + commit locally | No | No | Encouraged |

      TO:
      | DS | Commit + push + gold-script S3 upload (committed-ref) + qa-runner SSM dispatch | No (PROD) | QA-runner only | Encouraged |

      Preserve table header and all other rows unchanged.
    </deliverable>
    <deliverable id="ds-readme-can-cannot">
      **org/tier2_senior/0.4.0_DS_ClientPlatform/README.md — CAN DO + CANNOT DO sections** per PRD §6.4:

      Add to "CAN DO":
      - Upload committed gold-script SHAs to `s3://opal-bd-gold-code/gold/{script_id}.py` via `git show {sha}:{path} | aws s3 cp - s3://...`
      - Dispatch SSM commands to `bd-gold-qa-runner` instance
      - Trigger QA runner on single-script and single-group scope
      - Push to origin/CLOUD (for DS-authored commits only)

      Add / confirm in "CANNOT DO":
      - Cannot trigger `bd-gold-trigger` (PROD) — AE exclusive
      - Cannot start/stop EC2 instances — AE exclusive
      - Cannot modify IAM / Terraform — AE + DT exclusive
      - Cannot push portal submodule — DT exclusive

      Cross-reference DSFLOW.001 tool and CLAUDE.md Rule 13.
    </deliverable>
    <deliverable id="ds-prompt-gate-step">
      **org/tier2_senior/0.4.0_DS_ClientPlatform/prompt.md — add step N-1 before `git commit`.** Text:
      > **Step N-1 — Run pre-commit gate on every gold-script file touched:**
      > ```bash
      > .tools/ds-commit-gate.sh <files>
      > ```
      > This runs `python -m py_compile` + `.tools/ds-precommit-check.py` (AST undefined-name scan). Either failure blocks commit. Catches 081223b5 + 035352c3 latent-bug class. See CLAUDE.md Rule 13 + `docs/architecture/ADHC_DSFLOW.md` §6.1.

      Position: right before the existing `git commit --only --author=... -- <paths>` step in the DS workflow section (probably in "How I commit" or similar section of the prompt).
    </deliverable>
    <deliverable id="feedback-memory-enforcement">
      **memory/feedback_ds_commits_ae_deploys.md — append enforcement-reference note:**
      > **Enforcement 2026-04-21 (ADHC_DSFLOW PRD):** This memory is now enforced via CLAUDE.md Rule 13 + org/XXX.md Abilities table DS row + DS README CAN/CANNOT sections + DS prompt.md pre-commit gate step + `.tools/ds-commit-gate.sh` tool. PRD shipped in response to 2-in-2-days latent-PROD-crash pattern (081223b5 B_00 NameError + 035352c3 D_02 KeyError). Prior state: memory existed but was not consistently executed.

      Position: append at end of current body, before any trailer.
    </deliverable>
    <deliverable id="commit-single">
      `git commit --only --author="2.0.0_SA_COO <2.0.0_SA_COO@opal.agent>"` with all 5 paths explicit. Single atomic commit.

      Session log path: `org/tier1_exec/2.0.0_SA_COO/logs/2026-04-21/dsflow_002_org_docs_update.md` — reproduces each doc edit + Compiler Tools section + pass/fail on acceptance criteria.
    </deliverable>
    <deliverable id="ds-iam-verification">
      **Side-task — §11 Q4 verification.** Before this TO closes, verify DS has `s3:PutObject` on `opal-bd-gold-code/gold/*`:
      1. Identify the DS agent's AWS IAM role (likely stems from whatever Andrew's dev profile uses — may not be a specific role but rather Andrew's personal IAM user).
      2. Check via `aws iam get-user` + `aws iam list-attached-user-policies` + `aws iam list-user-policies` (if DS runs under Andrew's credentials) OR `aws iam list-role-policies --role-name <ds-role>` (if a dedicated role exists).
      3. `aws iam simulate-principal-policy --policy-source-arn <arn> --action-names s3:PutObject --resource-arns arn:aws:s3:::opal-bd-gold-code/gold/test.py` → expect "allowed".
      4. If "implicitDeny" or IAM role/user unclear: file micro-TO to 0.7.0_AE_CloudOps to provision.
      5. Document finding in session log. Flag to Andrew if gap.
    </deliverable>
  </deliverables>

  <wire_contract>
    Zero runtime system impact. Pure org-doc text edits + enforcement reference. DS workflow gains one step (run the gate); DS's AWS capabilities are clarified in the README but no IAM mutation unless §11 Q4 verification surfaces a gap.

    Non-retroactive per PRD §13: existing commits (HLOT2 5f5d0319, BFIX1/2 081223b5+1a54d46a) do NOT get retroactive gate runs. New workflow activates for commits AFTER this TO ships.
  </wire_contract>

  <acceptance_criteria>
    1. CLAUDE.md Rule 13 present, text verbatim from PRD §6.4, correctly positioned after Rule 12.
    2. org/XXX.md Abilities table DS row updated per PRD §6.4. Table remains well-formed (pipe-delimited).
    3. DS README has CAN DO + CANNOT DO sections reflecting PRD §6.2 authority split. CAN DO explicitly includes S3 upload via committed-ref pattern + qa-runner dispatch on single-script/single-group scope. CANNOT DO explicitly excludes PROD trigger + EC2 lifecycle + IAM/TF mutation + portal submodule push.
    4. DS prompt.md step N-1 added with `.tools/ds-commit-gate.sh <files>` command + CLAUDE.md Rule 13 + PRD §6.1 cross-reference.
    5. feedback_ds_commits_ae_deploys.md has enforcement-reference note appended with 2026-04-21 date + PRD link + DSFLOW.001 + CLAUDE.md Rule 13 cross-references.
    6. Single commit under 2.0.0_SA_COO author with --only flag + explicit paths. No other files swept.
    7. §11 Q4 DS IAM verification captured in session log — if gap, micro-TO to 0.7.0_AE_CloudOps filed. If no gap, explicit confirmation.
    8. DSFLOW.001 confirmed committed before this TO commits (or coordinated if parallel). CLAUDE.md Rule 13 should not land before the tool exists.
    9. Session log at `org/tier1_exec/2.0.0_SA_COO/logs/2026-04-21/dsflow_002_org_docs_update.md` reproducing each file edit + compiler tools section + acceptance criteria pass/fail.
    10. MCP ACK to CTO on commit + flag any IAM finding.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Read CLAUDE.md + org/XXX.md + org/tier2_senior/0.4.0_DS_ClientPlatform/README.md + prompt.md + memory/feedback_ds_commits_ae_deploys.md in full — capture current state for diff-awareness</run>
        <expect>All 5 files readable, current content captured. Identify exact insertion points for each delta.</expect>
        <if_mismatch>If any file missing or structurally different than PRD §6.4 assumes, surface to COO-self (edit the scope inline before executing) or flag to CTO for PRD amendment.</if_mismatch>
      </step>
      <step>
        <run>Confirm DSFLOW.001 committed status: `git log --oneline --all | grep ADHC_DSFLOW.001` (or check via MCP DS~A latest log)</run>
        <expect>DSFLOW.001 committed. CLAUDE.md Rule 13 can cite `.tools/ds-commit-gate.sh` path safely.</expect>
        <if_mismatch>If DSFLOW.001 not yet committed, HOLD .002 commit until .001 lands. Or, if CTO/Andrew directs parallel commit, document the sequencing risk in session log.</if_mismatch>
      </step>
      <step>
        <run>§11 Q4 DS IAM probe: `aws iam simulate-principal-policy --policy-source-arn &lt;DS-principal&gt; --action-names s3:PutObject --resource-arns arn:aws:s3:::opal-bd-gold-code/gold/test.py`</run>
        <expect>"allowed" decision. Confirms DS has the S3 upload authority that §6.2.1 requires.</expect>
        <if_mismatch>If "implicitDeny" or policy-source-arn unclear, file micro-TO to 0.7.0_AE_CloudOps for provisioning. Document gap in session log + flag to Andrew via COO status update.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>Diff review: `git diff --stat` after all 5 edits</run>
        <expect>Exactly 5 files changed. Total lines changed consistent with the verbatim texts in Deliverables (rough: Rule 13 ~5 lines, XXX.md ~1 line, DS README ~10-15 lines, prompt.md ~8 lines, feedback memory ~4 lines). No unintended edits.</expect>
        <if_mismatch>If any file changed that wasn't in scope, revert that edit before commit. Enforce --only discipline.</if_mismatch>
      </step>
      <step>
        <run>Verify CLAUDE.md Rule 13 position: `grep -n "^## " CLAUDE.md | head -20` + confirm Rule 13 lands in "Critical EC2 Deployment Rules" section, not "Agent Autonomy Rules" or elsewhere</run>
        <expect>Rule 13 is the final numbered rule in the EC2 Deployment Rules section (after Rule 12). Preserves ordering.</expect>
        <if_mismatch>Re-position Rule 13 before commit.</if_mismatch>
      </step>
      <step>
        <run>`.tools/ds-commit-gate.sh <not-applicable-skipped>` — this TO edits org docs, not gold scripts. Gate is for `data/black_diamond/scripts/gold/*.py` files only. Smoke-gate doesn't apply.</run>
        <expect>Skipped — org-docs commit doesn't trigger gate.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>Post-commit grep for all 5 changes: `grep -l "Rule 13" CLAUDE.md + grep "QA-runner" org/XXX.md + grep "CAN DO" org/tier2_senior/0.4.0_DS_ClientPlatform/README.md + grep "ds-commit-gate" org/tier2_senior/0.4.0_DS_ClientPlatform/prompt.md + grep "Enforcement 2026-04-21" memory/feedback_ds_commits_ae_deploys.md`</run>
        <expect>All 5 greps return hits. Changes landed.</expect>
        <if_mismatch>Re-apply any missed edit via fast-follow commit.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>Sequencing: DSFLOW.001 ships first (tool must exist before CLAUDE.md Rule 13 references it). If both TOs fire in parallel, serialize commits so .001 lands first.</item>
    <item>DS IAM verification (§11 Q4): may trigger micro-TO to 0.7.0_AE_CloudOps for provisioning if gap found. Non-blocking for the org-docs update — docs can land even if IAM provisioning is pending (docs represent target state).</item>
    <item>Non-retroactive clause per PRD §13: HLOT2 `5f5d0319` already committed pre-gate, exempt. DSFLOW.003 training run is the first POST-gate deploy cycle.</item>
    <item>No AE / DT concurrent-edit conflict on the 5 target files. CLAUDE.md is the main risk — if CTO is amending CLAUDE.md (e.g., PRD v1.2 amendment), coordinate commit order.</item>
  </cross_domain_coordination>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADHC_DSFLOW.001" status="pending">DSFLOW.001 must commit before .002 to avoid CLAUDE.md Rule 13 citing a non-existent tool path. Parallel-authorized per PRD §13 handoff; serialize at commit order.</dependency>
  </dependencies>

  <next>On commit: MCP ACK to CTO (closeout of my own TO); flag any IAM finding from §11 Q4 probe. DSFLOW.003 trigger-ready once both .001 + .002 are complete. Andrew §11 Q1 (git hook vs startup reminder) answer folds into potential v2 enhancement.</next>
</task_order>
