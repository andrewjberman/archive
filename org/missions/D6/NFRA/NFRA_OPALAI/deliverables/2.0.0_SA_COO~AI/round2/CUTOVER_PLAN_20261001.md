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
