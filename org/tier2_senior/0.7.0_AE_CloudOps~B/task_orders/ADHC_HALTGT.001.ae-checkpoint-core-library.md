<task_order>
  <metadata>
    <id>ADHC_HALTGT.001</id>
    <slug>ae-checkpoint-core-library</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-20 (COO~B decomposition of ADHC_HALTGT PRD v0.1 §6). HARD-GATED on ADHC_HALTGT.000 -- the classifier cannot be written until the STOP-class convention doc (HALTGT_SEVERITY_CONVENTION.md) exists. COO~B flips to pending + fires GO when .000 reports complete.</dispatch_unblock_condition>
    <project_code>ADHC_HALTGT</project_code>
    <priority>P1 -- the checkpoint core. ADHC_HALTGT.002 and .003 both source this library; it is the project's load-bearing TO.</priority>
    <sla>1-1.5d wall.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_HALTGT.md (v0.1) -- §6 TO-1; §3.1 (checkpoint behavior); §3.2 (tiered verdict); §7-Q3 (override audit); R3 (Git Bash 3.6.7); R4 (serial detection).</prd>
    <gate>ADHC_HALTGT.000 -- docs/architecture/HALTGT_SEVERITY_CONVENTION.md (the STOP-class match rule).</gate>
    <ruling>CTO~B §7-Q3 resolution (confirmed at decomposition): a hard-blocked STOP is bypassable via an AUDITED override, written to a DEDICATED log -- org/halt-gate-override-audit.log -- kept separate from org/git-author-override-audit.log (commit-scope forensics) so STOP-override forensics are isolated.</ruling>
  </references>

  <objective>
    Author the reusable `.tools/` shell library that is the HALTGT checkpoint: given the running agent's serial, read its inbox, enumerate pending messages, classify each as STOP-class or routine per the ADHC_HALTGT.000 convention, render the §3.2 tiered verdict (pass silent / surface + require ack / hard-block), and support an audited override of a hard-block. This library is authored once and sourced by several insertion points (ADHC_HALTGT.002 / .003).
  </objective>

  <context>
    PRD §3.2 tiered verdict:
      - Empty inbox -> PASS silently, zero friction.
      - Any pending routine message -> SURFACE loudly (print sender + subject + age) and require an explicit acknowledgement token to proceed. The agent must SEE what is waiting.
      - A STOP-class message present -> HARD-BLOCK. The deploy does not proceed until resolved; bypass requires an audited override.

    Serial detection (PRD R4): the library reads the agent serial from `.comp-graph/.agent_context` (the `SERIAL=` line). It must read BOTH org/mcp/inbox/{serial}/ AND the base-serial inbox dir (strip any `~X` suffix) -- a tilde-lane agent's STOP can land in either. If the serial cannot be determined, the library MUST fail loud (treat as a hard-block / non-zero exit), NEVER silently pass -- a checkpoint that can't find its inbox must not green-light a deploy.

    Git Bash 3.6.7 (PRD R3 / CLAUDE.md Rule 16): local-runtime shell. Use only utilities in the default install -- no `pgrep`/`pkill`/`flock`/`pidof`/`setsid`/`wget`. Safe: bash, ps, awk, sed, grep, find, timeout, curl, xargs, mktemp, realpath, tee, jq (workspace-local). Any missing utility needs a `command -v`-guarded fallback.

    "Pending" = messages in the inbox dir that are NOT under inbox/read/ (unread). The library enumerates unread message files; it does not mark them read (that is the agent's action, not the checkpoint's).
  </context>

  <scope>
    <step>Phase 1 -- Read HALTGT_SEVERITY_CONVENTION.md (the .000 deliverable) for the exact STOP-class match rule. Inspect the inbox layout under org/mcp/inbox/ and the `.comp-graph/.agent_context` format. Inspect an existing `.tools/` shell wrapper (e.g. safe-commit.sh) for the house style + the audited-override pattern (the `--force` -> org/git-author-override-audit.log precedent).</step>
    <step>Phase 2 -- Author the library at .tools/halt-gate-check.sh (a sourceable library + a directly-runnable form). Functions: resolve the agent serial from .comp-graph/.agent_context (fail loud if absent/empty); enumerate unread messages in inbox/{serial}/ + inbox/{base-serial}/; for each, extract sender + subject + file mtime (age); classify STOP-class via the .000 grep rule; emit the §3.2 tiered verdict; exit code: 0 = pass (empty or acked), non-zero = blocked.</step>
    <step>Phase 2 -- Implement the tiered verdict: empty -> exit 0 silent; routine pending -> print each (sender / subject / age), exit non-zero; the caller re-invokes with the ack env var HALT_ACK=1 to pass. STOP-class present -> print loudly, exit non-zero (hard-block), UNLESS the audited override env var is supplied. The ack and the override are BOTH non-interactive env-var / re-invocation gates -- the checkpoint NEVER reads stdin (every consumer is an agent Bash-tool call with no TTY; a stdin `read` would hang the deploy indefinitely).</step>
    <step>Phase 2 -- Implement the audited override: an override flag/token that, when supplied, appends a structured line to org/halt-gate-override-audit.log (timestamp, agent serial, the STOP message sender + subject, the deploy context) and then exits 0. Mirror the safe-commit.sh `--force` audit pattern.</step>
    <step>Phase 3 -- shellcheck the library clean. Run the anchor-reproduction test (below).</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Read docs/architecture/HALTGT_SEVERITY_CONVENTION.md + inspect org/mcp/inbox/ layout + .comp-graph/.agent_context + .tools/safe-commit.sh (override-audit precedent).</run>
        <expect>The .000 match rule is transcribable into a shell grep; the inbox dir structure and unread-vs-read distinction are confirmed; the safe-commit.sh `--force` audit pattern is the model for the override log. comp-* tools N/A -- `.tools/` shell + org/mcp are not graph-modeled (PRD §5).</expect>
        <if_mismatch>If HALTGT_SEVERITY_CONVENTION.md is absent or its rule is not transcribable, STOP -- the .000 gate is not satisfied; MCP COO~B.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>shellcheck .tools/halt-gate-check.sh</run>
        <expect>shellcheck exits 0 (clean) -- no SC errors. No use of pgrep/pkill/flock/pidof/setsid/wget without a `command -v`-guarded fallback (CLAUDE.md Rule 16 / PRD R3).</expect>
        <if_mismatch>Fix every shellcheck finding before commit; replace any banned utility with a guarded fallback.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Anchor-reproduction test: (1) empty inbox -> run the checkpoint; (2) seed a routine message -> run; (3) seed a `[STOP]`-subject message -> run; (4) serial-detection failure -> run with .comp-graph/.agent_context absent; (5) run with no stdin attached (`&lt;/dev/null`) in every verdict path.</run>
        <expect>(1) exits 0 silently. (2) surfaces the message (sender/subject/age) and exits non-zero; a re-invocation with HALT_ACK=1 exits 0. (3) hard-blocks (non-zero exit); supplying the override env var exits 0 AND appends an audit line to org/halt-gate-override-audit.log. (4) fails loud / non-zero -- never silently passes. (5) the checkpoint completes (does not hang) in every verdict path with no stdin attached.</expect>
        <if_mismatch>Any deviation -- especially case (4) silently passing, case (3) not auditing, or case (5) hanging -- is a checkpoint correctness defect. Do not mark complete; fix and re-run.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Local-runtime shell tooling -- no data, no Lambda, no S3, no silver/bronze script. No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: .tools/halt-gate-check.sh (new) ; org/halt-gate-override-audit.log (new, created on first override)
    also_in_to: ADHC_HALTGT.002 + ADHC_HALTGT.003 both SOURCE this library -- they are downstream consumers, gated on this TO. No concurrent writer to .tools/halt-gate-check.sh.
    last_write_owner: 0.7.0_AE_CloudOps owns the full HALTGT lane.
    required_action: This TO gates .002 and .003. Land the library with a stable sourceable interface (documented function names + exit-code contract) so .002/.003 wire against a fixed surface.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">.tools/halt-gate-check.sh exists -- sourceable library + directly-runnable form -- resolving the agent serial from .comp-graph/.agent_context and reading inbox/{serial}/ + inbox/{base-serial}/ for unread messages.</ac>
    <ac id="AC2">Tiered verdict per PRD §3.2: empty inbox exits 0 silent; a routine pending message surfaces (sender/subject/age) and exits non-zero; a STOP-class message hard-blocks (non-zero exit). The ack mechanism is NON-INTERACTIVE -- the checkpoint never reads stdin: a routine-message block surfaces the messages and exits non-zero, and the caller re-invokes the deploy with the ack env var HALT_ACK=1 set to pass. Rationale: every consumer is an agent Bash-tool call with no TTY; a stdin `read` would hang the deploy indefinitely.</ac>
    <ac id="AC3">A STOP-class hard-block is bypassable via an audited override token; the override appends a structured line (timestamp, serial, STOP sender+subject, context) to org/halt-gate-override-audit.log and then exits 0.</ac>
    <ac id="AC4">Serial-detection failure (absent/empty .comp-graph/.agent_context) fails loud (non-zero exit) -- the checkpoint NEVER silently passes when it cannot determine its inbox (PRD R4).</ac>
    <ac id="AC5">shellcheck clean; Git Bash 3.6.7-safe -- no banned utility without a `command -v`-guarded fallback (CLAUDE.md Rule 16).</ac>
    <ac id="AC6">No emoji. Session log with the Compiler Tools section reproducing the Phase 2 shellcheck + the Phase 3 4-case anchor-reproduction test with observed results. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="create">.tools/halt-gate-check.sh</file>
    <file action="create">org/halt-gate-override-audit.log (created on first override; may ship as an empty/header file)</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">.tools/halt-gate-check.sh -- the HALTGT checkpoint core library. Note: .tools/ is gitignored-prefix -- use `git add -f` so safe-commit.sh sees the new file.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section (shellcheck + 4-case anchor test). RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT let the checkpoint silently pass when it cannot determine the agent serial -- fail loud. A false-green checkpoint is worse than no checkpoint.</rule>
    <rule>Do not hard-block on routine messages -- that is the R1 dead-gate risk; routine = surface + ack, STOP-class only = hard-block (PRD §3.2 / R1).</rule>
    <rule>Do not use pgrep/pkill/flock/pidof/setsid/wget without a `command -v`-guarded fallback (CLAUDE.md Rule 16).</rule>
    <rule>Do not wire the library into any deploy path here -- that is ADHC_HALTGT.002 / .003. This TO ships the library only.</rule>
    <rule>Do not mark messages read -- the checkpoint enumerates, it does not mutate the inbox.</rule>
    <rule>Do not implement the ack or the override as an interactive stdin prompt (`read`) -- every consumer is an agent Bash-tool call with no TTY; a stdin read hangs the deploy indefinitely. Both are env-var / re-invocation based (HALT_ACK=1 for the routine ack; the override env var for a STOP-class bypass).</rule>
  </do_not>
</task_order>
