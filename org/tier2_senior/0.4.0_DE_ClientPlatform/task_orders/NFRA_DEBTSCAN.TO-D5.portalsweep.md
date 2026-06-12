# Task Order: NFRA_DEBTSCAN.TO-D5
## PORTALSWEEP — full portal/webapp structural sweep (DT + DE JOINT)

**Project:** NFRA_DEBTSCAN (v0.2, Andrew-direct)
**Assigned to:** 0.4.0_DT_ClientPlatform (toolchain + route/deploy) + 0.4.0_DE_ClientPlatform (component/data-channel/type-contract)
**Priority:** P1 — JOINT, Andrew-named both serials
**Authority:** CTO PRD v0.2 a5e58490e (Andrew-direct ~19:15Z 2026-06-12)
**Sequence:** GO immediately for DT; DE pending spawn (MSTR spawn request in parallel)

---

## Context

Andrew-direct directive (PRD §2f): full portal/webapp structural sweep, DT + DE joint. Supersedes the §6 Q4 P3 deferral — portal-source debt is IN now. Priority order: **Advisor Intelligence + Model Portfolios first** (the heavy sections), then everything.

---

## Hunt List (Andrew-named + family-mapped)

### Toolchain sweeps — DT primary

1. **TypeScript warnings of ANY kind**: run `tsc --noEmit` + full ESLint sweep — warnings, not just errors. Zero-tolerance flag: if it produces warnings, they get filed.
2. **Route/deploy liveness**: every route → CloudFront behavior → Lambda@Edge path. Is every registered route actually reachable end-to-end? File dead/missing routes.
3. **Build toolchain health**: check bun config, import maps, alias resolution, any version mismatches.
4. **Dead exports (toolchain angle)**: exports that compile fine but nothing imports (knip-style or grep-based).

### Component/data-channel/type-contract sweeps — DE primary

5. **Broken/dead processes** (family 2a): components that mount but never receive data; fetches that succeed but data never reaches a render path.
6. **Out-of-pattern items** (family 2c): component structure that deviates from the dominant portal motif (count instances; 1-2× vs N× = unusual-by-construction).
7. **Unused imports**: every `import` statement that is not referenced in the same file.
8. **Dead data channels**:
   - Fetches with no rendering consumer (data fetched, never displayed)
   - State/props channels with no producer (component reads a prop that is never passed)
   - React-Query keys nothing reads
   - comp-cache + comp-transform + comp-platinum coverage where graph-indexed
   - **File-level sweep where not graph-indexed** (D8 Layer-2 lesson: BenchmarkHeatmap/portal-proxy/PeersTab are graph-blind — sweep them with file-level SHA/grep approach, not kuzu)
9. **Dead exports/components**: knip/ts-prune-style census; grep-based if no tool present.

### Priority order

**Phase 1 (heavy first):** `portal/src/components/advisorIntelligence/` + `portal/src/components/modelPortfolios/`
**Phase 2 (everything):** all remaining portal/src directories

---

## Split / Adjudication

| Dimension | Owner |
|---|---|
| `tsc --noEmit` + ESLint config + run | DT |
| Route/deploy-path liveness (CF behaviors → Lambda@Edge) | DT |
| Build toolchain (bun, import maps, aliases) | DT |
| Component/data-channel/type-contract analysis | DE |
| Unused imports census | DE |
| React-Query dead key sweep | DE |
| Dead export/component census | DE |
| Joint adjudication | DT + DE together |

**ONE merged ledger entry per sweep** — DT files toolchain findings; DE files component findings; final ledger entry is co-signed.

---

## Day-0 known FPs (pre-seeded, do not file as new):

- `getAUMMetrics` unresolved fetch — D8 coverage-gap Day-0 known
- D8 coverage-gap trio (BenchmarkHeatmap/PeersTab/portal-proxy) — graph-blind by design; sweep with file-level approach
- Portal type aliases (T1 T3 fixes, 8b6a6466) — already fixed; check for regressions only

---

## Zero-mutation guarantee

The SWEEP is read-only. TypeScript compile runs, linting runs, grep runs, comp-* tool queries — all read-only. NO code changes during sweep.

Fixes = separate TOs after joint adjudication. They ride normal DE/RD/DT lanes + VALGATE.

---

## Acceptance Criteria

- AC1: tsc --noEmit output (0 errors required; warnings exhaustively listed)
- AC2: ESLint output (warnings listed, not suppressed)
- AC3: Route/deploy liveness table (every registered route → reachable=Y/N)
- AC4: Dead data channels list (fetch-no-consumer, state-no-producer, unread React-Query keys)
- AC5: Unused imports census (count + list)
- AC6: Dead exports/components census
- AC7: Per-finding format per §4 (family, severity, firm-scope, triage, owner-lane)
- AC8: Zero mutations (run logs)
- AC9: One merged ledger file: `org/modules/graph/debtscan/2026-06-12_D5_portalsweep_dt_de.md`
- Precision gate: §3 CVO-adjudicated before promoting above ADVISORY

---

## RAVC2 to COO

Include in body (can be combined DT+DE, or DT first + DE follows):
1. Commit hash(es) for the ledger file
2. tsc + ESLint warning counts (numbers alone are enough for RAVC2)
3. Dead data channel top-3 findings
4. AC8 zero-mutations confirmation

CC 3.0.0_SA_CVO on RAVC2.

---

*Dispatched by 2.0.0_SA_COO 20260612T192300Z*
*CTO PRD v0.2 a5e58490e (Andrew-direct)*
*DE to be spawned; DT GO effective immediately on receipt*
