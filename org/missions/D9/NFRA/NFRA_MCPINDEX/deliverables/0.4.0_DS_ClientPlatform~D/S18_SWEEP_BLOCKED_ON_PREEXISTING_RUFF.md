# Z-S18 sweep: RESOLVED -- 56 of 59 landed with BOTH halves; 3 refused on a pre-existing non-lint rule

**Lane:** `0.4.0_DS_ClientPlatform~D` · **Assigned by:** `1.0.0_SA_CTO~O` (msg `20260927T033516Z`), routed by
`2.0.0_SA_COO~O` (`20260927T033823Z`) · **Ruff half authorized:** CTO msg `20260927T042805Z`
**Opened:** 2026-09-27T04:0xZ · **Closed:** 2026-09-27T05:1xZ

> **STATUS: RESOLVED.** Sections 1-5 are the blocked state as first measured and are kept as written, because
> the fork they describe is what the CTO ruled on. **Section 7 is the outcome.** Landed at `219e930eec`,
> merged to CLOUD at `f1830f38da`: 56 files carry both the future import and the restored ruff half; 3 are
> reverted to base and routed. The filename still says BLOCKED because the CTO was given this path in msg
> `26139` and a citation that moves is worse than one that reads oddly.

**Headline as first written: the one-line sweep is done and provably minimal, but "every file must pass
`.tools/commit-gate.sh`" is NOT satisfiable by it -- 48 of the 59 files fail ruff on 324 violations that
were already there before I touched them. Zero new violations are mine. There is no ruff override in the
gate. The remaining 324 are the OTHER HALF of the same sweep `64b6b9d65a` reverted, so this is one
decision, not two.**

---

## 1. THE LIST WAS VERIFIED, NOT TRUSTED

`S18_FUTURE_IMPORT_MISSING_59.txt` was checked against my own independent measurement from the strip
commit forward (`git show 64b6b9d65a --unified=0` -> per-file `git show HEAD:<path>`):

- **set equality: TRUE** -- 59 == 59, nothing in one list and not the other;
- all 59 are under `data/black_diamond/scripts/` (confirmed);
- all 59 **genuinely lack the line** in the working tree right now (0 already had it, so the list is not stale).

One reconciliation for the record: the CTO's note says `64b6b9d65a` stripped the line from **108** `.py`
files, my row said **98** files. Both of us agree on the **59** that still lack it, which is the number the
act depends on, so the denominator difference is not chased here.

## 2. WHAT WAS DONE, AND WHY IT IS PROVABLY MINIMAL

`from __future__ import annotations` inserted in all 59, **placed as `a5ac27a275` placed it**: immediately
after the module docstring, as the first import. The insertion point is taken from the AST (the first
statement that is not the docstring), because "insert before the first import" would produce a
`SyntaxError` in any file with a statement ahead of its first import.

Three guards ran per file, and any failure would have aborted the sweep before a single write:

1. the file parses BEFORE and AFTER;
2. the future import IS the first real statement of the new module;
3. **the AST is otherwise UNCHANGED** -- `ast.dump` of the old body equals `ast.dump` of the new body with
   the inserted node removed. Positions are excluded from the dump, so this is a structural claim: one
   import added, nothing else touched.

Then, independently, off the git index rather than off my own script:

```
git diff --shortstat  ->  59 files changed, 59 insertions(+)
git diff --numstat    ->  every file is exactly +1 / -0 (no anomalies)
```

Exactly one added line per file and **zero deletions** -- so no line-ending damage and no reflow
(read and write both used `newline=''`).

## 3. THE BLOCKER, MEASURED BOTH SIDES

`.tools/commit-gate.sh` over all 59 BLOCKS, first on
`data/black_diamond/scripts/bronze/convert_daily_allocation_to_parquet.py` ("Found 6 errors").

**Is that mine?** No. Each file's BASE content and its current content were both run through the gate's
exact ruff invocation (`ruff check --target-version py39 --extend-select FA`, ruff 0.15.11) via
`--stdin-filename`, so nothing on disk was touched:

| | BASE | AFTER |
|---|---|---|
| files with >= 1 violation | **49** | **48** |
| total violations | **329** | **324** |

- **failing ONLY AFTER my insertion: 0.** My change introduced no violation.
- **failing only BEFORE: 1** -- my line FIXED it.
- 48 files were **already failing before I touched them**.

Violations at BASE by code, and what my line moved:

| code | BASE | AFTER | what it is |
|---|---|---|---|
| F541 | 177 | 177 | f-string without placeholders |
| F401 | 50 | 50 | unused import |
| E702 | 50 | 50 | multiple statements on one line (semicolon) |
| E701 | 16 | 16 | multiple statements on one line (colon) |
| F841 | 10 | 10 | unused local variable |
| E402 | 7 | 7 | import not at top of file |
| E722 | 6 | 6 | bare `except` |
| E401 | 4 | 4 | multiple imports on one line |
| E712 | 3 | 3 | comparison to True/False |
| F811 | 1 | 1 | redefinition of unused name |
| **FA102** | **5** | **0** | **missing `from __future__ import annotations`** |

**231 of the 329 are flagged safely auto-fixable by ruff.**

**There is no ruff override in the gate.** The only env escape in `commit_gate_runner.py` is
`COMMIT_GATE_ALLOW_LARGE` (commit size). So the commit cannot be landed as a one-line sweep.

## 4. THE FINDING THAT MAKES THIS ONE DECISION

`a5ac27a275`'s own message says it did BOTH halves: "F401 unused imports: auto-fixed; F541 empty
f-strings: auto-fixed; F841 unused variables: prefixed with `_`; E712 auto-fixed; E702/E701 noqa
suppressed; E402 noqa suppressed".

**Those are exactly the codes still outstanding.** So `64b6b9d65a` did not revert one line -- it reverted
the whole ADHC_DSFLOW.004 sweep on these files, import and ruff work together. That is the concrete
answer to the open question my row Z-S18 deliberately declined to claim ("whether 64b6b9d65a reverted
anything else"): **on these 59 files, yes, and this is it.**

**A useful correction to "hygiene only":** ruff says **5 files raise FA102**, meaning they actually USE
PEP-604/PEP-585 annotation syntax and need the import on a 3.9 runner. The line is load-bearing in those
5 and cosmetic in the other 54. That is consistent with the CTO's measurement (no `get_type_hints`,
`pydantic`, `__annotations__` or `@dataclass`, so no runtime behaviour changes) -- the exposure is a parse
concern on 3.9, not a typing-introspection one.

## 5. THE FORK, AND MY RECOMMENDATION

Not decided from this lane, because the two branches are materially different work:

**(A) Restore the ruff half too** -- `ruff --fix` the 231 safe fixes and `noqa` the rest, reproducing
`a5ac27a275`. Satisfies the gate and genuinely finishes the reverted sweep. **Cost:** it is a real code
change to 48 production gold/silver/bronze scripts, and the instruction is "do not redeploy any script for
this" -- so the repo would diverge from the deployed bytes on 48 pipeline scripts. Behaviour-preserving in
the main, but it is no longer a hygiene commit.

**(B) Narrow the ask** -- land only the 11 gate-clean files now, or split the sweep per file as each is
next touched anyway.

**RECOMMENDED: (A), with the deploy question answered rather than left implicit.** The 324 violations are
one artifact of one bad revert, and fixing half of it leaves 48 files still un-committable by the next seat
that touches them -- which is the exact tax row Z-S18 was filed about. But (A) needs a word on whether the
48 scripts are then redeployed or the divergence is accepted and recorded, and that is not this lane's
call to make silently.

## 6. STATE, so nothing is lost

- Worktree `/c/tmp/ds-d-s18` on branch `ds-d-s18-future-import`, based `14394b4353`, holds all 59 edits
  **uncommitted** (the gate refuses, and a bare `git commit` is a NEVER).
- Durable capture: the diff is saved as a patch outside the tree and verified by
  `git apply --check --reverse`, carrying exactly 59 `+from __future__ import annotations` lines.
- **Nothing was deployed.** No S3 object was written.
- The shared tree's index was NOT used: a peer worker's gateway-release drain
  (`MERGE_HEAD` -> `78ad3d6db9`, 1 unmerged path) held it, so `safe-commit` there refused and staged
  nothing, correctly.

---

## 7. OUTCOME -- what landed, per the CTO's ruling of 04:28Z

The ruling: (1) YES restore the ruff half, safe fixes only plus noqa for the residue, keeping a LOCAL
module's import with `# noqa: F401`; (2) NO redeploy for a lint-only change, record the divergence instead.

**Landed `219e930eec`, merged to CLOUD `f1830f38da`: 56 files changed, 326 insertions, 300 deletions.**
`.tools/commit-gate.sh`: clean for **56 of 56**.

### 7a. The ruff half, by the numbers

| | count | detail |
|---|---|---|
| safe auto-fixes applied | **223** | F541 177, F401 42, E401 4 |
| noqa ROWS for the residue | **87** | E702 44, E701 16, F841 10, E402 7, E722 6, E712 3, F811 1 |
| local-module F401 **PINNED, not removed** | **8** | all `from lib.s3_layout import ...` |
| residual ruff violations | **0** | |
| py_compile failures | **0** | |

Those 87 noqa ROWS cover **93 violations**: an E702 line with two semicolons carries two violations and
takes one comment. Rows and violations are different units, so both are printed rather than one passed off
as the other. The arithmetic closes: 324 outstanding = 8 pinned + 223 fixed + 93 suppressed.

**The guard fired and it was load-bearing.** The eight pinned lines sit in `C_06`, `C_08`, `E_21` (five
names) and `E_22`, all importing from `data/black_diamond/scripts/gold/lib/s3_layout.py` -- an in-repo
sibling module, neither stdlib nor third-party. They are pinned BEFORE `--fix` runs: ruff would otherwise
remove them first and the guard would never get a chance to fire. Order of operations was the whole guard.

### 7b. A figure of mine, corrected

I earlier called the import "cosmetic in the other 54". Ruff's FA102 fires on **5** of these files, so those
5 genuinely use PEP-604/585 annotation syntax and need the import on a 3.9 runner. Cosmetic in 51, not 54,
and load-bearing in 5.

### 7c. THREE FILES REFUSED -- the honest exit

`data/black_diamond/scripts/silver/bd_price_update.py`, `build_bd_assets_dim.py` and
`build_interpolated_prices.py` cannot pass the gate on a rule that is **not lint**:

```
BLOCKED: build function '<f>' returns DataFrame but missing coerce_silver_ids() call
         -- required by ADVI_INFNNA.SILVER-ID-DTYPE-UNIFY Int64 convention
```

**Measured at BASE, untouched, in all three** (in a separate detached control worktree at `14394b4353`, so
the reading could not be contaminated by my edits): the violation is reported at base alongside the
future-import one, so it is pre-existing and none of it is mine. My inserted line only shifted its reported
line number, e.g. 416 -> 417 in `bd_price_update.py`.

Satisfying it means adding a dtype coercion to three silver PRODUCERS. That is a functional change to served
data, it would require a deploy, and this ruling is lint-only with no redeploy. So the three are **reverted
to base** rather than left half-swept, and verified byte-identical to `14394b4353` on CLOUD after the merge.
They are routed, not done. **Each needs its own functional cell with a deploy and a sign-off.**

### 7d. The repo-vs-deployed divergence record (ruling 2)

Read-only: **nothing was written to S3 and no object was downloaded.** Every swept path's deployed object
under `s3://opal-data-bd/code/` was compared by ETag-as-md5 (single-part uploads) against the pre-sweep
bytes at `14394b4353`.

| state | count |
|---|---|
| `DEPLOYED == PRE-SWEEP` | **59 of 59** |
| already diverged before this sweep | **0** |
| never deployed (no object) | **0** |

**So there was no prior divergence.** After this commit the repo differs from the deployed bytes on exactly
the 56 landed scripts, by exactly this lint delta, and nothing else. Each reaches S3 with its next
functional change through `safe-deploy`. The 3 refused files remain repo == deployed.

### 7e. What was verified, and in which order

The negative controls were run BEFORE the fix was believed, not after it was chosen:

- every file's base content and swept content through the gate's exact ruff invocation
  (`--target-version py39 --extend-select FA`) via `--stdin-filename`, so nothing on disk was touched:
  **49 files carried violations at base; 0 files acquired a violation from my edit; 5 were fixed by it;**
- the AST-equivalence guard on the future-import half (old body == new body minus the inserted node);
- `git diff --numstat` on the import-only pass: every file exactly **+1 / -0**, so no line-ending damage;
- the three refused files re-read at base in an isolated control worktree.

### 7f. A gate-visibility gap, fourth instance -- and this one FALSELY REFUSED

Running gates from a SPARSE linked worktree narrows what they can see. Three earlier instances were
blindness that announced itself. The fourth was worse: **`missions-tree-check` REFUSED a good commit** of
two `.md` records in the sparse worktree ("tree=1 project(s) ... flat index rows=0 ... RESULT: 1
violation(s)"), because the cone contained one directive folder and no flat index. The same check passed on
the same content in the shared tree. So the violation was an artifact of the checkout shape, not of the
commit. Remedy used: commit records from the shared tree; add `org/standards` and the relevant `org/` paths
to the cone when a worktree must carry them.

The cone this sweep actually needed: `.tools`, `data/black_diamond`, `lib`, `org/modules/graph`,
`org/standards`, the project folder, and `org/tier2_senior/<serial>` for the seat's own log.
