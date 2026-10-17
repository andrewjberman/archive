# NEVER-WIDEN, COO HALF -- the Cottonwood gold day 2026-07-27 rewritten from the full carrier delivery, and the series republished (IRPT_DASHBD round 150)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-17 ~07:1xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH.md`), sha256 `8596f43f1d0f06ba3944da6640c490c19e8440bc3426ec367f32e550b6b9252e` (computed by this seat on the file; 10,276 bytes; blob `7c6564cc6f41`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2.

## 1. What this half covers

Nine acts, in order: the gates and ledger; the before reads; a DRY RUN of the explicit rewrite event for the one gold day 2026-07-27 (rows between 840 and 920, `held` 0); the rewrite itself (a new version of that day's object; the 3-row version kept); a read-only pre-write diff of the republish (only 2026-07-28's `total_return_daily`, `day_quality` and `return_basis` may change on a common day; the only day added is 2026-07-27; no day removed; refused 0); a dry build of the republish; ONE canary account checked against the previous version of its own object; the full republish of the 939 series; the after-read and receipt. **No code, role, schedule or other gold day changes.** The six other absent days are not touched (dell1's carrier lane owns that pull).

## 2. What this seat measured and ran, and what it did not

- **Read-only, by this seat:** the carrier's landed silver for the seven days and the full-day comparator (the read file @5e3c0c1d92); the gold day's 3 rows against 879 on 2026-07-21; the live configuration of both functions; the handler's `_rewrite` path (it refuses a day before the floor, a day not already landed and more than 25 days, and writes nothing else).
- **NOT done by anyone:** the dry run of this day against the full silver; any republish with the rewritten day; the page.

## 3. Writers, blast radius, limits

Writers of the changed properties: the account-return function (one gold day, N = 1) and the publish function (series and manifests, N = 1, schedule DISABLED). Blast radius: one gold day (a new version), up to 939 series and manifests (new versions at the same keys). **A client-facing sentence this pair can move: a Cottonwood account (viewed by Opal staff) shows one more trading day and one more measured daily return.** Not covered: the six other days, any code, role or schedule change, any delete.

## 4. Both branches, rollback

As the packet's sections 5 and 6: a dry run outside its band, a held day, a pre-write read outside its STOP lines or a canary that breaks the previous-version invariant STOPS the pair before the next act; the rollback is a copy of the kept prior version over the key (a write under the ledger), never a delete.

## 5. Conditions of this half

Ledger first, bound to the packet's sha256; live state re-read at the moment of each act; no act in a weekday fire window (12:05 to 13:15 UTC); stop at once on a timeout, an AccessDenied or a memory or duration line above the packet's; counts and words only, never an account id, a name or a body.
