# TO ETFS_INGEST.TO-9-DS — FIX THE `industry_group` TRUNCATION AT SOURCE

<id>ETFS_INGEST.TO-9-DS.industry-group-truncation-fix</id>
**DECOMP CELLS -- NONE CLAIMED:** ⚠ **NO CELL CLAIMED.** Same disclosure as `ETFS_POSITIONING.TO-12-DE`: this is a fix to a defect discovered by running `ETFS_INGEST.TO-6`'s own delivery, on a direct sovereign request. **Not fabricating a cell reference to satisfy Rule 27.**
>> **THE DECOMP-REF ELEMENT IS DELIBERATELY ABSENT, NOT FORGOTTEN.** `proof-of-spec-check.py:24,161` arms alignment ENFORCE on the mere PRESENCE of that element, whatever its content. This face carried one whose text was a DISCLAIMER saying no cell is claimed -- **so the TO's own honest disclosure armed the enforcement that then refused the TO's own criteria.** The disclosure is preserved above verbatim; the element is gone so the instance can validate. ⛔ **NEVER fabricate `cell_refs` to satisfy it** -- that yields a VALID-READING INSTANCE THAT LIES.
<issued_to>`0.4.0_DS_ClientPlatform~Q` — **SEATED 2026-08-28 ~19:3xZ by `2.0.0_SA_COO~Z` (issuer, COO spawn/seat authority per Andrew 15:32Z), for THE INSTANCE FILING ONLY.** The build is COMPLETE and Andrew closed it himself; what remains is a RECORDS act over evidence that already exists. ⚠ ~~NO LIVE DS LANE — seat is `0.0.0_AB_MSTR~Z`'s act.~~ **THAT WENT FALSE: three DS lanes are live.**</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T15:3xZ</issued>
<status>BUILD COMPLETE, AWAITING ITS INSTANCE -- ⛔⛔ **THE BLOCK BELOW WAS DISCHARGED BY ANDREW AT ~17:0xZ AND THE FACE KEPT ASSERTING IT FOR OVER TWO HOURS. CORRECTED 2026-08-28 ~19:3xZ by `2.0.0_SA_COO~Z` (issuer), on `0.4.0_DS_ClientPlatform~Q`'s report.** (1) **THE SOVEREIGN VENDOR-CALL WORD WAS GRANTED** — Andrew ruled *"all recs approved"* at ~17:0xZ, which included the per-use Bloomberg grant scoped to one call. (2) **AND THE WORK THEN SHIPPED AND HE CLOSED IT HIMSELF**, 18:24Z VERBATIM: *"the subsector name is not that important, as long as it is properly managed within ETFClassifier, it is done. i dont need to thrash with the fabric about it any further."* The decode is FOLDED INTO `ETFClassifier`, the standalone module DELETED, the 6th basis member minted, 50 assertions PASS (`09408b19e5`/`5af6ef6ff6`/`0694d2ddac`/`b0e1f33471`), ledger entry CLOSED `@c5ef160e7e`, and the producer package carrying it was APPLIED at 18:49:14Z under `ETFS_INGEST.TO-10-AE`. ⛔ **A D4 CLOSE THAT READ THIS FACE AT FACE VALUE WOULD HAVE RECORDED A FALSEHOOD ABOUT WORK ANDREW PERSONALLY CLOSED** — the same class as the *"STAGED, never started"* register line corrected at `f91b759200`. **REMAINING: the proof-of-spec instance, ABSENT (positive-controlled — the same probe finds `TO-6`/`TO-8` present one directory over). A RECORDS ACT, NOT A BUILD.** ⛔ The member, the completions, the radius and the naming are NOT re-opened — Andrew stopped that traffic at 18:24Z. ⚠ ORIGINAL APPENDED, NOT REPLACED. ~~pending -- BLOCKED ON A SOVEREIGN VENDOR-CALL WORD, AND CUT ANYWAY SO THE BLOCK IS VISIBLE. Cut 15:3xZ after a sweep of Andrew's 15:0xZ verdicts found this was a BUILD REQUEST living only in a message thread, exactly like the one he had to chase.~~</status>
<priority>P2 — real, sovereign-requested, and genuinely gated. **Not urgent: the values are wrong-looking, not wrong-valued, and the served field is faithful to its vendor.**</priority>

<authority>
**ANDREW-DIRECT ~15:0xZ, VERDICT 1, VERBATIM** (typos his, preserved):
> *"I do like this, I feel like it should be possible to just predict what the truncated word is
> somehow as the ones truncated seem to mostly be "equipment", seems like we should be able to ix this
> after the fact, or just whatever field we're using for that pull make sure it has more character
> count."*
</authority>

## 1. ⛔ WHY THIS TO EXISTS — IT WAS FOUND BY A SWEEP, NOT BY BEING REMEMBERED

`1.0.0_SA_CTO~Z` (13311 §5) observed that if verdict 2 fell through, **the other verdicts deserved the
same audit** — nobody had swept his 15:0xZ message for **build requests wearing verdict clothes.**
**Swept. This is the one that was uncut.** It had been living as a *"held fork"* in a broker thread,
which is the exact state that made him chase verdict 2.

## 2. THE DEFECT, MEASURED

```
served industry_group values are TRUNCATED AT 30 CHARS -- BLOOMBERG'S CAP, not ours
'Technology Hardware & Equipmen'  'Semiconductors & Semiconductor'  'Commercial & Professional Serv'
'Health Care Equipment & Servic'  'Consumer Discretionary Distrib'  'Pharmaceuticals, Biotechnology'
```
⭐ **THE PIPELINE IS CORRECT.** `1.0.0_SA_CTO~Z`'s free CODE READ (authorised; no vendor call spent)
found **NO truncation in client, server or pull** — the only slices are a date and a log list. **The
passthrough is faithful and this is not a regression.**

## 3. ⛔ HIS OPTION (a) MUST NOT BE BUILT AS STATED — AND THE REASON IS MEASURED

His premise: *"the ones truncated seem to mostly be equipment."* **MEASURED: only 2 of 7 involve
"Equipment"; the other five complete FIVE DIFFERENT WAYS** (`...ices`, `...es`, `...ution & Retail`,
`... & Life Sciences`, `... & Retail`).
>> ⛔⛔ **AND LENGTH CANNOT IDENTIFY WHAT NEEDS REPAIRING:**
```
'Household & Personal Products'   29 chars   COMPLETE -- that IS the full GICS name
'Consumer Staples Distribution'   29 chars   TRUNCATED from "... & Retail"
```
**Two values, identical length, opposite states.** Keyed on `len >= 29` a repair CORRUPTS a correct
value; keyed on `len == 30` it MISSES this one. **THE REPAIR FUNCTION CANNOT DETECT ITS OWN INPUT SET.**
⭐ **The SAFE form of his instinct exists and the distinction is exact: a 30-char PREFIX LOOKUP against
a CLOSED AUTHORITATIVE LIST is deterministic where the prefix is unique; a WORD GUESS is not.**

## 4. THE FORK — ⛔ ONE LIMB NEEDS ANDREW'S EXPLICIT PER-USE WORD

```
A  WIDEN AT THE PULL -- his own second suggestion, and 1.0.0_SA_CTO~Z's RECOMMENDATION.
   Field-width override or an alternate mnemonic on GICS_INDUSTRY_GROUP_NAME.
   Yields MEASURED true values: no inference, no lookup table, no minted constant.
   ⛔⛔ REQUIRES A BLOOMBERG VENDOR CALL = ANDREW'S EXPLICIT PER-USE WORD. NOT YET GIVEN.
   ⚠ His "just whatever field we're using for that pull make sure it has more character count" is
     PLAUSIBLY that word. ⛔ IT IS NOT TREATED AS ONE. Availability is not authorisation and neither
     is a description of the outcome he wants. THREE SEATS INDEPENDENTLY DECLINED TO READ IT AS ONE.
B  PREFIX-RESOLVE against the canonical 25 GICS industry groups. Free, no vendor call.
   ⛔ THE LIST IS NOT IN THE ESTATE -- every in-repo hit is a fixture or our own correspondence.
   ⛔ Typing it from memory is the EXACT "unmeasured exact constant" etf_positioning_gold.py:173-180
     deliberately refused. It needs an AUTHORITATIVE SOURCE, not a recollection.
   ⚠ And only 23 of 25 members have been OBSERVED -- a table built from today's data has a PARTIAL
     DENOMINATOR.
```
⛔ **A REPAIRED VALUE IS *DERIVED*, NOT *OBSERVED*** — it needs its own `industry_group_basis` member
reading ~~`RESOLVED`~~ **`inferred-from-truncation`** (RULED 18:2xZ — see the s4 amendment), or the
estate serves a derived value under a measured label.

## 5. ⛔⛔ SEQUENCING — LOAD-BEARING, AND IT BINDS A DIFFERENT TO

**`etf_positioning_gold.py:173-180` deliberately mints no closed value list and names the designed
follow-on: the manifest prints the OBSERVED member set so a vocabulary can be ADOPTED FROM MEASUREMENT
later.** The 13:00Z fire has now landed that measurement **and the values in it are truncated.**
>> ⛔ **FIX THE TRUNCATION FIRST. ADOPT THE VOCABULARY SECOND.** Reversed, the defect stops being a
   transport artifact and becomes **a ratified constant that reads as measured.**
⚠ **TWO INDEPENDENT REASONS not to adopt today, either sufficient alone: the set is TRUNCATED, and it
is INCOMPLETE (23 of 25).**

## 6. ACCEPTANCE CRITERIA

| id | criterion |
|---|---|
| `INGEST-TO9-AC1` | ⛔ **OVERRIDDEN BY ANDREW-DIRECT 18:02Z (`@7d4f4700a6`) — see §7.** The authoritative-source requirement is LIFTED; completions are INFERRED from the truncated text and hard-coded, on his instruction. **REPLACEMENT BAR:** every completion round-trips — `truncate(proposal, 30).rstrip()` EQUALS the observed string byte for byte — and binds 1:1 to an authoritative 4-digit `GICS_INDUSTRY_GROUP` code from the spent call. ⚠ **THE ROUND-TRIP IS NECESSARY AND NOT SUFFICIENT: more than one completion can round-trip to the same 30 chars, so it proves CONSISTENCY WITH the truncation and NEVER that the completion is the right one.** State that limit in the file beside the table, not only in a message. **`industry_group_basis` = INFERRED/RESOLVED, never `observed`.** ~~verified against an authoritative source — not against our own prior output~~ Print the full observed set with its denominator. |
| `INGEST-TO9-AC2` | ⛔ **THE VALUE STILL CARRIES ITS CLAIM.** If any value is **`inferred-from-truncation`** rather than OBSERVED, `industry_group_basis` says so in a field a consumer can reject on. **A derived value served under a measured label is a FAIL.** |
| `INGEST-TO9-AC3` | ⛔ **EXERCISED ON A SCHEDULED FIRE.** Read the served artifact after a scheduled run; state which run and how you know. **An ad-hoc artifact is never production evidence.** |
| `INGEST-TO9-AC4` | **NO REGRESSION IN COVERAGE.** `industry_group` key presence stays at its current **189 of 189**, and the basis distribution is printed before and after. ⚠ **A fix that improves values while dropping rows is a FAIL.** |
| `INGEST-TO9-AC5` | ⛔ **IF (a) IS BUILT: it FAILS LOUD on a prefix matching two members.** Never picks one. **And it is keyed on a closed list, NEVER on string length** — length does not discriminate truncated from complete. |

## 4a. ⛔ VOCABULARY MEMBER — RULED 2026-08-28 ~18:2xZ, AND `RESOLVED` WAS MY ERROR

**s4 named the member `RESOLVED`. STRUCK.** The ruled spelling is **`inferred-from-truncation`**,
proposed by `0.4.0_DS_ClientPlatform~Q` with the four-postulate record and word-boundary census Rule 24
requires — which my one-word sentence was not.
```
  POSTULATE (iii) INTENT COHERENCE — the axis is PROVENANCE, "how did this value come to be"
    inferred-from-truncation   names an ORIGIN and a MECHANISM      ON AXIS
    resolved                   names a STATE something reached      LIFECYCLE — OFF AXIS
  CENSUS (corpus default, denominator 27,844 files)
    inferred-from-truncation      3 hits   COLLISION-FREE
    resolved                 33,401 hits   CATASTROPHICALLY overloaded — unscopeable by census
```
>> ⭐ **THIS SECTION'S OWN SENTENCE SETTLES IT AGAINST ITSELF:** s4 says *"A REPAIRED VALUE IS DERIVED,
   NOT OBSERVED"* — **which demands a PROVENANCE word and then supplies a lifecycle one.** The banked
   failure is *Rule 24(iii) applies INSIDE a value's wording*, and I committed it in the same section
   that states the correct principle. <<
⭐ **AND THE RULING IS COMPELLED, NOT MERELY BETTER-ARGUED** (`1.0.0_SA_CTO~Z`, read at source):
CLAUDE.md's value-carries-its-claim rule names the canonical set in terms — **`measured / inferred /
held / absent`**. `inferred-from-truncation` **SPECIALIZES `inferred`, one of the law's own four**;
`resolved` maps to **none of them**. So the member was never available regardless of how the census
came out. **A future seat re-opening this will reach for the census first — the census is the WEAKER
of the two grounds and this line exists so the stronger one is found.**

⛔⛔ **BOUNDARY, RECORDED DELIBERATELY WHILE IT IS STILL ONE MEMBER WIDE — the axis WIDENS here.**
Read at `etf_positioning_gold.py:204-216`, all five existing members are **SOURCE-SIDE facts**: one
says a value IS PRESENT (`observed`), four say WHY A VALUE IS ABSENT.
>> **`inferred-from-truncation` IS THE SECOND PRESENT-VALUE MEMBER AND THE FIRST THAT DESCRIBES
   SOMETHING *WE* DID.** The axis moves from *"what the source did"* to *"what the source did OR what
   we did."* **That extension is CORRECT** — the law's `inferred` exists precisely for it — **but it is
   an EXTENSION, and it is recorded as deliberate so it does not become precedent by accident.** <<
⚠ **THE COST OF NOT WRITING THIS DOWN:** the next proposed member is tested against a SIX-member set
whose axis is wider than the five it was written for. *"We did something to this value"* admits far
more members than *"the vendor did not supply it"* — a future `estimated`, `carried-forward` or
`defaulted` would all pass postulate (iii) on the widened axis and **none would have passed on the
original one.** Not an objection to this member; a fence around what it licenses.

⛔ **WIRING THIS IS AN ENUM CHANGE, NOT A PUBLISHER EDIT.** The value is not in the 5-member vocab at
`etf_positioning_gold.py:210` and two LIVE assertions reject it (`test_etf_positioning_industry_group.py:146`
and `:341`). **Mint the sixth member and update the consumers IN THE SAME CHANGE** —
`portal-proxy.ts`, `etfAdapter.ts`, `HoldingsTab.tsx`, the gold test — because a member landing on one
side of that seam is dropped by the adapter, the page looks untouched, and **both halves pass their
own checks.**

## 7. NOT YOURS

⛔⛔ **AMENDED BY ANDREW-DIRECT 2026-08-28 ~18:02Z — READ THIS BEFORE THE LIST BELOW.** VERBATIM
(typo his, preserved): *"I think it can probaably just be inferred from the truncated text and hard
coded"*. Record `@7d4f4700a6`.
>> **~~Minting the GICS list from memory.~~ LIFTED BY NAME.** Inferring the completions from the
   truncated text and hard-coding them is now the INSTRUCTED route. It was a `2.0.0_SA_COO~Z`
   constraint and **a Tier-1-authored constraint does not survive a direct sovereign instruction to
   the contrary.** <<
⚠ **THIS IS A REAFFIRMATION, NOT A FIRST PASS.** §3 records his ~15:0xZ instinct, this seat MEASURED
it and found the naive form unsafe (only 2 of 7 completions involve "Equipment"), and he restated the
route AFTER being shown the 7-of-23 split, the 29-char trap and the family-wide cap. **A concern
raised once and then overruled is a decision.**
⛔ **WHAT HIS WORD DOES *NOT* LIFT — he did not address it, and a silence is not a lift:**
`CLAUDE.md`'s *"A VALUE MUST CARRY ITS CLAIM — in a field a consumer can reject on."* He instructed
WHERE the values come from, not how they are labelled. **`industry_group_basis` reads
**`inferred-from-truncation`**, NEVER `observed`.** That is the difference between *hard-coded and the artifact
says so* and *hard-coded and the artifact lies*, and it costs nothing.

**STILL NOT YOURS:**
⛔ **A SECOND VENDOR CALL** without Andrew's explicit per-use word — the ~17:0xZ grant was SINGULAR
and is SPENT `@4b8dc359ed`. ⛔ **Adopting the observed vocabulary** as the authoritative key — the
decode keys on the vendor's 4-digit `GICS_INDUSTRY_GROUP` code, never on our observed strings.

<proof_of_spec>
  <criterion id="INGEST-TO9-AC1"/>
  <criterion id="INGEST-TO9-AC2"/>
  <criterion id="INGEST-TO9-AC3"/>
  <criterion id="INGEST-TO9-AC4"/>
  <criterion id="INGEST-TO9-AC5"/>
  <expected_criteria>INGEST-TO9-AC1,INGEST-TO9-AC2,INGEST-TO9-AC3,INGEST-TO9-AC4,INGEST-TO9-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_INGEST.TO-9-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 5, all FIRM-TOKENED (`INGEST-TO9-ACn`) per the estate rule that `ETFS_INGEST.TO-8` was measured to violate. No cell claimed; see decomp_ref.</alignment_denominators>
</proof_of_spec>
