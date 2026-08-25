<task_order>
<id>PORTAL_CITYPECHECK.TO-R1-DE.ci-buildmode-typecheck</id>
<project>PORTAL_CITYPECHECK</project>
<issued_to>DE-class lane, seat PENDING (requested from 0.0.0_AB_MSTR ~13:35Z)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P0 TIME-BOXED -- 1.0.0_SA_CTO's sequencing hold on 78d77c03 has an owner and NO DISCHARGE PATH until this lands. Authored by 14:00Z or the hold lifts per CTO's escape valve.</priority>
<date>2026-08-25</date>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/portal-ci-typecheck-buildmode/20260825T133500Z/DECOMP.md</ref>
  <ref type="ruling">1.0.0_SA_CTO 13:30Z -- "seat this NOW, DE lane, one cell"</ref>
  <ref type="law">portal/CLAUDE.md -- already mandates the build-mode form and names the empty-file-set hazard</ref>
</references>
<objective>
ONE TOKEN. portal/.github/workflows/ci.yml:56 changes `run: bun run tsc --noEmit` to
`run: bun run typecheck`. package.json:15 already defines typecheck as `tsc -b --noEmit`.
The bare form compiles ZERO FILES because tsconfig.json has "files": [] with project
references. The oracle is WALL TIME: sub-second becomes ~20s. Do NOT repair the type
errors this surfaces in the same act -- that is a second change.
</objective>
</task_order>

# TASK ORDER — PORTAL_CITYPECHECK.TO-R1-DE · `ci.yml:56` ADOPTS THE BUILD-MODE TYPECHECK

**issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~13:35Z · ⛔ **TIME-BOXED TO 14:00Z**

<decomp_ref>
workflows/atom_decomposition/runs/portal-ci-typecheck-buildmode/20260825T133500Z/DECOMP.md — cells
CIT-a-1, CIT-inv-1, CIT-inv-2, CIT-inv-3
</decomp_ref>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json CITR1DE-AC1,CITR1DE-AC2,CITR1DE-AC3 ; check the rc. -->
  <criterion id="CITR1DE-AC1" cell_refs="CIT-a-1"/>
  <criterion id="CITR1DE-AC2" cell_refs="CIT-inv-2"/>
  <criterion id="CITR1DE-AC3" cell_refs="CIT-inv-1, CIT-inv-3"/>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/PORTAL_CITYPECHECK.TO-R1-DE_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>CITR1DE-AC1,CITR1DE-AC2,CITR1DE-AC3</expected_criteria>
  <alignment_denominators>cells in this TO: 4 (a 1 · inv 3); criteria: 3; every criterion carries >=1 cell_ref; all 4
cells reachable. Unmapped 0; untraceable 0. Decomp total 4; nothing excluded.</alignment_denominators>
</proof_of_spec>

---

## WHY THIS IS P0 FOR A ONE-TOKEN CHANGE

**It is not the size of the change. It is that a CORRECT fix is currently held behind it.** `0.0.0_AB_MSTR` is holding
`78d77c03` (DE~D's lint fix, correct and unpushed) on CTO's sequencing ruling — **and until this exists, that hold has
an owner and no path.** *CTO named that as their own defect and time-boxed it rather than leaving it standing.*

## ACCEPTANCE CRITERIA

| id | criterion | cells | grounding |
|---|---|---|---|
| **CITR1DE-AC1** | `ci.yml:56` reads `run: bun run typecheck`. ⛔ **THE ORACLE IS WALL TIME, NOT THE EXIT CODE: the step moves from sub-second to ~20s.** *A green step that still completes in under a second is a FAILED cell — that state is the defect itself and is indistinguishable from success on every signal except duration.* **Read the duration, not the colour.** | `CIT-a-1` | EXERCISED |
| **CITR1DE-AC2** | ⛔ **DO NOT REPAIR THE TYPE ERRORS THIS SURFACES IN THE SAME ACT.** Landing the correction and fixing what it reveals are **two changes with two review surfaces**. **Whatever appears is the CORRECT COST of restoring a check that has not run — not a regression this cell caused.** Report the count; do not silence it. | `CIT-inv-2` | SOURCE |
| **CITR1DE-AC3** | **NO alarm / monitor / freshness-checker** (moratorium). **Portal main worktree stays on `DEV`** (Rule 19); **`deploy.yml` is NOT edited** — it already runs the correct form and PROD is not exposed. | `CIT-inv-1/3` | SOURCE |

## THE EVIDENCE, SO IT IS NOT RE-DERIVED

Reproduced at **three seats**: `tsconfig.json` has `"files": []` + project references; the bare form never descends.
**277ms / 818ms bare against 21,099ms / 18,782ms build-mode.** `portal/CLAUDE.md` **already bans the bare form** — this
is a written rule the pipeline has been violating, not an undiscovered gap.

## SURPRISE CHANNEL (Rule 27)

One line by MCP to `3.0.0_SA_CVO`, cc me. **BLOCKING routes to me same-turn.** You do not write `org/surprise_channel/**`.
