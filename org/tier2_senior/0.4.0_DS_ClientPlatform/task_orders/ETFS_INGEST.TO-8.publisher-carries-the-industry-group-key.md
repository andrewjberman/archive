# TO ETFS_INGEST.TO-8 — the PUBLISHER carries `GICS_INDUSTRY_GROUP_NAME` to platinum (`INGEST-T4-1`, the rung `TO-6` stops one short of)

<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED) — `INGEST-T4-1` (the publisher + the served key `platinum/etfs/positioning_data.json`) and the SERVED half of `INGEST-T5-1` (condition (ii)).</decomp_ref>
<certification>Rides the SAME certified decomp as `TO-6` (`3.0.0_SA_CVO~Z` @422bdb431b, bound to @fcdf042972). ⛔ **NO new cell is added** — `INGEST-T4-1` is an existing certified cell that no live TO claimed. Cut as a SEPARATE TO rather than as a `TO-6` amendment **precisely so `TO-6`'s certification is not disturbed** under a live clock.</certification>
<issued_to>0.4.0_DS_ClientPlatform~Q</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>SEATED — same lane, same project, same context as `ETFS_INGEST.TO-6`. **Rule 27 is satisfied: one instance, one project.** Take `TO-6` first; this TO is the rung immediately after it.</seating_trigger>
<placement>SITE Z (Rule 26) — D4 is SITEZ-placed until the project is done.</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T01:1xZ</issued>
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

**ORIGINAL STATUS, PRESERVED VERBATIM:** ACTIVE — GATED ON `TO-6` by data dependency (the gold row must carry the key before the publisher can read it). **Not gated on a decision.**</status>
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

⛔ **The gold row carrying the key is necessary and NOT sufficient.** `etf_positioning_publisher.py:230`
`HOLDING_KEYS` is an explicit key list; a key absent from it is dropped on the way to platinum **with no
error**. Without this TO, `TO-6` lands, the gold parquet carries the field, and the served artifact
still does not — a green build with an invisible loss.

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
| `TO8-AC4` | **NO CONSUMER REGRESSION.** `sub_asset_class` values on the served artifact are **byte-identical** to their pre-change values for every row. ⚠ **The positive control matters more than the diff:** show the 11 sector values and the 2 non-equity values still resolve in `SUB_ASSET_CLASS_ORDER` — *an absence check cannot tell a fix from a refactor.* | `INGEST-T4-1` | |
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

<proof_of_spec>
  <criterion id="TO8-AC1" cell_refs="INGEST-T4-1"/>
  <criterion id="TO8-AC2" cell_refs="INGEST-T4-1,INGEST-T5-1"/>
  <criterion id="TO8-AC3" cell_refs="INGEST-T4-1"/>
  <criterion id="TO8-AC6" cell_refs="INGEST-T4-1"/>
  <criterion id="TO8-AC4" cell_refs="INGEST-T4-1"/>
  <criterion id="TO8-AC5" cell_refs="INGEST-T5-1"/>
  <expected_criteria>TO8-AC1,TO8-AC2,TO8-AC3,TO8-AC4,TO8-AC5,TO8-AC6</expected_criteria>
  <alignment_denominators>cells declared: 2 (INGEST-T4-1, INGEST-T5-1); criteria: 6. FORWARD — 6 of 6 criteria carry >=1 cell_ref. BACKWARD — 2 of 2 declared cells reachable (INGEST-T4-1 from AC1/AC2/AC3/AC4, INGEST-T5-1 from AC2/AC5). Unmapped 0; untraceable 0. NOTE: `INGEST-T4-1` was an existing CERTIFIED cell claimed by NO live TO — this TO claims it; it is not a new cut. The DATA half of `INGEST-T5-1` is `TO-6`'s and is not duplicated here.</alignment_denominators>
</proof_of_spec>
