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
> >> So `perfrp_book_advisor` is **MORE OF THE SAME SHAPE AT LARGER SCALE (3,297 vs 190), NOT A NEW
>    EXPOSURE CLASS.** The 9,868/9,868 census below stands as a true measurement of the leaf; it is
>    NOT a live blocker, and no seat may cite this file to hold a serve. <<
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
