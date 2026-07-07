# Task Order: ADHC_COMMITGATE -- consolidate ds-commit-gate.sh's per-check forks + rename off the misleading "ds-" prefix

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-adhc-commitgate</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <dispatch_state>DISPATCHED 2026-07-07 -- MSTR relay of CTO APPROVED arch-gate (Andrew-direct origin). SEQUENCE BEFORE NFRA_CMTQUE.TO-6R's load-test (CTO + MSTR both confirmed) -- the load-test must measure this corrected design, not the current fork-heavy baseline.</dispatch_state>
    <gate_note>Andrew-direct origin: this script is the likely DOMINANT fork-volume source stressing the Huntress EDR process (bigger than CMTQUE's mutex contention), discovered while diagnosing today's post-reboot concurrency pressure. Priority: land before TO-6R, not urgent-emergency otherwise.</gate_note>
  </metadata>

  <objective>`.tools/ds-commit-gate.sh` currently loops per-.py-file and forks ~6 separate python subprocesses per file (py_compile, ds-precommit-check.py, ruff, comp_constants_cli.py, manifest_check_cli.py, log_open_lint.py) -- a 10-file commit forks ~60 processes. Consolidate the python-invoked checks into a single python process that runs all checks per file via direct import/call (not subprocess), batched across every file in one invocation rather than re-forked per file. Also rename off the misleading "ds-" prefix -- the gate is universal/ANY-lane (every agent's every .py/.sh commit runs through it), not DS-specific.</objective>

  <requirements>
    <requirement id="1">Consolidate the python-side checks (ds-precommit-check.py's AST scan, ruff invocation, comp_constants_cli.py, manifest_check_cli.py, log_open_lint.py) into ONE python process per commit invocation -- direct function calls/imports, not `subprocess`/shell-outs to separate scripts. py_compile may stay a distinct call if consolidating it isn't straightforward (compileall accepts multiple files in one process) -- minimize total process count, don't force a specific internal shape.</requirement>
    <requirement id="2">Batch across ALL files passed to the gate in one process invocation, not one process-spawn per file. The current shell loop (`for f in "$@"`) re-invokes all 6 python subprocesses per file; the consolidated version processes the whole file list in a single python process lifetime.</requirement>
    <requirement id="3">PARITY IS THE BAR (CTO condition 1): identical pass/fail verdicts + identical per-check attribution in output vs today's gate, across a representative test set covering (a) all-pass, (b) each individual check failing alone, (c) multiple checks failing simultaneously on the same file. Explicit before/after regression comparison required in the session log -- "runs faster" alone does not satisfy this requirement.</requirement>
    <requirement id="4">Watch for `sys.exit()`/`SystemExit` in any of the 5 consolidated scripts -- these are standalone-CLI leftovers that will kill the whole shared process if not converted to return codes/exceptions the orchestrator catches. One check's failure must not swallow or misattribute a later check's result. Also audit for import-time side effects or global state in any of the 5 scripts that could leak across checks now sharing one process (CTO condition 2).</requirement>
    <requirement id="5">Rename off "ds-commit-gate.sh" (CTO condition 3). `commit-gate.sh` is the suggested name unless a better one emerges. Before renaming: comp-grep/grep the literal string "ds-commit-gate" across the FULL repo (docs, CLAUDE.md Rule 14/14a, any git-hook wiring, org/XXX.md, memory files, skill docs, other .tools scripts) and update EVERY reference in the SAME commit as the rename -- do not leave a stale name anywhere. A preliminary grep already surfaced hits in CLAUDE.md, `.claude/skills/{cloud-ops,freeform,gold-runner-code-review,work}/SKILL.md`, `.tools/commit-worker.sh`, and several `data/*/scripts/gold/gold_validate_config.yaml` + docs files -- treat this as a starting list, not exhaustive; your own comp-grep pass is authoritative.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-blast ds-commit-gate.sh</run>
        <expect>Enumerates every caller (git hooks, safe-commit.sh chain, commit-worker.sh, any CI wiring) so the rename touches every real call site, not just the docs hits found by a plain grep.</expect>
        <if_mismatch>If comp-blast doesn't resolve shell-script callers cleanly, fall back to comp-grep across the full repo (not raw grep per Rule 21) and document why comp-blast didn't cover it.</if_mismatch>
      </step>
      <step>
        <run>comp-grep "ds-commit-gate" .</run>
        <expect>Full reference list across docs/skills/scripts/memory -- superset of the preliminary list in requirement 5 above.</expect>
        <if_mismatch>N/A -- this IS the discovery step; whatever it finds becomes the update list.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Run the before/after parity test set (all-pass, each-check-fails-alone x5, multi-fail) against both the current gate and the consolidated version</run>
        <expect>Identical exit codes + identical per-check BLOCKED/OK messages across every test case.</expect>
        <if_mismatch>STOP. Do not commit until parity holds -- this is CTO's non-negotiable condition 1.</if_mismatch>
      </step>
      <step>
        <run>py_compile + import the consolidated module standalone (outside a commit) to confirm no import-time side effects fire unexpectedly</run>
        <expect>Clean import, no unexpected stdout/stderr/state mutation on bare import.</expect>
        <if_mismatch>STOP. Isolate and fix the side-effecting import before proceeding -- this is CTO's condition 2.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-grep "ds-commit-gate" . (re-run post-commit)</run>
        <expect>Zero hits remaining (all references updated to the new name in the same commit).</expect>
        <if_mismatch>Surface immediately -- a stale reference post-rename is a broken pointer for the next agent who reads it.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>Sequencing: this TO's completion is a precondition for NFRA_CMTQUE.TO-6R's load-test (CTO + MSTR confirmed) -- notify 2.0.0_SA_COO on completion so TO-6R's quiet-window trigger can proceed against the corrected baseline.</item>
    <item>Universal impact: every agent's every .py/.sh commit runs through this gate. A regression here blocks the ENTIRE fabric's commit path -- the parity requirement (req #3) is the safety net, treat it as non-negotiable, not a nice-to-have.</item>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion>Consolidated gate produces byte-identical pass/fail verdicts + per-check attribution vs the current gate across the full before/after parity test set (req #3) -- cited in the session log with the actual test commands + outputs, not a summary claim.</criterion>
    <criterion>Fork count per commit invocation measurably reduced -- cite the actual before/after process count for a representative multi-file commit.</criterion>
    <criterion>Zero remaining "ds-commit-gate" references anywhere in the repo post-rename (comp-grep output showing 0 hits, reproduced in the session log).</criterion>
    <criterion>Session log's Compiler Tools section reproduces every &lt;run&gt; from &lt;compiler_tools_mandate&gt; with observed output and explicit pass/fail vs &lt;expect&gt;. Missing rows = REWORK.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="source">.tools/ds-commit-gate.sh</ref>
  </references>
</task_order>
```
