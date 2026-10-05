# L8 drain end -- IRPT_BCKEND rounds 47-51, workstream ~P (plus IRPT_DASHBD rounds 12-14, workstream B)

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-05 ~05:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Every order of these rounds is terminal and merged:
- 8 IRPT_BCKEND orders (IB-pr-313..320) and 3 IRPT_DASHBD orders (DB-b-20..22);
- 0 JUDGMENT criteria;
- one order of round 52 (IB-pr-321) is open and is not in this packet.

Three IRPT_BCKEND orders are WORLD-risk code with no deploy yet:
- IB-pr-317, S324's export bundle;
- IB-pr-320, the eight remainder repairs;
- IB-pr-321, still in flight.

Their served release is ONE issuer round, under never-widen halves, after IB-pr-321 merges. No served byte moved from these code
cells.

## IRPT_BCKEND

| order | round | drain | criteria (issuer re-run before the drain) | real run / served state |
|---|---|---|---|---|
| IB-pr-313 (E1 reconcile, 42 rows) | 47 | @db0adf0053 | IB47 E1 criteria PASS | a record: 17 HOLDS closed by W116-S2..S14; 25 LIVE handed back, of which 9 were cut in rounds 48-51 and 16 batched (section 42) |
| IB-pr-314 (record six lagging functions) | 47 | @91181ca88d | IB47 E3 criteria PASS | source map = live CodeSha256 for the six |
| IB-pr-315 (sha handoff by file, asserted) | 48 | @a0d75c7308 | IB48 criteria PASS | CI script; exercised by the next build-and-upload |
| IB-pr-316 (49F reporting chain at live names) | 48 | @f9d6238f11 | IB48 criteria PASS | source map rows keyed by live names (S322, S178) |
| IB-pr-317 (S324 PATH B narrative NOT_ATTACHED) | 49 | @82ff1bf64a | IB49-1-AC1, AC2 PASS (4 + 22 tests) | NOT deployed: the export Lambda release is owed |
| IB-pr-318 (W100-S2 readers census) | 49 | @0f69381e7c | IB49-2-AC1 PASS | LIVE_READER found, so the next two acts followed |
| IB-pr-319 (W100-S2 withdrawal packet) | 50 | @a99454d66b | IB50-1-AC1 PASS under amendment 1 (@960db69a15: the account leaf is in by ruling) | REAL RUN: the leaf was deleted on Andrew's card 1 (@c9c8e0c191) under the CTO half @4a63c9b600 and the COO half @48fa2860ab. The after-reads: head 404 with the marker current; the route answers 403/403/200 (withdrawn = never-served). Ledger irpt-w100s2-perfrp-leaf-withdrawal-20261005 CLOSED @752ffa138a (CTO batch 256) |
| IB-pr-320 (8 LOCAL remainder rows) | 51 | @f9e1c4ab96 | IB51-1-AC1/AC2/AC3 PASS (7 suites + 2 CI shell tests; 8 rows named; 18 paths in grant) under amendment 1 (@37e246c6df, W123-S1 empty-plan no-op) | NOT deployed: releases owed (authz consumers, holdings-performance x2, performance, export) |

## IRPT_DASHBD (workstream B)

| order | round | drain | criteria | real run |
|---|---|---|---|---|
| DB-b-20 (the ONE BD pull) | 12 | @5a671b2aba | DB12 PASS | aborted at call 19 (HTTP 401, bearer expiry) |
| DB-b-21 (completion mode) | 13 | @7cadb6e555 | DB13-1-AC1/2/3 PASS | aborted after 127 calls (a second transport URLError) |
| DB-b-22 (concurrent completion) | 14 | @7c8d60abc8 | DB14-1-AC1/2/3 PASS (14 tests) | LIVE: 1,895 calls, 0 FAILED, no 401 or 429, 55 mints. The session's 2 h job cap stopped it at ~04:11Z, not its own rules. S3 holds 2,012 of 5,252. The relaunch is Andrew's call. Ledger irpt-dashbd-e3-bd-population-pull-20261004 is OPEN (window 9 h) |

## Other acts in the window

- **MDPF daily runner:** EC2 i-02448edb624a7a7cf was started on Andrew's card 2. Ledger mdpf-daily-runner-restart-s323-20261005 has
  S1 and V1 closed @0a20399ff8. V2 (the next directory refresh manifest, at all three firms) is OPEN for the 12:52Z chain.
- **W80-S1:** ACCEPTED on CTO batch 252 (INF keeps T-1). It disarms on the issuer's read of the 14:00Z INF fire.
- **S326:** ~Y's irpt-status CHANGELOG entry is committed @2b7ef46538.

## Rows

| row | class | standing |
|---|---|---|
| W121-S1 | BLOCKING | DISARMED by S331 (@4f6405b61f; CTO batch 256) |
| W100-S2 | BLOCKING | disarmed with W121-S1 (S331) |
| W122-S1 | BLOCKING, INERT | resolved by IB-pr-319 amendment 1 |
| W123-S1 | OBSERVATION | resolved by IB-pr-320 amendment 1 |
| W69-S1 | OBSERVATION | DISARMED by S328 (@a980c1b141; MSTR ruling 105150) |
| S330 | OBSERVATION, INERT | the 403 read; re-pointed to ADVI_PERFRP's owner (batch 256) |
| W80-S1 | OBSERVATION, ARMED | accepted (batch 252); disarms on the 14:00Z read |
| S260, S175, S180 | OBSERVATION | in IB-pr-321 (round 52) |
| S218 | BLOCKING, ARMED | OPEN: an SSM journal read plus a CTO allowance ruling are owed |
| S204 | OBSERVATION | OPEN: ledger irpt-adapter-holdings-gold-49f-r3-20260929 leg A1 (the all-accounts served census) is unproven; a census cell is owed |
| S252 | OBSERVATION | parked by its own declaration (it un-parks when Cottonwood holdings gold is served) |
