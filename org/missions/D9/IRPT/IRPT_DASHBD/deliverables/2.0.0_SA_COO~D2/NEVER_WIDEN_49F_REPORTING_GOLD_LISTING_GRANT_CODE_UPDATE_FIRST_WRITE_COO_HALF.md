# NEVER-WIDEN, COO HALF -- the 49 Financial reporting-gold function: listing grant, code update (history_scope derived), the hop-1 first write, a one-day backfill and the republish (IRPT_DASHBD round 149)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-16 ~13:0xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_49F_REPORTING_GOLD_LISTING_GRANT_CODE_UPDATE_FIRST_WRITE.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_GOLD_LISTING_GRANT_CODE_UPDATE_FIRST_WRITE.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_GOLD_LISTING_GRANT_CODE_UPDATE_FIRST_WRITE.md`), sha256 `d2c27ac2bdc591f38e8b59b4c5d6fd6039a95e4e1906e2b124881be8365d7b16`
(computed by this seat on the file; 13,874 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is uploaded, applied or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Six acts, in order. (1) The bundle build and upload of `irpt-49f-reporting-gold-lambda` as a NEW VERSION of its artifact key (base64 sha256 `JNTOivgNaJ8spRxoXSkXAYWhf1cLqXr350sTpH5ADg4=` or STOP). (2) ONE `safe-apply` of `reporting-gold`, plan exactly 0 add / 2 change / 0 destroy: the role policy's one list pattern and the function's code. (3) ONE hand event `{"day": "2026-10-15"}`: the hop-1 first write of ONE filled partition at an empty prefix. (4) A ONE-DAY backfill of 2026-10-15. (5) The republish of the 6,949 series, not before the earlier publish pair's ledger is CLOSED. (6) The receipt. Both schedules are untouched.

## 2. What this seat measured and re-ran, and what it did not

- **Live state, read by this seat (read-only):** the function at CodeSha256 `jz6fRzL52EaI+3ZBI5cWHuDuGwiBDM/S5DPX/CmjeaM=`, 8,192 MB, 900 s; the role policy's eleven statement ids; the schedule ENABLED at 07:41 New York on weekdays; the gold tables (572 returns days to 2026-10-15; class and activity 7 days; `filled_report_values` 0).
- **Re-run by this seat on the landed tree:** the producers `DB162-1-AC1..AC3`, the publisher `DB163-1-AC1..AC3`, the re-pin `DB165-1-AC1..AC3` and the listing grant `DB167-1-AC1..AC3`: all PASS; the build-only hash above is this seat's own build.
- **Read-only census, counts only** (`reads/RD_GOLD49F_CENSUS_20261016.json`): 2,852 floor-start accounts, 4,097 later, 3 whose newest row is before the last partition.
- **NOT done by anyone:** a `terraform plan` of this root with the policy change; any run of the filled stage past its listing (the first run never got there); the Lambda's memory use on the filled stage's whole-history read; the producer's derived rows against the real S3.

## 3. Writers of the changed property, counted

One rule per property: `filled_write` (the filled prefix), `emit_day` (the returns table), the publish handler's `put_object` (the series), as the packet's section 5 counts.

## 4. Blast radius, and the limits this half signs under

- Act 1 adds an artifact version. Act 2 adds one list pattern to a role policy and replaces the function's code. Act 3 writes one NEW filled partition. Act 4 overwrites one day of five served gold tables at the same keys (prior versions kept). Act 5 overwrites the served series and manifests at the same keys (prior versions kept). Act 6 reads.
- **Honest limits, signed on:** no plan has run for the policy change; the filled stage's whole-history read is unmeasured against the function's memory; the derived `history_scope` reaches the series only for accounts with a row on 2026-10-15, and older gold rows keep the old constant and no claim; the one-day backfill re-emits four tables beyond the returns table for that one day.
- **Not covered:** any other day's rewrite; the Cottonwood side; the schedules; any reader; any delete of any object or version.

## 5. Both branches

Branch A: the events return counts and the after-reads pass. Branch B: the listing is still denied; nothing else is written. Branch C: the filled stage runs out of memory or time; nothing is written. Branch D: Act 4 changes a value column; STOP before Act 5. Branch E: a fire overlaps an act; kept out by the packet's condition 3. Branch F: a repeated act rewrites the same keys.

## 6. Conditions of this half

0. **Act 1:** the build line equals the packet's or STOP; the prior artifact version recorded. 1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-49f-reporting-gold-listing-codeupdate-20261016`, the applier named); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, else STOP; the naming gate passes with 0 REFUSE. 3. **The plan read first:** exactly 0/2/0 on the two addresses, the policy change being the one condition value and the function change by code attributes only, else STOP. 4. **Acts 2 to 4 stay out of 11:35Z to 12:00Z on a trading weekday; Act 5 out of 12:05Z to 13:00Z.** 5. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id. 6. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to either schedule.** 7. **The receipt** carries the three phrases of the packet's Act 6.

## 7. The questions, from this seat (the CTO's half decides them)

1. **One packet for the listing grant, the code update, the first write, the one-day backfill and the republish:** ACCEPT as written; each act has its own stop and the grant is one list pattern on the function's own prefix.
2. **A one-day backfill of the newest day in place of a rebuild of 571 days:** ACCEPT; the publisher reads the newest row of each account, and the scheduled fires write derived rows from now on.
3. **The hand event for the first write:** ACCEPT; it writes one partition at an empty prefix, skips a landed day and chains nothing.

-- 2.0.0_SA_COO~D2
