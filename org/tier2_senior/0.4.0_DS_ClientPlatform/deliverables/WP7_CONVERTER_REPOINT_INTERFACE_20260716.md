# WP7 CONVERTER RE-POINT — the authoring half's interface contract (A4 L5)

**TO:** OPAL_GLDRNS.A4 L5 | **Author:** 0.4.0_DS_ClientPlatform~A | 2026-07-16 ~15:0xZ
**Deploy half:** 0.5.0_AE_OpalETL (schedule re-point, legacy-bridge retirement, 01_raw/OneDrive
retirement) | **Gate:** CTO seam review convenes on this authoring (his 140844Z re-sequence).
**Why now:** the SI2 box lands monolith bronze daily ~09:46Z while the legacy 01_raw tree falls
a day behind every morning, patched by a MANUAL 0.5.0 bridge cycle — this re-point kills it.

## What changed (all @ this commit; commit-gate 10/10)

**ONE read path, in the lib** (`data/canonical/schwab/silver/_canonical_silver_lib.py`):
- `MONOLITH_BUCKET` / `MONOLITH_MASTER` (0833 — never summed with 0824) constants.
- `monolith_bronze_key(feed, yyyymmdd)` — the key grammar in one place:
  `schwab/08335338/bronze/{feed}/{YYYYMMDD}/08335338.CRS{YYYYMMDD}.{FEED}.zip`
- `latest_bronze_date(feed)` — partition listing per feed (replaces every converter's
  private 01_raw scan).
- `fetch_schwab_raw_text(bucket, key)` — GET + **unzip-AT-READ** + latin-1 decode; used by
  the generic H2 parser AND custom-section parsers (TNN H02).
- `_unzip_at_read` — the delivery is a **NESTED zip** (measured on bytes 2026-07-16: outer
  zip → ONE inner zip → ONE `CRS{d}.{FEED}` pipe-text file); the reader unwraps recursively,
  **exactly one member per level or REFUSE** (a multi-member delivery is a contract change).
  Bronze stays byte-for-byte as-delivered per 17a — the double-unzip lives here, never in bronze.

**Ten converters re-pointed** (SCOPE NOTE: the TO said "the seven converters"; the ESTATE
said ten — the three dim builders read the same legacy tree directly, and leaving them alive
keeps the manual bridge alive, defeating WP7's purpose. Measured, extended, stated):
| converter | feed | read path |
|---|---|---|
| build_fact_transaction | trn | read_schwab_raw |
| build_fact_position | rps | read_schwab_raw |
| build_fact_lot_unrealized | uln | read_schwab_raw |
| build_fact_lot_realized | rld | read_schwab_raw |
| build_fact_tax_1099div | tnn | fetch_schwab_raw_text (custom H02/DIV section parser) |
| build_fact_schwab (generic: SEC/ACC/TCF/TCFX/ULT/UPN/UPT/RLY/RLW/RLU/RTY/RTU) | {form} | read_schwab_raw |
| build_dim_asset | sec | read_schwab_raw |
| build_dim_account | acc | fetch_schwab_raw_text |
| build_dim_relationship | acc | fetch_schwab_raw_text |
| build_fact_asset | (no raw read — derives from silver; untouched) | — |
(dim_advisor_role/fee read the opal-data-bd XREF — a different source, out of WP7 scope.)

## Exercised (Rule 22a: the path, not the config)

- `build_fact_transaction --dry-run` vs live bronze `trn/20260715`: **1,166 rows / 328
  accounts / 144 cols, txn_uid unique — EXACTLY ties the monolith dim_transaction partition's
  1,166 rows** (two independent readers, one delivery — a free cross-instrument tie).
- `build_fact_tax_1099div --date 2026-07-13 --dry-run`: fetch+double-unzip+decode worked;
  verdict "header-only (no H02)" — the honest periodic-form SKIP, now derived through the zip.
- Behavior change stated, not silent: TNN's legacy 265B-stub size heuristic does NOT carry to
  compressed zips — header-only discrimination now rides the H02 check alone (always the truth).

## 0.5.0's deploy half (staged for the seam review)

1. Schedule re-point: whatever invokes these converters points at the new source implicitly
   (source resolution is code-side) — the deploy is the code push + S3 upload per Rule 13 lanes.
2. Retire the manual bridge + the OneDrive→01_raw sync + the 01_raw tree itself (Andrew/CTO
   word on retention).
3. BACKFILL QUESTION (named, not answered here): monolith bronze history starts where the SI2
   box started; sparse/periodic feeds (TNN: 4 dates in bronze today) and any pre-SI2 dates the
   legacy tree carries need a one-time bronze backfill ruling before 01_raw deletion.
4. Idempotency unchanged: converters skip converted dates / --force rewrites — the deploy
   can roll forward day-one with no special sequencing.
