# NEVER-WIDEN, COO HALF -- the Cottonwood account-return landing function: code update (history_scope derived, the explicit rewrite event), a dry run and the rewrite of the 66 landed gold days (IRPT_DASHBD round 149)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-16 ~14:0xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE.md`), sha256 `778009ecda403f17f2eb81163507e6ca9f1738dfa3417735bb6cf4b8e4d5aeaf`
(computed by this seat on the file; 13,345 bytes; blob `05b8884c840de0dfcdc3e8a005c2264a29fe0b69`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is uploaded, applied or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Six acts, in order. (1) The bundle build and upload of `irpt-cot-account-return-daily-lambda` as a NEW VERSION of its artifact key (base64 sha256 `FH4+ZDunLNxCc2pb03bx9U10iAcmQQrvYPaBx5xnjew=` or STOP). (2) ONE `safe-apply` of `account-return-daily`, plan exactly 0 add / 1 change / 0 destroy, the function's code only. (3) A dry run of the rewrite on the first range (derives, writes nothing). (4) Four explicit rewrite events over the 66 landed days, oldest first, each with its own after-read. (5) The whole-prefix after-read. (6) The receipt. The schedule is untouched.

## 2. What this seat measured and re-ran, and what it did not

- **Live state, read by this seat (read-only):** the function at CodeSha256 `fQFe4moIeMHspIjLxO2C04TobQW6cNZc7mfwstcMWzs=`, 1,024 MB, timeout 900, reserved concurrency 1, the one layer; the five-statement execution policy; the schedule ENABLED at 08:15 New York on weekdays; the gold prefix at 3,391 `date=` partitions to 2026-10-15, 66 of them from the floor 2026-07-10; the three trading days without a partition (2026-08-19, 2026-09-24, 2026-09-25), explained by the adapter's `presence_hold` (row `IRPT_DASHBD-D2-S122`).
- **Re-run by this seat on the current tree (c2b2f1e950 or later):** the producers `DB162-1-AC1..AC3` and the rewrite event `DB164-1-AC1..AC3`: all PASS. The re-pin criteria `DB165-1-AC1..AC3` pass at their drain (7f54bece4e) and now FAIL by design: they hold the entries outside their order to the drain's base, and `DB-b-298`'s upload legitimately changed the 49 Financial publish entry's `artifact_sha256` (message: "an entry outside the order changed: irpt-49f-reporting-publish-lambda"). In their place this seat compared this entry's 15 staged pins to the working tree by sha256: 14 equal, and the calendar member is pinned at its older, functionally equal content. The build-only hash above is this seat's own build.
- **NOT done by anyone:** a `terraform plan` of this root with the new bundle; any run of the rewrite path against the real S3; the Lambda's memory and time on a 25-day range (the dry run is the first measurement); the producer's derived rows against the real silver.

## 3. Writers of the changed property, counted

One rule per property: `write_day` writes the gold partition keys (two `put_object` calls); it is entered by the scheduled fire, the `day`/`days` events and the rewrite event, as the packet's section 5 counts. N = 1.

## 4. Blast radius, and the limits this half signs under

- Act 1 adds an artifact version. Act 2 replaces the function's code. Act 3 writes nothing. Act 4 overwrites two keys per day for 66 days at the same keys (prior versions kept). Acts 5 and 6 read.
- **Honest limits, signed on:** no plan has run for the new bundle; the rewrite's memory and time on a 25-day range are unmeasured until the dry run; the derived rows have not met the real silver; the three held days stay unlanded; the Cottonwood series stay on the old value until the publish pair.
- **Not covered:** any day before 2026-07-10 (never) or a held day; the Cottonwood publish function; the schedule; any delete of any object or version.

## 5. Both branches

Branch A: the dry run and each event return the expected counts and the after-reads pass. Branch B: a day is held or a value column differs: STOP before the next event. Branch C: the dry run peaks above 819 MB or 720 s: nothing is written and no resize is made inside this pair. Branch D: a scheduled fire overlaps an event: kept out by the packet's condition 3. Branch E: a repeated event rewrites the same keys.

## 6. Conditions of this half

0. **Act 1:** the build line equals the packet's or STOP; the prior artifact version recorded. 1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-cottonwood-landing-codeupdate-rewrite-20261016`, the applier named); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, else STOP; the naming gate passes with 0 REFUSE. 3. **The plan read first:** exactly 0/1/0 on the one address, by code attributes only, else STOP. 4. **Acts 2 to 4 stay out of 12:05Z to 12:45Z on a trading weekday.** 5. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id. 6. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to the schedule.** 7. **The receipt** carries the three phrases of the packet's Act 6.

## 7. The questions, from this seat (the CTO's half decides them)

1. **One packet for the code update, the dry run and the four-event rewrite:** ACCEPT as written; each act has its own stop and the dry run precedes every write.
2. **The three held days stay unlanded:** ACCEPT; it is the adapter's rule, and changing it is its own ruling.
3. **The dry-run event as the measurement:** ACCEPT; the handler's `dry_run` derives and writes nothing.

-- 2.0.0_SA_COO~D2
