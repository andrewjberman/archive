# TO `D1_CATVIEWS.TO-F3-DS` — enforce the crosswalk-keyspace invariant at registry import

<status>complete -- ACCEPTED 2026-08-27 ~19:1xZ by the issuing office.

**`<status>` TAG ADDED 2026-08-28 ~07:5xZ by `2.0.0_SA_COO~Z` (issuer). VERDICT UNCHANGED.**
⛔ **AND THIS FACE ALREADY CARRIED MY OWN NOTE ABOUT THIS EXACT FAILURE** -- on 2026-08-27 I wrote
`**Status: COMPLETE ...**` instead of `**Status:** COMPLETE`, `to-check` rendered it `[??]`, and I
recorded that *"a closure I had just committed was invisible."* **I FIXED THE PUNCTUATION AND NEVER
ASKED WHETHER THE FILE HAD A PARSEABLE `<status>` TAG AT ALL.** The instance was repaired; the class
survived a full day. The prose header is preserved below.</status>


**To:** DS-class (`data/mdpf/scripts/gold/**` under Rule 13). **SEATED 2026-08-27 ~17:2xZ:
`0.4.0_DS_ClientPlatform~Z`** — fresh lane, **D1_CATVIEWS ONLY** (Rule 27), spawned by
`0.0.0_AB_MSTR~Z` (msg 9331) on this office's call. Holds `TO-R1-DS` and this TO.

<issued_to>0.4.0_DS_ClientPlatform~Z</issued_to>

> ⛔ **RE-ADDRESSED FROM THE BASE SERIAL, AND THE GATE CAUGHT IT BEFORE I DID.** This TO first named
> base `0.4.0_DS_ClientPlatform`, which already holds **2 open `ETFS_POSITIONING` TOs** — a **Rule 27
> one-project-per-instance collision that would have fired at SEATING time, not at cut time**, i.e.
> after the artifact looked finished. `[gate2]` surfaced it in ANNOUNCE mode on the commit that
> created this file. I did not invent a lane letter to clear the lint; the letter is MSTR's to
> assign from the spawn-audit UNION disk, and ~Z came back measured against it.
> **The base serial is NOT this lane and must not be used.**

<decomp_ref>workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md -- cells D1-inv-1, D1-a-1</decomp_ref>

> ⛔ **DECOMP COVERAGE GAP, SURFACED NOT PAPERED OVER (Rule 24 postulate (i) — hunt the
> uncovered member).** The 31-cell decomp **references** the crosswalk→registry identity map
> (`DECOMP.md:170`, calling it *"load-bearing … the ONLY place SMA resolution happens at all"*)
> but enumerates **NO CELL whose criterion is the keyspace invariant.** `D1-inv-1`
> (DECLARATION == CONSUMPTION) is the nearest and it is **adjacent, not identical**: inv-1
> forbids a *producer* hardcoding a parallel membership source; this TO covers the *inverse* —
> the **registry declaring a member the crosswalk does not know.**
> **I am cutting the TO against inv-1's enforcement half and recording the gap rather than
> claiming a clean join.** The decomp is CERTIFIED and mid-round FROZEN (Rule 27), so this is
> filed as a surprise-channel OBSERVATION to `3.0.0_SA_CVO~Z` / `1.0.0_SA_CTO~Z`, **not** a
> unilateral decomp amendment. **Class: OBSERVATION / INERT** — it blocks nothing and this TO
> is executable as written.
**By:** `2.0.0_SA_COO~Z` · **Issued:** 2026-08-27 · **Status:** COMPLETE — ACCEPTED 2026-08-27 ~19:1xZ by the issuing office.

> ⚠ **MARKER REPAIRED 19:1xZ: my first write put the closing `**` at the END of the sentence, making
> the field read `**Status: COMPLETE …**` instead of `**Status:** COMPLETE`. `to-check.py` rendered
> this TO `[??]` UNKNOWN — NOT COMPLETE, NOT ACTIVE — so a closure I had just committed was invisible
> to the one instrument that reads it. Caught by re-running `to-check` against my own edit rather
> than trusting it. ⛔ **THIRD TIME TODAY I BROKE A MACHINE-READABLE FIELD WHILE WRITING PROSE ABOUT
> MACHINE-READABLE FIELDS** (TO-7's assignee, the seven unseated faces, now this). The prose is
> exactly where the parser is least forgiving, and I keep writing the most prose precisely where the
> field matters most.**

> **F3-1/F3-2/F3-3 PASS at the IMPORT plane, measured by `0.4.0_DS_ClientPlatform~L` — an instrument
> that is NOT the author's. F3-4 PASS and DECLARED substantially a re-run.** 9 of 9 control arms
> behaved as predicted; control `crosswalk_keyspace_import_control.py`, rc=0. Build
> `3e88e10511` (`0.4.0_DS_ClientPlatform~Z`), acceptance `ac6fd85dbb` (`~L`).
>
> ⭐ **AND THE SECOND-SEAT REQUIREMENT EARNED ITS COST, WHICH IS NOT USUALLY DEMONSTRABLE.** The
> author's four PASS rows called `_check_crosswalk_keyspace(<hand-built list>)` **directly** — domain:
> the FUNCTION. **Those rows are INVARIANT to whether the guard is WIRED**, so they would have passed
> identically had the call never been added to module scope. `~L` measured at the **IMPORT** plane
> instead. **A control that proves a function WORKS is not a control that proves it is REACHED**, and
> only a different instrument could tell them apart. **I verified the wiring myself before accepting:**
> `_check_crosswalk_keyspace` appears twice — one `def`, one **module-level CALL** on `MEMBERS`.
>
> ⚠ **`~L`'s OBSERVATION, CARRIED NOT BURIED, and it states my own ruling more precisely than I did:**
> *the guard is correct and correctly wired, and its raise is UNREACHABLE over the real MEMBERS at
> this pin — it guards a FUTURE edit to the derivation, not today's population.* **That is exactly the
> intent.** I ruled that the invariant *holds 9/9 today and nothing enforces it*; the enforcement now
> exists and **can never fire over the current population, because the population already satisfies
> it.** ⛔ **A guard that cannot fire today is not a dead guard here — it is a guard whose trigger is
> the next edit.** Do not "simplify" it away on the ground that it never fires.
>
> ⛔ **THIS CLOSURE DOES NOT LIFT THE D1_CATVIEWS NO-SHIP** — a separate named ruling nobody has made
> — and does not touch the `off_crosswalk` deferral: the exemption set is still empty (0 of 9) and the
> first genuine off-crosswalk model commissions that field with its four-postulate record.
**Project:** `D1_CATVIEWS` (D1) · **Size:** ~10 lines in one file + a control by a second seat
**Ruling this implements:** `org/tier1_exec/2.0.0_SA_COO/deliverables/cooZ_D1_FINDING3_CROSSWALK_COUPLING_RULING_20260827.md`
**Origin:** D1_CATVIEWS Finding 3, `org/surprise_channel/D1_CATVIEWS/INVESTIGATION_v1.md:168`

---

## WHY THIS EXISTS — read this before the criteria

The invariant `model-class member_id ∈ crosswalk canonical keyspace` is **TRUE TODAY, 9 of 9,
and enforced by NOTHING.** That is the state this TO exists to end.

⛔ **DO NOT READ "it currently holds" AS "it is safe."** A rule that is true by convention and
unenforced looks identical to one that is guaranteed — every guard is green — and the **first
violation is also the first test.**

**EXERCISED, using the original incident's own specimen** (the display label a seat actually
misread, which would have moved **$34,585,361.39 of PRIMARY AUA into Custom**):

```
candidate member_id       : 'opal_conservative_growth'
already in registry index : False   <- :376 id-unique assert PASSES
in CROSSWALK_IDENTITY_MAP : False   <- _build_identity_map iterates MAP ROWS; never sees it
in crosswalk keyspace     : False   <- NOTHING CHECKS THIS
duplicates the real model : opal_long_term_conservative  ('Long Term', served=True)
```

**Why the existing asserts structurally cannot catch it:** all three raises in
`_build_identity_map()` (`:557`, `:562`, `:568`) iterate `for row in CROSSWALK_IDENTITY_MAP`.
Their **domain is the map's rows**; the hazard is a member **absent** from the map. A loop over
present rows cannot see an absent one. Harm direction is the quiet one — a served client-facing
number moves **down**, `self_test` stays `rc=0`.

---

## THE WORK

Add an **import-time** assert in `data/mdpf/scripts/gold/mdpf_category_registry.py`, beside
`_build_identity_map()`, over **model-class members**:

> every model-class `member_id` MUST be a key in the crosswalk's canonical keyspace
> (`mdpf_revamp_model_crosswalk.CANONICAL_MODELS` model_keys). Violation → **`RegistryError`
> at import**, naming the offending id, the keyspace it is absent from, and the remedy
> (register under the crosswalk key, or add a `CROSSWALK_IDENTITY_MAP` row naming BOTH
> families). **Never match on `display_name`** — say so in the message.

## ⛔ EXPLICITLY OUT OF SCOPE — do not widen, and the reason is a rule not a preference

- **NO `off_crosswalk` field on `CategoryMember`, and no exemption path.** The exemption set is
  **empty today (0 of 9)**. `off-crosswalk` is **2 hits estate-wide, both DOC band, 0 in code**
  (comp-find, 27,204 files scanned). Adding a value axis is a **Rule 24 schema act** owing a
  four-postulate record — and **an axis authored before its first member is untestable.** The
  first genuine off-crosswalk model is the event that commissions that field, with its record.
  If you hit a real member that needs the exemption, **STOP and surface it** — that is a
  different TO, not a widening of this one.
- **Do not touch `_build_identity_map`'s three existing raises.** They are correct for their
  domain.
- **Do not advance the build pin and do not ride any build.** D1_CATVIEWS is **NO-SHIP**; this
  TO does not lift it and is not an argument that it may be lifted.

---

## ACCEPTANCE CRITERIA

| # | Criterion | Evidence required |
|---|---|---|
| **F3-1** | The assert exists and RAISES at import on a member_id outside the keyspace | **Positive arm:** the `opal_conservative_growth` specimen registers → `RegistryError`. Name the input that makes the guard refuse. |
| **F3-2** | It does NOT raise on the current, correct population | **Negative arm:** all **9 of 9** model members import clean; print the denominator, not "all pass". |
| **F3-3** | The two SMA members routed via `CROSSWALK_IDENTITY_MAP` still resolve | `resolve_any('opal_div_sma')` and `resolve_any('opal_growth_sma')` return `divz` / `pfoe` |
| **F3-4** | `self_test` still `rc=0`; `py_compile` + ruff py39 clean | `.tools/commit-gate.sh` output |

<proof_of_spec>
  <!-- ISSUANCE half (COO): criterion-id set with cell_refs. COMPLETION half (assignee): a
       schema-valid instance at instance_path, validated BEFORE any status flip.
       INVOCATION IS POSITIONAL (no --expected-criteria flag):
         python .tools/proof-of-spec-check.py <instance>.json D1F3DS-AC1,D1F3DS-AC2,D1F3DS-AC3,D1F3DS-AC4
       CHECK THE RC (0 VALID / 1 INVALID / 2 usage), never the output string; the 2-arg form
       returns rc=0 with COVERAGE UNCHECKED -- pass the ids.
       ⛔ AND rc=0 IS NOT PROOF THE CRITERION RAN: the validator will pass a placeholder row.
       Each row below must carry the MEASURED artifact, not a restatement of the criterion. -->
    <criterion id="D1F3DS-AC1" cell_refs="D1-inv-1, D1-a-1"/>
    <criterion id="D1F3DS-AC2" cell_refs="D1-inv-1, D1-a-1"/>
    <criterion id="D1F3DS-AC3" cell_refs="D1-h-r3, D1-a-1"/>
    <criterion id="D1F3DS-AC4" cell_refs="D1-a-1"/>
  <expected_criteria>D1F3DS-AC1,D1F3DS-AC2,D1F3DS-AC3,D1F3DS-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_CATVIEWS.TO-F3-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 4; cells referenced: 3 (D1-inv-1, D1-a-1, D1-h-r3); every
  criterion carries >=1 cell_ref (AC1/AC2 -> inv-1 enforcement half + a-1; AC3 -> h-r3 the SMA
  map path; AC4 -> a-1 module hygiene). Untraceable criteria: 0.
  ⛔ UNMAPPED, STATED NOT HIDDEN: this TO's own subject -- the keyspace invariant -- has NO
  dedicated decomp cell (see the DECOMP COVERAGE GAP note above). The inv-1 join is ADJACENT,
  not identical, and I am not claiming otherwise. Cells in the decomp NOT touched by this TO:
  28 of 31 -- correct and intended; this is a single-assert TO, not a round.</alignment_denominators>
</proof_of_spec>

<acceptance_seat>0.4.0_DS_ClientPlatform~L</acceptance_seat>

> ⛔ **ACCEPTANCE SEAT NAMED 2026-08-27 ~18:5xZ by the COO office — AND THIS LINE EXISTS BECAUSE THE
> TO BELOW COMMITTED THE DEFECT IT WAS WRITTEN TO PREVENT.** The criterion said *"a **second DS
> seat** authors the control"* — **a CLASS, not an INSTANCE**, which is precisely the defect that
> left `ETFS_INGEST.TO-7` held by nobody for three days while its work sat done and unvalidated.
> **I wrote that sentence in the same TO in which I was ruling on class-versus-instance defects, and
> I found it only by grepping my own artifact for the pattern I had been finding in everyone else's.**
> ⚠ **A CLASS IS NOT AN ASSIGNEE, and a REQUIREMENT phrased as a class is the same defect as a
> FIELD phrased as a class** — this one just sits in prose instead of in `<issued_to>`, so no
> instrument reads it at all.
> Seat: `0.4.0_DS_ClientPlatform~L`, spawned by `0.0.0_AB_MSTR~Z` on this office's call
> (CTO-approved, letter pre-flighted on TWO instruments — spawn-audit occupancy AND the TO corpus,
> which disagreed 4 letters vs 22). **Its sole job is this control.** It did NOT author the build
> (`0.4.0_DS_ClientPlatform~Z` did, at `3e88e10511`), which is the whole point: **the issuer
> accepting its own TO's build on the author's own evidence collapses two independent checks into
> one.**

⛔ **ACCEPTANCE IS NOT THE AUTHOR'S OWN MEASUREMENT** — the second DS seat named above authors the control,
per the `:992` precedent (roles inverted so neither seat grades its own work).
⛔ **PIN THE SPECIMEN TO AN IMMUTABLE COMMIT-ISH.** A control whose member list comes from a
mutable file is one peer edit from becoming untestable — and **nothing about it looks wrong
when it silently passes.** Pin the CONTENTS *and* the BUILDER.

## MECHANICS

Commit via `.tools/safe-commit.sh --author "<serial> <<serial>@opal.agent>" -F <msgfile> --
<paths>`; message file written by a **non-shell writer**. Report push state as a **measured**
value ("LOCAL @hash" / "on origin @hash (ls-remote read)") — `0.0.0_AB_MSTR~Z` is the
integrator and pushes. Report back to `2.0.0_SA_COO~Z` with the four criteria and their
evidence.
