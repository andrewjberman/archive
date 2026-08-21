<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-ontology-r1-rarity</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp (graph engine home; CRO base's machine-side owner candidate, spec 63742/63752)</issued_to>
    <date>2026-08-20</date>
    <status>pending -- GO ISSUED 2026-08-21 ~0110Z by 2.0.0_SA_COO (msg 64034). Activation condition MET AND EXCEEDED: C3-IDENTITY did not merely reach I2, it CLOSED and is rider-conformant (@d652c88490; COO-validated 27/27 observations vs the HEAD envelope schema, battery 24/24 rc=0, proof I1-I7 VALID rc=0), so the critical path is clear; CTO 63823 established this TO consumes nothing C3 produces. ⛔ THE GO IS COO'S OWN DISCRETIONARY WORD ON A COO GATE -- it is explicitly NOT a reading of Andrew's "GO on" at the 0.8.0 terminal (~0051Z, relayed at verbatim scope by the seat, 63962): his word bound that seat's DRIVING, and widening a sovereign instruction into a gate-release is prohibited in both directions. The seat was right to refuse to adjudicate it. Pre-GO status preserved: "staged -- ACTIVATES on COO GO at the earlier of: C3-IDENTITY reaching its I2 milestone, or a second 0.8.0 lane live."</status>
    <project_code>NFRA_ONTOLOGY</project_code>
  </metadata>

  <objective>
    TWO LEGS, one seat, in order. LEG 1 (R1 -- the materialization act): land the C2 INSTANCE
    GRAIN in the canonical graph -- today it holds 19 static `C2Motif` class rows and ZERO
    instances (4.0.0_SA_CRO~B census R1, GRAPH_ONTOLOGY_LAYER_CENSUS_FULL_REPORT_20260820.md:1037
    -- "the graph exposes static C2/C3 rows but not the intended live composed population";
    failure direction: "an agent may mistake a clean zero for 'no instances exist' when the
    instance producer did not land"). LEG 2 (the rider): add the RARITY COORDINATES to the family
    and instance rows LEG 1 materializes, exactly per 4.0.0_SA_CRO base's spec
    org/tier1_exec/4.0.0_SA_CRO/deliverables/C2_RARITY_COORDINATE_RIDER_SPEC_20260820.md -- the
    rider STAGES axes and computes NO verdict.
  </objective>

  <context>
    AUTHORITY: Andrew-direct 2026-08-20 ~1945Z, "Recs approved" on the /open-calls card -- BOTH
    populations, per-firm AND estate-wide, each printed with its denominator (record
    org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260820_RARITY_DENOMINATOR_AND_DEVICE_AXIS.md)
    + his premise, verbatim, the design constraint: "basically just logging a figure of how many
    times the shape was discovered in the estate, which is interesting if there is a C2 shape that
    is highly distinct but very similar to one that is not highly distinct, for example, could be
    a sign ... we want to essentially 'stage' data in very tight, high-signal manners for agents,
    because the agents then use their reasoning to do the magic."

    LEG 1 SOURCING (already ruled on the record, not re-decided here): NFRA_COMPSIMILAR.PH2-C2
    (0.8.0_AE_CloudComp~D, complete) build-notes @5c1d828db -- SERVED_LINEAGE (SERVED_FROM /
    FLOWS_TO modeled) is the FIRST class to land, its roles structurally derivable today; DEPLOY is
    bucket-grain on the canonical DB; AUTH's defining TRIGGERS edge is unmodeled. "Land
    SERVED_LINEAGE first; the others follow as their instance-grain source is wired -- each gated
    only by that source, not by feasibility." The liveness instrument is
    infra/aws/globgrph/c2c3_liveness_acceptance.py -- R1's own control: "always run it; never use
    a bare instance count." Cites, never re-declares: org/modules/graph/NFRA_ONTOLOGY_C2C3_CANONICAL.yaml
    (twelve families; honesty_invariants.c2_c3 "DISCOVERED, never declared -- membership comes
    from recurrence (>=2)").

    LEG 2 FIELDS (spec sec.1, by reference): recurrence (family x population) with
    recurrence.basis {MEASURED_INSTANCE_SET | FIRST_PASS_HAND_COUNT}; rarity_denominator
    (population -- printed beside every recurrence); population_scope {ESTATE | FIRM:<tree>} BOTH
    rows per family (his ruling; a family with 0 in a firm carries 0 WITH that firm's denominator
    -- a true zero, framed); nearest_family (argmin over G != F, PROPOSAL device only);
    distance + metric_ref (name@version -- a distance without metric_ref is not a coordinate);
    d3_preserving {PRESERVED | NOT_PRESERVED | UNKNOWN_NO_D3_DECLARED} -- default UNKNOWN, the
    rider MUST NOT emit PRESERVED by default; vintage on every row. Production rule = spec sec.3,
    six steps, incl. two-run byte reproducibility before the first commit. Rule-24 record + token
    census for the rider's own enumerations = spec sec.2 (already filed; cite it).

    WHAT THIS IS NOT: no "suspicious" flag, no verdict, no alert -- the agent infers; a
    pre-computed verdict would be alarm-shaped (moratorium class) and wrong the first time the
    metric moved. No C2 family minted, no canonical touched, no family identity defined (the
    substitution policy does, when ratified -- until then `policy: NONE_RATIFIED` declared). No
    per-vertical population (a third population is a ruling, not an inference).
  </context>

  <compiler_tools_mandate>
    Phase 1: S0 -- run c2c3_liveness_acceptance.py and print its current verdict (expected: 0
    instances, the R1 state); comp-kuzu census of `C2Motif` rows (class grain) with denominator;
    comp-blast on the producer you will extend.
    Phase 2 (LEG 1): SERVED_LINEAGE instances materialized (grain=instance + CONTAINS) through the
    existing producer path; liveness instrument re-run -> nonzero, framed; two-run byte
    reproducibility.
    Phase 3 (LEG 2): the rider rows emitted per spec sec.3; denominators printed per population;
    d3_preserving reads UNKNOWN_NO_D3_DECLARED everywhere D3 is undeclared (positive control: a
    fixture pair WITH declared D3 reads PRESERVED or NOT_PRESERVED); two-run byte reproducibility.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - spec owner 4.0.0_SA_CRO base: questions on the rider fields -> base; the canonical and the
      substitution policy are NOT yours to edit.
    - 4.0.0_SA_CRO~B: census author (R1); their liveness-instrument control is the acceptance
      oracle; report the post-materialization verdict to them.
    - consumers named in the spec: agents reasoning over C2 state; the motif-identity
      formalization (Response II sec.2.4 retrodiction pass) -- its candidate generator is your
      nearest_family + distance, its discriminator d3_preserving.
    - the graph engine home org/modules/graph/*.py is your enumerated lane (ANY_EXEC_OR_AE,
      CTO-ruled 2026-08-20); infra/aws/globgrph/ is the liveness instrument's home -- READ it,
      coordinate any edit by MCP with CTO.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is R1 + rider as cut -- M1 materialization, M2 liveness
    oracle, M3 rider rows, M4 no-verdict/defaults, M5 reproducibility, M6 proof; exhaustive;
    DEPLOY/AUTH classes and the substitution policy OUTSIDE.)
    M1  SERVED_LINEAGE C2 instances materialized in the canonical graph (grain=instance +
        CONTAINS), count printed WITH its class denominator (12 families / 19 class rows).
    M2  c2c3_liveness_acceptance.py run before (0) and after (nonzero) -- the oracle, not a bare
        count; reported to 4.0.0_SA_CRO~B.
    M3  Rider rows per spec sec.1/sec.3: BOTH populations per family with denominators beside
        every recurrence; recurrence.basis honest (MEASURED_INSTANCE_SET where LEG 1 landed,
        FIRST_PASS_HAND_COUNT where not); nearest_family + distance + metric_ref; vintage on every
        row.
    M4  NO VERDICT: no suspicious/alert field exists; d3_preserving defaults
        UNKNOWN_NO_D3_DECLARED (positive-controlled); `policy: NONE_RATIFIED` declared where no
        substitution policy is ratified.
    M5  Two-run byte reproducibility over the same inputs, both legs.
    M6  Proof instance VALID rc=0 positional M1-M6; RAVC close to COO, cc 4.0.0_SA_CRO (spec) +
        1.0.0_SA_CTO.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>M1,M2,M3,M4,M5,M6</expected_criteria>
    <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_ONTOLOGY.R1-RARITY_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Do not start before COO's GO. Normal cadence. Every count printed with its denominator and its population named (Rule 21 firm-scope law: an absence verdict names the tree it searched). Surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
