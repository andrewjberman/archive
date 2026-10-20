# NFRA_SCHWABBF round 1 -- release plan R0-R8 and the never-widen pair (COO half)

**Issuer:** `2.0.0_SA_COO~SB` (laptop). **Halves:** CTO half = `1.0.0_SA_CTO` (OWED); COO half = this file (SIGNED below).
**Status: SUPERSEDED before any act ran (2026-10-20 ~14:5xZ).** PRD v0.3/v0.4 moved C-KEYFORM from `schwab/<master>/bronze/...` to `schwab/<firm>/bronze/...` on Andrew-direct (CTO msg 109902). Every key in sections 2, 4 and 5 below is the master form and is wrong under v0.4; the acts R0-R8 are re-cut in round 2 on the firm form. Kept as written because it records the sequence, the hazard that a push of `box/laptop` deploys the bd-tree reader (the hold request to MSTR stands), and the converter-event fan-out. NO halves are signed on it; the COO half below is VOID.
**Original status:** all six round-1 cells merged and drained; NOTHING DEPLOYED, NOTHING MOVED. This plan was the cutover of PRD C-MOVE, C-DAILY, C-EQUAL and the FWD-1 trace.
**Andrew-direct (2026-10-20 ~13:0xZ call 2, "Yes, rec is accurate"):** one cutover, same-day rollback, no side-by-side period; the old keys are deleted only on his confirmation.

## 1. Code and pin

- **Pin:** `293346aff1` on `box/laptop` (the chain-A drain merge; it carries `98290da161` (puller), `c98271602c` (trace) and `39f21f2064` (equality) already on origin as of `efe09d5f9156` (ls-remote read 2026-10-20 ~14:3xZ); `293346aff1` is LOCAL). It must be on origin before R5.
- **Cells:** `BF-k-1` the key function pair; `BF-m-1` the move tool; `BF-r-1` the two hand-parsing readers; `BF-w-1` the puller; `BF-e-1` the equality tool; `BF-t-1` the trace.
- **Drain evidence (merged tree, 2026-10-20 ~14:3xZ):** 310 passed across the six round test files; `data/assets/scripts/silver/tests/test_schwab_runtime.py` 11 passed; `py_compile` clean on 7 files. Live read-only seams: move plan `in_scope=516` on the real `08403355/bronze/acc` listing; trace `THREAD-OK` on 2026-10-16 and `NOT-HELD` on 2026-10-17.

## 2. The acts, in order (one change-management entry opened before R3; the NFRA CloudOps lane runs the AWS acts, rule 34)

| # | act | who | home | rollback |
|---|---|---|---|---|
| R0 | re-read Schwab's served floor per master (wide `-Mode enumerate`, session lock, outside the fires) | NFRA CloudOps lane on the Schwab box | box `i-0f3d57a97f14727af` | read only |
| R1 | open the change entry naming EVERY family that reads Schwab bronze (one `describe` sweep) and confirm the copy identity's Get/Put on `schwab/<m>/bronze/*` | COO + CloudOps | `org/critical_paths/change_management/` | n/a |
| R2 | `equal_sample.py capture` on the named sample of days per master | COO | committed file | n/a |
| R3 | `move_bronze_key_form.py plan` on the LIVE listing: counts per master and type against 21,782 (7,960 + 7,758 + 6,064), and the printed event count | CloudOps | read only | n/a |
| R4 | `copy --apply`, then `verify` (count, size, sha256); window outside the fires (09:45, 10:15, 10:45, 21:45, 22:15, 22:45Z) | CloudOps, repo checkout, its own identity (never on the box) | `s3://opal-data-assets/schwab/<m>/bronze/<feed>/date=...` | old keys untouched until R7; the new keys are inert |
| R5 | push (the pre-push gate deploys `_monolith_bronze.py` to `s3://opal-data-bd/code/`), re-upload `sdd-daily-pull.ps1` to the box code home, deploy the two canonical readers if their headers name a target | MSTR push + CloudOps | as named | redeploy the prior object versions / prior script |
| R6 | `equal_sample.py compare` | COO | committed file | any DIFF stops the cutover before R7 |
| R7 | HELD FOR ANDREW: delete the old keys | Andrew confirms, CloudOps runs | old `schwab/<m>/bronze/<feed>/YYYYMMDD/` | versioning is ON: removal of the delete markers restores every key |
| R8 | FWD-1: pull `08403355`'s oldest served day through the new writer (`-OnlyAsOf <floor> -LookbackDays 1200`, session lock), let the event path convert it, run `thread_trace.py --master 08403355 --day <floor>` | CloudOps + COO | the builder's address | one new partition; delete on Andrew's word |

**THE PUSH IS R5.** A push of `box/laptop` deploys the bd-tree readers (the deploy gate maps `data/black_diamond/scripts/bronze/*.py` to `opal-data-bd`). Pushed before R4, the bd converters would read the new layout from data still in the old one and refuse. So the laptop `Opal box-sync` push is held (requested of `0.0.0_AB_MSTR`) until this lane sends GO naming the change entry.

## 3. Writers of the property (counted at the cut; N printed)

- Schwab bronze key form: 3 writers of the key grammar in code that runs: the daily puller (`sdd-daily-pull.ps1`), the move tool, and the one-time legacy scripts (`remap-bronze-to-monolith.py`, `sdd-backfill-08335338.ps1`, `sdd-history.ps1`, not run, not edited). N = 2 live, 3 dormant.
- Monolith silver for the three masters: 1 writer, the silver converter Lambda `opal-assets-silver-schwab` (S3 event). N = 1.
- Readers of the bronze keys: 31 files in the issuer's census (decomposition), 2 hand-parsers edited, the rest follow the shared function.

## 4. Blast radius (what the acts may touch)

- **Creates:** 21,782 new keys under `schwab/{08242234,08335338,08403355}/bronze/` in the builder's form. Each is an ObjectCreated event, so the silver converter re-runs about 21,782 times and rewrites the same silver partitions (row `NFRA_SCHWABBF-S1`).
- **Moves (served):** the silver partitions of the three masters, rewritten by those invocations; the bd converters' reads (after R5).
- **Does not move:** the other 210 masters (out of scope), the four Cottonwood masters, gold figures unless silver differs (R6 is the check).
- **R7 only:** removes the old keys; nothing else.

## 5. Expected outcome, read from the converter's own rule (both branches)

The converter (`schwab_conversion.py:133-197`) derives master from path segment 1 and type and date from the FILE NAME, and writes silver by those, so a new-form key yields the same partition path.
- **Branch A, rewrite deterministic:** `equal_sample.py compare` prints `EQUAL-OK` (the one excluded column is `_source_file`, which names the new key). Proceed to R7 on Andrew's word.
- **Branch B, rewrite differs** (a figure, a row count or any provenance column other than `_source_file`): `EQUAL-DIFF`. Stop. Do not run R7. Redeploy the prior readers and puller; the old keys are in place; report the diffs to the CTO. The new keys stay, inert, until Andrew rules on them.
- **Unmeasured today:** whether the Lambda is byte-deterministic. R6 answers it.

## 6. Acceptance after the acts

FWD-1: `THREAD-OK master=08403355 day=<floor>` with the bronze at the builder's address and `HOP second-form: NONE` after R7. FWD-4: a census of old-form keys outside R7's scope reads zero. FWD-5: R6's `EQUAL-OK`. FWD-6: the first scheduled fire after R5 lands its day at the builder's address.

## COO half -- VOID (superseded; see the status line)

`2.0.0_SA_COO~SB`, 2026-10-20, was signed for the blast radius in section 4, both branches in section 5, and rollback per act in section 2, on the conditions that `293346aff1` is on origin before R5 and that R7 waits for Andrew's confirmation.

## CTO half -- OWED (`1.0.0_SA_CTO`)
