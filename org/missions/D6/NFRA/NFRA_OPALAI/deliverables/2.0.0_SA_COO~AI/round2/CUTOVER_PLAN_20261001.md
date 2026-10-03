# NFRA_OPALAI -- cutover plan after G-PUSH (2.0.0_SA_COO~AI, 2026-10-01 ~16:1xZ)

Answers `1.0.0_SA_CTO~O` msg 27943. Every state below was measured at writing.

## Measured state

| item | value |
|---|---|
| opal_ai origin PROD | `9c0a80b8d0` (G-PUSH, Andrew-direct 15:51Z, pushed by `0.0.0_AB_MSTR~Z`, msg 27940) |
| opal_ai origin DEV | `fd8ab8a57f`, now 23 commits behind PROD |
| local opal_ai `DEV` | `32abfdb`: NFRA_MCPMSP's runtime-msp line, 5 ahead of origin DEV, 23 behind the new PROD, unpushed |
| runtime checkout `C:\opal_runtime\opal_ai` | `fd8ab8a57f` |
| 8194 wall rules live | 0 |
| workspace fence `.tools/hooks/bg-concierge-gate.sh` | on disk, **UNWIRED** since 4c179f1826 (Andrew-direct "pull that off right now"); no `.claude/*.json` registers it |

## The steps, each with its owner and the word it rests on

1. **DEV fast-forward to PROD: NOT done, and it needs Andrew's word.** `DEV` is a shared branch, pushed only by
   `0.0.0_AB_MSTR~Z` on Andrew's word, and his 15:51Z word named PROD only.
   - Recommendation: fast-forward origin DEV `fd8ab8a -> 9c0a80b`. A PROD ahead of DEV is an inverted state, and the
     move is a pure fast-forward.
   - Consequence to name on the card: NFRA_MCPMSP's local DEV (`32abfdb`, 5 commits on `fd8ab8a`) then merges 23
     commits before it can push. That is `2.0.0_SA_COO~MS`'s act, and it does not block this project.
2. **Runtime pull: no separate act.** The launcher fast-forwards `checkout_dir` to `prod_ref` on every launch
   (`launcher.ps1` step 1), and the launch gate refuses `CHECKOUT-NOT-AT-PROD`. The first launch after the wall
   (the item-0 close run) pulls `9c0a80b` into `C:\opal_runtime\opal_ai`, and that pull is the moment the OA-f-9
   launcher takes effect. Until then the runtime stays at `fd8ab8a`, and nothing runs from it: the Analyst is held.
3. **OA-t-3 parent half: DEFERRED to the cutover sitting** (a merge attempt at 16:07Z was refused by a silent downstream commit hook, row Z-S51; no live effect either way). It removes `.tools/hooks/bg-concierge-gate.sh` and its test. The
   fence has been unwired since 4c179f1826, so the removal changes no live behaviour. The hookup "remove the fence
   line from `.claude/settings.json`" is already done (MOOT).
4. **The 8194 wall: Andrew's admin act**, carded (msg 27831; `ANDREW_ACT_DAPI_8194_WALL_20261001.md`). Then the slot
   ~25 respawn runs AC3, and AC3 must read 8194 REFUSED.
5. **The item-0 close run.** The Analyst is launched by the OA-f-9 launcher from the runtime. That launch pulls PROD
   and reads `agent/refs`. OA-t-1's J2 is graded there by `3.0.0_SA_CVO~O`.
6. **OA-t-1 parent half, with the `.tools/ajb.ps1` BG-launch retirement: in the same sitting, AFTER step 5 passes,
   never before.** It removes the live workspace concierge's product files (`0.0.3_BG_BBGTerminal` prompt and refs,
   `portal_lookup.py`, and the `.claude/skills/bbg-teams-assist` skill). Removing them before the runtime Analyst
   passes its close run would leave Teams with no concierge, against PRD C11 ("the cutover drops nothing silently").
   The CLOUD push of that merge is `0.0.0_AB_MSTR~Z`'s, as for any trunk push.
7. **OA-e-8** (the speed-stage measure) after step 5, on slot ~12.

## Addendum 2026-10-02 ~15:0xZ (relaunch, Andrew-direct ~14:4xZ "yes do it")

Measured at writing. Step 4 is DONE: OA-f-11 AC3 PASS, the wall is live. Step 2 is CORRECTED by row Z-S56.

| item | value |
|---|---|
| opal_ai origin PROD | `9c0a80b8d0` (ls-remote read) |
| local `nfra-opalai-r2-dev` | `bd7cd5d`, PROD + 3 commits, fast-forward (is-ancestor read), not on origin |
| runtime checkout `C:\opal_runtime\opal_ai` | `9c0a80b8d0`, was `fd8ab8a57f`: pre-pulled by this seat (row Z-S56) |
| OA-f-12 AC1 on `bd7cd5d`, non-elevated, re-run now | PASS (seam `CLAUDE_EXE: C:\Users\Opal_Agent\.local\bin\claude.exe` rc=0) |

**Step 2 corrected.** A launcher that fast-forwards its own checkout keeps running the bytes it started with. The
`fd8ab8a` launcher would also abort at its own fetch, so the runtime could not self-update through it. The runtime is now at
PROD, and `launcher.ps1` on disk equals `bd7cd5d`'s. The push below changes only `resolve-claude.ps1` and the two wall
scripts, so no second pre-pull is needed. Standing rule: after any push that changes `launcher.ps1`, pre-pull the runtime
before the next launch.

**G-PUSH card (Andrew's call; the relaunch word does not cover it).** Push `nfra-opalai-r2-dev` `bd7cd5d` to origin
`PROD`, a fast-forward from `9c0a80b8d0`: yes / no? Pushed by `0.0.0_AB_MSTR~Z`.
- `bd7cd5d` OA-f-12: `resolve-claude.ps1` trusts a configured `claude_exe` whose existence test is access-denied.
  Without it the non-elevated launch dies before the Analyst starts.
- `0fb3fcb` OA-f-11: the WFP wall installer, already applied live by Andrew.
- `eeca5ca` OA-f-10: the per-user Firewall script fix. The mechanism is superseded; the file is inert.
- REC: yes. This is the last code act before the item-0 close run.

**Then the item-0 close run (Andrew).** From a NON-elevated PowerShell:
`powershell -File C:\opal_runtime\opal_ai\opal\runtime\launcher.ps1 -Config C:\opal_runtime\runtime.config.json`.
The launch pulls `bd7cd5d`. Andrew then messages the Analyst in Teams, and `3.0.0_SA_CVO~O` grades OA-t-1 J2. Steps 6 and 7
follow as written above.
