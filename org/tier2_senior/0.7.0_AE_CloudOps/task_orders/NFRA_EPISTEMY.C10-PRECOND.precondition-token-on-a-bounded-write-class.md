<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-epistemy-c10-precond</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-08-20</date>
    <status>pending -- STARTS NOW (your board cleared on DORMANT2's close ~2132Z; CTO 63768 + CRO base 63818: "pull the precondition-token leg EARLY as its own small build"). BUILD-STAGING ONLY: THIS TO DOES NOT ACTIVATE ANYTHING ON ANY LIVE WRITE PATH -- activation of the token check as a live gate on real writes is ANDREW'S WORDED ACT, not this TO's and not COO's/CTO's (the no-gates law; S5 header verbatim: "no reader may cite this document as authority to switch anything on").</status>
    <project_code>NFRA_EPISTEMY</project_code>
  </metadata>

  <objective>
    Build the PRECONDITION-TOKEN leg of COMPONENT 10 early, as its own small build: the
    Precondition_Token object {target_state_digest, read_at, read_window} (S5 sec.1, the
    `precondition_token` row; PRD sec.2.6 element D -- "atomically bound") + an atomically-bound
    capability-check for ONE NAMED, BOUNDED S3 write class, using the store's own conditional
    write (S3 If-Match / If-None-Match) where it provides it, with the TYPED two-field rejection
    (gate=TRANSACTION, reason=PRECONDITION_CHANGED -- S5 sec.2). Why early (CTO 63768, verbatim
    grain): "THE NAKED LAYER IS PLAIN S3 PUT. Everything else in component 10 gates a capability
    that does not exist yet; the precondition token gates writes THAT ARE HAPPENING TODAY, on the
    one surface with no atomic binding at all ... a rung-2 assembly rather than a greenfield
    build -- independently valuable even if component 10 never ships." Exercised on the bounded
    class's REAL PLANE in scratch-scoped form; NEVER a global write gate.
  </objective>

  <context>
    SPEC OF RECORD: org/tier1_exec/4.0.0_SA_CRO/deliverables/NFRA_EPISTEMY/S5_PROFILE_ALGEBRA_AND_MUTATION_GATEWAY_SPEC_20260820.md
    (PASS-AS-SPEC, CTO 63767/63768; 0.1.1 @4c023d5725) -- sec.1 row `precondition_token` ("LIVE
    read inside the declared window, ATOMICALLY BOUND (git ref / TF state serial / conditional-
    write where the store provides it; named GAP where it does not, e.g. plain S3 put); a token
    older than its window at act time = PRECONDITION_CHANGED"), sec.2 (two-field rejection: gate x
    reason; TRANSACTION reasons incl. PRECONDITION_CHANGED), sec.4 (estate correspondence: the
    transaction gate's embryos are safe-commit's remote-ref token, safe-apply/HALTGT, the
    deploy-completion ledger, TF plan staleness vs state serial; "the NAKED layer = plain S3 put (no
    token, last-writer-wins -> conditional-write where provided, named gap otherwise)"); PRD sec.2.6
    (element D) + sec.1 row 6 ("Naked spot: raw S3 put"). CTO's condition, verbatim: "it lands as a
    capability-check on a NAMED, BOUNDED write class first -- exercised there before anything
    wider, and never as a global write gate, which would be an activation act and is not yours or
    mine to take." Sequence against component 4 ONLY where lease semantics are needed -- the S3-put
    binding does not need them (CTO), so this TO has NO C4 dependency.

    THE NAMED BOUNDED WRITE CLASS (COO's choice; base/CTO may re-name at the spec cert -- say so
    if you disagree, in one line): THE DEPLOY CODE-ARTIFACT PUT -- `.tools/safe-deploy.sh` /
    `safe_deploy_core.py`'s `aws s3 cp` of gold/silver scripts to the `.../code/` prefixes of the
    firm trees (Rule 13; PIPELINE_MAP bd/inf/cot/mdpf; key-exists=update under the S3-membership
    guard). WHY THIS CLASS AND NOT A SERVED KEY (base nominated "one served-key class with the
    narrowest reader set"; recorded as the alternative): (i) BOUNDED -- one tool, four trees, an
    enforced update-vs-first-mint grammar already; (ii) NON-SERVED -- readers are the runners,
    NEVER#3 is not engaged, so the first exercise cannot strand a client-facing publish; (iii) a
    MEASURED incident in exactly this class: 2026-07-13, a hung `aws s3 cp --quiet` REPORTED
    SUCCESS while S3 kept the old artifact, and the upload-verify gate existed on 1 of 4 call sites
    (CLAUDE.md Git section) -- the last-writer-wins + no-verify shape the token exists to bind;
    (iv) FAILURE DIRECTION IS SAFE -- a refused code put fails LOUD at deploy time toward inaction;
    a refused served put fails toward a stranded publish, the expensive direction. Build the leg
    CLASS-AGNOSTIC (bucket/key/body/token) so the served class is a config choice later, under
    Andrew's word.

    BUILD LADDER, stated: S3 conditional writes are a NATIVE platform feature (rung 4) -- no new
    service, no lock table, no DynamoDB, no second store; the token's digest is the object ETag
    (or sha256 of the read bytes where ETag is multipart-ambiguous -- state which and why);
    read_window is declared, not defaulted.

    CONSUMES C1: every read/acquisition emits an Observation_Record (UNKNOWN on failure -- a
    head-object that fails is not "no object"); BIND-TIME CONDITION, CTO 63744 verbatim, pinned:
    "no consumer may parse, branch on, or key off `plane` until the ratified plane enum + separate
    substrate field land" -- carry the field opaque until 4.0.0_SA_CRO~A's rider hash is reported.
    S6 absence-semantics model on every nullable (a null read_window is not "no window" -- it is
    REFUSED).

    RIDERS (every NFRA_EPISTEMY TO, verbatim): (a) sec.2.9 is NOT buildable spec -- do not build
    against the harm surfaces; (b) CITE-NOT-COPY; the Precondition_Token object's schema act routes
    through 4.0.0_SA_CRO base (registry executor, S2) with Rule-24 record + token census, base's spec
    cert precedes 1.0.0_SA_CTO's arch gate -- NEVER landed in-lane; (c) interim shapes resolve into
    the envelope. FIRST ACT = S0 ground-read: the S3-put call sites of the bounded class
    (DENOMINATOR printed: how many call sites, which carry upload-verify today), the S3 conditional-
    write semantics AT SOURCE (botocore/AWS doc for If-Match / If-None-Match on PutObject, incl. the
    412 contract), and S5 sec.1/2/4.
  </context>

  <compiler_tools_mandate>
    Phase 1: S0 (above); comp-blast on safe_deploy_core.py (you will NOT edit its live path, but
    you will write the wiring PLAN against it, so know its consumers); comp-iam FLOOR on the
    principal that will exercise the scratch put (Rule 22a: comp-iam models (action) never
    (action, resource) -- the live primitive is `aws iam simulate-principal-policy` with ONE
    --resource-arns per call, positive control as a SEPARATE invocation; never to check an action
    NAME); Rule-24 pre-record for the rejection reason values you use (cite S5 sec.2 -- reuse, do
    not re-coin; if you need a reason S5 lacks, that is a proposal to base, not a local enum).
    Phase 2: mutant battery BEFORE commit (below, P4); determinism (two runs byte-identical).
    Phase 3: the scratch-scoped exercise on the real plane (P3) with every count's denominator and
    the scratch key named; scratch objects removed afterwards (the ONLY deletes in this TO are of
    the scratch objects you minted -- name them).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - spec owner 4.0.0_SA_CRO base: Precondition_Token schema act (S2) + spec cert against S5 sec.1;
      the named-class choice is reviewable at that cert.
    - 1.0.0_SA_CTO: arch gate after base's cert; owner of the deploy mechanics law (Rules 13/14,
      safe-deploy) -- the WIRING PLAN for the live class is delivered to CTO as a PROPOSAL with its
      activation condition (`# andrew-asked: <verbatim + date>`), never applied.
    - safe-deploy (`.tools/safe-deploy.sh`, `safe_deploy_core.py`): READ; its live path is NOT
      modified by this TO.
    - 0.8.0_AE_CloudComp (C4 lease): no dependency -- the S3-put binding needs no lease semantics;
      your token object must be leasable later (vintage + invalidation predicates present).
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is the PRECONDITION-TOKEN LEG as cut -- P1 object, P2
    bound check, P3 exercise, P4 battery, P5 no-activation + wiring plan, P6 envelope join, P7
    proof; exhaustive over the leg; the gateway, profile algebra, and any live wiring are OUTSIDE.)
    P1  Precondition_Token object schema-native per S5 sec.1 `precondition_token` + PRD sec.2.6
        element D (cited, not copied); Rule-24 record + token census through base; CTO gate; S6
        absence semantics (null read_window / null digest -> REFUSED, named).
    P2  ATOMICALLY BOUND: `put_if_precondition(bucket, key, body, token)` uses the store's
        conditional write (If-Match <etag> for update; If-None-Match:* for first mint); the token is
        read inside its declared window; an out-of-window token is rejected BEFORE any call; a
        precondition failure returns the TYPED two-field rejection (gate=TRANSACTION,
        reason=PRECONDITION_CHANGED) and the object is byte-unchanged (verified by re-read, not
        assumed).
    P3  EXERCISED ON THE REAL PLANE, scratch-scoped, under the bounded class's bucket (scratch key
        named in the proof): (a) fresh token -> put succeeds + re-read verifies bytes; (b) a second
        writer changes the object under a held token -> 412 -> PRECONDITION_CHANGED, bytes
        unchanged; (c) window expired -> rejected with no call made; (d) first-mint succeeds once,
        the repeat is rejected; denominators printed; scratch objects deleted afterwards (named).
    P4  MUTANT BATTERY, all FIRE: (m1) conditional header removed -> test (b) FAILS (the header is
        load-bearing); (m2) token without read_window -> REFUSED; (m3) digest computed from the
        wrong object -> REFUSED; (m4) a "successful" put that skips the verifying re-read -> the
        battery FAILS (the 2026-07-13 class, hung-cp-reports-success); determinism stable.
    P5  NO ACTIVATION, STATED AND TRUE: safe-deploy's live path is byte-unchanged (cite the sha);
        no global write gate; nothing armed; the WIRING PLAN for the named class (call sites, token
        source, verify step, the `# andrew-asked` activation marker requirement) delivered to CTO
        as a PROPOSAL.
    P6  Every read/acquisition emits an Observation_Record (UNKNOWN on failure); `plane` carried
        opaque until the rider hash is reported.
    P7  Proof instance VALID rc=0 positional P1-P7; RAVC close to COO, cc 1.0.0_SA_CTO + 4.0.0_SA_CRO
        (spec cert).
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>P1,P2,P3,P4,P5,P6,P7</expected_criteria>
    <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_EPISTEMY.C10-PRECOND_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Normal cadence. Scratch prefix ONLY on the real plane; the only deletes are your own scratch objects, named. No live path edited, no gate implemented, no alert/monitor. Surprise channel: one line to COO.</requirement>
    <requirement id="2">CLASS CHOICE RULED BY 1.0.0_SA_CTO (63836, ~2135Z) -- the deploy code-artifact put IS the first class, decided on the FAILURE-DIRECTION argument ("a refused CODE put fails LOUD TOWARD INACTION; a refused SERVED put fails toward a STRANDED PUBLISH -- for the FIRST exercise of a novel gating mechanism you want the class whose failure mode is a halt, not a partial"); base's served-key nomination = the right SECOND class, reachable by config. The S0 class-check line in the original requirement is therefore discharged -- build against this class.</requirement>
    <requirement id="3">TWO ARCH CONDITIONS ON THE BUILD (CTO 63836, verbatim grain, BINDING): (1) RUNG 4 IS LOAD-BEARING AND MUST NOT DEGRADE -- atomicity is bound to S3's OWN conditional write (If-Match / If-None-Match); "if the implementation ever needs a lock table or a second store to make it work, STOP AND SURFACE -- that is not an implementation detail, it is the mechanism failing its own premise, and a token that is not atomically bound to the write is a comfort, not a control." (2) m4 IS THE MUTANT THAT MATTERS MOST -- "a successful put that skips the verifying re-read must FAIL the battery" is the 07-13 hung-cp-reports-success class exactly; the battery output must SHOW m4 firing (P4 is read on the printed output, never on an assertion that the battery contains it). NO ACTIVATION confirmed by CTO: the wiring plan reaches CTO as a PROPOSAL carrying the `# andrew-asked` requirement; "I will not gate a wiring act into existence."</requirement>
  </requirements>
</task_order>
