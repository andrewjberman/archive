# NFRA_SCHWABBF round 2 -- release plan on the FIRM form, and the never-widen pair (COO half)

**Issuer:** `2.0.0_SA_COO~SB` (laptop). **Halves:** CTO half = `1.0.0_SA_CTO` (OWED); COO half = this file (SIGNED below, with two conditions).
**Status:** all eight round-2 cells merged and drained; NOTHING DEPLOYED, NOTHING APPLIED, NOTHING MOVED. This plan re-cuts round 1's R0-R8 on the firm form (`RELEASE_PLAN_R0_R8.md` is superseded).
**Andrew-direct:** 2026-10-20 ~13:0xZ call 2 ("Yes, rec is accurate": one cutover, same-day rollback, no side-by-side, the old keys deleted only on his confirmation) and ~14:3xZ ("abiding by the path structure that already exists in that bucket ... schwab vendor and 49 firm for the 0840 and cottonwood firm").

## 1. Code and pin

- **Pin:** `3d7a1d172f` on `box/laptop` (LOCAL at the time of writing; it must be on origin before R5). It carries the round-2 merges: `87d44e203b` (restore), `8360d83c35` (puller), `e26bd321b2` (trace), `95b30c139f` (IAM text, event rules, converter read), `ef38445985` (key function, move tool, readers), `3d7a1d172f` (converter, manifest, guard, census, twins).
- **Drain evidence (merged tree, 2026-10-20 ~16:0xZ):** `data/canonical/schwab/tests` 640 passed; the five converter-side test files 122 passed; `py_compile` clean on 11 files; the four vendored twins byte-equal to their sources. Live read-only: the move plan on the real prefixes (below).
- **Live denominators (move tool `plan --master M`, read-only, 2026-10-20 ~16:0xZ):**

| master | keys listed | plannable | unrecognized |
|---|---|---|---|
| 08242234 | 7,970 | 6,725 | **1,245** |
| 08335338 | 7,769 | 7,769 | 0 |
| 08403355 | 6,074 | 6,074 | 0 |
| total | **21,813** (the brief measured 21,782; 31 new days since) | **20,568** | **1,245** |

- **The 1,245 unrecognized keys are a DECISION, not a cell** (slug section 3): names `CRS{YYYYMMDD}.{FEED}` with no master prefix and no `.zip`, 241 dates from 2023-01-17 to 2024-07-05, all under 0824, dated BEFORE Schwab's served floor (2023-10-17) for 2023-01-17..2023-10-16, so irreplaceable. They fire no converter event (suffix is not `.zip`). R4 does not move them until the CTO rules.

## 2. The acts, in order (one change-management entry opened before R1; the NFRA CloudOps lane runs every AWS act, rule 34)

| # | act | who | home | rollback |
|---|---|---|---|---|
| R0 | re-read Schwab's served floor per master (wide `-Mode enumerate`, session lock, outside the fires) | CloudOps on the Schwab box | box `i-0f3d57a97f14727af` | read only |
| R1 | open the change entry naming EVERY family that reads Schwab bronze (one `describe` sweep); confirm the copy identity's Get/Put on `schwab/<m>/bronze/*` and `schwab/49financial/bronze/*` | COO + CloudOps | `org/critical_paths/change_management/` | n/a |
| R2 | `equal_sample.py capture` on the named sample of days per master (silver, by master) | COO | committed file | n/a |
| R3 | deploy the converter package (Terraform: the schwab `OPAL_BUILD_COMMIT` pin in `silver.tf` moves to the merge that carries `BF-c-2`; row W5-S5), then `safe-apply` of `BF-i-2` (box write statements per master, converter read of the firm prefixes, the two event rules) | CloudOps under `safe-apply` | `opal-assets` and `canonical-schwab-ec2` roots | revert the Terraform commit and re-apply: the three old rules and old grants were never removed |
| R4 | `move_bronze_key_form.py plan` on the LIVE listing, then `copy --apply` (concurrency 8) and `verify` (count, size, sha256); window outside the fires (09:45, 10:15, 10:45, 21:45, 22:15, 22:45Z) | CloudOps, repo checkout, its own identity (never on the box) | `s3://opal-data-assets/schwab/49financial/bronze/<feed>/date=.../<master>.*` | old keys untouched until R7; the new keys are inert |
| R5 | push (the pre-push gate deploys `_monolith_bronze.py` to `s3://opal-data-bd/code/`; the entry names it), then re-upload `sdd-daily-pull.ps1` to the box code home AFTER R4 verifies (row W3-S3: a legacy-only file makes the puller's guard exit 6) | MSTR push + CloudOps | as named | redeploy the prior object version / prior script |
| R6 | `equal_sample.py compare` | COO | committed file | any DIFF stops the cutover before R7 |
| R7 | HELD FOR ANDREW: delete the old keys (the 20,568 plannable old-form keys) | Andrew confirms, CloudOps runs | old `schwab/<m>/bronze/<feed>/YYYYMMDD/` | versioning is ON: removing the delete markers restores every key |
| R8 | FWD-1: pull `08403355`'s oldest served day through the new writer (`-OnlyAsOf <floor> -LookbackDays 1200`, session lock), the event path converts it, then `thread_trace.py --master 08403355 --day <floor>` | CloudOps + COO | the builder's address | one new partition; delete on Andrew's word |

**Event-order branch (CTO analysis, ruling 1: the cutover cell's choice, made here).** Chosen: converter and event rules FIRST (R3), then the copy (R4). Reason: the same event path converts the FWD-1 day at R8; and the copy then doubles as the rebuild whose result R6 compares.
Cost, stated: the copy fires the converter about 20,568 times, each rewriting the same silver partition.
Other branch (copy before the rules): converts nothing, so R6 would compare unchanged silver and prove nothing about the new path; rejected.

**THE PUSH IS R5, and the deploy gate holds `_monolith_bronze.py` until an OPEN change entry names it (MSTR's read, 2026-10-20 ~14:4xZ).** I open the entry at R1 and name the file there; before then nothing deploys.

## 3. Writers of the property (counted at the cut)

- Schwab bronze keys in the firm form: the puller (`sdd-daily-pull.ps1`) and the move tool. N = 2 live; the one-time legacy scripts (`remap-bronze-to-monolith.py`, `sdd-backfill-08335338.ps1`, `sdd-history.ps1`) are dormant and write the OLD form (not edited; round 3).
- Monolith silver for the three masters: 1 writer, the silver converter Lambda `opal-assets-silver-schwab` (S3 event). N = 1.
- Readers of the bronze keys: the key-function mirrors, the two hand-parsing readers, the converter set (scope function, conversion manifest, set-identity guard, runtime census), the trace. The silver and gold figures downstream are read by master from silver and do not move unless R6 shows a diff.

## 4. Blast radius (what the acts may touch)

- **Creates:** 20,568 new keys under `schwab/49financial/bronze/` (not the 1,245 unprefixed 0824 objects). Each is an ObjectCreated event: about 20,568 converter runs rewriting the same silver partitions of the three masters.
- **Changes (cloud):** the converter package and its build pin; the box role gains per-master write entries and a prefix-list entry on `schwab/49financial/bronze/`; the converter role gains read on the two firm prefixes; the bucket notification gains two rules (the singleton, additive).
- **Moves (served):** silver partitions of the three masters (rewritten, expected byte-identical except the provenance column `_source_file`); the bd converters' reads after R5.
- **Does not move:** the other 210 masters, the four Cottonwood masters (their write grant is the Alongside role's), gold figures unless silver differs.
- **R7 only:** removes the old keys; nothing else.

## 5. Expected outcome, read from the converter's own rule (both branches)

The converter now takes the master from the file name and the type and date from the file name too; its set-identity guard and manifest filter the shared folder by the master's file-name prefix (all tested, 122 passed).
- **Branch A, rewrite deterministic:** `equal_sample.py compare` prints `EQUAL-OK` (the single excluded column is `_source_file`, which names the new key). Proceed to R7 on Andrew's word, then R8.
- **Branch B, rewrite differs:** `EQUAL-DIFF` on any figure, row count or provenance column other than `_source_file`. Stop before R7. Rollback: Terraform revert (the event rules and grants), redeploy the prior converter pin and readers; the old keys are in place; the new keys stay, inert. Report the diffs to the CTO.
- **Unmeasured today:** whether the converter is byte-deterministic on a firm-form key. R6 answers it.

## 6. Acceptance after the acts

FWD-1: `THREAD-OK master=08403355 day=<floor>` with the bronze at the builder's address and `HOP second-form: NONE` after R7. FWD-4: the move tool's plan on the live listing reads `copy=0 already=N` and the old-form count is zero (the 1,245 per the CTO's ruling). FWD-5: R6's `EQUAL-OK`. FWD-6: the first scheduled fire after R5 lands its day at the builder's address and the guard reads `ok=True`.

## COO half -- SIGNED

`2.0.0_SA_COO~SB`, 2026-10-20: signed for the blast radius in section 4, both branches in section 5 and the rollback per act in section 2, on two conditions: (1) `3d7a1d172f` is on origin before R5; (2) the CTO rules on the 1,245 unprefixed objects (slug section 3) before R4, since R4's plan prints them as unrecognized and R7's delete must not leave a second form unexplained.

## CTO half -- OWED (`1.0.0_SA_CTO`)
