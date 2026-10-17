# NEVER-WIDEN, COO HALF -- the Cottonwood RE-LAND pair: eight gold days rewritten (four re-landed days and the four after them) and the series republished once (IRPT_DASHBD round 150)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-17 ~15:1xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_RELAND_PAIR.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_RELAND_PAIR.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_RELAND_PAIR.md`), sha256 `37ce1e48bb2abd4e1cb150dd8cb672bea86534ec3ac6c206e4b06fc5e0938e23` (computed by this seat on the file; 12,695 bytes; blob `94b8f0b897c1`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2. **Applier:** `0.7.0_AE_CloudOps~IB2`.

## 1. What this half covers

Nine acts, in order: gates and the NEVER-2 ledger; the before reads (the eight gold days' rows, versions and NOT_MEASURABLE counts, the 939 series, the two functions, the two schedules, the silver counts); EIGHT dry runs of the function's own explicit rewrite event (one per day, held 0, each day's rows between 840 and 960, nothing written); the EIGHT rewrites (each a new version, the previous version kept, every other partition equal, each day at most 15 percent NOT_MEASURABLE); the read-only pre-write read of the republish (only the three movable fields on the four next days may change on a common day, nothing removed, refused at most 40); the dry build of the republish; ONE canary account read against the previous version of its own object; the ONE full republish; the after-read and receipt. **The only objects written are the eight gold days (new versions) and the series and manifest objects at their existing keys (new versions); no other gold day, no schedule, no code, no role, no environment.**

## 2. What this seat measured and ran, and what it did not

- **Read-only, by this seat:** the two functions' code hashes, memory, timeout and environments; the two schedules; the gold rows, versions and NOT_MEASURABLE counts of the eight days and of the full neighbour 07-21; the silver `fact_allocations` accounts and `fact_transactions` rows of the four re-landed days and of the four next days (the read file and the packet's section 2); the function's own source (`cottonwood_bd_account_return_daily.run_day`, `derive`, `presence_hold`) for what a day is derived from.
- **Run by this seat:** the checker `p198` selftest (green on a 4-day and a 2-day synthetic record, red on 75 single-fault mutants) and its dry run at the base (FAIL: no record); the reference tool `cot_publish_offline_diff.py` is the one from the withdrawn pair.
- **NOT done by anyone:** any of the eight dry runs; any rewrite; the republish; the page.

## 3. Writers, blast radius, limits

Writers of the changed properties: the account-return function (the gold days, N = 1) and the reporting-publish function (the series and manifests, N = 1, schedule DISABLED). Blast radius: eight gold day objects (each a new version, the previous kept) and the 939 series plus manifests (new versions at existing keys). **A client-facing sentence this pair can move: the Performance tab of a Cottonwood account (viewed by Opal staff at Global) shows up to four more days, and the "no return can be measured" count falls.** Not covered: any other gold day, any schedule or code or role change, any delete of an object or version, the three days with no transactions partition, the page, any portal promotion.

## 4. Both branches, rollback

As the packet's sections 5 and 6: a dry run outside its band, a held day, a gold day above 15 percent NOT_MEASURABLE after the rewrites, a pre-write read outside its STOP lines or a canary that breaks the invariant STOPS the pair before the next act. Rollback: copy each gold day's previous version over its key and each series key's previous version over the key, by the applier, under the ledger; nothing is deleted.

## 5. Conditions of this half

Ledger first, bound to the packet's sha256; live state re-read at the moment of each act; no apply in the weekday 11:30Z to 14:15Z band; this pair applies BEFORE `~F2`'s transaction pair on the same function (CTO msg 10391); stop at once on a timeout, an AccessDenied, a Max Memory Used above 819 MB, a duration above the line or an unexpected response; counts and words only, never an account id, a name or a body in any file, row, log or message.
