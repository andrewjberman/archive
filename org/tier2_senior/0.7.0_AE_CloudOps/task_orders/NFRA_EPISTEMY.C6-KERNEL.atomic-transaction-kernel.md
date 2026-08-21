<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-21-epistemy-c6-kernel</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-08-21</date>
    <status>complete -- COO VALIDATED 2026-08-21T0502Z (64564 ack): battery 9/9 rc=0 re-run COLD at COO's own HEAD 7f3c1658572b BEFORE opening the proof; both inexpressibility claims probed by hand with their probe POSITIVE-CONTROLLED against a deliberately leaky class; and a THREE-CLAUSE INDEPENDENCE MUTANT (disarm each per-leg clause -> rc=1, 8/9, exactly the right check dead, three times) which DEMONSTRATED the clause-independence my own battery only ASSERTED. -- ALL 7 CRITERIA MET. Proof VALID rc=0 UNPIPED. CRO base spec cert @b895b7e337 (CERTIFIED-WITH-ONE-MINT; condition A1 = mint FAILED_MID_ACT on the LegOutcome axis, discharged @4914a06ac0 with battery case m8). CTO arch gate PASS (64541), every bar item exercised at CTO's own seat: module loaded and attacked 7/7 refused with the positive control firing, battery re-run 9/9 rc=0 in their run, FAILED_MID_ACT confirmed to have a REAL WRITE PATH that re-raises, sibling-substring check over 5 values / 20 ordered pairs = 0 collisions, and the vintage pins 3/3 MATCH against a NEGATIVE CONTROL THAT MISMATCHED. RAVC close SENT to COO cc CTO/CRO/0.8.0 (64547/64548/64549/64550, 4 DELIVERED / 0 QUEUED / 0 REFUSED). ⛔ THE FENCE STANDS AND IS NOT DISCHARGED BY THIS CLOSE: the gate covers the OBJECTS, not a live mutation class. Everything was exercised on FIXTURES -- emissions are EXERCISED/codebase, not APPLIED/aws, and plane/substrate are constructor parameters so an activated call site cannot inherit a fixture's identity. ACTIVATION AGAINST ANY REAL MUTATION CLASS IS ANDREW'S WORDED ACT AND NOBODY ELSE'S; the kernel is imported by NOTHING on a live path. AWAITING: COO validation. ORIGINAL: active -- ACTIVATED 2026-08-21T0309Z by COO GO 64235 (NFRA_EPISTEMY.C4-LEASE CLOSED on COO's independent cold exercise: 14/14 battery at their own HEAD, 4 engine + 2 validator mutants killed, and a VALID->EXPIRED flip observed on a lease they minted themselves across a live commit window). ACK'd 0316Z. Phase 1 (S0 embryo ground-read) in progress at 0.7.0_AE_CloudOps. INTAKE CONSTRAINT CARRIED FROM THE GO, COO note (b): repo_head is a support member, so a lease is structurally short-lived in this worktree and any consumer treating VALID as durable across its own runtime is wrong -- which would silently convert a lease into a lock, the one thing PRD sec.2.7 forbids by name. m5 as cut catches an over-asking claim at leg-open and does NOT catch a claim that was honest at leg-open and expired by leg-3; ADDING m7 (VALID at leg-open, EXPIRED at a later checkpoint, kernel proceeds -> must REFUSE), i.e. per-checkpoint re-read, cached verdict inexpressible. BUILD-STAGING FENCE UNCHANGED: no live wiring, no armed gate, activation on any real mutation class is ANDREW'S WORDED ACT. ORIGINAL: staged -- ACTIVATES on COO GO when NFRA_EPISTEMY.C4-LEASE (0.8.0_AE_CloudComp, in flight) closes, because the kernel's support handoff leases claims and a lease that does not exist cannot be honoured. CUT NOW, NOT LATER, so the activation costs zero round-trips: you built the precondition token (C10-PRECOND @82c3f36f24 + @cde3d4ba59), which IS this component's atomic-binding primitive, and the kernel is mostly WIRING EXISTING CONTROLS rather than a greenfield build (CTO 63768). Zero urgency, no clock.</status>
    <project_code>NFRA_EPISTEMY</project_code>
  </metadata>

  <objective>
    Build COMPONENT 6 -- THE ATOMIC TRANSACTION KERNEL (PRD sec.1 row 6, sec.2.7): precondition
    tokens, ledgers, rollback manifests, continuation capabilities -- "binds check to act; epoch
    pinning at change-unit grain." The estate already runs the pieces UNCONNECTED: git push token
    semantics (rejected push = token mismatch), safe-commit's lock, the deploy-completion ledger
    (element E's embryo), TF plan staleness against the state serial (a partial token), and YOUR
    precondition token (the only one that binds a plain S3 put). THE NAKED SPOT NAMED BY THE PRD
    IS RAW S3 PUT, and you already closed it for one bounded class -- this component generalises
    that binding into a kernel the other components transact through.
  </objective>

  <context>
    SPEC OF RECORD: PRD sec.2.7 Transition_Unit -- governed chains where LONG TRANSITIONS ARE NOT
    LONG TRANSACTIONS: an immutable transition manifest (graph, targets, action classes,
    checkpoints, terminals incl. rollback + containment); a PATHWISE RESIDUE ENVELOPE (a
    structured vector of incomparable limits, NEVER a scalar); a Cumulative_Residue_Ledger
    (gateway-maintained -- AGENT SELF-REPORT IS INADMISSIBLE); a recovery-capacity function with
    declared points of no return; policy_epoch + knowledge_basis + harm_model stamps. PREFIX
    SAFETY AT EVERY LEG: residue within envelope AND a safe terminal reachable AND recovery
    requirement <= remaining capacity -- ROLLBACK DEBT PRICED, which is the half-landed-deploy
    class finally instrumented (NEVER#8 is the law; this is its mechanism). Support handoff per
    claim: Required_Validity_Interval(c) SUBSET-OF Actual_Validity_Interval(c) -- A LEASE IS NOT
    A LOCK; tokens and isolation bind check to act. "The opening word accepts the envelope; each
    checkpoint proves the path remains inside it."
    ALSO: S5 sec.4's estate-correspondence map (the transaction gate's embryos, enumerated) and
    Response IX sec.2.2's EXERCISED-WITNESS FLOOR -- a recovery path never run on the real plane
    is ASSUMED and policy prices that assumption; "an estate that never rehearses recovery is
    holding reachability certificates issued by the map about the map." Our exercised embryo is
    same-window rollback verification on ports.

    CONSUMES: C1 (every acquisition emits an Observation_Record; the ratified plane enum +
    substrate are live as of @6f944857c4 -- emit them, the bind-time condition is discharged);
    C4's leases for the support-handoff inequality; your own Precondition_Token as element D.
    S6 absence-semantics model on every nullable: a null names what its absence DISQUALIFIES.

    RIDERS (every NFRA_EPISTEMY TO, verbatim): (a) sec.2.9 is NOT buildable spec -- the harm
    surfaces are OPEN requirements (sec.4b); the harm_model stamp is CITED AS A STAMP ONLY and
    nothing here builds against it. (b) CITE-NOT-COPY: new objects (Transition_Unit,
    Cumulative_Residue_Ledger, Transition_Manifest) route through 4.0.0_SA_CRO base as registry
    executor with a Rule-24 record + token census; base's spec cert precedes 1.0.0_SA_CTO's arch
    gate; NEVER landed in-lane. (c) interim shapes resolve into the envelope.

    ⛔ BUILD-STAGING ONLY, AND THIS IS THE SAME FENCE C10 CARRIED: nothing here is wired to any
    live write path, no gate is armed on any real work, and ACTIVATION of the kernel on any real
    mutation class is ANDREW'S WORDED ACT -- not mine, not CTO's, not yours. The deliverable is a
    kernel plus an EXERCISE on scratch-scoped or fixture transitions.
  </context>

  <compiler_tools_mandate>
    Phase 1: S0 ground-read of the five named embryos AT SOURCE with denominators (safe-commit's
    lock + ref token; safe-apply/HALTGT; the deploy-completion ledger schema in
    org/critical_paths/change_management/; TF state-serial staleness; your precondition_token) --
    state for each what it BINDS and what it does NOT; comp-blast before touching any of them
    (you will not modify them in this TO). Rule-24 pre-record for the terminal/checkpoint axis
    (MECE over the declared layer; hunt the uncovered member -- e.g. is CONTAINED distinct from
    ROLLED_BACK).
    Phase 2: mutant battery BEFORE commit: (m1) a leg proceeds while residue is OUTSIDE the
    envelope -> REFUSED; (m2) a leg proceeds with NO safe terminal reachable -> REFUSED; (m3)
    recovery requirement EXCEEDS remaining capacity -> REFUSED (rollback debt priced, not
    ignored); (m4) an AGENT SELF-REPORTED residue row accepted into the ledger -> REFUSED
    (inadmissible by construction, the C7 hand-authored-row control's sibling); (m5) a claim whose
    Required_Validity_Interval exceeds its Actual -> REFUSED; (m6) a recovery path never exercised
    presented as PROVEN -> ASSUMED-and-priced, never PROVEN. Determinism: two runs byte-identical.
    Phase 3: exercise a multi-leg transition end to end on scratch/fixture -- including ONE leg
    that must ABORT at a checkpoint and reach its rollback terminal, with the ledger showing the
    priced debt. An abort you cannot demonstrate is a terminal you do not have.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - 0.8.0_AE_CloudComp (C4-LEASE): leases are your support-handoff input; do not re-implement
      lease semantics -- consume them. Coordinate by MCP; their close is your activation.
    - 4.0.0_SA_CRO base: registry executor for the new objects (S2), spec cert against sec.2.7
      before CTO's gate.
    - 1.0.0_SA_CTO: arch gate; also the owner of the deploy-completion ledger law -- the kernel
      READS that ledger's shape as a precursor and proposes nothing to it in-lane.
    - The digest derivation home is YOUR precondition_token.py _request_hash (normative; any other
      serialization is NON-CONFORMANT even if the sha256 pattern matches -- CTO's 0.1.0 exercise).
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is COMPONENT 6 as cut -- K1 objects, K2 prefix safety,
    K3 ledger admissibility, K4 support handoff, K5 exercised abort, K6 envelope join + battery,
    K7 proof; exhaustive over the component; the gateway (10-build), the harm algebra (2.9) and
    any live wiring are OUTSIDE.)
    K1  Transition_Unit + Transition_Manifest + Cumulative_Residue_Ledger schema-native per PRD
        sec.2.7 (cited, not copied); Rule-24 record + token census through base; CTO gate; S6
        absence semantics on every nullable; the residue envelope is a STRUCTURED VECTOR and a
        scalar residue is inexpressible by construction.
    K2  PREFIX SAFETY ENFORCED AT EVERY LEG: residue-within-envelope AND safe-terminal-reachable
        AND recovery-requirement <= remaining-capacity, all three checked per checkpoint; m1/m2/m3
        FIRE.
    K3  LEDGER ADMISSIBILITY: the Cumulative_Residue_Ledger is kernel-maintained and an
        agent-self-reported row CANNOT enter it (m4 fires) -- inadmissible by construction, not by
        review.
    K4  SUPPORT HANDOFF: Required_Validity_Interval SUBSET-OF Actual_Validity_Interval per claim,
        consuming C4 leases; m5 fires; "a lease is not a lock" stated on the object.
    K5  EXERCISED ABORT: a multi-leg transition run on scratch/fixture where one leg aborts at a
        checkpoint and reaches its ROLLBACK terminal, with the priced rollback debt in the ledger;
        a never-exercised recovery path reads ASSUMED (m6), never PROVEN.
    K6  Every acquisition emits an Observation_Record carrying the RATIFIED plane enum +
        substrate (the bind-time condition is discharged at @6f944857c4); battery m1-m6 FIRE;
        determinism STABLE.
    K7  Proof instance VALID rc=0 positional K1-K7 (rc UNPIPED); RAVC close to COO, cc
        1.0.0_SA_CTO + 4.0.0_SA_CRO + 0.8.0_AE_CloudComp.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>K1,K2,K3,K4,K5,K6,K7</expected_criteria>
    <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_EPISTEMY.C6-KERNEL_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Do not start before COO's GO (activation = C4-LEASE closes). BUILD-STAGING ONLY: no live wiring, no armed gate, no alert/monitor; activation on any real mutation class is Andrew's worded act. Do not modify safe-commit, safe-apply, HALTGT, or the deploy-ledger in this TO -- you READ them as precursors. Scratch/fixture only on the real plane, and name every scratch object you mint and delete. Surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
