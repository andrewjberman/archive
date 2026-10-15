# IRPT_DASHBD B-CW -- the Cottonwood holdings_performance_daily pair (DB-c-5, round 115): CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~03:1xZ. **Bound to:** `deliverables/0.9.0_WK_IRPT_DASHBD~403/NEVER_WIDEN_PACKET_DB-c-5_R115.md`,
**blob `ad049d506c`** (`git hash-object`; sha256 `5c69518bab4f5bf0f5cd...`). A different blob voids this half. The COO half (`2.0.0_SA_COO~C2`)
is owed at the same bytes.

## The packet's questions, answered by this seat's own reads (~03:1xZ)

1. **The function does not exist.** `lambda get-function irpt-cot-holdings-performance-lambda` returns `ResourceNotFoundException`. Mode:
   BUILD, not adopt, with the name from the builder.
2. and 4. **The grants against the bucket policies:**
   - `opal-data-cottonwood`'s `DenyForeignFirmPrincipals` admits only principals matching `role/*-cot-*` (plus Andrew's users), and the
     role name `irpt-cot-holdings-performance-role` matches it.
   - The three restricted denies (read, list, write) name only `commonwealth/cottonwood/bronze/crm/`, so the gold prefix is not fenced.
   - `opal-data-assets` carries no statement that fences the Black Diamond silver read (its deny is a PutObject rule; the role writes
     nothing there).
   - **The grants are CONFIRMED as written:** read and list on the BD silver prefix; list and read on its own daily gold prefix; write only
     on the two gold tables.
3. **2026-06-09 is excluded, as the packet states.** Its prior trading day has no silver partition and no gap link is declared, so the rule
   has no base. That is ABSENT, not computed.

## Rulings

1. **W403-S2 (schema 1.1 history beside a HEAD 1.2 build): ship 1.2.** Never build the older emission to match old bytes. 1.2 only ADDS two
   keys (`partitions_read`, `span_trading_days`). **Condition:** the after-read runs each of the 3 `holdings_performance_daily` readers
   against one 1.1 and one 1.2 partition, and both read clean. The 1.1 history is NOT rewritten; that would move served output for no
   reader's need.
2. **W403-S4 (a refused listing silently falls back to one day):** the grant fixes the cause. **And the BUILD changes `_days_to_compute`
   so that a listing refusal raises and the fire fails loud.** A scheduled producer that quietly skips missing days is the defect class
   this whole pull fix exists to end. One test plants a refused listing and expects a failure.
3. **The order:** BUILD the function, create the principal, run the 12-date catch-up (36 keys, read absent first), after-read it, and only
   then create the schedule ENABLED at 08:15 New York with the input-frontier hold.
4. **The applier:** no AE lane is free and live, and the one-project-per-seat rule bars borrowing `~IB2` (IRPT_BCKEND). **This seat asks
   `0.0.0_AB_MSTR~DELL2` to seat ONE AE CloudOps lane for IRPT_DASHBD**, used by B-CW now and by the other IRPT_DASHBD writes later.
5. **Rollback** of a first write into empty prefixes is deletion, which is Andrew's act (W166-S2's rule). It is registered as ONE call with
   the exact key list only if a rollback is actually needed. The lane never deletes.
6. **`account_return_daily` after 2026-06-22** (Commonwealth silver stops at the 06-23 partition): **the source becomes Black Diamond**,
   the same daily feed this producer reads, which is Cottonwood's reporting system and the tie-out source the PRD names. It is a B-CW READ
   next round: whether BD carries an account-level return series, and at what grain. It is not Andrew's call. A Commonwealth delivery is
   not awaited.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `ad049d506c`, covering both branches of the packet.

-- 1.0.0_SA_CTO~DELL2
