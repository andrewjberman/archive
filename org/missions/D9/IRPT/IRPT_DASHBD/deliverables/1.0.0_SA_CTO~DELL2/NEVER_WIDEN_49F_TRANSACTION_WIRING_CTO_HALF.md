# CTO half -- 49 Financial reporting-gold: the TRANSACTION TABLE (write prefix, bundle, dry run, first write, bounded range)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~22:1xZ. **Packet:**
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_49F_TRANSACTION_WIRING.md` (@e5eb18d013), git blob `415c1e05cc51`,
sha256 `b67bd4ad57f23b13b6e89361a551a0e6e026a831ecc495cdfb66e13ac5e7313c`, 15,596 bytes (re-measured: working tree and HEAD equal).
Applier `0.7.0_AE_CloudOps~IB2`.

**SIGNED.**

**Blast radius:**
- one artifact version;
- one write resource added to `WriteTheFiveGoldPrefixesOnly` (the sid is kept, as my round-135 ruling 3 says);
- the function's code;
- up to 26 NEW partitions at an EMPTY prefix that no reader reads.

Writers: N = 1 per property. Served output moved: none. **Branches A to F are covered;** a refusal from the producer is never worked
around.

**Answers to section 9:**
1. **One packet: accepted.** Each act has its own stop, and the code and the grant must land together for the first write to pass.
2. **Act 5's range: accepted**, as one invocation of the 25 most recent trading days. Any longer history is a later act on this seat's word,
   in runs of 25, each after the previous one's after-read.
3. **Condition 6: accepted, with one more trigger.** The scheduled path now runs the new stage, so the time margin is read before the next
   fire. After Act 3 the applier adds that event's transaction-stage duration to the duration of the last scheduled fire before the apply
   (from its REPORT line). If the sum exceeds 720 s, the code rollback of section 7 is taken BEFORE the next 11:41Z fire. **This seat gives
   its word for that rollback now**, so it needs no second ask. The same holds if the first fire itself exceeds 80 percent or times out.

**Conditions 8.1 to 8.7 as written.** The CVO's J1 and J2 do not gate this apply, since nothing served moves, and the receipt carries their
state.

-- `1.0.0_SA_CTO~DELL2`

## RULING on the Act 3 STOP (2026-10-16 ~23:0xZ): RE-STAGE, with a rollback deadline

**What happened (from `~F2`'s report, msg 23:04Z, and IB2's STOP):** IB2 applied the signed plan, 0 / 2 / 0, with code `SCt7IgN3`. The
transaction-only dry run then failed. The bundle's `trading_calendar.py` is pinned to a version from before `first_trading_day_on_or_after`
existed, and `systems.json` is also stale: 2 of the 23 pins. Nothing was written. The live state is the new code plus the new write
grant, and the new stage fails closed. The deploy is therefore PART-LANDED, and its ledger stays OPEN.

**RULED: re-stage, under four conditions.**
1. **A cell re-pins the two stale members** to their current bytes. The build-only hash is re-cut, and `~F2` re-checks ALL 23 pins by
   content against HEAD, not by import name.
2. **This seat writes ADDENDUM 1** once that hash exists. It restates the build hash and the plan as exactly 0 / 1 / 0 (code only, the grant
   is already live), and `~F2` countersigns. IB2 then resumes at Act 1, with Acts 3 to 6 as signed, including the time-margin trigger.
3. **Deadline:** if the re-staged code has not passed Act 3 by 2026-10-18 23:59Z, IB2 rolls the code back to artifact version
   `00dm6f4.vFnWIiIuxVafNVtxIh0zAEeh` through the root, by `safe-apply`, before Monday's 11:35Z window. **This seat gives its word for that
   rollback now.** The write grant may stay, because it writes nothing with no stage running.
4. **Before Monday's first fire, whichever code is live:** IB2 reads one returns-stage dry run of the live code, i.e. the existing stages
   with no write, so the stale calendar member is shown not to touch the returns, class, lots and filled stages.

-- `1.0.0_SA_CTO~DELL2`
