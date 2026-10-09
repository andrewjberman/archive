# IRPT_DASHBD round 2 (workstream B) -- the issuer's drain-end record (spine L8 input; the CVO's channel compile is its own artifact)

**Issuer:** `2.0.0_SA_COO~P`, 2026-10-02 ~06:3xZ. **Issuance:** @97eaff05ff (decomposition section 2, two cells), on the CTO's round-1
analysis @57304c750b and its ADDENDUM 1 @7a888d7675 (DB-b-5 narrowed to the read root). PRD v0.6 @aabc054e89.

## The two cells, terminal

| cell | order | terminal state | evidence |
|---|---|---|---|
| `DB-b-5` | the issuer's served act | APPLIED 2026-10-02T05:52:22Z; ledger `irpt-dashbd-reporting-read-apply-20261002` CLOSED (5 of 5 legs) | packet @5cad424bd8 (blob f44ee4d312), COO half signed, CTO half batch 115 (`CTO_HALF_IRPT_DASHBD_READ_ROUTE_20261002.md`); 8 added, 0 changed, 0 destroyed |
| `DB-b-6` | TO-DB-b-6 (`0.9.0_WK_IRPT_DASHBD~1`, direct act) | COMPLETE @205f18b142, merged @119b8ed80a | DB-6-AC1 PASS, proof VALID rc=0 (issuer re-run); record `deliverables/0.9.0_WK_IRPT_DASHBD~1/FLOW_RESIDUAL_acct#89d0916a_R2.{json,md}` |

## The one real run of each outcome

- **FWD-1, end to end (the thread is LIVE):** `2.0.0_SA_COO~D`'s signed-in walk on portal DEV `39b7a0fc`, 06:26Z-06:28Z, against the
  real backend (`deliverables/2.0.0_SA_COO~D/FWD1_REAL_RUN_20261002.md` @74df2f62dd): 3 GETs through the route (2 manifest, 1 series),
  all HTTP 200; the covered account's page showed the dashboard figure with "Data through September 28th, 2026" beside it (ADDENDUM 1
  A2). The issuer's own read of the function log: 3 invocations (3 REPORT lines), one `irpt_error` `NOT_READY` -- the client's second,
  unpublished account, the route's expected branch, on which the page kept the tab's own figure.
- **The read root's controls:** V1 (CodeSha256 equals the source map; the route on `CUSTOM` / `naqxlm`; 17 of 17 prior
  investor-reporting routes unchanged; re-plan No changes) and N1 (an unauthenticated GET answered 401; no invocation).
- **FWD-8 enrichment (DB-b-6):** the 1,498.38 USD residual on acct#89d0916a is not one leg and not on 2026-07-07 (the issuer's inference,
  refuted): it is the net, over 2026-03-16 .. 2026-08-28, of four offsetting classes -- in-kind transfers valued -7,252.16 (measured),
  margin interest +10,724.31 classed internal at Opal and external at the vendor (measured), trade and merger differences -3,277.48
  (inferred) and the vendor cash asset +1,303.71 (inferred). The fee leg (2,423.40 on 2026-07-07) matches to the cent. No vendor call.
  Black Diamond's per-transaction data is not landed (bronze holds performance, allocation, costbasis, fees and roster only).

## Rows (19 in the channel, parsed at 06:3xZ; 0 ARMED)

| row | standing | disposition |
|---|---|---|
| S12 | OBSERVATION, INERT | E2 carried to the X10 register's incumbent `4.0.0_SA_CRO` (a retention family for `series.json.gz`) |
| S13 | BLOCKING, INERT | ruled by ADDENDUM 1 A1-A3: the gold has no clock; round 3 cuts DB-b-7 (the adapter's schedule) before the publisher |
| S14 | OBSERVATION, INERT | named in the packet's blast radius and signed by both halves (the boundary's scope and service-profile reads) |
| S15 | OBSERVATION, INERT | ACCEPTED by the CTO half (one writer per route key); naming the route in `routes.json` is round-3 hygiene |
| S16 | OBSERVATION, INERT | the gate2 seating lint truncates worker serials; owner `1.0.0_SA_CTO` |
| W1-S5 | OBSERVATION, INERT | ACCEPTED: the residual is a mixed-sign net; DB-6-AC1 sums `is_residual` legs by absolute value, so the record flags one derived net leg and carries the components unflagged. The check's shape is the issuer's defect; a net-aware sum is the fix if the check is reused. |

## Enrichment the issuer proposes for round 3 (workstream B), for the CTO's analysis

1. **DB-b-7, the adapter's scheduled fire** (ADDENDUM 1 A3, first): `account_return_daily.py` packaged unedited as a scheduled Lambda on
   the holdings-performance pattern, its own root and ledger, firing before 08:15 ET; WORLD.
2. **The publisher root with its 08:15 ET schedule** (A3, after 1): the planned `reporting-publish` root, re-planned against the
   policy-selector fix (S263) before its packet.
3. **IRPT_DASHBD-S6 limb (e)** (A4): foreign tax paid moves to internal in the CRO's classification file, the served engine's read moves
   under its own packet, and the adapter's override retires in the same act -- cut with `4.0.0_SA_CRO`.
4. **The margin-interest class** (DB-b-6): Opal classes INTR less S1INA internal, Black Diamond external (+10,724.31 on one account);
   the same classification question as item 3, for the CTO to rule with it.
5. **Hygiene:** the read route into `routes.json` without the `api` root generating it (S15); `BucketUnmapped` answering `UNEXPECTED`
   (IRPT_BCKEND-S260) at the next change to `entry.py`.

## Not done here

- The worker worktree DIR `C:\Users\AndrewBerman\Desktop\wk-irpt-dashbd-1` and branch `wk-IRPT_DASHBD-1` (all merged) are NOT removed
  (a recursive delete; held for Andrew's word).
- The page's time to paint and requests after a date change were not measured (`~D`'s record, "Not measured").
