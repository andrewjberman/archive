# OPAL_BBGTML.TO-Z6-R3 -- report: step 1 built on the branch; SIGNED-IN, exercise not possible, nothing landed

**archetype:** IMPLEMENT
**secondary_archetypes:** TRACE

**Seat** `0.7.0_AE_CloudOps~ZS` | **issuer** `2.0.0_SA_COO~ZB` (@`b066255b05`, GO msg 34003 acked) | **ruling** CTO @`61e3067f5c` disposition 3 | **risk** WORLD
**Order** [OPAL_BBGTML.TO-Z6-R3.signin-focus-reassert-and-bounded-refill.md](file:///C:/Users/Opal%20Bloomberg/Desktop/ajb_workspace/org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/OPAL_BBGTML.TO-Z6-R3.signin-focus-reassert-and-bounded-refill.md)
Released on Andrew-direct ~09:0xZ, verbatim *"What is the hold you are referring to? There should be no hold"* -- which also answers row Z-S17.

## Verdict, in the order's own words

**`SIGNED-IN: exercise not possible`.**

```
DAPI: UP (session + SPX Index/PX_LAST returned -- entitled session live)
dapi_check rc=0
```

Read twice, at **09:25:48Z** and again at **09:30:29Z** immediately before the exercise would have started. The order's
first step-2 precondition is that `dapi_check` reads DOWN, and it is explicit that on UP **no fill runs at all**,
because a `-Fresh` fill closes a signed-in Terminal. The release message restated it ("including no fill while
dapi_check reads UP") and so does the released status line. So **no fill, no verify, no submit, no Login click, no
ledger write, and no merge.**

**Step 1 is done and sits on the branch**, which is what the order's own fallback clause directs: "Land nothing, leave
the branch."

## What was built -- branch `zs-bbgtml-z6-r3`, commit `7ab72b201a`, NOT landed

### 1a. `bbg_signin.ps1`, `-Phase submit`

- Focus is re-asserted **up to 3 tries** (`SetForegroundWindow` + 300 ms + `GetForegroundWindow`), and rc=4 is returned
  only if all three fail. One assertion is what lost the window between the verified fill and the click on 2026-10-13.
- The **last** foreground check now sits immediately before the ledger write and the click, with **nothing** between the
  three -- no sleep, no screenshot, no further call. Verified by reading the lines back in order: check at `:187`,
  dry-run exit `:188`, ledger write `:189-191`, `Click` `:193`.
- New **`-DryRun`**: every guard runs up to and including that last check, then it prints exactly
  `DRY-RUN: focus held at the click point -- no ledger write, no click.` and exits 0.

### 1b. `bbg_fallback.ps1`, STEP 4

- On submit **rc=4** -- a focus loss *before* the ledger write, so zero Bloomberg attempts were spent and a re-fill
  costs nothing -- **exactly one** bounded re-fill runs, **without** `-Fresh` since the dialog is already open, then a
  re-verify, then one re-submit. It prints `rc=4 -- one bounded re-fill (1/1), no attempt spent` first. A second rc=3/4,
  or a re-fill that does not verify, falls through to the existing escalation. **rc=3 unchanged. Never more than one
  re-fill.**
- New **`-DrySubmit`** (passes `-DryRun` to every submit, then prints `DRY-SUBMIT: stopped before Login` and exits 0
  without reaching STEP 5) and **`-ForceRc4Once`** (forces the first submit's rc to 4 so the re-fill path can be
  exercised, printing its own `TEST:` line). Both TEST-ONLY, in the shape of the existing `-ForceDown`.
- **AMENDMENT 1 (row Z-S15)** folded in: the trailing `P0 gate: transport sustained-down, network OK` line is now
  `if ($absent -eq 3) { ... }`, so the `$absent -eq 0` path prints only its own classification and the gate no longer
  contradicts itself in an unattended log.

### What verification is honestly available on an un-exercised branch

Both files **parse** -- `[Parser]::ParseFile` 0 errors each, against a planted-syntax-error control that read 1 -- and
the parser reads the param blocks back as `(StubSubmit, ForceDown, SkipP0, DrySubmit, ForceRc4Once)` and
`(Phase, Fresh, DryRun)`, so the new switches are real parameters and not comment text. Every replacement anchor was
asserted to match exactly once before any write. Encoding held in both directions: `bbg_fallback.ps1` stays uniformly
CRLF (137 of 137 lines), `bbg_signin.ps1` stays LF, both 0 non-ASCII.

| file | before | after |
|---|---|---|
| `bbg_signin.ps1` | `sha256 58815b82...`, 188 lines | `sha256 04eee4c067...`, 201 lines |
| `bbg_fallback.ps1` | `sha256 f717d111...` (R2's bytes), 114 lines | `sha256 a7cea779bc...`, 137 lines |

**NO ACCEPTANCE CRITERION WAS RUN AND NONE IS CLAIMED.** AC1 needs a real fill; AC2 reads the sign-in ledger either side
of AC1; AC3 only exists after a merge. The behaviour of the focus re-assert and the bounded re-fill is therefore
**unproven** -- it parses and it reads correctly, which is not the same thing.

## Preconditions, each measured

| # | precondition | reading | verdict |
|---|---|---|---|
| 1 | `dapi_check.py` prints `DAPI: DOWN` | `DAPI: UP ... entitled session live`, rc=0, at 09:25:48Z and 09:30:29Z | **FAILS -- this is the blocker** |
| 2 | no window titled `BLOOMBERG: Login` | 0 matching, of 2 titled processes (denominator printed) | holds |
| 3 | **AMENDMENT 2**: not between 10:30Z and 12:30Z | 09:25:48Z, 64.2 minutes before the window opened | holds |

**`wintrv.exe` before the exercise: 0** -- recorded because the order requires it. The order's cleanup clause ("if
wintrv was NOT running before, close the Bloomberg UI tree again") **does not arm**: no fill ran, so no Bloomberg UI
tree was opened and there is nothing to close. `bbcomm.exe` was never touched, as required.

## The box is exactly as it was found

- **Shared tree untouched.** `git status --porcelain -- integrations/bloomberg/auth/` is empty, and the shared files
  still read `bbg_signin.ps1` `58815b82...` / 188 lines and `bbg_fallback.ps1` `f717d111...` / 114 lines -- the latter
  being R2's landed bytes, unchanged.
- **Sign-in ledger unchanged at 35 attempts**, last `2026-10-13T14:28:30Z`. This is the hard evidence that no submit
  ran: a submit writes that file before it clicks.
- No deploy-ledger entry was opened. Step 3 opens it, and step 3 did not begin.

## What this means for today's 11:00Z pull -- and it is good news

The Terminal is signed in and **entitled**, so when `OPAL_BBGTML_daily_pull` fires at 07:00 ET the fallback's STEP 1
will read `DAPI UP -- proceed with pull, no sign-in needed` and exit 0 before reaching any gate. **The pull should
proceed without needing a sign-in at all**, and R2's repair will not be exercised today. R2 remains correct and needed
for the day the session is genuinely down with 8194 held -- which is precisely the state nobody has observed yet.

## Z-S16 is now much better evidenced than when it was filed

The row said `wintrv.exe` absence is not a signed-out oracle, on two readings. It is now **four readings across more
than twelve hours** -- 21:14:16Z and 21:43:37Z on 10-13, 09:25:48Z and 09:30:29Z on 10-14 -- every one of them
`wintrv` = 0 with `dapi_check` returning an entitled session and a real SPX `PX_LAST`. The only Bloomberg processes
present are `bbcomm` and `blpcrashmon`.

That matters beyond the row: the trace's "after the 14:57 ET reboot there is no `wintrv.exe`, so the Terminal is
INFERRED signed out" is contradicted over a 12-hour span, and disposition 1's premise -- that Andrew needed to sign the
Terminal in before 07:00 ET -- was very likely already satisfied when it was written. The disarm is the issuer's; the
measurement is here.

## Push state -- MEASURED

`git ls-remote origin box/sitez` = `84bfc721a7` at 09:33Z. `git ls-remote origin zs-bbgtml-z6-r3` returns **nothing**:
the branch is local by design (CLAUDE.md: scratch branches are free, and this seat does not push a shared branch).

| ref | what | state |
|---|---|---|
| `7ab72b201a` | step 1, on `zs-bbgtml-z6-r3` | **LOCAL, branch only -- deliberately not merged** |
| this report | deliverable | LOCAL, pending `box-sync` |

## Not done, and why -- the resume conditions, exactly

- **Steps 2 and 3 are blocked on one measurable thing**, not on a judgement: `dapi_check` must read **DOWN**. It has
  read UP on every read for twelve hours.
- **AMENDMENT 2 window**: the exercise and the landing must also avoid **10:30Z-12:30Z** today.
- **Resume recipe for whoever picks this up** (this seat, or a successor): re-read `dapi_check`; if DOWN and outside the
  window, run AC2's ledger count, then AC1 from `C:/tmp/zs-z6-r3` under `bbg_credentials.py`, then AC2 again; on both
  PASS, open the ledger entry, merge with `.tools/safe-merge.sh zs-bbgtml-z6-r3`, run AC3 on the shared tree, close,
  and remove the worktree. The worktree stays **`git worktree lock`ed** so an idle GC cannot take it.
- **The `<status>` flip is the issuer's.**

## Compiler Tools

| tool | result |
|---|---|
| `dapi_check.py` x2 (09:25:48Z, 09:30:29Z) | **UP both times** -- the blocking read |
| `[Parser]::ParseFile` on both edited files + planted-error control | PASS 0 errors each; control read 1 |
| `ParamBlock` AST read-back on both files | PASS -- all three new switches are real parameters |
| binary anchor assertions (`count == 1`) x5 before any write | PASS -- no partial application possible |
| CRLF / LF + non-ASCII counts, before and after | PASS -- fallback 137/137 CRLF, signin LF, 0 non-ASCII both |
| `Get-Process` window + `wintrv` census with denominator | PASS -- 0 login windows of 2 titled; wintrv 0 |
| `git status --porcelain` + sha256 of the shared files | PASS -- shared tree provably untouched |
| sign-in ledger attempt count | PASS -- 35, unchanged; the hard proof no submit ran |
| `.tools/safe-commit.sh` from inside the linked worktree | PASS -- `7ab72b201a` on the branch, not the trunk |
| `git ls-remote` x2 | PASS -- trunk hash read; branch absent from origin, as intended |

**What worked.** Doing step 1 before testing the step-2 gate. The code is written, parsed and committed, so the moment
`dapi_check` reads DOWN the exercise is a few minutes of work rather than an hour -- and nothing about the blocked
precondition made the unconditional half of the order un-doable.

**What failed.** Nothing refused and nothing was mis-measured this round.

**Gap found.** None new. `commit-gate` again read `0 of 2` on the two `.ps1` files -- the same already-reported gap, and
the reason `[Parser]::ParseFile` was run beside it.
