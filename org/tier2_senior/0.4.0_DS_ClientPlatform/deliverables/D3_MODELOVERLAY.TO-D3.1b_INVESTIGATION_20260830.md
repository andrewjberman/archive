# D3_MODELOVERLAY.TO-D3.1b -- the 9-digit keys + the departure set: INVESTIGATION REPORT

**Seat** `0.4.0_DS_ClientPlatform~E` | **Issuer** `2.0.0_SA_COO` (GO 84309) | **Reported to** COO + CVO
**Clock** 2026-08-30 02:1x-03:0xZ | **Cap held**: read-only on the SmartX and 49F planes, no vendor
call, no remediation, no enum value added. REPORT, DO NOT FIX -- honored throughout.

**Vintages read** (every number below is anchored to one of these):
| plane | key | vintage |
|---|---|---|
| SmartX allocation map | `opal-data-assets` `smartx/platform/silver/fact_allocation_account_map` | `date=2026-08-28` (7,359 rows) + `date=2026-08-19` (7,305, the contract's own) |
| 49F account universe | `opal-data-assets` `schwab/08335338/silver/fact_acc` | 540 partitions `2024-07-08..2026-08-28` |
| sibling 49F scope | `opal-data-assets` `schwab/08242234/silver/fact_acc` | 659 partitions `2024-01-16..2026-08-28` |
| SmartX roster | `smartx/platform/silver/fact_model_allocation_roster` | `date=2026-08-28` (9,860 rows) |
| 49F gold | `opal-data-49financial` `gold/advi/**` | 23 dated tables, newest partitions |
| served model AUM | DynamoDB `opal-data-smartx` | full scan, 3,204 items |

**TRADING CALENDAR RESOLVED FIRST (NEVER#4).** 2026-08-29 is a Saturday and the map's Saturday
partition is 0 rows / 4,507 B -- as is every Sat/Sun in the record (08-15, 08-16, 08-22, 08-23).
That is the established weekend shape, not a break. **Friday 2026-08-28 is the live vintage** and
every "today" number below is read there.

---

## PART 2 -- THE DEPARTURE SET (done first, per the GO)

### D3.1b-3: the two accounts resolved to a state

**STATE: DEPARTED FROM THE CUSTODIAL FEED ON 2025-02-26 -- NOT CLOSED. The evidence points to a
CUSTODIAN TRANSITION (Schwab -> Vanguard), not a client departure.** The four candidate states the
TO named resolve as: **not "closed"** (no closure record exists anywhere, and both lifecycle fields
positively assert open), **not a migration artifact** (ruled out by measurement, below), **not a
reconciliation gap** (the absence is clean and contiguous, not intermittent) -- it is a **real
departure from the Schwab feed with the SmartX allocation left open behind it**.

| | `0041879643` | `0099250989` |
|---|---|---|
| account_name | `VANGUARD GROUP TTEE BHP USA 401K FBO JASON JONES` | `VANGUARD GROUP TTEE BHP USA 401K ROTH FBO JASON JONES` |
| AUM @ 2026-08-28 | $2,538,981.19 | $295,712.84 |
| model | Opal Ultra Long Term | Opal Ultra Long Term |
| roster status @ 2026-08-28 | **open** | **open** |
| last present in fact_acc | **2025-02-25** | **2025-02-25** |
| `absent_from_feed_since` | **2025-02-26** | **2025-02-26** |
| `closed_date` | **NULL** | **NULL** |
| `account_status_raw` / `account_is_open` | **`O` / True** | **`O` / True** |

**Combined $2,834,694.03. Both departed the same day; same `model_id`, same `rmid`, same client.**

#### The evidence, with its controls

1. **Contiguous presence, then total absence.** Both are present in **161 of 161** partitions in the
   span `2024-07-08..2025-02-25` (i.e. from the universe's first partition), and absent from **all
   379** partitions `2025-02-26..2026-08-28`. **540 of 540 partitions read OK** -- no partition was
   skipped, so the absence is not a read gap.

2. **POSITIVE CONTROL, and it is the load-bearing one.** A naive reading of "absent from recent
   partitions" would be worthless if the universe were lossy. Control account `0010020692` (drawn
   from the 2026-08-18 universe) is present in only **173 of 540** partitions -- which looks alarming
   until you see the shape: it **enters at 2025-12-19 and is present in every partition since,
   contiguously**. So the universe is an **accumulating point-in-time roster** where an account
   enters and stays while the custodian delivers it. The instrument therefore *can* distinguish
   entry, presence and exit -- and the pair's exit is real. Universe grows 4,075 -> 7,371 across the
   record.

3. **MIGRATION TO THE SIBLING 49F SCOPE IS RULED OUT BY MEASUREMENT, not by argument.** Neither
   account appears in **0 of 659** partitions of `schwab/08242234/silver/fact_acc`, ever. They did
   not move between the two 49F books.

4. **The custodian evidence, and it is a clean singleton.** The **only two rows in the entire
   7,359-row allocation map whose `account_name` contains "VANGUARD" are these two** -- while both
   carry **8-digit Schwab-grammar** account numbers. A 401(k) whose trustee is Vanguard, holding
   Schwab account numbers that Schwab stopped delivering on 2025-02-26, is a custodian transition
   with a stale key left behind.

5. **BOTH LIFECYCLE CARRIERS CAN EXPRESS CLOSURE AND NEITHER DOES.** This is what makes "open" a
   positive assertion rather than unmodelled lifecycle:
   - `dim_account.account_status_raw`: **188 of 8,633** rows are `C`. These two are `O`.
   - SmartX roster `status`: **2,498 `close` + 23 `workingClose` of 9,860**. These two are `open`.
   Two independent systems, each demonstrably capable of saying "closed", both saying open.

**WHAT I DID NOT RESOLVE, stated rather than guessed:** whether the client relationship persists at
Vanguard today. Confirming the transition (as opposed to observing evidence consistent with it)
needs a custodian or vendor check, which my cap forbids. The *state of our data* is fully resolved;
the *state of the client* is not, and I did not infer it.

### D3.1b-4: DOES ANYTHING LIVE STILL COUNT THEM? -- **CHECKED. THE ANSWER IS NO.**

**Stated explicitly, as the criterion requires, and it lands negative -- so no same-hour escalation
is triggered.**

**Method: I scanned every dated gold parquet table rather than reasoning from the code.** All 23
tables under `s3://opal-data-49financial/gold/advi/`, newest partition each, every column tested
against the account keys:

| the pair appears in | rows |
|---|---|
| `dimensions/dim_account` (8,633) | 2 -- carried with `absent_from_feed_since` populated |
| `dimensions/dim_identity_crosswalk` (7,359) | 2 -- flagged `in_account_universe=False` |

| the pair is ABSENT from -- every canonical/serving table | rows | hits |
|---|---|---|
| `canonical/canonical_valuation` | 7,370 | **0** |
| `canonical/twr_daily` | 7,370 | **0** |
| `canonical/valuation_integrity` | 7,370 | **0** |
| `canonical/canonical_positions` | 103,351 | **0** |
| `canonical/flow_ledger` | 4,468 | **0** |
| `canonical/nna_canonical` | 1,213 | **0** |
| `canonical/nna_atomic` | 328 | **0** |
| `dimensions/dim_boundary` | 7,371 | **0** |
| the other 15 gold tables | -- | **0** |

`dim_boundary` at **7,371 = exactly the fact_acc universe** is the tell: the serving boundary is
drawn at the universe, and the residual is outside it by construction.

Three further channels closed:
- **`platinum/` on `opal-data-49financial` is EMPTY** -- the serving tier does not exist yet.
- **`account_model_membership` HAS NEVER EMITTED.** b04 is the D3 fact designed to *carry* residual
  rows (D3-inv-2, "carried, never dropped"). S3 holds **0** data keys for it -- only the code at
  `_code/b04_account_model_membership.py`. It cannot be counting anything.
- **The served ModelPortfolios AUM does not come from this plane at all.** `/v1/aum/*` is served by
  `opal-portal-data-proxy` from DynamoDB `opal-data-smartx`; that lambda contains **zero**
  references to the allocation map.

**ONE CHANNEL IS UNDECIDABLE AND I AM NAMING IT RATHER THAN INFERRING.** The DynamoDB served AUM is
**vendor-computed at model grain with no account decomposition**, so it cannot be tested for the
presence of an individual account. The obvious cross-check -- compare served model AUM against the
map's per-model sum with and without the pair ($208,378,560.74 vs $205,543,866.71 for Opal Ultra
Long Term) -- **is not available: the planes do not overlap in time.** The served table's latest
daily period is **2026-01-12**, and the S3 allocation map's history **begins 2026-07-14**. I could
have argued "SmartX says open, therefore the vendor counts them" -- that is inference, not
measurement, and the TO asks for evidence. **UNRESOLVED, with the reason named.**

### SIZING -- so the shape is not over-read

The TO calls this "a small number with a large shape." The shape is **exactly 2**, and the
intersection is what makes it so:

```
dim_account                                                     8,633 rows
  present in the feed (absent_from_feed_since NULL)             7,371   <- = the universe
  absent from the feed                                          1,262
     absent >= 365d                                               529
        ...AND still account_is_open=True, closed_date NULL        452   <- all status 'O'
           ...AND carrying a LIVE SmartX allocation                  2   <- ONLY these two
           ...NOT in the allocation map                            450
```

**"SmartX believes it manages accounts the 49F universe no longer contains" is true of exactly 2
accounts, not of the 452.** The other 450 long-absent-but-open accounts carry no SmartX allocation,
so no vendor asserts management of them. Oldest `absent_from_feed_since` in the class: 2024-07-11.

### THE OTHER TWO MEMBERS -- and one of them is NEW

The class was 3 at the contract's 2026-08-19 measurement. **At 2026-08-28 it is 4.** Both
non-Vanguard members are *different states* and should not be folded into the departure finding:

- **`0010299365` "49 FINANCIAL"** -- **NEVER PRESENT, not departed.** 0 of 540 partitions of
  `08335338`, 0 of 659 of `08242234`, and **absent from `dim_account` entirely**. Carries
  $188,230.64 on Opal Ultra Short-Term Income, roster status open. Reads as a firm/house account
  that was never in the client account universe. (The contract already recorded "present at neither
  end"; this confirms it and adds that it is absent from the account dimension too.)
- **`0042708566` "KRISTI STOGO CHARLES SCHWAB & CO INC CUST IRA ROLLOVER"** -- **A NEW MEMBER, and
  it is one day old, not eighteen months.** `first_seen_date` 2026-05-19, `acc_as_of` 2026-08-27,
  `absent_from_feed_since` **2026-08-28**. $1,061,278.26. **Do not conflate it with the pair** -- a
  one-day absence is most likely a transient feed gap. **It needs a re-read on the next business
  day, not an investigation.** I flag it because the class grew silently between the contract's
  vintage and today, which is the kind of drift a fixed "3" in a ratified document will hide.

---

## PART 1 -- WHAT THE 13 NINE-DIGIT KEYS ARE

### D3.1b-1: characterised, on evidence, with denominators

**ANSWER: they are a SECOND CUSTODIAN'S ACCOUNT GRAMMAR -- Fidelity-registered accounts
(`FMT CO` / `FMTC` = Fidelity Management Trust Company) sitting inside a 49F-scoped SmartX feed.**
This is the "second custodian's grammar" candidate the TO listed, now **measured rather than
assumed** -- and the measurement is two-sided.

At `date=2026-08-28`: **18 rows, 13 distinct keys, all exactly 9 digits, $12,293,768.23**.

**THE EVIDENCE IS THE `account_name` COLUMN -- WHICH THE CONTRACT'S OWN INSTRUMENT NEVER READS.**
`a06_dim_identity_crosswalk.py:108` selects only `allocation_id`, `account_id`, `account_number`.
The custodian was in the map the whole time, one column over from the ones that were looked at.

| | count | denominator |
|---|---|---|
| 9-digit rows carrying an `FMT`/`FMTC` registration | **15** | of 18 |
| distinct 9-digit keys carrying it | **11** | of 13 |
| **8-digit rows carrying `FMT`/`FMTC`** | **0** | **of 7,341** <- the discriminating control |
| **9-digit rows carrying `SCHWAB`** | **0** | **of 18** <- the reverse control |
| 8-digit rows carrying `SCHWAB` | 4,383 | of 7,341 |

**The two grammars carry two DISJOINT custodian registrations, in both directions.** That is the
control that makes this a finding rather than a pattern: if the 9-digit keys were legacy 49F Schwab
numbering, FMT registrations would not be perfectly confined to them.

The 13 keys, with names:

| key | rows | AUM | registration |
|---|---|---|---|
| 346482072 | 1 | 819,908.31 | FMTC CUSTODIAN - SIMPLE & NANOHMICS INC & FBO MICHAEL WILLIAM MAYO |
| 628629323 | 3 | 1,121,716.50 | FMT CO CUST IRA & FBO ALETA M WOLF |
| 628629325 | 1 | 43,841.54 | FMTC CUSTODIAN - ROTH IRA & FBO ALETA M WOLF |
| 638330272 | 1 | 502,643.41 | FMT CO CUST IRA ROLLOVER & FBO ROY ANTHONY HOLLIER III |
| 638357130 | 1 | 197,804.62 | FMT CO CUST IRA & FBO STEPHANIE YORK |
| 638357389 | 1 | 27,713.04 | FMTC CUSTODIAN - ROTH IRA & FBO STEPHANIE YORK |
| 638379681 | 1 | 797,813.96 | FMT CO CUST IRA & FBO JAMES HIBBLER JR |
| 638380768 | 1 | 340,263.54 | FMT CO CUST IRA ROLLOVER & FBO SHANE A THOMAS |
| 638421860 | 1 | 267,230.28 | FMTC CUSTODIAN - ROTH IRA & FBO JASON LONG |
| 638451957 | 1 | 347,173.50 | FMT CO CUST IRA & FBO CHRISTOPHER RICHEY |
| **645624489** | 1 | 1,707,003.94 | **BRADLEY, CHRISTOPHER TODD** -- no custodian designation |
| 655417044 | 3 | 5,665,906.31 | FMT CO CUST IRA & FBO JEANE ANN THOMAS |
| **655417051** | 2 | 454,749.24 | **JEANE ANN THOMAS** -- no custodian designation |

**The 2 keys without a custodian designation do NOT imply a third custodian, and I am not claiming
they do.** `655417051` (JEANE ANN THOMAS) sits **7 apart from** `655417044` (FMT CO CUST IRA & FBO
JEANE ANN THOMAS) -- same person, same numbering block. The same pattern holds for ALETA M WOLF
(`628629323` IRA and `628629325` Roth IRA, 2 apart). A non-IRA account carries no trustee
"CUST FBO" registration at all, so a bare personal name in the same block is **consistent with** the
same custodian. Consistent-with is not proven, and I leave it there.

Numbering blocks across the 13 distinct keys: `3464`(1) `6286`(2) `6383`(5) `6384`(2) `6456`(1)
`6554`(2) -- clustered, not scattered, which is what a single custodian's issuance looks like.

### What I ruled out, and how

- **The instrument that would have settled it outright is DEAD, and I checked rather than assumed.**
  `smartx/platform/silver/fact_account_detail` carries **`custodian_name` and
  `brokerage_account_number`** -- exactly the discriminator. But **only 1 of its 46 partitions has
  content** (2026-07-14, 91 rows, `custodian_name='Schwab'` 91 of 91), and **0 of the 13 keys appear
  in it**. Every partition 2026-07-15..2026-08-29 is 14,375 B and empty. So a direct
  `custodian_name` read is **not available**; the registration-string evidence is what exists.
- **Vendor test/synthetic residue: rejected.** Inconsistent with 15 of 18 rows carrying real client
  registrations, $12.29M of real AUM, and coherent IRA/Roth pairings per named person.
- **Legacy pre-zfill 49F numbering: rejected** by the reverse control -- legacy Schwab numbering
  could not produce FMT registrations that appear on *zero* of 7,341 Schwab-grammar rows.
- **The relaxed-join control from the contract still holds** (0 of 13 present when zfilled to 10):
  these are not paddable Schwab keys.

**RESIDUAL UNKNOWN, named rather than papered over:** that `FMT CO`/`FMTC` is the registration
abbreviation for *Fidelity Management Trust Company* is standard custodial nomenclature, **not
something I measured in-estate** -- the estate carries no custodian dimension naming Fidelity
(`dim_account.money_manager` census: SmartX Advisory Solutions 8,210, blank 413, Opal Capital LLC 7,
PIMCO 2, Nuveen 1). **What is measured is that a second, non-Schwab custodian's grammar is present
and disjoint. Which custodian it is, by name, needs a registry or vendor check outside my cap.**

### D3.1b-2: THE SCOPE QUESTION, FRAMED FOR A DECISION (I do not decide it)

> **Is the 49F SmartX feed scoped to the 49F *Schwab book*, or to the 49F *book regardless of
> custodian*?**

Both readings are internally consistent with the data, which is precisely why it is not a data
question and cannot be settled in this lane. **What turns on it:**

| if 49F means... | then the 18 rows / $12.29M are... | and the remedy is... |
|---|---|---|
| the **Schwab book** | **foreign paper in a 49F-scoped feed** | upstream **feed scoping** -- not a new enum value |
| the **book, any custodian** | evidence the account universe is **structurally incomplete by $12.29M** | a **second universe source** |

**Whose call:** `1.0.0_SA_CTO` gates the cross-package contract, but the underlying question --
which custodians constitute the 49F book -- is a **firm-scope business fact, not an engineering
choice**. **My read: it reaches Andrew.** The TO records that CTO reads it as possibly sovereign; I
agree, and I have framed it rather than raising it raw, as asked.

**IT DOES NOT CHANGE THE RATIFIED AXIS EITHER WAY.** `KEY_OUTSIDE_ACCOUNT_GRAMMAR` remains the
correct *outcome* label under both readings. **The scope answer changes the REMEDY, not the
classification.** No enum amendment is implied by this report, and I propose none.

---

## FINDINGS FOR OTHER OWNERS -- surfaced, not chased, not fixed

**1. DECLARATIVE DRIFT ON THE RATIFIED CONTRACT -- the universe comment names the wrong account.**
`data/_contracts/smartx_bd_join_disposition.yaml` `measurement.as_of_universe` reads
`# schwab/08242234/silver/fact_acc`. **The universe actually measured is `schwab/08335338`.**
Discriminated by reproducing all three of the contract's own denominators against both candidates:

| | `schwab/08335338` | `schwab/08242234` | contract says |
|---|---|---|---|
| partitions <= 2026-08-18 | **532** | 651 | 532 |
| fact_acc accounts @ 2026-08-18 | **7,316** | 7,240 | 7,316 of 7,316 |
| allocation map rows @ 2026-08-19 | 7,305 | 7,305 | 7,305 |

**All three reproduce against `08335338`; none against `08242234`.** The contract's prose grounding
("532 fact_acc partitions (2024-07-08 .. 2026-08-18)") and the runner constant agree --
`runner_common.SCOPE = "schwab/08335338"`, unchanged since `941811c31f` (2026-08-11), and that is
its value **at the ratification commit `f097698bf6` itself**. Only the comment disagrees.
**SUBSTANCE UNAFFECTED: every measured number in the contract is correct.** The risk is a future
re-deriver reading the comment, pointing at `08242234`, getting **7,240**, and computing a different
residual. **Not fixed here** -- the contract is RATIFIED and amending it is a taxonomy act with an
owner (`1.0.0_SA_CTO` gate).

**2. THE `OTHER_CUSTODIAN` REJECTION RESTS PARTLY ON A GROUNDING THAT IS NOW FALSE -- and the
retraction is scoped to that clause only.** The contract rejects `OTHER_CUSTODIAN` on two grounds:

- *"A CAUSE, NOT AN OUTCOME (Rule 24(iii))"* -- **STANDS, UNAFFECTED.** Custody is a cause axis, not
  a join-outcome value. This ground alone sustains the rejection.
- *"AND IT WOULD BE INFERRED ... No evidence in the measured data names a custodian for the 9-digit
  keys"* -- **FALSIFIED.** `account_name` names one, in 15 of 18 rows. The claim is true of the
  three columns `a06` selects and false of the allocation map it selects them from.

**The rejection's CONCLUSION survives on its surviving ground. Only its second reason is wrong.** I
am not proposing the value be added -- 24(iii) still excludes it from this axis.

**3. OBSERVATION (off-task, one line, no action taken).** The served ModelPortfolios AUM table
(DynamoDB `opal-data-smartx`) has its latest `TIMESERIES#*#Daily` period at **2026-01-12**
(`last_updated` 2026-01-21) across the 5 named models, with a single unnamed-model item at
2026-05-29. Surfacing only; not my TO, not investigated, no owner asserted.

**4. OBSERVATION.** `in_account_universe` -- the flag `dim_identity_crosswalk` writes to distinguish
residual rows -- occurs **exactly once in 131,804 files scanned: the writer itself. ZERO readers.**
The residual is correctly carried and correctly flagged, and nothing consumes the flag. This is
**not currently producing a wrong number** (nothing downstream counts the residual, per D3.1b-4),
but the guard is **unexercised**, and an unexercised guard is the one that fails when a future
consumer joins on the crosswalk without it.

---

## What this report does NOT do

- **No remediation.** No enum value added, no contract edited, no data corrected, no allocation
  closed. The two contract findings above are routed, not fixed.
- **No vendor call.** Every number is a read of artifacts already landed in Opal S3/DynamoDB.
- **Nothing to `4.0.0_SA_CRO`** -- the GO's cap supersedes the face's CRO cc; flagged in my ACK.
