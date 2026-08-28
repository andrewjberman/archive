# TO ETFS_INGEST.TO-6 — add `GICS_INDUSTRY_GROUP_NAME` to the per-security pull and carry it to the gold row (`INGEST-T5-1` data half, `INGEST-T3-6`)

<task_order id="ETFS_INGEST.TO-6" project="ETFS_INGEST">
<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED) — the DATA half of `INGEST-T5-1` (the finer field), and `INGEST-T3-6` (the gold row's Rule-24 act, a SECOND schema act at a DIFFERENT GRAIN from T2's).</decomp_ref>
<certification>✅ CERTIFIED, `3.0.0_SA_CVO~Z` @422bdb431b, bound to `@fcdf042972`. Reduced-cohort; premise-oracle verification a SAMPLE not a census.</certification>
<issued_to>`0.4.0_DS_ClientPlatform~Q` — **RE-ADDRESSED 2026-08-28 ~01:1xZ by `2.0.0_SA_COO~Z` (issuer).** ~~`0.4.0_DS_ClientPlatform~P`~~, whose session died in the 00:3xZ fabric kill. `~Q` is LIVE, warm, and free: its own project (`D1_NAMEDISCOVERY`) is round-1 COMPLETE and CERTIFIED, it refused a false re-dispatch rather than re-executing accepted work (msg 11408), and it asked to be re-pointed rather than re-cut. **Rule 27 holds — one instance, one project: `~Q` moves to `ETFS_INGEST` holding nothing else.** Chosen over re-spawning `~P` because the ~13:00Z clock in `status` prices spawn latency, and a re-seated `~P` would start as cold as `~Q`. **`ETFS_INGEST.TO-7` remains `~P`'s and is NOT re-addressed by this edit.**</issued_to>

> ⛔ **RE-ADDRESSED `~Z` -> `~P` 2026-08-27 ~17:2xZ by `2.0.0_SA_COO~Z`. THE LANE LETTER WAS REUSED
> ACROSS PROJECTS AND THAT CREATED A LATENT RULE 27 COLLISION.** This TO was seated to
> `0.4.0_DS_ClientPlatform~Z` on 2026-08-24 as an **ETFS_INGEST** lane. On 2026-08-27 `~Z` was
> respawned as a **D1_CATVIEWS** lane (`0.0.0_AB_MSTR~Z` msg 9331, which scopes `~Z` to *"D1_CATVIEWS
> ONLY"* and assigns **TO-6 + TO-7 to `~P`**). Until this edit, `~Z` held **two projects** —
> D1_CATVIEWS (TO-R1-DS, TO-F3-DS) and ETFS_INGEST (this TO). MSTR's assignment and this TO's face
> disagreed; **the face is now corrected to MSTR's stated assignment. `~P` is the ETFS_INGEST lane.**
>
> ⛔ **THE MECHANISM, because it will recur: A LANE LETTER FREE ON *PROCESS* TRUTH CAN STILL BE
> ENCUMBERED BY AN *OPEN TO*.** The spawn checked liveness (no running process carrying `~Z`) and
> that check was correct and insufficient — **a dead seat's open TOs do not die with it.** Nothing
> refuses at spawn time: `[gate2]`'s seating-frame indexes exactly this ("open-TO holdings across
> seat instances") but it runs on **commit**, so it can only catch the collision when a TO is
> *written*, never when a lane is *spawned*. **Two different clocks, and the spawn is the earlier
> one.** Surfaced to `0.0.0_AB_MSTR~Z`; not a criticism of the spawn, which acted on the truth
> available to it.
>
> **THE ORIGINAL SEATING NOTE IS PRESERVED BECAUSE IT RECORDS SOMETHING WORTH KEEPING**, and it is
> about the *former* occupant, not `~P`: the `~Z` seat *"requested this TO rather than starting on a
> sovereign word that named their cell. That was right."* `~P` inherits the TO, not that credit.
<executor_class>DS-class</executor_class>
<seating_trigger>SEATED. ⛔ **BUT THE TOUCH IS SEQUENCED BY `1.0.0_SA_CTO~Z`, NOT BY ME — see below. DO NOT EDIT `etf_daily_pull.py` UNTIL THEY SEQUENCE IT.**</seating_trigger>
<placement>**SITE Z** (Rule 26). ⛔ **CORRECTED 2026-08-27 ~17:5xZ by `2.0.0_SA_COO~Z` — THE ISSUING OFFICE, AND THIS WAS OUR DEFECT.**

**THE FILE THIS TO DIRECTS YOU TO EDIT IS `integrations/bloomberg/pipeline/etf_daily_pull.py`, WHICH IS `ANY_EXEC_OR_AE` (`.owned-paths.yaml:1302`). NO DS-CLASS SEAT CAN COMMIT IT.**

The original placement line read: *"`data/**` and the etfs-pipeline Lambda are both yours to author (`.owned-paths.yaml:1661`, `POD4_OR_AE`); AE deploys."* **Every word of that is TRUE and NONE of it is about the file the TO actually assigns.** `etf_daily_pull.py` is neither `data/**` nor the etfs-pipeline Lambda. **A placement block that cites a real rule for the wrong paths reads as though it had been checked** — that is what made it survive: it is not vague, it is confidently precise about paths this TO does not touch.

⛔ **AND THE COST IS NOT MERELY A REFUSAL, BECAUSE OF WHAT THIS FILE IS.** `etf_daily_pull.py` is `RUNNER_TREE_IS_PRODUCTION` — **saving IS the deploy.** So the sequence is: the seat edits (production changes), then `safe-commit` refuses on lane. **THE GATE FIRES ONE STEP TOO LATE FOR THIS FILE CLASS**, and the seat is left holding a change that is **LIVE AND UNRECORDED** — the worst of the three states, and one no gate in the chain can prevent for a save-is-deploy path. `0.4.0_DS_ClientPlatform~P` hit exactly this at ~17:4xZ, did NOT reach for `GIT_COMMIT_AUTHOR_OVERRIDE` (correctly — a seat granting itself a lane it is not in is the SoD violation the rule's own note forbids), did NOT `--force` (which does not bypass a lane refusal anyway), did NOT `git stash` (the shared-worktree guard blocked it, correctly, with two peers holding dirty files), and surfaced it loudly instead. **That was right on all four counts.**

**RESOLVED:** `1.0.0_SA_CTO~Z` — an EXEC, and therefore in-lane — committed the verified edit at **`ebce987b42`**. I confirmed at source rather than from the report: the token is present (2 occurrences, negative control `zzz_no_such_token_9999` = 0) and the working tree is clean for that path.

**CORRECT PLACEMENT FOR THIS TO:** DS authors and verifies; **an EXEC or AE commits `integrations/**`.** Do not assume a `data/**`/Lambda grant extends to it.

⚠ **GENERALISE BEFORE THE NEXT TO:** a placement block must name **the lane of the FILE THE TO DIRECTS**, not the lane of the project's usual paths. This TO's subject sits outside its project's normal tree, and the placement line was written from the project, not from the file.</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-24T21:5xZ</issued>
<status>pending -- ⛔⛔ **NOT CERTIFIABLE: NO PROOF-OF-SPEC INSTANCE EXISTS. THIS NEEDS AN EXECUTOR, NOT A CERTIFIER.** Measured 15:2xZ by `3.0.0_SA_CVO~Z` and re-measured at this seat: this TO DECLARES an `instance_path` of `.../ETFS_INGEST.TO-6_PROOF_OF_SPEC.json` **AND THAT FILE DOES NOT EXIST ON DISK**. **POSITIVE CONTROL: the same probe finds `ETFS_INGEST.TO-5`'s instance present on disk, so the absence is a MEASUREMENT and not a broken read.**

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

<priority>P1 — it is the one input `ETFS_INGEST.TO-5`'s AC4 is blocked on, and AC4 is condition (ii).</priority>
<authority>**Andrew-direct ~21:47Z, VERBATIM:** *"Regarding the GICS, the way that needs to work is basically pulling all Opal ETF consitutent securities via the provider docs, then those securities get added to the ETFS bloomberg pull and we get that data from bloomberg itself. That way we dont need to do the constituent weighting process in bloomberg, we just get all the constituent data and we manage the calculations server side in our pipeline"* (record via `0.0.0_AB_MSTR~Z` msg 5199). Plus **C3 RULED** ~20:0xZ. CLAUDE.md Rule 13, Rule 24 (the gold row is a value-enum act at authoring).</authority>
</task_order>

## WHY THIS IS ADDITIVE AND NOT A NEW MECHANISM

**His 21:47Z word describes the shape `etf_daily_pull.py` ALREADY HAS:** it derives its universe from
`silver/holdings` — the **issuer** roster — then pulls per-security CHAR fields from Bloomberg for
that universe. `GICS_SECTOR_NAME` is **already in that list**. So this TO adds **one more field to a
per-security call that already runs**, and the aggregate is computed **by us, server-side, from
issuer weights × per-security GICS** — which is exactly what he said.

**Nothing architectural is being reversed.** What he ruled OUT is asking Bloomberg to enumerate or
weight constituents (the BQL path he already closed). What he ruled IN is the split we already have.

## ⛔ THE SEQUENCING IS NOT MINE AND I AM NOT SETTING IT

`etf_daily_pull.py` is **RUNNER_TREE_IS_PRODUCTION — saving the file IS the deploy**, no apply, no
review window. Three things want to touch it:

| who | what | status |
|---|---|---|
| `0.0.0_AB_MSTR~Z` | the **A5 one-expression** null-tolerance fix | ✅ **LANDED 22:0xZ and EXERCISED on the real 187-row partition (166 constituents derived, no raise)** |
| **you, this TO** | the additive CHAR field (locate by content, NOT `:141` — A5 moved it) | ⛔ **CTO~Z HAS RULED: A5 FIRST, GICS SECOND. A5 has LANDED, so your slot is OPEN** |
| you, later | `INGEST-INV-3` — derive `FUNDS` from the config instead of restating it | **stays on A2's trigger** |

⛔ **TWO HANDS ON ONE PRODUCTION-ON-SAVE FILE IS THE HAZARD, NOT THE EDIT.** `1.0.0_SA_CTO~Z` holds
A2/A5 and sequences this. **Ask them before you touch the file; do not infer a slot from A5 having
landed.** MSTR~Z said the same and was right to say it is not theirs to set either.

## ⚠ A LIVE SOVEREIGN QUESTION SITS BESIDE THIS — AND IT DOES NOT BLOCK YOU

At the time of writing, Andrew is being asked (via CTO~Z) to confirm **GICS as the SERVED vocabulary
with Bloomberg's HB labels as a cross-check** — because three seats measured that the HB vocabulary
has **zero per-security members** and could only be served by taking Bloomberg's own fund-level
weighting, the thing his 21:47Z word says we do not need.

**THIS TO IS SAFE UNDER EITHER ANSWER**, which is why it is cut now rather than held: the finer GICS
field is required to render the side-by-side comparison **whichever vocabulary he ultimately picks**.
⛔ **What his answer WOULD change is `INGEST-T3-6`'s gold-row vocabulary act — so if he rules before
you reach that half, use his ruling and tell me.** Do not pre-empt it.

## Acceptance criteria

| id | criterion | cell_refs | grounding |
|---|---|---|---|
| **`INGEST-TO6-AC1`** | `GICS_INDUSTRY_GROUP_NAME` added to the **per-security CHAR field list** — ⛔ **LOCATE IT BY CONTENT (the `CHAR` list containing `GICS_SECTOR_NAME`), NOT BY LINE NUMBER.** *(This criterion originally said `:141`; A5 shifted the file and that number is now wrong. See the citation note below.)* **ONE field, nothing adjacent** — `INGEST-INV-3` stays on A2's trigger even though it is in the same file and the same hand | `INGEST-T5-1` | **SOURCE** |
| **`INGEST-TO6-AC2`** | ⛔ **CTO~Z's sequencing word is CITED in your report before the edit** — who else touched the file, in what order, and where your save sits. **Saving is deploying** | `INGEST-T5-1` | **SOURCE** |
| **`INGEST-TO6-AC3`** | ⛔ **EXERCISED ON A SCHEDULED FIRE, not an ad-hoc run.** The landed `bbg/{as-of}/characteristics.csv` gains the column, `run_manifest.json` reads `run_class: scheduled`, and the field-exception counts are legible. **Report which run you read and how you know it was the scheduled one** | `INGEST-T5-1` | **EXERCISED** |
| **`INGEST-TO6-AC4`** | The **gold holding row** carries the field, as a **Rule 24 authoring act** with its four-postulate record — ⛔ **a SECOND schema act at a DIFFERENT GRAIN from T2's row, and the two MAY NOT SHARE AN AXIS.** Include the token-hygiene census (`comp-find -i`, denominator printed) | `INGEST-T3-6` | **SOURCE** |
| **`INGEST-TO6-AC5`** | ⛔ **RE-CHECK THE OVERLAP AT THIS EDIT — this is the hand-off `ETFS_INGEST.TO-5` AC5 named you for, by serial.** `0.4.0_DE_ClientPlatform~Z` measured that `characteristics.csv` carries **`TOTAL_NUMBER_OF_HOLDINGS_IN_PORT` but NOT `FUND_PCT_TOP_TEN_HOLD`** — so the "two fast-moving fields overlap" premise is **HALF TRUE**, and the second is **SOLE-SOURCED** from the constituents leg. *(I relayed that premise into a TO without measuring it; it is one of two relay defects of mine this round.)* **State both fields' post-edit sourcing** | `INGEST-T5-1` | **DATA** |

## AMENDMENT (22:0xZ) -- AC6 ADDED BY CTO~Z's RULING. Tonight's successful capture ARMED the thing your aggregate will consume.

**Measured independently at three seats on `silver/holdings/2026-08-24.parquet` (187 rows):**
`is_cash` -> **False 110 - None 73 - True 4**. **`SALXX` (STATE STREET INSTL U.S. GOVERNMENT MMKT -- the CASH SLEEVE) is in DIVZ at weight 0.58% and IDVZ at 0.89%, `is_cash=None`, and A5 admitted it into the 166-constituent Bloomberg universe.**

⛔ **A5 IS CORRECT AND IS NOT BEING REVISITED.** Declared-unknown -> INCLUDE is the conservative direction: carry the row forward VISIBLY rather than drop it silently. Had it defaulted the other way the cash sleeve would have vanished without trace and surfaced in a served number next month. **The inclusion is the safety net WORKING.**

> **THE DEFECT IS ONE LAYER UP: the TrueShares silver parser populates `is_cash` for ZERO of its 73 rows.** 39% of the partition is null on the field the downstream filter keys to, while Pathfinder's 114 rows carry it. **That asymmetry is the finding.**

**It is OBSERVATION and INERT today** -- nothing breaks at 07:00; `SALXX US Equity` returns sparse attributes, not an error. **It becomes ARMED ON A NAMED EVENT: the first served aggregate computed from these weights -- which is YOUR cell.** That is why it is an acceptance criterion here and not a floating channel item.

| id | criterion | cell_refs | grounding |
|---|---|---|---|
| **`INGEST-TO6-AC6`** | ⛔ **THE AGGREGATE STATES ITS OWN COVERAGE AND ITS OWN DENOMINATOR.** (1) Print **how many of N constituents carried a GICS value and what WEIGHT they represent** -- *a sector split that does not print its own coverage is the exact class this estate legislates against.* (2) **Cash/sleeve rows are classified EXPLICITLY, never by null-inheritance** -- either silver populates `is_cash` for TrueShares, or the aggregate DECLARES its treatment of a null-classification row. ⛔ **WHAT IS PROHIBITED IS A NULL QUIETLY BECOMING A SECTOR.** (3) **Issuer weights DO NOT SUM TO 100** -- measured on tonight's real bronze, **DIVZ 99.80%, IDVZ 99.51%** -- so the rollup carries a residual BEFORE any classification gap is added. **State which denominator you normalise to. Nobody discovers this from the served number.** | `INGEST-T3-6` | **DATA + EXERCISED** |

⛔ **AND THE SILVER `is_cash` GAP IS A SEPARATE CELL -- DO NOT FOLD IT IN AND DO NOT FIX IT IN PASSING.** Your file here is `etf_daily_pull.py`; that gap lives in the silver parser. **Surface it and I will cut it.** *One variable at a time is the entire reason for the A5-first ordering.*

⚠ **AND A CITATION CORRECTION THAT AFFECTS THIS TO: `etf_daily_pull.py:141` WAS MEASURED PRE-EDIT AND IS NOW WRONG** -- A5 shifted the file. **Re-locate by CONTENT (`GICS_SECTOR_NAME` in the `CHAR` list), never by the line number in AC1 or in the oracle table.** A line citation without a vintage is not a citation, and mine had a vintage I did not state.


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
  <!-- POSITIONAL invocation, no flag; CHECK THE RC not the output string; take it WITHOUT a pipe.
       The `firm` enum still has no ETFS value — enter FABRIC and DECLARE it, as you did on TO-2/TO-3.
       Routed to CTO~Z as gate owner; neither of us edits a gate. -->
  <criterion id="INGEST-TO6-AC1" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO6-AC2" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO6-AC3" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO6-AC4" cell_refs="INGEST-T3-6"/>
  <criterion id="INGEST-TO6-AC5" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO6-AC6" cell_refs="INGEST-T3-6"/>
  <expected_criteria>INGEST-TO6-AC1,INGEST-TO6-AC2,INGEST-TO6-AC3,INGEST-TO6-AC4,INGEST-TO6-AC5,INGEST-TO6-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_INGEST.TO-6_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Premise oracles — run at pickup

| premise | the read |
|---|---|
| the field is absent today | `head -1` the landed `bbg/{as-of}/characteristics.csv` → **11 columns, no `GICS_INDUSTRY_GROUP_NAME`**; ⛔ **positive control `GICS_SECTOR_NAME` MUST be present** or your read is broken, not the field absent |
| the CHAR list is locatable **BY CONTENT** (its line number has already moved once tonight) | `grep -n "GICS_SECTOR_NAME" integrations/bloomberg/pipeline/etf_daily_pull.py` |
| A5 has landed | ~~`grep -n "fillna(False)" ...`~~ ⛔ **THIS ORACLE IS BROKEN AND IT FAILS IN THE DIRECTION THAT STOPS WORK. RE-CUT 2026-08-28 ~19:3xZ by `2.0.0_SA_COO~Z` (issuer) on `0.4.0_DS_ClientPlatform~Q`'s report.** It returns a CLEAN ZERO while A5 **is landed** — so a seat reads "the premise is false", stops, and investigates a non-problem. ⚠ **AND THE ROW DIRECTLY ABOVE THIS ONE ALREADY SAYS WHY:** *"locatable BY CONTENT — its line number has already moved once tonight."* **I wrote that warning and then wrote a brittle literal-string oracle in the next row.** **AS RE-CUT:** locate the A5 behaviour BY CONTENT and **carry a POSITIVE CONTROL** — read the boolean-coercion site in `etf_daily_pull.py` and show a known-present neighbouring token resolving in the same read. ⛔ **A zero from this row is NOT an absence verdict until the positive control fires**; an out-of-corpus read and a true absence are byte-identical here. |
| the universe derives from the issuer roster | `sed -n '78,92p' integrations/bloomberg/pipeline/etf_daily_pull.py` — this is the half of his word that already exists |

## Standing constraints

- **The file is production-on-save.** One field. Nothing adjacent. **`INV-3` waits for A2.**
- **No alarm, no monitor.** The manifest and the log are the record.
- **Commit to your lane; do NOT push.** Report per-commit push state, as you did on TO-3 — **that
  discipline caught a difference two of your three commits had.**
- **Read the number, then write the sentence.**
- **Surprise channel:** `org/surprise_channel/ETFS_INGEST/` (`3.0.0_SA_CVO~Z`), coordinate `-Z-S{n}`.
  Mid-round the spec is FROZEN — route, do not adjudicate.
- **Status moves with the act, by you, same turn.**
