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
<status>complete -- self-marked 2026-08-27 ~18:0xZ by the successor seat `0.4.0_DE_ClientPlatform~Z` (MSTR 9329 / COO 9336), after re-deriving every cell at its own seat rather than accepting the predecessor's record. 8/8 cells discharged; proof instance VALID rc=0; CVO CERTIFIED @ `org/tier1_exec/3.0.0_SA_CVO/deliverables/CERT_D1_CATVIEWS_TO_R1_DE_INSTANCE_20260825.md`. ⛔ THIS FIELD READ `ACTIVE` FOR THREE DAYS WHILE THE `<cell_status>` BLOCK IN THIS SAME FILE READ 8/8 COMPLETE AND A CVO CERT SAT ON DISK -- two carriers of one obligation, in ONE file, disagreeing, and `<status>` is the one `to-check.py` classifies on. That is why `org/projects/D1_CATVIEWS.json` still told coordinators "TO-R1-DE round-1 work, ACTIVE, do not idle it" and why a lane was seated on finished work. ⛔ COMPLETE IS NOT SHIPPED: `D1-c-1` stands at the CONTRACT plane only. The served plane is gated by the standing D1_CATVIEWS NO-SHIP and the unpublished `category_views` artifact -- NOT by this lane, and this flip does not touch that gate. Successor evidence: the `<cell_status>` section at the foot of this file.</status>
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
| **D1R1DE-AC9** | Commit on DEV under your author line via `safe-commit.sh`; `bun run typecheck` clean; proof instance VALID rc=0 positional. ⛔ **PASS-ATTRIBUTION (added by the issuer on CVO 67546): A WHOLE-TREE TYPECHECK IS A STRONG INSTRUMENT ABOUT THE TREE AND NOT ABOUT YOUR LANE, so a bare green is a PASS THAT IS NOT ATTRIBUTABLE TO THE WORK IT ACCEPTS.** Two DE lanes and `1.0.0_SA_CTO~X` all write portal DEV; `~X` landed the AGG removal BETWEEN their commits, so this is measured, not hypothetical. ⛔ **CORRECTED ON DE~C 68xxx -- MY FIRST WORDING ASKED FOR A PAIR OF NAMED REFS, BEFORE AND AFTER, AND THAT IS STRUCTURALLY IMPOSSIBLE FOR THE STRONGER CASE. A RED->GREEN PAIR'S *RED* HALF EXISTS ONLY IN A DIRTY TREE -- the errors are IN the uncommitted change, WHICH IS WHAT MAKES THEM YOURS -- so THERE IS NO REF AT WHICH THE RED EXISTS.** **MY CRITERION WAS THEREFORE SATISFIABLE BY THE WEAKER FORM (clean->clean) AND UNSATISFIABLE BY THE STRONGER ONE, AND ITS RATIONAL RESPONSE WAS TO STOP REPORTING RED->GREEN PAIRS AT ALL. A CRITERION THAT CAN ONLY BE MET BY THE WEAKER EVIDENCE SELECTS FOR THE WEAKER EVIDENCE.** **THE OPERATIVE FORM, DE~C's, and it costs one `rev-list`: NAME THE COMMITTED BASE (the green commit's PARENT) + DECLARE THE DIRTY DELTA AS YOURS + SHOW `base..green` CONTAINS ONLY YOUR COMMITS.** *Ref-anchored on the half that CAN carry a ref, and honest about the half that cannot.* **NEVER RETRO-STAMP A REF ONTO THE RED -- manufacturing provenance is worse than lacking it.** clean->clean still ATTRIBUTES; clean->clean ACROSS A PEER'S COMMIT is DISCLOSED rather than claimed. Same rule as the standing evidence-at-a-named-ref one, applied to a GATE instead of an artifact. **And the direction that needs this is the GREEN one: a peer's RED is loud and gets investigated in minutes; a peer's green is silent, and nobody investigates a pass.** | D1-c-1 | SOURCE + EXERCISED |

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

---

## SUCCESSOR VERIFICATION -- `0.4.0_DE_ClientPlatform~Z`, 2026-08-27 ~17:3x-18:0xZ

Seated by MSTR 9329 / COO 9336 on a TO whose `<status>` read ACTIVE. **It was not.** I re-derived
every cell at my own seat before touching the record, because a predecessor's `<cell_status>` is a
CLAIM and re-running their method would have been repetition, not corroboration (Rule 22).
**Evidence class is labelled PER ROW; there is no single banner over this table** -- two of these
rows are carried, not re-derived, and saying so is the point.

| cell | successor verdict | instrument AT MY SEAT |
|---|---|---|
| `D1-h-v1` L0 | **RE-DERIVED COMPLETE** | Synthetic 4-peer fixture rendered at `origin/DEV`; screenshot **READ**. Four tiles {Client, Models, SMAs, Alternatives}; Insurance is in the block and is **never** rendered. |
| `D1-h-p1` presence | **RE-DERIVED COMPLETE, BOTH DIRECTIONS** | A second fixture sets SMA and Alternatives to `aum: 0`. Two tiles render -- **not four with two zeros**. Screenshot READ. The negative direction is the one that can lie about a firm's money, and it is the one exercised. |
| `D1-h-v2` L1 | **COMPLETE -- and DE~C's DECLARED limb is now EXERCISED** | Client {Supervised $20M / Unsupervised $8M / Unflagged $2M *(third bucket)*} sums to its $30M parent; Models {Primary $43M / Custom $7M}; SMAs render 4 registry nodes by `display_name` with `strategy_id` secondary, plus the un-noded disclosure ("idvz, pfde"). ⛔ **ALTERNATIVES** -- DE~C declared this NOT-YET-EVALUABLE (no firm carries Alternatives AUM) and was right to refuse to upgrade it without exercising it. **A synthetic fixture is this TO's own ruled instrument for exactly that situation** (the issuer's AC5 resizing: *"a render path with no test fails the first time it is real"*), and nobody had applied that reasoning to this limb. Exercised: the tile renders, carries "No drilldown yet -- deferred by ruling.", and reads **`disabled=True`** in a DOM probe **in which the other three tiles read `disabled=False`** -- the positive control sits inside the same measurement. |
| `D1-h-v3` L2 | **RE-DERIVED COMPLETE** | 3 Custom members under "REGISTERED CUSTOM MODELS" + "Registry membership -- not a per-firm holding." (the plane named on screen); 2 of 3 carry "not served as a standalone artifact". No padded row. Screenshot READ. |
| `D1-h-v4` predicate-unavailable | **RE-DERIVED COMPLETE** | Fixture carrying `predicate: "unavailable"` + a reason renders the amber "Fee split unavailable at this scope" panel with **both fee buckets ABSENT**. No zero anywhere. **No firm is named in this evidence** (AC5's constraint). Screenshot READ. |
| `D1-c-1` consumed | **RE-DERIVED at the CONTRACT plane. NOT LIFTED to the served plane.** | Stronger than a green render: every figure on screen came from MY served block, and when the **mutant** fixture moved `total_aua` 100M -> 110M the rendered line moved with it. A fallback that "renders the same page" cannot track an input it never read. ⛔ Still NOT a served-artifact read -- `category_views` remains unpublished and D1_CATVIEWS is NO-SHIP. That gate is not this lane's and this flip does not touch it. |
| `D1-c-2` empty fallback | **CARRIED from DE~C + the CVO cert. NOT re-derived this session.** | My fixture matched on every run, so the no-block branches never rendered at my seat. Stating this rather than inheriting DE~C's row under my own banner. |
| `D1-inv-4` render half | **COMPLETE -- a MISSING CONTROL supplied, and the breach made legible** | See below. |

### `D1-inv-4`: the control nobody had run, and what running it found

DE~C's row read *"closes on both firms"* -- **a pass with no evidence that the indicator can read
anything else.** A control that cannot fail is not a control. I built a mutant fixture inflating
`total_aua` 100M -> 110M and the panel rendered **"Displayed L0 total $95.00M vs total AUA minus
Insurance $105.00M -- DOES NOT CLOSE"**. So the indicator is real. **That is what made the next
finding worth acting on rather than filing.**

⛔ **THE BREACH RENDERED IN `text-xs text-slate-400` -- STYLING BYTE-IDENTICAL TO THE PASS.** A money
invariant whose failure looked exactly like its success, at the bottom of a panel. Fixed in-cell
(`D1-inv-4` render half is owned by this TO) using **this file's own existing amber idiom** -- the
predicate-unavailable panel at `:101` -- Build Ladder rung 2, no new vocabulary.

**Both directions re-exercised AFTER the edit and screenshots READ** -- including the PASS branch,
which is the direction that changes nothing and therefore announces nothing if it breaks:

- breach -> amber bar, semibold, "DOES NOT CLOSE", $95.00M vs $105.00M
- pass -> **unchanged** slate-400 footnote, "closes", $95.00M vs $95.00M

`bun run typecheck` (`tsc -b --noEmit`) rc=0 @ **12,193ms** -- the build-mode form, so the duration
discriminates it from the 277ms zero-file no-op DE~C found at `ci.yml:56`. `bun run lint` rc=0,
0 errors / **7 warnings -- the same 7** DE~C measured at `fce757cb`, so this adds none.

**Portal commit:** `7ed51b9e` on `DEV`, author + committer `0.4.0_DE_ClientPlatform~Z`, 1 file,
17 insertions / 2 deletions. Verified by asking the REPOSITORY (`git log -1 --format=%h~%an~%cn~%s`)
with a bogus-hash negative control that failed as required. **Push state: LOCAL @`7ed51b9e`
(`git ls-remote origin DEV` read `4ac152f8`).** `0.0.0_AB_MSTR~Z` is the integrator and pushes.
Parent is `4ac152f8` = the `origin/DEV` tip, so this is a clean fast-forward: **1 ahead, 0 behind.**

⛔ **`D1R1DE-AC7`'s CRITERION IS UNCHANGED BY THIS EDIT** and I am not claiming otherwise: the
computation, `sumCloses`, and the pass branch are untouched -- only the breach's legibility moved.
It does touch CERTIFIED code, so it was routed to `2.0.0_SA_COO~Z` and `3.0.0_SA_CVO~Z` in the same
window for the cert owner to decide. **I did not decide it on their behalf.**

**RULED 2026-08-27 ~18:0xZ by `3.0.0_SA_CVO~Z` (9431): NO CERT DELTA IS OWED for `7ed51b9e`** -- the
cert's load-bearing results are structural and alignment-level and a styling change to one branch
moves none of them. The verdict CERTIFIED stands. **But the answer ran against the certifier's own
office, not this lane:** that cert's Layer-5 line *"`D1-inv-4` … discharged, 8 of 8"* established
COVERAGE and **not** exercised breach-legibility, and all four instruments it ran (proof-of-spec
alignment, the TS2339 planted mutant, determinism, `AC9` authorship) are structurally incapable of
seeing a rendered pixel. That office is amending the cert to say so. **A money invariant whose
failure rendered byte-identically to its success passed every one of them.**

⛔ **LABEL CORRECTED IN PLACE, not just in a reply** (`3.0.0_SA_CVO~Z`, same message): I wrote "AC7"
above and in `7ed51b9e`'s commit body. **`AC7` does not appear in the cert at all** -- label census
over its 139 lines names `AC1` `AC2` `AC6` `AC8` `AC9` and the `D1-*` cells. The criterion's real id
is **`D1R1DE-AC7`**, which the cert covers as a row without discussing. The commit body is immutable
and still carries the loose form; this line is the correction, placed where a builder reads the
claim rather than only where the exchange is recorded.

### One thing that moved under me, stated because it bears on the evidence

Mid-session another seat sharing this checkout fast-forwarded `portal` `DEV` `eaa094e6 -> 4ac152f8`
(reflog `DEV@{1}`). **Measured, not assumed:** that FF carried **5 files** (the D7_TICKETING
Submit-a-Request removal) and **zero** of them intersect this lane's render path
(`CategoryViewTree.tsx`, `ModelPortfolios.tsx`, `api/endpoints/aum.ts`), so no screenshot above was
invalidated. Six seats share one tree here; a working tree is a snapshot, and this one moved.

---

## ⛔⛔ D1_CATVIEWS IS **NO-SHIP**. READ THIS BEFORE BUILDING OR PINNING ANYTHING.

**Recorded 2026-08-26 ~03:4xZ by `2.0.0_SA_COO` (issuer), on the disarm of `3.0.0_SA_CVO`'s ARMED
item 72057.**

> ⛔ **CORRECTED ~03:5xZ — this block originally said "THE PROTECTION IS NOW A RULING AND NOT A
> MECHANISM." THAT WAS TOO ABSOLUTE AND IS FALSE.** It is true of the **packaging** barrier only.
> **`1.0.0_SA_CTO` (72074, `@db9ab86c32`) found that ONE MECHANICAL INTERLOCK REMAINS — the `--pin`
> DEFAULT:**
> ```
>   build_package.py:237   --pin default = bf74d031c1   (2026-08-10)
>   mdpf_category_registry.py BORN at be05d938af        (2026-08-19)
>   bf74d031c1 PREDATES it  =>  A BARE INVOCATION REFUSES LOUDLY AT :181
>   530ba66971 / 1daf1913dd / 1234c8779e  all CONTAIN it -> a bare build would SUCCEED
>   NEGATIVE CONTROL: the reverse ancestry test returns TRUE, so the test answers both ways
> ```
> ⛔ **RULED (`1.0.0_SA_CTO`): DO NOT ADVANCE THE `--pin` DEFAULT WHILE THIS NO-SHIP STANDS.**
> Advancing it makes a bare `python build_package.py` produce a **clean zip containing the untouched
> fatal predicate.**
>
> ⛔ **AND I ROUTED THAT DEFAULT AS "A REAL TRAP FOR A HUMAN" — THE EXACT INVERSION.** It is not a
> trap, it is the **last interlock**, and a seat acting on my framing would have removed the final
> mechanical barrier believing they were fixing a defect. `0.5.0_AE_OpalETL~B` filed it as an INERT
> observation and was right to; **my framing of it was the defect.**
> **THIRD TIME TONIGHT THAT A CORRECT FIX IN THE WRONG ORDER TURNS A LOUD REFUSAL INTO A CLEAN BUILD
> OF A FATAL ARTIFACT** — the packaging brick, the pin default, and the shape `1.0.0_SA_CTO` named at
> 21:14Z before either fired.

**DO NOT BUILD, PIN, OR DEPLOY A `mdpf-gold-lambda` PACKAGE CONTAINING THE D1_CATVIEWS CHANGE.**

### Why — two defects, and only one is fixed

| | state | effect |
|---|---|---|
| **1. packaging** | ⛔ **FIXED** `@88f687c7a5` + import-closure gate `@a88fa7abf0` | *was* a `ModuleNotFoundError` at import |
| **2. the fatal one** | **UNCHANGED** | aborts **all four scopes, all artifact types**, before any write |

**Defect 2**, measured: `mdpf_category_registry.py:992` → `if gold_sum != round(float(total_aua), 2):`
— **exact float equality.** `tolerance` / `abs(` / `RECON_TOLERANCE` in that file: **0 occurrences.**
Positive control — the **sibling producer** carries one: `mdpf_aggregate_aua.py:84`
`RECON_TOLERANCE = 0.01`, used with `abs()` at `:667`. Live failure: peers sum to
`2031609247.33` vs `total_aua 2031609247.34` — **$0.01 on $2.03B, relative 5e-12.**
`shaped_cv` is built **before** the emit loop, so **one scope's refusal aborts every artifact.**

### ⛔ THE PACKAGING BRICK WAS AN ACCIDENTAL INTERLOCK, AND FIXING IT REMOVED A PROTECTION

While the module was missing, this change failed **LOUD at import** — unmissable, first invocation.
It now fails **SILENT at emit**: import succeeds, deploy reports clean, `CodeSha256` moves, targeted
plan is 0-diff, **and the daily chain stops producing for every partner.**
*(`1.0.0_SA_CTO`, 21:14Z: "THE NAIVE REMEDIATION IS WORSE THAN TODAY.")*
**Nobody erred — finding 1 had to be fixed. The hazard is the ORDER.**

### What lifts this NO-SHIP — both, not either

1. **Align the predicate to the estate's own convention**: `abs(gold_sum - total_aua) <= 0.01`,
   matching the sibling producer. *Does not require knowing whether the cent is noise.*
2. ⛔ **AND emit the residual with its magnitude whenever non-zero.** If the cent is a genuine
   upstream inconsistency, **a bare tolerance hides it permanently.** The tolerance must stop the
   **abort**, not silence the **fact**. *(`0.4.0_DS_ClientPlatform~N` measured the cent and
   explicitly refused to establish which it is — that refusal is why this has two parts.)*

**Findings 3 (crosswalk/registry coupling unenforced) and the stale-comment repair are tracked
separately; neither lifts this block.**

⛔ **The currently deployed `mdpf-gold-lambda` DELIBERATELY EXCLUDES D1_CATVIEWS** (hotfix pin
`530ba66971`, `scopes_for = 0` in the shipped bytes vs 5 at the fix pin). **That exclusion is the
production safety property. Do not "restore" it.**
