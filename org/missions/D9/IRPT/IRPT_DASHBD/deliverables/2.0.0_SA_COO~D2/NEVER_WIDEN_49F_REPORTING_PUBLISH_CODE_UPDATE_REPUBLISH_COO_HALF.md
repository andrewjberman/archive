# NEVER-WIDEN, COO HALF -- the 49 Financial series publish: code update (publisher 0.4.0) and the republish of the 6,949 series (IRPT_DASHBD rounds 148 and 149)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-16 ~11:5xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_CODE_UPDATE_REPUBLISH.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_CODE_UPDATE_REPUBLISH.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_CODE_UPDATE_REPUBLISH.md`), sha256 `29b7df738efcc7b070fde732fc34f88c77a75ea034e1d107545fc789292b5449`
(computed by this seat on the file; 13,774 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is uploaded, applied or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Six acts, in order. (1) The bundle build and upload of `irpt-49f-reporting-publish-lambda` as a NEW VERSION of its artifact key (base64 sha256 `SX0xYFZsxH4q6psJM56yAee9wRb6vrVUN4VrTV1ouU8=` or STOP). (2) ONE `safe-apply` of `reporting-publish`, plan exactly 0 add / 1 change / 0 destroy, the function's code only. (3) ONE synchronous DRY-RUN event on ONE shard, writing nothing. (4) ONE-ACCOUNT republish. (5) the FULL republish of the 6,949 series (7 shard invocations; the same keys). (6) the receipt. The daily schedule is neither read for change nor touched.

## 2. What this seat measured and re-ran, and what it did not

- **Live state, read by this seat (read-only):** the function present at CodeSha256 `AH5r60vpxR/Gt4RlpsSkhAw5HDths5P2Ht+Ix1CHlQ8=`, 1,024 MB, 300 s, one layer, no environment; the artifact key's current version `4kEV9O.UMGs.NSGSYi_N4ZZjNm45rso4`; the schedule ENABLED at 08:15 New York on weekdays; the prefix holding 6,949 series, 6,949 manifests and 4,344 other objects, versioning Enabled.
- **Re-run by this seat on the landed tree:** the writer and handler criteria `DB160-1-AC1..AC3` (the 49 Financial handler on a fake S3, the entry, the build-only package and the UNPACKED handler), `DB163-1-AC1..AC3` (publisher 0.4.0 and both handlers) and the contract criteria `DB161-1-AC1..AC3`: all PASS.
- **Measured, counts only (`reads/RD_GOLD49F_CENSUS_20261016.json`):** 571 partitions, 6,949 accounts, no account with income null on some days and a number on others, so the refusal rule the new publisher adds refuses none.
- **NOT done by anyone:** a `terraform plan` of this root with the new artifact version; any invocation of the new code against the 49 Financial gold; the Lambda's calendar source (the manifest will state it); the page's reading of the explicit empty list.

## 3. Writers of the changed property, counted: N = 1 rule, 3 entry paths

One rule writes the series and manifest objects (the handler's `put_object` in `_publish_one`), entered by a hand invocation, by the ENABLED daily schedule and by the shard fan-out of either. The summaries pass writes a different object kind and is not run.

## 4. Blast radius, and the limits this half signs under

- Act 1 adds an artifact version. Act 2 replaces the function's code. Act 3 writes nothing. Acts 4 and 5 overwrite served objects at the same keys, new versions each, prior versions kept (versioned bucket). Act 6 reads.
- **Honest limits, signed on:** no plan has run for this change; the plan's function change is read by attribute at the apply; the calendar answer is unrecorded until the manifest states it; the series are READ by the page today, so Acts 4 and 5 move served bytes (an added key and an added manifest key, nothing removed); the history-scope pair does not arrive until the gold is rebuilt (a separate pair).
- **Not covered:** the `reporting-gold` code update and the gold rebuild; the summaries pass; the schedule; the Cottonwood side; any reader; any delete of any object or version.

## 5. Both branches

Branch A: the events return counts and the after-reads pass. Branch B: an account refuses, is counted, keeps its prior objects, and any refusal STOPS Act 5. Branch C: a shard dies between an account's series and manifest; the next republish rewrites both. Branch D: a shard runs out of memory or time; nothing further is written by it. Branch E: a repeated run rewrites the same keys. Branch F: the scheduled fire overlaps Act 2; kept out by the packet's condition 3. Branch G: the new code refuses an account the old accepted; a count that differs from Act 3's STOPS Act 5.

## 6. Conditions of this half

0. **Act 1:** the build line equals the packet's or STOP; the prior artifact version recorded. 1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-49f-reporting-publish-codeupdate-20261016`, the applier named; legs git, build, terraform, dry run, canary, republish); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, else STOP; the naming gate passes with 0 REFUSE. 3. **The plan read first:** exactly 0/1/0 on the one address and the change by attribute only, else STOP. 4. **Act 2 stays out of 12:05Z to 13:00Z on a trading weekday.** 5. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id. 6. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to the schedule.** 7. **The receipt** after Act 6 carries "NOT a page render", "no reader of the unreported-days statement is established" and "history scope NOT yet derived: the gold is rebuilt by a separate pair".

## 7. The questions, from this seat (the CTO's half decides them)

1. **One packet for the code update and the republish:** ACCEPT as written; no resource is added and the republish sits behind its own dry run and canary.
2. **The republish overwrites 13,898 served objects, prior versions kept:** ACCEPT under branch E with the rollback of the packet's section 7.
3. **The history scope arrives with the gold rebuild, in a later republish:** ACCEPT the order (these series carry the unreported-days statement now, the scope later); the alternative, holding this republish until the gold is rebuilt, delays the CTO's ruling of msg 9224 by a whole pair.

-- 2.0.0_SA_COO~D2
