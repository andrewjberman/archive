# TO ETFS_INGEST.TO-9-DS — FIX THE `industry_group` TRUNCATION AT SOURCE

<id>ETFS_INGEST.TO-9-DS.industry-group-truncation-fix</id>
**DECOMP CELLS -- NONE CLAIMED:** ⚠ **NO CELL CLAIMED.** Same disclosure as `ETFS_POSITIONING.TO-12-DE`: this is a fix to a defect discovered by running `ETFS_INGEST.TO-6`'s own delivery, on a direct sovereign request. **Not fabricating a cell reference to satisfy Rule 27.**
>> **THE DECOMP-REF ELEMENT IS DELIBERATELY ABSENT, NOT FORGOTTEN.** `proof-of-spec-check.py:24,161` arms alignment ENFORCE on the mere PRESENCE of that element, whatever its content. This face carried one whose text was a DISCLAIMER saying no cell is claimed -- **so the TO's own honest disclosure armed the enforcement that then refused the TO's own criteria.** The disclosure is preserved above verbatim; the element is gone so the instance can validate. ⛔ **NEVER fabricate `cell_refs` to satisfy it** -- that yields a VALID-READING INSTANCE THAT LIES.
<issued_to>`0.4.0_DS_ClientPlatform~M`</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T15:3xZ</issued>
<status>** THE MECHANISM IS RESOLVED AND THE "WEEKEND LAW" BELOW IS FALSIFIED -- amended 2026-08-29 ~11:3xZ by 2.0.0_SA_COO~Z, BEFORE the fire. Read this before the paragraph beneath it, which was written 20 minutes earlier and is superseded on its REASON while surviving on its EXPECTATION. ** FALSIFIED ON DISK, ONE SCOPE, FULL LISTING (0.4.0_DS_ClientPlatform~Z): a SINGLE Saturday run at 2026-08-29T03:55:57Z wrote account-distribution/2026-08-28.json AND category-views/2026-08-27.json AND aggregate-aua-timeseries/2026-08-27.json -- ONE run, ONE timestamp, ONE type ADVANCED and TWO DID NOT. A calendar-derived write date cannot produce two different dated keys in one run, and here it produced two. ** SO IT WAS NEVER A LAW OF THE CALENDAR: the as_of is PER-TYPE and CONTENT-DERIVED (derive_as_of() consolidator:1106, TYPE_AS_OF_FIELD :247), gated by EACH TYPE S OWN UPSTREAM FRONTIER. category-views held at 08-27 because ITS upstream (aggregate-aua-timeseries) held at 08-27 -- not because it was a Saturday. ** THE REAL GATE FOR THIS FACE, STATED PRECISELY: category-views advances when aggregate-aua-timeseries advances. That is the thing to look at, and "is it a weekday" is not. ** WHAT SURVIVES: MONDAY 2026-08-31 IS STILL THE LIKELY LIFT, because the upstream cadence usually moves then -- but that is now a PREDICTION ABOUT A FEED CHAIN, not an inference from the day of the week, and it can be checked directly instead of waited out. ** AND A 13:30Z ADVANCE IS A LIVE POSSIBILITY, not the surprise the paragraph below implies: one type already advanced today. ** BOTH OUTCOMES REMAIN LEGITIMATE AT ~13:3xZ. AFTER == BEFORE is correct if the upstream has not moved; a NEW DATED KEY is correct if it has. NEITHER IS A DEFECT, and nobody fires an ad-hoc run to find out -- that consumes the discriminator. ** THREE SEATS WITHDREW A CLAIM TO GET HERE: 0.4.0_DS_ClientPlatform~Z retracted "the feed has nothing to do with it" (weekend and stale-feed are CONFOUNDED -- vendors do not publish Saturdays); 0.7.0_AE_CloudOps~Z withdrew a conclusion about the WRITE key proved from expected_t1(), which is the PREFLIGHT S EXPECTATION in a different program -- a GRAIN error; and this seat over-stated "CANNOT discharge today" twice, first as a calendar law and then as a contested one. 1.0.0_SA_CTO~Z s feed-frontier mechanism was RIGHT for the write plane. ** ** TRADING-CALENDAR CORRECTION, 2026-08-29 ~11:2xZ by 2.0.0_SA_COO~Z (issuer). TODAY IS SATURDAY 2026-08-29 AND TODAY S SCHEDULED FIRE WRITES NO NEW ARTIFACT. Surfaced by 3.0.0_SA_CVO~Z, corroborated by 0.4.0_DS_ClientPlatform~Z from an EARLIER vintage (@df2232c357, 08-28 17:15Z, before today s runs existed), confirmed here. MECHANISM AT SOURCE: the gold key is {as_of}.json and as_of comes from the artifact s OWN CONTENT, never the run date -- derive_as_of() mdpf_gold_consolidator.py:1106, TYPE_AS_OF_FIELD :247. So a weekend run EXECUTES, writes a manifest, and writes NO ARTIFACT. MEASURED: 4 of 4 weekend runs NO-ADVANCE, 2 of 2 Monday runs ADVANCE to the preceding Friday, across 18 scheduled 13:31Z runs of 42 manifests; 63 gold objects at 49financial and ZERO carry a Saturday or Sunday write; the only served category-views vintage is 2026-08-27.json, denominator 1. ** CONSEQUENCE FOR THIS FACE: any criterion requiring a NEW or CHANGED SERVED ARTIFACT CANNOT DISCHARGE TODAY -- its lift is MONDAY 2026-08-31, which carries as_of 2026-08-28. A criterion that measures the TRIGGER or the EXECUTION of the fire is NOT affected: a Saturday run does execute. ** AFTER == BEFORE AT ~13:3xZ TODAY IS THE EXPECTED AND CORRECT OUTCOME, NOT A REGRESSION -- CLAUDE.md s trading-calendar NEVER-rule exists for exactly this false alarm. ** AND THIS CORRECTS MY OWN LINE: the head below asserted today s fire as the LIFTING EVENT. It is true that the fire is ENABLED and true that this face is clock-gated; it is FALSE that today s clock lifts an artifact-dependent criterion. I attested the fires as lifting events without resolving the trading calendar, which is the NEVER-rule I walked past. ** ACTIVE -- WAITING ON ONE EVENT: the SATURDAY 2026-08-29 13:00Z scheduled fire (`etf-positioning-producer-daily`, `cron(0 13 * * ? *)`, ENABLED, EventBridge RULES plane). BUILD DONE. INSTANCE PRESENT (33,893 B; 3 PASS + 2 UNCOMPUTABLE, ZERO FAIL). REMAINING: score `AC3`+`AC4` against the POST-FIRE served artifact -- A LANE IS NEEDED THEN, NOT BEFORE. If Saturday does not move the trading-day frontier, true completion is MONDAY 2026-08-31; AFTER == BEFORE on a Saturday is the EXPECTED weekend outcome, never a defect. HISTORY BELOW, and the head of this field read "BUILD COMPLETE, AWAITING ITS INSTANCE" until 2026-08-29 ~07:5xZ -- STALE, because `to-check` renders only the HEAD and the correction was in the TAIL. -- ⛔⛔ **THE BLOCK BELOW WAS DISCHARGED BY ANDREW AT ~17:0xZ AND THE FACE KEPT ASSERTING IT FOR OVER TWO HOURS. CORRECTED 2026-08-28 ~19:3xZ by `2.0.0_SA_COO~Z` (issuer), on `0.4.0_DS_ClientPlatform~Q`'s report.** (1) **THE SOVEREIGN VENDOR-CALL WORD WAS GRANTED** — Andrew ruled *"all recs approved"* at ~17:0xZ, which included the per-use Bloomberg grant scoped to one call. (2) **AND THE WORK THEN SHIPPED AND HE CLOSED IT HIMSELF**, 18:24Z VERBATIM: *"the subsector name is not that important, as long as it is properly managed within ETFClassifier, it is done. i dont need to thrash with the fabric about it any further."* The decode is FOLDED INTO `ETFClassifier`, the standalone module DELETED, the 6th basis member minted, 50 assertions PASS (`09408b19e5`/`5af6ef6ff6`/`0694d2ddac`/`b0e1f33471`), ledger entry CLOSED `@c5ef160e7e`, and the producer package carrying it was APPLIED at 18:49:14Z under `ETFS_INGEST.TO-10-AE`. ⛔ **A D4 CLOSE THAT READ THIS FACE AT FACE VALUE WOULD HAVE RECORDED A FALSEHOOD ABOUT WORK ANDREW PERSONALLY CLOSED** — the same class as the *"STAGED, never started"* register line corrected at `f91b759200`. **REMAINING: the proof-of-spec instance, ABSENT (positive-controlled — the same probe finds `TO-6`/`TO-8` present one directory over). A RECORDS ACT, NOT A BUILD.** ⛔⛔ **THAT `ABSENT` IS NOW STALE AND THE RECORDS ACT IS DONE — amended 2026-08-29 ~02:5xZ by `2.0.0_SA_COO~Z` (issuer), on a scoped D1+D4 drive census.** The instance is **PRESENT at 33,893 B**, positive-controlled by the identical probe against `TO-6` (36,487 B) and `TO-8` (36,427 B). It scores **5 rows: 3 PASS + 2 UNCOMPUTABLE, ZERO FAIL.** ⛔ **THIS FACE IS THEREFORE NOT WAITING ON A RECORDS ACT AND NOT WAITING ON A BUILD — IT IS WAITING ON ONE EVENT, and `AC3`+`AC4` are the SAME gate, not two:** `etf-positioning-producer-daily`, `cron(0 13 * * ? *)`, **ENABLED**, read live off the **EventBridge RULES plane** (⚠ it is NOT on the Scheduler plane — a Scheduler-only census returns this rule as UNSCHEDULED). The decode was applied **18:49:14Z** and the last scheduled fire wrote at **13:01:26Z** — **the clocks do not overlap by 5h48m, so no scheduled run has yet executed the deployed decode**, exactly as `AC3` requires and as the instance itself measured rather than assumed. ⭐ **CORROBORATION, NOT REPETITION: the instance read the ARTIFACT, this amendment read the SCHEDULE — two planes, ~86s apart, one answer.** **CLOSE THIS FACE BY SCORING `AC3`/`AC4` AGAINST THE POST-FIRE SERVED ARTIFACT; a lane is needed THEN, not before — seating one now would be seating it on a read that does not exist yet.** ⛔⛔ **NAME THE FIRE BY DATE, NOT AS "TODAY" — the next one is SATURDAY 2026-08-29 13:00Z** (`2026-08-28T13:01:26Z` was FRIDAY's and is already past; this face's own evidence proves it could not have exercised the deployed decode). **A first draft of this amendment said "today's fire" and pointed at the wrong side of a date boundary; caught by `3.0.0_SA_CVO~Z` before it committed.** ⛔ **AND THE TWO CRITERIA HAVE DIFFERENT EXPOSURE TO THAT SAME FIRE, so do NOT treat them as discharging together:** `AC3` ("EXERCISED ON A SCHEDULED FIRE") **likely discharges Saturday** — a Saturday run does execute deployed code on a scheduled trigger. `AC4` needs a **DISTINGUISHABLE** after-image, and **a correct Saturday run may write NOTHING because the trading-day frontier has not moved** — the MDPF floor did exactly that on 2026-08-28: right code, right trigger, zero writes. >> ⛔ **A SEAT THAT STANDS UP AT ~13:0xZ SATURDAY AND FINDS AFTER == BEFORE MUST NOT FILE A DEFECT. THAT IS THE EXPECTED WEEKEND OUTCOME, NOT A REGRESSION** — CLAUDE.md's trading-calendar NEVER-rule and the `freshness_basis: trading-day-frontier` clause exist for precisely this false alarm. << **IF SATURDAY DOES NOT MOVE IT, THIS FACE'S TRUE COMPLETION IS MONDAY 2026-08-31.** Stated now so it is a PREDICTION rather than a surprise. ⚠ **BOUND, STATED HONESTLY: the etf-positioning producer's write semantics have NOT been read. The claim here is not that `AC4` fails on Saturday — it is that nobody has established that it passes.** ⛔ The member, the completions, the radius and the naming are NOT re-opened — Andrew stopped that traffic at 18:24Z. ⚠ ORIGINAL APPENDED, NOT REPLACED. ~~pending -- BLOCKED ON A SOVEREIGN VENDOR-CALL WORD, AND CUT ANYWAY SO THE BLOCK IS VISIBLE. Cut 15:3xZ after a sweep of Andrew's 15:0xZ verdicts found this was a BUILD REQUEST living only in a message thread, exactly like the one he had to chase.~~</status>
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


## SEATING -- RE-ADDRESSED 2026-08-29 ~13:0xZ TO `0.4.0_DS_ClientPlatform~M`

⛔ **THE PRIOR LANE WAS DEAD AND THE FACE SAID SO; THE EVENT IT WAITED ON HAS NOW HAPPENED, SO THE
SEAT IS CORRECT NOW AND WOULD HAVE BEEN PREMATURE BEFORE.** The face's own plan was *"at ~13:0xZ,
seat a FRESH lane of this class and re-address this face"*. This is that act, by `2.0.0_SA_COO~Z`
(issuer; COO spawn/seat authority per Andrew 2026-08-28 15:32Z).

```
  1pt process truth   9 claude.exe live -- 0.4.0_DS_ClientPlatform~M proc=0
                      POSITIVE CONTROL 0.4.0_DS_ClientPlatform~Y (seated 12:5xZ) proc=1 -> not blind
  1b  marker scan     0 hit(s)   (same control: ~Y = 1 hit)
  1c  concurrency     8 of 16 spawn-marker windows
  1d  encumbrance     0 open TOs . 0 project/mission owner rows . channel hits are `surfaced_by`
                      ONLY -- AUTHORSHIP, NOT OWNERSHIP, and only ownership is an obligation
  1d-ii artifact      the proof-of-spec INSTANCE is PRESENT and its event-gated criteria were
                      UNSCORABLE until this fire. NOT a stale face over finished work.
```

⚠ **`<issued_to>` NOW CARRIES THE SERIAL AND NOTHING ELSE.** `to-check` renders the FIRST
serial-shaped token in that field, so prose containing serials makes a face render against the wrong
seat. The prior field's text is preserved in git history; the seating narrative lives here.


## POST-FIRE EVIDENCE, MEASURED BY THE ISSUER 2026-08-29 ~13:0xZ -- LOCATED, NOT ADJUDICATED

The **Saturday 2026-08-29 13:00Z** `etf-positioning-producer-daily` fire RAN AND ADVANCED THE
FRONTIER. This face's event gate is DISCHARGED: there is now a post-fire served artifact to score.

```
  gold/holding/date=2026-08-28/holding.parquet   45,630 B   LastModified 2026-08-29T13:01:22Z
  gold/_manifests/2026-08-28/0f277195f2d7.json    3,068 B   same stamp -- THE RUN COMPLETED
  189 rows . 169 distinct ticker . 183 rows at 8-of-8 return windows . 6 rows at 0-of-8
```

⛔ **AND THE WEEKEND PREDICTION IN THIS FACE'S OWN HISTORY WAS WRONG FOR THIS PIPELINE — READ THIS
BEFORE SCORING.** An earlier amendment warned that *"a correct Saturday run may write NOTHING because
the trading-day frontier has not moved"* and that **`AFTER == BEFORE` is the expected weekend
outcome**. That is the **MDPF** mechanism — a CONTENT-derived `as_of` (`derive_as_of()`,
`mdpf_gold_consolidator.py:1106`). **ETF positioning is CALENDAR-anchored**:
`etf_positioning_gold.py:497` and `:1672` use `tcal.expected_last_trading_day(now)`, which for
Saturday 2026-08-29 is **2026-08-28** — and `bbg/2026-08-28/` existed as input. **So it advanced, as
predicted before the fire.** `3.0.0_SA_CVO~Z` fenced their MDPF frontier result at exactly this
pipeline boundary (msg 16732) before anyone carried it across. **AFTER == BEFORE WOULD HAVE BEEN THE
DEFECT HERE, NOT THE EXPECTED OUTCOME.**

⚠ **THE MEASUREMENTS BELOW ARE EVIDENCE LOCATED FOR THE SEAT, NOT A VERDICT ON ANY CRITERION. THE
ISSUER HAS NOT READ THIS FACE'S AC TEXT IN FULL AND IS NOT SCORING IT.** In particular Andrew
narrowed the delivered scope at 2026-08-28 18:24Z, VERBATIM: *"the subsector name is not that
important, as long as it is properly managed within ETFClassifier, it is done."* **Whether a served
30-char string is in or out of the accepted scope is the executor's reading, not the issuer's.**

```
  industry_group in the POST-FIRE artifact: 23 distinct values over 180 non-null of 189 rows
  SIX sit at EXACTLY 30 chars (Bloomberg's cap), max len over all values = 30:
    'Commercial & Professional Serv'   'Consumer Discretionary Distrib'
    'Health Care Equipment & Servic'   'Pharmaceuticals, Biotechnology'
    'Semiconductors & Semiconductor'   'Technology Hardware & Equipmen'
```

⭐ **AND AN UNRELATED FINDING IN THE SAME ARTIFACT, ROUTED ELSEWHERE — DO NOT CHASE IT FROM THIS
FACE.** `ABT` (Abbott, DIVZ) carries **0 of 8** return windows in BOTH the 08-27 and the 08-28
partition, so the defect is **REPRODUCED ACROSS TWO CONSECUTIVE SCHEDULED FIRES** rather than a
one-day glitch. Its weight moved **2.36 -> 2.33** between them, which is the discriminator: **the
book row refreshes daily and only the RETURN SERIES has no source.** That is
`ETFS_POSITIONING.TO-13-DS`, seated on `0.4.0_DS_ClientPlatform~Y`, and it is NOT this face's work.


## ⛔ THE PLANE IS SETTLED AND THE BLOCK ABOVE NAMED THE WRONG ONE -- issuer correction, 2026-08-29 ~13:2xZ

**The post-fire block above measured `industry_group` in `gold/holding/date=2026-08-28/holding.parquet`
and reported SIX values at exactly 30 chars. THAT MEASUREMENT IS CORRECT AND IT IS ABOUT THE WRONG
OBJECT.**

```
  the decode runs   etf_positioning_publisher.py  _industry_group
                    PUBLISHER-SIDE, at PLATINUM-WRITE TIME, applied pin b066be7a92
  => GOLD SITS UPSTREAM OF THE DECODE and legitimately still carries Bloomberg's capped
     strings. Gold looking unchanged is CORRECT, not a failure.
```
>> **`0.7.0_AE_CloudOps~M`, who established this at source while scoring `TO-10-AE`: "Scoring AC3 on
the plane handed over would have FAILED a criterion that passes -- a real measurement, correctly
taken, of the wrong object."** ⭐ **`0.4.0_DS_ClientPlatform~M` raised exactly this hazard BEFORE
measuring, rather than reporting a clean no-change against the wrong plane.** <<

**THE SERVED PLANE, re-measured independently by `2.0.0_SA_COO~Z`** -- `platinum/etfs/positioning_data.json`,
ContentLength **148,372 B**, VersionId `bpgnYq4ir2yrM5cnWgJ35DzmnqalquU5`, LastModified 13:01:25Z:
```
  180 rows carry industry_group . 23 distinct . MAX LENGTH 46  (was 30)
  values at EXACTLY 30 chars: 0        <- was 6 pre-fire
  longest: 'Pharmaceuticals, Biotechnology & Life Sciences'   len 46
  basis: observed 121 . inferred-from-truncation 59 . not-applicable-non-equity 8 .
         absent-from-source 1   = 189
```

⛔ **AND THE SIX-VERSUS-SEVEN GAP WAS AN INSTRUMENT ARTEFACT, THE ISSUER'S.** `0.4.0_DS_ClientPlatform~Q`
predicted SEVEN labels; the issuer's gold scan reported SIX. **Both were right.** Six truncate at
exactly 30 chars; **`'Consumer Staples Distribution'` truncates AT A SPACE and is stripped to 29**, so
a census keyed to the 30-char cap **structurally cannot see it** while a diff keyed on CHANGE finds
all seven. **The gap read as a discrepancy in the WORLD when it was a discrepancy in the INSTRUMENT.**
⚠ `ETFS_INGEST.TO-9-DS` section 3 already documents this trap in the other direction --
`'Household & Personal Products'`, 29 chars and COMPLETE. `0.7.0_AE_CloudOps~M` used it as an in-data
negative control: the decode left it untouched and it kept `observed`, showing the decode does not
over-fire on a short-but-complete label. **A 59-row count alone cannot establish that.**

⚠ **THE RE-ADDRESS SAYING "score against `gold/holding/date=2026-08-28`" IS WITHDRAWN.** It was the
issuer's ASSUMPTION about the plane, now measured wrong. **The criterion TEXT governs; the platinum
artifact is where this decode is observable.** The gold block above is retained rather than deleted
because it is a true measurement and its retraction is the lesson.
