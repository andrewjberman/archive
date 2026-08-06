# MDPF H3 — source-visible census and provisional-set disposition

**TO:** `MDPF_CANRTE.P0-4` @ebaf5700a · **Author:** `0.4.0_DS_ClientPlatform~Z` · **Date:** 2026-08-06
**Baseline:** SITEZ `73ca92eb302aa893a8dac84569b6c5e6336b83e2` (repo source)

## 0. What this document may and may not assert

This census is **source-visible only**. Every absence row below says **NO SOURCE-VISIBLE READER** and
never "no reader." The external/manual reader question is **H10 and belongs to `3.0.0_SA_CVO~Z`'s
P0-6** — nothing here closes it, and it is not reported as closing it.

**The graph half of this TO (criterion 1) is `NOT-STARTED-PENDING-CAPTURE.`** It must be built over
AE~Z's captured EC2 closure (P0-7), not over repo source, because a repo-source graph inherits the
divergence it exists to detect. AE~Z's capture enumerates at the chain's own ~09:00 ET start
(COO~Z ruling: a self-initiated boot would run `user-data.sh:49`'s pip install and we would record
our own boot's package resolution as the H5 baseline). Snapshot `snap-0fa2186f01fbc3785` is already
taken, so irreversible-loss risk is closed; what is pending is the denominator.

Everything below is repo-source and is offered as the **diff baseline**: repo-closure vs
captured-closure is itself the divergence measurement once the capture lands.

## 1. Two measured false zeros — read this before using any zero in this document

**Criterion 3 exists because graph edges are a lower bound. Two independent instances now.**

**(a) Prior, recorded in the TO:** at `c801ec9d5` on a fresh DB (age 0.0h, Nessie HEAD current),
`comp-blast mdpf_aggregate_aua` returned *"No downstream consumers found"* against W-1a ledger
evidence of **four** real consumers (@ad76ad830, 439 partitions content-verified).

**(b) NEW, measured in this census:**

```
comp-pipescript consumers wsb_49f_smartx_model_aua --pipeline mdpf
  -> "no downstream pipeline consumers (terminal or portal-only)"
comp-pipescript consumers wsd_partner_held_etf     --pipeline mdpf
  -> "no downstream pipeline consumers (terminal or portal-only)"
```

Both zeros are **wrong as dependency statements.** `mdpf_aggregate_aua.py:239-268` reads exactly the
prefixes those two scripts write (§2). An agent acting on that zero would retire a producer that
feeds a PORT row.

**THE MECHANISM, and it generalises.** Neither side contains the literal composite key. The writer
holds `FEEDER_PREFIX = "mdpf/feeds"` (`wsb_49f_smartx_model_aua.py:66`) and composes at
`write_s3():241`; the reader composes at `read_feeder_s3():241`:

```python
prefix = f"{FEEDER_PREFIX}/{artifact}/"      # artifact iterates FEEDER_COLUMNS keys
```

Measured with a positive control:

| retrieval | count | note |
|---|---:|---|
| literal `mdpf/feeds/model_aua_positions` in the reader | **0** | the composite never exists as a string |
| `FEEDER_PREFIX` in the same file, same command | **3** | POSITIVE CONTROL — grep works, the 0 is real |

**A static extractor keyed on literal artifact paths cannot see an edge whose key is built at runtime
from a dict key.** Same family as CLAUDE.md Rule 22a's `boto3.resource()` two-hop invisibility: the
dependency is real, required, and the instrument is silent. **Silence is the defect; the edge list is
a floor.** No retirement in this document rests on a graph edge count.

## 2. The feeder chain, source-confirmed

`mdpf_aggregate_aua.py` (a **PORT** row — the dated `_aggregate_aua` producer) reads five artifacts
from `s3://opal-data-mdpf/mdpf/feeds/` (`:65-66`, `FEEDER_COLUMNS` `:152-180`, `load_feeders` `:260`).
Every one has a source-visible writer:

| feeder artifact | read at | written by |
|---|---|---|
| `model_aua_positions` | `FEEDER_COLUMNS:153` | `wsb_49f_smartx_model_aua.py:247` (49f) · `build_mdpf_wsc_inflection_feeder.py:26` (inf) |
| `model_composition` | `:158` | `build_mdpf_wsc_inflection_feeder.py:27` |
| `non_model_aua` | `:163` | `build_mdpf_wsc_inflection_feeder.py:28` (inf) · `build_mdpf_wse_49f_non_model_aua.py:65` (49f) |
| `etf_net_assets` | `:168` | `build_mdpf_wsd2_etf_netassets_feeder.py:25` |
| `partner_held_etf` | `:177` | `wsd_partner_held_etf.py:42` (49f) · `wsc_inflection_held_etf.py:45` (inf) |

**Denominator:** 5 of 5 feeder artifacts resolved to a writer. 0 unresolved.

## 3. Provisional-set disposition — PER ITEM (criterion 9)

States: `SOURCE-VISIBLE-READER-FOUND` · `NO-SOURCE-VISIBLE-READER` · `NOT-DETERMINABLE` (+reason).
**`NOT-DETERMINABLE` is not `NO READER`.**

### R1 — `wsb-49f-model-aua-daily` → **SOURCE-VISIBLE-READER-FOUND. DO NOT RETIRE.**

Script `data/mdpf/scripts/feeders/wsb_49f_smartx_model_aua.py`, writes
`mdpf/feeds/model_aua_positions/49financial/{date}.parquet` (`:247-248`).
Reader: `mdpf_aggregate_aua.py` `load_feeders` → `read_feeder_s3("model_aua_positions", …)`.
It is **required to calculate a PORT row**, which is 02's own port test. It is not legacy.
*The graph reported zero here (§1b). The zero is wrong.*

### R2 — `wsd-49f-partner-held-etf-daily` → **SOURCE-VISIBLE-READER-FOUND. DO NOT RETIRE — and its absence is FAIL-GREEN.**

Script `data/mdpf/scripts/feeders/wsd_partner_held_etf.py`, writes
`mdpf/feeds/partner_held_etf/49financial/{date}.parquet` (`:42`, put at `:194`).
Reader: `mdpf_aggregate_aua.py` → `build_etf_decomposition(..., partner_held=...)` `:414`.

**Retiring this does not fail. It silently changes the number.** From the function's own docstring
(`:420-427`) and body:

- `partner_held = partner_held or {}` — absence is a legal empty dict, no raise.
- override path: `if (firm_id, etf) in partner_held: held_by_partner[firm_id] = partner_held[(firm_id, etf)]`
- estimate path: `held = model_aua * float(row["target_weight"])`
- docstring, verbatim: *"The estimate stays the fallback where no override row ships"* … *"This makes
  identity_2 a measurement, not an estimate (CTO ruling iii): empirically the target_weight estimate
  ran ~1-3% high."*

So retirement reverts `identity_2` from a **measurement** to an **estimate the code itself records as
running ~1-3% high**, with no error and no log of degradation. The enabling mechanism is
`_empty_feeder()` `:217-219`, which returns an empty frame carrying exactly the right columns
*"so every downstream op is total"* — absence is silent **by design**.

**Same shape as the `pandas_market_calendars` finding: a dependency whose absence degrades rather
than raises.** Two instances in one closure is a pattern, not a coincidence: this pipeline's
house style is total-by-construction readers, which converts every missing input into a quiet
number change.

### R3 — `s3://opal-data-mdpf/mdpf/feeds/*` → **SOURCE-VISIBLE-READER-FOUND. Live prefix.**

Reader `mdpf_aggregate_aua.py:239-268` (paginated `list_objects_v2` + `get_object` per key).
Writers: the six feeder scripts in §2. **Denominator: 5/5 artifacts have both a reader and ≥1 writer.**
Not a retirement candidate while `mdpf_aggregate_aua` is a PORT row.

### R4 — feeder computations used by `mdpf_aggregate_aua.py` → **SOURCE-VISIBLE-READER-FOUND (all six).**

`wsb_49f_smartx_model_aua.py` · `wsc_inflection_held_etf.py` · `wsd_partner_held_etf.py` ·
`build_mdpf_wsc_inflection_feeder.py` · `build_mdpf_wsd2_etf_netassets_feeder.py` ·
`build_mdpf_wse_49f_non_model_aua.py`.
02's own instruction applies: *"If a feeder is required only to calculate `_aggregate_aua`, port the
calculation into the one Lambda; do not preserve a separately scheduled feeder without a
consumer-level reason."* → **port the computation, retire the separate schedule** — that is a
different act from retiring the capability, and the two must not be conflated in the ledger.

### R5 — any captured script used as a library or imported source → **NOT-DETERMINABLE — PENDING CAPTURE.**

Reason: requires AE~Z's P0-7 capture. Repo source cannot answer it — that is the whole point of
criterion 1. **Not** a zero-reader finding.

## 4. Repo-source closure (diff baseline for the capture)

AST-derived, all nesting depths. **Denominators:** 10 entrypoints seeded · 14 files parsed ·
124 import edges · 14 local modules · **0 unresolved**.

14 modules / **9,442 lines** across **three** directories — vs the pack's implicit 7 modules / 6,158
lines. **The real closure is 53% larger and spans a second repo tree.**

Modules nobody had named, pulled in transitively (MSTR~Z's "library or imported source" class):

| module | lines | tree | note |
|---|---:|---|---|
| `build_dim_model_portfolio.py` | 445 | assets/gold | one importer is FUNCTION-SCOPED (`slice:350`) |
| `validate_interpolated_backfill.py` | 129 | assets/gold | |
| `rebalancer_schemas.py` | — | assets/**silver** | a silver-tier module imported into gold |
| `mdpf_revamp_model_crosswalk.py` | 371 | mdpf/gold | |

**Third-party (6):** `boto3` · `numpy` · `pandas` · `pandas_market_calendars` · `pyarrow` · `yaml`.

**Instrument caveat, recorded because it nearly bit:** a closure tool reports "third-party" for
anything it cannot locate, so **an unresolved LOCAL module and a real pip package produce identical
output.** `rebalancer_schemas` first appeared as third-party purely because it sat outside the two
directories searched. Caught on shape (absent from `requirements.txt`, wrong for PyPI naming), then
resolved to `data/assets/scripts/silver/`. Anyone reading a `vendored_modules` list needs this.

**Function-scoped import edges: 6** — invisible to any top-of-file scan.

## 5. Cottonwood's L2 producer (criterion 5 — CLOSED, accepted by COO~Z 205641Z)

`data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` → `SLICE_KEY` `:98`, `put_object` `:945`,
delivery-verified by `head_object` `:946-951`, writing
`s3://opal-data-assets/gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json` — the exact object
`build_mdpf_spine.py:103` emits as bytes verbatim.

A **family of three** with a real ordering constraint (`interpolated_backfill` → `slice` → spine):
`build_cottonwood_mdpf_slice.py` (956) · `build_cottonwood_mdpf_pair.py` (510, put `:388`) ·
`build_cottonwood_interpolated_backfill.py` (748, put `:736`).

**Bidirectional coupling, on a private symbol.** `build_cottonwood_mdpf_pair.py:64-65` imports
`_distribution_stats` (**private**) from `dim_mdpf_account_distribution` and
`calc_metric`/`quarter_ends` from `dim_mdpf_aum_metrics`, via a relative `sys.path` hop at `:59`.
A P1-1 refactor of the MDPF module breaks Cottonwood **across a tree boundary with no import-side
signal in the MDPF tree.**

## 6. A measured break in the planned zip layout

`build_dim_model_portfolio.py:66`:

```python
sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts/silver")
```

Exercised both layouts, positive control first:

| `__file__` | derived path | `isdir` |
|---|---|---|
| repo `.../data/assets/scripts/gold/build_dim_model_portfolio.py` | `.../data/assets/scripts/silver` | **True** (control passes) |
| `/var/task/build_dim_model_portfolio.py` | `/var/task/build_dim_model_portfolio.pyscripts/silver` | False |
| `/var/task/gold/build_dim_model_portfolio.py` | `/var/task/gold/build_dim_model_portfolio.pyscripts/silver` | False |

Flat vendoring at zip root has no `scripts` segment, so `rsplit` returns the whole path.
`sys.path.insert` does not raise on a nonexistent directory, so the failure surfaces later as
`ModuleNotFoundError` — and via the slice the import is function-scoped (`:350`), so it **waits for
the Cottonwood leg to run.** Fix belongs to P1-1 (this seat), not to AE's packaging.

**Basename collision check: CLEAR.** Denominator 45 `.py` across the three source dirs (20/7/18);
duplicate basenames **0**; positive-controlled (the same pipeline fed a synthetic duplicate printed it).

## 7. Tool-interface gap (Rule 21 report to COO~Z)

The TO's `<compiler_tools_mandate>` Phase 2 says `comp-pipescript consumers <artifact key>`.
**`consumers` takes a SCRIPT name, not an artifact key** — an S3 key argument is rejected
(`Unknown script: MDPF/FEEDS/PARTNER_HELD_ETF`, and note it upper-cased the argument).
Not a tool defect; a mandate/interface mismatch. Reported rather than worked around.
Artifact-key questions were answered by literal-key retrieval with printed denominators and positive
controls instead.

## 8. Rows for CVO~Z (P0-6 alignment)

Prefixes CVO~Z asked for, and the bucket answer that matters to their verdict:

- R1 `wsb-49f-model-aua-daily` → `s3://opal-data-mdpf/mdpf/feeds/model_aua_positions/49financial/`
- R2 `wsd-49f-partner-held-etf-daily` → `s3://opal-data-mdpf/mdpf/feeds/partner_held_etf/49financial/`
- R3 → `s3://opal-data-mdpf/mdpf/feeds/*`

All three are **`opal-data-mdpf`** — **not** `opal-data-bd` and **not** `opal-data-inf`, the only two
buckets with read data-event coverage. **CVO~Z's `NOT-OBSERVABLE` verdict holds for these rows; no
re-measurement is available.** Rows added by this census beyond CVO~Z's eight: **none** — but note R1
and R2 are now `SOURCE-VISIBLE-READER-FOUND`, so they are **no longer deletion candidates at all**,
which changes what an external declaration on them is even for.

## 9. Scope bounds held

- **H10 NOT closed.** No reserved word appears on any absence claim here.
- Vendored `trading_calendar.py` copies under `bd-served-vintage-alarm`, `inf-etf-ownership-daily`,
  `opal-assets-absence-check` — **not touched, not bound, not swept.** Other pipelines, WS-1's scope.
- **Nothing deleted.** This document dispositions; it does not retire.
- One scope question routed, not adjudicated: `build_cottonwood_mdpf_slice.py:87-93` imports the shim
  being retired and computes `trading_days_behind_settled_frontier` `:801`. It is inside MDPF's port
  scope and is not one of CTO~Z's three bounded-out pipelines. Asked to be **stated, not inferred.**
