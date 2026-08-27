<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-21-epistemy-c5-policy</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-08-21</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_EPISTEMY, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active -- ACTIVATED 2026-08-21T0620Z by COO GO (64596). Precondition discharged: C6-KERNEL closed 0503Z and COO-validated (64559). ACK'd 0618Z; I answered COO's now-or-morning question with NOW and COO WITHDREW the deferral option, not merely its framing -- deferring with an idle seat and a just-satisfied precondition is the CLAUDE.md coast-failure, and a TO carrying no clock is a reason not to RUSH it, not a reason not to START it. GOVERNING CONSTRAINT, ratified by COO OVER THEIR OWN PROSE where the two diverge: the scope engine is INERT BY CONSTRUCTION, NOT INERT BY CONFIGURATION -- a config flag that could be flipped to make it binding is one commit from an approval step nobody authorized, which is the accident this TO's doubled fence exists to prevent. PRECEDENCE RATIFIED IN ADVANCE (COO 64596): if COT_SUPERVISED.G4-ACCEPT-HANDOVER fires at 10:30Z because no PartnerETL seat is live, IT TAKES PRECEDENCE and interrupting C5 is CORRECT. Adopting COO's clause-independence mutant for C5's conjunctive predicates -- the C6 battery proved PRESENCE and only ASSERTED independence; that gap does not repeat. ORIGINAL: staged -- ACTIVATES on COO GO, sequenced AFTER NFRA_EPISTEMY.C6-KERNEL at your seat (the epoch service stamps what the kernel transacts, so building the stamp before the thing it stamps inverts the dependency). CUT NOW so the activation costs zero round-trips. The PRD builds 5 and 6 in parallel with 1-4; at this seat they are sequential because one seat cannot parallelise itself -- if a second AE-class lane comes live, this TO moves to it unchanged. Zero urgency, no clock.</status>
    <project_code>NFRA_EPISTEMY</project_code>
  </metadata>

  <objective>
    Build COMPONENT 5 -- POLICY OBJECTS + SCOPE ENGINE + EPOCH SERVICE (PRD sec.1 row 5):
    "mechanically enforceable authority vs policy-shaped inference." The estate's precursors are
    the ACT-TIME GATEWAY EMBRYO already running: owned-paths (ENUMERATED waivers), lane classes
    (PREDICATES), and the PreToolUse hook layer -- your own hook ecosystem. The component turns
    those into typed objects with a scope engine that can answer "is this act inside this
    authority's declared scope?" mechanically, plus an epoch service that pins WHEN a policy was
    in force.
  </objective>

  <context>
    SPEC OF RECORD: PRD sec.2.5's waiver law -- "A NEW MEMBER IS NEVER COVERED BY AN OLD
    ENUMERATED WAIVER; it may be covered by a RATIFIED PREDICATE whose declared scope includes
    it." That single sentence is the component's spine and it is the exact distinction the
    estate's own owned-paths file lives on: an enumerated path list is a WAIVER SET (a new file is
    NOT covered), a lane-class predicate is a PREDICATE (a new member IS covered if it satisfies
    the declared scope). Also sec.2.6's authority/scope gate with its TYPED rejection
    (AUTHORITY_SCOPE_MISS) and policy_epoch; S5 (@c67ef52c1a, CTO PASS-AS-SPEC 63768) sec.2/sec.4
    -- the two-field rejection (gate x reason, never flattened), `required_authority_class` AS A
    FIELD NOT A THRESHOLD ("no proof count reaches a word" -- evidence never converts into
    authority), and the estate-correspondence map naming owned-paths + lane refusals as the
    authority gate's live embryo.

    ⛔ THE FENCE THAT MATTERS MOST ON THIS COMPONENT, and it is not a formality: THIS IS A
    SPECIFICATION AND A BUILD OF OBJECTS, NOT AN ACTIVATION OF ANY APPROVAL STEP. Andrew's
    standing law is that NO GATE IS IMPLEMENTED ON ANY WORK WITHOUT HIS EXPLICIT WORD, and a
    "scope engine" is precisely the shape that could become one by accident. Nothing in this TO
    evaluates a real act, blocks a real commit, or wires into a real hook. The engine answers
    questions ABOUT declared policy objects, on fixtures and on READ-ONLY snapshots of the
    existing enumerations. If you find yourself editing a live hook, you are outside this TO.

    CONSUMES C1: every acquisition emits an Observation_Record with the RATIFIED plane enum +
    substrate (discharged @6f944857c4). S6 absence semantics on every nullable.
    RIDERS (verbatim, every NFRA_EPISTEMY TO): (a) sec.2.9 is NOT buildable spec; (b)
    CITE-NOT-COPY -- Policy_Object / Scope_Declaration / Policy_Epoch route through 4.0.0_SA_CRO
    base as registry executor with Rule-24 record + token census, base's cert precedes CTO's arch
    gate, NEVER landed in-lane; (c) interim shapes resolve into the envelope.
  </context>

  <compiler_tools_mandate>
    Phase 1: S0 ground-read of the live embryos WITH DENOMINATORS, read-only: .owned-paths.yaml
    (how many path rules are ENUMERATIONS vs how many lanes are PREDICATES -- that count IS the
    component's motivating measurement), the PreToolUse hook layer's refusal types, and the
    distinction between a lane refusal and a gate failure that safe-commit already draws
    (safe-commit.sh:547 -- "--force does NOT bypass a gate FAILURE"). Rule-24 pre-record for the
    rejection axis: REUSE S5 sec.2's two-field (gate, reason) shape -- do NOT re-coin reasons; if
    you need one S5 lacks, that is a PROPOSAL to base, exactly as C10's TOKEN_INADMISSIBLE was
    (and note base HOMED those cases at (COMPILATION, BUNDLE_MALFORMED) instead -- two remedies
    never share one gate).
    Phase 2: mutant battery BEFORE commit: (m1) a NEW member claimed covered by an OLD ENUMERATED
    waiver -> REFUSED (the sec.2.5 law, the component's spine); (m2) the same new member under a
    RATIFIED PREDICATE whose declared scope includes it -> ADMITTED (the positive control that
    proves m1 discriminates rather than just denying); (m3) an act evaluated against a policy
    epoch that was not in force at the act's instant -> REFUSED; (m4) a scope miss returned as a
    generic failure instead of the typed (AUTHORITY, AUTHORITY_SCOPE_MISS) pair -> the battery
    FAILS; (m5) `required_authority_class` satisfied by an accumulation of evidence -> REFUSED
    (no proof count reaches a word). Determinism: two runs byte-identical.
    Phase 3: the engine answers over a READ-ONLY snapshot of the real enumerations -- report how
    many real owned-paths rows are enumerations vs predicates, with the denominator printed. This
    is a MEASUREMENT of the estate's authority surface, not an enforcement of it.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - 4.0.0_SA_CRO base: registry executor + spec cert (S2/S3 pattern) before CTO's arch gate.
    - 1.0.0_SA_CTO: arch gate; owner of the hook/gate layer -- any proposal touching a live hook
      is theirs to route and ANDREW'S to authorize, never this TO's act.
    - C6-KERNEL (yours, sequenced first): the kernel consumes policy_epoch stamps; build the epoch
      service so the kernel's stamp has a real source rather than a placeholder.
    - 0.8.0_AE_CloudComp C4-LEASE: eligibility evaluation applies a POLICY PREDICATE -- align the
      predicate shape with theirs by MCP rather than minting a second vocabulary.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is COMPONENT 5 as cut -- P1 objects, P2 the waiver law,
    P3 epoch, P4 typed rejection, P5 measurement, P6 envelope join + battery, P7 proof; exhaustive
    over the component; the gateway (10-build), the kernel (C6) and any live enforcement are
    OUTSIDE.)
    P1  Policy_Object + Scope_Declaration + Policy_Epoch schema-native per PRD sec.2.5/2.6 + S5
        (cited, not copied); Rule-24 record + token census through base; CTO gate; S6 absence
        semantics on every nullable; `required_authority_class` is a FIELD, never a threshold.
    P2  THE WAIVER LAW ENFORCED BY CONSTRUCTION: m1 fires (new member vs old enumerated waiver ->
        REFUSED) AND m2 admits the same member under a ratified predicate whose declared scope
        includes it -- both directions exercised, because a denier that denies everything is not a
        discriminator.
    P3  EPOCH REAL: an act is evaluated against the policy in force AT ITS INSTANT; m3 fires;
        epochs carry vintage and are consumable as a stamp by C6.
    P4  TYPED REJECTION: (gate, reason) two-field per S5 sec.2, reasons REUSED not re-coined; a
        scope miss returns (AUTHORITY, AUTHORITY_SCOPE_MISS); m4 fires on a flattened/generic
        failure; m5 fires on evidence-substituting-for-authority.
    P5  MEASUREMENT, NOT ENFORCEMENT: the read-only census of the real enumerations reports the
        enumeration-vs-predicate split with its denominator printed; NOTHING in the estate's live
        authority surface is edited, and the proof says so.
    P6  Every acquisition emits an Observation_Record with the ratified plane enum + substrate;
        battery m1-m5 FIRE; determinism STABLE.
    P7  Proof instance VALID rc=0 positional P1-P7 (rc UNPIPED); RAVC close to COO, cc
        1.0.0_SA_CTO + 4.0.0_SA_CRO + 0.8.0_AE_CloudComp.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>P1,P2,P3,P4,P5,P6,P7</expected_criteria>
    <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_EPISTEMY.C5-POLICY_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Do not start before COO's GO (sequenced after C6-KERNEL at this seat). ⛔ NO LIVE HOOK IS EDITED, NO GATE IS ARMED, NO REAL ACT IS EVALUATED -- objects + engine + fixtures + a read-only census only; activation of any scope check on real work is ANDREW'S worded act. No alert/monitor machinery. Surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
