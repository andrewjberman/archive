# OPAL_ASSETS C12 — Legacy Prefix Inventory

**TO:** `OPAL_ASSETS.C12.legacy-prefix-inventory` · **Author:** `0.4.0_DS_ClientPlatform`
**Enumerated:** 2026-07-14 ~01:35Z · **Spec of record:** `OPAL_ASSETS_CONSOLIDATION_PRD.md` v1.3.2
**Method:** full `list-objects-v2` pagination, every bucket, **no sampling**. Denominators printed.
**Deletions performed: ZERO. Deletions proposed-as-performed: ZERO. Lifecycle rules touched: ZERO.**

---

## 0. READ THIS BEFORE YOU DELETE ANYTHING — the `01_raw` finding

> ### The PRD contradicts itself about the same 257 objects, and **the later ruling is the destructive one.**

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

### Disposition recorded here

`01_raw` = **RETIRE-SEQUENCED — WITH A CARVE-OUT PENDING ANDREW.** The 257 pre-floor objects are
**NOT** covered by the disposable ruling's premise and must not ride its authority. Recommended (CTO
holds; Andrew decides): **copy the 257 into the monolith first — additive, cheap, reversible — then
retire the folder.** The copy is all three of those things; the delete is none of them.

> **A document that resolves a contradiction by taking the later ruling is how the irreversible thing
> happens.** This inventory is the checklist the eventual delete will be run from. It therefore carries
> the ruling **and** the fact that falsifies it, adjacent and unresolved, on purpose.

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

| Prefix | Objects | Size | written | business | Disposition | Replaced by |
|---|---:|---:|---|---|---|---|
| **`01_raw/`** | **7,142** | 178.2 GB | 2025-11-14 … 2026-07-07 | **2023-01-17 … 2026-07-06** | **RETIRE-SEQ — ⚠ 257-object carve-out PENDING ANDREW (§0)** | C3(b) REST pull — **for 6,885 of 7,142 only** |
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
