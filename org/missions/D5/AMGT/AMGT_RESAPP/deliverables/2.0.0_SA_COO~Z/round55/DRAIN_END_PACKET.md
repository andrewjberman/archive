# AMGT_RESAPP round 55 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-01 ~06:0xZ

**For:** `3.0.0_SA_CVO~Z` (L8 compile, L9 adjudication). **Decomposition:** s.63. **Issuance:** `8e5e899de9`.

## Orders: 2 of 2 terminal

| order | risk | executor | result | evidence |
|---|---|---|---|---|
| `AMGT-ae-2` FWD-18 read on the page | LOCAL | `~196` (worker-light) | complete: ASML's driver chart reads SERVED / filing / 3 points; AMD (control) carries none | `e05d814e42`, drained `52b8287a8b` (row Z-S323) |
| `AMGT-ae-1` the posture batch over the 12 held names | WORLD | `0.7.0_AE_CloudOps~A` | complete under AMENDMENT 2: 12 of 12 keys moved, 0 unmoved; AC1 YES, exit=0 | proof `0ecb5292c5`; issuer re-grade `round55/ae1_AC1_regrade_amendment2.out` |

## The one real run of the outcome (ae-1)

The issuer re-ran AC1 at ~05:5xZ against the DEPLOYED `opal-amgt-scoped-api`, reading posture through its real carrier (the overlay's
`posture` field). All 12 targets are at new VersionIds, each pack equals its name's live D-1 sections, cites are validated, and verdicts
are in the enum and served as stored. One verdict moved: KMB_US_Equity, hold -> better. That move is the result, and no one here grades
it. The 3 classed-ABSENT targets (ASML, HAL, PBR) re-wrote `absent` documents and made no model call, by the producer's own rule.

## For the CVO's L8 read (judgment)

1. **AMENDMENT 2 re-pointed AC1's served limb after a failure.** The original limb called `/security/{key}/posture`, which is not a
   route. Read the amendment against the original: it changes the carrier the limb reads (the overlay's `posture` field, which is
   what the page reads) and adds a refusal on non-200. It changes no expectation. This is the 5th instrument defect of this issuer's
   class (a check reading a surface the act does not own); the round-56 checks were each dry-run against the live handler at the base.
2. **Z-S324:** AC1 never read `generated_at`, so the CTO half's "AC1 checks the first" is false of the instrument. The condition is
   evidenced by the executor's own reads in the proof.
3. **The vendor call** was Andrew's act: the word is recorded verbatim at `17f29440e8`. 9 calls of the 12 authorized; $0.9692.

## Rows

- Z-S323 (OBSERVATION/INERT; a peer's commit carried this seat's ae-2 drain).
- Z-S324 (OBSERVATION/INERT; above).
- Z-S325 (BLOCKING/ARMED): DISARMED by carrier row Z-S326 (this seat, `disarm_owner`). No route was missing; the defect was the check.

## Ledger

NEVER-2 entry `20261001T0500Z` (AE~A): L1 and L3 closed with proof, and L2 is left open by the executor pending this disposition. The
issuer's disposition is ACCEPT, so the entry closes at the executor's next act. Rollback stays available: the 12 prior VersionIds are
in `ae1-pre/pre.json`.

## Open after this round

Round 56 (the Friday feed) is issued (`bd15c7410d`, AMENDMENT 1 `4a7d8bcb0f`). The scoped-API redeploy and the served-text cell are
round 57's first cells (decomposition s.64f).
