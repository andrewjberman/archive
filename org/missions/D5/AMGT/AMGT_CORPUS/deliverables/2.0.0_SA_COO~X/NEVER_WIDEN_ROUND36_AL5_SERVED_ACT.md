# AMGT_CORPUS round 36 -- never-widen pair for `CRPS-al-5`: one code-only redeploy of `opal-amgt-scoped-api` carrying al-1

**Authority:** round-35 analysis @`02bbbc0208` ruling 1 (FWD-20: the V3 rows "with their reason where none is measured").
Decomposition v36.0 @`80717c897c` s.1, cell al-5. al-1 drained @`98a93db70b` (`read_model` serves `fiscal_unresolved`).

**The act (ONE):** build `opal-amgt-scoped-api` at `288de3d95d` (or a descendant whose CONTENT-DIFF against the deployed function
equals the one file below), upload ONE artifact, then ONE code-only `safe-apply`. `memory_size` stays 1769. One NEVER-2 entry,
slug `amgt-corpus-r36-al5`, opened before the upload and closed after the reads.

## SEQUENCING -- after AMGT_RESAPP's in-flight redeploy

`amgt-resapp-r67-aq5-grant-and-code-20261004` (`0.7.0_AE_CloudOps~A`, opened 21:15Z) re-deployed this function at pin
`d8bafe6896`. Its upload and code-only apply landed. Its verify leg L4 is OPEN at this half's writing. **This act starts only after
that entry CLOSES.** If aq-5 rolls back instead, this half's base is void: re-read the base and re-sign.

## THE BASE, read live at writing (2026-10-04 ~22:2xZ) -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `aoQ+WrefJ+JjQcymqyrt2c7MEIlTPmvjJEv8sqZ6M98=` (aq-5, LastModified 2026-10-04T21:41:09Z, LastUpdateStatus Successful) |
| function MemorySize | 1769 |
| artifact S3 VersionId | `auoGQqF5cmI7xLgeCy6Z5Qq4w2TQ7icX` (41,158,901 B, 21:35:13Z, aq-5's upload) |

## THE FILE LIST (`build-and-upload-scoped-amgt.sh --build-only` at `288de3d95d`, clean detached checkout)

Build rc=0. VERIFY-SCOPE reads cold-start FATAL [] and request-time break []. ISOLATED OK, 3 of 3 arms. SIZE is 253,753,934 B
against the 262,144,000-byte ceiling (96.8% used, 8,390,066 B spare). Against the deployed `aoQ+WrefJ...`:
`CONTENT-DIFF SUMMARY: files 356, IDENTICAL 355, CHANGED 1, ADDED 0, REMOVED 0`.

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED (+6) | al-1 `b1b78d3812` | the `/thesis` payload's model slice gains `fiscal_unresolved`: the block's fiscal-scope `unresolved` entries `{mnemonic, fiscal_year, reason}`, as served; `[]` when none or no block. No other key moves. |

The commits between `d8bafe6896` and `288de3d95d` also change `lib/opal_data_harvest/{config.json, worker.py}`. They are OUTSIDE
this function's import closure (the content diff lists 0 such files). **Any changed file beyond the one above, at build time, is a
STOP.**

## WRITERS of the served property

One writer: `read_model` in `scoped_amgt.py`, reached by the `/thesis` route of this function. The values it copies are
written by one producer, `stage_derive` (round 35, 96 blocks of 2026-10-04T1956-1958Z).

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned bucket) | the prior VersionId `auoGQqF5cmI7xLgeCy6Z5Qq4w2TQ7icX` |
| code-only `safe-apply` | the function's code only; memory stays 1769 | a code-only `safe-apply` with that VersionId, restoring `aoQ+WrefJ...` |

Never touched: any S3 data object, any model block, any portal file, any grant, any other function.

## EXPECTED OUTCOME -- both branches

| read on the DEPLOYED function | base (`aoQ+WrefJ...`) | after |
|---|---|---|
| `/thesis` 1299_HK_Equity: `model.fiscal_unresolved` | key absent | 97 entries, equal as a multiset to the block's fiscal-scope `unresolved` (al1_check b1's rule) |
| `/thesis` BA_US_Equity: `model.fiscal_unresolved` | key absent | `[]` (the block has none) |
| `/thesis` both: `model.fiscal_year_figures` length | 543 / 686 | 543 / 686, unchanged (al1_check c1's rule) |
| aq-5's L4 regression set (r64 c9-c14, r65 c17, r66 c18/c19/c22, r67 c23-c26, c15 cold on the day route, the RANGE route) | as aq-5 closes it | unchanged |

- **Branch A, the act holds:** every row above reads as "after". Close the entry.
- **Branch B, it does not:** any regression changes, a non-200 on a covered key, or a `fiscal_unresolved` count that differs from
  the block. Roll back to `auoGQqF5...` the same session, re-read the CodeSha256 as `aoQ+WrefJ...`, and file a row.

**Executor:** `0.7.0_AE_CloudOps~A` (the seat that ran ap-4 and aq-5 on this function), on the issuer's word once the CTO half is
signed and aq-5 is closed. Otherwise the issuer runs it under the same entry.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-04 ~22:2xZ, for the one upload plus one code-only `safe-apply` at `288de3d95d`
(or a descendant with an equal content diff), memory 1769, with the `auoGQqF5...` rollback, covering branches A and B, after aq-5
closes.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
