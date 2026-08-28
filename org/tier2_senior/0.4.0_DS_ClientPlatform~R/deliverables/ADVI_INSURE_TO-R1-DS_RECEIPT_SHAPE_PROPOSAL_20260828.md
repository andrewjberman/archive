# ADVI_INSURE TO-R1-DS — THE RECEIPT'S SILVER SHAPE (proposal to the issuer)

**Seat:** `0.4.0_DS_ClientPlatform~R` · **Authority:** `2.0.0_SA_COO` 78303(ii) — *"`0.4.0_DS_ClientPlatform~R`
PROPOSES the shape in the instance, `2.0.0_SA_COO` rules it on the AC1 re-read."*
**Taken:** 2026-08-28 ~16:4xZ · **Cells:** `INS-b-1`, `INS-inv-4` · **Feeds:** `INSR1DS-AC1`
⛔ **DISTRIBUTION: NOT TO `4.0.0_SA_CRO`** (PRD s.3, Andrew ~16:1xZ).

---

## 0. THE PROPOSAL, IN ONE LINE

**`insurance_insurancerelationshiplist` must NOT convert to silver.** Keep it
`UNCONVERTED-AND-REPORTED`, which is where `0.4.0_DS_ClientPlatform~J`'s writer already
has it. **This is a recommendation, not a refusal** — s.4 states what I build instead, on
the issuer's word, and it is one edit.

---

## 1. WHAT THE OBJECT ACTUALLY IS — measured, not inferred from its prefix

```
blackdiamond/49financial/bronze/insurance_insurancerelationshiplist/2026-08-25/
    insurance_insurancerelationshiplist_page0.json          77 bytes, 2026-08-25T23:00:17Z
```
Full content, verbatim:
```json
{"exportResultID":282393,"resultGuid":"c0f5ac97-b204-4266-b197-0dee406adf34"}
```

That is the **async job handle** of `INS-a-2`'s `run -> resultGuid -> download` bulk-export
pattern. The **data** that job produces lands in the sibling feed
`insurance_insurancerelationshiplist_export` — an XLSX workbook (magic `50 4b 03 04`),
77 rows x 9 columns — which **already converts** to
`silver/fact_insurance_insurancerelationshiplist_export/date={D}/data.parquet`.

> ⚠ **THE TWO FEED NAMES DIFFER BY THE SUFFIX `_export` AND THAT IS THE ENTIRE DISTINCTION
> BETWEEN A JOB TICKET AND A DATASET.** I read the prefix list and reported four data tables
> to `2.0.0_SA_COO` + `1.0.0_SA_CTO` (78279/78280) without opening the 77-byte object. The
> correct reading was already in my own lane's writer, in its docstring, since 2026-08-25
> `@4b494cf3ae`. **Build-ladder rung 2 — "the estate already has it" — applies to the
> REPORTING step, not only the building step.**

---

## 2. WHY IT SHOULD NOT CONVERT — three reasons, in falsifiable order

### 2.1 GRAIN — Rule 24 postulate (ii), SAME GRAIN

The receipt is **JOB-grain**: one row per export invocation, keyed by `exportResultID`.
Every other table in this family is **RELATIONSHIP-grain**, keyed by `relationship_id`.

**A fact table mixing two grains is malformed however its rows are populated** — so this
objection is not answered by choosing better columns, and it is the reason the other two
reasons are secondary. *Measured corroboration that the grain is real: the day carries
**two** `exportResultID`s (282394, 282397) against **one** 77-relationship cohort. Job count
and relationship count are already 2-vs-77 on a single day.*

### 2.2 THE RECEIPT IS NOT EMPTY, SO THERE IS NO EMPTINESS IN IT FOR A ROW TO CARRY

78303(ii) reasons that *"a receipt ROW carrying the affirmatively-empty outcome
(`f4836ad706`) is the shape that keeps the denominator honest."* **The affirmative emptiness
named there belongs to a different feed.**

| the object | its state |
|---|---|
| `insurance_insurancerelationshiplist` (the receipt) | **COMPLETE and well-formed** — both fields present and populated |
| `insurance_relationshipdetail.financialTeam` (`f4836ad706`) | **`[]` — the vendor affirmatively answering "no financial team"** |

⛔ **A receipt row carrying `financialTeam`'s emptiness would state one feed's measurement on
another feed's object.** The row would read as evidence about a surface it never observed —
and it would read that way to a consumer who has no way to tell.

### 2.3 THE DENOMINATOR IS ALREADY KEPT HONEST WHERE IT ACTUALLY LIVES

Rule 17's no-fillna / no-droprow clause lands the empty array in the feed that measured it.
**Measured this round on the partition I wrote:**

```
financialTeam_empty_array : 1     <- "[]", the vendor's affirmative "none"
financialTeam_absent_null : 0     <- the vendor never sent the field
```

**The two states are counted APART.** That is precisely the distinction the AC1 prep s.2
demanded (*"silver must not drop a row for having nothing in it, or the denominator shrinks
silently and the emptiness becomes unmeasurable"*), and it is discharged in
`fact_insurance_relationshipdetail` — not in a receipt row.

### 2.4 DECLINING TO CONVERT IS NOT DECLINING TO ACCOUNT FOR IT

The producer prints the feed on **every** run:

```
FEED insurance_insurancerelationshiplist
  bronze objects: N
  UNCONVERTED (reported, not skipped): async job receipt (exportResultID/resultGuid)
      -- an operational handle, not a data surface
```

**A feed the registry cannot name stays visible either way.** The choice is between a
visible non-conversion and a malformed table, never between visibility and silence.

---

## 3. ⛔ THE EFFECT ON AC1'S CLOSE CONDITION — this needs the issuer's word either way

78303 sets AC1 to close *"when **4 of 4** land at the grammar."* **If this proposal is
adopted, 4 of 4 is unreachable and AC1 cannot close on its own terms.** The condition should
be restated as:

> Closes to PASS when **3 of 3 CONVERTIBLE** feeds land at the grammar under the Rule-17
> empty-row clause, the receipt is declared non-convertible on the record, and the silver
> limb is measured on all three.

**Current state against that restatement — 3 of 3 landed, all three measured:**

| feed | silver partition | Rule 17 |
|---|---|---|
| `relationshipaccountdetailsearch` | `date=2026-08-25` (08-26T00:02:07Z) | CONFORMS |
| `insurancerelationshiplist_export` | `date=2026-08-25` (08-26T00:02:08Z) | CONFORMS |
| `relationshipdetail` | `date=2026-08-27` (**08-28T16:39:19Z, this seat**) | CONFORMS |
| `insurancerelationshiplist` (receipt) | **none, by this proposal** | n/a — not a data surface |

⚠ **A SEPARATE AND STILL-OPEN GAP, NOT CLOSED BY THIS PROPOSAL:** the landed
`relationshipdetail` partition holds **1 relationship, not the 77-relationship cohort**. S4 is
a per-id fan-out and exactly one call was made. That is a *complete silver of an incomplete
pull*; the producer reports it as `COHORT COVERAGE` rather than hiding it in a row count.
**Do not read 3-of-3 tables as 77-of-77 relationships.**

---

## 4. IF THE ISSUER RULES OTHERWISE — what I build, on the word

One edit to `bd49f_insurance_conversion.py`: promote `FEED_RECEIPT` out of `NON_DATA_FEEDS`
into the reader tuple with a `read_receipt()` that lands **one row per `exportResultID`** —
columns `exportResultID`, `resultGuid`, plus the framework's five `_source*` meta — at
`silver/fact_insurance_insurancerelationshiplist/date={D}/data.parquet`.

**It would be dedup-on-`exportResultID`, and it would carry NO field from any other feed** —
if a receipt table is ruled in, it must still describe only what the receipt observed.

---

## 5. WHAT I AM NOT DOING

- **Not editing AC1's status.** The re-read is the issuer's act (73382 stands on synthesis);
  78303's status_reason is transcribed **verbatim** into the instance with my post-ruling
  measurement appended as a **separately marked** note, never folded into the issuer's words.
- **Not converting the receipt on my own judgment.** The producer is unchanged on this feed
  until `2.0.0_SA_COO` rules.
