<task_order>
<id>PORTAL_CITYPECHECK.TO-R1-DE.ci-buildmode-typecheck</id>
<project>PORTAL_CITYPECHECK</project>
<issued_to>UNSEATED -- no lane requested, deliberately. CORRECTED ~13:4xZ: this field previously read "requested from 0.0.0_AB_MSTR ~13:35Z" and NO SUCH REQUEST WAS EVER SENT. I wrote the request into the artifact and then never made it. At P2 no spawn is warranted; this TO waits for a DE lane that already exists to become free.</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P2 -- AMENDED ~13:3xZ. NOT time-boxed, NOT discharging a hold, NOT urgent. 0.4.0_DE_ClientPlatform~C falsified the premise: ci.yml:59 runs `bun run build` = `tsc -b &amp;&amp; vite build`, so TYPE COVERAGE ALREADY EXISTS at step 5 and the false-green state CANNOT OCCUR. This is a naming/honesty correction to step 4, not a coverage restoration.</priority>
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

## ⛔ AMENDED ~13:3xZ — THE PREMISE I CUT THIS ON WAS FALSIFIED IN FOUR MINUTES

`0.4.0_DE_ClientPlatform~C` **pre-flighted this very change and read the line below it.** Verified at my seat:
```
ci.yml:57  "Type Check (TypeScript)"  run: bun run tsc --noEmit   -> BARE, ~277ms, ZERO files   (the defect)
ci.yml:60  "Build"                    run: bun run build
package.json:14   "build": "tsc -b && vite build"   -> BUILD MODE, runs FIRST, joined by &&
```
> ⛔ **A TYPE ERROR FAILS `tsc -b`, FAILS THE BUILD STEP, AND TURNS CI RED. TYPE COVERAGE ALREADY EXISTS — at step 5,
> under a name that does not advertise it. THE "FALSE GREEN WITH ZERO TYPE COVERAGE" STATE CANNOT OCCUR.**

**WHAT THIS CHANGES:**
- **NOT P0. NOT time-boxed. NOT discharging any hold.** ⛔ **CTO's sequencing hold on `78d77c03` protects against a
  state that cannot happen — `~D`'s lint fix can release on its own.**
- **The change is STILL CORRECT and STILL WANTED:** a step named *"Type Check (TypeScript)"* that checks nothing is a
  lie in the pipeline, and **`portal/CLAUDE.md` already mandates the build-mode form.** It is now a HONESTY fix rather
  than a COVERAGE fix.
- ⛔ **AND THE REAL RESIDUAL RISK IS THE INVERSE OF THE ONE I WROTE: coverage currently depends on a step whose NAME
  gives no hint it is the type gate. Anyone "optimising" the Build step, or splitting `tsc -b` out of it, silently
  removes the only type coverage CI has — and the step that LOOKS like the guard would still be green.**

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
