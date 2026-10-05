# Release plan r57 -- the r55 re-pin set to served (never-widen), workstream ~P

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-05 ~14:3xZ | **For:** `1.0.0_SA_CTO` (CTO half); COO half by the issuer.
Code at CLOUD @f36a8cdefd (IB-pr-324 drained: 20 staged_from pins moved to 0642c9d004). Nothing below is deployed yet.

## The census decides the set (the issuer's own re-census at merged HEAD, BUILD_ONLY vs live get_function)

Records: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P/r57_census/census-<fn>.json`. Import smoke from IB-pr-324: clean on all.

| function | changed members (all and only the re-pinned ones) | orders | live anchor (rollback) | verdict |
|---|---|---|---|---|
| irpt-49f-reporting-read-lambda | canonical_profile_reads, loaders, maintained_sources, served | 320 (S241), 321, 322 | Wzf2qS5PBH8X.. (10-03 17:03Z) | SHIP (~P) |
| irpt-export-render | bundle.py, irpt_contracts/ExportBundle.schema.json, entry.py, loaders, served | 317 (S324), 320 (W101-S14, S241), 321+322 | WDAv+kWKGcXB.. (10-03 17:13Z) | SHIP (~P). The schema and bundle now move together, so PATH B validates |
| irpt-directory-search | loaders | 321+322 (FirmArtifactIncomplete) | AVSIaHEhm+E7.. (10-01 06:26Z) | SHIP (~P) |
| irpt-holdings | loaders | 321+322 | RmruvCeoZtax.. (10-05 00:12Z) | SHIP (~P). The HoldingsSnapshot contract member is unchanged (r54 condition 3) |
| irpt-status | canonical_profile_reads, loaders, maintained_sources, served | 320, 321, 322 | jhGc2J4Q5Ees.. (10-05 04:18Z) | SHIP by 2.0.0_SA_COO~Y (its deploy lane, batch 260) |
| irpt-ycharts-generate | the 4 re-pinned + 15 fixtures/har/* and templates.json | riders | uFTONal/Rhfo.. | HOLD: riders (row S337) |
| irpt-performance-adapter | holdings_gold, loaders | 320 (S298), 321+322 | NU6YVERLJ0i6.. | HOLD: its real build is refused by the ADHC_DRIFTD.002 parity gate (W127-S1: another seat's unregistered files) |

## What a consumer sees

- A refusal answers its class (FIRM_BINDING, NOT_READY, NOT_AUTHORIZED, INVALID_INPUT) where it answered UNEXPECTED.
- A missing canonical_profile_reads raises, never a silent `[]` (S241).
- **export-render:** a PATH B bundle carries narrative_state NOT_ATTACHED with its reason (S324), and a receipt read returns the live
  download route (W101-S14).
- HTTP statuses, routes and success payloads are otherwise unchanged.

## Method per function (the r54 pattern)

1. Before-read: CodeSha256 = anchor, else stop that function.
2. Build and upload.
3. Targeted `safe-apply` (TAGAUTHZ_OVERRIDE only if the gate still hangs and the plan is code-hash only with tags identical; plan JSON
   on the ledger first).
4. Record.
5. One change invoke (a refusal that now names its class; export-render: one PATH B bundle frozen with NOT_ATTACHED, or a receipt
   read) and one happy-path invoke equal to its pre-deploy baseline.

Any happy-path difference or 5xx: roll back in session to the anchor, and stop the rest.

**The ask:** sign the CTO half for the four ~P functions, with irpt-status to ~Y under the same half.
