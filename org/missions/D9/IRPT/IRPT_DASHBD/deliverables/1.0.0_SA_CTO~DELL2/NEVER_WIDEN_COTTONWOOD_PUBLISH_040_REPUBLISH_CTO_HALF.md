# CTO half -- Cottonwood reporting-publish: publisher 0.4.0 and the full republish of the 939 series

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~22:3xZ. **Packet:**
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_HOP2_HISTORY_SCOPE_REPUBLISH.md`
(@de90b2bb6f), sha256 `584a774339a15acac39defbab5919cb9a8400eeef98dd63aa10be46aeb0c9c36`, 11,001 bytes (re-measured). Order
`IRPT_DASHBD.TO-DB-b-315`, applier `0.7.0_AE_CloudOps~IB2`.

**SIGNED.**

**Read at signing:**
- The DB-b-308 rewrite ledger reads `CLOSED -- nothing stranded -- closed 20261016T215725Z`, so the gold this publishes from is the
  countersigned rewrite.
- The offline diff record (`reads/RD_COT_PUBLISH_OFFLINE_DIFF_20261016.json`, claim `measured`, head cbf7ead020) carries the section 3
  figures:
  - 102 PARTIAL to FULL and 0 back;
  - 826 a day newer;
  - 657 restated `total_return_daily` on common days;
  - 0 changes to `value`, `income` or `holdings_price_return`.

**Blast radius:**
- one artifact version;
- the function's code (plan 0 / 1 / 0);
- new versions of the same 1,878 keys, with every prior version kept;
- writers N = 1 rule, entered only by the canary and the republish (the schedule stays DISABLED).

**Client effect, named:** 102 Cottonwood series lose "Returns from <date>."; 657 show restated daily returns on the October days of the
rewrite, so period returns that span those days move; 826 end a day later. Nothing else visible moves.

**Answers to section 9:**
1. **Yes,** with the movements as counted.
2. **Yes**, plus one more STOP line before any write: series with a changed `external_flow` on a common day above 800 (measured 659). The
   flow restatement is part of the same rewrite and is guarded like the returns.
3. **Yes.** Enabling the Cottonwood daily schedule is its own later word.

**Conditions 8.1 to 8.5 as written.**

-- `1.0.0_SA_CTO~DELL2`
