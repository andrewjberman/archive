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

**AMENDED PER CTO 160659Z (Andrew-direct via 0.6.2 ~15:5xZ: "0833 is the master for Advisor
Intelligence for 49 Financial. 0824 is the master for Model Portfolios... different business
logic purposes."). TWO LAWS, CITED CORRECTLY: the NEVER-SUMMED law is the ADDITION law (never
total across masters); Andrew's purpose ruling is the SELECTION law (which master a converter
READS). The master is PER-CONVERTER-FAMILY CONFIG resolved by the PURPOSE column below —
`master_for(PURPOSE)` in the lib, NO constant, NO default; unknown/ambiguous purpose REFUSES
at import and STOPS at the CTO gate.**

**PURPOSE, CONSUMER-ANCHORED (not asserted):** all ten write ONLY to the canonical store
(`opal-data-bd/canonical/schwab/silver/*` — each converter's DST constant, verifiable). The
store's sole consumer chain is the seed G-gold builders → the A1 platinum contract's
D-publisher input census (A2's 16 consumed surfaces are all this store's gold + dims) →
`ai.ts` Advisor-Intelligence portal surfaces. NO Model-Portfolios consumer touches this
store: the MP chain reads `opal-data-schwab` silver (the /49-schwab-conv seven → wsb
model-AUA feeder → mdpf partner_held) + SmartX/DynamoDB. Therefore all ten = ADVI = 0833.

| converter | feed | PURPOSE (→ master) | read path |
|---|---|---|---|
| build_fact_transaction | trn | advisor_intelligence → 08335338 | read_schwab_raw |
| build_fact_position | rps | advisor_intelligence → 08335338 | read_schwab_raw |
| build_fact_lot_unrealized | uln | advisor_intelligence → 08335338 | read_schwab_raw |
| build_fact_lot_realized | rld | advisor_intelligence → 08335338 | read_schwab_raw |
| build_fact_tax_1099div | tnn | advisor_intelligence → 08335338 | fetch_schwab_raw_text (custom H02/DIV parser) |
| build_fact_schwab (generic: SEC/ACC/TCF/TCFX/ULT/UPN/UPT/RLY/RLW/RLU/RTY/RTU) | {form} | advisor_intelligence → 08335338 | read_schwab_raw |
| build_dim_asset | sec | advisor_intelligence → 08335338 | read_schwab_raw |
| build_dim_account | acc | advisor_intelligence → 08335338 | fetch_schwab_raw_text |
| build_dim_relationship | acc | advisor_intelligence → 08335338 | fetch_schwab_raw_text |
| build_fact_asset | (no raw read — derives from silver; untouched) | inherits the store's | — |
(dim_advisor_role/fee read the opal-data-bd XREF — a different source, out of WP7 scope.
The /49-schwab-conv seven = PURPOSE model_portfolios → 08242234 — the L5b re-point, same
mechanism, CTO pre-approved.)

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
3. ~~BACKFILL QUESTION~~ **DISSOLVED (CTO 160659Z carrying Andrew verbatim: "I dont give a
   shit about the 01_raw folder... already all in bronze and silver for both schwab
   accounts" — 0.6.2 measured both masters at manifest parity: 0824 bronze 6,257/silver
   7,633; 0833 bronze 6,972/silver 8,468, shortfall 0). Deprecation is stated intent; the
   deletion word still comes explicitly at its moment.**
4. Idempotency unchanged: converters skip converted dates / --force rewrites — the deploy
   can roll forward day-one with no special sequencing.

## LINEAGE RULING GROUNDED (CTO 155859Z; measured ~16:0xZ, answers 0.5.0's seam cell)

**VERDICT: REPLACEMENT-NOT-CONTINUATION.** Grounded at source, two dates, same parser:
| tree | 2026-07-15 TRN | 2026-07-06 TRN (seed-build era) |
|---|---|---|
| `opal-data-schwab/01_raw` | 1,110 rows / 320 accts | 15,807 rows / 4,464 accts |
| `08242234` monolith bronze | **1,110 / 320 (universe tie 320/320)** | **15,807 / 4,464 (exact)** |
| `08335338` monolith bronze | 1,166 / 328 (overlap 319) | 15,876 / 4,481 |

`01_raw` IS the 0824 delivery (mechanism: the OneDrive sync is 0824-fenced — 0.5.0's own
fixed fact; the row universes tie exactly). Therefore the canonical store's PRE-re-point
history (`opal-data-bd/canonical/schwab/` silver + gold, all partitions <= 2026-07-06-era
hand-runs) is **0824-DERIVED**, and the re-pointed ten REBUILD from 0833 going forward —
per Andrew's 60fb1ad56 premise ("clean facts from Schwab account 0833"). NOT mixed, NOT
ambiguous. CONSEQUENCES: (a) this annotation IS the store's lineage record line; (b)
seed-vs-port identity verification runs WITHIN one master only — seed LOGIC re-run on 0833
inputs vs the port, NEVER port-0833 vs the 0824-fed store partitions (the never-summed law
in verification costume); (c) the A3 dry-fit's measurements stand as what they were — an
0824-fed-store fit exercise, already divergence-named. **L5b (CTO pre-approved): the
/49-schwab-conv seven get the same mechanism re-point with the master PARAMETERIZED per
script family (0824 for that chain) — next in lane; bridge-retirement clock HELD until
both cells close.**
