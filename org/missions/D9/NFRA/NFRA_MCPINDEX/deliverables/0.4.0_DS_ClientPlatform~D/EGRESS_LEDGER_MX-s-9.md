# EGRESS LEDGER -- NFRA_MCPINDEX MX-s-9 (Black Diamond asset dimension by REST)

**Seat:** `0.4.0_DS_ClientPlatform~D`   **Firm:** 49 Financial (49F) ONLY. Cottonwood untouched.
**Vendor:** Black Diamond (`bd3.bdreporting.com`, DataMining).
**Date:** 2026-09-28.

## Authority (the RECORD question, answered by reading, not from memory)

The vendor NEVER line applies to these calls, and the word IS given and recorded:

- `@785fc4d71f` -- Andrew-direct 2026-09-27 ~19:5xZ, recorded by `1.0.0_SA_CTO~O`. Verbatim, on the
  proven route: *"...after which future lambdas or devices use that long term trust token to bypass
  login and go straight to REST API."* The same record closes: *"MX-s-4's reseat was keyed on
  'Andrew's vendor word'. That word is now given."*
- Andrew-direct 2026-09-27 ~20:1xZ (refinement), carried in the CTO design ruling `@1973056c51` and
  msg `20260927T203308Z`: *"see if you can just have a rest api pull for those tables. shouldnt need
  to make another 49 Financial bd crawler"*.
- Session egress term (Andrew-direct 2026-09-26): egress is permitted for API calls this session,
  **each ledgered by the seat that makes it**. This file is that ledger.
- MECHANISM half (R-21 `@b390c36444`): the pull is a deterministic, re-runnable SCRIPT
  (`data/black_diamond/scripts/bronze/pull_bd_asset_dim_rest.py`), not an agent-turn fetch.

**Citation correction, stated rather than quietly fixed:** the task order attributes the
"rest api pull for those tables" quote to `@785fc4d71f`. Those bytes do not contain it -- they carry
the 19:5xZ MFA/trust-token answer. The quote is genuine but belongs to the ~20:1xZ refinement (CTO
ruling `@1973056c51`; msg `20260927T203308Z`; CTO log `ctoO_self_drive_O_fabric_tick82.md`). Verified
by printing the bytes at the pin, not by grepping for the quote. Substance is unaffected: both records
are Andrew-direct, 2026-09-27, and both authorize the REST route.

## No new login, no new crawler

Auth was a bearer minted from the EXISTING session secret `blackdiamond/49f/session` (written by
`bd-49f-auto-login`), read-only. This seat performed NO login and built NO crawler.

## Calls

| UTC time | endpoint class | purpose | outcome |
|---|---|---|---|
| 2026-09-28T05:15:52Z | DataMining auth + template roster (GET) + `Query/DimensionsFacts` (POST qt4) | THE ONE DISCOVERY READ: persisted template `AssetDimTXNs` + the qt4 dimension catalog, to name the asset super-class dim id or prove it absent | 200. Roster 19 templates; `AssetDimTXNs_OpalCapital_Daily` (id 440247) is queryType **Transactions (qt2)**, so it CANNOT carry assetClass/segment. qt4 catalog: 8 levels, 201 dimensions. All 10 required identity/class dims present. |
| 2026-09-28T05:20:0xZ | DataMining `v1/run` (POST) | FIRST pull attempt -- OVERRUN, see the bound note below | Run 541482's predecessor **541481 fired server-side** but this seat did not parse the response (BD returned the template at top level, not wrapped in `"template"`), so no export was downloaded. No template created; an orphan run record only. |
| 2026-09-28T05:22:13Z | DataMining `v1/template/{id}` (GET) + `v1/run` (POST) + `run/{id}/status` (poll) + `Api/DataMining/ExportResults/{guid}` (GET) | THE PULL: one qt4 (UnrealizedGainLoss, open-lot holding grain) selection of assetID plus the builder's identity and class columns, deduplicated to one row per asset_id | 200. Run 541482, guid `d9e8d5bb-b530-4931-b948-73d0b00ec9b2`, complete in 10s, export 673,669 bytes, 12,132 rows. |

## Super-class discovery outcome

**asset super class: FOUND, dim id 7** -- `Asset SuperClass`, `mappedColumn=assetSuperClass`, on its
own qt4 level `Asset SuperClass`. Measured by scanning 148 qt4 dimensions (DENOMINATOR printed by the
discovery run; full record `discovery_MX-s-9.json`).

This **overturns the outcome the ruling anticipated**. The design ruling allowed for the column being
`absent` (it is not in `field_dictionary.md`, whose qt4 section carries no super-class row), in which
case the builder would write NULL carrying the claim `absent`. It is NOT absent: it is dim id 7, and
the pulled column is 100% non-null over 12,132 rows with exactly the six values
`build_bd_assets_dim.py` already maps. Nothing is inferred; the value carries the claim `measured`.

## Vendor-side writes

**NONE.** No persisted template was created. The pull reused an EXISTING persisted qt4 template's
envelope (id 486228, `Unrealized_Template`) and swapped the dimension selection into the inline run
body, which BD does not persist. The module's `--allow-template-create` flag exists for the fallback
the ruling permits and was NOT passed. The only server-side state created was two run records
(541481 orphaned, 541482 exported), which every pull creates by construction.

## Bound note -- the order's "at most two BD calls" was EXCEEDED by one

Bound 2 of MX-s-9 reads: *"At most two BD calls (discovery + pull), each ledgered."* This seat made
**three** vendor operations: the discovery read, a failed pull attempt, and the pull. The extra call
was caused by a response-shape defect in this seat's own parser (BD returns the run either wrapped in
`"template"` or at the top level; only the wrapped shape was handled). It is recorded here rather than
netted out of the count. Cost: one extra server-side run record, no vendor write, no data movement.
