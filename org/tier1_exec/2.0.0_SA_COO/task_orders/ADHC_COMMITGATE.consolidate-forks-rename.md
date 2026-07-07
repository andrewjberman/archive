# Task Order: ADHC_COMMITGATE -- consolidate ds-commit-gate.sh's per-check forks + rename off the misleading "ds-" prefix

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-adhc-commitgate</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <dispatch_state>DISPATCHED 2026-07-07 -- MSTR relay of CTO APPROVED arch-gate (Andrew-direct origin). SEQUENCE BEFORE NFRA_CMTQUE.TO-6R's load-test (CTO + MSTR both confirmed) -- the load-test must measure this corrected design, not the current fork-heavy baseline. CLOSED 2026-07-07T16:05Z -- all 4 requirements met, parity proven via a 9-fixture before/after matrix (3 real bugs caught+fixed by the fixtures, not assumed away).</dispatch_state>
    <gate_note>Andrew-direct origin: this script is the likely DOMINANT fork-volume source stressing the Huntress EDR process (bigger than CMTQUE's mutex contention), discovered while diagnosing today's post-reboot concurrency pressure. Priority: land before TO-6R, not urgent-emergency otherwise.</gate_note>
  </metadata>

  <objective>`.tools/ds-commit-gate.sh` currently loops per-.py-file and forks ~6 separate python subprocesses per file (py_compile, ds-precommit-check.py, ruff, comp_constants_cli.py, manifest_check_cli.py, log_open_lint.py) -- a 10-file commit forks ~60 processes. Consolidate the python-invoked checks into a single python process that runs all checks per file via direct import/call (not subprocess), batched across every file in one invocation rather than re-forked per file. Also rename off the misleading "ds-" prefix -- the gate is universal/ANY-lane (every agent's every .py/.sh commit runs through it), not DS-specific.</objective>

  <requirements>
    <requirement id="1" status="met">Consolidate the python-side checks into ONE python process per commit invocation -- direct function calls/imports, not `subprocess`/shell-outs to separate scripts. py_compile may stay a distinct call if consolidating it isn't straightforward. `.tools/commit_gate_runner.py`: all 5 scripts' pure functions (scan_file/cmd_check/cmd_scan/main(argv)) called in-process; py_compile fully consolidated too (stdlib, trivially importable). Only ruff stays a subprocess -- no stable public Python API exists (Rust binary, CLI-only), and coupling to internal bindings would be fragile against the pinned ruff==0.15.11 contract.</requirement>
    <requirement id="2" status="met">Batch across ALL files in one process invocation. `process_files(files)` runs the full argv list in a single python process lifetime; ruff is the only remaining per-file subprocess (unavoidable, see #1).</requirement>
    <requirement id="3" status="met">PARITY IS THE BAR. 9-fixture before/after matrix (all-pass, 6 individual-check-failures incl. shell, 1 multi-fail, 1 manifest-check advisory/non-blocking) -- every case `cmp -s` byte-identical + matching exit code vs the real `ds-commit-gate.sh`. 3 real bugs were caught and fixed by the fixtures (py_compile print-order, stdout/stderr buffering interleave, Windows CRLF-translation scope) -- full detail + exact commands in the session log (org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-07-07/adhc_commitgate_fork_consolidation_and_rename.md, commit 517e632b2).</requirement>
    <requirement id="4" status="met">sys.exit()/SystemExit audit: confirmed by reading all 5 scripts top-to-bottom BEFORE writing any code -- none of the functions this runner calls (scan_file/cmd_check/cmd_scan/log_open_lint.main) call sys.exit() themselves; only each script's own `if __name__=="__main__":` guard does, never reached. No import-time side effects found; independently re-verified via a StringIO-redirected import test (0 output). That same test caught a real defensive gap (reconfigure() assumes a real stream) -- fixed with contextlib.suppress, re-verified no parity regression.</requirement>
    <requirement id="5" status="met">Renamed to commit-gate.sh. comp-blast NOT-FOUND (documented, fell back to comp-grep per the TO's own fallback). comp-grep "ds-commit-gate" . -- 210-line/~70-file sweep, superset of the preliminary list. Every LIVE reference updated across 3 commits (mine: 3ebdcf9bf AE/ANY-lane + b7f1dce45 defensive fix; CTO's: 4ea728d53 for CLAUDE.md + 18 docs/architecture files, ANY_CTO/BASE_EXEC-lane, owned-paths-blocked for AE; DS routed separately for 2 POD4-lane gold_validate_config.yaml comment fixes). Deliberately excluded 35 dated docs/briefs/*.md + 5 CHANGELOG.json + org/compiler-tools-log.md + 2 point-in-time deploy-notes as historical record, not live pointers (flagged explicitly in both commit messages, not silently decided). One straggler (docs/architecture/COMP_LEARNS_DS_ROLE_ADDENDUM.md) dropped entirely per CTO relay of Andrew-direct: file is deprecated, no CompLearns fabric exists to own it.</requirement>
  </requirements>

  <closure_evidence>
    Commits: 3ebdcf9bf, b7f1dce45 (AE), 4ea728d53 (CTO). Session log:
    org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-07-07/adhc_commitgate_fork_consolidation_and_rename.md
    (517e632b2) -- contains the full 9-fixture parity matrix with exact commands + the 3 bugs
    caught/fixed. Fork-count reduction: 6/file -> 1/file (ruff only) + 1 shared runner process;
    a representative 10-file commit goes from 60 forked subprocesses to 11.
  </closure_evidence>

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
