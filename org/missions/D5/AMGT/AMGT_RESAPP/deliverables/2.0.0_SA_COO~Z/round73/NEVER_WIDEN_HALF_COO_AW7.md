# AMGT_RESAPP round 73 -- `AMGT-aw-7` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-06 ~03:2xZ

**The act (TWO legs, in this order)** for `opal-amgt-scoped-api`, under ONE NEVER-2 entry. Executor `0.7.0_AE_CloudOps~A`.
Order: `task-orders/AMGT_RESAPP.TO-AMGT-aw-7.the-code-redeploy-and-legs.md`, with AMENDMENT 1.

1. **Code leg.** ONE artifact at build commit `9d2b7b3d7c` (or a descendant with the same CONTENT-DIFF), then ONE code-only
   `safe-apply`. `memory_size` stays 1769. Right after it, run `round71/checks/leadpanel_cold_warm.py --label after` and read the
   cold invokes' `AMGT_PHASE` log lines.
2. **Pool universe write leg.** `python -m lib.research.identity.build_universe --as-of 2026-10-06 --write-pool`, from CLOUD at or
   after `1aa1d8f2df` (aw-6's keep-prior rule). It writes the NEW key `s3://opal-data-harvest/universe/v1/2026-10-06.json`.

**No grant leg:** aw-1 reads `bloomberg/harvest/bronze/refdata/security_key=<key>/<stamp>.json`. The role already holds it,
simulated at signing: GetObject allowed, ListBucket(s3:prefix) allowed.

## THE BASE, read live at signing (03:21:10Z) -- the rollback per key

| object | value | rollback |
|---|---|---|
| function CodeSha256 | `2lUlZomoyb2ttLBaQTg6l3ysfw2aEjZGD7mInm8J/WQ=` (round 72 av-8), MemorySize 1769 | prior artifact version, one code-only safe-apply |
| `universe/v1/2026-10-06.json` | ABSENT. The newest is `universe/v1/2026-09-16.json` (07:32:10Z) | **re-put the 2026-09-16 bytes at `universe/v1/2026-10-06.json`.** Every reader takes the newest dated key, so this restores the prior content without an S3 delete |
| open NEVER-2 entries on this function | the executor reads every live worktree | -- |

## THE CONTENT-DIFF, measured by the issuer at signing

A detached worktree at `9d2b7b3d7c`, `--build-only`, then `content_diff.py --zip` against the deployed `2lUlZomo`.

| class | files |
|---|---|
| CHANGED | `lib/research/api/scoped_amgt.py`, `lib/research/api/monthly_chatter.py`, `lib/research/print/render_pack.py`, `lib/research/harvest/publication_gold.py` |
| ADDED / REMOVED | none |
| IDENTICAL | 361 of 365 |

- **Size:** 253,976,309 B against 262,144,000 B (96.9%).
- **VERIFY-SCOPE:** cold-start FATAL [] and request-time break [].
- Any other file is a STOP.
- `publication_gold.py` is packaged but never called by this function; the gold rebuild is AMGT_HARVST's own act.

## WRITERS OF WHAT MOVES (NEVER-1)

- **The function's code: N = 1 writer,** this act.
- **`universe/v1/<date>.json`: N = 1 writer,** `build_universe --write-pool`, hand-run by this project's seats and never scheduled.
  - Its READERS take the newest dated key: the crosswalk build (`crosswalk.py:1003`), peers, posture, filings, management,
    chatter and /freshness.
  - **Expected effect, read from the producer's own rule (aw-6):** the covered names in the universe go 53 -> 95; the 13 prior
    decided `form_expected` values are KEPT (c52: 0 regressions); 302 names in all.
  - Every new name enters with `form_expected` "none" (the stored filer list cannot decide) and a plain provenance note.

## EXPECTED OUTCOMES (both branches)

| check | before (2lUlZomo) | expected after | if not |
|---|---|---|---|
| r73 c48 / c49 / c50 deployed | FAIL (2,719 codes / 95 NEVER / 131 caps) | YES each | rollback of the code leg |
| r73 c52 local (against the new pool) | FAIL (13 regress) | YES (0 regressions) | re-put the prior bytes at the new key |
| r72 c39-c45, r71 c38 deployed | YES | YES (no regression) | rollback of the code leg |
| /freshness latency (now ~105 ledger reads per request) | -- | reported; a warm read over 2,000 ms is a row, not a rollback | -- |
| cold first read (leadpanel `after`, AMGT_PHASE lines) | chatter 7.0-8.6 s | reported only: lower expected (the names phase was 2.5-3.0 s locally) | not a rollback; above about 2 s keeps provisioned concurrency on Andrew's list |

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-06 ~03:2xZ. The CTO half is owed at `ledger/NEVER_WIDEN_ROUND73_AW7_CTO_HALF.md`.
