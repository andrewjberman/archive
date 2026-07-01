# TASK ORDER — NFRA_COMPUNIFY.V1

<issued_to>3.0.0_SA_CVO~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete</status>
<priority>HIGH — Andrew-direct close-out drive (2026-07-01). SEQUENCED behind your in-flight GRAPHDEPTH gate-lift verdict (that fires first). The COMPUNIFY map (the comp-tool taxonomy) is independent of the GRAPHDEPTH substrate population — V1 can run right after the gate-lift; flag me if you read a dependency I've missed.</priority>
<date>2026-07-01</date>

## Context
NFRA_COMPUNIFY = the foundational comp-tool coverage MAP (the MAPS verb; the PRIOR both COMPDRIFT and COMPLEARN and now COMPROUTE reference). PRD: `docs/architecture/NFRA_COMPUNIFY_PRD.md`. ~C (COMPUNIFY governor) landed S0-S4 + S4-AUDIT GREEN (df606c15a) — the map is V1-ready. V1 = YOUR independent acceptance, the last gate before COMPUNIFY closes.

## Objective
Independently ACCEPT (or REWORK) the COMPUNIFY coverage map against its two load-bearing acceptance properties: COMPLETENESS and NON-REDUNDANCY. Ground against the LIVE map artifact + the comp-coverage-check gate — never ~C's self-report.

## Scope — V1
1. **COMPLETENESS:** every comp-tool has exactly ONE home in the coverage/provenance ledger (`comp-coverage-map.yaml`), across the 5 surfaces (local/git/aws-cloud/ms-cloud/trino-federation). No tool unmapped; the ledger SUPERSEDES the flat tools_index (generated-view, one catalog).
2. **NON-REDUNDANCY (the load-bearing machine-checkable invariant):** every tool's home = (surface|seam) x granularity x concern; a shared resource appears twice ONLY on a DECLARED concern-difference. Any SILENT overlap = a violation -> REWORK to ~C (merge/disambiguate). Spot-check the known redundancy clusters the census flagged (IAM x3 / parity x3 / freshness x4) resolve to declared-concern-differences, not silent dupes.
3. **The gate:** `comp-coverage-check` runs clean (the invariant-as-gate, PRD ruling). The gap census (seeds COMPLEARN) + redundancy census are present + honest.
4. **Verdict:** RAVC ACCEPT (map V1-certified -> COMPUNIFY closes) or REWORK (specific violations cited back to ~C). Ground every claim against the live artifact + a sharp structural test (not "looks mapped").

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-coverage-check (or the COMPUNIFY gate ~C shipped) + read the live comp-coverage-map.yaml</run>
      <expect>The gate exists + runs; the ledger enumerates every tool with a single (surface|seam)x granularity x concern home; gap + redundancy censuses present.</expect>
      <if_mismatch>Could-not-verify is a finding. If the gate is absent/broken, that itself blocks V1 -> REWORK to ~C.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after verify">
    <step>
      <run>the sharp test: pick the 3 flagged redundancy clusters (IAMx3/parityx3/freshnessx4) + confirm each duplicate carries a DECLARED distinct concern (not silent overlap)</run>
      <expect>Each apparent dup resolves to a declared concern-difference; zero silent overlap. Every tool reachable to exactly one home.</expect>
      <if_mismatch>REWORK: cite the silent-overlap tool(s) back to ~C for merge/disambiguate.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~C: the COMPUNIFY governor — REWORK routes to ~C (map is read-only from every other lane; only ~C mutates it).
- 1.0.0_SA_CTO: PRD rulings (ledger-supersedes-manifest / seam==COMPDRIFT-topology one-artifact / invariant-as-gate). CC on the V1 verdict.
- NFRA_COMPDRIFT + NFRA_COMPLEARN + NFRA_COMPROUTE: all consume this map as their PRIOR — a V1 ACCEPT stabilizes the shared foundation.
</cross_domain_coordination>

<acceptance_criteria>
1. COMPLETENESS verified: every comp-tool has exactly one ledger home across the 5 surfaces; ledger supersedes tools_index. Grounded against the live artifact.
2. NON-REDUNDANCY verified: the machine-checkable invariant holds (one home = surface|seam x granularity x concern); the 3 flagged clusters resolve to declared concern-differences; zero silent overlap. comp-coverage-check clean.
3. RAVC verdict emitted (ACCEPT -> COMPUNIFY closes / REWORK with cited violations -> ~C). Session log Compiler Tools section reproduces every `<run>` + observed output + pass/fail. RAVC COO~B + CC CTO + ~C.
</acceptance_criteria>

## Note
This is the COMPUNIFY close-gate. Sequenced behind the GRAPHDEPTH gate-lift verdict (that first). Ground against the live map + a sharp structural test — never ~C's self-report (NEVER#5). Could-not-verify is a finding, not a pass.
