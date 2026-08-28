# TO ETFS_INGEST.TO-8 — the PUBLISHER carries `GICS_INDUSTRY_GROUP_NAME` to platinum (`INGEST-T4-1`, the rung `TO-6` stops one short of)

<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED) — `INGEST-T4-1` (the publisher + the served key `platinum/etfs/positioning_data.json`) and the SERVED half of `INGEST-T5-1` (condition (ii)).</decomp_ref>
<certification>Rides the SAME certified decomp as `TO-6` (`3.0.0_SA_CVO~Z` @422bdb431b, bound to @fcdf042972). ⛔ **NO new cell is added** — `INGEST-T4-1` is an existing certified cell that no live TO claimed. Cut as a SEPARATE TO rather than as a `TO-6` amendment **precisely so `TO-6`'s certification is not disturbed** under a live clock.</certification>
<issued_to>0.4.0_DS_ClientPlatform~Q</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>SEATED — same lane, same project, same context as `ETFS_INGEST.TO-6`. **Rule 27 is satisfied: one instance, one project.** Take `TO-6` first; this TO is the rung immediately after it.</seating_trigger>
<placement>SITE Z (Rule 26) — D4 is SITEZ-placed until the project is done.</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T01:1xZ</issued>
<status>pending -- ⛔⛔ **NOT CERTIFIABLE: NO PROOF-OF-SPEC INSTANCE EXISTS. THIS NEEDS AN EXECUTOR, NOT A CERTIFIER.** Measured 15:2xZ by `3.0.0_SA_CVO~Z` and re-measured at this seat: this TO **DECLARES NO `instance_path` AT ALL**. **POSITIVE CONTROL: the same probe finds `ETFS_INGEST.TO-5`'s instance present on disk, so the absence is a MEASUREMENT and not a broken read.**

⛔ **AND THE DISPOSITION THIS FACE CARRIED WAS MINE AND WRONG.** After the 13:00Z fire `2.0.0_SA_COO~Z` disposed this TO to `queued -- for 3.0.0_SA_CVO~Z CERTIFICATION`. **The three rungs did pass and that evidence stands -- but a certifier cannot certify a TO with no instance to validate. I routed a BUILD-SIDE GAP to the certifier.** ⚠ **I made this same error on `ETFS_POSITIONING` TO-1/TO-5 and was corrected on it minutes earlier; I then repeated it here without re-checking whether an instance existed for a TO I was disposing myself.**

⭐ **WHAT SURVIVES UNCHANGED:** all three rungs PASS on the 13:00Z SCHEDULED fire, the falsifiable prediction held on both exact limbs (`ABSENT_FROM_SOURCE`=1=ABT; `NOT_APPLICABLE_NON_EQUITY`=8= the run's own FI count), and every measurement on this face is intact. **What is missing is the INSTANCE that records it in the form a certifier can reject on** -- and per CLAUDE.md a value must carry its claim in a field a consumer can reject on. **The evidence exists; its machine-readable carrier does not.**

**OWNER: an EXECUTOR to file the instance. No live DS lane; seat request with `0.0.0_AB_MSTR~Z`, Andrew's word governs.** ⛔ **NOT a certification item; must not be counted as one.**

⚠ **ORIGINAL `<status>` PRESERVED VERBATIM BELOW -- APPENDED, NOT REPLACED.**

queued -- for `3.0.0_SA_CVO~Z` CERTIFICATION. **THE 13:00Z EXERCISE GATE IS DISCHARGED, ALL THREE RUNGS PASS, AND THE FALSIFIABLE PREDICTION HELD ON BOTH EXACT LIMBS** (`ABSENT_FROM_SOURCE` = 1 = ABT; `NOT_APPLICABLE_NON_EQUITY` = 8 = the run's own FI count). Served `industry_group` KEY PRESENT 189 of 189 against a measured baseline of 0; gold parquet read directly with a negative control; `TO8-AC4` no-regression 189 of 189 identical against the pre-fire copy, all 11 sectors matching. Evidence and method are on this face. **NO EXECUTOR ACT IS PENDING AND NO DS LANE IS NEEDED.** ⚠ First token is deliberately `queued` and NOT `complete`: this seat measured the EXERCISE, not the SOURCE/DATA-class criteria the dead lane discharged, so `queued` keeps the row VISIBLE on the register -- the over-pessimistic direction announces itself and the over-optimistic one cannot.</status>

## ⛔⛔ THE OBSERVED `industry_group` MEMBER SET IS VENDOR-TRUNCATED AT 30 CHARS AND IS **NOT ADOPTION-READY**

**DISARM of a surprise-channel {OBSERVATION, ARMED} raised by `1.0.0_SA_CTO~Z` (msg 13156), which
named `2.0.0_SA_COO~Z` as disarming owner. This line IS the disarm, written same-turn.**

`etf_positioning_gold.py:173-180` deliberately mints **no closed value list**, and says the manifest
will print the OBSERVED member set *"so a vocabulary can be ADOPTED FROM MEASUREMENT on a later TO."*
⛔ **THAT MEASUREMENT NOW EXISTS AND IT IS CONTAMINATED. DO NOT ADOPT A VOCABULARY FROM TODAY'S
OBSERVED SET.** It would enshrine `'Technology Hardware & Equipmen'` as a ratified member name.

```
MEASURED on bbg/2026-08-27/characteristics.PARQUET by 2.0.0_SA_COO~Z -- a DIFFERENT FILE from the
.csv 1.0.0_SA_CTO~Z read, same run, so this is corroboration and not repetition:
  165 non-blank · MAX LENGTH 30 · 51 rows AT the cap · nothing above it
  'Commercial & Professional Serv'  'Consumer Discretionary Distrib'  'Health Care Equipment & Servic'
  'Pharmaceuticals, Biotechnology'  'Semiconductors & Semiconductor'  'Technology Hardware & Equipmen'
CONTROL: GICS_SECTOR_NAME max length 22 on the same rows -- entirely BELOW the cap, so the truncation
is invisible there. Consistent with a per-field limit; NOT proof of one.
```
⛔⛔ **SECOND, INDEPENDENT REASON NOT TO ADOPT -- ADDED 15:0xZ from `1.0.0_SA_CTO~Z` (13255) and
`3.0.0_SA_CVO~Z` (13251). EITHER ONE ALONE IS SUFFICIENT.**
```
REASON 1 (already recorded)  the observed values are TRUNCATED
REASON 2 (new)               the observed set is INCOMPLETE -- 23 distinct values against a CLOSED
                             PUBLISHED GICS SET OF 25. A table built from today's data rests on a
                             PARTIAL DENOMINATOR, and 2 members have never been seen.
```
⛔ **AND THE REPAIR-AFTER-THE-FACT OPTION HAS A HAZARD THAT KILLS ITS NAIVE FORM: LENGTH CANNOT
IDENTIFY WHAT NEEDS REPAIRING.**
```
'Household & Personal Products'   29 chars   COMPLETE -- that IS the full GICS name
'Consumer Staples Distribution'   29 chars   TRUNCATED from "... & Retail" (37)
```
>> **TWO VALUES, IDENTICAL LENGTH, OPPOSITE STATES.** Keyed on `len >= 29` a repair CORRUPTS a correct
   value; keyed on `len == 30` it MISSES this one. **THE REPAIR FUNCTION CANNOT DETECT ITS OWN INPUT
   SET.** ⭐ Same shape as the `ContentLength 2196 -> 2196` near-miss: **a length is not a
   discriminator for a content question.**
⚠ **AND THE SOVEREIGN'S STATED PREMISE FOR THAT OPTION IS FACTUALLY WRONG** -- *"the ones truncated
seem to mostly be equipment"*: measured, only **2 of 7** involve "Equipment"; the other five complete
five different ways (`...ices`, `...es`, `...ution & Retail`, `... & Life Sciences`, `... & Retail`).
⛔ **A repaired value would also be DERIVED, not OBSERVED** -- it needs its own `industry_group_basis`
member saying RESOLVED rather than OBSERVED, or it serves a derived value under a measured label.

⭐ **THE PIPELINE IS CORRECT AND THIS IS NOT A REGRESSION.** Bloomberg emitted the value truncated;
the passthrough passed it through faithfully, which is exactly what the ruling specified (no default,
no fallback). Every rung behaved correctly and the artifact is faithful to its source.
⚠ **The rendered page will show truncated labels until this is addressed.** ⛔ **NOT CHASED HERE:** a
field-width override or an alternate Bloomberg field is a VENDOR-API act in the INGEST lane, and
CLAUDE.md forbids a vendor call without Andrew's explicit per-use word. **Surfaced, disarmed, not
implemented.**

## ⭐⭐ THE 13:00Z FIRE LANDED. ALL THREE RUNGS PASS. MEASURED 2026-08-28 13:1xZ by `2.0.0_SA_COO~Z`.

```
TRIGGER   etf-positioning-producer-daily cron(0 13) ENABLED
GOLD      gold/holding/date=2026-08-27/holding.parquet   written 2026-08-28T13:01:23Z
SERVED    platinum/etfs/positioning_data.json            written 2026-08-28T13:01:26Z
          128122 B -> 146944 B      data_as_of 2026-08-27   <- the as_of predicted from gold's OWN resolver
```

**RUNG 1 -- VENDOR RETURNS IT.** `bbg/2026-08-27/characteristics.parquet`, 14 cols, field present,
`GICS_SECTOR_NAME` control present, bogus-token control absent. 165 of 165 RESOLVED rows populated.
**RUNG 2 -- GOLD CARRIES IT.** Read on the gold parquet ITSELF, not inferred from the served artifact:
189 rows, `industry_group` and `industry_group_basis` columns PRESENT, negative control
`industry_group_bogus` ABSENT (the probe discriminates).
**RUNG 3 -- SERVED CARRIES IT TO THE CONSUMER.** ⛔ Scored as **KEY PRESENCE**, not `.get()`:
```
industry_group        KEY PRESENT on 189 of 189      (BASELINE 0 of 189)
industry_group_basis  KEY PRESENT on 189 of 189      (BASELINE 0 of 189)
```

### ⭐ THE FALSIFIABLE PREDICTION HELD ON BOTH EXACT LIMBS
```
PREDICTED  ABSENT_FROM_SOURCE == 1, and it is ABT      MEASURED  1, and it is ABT in DIVZ      ✓
PREDICTED  NOT_APPLICABLE_NON_EQUITY == the run's OWN FI count
                                                       MEASURED  8, and the run's FI count is 8  ✓
NOT PREDICTED (deliberately): the observed / not-in-characteristics split.
BASIS, gold AND served, IDENTICAL: observed 180 | not-applicable-non-equity 8 | absent-from-source 1
ASSET CLASS: Equity 181 | Fixed Income 8.   180 + 8 + 1 = 189, complete and MECE.
```
⚠ **THE `8` COINCIDED WITH THE LITERAL I REFUSED TO PIN TO, AND THE REFUSAL WAS STILL RIGHT.** It was
scored against the RUN'S OWN Fixed-Income count, not against the 08-26 observation that happened to
equal it. A criterion that reads the run cannot false-FAIL when holdings move; one pinned to `8` can.

### `TO8-AC4` -- NO CONSUMER REGRESSION, MEASURED AGAINST THE PRE-FIRE COPY
Captured before the fire precisely so this could be a DIFF and not a recollection:
```
sub_asset_class IDENTICAL on 189 of 189 (book,ticker) pairs
holdings added 0 · dropped 0 · intersection COMPLETE  -> no cross-vintage caveat applies
POSITIVE CONTROL, the 11 sectors AC4 names: all 11 present both sides, EVERY count identical
  Info Tech 35 · Financials 32 · Health Care 22 · Industrials 22 · Staples 16 · Comms 15
  Discretionary 14 · Utilities 11 · Energy 9 · Materials 4 · Ultra Short Duration 8
```

### ⚠ WHAT THIS SEAT DID **NOT** SCORE
`TO6-AC1/AC2/AC4/AC5` are SOURCE- and DATA-class criteria discharged by the executing lane BEFORE it
died; this seat measured the **EXERCISE**, which is what the clock gated. **No claim of "6 of 6" is
made here** -- that would assert a discharge nobody performed. ⚠ Served rows are 189 while the 08-27
silver partition holds 187; the producer synthesizes residual/cash rows. **Noted, not chased.**

<priority>P1 — with `TO-6` it completes the producer half of Andrew's promote condition (ii). ⚠ **Both must land before the ~13:00Z gold fire** or the field does not reach platinum today.</priority>
<authority>Andrew-direct 2026-08-24 ~22:12Z (GICS is the served sub-category vocabulary) · his promote condition (ii), VERBATIM: *"and it displays properly on DEV build with GICS replaced for sub-categories on frontend"* · `1.0.0_SA_CTO~Z`'s Rule-24 ruling (msg 11384): **a NEW PARALLEL FIELD, never a swap into `sub_asset_class`**.</authority>

---

## WHY THIS TO EXISTS — a measured one-rung gap

`1.0.0_SA_CTO~Z` measured seven rungs between the vendor pull and the rendered page (msg 11384) and
found the field absent on every plane. `TO-6` covers the pull and the gold row. **It stops there.**

```
MEASURED at @9ace0b75b9, on TO-6's own file:
  grep -ci "publisher|HOLDING_KEYS"  ->  0     <- the publisher rung is NOT in TO-6
  grep -ci "gold"                    ->  5     <- POSITIVE CONTROL: the instrument sees what is there
```

⛔ **The gold row carrying the key is necessary and NOT sufficient** -- but **THE MECHANISM THIS
PARAGRAPH GAVE WAS WRONG**, corrected by `1.0.0_SA_CTO~Z` (msg 13091) against the DEPLOYED bytes, and
relayed here -- **not re-measured** -- by `2.0.0_SA_COO~Z` on 2026-08-28. `HOLDING_KEYS` is **not a
projection and drops nothing**: it is a COMPLETENESS ASSERTION (`:525` computes expected-but-absent
keys, `:527` appends them to `problems`), so it **FAILS LOUD**. A key absent from it goes
**UNCHECKED**, which is the OPPOSITE direction from "dropped on the way to platinum with no error".
⭐ **THIS TO'S ACT IS STILL RIGHT AND ITS STATED REASON WAS NOT** -- a distinction worth keeping on
the face rather than quietly rewriting. Adding the key restores the validator's COVERAGE of that key;
it does not rescue the key from a silent drop this file never performed. The real enumerated
allowlist is `etfAdapter.ts:77`, a different file and a different lane, and it already carries the
field.
⚠ **LINE NOTE:** this paragraph and `TO8-AC1` cite `:230` from the repo at cut time; the deployed
bytes read `:269`. **Cite BY CONTENT, not by line** -- the list has moved once already.

## OBJECTIVE

Carry `GICS_INDUSTRY_GROUP_NAME` from the gold row through the publisher onto every holding row of
`s3://opal-data-portal-v2/platinum/etfs/positioning_data.json`, **as a NEW KEY ALONGSIDE
`sub_asset_class`.**

## ⛔ THE SHAPE IS RULED — DO NOT SWAP

`1.0.0_SA_CTO~Z` ruled against re-pointing `sub_asset_class` to the finer value. **Two independent
grounds; either alone is sufficient:**

1. **Rule 24 (i) MECE / (ii) SAME GRAIN / (iii) INTENT COHERENCE.** GICS industry groups classify
   **equities**. The four books also carry a money-market security, a canonical cash line, a
   synthesized residual row and a fixed-income sleeve. A swap sends every non-equity row to null and
   strands `Cash & Cash Equivalents` and `Ultra Short Duration` at a **different level of the same
   hierarchy inside the same field.**
2. **`sub_asset_class` is a byte-verified ratified consumer contract.** `etf_positioning_gold.py:141-147`
   warns in source that a near-miss **does not fail loudly**: it misses `SUB_ASSET_CLASS_ORDER`, drops
   to the unmapped bucket and renders at the bottom of the panel — **presenting as a SORT BUG on the
   client's surface rather than a producer defect. It ships GREEN.**

⭐ Consistent with what is already ruled: sub-category renders as **recessive text beside** the coloured
sector (`ETFS_INGEST.TO-5` AC6, option (b), COMPLETE). **Recessive text beside a coloured value IS a
parallel field**; a replacement would have required a colour act that TO-5 already ruled out.

## ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `TO8-AC1` | **`HOLDING_KEYS` carries the new key** — `etf_positioning_publisher.py:230`, cited `file:line @ <commit-ish>`. ⛔ **ADDITIVE: `sub_asset_class` remains present, unchanged, and at its existing grain.** Show the key list before and after. | `INGEST-T4-1` | |
| `TO8-AC2` | ⛔ **THE SERVED ARTIFACT CARRIES IT, WITH A PRINTED DENOMINATOR.** Census **every** holding row of the served `positioning_data.json` — the current denominator is **189 rows / 4 portfolios** and must be re-derived, not copied. Report: rows carrying a non-null industry group, rows null, and **the denominator**. ⛔ **A coverage number without its denominator is not a result.** | `INGEST-T4-1` `INGEST-T5-1` | |
| `TO8-AC3` | ⛔ **NULLS ARE EXPECTED AND MUST BE EXPLICIT, NOT INHERITED.** The non-equity rows (cash, the money-market security, the synthesized residual, the fixed-income sleeve) have **no** industry group **by construction**. State their treatment. ⛔ **WHAT IS PROHIBITED IS A NULL QUIETLY BECOMING A SECTOR** — the same prohibition `TO-6`'s `AC6` carries at the aggregate grain, restated here at the row grain because the two fail independently. | `INGEST-T4-1` | |
| `TO8-AC6` | ⛔ **THE VALUE CARRIES ITS CLAIM — `industry_group_basis` IS REQUIRED ON THE SERVED ROW. ADDED BY ISSUER AMENDMENT 2026-08-28 ~02:2xZ (msg 12038).** CLAUDE.md: *"A VALUE MUST CARRY ITS CLAIM — in a field a consumer can reject on... **the consuming half is the whole mechanism; an unenforced provenance field drifts to unpopulated.**"* An `industry_group` served without a rejectable basis is a value that does not carry its claim, on a client-facing key. <br>**The BASIS enum is CLOSED** — its members are facts about our own pipeline, not vendor values: `observed` · `not-applicable-non-equity` · `field-not-in-source` · `security-not-in-characteristics` · `absent-from-source`. ⭐ **The uncovered member hunted and found was `security-not-in-characteristics`**, which a four-member draft had collapsed. <br>⛔ **NO CLOSED VALUE LIST IS MINTED FOR THE GROUP NAMES THEMSELVES** — the field has not landed, so enumerating its members would be an **UNMEASURED EXACT CONSTANT that fails closed while looking principled.** The declared domain is the vendor's value set; emit `industry_group_observed_members` **IN THE GOLD RUN MANIFEST — NOT on the served row.** ⛔ **PLANE NAMED BY ISSUER AMENDMENT 2026-08-28 ~02:3xZ (msg 12089): the original clause named NO PLANE while sitting under a `cell_ref` of `INGEST-T4-1`, the PUBLISHER/served-key cell — a RUN-LEVEL clause attached to a PER-ROW cell. That was a defect in this criterion, not in the build.** Grounds, any one sufficient: (i) **Rule 24 (ii) SAME GRAIN** — a member list riding on every book inside a row-shaped served document is a grain error; (ii) the clause's own stated reader is *a future DS/CVO seat doing a vocabulary act*, **not the frontend**; (iii) putting it on the served key would **widen the CLIENT-FACING contract for a purely INTERNAL purpose**, which is what this TO's own `AC1` one-key discipline exists to prevent. ⭐ **The same reading governs `TO-6` `AC6`'s run-level coverage/denominator emissions: also correct in the gold manifest, also not to be moved.** So the vocabulary can be **ADOPTED FROM MEASUREMENT** on a later TO. *`GICS_SECTORS` is adopted-not-minted precisely because it WAS measured; this has not been.* <br>⚠ **THIS IS NOT NEW SCOPE — IT MAKES `TO8-AC3` EXECUTABLE.** AC3 already required *"nulls are EXPLICIT, never inherited"* and prohibited *"a null quietly becoming a sector"*; the basis enum is the MECHANISM by which a row says WHY it has no group instead of being silently absent. <br>⭐ **PROCESS NOTE, recorded because the record is the point:** this requirement first reached the lane as `1.0.0_SA_CTO~Z`'s 11832, which **that seat withdrew unprompted** on the ground that adding an AC to a frozen TO is the ISSUER's act under Rule 27. **It is now taken as the issuer's act.** The substance never changed; the authority did. `f0e2a05889` stands and is NOT reverted. | `INGEST-T4-1` | |
| `TO8-AC4` | **NO CONSUMER REGRESSION.** `sub_asset_class` values on the served artifact are **byte-identical** to their pre-change values for every row. ⚠ **The positive control matters more than the diff:** show the sector values and **every non-equity value PRESENT IN THE SERVED SET** still resolve in `SUB_ASSET_CLASS_ORDER`, **with the denominator printed** ⛔ **RE-CUT 2026-08-28 ~19:3xZ by `2.0.0_SA_COO~Z` (issuer). ~~the 2 non-equity values~~ WAS AN UNMEASURED PINNED LITERAL AND THE SERVED ARTIFACT CARRIES ONE.** Measured by `0.4.0_DS_ClientPlatform~Q`: all four CASH rows read `Ultra Short Duration`; **`Cash & Cash Equivalents` is not a served `sub_asset_class` value at all** (manifest vocab 13, served exercises 12) — identical pre- and post-fire, so **NOT a regression and NOT caused by this TO**, but the positive control could not be run as written. ⚠ **AND THIS CRITERION VIOLATES A PRINCIPLE STATED IN ITS OWN PREAMBLE**, eleven lines above: *"A criterion that reads the run cannot false-FAIL when holdings move; one pinned to `8` can."* **I refused the literal `8` and then pinned the literal `2` in the next criterion.** Scoring PASS on the values that exist was correct — *an absence check cannot tell a fix from a refactor.* | `INGEST-T4-1` | |
| `TO8-AC5` | **PROVENANCE ON THE RUN.** State whether the evidence comes from a **scheduled** fire or an **ad-hoc QA** run, in a field a certifier can reject on. ⛔ **An ad-hoc artifact is never production evidence** (CLAUDE.md §5). A QA run is legal here and is legal ONLY if it says so. | `INGEST-T5-1` | |

## NOT YOURS

- ⛔ **The FRONTEND.** Rung 7 is `0.4.0_DE_ClientPlatform~Z`'s. This TO makes the field **available**; it
  does not render it. **Do not touch `portal/`.**
- ⛔ **`ETFS_INGEST.TO-7`** — `0.4.0_DS_ClientPlatform~P`'s, not re-addressed.
- ⛔ **`ETFS_POSITIONING.TO-5`'s discharge** — sits with `3.0.0_SA_CVO~Z`. TO-6's lifted sequence is
  **not** a discharge and must not be cited as one.

## STANDING

⛔ **No ad-hoc `mdpf` gold run before 2026-08-28 13:30Z** (destroys `D1_CATVIEWS.TO-P1-AE` AC1's
discriminator — different pipeline, same box). · `data/*/scripts/gold/*.py` is the DS lane's own
commit→QA-deploy path (Rule 13). · Every `.py` edit passes `.tools/commit-gate.sh`.

## REPORTING

Deliverable + proof instance in this lane's `deliverables/`, via `.tools/safe-commit.sh --author
"0.4.0_DS_ClientPlatform~Q <0.4.0_DS_ClientPlatform~Q@opal.agent>" -F <msgfile>` (message file written
by a **non-shell** writer). Report to `2.0.0_SA_COO~Z`; `3.0.0_SA_CVO~Z` certifies. **ACK on receipt.**


## POST-FIRE RECIPE -- SO NO SEAT NEEDS TO SURVIVE UNTIL 13:00Z

**Added 2026-08-28 ~08:1xZ by `2.0.0_SA_COO~Z` (issuer).** ⛔ **The executing lane `0.4.0_DS_ClientPlatform~Q`
IS GONE.** `0.0.0_AB_MSTR~Z` ruled no builder is needed -- **all build commits precede the third apply
`e0672e24a0` (22:46:16Z), verified BY CONTENT** -- so what remains here is an OBSERVATION, and this is the
method for it. **Same pattern as `ETFS_SATELLITES.TO-6-AE`, which discharged cleanly on exactly this.**

**PRE-VERIFIED AT 08:1xZ, so a successor does not re-derive it:**
```
  the pull REQUESTS the field   integrations/bloomberg/pipeline/etf_daily_pull.py:239
                                "GICS_SECTOR_NAME", "GICS_INDUSTRY_GROUP_NAME"
  committed + ON ORIGIN         2 occurrences at HEAD and at origin/SITEZ; no local drift
                                NEG CONTROL: a bogus token returns 0
  authored                      1.0.0_SA_CTO~Z @ebce987b42, 08-27 13:46Z
```
⚠ **THAT ESTABLISHES THE PULL ASKS. IT DOES NOT ESTABLISH THE VENDOR RETURNS.** **Requesting is not
receiving** -- rung 1 below is what closes that.

**THE CHAIN, THREE RUNGS, EACH ITS OWN READ:**
```
1  VENDOR FILE   header of bbg/{as-of}/characteristics.csv contains GICS_INDUSTRY_GROUP_NAME
     >> RUNG 1 PASS, measured 2026-08-28T11:1xZ by 2.0.0_SA_COO~Z. bbg/2026-08-27/characteristics.csv,
        LastModified 2026-08-28T11:06:33Z, 14 columns. GICS_SECTOR_NAME col 3 = THE CONTROL, PRESENT.
        GICS_INDUSTRY_GROUP_NAME col 4. THE VENDOR RETURNS THE FIELD -- not merely that the pull asks.
        Rungs 2 and 3 stay OPEN and wait on the ~13:00Z scheduled gold fire. <<
     CORRECTION TO THIS RECIPE, BY ITS AUTHOR: it hardcoded bbg/2026-08-28/. {as-of} IS T-1, NOT THE
        RUN DATE. The literal key I wrote lists EMPTY, and an empty listing reads as 'the pull did not
        fire' -- a FALSE ABSENCE handed to a successor. The AC and the premise-oracle table both said
        {as-of} correctly; only the recipe resolved it, and resolved it wrong.
     POSITIVE CONTROL: GICS_SECTOR_NAME must be present in the SAME header. If the control is
     absent the read is BROKEN, not a negative -- say which you got.
     Measured 08-21 by 3.0.0_SA_CVO~Z: INDUSTRY_GROUP 0, SECTOR 1. That is the pre-state.
2  GOLD ROW      gold/holding/date=2026-08-27/holding.parquet carries the key
     ⛔ THE SAME T-1 TRAP AS RUNG 1, AND THIS RECIPE HAD IT WRONG HERE TOO. It said "the gold
     parquet for 2026-08-28". MEASURED 2026-08-28T11:2xZ by 2.0.0_SA_COO~Z (author of the defect):
     the two most recent SCHEDULED fires both wrote T-1 -- 2026-08-27T13:01:23Z -> date=2026-08-26,
     and 2026-08-26T13:01:23Z -> date=2026-08-25. Newest partition at read time IS date=2026-08-26;
     date=2026-08-27 is what today's 13:00Z fire lands. A listing at date=2026-08-28 is EMPTY and
     reads as a FALSE ABSENCE. Bucket opal-data-etfs, per etf_positioning_gold.py:98.
3  SERVED        platinum positioning_data.json carries it to the CONSUMER
     ⛔ THE MECHANISM WRITTEN HERE WAS WRONG. CORRECTED BY 1.0.0_SA_CTO~Z (msg 13091) against the
     DEPLOYED bytes (CodeSha256 wuu+/cHD5gHb..., matched BEFORE reading), and RELAYED HERE, NOT
     RE-MEASURED, by 2.0.0_SA_COO~Z: etf_positioning_publisher.py HOLDING_KEYS is a TUPLE of 15 keys
     at :269 whose ONLY other occurrence is :525 `hm = [k for k in HOLDING_KEYS if k not in h]` ->
     :527 appends to `problems`. IT IS A COMPLETENESS ASSERTION THAT FAILS LOUD, NOT A PROJECTION.
     Nothing is dropped by that file; a key absent from HOLDING_KEYS goes UNCHECKED -- the OPPOSITE
     direction from the hazard named. THE REMEDY STILL STANDS (an unchecked key is a real loss of
     validator coverage); only the reason given for it was false.
     ⭐ THE SILENT-DROP CLASS IS REAL AND LIVES IN ANOTHER FILE AND ANOTHER LANE:
     portal/src/pages/Positioning/shared/etfAdapter.ts:77 toCurrentHolding is the enumerated
     allowlist, and its own comment records 2026-08-25, when it silently dropped five return windows
     the producer had begun emitting. 1.0.0_SA_CTO~Z measured that it ALREADY CARRIES the field:
     :85-86 industry_group + industry_group_basis at the tree that IS on PROD (2858e7f5), rendered
     at HoldingsTab.tsx:1462-1469; neg control sub_asset_class 2 / industry_group 2, same file.
     >> THEREFORE IF industry_group IS ABSENT OR EMPTY AFTER 13:00Z, THE CAUSE IS UPSTREAM
        POPULATION -- gold, or the join -- AND NOT A DROPPED KEY IN THE SERVING PATH.
     ⚠ WHAT 1.0.0_SA_CTO~Z EXPLICITLY DID NOT MEASURE, so nobody inherits more than was checked:
        gold POPULATION is UNTESTED and is exactly what 13:00Z exercises; the rest of the publisher
        write path is UNAUDITED; and A KEY PRESENT IN AN ALLOWLIST IS NOT A POPULATED VALUE.
        RUNGS 2 AND 3 STAY OPEN.
```

### PRE-FIRE STATE, MEASURED 2026-08-28T11:2xZ -- READ THIS BEFORE SCORING AT 13:05Z

**RUNG 1 IS CLOSED ON THE ARTIFACT GOLD ACTUALLY CONSUMES, NOT ONLY THE CSV I FIRST READ.**
`etf_positioning_gold.py:1669` loads `characteristics.PARQUET`; my first read was the `.csv`. Same run
wrote both, but "same run implies same schema" is an INFERENCE, so the parquet was read directly:
```
opal-data-etfs/bbg/2026-08-27/characteristics.parquet   14 columns
  GICS_INDUSTRY_GROUP_NAME   PRESENT        <- the field
  GICS_SECTOR_NAME           PRESENT        <- positive control
  GICS_NOT_A_REAL_FIELD      ABSENT         <- negative control: the probe discriminates
  POPULATION 165 of 172 rows non-null (96%), real values ("Banks", "Capital Goods", ...)
```

**RUNG 2's LIVE QUESTION -- WHICH PARTITION GOLD LOADS -- IS ANSWERED, USING GOLD'S OWN RESOLVER.**
Asked by `1.0.0_SA_CTO~Z` (msg 13097 s.4) and measured by `2.0.0_SA_COO~Z` by executing
`resolve_as_of()` READ-ONLY (`list_objects_v2` only -- NOT a pipeline run, the discriminator is intact):
```
expected_last_trading_day = 2026-08-28   (NYSE/hardcoded-fallback-2024-2027)
newest silver/holdings    = 2026-08-27   (76 partitions, 17 non-trading skipped, newest 08-23 Sun)
>> RESOLVED as_of = 2026-08-27   trading_days_behind = 1
>> gold will load opal-data-etfs/bbg/2026-08-27/characteristics.parquet
```
The exact landing signal `_bbg_partition_exists` compares -- TOP-LEVEL `bbg/2026-08-27/run_manifest.json`,
not the `constituents/` sibling -- EXISTS (1 key, exact match).
⚠ **RESOLVED AT 11:2xZ, NOT AT 13:00Z.** It is stable across the window only because silver's producer
fires `0 22 * * ?` and `bbg/2026-08-28/` needs a pull that has not run -- a REASONED EXPECTATION with its
basis stated, NOT a measurement of 13:00Z.

### ⛔ SCORE ON THE BASIS FIELD, NEVER ON THE NULL (`1.0.0_SA_CTO~Z`, msg 13097, relayed)

`industry_group_of()` never returns a bare null -- **every null carries its reason**, MECE-ordered. An
all-null result is **not one outcome, it is four**, distinguishable with no extra query:
```
manifest industry_group_field_in_source == false  -> gold never SAW the column. Upstream/partition.
basis all FIELD_NOT_IN_SOURCE                     -> same cause, per-row confirmation.
basis all SECURITY_NOT_IN_CHARACTERISTICS         -> the JOIN failed. hc is None per row.
basis all ABSENT_FROM_SOURCE                      -> vendor returned the column BLANK.
basis OBSERVED + values                           -> success.
NOT_APPLICABLE_NON_EQUITY on cash/FI rows         -> CORRECT, not a miss. EXPECT THESE.
```
⛔ **A SCORER WHO CHECKS ONLY "IS industry_group NULL" CONFLATES FOUR CAUSES ACROSS THREE LANES** and
throws away the instrument the producer already built.
⚠ **STALE COMMENT, FLAGGED NOT EDITED** (`etf_positioning_gold.py:174`): it says the field *"has not
landed in our artifact yet"*. **That premise expired at 11:06:33Z today.** Its REASONING still stands
(no closed value list is minted). A reader hitting it mid-investigation concludes the field cannot be
there yet.

### WHAT REMAINS GENUINELY UNTESTED -- nobody may inherit more than was checked
- ⛔ **THE JOIN IS NOT UNTESTED -- THAT LINE WAS WRONG AND IS RETRACTED HERE.** `2.0.0_SA_COO~Z`
  wrote "untested until the fire"; `1.0.0_SA_CTO~Z` (msg 13103) falsified it with a PRODUCTION
  POSITIVE CONTROL: `industry_group` rides the IDENTICAL `hc` object from the IDENTICAL lookup line
  (`:1189`) that already produces the SERVED `sub_asset_class` (`:1190` -> `:1198`). Measured on the
  served artifact (`platinum/etfs/positioning_data.json`, `data_as_of 2026-08-26`, 189 holdings):
  **NINE distinct GICS sectors** -- IT 35, Financials 32, Health Care 22, Industrials 22, Staples 16,
  Comms 15, Discretionary 14, Utilities 11, Energy 9. **A dead join manufactures a clean TOTAL
  absence; nine populated sectors is the opposite shape.** The join is live and load-bearing today.
  ⚠ **LATENT, NOT LIVE:** the two sides normalise ASYMMETRICALLY -- chars `:1122` applies
  `_strip_bbg_security`, holdings `:1188` does NOT split. Served tickers are BARE (`PM`, `VZ`, `MPLX`),
  so both land on the same string. **If an issuer ever emits a suffixed `holding_ticker` that row
  silently misses the join** -- and would surface, correctly labelled, as
  `SECURITY_NOT_IN_CHARACTERISTICS`. Recorded, not chased.

### ⛔ CALIBRATE BEFORE SCORING, OR A CORRECT RUN READS AS A FAILURE (`1.0.0_SA_CTO~Z`, msg 13103)
```
characteristics parquet   172 rows   (165 populated = 96%; 7 already BLANK)
served holdings           189
>> EVEN A PERFECT JOIN LEAVES >= 17 HOLDINGS WITH NO CHARACTERISTICS ROW.
```
⛔ **A NON-ZERO `SECURITY_NOT_IN_CHARACTERISTICS` AT 13:00Z IS CORRECT BEHAVIOUR, NOT A DEFECT --
and so is a non-zero `ABSENT_FROM_SOURCE`** (7 of 172 source rows are already blank). Cash, residual
and non-equity lines account for some of the 17; the rest are genuine misses in the vendor set.
⛔ **A SCORER EXPECTING 100% `OBSERVED` FILES A FALSE FAIL ON A WORKING PIPELINE.**
⭐ `ig_basis_counts` at `:1218` tallies every basis value, so **the run reports its own coverage --
read that, not a spot-check.**

### ⭐ THE SOURCE SIDE, RESOLVED EXACTLY -- 96% WAS THE WRONG DENOMINATOR (`2.0.0_SA_COO~Z`, 12:1xZ)

I first reported "165 of 172 non-null (96%)" and left 7 blanks unexplained. **Measured, the 172 partition
cleanly and the population is BETTER than 96%:**
```
165  equities WITH GICS_INDUSTRY_GROUP_NAME            -> populated
  6  FUNDS (FXFXX, SALXX, PFDE, PFOE, DIVZ, IDVZ)      -> CORRECTLY blank; an ETF has no industry group
  1  ABT US Equity -- VENDOR REJECTION                 -> __error__ = "Unknown/Invalid Security [nid:19354]"
                                                          EVERY column nan. The ONLY non-null __error__ in 172.
>> AMONG ROWS THE VENDOR ACTUALLY RESOLVED, POPULATION IS 165 of 165 = 100%.
```
Fund/equity separation verified, not assumed: `IG non-null AND FUND_EXPENSE_RATIO non-null` = **0**, so
the proxy discriminates perfectly on this data.
⚠ **MY FIRST STORY WAS "the 7 blanks are the funds" AND IT WAS WRONG BY ONE.** Six are. The seventh is
ABT, and it is the informative case -- **the row that did not fit was the finding, not a caveat.**

### ⛔ WHAT A 13:05Z SCORER MUST NOT CHASE
- **ABT US Equity will carry NO characteristics at all** -- not a pipeline defect, a vendor rejection
  upstream of everything here. It should surface as `ABSENT_FROM_SOURCE` (or as a missing join row) and
  **that is CORRECT.** Do not debug the pipeline for it.
- **The six funds will carry no industry group** and should read `NOT_APPLICABLE_NON_EQUITY`. Also correct.
⭐ **SURFACED, NOT CHASED (surprise-channel class OBSERVATION / INERT):** `ABT US Equity` is a large,
real, listed equity and Bloomberg is returning *Unknown/Invalid Security*. **That is worth someone's
attention as a VENDOR/TICKER question -- it is not this TO's, and nothing here waits on it.**

### ⭐ ETFs IS **ONE STAGE** -- THE PRODUCER WRITES THE SERVED KEY ITSELF (`1.0.0_SA_CTO~Z` msg 13147)

Version history, `platinum/etfs/positioning_data.json`:
```
08-27 13:01:25  *  08-26 13:01:26  *  08-25 13:01:23     <- SCHEDULED cadence, 85s after cron(0 13)
08-25 16:30 / 17:47 / 17:50 / 18:07 / 18:54              <- ad-hoc, that day's QA burst
```
**Both planes censused for a second stage and there is none:** Rules holds
`etf-positioning-producer-daily cron(0 13)`; the other eight `etf*` entries are DIFFERENT PRODUCTS
(`etf-ownership-dashboard-daily` 16:00, `etfs-canon-fanin-daily` 15:45, `etfs-netassets-daily` 22:00).
**Scheduler holds no ETFs publisher.**
>> **`industry_group` SHOULD BE READABLE AT THE SERVED KEY BY ~13:01:30Z.** No publisher sits between
   the fire and the artifact -- unlike mdpf.

⛔ **AND THAT ASYMMETRY IS WHY THE mdpf 13:30Z ERROR WAS EASY TO MAKE:**
```
ETFs   cron(0 13)  -> SERVED 85 seconds later                                ONE stage
mdpf   cron(30 13) -> gold -> accrual -> publisher -> SERVED 20 min later     FOUR stages
```
**A CORRECT model from the NEIGHBOURING pipeline, transferred to one with a different shape.** Everyone
reasoning about mdpf had the ETFs chain in working memory -- fire, then served, within the minute --
and that is *exactly right* for ETFs. **Two pipelines, both called "the 13:xx fire", and only one is
direct.**
⭐ **THE RULE THAT MAKES IT UNWRITABLE: A SERVED-ARTIFACT CLAIM NAMES THE *WRITER*, NOT THE TRIGGER.**
`TP1AE-AC1` scores `mdpf-gold-lambda`; the page reads what `opal-assets-mdpf-portal-publisher` wrote.
Naming the writer makes a twenty-minute gap self-evident. ⛔ **A PIPELINE'S STAGE COUNT IS NOT
INFERABLE FROM ITS SIBLING'S** -- census it, do not carry it over.

### ⭐ THE PRE-FIRE BASELINE AT THE SERVED KEY, AND THE EXACT RUNG-3 TEST (`2.0.0_SA_COO~Z`, 12:5xZ)

⚠ **THE BUCKET IS `opal-data-portal-v2`, NOT `opal-data-assets`.** My first probe guessed the latter
and returned **404** -- which at 13:05Z would have read as *"the publisher did not write"*. **FOURTH
false-absence of this shape on this TO today.** Source of truth: `etf_positioning_publisher.py:8`
`s3://opal-data-portal-v2/platinum/etfs/positioning_data.json`.
```
BASELINE, read 12:5xZ:  LastModified 2026-08-27T13:01:25Z · 128122 B · data_as_of 2026-08-26
  189 holdings across DIVZ / IDVZ / PFDE / PFOE
  'industry_group'        KEY PRESENT on   0 of 189
  'industry_group_basis'  KEY PRESENT on   0 of 189
  ABT in DIVZ: asset_class 'Equity', sub_asset_class None
```
⛔ **`.get()` CANNOT TELL "KEY ABSENT" FROM "KEY PRESENT, VALUE NULL" -- BOTH RETURN None.** The
earlier reading *"industry_group: None x 189"* was `.get()`-based and conflated the two. Today the key
is **absent entirely**. ⭐ **SO THE RUNG-3 TEST IS KEY-PRESENCE 0 -> N, NOT "the value became
non-null"** -- and after the fire a PARTIAL success (key present, some values null with a basis) would
read identically to TOTAL failure under `.get()`. **Test `"industry_group" in h`, not `h.get(...)`.**

**THE EMITTERS ARE MEASURED, and they are not `HOLDING_KEYS`:** that tuple is the VALIDATOR (15 keys,
both present). The writes are `:381 "industry_group": _n(h["industry_group"])` and
`:393 "industry_group_basis": _n(h["industry_group_basis"])`. ⚠ **SUBSCRIPT, NOT `.get()`** -- a gold
row missing the column makes the publisher RAISE rather than quietly omit. Fails loud.

### THE POST-FIRE READ IS THREE-WAY, NOT PASS/FAIL
```
1  LastModified advances to ~13:01:2xZ  AND  key present on N holdings   -> PASS. Score the BASIS.
2  LastModified advances  BUT  key absent on all rows                    -> the emitter did not run;
                                                                            deployed bytes != source.
3  LastModified DOES NOT advance (still 08-27T13:01:25Z)                 -> the run did not complete.
                                                                            Check etf-positioning-producer-daily
                                                                            fired at all; a KeyError at :381
                                                                            is one candidate cause.
```
⛔ **DO NOT COLLAPSE 2 AND 3.** "No industry_group at the served key" is true of both and they have
different owners and different remedies.

### THE COMPLETE PRE-FIRE TIMELINE
```
13:00:00Z  etf-positioning-producer-daily fires     ENABLED, cron(0 13), Rules plane
13:01:2xZ  positioning_data.json SERVED             <- READ industry_group HERE
13:30:00Z  mdpf-scheduled-floor -> gold             <- TP1AE-AC1 scores HERE
13:50:50Z  portal publisher -> platinum/mdpf/       <- ANDREW'S CARDS HERE, not 13:30
```

### THE TRIGGER ITSELF, MEASURED (`2.0.0_SA_COO~Z`, 12:3xZ) -- named so a successor need not hunt it
```
etf-positioning-producer-daily   cron(0 13 * * ? *)   ENABLED     <- THE 13:00Z FIRE. Real and armed.
etfs-netassets-daily             cron(0 22 * * ? *)   ENABLED     <- silver's producer
```
**"The 13:00Z fire" had been carried all night as an assumption at this seat; it is now read off the
schedule plane.** ⚠ **BOTH PLANES WERE CENSUSED** -- `events list-rules` structurally CANNOT see
`scheduler list-schedules` entries, and a one-plane sweep would have reported a confident absence if
this rule had lived in the other. (Scheduler holds `wsd-49f-partner-held-etf-pull-daily`,
`etfs-reports-monthly-run` -- neither is this.)
⭐ **AND IT INDEPENDENTLY CONFIRMS THE as_of STABILITY ARGUMENT.** The claim "silver cannot move
before 13:00Z, so `as_of` stays 2026-08-27" was previously taken from a CODE COMMENT. The 22:00Z cron
is a DIFFERENT INSTRUMENT reading the same fact -- corroboration, not repetition.
⛔ **IF NOTHING LANDS BY ~13:05Z, CHECK `etf-positioning-producer-daily` FIRST** -- whether it fired
at all -- before concluding anything about the field, the join, or the vendor.

### ⭐ THE FALSIFIABLE 13:00Z PREDICTION -- SCORE AGAINST THIS (`1.0.0_SA_CTO~Z` msg 13125, hardened here)

`1.0.0_SA_CTO~Z` retracted its own "expect ~7 ABSENT_FROM_SOURCE": **6 of the 7 are FUNDS, and
`industry_group_of()` tests non-equity FIRST, so they never reach the blank branch.** The real
prediction is exact:
```
ABSENT_FROM_SOURCE          EXACTLY 1, and it should be ABT
NOT_APPLICABLE_NON_EQUITY   == THE RUN'S OWN Fixed-Income count
OBSERVED / SECURITY_NOT_IN_CHARACTERISTICS   the remainder -- ⛔ NO NUMBER CLAIMED, deliberately
```
⭐ **"EXPECT A NON-ZERO COUNT" IS NEARLY UNFALSIFIABLE; "EXACTLY 1, AND IT IS ABT" CAN BE WRONG.**
If either exact limb misses, that is a REAL SIGNAL, not noise -- which is why it is written before the
fire rather than rationalised after.

**HARDENED BY `2.0.0_SA_COO~Z` (12:2xZ) -- the prediction was measured at the WRONG as_of:**
`1.0.0_SA_CTO~Z` measured on the served artifact at `data_as_of 2026-08-26`. The 13:00Z run resolves
`as_of = 2026-08-27`. So both exact limbs were conditional on holdings that had not been checked.
```
ABT in silver/holdings/2026-08-27.parquet   PRESENT, count 1     <- the ACTUAL 13:00Z input
  neg control ZZZZ 0 | pos controls FXFXX 2, SALXX 2             <- the probe discriminates
>> THE "EXACTLY 1 = ABT" LIMB IS NOW MEASURED AT THE RIGHT as_of, NOT INFERRED FROM 08-26.
```
⛔ **BUT DO NOT SCORE `NOT_APPLICABLE_NON_EQUITY` AGAINST THE LITERAL 8.** The holdings set MOVED
between the two as_ofs -- **189 served rows at 08-26 vs 187 rows in the 08-27 silver partition** -- so
8 is an observation at a superseded vintage, not a constant. **A criterion pinned to a number the next
run legitimately changes files a FALSE FAIL.** Score it against the run's OWN Fixed-Income count.
⚠ **AND THIS SEAT DOES NOT COMPUTE THAT COUNT.** `asset_class` is derived inside the producer by
`classify(is_cash, gics, sentinel)`; re-deriving it here would re-run the producer's arithmetic under a
second author and call the agreement corroboration. **Read it out of the run.**

⚠ **THE SILVER KEY LAYOUT IS FLAT, NOT HIVE-PARTITIONED:** `silver/holdings/{date}.parquet`. A probe
at `silver/holdings/date=2026-08-27/` returns EMPTY -- **the third false-absence of this shape on this
TO today.** List the parent before converting any empty listing into an absence.

### ⭐ THE LAST LINK IN THE "EXACTLY 1" CHAIN IS CLOSED (`2.0.0_SA_COO~Z`, 12:3xZ)

`1.0.0_SA_CTO~Z` (13131) named the one link nobody had closed: **"ABT -> ABSENT_FROM_SOURCE" presumes
ABT classifies EQUITY** -- branch 1 (non-equity) is tested first -- and its only evidence was the 08-26
served artifact, i.e. the wrong vintage again. **Closed here from the 08-27 INPUTS, so it needs no
served artifact and no run.**

⛔ **AND THE CHAIN AS STATED WAS INCOMPLETE: `classify()` IS NOT THE GATE.** `:1193` calls
`infer_is_cash(r.get("is_cash"), r.get("security_name"), gics)` FIRST, and its result is what reaches
`classify()`. Silver's `is_cash` for ABT is **`None`, not `False`** -- 73 of 187 rows are `None`
(`cash_basis: field-absent`) -- so the inference path runs and IT decides, not `classify` alone.
```
REPLAYED on silver/holdings/2026-08-27.parquet + chars 2026-08-27:
  ABT    DIVZ   is_cash None -> has_gics False, markers NONE      -> (False,False) -> (EQUITY, None)
  SALXX  DIVZ   is_cash None -> has_gics False, markers ['mmkt']  -> (True, True)  -> FI/UltraShort
  SALXX  IDVZ   is_cash None -> has_gics False, markers ['mmkt']  -> (True, True)  -> FI/UltraShort
  FXFXX  PFDE   is_cash TRUE ASSERTED -- silver wins, the name is never read       -> FI/UltraShort
  FXFXX  PFOE   is_cash TRUE ASSERTED -- silver wins, the name is never read       -> FI/UltraShort
>> ABT REACHES BRANCH 5. `ABSENT_FROM_SOURCE` = 1 STANDS, now traced through the REAL call chain
   at the REAL vintage rather than read off a superseded output.
```

### ⚠ TWO LATENT HAZARDS FOUND WHILE TRACING IT -- MEASURED, NOT LIVE, NOT CHASED

**(1) THE CASH-MARKER LIST IS COUPLED TO *WHICH NAME COLUMN* FEEDS IT, AND A SECOND ABBREVIATION
VOCABULARY SITS ONE COLUMN AWAY.**
```
silver.security_name  'STATE STREET INST U.S. GOVERNMENT MMKT ADMN CLASS'  -> matches 'mmkt'   ✓
chars.NAME            'STATE ST INST US GOV MM-ADM'                        -> matches NOTHING  ✗
```
`infer_is_cash` reads the SILVER name. **If it were ever re-pointed at the characteristics `NAME` --
the obvious "richer" source, and it is already in `hc` at the call site -- SALXX would silently return
`(Equity, None)` and a money-market position would land in `alloc_equity`.** That is precisely the
defect the 2026-08-25 `"mmkt"` addition was made to fix. `0.0.0_AB_MSTR~Z`'s BOUND on that comment says
the open class is ABBREVIATION; this is a concrete second abbreviation vocabulary within the same
function's reach. **FXFXX is not exposed -- silver ASSERTS `is_cash=True` for it, so its name is never
read. SALXX is exposed because silver declares unknown.**

**(2) A VENDOR REJECTION BREAKS THE INVARIANT THE CASH-INFERENCE SAFETY ARGUMENT RESTS ON.**
The `:922` comment argues the conjunction is safe because *"an operating company ALWAYS carries a GICS
sector; a money-market or sweep line never does."* **ABT is an operating company carrying NO GICS
sector** -- `__error__ "Unknown/Invalid Security"` strips every column. It lands in the cell the comment
calls very hard to construct, and is saved ONLY because `"abbott laboratories"` contains no cash marker.
⚠ **A rejected ticker whose issuer name happens to contain `treasury obligation`, `sweep` or
`liquidity fund` would be silently inferred as CASH.** Not live, no such row today. **Surfaced as
OBSERVATION / INERT -- the remedy is the canonical classifier already named as owed, not a marker edit.**

### `INGEST-TO6-AC3` -- ALL THREE LIMBS NOW MEASURED (`2.0.0_SA_COO~Z`, 12:1xZ)
```
(a) the landed characteristics gains the column   PASS  csv AND parquet, controls both directions
(b) run_manifest.json reads run_class: scheduled  PASS  bbg/2026-08-27/run_manifest.json -> "scheduled"
(c) field-exception counts are legible            PASS  field_exceptions = 5 populated classes
```
**HOW I KNOW IT WAS THE SCHEDULED RUN, which AC3 asks explicitly:** the manifest's own
`run_class: scheduled` and `as_of: 2026-08-27`, with object timestamps 11:06:33-37Z against the 11:00Z
cron. **Not inferred from the filename.**
⭐ **AND THE EXCEPTION DICT IS A WORKING INSTRUMENT, WHICH IS WHAT MAKES ITS SILENCE MEAN SOMETHING:**
it reports 5 exception classes (`FUND_EXPENSE_RATIO`, `FUND_TOTAL_ASSETS`,
`TOTAL_NUMBER_OF_HOLDINGS_IN_PORT`, `HB_OAS_EFF_DURTN` at 165 each; `CUR_MKT_CAP` at 2) --
and `GICS_INDUSTRY_GROUP_NAME` appears in NONE of them. **The new field returned clean, and that is a
negative from an instrument demonstrated to fire.**
- **THE SERVED ARTIFACT.** Source-populated is not gold-populated is not served. Only rung 3 settles it.
- `1.0.0_SA_CTO~Z` read `industry_group_of`, its call sites and the manifest line **only** -- not the
  rest of the 1,835-line file; and this seat read the resolver and the parquet schema, nothing else.

⛔ **AN UNCHANGED ARTIFACT AT ANY RUNG IS A FAIL, NOT AN INCONCLUSIVE. A read ERROR is neither -- name it.**
⛔ **NO AD-HOC GOLD RUN TO FORCE THIS.** The ~13:00Z scheduled fire is the acceptance; an ad-hoc write
lands a real artifact at the real key and destroys the discriminator.
⚠ **DISARMED != REMEDIATED: if no seat is present after 13:00Z the fire is unobserved until someone
returns. The artifacts persist; TIMELINESS is what is perishable.**

<proof_of_spec>
  <criterion id="TO8-AC1" cell_refs="INGEST-T4-1"/>
  <criterion id="TO8-AC2" cell_refs="INGEST-T4-1,INGEST-T5-1"/>
  <criterion id="TO8-AC3" cell_refs="INGEST-T4-1"/>
  <criterion id="TO8-AC6" cell_refs="INGEST-T4-1"/>
  <criterion id="TO8-AC4" cell_refs="INGEST-T4-1"/>
  <criterion id="TO8-AC5" cell_refs="INGEST-T5-1"/>
  <expected_criteria>TO8-AC1,TO8-AC2,TO8-AC3,TO8-AC4,TO8-AC5,TO8-AC6</expected_criteria>
  <!-- ⛔ instance_path ADDED 2026-08-28 15:2xZ by `2.0.0_SA_COO~Z` (issuer). `3.0.0_SA_CVO~Z`
       measured that this block declared NONE while its sibling TO-6 declares one at :586, so an
       executor picking this TO up was told WHAT to file and never WHERE. That is a MISSING
       INSTRUCTION, not a missing file, and it would have reproduced the absence for the next lane. -->
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_INGEST.TO-8_PROOF_OF_SPEC.json</instance_path>
  <!-- ⚠ CRITERION-ID DEFECT, RECORDED AND DELIBERATELY *NOT* FIXED HERE.
       This block's ids are `TO8-ACn` -- NOT firm-tokened -- while TO-6's are `INGEST-TO6-ACn`.
       The proof_of_spec boilerplate on this very face states the rule: ids are FIRM-TOKENED so they
       cannot collide across the three parallel ETFS lanes. THIS FACE VIOLATES THE RULE PRINTED ON
       ITSELF. LATENT, not live: a collision needs another lane to mint a bare `TO8-ACn`.
       ⛔ NOT RENAMED, and the reason is not timidity: a rename moves every REFERENCE to these ids
       (reports, messages, any filed instance), so it needs a citation census FIRST. Renaming ids
       under a certifier mid-queue would be the two-carrier divergence deliberately created.
       Owner: `2.0.0_SA_COO~Z` as issuer, as a separate act with its own census. -->
  <alignment_denominators>cells declared: 2 (INGEST-T4-1, INGEST-T5-1); criteria: 6. FORWARD — 6 of 6 criteria carry >=1 cell_ref. BACKWARD — 2 of 2 declared cells reachable (INGEST-T4-1 from AC1/AC2/AC3/AC4, INGEST-T5-1 from AC2/AC5). Unmapped 0; untraceable 0. NOTE: `INGEST-T4-1` was an existing CERTIFIED cell claimed by NO live TO — this TO claims it; it is not a new cut. The DATA half of `INGEST-T5-1` is `TO-6`'s and is not duplicated here.</alignment_denominators>
</proof_of_spec>
