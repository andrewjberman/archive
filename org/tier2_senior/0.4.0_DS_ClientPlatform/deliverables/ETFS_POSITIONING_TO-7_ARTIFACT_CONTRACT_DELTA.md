# ETFS_POSITIONING.TO-7 — ARTIFACT CONTRACT DELTA (per-fund as-of)

**Author:** `0.4.0_DS_ClientPlatform~F` · **Date:** 2026-08-28 · **Code vintage:** `25f30acc63`
**Discharges:** `POS-TO7-AC3` (contract half) · **Cells:** `ETFS-e-2`
**Amends:** AE CONTRACT v1 (`org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_POSITIONING_TO-2_ARTIFACT_CONTRACT_v1.md`)
**Served key:** `s3://opal-data-portal-v2/platinum/etfs/positioning_data.json` → `/api/general/etfs/positioning_data.json`

> ⚠ **THIS IS A DELTA FILED BESIDE CONTRACT v1, NOT AN EDIT OF IT.** v1 is `0.7.0_AE_CloudOps`'s
> deliverable and this seat does not write another seat's contract.
>
> ⛔ **ROUTING CORRECTED 2026-08-28 ~02:5xZ. THIS BLOCK FIRST READ "Routed to `0.7.0_AE_CloudOps`
> (owner) ... for fold-in or rejection" AND THAT ROUTING CANNOT BE DISCHARGED FROM SITE Z.**
> `0.7.0_AE_CloudOps~I` refused it and was right; re-measured at source by this seat rather than
> taken on their word:
> ```
> CONTRACT v1 :7            **Owner:** `0.7.0_AE_CloudOps`      <- BASE serial, no lane
> TO-2 face   :9            <placement>LAPTOP (Rule 26).</placement>
> this device               org/mcp/inbox/0.7.0_AE_CloudOps/ holds ~D ~I ~P ~S ~Y ~Z -- lanes only
> ```
> **I named an OWNER without measuring whether that owner is REACHABLE FROM THIS FABRIC.** A
> laptop-placed base serial is not addressable from a `~Z` fabric, and no site-Z AE lane can take
> it: Rule 27 (a second PROJECT on one instance), the `ETFS_INGEST` TO's explicit fence against
> `ETFS_POSITIONING.TO-2`, and Rule 26 placement each independently forbid it.
> ⚠ **AND THE PACKAGE-APPLIER RULING DOES NOT REACH IT** -- `2.0.0_SA_COO~Z` 12179 made one seat the
> single applier of a ZIP; that is an apply authorization and says nothing about owning another
> project's contract document.
>
> ⭐ **DISPOSITION RULED by `2.0.0_SA_COO~Z` (12294), and this is the standing state -- not this
> seat's routing question, which the ruling supersedes:**
> ```
> BLOCKED-BY-PLACEMENT, NOT UNOWNED. FILED, and it RIDES THE NEXT /integrate to the
> fabric that owns it. NOBODY ON ~Z FOLDS IT IN.
> ```
> The issuing office is itself barred from the base-serial row (`0.0.0_AB_MSTR~Z` 11361), and
> Andrew's standing rule is that site Z does not route work to the main fabric. **So the item is
> OWNED -- it is simply owned somewhere this fabric is not.**
>
> ⛔ **IT IS NOT A GATE ON `ETFS_POSITIONING.TO-7` OR ON D4, and the reason is worth stating:**
> this document records a shape change **whose shape is already deployed and verified** -- the
> package is current on all three members and the served bytes match the object. **A contract
> document lagging its artifact is a RECORD gap, not a BUILD gap.** ⚠ **It becomes urgent the
> moment someone reads CONTRACT v1 as current**, which is exactly why it is filed with its
> staleness named rather than left silent.

---

## 1. THE ONE SENTENCE THAT IS THE CONTRACT CHANGE

**`data_as_of` MAY DIFFER ACROSS BOOKS WITHIN A SINGLE PAYLOAD, and a consumer must not
assume otherwise.**

Under contract v1 a consumer could read any book's `data_as_of` and treat it as the page's
date, because the publisher *enforced* agreement — `etf_positioning_publisher.py:403-404`
at `dd75f6bd64` raised `RuntimeError("books disagree on data_as_of")`. That enforcement is
removed, because it fired on exactly the output AC1 specifies.

---

## 2. FIELD-LEVEL DELTA

| field | location | status | meaning |
|---|---|---|---|
| `portfolios.{CODE}.data_as_of` | per book | **SEMANTICS CHANGED** | Was: the run's as-of, identical across books. **Now: the provider's own date for THAT BOOK'S HOLDINGS**, read from the silver `data_as_of` column. **May be `null`** — see AC6 below. This is the ONLY provenance stamp in the payload. |
| `portfolios.{CODE}.as_of_basis` | per book | **NEW** | How that book's date was derived. Enum below. Travels beside the date, never instead of it: a null date is only interpretable with its basis. |
| `portfolios.{CODE}.prior_date` | per book | **SEMANTICS CHANGED** | Now the trading day before **that book's** date, not the run's. `null` when the book has no date. |
| `data_as_of` | top level | **SEMANTICS CHANGED** | Now a **DECLARED DERIVED SUMMARY**: the NEWEST book date. ⛔ **It is NOT a provenance stamp for any individual book.** Kept populated so the existing page-level surface does not break while TO-7 AC4 lands. |
| `data_date` | top level | unchanged in derivation | Mirrors `data_as_of`, as before. |
| `data_as_of_spread` | top level | **NEW** | Sorted list of the DISTINCT non-null book dates. One element is the ordinary day; several is a divergent day. **Emitted always**, so "all books agreed" is a reading rather than an absence. |

### `as_of_basis` enum

| value | meaning | who fixes it |
|---|---|---|
| `row-sourced` | Read from the fund's silver `data_as_of`, single distinct value. The normal case. | nobody — this is health |
| `row-sourced-multi` | The fund's rows carried >1 distinct date; the newest was emitted. | ingest (a silver GRAIN defect) |
| `row-null` | Rows present, provenance column empty or absent. | ingest (a silver POPULATION defect) |
| `absent` | No holdings rows at any candidate partition. `data_as_of` is `null`. | ingestion coverage — **no producer change can clear it** |

Rule 24 record (four postulates, declared domain, uncovered-member hunt) is inline at the
`AS_OF_BASIS_VOCAB` definition in `etf_positioning_gold.py` @`25f30acc63`.

---

## 3. THE RULE A CONSUMER MUST NOT BREAK (AC6)

```
holdings_status == "book_only"   ->  data_as_of IS NULL      (and as_of_basis == "absent")
holdings_status == "full"        ->  data_as_of IS NON-NULL
```

⛔ **A shell carrying a date has BORROWED one** — from the run, or from a neighbouring book.
It renders perfectly and lies about provenance, and no downstream check can see it. Both
directions are **refused in `shape_check()` before a byte leaves**, together with the literal
string `'nan'` (which is what `str()` of a pandas null yields on some frame shapes).

⭐ **`null` is the honest empty and consumers must render it as such** — not as today's date,
not as a neighbour's, not as the string "nan".

---

## 4. WHAT DID **NOT** CHANGE (so the delta is not read wider than it is)

- **The global as-of selector is untouched.** `resolve_as_of` still picks ONE run as-of — the
  newest trading day with BOTH silver and bbg present. A fund can only ever step **back** from
  it, never forward. Loosening the selector was named in the TO as the fix that breaks the two
  funds that already work; this is not that.
- **The gold partition key is unchanged.** Both tables still land under `date={run as_of}/`,
  and the `date` column still carries the run's as-of. `date` is a partition key and claims no
  provenance; `data_as_of` is the claim.
- **Characteristics, `fund_daily` and `netassets` stay on the GLOBAL as-of.** Keying reference
  data per fund would let ONE security classify two different ways in two books of the same
  payload. **So `data_as_of` describes THE HOLDINGS**, which is the plane the Andrew-direct
  complaint is about. Stated here because it is a real design decision, not an oversight.
- **Every other book and holding field**, and their units. Measured: at `as_of=2026-08-26` all
  four books moved **0 of 29 fields** with order-sensitive holdings fingerprints identical.

---

## 5. EVIDENCE THIS DELTA IS REAL AND NOT ASPIRATIONAL

Measured on live silver, 24 partition × fund cells / 976 holding rows across 6 partitions:

```
silver/holdings/2026-08-24.parquet
    PFDE / PFOE rows   data_as_of = 2026-08-24     (== the partition name)
    DIVZ / IDVZ rows   data_as_of = 2026-08-21     (2 trading days EARLIER)
```

Producer BEFORE (`dd75f6bd64`) at that as-of stamped **all four books 2026-08-24** — serving
08-21 data under an 08-24 date. AFTER (`25f30acc63`) DIVZ/IDVZ read 2026-08-21 and PFDE/PFOE
are byte-unchanged.

⛔ **Note the defect class this exposes, which the TO frames only as under-reporting:** the
live artifact also **OVER-CLAIMS**. A book rendering as FULL with a wrong date is invisible to
an absence check — it looks complete. That is the case `data_as_of_spread` and `as_of_basis`
exist to make legible.

---

## 6. CONSUMER IMPACT — NAMED, NOT ASSUMED

- **`portal/src/pages/Positioning/shared/etfAdapter.ts:131`** already reads
  `book.data_as_of ?? null` — **per-book, so the data grain is already correct** and the new
  nullable value flows without an adapter change. *(Read at source; not this seat's lane to
  change.)*
- **`useYangDataAsOf('positioning', ...)` is the WRONG GRAIN** for a book-level date and must
  not be stretched to carry it — that is **TO-7 AC4**, `0.4.0_DE_ClientPlatform`'s work, and it
  is a **precondition of this delta reaching users**: four differently-dated books with no
  visible date is worse than today.
- **`as_of_basis` is additive.** An allowlist consumer that does not know the key drops it with
  no error — the same enumerated-allowlist behaviour recorded at `BOOK_KEYS` and
  `etfAdapter.ts:77`. It is in `BOOK_KEYS` here; the adapter rung is DE's.

---

## 7. STATE

⚠ **DESIRED, NOT APPLIED.** Both producer files are members of the `etf-positioning-producer`
Lambda package; the ~13:00Z fire runs **deployed bytes**. Measured 2026-08-28 02:4xZ against
the live function: the running package carries the publisher and gold members at **`f0e2a05889`**,
**not** `25f30acc63` — a three-way content discriminator (raw + newline-normalised sha256,
0 CRLF in the package) naming which version is live rather than only that it is not the newest.
**Nothing in this delta is on the served plane until an AE-lane apply rebuilds the package
after `25f30acc63`.** Sequencing is `2.0.0_SA_COO~Z`'s.
