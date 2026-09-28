# MX-s-4 step 1.2 -- the BD asset-dim REST pull: design ruling (1.0.0_SA_CTO~O, 2026-09-27 ~22:2xZ)

**Asked by:** `2.0.0_SA_COO~O`, file 20260927T215826Z (row NFRA_MCPINDEX-Z-S30 @e8fcf04e58).
**Andrew's word:** "see if you can just have a rest api pull for those tables. shouldnt need to make another 49
Financial bd crawler" (record @785fc4d71f).
**Ruling: DESIGN IT as one cell, on the terms below.** It is not ruled out.

## The three blockers, each answered

**(i) Firm line: the cell writes NOTHING in cot's tree.**
- The pull is a bd-owned bronze module under `data/black_diamond/scripts/bronze/`.
- It reuses only firm-neutral pieces:
  - the vendor catalog `data/black_diamond/API/`. Its README states that it is vendor-API knowledge, not firm data,
    and that it is shared deliberately under NEVER#1.
  - the 49F session secret `blackdiamond/49f/session`, written by the existing `bd-49f-auto-login`.
- Adding an `assets` entry to `data/cot/scripts/bronze/cot_bronze_ingest.py` is REFUSED.
- That the 49F runner imports a cot-tree module is a pre-existing placement question. It is not this cell's to fix, and
  not a precedent to extend.

**(ii) The three columns.** The catalog documents two of the three:
- `assetClass` (dim id 1) and `segment` (dim id 1138) are holding-level dimensions on **qt3 and qt4**
  (`domains/datamining/endpoints/payloads/field_dictionary.md:310-311`, `:574-575`). They are not on qt2, which is why
  COO~O's qt2 read found no route.
- `asset_super_class` is not in the dictionary. The cell makes ONE discovery read (below) to name its dim id or prove
  it absent.
- If it is absent, the builder writes `asset_super_class_bd` as NULL, and the output carries the claim `absent` for it
  (A_VALUE_MUST_CARRY_ITS_CLAIM). It is never inferred.
- Measured locally: the bd silver `unrealized` and `realized` parquets (newest 2026-09-25 / 2026-09-27) carry neither
  column (17 and 15 columns), so there is nothing to derive from without a pull.

**(iii) The vendor read.** It is permitted by the session's egress term ("egress is permitted for API calls this
session, each ledgered by the seat that makes it"). The executing seat ledgers every call. The shape is:
1. First, one read of BD's persisted template (AssetDimTXNs) and the qt4 dimension catalog, which covers the
   super-class discovery in the same read.
2. Then the pull itself: a qt4 (open-lot, holding grain) selection of `asset_id` plus the builder's identity and class
   columns, deduplicated to one row per asset.
- Creating a NEW vendor-side template is a write to vendor state. Do it only if no persisted template can carry the
  columns, and say so in the ledger.

## Coverage, stated so no one reads it wider

qt4 carries assets that are HELD on the pull date. An asset that has been fully sold since 2026-04-14 is not on it.
- The builder UNIONS the new pull with the frozen 2026-04-14 dim, latest-wins per `asset_id`, as `build_bd_assets_dim.py`
  already does with its trade dates.
- The output states both counts: rows from the pull, and rows carried from the frozen dim.

## Fees, measured while answering

`s3://opal-data-bd/bronze/fees/` is CURRENT: its newest object is `Fees_OpalCapital_Daily_2026-09-11_to_2026-09-25.xlsx`.
So fees are already served by the REST runner, and the fees downloader is a dead path to report, not rebuild. That is
step 1.1's answer for fees. Allocation is still step 1.1's read.

## Out of this ruling

- The pull runs 49F only.
- Served gold is untouched.
- MX-s-6 step 2 follows once the dim is rebuilt.
