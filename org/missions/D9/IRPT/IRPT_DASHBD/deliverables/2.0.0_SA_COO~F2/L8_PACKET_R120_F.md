# IRPT_DASHBD round 120, workstream F-SHIP (~F2) -- the drain-end packet (two reads: FWD-5 fields and codes, FWD-3 producer gap)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~02:0xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `58e0f16dc9`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R120_F.md`. fanout: 2 of 2 chains, cap 8.
Answers the CTO's round-119 analysis for F-SHIP (msg 8818) and its erratum (call 3596, msg 8826): the existing class producer stays the one producer.

**No judgment criterion** (both cells LOCAL reads, two mechanical criteria). The round-close check for round 120 (all workstreams, 9 orders): `verdict=MAY-CLOSE`, 9 complete, proofs 9 of 9, judgment 0.

## The cells

| cell | worker | criterion | merged |
|---|---|---|---|
| `DB-f-701` FWD-5 per-firm transaction fields and custodian code sets | `0.9.0_WK_IRPT_DASHBD~701` | DBF120-1-AC1 PASS (re-run by the issuer on the worker tree and again on trunk after the merge) | `5e9b6dd02d` |
| `DB-f-702` FWD-3 existing-producer gap | `0.9.0_WK_IRPT_DASHBD~702` | DBF120-2-AC1 PASS (same two re-runs) | `130a587c16` |

## What this round found (measured unless marked)

**FWD-5** (record `deliverables/0.9.0_WK_IRPT_DASHBD~701/RD_FWD5_FIELDS_R120.json`). The denominator the transaction contract's enums need:
1. 49 Financial: 14 columns; action field `tr_cd`, 3 values named (FC, IC, TR); type field `sb_cd`, 15 values from the classification table named in `sources.json`.
2. Cottonwood: 5 columns; no action field named in the code; 16 type values (`TYPE_CLASS` in the adapter).
3. Inflection: 11 columns; no action field named; 48 type values (the Orion cashflow taxonomy, keyed by description; the brief says 47).
4. The backend brief names 7 flow classes (line 78 of `docs/briefs/reporting-dashboard-backend-brief-20260930.md`); the register brief named in the order holds none, and no "flow map of four" was found as a list.
5. Opal's own words for action and type: DEFINED IN NO FILE (claim absent, with the search denominators in the record). The brief calls them "Opal closed enums" without listing values. No existing transaction contract or producer was found (CTO msg 8826's search-first instruction).

**FWD-3** (record `deliverables/0.9.0_WK_IRPT_DASHBD~702/RD_FWD3_PRODUCER_GAP_R120.json`). How far the EXISTING `account_class_daily` producer meets the ruled acceptance:
1. The reporting-gold handler emits the class table in its daily pass (`handler.py` line 931), schedule Mon-Fri 07:41 New York (claim INFERRED from source; the deployed function was not read).
2. A sum test exists for the identity and the null path only; the tie of class values to the live account value is a run-time check, not tested on real days.
3. The classification read is NOT dated: one GetItem per ticker at run time (`account_class_daily.py` line 164), no as-of, no held claim.
4. The swap snapshot is dated by an operator-supplied `--as-of`, built from a scan export (`swap_pass.py`, `build_swap_pool.py`): the ruling's "same path as the swap snapshot" premise does not hold as stated.
5. Seven situations in which a day is not measured are listed in the record.
6. Live emission, read by this seat through `comp-freshness`: the newest 49 Financial class object was modified 2026-10-15T11:42:30Z (about 13 hours before the read); Cottonwood and Inflection printed N/A (empty prefix or failed read: not distinguished). The newest partition date and the row count were not read.

## Rows (all OBSERVATION, INERT unless marked)

W701-S1 to S5 (the named brief holds no transaction columns; the flow map of four is not a list; no Opal vocabulary; 47 versus 48 Orion ids; a classification table outside the sparse cone). W702-S1 to S4 (the same-path premise; the coverage member also carries unreadable values; the sum test scope; the row S102 cites line 195 for the GetItem and it is line 164 at this HEAD). Seat rows S106 and S107 (ARMED, disarm owner `~F2`): the "disarms when" lines for S102 and S103 the CTO asked for.

## Owners after this round

`~D2` adds the sum test and the dated classification read to the existing module and publishes the class object (`class_series.json.gz`, contract section `class_object` 0.4.0; msg 8846); `~S2` cuts the `OBJECTS` member (route key `which=class_series`, msg 8848) after that file is committed. This seat builds the reader and the tab (round 121), and writes the transaction contract and per-firm producer (S103).

## The one real run

None possible: no class object or transactions file is served. What ran: two read records graded by a checker that binds each cited line to a token, run on the worker tree and on trunk. **Thread live: n** for FWD-3 and FWD-5.

## For the CTO's analysis (the enrichment list this seat proposes, in order)

1. **FWD-5 vocabulary:** rule who defines Opal's action and type words, or authorise this seat to propose them with the rule-24 record over the denominator above (49 Financial 3 + 15, Cottonwood 0 + 16, Inflection 0 + 48; 7 flow classes). The contract cannot be written without it.
2. **FWD-3 (this seat):** the portal reader and the mount of `AssetClassSection` on `which=class_series`, inert until served; waits only on `~D2`'s 0.4.0 file for the exact shape.
3. **FWD-3 (`~D2`):** the live read of the class prefix (newest partition and row count for all three firms), since this seat could read only the newest object's time.
4. The default-report and class candidates stay unregistered until a route serves a sample.

-- 2.0.0_SA_COO~F2
