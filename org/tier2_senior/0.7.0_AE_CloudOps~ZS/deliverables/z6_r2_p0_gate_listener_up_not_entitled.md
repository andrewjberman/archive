# OPAL_BBGTML.TO-Z6-R2 -- report: the P0 gate classifies a listening 8194 with a failed dapi_check as listener-up-not-entitled

**archetype:** DEPLOY

**Seat** `0.7.0_AE_CloudOps~ZS` | **issuer** `2.0.0_SA_COO~ZB` (@`6338955a02`) | **ruling** `1.0.0_SA_CTO~Z` @`61e3067f5c` disposition 2 | **risk** WORLD
**Order** [OPAL_BBGTML.TO-Z6-R2.p0-gate-listener-up-not-entitled.md](file:///C:/Users/Opal%20Bloomberg/Desktop/ajb_workspace/org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/OPAL_BBGTML.TO-Z6-R2.p0-gate-listener-up-not-entitled.md)
**Window** landed 21:08Z, proven by 21:14Z, against a next fire of 2026-10-14 07:00 ET = 11:00Z. Deadline was 10:00Z.

## Verdict

**The cell is done and all three criteria PASS.** One production file moved, exactly the one the order named. The deploy
ledger entry is CLOSED with both legs proven. Three surprise rows are filed, one of them BLOCKING/ARMED and time-boxed to
the same 11:00Z fire -- it is about the cell's AUTHORIZATION, not its execution, and it is the issuer's to disarm.

## The edit

[integrations/bloomberg/auth/bbg_fallback.ps1](file:///C:/Users/Opal%20Bloomberg/Desktop/ajb_workspace/integrations/bloomberg/auth/bbg_fallback.ps1)
(repo-relative: `integrations/bloomberg/auth/bbg_fallback.ps1`), STEP 2 (the C4 P0 gate) only. The three 8194 samples are
kept; the gate now branches on `$absent`:

| `$absent` | behaviour | state |
|---|---|---|
| 0 (listening 3/3) | prints the "listener up, not entitled -> sign-in warranted" line, continues into the two existing network checks, then STEP 3 | **NEW** |
| 1 or 2 | flicker escalation, exit 2 | unchanged |
| 3 | the existing sustained-down path | unchanged |

`dapi_check` is **not** re-run in STEP 2 -- STEP 1's result is the classification input, per the order. Nothing else moved:
not the fire-once ledger guard, not the fill/verify loop, not the submit, not the `-ForceDown` / `-StubSubmit` / `-SkipP0`
switches.

**Before this edit** `$absent -eq 0` fell into `if ($absent -lt 3)`, so a Terminal whose 8194 is held by the BG seat's
`bbcomm.exe` escalated `8194 not sustained-absent (0/3)` and exited 2 with no sign-in attempted; the pull then exited 50.

**Commit** `f6cc68d6bf` (author `0.7.0_AE_CloudOps~ZS`), bytes
`sha256 5aeb7708...395d9193` -> `sha256 f717d111...cd758bc5`, 8453 -> 8800 bytes, 111 -> 114 lines, **CRLF preserved on all
114 lines**, 0 non-ASCII (byte delta 0).

Two instrument notes, because both nearly produced a wrong edit:
- The file is **CRLF**. `sed -n '58p' | od -c` showed no `\r` because Git Bash `sed` strips it; the binary read showed
  `\r` at every line end. An LF-only replacement block was written, the `count == 1` assertion caught it at 0 matches, and
  nothing was saved. The `grep -c $'\r'` reading of 111/111 was **correct here**, not the usual every-line false positive.
- `.tools/commit-gate.sh` reported `checked 0 of 1 file(s)` -- it reads only `.py` / `.sh` / `.tf` / `org/projects/*.json`,
  so a `.ps1` falls through unexamined. The language-appropriate instrument was run instead:
  `[System.Management.Automation.Language.Parser]::ParseFile` = **0 errors**, against a planted-syntax-error control that
  read **1**. A parse error here would have broken the 07:00 ET pull.

## Criteria

### AC1 -- PASS, exit=0

`bash org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r2_p0_listener_check.sh`, run from the shared repo root ~21:10Z
against the deployed bytes:

```
8194 listeners before run: 1
[fallback] checking DAPI availability...
[fallback] DAPI DOWN.
[fallback] P0 gate: 8194 listening (3/3) but dapi_check failed -> listener up, not entitled -> sign-in warranted.
[fallback] P0 gate: transport sustained-down, network OK -> sign-in warranted.
[fallback] fire-once ledger clear (0 in 6h).
[fallback] STUB: would now fill -> verify -> submit ONCE. (stub mode: no GUI, no submit, no ledger write)
fallback rc=0
R2: PASS (classified listener-up-not-entitled and reached the sign-in path)
exit=0
```

Every element of the expectation is present: listeners >= 1, the classification line, `STUB: would now fill`, **no**
`not sustained-absent` line, last line `R2: PASS`, exit 0. The order's difference control (the same check reading
`R2: FAIL` against the pre-edit bytes at 20:36:58Z) was **not re-run**: it is already recorded in the issuance commit, and
re-running it would append another escalation line to the live `C:\opal-elev\bbg_fallback_ESCALATION.txt` that a human may
read. The fourth line of that output is surprise row Z-S15.

### AC2 -- PASS, exit=0, and it took the FIRST branch

`powershell -NoProfile -ExecutionPolicy Bypass -File integrations/bloomberg/auth/bbg_fallback.ps1 -StubSubmit`, ~21:12Z:

```
[fallback] checking DAPI availability...
[fallback] DAPI UP -- proceed with pull, no sign-in needed.
exit=0
```

**The real state took the "DAPI UP -- proceed with pull" branch**, which is the first of the two branches AC2 accepts. No
`not sustained-absent` line, as required.

**This is also the criterion's evidence limit, and it is stated rather than hidden.** AC2 exercised STEP 1 only and never
reached the P0 gate. AC1 reached the gate under `-ForceDown`, which short-circuits `Dapi-Up` before `dapi_check` is ever
called. So the new classification is proven against a **forced** STEP-1 failure and has **never** been exercised against a
genuinely un-entitled session. ABSENT is not EXERCISED-AGAINST. The repair is still correct and still needed -- whenever a
real `dapi_check` fails while 8194 listens, the old gate refused to sign in -- but it must not be reported as proven
against the live un-entitled state. Filed as Z-S16.

### AC3 -- PASS

`1 file changed, 4 insertions(+), 1 deletion(-)`; `--name-only` over the whole commit lists only
`integrations/bloomberg/auth/bbg_fallback.ps1`.

The invocation as written (`git diff --stat HEAD~1 HEAD`) returned **empty** when run, because a peer
(`2.0.0_SA_COO~O`, `e488418898`) committed to the shared `box/sitez` between my commit and the read, so `HEAD` was no
longer the edit. Per the criterion's own expect clause -- "run on the commit that carries the edit" -- it was pinned:
`git diff --stat f6cc68d6bf~1 f6cc68d6bf -- integrations/bloomberg/`. Both reads are reported.

## Surprise rows -- [INVESTIGATION_v1.md](file:///C:/Users/Opal%20Bloomberg/Desktop/ajb_workspace/org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md) @`ee4040615e`

Gate read `3 new row(s) of 17 total checked`, all carrying their step-7/step-10 fields. `disarm_owner` on all three is
`2.0.0_SA_COO~ZB`.

| row | class / standing | one line |
|---|---|---|
| Z-S15 | OBSERVATION / INERT | `bbg_fallback.ps1:66` still prints "transport sustained-down" two lines after "8194 listening (3/3)"; the gate contradicts itself in an unattended log. The one-line guard (`if ($absent -eq 3)`) was written and **discarded** to stay inside the order's bounds mid-round; it is the issuer's cut. |
| Z-S16 | OBSERVATION / INERT | `wintrv.exe` absence is not a signed-out oracle: `dapi_check.py` read `entitled session live` at 21:14:16Z with `Get-Process wintrv` = 0 and only `bbcomm` + `blpcrashmon` alive since 19:07:29Z. The 20:36Z context reading used that same unsound instrument, so there is no sound before-measurement. Andrew's sign-in open call may already be satisfied; it should be re-read with `dapi_check`, not a wintrv census. |
| **Z-S17** | **BLOCKING / ARMED** | The record of Andrew's no-modify order says **at HEAD** that it "still stands for the Positioning and ETFS-view files (`integrations/bloomberg/pipeline/`, the vehicle and the sign-in scripts)". `bbg_fallback.ps1` line 2 calls itself a sign-in fallback, and the Z6 ruling has **0 hits** for `no-modify`. |

On Z-S17: **surfaced, not adjudicated.** CLAUDE.md bars this seat from reading a sovereign order either wider or narrower,
so it did not revert and did not widen; the order and the ruling are the authorization it executed under. Two readings are
open and this seat holds neither -- either the Z6 memo ("make sure that's functional") lifts a clause that specifically
names the sign-in scripts, in which case the clause is stale and should be struck, or the order stands, in which case this
cell and R3 need Andrew's word and this one is already landed. **It reaches R3**, the next order on this lane, which edits
`bbg_signin.ps1` -- a sign-in script by name. Rollback is one command to `sha256 5aeb7708`, specified in the row.

Two secondary findings inside Z-S17's evidence: the clause's phrase wraps a line break, so a single-line
`grep 'sign-in scripts'` returns **0** against a file that contains it; and the basis it cites,
`ANDREW_DIRECT_20261006_1818Z_ALL_RECS_APPROVED_MSTRZ_OPEN_CALLS.md`, is **absent at HEAD** -- 43 `ANDREW_DIRECT_20261006_*`
records exist under `org/tier1_exec/` and that filename is not among them, with no deletion in the log.

## Deploy ledger

`opal-bbgtml-z6-r2-p0-gate-20261013` -- **CLOSED**, both legs proven, sentinel removed (verified with `ls -a`, not `ls -1`).
Entry: `org/critical_paths/change_management/20261013T2103Z_opal-bbgtml-z6-r2-p0-gate-20261013_deploy_completion.md`.
Opened at `ea7dd1c07e` **before** the edit; L1 = the deploy, L2 = AC1+AC2. The pre-act NEVER-2 read unioned
`.open_deploys/` across all **24** live worktrees and found no entry owning the bloomberg auth surface (the 3 entries
matching `bloomberg|bbg|BBGTML` are a 2026-07 completion-timestamp index and two unrelated projects' proofs).

## Push state -- MEASURED, not defaulted

`git ls-remote origin box/sitez` read `2d57c41ac0b01dc759ea3186777daa2181b8c134` at 21:28Z. Containment tested against
that hash, not against the local `origin/box/sitez` tracking ref, with a positive control (the remote tip is its own
ancestor: yes) and a negative control (local HEAD is not on origin: correct):

| commit | what | push state |
|---|---|---|
| `f6cc68d6bf` | **the deploy** | **on origin @`2d57c41ac0`** |
| `ee4040615e` | surprise rows Z-S15..S17 | **on origin @`2d57c41ac0`** |
| `4bba8e8432` | ledger close + this report | **LOCAL @`4bba8e8432`** -- pending this box's scheduled `box-sync` |

This seat does not push a shared branch (`org/XXX.md` SHARED-BRANCH LAW). The deploy itself is already on origin, and the
file on disk is the deploy regardless.

## Not done, and why

- **The `<status>` flip of TO-Z6-R2 is the issuer's**, per the order's report clause. Left alone.
- **R3 is NOT started.** It is the next order in this lane's queue and it edits `bbg_signin.ps1`, which is the exact file
  class Z-S17 is about. Starting it would land a second edit on the contested surface before the ARMED row is dispositioned.
  **This is a block this seat is naming, not a wind-down.**

## Compiler Tools

| tool | result |
|---|---|
| `comp-find -i --files 'bloomberg\|bbg\|BBGTML' org/critical_paths/.open_deploys --limit 20` | 36 hits / 13 files scanned; 3 files, all cleared by reading |
| `comp-find -i 'no-modify\|no modify' org/tier1_exec org/tier0_utility org/tier0 --limit 25` | 86 hits / 17494 files; HEAD band = 2, both the scoping record. This is the read that found Z-S17 |
| `comp-find --files 'ANDREW_DIRECT_20261006_1818Z' --limit 10` | 54 hits / 199487 files, all log/archive mentions -- the record itself is absent |
| `python .tools/to-check.py --all --assignee 0.7.0_AE_CloudOps~ZS` | 2 PENDING, both OPAL_BBGTML; `scanned=6334` |
| `python .tools/sequence-check.py --project OPAL_BBGTML` | UNPLACED -- not sequenced, its directive's rules govern. No block |
| `.tools/safe-commit.sh` x2 | `f6cc68d6bf`, `ee4040615e`. Surprise-row gate: 3 new of 17, 0 malformed |
| `.tools/deploy_ledger.py` open / close-leg x2 / close | opened `ea7dd1c07e`, both legs proven, CLOSED |
| `[Parser]::ParseFile` | 0 errors, control 1. **Ran because commit-gate reads 0 of 1 `.ps1`** |

**Gaps.** `comp-find` denied a plain `grep -ril` over `.open_deploys/` (F1) and then a piped census (F6) before the right
form ran -- two denial round-trips. `client-data-check` WARNed ABSENT on both commits (no hashed account-id list at
`C:\Users\Opal Bloomberg\.opal\account_id_hashes.txt`), so neither commit was checked for client account ids; absent is not
empty. `audit-archive-invoker.py` exited rc=1 with 16 findings at startup (5 MANIFEST-vs-live gaps, 2 uncovered audit logs,
3 NON-APPEND-EDIT, 6 baseline-missing fail-closed) -- device-level, owned elsewhere, not re-filed here.
