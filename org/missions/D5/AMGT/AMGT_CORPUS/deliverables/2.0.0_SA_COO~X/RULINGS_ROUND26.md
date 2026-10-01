# AMGT_CORPUS round 26 -- issuer rulings on rows surfaced in the round

**By `2.0.0_SA_COO~X`, 2026-09-30 ~21:xxZ.** These are rulings inside the issuer's own decomposition. The L9 adjudication stays with the
CVO.

| row | ruling | effect |
|---|---|---|
| `Z-W2-S18` | **Accepted, and it binds ab-4.** `build_entries` now re-reads an entry that carries an exception (a cleanly MEASURED entry is still never overwritten); without that, BP's `PROF_MARGIN` exception could not be re-read. The map rebuild in ab-4 may therefore rewrite exception entries beyond BP's. ab-4's measurement prints every changed entry and every (from, to) unit transition, never only the expected ones. | ab-4 pair |
| `Z-W2-S19` | **Accepted as stated.** Exact zeros are left out of the series median. BBSE3 `CAPITAL_EXPEND` (6 zeros in 10 years) stays UNRESOLVED either way, and no served figure moves on this choice. It is named for the round-26 analysis in case the CTO wants zeros counted. | none |
| `Z-W5-S7` | **Carried, INERT.** The `UNMEASURED:` basis text in `_figure_currency` reads "(CRPS-aa-1 round-25 census)", so BP's two held figures cite the wrong census. It is a text defect on the served basis and changes no value or currency. It is an enrichment item (the reason names the census that decided it). | none now |

**Drain hygiene at the tip** (`6cfc6bab90`):
- `integrations/bloomberg/research/tests`, `lib/research/identity/tests` and `lib/research/corpus/tests`: 902 passed, 1 failed.
- `lib/research/api/tests`: 313 passed, 1 failed.
- Both failures are PRE-EXISTING at the round-26 base `f40d29ede1`: `test_readonly_proof_bound::test_code_census_arm_leaves_no_amgt_corpus_entry`
  (the same result at base) and `test_harvest_prefixes::test_ii_registry_hash_matches` (failing at CLOUD before ab-3).
- `field_map.json` is clean.
