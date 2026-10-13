# OPAL_BBGTML.TO-Z6-R5 -- the [TEAMS-ARMED] stdout receipt

**archetype:** DEPLOY
**Seat:** `0.7.0_AE_CloudOps~ZT` | **Issuer:** `2.0.0_SA_COO~ZB` (issuance `6338955a02`) | **Risk:** WORLD
**Spec:** CTO ruling `@61e3067f5c` disposition 5, verified at its bytes (lines 35-38 of
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPAL_BBGTML_Z6_REPAIR_DISPOSITIONS_20261013_Z.md`)
**Commit:** `fab731853ec027c80522bb0181aa3a6f308fa40b` | **Ledger:** `opal-bbgtml-z6-r5-teams-armed-20261013`, CLOSED

## What changed

`.claude/skills/teams-assist/teams-watch.py` `main()`, immediately after the existing stderr banner, prints ONE
stdout line, `flush=True`:

```
[TEAMS-ARMED] pid=<os.getpid()> identity=<PIN_IDENTITY or BARE> channels=<len(channels)> cursor=<cursor>
```

Nothing at import time; nothing else added to stdout; the `[TEAMS]` message-event format untouched.

`.claude/skills/bbg-teams-assist/SKILL.md` arm section: the stdout receipt -- not the banner -- is the arm proof;
read it as a receipt, never as a message (no ACK, no reply, no cursor effect); it must carry
`identity=517aa5ee-b4d0-425a-b493-5a22ff77ac4f` and `channels=1`, with `channels=0` and `identity=BARE` named as the
two bad arms; **no `[TEAMS-ARMED]` within 60 seconds of an arm means the watcher did not arm** -- census, then re-arm.
The stale sentence claiming the arm banner must print `channels=1 watched (...)` is corrected (the banner stays on
stderr, where a Monitor cannot deliver it). The `while True` citation moved `teams-watch.py:531` to `:537`, because
this insert displaced the line the skill cites -- a reference my own edit invalidated.

## Criteria

### AC1 -- `bash org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r5_teams_armed_check.sh; echo "exit=$?"`

```
ARM leg: rc=0 stdout_lines=1 TEAMS-ARMED_lines=1
[TEAMS-ARMED] pid=34428 identity=517aa5ee-b4d0-425a-b493-5a22ff77ac4f channels=1 cursor=2026-10-13T21:08:54Z
RUNNER leg: stdout bytes on the runner's import path = 0
ARM leg: PASS
RUNNER leg: PASS
R5: PASS
exit=0
```

PASS on both legs and on every clause of the expect: `rc=0`, `TEAMS-ARMED_lines=1`, the line naming
`identity=517aa5ee-b4d0-425a-b493-5a22ff77ac4f` and `channels=1`, zero stdout bytes on the runner's import path.

**DIFFERENCE CONTROL, measured by this seat rather than inherited from the issuance commit.** The same check on the
pre-edit bytes (blob `c2a16eb07f236f4c24153143993a58c810829a5d`, run 21:02Z) read:

```
ARM leg: rc=0 stdout_lines=0 TEAMS-ARMED_lines=0   -> ARM leg: FAIL
RUNNER leg: stdout bytes = 0                       -> RUNNER leg: PASS
R5: FAIL   exit=1
```

So the ARM leg moved FAIL -> PASS and the RUNNER leg held PASS -> PASS. That pre-edit run is also the evidence that
the receipt is not contingent on token health: it printed the stderr banner while its token was expired
(`pinned token expired -- quiet retry, pin HELD`), and the post-edit pass printed the receipt with a live token
(`token selected`). The receipt attests THE ARM, which is what disposition 5 asked for.

The bytes AC1 ran against are the committed bytes, not an inference: `git diff HEAD` over both files reads 0 lines.
Committed blob `1494429d061ded5c0572f87b99eb46b7f10d72bb`.

### AC2 -- `git diff --stat HEAD~1 HEAD -- .claude/skills/ | tail -1`

```
 2 files changed, 22 insertions(+), 3 deletions(-)
```

PASS. Read whole rather than by positional slice, and widened to the whole commit, because AC2's path-scoped diff
cannot see a third file landing outside `.claude/skills/`:

```
 .claude/skills/bbg-teams-assist/SKILL.md   | 19 ++++++++++++++++---
 .claude/skills/teams-assist/teams-watch.py |  6 ++++++
git diff --name-only HEAD~1 HEAD  ->  exactly those two paths
```

## Launcher census (step 2c)

`comp-find 'teams-watch.py' --files --all`:
**DENOMINATOR 1334 hit(s) across 199430 file(s) scanned, corpus=all** (232849 ephemeral-floor, 134 unreadable, 35552
binary, all NOT searched); 471 files, PAGE 1 of 1; bands HEAD=152 DEF=3 SURFACED=654 CONFIG=35 DOC=490.

471 files is the MENTION population, not the launcher population, so the launcher cut was taken by subtraction from
printed denominators rather than by a forward list:

| cut | denominator | launchers found |
|---|---|---|
| `--band HEAD` | 62 of 62, all read | 2 executable: the module itself; `z6_checks/r5_teams_armed_check.sh` |
| `--band DEF` | 3 of 3, all read | 1: `integrations/ticketing/intake/runner.py:69` |
| `--band CONFIG` | 12 of 12, all read | 0 (channels.json is data; the rest are comp-graph caches and proof_of_spec) |
| exec shape `teams-watch\.py --server` | 32 hits / 31 files | 0 in code -- audit logs, message archives, records, SKILL.md (DOC) |
| exec shape `python[^\|]{0,40}teams-watch\.py` | 30 hits / 27 files | 0 in code -- same shape |

**Every launcher, named and classed:**

1. **`integrations/ticketing/intake/runner.py:69` (`_load_teams_watch`) -- D7 intake runner, every 5 minutes.
   UNAFFECTED, and proven so rather than argued.** It imports the module and never calls `main()`; the receipt is
   inside `main()`. AC1's RUNNER leg measures its exact import path and reads 0 stdout bytes.
2. **The BG seat's Monitor arm (`0.0.3_BG_BBGTerminal`, every ~29.5 minutes). AFFECTED BY DESIGN and HANDLED.** It
   reads stdout as events, so it now receives one receipt per arm; the SKILL.md half of this order is what teaches it
   to read that as a receipt and not a message. Its live watcher keeps its old bytes until its own next re-arm: not
   killed, not re-armed, not signalled.
3. **`org/tier1_exec/2.0.0_SA_COO~ZB/deliverables/z6_checks/r5_teams_armed_check.sh`. AFFECTED BY DESIGN** -- it is
   AC1 and requires the line.
4. **No other launcher exists.** No script, scheduled task, cron, `.ps1`, `.cmd` or service definition execs this
   module anywhere in the corpus. A zero with its cause named: the two exec-shape censuses returned code-band zeros
   against printed denominators of 199488 files scanned, and the HEAD/DEF/CONFIG bands were read entry by entry
   rather than sampled.

**One CONSUMER, not a launcher, needs a change this order does not carry -- filed, not edited:**
`org/missions/D6/NFRA/NFRA_OPALAI/deliverables/2.0.0_SA_COO~AI/round2/checks/e7.AC1.sh` reads the file via `git show`
and asserts its AST equals the round-2 cut `c8df03c408`. It never runs `main()` and never reads stdout, so the stdout
contract is untouched -- but its verdict flips on this commit. Measured, not predicted: cut=39398 bytes, HEAD=39750,
worktree=40285; `AST cut==HEAD True`, `AST cut==WORKTREE False`. Run live with the edit uncommitted it printed
`RESULT: PASS`, because `git show HEAD:<file>` cannot see a dirty worktree; from `fab731853e` on it reads FAIL.
Row **`OPAL_BBGTML-Z-S18`** (OBSERVATION / INERT, `disarm_owner 2.0.0_SA_COO~ZB`), commit `b06e607e30`.
Negative control carried in the row: the sibling `f15.AC1.sh` also reads FAIL, but on `git -C opal_ai show` of a file
in the SEPARATE `opal_ai` repo -- pre-existing and not caused by this edit.

## Bounds held

Exactly two files touched. No new standing process, alert, monitor or cron. AC1 ran `--once` against a throwaway
`TMPDIR`, never the live cursor files. The intake runner, its config, the BG seat's processes and its inbox were not
touched. The row was appended with `>>` only, never a rewrite.

**The row id collided and the gate caught it.** Filed first as `Z-S15`; sibling lane `0.7.0_AE_CloudOps~ZS` had taken
`S15-S17` in `ee4040615e` concurrently -- the shared-append race rule 14b says to take rather than isolate. Renumbered
to the next free id against a printed denominator (`comp-find 'OPAL_BBGTML-Z-S1[5-9]'`, 9 hits: S15, S16, S17 held,
S18 free) by changing only my own two lines; the peer's three rows are byte-untouched and the diff reads
32 insertions, 0 deletions.

## Ledger

`opal-bbgtml-z6-r5-teams-armed-20261013` -- opened BEFORE the edit, **CLOSED**, both legs proven, sentinel removed.
Entry: `org/critical_paths/change_management/20261013T2101Z_opal-bbgtml-z6-r5-teams-armed-20261013_deploy_completion.md`

- **L1 git** -- `fab731853e`, closed with the AC2 output and the whole-commit path set.
- **L2 verify** -- closed with the AC1 output and the pre-edit difference control.

## Push state -- MEASURED

**ON ORIGIN @`fab731853e`** (`git ls-remote origin box/sitez` read 21:41:28Z, then re-read; the branch tip advanced
`2bbce5d267` to `1c4d63b462` between reads -- the box's `box-sync` is active and carried it). Confirmed by CONTENT at
origin's tip, not by reachability alone: the receipt line greps 1 at the tip's blob and **0 at the pre-edit blob**
(negative control); the SKILL.md receipt section greps 1; row `Z-S18` greps 2 (heading + id).

## Not this seat's acts

- The `<status>` flip of TO-Z6-R5 is the issuer's.
- Disposition of row `OPAL_BBGTML-Z-S18` is `2.0.0_SA_COO~ZB`'s; the routing candidates are in the row's `notes`.

Next: `OPAL_BBGTML.TO-Z6-R4` (same folder), per this order's report clause.
