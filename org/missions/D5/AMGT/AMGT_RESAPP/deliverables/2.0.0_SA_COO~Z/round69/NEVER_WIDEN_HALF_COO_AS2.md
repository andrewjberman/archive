# AMGT_RESAPP round 69 -- `AMGT-as-2` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-05 ~04:0xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at build commit `863c62a855`, or a descendant whose CONTENT-DIFF against the
DEPLOYED build equals the list below. Build and upload ONE artifact, then ONE code-only `safe-apply`. `memory_size` stays 1769.
- Executor: `0.7.0_AE_CloudOps~A`.
- Order: `task-orders/AMGT_RESAPP.TO-AMGT-as-2.the-code-redeploy.md` (`<proof_genre>DEPLOY</proof_genre>`).
- It carries as-1, drained `863c62a855`: the /ledger filings reason printed once, plus the driver-chart and forecast articles.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `6wwEU3Sw+zFE66qfpFMXKL07e5QobD35LsRm2GsOZws=` (round 68 ar-3) |
| function MemorySize | 1769 |
| artifact S3 VersionId | `3eIFUS9kZLTBHPeHXkhsf_4OF8rE41Fc` (ar-3's upload, 2026-10-05T02:08:58Z) |
| open NEVER-2 entries on this function | none (`.open_deploys/` read at signing) |

## THE FILE LIST (`--build-only` at `863c62a855`, from a detached checkout)

The build read cold-start FATAL [] and request-time break []. It is 253,758,795 B against the 262,144,000 B ceiling (96.8%,
8,385,205 B spare). Against the DEPLOYED `6wwEU3Sw...`: `CONTENT-DIFF SUMMARY: files 356, IDENTICAL 355, CHANGED 1, ADDED 0, REMOVED 0`.

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | as-1 | /ledger filings `source_reason` prints its clause once, and keeps an informative overlay clause. The covered-no-block /thesis reads "for the driver chart" and "for the forecast" (c29) |

Any other changed file at build time is a STOP.

**New S3 read paths (CTO round-67 ruling 4): NONE.** I scanned the diff `0acdb72fba..863c62a855` under `lib/` for boto3, get_object,
list_objects, s3://, Bucket= and the snapshot readers: 0 added lines. No simulate arm is owed.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `3eIFUS9kZLTBHPeHXkhsf_4OF8rE41Fc` |
| code-only `safe-apply` | the function's code only; memory stays 1769 | a code-only `safe-apply` with that VersionId, restoring `6wwEU3Sw...` |

## EXPECTED OUTCOME -- both branches

| check | base (deployed `6wwEU3Sw`, ~03:3xZ) | after (local at `863c62a855`) |
|---|---|---|
| r69 c29 | NO: C1 95 of 95 filings reasons repeat a clause; C2 "for driver chart" | YES: 95 names, 570 classes, 0 offenders, 0 hits |
| r68 c27, c28 | YES | YES |
| r67 c23, c24, c25, c26 | YES | YES |
| r64 c9, c10 (30-day), c11-c14; r65 c17; r66 c18/c19/c22 | YES | YES |
| r64 c15 (cold, day route) | YES, 1.84-1.95 s at ar-3 | read on deployed |

**Failure branch:** any of the following is a ROLLBACK, per the table:
- c29 is not YES;
- any other check moves;
- c15 reads over 5 s;
- a non-200 on a covered key's overlay, thesis, peers, timeline, ledger or collected/chatter;
- ZZZZ_US_Equity answers anything other than 404.

## WHAT THIS HALF DOES NOT COVER

Any of the following in the plan is a STOP:
- a memory change;
- any IAM change;
- a store write or an S3 delete;
- a vendor call;
- a route or gateway change;
- a data-engineering operation.
