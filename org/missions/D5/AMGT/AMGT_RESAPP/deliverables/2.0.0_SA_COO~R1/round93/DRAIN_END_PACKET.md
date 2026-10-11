# AMGT_RESAPP round 93 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~12:0xZ. Six orders, all complete: `ss-1`, `ss-2`, `ss-3` built and merged (`ss-1`'s portal candidate LANDED on DEV); `ss-4`, `ss-5`, `ss-6`
(three served writes, three windows, none shared) APPLIED and HELD; `ss-7` STAGED with no order (no DEMQUE answer); `AMGT-nn-6` parked at Andrew.** Round 93 implements the CTO~DELL1
round-92 analysis `ledger/ROUND_ANALYSIS.round92.md` @1edd8be57d (items 1-5; msg 3732); decomposition s.101; issuance @cab1577aba. Amendments (all the issuer's own check or face
errors, each recorded with its gate limb): ss-3 AMENDMENT 1 @9216247b95, ss-2 AMENDMENT 1 @e784178341, ss-6 AMENDMENT 1 @e6910d1ddc. `round-close-check.py --round 93`: orders 6,
proof_ok 6 of 6, judgment 0, verdict MAY-CLOSE. The cell prefix is `ss` (`rr` was used in an earlier round).

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-ss-1` | 1: the peers table says, in one plain sentence, that the subject's cap and the peers' caps are not on one date | complete; portal candidate `wk-AMGT_RESAPP-384-portal` @f4e09f2d47 CTO-approved and LANDED on portal DEV @6398c79eb4 (MSTR msg 3772) | worker ~384 @9e8cdb95ac, proof VALID, merged @34b31975c9 |
| `AMGT-ss-2` | 2: a driver point set whose figures are stated on different scales is held as a set | complete, merged @f79fdc7f28; producer-side | worker ~385 @d327b01518, proof VALID (re-seated once) |
| `AMGT-ss-3` | 3: a candidate row that is the subject's own company, by held identity, is excluded at the ranker; the held-name index comes from `lib/research/api/peers_rebuild.py` | complete, merged @3318cd4e85; producer-side | worker ~386 @13bdd83e95, proof VALID (re-seated once) |
| `AMGT-ss-4` | 2: SAP's stored driver re-verified under the scale rule and spliced | complete, SERVED: SAP 1 -> 0 points, 2 VersionIds moved | RA1 ledger `amgt-resapp-r93-ss4-sap-driver-dell1` CLOSED 8 of 8, proof VALID |
| `AMGT-ss-5` | 4: the candidate universe's new dated key | complete, SERVED: `date=2026-10-02`, 2,856 rows, 3,759,160 bytes, put 11:11:09Z | RA1 ledger `amgt-resapp-r93-ss5-universe-key-dell1` CLOSED 5 of 5, proof VALID |
| `AMGT-ss-6` | 3: the peers objects rebuilt without the self peer | complete, SERVED: 243 new objects at partition `2026-10-11T1125Z` | RA1 ledger `amgt-resapp-r93-ss6-peers-rebuild-dell1` CLOSED 6 of 6, proof VALID |
| `AMGT-ss-7` | 5: the DEMQUE answer's reader (pp-4) | STAGED, no order | request has no quote and no answer; row `MDPF_DEMQUE-D1-S10` stands |
| `AMGT-nn-6` (round 89) | mm-2 to PROD | PARKED at Andrew | call `dell1-20261011T033643Z-e7f2` |

## 2. The issuer's ONE REAL RUN at close

- **ss-6 (SERVED, WORLD): re-run by the issuer, not RA1's report.** `r93_self_peer_census.py --baseline PEERS_BASELINE_20261011.json --class-b HEI_US_Equity:HEI.A,JD_US_Equity:BKPQZT` on the live
  routes: S1 no subject lists its own company (the baseline had 10), S2 every removed member was an own-company member or a named class-B line, S3 backfilled, S4 every other
  subject member-for-member equal (231 of 243), S5 HEI.A and BKPQZT were members and are gone; `R93 SELF PEER CENSUS: YES`. Partition count read from S3: `2026-10-11T1125Z` 243
  objects, `2026-10-11T0707Z` 243 (untouched). The dry batch before the act (control arm without the index: the live objects' member lists 243 of 243) named the 12 sets; RA1's
  full-record compare of the written objects equals it (231 equal, 12 differ, 0 retained-member changes, 243 prior VersionIds unmoved).
- **ss-5 (SERVED, WORLD):** `r93_universe_pool.py --prior-version-id D.ZdXaKfQXNoHYeZ7.58h0t7peUmVcKB`: U1 the dated key exists, U2 vintage 2026-10-02 / 2,856 rows / `document-sha256` equals
  the bytes, U3 `date=2026-08-06` untouched (one version), U4 the loader returns 2026-10-02 (it REFUSED the old document at the base); `R93 UNIVERSE POOL: YES`. The digest equals round 91's
  pp-3 cache after pooling, so ss-6 and round 91's rebuild read one universe.
- **ss-4 (SERVED, WORLD):** `r92_driver_reverified.py --write-set SAP_GY_Equity`: R1, R2, R5 PASS, `R92 DRIVER REVERIFIED: YES`; live `/thesis` drivers: SAP none (was one point, 2024 = 18,078,
  a million figure under a billions unit text), ASML none, BABA FY2025 = 118,028 and FY2026 = 158,132; VersionIds of both of SAP's objects moved (RA1's 24-object head compare: 2 moved, 22 unchanged, so ASML's and BABA's
  are untouched since round 92); the drafting diff is `thesis_driver` and `thesis_driver_provenance` only.
- **Currency and no-regression arms, after all three writes:** `r92_minor_unit_census.py` M1 0 minor-unit labels, M2 0 rows with a currency beside a stale reason, M3 154 major-unit rows
  (160 before: the 6 removed members' currencies), M4 YES; `r89_peers_deployed.sh` and `r89_deployed_close.sh --want amgt-corpus-dossier/11` YES; the function's CodeSha256 unchanged at
  `SOzAz9/gfKE++UOSB8qWSDJvhOsDQMoE+DDPzaFbeSI=` (no redeploy this round).
- **ss-1 / FWD-38 (the CVO's ground):** `origin/DEV` @11f25102dd carries ss-1 as 6398c79eb4. The real `PeersTab.tsx` there, server-rendered over fresh live payloads of ASML, BA and ROG, prints one
  element after the table: "Market caps are not on one date: the subject's is as of October 10th, 2026; the peers' are as of October 2nd, 2026. The size band compares them as they are;
  neither is restated to the other date." The subtitle still prints the universe vintage and the subject cap its own as-of. A server render, not a browser walk
  (`round93_prep/FWD38_RENDERED_READ_DEV_20261011.md`).
- **ss-1, ss-2, ss-3 (LOCAL): on the merged tree.** `r93_scale_set.py` 5 of 5, `r93_self_peer.py` 8 of 8, `r93_locator.py` 14 of 14, `r93_scale_table.py` YES (12 objects, 0 changed now: the
  write has landed), `r92_block_bound.py` 5 of 5; drain checks 529 passed (peers, filings, the price-currency and rebuild api tests).

## 3. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **`ss-3`'s first face told the worker to import the api package from the engine.** A standing guard test forbids that literal in `lib/research/peers`, and it is right (the engine is
   producer-side and the api package imports it). The worker stopped on its own row and kept the order's import; the fix put the index-building caller above the package
   (`peers_rebuild.py`). Cost: one worker re-seat.
2. **`ss-2`'s AC3 chained round 91's locator, whose L3, L4 and K1 asserted SAP's three points the new rule (rightly) holds as a set.** Two criteria that could not both pass; the worker
   reported AC3 FAIL and held the order open. Fixed by a re-based locator that asks one point at a time (14 arms). Cost: one re-seat. A later stale-state dependency in the same
   check (K1 read SAP's stored point, which `ss-4` then emptied) was found at this close and removed.
3. **`ss-6`'s AC1 defined an own-company member by its served key**, which the CTO's signed class B (HEI.A, BKPQZT) lacks by design; RA1 held the order open with the writes landed.
   Fixed by a `--class-b` input and an S5 arm. The act matched the signed table throughout.
4. **A statement of mine was too cautious:** the `ss-5` half called the digest device-bound; RA1 read that the two model-block rows come from a directory tracked at the pin (ADDENDUM 1).

## 4. JUDGMENT for L9

No JUDGMENT criterion in an order. Offered for the CVO's own re-run: `r93_self_peer_census.py` (243 routes, a few minutes), `r93_universe_pool.py`, `r92_driver_reverified.py --write-set SAP_GY_Equity`,
`r92_minor_unit_census.py`, and the browser walk of the DEV peers page on ASML, BA and ROG for **FWD-38**: the page now shows each date and why they differ (see section 2).

## 5. Rows filed this round

Workers: `D1-W384-S1`, `S2`, `S3` (OBSERVATION, INERT: the product commit lands in the nested repo by design; the portal repo carries no committer identity; comp-pulse and the commit gate were
blind on a .ts/.tsx pair; all stand). `D1-W385-S1` (BLOCKING, ARMED: AC3's locator link and the scale rule could not both pass) disarmed by AMENDMENT 1; `S2`, `S3` INERT (stand); `S4`
(ARMED: CRLF normalised, restored; the merged channel diff is additions only) disarmed. `D1-W386-S1` (BLOCKING: the guard test) resolved by AMENDMENT 1; `S2` (AC2's expect wording) INERT.
RA1: none. Issuer: **`D1-S23`** (ARMED): the served display name of `SAN_FP_Equity` (Sanofi) is "Banco Santander S.A." (etf-classifications), and the held-name index carries Santander's name
under Sanofi's key; it changes no set (a bank is never a candidate for a pharmaceutical set) and the CTO made its repair round 94's first cell. **Disarmed by this round:** `D1-S21` (self-peers:
censused 0), `D1-S22` (the scale rule and SAP's write). `D1-W381-S1` (dell1's client-account hash list) is `0.0.0_AB_MSTR~DELL1`'s by the CTO's ruling.

## 6. For the next round (the ENRICHMENT LIST's inputs)

1. **D1-S23, the CTO's round-94 cell 1:** the display-name chain must not take a classification name that disagrees with the registered name, and the held-name index must carry one company
   per key; a census of every subject whose served display name differs from its crosswalk company, count printed (3 of 95 held keys are spelling variants, 1 is the wrong company).
2. **A rescale cell:** a series whose excerpt states the conversion (SAP's 2023-2025 backlog is stated in millions and billions in one passage) can be shown on one scale instead of held; the
   analysis's exception clause was not built in ss-2.
3. **The pp-3 entry's cache-file rule retires** (the loader reads the pool again); no rebuild now needs a local cache.
4. **ss-7 / pp-4** when the DEMQUE answer lands. `AMGT-nn-6` and FWD-16 stay Andrew's.

checked 6 of 6 orders terminal, 6 of 6 proofs VALID
