<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-epistemy-c4-lease</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp</issued_to>
    <date>2026-08-20</date>
    <status>staged -- ACTIVATES on the close of NFRA_EPISTEMY.C3-IDENTITY (same seat) AND 4.0.0_SA_CRO base's Knowledge_Basis object (PRD sec.2.3) reaching schema form through the S2 program (CRO base 63752: "order 2->3->4 is a DEPENDENCY order, not a preference"); COO GO on both</status>
    <project_code>NFRA_EPISTEMY</project_code>
  </metadata>

  <objective>
    Build COMPONENT 4 -- THE FOUR-STATE LEASE SERVICE (VALID / INVALID / UNKNOWN / EXPIRED;
    "failure to reevaluate never preserves validity") + the Eligibility_Evaluation object it
    serves (PRD sec.2.5): "invalidation against real support identities, not names" (sec.1 row 4).
    A lease is not a lock. The precursors the estate already runs by hand: view-time compilation,
    the 14-day stale banner, the generated_at / last_review split (sec.3 law 7: a regen is not a
    review).
  </objective>

  <context>
    SPEC OF RECORD: PRD sec.2.5 -- a separate, dated, attested object over an IMMUTABLE assessment
    ("metadata about a record is not the record"): prior/current knowledge basis, intersecting
    changes, exclusion proofs (necessity-aware: incompatible with EVERY admissible realization --
    attested absence may prove; untyped silence never does), residual before/after, policy
    predicate applied, result ELIGIBLE / INELIGIBLE / UNKNOWN with one-evaluation-per-(assessment,
    scope). THE INVALIDATION PIPELINE, in order: coarse coordinate intersection (OVER-include, never
    under-include) -> exclusion-proof replay -> residual recomputation -> policy application. "A new
    member is never covered by an old enumerated waiver; it may be covered by a ratified predicate
    whose declared scope includes it." Sec.2.3 Knowledge_Basis: a signature edit or normalization
    change invalidates as surely as a new member -- base authors that object; you consume it.

    DEPENDENCIES (why this is staged): the lease invalidates against SUPPORT IDENTITIES -- the
    Support_Closure members component 3 compiles -- not against names; and the Eligibility
    evaluation reads a Knowledge_Basis digest. Neither exists yet. The dependency is structural:
    a lease service built before the identity chain would lease NAMES, the exact thing the spec
    forbids.

    CONSUMES C1 + C2 + C3: every acquisition emits an Observation_Record; leases may reference
    Discrimination_Certificates (4.0.0_SA_CRO~A) and Support_Closures (yours); `plane` consumed as
    the ratified enum (the bind-time condition will be discharged by then -- cite the hash). S6
    absence-semantics model on every nullable field.

    RIDERS (every NFRA_EPISTEMY TO, verbatim): (a) sec.2.9 not buildable spec -- do not build
    against the harm surfaces; (b) CITE-NOT-COPY; Lease + Eligibility_Evaluation objects and any
    field change route through 4.0.0_SA_CRO base (registry executor) with Rule-24 record + token
    census, CTO gate after base's spec cert; (c) interim shapes resolve into the envelope.
  </context>

  <compiler_tools_mandate>
    Phase 1: S0 ground-read of the three precursors (where view-time compile, the 14-day banner,
    and generated_at/last_review live today; denominators) + Rule-24 pre-record for the lease state
    axis (MECE over the declared layer: VALID/INVALID/UNKNOWN/EXPIRED; hunt the uncovered member --
    e.g. NEVER_EVALUATED vs UNKNOWN -- and decide it in the record, not in code).
    Phase 2: mutant battery BEFORE commit: (m1) a support member changes and the lease is NOT
    re-evaluated -> it must read EXPIRED/UNKNOWN, never stay VALID; (m2) coordinate intersection
    that UNDER-includes -> fires; (m3) a new member claimed covered by an old enumerated waiver ->
    REFUSED; (m4) a second evaluation for the same (assessment, scope) -> REFUSED (one per pair);
    (m5) untyped silence offered as an exclusion proof -> REFUSED; determinism.
    Phase 3: live leases over >= 3 real closures from C3 + one re-evaluation exercised across a
    real support change (pick a Lambda whose tree moved today; the lease must flip).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - upstream: NFRA_EPISTEMY.C3-IDENTITY (yours) and 4.0.0_SA_CRO base's Knowledge_Basis schema
      act (S2) -- both must exist; 4.0.0_SA_CRO~A's certificates optional members.
    - downstream: components 5/6 (policy/scope/epoch; transaction kernel) consume leases and
      epochs -- staged at COO until base's S5 spec half lands; build nothing for them.
    - registry: Lease / Eligibility_Evaluation objects -> base registry-executes; CTO gates.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is COMPONENT 4 as cut -- L1 objects, L2 pipeline, L3
    failure-to-reevaluate, L4 waiver law, L5 live leases, L6 envelope join + battery, L7 proof;
    exhaustive over the component; components 5/6 OUTSIDE.)
    L1  Lease + Eligibility_Evaluation objects schema-native per PRD sec.2.5 (cited); four-state
        axis Rule-24-recorded; registry-executed via base; CTO-gated; S6 absence semantics on every
        nullable.
    L2  The invalidation pipeline runs in the spec's order (coarse intersection -> exclusion replay
        -> residual -> policy) and OVER-includes by construction (m2 fires on under-inclusion).
    L3  "FAILURE TO REEVALUATE NEVER PRESERVES VALIDITY" enforced: m1 fires; a stale lease cannot
        read VALID.
    L4  WAIVER LAW: a new member is never covered by an old enumerated waiver (m3); covered only by
        a ratified predicate whose declared scope includes it -- exercised both directions.
    L5  LIVE: >= 3 leases over real C3 closures + one real flip across a support change, with the
        Knowledge_Basis digest recorded on each evaluation.
    L6  Every acquisition emits an Observation_Record (UNKNOWN on failure); battery m1-m5 FIRE;
        determinism stable.
    L7  Proof instance VALID rc=0 positional L1-L7; RAVC close to COO, cc CTO + CRO base.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>L1,L2,L3,L4,L5,L6,L7</expected_criteria>
    <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_EPISTEMY.C4-LEASE_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Do not start before COO's GO (two activation conditions above). Bounds as C3: read-only live AWS, nothing armed, no deploys, registry acts through base. Normal cadence; surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
