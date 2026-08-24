# TO ADVI_PERFRP.TO-R1-DE — round 1, DE lane: the shared controls · Books L3 card grid (exactly five) · L4 cards · the advisor Book view · L2 columns · the existing-panels decision · labels / known-not-held · DEV render

<task_order id="ADVI_PERFRP.TO-R1-DE" project="ADVI_PERFRP">
<decomp_ref>workflows/atom_decomposition/runs/advi-perfrp/20260824T201222Z/DECOMP.md @1ce9b2d6bc — cells PRF-d-1, PRF-d-2, PRF-d-3, PRF-d-4, PRF-d-5, PRF-d-6, PRF-d-7, PRF-d-8, PRF-inv-1, PRF-inv-3 (render half). Reads PRF-b-1's contract (TO-R1-DS). Constrained by PRF-g-1 (deferred cards ABSENT), PRF-g-4 (insurance beside, never inside). NOT in this TO: any producer/serving cell; the PROD promote (DT).</decomp_ref>
<certification>**CERTIFIED DECOMP** — `3.0.0_SA_CVO` @62598c1bfb (36/36, no P1). Issuer re-derives on a DECOMP-INVALIDATING item.</certification>
<issued_to>DE-class (portal, `portal/src/pages/AdvisorIntelligence/**` on DEV). **SEATED: `0.4.0_DE_ClientPlatform~D` (MSTR 66575, ADVI_PERFRP ONLY); watches `0.4.0_DS_ClientPlatform~G` for the start condition.** ONE PROJECT PER INSTANCE.</issued_to>
<executor_class>DE-class</executor_class>
<seating_trigger>Spawn call routed to MSTR same turn (66493). **Start condition (OBSERVED): the DS lane's `b-1` contract SKELETON is COMMITTED with its `contract_version`** — `d-1` shared controls begin on the skeleton; card acceptance (AC3–AC8) waits for leaves on DEV. Dark mid-execution → MSTR same turn.</seating_trigger>
<placement>LAPTOP (portal dev-server + screenshot verification). PROD is DT's (`/prod-deploy`); this TO stops at DEV.</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-24T20:3xZ</issued>
<status>ACTIVE (start condition above)</status>
<priority>P1 — the 49F purpose project; wave-2 first.</priority>
<scope_guard>ONE PROJECT. Exactly the cells above. **Advisor + Distribution tabs are OUT — byte-identical is an acceptance criterion, not a courtesy.** No INSURE UI (the Total Assets element is INSURE's cell). Surprises → `3.0.0_SA_CVO` by MCP, cc `2.0.0_SA_COO` (CVO FILES it under `org/surprise_channel/ADVI_PERFRP/`; executing seats do NOT write that tree -- CVO_WORKSPACE lane, ruling 66580), one line. **Nothing to `4.0.0_SA_CRO*` this session.**</scope_guard>
<authority>PRD `docs/architecture/ADVI_PERFRP_PRD.md` v0.3 s.6 (the shape, PINNED from Andrew's recording + 13 screenshots — STRUCTURE only, the inputs stay local) / **s.11 rulings #1–#4, #6–#9, #11 (FIXED)** / s.7 acceptance 8–11.</authority>
<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json PRFR1DE-AC1,...,PRFR1DE-AC13 ; check the rc. -->
    <criterion id="PRFR1DE-AC1" cell_refs="PRF-d-1"/>
    <criterion id="PRFR1DE-AC2" cell_refs="PRF-d-1"/>
    <criterion id="PRFR1DE-AC3" cell_refs="PRF-d-2"/>
    <criterion id="PRFR1DE-AC4" cell_refs="PRF-d-3"/>
    <criterion id="PRFR1DE-AC5" cell_refs="PRF-d-4"/>
    <criterion id="PRFR1DE-AC6" cell_refs="PRF-d-5"/>
    <criterion id="PRFR1DE-AC7" cell_refs="PRF-d-6"/>
    <criterion id="PRFR1DE-AC8" cell_refs="PRF-d-7"/>
    <criterion id="PRFR1DE-AC9" cell_refs="PRF-d-1, PRF-d-2"/>
    <criterion id="PRFR1DE-AC10" cell_refs="PRF-inv-1"/>
    <criterion id="PRFR1DE-AC11" cell_refs="PRF-inv-3"/>
    <criterion id="PRFR1DE-AC12" cell_refs="PRF-d-8"/>
    <criterion id="PRFR1DE-AC13" cell_refs="PRF-d-1"/>
  <expected_criteria>PRFR1DE-AC1,PRFR1DE-AC2,PRFR1DE-AC3,PRFR1DE-AC4,PRFR1DE-AC5,PRFR1DE-AC6,PRFR1DE-AC7,PRFR1DE-AC8,PRFR1DE-AC9,PRFR1DE-AC10,PRFR1DE-AC11,PRFR1DE-AC12,PRFR1DE-AC13</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform~D/deliverables/ADVI_PERFRP.TO-R1-DE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells: 10 (d-1..d-8, inv-1, inv-3); criteria: 13; every criterion ≥1 cell_ref; every cell reachable (d-1 AC1/AC2/AC9/AC13 · d-2 AC3/AC9 · d-3 AC4 · d-4 AC5 · d-5 AC6 · d-6 AC7 · d-7 AC8 · d-8 AC12 · inv-1 AC10 · inv-3 AC11). Unmapped 0; untraceable 0.</alignment_denominators>
</proof_of_spec>
</task_order>

## ⛔ SPEC-AT-PICKUP — YOUR FIRST ACT

| # | Premise | Oracle that would FALSIFY it |
|---|---|---|
| O-1 | The Books surface is the L2→L3→L4 chain with RQ keys `advisor-book-view / -client / -account` | `sed -n 1,25p portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx` |
| O-2 | L3 today = CanonicalBookView · FeeSummaryPanel · TaxCostBasisPanel · AccountsTable + the RFS window (QTD default) | `grep -n -E 'Panel|window' portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookClientDetail.tsx` |
| O-3 | `composition.ts CANONICAL_CLASSES` = `['equity','fixed_income','alternatives']` (never-blend control, not yours to touch) | `sed -n 32p portal/src/pages/AdvisorIntelligence/_shared/lib/composition.ts` |
| O-4 | Portal main worktree on DEV | `git -C portal branch --show-current` → DEV (else `git -C portal checkout DEV` first, Rule 19) |
| O-5 | The DS contract skeleton is committed with a `contract_version` (your start condition) | `git log --oneline -- data/assets/scripts/gold/runners_49f/ \| head` + read the contract's version field |

## Cells

- **`PRF-d-1` SHARED CONTROLS (one component set, reused by every card):** period picker **{QTD, YTD, 1Y, 3Y, SI, custom}** (s.11 #2), level switch (relationship / account), Group by **{Account, Class, Asset}** (#3), Expand / Collapse, Manage Table, **CSV export on every table** (#8), the three footnotes **VERBATIM** (#9): *"shown net of advisory fees"* · *"not held entire period"* · *"annualized"* (>1Y). ⛔ **The renderer's oracle asserts the `contract_version` it built against and REFUSES (fails loud) on a mismatch; a DECLARED-ABSENT column never renders as an empty tile** (CTO ruling 66489 — the seam between `b-1` and your tiles; a field and an assert, not a gate).
- **`PRF-d-2` Books L3 card grid — EXACTLY FIVE** (Activity Summary, Performance, Allocation, Gain/Loss, Transactions) + the Net Worth roster row; each card expands to a detail panel **INSIDE Books, no new routes** (#1, #7). **DEFERRED / GAP cards ABSENT — no empty tiles, no placeholders** (benchmarks, Capital Markets, Allocation vs Target, Projected Income, Fixed Income, Wallet Share, Reports). Gain/Loss renders only when its leaf lands (the DS lane sequences it LAST).
- **`PRF-d-3` Books L4** — the same cards for ONE account; today L4 = `AdvisorBookAccountModal` (721 lines): render the cards in its slot; **extend the modal, do not replace it.**
- **`PRF-d-4` advisorpublicprofile Book view** — 4 KPI tiles (Market Value; Management Fees; Relationships new/lost; Net Flows in/out/net) + 4 summary tabs (Executive, Fees, Relationships, Net Flows); **Wallet Share OUT** (#4); the `canSeeBookToggle` permission gate UNCHANGED; tile values == the DS `b-6` leaf by join, no second computation.
- **`PRF-d-5` Books L2 list** gains the `b-6` client-table columns.
- **`PRF-d-6` THE EXISTING PANELS — DECISION FIXED** *(premise re-confirmed 2026-08-24: DE~D's stale-premise flag was WITHDRAWN by its author — `TaxCostBasisPanel` IS rendered at L3 via `panels/CanonicalBookView.tsx:133-155`, one composition level below `AdvisorBookClientDetail.tsx`; execute as written)*: the RFS window (QTD default, ADVI_FNTEND.B2) **BECOMES the shared period picker's state — one window state, not two** (two would make two panels disagree on "QTD"); FeeSummaryPanel + AccountsTable persist beside the cards; **TaxCostBasisPanel is superseded by the Gain/Loss card ONLY when that leaf lands — until then it stays.**
- **`PRF-d-7` labels + known-not-held:** SI labelled *"since 2024-07-08"* with the STITCH tier's label slot reserved; a Fidelity / position-only account renders **known-not-held with custodian** (s.7 #10) — never omitted, never `0`.
- **`PRF-inv-1`** Advisor + Distribution tabs **BYTE-IDENTICAL** (build-output diff of `AdvisorsTab` / `DistributionTab` bundles = 0 bytes changed).
- **`PRF-inv-3` (render half)** L2 / Book view == Σ L3 == Σ L4 as DISPLAYED, by join; relationship→account only (advisor→firm is NEVER computed — R-p5).
- **`PRF-d-8`** DEV render as leaves land; **screenshot READ** (silver-canvas colour law); **PROD exposure rides the 49F switch promote** (#11) — no promote here, no new gate; the CVO parity report accompanies the render.

## Mandate
1. `comp-transform schema-check AdvisorBookView` / `AdvisorBookClientDetail` / `AdvisorPublicProfile` (MISSING = runtime undefined) + `comp-cache` collisions on the new RQ keys. Rule 20(b).
2. Portal main worktree on DEV (Rule 19). `bun run typecheck` clean before every commit.
3. `/frontend-dev` screenshot verification — READ it.

## Acceptance criteria

| id | criterion | cell_refs | grounding |
|---|---|---|---|
| **PRFR1DE-AC1** | schema-checks clean; `comp-cache` re-run; DEV branch confirmed | PRF-d-1 | SOURCE |
| **PRFR1DE-AC2** | Shared controls carry the RULED enums (periods 6, groupings 3), CSV export on every table, the three footnotes verbatim | PRF-d-1 | EXERCISED |
| **PRFR1DE-AC3** | L3 renders EXACTLY five cards + roster row; a grep for every deferred card name in the L3 tree == 0; detail panels open in-Books, `git diff` shows no new route | PRF-d-2 | EXERCISED |
| **PRFR1DE-AC4** | L4 cards render inside the extended `AdvisorBookAccountModal` from the account-level leaf | PRF-d-3 | EXERCISED |
| **PRFR1DE-AC5** | Book view: 4 tiles / 4 tabs; Wallet Share absent; tile values == `b-6` leaf; `canSeeBookToggle` tests unchanged | PRF-d-4 | EXERCISED |
| **PRFR1DE-AC6** | L2 list column set == the `b-6` client-table set | PRF-d-5 | EXERCISED |
| **PRFR1DE-AC7** | ONE window state variable feeds the picker AND the legacy RFS consumers (`comp-find` shows one); TaxCostBasisPanel present until the Gain/Loss leaf exists | PRF-d-6 | SOURCE + EXERCISED |
| **PRFR1DE-AC8** | SI label rendered; known-not-held fixture renders with custodian; no `0` where the value is unknown | PRF-d-7 | EXERCISED |
| **PRFR1DE-AC9** | `contract_version` assert EXERCISED: a mismatched-version fixture → the renderer REFUSES loud; a declared-absent column → no tile (mutant: an absent column forced into a tile fails the test) | PRF-d-1, PRF-d-2 | EXERCISED (mutant) |
| **PRFR1DE-AC10** | ⛔ **RESTATED AT SURFACE GRAIN 2026-08-24 ~21:5xZ by the ISSUER on your 66697/66707** (the bundle oracle is UNRUNNABLE — one chunk carries both protected tabs and your `d-4` target; decomp `PRF-inv-1` corrected at source, so the next round cannot re-derive it). Three parts, ALL required: **(a) SOURCE** `git diff` over `tabs/AdvisorsTab.tsx` + `tabs/DistributionTab.tsx` + their NON-SHARED closure = 0 changed lines, closure file-count PRINTED; **(b) CONFINEMENT** every `d-4` edit inside the Book-face branch at `AdvisorPublicProfile.tsx:1201` `hideBookToggle = !canSeeBookToggle(permissionScope)`, Profile-face path provably untouched; **(c) RENDER** `/frontend-dev` screenshot of BOTH tabs pre/post, READ, identical — **capture the PRE-state baseline NOW, before any edit** (your offer, accepted: cheap today, unreconstructable later) | PRF-inv-1 | SOURCE + EXERCISED |
| **PRFR1DE-AC11** | Displayed L2 == Σ L3 == Σ L4 by join (relationship→account); no double count expressible; advisor→firm never displayed as a sum | PRF-inv-3 | EXERCISED |
| **PRFR1DE-AC12** | Screenshot READ on record + colour law; `git -C portal ls-remote origin PROD` unchanged | PRF-d-8 | EXERCISED |
| **PRFR1DE-AC13** | `bun run typecheck` clean; `safe-commit.sh` on DEV under your author line; proof instance VALID rc=0 positional | PRF-d-1 | SOURCE |

## Do not
No PROD promote · no benchmark rows (P-7 deferred; slot reserved, nothing rendered) · no second computation of any figure · no touch to `composition.ts` · nothing on the Advisor / Distribution tabs.

## Status + reporting
Cell-level `<cell_status>`; proof instance + flip = one commit. Report to COO per flip (hash + push state); cc `3.0.0_SA_CVO` at AC9/AC10/AC11; cc the DS PERFRP lane at render-verified. Surprises: `3.0.0_SA_CVO` by MCP, cc `2.0.0_SA_COO` (CVO FILES it under `org/surprise_channel/ADVI_PERFRP/`; executing seats do NOT write that tree -- CVO_WORKSPACE lane, ruling 66580).
