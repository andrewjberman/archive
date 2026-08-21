<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-epistemy-c2-attest</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>4.0.0_SA_CRO~A (Codex lane; delivered over the Codex channel by 4.0.0_SA_CRO base; GO gates on YOUR ack -- SENT is not READ)</issued_to>
    <date>2026-08-20</date>
    <status>pending -- GO ISSUED 2026-08-21 ~0057Z by 2.0.0_SA_COO (msg 63997); the seat STARTED at 0054Z on Andrew's direct "Proceed" at their tab, base administering the review gate (CRO 64016). RECORD-TRUTH FLIP made ~0120Z in the /drive cycle: this file still read "staged" while the work was live -- a lagging status is a record defect, not a formality, because the board is read by seats that cannot see the tab. ACTIVATION EVIDENCE: R1+R2 landed @6f944857c4 (both riders confirmed by base 63937 and independently by 3.0.0_SA_CVO); R1 verified at base (battery 8/8 STABLE 6/6, envelope validator PASS) and at MY seat (evidence carries the ratified plane enum + required substrate; battery + validator + negative control re-run); R2 GREEN at HEAD after ~A's decorated-vintage parser fix @6c2a776b07, with base's four controls and MY OWN independently-minted no-pin mutants (two shapes, both VINTAGE_UNRESOLVABLE rc=1 unpiped) -- and my first self-minted mutant DID NOT FIRE because it missed both resolver sources, which is recorded as the live instance of a control measuring its author. The one Scope FAIL my run surfaced was a TRUE finding (a bundle over-carrying R24-AL0-012 against an 11-record pin), fixed by ~C's per-vintage restore @799bc83fd2 -- a bundle defect surfaced BY a working validator, never a validator defect. Pre-GO status preserved: "staged -- ACTIVATES when your ONE rider commit (R1 plane x substrate split + R2 ATOM_LAYER0 vintage-aware validator) lands and is base-validated + COO-revalidated (wave-2 round, CRO base 63752: '~A -> 2 after the two riders land'); GO rides that validation, gated on your ack".</status>
    <project_code>NFRA_EPISTEMY</project_code>
  </metadata>

  <objective>
    Build COMPONENT 2 -- THE INSTRUMENT-ATTESTATION HARNESS -- the producer of
    Discrimination_Certificate objects (PRD sec.2.2): "establishes discrimination per observation
    mechanism." It is the emitter-side twin of the envelope you just landed: the envelope carries a
    nullable discrimination_certificate_ref and today EVERY live ref is null (a declared absence,
    S3 cert line 16) -- this component is what makes that field non-null, honestly. Termination of
    the verifier regress, verbatim from the spec: "a demonstrated contrast across an independence
    cut -- local, expiring, never global trust."
  </objective>

  <context>
    SPEC OF RECORD: docs/architecture/PRD_EPISTEMIC_MECHANIZATION_20260820.md sec.2.2
    (Discrimination_Certificate -- instrument x version x plane x population x grain; declared
    failure directions; ISOLATED positive control; GENERATED negative/mutant; observed
    discrimination; shared failure domain of instrument+controls + at least one independence
    crossing; vintage; invalidation predicates), sec.1 row 2 (precursors: Known_Negative /
    Failure_Direction registry terms, VL#10 practice), sec.3 law 1 ("the cleaner and more
    comprehensive a pass appears, the more important it is to demonstrate the pass and its
    controls do not share a total failure domain"). Base's spec read (63752): fields enumerated,
    7 of 10 ALREADY RATIFIED in registry vocabulary -- REUSE, do not re-coin; the two genuinely new
    fields are shared-failure-domain and invalidation predicates.

    THE LAW THIS COMPONENT MECHANIZES (CLAUDE.md 22a/22b, already practiced by hand): a positive
    control is a control ONLY if run in ISOLATION from the target; a hand-chosen negative control
    measures the AUTHOR, a generated one measures the INSTRUMENT; an instrument whose clean answer
    is strongest when the failure is total (the anti-correlated class) passes the random-input
    control -- so the certificate MUST name the shared failure domain and cross it at least once.
    The harness makes those sentences a typed object that expires.

    CONSUMES C1 (yours): every acquisition the harness performs emits an Observation_Record; a
    failed acquisition is UNKNOWN, never a clean zero. BIND-TIME CONDITION, CTO 63744 verbatim,
    pinned: "no consumer may parse, branch on, or key off `plane` until the ratified plane enum +
    separate substrate field land" -- this TO activates AFTER your rider commit lands, so you
    consume the RATIFIED plane enum + substrate field, never the fused token.

    S6 ABSENCE-SEMANTICS MODEL (CTO 63744, base S3 cert): every nullable field NAMES what its
    absence disqualifies -- "a nullable field with no declared absence semantic is just a hole; a
    nullable field that names what its absence DISQUALIFIES is a control." Apply it to every
    nullable in the certificate.

    RIDERS (every NFRA_EPISTEMY TO, verbatim): (a) sec.2.9 is NOT buildable spec -- the harm
    surfaces are OPEN requirements (sec.4b); do not build against them. (b) CITE-NOT-COPY on shared
    objects: Observation_Record / Discrimination_Certificate / Knowledge_Basis cite the PRD section
    as source of record; ANY proposed field change routes through 4.0.0_SA_CRO base as registry
    executor -- NEVER landed in-lane. (c) interim status shapes resolve into the envelope (yours).
    FIRST ACT = your own S0 ground-read: the registry vocabulary the 7/10 reuse names (print which
    7, by term), and the three C1 wrapped instruments' current control practice.
  </context>

  <compiler_tools_mandate>
    Phase 1: S0 ground-read (registry-term census for the 7 reused fields; comp-find word-boundary
    token census for the 3 new-or-renamed tokens, counts printed defs/bank/canon); the Rule-24
    pre-record for the certificate's status/verdict axis (MECE over the DECLARED attestation-outcome
    layer: every terminal named, UNKNOWN + EXPIRED explicit -- outcome arrays are schemas).
    Phase 2: the mutant battery BEFORE commit -- at minimum: (m1) control shares the instrument's
    total failure domain -> certificate must REFUSE/INVALID; (m2) positive control run against the
    target, not in isolation -> REFUSE; (m3) hand-authored negative presented as generated -> the
    generation provenance check fires; (m4) instrument version bumps -> certificate reads EXPIRED;
    (m5) an anti-correlated instrument (clean answer strongest on total failure) -> the crossing
    requirement catches it; determinism (two runs byte-identical).
    Phase 3: live certificates for the three C1 wraps (comp-find, comp-estate, census_substrate),
    each with its isolated positive control + generated negative actually RUN, denominators printed.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: Discrimination_Certificate (PRD sec.2.2) -- source of record is the PRD;
      field changes -> 4.0.0_SA_CRO base (registry executor, S2 program), 1.0.0_SA_CTO gates the
      schema act; base's S3 spec cert precedes the CTO gate.
    - consumer: the envelope's discrimination_certificate_ref (yours) -- populated ONLY by a minted
      certificate; absent -> null stays null (declared absence), never a fabricated ref.
    - consumer: component 3 (0.8.0_AE_CloudComp, identity + support closure) will reference
      certificates as support members; component 4 (lease) will lease them. You do not build
      either; you make the object leasable (vintage + invalidation predicates present).
    - shared_resource: the comp-tool engines (org/modules/graph/*.py) -- prefer wrapping over
      editing; any engine-side touch coordinated by MCP via base.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is COMPONENT 2 as cut -- A1 object, A2 live
    certificates, A3 independence crossing, A4 expiry, A5 envelope join, A6 battery, A7 proof;
    exhaustive over the component; components 3/4 explicitly OUTSIDE.)
    A1  Discrimination_Certificate implemented schema-native per PRD sec.2.2 (cited, not copied);
        7/10 fields REUSE ratified registry vocabulary by term; Rule-24 record + token census
        committed WITH the schema act through 4.0.0_SA_CRO base; 1.0.0_SA_CTO arch-gates; every
        nullable field carries its S6 absence semantic.
    A2  THREE LIVE CERTIFICATES: comp-find, comp-estate, census_substrate each attested -- isolated
        positive control RUN, GENERATED negative/mutant RUN (provenance of generation recorded),
        observed discrimination recorded with denominators.
    A3  INDEPENDENCE CROSSING ENFORCED BY CONSTRUCTION: each certificate names the shared failure
        domain of instrument+controls and at least one crossing; a certificate whose controls share
        the instrument's total failure domain CANNOT be minted VALID (mutant m1 fires).
    A4  EXPIRY IS REAL: vintage + invalidation predicates present; an instrument-version change
        makes the certificate read EXPIRED (m4 fires); "failure to re-attest never preserves
        validity" stated and exercised.
    A5  ENVELOPE JOIN: an Observation_Record emitted under an attested instrument carries the
        non-null certificate ref; under an unattested one the ref stays null; `plane` consumed
        ONLY as the ratified enum + substrate field (bind-time condition discharged, cited by hash).
    A6  Mutant battery m1-m5 all FIRE; determinism stable (house standard: atom_layer0 discipline).
    A7  Proof instance VALID rc=0 positional A1-A7; RAVC close via base to COO, cc CTO.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>A1,A2,A3,A4,A5,A6,A7</expected_criteria>
    <instance_path>org/tier1_exec/4.0.0_SA_CRO~A/deliverables/NFRA_EPISTEMY.C2-ATTEST_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Bounds: no envelope field change in-lane (base executes); no owner-engine/cloud/enforcement edits; nothing armed (no alert, monitor, gate -- gate CANDIDATES may be proposed in the deliverable); components 3/4 untouched. Surprise channel: one line to base -> COO. Falsifier duty (atom_layer0) stays yours in parallel.</requirement>
  </requirements>
</task_order>
