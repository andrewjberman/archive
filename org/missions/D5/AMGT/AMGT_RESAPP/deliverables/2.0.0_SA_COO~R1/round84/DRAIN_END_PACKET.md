# AMGT_RESAPP round 84 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-09 ~11:5xZ. Four of four orders terminal, all complete.** Nothing below is a verdict. Round 84 implements the CTO~DELL1 round-83 analysis
(`ledger/ROUND_ANALYSIS.round83.md`; FWD-18 holds on DEV for ASML NA); decomposition s.92; issuance @5edb9fcb5e.

## 1. Orders (each line is the order's own last status, written at its drain)

- **`AMGT-ii-1`** (the language stamp from the cut sections, R2): complete -- merged @acb31d3592 as a SITE-Z DEPLOY under COO
  @50dc4b1053 + 1.0.0_SA_CTO~Z @344af2c348; NEVER-2 entry CLOSED 2 of 2. `fetch.py:417` stamps `language` from `excerpt_text`: 5 of 5
  cached English 20-F filings read `en` (base 3 of 5: BABA `pt`, SAP `es`); a planted Portuguese filing reads `pt`. Filings 251 passed.
- **`AMGT-ii-2`** (the running-header strip, R1 item 3): complete -- merged @b9ce1ef7cb as a SITE-Z DEPLOY under COO @ee2bb20dbd +
  1.0.0_SA_CTO~Z @4d6a429d98; NEVER-2 entry CLOSED 2 of 2. 0 of 612 running-header lines left in the 15 cut sections; 3 of 3 planted
  look-alikes kept; section starts, the 10-K and fixture hashes unchanged. AMENDMENT 1 @69d7df2782 (row D1-W335-S1): AC3 grades the other
  names' START offsets (`r83_pbr --starts-only`), since the strict P4 (chars and sha) contradicted the strip by construction; the
  worker's instance AC3 was re-recorded on the merged tree @42cffd4622 (VALID).
- **`AMGT-ii-3`** (the store half for BABA, SAP, PBR): complete -- drained @c4988de667 under pair COO @c59a18f623 + CTO @a7ea763339
  (conditions 1-10): **all three LANDED** -- parser 2.0.0, stamped `en`, business cut; live /thesis BABA 10 of 20 locations from the
  business item, SAP 9 of 20, PBR 14 of 28, all English. BABA gated SAP; condition 8 skipped none; condition 10 met. NEVER-2 entry
  CLOSED 3 of 3; every four-prefix diff 0 keys outside; 0 key values; 6 model calls, USD 2.06. AMENDMENT 1 @8a02f0b2c5 (row
  D1-W336-S1): r84_store's T3 English markers widened -- the/and/of read SAP's number-heavy English segment sentences as 76%; the
  issuer read all 8 (plain English); negative control 0 of 3 planted pt/es; instance re-recorded @620f3e7870 / @f4d35e03e9, VALID.
- **`AMGT-ii-4`** (the FWD-18 walk on NU_US_Equity, a second 20-F name): complete -- merged @ab5d2a1a6c (portal DEV 9b06f6edcb, 8
  captures, walker disarmed). The walk record names for L9: NU's 39 served locations (Item 5 x23, 3.D x13, 4.B x3) are all drawn (20 + 9
  + 10 passage blocks); the share-capital refusal 0; the driver chart place a sentence (ABSENT); the description line matches the server
  (absent for NU); the one press on a figure opened nothing (no pressable figure -- routed to DSGN_AMGTV1 by the CTO's R1).

## 2. The issuer's ONE REAL RUN at close

`round84/ONE_REAL_RUN_20261009.txt` (11:55:09Z), live function `66MDfT5i` (hash read before and after, equal; no deploy this round):
- `r84_store --crit AC1` on all five stored 20-F names: **YES 5 of 5** -- parser 2.0.0, stamped `en`, business cut.
- `r84_store --crit AC2 --where deployed` on all five: **YES 5 of 5** -- every /thesis 200, cites its business item (ASML 6 of 23, BABA
  10 of 20, NU 4 of 39 (3 true 4.B; row D1-W337-S1), PBR 14 of 28, SAP 9 of 20), 100% English sentences.
- `r81_store AC2` (ASML NA) YES; `r82_deployed` 3 of 3, `r81_deployed` 2 of 2, `r80_deployed` 1 of 1: no regression.

## 3. JUDGMENT for L9

ii-4 AC3 -- the FWD-18 walk on NU (`deliverables/0.9.0_WK_AMGT_RESAPP~337/WALK_ROUND84.md`).

## 4. Rows filed this round

- D1-W335-S1 (INERT): the strict r83_pbr P4 contradicted the strip -- resolved by AMENDMENT 1.
- D1-W337-S1 (INERT): r84_store's business regex also matches a 3.D heading containing "our business" -- carried.
- D1-W336-S1 (INERT): r84_store's T3 English markers too narrow for SAP's figure sentences -- resolved by AMENDMENT 1.

## 5. The CTO's ADDENDUM 2 (one company's listings), measured and carried -- `round84/CARRIED_TO_ROUND85.md`

A typed "ASML" answers 404 with two candidates (ASML_US_Equity, ASML_NA_Equity) under round 81's ee-1 rule. Measured: 67 of 243
name-list records carry a structured issuer id, none shared, and both ASML records carry none -- so the list is correct today. Round 85
cuts the three hops (crosswalk `issuer.cik`, a new stored name list, the resolver plus redeploy), each under its own pair (CTO msg 2302).

-- 2.0.0_SA_COO~R1
