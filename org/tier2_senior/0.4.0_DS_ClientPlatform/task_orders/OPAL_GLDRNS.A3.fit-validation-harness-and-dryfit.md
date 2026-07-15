<task_order>
<to_id>OPAL_GLDRNS.A3</to_id>
<title>The fit-validation harness (S4 parity differ) + the READ-ONLY DRY-FIT: one legacy D publisher exercised against canonical C outputs</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<status>complete</status>
<project>OPAL_GLDRNS (the "testing and validation" half of directive 3, verbatim)</project>
<provenance>Andrew-direct directive 3: "...then let's create a series of TOs for an additional DS
0.4.0_DS_ClientPlatform~A, to go run that testing and validation." Sequenced after A2 (the verdict
tells the harness which divergences are pre-declared).</provenance>

<scope>
(1) THE HARNESS: the S4 parity instrument — legacy-served platinum JSON vs new-D output, per
surface, FIELD-LEVEL diff, keyed off A1's pinned contract; consumes A2's pre-declared-divergence
list (declared divergences report as DESIGN, undeclared as FAIL). Committed beside the runner
tests (the committed-harness law, chunking-arch sec-3 — never a scratchpad). Multi-day streak
accounting built in (N=3 default, Andrew may set).
(2) THE DRY-FIT (the end-to-end fit exercise Andrew asked for, made real EARLY): take ONE legacy D
publisher (D_04 preferred — the largest surface; D_00f as the fallback if D_04's input set is not
yet coverable) and exercise it READ-ONLY against the canonical seed's C-equivalent outputs
(data/canonical/schwab G-tables) — outputs to a SCRATCH prefix or local sink, NEVER a serving or
parallel-serving location, ZERO platinum writes. The dry-fit's diff vs the legacy-served artifact
is the FIRST REAL MEASUREMENT of the fit; its failures are A2-verdict corrections, not defects.
</scope>
<deliverable>The harness (committed, re-runnable, usage in header) + the dry-fit report (surfaces
diffed, field match rates w/ denominators, divergences classed declared/undeclared, A2 corrections
routed).</deliverable>
<compiler_tools_mandate>comp-pipescript postdeps before ANY script execution (ad-hoc run law);
comp-validate on any produced artifact before citing it. NEVER#4: no gold runs against SERVED
locations — the scratch-sink constraint is absolute (a dry-fit that writes platinum is a deploy,
and this TO authorizes none).</compiler_tools_mandate>
<cross_domain_coordination>A1/A2 (same lane); 0.7.0 (if the dry-fit needs a box/execution vehicle
— coordinate, do not self-provision); CTO gate before ANY execution beyond read-only analysis.</cross_domain_coordination>
<acceptance_criteria>Harness committed + exercised on real artifacts (self-test: a mutated field
FAILS loud); dry-fit executed zero-serving-writes with the run's read/write surfaces enumerated in
evidence; field match rates reported w/ denominators; every undeclared divergence either becomes an
A2 correction or a named finding at CTO's gate.</acceptance_criteria>
<session_log>Required, Compiler Tools section mandatory.</session_log>
</task_order>
