# TO D1_CATVIEWS.TO-R1-DE — round 1, DE lane: the MDPF global view TREE — L0 present-subset tiles · L1 drilldown · L2 Custom enumeration · the predicate-UNAVAILABLE state · consumed-not-rendered acceptance

<task_order id="D1_CATVIEWS.TO-R1-DE" project="D1_CATVIEWS">
<decomp_ref>workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md @469a9e9868 (+ s.4a post-cert amendment) — cells D1-h-v1, D1-h-v2, D1-h-v3, D1-h-v4, D1-h-p1, D1-c-1, D1-c-2, D1-inv-4 (render half).</decomp_ref>
<!-- ISSUER FIX 2026-08-24 ~22:4xZ on 0.7.0_AE_CloudOps~G's BLOCKING-INERT finding (66872), which measured that
     proof-of-spec-check.py:259 harvests EVERY cell id in the WHOLE <decomp_ref> element via CELL_ID_RE and treats
     each as a cell the TO CLAIMS -- so a READ-DEPENDENCY reads as an unclaimed claim and, worse, an EXPLICIT
     EXCLUSION CLAUSE is INVERTED into a claim the TO is then faulted for not discharging.
     THE FIX IS RELOCATION, NOT DELETION. Every sentence below is preserved VERBATIM; it has simply moved out of
     the harvested element into this sibling one, so <decomp_ref> now carries EXACTLY the cells this TO OWNS and
     DISCHARGES. Deleting the read/exclusion prose to make a regex quiet -- the wrong fix AE~G named before anyone
     reached for it -- would have destroyed the only record of what this TO reads and what it deliberately does not.
     The durable repair is the EXTRACTION (scope the harvest to the owned-cells clause), routed to CTO/the tooling
     lane; this element is forward-compatible with it. No acceptance row, criterion, cell_ref or attestation changed. -->
<decomp_context>Reads D1-b-1's contract (the DS lane's mint, TO-R1-DS). Constrained by boundaries D1-g-1, D1-g-2. NOT in this TO: any registry/gold cell (TO-R1-DS), D1-f-1.</decomp_context>

<certification>**CERTIFIED DECOMP** — `3.0.0_SA_CVO` cert @60d4e2f1b4 (28/28). If a surprise item returns DECOMP-INVALIDATING, the ISSUER re-derives these premises — the executing seat does not adjudicate that.</certification>
<issued_to>DE-class (portal frontend, `portal/**` on DEV). **SEATED: `0.4.0_DE_ClientPlatform~C` (MSTR 66470, spawned 2026-08-24 ~20:24Z, D1_CATVIEWS ONLY); watches `0.4.0_DS_ClientPlatform~F` for the start condition.** ONE PROJECT PER INSTANCE (Andrew-direct @b705331f7d).</issued_to>
<executor_class>DE-class</executor_class>
<seating_trigger>Spawn call routed to MSTR same turn (66463). **Start condition (OBSERVED, never a date): the DS lane's `category_views` CONTRACT SKELETON is COMMITTED** (the field shape of D1-b-1: nodes, sub-nodes, the `predicate: "unavailable"` marker, the Insurance view-plane flag) — component work starts on the skeleton; render ACCEPTANCE (AC2–AC7) waits for the first DEV-readable emission. If the class goes dark mid-execution the spawn call re-routes to MSTR same turn.</seating_trigger>
<placement>LAPTOP (Rule 26; portal dev-server + screenshot verification proven here). PROD is NOT this TO (DT lane, `/prod-deploy`).</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-24T20:2xZ</issued>
<status>ACTIVE (start condition above)</status>
<priority>P1 — Andrew's "beeline" + the Monday push order (D1 IMMEDIATE TERM).</priority>
<scope_guard>ONE PROJECT. Exactly the cells in `<decomp_ref>`. No Positioning page, no ETFS GICS→sub-categories work (that is site Z's D4 chain), no Books/ADVI work. Adjacent findings → one line to `3.0.0_SA_CVO` by MCP, cc `2.0.0_SA_COO` (CVO FILES it under `org/surprise_channel/D1_CATVIEWS/`; executing seats do NOT write that tree -- CVO_WORKSPACE lane, ruling 66580), no action, keep working.</scope_guard>
<authority>PRD `docs/architecture/D1_ASSET_CATEGORY_VIEWS_PRD.md` s.8 + **s.8.6 (the view tree, Andrew-direct ~18:5xZ, verbatim record in `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260824_D1_VIEW_TREE_L0_L1_L2_CLIENT_MODELS_SMAS_ALTERNATIVES.md`)** + s.4.3 + the CVO amendment @d476339293 (the invisible-fallback class). Supersedes pre-pipeline TO-D1d (never started).</authority>
<proof_of_spec>
  <!-- Positional invocation, check the rc:
         python .tools/proof-of-spec-check.py <instance>.json D1R1DE-AC1,D1R1DE-AC2,D1R1DE-AC3,D1R1DE-AC4,D1R1DE-AC5,D1R1DE-AC6,D1R1DE-AC7,D1R1DE-AC8,D1R1DE-AC9 -->
    <criterion id="D1R1DE-AC1" cell_refs="D1-c-1"/>
    <criterion id="D1R1DE-AC2" cell_refs="D1-h-v1, D1-h-p1"/>
    <criterion id="D1R1DE-AC3" cell_refs="D1-h-v2"/>
    <criterion id="D1R1DE-AC4" cell_refs="D1-h-v3"/>
    <criterion id="D1R1DE-AC5" cell_refs="D1-h-v4"/>
    <criterion id="D1R1DE-AC6" cell_refs="D1-c-1, D1-c-2"/>
    <criterion id="D1R1DE-AC7" cell_refs="D1-inv-4"/>
    <criterion id="D1R1DE-AC8" cell_refs="D1-h-v1"/>
    <criterion id="D1R1DE-AC9" cell_refs="D1-c-1"/>
  <expected_criteria>D1R1DE-AC1,D1R1DE-AC2,D1R1DE-AC3,D1R1DE-AC4,D1R1DE-AC5,D1R1DE-AC6,D1R1DE-AC7,D1R1DE-AC8,D1R1DE-AC9</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform~C/deliverables/D1_CATVIEWS.TO-R1-DE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells in this TO: 8 (v1 AC2/AC8 · v2 AC3 · v3 AC4 · v4 AC5 · p1 AC2 · c-1 AC1/AC6/AC9 · c-2 AC6 · inv-4 AC7); criteria: 9; unmapped cells: 0; untraceable criteria: 0.</alignment_denominators>
</proof_of_spec>
</task_order>

## ⛔ SPEC-AT-PICKUP — YOUR FIRST ACT

| # | Premise | Oracle that would FALSIFY it |
|---|---|---|
| O-1 | The page has NO drilldown and does not consume the block today | `comp-find -i 'drilldown\|category_views\|Supervised' portal/src/pages/ModelPortfolios.tsx` → 0 hits / 1 file (2,471 lines) |
| O-2 | The portal main worktree is on DEV | `git -C portal branch --show-current` → `DEV` (if PROD: `git -C portal checkout DEV` first — Rule 19) |
| O-3 | The DS lane's contract skeleton is committed (your start condition) | `git log --oneline -- data/mdpf/scripts/gold/ | head` shows the TO-R1-DS contract commit; read the field shape from it |
| O-4 | Insurance has zero members → the view plane and the gold plane coincide today | the served block carries the Insurance view-plane flag and `Insurance == 0` |

## THE TREE YOU RENDER (his words; decomp s.2.h.0)

| L0 (rendered iff PRESENT for the firm) | L1 (on click) | L2 |
|---|---|---|
| Client | Client Supervised / Client Unsupervised (+ the labelled third bucket where the emitter carries it) | — |
| Models | Primary Models / Custom Models | Custom Models ENUMERATED |
| SMAs | the registry-driven nodes ⛔ **(today, as `strategy_id` values and NOT render labels: `tax` / `muni` / `divz` / `pfoe` -- corrected on DE~C self-scan 67764. The block's `display_name`s are "Tax-Managed SMA" / "Muni SMA" / "Dividend SMA" / "Opal Equity Growth SMA"; a seat rendering this list draws "DIVZ" where the block says "Dividend SMA")** -- OPEN enumeration, **render whatever the block carries**, which is the clause that made this MEDIUM instead of HIGH: the row already carried its own antidote and DE~C got it right BECAUSE of it | — |
| Alternatives | NO drill (deferred by his word) — an L0 tile with a DISABLED, labelled state, not an empty panel | — |
| Insurance | NOT in the tree (view-plane flag) | — |

## Cells

- **`D1-h-v1` L0 view** on `ModelPortfolios.tsx` — present-subset tiles. **Presence (`D1-h-p1`) = the node's served AUM at the firm's as-of > 0**, not members-registered. By construction today: Alternatives ABSENT for every firm; Insurance excluded; L0 = {Client, Models, SMAs} or {Client, Models}. **An absent node is ABSENT (no tile), never an empty tile.** No route change.
- **`D1-h-v2` L1 drilldown** — Client: two fee buckets + the labelled third; Models: Primary / Custom; SMAs: the block's nodes; Alternatives: inert click that says why.
- **`D1-h-v3` L2** — Custom Models enumerated from the block (= `members_for('Models > Custom')` on the emitter side); if the DS lane disclosed a gap (r4), render the disclosure, never a padded row.
- **`D1-h-v4` PREDICATE-UNAVAILABLE STATE** — where the block carries `predicate: "unavailable"` ⛔ **-- "(Inflection today)" STOOD HERE AND WAS STALE. CORRECTED ON DE~C SELF-SCAN 67764: INFLECTION IS *NOT* THE UNAVAILABLE CASE** (it carries a live account-grain predicate `is_fee_earning`, 911 accounts), so **ZERO FIRMS EXERCISE THIS TODAY** -- build the state, fixture it synthetically, do not build an Inflection fixture. **THE ISSUER DEFECT THIS EXPOSES IS MINE AND IT IS GENERAL: I LANDED THE AMENDMENT ON THE ACCEPTANCE ROW AND NOT ON THIS CELL DESCRIPTION, so the file asserted both halves at once -- and the STALE half sat where a builder looks for WHAT TO BUILD while the fresh half sat where they look for HOW IT IS JUDGED. AN AMENDMENT LANDS ON EVERY SURFACE THAT CARRIES THE CLAIM, OR IT HAS NOT LANDED**, the Client L1 renders "fee split unavailable for this firm". ⛔ **NEVER `Unsupervised = 0`, NEVER `Supervised = Client`.** An unavailable predicate rendered as a zero is a false frame on a fee line.
- **`D1-c-1` CONSUMED, not merely rendered** + **`D1-c-2` the EMPTY-`category_views` fallback path (feature-gated) is ITS OWN CELL** — *"the page is not evidence when the fallback renders the same page"* (CVO @d476339293). Drive the empty case on purpose; it must be DISTINGUISHABLE in the test record from the consumed case. If you cannot tell them apart, AC2–AC5 are not established either.
- **`D1-inv-4` (render half)** — the displayed L0 sum == `total_aua − Insurance`; every L1 set sums to its L0 parent in the UI; **no double count expressible**. Do NOT display the five-peer gold total as the L0 sum.

## Mandate (three-phase, as TO-D1d had it — carried)
1. `comp-transform schema-check ModelPortfolios` (MISSING = runtime undefined) + `comp-cache` collisions. Rule 20(b): dependency graph BEFORE the frontend commit.
2. Portal main worktree stays on DEV (Rule 19).
3. `/frontend-dev` screenshot verification — READ the screenshot; silver-canvas colour law (light text / ghost-white buttons outside a dark Panel = the #1 recurring defect; a grep cannot see contrast).

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding |
|---|---|---|---|
| **D1R1DE-AC1** | **AMENDED BY THE ISSUER 2026-08-24 ~20:4xZ on DE~C's BLOCKING-INERT item 66518** — `comp-transform schema-check ModelPortfolios` has NO DOMAIN on this flat single-file page (no `types.ts`; rc=1 `[WARN] types-resolution`, the check aborts before running; positive controls Correlation/FactorTilts discriminate) — so a 0-MISSING there could not have said otherwise and is NOT a pass. **The exercised discriminator for the same defect class (renders a field the response type does not carry) is: declare the `category_views` response types in `@/api/endpoints/aum` (where this page's other response types `MdpfPerFirmTimeSeries` / `MdpfFirmAUMMetrics` already live — Build Ladder rung 2) and let `bun run typecheck` (AC9) fail on any rendered field the type does not carry — exercise it once with a mutant (render a field absent from the type → typecheck FAILS).** The `comp-transform` call stays ON RECORD as run-with-its-domain-disclosed, never deleted. `comp-cache` collisions re-run (the pre-existing `['model-portfolio-benchmarks']` collision at `ModelPortfolios.tsx:533` / `ModelPortfolioModal.tsx:114` is NOT yours to fix — add no colliding key); DEV branch confirmed | D1-c-1 | SOURCE + EXERCISED (typecheck mutant) |
| **D1R1DE-AC2** | L0 renders the PRESENT subset; a fixture with one node at 0 AUM shows the tile ABSENT (not empty); with SMA AUM > 0 three tiles, else two | D1-h-v1, D1-h-p1 | EXERCISED |
| **D1R1DE-AC3** | L1 drill per L0 value renders from the block: Client fee buckets (+ third), Models Primary/Custom, SMAs registry-driven; Alternatives click inert + labelled | D1-h-v2 | EXERCISED |
| **D1R1DE-AC4** | L2 Custom list equals the block's Custom members; the DS-disclosed gap renders as a disclosure | D1-h-v3 | EXERCISED |
| **D1R1DE-AC5** | ⛔ **RE-SIZED BY THE ISSUER 2026-08-24 ~22:0xZ on DS~F's census (66722): Inflection is NOT the unavailable case — it carries a live account-grain predicate (`is_fee_earning`, 911 accounts), so ZERO firms exercise this today.** The cell STAYS and its exercise is now an explicit **FIXTURE** carrying `predicate: "unavailable"` (a render path with no test fails the first time it is real): the panel shows the unavailable state; both fee buckets ABSENT, not zero; **no firm is named in the evidence** | D1-h-v4 | EXERCISED (fixture) |
| **D1R1DE-AC6** | Consumed vs empty-fallback cases BOTH captured and DISTINGUISHABLE in the test record (NON-NULL member lists for ≥1 firm in the consumed case) | D1-c-1, D1-c-2 | EXERCISED |
| **D1R1DE-AC7** | Displayed L0 sum == `total_aua − Insurance`; each L1 sums to its L0 parent; no double-count expressible in the UI | D1-inv-4 | EXERCISED |
| **D1R1DE-AC8** | Screenshot READ on record + colour law checked on the silver canvas | D1-h-v1 | EXERCISED |
| **D1R1DE-AC9** | Commit on DEV under your author line via `safe-commit.sh`; `bun run typecheck` clean; proof instance VALID rc=0 positional. ⛔ **PASS-ATTRIBUTION (added by the issuer on CVO 67546): A WHOLE-TREE TYPECHECK IS A STRONG INSTRUMENT ABOUT THE TREE AND NOT ABOUT YOUR LANE, so a bare green is a PASS THAT IS NOT ATTRIBUTABLE TO THE WORK IT ACCEPTS.** Two DE lanes and `1.0.0_SA_CTO~X` all write portal DEV; `~X` landed the AGG removal BETWEEN their commits, so this is measured, not hypothetical. **Record the typecheck as a PAIR OF NAMED REFS -- BEFORE your change and AFTER -- on the face of the proof instance: clean->clean ATTRIBUTES, red->green ATTRIBUTES, and clean->clean ACROSS A PEER'S COMMIT is DISCLOSED rather than claimed.** Same rule as the standing evidence-at-a-named-ref one, applied to a GATE instead of an artifact. **And the direction that needs this is the GREEN one: a peer's RED is loud and gets investigated in minutes; a peer's green is silent, and nobody investigates a pass.** | D1-c-1 | SOURCE + EXERCISED |

## Do not
- No PROD promote (DT lane). Stop at DEV.
- Do not treat a green render as consumption (AC6 is the discriminator; not optional).
- Do not add L1 nodes for IDVZ / PFDE or any node the block does not carry — the enumeration is the registry's (Q-h1 is at Andrew).

## Status + reporting
Cell-level status in a `<cell_status>` block on this file; proof instance + flip = one atomic commit. Report to COO at each flip (hash + push state, never bare "landed"); cc `3.0.0_SA_CVO` at AC6/AC7; cc the DS lane at render-verified so the projection owner sees the consumption result. Surprises: `3.0.0_SA_CVO` by MCP, cc `2.0.0_SA_COO` (CVO FILES it under `org/surprise_channel/D1_CATVIEWS/`; executing seats do NOT write that tree -- CVO_WORKSPACE lane, ruling 66580). **Nothing to `4.0.0_SA_CRO*` this session.**

## `<cell_status>` -- 0.4.0_DE_ClientPlatform~C, 2026-08-25

<cell_status>
| cell | state | evidence |
|---|---|---|
| `D1-h-v1` L0 view | **COMPLETE** | 49F three tiles / inflection two tiles; Alternatives ABSENT (no tile, not an empty one); Insurance never rendered. Screenshots READ. |
| `D1-h-p1` presence | **COMPLETE** | served AUM > 0 is the predicate; a 0-AUM node renders NO TILE. Exercised both directions (SMA present on 49F, absent on inf). |
| `D1-h-v2` L1 drilldown | **COMPLETE, one limb DECLARED** | Models Primary/Custom and the Client predicate panel render from the block. Alternatives' inert+labelled state is NOT-YET-EVALUABLE -- no firm carries Alternatives AUM this round. Declared, not claimed. |
| `D1-h-v3` L2 Custom | **COMPLETE** | 3 rows against 3 members; disclosure rendered, not hidden; plane named on screen after COO 67612. |
| `D1-h-v4` predicate-unavailable | **COMPLETE** | "Fee split unavailable for this firm" + the emitter's own reason; BOTH fee buckets ABSENT and no zero rendered anywhere. |
| `D1-c-1` consumed | **COMPLETE AT THE CONTRACT PLANE** | The page consumes the block via its own query key. NOT a served-artifact proof: category-views is emitted but unpublished, and per `D1-inv-5` a commit is not execution. |
| `D1-c-2` empty fallback | **COMPLETE** | Three states render DIFFERENT text -- consumed / unavailable-at-a-firm / absent-by-scope. The rest of the page is identical across all three, which is exactly why the panel and not the page is the discriminator. |
| `D1-inv-4` (render half) | **COMPLETE** | Sum recomputed FROM THE RENDERED TILES and printed beside `total_aua - Insurance`; closes on both firms. No double count expressible: children are drawn from the emitter's single partition and `held_axes` is never drawn. |

**Proof instance:** `org/tier2_senior/0.4.0_DE_ClientPlatform~C/deliverables/D1_CATVIEWS.TO-R1-DE_PROOF_OF_SPEC.json` -- VALID rc=0 positional (9/9 criteria carry cell_refs; 8/8 cell_refs resolve to the decomp; 8/8 declared cells reachable from a criterion).
**Portal commits (DEV, under my author line):** `760504f0`, `4034239c`, `d1f8f38a`, `cd2f059c`, `7def244d`.
**Evidence discipline:** every fixture was built by exercising `build_category_views` AT REF `23271aac64` in an isolated extraction -- never from the shared working tree (COO standing rule 67436).
**NOT CLAIMED:** a served-artifact read. AC2-AC8 prove the RENDER against the contract at a named ref; they do not prove a live emission, and `D1-inv-5` is why that distinction is stated rather than blurred.
</cell_status>
