# WP8 trn_nna OPTION-B — grounded parity + retirement-readiness

**serial:** 0.4.0_DS_ClientPlatform~A | **date:** 2026-07-17 | **gate:** 1.0.0_SA_CTO
**ruling:** CTO 182433Z (option-b: C_01 re-derives NNA from monolith fact_trn; NNA-in-silver is a
Rule-17 violation to RETIRE, not replicate). AC1 parity + AC2 field-sufficiency, behind A4.

## TL;DR

The build is **already landed** (A4 L4 flip, 2026-07-16, CTO GO 185225Z): `lib/schwab_flows.py`
`DEFAULT_FLOW_SOURCE='monolith'`, deriving Layer-B gold-side via `lib/schwab_trn_nna_gold.py`.
My job was to GROUND it. Result:

- **AC1 PARITY: PASS** — monolith-derived NNA == legacy Layer-B NNA **to the cell** over the full
  overlapping window: **495 common dates (2024-07-08..2026-07-15), 26,504 (account,date) cells,
  0 dollar/count mismatches, 0 txn_key-set mismatches.**
- **AC2 FIELD-SUFFICIENCY: CONFIRMED** — the monolith transaction table carries every classifier
  input column (`MONOLITH_REQUIRED`); a loud `KeyError` refuse guards against drift. No passthrough
  needed, no compute-move.
- **Classifier is VERBATIM** — `schwab_trn_nna_gold.classify()` / `_txn_key` / all exclusion &
  direction rule-sets are byte-identical to the retiring `convert_schwab_trn_to_nna_silver.py`
  (move-not-copy is faithful).
- **Zero-live-readers de-risk: VERIFIED MYSELF** (COO ask).

## TWO DECISIONS FOR CTO

### D1 — source table: `dim_transaction` (code) vs `fact_trn` (ruling + naming law)

The gold classifier currently reads `schwab/08242234/silver/dim_transaction/` (a **44-col
projection**), NOT `fact_trn` (the **140-col COMPLETE** silver table the ruling names). Both carry
1,110 rows/day and **every** classifier-required column; classifier output is **byte-identical**
(verified 6 dates: rows, key-sets, dollar sums to the cent).

- **Naming law** (silver `fact_{type}` COMPLETE / gold `dim_*` projections / gold is the ONE
  parse-down point): the gold classifier IS the parse-down point and should read the COMPLETE silver
  `fact_trn`. A `dim_*` projection living under `silver/` is itself a monolith-producer naming
  deviation; the classifier depending on it means the parse-down happened one layer too early.
- **Efficiency** (the case for the projection): 50KB vs 121KB/partition (~2.4x I/O) — negligible for
  a nightly gold job.
- **Robustness**: reading the complete `fact_trn` + `MONOLITH_REQUIRED` loud-refuse is drift-proof;
  the projection could silently drop a required column.

**RECOMMENDATION:** re-point to `fact_trn` (ruling-faithful, naming-law-correct, drift-proof;
output proven byte-identical). 1-line prefix change in `schwab_trn_nna_gold.monolith_dim_transaction_prefix`.
IAM: the 07-16 grant (87f5940a7 / bd-v2.52.0) is on `opal-data-assets/schwab/08242234/silver/*`
(wildcard) per the deploy record — `fact_trn/` is covered, but **verify live `get-role-policy` before
deploy** (grounding this from the commit msg, not live IAM). Ready to land on GO.

### D2 — pre-2024-07-08 coverage gap on legacy retirement

Monolith transaction history starts **2024-07-08**; the legacy path covered **2024-04-12** onward.
The 57 legacy-only days (2024-04-12..2024-07-05) carry **$46.15M inflow / $28.08M outflow /
+$18.07M net NNA** across 2,415 cells. `account_gains` (C_01's date driver) spans 2020-01-02..
2026-07-13, so C_01 *can* process those dates. The 07-16 flip already stopped reproducing this
overlay on any **fresh historical rebuild** (existing pre-flip partitions are untouched; single-mode
source, no blend). Latent, not live — triggers only on a `--start-date` before 2024-07-08.

**RECOMMENDATION:** before retiring the converter, rule one of: (a) accept — pre-2024-07-08 Schwab
overlay is immaterial/not-served; (b) keep `source='legacy'` reachable + frozen legacy partitions
preserved for historical rebuilds; (c) extend monolith txn horizon to 2024-04-12 (monolith-producer
work, 0.7.0). This is a CTO/architecture call.

## Grounding (paths disambiguated — THREE distinct trn_nna locations)

| # | path | state | readers |
|---|---|---|---|
| 1 | `s3://opal-data-schwab/03_silver/TRN_NNA/` | froze 2026-04-20 (oldest) | **ZERO production** — only `enrich_transactions_with_schwab_diagnostic.py` (retired diagnostic) + `data/schwab/analysis/nna_parity_harness.py` (analysis). account_xref companion consumers repointed off it to opal-data-bd 2026-06-29. |
| 2 | `s3://opal-data-bd/schwab/silver/trn_nna/` | live legacy converter output, through 20260715 | ONE: `lib/schwab_flows.load_schwab_flows_by_date(source='legacy')` — now non-default (rollback lever). |
| 3 | monolith `fact_trn`/`dim_transaction` on `opal-data-assets` | live, default since 07-16 | `C_01.canonical_nna` (bd). |

The CTO's "legacy 03_silver/TRN_NNA-path NNA" = the Layer-B classified NNA; the operative LIVE
instance is #2 (what the converter produces + what `source='legacy'` reads). Parity ran monolith(#3)
vs #2 — the correct retire-side target ("RETIRES on parity-pass").

**cot** (`data/cot/scripts/gold/lib/schwab_flows.py`) is a SEPARATE-firm copy (`opal-data-cot`
bucket, no `schwab_trn_nna_gold.py`, no monolith re-point) — no cross-firm coupling; untouched (Rule 13).

## Evidence (reproducible)

- AC1 harness: monolith vs legacy via `load_schwab_flows_by_date`, per (account_id,date) diff on
  schwab_inflow/outflow/event_count + txn_key-set. 26,504 cells, 0 mismatch.
- fact==dim classifier-output identity: `derive_trn_nna_partition` over 6 dates, `.equals()` True +
  key-set equal + dollar-sum tie.
- Reader census: `comp-grep load_schwab_flows_by_date` / `03_silver` / `trn_nna`.
- Caveat sizing: legacy source over 2024-04-12..2024-07-05.

## Deployed-runtime verification (not just repo)

Pulled the DEPLOYED gold lib from `s3://opal-data-bd/code/gold/lib/` (deploy 2026-07-16 14:55Z):
- `schwab_flows.py`: `DEFAULT_FLOW_SOURCE=os.environ.get('SCHWAB_FLOW_SOURCE','monolith')` — live
  code default IS monolith.
- `schwab_trn_nna_gold.py`: `monolith_dim_transaction_prefix` returns `.../silver/dim_transaction/`
  — **D1 applies to the RUNTIME**, not just the repo.
- **No drift**: deployed md5 == repo md5 for both (`851eaf6a…`, `1b0904d1…`) — clean baseline; a D1
  GO commits+deploys in sync.
- Caveat (not overclaimed): code default = monolith is verified; definitive runtime proof that the
  nightly READS monolith is its loader `[monolith]` line (the exercised evidence at CTO's gate) +
  absence of a `SCHWAB_FLOW_SOURCE=legacy` env override on the scheduled job.
