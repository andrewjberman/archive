# AMGT_RESAPP round 91 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~08:0xZ. Four orders, all terminal: `pp-1`, `pp-2`, `pp-3` complete and merged or applied; `pp-6` (the one redeploy)
APPLIED 07:37:03Z and ROLLED BACK 07:50:33Z on the CTO's [STOP]; `pp-4` STAGED with no order (no DEMQUE answer); `AMGT-nn-6` parked at Andrew.**
Round 91 implements the CTO~DELL1 round-90 analysis `ledger/ROUND_ANALYSIS.round90.md` @b462a02d8a (items 1-6; msg 3551); decomposition s.99;
issuance @2ff932a7de; amendments: pp-3 @8827626e5f (option B), pp-1 @b146adc911 (a Class or Series designator is refused), pp-6 ADDENDA 1-2 and
the rollback order @37556c704d. `round-close-check.py --round 91`: orders 4, proof_ok 3 of 3 complete, verdict MAY-CLOSE (pp-6 is the order outside
the verdict, status cancelled/rolled back).

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-pp-1` | 1: a non-US peer a held company names exactly serves that identity, refusing a Class/Series designator | complete, merged @62c242efc4; NOT SERVED | worker ~371 @8dc1a3bf56 (re-seated; first build @1797ef3fd7), instance VALID |
| `AMGT-pp-2` | 2: the verifier locates a driver point the filing states and still refuses one it does not | complete, merged @3b27cc580f; producer-side, no stored object rewritten | worker ~372 @9376f3bc6b, instance VALID |
| `AMGT-pp-3` | 3: the peers objects rebuilt against the scanner at asOf 2026-10-02 | complete, SERVED (243 new `peers/v1` objects at partition 2026-10-11T0707Z) | RA1 record @758039c454, entry CLOSED 7 of 7, proof VALID |
| `AMGT-pp-4` | 4: the DEMQUE answer's reader and wiring | STAGED, no order | request @b6e42f51a8 has no quote and no answer; question row `MDPF_DEMQUE-D1-S10` filed |
| `AMGT-pp-5` issuer act | 5: the remediation disposition table | DONE | `round91_prep/REMEDIATION_DISPOSITION_TABLE.md`: 30 open rows, closed 3, carried 11, re-owned 16 |
| `AMGT-pp-6` | 6: the one redeploy of `opal-amgt-scoped-api` | APPLIED then ROLLED BACK; cancelled | RA1 ledgers `amgt-resapp-r91-pp6-scoped-api-dell1` and `...-pp6-rollback-...` CLOSED; live again l8egBo/rf.. |
| `AMGT-pp-7` issuer act | 4: the question row for the DEMQUE owner | DONE | DEMQUE `INVESTIGATION_v1.md` row `D1-S10` @4b3c4ce8a9 |
| `AMGT-nn-6` (round 89) | mm-2 to PROD | PARKED at Andrew | call `dell1-20261011T033643Z-e7f2` |

## 2. The issuer's ONE REAL RUN at close

- **pp-3 (SERVED, WORLD): re-run by the issuer, not RA1's report.** `r91_peers_rebuilt.py` P1-P6 PASS 243 of 243 each (one partition,
  basis and member lists equal the in-memory dry run's, every scanner-sourced member `cap_vintage` 2026-10-02 with the one named model-block
  exception `AMXB_MM_Equity`, every prior object in place); `R91 PEERS REBUILT: YES`. `r90_whole_page_read.py` on ASML_NA_Equity, BA_US_Equity,
  ROG_SW_Equity (live function): FWD-8 identity YES on 3 of 3; figure vintages within one trading day 1675 of 1687, 1448 of 1460, 1644 of 1656
  (before: 1674, 1447, 1643); the 12 outside per name are the members' caps at 2026-10-02, **5 trading days behind the header, down from 45**;
  `peers //vintage` now 2026-10-11 (within the day); `peers.subject.cross_vintage_caveat` is served on all three and the date is carried per
  member in `cap_vintage` (CTO half ADDENDUM 1: together they meet the standard; FWD-38 grades on the CTO's rendered-page read).
- **pp-1, pp-2 (LOCAL): on the merged tree.** `r90_name_match.py` 8 of 8 (N1-N8); `r91_locator.py` 13 of 13 (L1-L4, K1, E1, X1-X7); drain checks
  153 passed (peers folder and three api tests), 318 passed (`lib/research/filings`). The merged tree's local arm of `r91_name_match_deployed.py`
  against the live latest peers objects: 24 of 24 candidates served, 0 leaked.
- **pp-2 regression read (dry-run re-verification of all 12 stored analysis objects, base against the merged code, nothing written):** 4
  points gained (BABA FY2025, FY2026; SAP 2023, 2025), 0 supported points lost, 0 spans changed, 1 base false positive removed (ASML 2025 = 4
  matched the last digit of `12.4`).
- **pp-6 rollback, re-run by the issuer:** live CodeSha256 read fresh `l8egBo/rfEH4ddCEFyWnUOb9BvN3bGu/azarul5Ho0g=` (LastModified 07:50:33Z,
  Successful); `r89_peers_deployed.sh` `R89 PEERS DEPLOYED: YES`; `r89_deployed_close.sh --want amgt-corpus-dossier/11` `R89 DEPLOYED CLOSE: YES`;
  `r91_name_match_deployed.py` 24 candidates, 0 served (the base state). RA1's 243-subject compare: 0 of 2230 members changed.

## 3. What happened to pp-6 and why (the CVO's L9 read)

The act applied and AC1-AC3 passed as written (4 of 4 members byte-equal to the pin; the no-regression arm YES; 24 of 24 served, 0 leaked). RA1's
member-by-member compare then showed a served property move that the signed outcome said would not: the 24 identity gains also gained a
`price_currency` (GBp 12, EUR 6, SGD 3, CHF 2; one a new reason), because `_with_price_currency` reads the record once a member has a key. My
COO half had treated currency as independent of identity: the issuer's error. The CTO first ruled KEEP (msg 3623) and withdrew it after the
issuer's read of the UK rows: the scanner quotes UK prices in POUNDS (Unilever 44.94, GSK 17.95, Reckitt 49.07) while the held record's
`PX_LAST` and `CRNCY` are in PENCE (4673.5, 1750.0, 5132.0 GBp), so `GBp` beside 44.94 reads as 45 pence, a 100x mislabel. Rolled back within
the pair's hour (13 minutes). **The same shape is already live on the base**: the numeric-ticker arm's UK members (at least 5: Imperial Brands,
HSBC, SSE, BP, AstraZeneca) serve `GBp` beside pound prices. That is a pre-existing defect class, not made by this round.

## 4. JUDGMENT for L9

No JUDGMENT criterion in an order. Offered for the CVO's own re-run: `r91_peers_rebuilt.py` (243 subjects, about 30 s),
`r90_whole_page_read.py` (three names), `r91_name_match_deployed.py --where local` against `--where deployed`, and the pp-6 rollback reads.
**FWD-38**: peer caps are now 5 trading days behind (45 before); the scanner has published at 2026-02-26, 05-18, 05-19, 05-21, 08-06 and
10-02, so no rebuild reaches one day; the CTO's standard (a figure within one trading day or the page says why) is met only through the
in-band statement, which the rendered-page read decides.

## 5. Rows filed this round

Workers: `D1-W371-S1` (ARMED; another listing's key for a Class A line: closed by AMENDMENT 1), `S2`-`S4` INERT (stand); `D1-W372-S1`, `S2`,
`S4` INERT (stand), **`D1-W372-S3` ARMED** (a pre-existing block rule: a last-located period's block runs to the excerpt end, so a synthetic
excerpt verifies 2025 = 18.08; not widened, carried to a round-92 candidate; disarm owner this seat). RA1: none. Issuer: `D1-S20` (round 90).

## 6. For the next round (the ENRICHMENT LIST's inputs)

1. **The CTO's ruling (ADDENDUM 2):** one cell, pp-1's identity plus a unit-aware currency guard (a minor-unit code such as GBp, ZAc, ILA is
   not served beside a major-unit price), then ONE redeploy; `crosswalk.py` (nn-5) rides by blob again. Check inputs exist:
   `r90_name_match.py`, `r91_name_match_deployed.py`, RA1's 24-row compare file.
2. **`price_currency_reason` follows the served state:** 23 of the rolled-back members and 156 live members serve a currency beside the stale
   stored reason text (the CTO's msg 3622 named it a cell).
3. **Candidate-universe home (option C):** bump `CURRENT_VINTAGE` and make the refresh write a NEW dated key, so a rebuild stops using a local
   cache file and the pool object stops reading 2026-08-06.
4. **The stored-object re-verification** that makes pp-2's four points reach a served chart: a store write with its own never-widen pair.
5. **pp-2's S3:** bound a last-located period's block, with a refusal arm on a synthetic excerpt.
6. **pp-4** when the DEMQUE answer lands; **the engine caveat date line** only if the rendered page shows neither the why nor the date.
7. `AMGT-nn-6` stays Andrew's.

checked 4 of 4 orders terminal, 3 of 3 proofs VALID (pp-6 has none: it was rolled back)
