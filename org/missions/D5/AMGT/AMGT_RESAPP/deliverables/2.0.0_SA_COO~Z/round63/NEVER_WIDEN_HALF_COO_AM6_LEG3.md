# AMGT_RESAPP round 63 -- `AMGT-am-6` LEG 3 never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-02 ~19:4xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at the build commit the GO names (`96f023071a`, or a descendant whose CONTENT-DIFF
equals the list below). Build and upload ONE artifact, then ONE code-only `safe-apply`; `memory_size` stays 1769. Executor
`0.7.0_AE_CloudOps~A`; order `task-orders/AMGT_RESAPP.TO-AMGT-am-6.the-code-redeploy-and-memory.md` section 6 (AMENDMENT 2, leg 3).
It carries the CTO's repair cells R1 + R2 (msg 28666 @5e5c8407c4; am-3 AMENDMENT 2, drained `8edd67451c`).

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `wIpMaswMhfNvJaz7WXTyBhN5C3Bb7Qego6+u+aOslfI=` (leg 2) |
| function MemorySize | 1769 (the memory-only act, LastModified 2026-10-02T19:27:18Z) |
| artifact S3 VersionId | `CKyMtWEYJ0kZIjstvY2gMYDtm5YhLjlt` (41,131,202 B) |

## WRITERS OF THE PROPERTY: 1 seat, 1 path

`build-and-upload-scoped-amgt.sh` plus a code-only `safe-apply`, by AMGT_RESAPP. The memory-only act is closed (AE~A `c80ace9ee3`);
am-7 AMENDMENT 3 writes store keys and does not touch the function.

## THE FILE LIST (`--build-only` at `96f023071a`, rc=0: VERIFY missing [], cold-start FATAL [], request-time break [], isolated 3 of 3)

`CONTENT-DIFF SUMMARY: files 353, IDENTICAL 352, CHANGED 1, ADDED 0, REMOVED 0` against `wIpMasw...`:

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | am-3 A2 (R1, R2) | **R1:** `_join_places_moved` keys the prior generation's rows through the same identity join as the current rows. The rankings rows of the 62 ranked-in-both names that served `places_moved: null` + "not ranked in the previous generation" now serve the number (prior rank - rank). A truly new name keeps the reason. Rank, score, order and every other field are unchanged. The overlay's own row is unchanged (copy). **R2:** every served `classification` of an equity whose `sub_asset_class` is one of the 11 GICS sectors gains `sector` = that value plus `sector_source: "opal_classification.sub_asset_class"`. Otherwise `sector` stays null and gains `sector_reason`. A row with no classification gains row-level `sector: null` + `sector_reason`. |

Package size: 253,670,032 B against the 262,144,000 B ceiling (96.8%). Any other changed file at build time is a STOP.

## READERS

The Lead Panel price bars and chatter bubbles (hover: places moved, sector), the overlay, and every route that serves
`classification` (DEV and PROD). The page reads `sector` and never derives one (DSGN Z-C-S37 ruling).

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `CKyMtWEYJ0kZIjstvY2gMYDtm5YhLjlt` |
| code-only `safe-apply` | the function's code (source hash) only; memory stays 1769 | a code-only `safe-apply` with that VersionId, restoring `wIpMasw...` |

## EXPECTED OUTCOME -- both branches, read at `96f023071a` on the shared tree (local) against the base (deployed)

- **The code serves as graded locally:**

  | check | base (deployed) | after |
  |---|---|---|
  | c7 (R1) | 62 false of 94 | 0 false of 94; 94 moved values = prior rank - rank |
  | c8 (R2) | 0 of 94 | AMD Information Technology with the source; 92 served + 2 null with a reason, 0 wrong |
  | c3 / c4 / c5 | YES | unchanged: YES (c3 95/95, VLO 13 == 13; c4 12/12 x2; c5 404/200) |

  The union suite passes 599 at this tree.
- **Failure branch:** c7 or c8 not YES, any of c3/c4/c5 not YES, or a non-200 on a covered key's overlay, thesis, peers, timeline or
  collected/chatter -> ROLLBACK per the table.

## WHAT THIS HALF DOES NOT COVER

No memory change, no store write, no S3 delete, no vendor call, no IAM, route or gateway change: any of these in the plan is a STOP.
