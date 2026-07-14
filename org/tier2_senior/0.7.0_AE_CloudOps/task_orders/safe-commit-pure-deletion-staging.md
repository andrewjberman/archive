# safe-commit pure-deletion staging fix (ADHC_COMMITGATE lineage)

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO (fix shape RULED by 1.0.0_SA_CTO 081918Z; incident 0.6.2 deletion-chain 081645Z)</issued_by>
<date>2026-07-14</date>
<status>staged</status>
<!-- Original scope CLOSED-ACCEPTED @ db39dcf9d (COO second-observer 11/11 incl. e4 mutant kill, 2026-07-14).
     Status re-flipped to staged 2026-07-14 19:0xZ SOLELY for AMENDMENT-2 (CTO-ratified 190021Z);
     acceptance criteria 1-6 remain closed and are NOT re-opened. -->
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

## AMENDMENT-1 (2026-07-14 17:0xZ, COO per CTO gate-candidate routing 170201Z): __pycache__/.pyc exclusion

THE DEFECT (measured TWICE in 2 days, identical mechanism): commit-gate's py_compile step CREATES
`__pycache__/*.pyc` DURING the commit run itself; a directory pathspec then sweeps those binaries into
the commit. Fired: c36710809 (cleaned @ a58c19bfb) + fbdb335b4 (cleaned @ 36005c8b7), both 0.6.2,
root-caused by them 170126Z. Two cleanup commits from one mechanism = the class gets a GATE, not care.

FIX SHAPE (mechanical; land in the SAME commit as the staging branch -- one wrapper touch, one announce):
safe-commit filters `__pycache__/` directories + `*.pyc` files out of the staged set inside its lock
(or commit-gate REFUSES them staged -- assignee picks whichever composes cleaner with the pure-deletion
branch). The exclusion prints per path (`SKIP: pycache-artifact`), NEVER silent -- same ZERO_CHECKS
lesson as the deletion skip.

TEST CLASS (e): a directory pathspec whose tree contains a fresh .pyc (created by the gate's own
py_compile in the same run) commits WITHOUT the .pyc; positive control run SEPARATELY: the same pathspec
shape with a legitimate .py lands the .py. MUTANT: bypass the filter and confirm the test FAILS -- an
exclusion that cannot fail is not a control.

<phase id="3-amendment" when="after commit">
  <step>
    <run>REPLAY the two incident pathspec shapes (c36710809 / fbdb335b4 directory pathspecs) through the fixed wrapper with fresh py_compile artifacts present</run>
    <expect>Both commits land with ZERO .pyc / __pycache__ entries in the committed tree (verify with git show --stat); SKIP lines printed per excluded artifact.</expect>
    <if_mismatch>Fix is not acceptance-complete -- reopen, do not close the TO.</if_mismatch>
  </step>
</phase>

## AMENDMENT-2 (2026-07-14 19:0xZ, COO per CTO gate ratification 190021Z): log-commit source-sweep guard

THE DEFECT (measured, 0.7.0's ES-1 grounding @ 85f37e915): commit 64b6b9d65 (2026-04-27, subject
"log(COMP_LEARNS.session13)...") DELETED all 15 source files of infra/aws/lambda/exec-summary-generator/
(~1,030 lines incl. the 455-line handler) and SAT UNNOTICED 11 WEEKS -- deployed lambda repo-unrebuildable
(Rule-10-class), source-map listing 15 phantom files. Same sweep-deletion family as AMENDMENT-1's pycache
class (a broad pathspec riding an unrelated commit), except this one took SOURCES. The pycache fix
(db39dcf9d) does not cover it: a source-tree sweep inside a log commit remains structurally possible.

FIX SHAPE (CTO-ratified 190021Z; land atomically + fabric-announce, same discipline as the staging branch):
a log-prefixed commit (subject class: `log(`-style session-log commits; assignee defines the predicate
conservatively) whose staged set DELETES non-log paths (any deletion outside the session-log/org-record
surface) REFUSES-OR-SCREAMS inside safe-commit -- assignee picks refuse vs contamination-style scream by
whichever composes cleaner with the existing staging branch, but silence is not an option, and the loud
path prints EVERY offending deletion per path (ZERO_CHECKS lesson, same as the deletion/pycache skips).
Audited override permitted (`# never-override:` class) for a legitimately intended mixed commit.

TEST CLASS (f): REPLAY 64b6b9d65's exact shape as the acceptance mutant -- a log( commit whose pathspec
sweeps lambda source deletions must refuse-or-scream; positive control run SEPARATELY: a log( commit
deleting only log-surface paths lands clean; MUTANT: bypass the guard and confirm the test FAILS (a guard
that cannot fail is not a control).

GO: STAGED behind Andrew's parity push (his ~18:5xZ all-channel drain directive owns every AE lane
tonight). COO GO fires when your lane frees post-parity; possibly batched with the ES-1 restore
(same ruling window, CTO 190021Z -- restore-first w/ member-level byte-tie, separately assigned).

<phase id="3-amendment2" when="after commit">
  <step>
    <run>REPLAY 64b6b9d65's commit shape (log( subject + staged source-file deletions) through the fixed wrapper; positive control (log( subject + log-only deletions) as a SEPARATE invocation; then the mutant (guard bypassed)</run>
    <expect>Target refuses-or-screams with per-path deletion lines; positive control lands clean; mutant run FAILS the test.</expect>
    <if_mismatch>Fix is not acceptance-complete -- reopen, do not close AMENDMENT-2.</if_mismatch>
  </step>
</phase>

## <acceptance_criteria>
1. One measured staging branch per the ruled shape -- no new mode flag, no caller-visible convention change.
2. `SKIP: deleted` printed per deleted path; never a silent skip.
3. Four new test classes green (incl. staged rename); untracked+missing fails loud.
4. Replay acceptance: both historical override cases commit clean without override (transcript committed).
5. Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail vs <expect>.
6. AMENDMENT-1: test class (e) green INCLUDING its mutant kill; both incident pathspec shapes replayed with zero .pyc in the committed tree; exclusion SKIP lines never silent.
7. AMENDMENT-2: test class (f) green INCLUDING its mutant kill; 64b6b9d65's shape replayed refuse-or-scream with per-path loudness; positive control separate + clean; fabric announce after landing.
</acceptance_criteria>
