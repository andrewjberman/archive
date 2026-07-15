<task_order>
<to_id>OPAL_GLDRNS.A2</to_id>
<title>The D-consumed input census (column-level, all 8 publishers) + the B/C->D SUFFICIENCY VERDICT</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<status>staged</status>
<project>OPAL_GLDRNS (executes OPAL_CONSOLIDATION WS-C gate C5b — no Wave-3 C-port spec freezes until this verdict)</project>
<provenance>Andrew-direct directives 3 (~19:0xZ: "proceed through the B & C group scripts and make
sure that we can get that fit to D_04 or whatever the final script is") + 4 (the ~A lane). Sequenced
after A1 (the output contract) — A1's D-to-D edge map is this TO's input.</provenance>

<scope>READ-ONLY, source-grounded. Per bd D script (all 8): every upstream field it READS — which
legacy A/B/C tables + gold keys + D-to-D inputs, column-level. Then the VERDICT: map that census
against the PLANNED replacement shapes — the ratified A-to-D build plan's C tables (build plan @
baba79230, Wave-2 cores @ 80240881d), the dictionary rows (OPAL_RUNNERS_49F_SILVER_DATA_DICTIONARY.md,
current @ dd9a46692), the D1 dim v1.1 (incl. the NO-FEE binary — ruling 6), and B_00 lots-union.</scope>

<deliverable>
org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/BC_TO_D_SUFFICIENCY_VERDICT_49F_20260715.md:
per consumed field, ONE verdict — CARRIED (cite the C-table column) / RENAMED (cite the mapping) /
DERIVED-IN-D (lawful, the derivation named) / **MISSING (the finding class — each MISSING routes to
CTO BEFORE Wave-3 C-port specs freeze)**. Fields fed by the DELETED legacy layers (reconciliation/
injection/phantom-exclusion, the ruled-unacceptable transaction-engine valuation) get a NAMED
disposition: what replaces the input, or why the output LAWFULLY CHANGES — every lawful change
pre-declared as an expected divergence for the S4 parity streak (an undeclared divergence resets
the streak; a pre-declared one is design). Honest denominators: publishers/fields/verdicts counted;
UNKNOWN is a legal verdict with a named reason.
</deliverable>
<compiler_tools_mandate>comp-pipescript io per script; comp-blast on shared C tables; comp-kuzu for
cross-layer edges where the graph carries them (read the provenance header). Commit-gate per law.</compiler_tools_mandate>
<cross_domain_coordination>A1's contract doc (same lane, sequenced); base 0.4.0_DS dictionary
(read; corrections route to CTO — ANY_CTO surface); 0.6.2's W1 census (cite, don't redo).</cross_domain_coordination>
<acceptance_criteria>8/8 publishers censused; 100% of consumed fields carry a verdict; every
MISSING at CTO's gate with a proposed resolution; every deleted-layer input dispositioned; the
pre-declared-divergence list exists as its own section (the S4 harness consumes it).</acceptance_criteria>
<session_log>Required, Compiler Tools section mandatory.</session_log>
</task_order>
