# AMGT_RESAPP round-84 PREP -- one company, several listings: is there an issuer identity to collapse on?

Grounding fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~10:5xZ. READ-ONLY (no store write, no deploy). Ruling:
`org/missions/D13/DSGN/DSGN_AMGTV1/ledger/CTO_RULING_ROUND57_R1A_R6_20261009.md` ADDENDUM 2 (CTO~DELL1 msg 2284): collapse ONLY when
the candidates share an issuer identity **in the name list's own data** and exactly one listing is covered; if the list carries no
issuer identity, the cell's first act is to measure that.

## 1. Measured: the name list carries NO issuer identity for the ASML rows

The name list is the crosswalk `name_search.resolve_query` reads (`lib/research/api/name_search.py:83`,
`crosswalk.load_crosswalk()[0]["records"]`; S3 `crosswalk/v1/<date>.json`).

| measure | value |
|---|---|
| records | 243 |
| records with an `identity` block | 68 of 243 |
| `identity.cik` non-null | 65 of 243 |
| `identity.composite_figi` non-null | 65 of 243 |
| any structured issuer id (cik or composite_figi) | 67 of 243 |
| structured ids shared by 2 or more records | **0** |
| `ASML_NA_Equity.identity` | **null** |
| `ASML_US_Equity.identity` | **null** |

CIK 937966 exists for both ASML listings, but only as text, never as a field the list can join on:
- `ASML_US_Equity`: inside free text, `source_row.bloomberg_ticker.evidence` and `provenance.resolution` ("cik 937966 from the SEC
  ticker-to-CIK table on root 'ASML'").
- `ASML_NA_Equity`: nowhere in its crosswalk record; only in the stored filing's EDGAR URL
  (`sec/harvest/silver/filing_source` row, `url` .../edgar/data/937966/000162828026011378/..., `entity_name` "ASML HOLDING NV").
  The silver rows carry no `cik` field (0 of 13).

So today the ruling's arm is **"none share a served identity -> keep the list"**: "ASML" correctly answers the 404 candidate list.

## 2. Covered

The route's coverage notion is `_covered_key_known` -> `lib.research.coverage.covered_universe.covered_security_keys()` (the research
dossier folders, read fresh; 95 keys). `ASML_NA_Equity` is covered; `ASML_US_Equity` is not. Exactly one of the two is covered, so
the collapse would apply once the identity is a field.

## 3. Similar names, different issuers (must still list)

`resolve_query`, local, base: "Micro" -> AMD_US_Equity, MU_US_Equity, MSFT_US_Equity (three issuers); "Advanced Micro Devices" -> AMD
only; "Nu" -> NU only; "SAP" -> SAP only; "Taiwan" -> TSM only; "zzqx" -> none.

## 4. The smallest change (two parts, in order)

1. **Give the list the identity (a crosswalk BUILD change -- `lib/research/identity/crosswalk.py` `build_crosswalk`, :646).** Carry a
   structured `issuer.cik` on each record from MEASURED sources only, in precedence: `identity.cik` where registered (65 rows); else
   the SEC ticker-to-CIK table the Positioning chain already reads (the source ASML_US's evidence names); else the CIK in the record's
   own stored filing (its EDGAR path). Each value carries its claim (`measured` + source); no CIK is ever inferred from a name. This
   writes a new crosswalk object (`crosswalk/v1/<date>.json`): a served-store write, so it goes under its own pair.
2. **Collapse in `name_search.resolve_query` (`name_search.py:90`, after `ordered`).** When there are 2 or more candidates, ALL carry
   the same non-null `issuer.cik`, and exactly ONE of them is in `covered_security_keys()`, answer `status "exact"`,
   `security_key` = the covered one, `candidates` = all of them, and a `reason` naming the chosen listing and the others
   ("ASML_NA_Equity, the listing we cover; also listed as ASML_US_Equity"). Otherwise unchanged.
   The route (`scoped_amgt.py:7059-7063`) already serves an `exact` answer as that key; add the other listings to the served body
   (e.g. `identity["other_listings"]` beside `identity["requested"]`, `scoped_amgt.py:7066`) so the page can say which listing and that
   others exist. `/resolve` (`:7165`) needs no change.

A route-only change cannot satisfy the ruling: without part 1 there is no shared identity in the list.

## 5. The check

`round84_prep/checks/r84_listing.py --crit AC1 [--where deployed|local]` (base fingerprints in `r84_listing_base.json`, written at
the base with `--write-base`). Base dry-run, local AND deployed (identical):
- R1 FAIL -- thesis "ASML" 404, `/resolve` status candidates, security_key None.
- R2 PASS -- "Micro" 404 with AMD, MSFT, MU.
- R3 PASS -- `resolve|Nu` 200:ecb54e1b, `resolve|zzqx` 200:7fecf064, `thesis|zzqx` 404:072e9755: 3 of 3 byte-equal.
- `R84 LISTING AC1: NO`, exit 1. ruff py39 clean.
