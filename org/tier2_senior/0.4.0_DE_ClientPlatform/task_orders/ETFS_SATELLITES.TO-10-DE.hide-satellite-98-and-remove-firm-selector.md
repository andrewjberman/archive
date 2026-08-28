# TO ETFS_SATELLITES.TO-10-DE — ANDREW'S SMOKE FEEDBACK: HIDE Satellite 98 at the RENDER + REMOVE the firm selector

<decomp_ref>workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md — `SAT-d-1` (all four POSITIONING SUMMARY sections blend row-wise — the panel that clipped), `SAT-b-5` (`Opal Satellite 90` has ZERO accounts, `Opal Satellite 98` has ELEVEN — membership derives from the roster predicate), `SAT-c-2` / `SAT-c-3` (firm resolution server-derived-or-validated; visibility gate, not an authorization boundary). **NO new cell.**</decomp_ref>
<certification>Decomp CERTIFIED (`3.0.0_SA_CVO~Z`). No cell added. `SAT-c-2`/`SAT-c-3` are cited on the SAME limbs `TO-9-DE` cited — what changed is the ruled ANSWER on those cells, not their scope. `SAT-b-5` is cited as the CONSTRAINT that makes AC1 a display act rather than a membership act.</certification>
<issued_to>0.4.0_DE_ClientPlatform~S</issued_to>
<executor_class>DE-class (portal, `portal/**` on DEV)</executor_class>
<seating_trigger>SEATED — **same project, same instance, Rule 27 satisfied.** This lane built `TO-8-DE` and `TO-9-DE`, holds the four-way state discrimination, and wrote the selector this TO removes. **Context already loaded; no spawn needed.** ⭐ It also reported `NO SCROLL WORK STARTED` before this TO existed, so nothing is being thrown away.</seating_trigger>
<placement>SITE Z (Rule 26). `portal/` is a WORK-SITE. **Main tree stays on DEV (Rule 19).**</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T04:2xZ</issued>
<status>ACTIVE -- **8 of 9 CRITERIA MET @`5a4349a5`** (portal, DEV). Delivered by `0.4.0_DE_ClientPlatform~S` ~04:3xZ, about ten minutes after issue.

**THE ONLY OPEN CRITERION IS `T10DE-AC3`, AND IT IS PENDING A SOVEREIGN CALL, NOT PENDING WORK.** It is width-dependent and this office never named a viewport -- see AC3's row. **No lane is blocked and no seat is needed.** Certification of the other eight is `3.0.0_SA_CVO~Z`'s and does not wait on AC3.

*** AC2 WAS RE-READ AFTER THE EDIT RATHER THAN CITED FROM BEFORE IT*** -- 9 books served, `Opal Satellite 98` still present, registry sha256 UNCHANGED. **The criterion is about the state AFTER the change, and quoting a prior read answers a different question.**

ORIGINAL: ACTIVE — cut from an ANDREW-DIRECT smoke test, **already amended once by a second Andrew-direct before issue.** He has SEEN the built view and approved it; these are the named remaining points.</status>
<priority>P0 — **the remaining distance to D4's bar.** He smoke-tested Satellites: *"looks very good, its basically done only a couple points id add"*. **The bar is HIS EYE and he has now used it.**</priority>
<authority>**ANDREW-DIRECT 2026-08-28 ~04:2xZ, VERBATIM** (relayed `1.0.0_SA_CTO~Z` 12691) — items (2) and (3) below:

> *"Satellites product looks very good, its basically done only a couple points id add ... Second, need a logical color gradient for the toggle selectors of the different satellites ... third, Satellites doesnt ned a firm selector, because only one firm has this function. maybe good to keep the dropdown code available just comment it oout and have it default to cottonwood, just in case later we may add other custom models for other firms."*

**ANDREW-DIRECT 2026-08-28 ~04:2xZ, VERBATIM, SUPERSEDING HIS OWN ITEM (1)** (relayed 12702):

> *"one coment, i dont think we have to display visually satellite 98, even if we track it otherwise, the premise is that its the same characteristics as 90, so no need to show two, just a frontend change only, that would solve the issue with the width and no need for arrows"*
</authority>

---

## 0. THE HEADLINE, WHICH IS NOT A CRITERION

**HE SMOKE-TESTED THE SATELLITES VIEW AND IT PASSED** — a real localhost build on 5173, against the nine real books. That is the bar he reserved to himself for D4, exercised.

⛔ **NOBODY WRITES A CLOSURE.** His standing word: *"I dont want to see comp-closure on the directives item until i smoke it and its DEFINITIVELY done"* — and he said *"basically done ... a couple points id add."* **The points ARE the remaining distance.**

## 1. ⛔ THE SCROLL WORK IS SUPERSEDED — DO NOT BUILD IT

His first message asked for horizontal scroll on `POSITIONING SUMMARY`. **His second message withdrew the problem instead of the solution:** *"that would solve the issue with the width and no need for arrows."*

>> **EIGHT COLUMNS FIT. The cutoff was a NINE-column problem and he removed the ninth.** No scroll container, no shrink, no arrows.

## 2. ⛔ THE ARCHITECTURE LIMB — THE ONE THAT CAN BE GOT WRONG CHEAPLY

*"even if we track it otherwise ... just a frontend change only."*

>> **THE FILTER IS A RENDER-LAYER FILTER. IT IS NOT A REGISTRY EDIT AND NOT A PRODUCER CHANGE.**

```
  registry.json    KEEPS NINE BOOKS      (as published + verified: 2,196 B, 9 books, 9/9 -> 100.000)
  the producer     KEEPS DERIVING 98
  the PAGE         SHOWS EIGHT
```

⛔ **DO NOT drop `98` from `SATELLITE_MEMBERS`, from the registry, or from the producer.** That destroys tracked data to solve a display choice, and it would silently change what the derived aggregate is computed FROM. ⚠ **`SAT-b-5` is why this matters concretely: `Opal Satellite 98` has ELEVEN accounts and `90` has ZERO.** Removing 98 from membership would remove the populated book and keep the empty one.

## 3. ITEM (2), THE COLOUR GRADIENT -- **BOTH QUESTIONS ANSWERED; IT IS NOW IN THIS TO (AC8/AC9)**

**AMENDED 2026-08-28 ~04:2xZ by `2.0.0_SA_COO~Z` (issuer).** This section previously held item (2) OUT on two open questions. **Both are closed, so it lands HERE rather than in a second TO** -- a separate carrier over the same component is the two-carrier class, and worse, **`AC1` DETERMINES this item's span.**

**(a) DIRECTION -- ANDREW-DIRECT ~04:2xZ, VERBATIM:**

> *"orange on satellite 15, leftmost, the reason is just that equity is becoming higher weighted as we go to the right which does not have duration, therefore it seems like duration is getting smaller but its actually a misnomer"*

**BUILD ANSWER: ORANGE ON SATELLITE 15 (LEFTMOST), RUNNING LEFT TO RIGHT.**

*** HIS REASON IS WORTH MORE THAN THE ANSWER AND IT CORRECTS A MEASUREMENT.*** `1.0.0_SA_CTO~Z` read the Duration row off the screenshot (`2.89 ... 1.81`) and inferred *shortest = rightmost*, which would have run the gradient BACKWARDS. **The number was read correctly and meant something different: equity weight RISES rightward (17.4% -> 91.9%) and equity has NO duration, so the blended average falls because the FIXED-INCOME SLEEVE SHRINKS, not because anything got shorter.** No amount of re-measuring that column would have produced this. **Asking instead of guessing is what caught it.**

**(b) THE ELEMENT** -- identified by `0.4.0_DE_ClientPlatform~Z` (12709) from its own rendered captures, **handed over WITHOUT taking the build** (`ETFS_SATELLITES` is not that lane's project):
```
  HoldingsTab.tsx:969-980   the BOOK-CHIP ROW in the PORTFOLIO COMPOSITION panel header
                            displayPortfolios.map(p => button style backgroundColor:
                              isActive ? p.color : transparent
  HoldingsTab.tsx:66        color: BOOK_COLOR_CYCLE[i % BOOK_COLOR_CYCLE.length]  <- in portfoliosFor
```
*** THE PALETTE ANDREW DESCRIBES ALREADY EXISTS, IN HIS EXACT ORDER -- orange/amber/green/blue/red. THE DEFECT IS THAT IT IS A 5-CYCLE.*** With more than five books the colours REPEAT. **He is asking for INTERPOLATION ACROSS the existing stops, not for a new palette.**
**An earlier search missed it because the constant is named neither `chip` nor `selector` nor `BOOK_COLORS` -- it is `BOOK_COLOR_CYCLE`, and it lives in `HoldingsTab.tsx`, not `bookSet.ts`.**

## 4. ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `T10DE-AC1` | **`Opal Satellite 98` IS NOT DISPLAYED, AND THE FILTER IS AT THE RENDER LAYER.** The Positioning Summary shows eight books. ⛔ **Cite the edit site: it must be a display/selection concern, NOT `SATELLITE_MEMBERS`, NOT the registry, NOT the producer.** | `SAT-d-1` | |
| `T10DE-AC2` | ⛔ **98 IS STILL TRACKED — PROVE THE DATA SIDE IS UNTOUCHED.** `platinum/satellites/registry.json` still carries **NINE** books and still sums to 100.000. **Exhibit the served artifact AFTER the change**, not the source. *"even if we track it otherwise"* is a requirement, not a nicety. | `SAT-b-5` | |
| `T10DE-AC3` | **THE WIDTH PROBLEM IS GONE, AND NO SCROLL WAS ADDED.** No horizontal scrollbar on the panel OR the page body, and no arrows -- *"no need for arrows"*. **AMENDED ~04:4xZ by `2.0.0_SA_COO~Z` (issuer): THIS CRITERION AS FIRST WRITTEN WAS UNSCOREABLE AND THAT IS MY DEFECT.** It said *"eight columns fit without clipping"* and **NAMED NO VIEWPORT WIDTH**, so its truth value depends on an unstated parameter. `0.4.0_DE_ClientPlatform~S` measured rather than guessed: `1440px` 8 columns CLIP - `1600px` labels present but the 8th bar's VALUE labels clip - `1920px` FITS CLEAN. **Removing the ninth column HELPED and did not solve it below ~1920.** >> **THE ACCEPTANCE VIEWPORT IS A SOVEREIGN CALL AND IS WITH ANDREW.** His premise -- *"that would solve the issue with the width"* -- holds at wide viewports and not at common laptop ones, and his own width was called unknown and IS NOT -- **MEASURED 2026-08-28 ~04:4xZ: `1840 x 860`, read from the PNG header of his own screenshot** (`3.0.0_SA_CVO~Z` spotted that the screenshot carries it; `1.0.0_SA_CTO~Z` read it at source). **1840px SITS BETWEEN THE MEASURED THRESHOLDS -- 1600 clips the 8th bar's value labels, 1920 is clean -- SO HE IS ~80px SHORT OF CLEAN AND WILL PROBABLY SEE IT ON THE MACHINE HE ACTUALLY USES.** **BOUND, and it points the unsafe way:** 1840 is the SCREENSHOT width, an **UPPER BOUND** on the browser viewport -- window chrome, scrollbars and any inset come out of it -- so his usable width is **1840 OR LESS**, which moves the estimate TOWARD clipping, not away. **This is a CEILING, not a measured viewport.** *** THE CRITERION IS STILL UNEVALUABLE AS WRITTEN AND THE MEASUREMENT DOES NOT REPAIR THAT:*** *"eight columns fit without clipping"* carries a FREE VARIABLE the criterion never names, so any verdict on it is a verdict about the TESTER'S MONITOR rather than about the page. **A WIDTH-DEPENDENT CRITERION NAMES ITS WIDTH OR IT CANNOT BE SCORED.** **What the 1840 ceiling changes is the RECOMMENDATION, not the scoreability: a narrower-viewport fix is now probably NEEDED rather than hypothetical.** The form is still Andrew's -- he withdrew the scroll explicitly and named shrinking text/bars as his alternative. **UNTIL HE ANSWERS THIS CRITERION IS NOT SCOREABLE AND MUST NOT BE MARKED MET OR FAILED.** - **DO NOT add a scroll to close it:** he withdrew that explicitly, and building it anyway substitutes a lane's judgement for his ruling on a page he had just approved. `0.4.0_DE_ClientPlatform~S` declining to do so was correct. | `SAT-d-1` | **PENDING SOVEREIGN -- viewport unnamed** |
| `T10DE-AC4` | **NO FIRM SELECTOR ON SATELLITES, DEFAULTED TO COTTONWOOD.** *"only one firm has this function."* An internal viewer lands on cottonwood satellites with **no selector and no extra click**. | `SAT-c-2` | |
| `T10DE-AC5` | **THE DROPDOWN CODE IS COMMENTED OUT, NOT DELETED.** *"keep the dropdown code available just comment it oout ... just in case later we may add other custom models for other firms."* **A deletion loses the reasoning; the comment preserves it.** Show re-enabling is a comment-uncomment, not a rebuild. | `SAT-c-3` | |
| `T10DE-AC6` | ⛔ **`TO-9-DE`'s FOUR-WAY DISCRIMINATION SURVIVES.** A 400 must still render as an ERROR and never as *"no satellites"*. **Removing the selector must not collapse those states** — re-exhibit by hash. **A default that turns a failed fetch into an empty registry is the regression this catches.** | `SAT-c-3` | |
| `T10DE-AC7` | **RENDERED, NOT GREPPED.** Read screenshots: the eight-book Positioning Summary with no clipping · the satellites view with no selector, defaulted to cottonwood. ⚠ **THE CANVAS IS SILVER.** | `SAT-d-1` | |
| `T10DE-AC8` | **THE GRADIENT RUNS ORANGE -> YELLOW -> GREEN -> BLUE -> RED, LEFT TO RIGHT, ORANGE ON `Satellite 15`.** Andrew-direct, and his reason is recorded in s.3: the falling Duration column is a MISNOMER. **Do NOT derive the direction from the Duration values** -- that inference was made and was wrong. | `SAT-d-2` | |
| `T10DE-AC9` | **EVERY DISPLAYED BOOK GETS ITS OWN COLOUR -- INTERPOLATE, DO NOT CYCLE.** `BOOK_COLOR_CYCLE[i % len]` at `HoldingsTab.tsx:66` REPEATS once the book count exceeds the palette length. **The palette already carries his exact five stops; blend BETWEEN them across the displayed set.** *** THE SPAN IS THE SET `AC1` LEAVES RENDERED -- EIGHT books, not nine.*** Exhibit each chip distinct in a read render. | `SAT-d-2` | |

## 5. WHY ITEM (3) REVERSES `TO-9-DE`, AND WHY THAT IS NOT A DEFECT

`ETFS_SATELLITES.TO-9-DE` — the internal-viewer firm SELECTION — was cut, built, accepted 5/5 and CERTIFIED between 03:09Z and 03:38Z. **He has now seen it and does not want it.**

>> ⭐ **THE SELECTOR IS WHAT MADE THE VIEW REACHABLE FOR HIM AT ALL.** Without it an internal viewer hit a 400 and **could not have smoke-tested anything.** It did its job, and he is now ruling on the PRODUCT rather than on the build. **This is a RE-SCOPE, not a rework. `0.4.0_DE_ClientPlatform~S` did nothing wrong and `TO-9-DE`'s certification STANDS as history — it was correct for its spec.**

⭐ **And his remedy preserves the reasoning rather than discarding it** — commented-out, not deleted, because other firms may later get custom models. **He is scoping to today's truth without throwing away tomorrow's**, which is the same instinct as *"even if we track it otherwise"* in AC2.

## 6. NOT YOURS

- **The router.** The 400 is CORRECT and stays. Do not touch `index.mjs`.
- **Item (2), the colour gradient** — held on Andrew, see §3.
- **The registry, the producer, `SATELLITE_MEMBERS`** — see §2. **Render layer only.**
- **The PROD promote** — DT lane, Rule 19, held at Andrew's word.
- **`ETFS_INGEST` / `ETFS_POSITIONING` / `D1_CATVIEWS`** — other projects. **Rule 27.**

## 7. REPORTING

Deliverable + read screenshots + proof instance in this lane's `deliverables/`, via `.tools/safe-commit.sh --author "0.4.0_DE_ClientPlatform~S <0.4.0_DE_ClientPlatform~S@opal.agent>" -F <msgfile>` (message file by a **non-shell** writer). Report to `2.0.0_SA_COO~Z`; `3.0.0_SA_CVO~Z` certifies. **ACK on receipt, then report.**

⚠ **`proof-of-spec-check` may return INVALID on vocabulary grounds — FILE THE TRUE VALUES ANYWAY.** Standing ruling: when an instrument and the truth disagree, the instrument is what changes.

<proof_of_spec>
  <criterion id="T10DE-AC1" cell_refs="SAT-d-1"/>
  <criterion id="T10DE-AC2" cell_refs="SAT-b-5"/>
  <criterion id="T10DE-AC3" cell_refs="SAT-d-1"/>
  <criterion id="T10DE-AC4" cell_refs="SAT-c-2"/>
  <criterion id="T10DE-AC5" cell_refs="SAT-c-3"/>
  <criterion id="T10DE-AC6" cell_refs="SAT-c-3"/>
  <criterion id="T10DE-AC7" cell_refs="SAT-d-1"/>
  <criterion id="T10DE-AC8" cell_refs="SAT-d-2"/>
  <criterion id="T10DE-AC9" cell_refs="SAT-d-2"/>
  <expected_criteria>T10DE-AC1,T10DE-AC2,T10DE-AC3,T10DE-AC4,T10DE-AC5,T10DE-AC6,T10DE-AC7,T10DE-AC8,T10DE-AC9</expected_criteria>
  <alignment_denominators>cells declared: 5 (SAT-d-1, SAT-b-5, SAT-c-2, SAT-c-3, SAT-d-2); criteria: 9. FORWARD -- 9 of 9 carry >=1 cell_ref. BACKWARD -- 5 of 5 reachable (SAT-d-1 from AC1/AC3/AC7, SAT-b-5 from AC2, SAT-c-2 from AC4, SAT-c-3 from AC5/AC6, SAT-d-2 from AC8/AC9). Unmapped 0; untraceable 0. NOTE: no cell is added. SAT-c-2/SAT-c-3 are cited on the SAME limbs TO-9-DE cited -- the sovereign changed the ruled ANSWER, not the cell. SAT-b-5 is cited as a CONSTRAINT rather than a deliverable: it records that 98 holds eleven accounts and 90 holds zero, which is what makes AC1 a DISPLAY act and forbids solving it as a membership edit. AMENDED ~04:2xZ: AC8/AC9 carry Andrew's colour gradient, which this TO originally held OUT pending two open questions -- both are now answered (direction by Andrew-direct, element by 0.4.0_DE_ClientPlatform~Z 12709). They land HERE rather than in a second TO because AC1 DETERMINES their span: a separate carrier over the same component would race, and the loser ships a nine-stop gradient over an eight-book row.</alignment_denominators>
</proof_of_spec>
