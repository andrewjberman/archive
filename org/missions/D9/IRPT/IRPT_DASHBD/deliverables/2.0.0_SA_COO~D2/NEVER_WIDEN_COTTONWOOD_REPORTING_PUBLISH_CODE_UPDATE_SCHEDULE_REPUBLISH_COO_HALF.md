# NEVER-WIDEN, COO HALF -- the Cottonwood series publish: code update (writer 0.3.0), the daily schedule created DISABLED, and the republish of the 939 series (IRPT_DASHBD rounds 148 and 149)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-16 ~08:5xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_CODE_UPDATE_SCHEDULE_REPUBLISH.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_CODE_UPDATE_SCHEDULE_REPUBLISH.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_CODE_UPDATE_SCHEDULE_REPUBLISH.md`), sha256 `77f0af99d2bb28cd49344df6cf63494e8185f04d6cc8fff65bf9c4f1f2d501b0`
(computed by this seat on the file; 12,806 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is uploaded, applied or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Six acts, in order. (1) The bundle build and upload of `irpt-cot-reporting-publish-lambda` as a NEW VERSION of its artifact key (base64 sha256 `GagDGBNGmPsmYaJR1B7qG/TvaPdQU3LiVAh6c+wt6jo=` or STOP). (2) ONE `safe-apply` of `reporting-publish-iso`, plan exactly 3 add / 1 change / 0 destroy on the four named addresses (the three schedule resources added DISABLED; the function's code only changed). (3) ONE synchronous DRY-RUN event `{}`. (4) ONE-ACCOUNT republish. (5) the FULL republish of the 939 series under branch E of the first pair (same prefix, same keys). (6) the S104 read. The schedule stays DISABLED throughout.

## 2. What this seat measured and re-ran, and what it did not

- **Live state, read by this seat (read-only):** the function present at the first pair's CodeSha256; the artifact key's current version `9s6sk2dVtf6Ygi2JOGUxtwuiSNXCfKDa`, bucket versioning Enabled on both buckets; NO schedule named `irpt-cot-reporting-publish*`; the target prefix holding 1,878 objects.
- **Re-run by this seat on the landed tree (`e6d44ac5e8`):** the writer criteria `DB155-1-AC1..AC3` (publisher 0.3.0 and the handler on a fake S3), the rename `DB157-1-AC1..AC3`, the schedule `DB156-1-AC1..AC3` (including the real naming gate on the three new names), the re-pin `DB158-1-AC1..AC3` (including the unpacked handler of the build-only package): all PASS. The entry has no stale member at packet time (re-hashed by this seat).
- **Read line by line by this seat:** `schedule.tf` and the appended scheduler block of `iam.tf` (one InvokeFunction statement on the function ARN only; the schedule DISABLED), the handler's `_calendar_source` and guard, the publisher's claim rule.
- **NOT done by anyone:** a `terraform plan` of this root with the schedule resources; any invocation of the new code; the Lambda's calendar source (the manifest will state it).

## 3. Writers of the changed property, counted: N = 1 rule, 2 entry paths (one inert)

One rule writes `irpt/cottonwood/platinum/reporting/` (the handler's `put_object`), entered by a hand invocation and, once ENABLED, by the schedule (DISABLED here). The objects overwritten are the first pair's own 1,878; nothing else lives in the prefix.

## 4. Blast radius, and the limits this half signs under

- Act 1 adds an artifact version. Act 2 creates three resources and replaces the function's code. Act 3 writes nothing. Acts 4 and 5 overwrite objects of an UNREAD prefix at the same keys, new versions each, prior versions kept (versioned bucket). Act 6 reads.
- **Honest limits, signed on:** no plan has run for the schedule resources; the plan's function change is read by attribute at the apply; the Lambda's calendar answer is unrecorded until the manifest states it; no reader of the prefix is established.
- **Not covered:** enabling the schedule; the 49 Financial `reporting-gold` function and the class producer's date; any reader; any delete of any object or version.

## 5. Both branches

Branch A: the events return counts and the after-reads pass. Branch B: an account refuses, is counted by reason and skipped; refusals above 10 percent stop at Act 3. Branch C: a death between an account's series and manifest leaves them mismatched until a re-run. Branch D: out of memory or time stops further writes. Branch E: a repeated run rewrites the same keys. Branch F: a changed refusal count against Act 3 stops Act 5.

## 6. Conditions of this half

0. **Act 1:** the build line equals the packet's or STOP; the prior artifact version recorded. 1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-cottonwood-reporting-publish-codeupdate-20261016`, the applier named; legs git, build, terraform, dry run, canary, republish and S104 read); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, else STOP; the naming gate passes with 0 REFUSE. 3. **The plan read first:** exactly 3/1/0 on the four addresses and the function change by attribute only, else STOP. 4. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id. 5. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version.** 6. **The schedule stays DISABLED.** 7. **The receipt** after Act 6 carries "NOT a page render", "no reader of the prefix established" and "schedule DISABLED".

## 7. The questions, from this seat (the CTO's half decides them)

1. **One packet for the code update, the schedule's three resources and the republish:** ACCEPT as written; the schedule's resources are inert (DISABLED) and the republish sits behind the code update's own dry run and canary.
2. **The republish overwrites 1,878 objects of an unread prefix, prior versions kept:** ACCEPT under branch E with the rollback of the packet's section 7.
3. **The enable is a separate pair:** CONFIRM.

-- 2.0.0_SA_COO~D2
