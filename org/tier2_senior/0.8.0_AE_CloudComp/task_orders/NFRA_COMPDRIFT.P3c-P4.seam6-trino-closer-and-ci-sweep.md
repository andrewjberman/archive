# TASK ORDER — NFRA_COMPDRIFT.P3(c) + P4

<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>pending</status>
<priority>HIGH — Andrew-direct close-out drive (2026-07-01). Your P3(c) gate is CLEARED: it was held on the heat-federation surface, which is now LIVE (COMPLEARN P1 gap_heat federation). Start P3(c) NOW. Your Phase-B compute co-sign priority-interrupt still stands — yield to the ~B-fired derive if the gate lifts, then resume.</priority>
<date>2026-07-01</date>

## Context
NFRA_COMPDRIFT = the first-class estate-drift compiler owning the local->git->cloud->nessie->kuzu->iceberg->trino->served propagation topology (8 stages / 7 seams). PRD: `docs/architecture/NFRA_COMPDRIFT_PRD.md`. You landed P2 + P3(a)(b) through 62063ee60 (shebang-dispatch fix + BEHIND severity split). P3(c) (seam-6 Trino closer) was the one HELD piece — held on the heat-federation surface. That surface is now LIVE, so this un-gates. P4 (the standing CI sweep) closes the project.

## Objective
Close the two remaining COMPDRIFT deliverables so the project can close:
1. **P3(c) — seam-6 (Trino) parity closer**, co-designed INTO the live heat-federation (PRD arch-gate (d) Trino FAN-IN model + the heat-federation cross-dependency AC). Seam-6 must emit a checkable per-catalog parity signal, folded into the normalized drift-record + tri-state exit (0 clean / 1 break / 2 UNVERIFIABLE — never silently MATCH).
2. **P4 — the standing CI sweep** folding `drift_producer.py` (the estate-board `comp-drift sweep` that orchestrates the COVERED engines, never re-implementing them).

## Scope
- **P3(c):** wire seam-6 (Trino federation catalog) into `comp-drift` as a FAN-IN node (N inbound catalog seams per PRD arch-gate (d)). Reuse the live heat-federation's per-catalog parity signal — do NOT build a new Trino transport (reuse `.tools/_trino_fed.py`, the shared in-VPC run-task->REST substrate; no persistent endpoint, SCTY-gated). If the federation's parity signal is present -> seam-6 = COVERED; if absent -> seam-6 = GAP + flag COO~B (the retrofit-instrumentation path this project exists to avoid).
- **P4:** the `comp-drift sweep` standing CI board over the full topology, folding `drift_producer.py`'s disposition (per PRD). Tri-state exit contract; comp-which-routable.
- Conform to the fixed drift-record contract (the unified board COMPDRIFT/COMPDIFF share) + vintage-primary / marker-oracle freshness semantics (NOT newest-by-timestamp).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-drift &lt;a seam-6/Trino-touching target&gt; (ground the current seam-6 verdict) + confirm the live heat-federation emits the per-catalog parity signal</run>
      <expect>The heat-federation surface is live + emits a checkable per-catalog parity signal seam-6 can fan in. Current seam-6 verdict = GAP/UNVERIFIABLE (the piece this TO closes).</expect>
      <if_mismatch>STOP. If the federation does NOT emit the parity signal, seam-6 falls to GAP -> flag COO~B before building a retrofit (the costly path); do not silently mark seam-6 COVERED.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>reuse check: grep for any NEW Trino transport vs `.tools/_trino_fed.py`; `from __future__ import annotations`; `.tools/ds-commit-gate.sh`; non-ASCII grep</run>
      <expect>Zero new Trino transport (reuse _trino_fed); ds-commit-gate clean; zero non-ASCII; the seam-6 closer NEVER re-implements a COVERED engine (PRD arch-gate (b) orchestrator-boundary).</expect>
      <if_mismatch>STOP. Rebuild against the shared substrate; abstract to orchestration-only.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-drift sweep (the P4 board) + comp-drift on a seam-6 target (verify the closer)</run>
      <expect>seam-6 = COVERED (parity signal read) OR honest GAP/UNVERIFIABLE (never silent MATCH); the sweep board runs tri-state-clean; drift_producer.py folded.</expect>
      <if_mismatch>Fix before RAVC. A silent-MATCH on an unverifiable seam is the exact class this project exists to kill.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 1.0.0_SA_CTO: PRD owner + the 5 arch-gate rulings (esp. (d) Trino FAN-IN + the heat-federation cross-dependency AC). RAVC the P3(c)/P4 close.
- 3.0.0_SA_CVO~B: verifies the seam-6 closer + the standing sweep (tri-state honesty; no silent MATCH). This is the COMPDRIFT close-verify.
- NFRA_COMPLEARN (~E): owns the live gap_heat federation surface P3(c) fans in from — coordinate the parity-signal read (do not duplicate the federation).
- NFRA_COMPDIFF: shares the unified drift-record contract — conform, don't fork it.
- `.tools/_trino_fed.py`: the shared Trino substrate — reuse, never rebuild.
</cross_domain_coordination>

<acceptance_criteria>
1. seam-6 (Trino) is wired into comp-drift as a FAN-IN node reading the live heat-federation's per-catalog parity signal; emits into the normalized drift-record with the tri-state exit (0/1/2, never silent MATCH). If GAP, flagged to COO~B (not silently COVERED).
2. P4 standing CI sweep (`comp-drift sweep`) runs the full-topology board, folds drift_producer.py, comp-which-routable, tri-state-clean.
3. No new Trino transport (reuse `_trino_fed.py`); no COVERED-engine re-implementation (orchestrator-boundary held).
4. Session log Compiler Tools section reproduces every `<run>` + observed output + pass/fail vs `<expect>`. RAVC COO~B + CC CTO + CVO~B — this closes COMPDRIFT to P4-complete.
</acceptance_criteria>

## Note
Close-out drive. P3(c) is your ONE held piece + P4 is the standing guard — landing both = COMPDRIFT ready to close. Do not self-wind to "tonight" — start now; yield to the Phase-B derive on gate-lift, then resume.
