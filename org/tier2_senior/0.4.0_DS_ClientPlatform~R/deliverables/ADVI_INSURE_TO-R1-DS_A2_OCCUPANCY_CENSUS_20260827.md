# ADVI_INSURE TO-R1-DS — INS-a-2 OCCUPANCY CENSUS

**Seat:** `0.4.0_DS_ClientPlatform~R` (S4) · **Issued under:** `2.0.0_SA_COO` GO 76135, scope confirmed 76146
**Taken:** 2026-08-27 ~16:3x–16:5xZ · **Cell:** `INS-a-2` · **Phase:** D2 P2 source step

---

## 0. WHAT THIS CENSUS IS, AND WHAT IT IS NOT

**IS:** which v1 fields are actually POPULATED in what the source **already landed**, per surface, with
denominators, so the landing/gold planes know what they will consume.

**IS NOT:** a vendor call. **No Black Diamond REST egress was performed at this seat.** The
2026-08-25T2248Z Andrew grant was per-use for the `0.6.0_AE_PartnerETL` lane's exercised calls; it is not a
standing wire and does not extend here (COO 76146 confirms). Availability is not authorization.

**INSTRUMENT:** the landed **bronze bytes** (raw vendor JSON) plus the landed **silver parquet**, read
directly from S3. ⛔ **The AE lane's proof instance was NOT used as corroboration.** Its AC2 map and the
vehicle's `V1_FIELD_MAP` both descend from the same 08-25 live exercise — reading one as confirmation of
the other is *inheriting* the claim, not corroborating it. The landed bytes are the independent substrate.

**GRAIN NOTE ON `INS-a-3`:** every empty result below is reported per-surface with its denominator. Nothing
here generalises to "insurance data is unavailable."

---

## 1. THE LANDED CORPUS — and the denominator that matters

`s3://opal-data-assets/blackdiamond/49financial/` = **8,860 keys** (client-side count, auto-paginated).

⛔ **8,852 of those 8,860 are `bronze_legacy/` + `silver_legacy/` (fees, assets, transactions, realized,
prices, allocations, unrealized). THE INSURANCE PLANE IS 8 KEYS.** A count of the tree is not a count of
the subject; quoting 8,860 as "the insurance landing" would overstate it by three orders of magnitude.

| surface | layer | objects | bytes | vintage |
|---|---|---|---|---|
| `insurance_relationshipaccountdetailsearch` | bronze | 3 | 82,136 / 41,688 / 82,136 | 2026-08-25 |
| `insurance_insurancerelationshiplist_export` | bronze | 2 | 13,090 / 13,089 | 2026-08-25 |
| `insurance_insurancerelationshiplist` | bronze | 1 | 77 | 2026-08-25 |
| `fact_insurance_relationshipaccountdetailsearch` | silver | 1 | 32,934 | 2026-08-25 |
| `fact_insurance_insurancerelationshiplist_export` | silver | 1 | 12,120 | 2026-08-25 |

⛔ **EVERY OBJECT IS VINTAGE 2026-08-25. There is no 08-26 and no 08-27 partition.** This is a **single QA
capture**, not a running feed. Read as: the landing plane has a *specimen*, not a *cadence*. (Stated as a
property of the corpus, not as a staleness alarm — no trading-calendar claim is being made.)

**`page0` IS A BYTE-DEEP DUPLICATE OF `offset0`** (deep compare, sorted keys: `True`). The 3
`relationshipaccountdetailsearch` objects are **2 distinct captures**: the earlier `page0` run (23:00:16Z)
was superseded by the paginated `offset0`/`offset50` pair (23:08:5xZ). **A consumer globbing the prefix
double-counts 50 of 77 relationships.** Dedup on relationship `id`, or read the `offset*` pair only.

---

## 2. COHORT COVERAGE

| | |
|---|---|
| vendor-reported `total` | **77** |
| relationships materialised (offset0 + offset50, deduped) | **77** |
| duplicate relationship ids dropped | 0 |
| relationships with ZERO accounts | 0 |
| **ACCOUNT RECORDS — the census denominator** | **106** |

**walked == vendor total: TRUE.** The cohort is fully walked, not sampled, not a page.

---

## 3. ⛔ THE DECOMP FACE NAMES THE WRONG CALL — and the two names differ by a prefix

`INS-a-2` as written says: *"`accountdetailsearch` supplies per-account identity + characteristics +
`currentEmv` + `asOfDate`."* **Measured, that is false in this estate, and the cell's own instruction
("name which call supplies which field — do not assume one call covers both") is what catches it:**

| call | status | what it actually supplies |
|---|---|---|
| **`relationshipaccountdetailsearch`** (`/relationship/request/query/...`) | **SANCTIONED, landed** | **all 8 v1 fields**, measured below |
| `accountdetailsearch` (`/account-api/query/...`) | ⛔ **EGRESS-REFUSED** | `insuranceCharacteristics` only — riders / death-benefit / cash-value, all **DEFERRED by Ruling 6** |

`insurance_leg.py:78-89` refuses `accountdetailsearch` mechanically: `/account-api/*` carries **a different
project's gate** (OPAL_TAXSMA PRD D3), which the 08-25 insurance sanction did not dissolve.

>> **THE TWO NAMES DIFFER ONLY BY THE `relationship` PREFIX, ONE IS GATED AND ONE IS NOT, AND THE SILVER
>> TABLE IS NAMED `fact_insurance_relationshipaccountdetailsearch`.** A reader who compresses that to
>> "accountdetailsearch" reaches for a surface that raises `EGRESS REFUSED` — and, reading the decomp face,
>> would believe the *sanctioned* call cannot supply `currentEmv`. **v1 needs nothing from the gated
>> surface.** Routed as an OBSERVATION; the decomp face is not mine to edit.

---

## 4. ACCOUNT-GRAIN OCCUPANCY — denominator 106

Occupancy is **three-valued**. A consumer that cannot separate these will write a `fillna` and call it coverage.

| v1 field | JSON path | POPULATED | NULL | MISSING | pct |
|---|---|---|---|---|---|
| `bd_account_id` | `accounts[].id` | **106** | 0 | 0 | 100.0% |
| `account_number` | `accounts[].accountNumber` | **106** | 0 | 0 | 100.0% |
| `carrier` | `accounts[].custodian.name` | **106** | 0 | 0 | 100.0% |
| `product` | `accounts[].accountRegistrationType.identifier` | **106** | 0 | 0 | 100.0% |
| `current_emv` | `accounts[].currentEmv.emv` | 102 | **4** | 0 | **96.2%** |
| `as_of_date` | `accounts[].currentEmv.asOf` | 102 | **4** | 0 | **96.2%** |

Relationship grain (denominator 77): `relationship_id` **77/77**, `relationship_name` **77/77**.

⚠ **SELF-CORRECTION, because the difference changes the gold builder's code.** My first pass reported
`current_emv` as **MISSING** on 4. It is **NULL**. The key `currentEmv` is present on **106 of 106**; on 4
its *value* is JSON `null`, and my path-walker charged a null parent to the child hop. **`.get()` chaining
will raise `AttributeError` on those 4, not return a default** — the two classifications imply different
code, which is why the distinction was worth re-measuring rather than reporting the first number.

### The 4 unvalued accounts — named, not summarised

| account id | accountNumber | `currentEmv` | `asOfDate` | `closedDate` | carrier |
|---|---|---|---|---|---|
| `z0820076181` | 13898655 | `null` | 2025-11-17 | — | Allianz Life |
| `z0820076191` | 13898656 | `null` | 2025-11-17 | — | Allianz Life |
| `z0821249311` | 14456139 | `null` | 2025-11-17 | — | Vanguard |
| `z0821249321` | 14456140 | `null` | 2025-11-17 | — | Vanguard |

**They are NOT closed** (`closedDate` null on all 4 — and on all 102 others, so closure does not
discriminate here and I am not offering it as the cause). They are live accounts carrying **no current
valuation**, last dated 2025-11-17. Two consecutive-numbered pairs at two carriers.

⛔ **THE GOLD TABLE MUST CARRY THESE AS ROWS WITH A NULL NAV.** Dropping them under-counts the cohort by 4;
`fillna(0)` asserts a $0 policy value that the vendor did not state. Both are wrong, and both read as clean.

---

## 5. VINTAGE SPREAD — 7 of 106 accounts are not "current"

| `asOfDate` | accounts | `currentEmv.asOf` |
|---|---|---|
| **2026-08-24** | **99** | 2026-08-24 |
| 2025-11-17 | 4 | `None` |
| 2024-03-28 | 2 | 2024-03-28 |
| 2026-02-06 | 1 | 2026-02-06 |

⛔ **A SINGLE `date={D}` RUN-DATE PARTITION WOULD STAMP ALL 106 ROWS AS ONE VINTAGE AND MISLABEL 7 OF
THEM** — including two accounts ~17 months stale that **do carry an emv** and so survive every non-null
check. The TO's own AC2 wording already anticipates this: *one row per insurance account per `asOfDate`*.
This census supplies the reason that clause is load-bearing rather than stylistic.

### Input to the OPEN Ruling-5 question (`asOfDate` vs `currentEmv.asOf`)

`insurance_leg.py:158-161` records which date the client-facing "statement as of" prints as **open — a
ruling, not a measurement**. I am not ruling it. The measurement it needs:

- **Where both exist, they never disagree: equal on 102 of 102 comparable records, 0 differ.**
- **Coverage differs: `asOfDate` 106/106; `currentEmv.asOf` 102/106.** On exactly the 4 unvalued accounts,
  `currentEmv.asOf` is null while `asOfDate` still carries 2025-11-17.

>> So the choice is not between two disagreeing dates — it is between **a stamp that is always present**
>> and **a stamp that is present only when a value is**. `currentEmv.asOf` is the honest vintage *of a NAV*
>> (it cannot outlive its value); `asOfDate` is the honest vintage *of a record*. **For a row whose NAV is
>> null, only `asOfDate` can say anything at all.** Ruling remains with the issuer.

---

## 6. NAV MAGNITUDE (sanity only — NOT a served figure, AC4 is shut)

Over the 102 valued accounts: **sum 51,807,815.31 · min −309,502.70 · max 3,703,469.55 · 3 zero-valued ·
1 negative.** Order of magnitude is plausible for a 106-account insurance book. The single negative
balance is recorded as an OBSERVATION, not chased.

---

## 7. ⛔ GRAIN SEAM — the landed silver is NOT at the grain the gold table needs

| artifact | grain | rows |
|---|---|---|
| bronze `relationshipaccountdetailsearch` | relationship, accounts nested | 77 → 106 nested |
| **landed silver `fact_insurance_relationshipaccountdetailsearch`** | **RELATIONSHIP** | **77** |
| **gold `insurance_nav_current` (AC2 requirement)** | **ACCOUNT × asOfDate** | **106** |

**Silver is lossless — verified by round-trip, not assumed:** exploding its nested `accounts` column
yields **106 account records (matches bronze exactly)** and **4 null `currentEmv` (matches bronze
exactly)**. No field slimming, no fillna, no business-row filter — **Rule 17 satisfied.**

**Two mechanical facts the gold builder needs:**
1. **It must EXPLODE.** Silver's 77 rows are relationships; AC2 requires one row per account. The explode
   is possible from silver alone — no second bronze read.
2. ⛔ **`accounts` is stored as a JSON *string* column, not a native nested struct** (`dtype=object`,
   element type `str`). It requires `json.loads` per row. A builder assuming a native list gets a string
   and will iterate its *characters* — which fails as data, not as an exception.

Also noted: silver `displayName` is null on **51 of 77** relationships. Not a v1 field; recorded so it is
not later mistaken for breakage.

---

## 8. FORBIDDEN-SET PROBE — input to AC3, not AC3 itself

Over the **34 distinct keys** in the payload (27 account-object + 11 relationship-object, minus overlap),
tokens `return, twr, irr, performance, series, benchmark, alpha, beta, sharpe, yield`:

**0 hits.** The source projection carries no analytics, returns, or series field. AC3's own census runs
against the gold schema I author; this measures the *input* and shows the forbidden set is not arriving
from upstream.

Full account-object projection, enumerated, **no ellipsis** (27): `accountDisplayNumber, accountNumber,
accountRegistrationType, asOfDate, closedBy, closedDate, closedWhen, correlation, createDate, currentEmv,
custodialAccountNumber, custodian, custodianID, dataAsOfDate, dataFormatID, displayName, firmID, id,
internalId, modifiedBy, modifiedDate, name, ordinal, relationshipID, repCodes, startDate, taxStatus`.

---

## 9. CONTROLS — the census can fail in BOTH directions

| control | expectation | result |
|---|---|---|
| **NEGATIVE** — `insuranceCharacteristics` (lives only on the egress-refused `/account-api/*`; Ruling-6 deferred) | must read absent | **MISSING 106 of 106** — matches the refusal |
| **POSITIVE** — `accountNumber` (the Ruling-2 join key) | must read present | **POPULATED 106 of 106** — the instrument can see a field that is there |

**Both arms fire.** Without the positive arm, every `MISSING`/`NULL` above would be indistinguishable from
a dead reader. `accountNumber` is **UNMASKED on 106 of 106**, so the Ruling-2 join does not depend on the
gated surface.

---

## 10. WHAT THIS UNBLOCKS, AND WHAT IT DOES NOT

**Unblocked for the gold DESIGN limb (AC2 `DESIGN-COMPLETE`), now grounded in measured occupancy:**
6 account-grain fields + 2 spine fields, 4 at 100% and 2 at 96.2%; nullable NAV with a named 4-row
population; per-row `asOfDate` mandatory; explode-from-silver with a JSON-string decode.

**NOT changed by this census:**
- **`INSR1DS-AC1` APPLIED limb stays gated.** One 08-25 specimen is not a landing *plane*; `INS-b-1` /
  `INS-inv-4` still wait on `INS-a-1..3` at `0.6.0_AE_PartnerETL` (S5, seated).
- **`INSR1DS-AC4` stays shut** — arm-(a) sovereign gate (@7a843d25da, @8155516dbd). Build proceeds, serve
  waits. Not re-asked.
- **No vendor call, no vehicle leg, no bronze mint.** Nothing was written to any tree by this census.

---

## 11. SURPRISE ITEMS — routed to `3.0.0_SA_CVO`, cc `2.0.0_SA_COO`, NOT `4.0.0_SA_CRO`

| # | class | standing | item |
|---|---|---|---|
| 1 | OBSERVATION | INERT | `INS-a-2`'s face names `accountdetailsearch`; the measured supplier of all 8 v1 fields is `relationshipaccountdetailsearch`. The gated call supplies only Ruling-6-deferred fields. Decomp face is not mine to edit. |
| 2 | OBSERVATION | INERT | `page0` is a byte-deep duplicate of `offset0`; a prefix-glob consumer double-counts 50 of 77 relationships. |
| 3 | OBSERVATION | INERT | 4 live, unclosed accounts carry `currentEmv: null`, last dated 2025-11-17; 2 further accounts are ~17 months stale but *do* carry an emv, so no non-null check separates them. |
| 4 | OBSERVATION | INERT | One negative account balance (−309,502.70) and 3 zero-valued in the landed corpus. Recorded, not chased. |

**None are BLOCKING.** No ARMED hazard; nothing requires same-turn disarm.

---

**Instrument:** `scratchpad/ins/a2_occupancy_census.py` (three-valued classifier + both control arms),
plus direct `s3api` reads. **Denominators printed throughout: 8,860 tree keys / 8 insurance objects /
77 relationships / 106 account records / 34 distinct keys.**
