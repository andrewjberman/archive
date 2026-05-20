<task_order>
  <metadata>
    <id>ADHC_HALTGT.004</id>
    <slug>ae-claudemd-rule-and-memory-update</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-20 (COO~B decomposition of ADHC_HALTGT PRD v0.1 §6). HARD-GATED on ADHC_HALTGT.002 AND ADHC_HALTGT.003 -- the CLAUDE.md rule mandates wrappers that must exist + be verified before they are mandated. COO~B flips to pending + fires GO when both .002 and .003 report complete. Last TO in the HALTGT sequence.</dispatch_unblock_condition>
    <project_code>ADHC_HALTGT</project_code>
    <priority>P2 -- docs/adoption. Closes the R2 adoption risk: a wrapper only works if agents are mandated to use it.</priority>
    <sla>0.5d wall -- documentation only.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_HALTGT.md (v0.1) -- §6 TO-4; §4 (ADHC_CLCOMM cross-ref); R2 (adoption risk).</prd>
    <gate>ADHC_HALTGT.002 (checkpoint wired into pre-push / safe-deploy / safe-ec2-deploy) AND ADHC_HALTGT.003 (.tools/safe-apply.sh shipped + anchor-verified).</gate>
    <related>docs/architecture/HALTGT_SEVERITY_CONVENTION.md (ADHC_HALTGT.000 -- the STOP-class subject-prefix convention senders follow); memory/feedback_inbox_check_before_landing.md (the cultural practice this project structuralizes).</related>
  </references>

  <objective>
    Close the R2 adoption gap. A safe-apply wrapper and checkpoint-bearing deploy scripts only work if agents are structurally directed to use them. Add the CLAUDE.md rule mandating the HALTGT checkpoint path, document the STOP-class sender convention where senders will see it, update the feedback_inbox_check_before_landing memory to point at the now-structural gate, and cross-reference ADHC_CLCOMM.
  </objective>

  <context>
    HALTGT after .001-.003: .tools/halt-gate-check.sh (the checkpoint), .tools/safe-apply.sh (the primary pre-apply net), and the checkpoint wired into pre-push-safe-deploy.sh / safe-deploy.sh / safe-ec2-deploy.sh (the second net). What remains is the mandate -- bare `terraform apply` is still physically possible (PRD R2), and message senders need to know the `[STOP]`/`[HALT]` subject convention or the classifier has nothing to classify.

    This TO is documentation only. It edits CLAUDE.md, a memory file, and (lightly) the message-sender guidance. It is the single CLAUDE.md writer in the HALTGT project -- .002 and .003 deliberately do not touch CLAUDE.md so this TO owns it conflict-free.
  </context>

  <scope>
    <step>Phase 1 -- Confirm .002 + .003 shipped: .tools/safe-apply.sh exists and anchor-verified; the 3 deploy/push scripts carry the sourced checkpoint. Read the current CLAUDE.md deployment-rules section + memory/feedback_inbox_check_before_landing.md + docs/architecture/HALTGT_SEVERITY_CONVENTION.md.</step>
    <step>Phase 2 -- Add a CLAUDE.md rule (next number in the deployment-rules sequence): mandate `safe-apply` over bare `terraform apply`; state that the pre-push / safe-deploy / safe-ec2-deploy paths carry a STOP checkpoint; state that a STOP-class hard-block is overridable only via the audited override (org/halt-gate-override-audit.log). Keep it consistent in tone/length with the existing Rules 1-17.</step>
    <step>Phase 2 -- Add the STOP-class sender convention where senders see it: a short note in CLAUDE.md and/or org/XXX.md RAVC section pointing at HALTGT_SEVERITY_CONVENTION.md -- an exec issuing a STOP/halt prefixes the subject with `[STOP]` (or `[HALT]`).</step>
    <step>Phase 2 -- Update memory/feedback_inbox_check_before_landing.md: the cultural "check inbox before landing" practice is now backed by a structural gate; point the memory at the HALTGT checkpoint (safe-apply + the wired deploy paths). Cross-reference ADHC_CLCOMM (the watcher-liveness sibling, PRD §4). Update MEMORY.md's index line if the hook/summary changed.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Confirm .002 + .003 deliverables exist (.tools/safe-apply.sh; the sourced checkpoint in the 3 scripts). Read CLAUDE.md deployment rules + feedback_inbox_check_before_landing.md + HALTGT_SEVERITY_CONVENTION.md.</run>
        <expect>safe-apply.sh and the wired checkpoint are present and anchor-verified per .002/.003 RAVC2s. comp-* tools N/A -- documentation TO (PRD §5).</expect>
        <if_mismatch>If .002 or .003 is not actually complete/verified, STOP -- do not mandate a wrapper that is not shipped. MCP COO~B.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Self-review: read the new CLAUDE.md rule + the memory edit end-to-end; confirm every wrapper/path the rule mandates actually exists and was verified by a RAVC2.</run>
        <expect>The CLAUDE.md rule references only shipped + verified tooling; no forward-reference to unbuilt wrappers. The sender convention note resolves to HALTGT_SEVERITY_CONVENTION.md. No emoji.</expect>
        <if_mismatch>If the rule mandates anything not shipped, fix the rule text before commit.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Documentation-only TO -- CLAUDE.md + a memory file + sender guidance. No data, no code, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: CLAUDE.md ; memory/feedback_inbox_check_before_landing.md ; MEMORY.md ; org/XXX.md (light, optional)
    also_in_to: ADHC_HALTGT.002 and .003 deliberately do NOT edit CLAUDE.md -- this TO is the single CLAUDE.md writer for the project, conflict-free. CLAUDE.md is a high-traffic shared file across all agents -- commit promptly with a tight pathspec via safe-commit.sh.
    last_write_owner: 0.7.0_AE_CloudOps owns the full HALTGT lane.
    required_action: Gated on .002 + .003. Pull latest CLAUDE.md immediately before editing -- other agents amend it frequently.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">CLAUDE.md carries a new deployment rule mandating `safe-apply` over bare `terraform apply` and stating the pre-push / safe-deploy / safe-ec2-deploy paths carry the STOP checkpoint + the audited-override path (org/halt-gate-override-audit.log).</ac>
    <ac id="AC2">The STOP-class sender convention (`[STOP]`/`[HALT]` subject prefix) is documented where senders see it, pointing at HALTGT_SEVERITY_CONVENTION.md.</ac>
    <ac id="AC3">memory/feedback_inbox_check_before_landing.md is updated to point at the now-structural HALTGT gate and cross-references ADHC_CLCOMM; MEMORY.md index line updated if changed.</ac>
    <ac id="AC4">The CLAUDE.md rule references only shipped + RAVC2-verified tooling -- no forward-reference to unbuilt wrappers.</ac>
    <ac id="AC5">No emoji. Committed via safe-commit.sh with a tight pathspec. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">CLAUDE.md</file>
    <file action="modify">memory/feedback_inbox_check_before_landing.md</file>
    <file action="modify">MEMORY.md (index line, if changed)</file>
    <file action="modify">org/XXX.md (light -- sender-convention note, optional placement)</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">CLAUDE.md HALTGT rule + sender-convention note + memory update.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B. This RAVC2 closes the HALTGT project sequence -- COO~B does the 3-step project closure on accept.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not mandate a wrapper that is not shipped + RAVC2-verified -- AC4. A CLAUDE.md rule pointing at vapor is worse than no rule.</rule>
    <rule>Do not `git add -A` / sweep CLAUDE.md -- it is high-traffic; use safe-commit.sh with an explicit pathspec.</rule>
    <rule>Do not restructure the existing CLAUDE.md rules -- add one new rule consistent with the existing format.</rule>
    <rule>Do not change message delivery or org/mcp/server.py -- HALTGT does not touch delivery (PRD §4 out-of-scope).</rule>
  </do_not>
</task_order>
