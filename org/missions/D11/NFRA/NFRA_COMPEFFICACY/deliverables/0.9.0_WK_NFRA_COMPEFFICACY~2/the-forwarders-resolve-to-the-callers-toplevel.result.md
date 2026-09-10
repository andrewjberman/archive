# CE-e-2 -- THE FORWARDERS RESOLVE TO THE CALLER'S TOPLEVEL: what was measured, what was fixed, what did not land

**TO:** `NFRA_COMPEFFICACY.TO-CE-E-2` | **assignee:** `0.9.0_WK_NFRA_COMPEFFICACY~2` |
**branch:** `wk-nfra_compefficacy-8-1` | **worktree:** `C:/tmp/wk-compeff-8-1` | **date:** 2026-09-10

**HEADLINE.** Both mechanical criteria PASS by output: `E2-AC1` rc 0 with
`CEE2-FORWARDERS-RESOLVE-TO-CALLER`, **12 of 12 arms**, 186.8 s of a 900 s bound; `E2-AC2` `rc=0`.
A bare-name comp-tool now runs **the file the caller changed**: from a fresh linked worktree
`comp-which --which` answers that worktree's `.tools/comp-which`, from the main tree it answers the
main tree's, and a marker planted in the worktree's copy **executes** from the worktree and not from
the main tree. **210 of 210** regenerated forwarders carry the resolution and `--which`, on both
planes. **`<status>` was NOT flipped**: limb (ii) is edited, exercised and **not landed** — the
commit-gate refuses any commit touching a `.tools/comp-*` file while `infra/system/06_current_state`
is stale, and that staleness pre-dates this order (row `NFRA_COMPEFFICACY-W2-S6`, BLOCKING).

---

## 1. THE DEPLOY, IN THE ORDER SPINE v3.9 FIXES

| step | when | what |
|---|---|---|
| **(1) OPEN** | 03:49Z | `deploy_ledger.py open --slug compefficacy-ce-e-2-forwarder-resolution` — 3 legs, naming the 210 targets, the backup's absolute path and the rollback |
| **(2) ACT** | 03:59Z | `bash .tools/provision-path-shims.sh` against the real `~/bin`, rc 0 |
| **(3) CLOSE + COMMIT** | 04:0xZ | all 3 legs proven, entry CLOSED, committed as `e5f2fa3eae` |
| **(4) READ** | 04:1xZ→ | every grading read AFTER that commit |

**BACKUP:** `C:/tmp/wk-compeff-8-1/.scratch/bin-backup-pre-ce-e-2` — 211 of 211 files, 628K, `cp -p`.
**ROLLBACK:** copy it back over `C:/Users/AndrewBerman/bin`, then re-run the previous provisioner
from `git show CLOUD:.tools/provision-path-shims.sh`. The script's own old rollback note said
`rm -rf ~/bin/{aws,comp-which,comp-system,...}` — **six files against a loop that writes two
hundred-plus**, and deleting them restores nothing; every shell then reaches no comp-tool by bare
name at all. Corrected in the same commit: a rollback that is a partial delete is not a rollback.

---

## 2. E2-AC1 — PASS by output

```
$ timeout 900 python org/missions/D11/NFRA/NFRA_COMPEFFICACY/deliverables/0.9.0_WK_NFRA_COMPEFFICACY~2/test_cee2_forwarders_resolve.py
```
rc **0**, elapsed **186.8 s** of the 900 s bound.

```
  [PASS] a                          210 of 210 written forwarders carry the resolution and --which, on BOTH planes (105 + 105 of 210 expected)
  [PASS] b:bash                     bash plane: the MAIN tree answers C:/Users/AndrewBerman/Desktop/ajb_workspace/.tools/comp-which and the FRESH worktree answers C:/tmp/cee2-fresh-9160/.tools/comp-which -- absolute, and DIFFERENT
  [PASS] b:cmd                      cmd/PowerShell plane: C:/Users/AndrewBerman/Desktop/ajb_workspace\.tools\comp-which vs C:/tmp/cee2-fresh-9160\.tools\comp-which -- absolute, and DIFFERENT
  [PASS] c                          the planted marker appears in the bare-name run from the worktree and NOT from the main tree, and the file is byte-restored (sha256 equal)
  [PASS] d:says-so                  the fallback is LOUD on stderr (rc 0, 260 bytes) and names the path it chose -- a silent fallback would rebuild this cell's defect one layer down
  [PASS] d:baked-is-durable         and the baked fallback names the MAIN worktree (C:/Users/AndrewBerman/Desktop/ajb_workspace/.tools/comp-which), not the temporary checkout that ran the provisioner
  [PASS] e:baseline-untouched       the bare invocation left org/tier2_senior/0.8.0_AE_CloudComp/deliverables/comp-which-routing-baseline.json byte-identical (1 of 1 file under the CloudComp deliverables that this harness could write)
  [PASS] e:inside-stated-bound      measured runtime 651.6 s <= the bound the file states, 1200 s (round 7's own rc-124 pair at ~601 s under a 600 s bound is why the bound is stated from measurements)
  [PASS] e:rc                       the harness's bare invocation returned rc 0
  [PASS] f:sample                   7 of 7 sampled forwarders (of 210 written) resolve to the CALLER'S tree and differ from the main tree's
  [PASS] f:real-run                 a bare-name forwarder still EXECUTES its tool after the regeneration (rc 0, 1407 B)
  [PASS] cleanup                    the worktree this run cut is removed and its branch deleted

  12 of 12 arm(s) PASS   elapsed 186.8s
CEE2-FORWARDERS-RESOLVE-TO-CALLER
```

### (a) THE POPULATION, re-derived — and it is not 186

```
  ~/bin present            : 211 file(s)  (106 extensionless + 105 .cmd)
  .tools/comp-* in C:/Users/AndrewBerman/Desktop/ajb_workspace: 104
  DERIVED at this seat     : 105 tool(s) (104 comp-* + 1 aws) x 2 forms = 210 file(s)
  ROUND 7 CITED            : 186 -- and it differs, by +24.
  NOT WRITTEN BY THIS PROVISIONER: 1 of 106 extensionless -- az
  CARRY THE CALLER-TOPLEVEL RESOLUTION + --which:
    extensionless: 105 of 105   .cmd: 105 of 105   MISSING: none
```

**Why they differ:** the set is DERIVED from `.tools/comp-*` at run time, never a named list — the
generator's own header records that *the named set WAS the defect* (4 of 92 tools resolved, and both
commit-gate tools were outside the named five, so `safe-commit`'s coverage gate silently skipped).
186 was the count when that header was written (93 tools x 2); `.tools` now carries 104. **The
number is re-derived, never quoted.** And the denominator is not overclaimed: `az` is present in
`~/bin` and this provisioner neither emits nor touched it, so **210 written, 211 present, 1 foreign**.

### (b) BOTH DIRECTIONS — the bare name, on both planes

```
  BARE NAME RESOLVES TO      : /c/Users/AndrewBerman/bin/comp-which
  bash  cwd=C:/Users/AndrewBerman/Desktop/ajb_workspace -> rc=0  C:/Users/AndrewBerman/Desktop/ajb_workspace/.tools/comp-which
  bash  cwd=C:/tmp/cee2-fresh-9160                     -> rc=0  C:/tmp/cee2-fresh-9160/.tools/comp-which
```
and the same two answers on the `.cmd` plane. **The bash plane is invoked through an explicitly
resolved `bash.exe`** (`C:/Program Files/Git/usr/bin/bash.exe`, via `.tools/git_bash_resolver.py`):
a bare `bash` from Python on this box resolves to the WSL stub, not Git Bash.

### (c) THE PLANTED EDIT — because a path that PRINTS right can still EXEC wrong

```
  marker line inserted after the last module-level import, at line 32
  bare-name run FROM THE WORKTREE : rc=0  marker present: True
      stderr| CEE2-PLANTED-MARKER-9160
  bare-name run FROM THE MAIN TREE : rc=0  marker present: False
  REVERTED: sha256 before 4a56d2b5fafa2ef3617a4dd14d038c601a65a86c4246879e00680ef59ddf4071 / after 4a56d2b5fafa2ef3617a4dd14d038c601a65a86c4246879e00680ef59ddf4071 -- IDENTICAL
```

**A bug in my own control, caught and fixed before the run:** arm (c) first used
`comp-which --which` as the probe — and `--which` prints the target and **exits before the exec**, so
a marker planted *inside the tool* could never have appeared. The arm would have been a constant.
It now uses a real invocation. That is this cell's own defect shape sitting inside its own control.

The plant is in the **fresh worktree only** — never the main tree, never committed, sha256-verified
back, and the worktree destroyed in cleanup.

### (d) THE NO-TOPLEVEL CASE — loud, and durable

```
  probe dir: C:/Windows/Temp   `git rev-parse --show-toplevel` there -> rc=128 (non-zero = no toplevel, as required)
  STDERR (the exact line):
      WARN: comp-which: no git toplevel at /c/Windows/Temp (git rc=128: fatal: not a git repository (or any of the parent directories): .git) -- EXECUTING THE BAKED PATH C:/Users/AndrewBerman/Desktop/ajb_workspace/.tools/comp-which instead (run: comp-which --which)
```
rc 0, 260 bytes on stderr, and the baked path is the **MAIN worktree** — see §3.1.

### (e) THE HARNESS

Baseline `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/comp-which-routing-baseline.json`:
sha256 `1befbed889d486dcfbbf6f58f5164f7c563b805afaec204fbb3819c8c30fda8b` **before, after and now** —
byte-identical, `git status` clean on it. The bare run wrote
`.comp-graph/routing-test/routing-report-20260910T043628Z.json` (gitignored) and **said so**.
Runtime **651.6 s** (rc 0) against the bound the file now states, **1200 s**. Evidence, with its
environment named per R-8: `cee2_harness_runtime.json` beside this file.

**The battery does not itself run the harness, and that is disclosed, not hidden** — row
`NFRA_COMPEFFICACY-W2-S8`. See §4.

### (f) NOTHING ELSE MOVED

7 of 7 named sample forwarders (`comp-find`, `comp-read`, `comp-system`, `comp-estate`,
`comp-coverage-check`, `comp-manifest-check`, `aws`) resolve to the caller's tree and differ from the
main tree's; a real run through a bare-name forwarder still executes (`comp-read --help`, rc 0,
1407 B). The sample is **named, not sliced at random**: two python tools, two bash tools, the
non-comp `aws` case, and the two commit-gate tools whose absence once turned `safe-commit`'s coverage
gate off silently.

---

## 3. FOUR THINGS THE EXERCISE FOUND BEFORE THE FLEET SAW THEM

Every one was caught by **dry-running the generator into a scratch HOME**
(`HOME=<worktree>/.scratch/dryhome bash .tools/provision-path-shims.sh`) and exercising the
**generated artifact**, rather than reading the generator and running it at `~/bin`.

**3.1 THE BAKED FALLBACK WAS ABOUT TO POINT INTO A DIRECTORY I WAS GOING TO DELETE.** The script
baked whatever checkout RAN it. Run from a worker's linked worktree under `C:/tmp`, all 210
forwarders would have carried a fallback into a tree that is removed when the order ends — and the
first caller standing outside any git worktree would have got **rc 127 from every comp-tool on the
machine**. That is this cell's own defect family one layer down: *a generated artifact bound to the
tree that generated it*. Now derived, never hardcoded — `git worktree list --porcelain` line 1 names
the MAIN worktree — and both paths are printed (`RUNNING FROM /c/tmp/wk-compeff-8-1` /
`BAKING ... C:/Users/AndrewBerman/Desktop/ajb_workspace`).

**3.2 THE `.cmd` TWINS ARE THE ONLY FILES THAT NEED THE ACL RESTORE, AND THE SCRIPT SAID THE
OPPOSITE** (`"the .cmd twins never needed it"`). Dry run: **105 of 210 protected, every one a
`.cmd`**; the chmod'd extensionless forwarders all read `AreAccessRulesProtected=False`. Live
pre-state **0 of 211** — so running it unchanged would have taken the fleet from 0 to 105 protected,
**S26 re-armed by the very act this cell commands**, at rc 0, with a WARN scrolling past as the only
tell. Fixed; the live run reports `protected 0 of 211`. Row `W2-S5`.

**3.3 A MULTI-LINE `if (...)` BLOCK BROKE cmd's PARSER.** `comp-which.cmd "what produces canonical
prices"` answered `produces was unexpected at this time` while `--which` on the same file worked.
Replaced by a `goto`; the twins are now written CRLF; and the comparison is `[%1]==[--which]`, not
`"%~1"=="--which"` — `%~1` strips only the OUTER quote pair, so an argument arriving with doubled
quotes leaves an ODD number and the compare becomes unbalanced and **fatal** rather than false.

**3.4 A BACKTICK IN A `rem` COMMENT WAS EXECUTED AT PROVISION TIME.** Every forwarder body is an
**unquoted heredoc**, so an unescaped backtick is a command-substitution vector: bash ran
`cmd.exe /c` while generating and pasted `Microsoft Windows [Version 10.0.26100.9168]` into all 105
`.cmd` shims. My own doing — I introduced it through an inline `python -c "..."` whose bash
double-quoting ate the escapes. Removed, and an **unescaped-backtick audit over all 408 lines** now
reads 27, all in `#` script comments outside any heredoc, **0 inside a heredoc body**.

---

## 4. WHAT DID NOT LAND, AND WHY

**Limb (ii) is edited, exercised and NOT COMMITTED.** `safe-commit` refuses:

```
ERROR: BLOCKED -- comp-system 06_current_state is STALE and this commit touches a _SOURCE.
  [comp-system-gate] SYSTEM BLOCKED-ON-PEER-LANDING: genuine drift (source drift: fingerprint
  (content-sha256, file_count) ('4270b32...', 260) -> ('f50fbd7...', 260)), but source file(s) are
  uncommitted -- .tools/comp-which-routing-test.py. Wait for landing, then re-run.
```

That instruction cannot be followed by the seat it addresses: **the uncommitted source is mine, and
the gate blocks the very commit that would land it.** The staleness pre-dates this order —
`comp_system.py:1562` `_SOURCES` includes `(WS/.tools, "comp-*")`, `06_current_state.json` was last
regenerated at `971375191a` 17:37 -04, and **round 7's own drain `8c3cadf936` 20:50 -04 changed
`.tools/comp-which`** after it. The discriminator is the glob: `provision-path-shims.sh` does **not**
match `comp-*` and committed cleanly at `13df262a9b` in the same minute its sibling was refused.
The gate's two remedies are staging `infra/system/06_current_state.{md,json}` (outside this grant) or
spending the audited `system-current-override`. **A path I need that `<paths>` does not name is a
BLOCKING row, never an override.** Row `W2-S6`.

### 4b. THE REMEDY WAS APPLIED, AND THE BLOCK SURVIVED IT — the loop does not converge

`2.0.0_SA_COO` regenerated and landed `infra/system/06_current_state.{md,json}` at `ec39a2668f`
(comp-system rc 0, `as_of HEAD=d30e3ca107`) and directed a re-run, on the gate's own instruction
*"Wait for landing, then re-run"*. CLOUD was merged (the harness's sha256 `bf778f5d99c2…` unchanged
across the merge, so the measured object did not move) and **the re-run was refused again, with NEW
fingerprints**: `(491f0189b4…, 260) -> (a8192f19f4…, 260)`.

**The regeneration was correct — that is the point.** Measured rather than inferred: with HEAD's
version of the harness swapped into this worktree, `comp_system._source_fingerprint()` returns
`['491f0189b4c0a30adedecf4eb7dc0efc77f5e501a29c3755f45d287b1adefc70', 260]`, **byte-identical to what
06 records**. So 06 describes every *committed* source here perfectly and **this seat's uncommitted
edit is the sole remaining delta** (same file count, content only). The edited copy was then restored
and re-verified at `bf778f5d99c2…`.

**The loop, closed and proven:** regenerate 06 → the pending edit re-drifts it → the gate refuses
because a source is uncommitted → the edit cannot be committed → 06 can never cover it.
`_source_fingerprint()` reads the **worktree** (`content_fingerprint(_SOURCES, rel_root=WS)`), while a
regeneration on another branch necessarily reads a tree the edit is not in; and `_dirty_sources()`
takes `line[3:]` of `git status --porcelain`, so **staging the source does not help either**. Its own
docstring names the intent the predicate cannot express here — *"regenerating now would launder a
PEER'S unlanded work"* — and the predicate cannot tell a peer's unlanded work from **the file this
very commit is landing**. The only exit is a regeneration in a tree where the edit is present, with 06
and the source in **one** commit: `infra/system/` inside `<paths>`. Row `W2-S9`; the override remains
unspent.

**The measured behaviour of limb (ii) is on the record even though git does not carry it:** the two
argparse refusals both fire (`--rebaseline` with `--out`; `--out` naming the baseline path), the bare
run writes `.comp-graph/routing-test/…` and says so, the committed baseline is byte-identical across
two full runs, and the bound is stated from `MEASURED_RUNTIME_S = (680, 826)` /
`MEASURED_TIMEOUT_S = (601, 601)` with `RECOMMENDED_TIMEOUT_S = 1200`.

**A summary field I broke and then fixed:** after moving the WRITE site off the baseline, the two
REPORT sites still printed `baseline -> org/tier2_senior/.../comp-which-routing-baseline.json` while
writing `.comp-graph/routing-test/…`. The truthful NOTE printed earlier in the same run does not
repair it — **a summary field is not repaired by prose beside it** — so both print sites now name the
file actually written and say whether it was the committed baseline. Caught by reading the 824 s
run's last line, not by reading the diff.

---

## 5. E2-AC3 — THE READING FOR THE CVO (no verdict)

**(a) Can a worker seat now verify its own comp-tool edit?** Yes, and it is measured rather than
asserted: arm (c) planted a marker in a fresh worktree's `.tools/comp-which` and the **bare name**
executed it from that worktree and did **not** from the main tree, then restored the file
byte-identically. Arm (b) shows the two `--which` answers differing on both planes. FWD-9's sentence
— *"a tool cleared here stays cleared from any seat"* — now holds for the bare-name path a worker
actually types. Before this cell, that same invocation returned rc 0 with a byte-identical answer
from the wrong file.

**(b) What does the no-toplevel fallback do, and is its loudness enough to tell a caller which file
answered?** It execs the baked path and writes one `WARN:` line to stderr naming the git rc, git's
own message, and **the absolute path it chose**, plus how to ask (`run: comp-which --which`). It is
enough to tell a *reader* which file answered. It is **not** enough to tell a *program*: the line is
on stderr with no machine-readable field, and a caller capturing only stdout sees nothing. The
sufficient instrument is `--which`, which is why it exists. Cost, stated: one `git rev-parse` per
invocation on every comp-tool call.

**(c) Is the harness's new bound stated from a measurement, and what was the spread?** Stated from
measurement: `MEASURED_RUNTIME_S = (680, 826)` and `MEASURED_TIMEOUT_S = (601, 601)` from round 7,
with `RECOMMENDED_TIMEOUT_S = 1200` = the largest measured completion + ~45%. This seat added two
more rc-0 completions, **824.0 s and 651.6 s**, on the same file in the same tree within half an
hour. Four completions now span **651.6 → 826 s, a 174 s / 27% spread**, which is why the bound is
set above the maximum observed rather than at it.

**(d) What can a future worker still not see from inside its worktree?** Four, each measured:
1. **A `.tools/comp-*` edit cannot be committed** while `06_current_state` is stale, and nothing in
   the worktree says so until `safe-commit` refuses (row `W2-S6`).
2. **`E2-AC1`'s own 900 s bound is a coin toss against arm (e)'s subject** (row `W2-S8`): 651.6 s
   passes inline, 824 s does not.
3. **A worktree cut before `CE-e-1` landed still renders `tokenizer.json` CRLF**, so `comp-which`
   run *in this worktree* still emits the potion ALARM and ranks lexically — visible throughout this
   order's own transcripts (row `W2-S3`). A FRESH worktree does not.
4. **The `~/bin` forwarders are not in git.** Nothing in a worktree tells a seat which vintage of the
   provisioner produced the shims it is calling; `--which` names the file, not the generator.

**Evidence with vintage:** `.tools/provision-path-shims.sh`@`13df262a9b`;
`.tools/comp-which-routing-test.py` **uncommitted**, sha256
`bf778f5d99c2e2762f9f7029e7fc8de701a7c4c72faf4a021c679921138257da` at measurement time;
`org/modules/graph/comp_system.py`@`bf236f4fa7` `:1562`, `:1575`; the ledger entry @`e5f2fa3eae`;
`cee2_harness_runtime.json` beside this file.

---

## 6. ROWS FILED

| id | class | hazard | subject |
|---|---|---|---|
| `NFRA_COMPEFFICACY-W2-S5` | OBSERVATION | ARMED | the provisioner's comment names the wrong plane for the ACL restore; unchanged, the run would have taken the fleet 0 → 105 protected |
| `NFRA_COMPEFFICACY-W2-S6` | **BLOCKING** | ARMED | a granted path is uncommittable by the lane it was granted to; the staleness pre-dates the order |
| `NFRA_COMPEFFICACY-W2-S7` | OBSERVATION | INERT | the face commands `deploy_ledger.py open` while `<paths>` does not name `org/critical_paths/` |
| `NFRA_COMPEFFICACY-W2-S8` | OBSERVATION | ARMED | `E2-AC1`'s 900 s bound vs arm (e)'s 651.6–826 s subject |
| `NFRA_COMPEFFICACY-W2-S9` | **BLOCKING** | ARMED | the W2-S6 remedy was applied and the block survived it; 06 can only describe committed content, so the loop does not converge |

---

## 7. WHAT WAS **NOT** DONE

- **No forwarder was hand-edited.** The generator is the artifact; a hand-edited shim proves nothing
  about the generator every future seat runs.
- **The committed CloudComp baseline was never written** — sha256 `1befbed889…` before the first run,
  after the second, and now; `git status` clean on it across both 650–830 s runs.
- **`infra/system/06_current_state.{md,json}` was not touched** and no `system-current-override` was
  spent — out of grant, hence rows `W2-S6` and `W2-S9` rather than a bypass, and still unspent after
  the issuer's regeneration failed to clear the block.
- **`<status>` was NOT flipped to `complete`, and was re-withheld after the remedy.** Both
  mechanical criteria pass by output and the instance validates rc 0, but DELIVERABLE 1 says *the fix,
  both limbs, committed on your branch*, and limb (ii) is not committed — the re-run directed after
  the regeneration was refused again (row `W2-S9`). A valid instance is not a met order.
- **Nothing pushed, merged or rebased** beyond merging CLOUD into this branch as the issuer directed.
- **The backup is still in place** at `C:/tmp/wk-compeff-8-1/.scratch/bin-backup-pre-ce-e-2` (211
  files) for the length of the order.
