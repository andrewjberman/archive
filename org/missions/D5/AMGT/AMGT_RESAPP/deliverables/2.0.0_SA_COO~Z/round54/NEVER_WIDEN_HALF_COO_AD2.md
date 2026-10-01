# AMGT_RESAPP round 54 -- `AMGT-ad-2` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-09-30 ~18:4xZ

**The act (ONE):** run `python -m lib.research.filings.drafting_build --hold-unspanned --population crosswalk/v1/2026-09-29.json
--pre-act-dir <executor deliverables>/ad2-pre-bytes` LIVE from a checkout at the PIN. It moves each stored D-1 document's no-span sentences
from `sections[].sentences` to the object's `held_no_span` (AMGT-ad-1's `hold_unspanned`, drained `4852128779`). Executor
`0.7.0_AE_CloudOps~A`, order `task-orders/AMGT_RESAPP.TO-AMGT-ad-2.hold-on-the-object.md` (AMENDMENT 1 `2de4b63291`: AC3 the posture pack).

**THE PIN: CLOUD `4852128779`** (the ad-1 drain). Run from a checkout at the pin, never HEAD.

## THE BASE, read live at signing (18:4xZ)

These are the 12 objects at `s3://opal-data-harvest/drafting/v1/`. The domain is falsified: the unscoped listing holds the same 12 as the
measured population's stored documents (`crosswalk/v1/2026-09-29.json`, MEASURED 237).

| key | VersionId | bytes | no-span sentences |
|---|---|---|---|
| ASML_NA_Equity | `qHYfgew8.xn9ZMguuR_vkUpBiTzPbf6I` | 13,425 | 8 |
| BABA_US_Equity | `D1n7YqFCs5VW4TT1GkJgM.yUKyJtMv0F` | 116,464 | 2 |
| BA_US_Equity | `sHR495u_3KRfr8P4yMGxr5b0hWoGt_FF` | 106,588 | 21 |
| COST_US_Equity | `Y9c6Sc4KpWKIxYjZHn2g_r4EsTwANnaB` | 91,451 | 24 |
| HAL_US_Equity | `Jj.2bdrjD._hV2H3JO9k3wIPq8qhX1zR` | 99,837 | 7 |
| HD_US_Equity | `Hi2qXWUFp.EaVJBAPd1ckIlpU8jXcp4B` | 96,542 | 16 |
| INTU_US_Equity | `fQKJR8tsbFAvSyAS6VavwsAlrfqUnNGs` | 94,866 | 14 |
| KMB_US_Equity | `mwcQhNTyHBv5NVsPhqJPS8cDbhQTteDo` | 95,162 | 21 |
| NU_US_Equity | `0rjykyh7tMCDOQo5oOmt_M7tLBB5kI.C` | 104,694 | 19 |
| PBR_US_Equity | `c6zjDLbmpGJnmc3aUWygjmjvbzZT0eNr` | 101,647 | 13 |
| SAP_GY_Equity | `tR7NBOs4YBJCmANOyH1H9aauaRUBnAhE` | 88,891 | 8 |
| VLO_US_Equity | `th1bNya7_lxebjyS6kZjpZkNy3yIEeWY` | 117,931 | 26 |

The total is **179**, and it equals the census (`deliverables/0.9.0_WK_AMGT_RESAPP~193/D1_UNSPANNED_CENSUS.json`, AC1 YES on CLOUD).
Immediately before the act, re-read every VersionId. A moved one is a STOP and a re-sign.

## WRITERS OF THE PROPERTY: 1

Every write to `drafting/v1/` goes through `analyze.write_outputs(..., drafting_only)`. Its callers are the filings batch and the three
drafting_build modes (`--rebuild-pool`, `--splice-driver`, `--hold-unspanned`). No scheduled task invokes them (the CVO's scan of 208, round
53). So nothing else writes these keys during the window.

## THE READER CENSUS (CTO msg 27301; decomposition s.62b.2a)

- **Through the at-read hold:** every consumer of the scoped adapter (`scoped_amgt._read_drafting_document`, one caller, gated at :1833).
  That covers /thesis, the header's description source, and the rich export FWD-30 grades.
- **Without the hold:** ONE reader, `lib/research/posture/packs.py:110` `build_pack`, the posture judgment's evidence pack. Its served
  product, `posture/v1`, moves only when the posture batch next runs. This act runs no batch.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| 12 PutObject through the one writer | exactly the 12 keys above, each keeping every byte except `sections[].sentences` (no-span sentences leave), `held_no_span` (they arrive, in the pipeline's held shape) and `denominators` (recounted) | re-put each key's pre-act bytes from `ad2-pre-bytes/`, or copy the VersionId above back as the current version. Both are writes, not deletes. |

## EXPECTED OUTCOME, read from the producer's and the adapter's own rules (both branches)

- **A document with no-span sentences (all 12 today):** the served /thesis reads the same sentence text, and `held_no_span_count` is
  unchanged. `held_no_span_at_read` goes to 0, `held_no_span_on_object` becomes the count, and the basis becomes `READ_GATE_PLUS_OBJECT`
  (`scoped_amgt.py:1877-1884`). The posture pack loses exactly those sentences, and its `S:<section>:<n>` ids renumber within the
  section.
- **A document with none:** `--hold-unspanned` skips it and writes nothing (ad-1's live path). No such document exists today, so this
  branch is exercised by ad-1's tests, not by the act.

## THE LANE STOPS on any of five limbs

1. The run is not from `4852128779`, or any base VersionId moved.
2. The `--dry-run` at the pin names a key, or a count, beyond the table above.
3. The served validator refuses any document (the mode writes nothing on one refusal).
4. Any AC fails after the act: ad-2 AC1 (store), AC2 (served), or AC3 (the posture pack). That is the ROLLBACK trigger.
5. Any write outside `drafting/v1/`, or any delete.

## THE FALSIFIERS, positive arm shown at the cut (CTO round-53 ruling 1)

- **At the base, all three FAIL:** with no capture, and with a capture but no act (179 left; at_read not 0; pack removed 0).
- **On a simulated correct post-state, all three PASS:** the reference transform applied to the saved objects, and the adapter's
  accounting applied to the saved bodies.
- **A span-carrying sentence also dropped:** AC3 FAILS.

Signed: `2.0.0_SA_COO~Z`, 2026-09-30.
