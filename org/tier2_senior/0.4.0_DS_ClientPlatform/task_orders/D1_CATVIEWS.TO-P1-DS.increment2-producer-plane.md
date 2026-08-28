# TO D1_CATVIEWS.TO-P1-DS — INCREMENT 2, THE PRODUCER PLANE

<task_order id="D1_CATVIEWS.TO-P1-DS" project="D1_CATVIEWS">
<id>D1_CATVIEWS.TO-P1-DS.increment2-producer-plane</id>
<decomp_ref>workflows/atom_decomposition/runs/d1-catviews-fullproduct/20260828T2245Z/DECOMP-INCREMENT-2.md @b7921ff493 <owned_cells>CATV2-a-1, CATV2-a-3, CATV2-b-1</owned_cells></decomp_ref>
<issued_to>`0.4.0_DS_ClientPlatform~Z` — seated 2026-08-28 ~22:45Z by `2.0.0_SA_COO~Z` (msg 14422). Rule 27: D1_CATVIEWS only.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T23:0xZ</issued>
<status>pending -- CUT AFTER EXECUTION BEGAN. AC1-AC4 are ALREADY SATISFIED AND EXERCISED; AC5 is the live act. See WHY below -- this face exists so `3.0.0_SA_CVO~Z` has something to certify, not to direct work already done.</status>
</task_order>

<proof_of_spec>
  <criterion id="CATV2-TOP1-AC1" cell_refs="CATV2-b-1"/>
  <criterion id="CATV2-TOP1-AC2" cell_refs="CATV2-b-1"/>
  <criterion id="CATV2-TOP1-AC3" cell_refs="CATV2-a-1"/>
  <criterion id="CATV2-TOP1-AC4" cell_refs="CATV2-a-1"/>
  <criterion id="CATV2-TOP1-AC5" cell_refs="CATV2-a-1"/>
  <expected_criteria>CATV2-TOP1-AC1,CATV2-TOP1-AC2,CATV2-TOP1-AC3,CATV2-TOP1-AC4,CATV2-TOP1-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_CATVIEWS.TO-P1-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 5, firm-tokened `CATV2-TOP1-ACn`. Cells: 3, all pre-existing in the @b7921ff493 decomp. **CATV2-a-2 carries no criterion** — it is a framing statement (the D-4 box thread), not a buildable cell. **CATV2-c-* carry no criterion HERE** — item 3 is AE-plane upstream plus a sovereign mapping ruling, and a criterion on a gated cell is a criterion that cannot be scored.</alignment_denominators>
</proof_of_spec>

## WHY THIS FACE EXISTS, AND WHY IT IS CUT LATE

**Andrew's pipeline is `PRD -> registry -> COO TOs -> execution -> CVO proof-of-spec and ratify`.**
I dispatched increment 2 by message against decomp cells (14422) and the lane executed correctly —
but **I never cut the face**, so delivered, exercised, on-origin work had nothing for the certifier
to score against. **That is my gap, not the lane's**, and this closes it.

⛔ **THIS TO DIRECTS NOTHING THAT IS ALREADY DONE.** AC1-AC4 are recorded here **as satisfied**, with
the evidence the lane produced. **AC5 is the only live act.** A reader must not mistake this for a
re-issue: **re-executing an accepted round is a REWIND** (NEVER#2).

## ACCEPTANCE CRITERIA

**AC1 `CATV2-TOP1-AC1` — ✅ SATISFIED @`7f06a2ee40`. L2 MEMBER `aum` IS EMITTED IN BOTH DIRECTIONS.**
`member_aum={**models_member_aum, **sma_member_aum}` at the `build_category_views` call.
**MEASURED, two-sided and date-independent (no literals; fixture amounts arbitrary):**
```
  AFTER   SMA     P1a measured -> NUMERIC PASS | P1b unmeasured -> NULL PASS | P2 recon PASS
  AFTER   Models  PASS/PASS/PASS   <- regression guard on a family the change did not touch
  CONTROL pre-fix P1a FAIL measured-but-null=[(ETF,divz),(ETF,pfoe)] | P2 FAIL [(ETF,0,150.0)]
```
⭐ **THE NEGATIVE CONTROL EARNED ITS PLACE AND THE LANE SAID SO UNPROMPTED:** the first harness was
**VACUOUS** — the walker guessed the emitted shape (`view_path` keys that do not exist; the real path
is `nodes[L0].children[label].members`) and matched NOTHING, so **every assertion ran over empty
sets and both arms passed.** ⛔ **A HARNESS THAT MATCHES NOTHING SCORES IDENTICALLY TO A PERFECT
FIX.** The lane read the object instead of assuming it.
⚠ **AND THE PROPOSITION ITSELF WAS CORRECTED:** *"no null child under a funded bucket"* is
**FALSE-BY-DESIGN** — `idvz`/`pfde` have no `by_model` entry and MUST emit null. The law now keys on
MEASUREMENT, both directions. **Scoring the original proposition would have failed a correct build.**

**AC2 `CATV2-TOP1-AC2` — ✅ SATISFIED. THE FIX MOVES NO NODE TOTAL.**
Keys disjoint BY CONSTRUCTION (`view_path` L0 is Models XOR SMA); **intersection MEASURED EMPTY over
9 Models + 6 SMA = 15 registered L2 members** — denominator printed. The L1 buckets already carried
these dollars; this populates member rows beneath unchanged parents.
⛔ **THIS IS THE CRITERION THAT WOULD CATCH A DOUBLE-COUNT**, and it is the reason the fix is safe to
land while the rest of the increment is gated.
⚠ `ALT Strategies` remains `0.0` with muni/tax null — **CORRECT today: unmeasured, not mis-emitted.**

**AC3 `CATV2-TOP1-AC3` — ✅ SATISFIED. AC-DERIVATION: THE PRODUCER PATH DOES NOT READ THE FIRM FLAG.**
Per decomp s.3.3 — **a VALUE-based criterion is structurally blind here**, because Opal-Supervised
and Firm-Supervised are both a plausible dollar amount in the same slot under the same parent.
**MEASURED, with the mandatory positive control firing:**
```
  producer path (consolidator + registry): supervised_split|account_supervised|D_05  ->  0 hits
  POSITIVE CONTROL data/cot/scripts/gold/D_05.supervised_split.py                    -> 10 hits
```
⛔ **THE POSITIVE CONTROL IS NOT OPTIONAL** — without it a zero is indistinguishable from a broken
search, and tonight produced four broken greps that each returned a clean zero.

**AC4 `CATV2-TOP1-AC4` — ✅ SATISFIED ON THE LABEL SURFACE. AC-NON-FLATTENING.**
`VIEW_NODE_AXIS` + `NODE_DISPLAY_LABEL` are perspective-qualified throughout; no bare `Supervised`
node, label or axis, and no axis on which a consumer can sum the two lenses.
⭐ **SELF-CORRECTION THE LANE CAUGHT BEFORE REPORTING, RECORDED BECAUSE IT IS THE USEFUL PART:** its
first naming census flagged `:128` as a bare `"Supervised"` label. **It is COMMENT TEXT — the
paragraph documenting the two-referent hazard itself.** The probe conflated comment prose with code
literals. **No violation exists, and a census that cannot tell prose from a literal would have
manufactured one.**
⚠ **SCOPE STATED HONESTLY: this is the LABEL surface.** (c) binds the schema and the renderer too;
the RENDER limb is not this lane's and is not claimed here.

**AC5 `CATV2-TOP1-AC5` — ⬜ THE LIVE ACT. A HELD NODE EMITS `aum: null`, NOT A RESIDUAL.**
**MEASURED TODAY:** a held Client node emits `aum: 290426813.47` — **a RESIDUAL that happens to equal
49financial's Client total.** A node whose predicate is `unavailable` must carry `aum: null`.
>> ⛔ **A HELD NODE CARRYING A CONFIDENT NUMBER OF KNOWN-BAD PROVENANCE IS LIVE ON AN ADVISOR-FACING
   SURFACE TODAY.** <<
⭐ **THIS IS UNBLOCKED *BY* THE `WSE_COTMDL` STOP, NOT BLOCKED BY IT** — the STOP is exactly what
keeps those nodes held, so the fix has its full effect while the STOP stands and needs nothing from it.
⭐ **AND IT MAKES `D1_CATVIEWS.TO-F1-DE` AC5's SUPPRESSED HEADLINE CORRECT BY CONSTRUCTION** — that
suppression currently stands on PROVENANCE; fix the provenance and the headline can return on its
own merits. **The follow-on recorded at AC5, now actionable.**
```
  TWO-SIDED: a HELD node -> aum null;  an AVAILABLE node -> its measured figure, UNCHANGED.
  NEGATIVE CONTROL MANDATORY: pre-fix the held node MUST show the residual, or the harness is
    vacuous -- the exact failure this lane already caught once in this same increment.
  DATE-INDEPENDENT: no market-valued literal. `290426813.47` is a POINTER TO THE DEFECT,
    NEVER A PASS TARGET -- it moves every trading day.
```
⛔ **LAND ON ORIGIN. DO NOT PROMOTE, DO NOT RELAND, NO AD-HOC GOLD RUN.** Monday's scheduled fire
carries it alongside `7f06a2ee40`.
⛔ **DO NOT ALSO CHANGE THE RENDERER** — the headline restoration is a separate act on a different
lane once the data is right. **One plane per change is what made tonight's promote verifiable.**

## CARRIED, NOT SCORED HERE

- **`CATV2-a-3` (cottonwood's THREE-VALUE split) is PRE-COMMITTED BUT NOT SCOREABLE** while the
  `WSE_COTMDL` STOP holds: when the hold lifts, cottonwood emits three values with `unflagged`
  **LABELLED, never folded.** ⚠ **AND A `0.00` unflagged bucket WILL BE SUPPRESSED by the same
  on-rule L1 rule** — on-rule, moves no money, **but decide it deliberately rather than meet it in a
  screenshot.**
- **`938667e5ab`** corrected a `client_predicate` docstring that documented a key shape **nothing
  produces** (all-bare keys; the real contract is MIXED — two fee buckets keyed by VIEW PATH,
  `unflagged` bare). ⚠ **Severity not inflated: bare keys make both fee buckets default to `0.0` and
  the c3 assert then REFUSES the emit — a debugging cycle, NOT a wrong number shipped.** The mixed
  shape is **left as-is deliberately**: 49financial and inflection emit through it live, so a
  key-shape change is its own act with its own evidence, not a docstring passenger.

## BARRED / REPORTING

⛔ **Do NOT touch the renderer, the publisher, or any TO face.** ⛔ **No ad-hoc gold run, no reland,
no S3 write.** ⛔ **Push is the integrator's act.**
⛔ **Item 3 is NOT in this TO** — AE-plane upstream plus a sovereign mapping ruling.
Off-task findings: one line to the surprise channel, keep working. RAVC to `2.0.0_SA_COO~Z` once,
stating push state as a MEASURED value.
