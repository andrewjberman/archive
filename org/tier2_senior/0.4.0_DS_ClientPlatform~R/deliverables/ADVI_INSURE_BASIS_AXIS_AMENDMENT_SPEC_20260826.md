# `{attr}_basis` AXIS AMENDMENT -- ADD `STRUCTURALLY-INAPPLICABLE`

**seat:** `0.4.0_DS_ClientPlatform~R` · **scope authority:** `2.0.0_SA_COO` 72212
**status:** PROPOSAL. **NOT IMPLEMENTED.** No producer edited -- gold-tier changes go through the lane
with the commit gate, per the issuer's instruction.
**amends:** the `{attr}_basis` axis declared by `0.4.0_DS_ClientPlatform~J` in
`ADVI_INSURE_GOLD_BUILDER_DESIGN_v1.md` s.2 (which carries its own four-postulate record).

---

## 1. THE ONE-LINE CHANGE

`account_id_basis` must stop saying `NOT-DERIVABLE-UPSTREAM` and start saying
**`STRUCTURALLY-INAPPLICABLE`**. `advisor_basis` **keeps** `NOT-DERIVABLE-UPSTREAM` and must not move.

> ⚠ **"AND MUST NOT MOVE" DID NOT SURVIVE 2026-08-27 — SEE AMENDMENT 2 AT THE FOOT OF THIS FILE.**
> `advisor_basis` moved twice that day (→ `NOT-CAPTURED-PENDING-SURFACE` → back to
> `NOT-DERIVABLE-UPSTREAM`) because its WARRANT was falsified and then re-established on a capture.
> It ends on the same string this line names, so a reader who stops here reaches the right value **by
> a reasoning that has since been proven wrong.** Prior text preserved, not overwritten; the pointer
> is here because a correction is only as complete as its last surviving carrier, and this line is
> the one a top-down reader hits first.

**Today both columns are set from the SAME constant, and they sit on OPPOSITE sides of the exact
distinction the issuer drew.** That is the defect: not a wrong string, but two different states sharing
one value with no way for a consumer to branch.

---

## 2. WHY THE EXISTING VALUE IS WRONG HERE -- FROM THE AXIS'S OWN (iv) CLAUSE

`~J`'s s.2 does not merely name `NOT-DERIVABLE-UPSTREAM`; it states the remedy that moves it:

> *"neither one ever clears `NOT-DERIVABLE-UPSTREAM`, because its remedy is a change in Black Diamond's
> own template configuration (dim 436 / template 390224)."*

**That is TRUE of `advisor` and FALSE of `account_id`.**

- **`advisor`** -- a BD template change (dim 436) would populate it. `1.0.0_SA_CTO`'s finding
  `a6c76382b1` names that remedy vendor-side, and `0.4.0_DS_ClientPlatform~S`'s D3 work has it RESERVED
  to Andrew as a vendor ask. **A remedy exists. The value is correct.**
- **`account_id`** -- measured this session: `dim.account_id == xref.schwab_account_id`, **5,337 of
  5,337, shuffle negative control 0 of 5,337.** The identifier IS a Schwab account number. **No BD
  template change produces a Schwab account number for a Brighthouse annuity**, because the asset is not
  held at Schwab. The 96 insurance accounts present in `dim_account_xref` carry `match_method=unresolved`
  96/96 with `schwab_account_id` NULL 96/96 **on accounts the xref knows are open** (`account_is_open`
  True 96/96) -- the xref looked and correctly found nothing.

**So `account_id` is an UNCOVERED MEMBER of the declared domain** (24(i) coverage), currently hidden by
assignment to the nearest-looking value. It is not "a gap upstream that may close." It can never close.

> ⛔ **THE HARM IS SPECIFIC AND IT REPEATS A WARNING THE AXIS ALREADY CARRIES.** `~J`'s (iv) clause warns
> that *"a reader who sees the egress grant land will reasonably expect `advisor_id` to fill, and it will
> not."* **The same shape now sits one level down:** a seat who lands the dim-436 vendor ask will
> reasonably expect BOTH stamped columns to fill. **Only `advisor` will.** The other will start an
> investigation that has no terminating state, because its stamp promises a remedy that does not exist.

---

## 3. RULE 24 FOUR-POSTULATE RECORD -- over the AMENDED five-value domain

**DECLARED DOMAIN (unchanged):** *for each v1 attribute the gold row carries, why it is or is not
populated.* **GRAIN: ATTRIBUTE-level** (a property of the COLUMN), never row-level.

| value | meaning | remedy that moves it |
|---|---|---|
| `MEASURED` | populated from a field observed in captured vendor bytes | none -- terminal |
| `AWAITING-FIRST-RUN` | supplying call AND response shape known; no run has happened | a scheduled run |
| `UNOBSERVED-CONTAINER` | a call names the field, its populated shape never observed | one populated specimen |
| `NOT-DERIVABLE-UPSTREAM` | **no upstream field SUPPLIES it — whether because none carries it, or because the one that does is unpopulated for this firm — and a vendor-side config change could** | vendor-side CONFIG change |
| **`STRUCTURALLY-INAPPLICABLE`** *(NEW)* | **the attribute is defined only for a population this table's asset class is not in; NO upstream change of any kind can populate it** | **NONE -- terminal** |

**(i) MECE over the declared domain.**
*Exclusivity:* the amended set is separated by **three** independent tests, one more than before --
*does an upstream field exist?* · *has its shape been observed?* · **and now: could ANY upstream change
make this attribute applicable to this asset class?** The two negative values are disjoint on that third
test alone: **YES, a change could populate it -> `NOT-DERIVABLE-UPSTREAM`; NO, none could ->
`STRUCTURALLY-INAPPLICABLE`.** Every other pair remains disjoint exactly as `~J` established.
*Coverage:* "attribute not populated" now decomposes into: no run yet · shape unseen · field
absent-but-addable · **field cannot exist for this class**. **Hunted for an uncovered member:** the
candidate is *"a field exists and applies, a run happened, and it is still null"* -- that is a ROW-level
value condition, **OUT of domain by the grain clause**, unchanged from `~J`'s hunt.

**(ii) SAME GRAIN.** `STRUCTURALLY-INAPPLICABLE` is attribute-level like every other value: it describes
the COLUMN for this table.
⚠ **LIMIT, NAMED RATHER THAN LEFT TO BE DISCOVERED:** it is attribute-level *only because every row in
this table is one asset class*. **In a table mixing insurance and AM rows, applicability would vary
row-to-row and this value would break the grain postulate.** If such a table is ever built, the value
does not travel to it unchanged -- it becomes a row-level condition and needs a different home. This
table is insurance-only by construction (`insurance_nav_current`), so the postulate holds here.

**(iii) INTENT COHERENCE.** One intent, unchanged: **derivability.** The new value answers "can this be
derived, ever?" -- the same question as the other four. It encodes no handling policy (`spine_class`
owns never-drop) and no data quality (a null EMV is not a basis).

**(iv) STATE COHERENCE -- and this postulate is the entire reason for the amendment.**
State axis: *what remedy moves this value?* Run the test -- **does ONE remedy move every value
together?** **No, and that is now visible rather than hidden.**
⛔ **NAMING WHICH VALUES DO NOT MOVE, as the postulate requires:** the obvious instrument for this axis
is **the vendor ask** (dim 436 / template 390224). It moves `NOT-DERIVABLE-UPSTREAM`. It moves
`UNOBSERVED-CONTAINER` and `AWAITING-FIRST-RUN` not at all -- those take a specimen and a run.
**And it CANNOT move `STRUCTURALLY-INAPPLICABLE`, ever.**
**Under the CURRENT four-value axis those last two states are the same value**, so the axis reports that
one remedy covers both when it covers only one. **The amendment is what makes 24(iv) satisfiable at all.**

---

## 4. TOKEN-HYGIENE CENSUS (word-boundary, case-insensitive)

Estate-wide, denominator printed by the instrument:

```
STRUCTURALLY-INAPPLICABLE    0 hits / 26,746 files   <- CLEAN MINT, no collision
NOT-DERIVABLE-UPSTREAM      32 hits / 26,746 files   <- existing, PRESERVED for advisor
NOT-APPLICABLE             103 hits / 26,746 files   <- REJECTED, heavily occupied
INAPPLICABLE               149 hits / 26,746 files   <- REJECTED, superset of both above
account_id_basis             2 hits (1 producer line + 1 doc of mine)  <- NO downstream consumer
BASIS_NOT_DERIVABLE          3 hits, ALL in the producer (:112 def, :168, :172)
```
**REJECTED ALTERNATIVES AND WHY:** `NOT-APPLICABLE` at 103 occurrences is native estate vocabulary
carrying unrelated meanings -- adopting it makes every future census of this axis ambiguous.
`INAPPLICABLE` is worse (149), and as a substring it would also match the proposed token, so a census
of one could not discriminate the other. **`STRUCTURALLY-INAPPLICABLE` is the only candidate with zero
prior occupancy**, and its length is the price of that.

---

## 5. THE EXACT EDIT -- SPECIFIED, NOT APPLIED

**File:** `data/assets/scripts/gold/bd49f_insurance_nav_current.py`

| line | now | becomes |
|---|---|---|
| `:112` | `BASIS_NOT_DERIVABLE = "NOT-DERIVABLE-UPSTREAM"` | **keep**, and ADD beside it: `BASIS_STRUCTURALLY_INAPPLICABLE = "STRUCTURALLY-INAPPLICABLE"` |
| `:168` | `"account_id_basis": BASIS_NOT_DERIVABLE,` | `"account_id_basis": BASIS_STRUCTURALLY_INAPPLICABLE,` |
| `:172` | `"advisor_basis": BASIS_NOT_DERIVABLE,` | **UNCHANGED** -- this one is correct |

**Comment at `:110-112`** currently cites the axis's four-postulate record; it should cite this amendment
too. **Docstring `:41-46`** already states the account_id reasoning correctly -- *"Insurance is held at
carriers, not in the AM book, so a cohort that did NOT overlap is exactly what 'beside, never inside'
predicts"* -- so the prose is ALREADY right and only the STAMP disagrees with it. **The producer's own
docstring is the corroborating witness for this change.**

**Doc:** `ADVI_INSURE_GOLD_BUILDER_DESIGN_v1.md` s.2 gains the fifth row and the amended (i)/(iv) text.

**No other file changes.** `account_id` stays `None` -- **the VALUE is right and only its BASIS is
wrong**, which is why this is a stamp fix and not a data fix.

---

## 6. TWO QUESTIONS FOR THE ISSUER, NOT DECIDED HERE

1. **Does this bump `schema_version`?** It currently reads `"1"` (`:106`). Adding a value to an existing
   column's domain is consumer-visible. **There are ZERO downstream consumers today** (census above: the
   only non-producer hit is my own report, and the platinum leaf is unemitted), so the cheapest moment to
   decide is now. My read: **no bump** -- the column's TYPE and MEANING are unchanged and no consumer can
   have branched on a value that has never been served. **That is a recommendation, not a ruling.**
2. **Does the value belong in a shared registry rather than a per-producer constant?** The axis is
   declared as reusable across attributes and Cottonwood is expected to reuse the pattern. A second
   producer re-coining the string is the duplicate-vocabulary defect one layer up. **I did not act on
   this** -- it is a cross-producer schema question and it is not mine.

⛔ **AND THE TIMING ARGUMENT, STATED PLAINLY:** this is free right now and expensive after AC4 emits. Once
the platinum leaf carries the stamp, changing it is a served-key content change with consumers attached.

-- `0.4.0_DS_ClientPlatform~R`, 2026-08-26

---

# AMENDMENT 2 — 2026-08-27: `NOT-DERIVABLE-UPSTREAM`'s DEFINITION, corrected against measurement

**Authorized:** `2.0.0_SA_COO` 76430, wording adopted verbatim · **Author-of-record:** `0.4.0_DS_ClientPlatform~R`
**cc:** `3.0.0_SA_CVO` (the axis contract changes, so the change belongs on the channel record)
**Grounding measurement:** the `relationshipdetail` capture, `@113354aa60`, re-read at this seat from the
landed bytes — `financialTeam` **KEY PRESENT, type list, len 0**; `financialTeamTemplateId` None; 49F
relationship `z08117302`, one of the 77 this seat's own `INS-a-2` census walked.

## What changed, and why the VALUE did not

| | |
|---|---|
| **was** | "no upstream field carries it under any name, but a vendor-side config change could add one" |
| **now** | "no upstream field **SUPPLIES** it — whether because none carries it, or because the one that does is **unpopulated for this firm** — and a vendor-side config change could" |

**The old definition was measured FALSE of a state the value correctly holds.** `financialTeam` *does*
exist upstream and *does* carry the advisor hop; it is **empty for 49F**. Under the old wording that
state had no home, while its remedy — a vendor-side config act — is exactly what the value names.

> **THE AXIS IS REMEDY-KEYED, AND THAT IS WHY THE VALUE SURVIVED ITS OWN DEFINITION.** The stamp answers
> *what remedy moves this?*, not *what does the payload look like?*. A definition written in payload terms
> was always going to go stale against a measurement; the remedy did not move, so the value did not.

## (i) EXCLUSIVITY RE-CHECKED — the widening puts this value next to `UNOBSERVED-CONTAINER`

⛔ **The amendment creates a boundary that did not previously exist, and it must be stated or a future
seat will collapse it.** Both values now describe *a field that exists and is not populated*:

| value | the state | remedy |
|---|---|---|
| `UNOBSERVED-CONTAINER` | the field exists; **we have never observed a populated specimen.** Silence about whether it *can* be populated. | **one populated specimen** |
| `NOT-DERIVABLE-UPSTREAM` | the field exists; **we have MEASURED it empty for this firm** — the vendor affirmatively returned zero. | **vendor-side CONFIG change** |

**THE DISCRIMINATOR IS WHETHER A MEASUREMENT WAS TAKEN, NOT WHAT THE PAYLOAD LOOKS LIKE** — and the two
payloads can be byte-identical. *Absence of observation* and *observation of absence* are different
epistemic states with different remedies, and the whole advisor finding turned on that difference:
`financialTeam: []` is the vendor **saying zero**, not us **failing to look**.

**Worked example, this attribute, in one day:** `advisor_basis` sat at `NOT-CAPTURED-PENDING-SURFACE`
(the surface was never called — an *unobserved* state), and moved to `NOT-DERIVABLE-UPSTREAM` **only
once the call was made and returned empty.** Had we stamped it `NOT-DERIVABLE` before calling, the value
would have been right by luck on a false warrant — which is precisely what the original 70462 stamp was.

*Every other pair remains disjoint as established in Amendment 1; the third test (could ANY upstream
change make this applicable? **YES** → `NOT-DERIVABLE-UPSTREAM`, **NO** → `STRUCTURALLY-INAPPLICABLE`)
is untouched by this wording change.*

## What this amendment does NOT do

- **No new value.** Six values stand; no token census was required and none was run.
- **No producer change.** `data/assets/scripts/gold/bd49f_insurance_nav_current.py` already assigns
  `BASIS_NOT_DERIVABLE` (@f4836ad706). **This clears the definition debt declared in that commit's
  constant block** — the source comment says the debt was routed rather than self-served, and this is
  the routing landing.
- **No re-emit.** That is a separate act, held behind its own gate.

-- `0.4.0_DS_ClientPlatform~R`, 2026-08-27
