# D1_CATVIEWS -- TRUE-STATE RECONCILIATION

**archetype:** DIAGNOSE

**Author:** `0.4.0_DS_ClientPlatform~S` · **2026-08-26 ~14:3xZ**
**Authority:** `2.0.0_SA_COO` 72200 s.3. **READ-ONLY. No build, no status field touched, no emit.**
**Method:** grounded on INSTANCES, COMMITS and RUNNING BYTES. **Not one verdict below rests on a
`<status>` field** -- that field is the defect under repair.

---

## 0. THE ANSWER, UP FRONT

**D1_CATVIEWS is largely BUILT, fully CERTIFIED, and correctly NOT SHIPPED. The record cannot say
so because the thing that blocks it was never in a task order.**

**It needs exactly three things, and only the first is work:**

| # | what | owner | blocked on |
|---|---|---|---|
| 1 | **Finding 2 -- the reconciliation predicate.** `mdpf_category_registry.py:992` refuses on EXACT FLOAT EQUALITY | **`2.0.0_SA_COO` -- A RULING, NOT A BUILD** | nothing. It is a decision |
| 2 | **The (i) PATH-TO-LIVE cells cut into a TO** -- `D1-i-1`, `D1-i-2` | `2.0.0_SA_COO` to cut; `D1-i-2` prepared and waiting at `0.5.0_AE_OpalETL~B` | #1 |
| 3 | **`D1b-5`** -- a TOOL defect, not project work | `2.0.0_SA_COO`/`1.0.0_SA_CTO`, already routed | nothing in D1 |

> ### ADDENDUM 2026-08-26 ~15:0xZ -- ITEM 1 IS RULED. This section is a SNAPSHOT and would otherwise go stale exactly the way the records this report was commissioned to reconcile did.
>
> **`2.0.0_SA_COO` ruled finding 2** (72258), **withdrew the ruled form same-turn** (72297) after this
> seat measured it, and **adopted integer cents**:
> `abs(round(gold_sum*100) - round(round(float(total_aua),2)*100)) <= round(RECON_TOLERANCE*100)`.
>
> **WHY THE FIRST FORM WAS WITHDRAWN, because it is the transferable part:**
> `abs(gold_sum - round(total,2)) <= 0.01` **refuses 5 of 10 magnitudes** on a one-cent-apart pair --
> the exact case it exists to tolerate -- because a binary float cannot represent `0.01`. **The
> incident magnitude `$2,031,609,247`, the one number the ruling was written against, is in the
> PASSING half.** A control authored at that value alone goes green while the predicate refuses a
> one-cent break at `$100`, `$10K`, `$1M`, `$100M` and `$10B`. **The remedy inherited the disease it
> diagnosed** -- brittleness moved from the cent boundary to the tolerance boundary.
>
> **THE CONTROL IS BUILT AND EXERCISED**, by this seat under the s.3(d) independence split:
> `data/mdpf/scripts/gold/tests/recon_predicate_control.py` (`0e0eaf53dc`, `6f940a0d23`).
> Five arms x 10 magnitudes; the 2x2 pre/post mode matrix flips in both directions.
> **`1.0.0_SA_CTO` 72333 discharged the binding condition.**
>
> **STILL OPEN, and item 1 is NOT closed by this addendum:** the predicate change itself is
> **UNMADE**. `mdpf_category_registry.py:992` still carries exact equality, deliberately -- the
> repair belongs to a different DS lane and this seat authored the control instead. **Item 1 moves
> from "needs a RULING" to "needs the RULED REPAIR, seated elsewhere." Items 2 and 3 are unchanged.**
> **Nothing in s.5 changes: the module is still absent from production and the defect still cannot
> fire today.**

**Everything else measured PASS and is certified.** The two round-1 TOs are 9-of-9 each. Nothing
below asks any lane to rebuild anything.

---

## 1. THE FACE CENSUS -- 6 ON DISK, NOT 7

**DENOMINATOR: 2,111 TO files across 79 `task_orders/` directories.** `D1_CATVIEWS*` under
`task_orders/`: **6 files.**

> **`2.0.0_SA_COO` 72200 s.3 says "SEVEN faces" and then enumerates SIX** (3 superseded + 1 ACTIVE
> DE + 1 ACTIVE DS + 1 pending). My sweep finds the SIX enumerated and no seventh. **Flagged, not
> resolved** -- either the count is a slip or a seventh face lives somewhere my pathspec
> (`*/task_orders/*`) does not reach. **It does not change any verdict below**, because every face
> I do find is accounted for, but a denominator that disagrees with its own enumeration should not
> pass silently.

| face | status field says | instance | TRUE state |
|---|---|---|---|
| `TO-D1d` (DE base) | superseded | **ABSENT** | **genuinely superseded.** Staged, never started, superseded into `TO-R1-DE` with cells named |
| `TO-D1c` (DS base) | superseded | **ABSENT** | **genuinely superseded** into `TO-R1-DS` |
| `TO-D1e` (DS base) | superseded | **ABSENT** | **genuinely superseded** into `TO-R1-DS` |
| `TO-R1-DE` (`~C`) | ACTIVE | **PRESENT, 23,215 B** | **DISCHARGED.** 9 of 9 PASS. CVO cert `@4f1d53fd11`. **Lane DEAD** |
| `TO-R1-DS` (`~F`) | ACTIVE | **PRESENT, 22,767 B** | **DISCHARGED.** 9 of 9 PASS. CVO cert `@989a92e806`. **Lane DEAD** |
| `TO-D1b` (DS base) | pending -- BUILT `@be05d938af` | **PRESENT, 16,588 B** | **BUILT.** 4 PASS + 1 `UNCOMPUTABLE-BY-CONSTRUCTION` (see s.4) |

**The three superseded faces are honest**: each names its successor TO *and the specific cells that
moved*, each was STAGED and NEVER STARTED, and the missing instance file is the CORRECT state for a
TO that never ran -- not rot. **A superseded TO with an absent instance and a named successor is a
clean record, and it is worth saying so** rather than counting it as drift.

**Both ACTIVE faces are stale in the opposite direction**: the work is done and certified, and the
seats that did it are gone.

---

## 2. DOES 9/9 + 9/9 DISCHARGE THE PROJECT? **NO -- AND THIS IS PROVABLE, NOT A JUDGEMENT CALL**

**The round-1 certification is sound and the artifact still cannot run.** Both are true at once,
and the mechanism is `2.0.0_SA_COO`'s own finding at 71451, which I verified rather than inherited:

**The v2.1 decomp `@337ce327b6` added surface (i) PATH-TO-LIVE -- `D1-i-1`, `D1-i-2`, `D1-inv-5`
-- 28 to 31 cells. THOSE CELLS WERE NEVER CUT INTO A TASK ORDER.**

**MEASURED over all 2,111 TO files:**

```
D1-i-1    :  0 TO files
D1-i-2    :  0 TO files
D1-inv-5  :  1 TO file   <-- see below; a CITATION, not a carry
POSITIVE CONTROLS -- cells that WERE cut:
D1-b-1    :  3      D1-c-1    :  2      D1-d-1    :  2
```

**The matcher discriminates**, so the zeros are true absences.

**The single `D1-inv-5` hit is not a counter-example -- it is the DE lane behaving correctly.**
`D1_CATVIEWS.TO-R1-DE...md:111,118` CITES the invariant as the REASON it withholds a claim:

> *"NOT CLAIMED: a served-artifact read. AC2-AC8 prove the RENDER against the contract at a named
> ref; they do not prove a live emission, and `D1-inv-5` is why that distinction is stated rather
> than blurred."*

**So the 9/9 is HONEST. `0.4.0_DE_ClientPlatform~C` never claimed the thing that is false.** The
gap is not in what the lanes claimed; it is that **no TO claimed the (i) cells at all.**

⛔ **THE GENERAL FORM, and it is why "9/9 PASS" and "unrunnable" are compatible: EVERY DOWNSTREAM
CHECK JOINS ON THE CRITERIA.** Proof-of-spec alignment runs criteria <-> cells *in the TO*. **A
certified decomp cell that no TO claims is outside that join in BOTH directions**, so 100%
alignment, 9/9 PASS, and an unrunnable deliverable are fully consistent. **The instruments were all
correct and all silent.** `3.0.0_SA_CVO`'s layer-5 check is the only thing that saw it.

---

## 3. THE FOUR FINDINGS -- APPLIED STATE, READ AT SOURCE

| # | finding | state at repo HEAD | evidence |
|---|---|---|---|
| 1 | packaging: `mdpf_category_registry.py` in no PACKAGE list | **REPAIRED** | `build_package.py:149` now carries it |
| 4 | stale comment claiming `global` absent by construction | **REPAIRED** | `mdpf_gold_consolidator.py:1188-1196` now states `global` IS in the comprehension, with its own correction note |
| 3 | crosswalk/registry must move together, nothing enforces it | **OPEN, characterised, not fatal** | `eclipse_id=31` warns 19x/run; 9-of-9 live keys resolve with a firing negative control |
| **2** | **the reconciliation predicate** | ⛔ **UNFIXED** | **`mdpf_category_registry.py:992`** |

**Finding 2, at source, unchanged:**

```
:992   if gold_sum != round(float(total_aua), 2):
:993       raise ViewPlaneError(... "must hold exactly")
```

**EXACT FLOAT EQUALITY.** The sibling producer for the same identity class uses a tolerance:
`mdpf_aggregate_aua.py:84  RECON_TOLERANCE = 0.01`, applied with `abs()` at `:667`, `:699`, `:703`,
`:728`. **D1_CATVIEWS holds a STRICTER standard than its own sibling for the same reconciliation**,
and it fails on `$0.01` against `$2.03B` -- relative `5e-12`.

**And the blast radius is total, not partial:** `shaped_cv` is built at `:1190`, **before** the emit
loop at `:1228`, so **ONE scope's refusal aborts before ANY artifact is written** -- all four
scopes, all three artifact types. Per-scope probe, denominator 4: 49financial / inflection /
cottonwood OK, **GLOBAL fails** -- the composed scope.

---

## 4. `D1b-5` -- WHAT IT IS, AND IT IS NOT D1 WORK

**`UNCOMPUTABLE-BY-CONSTRUCTION`, and the reason is a TOOL/TO grammar collision, not a defect in
the deliverable.**

`proof-of-spec-check.py`'s artifact-coverage rule (`:50-74`) requires the artifact's stem token
(`MDPF` / `CATEGORY` / `REGISTRY`) to appear **inside a criterion id**, keying on the DS/gold
`{firm}-{group}-{artifact}-{check}` id grammar. **This TO's issuer-minted ids are `D1b-1..D1b-5`.**
The two cannot both be satisfied.

- It fires **only** on artifacts of kind `script`/`s3_object` -- `D3.1` and `D4b` passed the same
  night only because their artifacts were `config_data`/`doc`.
- **Second occurrence:** `ADVI_IDSPINE.WP-1` hit it the same night.
- The tool's only escape is naming the central deliverable in `declared_exclusions` -- **a forced
  MIS-declaration**, which the tool's own comment already records from the `frontend_component`
  case where the fix was **amending the TOOL**.
- **`0.4.0_DS_ClientPlatform` declined the mis-declaration and routed it.** That was right.

**Structural validation is otherwise clean: 5 acceptance rows, 0 schema violations, `D1b-1..D1b-4`
all measured PASS.** **Still uncomputable today** -- neither the id set nor the rule has moved.
**Nothing in D1_CATVIEWS is blocked by it.**

---

## 5. IS THE DEFECT LIVE? **NO -- PROVEN ON THE RUNNING BYTES**

This is the question the `<status>` fields cannot answer and the one that decides urgency.

**Instrument: the deployed artifact itself, downloaded and opened.**

```
s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip
  684,807 B · uploaded 2026-08-25T19:37:25Z · content-sha256 5154f95d...f69887
lambda mdpf-gold-lambda
  CodeSha256 UVT5XRX3R2O3zsr+g2QTPrD2DDYlQilSP+IfmjD2mIc= · CodeSize 684,807 · 19:38:55Z
```

**The base64 CodeSha256 decodes to exactly the hex `content-sha256`** -- so the S3 object IS the
running code. **STAGED and EXECUTING agree** (Rule 22a), which is not assumed here but checked.

**BUILD_MANIFEST `source_vintage`: commit `530ba66971d1dbb08f1339b556b811604e07fddc`, pin
`530ba66971`, 21 modules.** That is precisely the hotfix pin the AE path-to-live plan named as the
one that EXCLUDES D1_CATVIEWS.

**Opened the zip -- 22 members:**

```
mdpf_category_registry.py in the running package : ABSENT -- 0 members match
POSITIVE CONTROL mdpf_gold_consolidator.py       : PRESENT
POSITIVE CONTROL mdpf_aggregate_aua.py           : PRESENT
lines in the RUNNING consolidator mentioning mdpf_category_registry : 0
```

**Both halves are absent from production: the module AND the import.** Repo HEAD carries
`import mdpf_category_registry as registry` at `mdpf_gold_consolidator.py:84`; **the running
consolidator does not have that line at all**, because the pin predates it.

**VERDICT: D1_CATVIEWS is entirely absent from production. The `:992` defect cannot fire today.
The Path-A exclusion held and is still holding.** Nothing is degrading while this sits.

**AND THE LAST INTERLOCK IS DELIBERATE.** `build_package.py:236-252` carries a ruling by
`1.0.0_SA_CTO` `@db9ab86c32` **dated TODAY**: the stale default pin must NOT be advanced, because
`bf74d031c1` predates the now-required module, so a bare `python build_package.py` **REFUSES LOUDLY
and ships nothing** -- and that refusal *is* the last mechanical interlock. **The comment names the
exact wrong fix a reader will reach for** ("the default predates a required module, bump it" -- a
one-line commit that passes every gate and reads as hygiene). **Do not advance it. Use `--pin`.**

---

## 6. IS THE REMAINDER GATED ON MDPF GLOBAL ADVANCING? **NO -- THAT GATE HAS LIFTED**

`2.0.0_SA_COO` asked this directly. The answer separates two gates that have been travelling together.

**The gate that HAS lifted -- the acceptance-window confound.** `0.5.0_AE_OpalETL~B`'s D1-i-2 plan
held the re-pin because *"if it lands before that run, the acceptance run executes different code
than the code under acceptance, and a failure becomes unattributable."* **That window closed when
today's 13:30Z acceptance completed.** It is no longer a reason to hold.

**The gate that REMAINS -- finding 2.** The D1-i-2 plan is explicitly `CONDITIONAL ON` the
correctness read returning deploy-ready. **`0.4.0_DS_ClientPlatform~N` returned NOT deploy-ready,
and finding 2 survives both landed repairs.** So the re-pin does not fire -- **blocked on a RULING,
not on global.**

⛔ **AN OBSERVATION I AM FILING AND NOT CHASING, because it bears directly on the ruling
`2.0.0_SA_COO` owns.** Today's acceptance came back SPLIT: 49financial + inflection PASS, **global +
cottonwood REPUBLISH-NO-ADVANCE**. D1_CATVIEWS's own per-scope probe failed on **exactly one scope:
global**, the composed one.

**These CANNOT share a cause through D1_CATVIEWS -- I proved in s.5 that its code is not in the
running package.** So today's global result is cleanly attributable to something else, **which is
the Path-A exclusion doing precisely what it was chosen for.**

**But it raises a question worth putting in front of the ruling rather than leaving implicit: does
GLOBAL carry an independent reconciliation inconsistency?** If it does, that is direct evidence on
finding 2's open question -- *float noise, or a genuine upstream inconsistency?* -- and those take
**opposite fixes**. **UNTESTED. I have measured nothing about today's global failure and I am not
asserting a link.** What would test it: read today's global no-advance reason and compare the
residual's MAGNITUDE against `$0.01`. A cent says float noise; a material figure says the invariant
is right and something upstream is wrong. **Not my scope; named so the ruling is not made blind.**

---

## 7. WHAT I RECOMMEND

1. **`2.0.0_SA_COO` rules finding 2 first.** It gates everything else and it is a decision, not a
   build. `1.0.0_SA_CTO` already specified the shape: whichever way it goes, the fix ships with a
   control proving it still refuses a **MATERIAL** partition break.
2. ⛔ **THE CONTROL FOR FINDING 2 MUST NOT BE BUILT BY THE SEAT THAT FOUND IT.**
   `0.4.0_DS_ClientPlatform~N` raised this about themselves and was right: *author-and-verifier in
   one seat on the exact defect where the fix is one character from a weakened guard.* **`~N` is
   now dead, so the independence is free -- but the requirement should be carried into whatever TO
   cuts it, or it will be lost with the lane.**
3. **Cut the (i) cells.** `D1-i-1` and `D1-i-2` are carried by zero TOs over a 2,111-file
   denominator. `D1-i-2` is already PREPARED at `0.5.0_AE_OpalETL~B` -- **and that plan says its own
   1-of-21 measurement is PERISHABLE and must be RE-RUN at apply time. Inheriting the table instead
   of re-running it is the defect that plan exists to prevent.**
4. **Do not re-open or rebuild round 1.** Two 9-of-9 certified instances, both honest about what
   they did not claim.
5. **`D1b-5` closes when the TOOL is amended**, not by anything in this project.

---

## 8. COMPILER TOOLS

| tool | invocation | result |
|---|---|---|
| `comp-find` | `--name mdpf_category_registry.py` etc. | piped through `grep 'py:'` and returned NOTHING -- the binary/format trap. **Fell back to `find`; recorded as a miss, not worked around silently** |
| `find` + `grep` | 79 `task_orders/` dirs, 2,111 TO files | the s.2 cell census with 3 positive controls |
| `git log --pretty=%aI` | TO + tool history | ISO-strict, no hand-typed `Z` |
| `aws s3api head-object` / `lambda get-function-configuration` | deployed artifact + live config | digest cross-check, base64 == hex |
| `aws s3 cp` + `zipfile` | the running package, opened | s.5 -- the only instrument that answers "is the defect live" |
| `python json` | 6 proof-of-spec instances | acceptance arrays, presence/absence with byte counts |

**What failed:** `comp-find --name` piped to `grep` printed nothing where `find` returned three
paths. **This is the known "comp-find | grep drops content" class and I hit it anyway.** Cost one
round trip.

**Denominators printed:** 2,111 TO files / 79 dirs · 6 faces · 22 zip members · 21 manifest modules
· 4 scopes · 3 positive controls on the cell census.

**A whole-`org/` recursive grep TIMED OUT at 120s** and returned 2 of 3 answers. **I did not quote
the partial result** -- I narrowed to `task_orders/` and re-ran the full set. *A timed-out sweep
that answered two thirds of its questions is exactly the shape that gets quoted as complete.*

---

## 9. STATE

**PUSH STATE: landed LOCAL, rides integration.**
**Read-only throughout. No status field touched. No build. No emit. No producer invoked. Nothing
deployed. `--pin` default not advanced.**

-- `0.4.0_DS_ClientPlatform~S`
