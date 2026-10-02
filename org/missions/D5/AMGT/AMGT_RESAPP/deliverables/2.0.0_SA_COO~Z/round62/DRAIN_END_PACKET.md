# AMGT_RESAPP round 62 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-02 ~11:4xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.70 (+70f). **Issuance:** `59d350c2a4`; AMENDMENT 1 `a12291728f` (drained `a2ff06d1a1`).
**Input:** CTO round-61 addendum ruling 5 @`f1d5dac151` and ruling 5a @`e041af6102` (row `DSGN_AMGTV1-Z-C-S29`, demo risk).

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `al-1` (A) the memory raise | WORLD | `0.7.0_AE_CloudOps~A` | complete: 10240 MB | proof `339b159ea0`; 3538 missed (21.7/20.4/22.9 s); 10240: 3 of 3 cold 200 at 16.9/16.6/19.1 s; control sha unchanged |
| `al-2` the silver read under an 18 s deadline | LOCAL | issuer | landed | `a12291728f`; `test_timeline_silver_deadline.py` 3 passed; build-only CHANGED 1 |
| `al-1` (B) al-2's code-only redeploy | WORLD | `0.7.0_AE_CloudOps~A` | complete: LIVE 11:27Z, graded 11:32Z (inside the 12:30Z freeze) | proof `9da65fe4b6`; CodeSha256 `E+FAZF0f...` -> `bZBmEtRr...`; pair COO `a12291728f` / CTO `57dfa6bd84`; entry CLOSED |

## The real run on the DEPLOYED function

- **Executor (cold):** 3 of 3 concurrent BA `/timeline/day/2026-09-08` runs returned 200. Runs 1 and 2 took 15.1 and 16.5 s with
  headlines. Run 3 hit the deadline at 18,006 ms and served `headline_reason` with null headlines. Both control days (BA 2026-09-30,
  2026-10-01) were byte-equal to their pre captures.
- **Issuer (warm, ~11:4xZ):** deployed `bZBmEtRr...` at 10240 MB. BA 2026-09-08 returned 200 with 5 of 5 headlines and no reason. Both
  controls were byte-equal. The B1 regression (company names) read YES.

## For the CVO's L8 read

1. Memory is not the bound: max used was about 460 MB at every tier. 10240 is Lambda's maximum.
2. Row `Z-S337`: the 18 s line sits INSIDE the cold spread (15.1-19.1 s), so some cold BA day views serve null headlines with the plain
   reason. PROD's page renders that as '[no headline]' (TimelinePanel.tsx:354, CTO read). This is the specified outcome, and no rate
   is claimed from 3 runs. Track C (the read path itself) is post-demo.
3. Carried for DSGN after the demo: print `headline_reason` in place of '[no headline]' (CTO msg 28416).
4. The freeze holds: nothing deploys to this function between 12:30Z and the end of Andrew's read.

## Rows

`Z-S336` (AE~A: not memory-bound), `Z-S337` (AE~A: the deadline fires inside the cold spread). Both are carried to round 63, track C.
