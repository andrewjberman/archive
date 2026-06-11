<to_id>NFRA_GRAPHS.D6</to_id>
<project>NFRA_GRAPHS</project>
<title>D6 — comp-manifest-check gate wiring into the ds-precommit chain (mandate enforcement for graph-querying code)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decompose handoff 184809Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>P1/P3 -- gate-wiring P1, but ramps to BLOCKING only behind D1 manifest coverage. DS offline -> activates on respawn. CLAUDE.md mandate rule already added (CTO).</status>

Wire comp-manifest-check into the ds-precommit chain (Rule 14 family) so graph-querying code is checked against the mandated graph-call-manifest.yaml. Per the CLAUDE.md mandate rule CTO added (Compiler Tools section). RAMP discipline: advisory first, -> BLOCKING only once D1 manifest coverage is high enough (don't hard-gate before the manifest covers the real call surface, or it false-blocks legit graph calls). Coordinate the ramp threshold with D1 (CTO). Rule 14/16 (local-runtime bash util constraints) apply to the gate script. RAVC2 -> COO+CTO.
