# Proposal: make the merge's row gate fast -- changes 2 and 3 (change 1 has landed)

**From:** `0.0.0_AB_MSTR` (laptop), 2026-10-05, on Andrew's word at this terminal: "Yes start with change 1 now." and
"Then write a proposal for changes 2 and 3."
**For:** `1.0.0_SA_CTO` (owner of `.tools/surprise-row-gate.py`) and `2.0.0_SA_COO` (owner of `.tools/safe-merge.sh`).
**Status:** a proposal. Nothing in it is implemented. Neither change adds, removes or loosens a check.

## 1. The measurement behind it

One merge was rebuilt in a scratch worktree and the gate was run on it under `cProfile`: laptop CLOUD 81ba0160e5 merged
with origin f5d6919117, `--no-commit`, 743 staged paths, 38 surprise-channel files, about 9 projects.

| Run | Wall seconds | git processes started | `_blob` calls | Distinct reads |
|---|---|---|---|---|
| Before change 1 | 1,149 | 21,962 | 11,144 | not counted |
| After change 1 (the memo) | 171 | 2,661 | 11,144 | 1,274 |

- Before: 1,125 of 1,147 profiled seconds were inside `_blob`. `_seats_with_open_orders` alone made 8,828 of the
  11,144 calls (855 s), because it re-reads every task order of a project once per channel file.
- After: the gate's 332 output lines are byte-identical to the run before (`diff` rc 0, 0 lines), and `--self-test`
  reads "0 arm(s) failed of 229".
- What is left after change 1: 144 of 170 s is still `_blob_read`, 1,274 distinct reads at two git start-ups each
  (`ls-tree` or `ls-files -s`, then `show`), about 0.11 s per read on this laptop.
- On a real merge the gate still runs TWICE on the same index: `safe-merge.sh:422-424` and pre-commit step 9
  (`.git/hooks/pre-commit:177`). Today's merge showed it: first pass 12:34-12:51 local, second pass from 12:51.

## 2. Change 2 -- do not grade the same index twice (owner: `2.0.0_SA_COO`, with the hook's owner)

**What:** when `safe-merge.sh` has just graded the exact tree it is about to commit, pre-commit step 9 does not run
the row gate again.

**Mechanism, one identity and no flag:**
1. After its own grade passes, `safe-merge.sh` computes the tree of the private index it graded
   (`GIT_INDEX_FILE="$_PRIV_IDX" git write-tree`) and the blob id of the gate file that graded it
   (`git hash-object .tools/surprise-row-gate.py`), and exports both for the `git commit` it runs at line 482, for
   example `SAFE_MERGE_GRADED_TREE` and `SAFE_MERGE_GRADED_GATE`.
2. Pre-commit step 9 recomputes both from what it is actually committing (`git write-tree` on the index the hook
   sees, which is the same private index; `git hash-object` on the gate). If both equal the exported values it prints
   one line naming the tree and skips the gate. On any mismatch, or when either variable is empty, it runs the gate
   exactly as today.

**Why this is safe:** the skip is keyed on the content being committed, not on a claim. A different index, a peer's
staged path, or an edited gate changes one of the two ids and the gate runs. A bare `git commit` never has the
variables. A hand-exported pair that matches is a statement that this exact tree was graded by this exact gate, which
is checkable after the fact from the commit's tree.

**What it gives up, stated plainly:** `safe-merge.sh:446-448` treats a downstream refusal as proof its own grade was
wrong. With the skip, the row gate no longer cross-checks itself; the other pre-commit gates still run. The two runs
have been one program on one index since the private-index change, so the cross-check has had nothing to disagree
with.

**The alternative, if the owners prefer it:** keep the hook's run and drop `safe-merge.sh`'s own, since the hook also
refuses before anything lands. That loses the earlier, clearer refusal text and the vacuous-pass guard at lines
395-408, so the tree-identity skip is the recommendation.

**Saving:** one full gate run per merge. At today's sizes that is 171 s after change 1.

**Cost and non-application:** about 10 lines in each of two files and one new regression arm in each self-test (a
mismatched tree must still run the gate). It does not apply to an ordinary `safe-commit.sh` commit, which grades once
already.

## 3. Change 3 -- one git process for all reads (owner: `1.0.0_SA_CTO`)

**What:** `_blob_read` stops starting two git processes per read and asks one long-lived `git cat-file --batch`
process instead.

**Mechanism:**
1. Start `git cat-file --batch` once per grading run, with `cwd=root` and the inherited environment, so
   `GIT_INDEX_FILE` still selects the private index for `:path` specs.
2. For each read, write `<ref>:<path>\n` (or `:<path>\n` for the index) and read the reply header. A header of
   `<sha> blob <size>` is followed by exactly `<size>` bytes and a newline; decode them as today
   (`utf-8`, `errors="surrogateescape"`). A header of `<spec> missing` is the not-there case.
3. Keep the three states the gate depends on (`_blob`'s docstring, RC2): `cat-file --batch` says `missing` for a bad
   REF as well as for a missing PATH, which is the same trap the docstring records for `cat-file -e`. So verify each
   distinct ref once per run with `git rev-parse -q --verify <ref>^{commit}`; under a verified ref, `missing` is
   ABSENT. An unverifiable ref, a dead or timed-out batch process, or a malformed header is ERROR, and ERROR is never
   memoised.
4. The memo from change 1 stays in front of it.

**Expected saving, an estimate until built:** the 144 s left in reads becomes the cost of one process plus 1,274 pipe
round-trips, which should be a few seconds. The gate would then be dominated by the roughly 25 s outside `_blob`.

**Cost and non-application:** about 60 lines, plus self-test arms for the three states through the new path (present,
absent path under a good ref, bad ref) and for a batch process that dies mid-run. `--self-test` and `--acceptance`
keep the memo off, as now; whether they also use the batch reader is the owner's call, since the self-test rewrites
its scratch repos between reads and a long-lived reader would have to be restarted per scratch repo.

## 4. What the three changes add up to

| State | Row-gate time in one merge of this size |
|---|---|
| Before any change (measured twice today) | about 2 x 1,149 s, 38 minutes |
| Change 1 only (measured once) | 2 x 171 s, about 6 minutes |
| Changes 1 and 2 | 171 s |
| Changes 1, 2 and 3 (estimate) | under 1 minute |

The other pre-commit gates were not profiled. Today they were a small share of the commit stage, but that share is
not measured here.

## 5. A separate point Andrew raised, for the mass-deletion gate's owner

Andrew at this terminal, 2026-10-05, verbatim: "unexplained deletions are always me", "agents dont do unexplained
deletions ever", "because agents use safe commit for all changes". On 2026-10-04 that gate refused a merge commit
over 38 deletions that site-Z seats had already committed through the wrapper, and cost one full re-run. A merge that
only carries deletions its other parent already made deletes nothing itself. Whether the gate should note those,
as the row gate now notes carried row changes, is the owner's ruling; it is recorded here so it is not lost.
