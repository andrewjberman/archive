<task_order>
  <metadata>
    <id>ADHC_HALTGT.002</id>
    <slug>ae-wire-checkpoint-into-deploy-paths</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL~B</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-20 (COO~B decomposition of ADHC_HALTGT PRD v0.1 §6). HARD-GATED on ADHC_HALTGT.001 -- this TO sources the checkpoint library .001 ships. Runs in parallel with ADHC_HALTGT.003 (disjoint files). COO~B flips to pending + fires GO when .001 reports complete.</dispatch_unblock_condition>
    <project_code>ADHC_HALTGT</project_code>
    <priority>P2 -- the second net. Wires the checkpoint into the existing push/deploy structural-enforcement points.</priority>
    <sla>0.5-1d wall.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_HALTGT.md (v0.1) -- §6 TO-2; §3.3 (insertion points table); §3.1.</prd>
    <gate>ADHC_HALTGT.001 -- .tools/halt-gate-check.sh (the sourceable checkpoint library + its exit-code contract).</gate>
  </references>

  <objective>
    Source the ADHC_HALTGT.001 checkpoint library from the existing deploy/push structural-enforcement points so a pending STOP is surfaced before a git-push deploy or an EC2/gold-chain deploy proceeds. Extend the existing scripts -- do not duplicate the checkpoint logic.
  </objective>

  <context>
    PRD §3.3 names three existing insertion points that should carry the checkpoint as a second net (the primary net is safe-apply, ADHC_HALTGT.003):
      - the pre-push hook -- .tools/git-hooks/pre-push-safe-deploy.sh
      - .tools/safe-deploy.sh (the DS gold-chain deploy wrapper, CLAUDE.md Rule 13)
      - safe-ec2-deploy.sh (the EC2 deploy wrapper, CLAUDE.md Rule 7)
    Each already exists and already runs as a structural gate. This TO adds one sourced call to the .001 library near the top of each, before the irreversible step. The checkpoint's exit code drives the gate: non-zero (STOP-class hard-block) aborts the script; an acked routine message or an empty inbox lets it continue.

    Confirm the exact path of safe-ec2-deploy.sh in Phase 1 (CLAUDE.md Rule 7 names it; it may live under .tools/ or infra/aws/ec2/). Git Bash 3.6.7-safe per CLAUDE.md Rule 16.
  </context>

  <scope>
    <step>Phase 1 -- Read .tools/halt-gate-check.sh (the .001 deliverable) for the sourceable interface + exit-code contract. Locate and read the 3 insertion-point scripts; identify the correct insertion line in each (after arg-parsing / serial-resolution, before the irreversible push/deploy step).</step>
    <step>Phase 2 -- In each of the 3 scripts, source .tools/halt-gate-check.sh and invoke the checkpoint; on a non-zero (blocked) result, abort the script with a clear message and the checkpoint's output. Do not duplicate the checkpoint logic -- one sourced call per script.</step>
    <step>Phase 3 -- shellcheck each modified script clean. Anchor-reproduction: a push/deploy with a STOP-class message in the inbox is blocked; with only a routine message it surfaces + requires ack; with an empty inbox it proceeds unchanged.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Read .tools/halt-gate-check.sh + the 3 insertion-point scripts (pre-push-safe-deploy.sh, safe-deploy.sh, safe-ec2-deploy.sh).</run>
        <expect>The .001 library exposes a stable sourceable entry point with a documented exit-code contract; each of the 3 scripts has an identifiable insertion line before its irreversible step. comp-* tools N/A -- `.tools/` shell + git hooks are not graph-modeled (PRD §5).</expect>
        <if_mismatch>If .tools/halt-gate-check.sh is absent or its interface is unstable, STOP -- the .001 gate is not satisfied; MCP COO~B. If a named insertion-point script does not exist, MCP COO~B before improvising.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>shellcheck on each of the 3 modified scripts.</run>
        <expect>shellcheck exits 0 on all 3. The checkpoint call is sourced (not copy-pasted); no banned utility introduced (CLAUDE.md Rule 16).</expect>
        <if_mismatch>Fix every shellcheck finding before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Anchor-reproduction per insertion point: with (a) an empty inbox, (b) a routine message, (c) a `[STOP]`-subject message, exercise each of the 3 paths (the pre-push hook can be exercised with a no-op push to a scratch ref; safe-deploy.sh / safe-ec2-deploy.sh with a dry-run flag if available).</run>
        <expect>(a) the path proceeds unchanged; (b) the path surfaces the message + requires the ack token; (c) the path is hard-blocked before the irreversible step. Consistent across all 3 insertion points.</expect>
        <if_mismatch>If any path proceeds past a STOP-class message, the wire is wrong -- the checkpoint exit code is not gating that script. Do not mark complete; fix and re-run.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Local-runtime shell tooling -- no data, no Lambda, no S3, no silver/bronze script. No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: .tools/git-hooks/pre-push-safe-deploy.sh ; .tools/safe-deploy.sh ; safe-ec2-deploy.sh
    also_in_to: ADHC_HALTGT.003 (safe-apply) is a SIBLING insertion point but a NEW file -- disjoint from these 3; .002 and .003 run in parallel with no file overlap. Both source the .001 library (read-only consumers of it).
    last_write_owner: 0.7.0_AE_CloudOps owns the full HALTGT lane.
    required_action: Extend the 3 existing scripts; do not refactor their existing gate logic. Gated on .001.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">.tools/git-hooks/pre-push-safe-deploy.sh, .tools/safe-deploy.sh, and safe-ec2-deploy.sh each source .tools/halt-gate-check.sh and gate on its exit code before their irreversible step.</ac>
    <ac id="AC2">The checkpoint logic is sourced from the .001 library, not duplicated, in all 3 scripts.</ac>
    <ac id="AC3">shellcheck clean on all 3 modified scripts; Git Bash 3.6.7-safe.</ac>
    <ac id="AC4">Anchor-reproduction: each path blocks on a STOP-class message, surfaces+acks on a routine message, proceeds unchanged on an empty inbox.</ac>
    <ac id="AC5">No emoji. Session log with the Compiler Tools section reproducing the Phase 2 shellcheck + the Phase 3 3-state x 3-path anchor test. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">.tools/git-hooks/pre-push-safe-deploy.sh</file>
    <file action="modify">.tools/safe-deploy.sh</file>
    <file action="modify">safe-ec2-deploy.sh (path confirmed in Phase 1)</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">Checkpoint sourced into the 3 existing deploy/push enforcement points. `.tools/` is a gitignored prefix -- `git add -f` as needed.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not duplicate the checkpoint logic -- source the .001 library. One reusable library, several insertion points (PRD §3.3).</rule>
    <rule>Do not refactor or weaken the existing gate logic in these scripts -- add the checkpoint, leave the rest intact.</rule>
    <rule>Do not edit CLAUDE.md here -- the rule mandating these wrappers is ADHC_HALTGT.004's scope (single CLAUDE.md writer avoids a merge conflict with .003/.004).</rule>
    <rule>Do not use a banned utility (pgrep/pkill/flock/pidof/setsid/wget) without a `command -v`-guarded fallback (CLAUDE.md Rule 16).</rule>
  </do_not>
</task_order>
