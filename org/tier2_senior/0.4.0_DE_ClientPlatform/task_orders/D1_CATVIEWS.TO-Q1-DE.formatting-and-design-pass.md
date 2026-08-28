# TO D1_CATVIEWS.TO-Q1-DE — the FORMATTING / DESIGN pass on the Model Portfolios frontend (Andrew's item 1, second half)

<decomp_ref>workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md — `D1-c-1` (portal consumes: *"five views render"* → the L0/L1/L2 tree renders, `v1..v4`) and `D1-c-2` (empty-block fallback, UNCHANGED by this TO). **NO new cell** — this is a QUALITY pass over the surface `D1-c-1` already declares.</decomp_ref>
<certification>Rides the existing certified `D1_CATVIEWS` decomp. No cell added.</certification>
<issued_to>0.4.0_DE_ClientPlatform~C</issued_to>
<executor_class>DE-class (portal, `portal/**` on DEV)</executor_class>
<seating_trigger>⛔ **NEW LANE — `~C` for CATVIEWS, letter measured free** (spawn audit carries only `~Y` and `~Z` for this base across 388 lines). **Rule 27 requires it: `~Z` is on `ETFS_INGEST`, `~S` on `ETFS_SATELLITES`. `D1_CATVIEWS` is a third project.**</seating_trigger>
<placement>SITE Z (Rule 26). ⛔ `portal/` is a WORK-SITE, never a base. **Main tree stays on DEV (Rule 19).**</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T01:4xZ</issued>
<status>complete -- CERTIFIED 5/5 by 3.0.0_SA_CVO~Z @48485575ff; RAVC-closed by 2.0.0_SA_COO~Z (msg 12077). Self-marked by the assignee per org/XXX.md (driver ask msg 12429). CODE IS ON ORIGIN: portal origin/DEV @8c2ba9bb carries f93fb832, pushed by 0.0.0_AB_MSTR~Z under GATE 5 (a DEV push is INTEGRATOR-only; DT owns the separate PROD PROMOTE) -- verified at this seat by ls-remote plus a CONTENT read of the remote tip with negative controls, not by ancestry alone. EVIDENCE: workspace ad7580bee8 -- 11 READ renders + TQ1_AC_RECORD.md. STANDING, and none of it this lane's: D1_CATVIEWS remains NO-SHIP (blocks SHIP not BUILD, untouched, no met condition read as a lift); the PROD promote is held at Andrew's word; and Andrew's item-1 bar is HIS EYE per 1.0.0_SA_CTO~Z. LANDING ON origin/DEV IS A BRANCH STATE, NOT A DELIVERY -- re-measured at source here, not taken on relay: ci.yml is the ONLY workflow triggering on a DEV push and has ZERO publish verbs (its lone upload is a CI artifact), while deploy.yml alone does s3 sync + a CloudFront invalidation and triggers on PROD only. THERE IS NO DEV SITE. His eye is therefore reachable only by a LOCAL RUN (cd portal && bun run dev) or a PROD PROMOTE, which is DT-lane and held at his word. I previously wrote that landing the code made his bar REACHABLE; that was wrong, and 5/5 plus a certificate plus a branch is not his eye.</status>
<priority>P1 — half of a sovereign instruction. ⛔ **Named twice by `1.0.0_SA_CTO~Z` (11505 §B, 11617 cell 2) and picked up ZERO times.** That is why it is cut now rather than after the P0s.</priority>
<authority>**ANDREW-DIRECT 2026-08-28 ~01:3xZ, VERBATIM:** *"1.) Finalizing the Asset Clasification data flows for 'Model Portfolios' and **appropriately improving the formatting/design of the frontend for that function**."*</authority>

---

## 1. THE SURFACE

Measured by `1.0.0_SA_CTO~Z` (portal @`f1180aad`):
`portal/src/pages/ModelPortfolios.tsx` · `portal/src/components/CategoryViewTree.tsx` ·
`portal/src/api/endpoints/aum.ts`

## 2. ⛔ THE TWO CONSTRAINTS — settled, so you do not re-derive them

**(A) NO ACCEPTANCE CRITERION IS INVENTED, AND YOU MUST NOT INVENT ONE.**
His word is **"improving"** — a **QUALITY bar on an existing surface, not a correctness bar** — and he
attached no metric. ⛔ **Do not manufacture one** (no "reduce clicks by N", no invented density or
spacing target, no scorecard). **His eye is the bar**, the same shape as D4's smoke test.
⭐ **What this DOES mean: your deliverable is a RENDERED ARTIFACT HE CAN LOOK AT**, not a description of
improvements. **A written summary of design changes is not the deliverable.**

**(B) THE INSTRUMENT IS A RENDERED SCREENSHOT, NOT A GREP.**
⛔ **A contrast defect on the silver canvas is invisible to every static check this estate owns.** Use
`/frontend-dev`: render the route headlessly and **READ the screenshot**.
⚠ **THE CANVAS IS SILVER.** Light text or ghost-white buttons **outside a dark Panel** are the **#1
recurring portal defect** (Andrew-direct 2026-07-15, TicketCenter incident). **Check it by looking.**

## 3. ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `TQ1-AC1` | **A RENDERED BEFORE AND AFTER.** Two read screenshots of the same route at the same viewport. ⛔ **Both READ by the executing agent, not merely captured** — an unread screenshot is a file, not an instrument. | `D1-c-1` | |
| `TQ1-AC2` | ⛔ **SILVER-CANVAS COMPLIANCE, VERIFIED BY LOOKING.** No light text or ghost-white control outside a dark Panel. **State it as an observation from the read image**, never from a class-name grep. | `D1-c-1` | |
| `TQ1-AC3` | **THE FIVE VIEWS STILL RENDER.** `D1-c-1`'s `v1..v4` plus the L0/L1/L2 tree, and `D1-c-2`'s empty-block fallback, are **unchanged in behaviour**. ⚠ **A formatting pass that silently drops a view is the failure mode here** — exhibit each view, do not assert the set. | `D1-c-1` `D1-c-2` | |
| `TQ1-AC4` | **NO DATA-PLANE CHANGE.** ⛔ This TO touches **presentation only**. `aum.ts` may be read; **a change to what it REQUESTS or how the payload is shaped is out of scope** and belongs to the data-flow half. Show the diff is confined to presentation. | `D1-c-1` | |
| `TQ1-AC5` | **TYPESCRIPT CLEAN.** `tsc -b` zero errors — the language-appropriate instrument. ⛔ **`commit-gate` reads `.py`/`.sh`/`.tf` and will report "checked 0 of N files" on a frontend diff; that line is NOT evidence of a clean gate.** | `D1-c-1` | |

## 4. NOT YOURS

- ⛔ **The NO-SHIP lift.** `build_package.py:266` — it lifts **ONLY by name, by a COO/Andrew ship
  ruling.** No such ruling exists. **Build freely; do not ship, and do not read any met condition as a
  lift** ("a disarm condition being met is not a ship ruling").
- ⛔ **The Asset Classification DATA FLOWS** — item 1's *first* half, a different lane.
- ⛔ **`ETFS_SATELLITES` / `ETFS_INGEST`** — other projects, other instances. **Rule 27.**
- ⛔ **The PROD promote** — DT lane, Rule 19.

## 5. REPORTING

Deliverable + the screenshots + proof instance in this lane's `deliverables/` via
`.tools/safe-commit.sh --author "0.4.0_DE_ClientPlatform~C <0.4.0_DE_ClientPlatform~C@opal.agent>"
-F <msgfile>` (non-shell writer). Report to `2.0.0_SA_COO~Z`; `3.0.0_SA_CVO~Z` certifies.
⭐ **Because his eye is the bar, say plainly in the report what you changed and what you deliberately
left alone** — the second half is what lets him disagree cheaply.

<proof_of_spec>
  <criterion id="TQ1-AC1" cell_refs="D1-c-1"/>
  <criterion id="TQ1-AC2" cell_refs="D1-c-1"/>
  <criterion id="TQ1-AC3" cell_refs="D1-c-1,D1-c-2"/>
  <criterion id="TQ1-AC4" cell_refs="D1-c-1"/>
  <criterion id="TQ1-AC5" cell_refs="D1-c-1"/>
  <expected_criteria>TQ1-AC1,TQ1-AC2,TQ1-AC3,TQ1-AC4,TQ1-AC5</expected_criteria>
  <alignment_denominators>cells declared: 2 (D1-c-1, D1-c-2); criteria: 5. FORWARD — 5 of 5 carry >=1 cell_ref. BACKWARD — 2 of 2 reachable (D1-c-1 from all five, D1-c-2 from AC3). Unmapped 0; untraceable 0. NOTE: no cell is added. This is a QUALITY pass over the surface `D1-c-1` already declares, and the criteria are deliberately about EXHIBITING the rendered result rather than scoring it — the sovereign attached no metric and one must not be invented.</alignment_denominators>
</proof_of_spec>
