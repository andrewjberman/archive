<task_order>
<id>MDPF_3FIRMS.GC-W45</id>
<title>W-4 + W-5 — make count provenance VISIBLE at render, and make the count type contract tell the truth (nullable) at EVERY layer, not only the two lines the brief named</title>
<project>MDPF_3FIRMS</project>
<workstream>Global-Count closeout (MDPF_REVAMP_GLOBAL_COUNT_CLOSEOUT.md) — the ONE limb independent of W-1</workstream>
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T14:05Z</issued_at>
<status>staged</status>
<authorization>Andrew-direct ~1310Z at CTO's terminal ("have COO decompose those to the relevant agents, and call MSTR for spawn") -> CTO PRD @5d7522128 -> COO decomposition. SCOPE-BOUNDED: MDPF_REVAMP_GLOBAL_COUNT_CLOSEOUT W-1..W-7 only. The broader MDPF_3FIRMS_PRD decomposition REMAINS HELD on Andrew's word (LD-0333) — do not let the two merge.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_REVAMP_GLOBAL_COUNT_CLOSEOUT.md — W-4 (§6), W-5 (§4.4), Defect B (§3.2), acceptance criteria (§6)</ref>
  <ref type="input">DE P1 consumption map @b65625769 (CTO ACCEPTED 135700Z) — the write denominator + APPLIED serving path</ref>
  <ref type="ruling">CTO F-1 @135700Z: ONE ACCESS PATH + a required explicit `basis` sibling, rejectable on a field not a heuristic. CTO folded DE's F-3 (49F/INF have no working provenance channel) INTO W-4 so both are solved once.</ref>
</references>

<scope>
**WHY THIS RUNS NOW AND NOT BEHIND W-1.** Every other limb in this wave is held on W-1's measurement.
These two are not, and that is a deliberate exploitation of a real independence: `count_provenance` is
**already served per-date** and the FE simply does not read it. Nothing about making provenance visible
depends on knowing which cells were missing on which of the 40 null dates.

**W-4 — PROVENANCE MUST BE VISIBLE AT RENDER.**
Today a `band_2firm` point and a `measured` point are pixel-identical. The chart therefore asserts a
uniform series over three different bases (measured 382 / exempt_absorbed 38 / band_2firm 24 /
lag_window 2 / frontier_stamp 1). **The data to fix this is already on the wire** — this is a
consumption gap, not a data gap.
Per CTO's F-3 fold: 49F and INF have **no working provenance channel** at all. Solve that in the same
pass, not as a follow-on — one mechanism, three firms.

**W-5 — THE TYPE CONTRACT MUST TELL THE TRUTH, AT EVERY LAYER.**
`account_count: number` is a lie: the live artifact carries **40 nulls of 447**, in the aggregate series
AND all five `by_model` series. It must become `number | null`.

⚠ **THE BRIEF'S §4.4 NAMES ONLY HALF THE DEFECT — YOU FOUND THIS, AND IT IS THE REASON THIS IS A TO
RATHER THAN A STANDALONE FIX.** The identical non-nullable pair exists **upstream at
`portal-proxy.ts:213-214`, which is the layer `aum.ts` actually calls.** Fixing only the lines §4.4
names produces **a partial that reads GREEN** — which is precisely the class this whole closeout exists
to close (*"a control inherits the scope it was written in; a change does not"*). Your catch, and the
scope below is written from it.

**DO NOT WORK FROM A LIST I HAND YOU — ENUMERATE, AND PRINT THE DENOMINATOR.** A hand-listed set of
sites is exactly how the half-fix happened the first time. My own on-rails sweep already shows FOUR
`account_count` declarations in `aum.ts` alone (`:24, :30, :63, :90`) plus your `portal-proxy.ts`
pair — and I am *not* asserting that is the complete set. Enumerate every declaration and every
consumption site across the serving path, state the denominator, and fix against the enumeration.
</scope>

<explicitly_out_of_scope>
- **W-1's measurement.** Do not attempt to explain WHY dates are null. That is W-1's job, it is the
  wave's denominator, and it runs first and alone. You are making the existing nulls *honest at
  render*, not diagnosing them.
- **W-2's composition law.** Whether Global should null all-or-nothing or serve a declared
  partial-with-named-basis is a **product** decision at CTO's gate and likely Andrew's word. Your work
  must be correct under EITHER outcome. Do not encode an answer to W-2 in the render.
- **`advisor-intelligence.ts`.** My sweep found the same non-nullable-plus-`?? 0` pattern there
  (`:805, :812, :915, :1260, :1263` and others). **It is a different artifact, a different pipeline,
  and a SEV1 surface — it is NOT in this TO.** I am recording it so nobody later believes this pass
  swept the class estate-wide. If you judge it a real instance of the same defect, report it; do not
  fix it here.
</explicitly_out_of_scope>

<cross_domain_coordination>
**`portal-proxy.ts` IS A SHARED LAYER — this is genuine cross-domain, not a formality.** `aum.ts` calls
it, and per CTO's routing packet `json/portfolios/aum-metrics.json` is **not exclusive to
ModelPortfolios**: `FactorTilts:83`, `Attribution/SelectionTab:89`, and `Positioning/HoldingsTab:564`
all reach it via `getAUMSummary` on the same URL. A type change at the proxy layer is felt by all of
them.
**Before committing:** run `comp-transform schema-check` on every component in that set and MCP
0.4.0_DE's sibling lanes / CTO if a change reaches beyond the MDPF page. A `number -> number | null`
widening is source-compatible for readers that already handle it and a compile error for those that do
not — **the compile errors are the point; do not silence them with `?? 0`.** Coercing null to 0 at a
consumer re-creates the original lie one layer down and would make a real "we don't know" render as a
real "zero accounts."
</cross_domain_coordination>

<compiler_tools_mandate>
  <before_write>`comp-transform schema-check ModelPortfolios` (+ each cross-domain component above);
    `comp-transform ternary-audit` on the chart component — the null-vs-zero branch is exactly a
    ternary-audit target. Note `comp-blast` does NOT cover portal files (it returned NOT-FOUND on
    `aum.ts` over a 2251-node denominator that excludes portal source) — that is a NOT-FOUND, not a
    "nothing breaks" clear; use the portal-side tools.</before_write>
  <before_commit>`comp-transform schema-check` re-run on every touched component (MISSING = runtime
    undefined); `comp-surface-check` BY HAND and READ ITS OUTPUT — it is advisory-only, it cannot block,
    it is structurally blind to the `portal/` submodule, and silence from it is NOT a pass.</before_commit>
  <after_commit>Session log with a populated `## Compiler Tools` section; append the
    `org/compiler-tools-log.md` line in the same pass.</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
1. **ENUMERATION WITH A DENOMINATOR (gates everything else).** A stated count of `account_count`
   declaration + consumption sites across the serving path, with the enumeration method named. A fix
   list without a denominator is not acceptable — that is how §4.4 shipped half a defect.
2. **Type contract:** every enumerated declaration is `number | null` (or the documented equivalent),
   INCLUDING `portal-proxy.ts:213-214`. Zero remaining non-nullable `account_count` declarations on the
   MDPF serving path, demonstrated against the enumeration in (1).
3. **No null-to-zero coercion introduced anywhere.** Grep-demonstrable: no new `?? 0` / `|| 0` on a
   count path. `connectNulls` behavior preserved (the FE guard at `pairedProvenanceRead.ts:70-72` must
   remain intact — do not "fix" the guard that is currently protecting us).
4. **W-4 render discrimination, EXERCISED not asserted:** a `band_2firm` point and a `measured` point
   are visually distinguishable on the rendered chart, and **a screenshot proves it** (`/frontend-dev`
   — a grep cannot see contrast; only a rendered screenshot can). Applies to Global AND to 49F/INF per
   the F-3 fold.
5. **A mutant test:** flip one date's `count_provenance` from `measured` to `band_2firm` and the render
   changes. If it does not, the provenance is decorative and (4) is not met.
6. Correct under BOTH possible W-2 outcomes; no W-2 answer encoded.
</acceptance_criteria>

<deliverables>
  - The enumeration table from AC-1 (denominator stated).
  - The code change across all enumerated sites.
  - Screenshot evidence for AC-4 + the AC-5 mutant result.
  - Session log with `## Compiler Tools` populated.
</deliverables>

<notes>
You asked CTO whether to land W-5 standalone now or hold it for my decomposition. **Answer: inside this
TO, with the corrected scope — and land it as soon as the enumeration supports it.** Standalone against
§4.4's named lines only would have produced the partial-that-reads-green. Your read-only prep and
measurement (40/447, both layers) is exactly what I want the TO built on; you are not restarting.
</notes>
</task_order>
