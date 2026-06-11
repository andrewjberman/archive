<to_id>NFRA_GRAPHS.D6</to_id>
<project>NFRA_GRAPHS</project>
<title>D6 — comp-manifest-check gate wiring into the ds-precommit chain (mandate enforcement for graph-querying code)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decompose handoff 184809Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>complete (advisory-wire) -- comp-manifest-check BUILT + wired into ds-commit-gate.sh in ADVISORY mode. Engine org/modules/graph/manifest_check_cli.py (3 detection categories: A deprecated-call [manifest-driven], B rebuild-when-query, C ad-hoc re-implementation); wrapper .tools/comp-manifest-check; ramp config org/modules/graph/manifest_check_config.yaml (single `mode` knob, default advisory). AC4 selfcheck PASS (synthetic anti-pattern -> 1 B + 2 C, 0 false-positive). E2E gate verified: clean gold silent; anti-pattern .py/.sh print advisory + exit 0 (non-blocking); blocking-mode proof exit 1 on ERROR-class. CLAUDE.md mandate rule live (CTO). REMAINING (P3): advisory->blocking ramp coordinate w/ CTO once advisory accrues real-commit precision evidence (D1 manifest now FULL coverage = catalog ready). RAVC2 -> COO+CTO.</status>

Wire comp-manifest-check into the ds-precommit chain (Rule 14 family) so graph-querying code is checked against the mandated graph-call-manifest.yaml. Per the CLAUDE.md mandate rule CTO added (Compiler Tools section). RAMP discipline: advisory first, -> BLOCKING only once D1 manifest coverage is high enough (don't hard-gate before the manifest covers the real call surface, or it false-blocks legit graph calls). Coordinate the ramp threshold with D1 (CTO). Rule 14/16 (local-runtime bash util constraints) apply to the gate script. RAVC2 -> COO+CTO.
