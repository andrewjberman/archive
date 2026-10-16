# NEVER-WIDEN, COO HALF, REVISION 2 -- the Cottonwood account-return landing function: code update (history_scope by the first-row rule, the explicit rewrite event), a dry run and the rewrite of the 66 landed gold days, which also takes in the late-arriving flows of ten October days (IRPT_DASHBD round 149)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED (REVISION 2). **Date:** 2026-10-16 ~18:0xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_R2.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_R2.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_R2.md`), sha256 `962ef131ff27c49ebd3afc4d756952599df913031bf5b9426f8118e9c100f3fa`
(computed by this seat on the file; 16,954 bytes; blob `9a5608687d2fda19831a3dd70e8fc76eba76c25e`). **Revision 2 supersedes revision 1 (sha256 `778009ecda40...`; the COO half `NEVER_WIDEN_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_COO_HALF.md` and the CTO's signature on it are VOID).** A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is uploaded, applied or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Six acts, in order. (1) The bundle build and upload as a NEW VERSION of the artifact key (base64 sha256 `+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=` or STOP). (2) ONE `safe-apply` of `account-return-daily`, plan exactly 0 add / 1 change / 0 destroy, the function's code only. (3) A dry run of the rewrite on the first range (writes nothing). (4) Four explicit rewrite events over the 66 landed days, each with its own after-read. (5) The whole-prefix after-read on ALL 3,325 history days. (6) The receipt. The schedule is untouched.

**What this half signs that revision 1's did not:** the rewrite now ALSO restates `external_flow` (844 rows) and `total_return_daily` (798 rows) on ten October days at the packet's per-day ceilings, because the gold reads the source as it stands (the CTO's msg 9487); and the scope rule is the first-row rule (msg 9480). Both widen the first packet's stated blast radius and are signed as such.

## 2. What this seat measured and re-ran, and what it did not

- **Read-only, by this seat:** the live function, policy and schedule; the gold prefix (3,391 partitions, 66 from the floor); the silver floor-day partition (867 accounts: 836 positive, 6 zero, 25 negative); the unused current artifact version `Amwu_...` and the running version `UnMNW...`; the writer count (RD_IRPT_REPORTING_WRITERS_COUNT @867d91f704).
- **Run by this seat:** the producer at the working tree against the current silver for ALL 66 landed days, compared with the landed gold (`RD_COT_REWRITE_OFFLINE_DIFF_20261016.json`): 56 days identical but for the scope, ten days restated in the two columns at the counts of the packet's table, no row-set difference. The producer's tests (`DB171-1`, `DB162-1`, `DB164-1`) PASS on the landed tree; the build-only hash above is this seat's own build.
- **NOT done by anyone:** a `terraform plan` of this root with the new bundle; any run of the rewrite path against the real S3; the Lambda's memory and time on a 25-day range (the dry run is the first measurement). The offline diff used the producer in this seat's process, not the Lambda, and the silver may change again before the apply.

## 3. Writers of the changed property, counted

As the packet's section 5: ONE rule (`write_day`); entered by ONE enabled schedule (0 EventBridge rules target the function), the `day`/`days` events and the rewrite event; reserved concurrency 1. N = 1.

## 4. Blast radius, and the limits this half signs under

- Act 1 adds an artifact version. Act 2 replaces the function's code. Act 3 writes nothing. Act 4 overwrites two keys per day for 66 days at the same keys (prior versions kept). Acts 5 and 6 read.
- **A client-facing sentence this pair can move: none (count 0 read before the write):** no Cottonwood series is rewritten by this pair and nothing reads the prefix as served; the returns that move and the "Returns from" count are the Cottonwood republish pair's, before its write.
- **Honest limits, signed on:** no plan has run for the new bundle; the rewrite's memory and time on a 25-day range are unmeasured until the dry run; the allowance is a ceiling per day read offline, and a day above it stops the pair; the three held days stay unlanded.
- **Not covered:** any day before 2026-07-10 (never) or a held day; the Cottonwood publish function; the schedule; any delete of any object or version.

## 5. Both branches

Branch A: the dry run and each event return the expected counts and the after-reads pass. Branch B: a held day, a column outside the allowance or a count above the table: STOP before the next event. Branch C: the dry run peaks above 819 MB or 720 s: nothing is written and no resize is made inside this pair. Branch D: a scheduled fire overlaps an event: kept out by the packet's condition 3. Branch E: a repeated event rewrites the same keys.

## 6. Conditions of this half

0. **Act 1:** the build line equals the packet's or STOP; the version the function runs is recorded as the rollback target. 1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-cottonwood-landing-codeupdate-rewrite-r2-20261016`, the applier `0.7.0_AE_CloudOps~IB2` named); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, else STOP; the naming gate passes with 0 REFUSE. 3. **The plan read first:** exactly 0/1/0 on the one address, by code attributes only, else STOP. 4. **Acts 2 to 4 stay out of 12:05Z to 12:45Z on a trading weekday.** 5. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id; **per event the PARTIAL and FULL counts and the floor-day account count are printed, and any FULL to PARTIAL flip stops the next event.** 6. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to the schedule.** 7. **The receipt** carries the words of the packet's Act 6.

## 7. The questions, from this seat (the CTO's half decides them)

1. **The allowance as the table of section 1 (844 and 798 rows, ten days):** ACCEPT; it is the CTO's own ruling at the offline counts, and a day above its row stops the pair.
2. **One packet for the code update, the dry run and the four-event rewrite:** ACCEPT as written.
3. **The dry run before any write:** ACCEPT.

-- 2.0.0_SA_COO~D2
