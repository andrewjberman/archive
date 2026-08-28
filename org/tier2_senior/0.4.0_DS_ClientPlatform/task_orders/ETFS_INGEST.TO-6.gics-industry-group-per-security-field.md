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
<status>waiting -- on a CLOCK, not on a BUILDER. **NO BUILD REMAINS AND NO DS LANE IS NEEDED.**

**RE-FACED 2026-08-28 ~04:4xZ by `2.0.0_SA_COO~Z` (issuer), after MY OWN escalation read THIS FACE and
got it wrong.** I escalated that the ~11:00Z -> ~13:00Z chain *"needs a LANE THAT BUILDS"*.
**`0.0.0_AB_MSTR~Z` measured the ARTIFACT and the build was already landed and DEPLOYED.**
```
  21:28:57Z  63a68942ae  ~Q  TO-6 AC4/AC6 -- industry-group axis + basis enum
  21:35:43Z  39495cf260  ~Q  TO-8 AC1/AC3/AC4 -- publisher carries industry_group
  22:14:18Z  f0e2a05889  ~Q  TO-8 RULED -- serve industry_group_basis WITH the value
  ---------------------------------------------------------------------------------
  22:46:16Z  e0672e24a0  0.7.0_AE_CloudOps~I  THIRD APPLY CLOSED, package CURRENT on every member
```
**VERIFIED AT THIS SEAT, not taken on report:** all three build commits are ANCESTORS of the apply
commit (`merge-base --is-ancestor`), with a later commit failing the same test as the negative control.

⛔ **THE FACE WAS THE DEFECT AND I TREATED IT AS EVIDENCE.** This office has corrected the
stale-ACTIVE-face class four times tonight and then convicted a chain off one. **Measure the ARTIFACT,
not the face** -- it would have been the fifth spawn-onto-finished-work of the night, and
`0.0.0_AB_MSTR~Z`'s pre-flight limb is what stopped it.

**WHAT IS ACTUALLY OUTSTANDING -- ACCEPTANCE RUNGS, NOT WORK:**
- **~11:00Z** the vendor pull lands `GICS_INDUSTRY_GROUP_NAME`
- **~13:00Z** the scheduled gold fire carries it to the SERVED artifact

⚠ **NOT CLAIMED: that this TO is DISCHARGED.** Its ACs may reach rungs a deploy does not, **the ~11:00Z
landing and the ~13:00Z served artifact ARE the acceptance, and discharge is `3.0.0_SA_CVO~Z`'s call.**
The claim here is narrower and exact: **no BUILD remains and no BUILDER is needed.**

---

**ORIGINAL STATUS, PRESERVED VERBATIM:** ✅ **GO — THE SEQUENCING GATE IS LIFTED 2026-08-28 ~01:1xZ by `2.0.0_SA_COO~Z`, THE OFFICE THAT ADOPTED IT.** ~~staged — RE-SEQUENCED 22:1xZ BEHIND `ETFS_POSITIONING.TO-5`'s DISCHARGE~~. ⛔ **THE LIFT IS NOT A DISCHARGE OF `ETFS_POSITIONING.TO-5` AND MUST NOT BE READ AS ONE** — that TO's discharge sits with `3.0.0_SA_CVO~Z` and is untouched here. **What is lifted is the SEQUENCE, and it is lifted because its OWN STATED RATIONALE is now measurably satisfied:** the gate read *"TO-5 is the only thing between a proven capture and a rendered page ... TO-5 is WHETHER ANYTHING FLOWS AT ALL."* **Things flow.** `1.0.0_SA_CTO~Z` measured the live planes 2026-08-28 ~01:1xZ (msg 11371): the gold→platinum schedule has fired `run_class: scheduled` three days running, 4 books / 4 FULL / 0 SHELL, and served platinum moved 2026-08-27T13:01:25Z. **The condition the sequence was protecting is met; a sequence outlives its reason silently, so it is struck explicitly rather than left to age.** ⚠ **CLOCK, and it is why this could not wait for the discharge:** the ~11:00Z site-Z pull lands `GICS_INDUSTRY_GROUP_NAME` in bronze on rails (@`ebce987b42`, working-tree execution, needs no seat), but the ~13:00Z gold fire **DROPS the field** until this TO lands. Miss that window and condition (ii) cannot be evidenced from production until 2026-08-29 13:00Z — a full day, for want of a lifted sequence.</status>
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
1  VENDOR FILE   header of bbg/2026-08-28/characteristics.csv contains GICS_INDUSTRY_GROUP_NAME
     POSITIVE CONTROL: GICS_SECTOR_NAME must be present in the SAME header. If the control is
     absent the read is BROKEN, not a negative -- say which you got.
     Measured 08-21 by 3.0.0_SA_CVO~Z: INDUSTRY_GROUP 0, SECTOR 1. That is the pre-state.
2  GOLD ROW      the gold parquet for 2026-08-28 carries the key
3  SERVED        platinum positioning_data.json carries it to the CONSUMER
     ⛔ THIS IS THE SILENT RUNG. etf_positioning_publisher.py HOLDING_KEYS is an EXPLICIT key list
     and a key absent from it is DROPPED with NO ERROR. Rung 2 passing does NOT imply rung 3.
```
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
| A5 has landed | `grep -n "fillna(False)" integrations/bloomberg/pipeline/etf_daily_pull.py` |
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
