# AMGT_RESAPP round 74 -- `AMGT-ax-5` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-06 ~07:0xZ

**The act (item 0 and TWO legs, in this order)** for `opal-amgt-scoped-api` and gateway `opal-portal-data-proxy-api` (7k3ed8px20),
under ONE NEVER-2 entry. Executor `0.7.0_AE_CloudOps~A`. Order: `task-orders/AMGT_RESAPP.TO-AMGT-ax-5.the-code-redeploy-and-route-leg.md`,
with AMENDMENT 1.

0. **Item 0.** Apply `round74/ax5_build_fonts.patch` to `build-and-upload-scoped-amgt.sh` (three `DATA_MEMBERS` rows for the Lato
   faces and licence) and commit it alone. That commit is the build commit.
1. **Code leg.** ONE artifact at that build commit, then ONE code-only `safe-apply`. `memory_size` stays 1769. Then
   `leadpanel_cold_warm.py --label after` and the cold invokes' `AMGT_PHASE` lines.
2. **Route leg.** ONE added entry in `local.scoped_amgt_routes`: `"GET /api/scoped/amgt/security/{proxy+}"`, on the same
   integration and the same CUSTOM portal authorizer as every other route (the `for_each` resource sets both). Plan: 1 to add, 0 to
   change, 0 to destroy.

**No grant leg:** ax-1 and ax-3 re-read the same pool objects (the pack ledgers under `packs/`, the gold mention snapshot by ranged
GET, which `s3:GetObject` already covers); ax-4 adds package files only.

## THE BASE, read live at signing (06:5xZ) -- the rollback per key

| object | value | rollback |
|---|---|---|
| function CodeSha256 | `satkY3HXAhzfU7zYZ5fk+EmNHaqIRfj7bBtVlG4XfIY=` (round 73 aw-7), MemorySize 1769, LastModified 03:50:47Z | prior artifact version, one code-only safe-apply |
| gateway 7k3ed8px20 security GET routes | 10, all single-segment `{security_key}`; 0 greedy (r74 c55 C1 at the cut) | the reverse plan: remove the one added route key. The 10 existing routes are untouched in both directions |
| open NEVER-2 entries on this function | 0 on the shared tree; the executor reads every live worktree | -- |

## THE CONTENT-DIFF, measured by the issuer at signing

A detached worktree at `0c9b9db840` with the patch applied, `--build-only`, then `content_diff.py --zip` against deployed `satkY3HX`.

| class | files |
|---|---|
| CHANGED | `lib/research/api/scoped_amgt.py`, `lib/research/api/monthly_chatter.py`, `lib/research/coverage/pool_reader.py`, `lib/research/print/render_pack.py` |
| ADDED | `lib/research/print/fonts/Lato-Regular.ttf`, `lib/research/print/fonts/Lato-Bold.ttf`, `lib/research/print/fonts/FONT_LICENSE.txt` |
| REMOVED | none |
| IDENTICAL | 361 of 368 |

- **Size:** 255,309,631 B against 262,144,000 B (97.4%, 6,834,369 B spare). Without the patch: 253,992,020 B and ADDED 0 (the
  defect item 0 repairs).
- **VERIFY-SCOPE:** cold-start FATAL [] and request-time break []. It cannot see a file read by path, which is why item 0 exists.
- Any other file is a STOP.

## WRITERS OF WHAT MOVES (NEVER-1)

- **The function's code: N = 1 writer,** this act.
- **The gateway's route set: N = 1 writer,** `scoped-amgt-api.tf` through `safe-apply`. The added key matches only a path that no
  existing route matches (HTTP API prefers the most specific route), so a single-segment key keeps its current route. A path that
  404'd at the gateway now reaches the function behind the same authorizer, and the function answers its own 404 for a path it
  does not serve.
- **No store write.** The /freshness hold (60 s) and the ranged read are in-process; nothing is written.

## EXPECTED OUTCOMES (both branches)

| check | before (satkY3HX) | expected after | if not |
|---|---|---|---|
| r74 c53 deployed | FAIL (10.7-11.3 s warm) | YES (local warm 12-14 ms) | rollback of the code leg |
| r74 c55 deployed (C1 gateway, C2 function) | C1 FAIL, C2 PASS | YES (the greedy key present; 16 of 16 reads 200) | reverse plan of the route leg |
| r74 c56 deployed | FAIL (Lato 0.00; 3/2/5) | YES (local Lato 1.00; 1/1/0) | rollback of the code leg |
| r73 c48-c50, r72 c39/c42/c43/c45, r71 c38 deployed | YES | YES (no regression) | rollback of the code leg |
| /freshness cold miss (65 s after a warm call) | -- | reported only; the miss reads the ledgers 16-wide | a row, not a rollback |
| cold first read (leadpanel `after`, AMGT_PHASE lines) | mentions decode up to 3,720 ms | reported: lower expected (local 1,290 -> 307 ms) | not a rollback; above about 2 s keeps provisioned concurrency on Andrew's list |

c55 is a PIN from this act on: every later redeploy of this function runs it (CTO ruling 4).

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-06 ~07:0xZ. The CTO half is owed at `ledger/NEVER_WIDEN_ROUND74_AX5_CTO_HALF.md`.
