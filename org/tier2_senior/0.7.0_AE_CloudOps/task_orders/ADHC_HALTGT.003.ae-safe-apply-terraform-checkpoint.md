<task_order>
  <metadata>
    <id>ADHC_HALTGT.003</id>
    <slug>ae-safe-apply-terraform-checkpoint</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-20 (COO~B decomposition of ADHC_HALTGT PRD v0.1 §6). HARD-GATED on ADHC_HALTGT.001 -- safe-apply sources the checkpoint library .001 ships. Runs in parallel with ADHC_HALTGT.002 (disjoint files: .003 is a new wrapper, .002 edits 3 existing scripts). COO~B flips to pending + fires GO when .001 reports complete.</dispatch_unblock_condition>
    <project_code>ADHC_HALTGT</project_code>
    <priority>P1 -- the PRIMARY checkpoint. `terraform apply` is the irreversible step and it precedes the push; this is the only insertion point that fires immediately before the irreversible action (PRD §7-Q2).</priority>
    <sla>0.5-1d wall.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_HALTGT.md (v0.1) -- §6 TO-3; §3.3 (insertion points); §7-Q2 (insertion mechanism); R2 (adoption risk).</prd>
    <gate>ADHC_HALTGT.001 -- .tools/halt-gate-check.sh (the sourceable checkpoint library).</gate>
    <ruling>CTO~B §7-Q2 resolution (confirmed at decomposition): a `safe-apply` wrapper agents must use -- the same discipline shape as safe-commit.sh. Option (a). It is the only option that fires immediately before the irreversible step; (b) pre-push-only and (c) pre-commit are partial nets (apply precedes push; a window remains after commit). The pre-push net (ADHC_HALTGT.002) stays as defence in depth.</ruling>
  </references>

  <objective>
    Author a thin `safe-apply` wrapper around `terraform apply` that runs the ADHC_HALTGT.001 checkpoint first, then delegates to the real terraform binary. This is the primary HALTGT net -- it surfaces a pending STOP at the last reversible moment, immediately before `terraform apply` runs the irreversible change.
  </objective>

  <context>
    Today agents call the terraform binary directly (.tools/terraform.exe) -- `apply` is not wrapped. PRD §2.4: apply precedes push, so a pre-push-only checkpoint lets the irreversible apply happen before the STOP is seen. safe-apply closes that window.

    Design: a new wrapper (suggest .tools/safe-apply.sh, in PATH like the other .tools wrappers). It runs .tools/halt-gate-check.sh; if the checkpoint blocks (non-zero exit), safe-apply aborts and does NOT call terraform. If the checkpoint passes, safe-apply delegates to `.tools/terraform.exe apply` passing all arguments through transparently. Wrap ONLY `apply` -- `plan` is non-destructive and is not gated. Git Bash 3.6.7-safe per CLAUDE.md Rule 16.

    PRD R2 (adoption): a wrapper only works if agents use it; bare `terraform apply` remains physically possible. The CLAUDE.md mandate that closes that gap is ADHC_HALTGT.004's scope -- this TO ships the wrapper; .004 mandates it.
  </context>

  <scope>
    <step>Phase 1 -- Read .tools/halt-gate-check.sh (the .001 library) for the sourceable interface + exit-code contract. Inspect .tools/safe-commit.sh + .tools/safe-deploy.sh for the house wrapper style (arg passthrough, PATH form, exit-code propagation).</step>
    <step>Phase 2 -- Author .tools/safe-apply.sh: run the checkpoint; on a blocked result, print the checkpoint output and exit non-zero WITHOUT calling terraform; on a pass, exec `.tools/terraform.exe apply "$@"` with all args passed through and terraform's exit code propagated. Wrap `apply` only. Include a short usage header.</step>
    <step>Phase 3 -- shellcheck clean. Anchor-reproduction: safe-apply with a STOP-class message in the inbox blocks BEFORE terraform runs (terraform is never invoked); with an empty inbox it delegates to terraform apply normally; arg passthrough verified.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Read .tools/halt-gate-check.sh + .tools/safe-commit.sh + .tools/safe-deploy.sh.</run>
        <expect>The .001 library's sourceable interface + exit-code contract are clear; the house wrapper style (arg passthrough, exit-code propagation) is established. comp-* tools N/A -- `.tools/` shell is not graph-modeled (PRD §5).</expect>
        <if_mismatch>If .tools/halt-gate-check.sh is absent, STOP -- the .001 gate is not satisfied; MCP COO~B.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>shellcheck .tools/safe-apply.sh</run>
        <expect>shellcheck exits 0. The wrapper gates `apply` only; terraform's exit code is propagated; no banned utility without a guarded fallback (CLAUDE.md Rule 16).</expect>
        <if_mismatch>Fix every shellcheck finding before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Anchor-reproduction: (1) seed a `[STOP]`-subject message -> run safe-apply on a trivial/no-op terraform config; (2) empty inbox -> run safe-apply on the same config; (3) confirm arg passthrough (e.g. safe-apply with `-auto-approve` and a `-target`).</run>
        <expect>(1) safe-apply hard-blocks and terraform apply is NEVER invoked (verify: no apply ran -- state untouched, no plan output). (2) safe-apply delegates and terraform apply runs normally. (3) all arguments reach terraform unchanged; terraform's exit code is safe-apply's exit code.</expect>
        <if_mismatch>If terraform apply runs in case (1), the checkpoint is not gating the wrapper -- the primary net has failed. Do not mark complete; fix and re-run.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Local-runtime shell tooling -- a wrapper around the terraform binary. No data, no Lambda code, no S3, no silver/bronze script. No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: .tools/safe-apply.sh (new file)
    also_in_to: ADHC_HALTGT.002 (the 3 existing deploy/push scripts) is a SIBLING insertion point but disjoint -- .003 is a new file, .002 edits existing files; they run in parallel. Both source the .001 library (read-only consumers).
    last_write_owner: 0.7.0_AE_CloudOps owns the full HALTGT lane.
    required_action: Gated on .001. The CLAUDE.md rule mandating safe-apply is ADHC_HALTGT.004 -- do not edit CLAUDE.md here.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">.tools/safe-apply.sh exists -- runs the ADHC_HALTGT.001 checkpoint, then delegates to `.tools/terraform.exe apply` with full argument passthrough; wraps `apply` only (not `plan`).</ac>
    <ac id="AC2">On a checkpoint block (STOP-class), safe-apply exits non-zero and terraform apply is NEVER invoked. On a checkpoint pass, safe-apply delegates normally and propagates terraform's exit code. A routine-surfaced block under safe-apply is resolved by re-invoking safe-apply with HALT_ACK=1 -- the env var passes through to the checkpoint (non-interactive, no stdin read).</ac>
    <ac id="AC3">shellcheck clean; Git Bash 3.6.7-safe (CLAUDE.md Rule 16).</ac>
    <ac id="AC4">Anchor-reproduction confirms: STOP-class -> apply never runs; empty inbox -> apply runs; arg passthrough intact.</ac>
    <ac id="AC5">No emoji. Session log with the Compiler Tools section reproducing the Phase 2 shellcheck + the Phase 3 anchor test. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="create">.tools/safe-apply.sh</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">.tools/safe-apply.sh -- the primary pre-`terraform apply` HALTGT checkpoint. `.tools/` is a gitignored prefix -- `git add -f`.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not gate `terraform plan` -- plan is non-destructive; only `apply` is the irreversible step.</rule>
    <rule>Do not duplicate the checkpoint logic -- source the .001 library.</rule>
    <rule>Do not edit CLAUDE.md here -- ADHC_HALTGT.004 owns the mandate rule (single CLAUDE.md writer).</rule>
    <rule>Do not swallow terraform's exit code -- safe-apply must propagate it so CI / record-terraform-deploy.sh see the real result.</rule>
    <rule>Do not use a banned utility (pgrep/pkill/flock/pidof/setsid/wget) without a `command -v`-guarded fallback (CLAUDE.md Rule 16).</rule>
  </do_not>
</task_order>
