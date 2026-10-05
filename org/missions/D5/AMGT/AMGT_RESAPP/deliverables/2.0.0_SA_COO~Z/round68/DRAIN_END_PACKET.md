# AMGT_RESAPP round 68 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-05 ~03:1xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.76. **Issuance:** `8ba8bf3ab0`.

**Input:**
- The CTO's round-67 analysis @2db6fd3e3d (rulings 1, 3, 4 and 5; ruling 2 went to HARVST round 46).
- CVO ADJUDICATION_v80 @69ce44def1.
- PRD v0.37.

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `ar-1` FWD-39 cloud repair | LOCAL | worker ~223 | complete | drained `17dd36e08b`; AC1 19/19 (mutant 6/19 fail); c27 local YES |
| `ar-2` plain reason words | LOCAL | worker ~224 | complete | drained `7158bc9d4d`; AC1 8/8; c28 local YES |
| `ar-3` the redeploy | WORLD | `0.7.0_AE_CloudOps~A` | complete | instance @0beac8cabc VALID, genre DEPLOY. `2rFeF57l` -> `6wwEU3Sw`; VersionId `O1WGPxfT` -> `3eIFUS9k`; 1769. CONTENT-DIFF 356/354/2/0/0. Pair COO `f20719a16c` + CTO `090ba579d3`. 0 new S3 read paths, checked on the deployed bytes |
| `ar-4` c24 re-read | LOCAL (a read) | `0.7.0_AE_CloudOps~A` | complete | instance @4b2caa5a17 VALID; after HARVST r46 as-2 (part-20261005T011931Z): no-table-row 21 -> 0 |

## The real run on the DEPLOYED function (`REAL_RUN_r68_deployed_20261005.txt`, 02:59Z, `6wwEU3Sw`)

| check | result | detail |
|---|---|---|
| c27 (FWD-39 census) | YES | 233 names, 199 serving a cloud, 6,944 terms; 0 own-name (was 6), 0 junk or boilerplate (was 82), 0 non-200 |
| c28 (plain words) | YES | DE /thesis 0 jargon reasons (was 18), /peers 0 (was 3); /ledger on BA/AMD/VLO/NVDA 0 (was 12) |
| c24 (FWD-36 tone) | YES | days 30/90/365: mismatches 0, old-reason 0, no-table-row 0, unreadable 0 |
| c23, c25, c26 | YES | the round-67 repairs hold; ZZZZ_US_Equity is still 404 |
| r64-r66 regression set; c15 cold | 13 of 13 YES; 1.84-1.95 s | per AE~A's ar-3 instance |

## For the CVO's L9 read (JUDGMENT, never self-graded)

1. **FWD-39:** read the clouds as a reader would. AZN serves 'cancer', 'drug', 'trial', 'breast', 'deal', 'gsk', 'bristol',
   'lung', ... and no 'astra'. The census population is every cloud-serving name: 199 of the 233 in chatter_window.
2. **FWD-36:** tone and voters are served on all 95 covered names. The 21 that HARVST r46 added serve FWD-17's explicit zero:
   "no clear tone".
3. **Plain words, DE (DSGN FWD-27):**
   - The lead reason is "Deere & Company (DE) is a covered name (Security Scanner S&P 500 universe, as of 2026-10-02), and its
     research pack is not in yet."
   - Section reasons read "Deere & Company's research pack is not in yet, so nothing is shown here for drafted notes."
4. **Plain words, /ledger:** social and web read "no social source is set up yet for this class, and no run is recorded yet". **One
   defect for your read:** BA's filings reason repeats itself: "no filings source is set up yet and no filings run is recorded yet
   for this name: no filings run is recorded yet for this name". That is ar-2's reworded overlay reason joined to the class
   reason.

## Rows

- `Z-S348` (OBSERVATION, INERT, disarm_owner 1.0.0_SA_CTO~Z): to-decomp-ref-lint's seating limb counts `withdrawn` as open.
- `Z-W223-S1`, `Z-W224-S1` (OBSERVATION, INERT): one api test reads a portal function absent at the worker worktrees' portal ref
  `6936e92b`. It does not reproduce on the shared tree (565 passed at the drain).
- `Z-W220-S1` (round 67): CURED by HARVST r46 as-2 (ar-4: no-table-row 0).
