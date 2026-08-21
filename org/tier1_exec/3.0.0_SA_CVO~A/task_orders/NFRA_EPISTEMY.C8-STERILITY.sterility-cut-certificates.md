<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-epistemy-c8-sterility</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>3.0.0_SA_CVO~A (Codex lane; lane-administered by 3.0.0_SA_CVO base -- GO gates on YOUR agent-side ack, SENT is not READ; the S4 pattern CRO base runs for ~A/~B)</issued_to>
    <date>2026-08-20</date>
    <status>pending -- STARTS on your ack (wave 2 of NFRA_EPISTEMY: envelope landed @45a2892ed2 + base S3 cert issued; CRO base 63752: "8 PARALLEL now -- precursors exercised; certifiable now; two conditions in the TO"; you read "awaiting scoped validation work" on the live roster 2110Z -- this is certificate work, the validation seat's own object)</status>
    <project_code>NFRA_EPISTEMY</project_code>
  </metadata>

  <objective>
    Build COMPONENT 8 -- STERILITY-CUT CERTIFICATES -- the certificate object that attests an
    ISOLATION CONTROL (a deny-cut) at a boundary, so that a diagnostic intervention is admissible
    WITHOUT an impossible universal census. The law, PRD sec.3 #3, verbatim: "A census is an
    observation; isolation is a control; when the census is incomplete, admission rests on the
    control." The estate's two strongest exercised controls ARE this object, uncertified:
    the bronze-parquet bucket deny (opal-data-assets, d89cc4fc9 -- exercised behavior-grade:
    AccessDenied naming the policy, an ISOLATED same-path positive control landed + deleted) and
    the firm-partition IAM deny (bd/cot/inf, runtime). Certify them; make the object leasable.
  </objective>

  <context>
    SPEC OF RECORD: PRD sec.1 row 8 + sec.3 law 3; Response IV sec.1.6
    (org/tier1_exec/4.0.0_SA_CRO/deliverables/RESPONSE_IV_HYPOTHESIS_SET_GOVERNANCE_20260820.md:76-90)
    -- "the deny-cut is cheaper to attest than the census is to complete, because it is one
    boundary with two controls instead of an open enumeration"; and its widening: reader-
    reachability -> PRODUCTION-INFLUENCE closure (a completion marker whose only consumer is a
    trigger; scheduled consumers not active during a census are invisible to reader enumeration).
    Response VII :110-114 -- the sterility-cut certificate must sit in the SUPPORT CLOSURE as a
    LEASED member; "a sterility cut as a mint-time check rather than a leased closure member
    reopens the hole silently." THE TWO CONDITIONS BASE NAMED (63752), binding: (i) Response IX
    sec.2.2 EXERCISED-WITNESS FLOOR
    (org/tier1_exec/4.0.0_SA_CRO/deliverables/RESPONSE_IX_EXERCISED_WITNESS_FLOOR_20260820.md:92-112)
    -- "a NEVER-EXERCISED path is ASSUMED and policy prices that assumption"; a certificate over a
    cut whose denial was never actually exercised on the real plane is ASSUMED, never PROVEN, and
    says so; (ii) the S6 ABSENCE-SEMANTICS MODEL (CTO 63744; base S3 cert): every nullable field
    NAMES what its absence disqualifies.

    WHAT THE CERTIFICATE CARRIES (cite-not-copy; base registry-executes the schema act): the
    BOUNDARY (bucket/prefix or principal partition), the CONTROL (policy identity + statement +
    document hash -- the hash is an invalidation predicate), the EXERCISED WITNESS (the denied act
    with its error naming the policy + the ISOLATED positive control that proves the instrument
    could have said otherwise, both with vintage), exercised/assumed STATUS, the SHARED FAILURE
    DOMAIN of control+witness + at least one INDEPENDENCE CROSSING (a second principal/tool/plane
    that would have surfaced a silent non-denial), the INFLUENCE-CLOSURE note (what triggers /
    automation, not just readers, the boundary isolates), vintage, invalidation predicates, and
    LEASE STATUS (UNLEASED until component 4 exists -- declared, not implied).

    CONSUMES C1: every acquisition (get-bucket-policy, a denied write attempt, a policy read) emits
    an Observation_Record; a failed acquisition is UNKNOWN, never "no deny found". BIND-TIME
    CONDITION, CTO 63744 verbatim, pinned: "no consumer may parse, branch on, or key off `plane`
    until the ratified plane enum + separate substrate field land" -- carry the field opaque until
    4.0.0_SA_CRO~A's rider hash is reported (base relays it).

    RIDERS (every NFRA_EPISTEMY TO, verbatim): (a) sec.2.9 is NOT buildable spec -- the harm
    surfaces are OPEN requirements (sec.4b); do not build against them. (b) CITE-NOT-COPY on shared
    objects; the Sterility_Cut_Certificate is a NEW object -> its schema act routes through
    4.0.0_SA_CRO base (registry executor, S2) with Rule-24 record + token census, base's spec cert
    precedes 1.0.0_SA_CTO's arch gate -- NEVER landed in-lane. (c) interim shapes resolve into the
    envelope. FIRST ACT = S0 ground-read of the two precursors AT SOURCE (the bucket policy
    document; the firm IAM deny statements) with the exercised evidence located by record (CLAUDE.md
    Rule 17a gate note; firm-separation IAM) -- print what is exercised-on-record and what is only
    declared.
  </context>

  <compiler_tools_mandate>
    Phase 1: S0 (above); comp-iam on the denying principals as the FLOOR (Rule 22a: comp-iam
    models (action), never (action, resource) -- the live primitive is `aws iam
    simulate-principal-policy` with ONE --resource-arns per call and the positive control as a
    SEPARATE invocation; NEVER use it to check an action NAME); Rule-24 pre-record for the
    certificate's status axis (MECE over the declared layer: PROVEN / ASSUMED / UNMEASURED /
    UNKNOWN -- hunt the uncovered member; an expired witness is which?).
    Phase 2: mutant battery BEFORE commit: (m1) a cut with NO exercised witness presented as
    PROVEN -> REFUSED/ASSUMED; (m2) a witness whose positive control was not isolated -> REFUSED;
    (m3) the policy document hash changes -> certificate reads UNMEASURED on re-read; (m4) a
    certificate whose witness and control share a total failure domain with no crossing ->
    INADMISSIBLE as a reliance member; (m5) null witness / null crossing -> the S6 disqualification
    fires by name; determinism (two runs byte-identical).
    Phase 3: TWO LIVE CERTIFICATES over the two precursors. The bronze-parquet witness: cite the
    recorded exercise (d89cc4fc9, isolated positive control landed+deleted) AND re-exercise the
    denial READ-ONLY if that is possible without landing an object (a denied PutObject attempt is
    itself the witness -- it writes nothing; state exactly what you ran). The firm IAM witness:
    simulate-principal-policy per the rule above + the recorded runtime deny. NO new object landed
    in any bucket without COO's word -- the recorded positive control is citable evidence; a fresh
    positive control that LANDS an object is an act you surface first.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - lane admin: 3.0.0_SA_CVO base relays this TO to you over the Codex channel, administers your
      review gate, and carries your RAVC close to COO (the S4 pattern); base's own verification acts
      are unchanged and remain independent of this build.
    - registry: Sterility_Cut_Certificate -> 4.0.0_SA_CRO base registry-executes (S2), 1.0.0_SA_CTO
      arch-gates; CTO also owns the firm-separation gate + the 17a bucket policy -- READ them; any
      change to a policy is a CTO act, never this TO's.
    - downstream: component 4 (0.8.0_AE_CloudComp, staged) will lease these certificates;
      component 2 (4.0.0_SA_CRO~A) certifies the INSTRUMENTS you use (until it lands, your
      discrimination_certificate_ref stays null -- declared absence); component 7
      (4.0.0_SA_CRO~B, influence closure) is the long-run source of the influence-closure note --
      today you record what is known and mark the rest UNKNOWN.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is COMPONENT 8 as cut -- K1 object, K2 live certificates,
    K3 witness floor, K4 absence semantics, K5 expiry + crossing, K6 nothing armed + envelope join
    + battery, K7 proof; exhaustive over the component; new deny-cuts and components 2/4/7 OUTSIDE.)
    K1  Sterility_Cut_Certificate schema-native, citing PRD sec.1 row 8 + sec.3 law 3 + Response IV
        1.6 + Response IX 2.2 + Response VII as sources of record; Rule-24 record + token census
        through base; CTO gate; status axis MECE with UNKNOWN + UNMEASURED explicit.
    K2  TWO LIVE CERTIFICATES: the bronze-parquet bucket deny and the firm-partition IAM deny, each
        with boundary, control (+document hash), exercised witness (+isolated positive control,
        both vintaged), shared failure domain + >=1 independence crossing, influence-closure note,
        lease status UNLEASED (declared).
    K3  WITNESS FLOOR: a cut with a never-exercised denial certifies ASSUMED (priced), never PROVEN
        (m1); exercised-on-record vs re-exercised-now distinguished in the object.
    K4  ABSENCE SEMANTICS: every nullable field's disqualification named AND tested (m5) -- null
        witness -> ASSUMED; null crossing -> INADMISSIBLE as a reliance member.
    K5  EXPIRY + CROSSING ENFORCED: policy hash change -> UNMEASURED (m3); total-shared-failure-
        domain -> INADMISSIBLE (m4); m2 fires on a non-isolated positive control.
    K6  NOTHING ARMED: no new deny, no policy edit, no alert/monitor/gate (candidates PROPOSED only,
        routed to CTO); no object landed without COO's word; every acquisition emits an
        Observation_Record (UNKNOWN on failure); `plane` carried opaque until the rider hash;
        battery m1-m5 FIRE; determinism stable.
    K7  Proof instance VALID rc=0 positional K1-K7; RAVC close via 3.0.0_SA_CVO base to COO, cc
        1.0.0_SA_CTO + 4.0.0_SA_CRO (spec cert).
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>K1,K2,K3,K4,K5,K6,K7</expected_criteria>
    <instance_path>org/tier1_exec/3.0.0_SA_CVO~A/deliverables/NFRA_EPISTEMY.C8-STERILITY_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">GO gates on your ack (via 3.0.0_SA_CVO base). Normal cadence. Read-only against live AWS except the explicitly-stated denied-write witness (which lands nothing); every count with its denominator; an absence verdict names the tree/bucket/principal it searched (Rule 21 firm-scope law). Surprise channel: one line to CVO base -> COO.</requirement>
  </requirements>
</task_order>
