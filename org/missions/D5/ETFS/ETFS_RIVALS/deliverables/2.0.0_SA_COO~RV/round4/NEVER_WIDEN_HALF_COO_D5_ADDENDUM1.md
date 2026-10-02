# NEVER-WIDEN -- COO HALF, ADDENDUM 1: RIV-d-5's second in-place apply (rows Z-W4-S12 / Z-W4-S13)

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-01 ~21:4xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum half (agreed in msg 28062,
with conditions a-c). **Extends:** `round4/NEVER_WIDEN_HALF_COO_D5.md` @a10ebe8d92. Every gate, bound and Andrew-direct line of
that half stands. This addendum adds ONE act and widens nothing else.

**Why:**
- Row Z-W4-S13 is ARMED and confirmed by the issuer: `q-1.AC2` at CLOUD replays the morning order (BASG, then GQGU 5 s later).
  BASG's coverage row then reads GQGU's capture with 0 rows.
- The first 07:00 ET fetch with GQGU live is 2026-10-02.
- The fix (RIV-q-1 amendment 1, c91d7dc313) is drained to CLOUD @9f18b52c62.

**Code pin:** CLOUD **25f4ac5418**, which descends from 9f18b52c62 (`merge-base --is-ancestor`).
- The non-test package diff against d-5's deployed base 5a4b5b5391 is exactly two files:
  - `gold_holdings_coverage.py`: the fix.
  - `enrichment_bloomberg.py`: an additive CLI `main` (RIV-v-2 amendment 3). No Lambda handler path calls it.
- `guardrails_config.json` carries d-5's floors (issuer 0.23, bloomberg 0.99, home_producer 0.0) unchanged.

## VERDICT: SIGNED (at pin CLOUD 25f4ac5418)

## THE SERVED DELTA, MEASURED

**Instrument:** `round4/served_delta_g2.py`, output `round4/served_delta_g2.json`, run at 25f4ac5418.
- It mirrors, READ-ONLY, every input G2 reads: Bloomberg bronze 1876, issuer bronze 1264, issuer silver 632, home landings 28,
  G1 1160.
- It builds G2 in replay mode twice on that one mirror: with the DEPLOYED module (`git show 5a4b5b5391:...`) and with the fix.
- It diffs per (fund, expected date, source) on status, row count, selected and capture file.
- **Control:** the deployed-module build equals the SERVED G2 on **4094 of 4094** keys (0 differ). The mirror reproduces what is
  served.

| fund | G2 rows deployed -> fix | changed / added / removed |
|---|---|---|
| GQGU | 0 -> 307 | 0 / **307** / 0 -- new by design: its own `gqgu-*` captures |
| BASG | 645 -> 645 | 0 / 0 / 0 |
| BIDD, CGIC, ETFT, IDVZ, INEQ, PCLG, PFOE, SCHY, TSEL, TXUE, WCMG | equal | 0 / 0 / 0 |

- **Cross-fund rows:** issuer rows reading another fund's capture under the fix: **none**.
- **G1, G5 and G6:** NOT touched. The fix's only served-code change is in the G2 stage, and this act replays G2 alone.

**Re-run gate:** anything at the act beyond this table STOPs it. The worker re-runs `served_delta_g2.py` from the act's worktree
before the apply.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| A1 | the five stage Lambdas | d-5's apply (CodeSha256 per `0.9.0_WK_ETFS_RIVALS~4/evidence/lambda_after_apply_r4.txt`, verified LIVE by the issuer at 21:2xZ: all five equal) | in-place `source_code_hash` update to the package at the pin. No create, destroy, replace or policy change | re-apply at 5a4b5b5391, same window |
| A2 | gold G2 `holdings_coverage` | as served (4094 keys) | replay over the window: GQGU +307 rows, every other fund byte-equal by the table above | re-apply A1's rollback and replay G2 |
| A3 | platinum page for 2026-10-01 | `d5-publish-r4b` | republished once. GQGU's calendar reads from its own G2 rows. GQGU stays not-updated by freshness until the 07:00 ET fetch, as before | the prior page object is retained (new object, never an overwrite) |

**Writers counted:**
- **A1:** `safe-apply` only.
- **A2:** the daily Lambda's `build-coverage` stage.
- **A3:** the publish-page stage.

**Unmoved:** everything the parent half lists as unmoved, plus G1, G5 and G6, which are not replayed by this act.

## ACT-START GATES

1. `served_delta_g2.py` re-run equals the table.
2. The plan is exactly five `source_code_hash` updates (CTO condition a). Any other action is disclosed before the apply and
   STOPs until answered.
3. The live base is still d-5's apply: all five CodeSha256 values equal the evidence file (CTO condition c).
4. NEVER-2:
   - A new ledger entry `etfs-rivalfunds-round4-a1` and its sentinel are committed before the apply.
   - The union read over every live worktree comes first, with the per-tree denominator printed.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 07:00 ET 2026-10-02:** the morning fetch lands BASG then GQGU, and each fund's coverage row reads its own
  capture. S13 is DISARMED.
- **Not applied by 10:00Z (CTO fallback):** no act. The morning run writes a NEW G2 revision in which BASG's 10-01 row may read
  GQGU's capture. That is rowed under Z-W4-S13 and repaired by the next replay. **This half does not widen to cover that case.**
