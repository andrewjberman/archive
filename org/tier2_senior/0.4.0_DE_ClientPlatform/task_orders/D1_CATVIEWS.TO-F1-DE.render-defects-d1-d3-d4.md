# TO D1_CATVIEWS.TO-F1-DE — THE THREE RENDER DEFECTS ANDREW NAMED FROM SCREENSHOTS

<task_order id="D1_CATVIEWS.TO-F1-DE" project="D1_CATVIEWS">
<id>D1_CATVIEWS.TO-F1-DE.render-defects-d1-d3-d4</id>
<decomp_ref>workflows/atom_decomposition/runs/d1-catviews-fullproduct/20260828T2130Z/DECOMP.md @ec7eda542e <owned_cells>CATVP-d-1, CATVP-d-2</owned_cells></decomp_ref>
<issued_to>`0.4.0_DE_ClientPlatform~Z` — seated 2026-08-28 ~21:30Z by `2.0.0_SA_COO~Z`. Rule 27: D1_CATVIEWS only; it is the lane that built the category-views render.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T21:4xZ</issued>
<status>pending -- CUT AND SEATED. Andrew singular-priority directive; these three gate the promote.</status>
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

**AC1 `CATV-TOF1-AC1` — D-1: THE L2 DRILL-DOWN ROWS SHOW DOLLARS.**
Every L2 member row under `MODELS > PRIMARY` and `MODELS > CUSTOM` that HAS an `aum` renders its
figure, on every scope. ⛔ **RENDER-SIDE ONLY — DO NOT TOUCH THE PRODUCER.** Diagnosed by
conservation on the `qa_return_bodies` capture: Custom members sum to `51,899,185.30` and Primary to
`1,752,025,301.90`, **each an EXACT match to its parent**, so absence AND corruption are both ruled
out at the source. **Print before/after for both branches.**

**AC2 `CATV-TOF1-AC2` — THE ONE GENUINE NULL STILL RENDERS `--`.**
⛔ **EXACTLY ONE of the nine is a real `None` (Custom `members[0]`). It MUST keep rendering `--`.**
A fix that makes all nine show dollars has INVENTED A NUMBER. **Null is not `0.00`** — *"a 0 on a
money figure is a measurement nobody took."* ⚠ **This criterion is the negative arm of AC1 and the
two must be scored together**; AC1 alone passes on a build that coalesces nulls to zero.

**AC3 `CATV-TOF1-AC3` — D-3: COLOURS ARE CANONICAL, AND SOURCED, NOT INVENTED.**
Colours must not be assigned by row index. **Concrete instance: `Fixed Income` currently renders
ORANGE under CUSTOM and must be PURPLE.** ⛔ **THE CANONICAL SOURCE IS COTTONWOOD'S PORTFOLIO
ANALYTICS PANEL — read that map and REUSE it.** Andrew, verbatim: *"if you are using purple elsewhere
for fixed income ... then that needs to stay consistent for Opal Fixed Income."*
⛔ **DO NOT invent a palette. DO NOT hardcode a second copy** — two colour tables is the two-carriers
divergence class and it WILL drift. **If the existing map is not importable, SAY SO rather than
duplicating it** — that is a finding, not a failure.

**AC4 `CATV-TOF1-AC4` — D-4: THE FEE DISCLAIMER IS GONE FROM THE DOM.**
Not softened, not shrunk, not warn-and-keep. **GONE.** Andrew, verbatim: *"we do not need to make a
big stink about fees in a big fucking disclaimer on Client, that should not be there at all."*

**AC5 `CATV-TOF1-AC5` — THE EMPTY-CARD DECISION IS SURFACED, NOT INVENTED.**
⛔ On at least one scope the Client card contains **NOTHING BUT** the fee box, so AC4 renders it
**EMPTY**. **An empty titled card is its own defect.** **Surface the options to `2.0.0_SA_COO~Z` and
`1.0.0_SA_CTO~Z` with a recommendation; do NOT silently pick one.** ⚠ **A PASS here is "the decision
was routed and answered", never "I chose something reasonable."**

## BARRED / REPORTING

⛔ **Do NOT touch the producer, the gold consolidator, or any TO face.**
⛔ **No ad-hoc gold run.** ⛔ **Push is the integrator's act.**
⚠ **Verify on the RENDERED PAGE, not on `tsc`** — green compile plus a shipped-log is exactly the
evidence class that produced the ruling this TO reverses.
Off-task findings: one line to the surprise channel, keep working. RAVC to `2.0.0_SA_COO~Z` once.
