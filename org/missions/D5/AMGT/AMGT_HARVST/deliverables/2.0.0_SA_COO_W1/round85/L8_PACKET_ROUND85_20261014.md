# AMGT_HARVST round 85 -- the drain-end packet to the CVO (`2.0.0_SA_COO~W1`, 2026-10-14 ~14:0xZ)

Round 85 has four orders, all terminal. `round-close-check.py --project AMGT_HARVST --round 85` reads `orders=4 ... 3 complete, 0 not complete and outside the verdict ... PROOFS complete=3 proof_ok=3 proof_bad=0 ... verdict=MAY-CLOSE`
(bz-9, bz-10, bz-11, bz-12; the three complete are all but bz-11, which is CANCELLED, NOT MET). No order of the round is open. No ledger of the round is open (bz-10's closed on 5 legs).

## Orders and what each one's own criteria read

| order | executes | status | criteria |
|---|---|---|---|
| bz-9 | worker `~139` | complete | AC1 24 passed, AC2 76 passed; merged `44aadb7f1d` under COO `a3eba883d4` + CTO `9eef371300`; the one-refresh-per-publisher-per-cycle seam, flag `--refresh-once` default OFF |
| bz-12 | worker `~140` | complete | AC1 3, AC2 100 passed; merged `3d88eccbc3` under COO `edd78f4c0d` + CTO ADDENDUM 1 `5cace36910`; `REFRESH_PUBLISHERS = {wsj, barrons}` so a bbg job can never spend the refresh on the Google credential |
| bz-10 | `~ZW` | complete | AC1-AC3 PASS: runner re-registered windowless with `--refresh-once` from `3d88eccbc3`, T0=2026-10-14T00:08:31Z, R1-R4 TRUE at +3/+15, 5 of 5 pins locked, ledger CLOSED on 5 legs. Whether a refresh WORKS was bz-11's, not bz-10's |
| bz-11 | `~ZW` | **CANCELLED, NOT MET** | AC1 `CLOSE=NOT_MET` (committed `bz11_AC1.out`, `c5134bfbc2`): wsj `NOT_CURED`, barrons `NOT_CURED`. AC2 10 passed (re-run by me). Instance `VALID (rc=0)` with AC1 recorded FAIL as the order directs |

## What bz-11 read (the round's one real run)

Thirteenth and closing read, 2026-10-14T12:33:33Z, by `~ZW` from the site Z checkpoint files. wsj cycle `20261014T121845Z`: refusal class `expired` at 12:27:51Z, refresh begun, `REFRESH done` 12:28:08Z (17 s), the same publisher's retried job refused `class=expired` again at 12:29:46Z, detail `SignInRefused: 401 under --no-sign-in: no refresh`. barrons cycle `20261014T122950Z`: same shape, refresh done 12:30:24Z (16 s). Both publishers, first cycle each under the new pin. The runner then began its next bbg cycle and is running, untouched.
What it establishes: the refresh fires once, reports `done`, and does not cure the expiry in the next job. What it does NOT establish: why. No seat read a session, credential or producer source.

## Rows for your compile (my last read of your watermark: v78, 2026-10-13T19:45Z; later compiles unread by me)

- `AMGT_HARVST-Z-S121` (OBSERVATION / INERT, my disarm_owner, filed by `~ZW`, `UNDER_INVESTIGATION`): the bz-11 result above. Carried to the CTO's round-85 analysis; I do not answer it.
- `AMGT_HARVST-Z-S119` (BLOCKING / INERT, mine): the refresh round 85 built for it did not cure it on the first cycle of either publisher. My word: still open; Z-S121 is its evidence.
- `AMGT_HARVST-Z-S120` (INERT, mine): nothing creates the runner's stop file's parent directory; carried to the park record.
- `AMGT_HARVST-D1-S16` (BLOCKING / INERT, mine): the merged `--refresh-once` decided on the class only, so a bbg job could have spent its refresh through the Google credential. Answered by bz-12 (merged `3d88eccbc3`, CTO ADDENDUM 1).
- `AMGT_HARVST-D1-W139-S3` (BLOCKING / INERT, mine): the worker's proof instance carried a wrong `decomp_ref.to_ref`; corrected by the issuer after the merge (`8821b89159`), proof VALID. `D1-W139-S1`, `S2` OBSERVATIONS, no action.

## What I did NOT verify

- The site Z checkpoint files and `cycle_runner.log` behind the NOT_MET verdict: they live on site Z and I read none of them from dell1. I verified `~ZW`'s committed `bz11_AC1.out`, the instance (`proof-of-spec-check --governing-order` VALID rc 0 on a detached checkout of origin/CLOUD `9098d3db03`) and AC2.
- Why the refresh did not hold. No diagnosis is claimed anywhere in this packet.
- That any WSJ or Barron's session survives a cycle: this is still not shown.

## Inputs for the FWD board (graded by the CTO/CVO, never by me)

The journey outcome this project exists for, a harvest cycle that completes for wsj and barrons without an expiry stop, is NOT shown at the end of round 85. bbg completes cycles; wsj and barrons do not.
Andrew-direct ~21:1xZ 2026-10-13 (CTO msg 5209) set the park after round 85; with NOT_MET the CTO's analysis decides whether the park stands or round 86 is cut. I take no park action before that.
