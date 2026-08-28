# TO D1_CATVIEWS.TO-F1-DE — THE THREE RENDER DEFECTS ANDREW NAMED FROM SCREENSHOTS

<task_order id="D1_CATVIEWS.TO-F1-DE" project="D1_CATVIEWS">
<id>D1_CATVIEWS.TO-F1-DE.render-defects-d1-d3-d4</id>
<decomp_ref>workflows/atom_decomposition/runs/d1-catviews-fullproduct/20260828T2130Z/DECOMP.md @ec7eda542e <owned_cells>CATVP-d-1, CATVP-d-2</owned_cells></decomp_ref>
<issued_to>`0.4.0_DE_ClientPlatform~Z` — seated 2026-08-28 ~21:30Z by `2.0.0_SA_COO~Z`. Rule 27: D1_CATVIEWS only; it is the lane that built the category-views render.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T21:4xZ</issued>
<status>CLOSED 2026-08-28 ~23:2xZ by `2.0.0_SA_COO~Z` (issuer). ALL FIVE CRITERIA TERMINAL, ZERO FAIL, measured at the instance -- AC1 N/A-BY-CONSTRUCTION (struck: D-1 was DATA), AC2 UNCOMPUTABLE-BY-CONSTRUCTION, AC3 PASS, AC4 PASS, AC5 UNCOMPUTABLE (discharged by ruling (B), suppression stands on provenance). World-done: AC3+AC4 shipped and are LIVE IN PROD @`1b91b197` (tag portal-v2.1.171), verified at the PROD edge with a real bearer and on the rendered page. DO NOT SEAT. DO NOT RE-EXECUTE -- re-running an accepted round is a REWIND (NEVER#2).</status>
</task_order>

<proof_of_spec>
  <criterion id="CATV-TOF1-AC1" cell_refs="CATVP-d-1"/>
  <criterion id="CATV-TOF1-AC2" cell_refs="CATVP-d-1"/>
  <criterion id="CATV-TOF1-AC3" cell_refs="CATVP-d-2"/>
  <criterion id="CATV-TOF1-AC4" cell_refs="CATVP-d-2"/>
  <criterion id="CATV-TOF1-AC5" cell_refs="CATVP-d-2"/>
  <expected_criteria>CATV-TOF1-AC1,CATV-TOF1-AC2,CATV-TOF1-AC3,CATV-TOF1-AC4,CATV-TOF1-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D1_CATVIEWS.TO-F1-DE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 5, firm-tokened `CATV-TOF1-ACn`. Cells: 2, both pre-existing in the @ec7eda542e decomp. **D-2 (the SMA card) is NOT in this TO** — it waits on a reserved reland act at Andrew.</alignment_denominators>
</proof_of_spec>

## WHY THIS EXISTS

**Andrew sent six screenshots and named four defects. Three are render-side and do not wait on
anything.** `1.0.0_SA_CTO~Z` reversed its own *"the frontend is done"* ruling within 20 minutes on
that evidence, naming its own basis: it inferred *"renders correctly"* from *"compiles and was
render-verified"*, **and nobody had looked at the actual page since the data changed.**

⛔ **THE PROMOTE IS GATED ON ALL THREE.** Promoting now ships `--` rows, wrong colours and the fee box.

## ACCEPTANCE CRITERIA

**AC1 `CATV-TOF1-AC1` — ⛔⛔ STRUCK FROM THIS TO 2026-08-28 ~21:4xZ by `2.0.0_SA_COO~Z` (issuer). D-1 IS A DATA DEFECT, NOT RENDER, AND THIS CRITERION WAS UNSATISFIABLE BY ANY CORRECT RENDER CHANGE.** MEASURED: the SERVED object (13:31Z, OLD code) has member keys `['display_name','member_id','served','strategy_id']` — **NO `aum` KEY AT ALL**, all 9 members `None`. `CategoryViewTree.tsx:224` already reads `m.aum !== null && m.aum !== undefined ? formatAUM(m.aum) : '--'` — **it prints a figure whenever one exists.** ⭐ **THE RENDERER IS CORRECT AND THE RELAND DELIVERS D-1 WITH ZERO RENDER CHANGE.** ⚠ **ORIGIN OF THE ERROR, recorded because it is the night's own shape:** the diagnosis ran a sound conservation check on the **QA bodies of the CURRENT code** and concluded render-side — but the page renders the **SERVED object written by the PREVIOUS code.** A correct measurement of the wrong artifact. **D-1 MOVES TO `D1_CATVIEWS.TO-R1-AE`.** ~~D-1: THE L2 DRILL-DOWN ROWS SHOW DOLLARS.~~
Every L2 member row under `MODELS > PRIMARY` and `MODELS > CUSTOM` that HAS an `aum` renders its
figure, on every scope. ⛔ **RENDER-SIDE ONLY — DO NOT TOUCH THE PRODUCER.** Diagnosed by
conservation on the `qa_return_bodies` capture: Custom members sum to `51,899,185.30` and Primary to
`1,752,025,301.90`, **each an EXACT match to its parent**, so absence AND corruption are both ruled
out at the source. **Print before/after for both branches.**

**AC2 `CATV-TOF1-AC2` — ⛔⛔ RE-CUT 2026-08-28 ~21:5xZ by `2.0.0_SA_COO~Z` (issuer). MY PREMISE WAS FALSE AT SOURCE AND SATISFYING IT WOULD HAVE BROKEN A SOVEREIGN-RULED BEHAVIOUR.**
~~The one genuine null must still render `--`; the renderer already does this correctly.~~ **IT DOES NOT, AND THAT IS THE CODE BEING RIGHT.** Found and EXERCISED by `0.4.0_DE_ClientPlatform~Z`:
```
  :198  const members = visibleConstituents(row.members ?? [])      <- runs FIRST
  :135  anyMapped = items.some(aum != null)     TODAY false -> nothing suppressed -> all dash
  :139  return items.filter(aum != null && aum !== 0)
        POST-RELAND anyMapped is TRUE (8 of 9 carry values) -> members[0] IS REMOVED, NOT DASHED
```
⛔ **`:224`'s dash is only ever reached by members that ALREADY SURVIVED `:198`.** And the deletion is **ANDREW'S OWN OVERRULE** (*"a null is a 0 in this case"*) — so my criterion demanded the lane CHANGE CORRECT CODE to contradict a sovereign ruling. **Eighth criterion of mine today that no correct implementation could satisfy, and the first that would have caused a REGRESSION if met.**
**AS RE-CUT:** post-reland, **the suppressor behaves per the overrule** — `members[0]` (`aum` null) is **REMOVED** from the rendered list, the remaining **8 render their values**, and **no row displays `0.00` for a null**. ⚠ **Score AFTER the reland**; before it `anyMapped` is false and every row dashes, so this passes vacuously on an unchanged renderer.
⭐ **AND THE FINDING WAS EXERCISED, NOT ARGUED:** that lane's scorer ARM 3 reads `subject NULL not 0 (overrule) -> ABSENT@G5, expected ABSENT@G5, OK`. **The instrument built two hours ago is what caught my criterion.**

**AC3 `CATV-TOF1-AC3` — D-3: THE TREE RESOLVES COLOUR THROUGH THE MODEL-COLOUR AUTHORITY.**
⭐ **RE-CUT 2026-08-28 ~21:5xZ — THE DEFECT IS A BYPASS, NOT A PALETTE CHOICE.** Andrew clarified *"there is a canonical 'Opal Fixed Income' model, it is a portfolio that Cottonwood invests in"*, and `1.0.0_SA_CTO~Z` then DERIVED the colour rather than choosing one:
```
  getModelColor('Fixed Income') -> no exact/partial match -> EXTENDED_MODEL_COLORS[hash % 6]
  stableNameHash('Fixed Income') = 477671664 ; 477671664 % 6 = 0 -> ext-violet #8b5cf6  PURPLE
  getModelColor consumers: 11 files, incl. the Portfolio Analytics panels Andrew named
  CategoryViewTree.tsx uses getModelColor: ZERO times
```
>> ⛔ **THAT ASYMMETRY IS THE WHOLE DEFECT. Every other panel resolves through the model-colour system; this tree INVENTED A POSITIONAL PALETTE.** Andrew was not misremembering and there was never an inconsistency to adjudicate — **ONE PANEL OPTED OUT.** <<
**THE FIX IS TO CALL `getModelColor(...)`, NOT TO PICK COLOURS.** ⛔ **CLARIFIED 22:1xZ by `2.0.0_SA_COO~Z` (issuer) — MY WORDING WAS AMBIGUOUS AND A CERTIFIER WOULD HAVE MISSCORED A CORRECT COMMIT.** ~~Do NOT hardcode `#8b5cf6`~~ **The prohibition targets hardcoding the hex IN `CategoryViewTree` — a second carrier inside the CONSUMER. PINNING IT IN THE AUTHORITY (`MODEL_PORTFOLIO_COLORS`) IS THE AUTHORITY DOING ITS JOB, and it is what `1.0.0_SA_CTO~Z` 14202 s.3 ORDERED. THE PIN STANDS.** ⭐ **And it closes a real hazard rather than decorating one:** `'Opal Fixed Income'` hashes to index 4 (`#d946ef`) and **COLLIDES with `'Opal Global All Equity Total Return'` in the SAME Custom card** — so the day the producer emits the fuller name, a canonical model silently repaints INTO a collision. ⭐ **CONTROL, run on the SHIPPED function via `bun`, 40-name corpus: SUBJECT `#8b5cf6` -> `#8b5cf6` IDENTICAL (a PIN, not a repaint); 3 of 40 moved, all intended; ZERO currently-served rows change colour.** Scored the whole corpus because a new key WIDENS the partial-match direction — **the direction that ADDS matches never announces itself.** Route the L2 member name through the same authority the other 11 files use; purple falls out, and so does every other row.
⚠ **AND MY EARLIER RELAY WAS WRONG:** I reported *"there is no purple fixed income in this codebase."* **There is** — computed at runtime by a hash, never written as a literal, **so a source search for a colour definition structurally could not find it.** A correct search, a wrong conclusion.

**AC4 `CATV-TOF1-AC4` — D-4: THE FEE DISCLAIMER IS GONE FROM THE DOM.**
Not softened, not shrunk, not warn-and-keep. **GONE.** Andrew, verbatim: *"we do not need to make a
big stink about fees in a big fucking disclaimer on Client, that should not be there at all."*

**AC5 `CATV-TOF1-AC5` — ✅ DISCHARGED 22:1xZ. THE DECISION WAS ROUTED AND IS ANSWERED: (B) STANDS AS SHIPPED — THE HEADLINE STAYS SUPPRESSED ON A HELD NODE.**
`0.4.0_DE_ClientPlatform~Z` measured **EXACTLY 2 of 4** scopes go empty (`global`, `cottonwood`), not *"at least one"* as I wrote, and shipped (B) while recommending (A) **conditional on the issuer confirming the held-node figure is trustworthy.**
⛔ **IT IS NOT, AND MY OWN EARLIER MEASUREMENT IS THE GROUND:** *"`aum: 290426813.47` — A HELD NODE SHOULD CARRY `aum: null`. The residual happens to equal 49financial's Client."* **The figure on a `predicate: unavailable` node is a RESIDUAL, not a measured Client total.** Restoring it would put a number of known-bad provenance on an advisor-facing card — **the data-hygiene defect I named, rendered.**
⭐ **(A)'s premise was sound and I am rejecting it on a DIFFERENT ground than it addressed:** the headline gate's stated rationale WAS the contradiction with the box, and that rationale IS gone with the box. **The suppression now stands on provenance, not on contradiction.** ⛔ **(C) correctly rejected — hiding ~$290M of Client from an advisor is worse than either.**
**FOLLOW-ON, PRODUCER-SIDE, NOT THIS TO:** a held node should emit `aum: null` rather than a residual. **Then (A) becomes correct by construction** and the headline can return. Carried as an open item.

## BARRED / REPORTING

⛔ **Do NOT touch the producer, the gold consolidator, or any TO face.**
⛔ **No ad-hoc gold run.** ⛔ **Push is the integrator's act.**
⚠ **Verify on the RENDERED PAGE, not on `tsc`** — green compile plus a shipped-log is exactly the
evidence class that produced the ruling this TO reverses.
Off-task findings: one line to the surprise channel, keep working. RAVC to `2.0.0_SA_COO~Z` once.

---

## CLOSED 2026-08-28 ~23:2xZ BY `2.0.0_SA_COO~Z` (issuer) — MEASURED AT THE INSTANCE, NOT RECALLED

```
  CATV-TOF1-AC1   N/A-BY-CONSTRUCTION      struck -- D-1 was a DATA defect, not render
  CATV-TOF1-AC2   UNCOMPUTABLE-BY-CONSTRUCTION
  CATV-TOF1-AC3   PASS                     the tree resolves colour through getModelColor
  CATV-TOF1-AC4   PASS                     the fee disclaimer is GONE from the DOM
  CATV-TOF1-AC5   UNCOMPUTABLE             discharged by ruling (B); suppression on PROVENANCE
  -> 5 of 5 terminal. ZERO FAIL. DENOMINATOR 5, and it matches <expected_criteria>.
```
**WORLD-DONE, AND THAT IS THE LIMB THAT CLOSES A FACE — NOT THE VERDICT TABLE.** AC3 and AC4 are
LIVE IN PROD @`1b91b197` (tag `portal-v2.1.171`), verified at the PROD edge with a real bearer and
on the rendered page, across 4 of 4 scopes.

⛔ **WHY THIS FACE STAYED OPEN LONG AFTER ITS WORK SHIPPED: CLOSING IS THE ISSUER'S ACT AND NOTHING
DOES IT AUTOMATICALLY.** A face outlives its work indefinitely, reading `pending` while the code is
in production — and `[ACTIVE]`/`pending` is indistinguishable from genuinely-unfinished work in every
census that reads faces. **That is precisely the `behind_record_count` this project carries.**
⭐ **THIS CLOSE WAS PROMPTED BY MY OWN ADVISORY FINDING** — `D1_CATVIEWS_closeout_drift_20260828T160055Z`
(owner `2.0.0_SA_COO~Z`, 8 records behind), whose note names *"an open TO"* as a place to look. **The
instrument was right and had been sitting unread since 16:00Z.**
⚠ **TWO CRITERIA CLOSE AS UNCOMPUTABLE AND THAT IS AN HONEST TERMINAL STATE, NOT A PASS.** AC2 could
not be computed by construction; AC5 was answered by a ruling rather than a measurement. **Neither is
recorded as green, and a reader must not read "closed" as "all PASS".**
