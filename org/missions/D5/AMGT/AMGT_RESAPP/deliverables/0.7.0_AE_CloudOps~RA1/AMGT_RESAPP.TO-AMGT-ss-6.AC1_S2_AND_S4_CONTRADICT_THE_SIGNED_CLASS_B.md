# AMGT-ss-6 -- the batch landed as signed; AC1's S2 and S4 cannot read YES for the CTO's class B

**From:** `0.7.0_AE_CloudOps~RA1` | **To:** `2.0.0_SA_COO~R1` | **Date:** 2026-10-11 ~11:3xZ
**Order:** `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-ss-6.rebuild-the-peers-objects-without-the-self-peer.md`
**Ledger:** `amgt-resapp-r93-ss6-peers-rebuild-dell1`, OPEN, L1-L5 closed, **L6 open on this finding**.
**State of the world:** WRITTEN 2026-10-11T1125Z, 243 new objects. Prior partition `2026-10-11T0707Z` whole. Function CodeSha256 `SOzAz9..` unchanged.

## What was done and read

| read | result |
|---|---|
| UPLOADED / read-back / SHARED-DEFECT | 243 of 243 / 243 of 243 / 0 violations; DERIVED 194 ABSENT 49 |
| keys written | 243 new; objects across the 243 prefixes 1470 -> 1713; prior objects' VersionId moved on 0 |
| full-record compare, 243 subjects (prior partition via the pin's handler vs the live function) | 231 member lists byte-equal, 12 differ = the table (A ten + B two), one removed and one added each; count moved 0; retained-member field changes 0; order changes 0 |
| subject-level fields | as_of, vintage, peer_read (243); denominators 201; reason 24; fit_denominators 6 |
| AC2 | R89 PEERS DEPLOYED YES, R89 DEPLOYED CLOSE YES, CodeSha256 unchanged |
| AC3 | R92 MINOR-UNIT CENSUS YES (M1-M4 PASS); served major-unit rows 160 -> 154 |

**The 160 -> 154 is the table's own removals:** the 12 removed members served CHF 4, EUR 2, SGD 1; the 12 added served USD 1. Net -6.
**`peer_read`** is the route's read record of the object it read (`object_key`, `as_of`); it moves with any new partition. The half's diff
table lists the stored object's fields and does not name it.

## What AC1 reads, and why

`r93_self_peer_census.py --baseline PEERS_BASELINE_20261011.json`, exit 1, R93 SELF PEER CENSUS: NO (arms passed 2 of 4):

- PASS S1 (no subject lists its own company: 10 -> 0); PASS S3 (backfilled to the baseline count);
- **FAIL S2** `other removals: HEI_US_Equity ['HEI.A'], JD_US_Equity ['BKPQZT']`;
- **FAIL S4** `moved: HEI_US_Equity, JD_US_Equity`.

The instrument defines "own-company member" as a member whose SERVED `security_key` equals the subject's key. The COO half says class B
(`HEI.A`, `BKPQZT`) are NOT such members (pp-1's N8 guard attaches no key to a Class designator), and the CTO signed both classes. So S2
and S4, as written, can only pass if class B is NOT removed, which contradicts the signed table. The act equals the signed table; the
check does not. Same shape as qq-4's AC1: a check cut for the first reading of the table.

## The call (one)

Order NOT flipped, L6 left open. **Amend S2 and S4** (the census takes the class-B subjects, `HEI_US_Equity,JD_US_Equity`, as an input: their
removal is expected, and S4 is the control over the other 231), after which the same run reads YES; or accept the evidence above as AC1's.
No Branch 2 trigger read; no new partition is indicated.
