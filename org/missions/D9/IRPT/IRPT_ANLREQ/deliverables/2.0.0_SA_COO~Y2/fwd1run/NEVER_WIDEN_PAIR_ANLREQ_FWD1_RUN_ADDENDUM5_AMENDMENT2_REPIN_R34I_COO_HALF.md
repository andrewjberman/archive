# IRPT_ANLREQ FWD-1 run, ADDENDUM 5 AMENDMENT 2 -- R0e re-pinned from the resident r34h to the resident r34i (bindings only: the YCharts price tier taken out) -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. The window-5 order stays HELD until the CTO half of THIS amendment is signed on this file's blob AND ledger `irpt-resident-r34i-20261016` reads CLOSED with the V2S lines of section 2 AND the CTO hands over the 5174 server.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-17 00:4xZ. CTO half: owed, `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Amends: addendum 5 (COO blob `4a24c2443c76ce74c3c61ae1b0e11b583db287e9`, CTO half @02306c830e) section 2.2 (R0e, the resident) as carried by its amendment 1 (blob `e34ae09b3cabdd42c0ad830fc5fbc85917650e7e`, CTO half @51618a4fa1). **Only R0e's pins change.** Everything else of addendum 5 and its amendment 1 stands as signed (the inputs with two unknown symbols, the driver `bc228882...`, the mint helper, the advisor helper `3860d639...`, the weekday band, the R20-RV and R20-REL ledgers closed, the YCharts door quiet, no retry).

Claim words: MEASURED = this seat read it in this session; RECORD = a committed record this seat opened (named); RELAYED = carried by another seat; NOT READ = nothing read tells it.

## 1. Why R0e moves (RECORD)

The CTO ruled (msgs 9991, 10040) that the YCharts price tier stays unused in window 5 and that r34i takes it out of the bindings. `~G2` built it (RELAYED msg 10075): packet `NEVER_WIDEN_PACKET_RESIDENT_R34I_TIERS_BACK_20261016.md`, COO blob **`c5c086d1818b107eb3d0b5006c4f9490b03873ff`** (MEASURED by this seat with `git hash-object`), CTO half signed @f603e9a17c; ordered to `0.7.0_AE_CloudOps~IB2` (`TO-APPLY-R34I`). It changes the bindings file and the package sums only; every code member is byte-equal to r34h; `opal_pricing` tiers back to `[estate, yfinance]`, the `ycharts_window_budget` (6 calls, 390 s) kept.

## 2. R0e re-pinned (replaces R0e of addendum 5 section 2.2)

Root **`0485393f3a-r34i`**, tar `irpt-resident-0485393f3a-r34i.tar.gz` sha256 **`a6bd7c22327d378240626d4c70692183b13f29d11238d430ba8652d43d7564ab`**, **1,124,915 bytes**, 315 members; package pin `1a26b6aa37d02460d92cc9c906a28a1348d4f9dd`; V2 script `v2_service_env_r34i.sh` sha256 `4e2e8981394eb0d49464ddd588e5b64f20e538bd3c5cdffc88edcc640cade80c`. The gate at R0: ledger `irpt-resident-r34i-20261016` reads CLOSED; IB2's install record (`org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34i/A_AFTER_R34I.txt`) carries, from inside the service, `V2S OK SPY KEPT and ZQXWVK NOT_KEPT`, `V2S CONTROLS OK 4 of 4`, `V2S BACKOFF OK`, `V2S DOOR OK`, `V2S PRICING OK` (reading the two tiers `estate` and `yfinance`), `V2S BUDGET OK` and `V2S TIER OK` (the packet's step 6: r34h's checks kept, the pricing check reading two tiers and the 6 by 390 budget); the running root reads `0485393f3a-r34i`; `opal_pricing` enabled true with the tiers `estate` and `yfinance` and no `ycharts`. A record naming r34h or earlier as running, lacking any of those lines, or printing a `ycharts` tier, ABORTS. **If the ledger reads ROLLED-BACK, or r34i is not installed when the window opens, this amendment is VOID and addendum 5's pin to r34h stands unchanged.**

## 3. Blast radius and limits

No change to the blast radius of addendum 5 section 4; the install removes a path (the YCharts price tier) and adds none. NOT read: IB2's install record (the ledger has not closed at this writing); whether r34i is installed when the window opens.

## 4. Owed before the order is lifted

1. The CTO half of THIS amendment, on this file's blob (it may be signed before the ledger closes: section 2's VOID clause covers a rollback).
2. Ledger `irpt-resident-r34i-20261016` CLOSED with the V2S lines of section 2, read by this seat.
3. The CTO's 5174 hand-over and the R20-RV and R20-REL ledgers closed (addendum 5 amendment 1 section 2).
4. This seat's order amendment (re-pin R0e to r34i) in the held window-5 order and the `lift HOLD` commit.
