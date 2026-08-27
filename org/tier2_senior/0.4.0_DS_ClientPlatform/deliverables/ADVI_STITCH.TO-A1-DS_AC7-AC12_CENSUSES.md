# ADVI_STITCH.TO-A1-DS — AC7 · AC8 · AC9 · AC11 · AC12 — THE CENSUSES

**Seat:** `0.4.0_DS_ClientPlatform~Q` · **PINNED xref partition: `date=2026-08-24`** — stated on every
number below, per `STI-c-1`. Source
`s3://opal-data-assets/blackdiamond/49f/silver/dim_account_xref/date=2026-08-24/` (30 partitions,
2026-07-14 .. 2026-08-24).

## AC7 — `STI-c-1` + `STI-inv-3` — the key plane, READ not re-derived

| | measured | inherited (O-3) |
|---|---|---|
| rows × cols | **6,201 × 10** | ✓ exact |
| `seed-xref` | **5,375** | ✓ exact |
| `unresolved` | **826** | ✓ exact |

**No competing crosswalk producer.** `comp-find -i` over the estate: the only writers of
`bd_*_account_number` into an xref shape are `data/assets/scripts/silver/bd49f_dim_conversion.py`
(the dim producer) and `data/black_diamond/scripts/bronze/build_schwab_bd_account_xref.py` (the
Schwab-side xref). **Phase A wrote none.** ⚠ The clause "the landed copy's `match_method`
distribution equals the source's" **does not apply**: `dim_account_xref` lives under
`opal-data-assets/blackdiamond/49f/silver/`, which is **outside the declared scope set** (AC2), so
there is no landed copy — correctly, since `STI-c-1` says the key plane is read and adjudicated,
never migrated.

## AC8 — `STI-c-2` — the renumbering marker: **CONFIRMED, from the producer's own words**

The decomp records S8's verdict on this field as **INFERRED**. It is now confirmed from BD's own
producer rather than from behaviour I guessed at —
`data/black_diamond/scripts/bronze/build_schwab_bd_account_xref.py:15-17`:

> **Join key: Schwab `ACC.account_id` (10-char zero-padded) == BD `original_account_number`
> (8-char zero-stripped)**

So `bd_original_account_number` is **the field that joins BD to the custodian**, and
`bd_account_number` is BD's current number. `bd_original_account_number != bd_account_number`
therefore means **BD's current number differs from the number the custodian record matches on.**

⛔ **This confirms the FIELD'S MEANING and licenses NO class.** Inferring `MIGRATED` from it is R2,
Phase B (`STI-g-1`), and is not done here.

**541 rows** carry the difference — and the count is **not** a null artifact: both fields are
**0 null / 0 blank** across all 6,201 rows in both `match_method` values, and a strict
both-present-and-differ comparison returns the identical **541**.

## ⛔ AC11 — THE MECE CLOSE, AND ONE RESULT CONTRADICTS THE DECOMP

### Partition 1 — the legacy universe (the 8,259)

```
  IN XREF            6,107
  ABSENT FROM XREF   2,152
  ----------------------------
  TOTAL              8,259   vs universe 8,259   CLOSES
```
Universe = `s3://opal-data-bd/gold/entities/accounts/*` — **8,259 accounts, one
`aua_timeseries.json` each.** Re-grounds exactly to O-4.

### Partition 2 — the xref itself (a different denominator, stated as such)

```
  seed-xref   5,375 + unresolved 826 = 6,201   vs 6,201 rows   CLOSES
  in universe 6,107 + xref-only   94 = 6,201   vs 6,201 rows   CLOSES
```

### Overlaps — shown, never subtracted

| overlap | count |
|---|---|
| renumbered inside `seed-xref` | **0** |
| renumbered inside `unresolved` | **541** |
| renumbered inside the legacy universe | 489 |
| renumbered xref-only | 52 |
| `unresolved` inside the universe | 760 |
| `unresolved` xref-only | 66 |

⛔ **EVERY ONE OF THE 541 RENUMBERED ACCOUNTS IS `unresolved`. NONE OF THE 5,375 `seed-xref` MATCHES
IS RENUMBERED.** Perfect separation.

**The decomp's AC11 expects the opposite** — "the 541 shown INSIDE the 5,310", i.e. inside the
*matched* set. Measured, they are entirely inside the *unmatched* set. I checked this for the obvious
artifact (a null-vs-value comparison reading as a difference) and it is not one: zero nulls, zero
blanks, strict comparison identical.
**I am reporting the structural fact and NOT the mechanism.** Why renumbering and non-resolution
coincide is a causal claim, and causal claims about these accounts are R2 / Phase B.

### ⛔ CORRECTION TO THIS SECTION — I MIS-ATTRIBUTED BOTH DECOMP FIGURES

**An earlier draft of this file said the decomp's 5,310 was "J6/J7's Schwab-side coverage over
7,336 — a different population" and that its 65 disagreed with my 94. BOTH CLAIMS WERE WRONG, and
they were wrong in the direction that flatters my own numbers.** Corrected from the decomp's own
J6 line and the live cross-tab:

```
in_0833_universe   False   True
match_method
seed-xref             65   5310
unresolved           826      0
```

| decomp figure | what it actually is | measured |
|---|---|---|
| **5,310** | `in_0833_universe = True` — **a column in this very table**, not a Schwab population | **5,310 — EXACT** |
| **65** | `seed-xref` ∩ `in_0833_universe = False` | **65 — EXACT** |

**Both decomp figures re-ground EXACTLY.** There was no disagreement to name. My **94** is a
*different and additional* measurement — xref rows whose `bd_account_id` is absent from
`gold/entities/accounts/` — and it does not contradict the 65; they count different things.
`5,375 = 5,310 + 65` closes on the face.

**The lesson is mine: I named a "difference" without first identifying what the other number was
measuring.** A residual bucket is a claim, not a remainder — and so is a discrepancy.

### The contradiction that SURVIVES the correction, and is now stronger

`in_0833_universe = True` is exactly `seed-xref ∩ in-universe`, so the decomp's "the 541 sit INSIDE
the 5,310" is testable directly against the right field:

**0 of 541 renumbered accounts are inside `in_0833_universe = True`. All 541 are `in_0833 = False`,
and all 541 are `unresolved`.**

Confirmed on **both** readings — 0 of 541 in `seed-xref`, and 0 of 541 in the 5,310. The claim is
false against the correct field, not merely against a field I substituted for it.

## AC9 — `STI-d-1` + `STI-d-2` — census first, no class from silence

Artifact: `ADVI_STITCH.TO-A1-DS_AC9_CENSUS.jsonl` (2,978 rows).

| | |
|---|---|
| `ABSENT_FROM_XREF` rows | **2,152** |
| last-seen **ANSWERED** | **2,152 (100%)** — from `gold/entities/accounts/{id}/aua_timeseries.json` |
| `closed_date` **ANSWERED** | **216** — from `silver/bd_allocations.parquet` |
| `closed_date` **UNANSWERABLE** | **1,936** |
| **RESIDUE the planes cannot fully answer for** | **1,936 — printed as its own residue** |
| `OPEN_UNMATCHED` rows | **826**, every one labelled `UNKNOWN(elsewhere-candidate)` |
| **DROPPED verdicts anywhere** | **0** |

The 1,936 are not a defect: `bd_allocations` holds 6,385 accounts of the 8,259 universe, so most
absent accounts simply are not in the plane that carries `closed_date`. **Named as a residue rather
than defaulted to "not closed"** — absence of a close date is not evidence of an open account, and
`STI-d-1` says census first, no class from silence.

`UNKNOWN(elsewhere-candidate)` is **a LABEL, not a class**: the discriminating instrument (the
Fidelity ingestion) does not exist yet, so no verdict is available to assign.

## AC12 — `STI-inv-4` — the oracle is the SCHEMA, and it REFUSES AT WRITE

`assert_no_class_field()` runs inside the census emitter, before the file is opened. Exercised:

| arm | result |
|---|---|
| CONTROL — the real emitted schema | **ACCEPTED** |
| MUTANT + `class` / `rule` / `r2` / `account_class` / `ruled_version` / `disposition` / `verdict` / `category` | **REFUSED (8 of 8)** |

Emitted columns: `account_is_open · bd_account_id · closed_date · closed_date_source · label ·
last_seen_date · last_seen_source · planes_could_not_answer · population · unanswered_reason ·
xref_partition_pinned`. **No class/rule field.** A fixture carrying one **cannot be written at all**,
rather than being written and then reviewed. A separate guard refuses any `DROPPED` label.

## AC10 — `UNCOMPUTABLE-PENDING-SOURCE`

Ruled by `2.0.0_SA_COO`. `s3://opal-data-bd/schwab/silver/account_xref` is **100% `0008242234`
(MDPF Model Portfolios): 6,997 rows, 489 `<NA>`, ZERO `0008335338` (ADVI)** — and the dataset filed
under the ADVI path overlaps the MDPF subset at 6,926 and the ADVI subset at 0. Building AC10 on it
would compute a 49F residue from the other firm's accounts (`STI-inv-6`, NEVER-SUBSTITUTE).
**Not folded into any total above.** Routed to `3.0.0_SA_CVO` and `1.0.0_SA_CTO` as an estate item.
