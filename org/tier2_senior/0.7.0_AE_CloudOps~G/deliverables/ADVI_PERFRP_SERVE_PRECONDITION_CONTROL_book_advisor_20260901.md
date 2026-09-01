# ADVI_PERFRP SERVE PRECONDITION -- THE CONTROL, RUN. **TWO LIMBS, TWO DIFFERENT ANSWERS**

> ⛔⛔ **SCOPE YOUR CITATION OF THIS FILE TO A LIMB. THE PRECONDITION HAS TWO AND THEY DIVERGED ON
> 2026-09-01. AN EARLIER VERSION OF THIS HEADER SAID "the precondition is SUPERSEDED, do not block a
> serve on this file" -- THAT WAS TRUE OF ONE LIMB AND WOULD HAVE CLEARED THE OTHER.**
>
> | limb | status |
> |---|---|
> | **CLIENT DISPLAY LABEL** | **SUPERSEDED.** Andrew ruled directly; premise measured false (labels already on 5 of 12 served advi keys). See the note below. Do NOT hold a serve on this limb. |
> | **CUSTODIAN ACCOUNT IDENTIFIER** (+ book-scoping) | ⛔ **NOT DISCHARGED. UNRESOLVED, which is not dischargeable** (`1.0.0_SA_CTO` 90449). See §2a/§2b. |
>
> **`relationship` is ONE FIELD carrying BOTH limbs**, and that is the trap: tonight the names in it
> became permitted while the account ids in it stayed forbidden. A reader who takes "superseded" as a
> property of the FIELD rather than of ONE LIMB will stop scrubbing exactly where the live trigger is.

> ⛔⛔ **READ THIS BEFORE THE VERDICT BELOW. ANNOTATED 2026-09-01 ~00:1xZ, SAME SESSION.**
> **The measurement in this file is CORRECT and the precondition it tests is SUPERSEDED.** Those are
> not in tension and the distinction is the whole point of this note.
> `1.0.0_SA_CTO` 90406 lifted the halt and RESUMED CALL 2 after measuring, at source on the LIVE
> SERVED plane, that **the precondition's premise is FALSE: client display labels are ALREADY served
> on static advi keys today** -- `platinum/advi/49financial/partner_analytics_annual.json` carries
> `"label": "WILLIAM CHAN"`, and **5 of 12 served advi keys carry real client labels** (190 / 171 /
> 88 / 88 / 88). Router history corroborates on a different plane: a PII fix was attempted at v10/v11
> and **REVERTED at v12**. **ANDREW RULED IT DIRECTLY, VERBATIM:** *"This does not matter, client
> names are already published throughout the Advisor Intelligence views"* -- he is sovereign on firm
> exposure and answered with the fact in front of him.
> >> So on the CLIENT-LABEL limb, `perfrp_book_advisor` is **MORE OF THE SAME SHAPE AT LARGER SCALE,
>    NOT A NEW EXPOSURE CLASS**, and no seat may cite this file to hold a serve **ON THAT LIMB**. <<
> ⛔ **TWO SCOPE CORRECTIONS TO THIS PARAGRAPH, BOTH MADE LATER THE SAME NIGHT — it was written before
> either was known, and left unscoped it over-clears:**
> **(i)** the counts it leaned on are wrong — the "9,868/9,868" and the distinct figure are the
> INCONSISTENT ones §2a retracts, and the distinct count is INFLATED by sentinel strings. Do not quote
> a number from this paragraph.
> **(ii)** *"not a live blocker"* is true of the CLIENT-LABEL limb ONLY. The **CUSTODIAN limb is
> NOT DISCHARGED** and is tripped on **3 of the 4 publishable leaves** (§6). **This file DOES hold a
> serve on that limb.**
> ⚠ **WHY THIS ANNOTATION EXISTS AT ALL:** `1.0.0_SA_CTO` 90406 s.6 names the real defect -- the
> precondition sits ARMED in `org/projects/ADVI_PERFRP.json` `blocking` encoding a posture the estate
> abandoned at router v12, and **it will trip EVERY future serve until retired.** That record is CTO's
> to rewrite. **This file is the same hazard one carrier down**: an artifact of mine, titled UNMET,
> that a future reader would find and treat as current. Annotating it is the same stale-carrier
> discipline this lane applied to the TO face all session -- a correction is only as complete as its
> last surviving carrier.
> **What survives as genuinely useful here:** §1 (a docstring is not a state -- `book_advisor`
> WOULD_PUBLISH where I predicted it would refuse) and §3 (a partially-pseudonymised row makes an
> id-field check return a FALSE ALL-CLEAR beside an untouched name field). Both are instrument
> lessons and neither depends on the precondition being live.

**Author:** `0.7.0_AE_CloudOps~G` (the ruled OWNER: "the serving design (publisher lane / 0.7.0)")
**PRD author / discharge authority:** `1.0.0_SA_CTO` · **Date:** 2026-09-01 ~00:0xZ
**Raised by:** `0.4.0_DE_ClientPlatform~D` (90357, `[STOP]`) · **HOLD:** `2.0.0_SA_COO` 90365
**Plane:** the payload the publisher WOULD WRITE, built at the current vintage. Nothing was published.

## 0. The precondition (`org/projects/ADVI_PERFRP.json` `blocking`, 2026-08-28)

> served perfrp leaves carrying the client display label OR a custodian account identifier in any
> label/identity/key field owe the SAME server-side pseudonymisation + book-scoping as platinum
> summary.json (Lambda@Edge, **no static key**) **BEFORE any serve/flip**; CONTROL = a census over
> every served row: no name field AND no custodian account id, both denominators, positive control.

## 1. FIRST: A DERIVED CLAIM OF MINE THAT MEASURED FALSE

My 90349 gave a derived expected census listing `perfrp_book_advisor` among the families that
`emitter_refused` **by design**, citing `chain_49f_entrypoint.py`'s docstring and its
*MEASURED 2026-08-25: {would_publish: 6, emitter_refused: 5}*. **Measured false tonight.**

```
  DRY RUN -- no --publish, no OPAL_ADVI_PUBLISH_GRANT, ZERO S3 writes:
    WOULD_PUBLISH  perfrp_book_advisor -> platinum/advi/49financial/perfrp_book_advisor.json
    DENOMINATOR: 1 twin(s) attempted of 26 EMIT twins (23 emitter entries); 0 not clean
```

`book_advisor` **BUILDS and WOULD PUBLISH.** The 08-25 census is STALE -- round-2 wired the plane the
docstring says round 1 does not (`perfrp_emit_core` moved 2026-08-29 @`62a00eed67`).
**A docstring is a description, and a description is never a state.** Anyone resting on my 90349 would
have concluded the leaf never serves and the exposure was moot.

## 2. THE CONTROL -- census over EVERY served row

⛔⛔ **THE BLOCK BELOW IS THE ORIGINAL AND THREE OF ITS LINES ARE MUTUALLY INCONSISTENT. CORRECTED
IMMEDIATELY AFTER IT — READ BOTH. `1.0.0_SA_CTO` 90449 ruled this control NOT SOUND EVIDENCE for the
custodian limb while these figures stand, and that ruling is right.**

```
  client_table rows (DENOMINATOR) .........: 9,868
  rows whose `relationship` is a REAL NAME : 9,868      <- 100%, not a subset   [WRONG]
  DISTINCT REAL CLIENT NAMES ..............: 3,297                              [INFLATED]
  rows UNMAPPED-RELATIONSHIP-* ............: 0                                  [WRONG]
  rows pseudonymous in `relationship` .....: 0

  POSITIVE CONTROL (these SHOULD be pseudonymous; 0 = pass):
    rows where `client` NOT rel_* .........: 132
    rows where `relationship_id` NOT rel_* : 132
```

### 2a. CORRECTED — the three lines were ONE population counted twice with opposite verdicts

Caught by `3.0.0_SA_CVO` 90437; both candidate mechanisms it named are confirmed, and both are mine.
The read `3.0.0_SA_CVO` asked for and `1.0.0_SA_CTO` 90449 s.3 adopted, run:

```
  PATTERN USED:  PSEUDO = ^rel_[0-9a-f]+$
                 elif rel.startswith('UNMAPPED-RELATIONSHIP')      <- the arm that returned 0

  3 SAMPLES from the 132 rows the positive-control arm flagged:
    relationship    = 'UNLABELLED-RELATIONSHIP:UNMAPPED-RELATIONSHIP:0017633210'
    client          = 'UNMAPPED-RELATIONSHIP:0017633210'
    relationship_id = 'UNMAPPED-RELATIONSHIP:0017633210'

  of those 132, startswith('UNMAPPED-RELATIONSHIP') matches:  0
```

- **(a) HYPHEN-VS-PREFIX:** the value begins `UNLABELLED-`, not `UNMAPPED-`. The prefix arm could never
  fire, so the sentinel population reported as **0**.
- **(b) THE DETECTOR WAS NEGATION-DEFINED** — "REAL NAME" meant *not `rel_*`, not the prefix*. All 132
  sentinel strings fell through to `else`, were counted as real names, and were added to the distinct
  set. **This is the worse mechanism because it is SELF-CONSISTENT**: it produces 100% and 0 together.
- ⛔ **THEREFORE `DISTINCT REAL CLIENT NAMES = 3,297` IS INFLATED BY SENTINEL STRINGS AND MUST NOT BE
  QUOTED.** A negation-defined detector cannot distinguish *a name* from *any non-pseudonymous string*.

### 2b. ⛔ AND IT LANDS ON THE **SURVIVING** LIMB, NOT THE SUPERSEDED ONE

```
  DISTINCT >=6-DIGIT NUMERIC TOKENS embedded in those `relationship` values: 57
    samples: 0012581195  0013341925  0014816851  0015346352  0017329807
```

Ten-digit, zero-padded — the same shape as the schwab custodian ids quoted at `1.0.0_SA_CTO` 90328 s.3
(`0022002671`, `0026881039`, `0065125789`). They sit in `client` and `relationship_id` **too**, so for
these 132 rows pseudonymisation is absent across all three fields.

### ⛔ CONFIRMED BY JOIN — these are REAL custodian account identifiers, not account-SHAPED strings

An earlier revision of this section read *"SHAPE-CONSISTENT, NOT CONFIRMED."* **That is now understated
in the direction that matters.** The join, with controls in both directions:

```
  DENOMINATORS
    distinct sentinel tokens from the 132 rows : 57
    dim_account account_id population          : 8,633 (rows 8,633)

  JOIN: tokens present as a real dim_account.account_id ....... 57 of 57
    samples: 0012581195  0013341925  0014816851  0015346352  0017329807

  POSITIVE CONTROL (the three schwab ids at 1.0.0_SA_CTO 90328 s.3):
    0022002671 True    0026881039 True    0065125789 True
  NEGATIVE CONTROL:
    9999999999 False
```

Both directions hold — the instrument CAN see real ids and does NOT match everything. **57 of 57.**

>> **THEREFORE THE 08-28 RECORD IS FALSE ON MEASUREMENT, NOT MERELY SUSPECT.** It states this
   population was *"replaced by an opaque id at the re-open with the label-field removal."*
   **An opaque id does not resolve in `dim_account`. These do, all 57.** The replacement either never
   landed or did not hold, and the record has carried it as done for twelve days. <<

**REMEDY OPTIONS (reported, not chosen — `1.0.0_SA_CTO` rules):** (a) `--hold-leaves
perfrp_book_advisor` on the activation — available immediately in this lane, the publisher already
carries the flag and it BUILDS + manifests but never writes; (b) a producer-side opaque-id fix in the
DS emitter — durable, and the one the 08-28 record already believed had happened.

⭐ **AND THE FACT THAT MAKES THIS MORE THAN A CONTROL BUG** (`1.0.0_SA_CTO` 90449 s.2): the 08-28
precondition text *itself names this population* — *"the UNMAPPED sentinel token, **132 rows,
ten-digit account-shaped** — CVO 79804; **replaced by an opaque id** at the re-open with the
label-field removal."* Same sentinel, same cardinality, **twelve days later**. The believed
remediation either never landed or never held, and **the record has carried it as done since 08-28**.

>> **THE SUPERSESSION HAZARD, which is why this file needed correcting rather than deleting:
   `relationship` is ONE FIELD carrying BOTH limbs. Tonight the names in it became PERMITTED and the
   account ids in it stayed FORBIDDEN. A seat reading "the client-label limb is superseded" stops
   scrubbing that field — and the surviving trigger lives in the same field, in exactly the rows where
   the name is ABSENT.** <<

>> **VERDICT: UNMET.** A cleartext client-name field is present in every served row of a leaf that
   would be written to a STATIC key -- estate-wide authenticated-fetchable, irreversibly. <<

## 3. ⛔ THE DANGEROUS SHAPE: THE LEAF IS **PARTIALLY** PSEUDONYMISED

Row schema, read at source (three separate fields):

```
  client           = 'rel_05b7c126ca6dcf'        <- pseudonymised
  relationship_id  = 'rel_05b7c126ca6dcf'        <- pseudonymised
  relationship     = 'DIANNE AZZUNZIATA BARBER'  <- CLEARTEXT CLIENT NAME
```

**MY OWN FIRST CENSUS RETURNED A FALSE ALL-CLEAR ON EXACTLY THIS.** I guessed field names instead of
reading the row schema; the matcher hit `client` first, found `rel_*`, and scored the leaf label-free.
It was caught only because the printed sample did not look like names.

> **A pseudonymisation check that lands on the id fields PASSES while the name field sits untouched
> beside them.** "Is it pseudonymised?" is unanswerable without naming WHICH FIELD. Any
> re-verification of this leaf must census `relationship` specifically, and print its denominator.

## 4. LIMITS -- what this control does NOT cover

- **CLIENT-NAME limb only.** The CUSTODIAN-ACCOUNT-ID limb is not swept exhaustively here:
  `entries[].accounts` is an INT COUNT, not a list, so there is no per-account id surface at that
  path -- but that is one path, not a census. Prefer `3.0.0_SA_CVO`'s measurement on that limb.
- **ONE LEAF.** This covers `perfrp_book_advisor`. The precondition is written over "served perfrp
  leaves" **plural**, and the other ten families were NOT censused for the same defect. That gap is
  real; a ruling must not assume this one-leaf census covered the set.
- Numbers differ from 90357's 3,290 because that seat measured the COMMITTED origin/CLOUD artifact and
  this measures a payload BUILT at asof 2026-08-31 (inputs ALIASED from 08-28, declared by the port).
  Different objects, same conclusion; neither corrects the other.

## 5. OPTIONS (reported, not chosen -- the ruling is `1.0.0_SA_CTO`'s)

| | act | lane |
|---|---|---|
| (a) | `--hold-leaves perfrp_book_advisor` on the activation -- the publisher ALREADY has this flag; it BUILDS + manifests but never writes the leaf, so the other families serve while this one waits | this lane, available immediately |
| (b) | pseudonymise `relationship` at the emitter to match the `client`/`relationship_id` treatment already applied beside it | DS emitter lane -- the DURABLE fix |

**"Hold everything" and "publish the names" are not the only two options, and (a) is why.**

⛔ This lane will not activate on ANY signal until `1.0.0_SA_CTO` rules -- including a re-issued CALL-1
completion report.

---

## 6. THE PLURAL CENSUS -- all 11 families, and it MOVES THE REMEDY

This file was scoped to ONE leaf and said so. That gap is now closed. Dry run, all 11 PERFRP families
(`perfrp_emitters.PERFRP_EMITTER_FAMILIES`, the one definition), no `--publish`, no grant, zero S3 writes.

### 6a. The attempted set is not what anyone had been quoting

```
  WOULD_PUBLISH (4):   perfrp_performance_account   perfrp_gainloss_relationship
                       perfrp_gainloss_account      perfrp_book_advisor
  EMITTER_REFUSED (7): activity_rel, activity_acct, performance_rel, allocation_rel,
                       allocation_acct, transactions_rel, roster_rel
  DENOMINATOR: 11 attempted of 26 EMIT twins (23 emitter entries); 7 not clean
```

⛔ This contradicts `chain_49f_entrypoint.py`'s documented 2026-08-25 census
`{would_publish: 6, emitter_refused: 5}` **in both directions** -- gainloss rel+acct were listed as
refusing BY DESIGN and now PUBLISH; performance_relationship published and now REFUSES.
**The set has moved twice. Stop quoting that docstring -- including this lane's own quotations of it
at 90349.** The number that matters for a grade is not "10 of 11 attempted" but **4 that would write**.

### 6b. Custodian ids across every built payload

Joined against `dim_account` (8,633 ids). POSITIVE CONTROL `0022002671` True; NEGATIVE `9999999999` False.

| leaf (WOULD_PUBLISH) | real custodian account ids |
|---|---|
| `perfrp_performance_account.json` | **8,632** -- essentially the entire account universe |
| `perfrp_gainloss_account.json` | **6,183** |
| `perfrp_book_advisor.json` | **57** |
| `perfrp_gainloss_relationship.json` | 0 |

>> **THE LIMB IS TRIPPED ON 3 OF THE 4 PUBLISHABLE LEAVES, AND `book_advisor` IS THE SMALLEST INSTANCE
   BY TWO ORDERS OF MAGNITUDE.** <<

### 6c. ⛔ SO REMEDY (a) AS THIS FILE FIRST STATED IT IS WRONG, AND THE ERROR IS THIS LANE'S

`--hold-leaves perfrp_book_advisor` **would hold the leaf carrying 57 and publish the leaf carrying
8,632.** It was proposed having censused exactly one leaf -- the same one-leaf-reads-as-the-set mistake
this lane spent the night naming in other people's work. If taken, the hold list is at minimum
`perfrp_book_advisor,perfrp_performance_account,perfrp_gainloss_account`, i.e. the serve becomes one leaf.

### 6d. TWO DIFFERENT CASES -- not conflated, and the ruling probably turns on this

```
  ACCOUNT-GRAIN    entries[].key = '0010020692' -- a RAW custodian account id as the entity KEY.
                   performance_account (8,632), gainloss_account (6,183). The leaf's NATURAL GRAIN;
                   may be accepted design rather than a leak.
  RELATIONSHIP-GRAIN  book_advisor: client / relationship_id ARE pseudonymised to rel_*; the 57 leak
                   through the UNLABELLED sentinel into a field where a pseudonym was expected.
                   gainloss_relationship: 0 -- the scheme holds there.
```

The estate's pattern is coherent: **relationship grain is pseudonymised, account grain is keyed raw.**
The 57 are an ESCAPE from a working scheme; the 8,632/6,183 are the scheme not existing at that grain.
⚠ **But the precondition's text does not grant that distinction** -- it says *"a custodian account
identifier in any label/identity/**key** field."* Key fields are named. Whether account-grain keys were
always in scope, or the clause was written with only the label case in mind, is a **PRD-author
question** (`1.0.0_SA_CTO`), not this lane's.

### 6e. LIMITS

BUILD plane, not served -- nothing published. The `.verification.json` siblings also carry ids
(5,208 / 6,183 / 6,183) but the dry run does NOT list them as WOULD_PUBLISH, so they are excluded from
the served set here and it is NOT confirmed whether another path serves them. **This pass is the
CUSTODIAN limb only** -- the client-name limb is not censused across the other three leaves.

---

## 7. THE DECISIVE TEST -- are raw custodian ids ALREADY SERVED today? **YES**

`3.0.0_SA_CVO` 90481 s.2 named the one unrun test and set its own branch conditions: the client-label
limb was superseded not by argument but because the LIVE SERVING PLANE was measured and its premise
failed. **The parallel test for the custodian limb, run here.** It needs the serving plane, which is
this lane's.

All served advi keys listed via `s3api`, pulled, every string walked for >=6-digit tokens, joined
against `dim_account` (8,633 ids). POSITIVE CONTROL `0022002671` True; NEGATIVE `9999999999` False.

| served key | tokens | REAL custodian acct ids |
|---|---|---|
| `ownership_map.json` | 5,969 | **5,208 — SERVED, TODAY** |
| `cumulative_chart.json` | 27 | 0 |
| `partner_analytics_annual.json` | 55 | 0 |
| `partner_analytics_quarterly.json` | 43 | 0 |
| `timeseries_chart{,_full}.json` | 28 | 0 |
| `clients-tab-slim` / `leaderboard` / `mix_summary` / `timeseries_overview` | 0 | 0 |

**DENOMINATOR: 10 served data keys** (12 objects; 2 are `_manifests`, excluded).

### 7a. Not a coincidental token match -- the structure was read, not trusted

```
  ownership_map.json   generated_at 2026-08-21T15:03Z, firm_id 49financial
    advisors: 146, keyed by advisor slug ('abby_horton')
      accounts      = ['0015027485','0017926421','0026661490', ...]    <- RAW custodian ids, NAMED FIELD
      relationships = ['rel_05b7c126ca6dcf','rel_2892aa2691dd70', ...] <- PSEUDONYMISED
```

>> **THE SERVED PLANE ALREADY CARRIES RAW CUSTODIAN ACCOUNT IDS IN A FIELD LITERALLY NAMED `accounts`,
   AND HAS SINCE 2026-08-21** -- exhibiting the exact convention measured in the unserved perfrp
   leaves at §6d: **account grain raw, relationship grain pseudonymised.** The pattern is not only
   coherent, it is already in production. <<

So `3.0.0_SA_CVO` 90481's own IF-YES branch applies: *the custodian limb's premise is false the same
way the label limb's was, the same precedent applies, and this is more-of-the-same-shape rather than a
new exposure class.*

### 7b. ⚠ TWO PLACES THE PARALLEL IS WEAKER THAN THE LABEL CASE

Stated so no ruling is handed a cleaner story than the evidence supports:

- **BREADTH:** the label limb was already served on **5 of 12** keys. This is **1 of 10**. One live
  instance is a thinner precedent than five.
- **SCALE:** 5,208 served today vs **8,632** in `perfrp_performance_account` — 1.66x, so
  "more of the same shape at larger scale" is fair, but it would still be the largest single instance
  the estate holds.

Neither weakens the PREMISE finding: the premise was *"raw custodian ids are not served on static
keys"*, and that is now **false on measurement**.

### 7c. THIS IS NOT A DISCHARGE, AND THIS LANE IS NOT RULING

The label limb was superseded by **Andrew**, on a measured premise — not by the measurement alone.
This supplies the same CLASS of premise for the custodian limb. Whether it discharges, and whether the
convention should extend to 8,632, is `1.0.0_SA_CTO`'s call and his.
**Still open:** the client-name limb across the other three publishable leaves is uncensused, and the
`.verification.json` siblings' serve path is unconfirmed.
