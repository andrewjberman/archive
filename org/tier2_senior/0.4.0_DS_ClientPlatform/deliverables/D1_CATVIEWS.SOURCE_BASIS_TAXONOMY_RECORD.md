# `source_basis` — Rule 24 four-postulate record + word-boundary token census

**Author:** `0.4.0_DS_ClientPlatform~Z` · **2026-08-29** · **Cell:** D1_CATVIEWS increment 3, leg B
**Authority:** Andrew-direct 2026-08-29 *"this is an SMA, so our logic on models + smas simply has
to change, the plug doesnt work with this in mind."* Shape proposed by `1.0.0_SA_CTO~Z` (15917),
gate lifted by them (16047); external-test requirement from `3.0.0_SA_CVO~Z` (15942).

⛔ **AUTHOR-MEASURED, NOT CERTIFIED.** No independent certifier has signed this record. Anything
citing it inherits that status.

> **CITATION CONVENTION, and it is a limitation not a style choice.** Every bare `NNNNN`
> below is a broker Msg-ID **as delivered to `0.4.0_DS_ClientPlatform~Z`**. Measured
> 2026-08-29: one send writes ONE FILE PER RECIPIENT with a DIFFERENT id and a
> byte-identical body (one send -> 4 copies, ids 15849-15852, body md5 x1; a second ->
> 6 copies, ids 15934-15939, md5 x1). **So these ids resolve in THIS seat's inbox and
> nowhere else** -- another seat's copy carries a different number, and that number
> exists there pointing at an unrelated message, so the mismatch is SILENT. Each
> citation names its SENDER's serial, which is the half that survives delivery; to
> locate the exact message use the sender + the quoted content, or the stable
> `YYYYMMDDTHHMMSSZ_<sender>` filename prefix, which is identical in every copy.

---

## 0. WHY A RECORD AT ALL

Rule 24: *a value-enum proposal arrives WITH its four-postulate record + word-boundary token
census, or it is not a proposal.* This adds a value enum (`SMA_BASIS_VALUES`) to a **packaged
member** on a surface that decides an advisor-facing money figure, so it owes the record.

## 1. THE DECLARED DOMAIN — stated before the values, because the postulates are scored against it

> **For one registered SMA member: is the money it represents ALREADY INSIDE the population the
> firm total is built from (schwab 0824 / `non_model_aua`), or is it OUTSIDE that population?**

The domain is **members of `SMA_MEMBERS`**, and nothing else. Models members are not in the domain:
their dollars are inside `model_aua` by construction, so the question does not arise — they carry
`source_basis=None` meaning **NOT ON THIS AXIS**, which is distinct in kind from an undeclared basis
(the import check makes an undeclared SMA basis unreachable).

## 2. THE FOUR POSTULATES

### (i) MECE over the declared domain
| value | means | covers |
|---|---|---|
| `carve_out` | inside the firm-total population | the member's accounts sit in 0824 |
| `additive` | outside it | the member's accounts sit anywhere else |

**Exhaustive:** the two are inside/outside a single named population — a member's accounts either
are in 0824 or are not; there is no third location. **Disjoint:** an account cannot be both.
⛔ **THE UNCOVERED MEMBER I HUNTED FOR, AND IT IS REAL: a member with NO ACCOUNTS AT ALL.** `muni`
is exactly that (Andrew: *"Muni to my knowledge does not exist yet"*), as are `idvz` and `pfde`
(no dollars today). The location predicate has no truth value for an empty account set.
**RESOLVED BY DECISION, NOT BY A THIRD VALUE** — see §4. Adding an `UNDETERMINED` member would
have violated (iii), because "I have not measured it" is a *measurement-state* fact and the axis is
a *location* fact. Two axes in one field is the failure Rule 24(iii) names.

### (ii) SAME GRAIN
Both values describe **one registered SMA member's account population**. Neither is a property of a
dollar amount, a firm, a bucket, or a feed. `carve_out` and `additive` are the same kind of thing
about the same kind of object.

### (iii) INTENT COHERENCE — one axis, one intent
The axis measures **WHERE THE ACCOUNTS LIVE**. It deliberately does NOT encode:
- whether the member has a `strategy_id` (that axis exists and CROSSES this one),
- which L1 bucket it sits in (ETF vs ALT — `tax` is ALT and additive, `muni` is ALT and carve-out,
  so the two axes are not co-extensive and must not be derived from each other),
- whether the basis has been VERIFIED (that is §4's separate coverage statement, deliberately kept
  out of the value).

### (iv) STATE COHERENCE — name what one remedy does NOT move
`source_basis` moves **only when a member's accounts move custodian**, which is a firm event.
It does NOT move when the member gains a `strategy_id`, gains its first dollars, changes bucket,
or is served/unserved. ⛔ **And no remedy on any downstream identity moves it** — every identity is
built from these labels and re-satisfies under a wrong assignment (`3.0.0_SA_CVO~Z` 15942), so
"the numbers reconcile" is never evidence that a basis is right.

## 3. ⛔ THE TOKEN CENSUS, AND IT FOUND A REAL COLLISION

Word-boundary (`grep -rnw`), corpus `.py/.ts/.tsx/.json/.yaml`, node_modules and `.runtmp_*`
excluded. Counts are the sweep's, taken 2026-08-29:

| token | hits | verdict |
|---|---:|---|
| `source_basis` | 11 | mine + the sibling `supervised_basis` family; no foreign meaning |
| `carve_out` | 1 | CLEAN — mine |
| `CARVE_OUT` | 4 | CLEAN — mine |
| `additive` | **1176** | ⛔ **COLLISION** |
| `ADDITIVE` | **172** | ⛔ **COLLISION** |

⛔ **`additive` IS ALREADY A LOAD-BEARING WORD IN THIS ESTATE AND IT MEANS SOMETHING ELSE.**
Measured concentrations: `data/assets/scripts/silver/etf_schemas.py` and `etf_conversion.py` use
*additive columns* for *columns added to a vendor schema* (`output == vendor + additive + riders`,
with parity assertions built on that denominator); `data/_contracts/vendor_asof_registry.yaml:811`
uses *"skip-if-landed, additive-only"* for **append-only writes**; and
`data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py:440,554` uses *"additive"* for a field added to a
spec — **inside the same package tree as this registry.**

**DISPOSITION — NAMED AND ACCEPTED, NOT SILENTLY RENAMED:**
- The collision is **latent, not active**: the two vocabularies never meet in one table today. This
  axis is a property of an SMA member; the others are properties of a column set or a write mode.
- **The field name is the disambiguator and it must never be shortened.** `source_basis` — never a
  bare `basis`, never a bare `additive` flag. In code the constants carry the namespace too
  (`SMA_BASIS_ADDITIVE`), so the bare string appears only as a declared value of a named field.
- **I did NOT unilaterally rename the CTO's vocabulary.** `carve_out`/`additive` is already
  circulating in four seats' messages and a sovereign-facing explanation; fragmenting it to fix a
  latent collision would cost more than the collision does. **This is a recommendation to
  `1.0.0_SA_CTO~Z`, surfaced rather than acted on.** If it is judged worth renaming, the unambiguous
  pair on this axis is `INSIDE_FIRM_TOTAL` / `OUTSIDE_FIRM_TOTAL`, and the edit is one table plus
  two constants.
- ⚠ **THE CONDITION THAT ARMS IT:** the first artifact that carries BOTH an `additive` column-set
  field and a `source_basis: "additive"` value. Check before emitting `source_basis` into any
  schema that already speaks the column vocabulary.

## 4. THE UNVERIFIED MEMBERS — declared, not defaulted, and the direction is chosen

3 of 6 members have a **measured** basis; 3 do not. Denominator 6 (`3.0.0_SA_CVO~Z` 15942 corrected
this from "2 of 4" — the earlier count omitted `muni` and one ETF member).

| member | basis | evidence |
|---|---|---|
| `divz` | `carve_out` | model_value excluded from `model_aua`, sits in `non_model`; divz+pfoe sum EXACTLY to served SMA L1 22,794,766.25 |
| `pfoe` | `carve_out` | same |
| `tax` | `additive` | **0 of 5** accounts in 0824 (denom 7,282), **5 of 5** in 0833 (denom 7,362), positive-controlled per frame |
| `muni` | `carve_out` | ⚠ **UNVERIFIED** — no accounts exist to test |
| `idvz` | `carve_out` | ⚠ **UNVERIFIED** — no dollars today |
| `pfde` | `carve_out` | ⚠ **UNVERIFIED** — no dollars today |

⛔ **WHY `carve_out` IS THE RIGHT DIRECTION FOR THE UNVERIFIED THREE, AND IT IS NOT A COIN FLIP —
THE TWO ERRORS ARE NOT SYMMETRIC IN VISIBILITY:**
```
  wrongly carve_out  -> understates CLIENT. Client is the number Andrew personally watches
                        and the one that caught this entire bug. VISIBLE.
  wrongly additive   -> inflates the FIRM TOTAL by double-counting money already in
                        non_model. Nothing watches that delta. INVISIBLE.
```
So the unverified default is set to the error that announces itself. ⚠ **This is a declared
safe-direction choice, NOT a measurement, and it is recorded as such here so nobody later cites it
as one.** `3.0.0_SA_CVO~Z` named `muni` the member most likely to be given a basis by omission —
it is not omitted; it is unverified and says so in the table and in the code comment.
✅ **VERIFY EACH BEFORE ITS FIRST DOLLAR.** The verification is cheap and external: which master do
the member's accounts occupy.

## 5. THE ACCEPTANCE ROWS, AND WHICH ONE IS THE PROGRESS ROW

```
  PROGRESS    (a) CLIENT DOES NOT MOVE when an additive member arrives.
              (b) the REFUSED shape (net everything) produces a DIFFERENT Client.
              (c) each member's declared basis matches the master its accounts occupy.
  REGRESSION  the L0 identity sum(peers) == total_aua.
```
⛔ **THE IDENTITY IS A REGRESSION ROW AND MUST NEVER BE SCORED AS PROGRESS.** It is assembled from
these labels and re-satisfies exactly under a wrong assignment in either direction. It proves the
arithmetic, which nobody doubts. **`ALT aum > 0` is BANNED outright** (COO 15877): a one-account ALT
and a five-account ALT both satisfy it and only one is the deliverable.

## 6. WHAT THIS RECORD DOES NOT COVER

- The **value** of `tax` (6,445,461.07 @2026-08-27) and where it is emitted. Leg C, separate.
- Whether `tax` entering `by_model` is the right carrier at all — `by_model` is today a
  wholly-carve-out keyspace, and the first additive entry mixes two bases in one dict. The
  consolidator's cross-check makes that SAFE (it refuses on a mislabel or an uncarried additive),
  but SAFE is not the same as RIGHT, and the carrier choice is not mine.
- The 0833 master-scope question Andrew has not answered (`1.0.0_SA_CTO~Z` 15898 §3b).
