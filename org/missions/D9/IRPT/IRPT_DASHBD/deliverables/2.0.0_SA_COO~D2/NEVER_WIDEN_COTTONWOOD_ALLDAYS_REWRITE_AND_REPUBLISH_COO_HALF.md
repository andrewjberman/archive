# NEVER-WIDEN, COO HALF -- the Cottonwood ALL-DAYS rewrite pair: every landed gold day from 2026-07-10 rewritten with the corrected reader (four events of landed trading days) and the series republished once (IRPT_DASHBD round 150)

**Signer:** 2.0.0_SA_COO~D2. **Status:** READY, NOT YET SIGNED. This seat flips the line below to SIGNED in one commit the moment the corrected reader's first scheduled fire reads clean (CTO msg 10877); until then this file binds nothing. **Date prepared:** 2026-10-19 ~18:3xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_ALLDAYS_REWRITE_AND_REPUBLISH.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_ALLDAYS_REWRITE_AND_REPUBLISH.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_ALLDAYS_REWRITE_AND_REPUBLISH.md`), sha256 `1439a74f417e3de33fa5a7e4f909c8fd4a8dc44a6cc5b800e7815d47605e338e` (computed by this seat on the file; 14,987 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2. **Applier:** `0.7.0_AE_CloudOps~IB2`.

**THE SIGNING LINE (flips from READY to SIGNED, with the clean-fire read cited):** READY, NOT YET SIGNED.

## 1. What this half covers

Ten acts, in order: gates and the NEVER-2 ledger (including that the corrected reader is on the function and its first scheduled fire read clean); the before reads (every landed gold day's rows, versions, NOT_MEASURABLE and absolute-flow counts, the 939 series, the function, the two schedules); the scaling dry run of ONE day and the dry runs of the four events (held 0, each day's rows within 2 percent of the issuer's committed dry derivation, nothing written); the rewrites (each day a new version, previous versions kept, every other partition equal, each day at most 15 percent NOT_MEASURABLE except the floor day 2026-07-10, the daily absolute flows no higher than before on every day whose rows did not change); the read-only pre-write read of the republish; the dry build of the republish; ONE canary account read against the previous version of its own object; the ONE full republish; the after-read and receipt. **The only objects written are the landed gold days (new versions) and the series and manifest objects at their existing keys (new versions); no other gold day, no schedule, no code, no role, no environment.**

## 2. What this seat measured and ran, and what it did not

- **Read-only, by this seat:** the derivation of all 66 landed days with the corrected reader against the landed gold (`reads/RD_COT_ALLDAYS_DRY_20261017.json`: 61 of 66 days show summed absolute flows more than double the corrected derivation, up to 14 times; five days differ in row count; the four days after the re-landed days fall from 83 to 100 percent to under 15 percent NOT_MEASURABLE); the census of landed days and the four events (`reads/RD_COT_ALLDAYS_STATE_20261017.json`); the object versions of the eight earlier day keys (2 each, none written since 2026-10-17T15:00:54Z).
- **Run by this seat:** the apply checker `p201` selftest (green on a synthetic record, red on 89 single-fault mutants) and its dry run at the base (all three criteria FAIL: no record).
- **NOT done by anyone:** the deploy of the corrected reader; any dry run on the function; any rewrite; the republish; the page.

## 3. Writers, blast radius, limits

Writers of the changed properties: the account-return function (the gold days, N = 1) and the reporting-publish function (the series and manifests, N = 1, schedule DISABLED, re-read). Blast radius: the landed gold day objects (each a new version, the previous kept) and the 939 series plus manifests (new versions at existing keys). **A client-facing sentence this pair moves: on the Performance tab of a Cottonwood account the daily returns AND the daily flow entries CHANGE on every day that had an external flow (the flows stop being summed across overlapping transaction partitions), four days gain rows, and the four days after the re-landed days become measured; the YTD return still reads Not measured while any of 08-19, 09-24 or 09-25 is in the window.** Not covered: any other gold day, any schedule or code or role change, any delete of an object or version, the three days with no transactions partition, the page, any portal promotion.

## 4. Both branches, rollback

As the packet's sections 5 and 6: a dry run outside its band, a held day, a gold day above 15 percent NOT_MEASURABLE after the rewrites (the floor day excepted), a flow sum that rose on a day whose rows did not change, a pre-write read outside its STOP lines or a canary that breaks the invariant STOPS the pair before the next act. Rollback: copy each gold day's previous version over its key and each series key's previous version over the key, by the applier, under the ledger; nothing is deleted.

## 5. Conditions of this half

Ledger first, bound to the packet's sha256; live state re-read at the moment of each act; no apply in the weekday 11:30Z to 14:15Z band; this pair applies AFTER `~F2`'s release pair and the reader's first clean fire (CTO msgs 10627 and 10877) and only after the CTO releases it from Andrew's pause; stop at once on a timeout, an AccessDenied, a Max Memory Used above 819 MB, a duration above 720 s or an unexpected response; counts and words only, never an account id, a name or a body in any file, row, log or message.
