# THE DATA-ENGINEERING BIBLE — PART 1: THE ESTATE PLANE CENSUS

**Author:** 4.0.0_SA_CRO (Chief Research Officer)
**Home:** org/tier1_exec/4.0.0_SA_CRO/
**Date:** 2026-09-12
**Status:** MEASURED INVENTORY. ⛔ **NOT a migration plan. NOTHING MOVES ON THIS DOCUMENT.**
**Commissioned:** Andrew-direct ~16:2xZ 2026-09-12, verbatim *"Our job here is to focus on the plan,
let's start with the census let's start breaking this down"* — spoken alongside his ~16:1xZ pause on
projects actively building data pipelines.

---

## 0. INSTRUMENT, DENOMINATOR, AND WHAT THIS CENSUS CANNOT SEE

**Instrument:** `boto3` `list_objects_v2` / `head_object` / `get_public_access_block`, read-only, run
from this seat 2026-09-12 ~16:3xZ. **NOT** the `comp-find --corpus aws` graph (that is a repo-side
derive with its own vintage); this is the live key plane.

**BUCKET DENOMINATOR: 36 buckets in the account.** All 36 swept. Zero REFUSED.

### ⛔ TWO INSTRUMENTS WERE RUN AND THEY DISAGREED. THAT DISAGREEMENT IS A FINDING.

| instrument | what it certifies | result |
|---|---|---|
| **object sweep** (every key, counted) | object counts, newest/oldest write, format mix | `opal-data-assets` hit a **400,000-key CAP** |
| **prefix walk** (CommonPrefixes only) | the COMPLETE plane list | complete outside two deferred subtrees |

**The capped object sweep MISSED PLANES the prefix walk found.** S3 lists lexicographically, the cap
fell inside `smartx/`, and everything alphabetically later was never reached — so the object sweep
saw **no `smartx/model/*` planes and no `trueshares/*` planes at all**. Both exist.

> ⭐ **A CAPPED SWEEP DOES NOT UNDERCOUNT EVENLY — IT TRUNCATES THE ALPHABET.** The missing planes
> were not a random sample; they were the tail. Had only the object sweep been run, `trueshares`
> would have read as ABSENT from the monolith rather than as unmeasured.

**Therefore, stated precisely:**
- **Plane inventory for `opal-data-assets` is COMPLETE** (prefix walk) except inside
  `smartx/account/` and `smartx/allocation/`, which were deferred deliberately and characterized
  separately in §3.
- **Object counts for `opal-data-assets` are PARTIAL** and are marked `[partial]` wherever quoted.
  No `opal-data-assets` object total appears in this document as a total.
- Every other bucket swept **COMPLETE**, except `opal-cloudtrail-logs-313476888478` (CAPPED, a log
  bucket with zero tier planes — irrelevant to this census).

**NOT MEASURED HERE, and named so it is not assumed:** no CloudFront behaviour was exercised; no IAM
was evaluated; no producer was traced to its output; no file contents were read or diffed. Every
liveness claim is `LastModified`, which says a WRITE happened, never that the write was CORRECT.

---

## 1. THE HEADLINE — FIVE THINGS THE ESTATE ACTUALLY LOOKS LIKE

1. **The "legacy" buckets are the live production estate, not legacy.** `opal-data-bd` (125,653
   objects), `opal-data-inf` (96,774) and `opal-data-cot` (7,047) each carry a COMPLETE
   bronze→silver→gold→platinum stack **written today**. D10-2 is therefore not a cleanup question.
2. **Platinum lives in SIX buckets simultaneously.** Andrew's per-tenancy ruling (`dd9b33de65`) is
   already the dominant reality — it just lives in the OLD-spelled buckets.
3. **SmartX minted 12,432 tier planes by putting a UUID where the scope belongs.** One vendor
   accounts for ~99.6% of the monolith's planes.
4. **`opal-data-49financial` holds gold ONLY.** The same firm's silver, bronze and *served platinum*
   are in `opal-data-bd`. One firm, two buckets, split by tier.
5. **Format law is violated in both directions** — parquet under `bronze/`, JSON under `silver/`,
   and gold that is majority-JSON in the live firm buckets.

---

## 2. THE PLATINUM MAP — six buckets, one tier

| bucket | plane | objects | newest | age | verdict |
|---|---|---|---|---|---|
| `opal-data-bd` | `platinum/` | 24,631 | 2026-09-12 | 0d | **LIVE** |
| `opal-data-inf` | `platinum/` | 8,673 | 2026-09-12 | 0d | **LIVE** |
| `opal-data-cot` | `platinum/` | 1,136 | 2026-09-12 | 0d | **LIVE** |
| `opal-data-portal-v2` | `platinum/` | 576 | 2026-09-12 | 0d | **LIVE** |
| `opal-data-etfs` | `platinum/` | 38 | 2026-09-12 | 0d | **LIVE** |
| `opal-data-demo` | `platinum/` | 22,414 | 2026-06-05 | **98d** | **DEAD** |

⭐ **THE PER-TENANCY PATTERN ANDREW RULED AT 16:0xZ IS ALREADY WHAT THE ESTATE DOES.** Three firm
buckets serve their own platinum today; the shared bucket holds 576. The amendment did not introduce
a new architecture — **it ratified the majority behaviour and named the minority as the exception.**

**The minority is not empty, and it is client data.** Of `opal-data-portal-v2`'s 4,361 objects
(COMPLETE sweep), **34 are firm-identifiable** by whole-segment match:

- **13 written 2026-09-12** — `platinum/mdpf/{49financial,cottonwood,inflection}/*.json`. **LIVE
  non-conformance** against the rule amended the same hour.
- **19 dated 2026-08-21 / 09-01** — `platinum/advi/49financial/*`, including `perfrp_book_advisor.json`
  (15.0 MB), `perfrp_gainloss_account.json` (11.9 MB), `perfrp_gainloss_relationship.json` (7.4 MB).
  **INFERRED migration residue** — the `shared-advisor-router` header reads *"v3: origin migrated from
  opal-data-portal-v2 to opal-data-bd"*; the migration moved the ORIGIN and left the BYTES. Not traced
  to a producer, so not asserted as dead.
- **2 dated 2026-05-29** — `json/portfolios/{49financial,inflection}/account-distribution.json`.

⚠ **ON EXPOSURE — DELIBERATELY NOT CLAIMED.** All four public-access blocks on
`opal-data-portal-v2` read `true` (measured). Of 28 CloudFront behaviours only `/json-tiered/*` and
`/auth/*` lack a validator (1.0.0_SA_CTO's measurement, carried not re-derived), and these keys are
under `platinum/`, not `json-tiered/`. **On current evidence these are behind auth and this is a
CONFORMANCE finding, not a security incident.** One question is routed, not chased: `comp-routes`
reports a router refusal scoped to `platinum/**/summary.json` — a 401 block on ONE filename beneath a
prefix holding account-grain gain/loss is worth one deliberate read by whoever owns that surface.

---

## 3. THE SMARTX GRAMMAR BREAK — one vendor, 12,432 planes

The canonical grammar is `{source}/{scope}/{layer}/{type}/{date}/`. SmartX put the **entity UUID**
where `{scope}` belongs:

```
smartx/account/{uuid}/bronze/        7,066 planes      <- one plane PER ACCOUNT
smartx/allocation/{uuid}/bronze/     5,366 planes      <- one plane PER ALLOCATION
smartx/model/{uuid}/bronze/             11 planes      <- one plane PER MODEL
smartx/platform/{bronze,silver}/         2 planes      <- CORRECT: a stable scope name
                                     ------
                                    12,445 planes, 326,734+ objects [partial]
```

**Consequences, measured:**
- **99.6% of the monolith's tier planes are one vendor's UUIDs** (12,445 of 12,498).
- It is why `opal-data-assets` exceeded the 400,000-key cap.
- A per-entity plane cannot carry a hive `date=` partition usefully, so the layer's own partitioning
  contract is unavailable to it.
- `smartx/platform/` proves the correct shape exists **in the same vendor tree**, so this is not a
  vendor constraint. It is a choice that was made once and never revisited.

> ⛔ **THIS IS THE MEASURED FORM OF ANDREW'S "STABLE IDENTITIES" CONCERN.** A UUID is a stable
> identifier; it is not a stable *scope*. Putting an entity id in the position the grammar reserves
> for a scope makes the plane count grow with the DATA rather than with the BUSINESS — which is
> exactly the property a canonical pattern exists to prevent.

**`opal-data-imo` repeats the shape and is dead:** 304 planes on `corp/{company-name}/{tier}/`,
8,700 objects, newest **2026-06-01 (103 days)**.

---

## 4. THE 49 FINANCIAL IDENTITY SPLIT — measured

One firm, **four spellings**, and its tiers split across two buckets:

| where | plane | objects | newest | note |
|---|---|---|---|---|
| `opal-data-49financial` | `gold/` | 25,577 | 2026-09-12 | **the ONLY plane in that bucket** |
| `opal-data-bd` | `platinum/` `gold/` `silver/` `bronze/` | 107,637 combined | 2026-09-12 | the served stack |
| `opal-data-assets` | `blackdiamond/49f/{bronze,silver,gold}` | 5,669 [partial] | 2026-09-12 | |
| `opal-data-assets` | `blackdiamond/49financial/{bronze,silver}` | 114 [partial] | 2026-09-12 | |
| `opal-data-assets` | `blackdiamond/49financial/{bronze_legacy,silver_legacy}` | 8,852 [partial] | 2026-08-25 | **17d, dead** |

**So the firm is `bd` to the router, `49financial` to terraform, `49f` and `49financial` to the
monolith — and its gold is in the new bucket while its served platinum is in the old one.** The
`blackdiamond/49f/gold/` plane holds exactly **1 object, 56 days old**, which is what a
half-completed gold migration looks like from the outside.

---

## 5. FORMAT-LAW CONFORMANCE — violated in both directions

**Rule 17a: parquet under `bronze/` is "an architectural violation, not a format preference."** The
gate is a bucket-policy deny **live on `opal-data-assets` only**; other trees are ungated. Measured
in the ungated trees:

| plane | parquet under bronze | newest |
|---|---|---|
| `opal-data-inf/bronze/` | **4,802** | 2026-09-12 LIVE |
| `opal-data-bd/smartx/bronze/` | **242 (100% of the plane)** | 2026-09-12 LIVE |

**Rule 17: silver is parquet.** JSON found under `silver/`:

| plane | json under silver | newest |
|---|---|---|
| `opal-data-inf/silver/` | **3,066** | 2026-09-12 LIVE |
| `opal-data-cot/silver/` | 89 | 2026-09-12 LIVE |
| `opal-data-assets/blackdiamond/49financial/silver/` | 29 of 58 | 2026-09-12 LIVE |
| `opal-data-bd/silver/` | 7 | 2026-09-12 LIVE |

**Rule 17b as amended: GOLD IS PARQUET.** Gold is majority-JSON in the live firm buckets:

| plane | json | parquet | verdict |
|---|---|---|---|
| `opal-data-bd/gold/` | **44,782** | 26,809 | majority JSON |
| `opal-data-cot/gold/` | **2,856** | 789 | majority JSON |
| `opal-data-49financial/gold/` | 8,859 | **16,067** | majority parquet |
| `opal-data-assets/schwab/08335338/gold/` | 2,108 | 2,108 | **exactly equal — a dual-write twin** |

⭐ **THE ESTATE IS MID-TRANSITION AND BOTH FORMATS SIT SIDE BY SIDE, SOMETIMES 1:1.** This is the
measured form of the gold-format fork Andrew raised. It is not drift from a settled pattern; it is a
transition that was started and not finished.

---

## 6. CONFORMANT — recorded so a sweep does not "fix" what is already right

- **Code beside its gold process.** `code/gold/`, `code/silver/`, `code/bronze/` planes exist in
  `opal-data-bd`, `-cot`, `-inf`, `-mdpf` and `opal-runner-shared`. This is **Andrew's own 2026-08-25
  ruling** (*"this bucket is where the code for said gold process/aggregation/analytics should be as
  well"*), not clutter.
- **`pathfinder/` and `trueshares/` stopping at bronze/silver.** `pathfinder/filepoint/bronze/`,
  `pathfinder/{PFDE,PFOE}/silver/`, `trueshares/{DIVZ,IDVZ}/{bronze,silver}` have no gold or platinum.
  Per Andrew's ~15:5xZ word, data that can be served as ingested needs no derived tiers. **CORRECT,
  NOT DEBT — a conformance sweep must not flag these.**

---

## 7. RESIDUE INSIDE LIVE DATA BUCKETS — ~15,000 objects

| plane | objects | newest | class |
|---|---|---|---|
| `opal-data-inf/backup/gold_canonical_PRE_REDERIVE_20260713T1012Z/` | 8,805 | 2026-07-13 | pre-rederive backup |
| `opal-data-inf/_pre_rebuild_backup/20260630T234458Z/silver/` | 6,060 | 2026-06-30 | pre-rebuild backup |
| `opal-data-assets/_probe/**` (11 planes) | 11 | 2026-07-14 | probe artifacts |
| `opal-data-inf/_toolprobe_scratch/pk/silver/` | 1 | 2026-07-24 | tool scratch |
| `opal-data-bd/logs/gold/` | 2 | 2026-04-01 | 164d |
| `opal-data-bd/canonical/schwab/{silver,gold}` | 484 | 2026-07-24 | 49d |

**No disposition is proposed for any row.** Several are named in standing holds this census did not
re-read.

---

## 8. THE STALE HOLD — surfaced, and the scare story corrected

`org/critical_paths/DO_NOT_DECOMMISSION_portal-v2_json_mdpf_49financial_20260722.md` is marked
**ACTIVE HOLD** and states the key *"IS NOT A LEGACY LEFTOVER… Removing it SILENTLY BREAKS
49Financial account counts."* It names:

`s3://opal-data-portal-v2/json/mdpf/49financial/aggregate-aua-timeseries.json` → **HTTP 404.**

**The 404 is a genuine absence, not a permissions artifact** — this seat's own 4,361-object sweep of
that bucket is the positive control, so ListBucket demonstrably exists.

⭐ **AND THE ALARMING READ IS WRONG.** The same basename exists at
`platinum/mdpf/49financial/aggregate-aua-timeseries.json`, **written today**. The artifact moved
`json/` → `platinum/`; the hold record still names the old path. **INFERRED** (same basename, firm and
product; contents not diffed, producer not traced).

> **A HOLD WHOSE PATH 404s IS WORSE THAN A HOLD THAT IS SIMPLY WRONG.** The next reader either raises
> a false emergency, or concludes the hold is obsolete and clears it. Both are failures, and the
> second one is silent.

---

## 9. WHAT PART 2 NEEDS THAT THIS DOES NOT HAVE

1. **Producer→plane tracing.** Liveness here is `LastModified`. It says a write happened, never that
   the right thing wrote it or that the content is correct.
2. **The two deferred SmartX subtrees**, if a per-plane count is ever needed (the shape is settled).
3. **Re-derivation of `ADVI_APISCP_PRD.md` s.2's routing half.** Its storage half is now
   **FALSIFIED as a description of current state** (§2). Its routing claim — that all portal reads go
   to the partner's origin bucket — has **not** been exercised against live CloudFront.
4. **The scope tick-list for D10-1**, which is Andrew's per-case call and the mechanism he approved.
