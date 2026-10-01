# AMGT_RESAPP round 55 -- `AMGT-ae-1` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-09-30 ~23:5xZ

**The act (ONE):** for each of the 12 targets below, `python -m lib.research.posture.judge --security-key K --as-of <A> --write-pool`,
where `<A>` is the target's prior `as_of`. Each run makes ONE Anthropic message and OVERWRITES `posture/v1/K/<A>.json` in a versioned
bucket. Executor `0.7.0_AE_CloudOps~A`; order `task-orders/AMGT_RESAPP.TO-AMGT-ae-1.posture-batch-over-the-held-names.md`.

**THE VENDOR CALL IS ANDREW'S PER-USE WORD.** Asked in the terminal on 2026-09-30 ~23:2xZ: 12 messages, ~$1.3. This half does not
authorize it, and no GO issues without it.

**THE PIN: CLOUD `51df60aa1a`.** `lib/research/posture/` and `drafting_build.py` last changed at `8b71efd6fc`. Run from a checkout at the
pin, never HEAD.

## THE BASE, read live at signing (23:56Z) -- the rollback per key

| subject | as_of (the key) | VersionId (rollback) | verdict | comparable |
|---|---|---|---|---|
| ASML_NA_Equity | 2026-09-16 | `m5QcEcVW2G7eZ9fmd4tTzKblydmFpVWF` | absent | -- |
| BABA_US_Equity | 2026-09-15 | `JDmWDLUj4sENvxWyTee5NAMXwd7jI1R_` | worse | HD_US_Equity |
| BA_US_Equity | 2026-09-15 | `WzkPzvP1CR95Hhl7yG9aOsDkglOMXry5` | hold | DE_US_Equity |
| COST_US_Equity | 2026-09-16 | `CzHOxs2jSiCVVrx.RqsCmE7z1Adhdw7_` | better | TJX_US_Equity |
| HAL_US_Equity | 2026-09-16 | `56iI31aLljlgFbAln9A45uQ0wg3rHcYt` | absent | -- |
| HD_US_Equity | 2026-09-16 | `dPcDrN1Adz1ytjaJA8TKCs_zeMNSRyDr` | better | LOW_US_Equity |
| INTU_US_Equity | 2026-09-16 | `Qdcuo0_6jHsmenPlc5BM5jihuOo9HDH9` | better | CDNS_US_Equity |
| KMB_US_Equity | 2026-09-16 | `3PlyWiWFNGVoid0d7dkhUwWewf5C5NTp` | hold | EL_US_Equity |
| NU_US_Equity | 2026-09-16 | `ENfneKossJZvgmYjLT4YcLbf6ugz2DqX` | better | TFC_US_Equity |
| PBR_US_Equity | 2026-09-16 | `n86.UC0BIOm1F0GdNh8RzSLIqrP3ps4B` | absent | -- |
| SAP_GY_Equity | 2026-09-16 | `m43IKqV5pWvfzcnj6LZikZX2x8khoJkS` | better | ANET_US_Equity |
| VLO_US_Equity | 2026-09-16 | `ErRHPqYPzhV0.P25TVvkPnX7zXhgWBMj` | better | WMB_US_Equity |

**The target set, derived:** of 35 posture subjects, these 12 are the ones whose own name, or whose comparable, now holds D-1 sentences.
BABA's comparable HD is a held name; HD is also a subject. Immediately before the first call, re-read every VersionId. A moved one is a
STOP and a re-sign.

## WRITERS OF THE PROPERTY: 1

`posture/v1/` has one writer, `judge.write_pool_object`. It is reached by the judge CLI or by `management_posture_batch.py posture`. No
schedule invokes either (`comp-schedule` DECLARED-NOT-APPLICABLE at rk-22).

## READERS

- The scoped API's `read_posture` serves the LATEST `posture/v1/<key>/<as_of>.json` by date (`read_pool_object`), as stored. It does not
  re-read D-1.
- The page's posture card reads `read_posture`.
- A same-key overwrite therefore moves the served /posture for these 12 names and nothing else.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| 12 judge runs | exactly the 12 keys above, overwritten (a new version each); 12 Anthropic messages | copy each key's VersionId above back as the current version -- a write, not a delete |

## EXPECTED OUTCOME -- both branches, read from the producer's own rule (never predicted)

- **A target whose comparable resolves (9 of 12):** the packs are rebuilt from the LIVE D-1s, so each pack's `drafted_sentences` equals
  its name's live D-1 section count. The judgment re-runs, and its verdict is whatever the model returns on the new packs. The verdict
  MAY move; if it does, that move is the RESULT, printed and graded by no one here. Every S: cite is validated before the write (the
  judge refuses to write an unvalidated cite).
- **A classed ABSENT target (ASML, HAL, PBR):** the judge re-classes the unresolved side (`judge.run`). If it still cannot resolve, it
  writes an `absent` document again with no model call. If the side now resolves, it calls the model and writes a verdict. Both branches
  are covered by AC1's enum.

## THE LANE STOPS on any of six limbs

1. There is no per-use word from Andrew for the 12 calls.
2. The run is not from `51df60aa1a`, or a base VersionId moved.
3. `pre` lists a target count other than 12.
4. A 13th target, a 13th model call, or any management-stage call (Lusha / Bright Data).
5. Any write outside the 12 keys, or any delete.
6. AC1 fails after the act. That is the ROLLBACK trigger.

## THE FALSIFIERS, positive arm shown at the cut

- **At the base:** AC1 FAILS (12 keys at their pre-batch VersionIds).
- **On a simulated post-state:** AC1 PASSES (new VersionIds; packs equal to the live D-1 sections).
- **With the packs unchanged:** AC1 FAILS.
- **The volatile set:** two live /posture reads 3 s apart differ on 0 paths.

Signed: `2.0.0_SA_COO~Z`, 2026-09-30.
