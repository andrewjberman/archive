# NFRA_SCHWABBF -- the 0840 cutover on all three tiers: release plan and the never-widen pair (COO half)

**Issuer:** `2.0.0_SA_COO~SB` (laptop). **Halves:** CTO half = `1.0.0_SA_CTO` (OWED for this act); COO half = this file (SIGNED below, with three conditions).
**Status:** rounds 1-5 built and drained (round 5 closes with this plan); NOTHING DEPLOYED, NOTHING APPLIED, NOTHING MOVED. This plan supersedes `RELEASE_PLAN_R2_FIRM_FORM.md` (three masters, bronze only) and `RELEASE_PLAN_R0_R8.md`.
**Scope (Andrew-direct):** ~16:3xZ "I dont care about that 0824, I want the new Cottonwood accounts taken care of and the 0840 tax sma account sorted out." ~17:0xZ "I found it, its 0840-3355" and "a, yes. this needs to go through the same full bronze/silver process that the other masters go through." So the act moves ONE master, `08403355`, on THREE tiers (bronze, silver, state) in ONE cutover. 0824 (`08242234`) and 0833 (`08335338`) keep their daily pull and today's keys byte for byte. The four Cottonwood masters have no data in the monolith to move; their pull is `2.0.0_SA_COO~SA`'s.
**Earlier Andrew-direct (2026-10-20 ~13:0xZ):** one cutover, same-day rollback, no side-by-side, the old keys deleted only on his confirmation.

## 1. Code and pin

- **Pin:** `27acf60210d` on `box/laptop` (LOCAL at the time of writing; it must be on origin before R5). It carries the merges of rounds 2-5: bronze key function and puller (`8360d83c35`, `24eb435138`), converter, manifest, guard (`3d7a1d172f`), silver (`cdce7d6d13`..`16d4ae3ea0`), state (`4aa5ebc95a1` puller records, `ca13cfdd2d8` move tool, `f27dfcc831e` IAM text, `2b0918008fa` converter family), and the fence rows (`27acf60210d`).
- **Drain evidence (merged tree, 2026-10-20 ~19:5xZ):** `data/canonical/schwab/tests` 845 passed; the converter-side suites and `lib/tests/test_backfill_status.py` pass except 96 failures in `commonwealth_*`/`cotbkf_*` tests of other families (account-set file absent in this checkout; schema drift in a Commonwealth test) that no file of this project touches; `terraform test` (opal_name) 95 passed.
- **Live denominators (move tool `plan --master 08403355`, read-only, 2026-10-20 ~19:5xZ):**

| tier | source | destination | keys | unrecognized | converter events |
|---|---|---|---|---|---|
| bronze | `s3://opal-data-assets/schwab/08403355/bronze/<feed>/YYYYMMDD/` | `s3://opal-data-assets/schwab/49financial/bronze/<feed>/date=D/` | 6,074 | 0 | 6,074 |
| silver | `s3://opal-data-assets/schwab/08403355/silver/<table>/date=D/data.parquet` | `s3://opal-data-assets/schwab/49financial/silver/<table>/date=D/08403355.parquet` | 7,581 (18 tables) | 0 | 0 |
| state | `s3://opal-data-assets/schwab/08403355/{meta,_ops}/...` | `s3://opal-data-49financial/schwab/49financial/state/<table>/date=D/08403355.<name>` | 6,930 (complete 765, conversions 6,101, pulls 31, daily_pull 32, backfill_status 1) | 0 | 0 |
| total | | | **20,585** | **0** | 6,074 |

## 2. The acts, in order (one change-management entry opened before R1; the NFRA CloudOps lane runs every AWS act, rule 34)

| # | act | who | home | rollback |
|---|---|---|---|---|
| R0 | re-read Schwab's served floor for 08403355 (wide `-Mode enumerate`, session lock, outside the fires) | CloudOps on the Schwab box | box `i-0f3d57a97f14727af` | read only |
| R1 | open the change entry naming EVERY family that reads Schwab bronze (one `describe` sweep), the file `_monolith_bronze.py`, and the state readers; confirm the copy identity can read `opal-data-assets` and write `opal-data-assets` (`schwab/49financial/`) and `opal-data-49financial` (`schwab/49financial/state/`) | COO + CloudOps | `org/critical_paths/change_management/` | n/a |
| R2 | `equal_sample.py capture --form old` on the named sample of days (silver, master 08403355) | COO | committed file | n/a |
| R3a | `safe-apply` of the fence rows (`TO-BF-h5`: three scoped exemption rows) in `shared-infra` FIRST (CTO condition) | CloudOps under `safe-apply`, never-widen pair signed | `shared-infra` root | revert the three rows, replan, apply |
| R3b | deploy the converter package (the schwab `OPAL_BUILD_COMMIT` pin in `silver.tf` moves to the pin), then `safe-apply` of the identity text: `opal-assets` (converter read of the firm prefixes, silver write per master, state write, the event rules) and `canonical-schwab-ec2` (box write per master, `MonolithSchwabStateWrite`) | CloudOps under `safe-apply` | `opal-assets`, `canonical-schwab-ec2` | revert the commits and re-apply: old rules and old grants were never removed |
| R3c | the gateway edit in the SAME change window: `completion_prefixes` and `family_depth.py` read the firm form (newest partition at or before today for the rolling objects), fencing by master inside the firm tree | owner `2.0.0_SA_COO~O`, applier `0.7.0_AE_CloudOps~NFRA1` under its own pair | gateway root | prior gateway commit |
| R4a | `move_bronze_key_form.py plan/copy/verify --tier state --master 08403355` (cross-bucket, rename, re-date; count, size, sha256) | CloudOps, repo checkout, its own identity (never on the box) | `s3://opal-data-49financial/schwab/49financial/state/` | the old keys are untouched until R7; the new keys are inert |
| R4b | the same with `--tier silver` | same | `s3://opal-data-assets/schwab/49financial/silver/` | same |
| R4c | the same with `--tier bronze`, LAST, so the 6,074 converter events (silver rebuild, fresh completion markers and conversion manifests) land after the byte copies; window outside the fires (09:45, 10:15, 10:45, 21:45, 22:15, 22:45Z) | same | `s3://opal-data-assets/schwab/49financial/bronze/` | same |
| R5 | push (the pre-push gate deploys `_monolith_bronze.py` to `s3://opal-data-bd/code/`; the entry names it), then re-upload `sdd-daily-pull.ps1` to the box code home AFTER R4a-c verify (a legacy-only file makes the puller's guard exit 6) | MSTR push + CloudOps | as named | redeploy the prior object version / prior script |
| R6 | `equal_sample.py compare --form firm`, and the state spot-compare (the rebuilt marker and manifest of one day against the copied ones) | COO | committed file | any DIFF stops the cutover before R7 |
| R7 | HELD FOR ANDREW: delete the old keys of 08403355 on the three tiers (20,585 keys) | Andrew confirms, CloudOps runs | old `schwab/08403355/{bronze,silver,meta,_ops}/` | versioning is ON: removing the delete markers restores every key |
| R8 | FWD-1: pull `08403355`'s oldest served day through the new writer (`-OnlyAsOf <floor> -LookbackDays 1200`, session lock), the event path converts it, then `thread_trace.py --master 08403355 --day <floor>` | CloudOps + COO | the builder's address | one new partition; delete on Andrew's word |

**Event-order branch (carried from the round-2 plan, re-chosen here).** Converter and event rules FIRST (R3b), the bronze copy LAST (R4c). Reason: the same event path converts the FWD-1 day at R8, and the bronze copy then doubles as the rebuild whose result R6 compares. Cost, stated: the copy fires the converter 6,074 times, each rewriting the same new-form silver partition and writing a conversion manifest and a completion marker to the state tier. Other branch (bronze copy before the rules): converts nothing, so R6 would compare unchanged silver and prove nothing about the new path; rejected.
**The CTO's condition (msg 109991):** within the one window the fence applies first (R3a), then the converter deploy (R3b), then the puller upload (R5).
**THE PUSH IS R5, and the deploy gate holds `_monolith_bronze.py` until an OPEN change entry names it.** I open the entry at R1 and name the file there; before then nothing deploys.

## 3. Writers of the property (counted at the cut)

- Schwab bronze keys of 08403355 in the firm form: the puller and the move tool. N = 2 live. The one-time legacy scripts are dormant (not edited).
- Silver of 08403355: the converter Lambda `opal-assets-silver-schwab` (S3 event) and the move tool's silver copy. N = 2 (the converter's rebuild wins last by the R4c order).
- State of 08403355 in the firm bucket: the puller (`pulls`, `daily_pull`), the converter (`complete`, `conversions`, `backfill_status`), the move tool. N = 3.
- Readers: key-function mirrors, the two hand-parsing readers, the converter set, the trace, the gateway (R3c).

## 4. Blast radius (what the acts may touch)

- **Creates:** 6,074 + 7,581 keys in `opal-data-assets` under `schwab/49financial/` and 6,930 keys in `opal-data-49financial` under `schwab/49financial/state/`; 6,074 converter runs.
- **Changes (cloud):** the converter package and pin; the three fence rows (two principals, two buckets); the box role's per-master write entries and `MonolithSchwabStateWrite`; the converter role's read of the firm prefixes, silver write and state write; the bucket notification gains the firm-prefix rules; the gateway read path.
- **Moves (served):** 08403355's silver partitions (rewritten by the rebuild, expected identical except `_source_file`); the bd converters' reads after R5; the gateway's reads after R3c.
- **Does not move:** 08242234 and 08335338 (keys, grants, state), the other 210 masters, the four Cottonwood masters, gold figures unless silver differs.
- **R7 only:** removes the old keys of 08403355; nothing else.

## 5. Expected outcome, read from the converter's own rule (both branches)

The converter takes the master from the file name and writes silver to `<master>.parquet` and state to the firm bucket for the five firm-form masters (the shared backfill-status writer switches only for them; a test proves every other family byte for byte).
- **Branch A, rewrite deterministic:** `equal_sample.py compare --form firm` prints `EQUAL-OK` (the single excluded column is `_source_file`). Proceed to R7 on Andrew's word, then R8.
- **Branch B, rewrite differs:** `EQUAL-DIFF`. Stop before R7. Rollback: Terraform revert (rules, grants, fence rows), redeploy the prior converter pin, gateway and readers; the old keys are in place; the new keys stay, inert. Report to the CTO.
- **Unmeasured today:** whether the converter is byte-deterministic on a firm-form key; R6 answers it.

## 6. Acceptance after the acts

FWD-1: `THREAD-OK master=08403355 day=<floor>` with bronze, silver and state at the builder's address and `HOP second-form: NONE` after R7. FWD-4: the move tool's plan on each tier reads `copy=0 already=N`. FWD-5: R6's `EQUAL-OK`. FWD-6: the first scheduled fire after R5 lands its day and its run records at the builder's address and the guard reads `ok=True`; the gateway's completion read finds the day.

## COO half -- SIGNED

`2.0.0_SA_COO~SB`, 2026-10-20: signed for the blast radius in section 4, both branches in section 5 and the rollback per act in section 2, on three conditions: (1) the pin is on origin before R5; (2) R3a, R3b and R5 run in the CTO's order inside one window (msg 109991); (3) the gateway side (R3c) has its own signed pair and the same window before R4c, since the bronze copy is the first act that makes the new form visible to readers.

## CTO half -- OWED (`1.0.0_SA_CTO`)
