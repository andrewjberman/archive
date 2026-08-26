# ADVI_INSURE.TO-R1-DS -- AC2 SPINE JOIN: THE CONTRADICTION IS DISSOLVED

**seat:** `0.4.0_DS_ClientPlatform~R` · **scope authority:** `2.0.0_SA_COO` 72199 s.2(d)
**read taken:** 2026-08-26T14:12Z - 14:20Z · **acts:** READ ONLY. No producer, no emit, no write to any data plane.

---

## THE ANSWER IN ONE LINE

**The hypothesis is CONFIRMED: the two sets are entirely disjoint, so both records are true at their own
vintage.** And the join went one step further and found **WHY** -- `account_id` **is a Schwab account
number**, and an insurance policy held at Brighthouse or Allianz does not have one. **The
`NOT-DERIVABLE-UPSTREAM` stamp is CORRECT, and it is correct STRUCTURALLY, not pending a fix.**

---

## PART 1 -- THE JOIN ORDERED BY 72199 s.2(d)

**Trees named** (a firm-partitioned absence verdict must name the tree it searched):
```
GOLD  s3://opal-data-49financial/gold/advi/insurance/insurance_nav_current/date=2026-08-25/data.parquet
DIM   s3://opal-data-assets/blackdiamond/49f/silver/dim_advisor_fee_role/date=2026-08-24/data.parquet
```
The DIM partition is the latest available and is the **same vintage `~J` would have read on 2026-08-25**
(written 2026-08-25T07:06:47Z). Its shape reproduces `~J`'s citation exactly -- **160,091 rows x 44 cols,
`is_current` True = 5,337** -- so this is the same artifact they measured, not a lookalike.

### DENOMINATOR BOTH DIRECTIONS

| direction | result |
|---|---|
| GOLD -> DIM (all 160,091 rows) | **0 of 106** gold accounts found among 5,337 dim accounts |
| GOLD -> DIM (`is_current` only) | **0 of 106** |
| DIM (`is_current`) -> GOLD | **0 of 5,337** is_current accounts are insurance accounts |

### THE CONTROLS, BECAUSE A ZERO IS THE VERDICT THAT MOST NEEDS THEM

- **POSITIVE CONTROL on the join mechanism:** 200 ids taken **from the dim itself** and joined back to the
  dim matched **200 of 200**. The join fires; a zero is disjointness, not a dead comparison.
- **FORMAT / IDENTITY CHECK** (a format skew manufactures a false zero): both populations have the
  **identical single shape** `a9999999999` -- GOLD 106 of 106, DIM 5,337 of 5,337.
- **NORMALISED RETRY** (strip + lowercase, to rule out case/whitespace skew): still **0 of 106.**

**VERDICT: the disjointness is MEASURED.** `0.4.0_DS_ClientPlatform~J`'s *"LEG 1 ... ID JOIN EXISTS,
5,337 distinct each"* is **TRUE** -- it is a statement about the dim's STRUCTURE and about the AM
population. The landed artifact's `NOT-DERIVABLE-UPSTREAM` is **also TRUE** -- it is a statement about
COVERAGE over the insurance population. **Two different axes; neither record is wrong.**

> **THE TRANSFERABLE SHAPE:** *"the join exists"* and *"the join covers my rows"* are different claims
> and they read identically in a note. `~J` measured EXISTENCE and could not have measured COVERAGE --
> there were no insurance accounts in the estate when they looked.

---

## PART 2 -- BEYOND THE RE-CUT: WHY THE LEG IS EMPTY

> ⚠ **DECLARED AS A WIDENING.** 72199 s.2(d) asked only for the join. Part 2 is an ADDITIONAL read taken
> because "they sit outside the set" invites the immediate follow-up *"then is it derivable from somewhere
> else?"*, and answering it here saves a round trip. **`2.0.0_SA_COO` may discard it; Part 1 stands alone.**

### 2a. `account_id` IS THE SCHWAB ACCOUNT NUMBER -- measured, with a negative control

Third tree: `s3://opal-data-assets/blackdiamond/49f/silver/dim_account_xref/date=2026-08-24/data.parquet`
(6,201 rows x 10 cols). It carries `bd_account_id`, `bd_account_number`, `bd_original_account_number`,
**`schwab_account_id`**, `match_method`, `in_0833_universe`, `account_is_open`.

| test | result |
|---|---|
| AM `is_current` accounts joinable in BOTH dim and xref | **5,337 of 5,337** |
| `dim.account_id` **==** `xref.schwab_account_id` | **5,337 of 5,337 (100.0%)** |
| **NEGATIVE CONTROL** -- shuffle one side, expect ~0 | **0 of 5,337** |

Sample: `z0817426091 -> account_id 0010048935 == schwab_account_id 0010048935`.

**The Opal `account_id` on the 49F book IS the Schwab account number.** The 100% is not trivially true --
the shuffle control drives it to zero.

### 2b. AND THE INSURANCE ACCOUNTS HAVE NO SCHWAB ID TO MAP TO

Of the 106 insurance accounts, **96 are present in `dim_account_xref`** and 10 are absent entirely.
For those 96:

| field | value | count |
|---|---|---|
| `schwab_account_id` NON-NULL | -- | **0 of 96** |
| `match_method` | `unresolved` | **96 of 96** |
| `in_0833_universe` | `False` | **96 of 96** |
| `account_is_open` | `True` | **96 of 96** |

**POSITIVE CONTROL on the xref itself:** 5,337 of 5,337 AM `is_current` accounts DO match an xref
`bd_account_id`. The xref can resolve a 49F account; **the insurance zero is measured, not a dead lookup.**

### 2c. THE READING, MARKED AS A READING

**MEASURED:** `account_id` == Schwab id (5,337/5,337, control 0); insurance accounts carry
`match_method=unresolved` and a NULL `schwab_account_id` (96/96); they are open accounts
(`account_is_open` True 96/96), so this is not a stale-account artifact.

**THE READING (mine, not measured):** these are insurance policies custodied at the carriers named in the
table's own `carrier` column -- Brighthouse 85, Allianz 8, AXA 4 -- **not at Schwab**, so no Schwab
account number exists to resolve. `match_method=unresolved` is the xref correctly reporting that it looked
and found nothing, on an account it knows is open.

**IF THAT READING HOLDS, THE CONSEQUENCE IS THE USEFUL PART:** `NOT-DERIVABLE-UPSTREAM` on `account_id` is
not a pipeline gap that a later run closes. **It is structural.** Asking for an `account_id` on an
insurance row is asking for a Schwab account number for an asset that is not at Schwab.

---

## WHAT THIS MEANS FOR AC2 -- STATED AS INPUT TO A RULING, NOT AS ONE

AC2 requires the spine *"SO EVERY AGGREGATION IS A JOIN, NEVER A COMPUTATION IN THE FRONTEND."*

- `bd_account_id` -- **present, 106/106 distinct.** This is the real account-grain key for this asset class.
- `relationship_id` -- **present, 106/106, 77 distinct.** The relationship leg joins.
- `firm` -- **present, 106/106** (`3281`).
- `account_id` -- **empty, and structurally so** (Part 2).
- advisor -- **empty, and separately RULED** `NOT-DERIVABLE-UPSTREAM` (issuer 70462).

**So the aggregation spine that reaches the frontend is `bd_account_id -> relationship_id -> firm`, and
every level of it is a JOIN, not a computation.** Whether that satisfies AC2 as written is
`2.0.0_SA_COO`'s ruling. **What is now removed from that decision is the uncertainty:** the missing leg is
not a defect to be repaired before closing, and no future upstream run will populate it.

⛔ **ONE THING I DID NOT DO AND WILL NOT WITHOUT A WORD:** I did not propose adding `schwab_account_id`,
renaming `account_id`, or changing the gold schema. That is a schema act on another lane's producer, and
Rule 24 binds any axis change. Raising it is legal; doing it is not.

---

## RESIDUAL, NAMED RATHER THAN LEFT IMPLICIT

- **The 10 of 106 absent from `dim_account_xref` entirely** are unexplained. They are not a
  counter-example to anything above -- absent from the xref is not evidence of a Schwab id -- but they are
  **UNATTRIBUTED, not "the same as the other 96."** I did not itemise them.
- The reading in 2c is **INFERRED**, not source-confirmed. Confirming it means reading BD's custody model
  or the vendor surface, which is `0.6.0_AE_PartnerETL` ground and vendor-egress gated.

-- `0.4.0_DS_ClientPlatform~R`, 2026-08-26
