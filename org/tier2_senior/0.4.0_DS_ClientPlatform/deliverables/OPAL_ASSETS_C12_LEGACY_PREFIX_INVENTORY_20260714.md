# OPAL_ASSETS C12 — Legacy Prefix Inventory

**TO:** `OPAL_ASSETS.C12.legacy-prefix-inventory` · **Author:** `0.4.0_DS_ClientPlatform`
**Enumerated:** 2026-07-14 ~01:35Z · **Spec of record:** `OPAL_ASSETS_CONSOLIDATION_PRD.md` v1.3.2
**Method:** full `list-objects-v2` pagination, every bucket, **no sampling**. Denominators printed.
**Deletions performed: ZERO. Deletions proposed-as-performed: ZERO. Lifecycle rules touched: ZERO.**

---

## 0. READ THIS BEFORE YOU DELETE ANYTHING — the `01_raw` finding

> ## ✅ RULED BY ANDREW, 2026-07-14 ~01:46Z (PRD v1.3.5, `27841e6ab`)
> **Verbatim: *"We can keep those unique files in bronze, bring them over in migration."***
>
> **Disposition: `MIGRATE-257-THEN-RETIRE-PER-SEQUENCE`.** The 257 pre-floor objects — including the
> **121 RLD realized-lot tax files** — are **KEPT BY RULING**. They migrate into the monolith with the
> rest of bronze; the folder retires only afterwards, behind the consumer repoint, on a final Andrew
> confirm. Execution is `0.6.2_AE_PartnerETL`'s (C3 scope addition).
>
> **The measurement below stays even though the question is answered** — it is the evidence the eventual
> delete-confirm gets audited against. A resolved question with its evidence deleted is a question that
> re-opens later with nothing to answer it.

**What follows is the finding as it stood before the ruling.** It is retained because the *reasoning* is
the audit trail, not just the answer.

> ### The PRD contradicted itself about the same 257 objects, and **the later ruling was the destructive one.**

| Where | What it says |
|---|---|
| **Ruling 6** (PRD line 315–323) | Andrew ruled `01_raw` **disposable**; NOT migrated into bronze; retirement sequenced behind consumer repoint. Directs this inventory to change its entry *from* "irreplaceable — copy-only" *to* "Andrew-ruled disposable." |
| **The C12 row** (PRD line 365, never updated) | "257 objects Schwab can no longer serve (REST floor 2023-07-12) — **irreplaceable**; migration is a COPY job, never a re-pull, **and never a delete**." |

Both are live text in the spec of record. They cannot both hold. Do not migrate it *and* eventually
delete it, and 257 objects cease to exist.

**`latest + most-restrictive binds` does not arbitrate this — the LATEST ruling and the MOST-RESTRICTIVE
one point in opposite directions.** That is precisely the shape a rule cannot resolve and a human must.

### Grounded (full enumeration, 2026-07-14)

```
opal-data-schwab/01_raw/            7,142 objects        (matches the PRD's 7,142 exactly)
  pre-floor   (business date <  2023-07-12)     257      business dates 2023-01-17 .. 2023-07-11
  post-floor  (business date >= 2023-07-12)   6,885
  pre-floor composition:  RLD 121 · TCF 120 · RLY 6 · RTY 6 · RLU 2 · RTU 2   (121 distinct dates)
```

### The decisive test — is that data preserved anywhere else? **No.**

```
08242234/bronze/    1,578 objects   business dates 20230712 .. 20260710   PRE-FLOOR OBJECTS: 0
08335338/bronze/    6,932 objects   business dates 20230712 .. 20260710   PRE-FLOOR OBJECTS: 0

set-difference, the 257 pre-floor (date, type) pairs vs BOTH bronze trees:
    also present in bronze ............   0
    PRESENT ONLY IN 01_raw ............ 257     <-- a delete destroys these, permanently
```

**Both independent full-history REST pulls bottom out at exactly `20230712`.** That is what a hard API
floor looks like, and it corroborates 0.6.2's floor measurement from a direction nobody aimed at it.

### Why the ruling's premise is false for exactly these 257

Andrew, verbatim: *"we do not care about 01_raw, that entire folder can be deleted… **what we are getting
here** is more important, and will be the canonical form."*

"What we are getting here" is the REST pull. **The REST pull cannot return anything before 2023-07-12.**
So the premise — that the new canonical form *supersedes* `01_raw` — is **true for 6,885 objects and
false for 257.** He ruled that the replacement is a superset. For these 257 it is not, and there is no
evidence in the record that he was told so when he ruled.

**121 of the 257 are `RLD` — realized-lot detail, the primary realized-lot TAX source (`B_02
canonical_lots`). That is 121 business days of realized gain/loss history, Jan–Jul 2023, reconstructable
from nothing.**

### Disposition — RULED (was: pending Andrew)

`01_raw` = **`MIGRATE-257-THEN-RETIRE-PER-SEQUENCE`** (Andrew, 2026-07-14; PRD v1.3.5 `27841e6ab`).
The recommendation put to him — *copy the 257 first (additive, cheap, reversible), then retire* — was
adopted. The copy is all three of those things; the delete is none of them.

> **A document that resolves a contradiction by taking the later ruling is how the irreversible thing
> happens.** This inventory refused to do that: it carried the ruling **and** the fact that falsified
> it, adjacent and unresolved, until a human with the authority to decide actually decided.
>
> **The choice was never Andrew's to get wrong — it was ours to surface.** He ruled to keep the files
> within the hour of being shown that his own premise ("what we are getting here… will be the canonical
> form") was true for 6,885 objects and false for 257. Nobody had told him. That is the whole job.

---

## 1. How to read the date columns — they are two different clocks

**`written`** is the S3 `LastModified` (when the *object* landed). **`business`** is the date *inside* the
data. **They are not the same and the gap is not small:** `01_raw` was *written* 2025-11-14 → 2026-07-07
but *contains* business dates 2023-01-17 → 2026-07-06. Quoting a write-time as data coverage
misrepresents every row under it. `business` is stated only where it is derivable from the key; elsewhere
it is `—` (an explicit gap, not an assumption).

**Disposition classes** (PRD v1.3, §2b): `MONOLITH` migrates into `opal-data-assets` · `PLATINUM-HOME`
permanent stay-put (the ADVI partner serving structures) · `RETIRE-SEQ` retirement sequenced behind a
consumer repoint · `ACTIVE-PIPE` a live non-OPAL_ASSETS pipeline, out of this consolidation's scope ·
`OPS` operational//scratch, no data claim.

---

## 2. `opal-data-schwab` — **STAGING** (PRD ruling 9). 35,947 objects · 386.0 GB

> **ADDENDUM 2026-07-17 — WP8-DECOM:** Andrew ordered the whole `opal-data-schwab` bucket
> **decommissioned** (2026-07-16, 0.5.0's record 163256Z; consumer census @ `ee59022d1`, staged D0–D6).
> Every row below is now governed by that decommission's staged sequence, which supersedes the per-prefix
> RETIRE-SEQ pacing here (the disposition CLASSES stay correct; the schedule is WP8-DECOM's). Known
> bd-gold consumer: `B_02.canonical_lots` reads the UPPERCASE `silver/ULN` tree — its re-point is
> WP8-DECOM cell 4 (this serial), blocked on the D2 redirect-target ruling. Zero deletions by this doc.

| Prefix | Objects | Size | written | business | Disposition | Replaced by |
|---|---:|---:|---|---|---|---|
| **`01_raw/`** | **7,142** | 178.2 GB | 2025-11-14 … 2026-07-07 | **2023-01-17 … 2026-07-06** | **MIGRATE-257-THEN-RETIRE-PER-SEQUENCE** — Andrew-RULED 2026-07-14 (§0) | C3(b) REST pull for 6,885; **the 257 pre-floor migrate as bytes** (C3, `0.6.2`) |
| `backfill/` | 6,935 | 13.4 GB | 2026-07-13 | — | RETIRE-SEQ (superseded by the canonical bronze remap) | C3(a) |
| `08335338/` | 6,932 | 13.4 GB | 2026-07-14 | 20230712 … 20260710 | **MONOLITH** → `assets/schwab/08335338/bronze/…` | C3(a) |
| `_archive/` | 3,988 | 75.4 GB | 2026-04-01 | — | RETIRE-SEQ | — |
| `02_anonymized/` | 3,221 | 81.6 GB | 2025-12-11 | — | RETIRE-SEQ | — |
| `03_mappings/` | 3,193 | 0.8 GB | 2025-12-11 | — | RETIRE-SEQ | — |
| `08242234/` | 1,608 | 2.1 GB | 2026-07-13 … 2026-07-14 | 20230712 … 20260710 | **MONOLITH** → `assets/schwab/08242234/bronze/…` | C3(a) |
| `silver/` | 1,516 | 1.1 GB | 2026-03-31 … 2026-05-11 | — | RETIRE-SEQ — **superseded by C6** | C6 |
| `03_silver/` | 1,005 | 0.1 GB | 2026-03-31 … 2026-05-11 | — | RETIRE-SEQ — superseded by C6 | C6 |
| `bronze/` | 331 | 17.6 GB | 2026-04-01 … 2026-07-07 | — | RETIRE-SEQ (pre-master-first grammar) | C3(a) |
| `01_raw_quartz_validation/` | 54 | 2.5 GB | 2026-06-29 … 2026-07-10 | — | OPS | — |
| `_ops/` | 22 | ~0 | 2026-07-02 … 2026-07-14 | — | OPS | — |

⚠ **`08242234/` and `08335338/` are MOVING TARGETS.** Two `ls` calls seconds apart returned 1,056 then
1,081 objects under `08242234/bronze/`: the full-history REST pull is **actively landing objects**. Every
count in these two rows is a **timestamped reading, not a fixed denominator.** Per PRD ruling 13b the C3
migration denominator is **enumerated at run time** — do not use this table as an acceptance target.

⚠ **`silver/` + `03_silver/` (2,521 objects) were produced by `read_schwab_raw()`** — the reader that
silently drops the D2 account-balance section of every RPS file (see §5). Their completeness is
**UNVERIFIED and UNSCOPED** (scoping is a held verb). They are marked superseded-by-C6, not sound.

---

## 3. `opal-data-inf` — 88,244 objects · 36.2 GB · **INF CHAIN IS HELD**

Orion/Eclipse bronze is a **read-only source** for C6. Nothing in this consolidation writes here.

| Prefix | Objects | Size | written | Disposition |
|---|---:|---:|---|---|
| `bronze/` | 25,693 | 22.7 GB | 2026-04-21 … 2026-07-13 | **SOURCE — mirrors into MONOLITH** (C2); original stays |
| `gold/` | 21,709 | 1.6 GB | 2026-04-21 … 2026-07-13 | ACTIVE-PIPE — serving layer stays put (ruling 9) |
| `silver/` | 15,107 | 6.2 GB | 2026-04-29 … 2026-07-13 | ACTIVE-PIPE |
| `backup/` | 8,806 | 0.4 GB | 2026-07-13 | OPS |
| `platinum/` | 8,543 | ~0 | 2026-04-24 … 2026-07-10 | **PLATINUM-HOME** — permanent stay-put |
| `_pre_rebuild_backup/` | 6,061 | 5.3 GB | 2026-06-30 | OPS |
| `qa/` `code/` `diagnostic/` `telemetry/` `otp/` `config/` `_toolprobe_scratch/` `_compare/` `_rebuild_status/` | 2,302 | ~0 | — | OPS |
| *(empty-name prefix)* | 339 | ~0 | 2026-05-06 | **OPS — see gap G2** |
| `orion/` | 21 | ~0 | 2026-04-28 … 2026-07-13 | SOURCE (C2) |
| `eclipse/` | 1 | ~0 | 2026-06-24 | SOURCE (C2) |

> **`gold/meta/pipeline-complete.json` is NOT written by anything in this consolidation.** It is the INF
> spine sentinel; hand-writing it dispatches the runner and releases the held INF chain by the back door.
> Named here so the inventory cannot be mistaken for permission.

### 3a. ADDENDUM 2026-07-17 — ruling-20 measured disposition (the 257 method) + ruling-16 labels

**Author:** `0.4.0_DS_ClientPlatform` · **Measured:** 2026-07-17 ~16:3xZ · **Method:** full
`list-objects-v2` pagination per prefix (boto3, no console-encoding loss), (date × type) set-difference
per PRD v1.4.4 ruling 20(ii). **Zero writes to S3. Zero deletions.** Note the INF-hold banner on §3 is
HISTORICAL — the hold ended 2026-07-16 (daily dispatch restored); this addendum's measurements are
post-restoration.

**Denominators:** `bronze/orion-api/` **15,602** obj · `bronze/orion-api-v2/` **187** obj ·
`bronze/orion/` **21** obj · flat generation: `assets/` 4,539 · `positions/` 4,548 · `transactions/`
110 · `performance/` 105 obj. Raw evidence JSON: session scratchpad `c12_setdiff_result.json`
(full per-type date lists; summary reproduced here in full).

#### The ruling's premise is FALSIFIED by the measurement: two of the three "legacy" prefixes are LIVE

Ruling 20 classed `orion-api/`, `orion-api-v2/`, `orion/` as **legacy date-dir generation**. Measured:

| Prefix | Last write | Verdict |
|---|---|---|
| `bronze/orion-api/` | **2026-07-17 (today)** — tax_realized/tax_unrealized/billing/performance_dim/accounts_roster/_BRONZE_COMPLETE all carry today's date-dir | **LIVE PRODUCER TARGET, not legacy** |
| `bronze/orion-api-v2/` | **2026-07-17 (today)** — `household_rep_mapping.json` + `representatives.json` daily since 2026-04-29 (75 dates) | **LIVE for the two JSON types**; parquet types dead since 2026-04-30 |
| `bronze/orion/` | 2026-04-29 — 2 date-dirs of GUI SlickGrid/trn CSV exports | genuinely dead legacy |

A retire-with-pipeline disposition **cannot attach to a prefix a live producer writes daily.**

#### Set-difference (date × type-name) vs the flat generation — UNIQUE CONTENT IS MASSIVE

`bronze/orion-api/` unique-by-name types (no flat counterpart exists at all): **`tax_realized.csv`
2,090 dates (2020-01-01…2026-07-17)** · **`tax_unrealized.csv` 2,117 dates** · **`billing.csv` 1,577
dates** · `unified_account_dim.csv` 72 · `new_portfolio_accounts.json` 73 · `accounts_roster.json` 6 ·
`geo_verify.csv` 1 · markers/completion sentinels (~4,710 obj, non-data). Name-matched types with dates
ABSENT from flat raw: `performance_dim.csv` **2,146 of 2,200 dates** · `transactions.csv` **1,512 of
1,564 dates** · `assets.csv` 0 (fully covered). `bronze/orion-api-v2/` unique: `household_rep_mapping.json`
+ `representatives.json` 75 dates each; its parquet types are covered by flat (0–1 date diff).
`bronze/orion/`: both types unique (flat `transactions/` raw starts 2026-05-12; these are 2026-04
GUI exports).

**Caveat stated per the instrument:** the set-difference keys on **type-NAME equivalence** across
generations (e.g. `performance_dim.csv` ↔ flat `performance/`); content-level identity was NOT verified.
That is the measurement ruling 20 prescribed, and the honest limit of it.

#### Disposition per ruling 20(ii) — ANDREW-CLASS CARVE-OUT, routed via CTO/COO

> "ANY unique content → the carve-out goes to ANDREW — and since these prefixes trace to INF producer
> lineage, a unique-content disposition is Andrew-class regardless."

All three prefixes hold unique content; two are additionally LIVE. **No retire-with-pipeline class is
assigned to any of the three.** Disposition rows: `orion-api/` = `LIVE PRODUCER TARGET + unique content
— Andrew-class` · `orion-api-v2/` = `LIVE (2 JSON types) + unique content — Andrew-class` · `orion/` =
`dead GUI-export remnant + unique content — Andrew-class`. This TO performs zero deletions; the C2 map
ruling (flat-generation mirror) is unaffected.

#### Ruling-16 labels — `coerced-only survivor — NOT imported` (re-measured 2026-07-17)

At the 2026-07-14 measurement: 3 assets + 7 positions dates, accruing +1/business day. **Post
INF-restoration (07-16) the meter has STOPPED and partially reversed** — flat raw runs through
2026-07-17 for all four types. Current coerced-only survivor set, **9 dates**, each inventoried
`coerced-only survivor — NOT imported`:

- `assets`: 2026-07-11 · 2026-07-12 · 2026-07-13 · 2026-07-14 · 2026-07-15 (5)
- `positions`: 2026-07-01 · 2026-07-03 · 2026-07-04 · 2026-07-05 (4)
- `transactions` / `performance`: 0

These stay resident in `opal-data-inf`; importable later ONLY by explicit ruling into a labelled
`_coerced/` prefix (ruling 16 verbatim). The monolith shows honest holes on these dates.

---

## 4. The remaining buckets

### `opal-data-bd` — 112,872 objects · 83.3 GB · **49F SOVEREIGN HOLD**
**METADATA ENUMERATED ONLY** under the OPAL_ASSETS scoped lift. No disposition is assigned to bd custody
data: it is **out of this consolidation's authority.** Largest prefixes: `gold/` 70,282 · `platinum/`
23,593 · `silver/` 7,750 · `schwab/` 3,851 · `logs/` 3,245 · `smartx/` 1,381.

- **`smartx/` (1,381 obj)** → **MONOLITH**, and it is a *firm-boundary* item, not a tidiness one: SmartX
  is Opal's own model platform sitting in a held custody bucket (PRD ruling 10). The JWT park
  (`smartx/jwt/current.json`) retires to Secrets Manager. Owner: C5.
- **`ajb_workspace/` (703 obj, 2026-02-23)** — a *repo tree* in a client-custody bucket. Flagged, not
  touched. **Not mine to dispose of.**
- Everything else here: **NO DISPOSITION — HELD.** Not a gap in the inventory; a boundary of it.

### `opal-data-cot` — 5,294 objects · 0.7 GB · separate firm (never mirrored to bd)
`gold/` 3,180 · `platinum/` 1,115 (**PLATINUM-HOME**) · `silver/` 361 · `forwardfill_v2/` 273 ·
`logs/` 229 · `code/` 106 · `bronze/` 29 (**SOURCE → MONOLITH**, C2) · `blackdiamond/` 1.
Cot positions cube is C10's input (derivation code only; **no cohort row emitted**).

### `opal-data-etfs` — 530 objects
`silver/` 356 · `daily/` 124 · `snapshots/` 32 · `_cloudprobe/` 5 · `platinum/` 5 · `bronze/` 4 ·
`monthly/` 2 · `config/` 1 · root 1.
⚠ **`_cloudprobe/` is the LIVE PARITY QUARANTINE** for the ETF laptop→cloud cutover (parity 2/3 and 3/3
land 07-14 / 07-15). **THE LAPTOP STAYS ON.** Disposition: **MONOLITH** (C4) — *after* parity 3/3, never
before. Nothing in this inventory authorises touching it.

### `opal-data-smartx-v2` — 1,682 objects
`exports/` 1,386 · `archive/` 143 · `logs/` 73 · `views/` 26 · rest ≤20 each.
Disposition: **RETIRE-SEQ** — the legacy EC2 scrape chain is superseded by the C5 REST reconstruction.
**`smartx-daily-export-trigger` is NEVER re-enabled** (PRD C5). Retirement sequence: inventory → parity →
decommission. Nothing retired here.

### `opal-data-mdpf` — 1,608 objects
`mdpf/` 1,455 · `telemetry/` 114 · `code/` 28 · `bmkaud-evidence/` 10 · `cache/` 1.
Disposition: **ACTIVE-PIPE**, dissolves at P3 when the emitter reads only `opal-data-assets` (C11).
⚠ The AUM table is **correctly idle**, frozen behind our own chokepoint — *not broken*. The emitter is
event-driven on the INF spine sentinel. **Do not "fix" it by writing that key** (Door 6).

### `opal-data-portal-v2` — 3,486 objects
`json/` 954 · `security-reports/` 606 · `platinum/` 439 (**PLATINUM-HOME**) · `json-tiered/` 375 ·
`data-refresh/` 373 · `assets/` 190 · `canon/` 178 · `infrastructure/` 178 · `benchmarks/` 107 · 19 more ≤25 each.
Disposition: **PLATINUM-HOME / ACTIVE-PIPE — the serving layer stays where it is** (PRD ruling 9: "gold
runners + platinum buckets stay put for the ADVI partner structures"). **Nothing in portal-v2 migrates.**

---

## 5. Cross-cutting: two defects this enumeration surfaced

1. **`read_schwab_raw()` silently drops the D2 account-balance section of every RPS file** (6.4% of rows:
   3,932 of 61,786 on the file measured). It selects data rows by *most-common prefix* — asking which
   prefix is most **popular** rather than which rows are **data**. In held code (`data/canonical/schwab/
   silver/*`): **REPORTED to CTO, NOT FIXED, NOT VERIFIED, propagation UNSCOPED, materiality
   UNSPECULATED.** Superseded by C6 (migrate-on-next-touch). Taints `opal-data-schwab/silver/` +
   `03_silver/` (2,521 objects) with unverified completeness.
2. **Schwab attests its own row count in every file's `T1` trailer** and nothing in the estate read it.
   Now a required hard-raise on every monolith Schwab parser (**PRD v1.3.2 ruling 11a**, landed
   `44a5328ce`). A parser that misses a section cannot tie to the trailer.

3. **⚠ THE RULE 17a VIOLATION IN `opal-data-inf/bronze/` IS NOT HISTORICAL — IT IS ONGOING, AND IT LOSES
   ONE MORE DAY EVERY DAY.** Measured live 2026-07-14:

   | feed | raw `.jsonl.gz` | `.parquet` | consequence |
   |---|---:|---:|---|
   | `assets` | 2,265 — ends **2026-07-10** | 2,268 — runs to **2026-07-13** | **3 dates parquet-only** |
   | `positions` | 2,265 — ends **2026-07-10** | 2,272 — runs to **2026-07-13** | **7 dates parquet-only** |

   **The RAW producer died 2026-07-10. The PARQUET producer is still running.** For those dates the raw
   feed is **unrecoverable** — a parquet ingest coerces schema/dtypes at ingest, which is exactly the
   irreversibility Rule 17a exists to prevent (*"each layer has exactly one job; doing a later layer's
   job early is IRREVERSIBLE"*). Consistent with the known two-parallel-producers condition; **the
   quantification and the still-accruing loss are the new part.**

   **C6's parsers REFUSE a `.parquet` under `bronze/`** (`raw_json_reader.assert_raw_key`, mutant-
   exercised). A parquet-only date is reported **UNCONVERTIBLE**, never silently converted — reading it
   would launder an irreversible defect into the monolith and the result would look sound.

   **OPEN ARCHITECTURE FORK for CTO (surfaced, not adjudicated):** what does the C2 ingest-router mirror
   into the monolith for those dates — the raw that does not exist, or the parquet that violates 17a?
   Both answers are bad; only one is *ours to choose*. The INF chain is HELD, so nothing here touches
   the producer.

---

## 6. Explicit gaps — what this inventory does NOT establish

| # | Gap | Why it stays a gap |
|---|---|---|
| **G1** | The **REST floor (2023-07-12)** is 0.6.2's MEASURED claim, corroborated by both bronze trees bottoming out there. **I did not verify it against the Schwab API.** | Calling the vendor is **egress**; I do not have Andrew's per-use word. Corroboration is not confirmation, and I am not writing it as source-confirmed. |
| **G2** | `opal-data-inf` has **339 objects under an empty-name top-level prefix** (keys beginning `/`). | Not characterised. Flagged, not touched — INF is held. |
| **G3** | Whether the D2 drop propagated into **served** silver/gold, and its materiality. | Scoping the blast radius is **itself a held verb** (CTO's standing instruction). "Unknown, unverified, held" is the complete and correct sentence. |
| **G4** | Business-date ranges for prefixes whose keys do not carry a date. | Derivable only by opening objects. Not guessed — left `—`. |
| **G5** | `opal-data-bd` disposition beyond the two flagged prefixes. | 49F sovereign hold. A boundary, not an omission. |

---

## 7. Acceptance criteria

| AC | Status |
|---|---|
| 1. Per-prefix counts + date ranges + disposition + replacing-TO cross-ref | **MET** — §2–4, full enumeration, no sampling, denominators printed |
| 2. Zero delete/lifecycle operations performed or proposed-as-performed | **MET** — zero. §0 *recommends against* a delete and routes the decision to Andrew |
| 3. Session log + Compiler Tools; RAVC close | Log at session close; RAVC evidence to COO, §0 escalation to CTO |

**Totals enumerated: 249,663 objects across 8 buckets, 125 top-level prefixes.**
