# safe-commit pure-deletion staging fix (ADHC_COMMITGATE lineage)

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO (fix shape RULED by 1.0.0_SA_CTO 081918Z; incident 0.6.2 deletion-chain 081645Z)</issued_by>
<date>2026-07-14</date>
<status>staged</status>
<go>Staged behind your event slots (14:15Z cot verify, post-15:45Z C9) and any V2-7 gate opening -- pick it up in slack; COO GO rides this TO, no further gate. No urgency (the audited-override path held; the fix keeps it rare).</go>
<project>ad-hoc tooling (ADHC_COMMITGATE lineage -- .tools/safe-commit.sh + .tools/commit-gate.sh)</project>

## THE DEFECT (measured, 0.6.2 081645Z)
safe-commit's `git add -f` staging hard-fails rc=128 when a pathspec is a PURE DELETION (tracked file
absent from the worktree) -- the wrapper structurally cannot commit a file removal. Cost this chain: two
audited never-override bare commits on exactly the closure-shaped steps (tf removal + ledger-close JSON).
A wrapper that cannot express removal pushes every closure step off the safe path.

## THE RULED FIX SHAPE (CTO 081918Z -- build to this, not around it)
1. STAGING: inside the wrapper's lock, per pathspec -- if the path is TRACKED but ABSENT from the
   worktree (pure deletion), stage with `git add -A -- <path>` (stages deletions correctly, no-op
   surprise-free on present files); else the existing `git add -f`. ONE branch on measured file state.
   Explicitly NOT a --deletion mode flag (a second calling convention is a second thing to forget;
   the wrapper detects the state itself).
2. LINT: commit-gate SKIPS deleted paths (py_compile/AST/ruff have no bytes to check) -- but the skip
   prints per file (`SKIP: deleted`), NEVER silent: a gate run that checked nothing stays
   distinguishable from a gate run that passed everything (the ZERO_CHECKS lesson).
3. TESTS: extend the gate tests with (a) pure deletion, (b) mixed add+delete in one commit,
   (c) tracked-vs-untracked-missing -- untracked+missing = pathspec error, still FAILS loud (caller
   typo, not a deletion), (d) staged RENAME (assignee's own repro, 0.7.0 07:5xZ committing the
   contract-note git mv: R staged = add-side + delete-side, the wrapper must stage BOTH from a
   pathspec naming both; the old path exists in neither worktree nor unstaged index).

## <compiler_tools_mandate>
<phase id="1" when="before write">
  <step>
    <run>bash .tools/hooks/tests/test_never_rules_gate.sh</run>
    <expect>Existing suite green BEFORE the change (baseline; the wrapper shares the hook surface).</expect>
    <if_mismatch>STOP. A red baseline means the estate moved under this TO -- surface to COO before touching the wrapper.</if_mismatch>
  </step>
</phase>
<phase id="2" when="before commit">
  <step>
    <run>the extended gate tests (all three new classes) + the full existing suite</run>
    <expect>Green including (a)/(b)/(c); untracked-missing case FAILS loud.</expect>
    <if_mismatch>STOP. Do not commit a wrapper change on a partial suite.</if_mismatch>
  </step>
</phase>
<phase id="3" when="after commit">
  <step>
    <run>REPLAY the two 0.6.2 override cases through the fixed wrapper (a scratch tf-file removal + a scratch ledger-close JSON removal, same shapes)</run>
    <expect>Both commit CLEAN with NO override; the historical override audit trail untouched.</expect>
    <if_mismatch>Fix is not acceptance-complete -- reopen, do not close the TO.</if_mismatch>
  </step>
</phase>
</compiler_tools_mandate>

## <cross_domain_coordination>
.tools/safe-commit.sh + .tools/commit-gate.sh are EVERY agent's commit path -- land the change atomically
(wrapper + gate + tests in one commit) and announce on the fabric channel after landing so no agent
mid-commit is surprised by new SKIP lines. No other shared files.
</cross_domain_coordination>

## <acceptance_criteria>
1. One measured staging branch per the ruled shape -- no new mode flag, no caller-visible convention change.
2. `SKIP: deleted` printed per deleted path; never a silent skip.
3. Four new test classes green (incl. staged rename); untracked+missing fails loud.
4. Replay acceptance: both historical override cases commit clean without override (transcript committed).
5. Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail vs <expect>.
</acceptance_criteria>
