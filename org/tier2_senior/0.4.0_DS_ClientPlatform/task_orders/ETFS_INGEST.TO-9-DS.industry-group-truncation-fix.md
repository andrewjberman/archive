# TO ETFS_INGEST.TO-9-DS — FIX THE `industry_group` TRUNCATION AT SOURCE

<id>ETFS_INGEST.TO-9-DS.industry-group-truncation-fix</id>
**DECOMP CELLS -- NONE CLAIMED:** ⚠ **NO CELL CLAIMED.** Same disclosure as `ETFS_POSITIONING.TO-12-DE`: this is a fix to a defect discovered by running `ETFS_INGEST.TO-6`'s own delivery, on a direct sovereign request. **Not fabricating a cell reference to satisfy Rule 27.**
>> **THE DECOMP-REF ELEMENT IS DELIBERATELY ABSENT, NOT FORGOTTEN.** `proof-of-spec-check.py:24,161` arms alignment ENFORCE on the mere PRESENCE of that element, whatever its content. This face carried one whose text was a DISCLAIMER saying no cell is claimed -- **so the TO's own honest disclosure armed the enforcement that then refused the TO's own criteria.** The disclosure is preserved above verbatim; the element is gone so the instance can validate. ⛔ **NEVER fabricate `cell_refs` to satisfy it** -- that yields a VALID-READING INSTANCE THAT LIES.
<issued_to>DS-class (`integrations/bloomberg/pipeline/etf_daily_pull.py`). ⛔ **NO LIVE DS LANE — seat is `0.0.0_AB_MSTR~Z`'s act.**</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T15:3xZ</issued>
<status>pending -- ⛔ **BLOCKED ON A SOVEREIGN VENDOR-CALL WORD, AND CUT ANYWAY SO THE BLOCK IS VISIBLE.** Cut 15:3xZ after a sweep of Andrew's 15:0xZ verdicts found this was a BUILD REQUEST living only in a message thread, exactly like the one he had to chase.</status>
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
reading `RESOLVED`, or the estate serves a derived value under a measured label.

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
| `INGEST-TO9-AC1` | **The served `industry_group` values are COMPLETE GICS names**, verified against an authoritative source — **not against our own prior output.** Print the full observed set with its denominator. |
| `INGEST-TO9-AC2` | ⛔ **THE VALUE STILL CARRIES ITS CLAIM.** If any value is RESOLVED rather than OBSERVED, `industry_group_basis` says so in a field a consumer can reject on. **A derived value served under a measured label is a FAIL.** |
| `INGEST-TO9-AC3` | ⛔ **EXERCISED ON A SCHEDULED FIRE.** Read the served artifact after a scheduled run; state which run and how you know. **An ad-hoc artifact is never production evidence.** |
| `INGEST-TO9-AC4` | **NO REGRESSION IN COVERAGE.** `industry_group` key presence stays at its current **189 of 189**, and the basis distribution is printed before and after. ⚠ **A fix that improves values while dropping rows is a FAIL.** |
| `INGEST-TO9-AC5` | ⛔ **IF (a) IS BUILT: it FAILS LOUD on a prefix matching two members.** Never picks one. **And it is keyed on a closed list, NEVER on string length** — length does not discriminate truncated from complete. |

## 7. NOT YOURS
⛔ **THE VENDOR CALL ITSELF** without Andrew's explicit per-use word. ⛔ **Minting the GICS list from
memory.** ⛔ **Adopting the observed vocabulary** — that is the follow-on this TO must precede.

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
