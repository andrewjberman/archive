<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-epistemy-c3-identity</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp</issued_to>
    <date>2026-08-20</date>
    <status>pending -- STARTS NOW (wave 2 of NFRA_EPISTEMY; envelope landed @45a2892ed2 + base S3 cert issued; your board read clear on the live roster 2110Z; CRO base 63752: "3 is deployed-bytes/identity chain = 0.8.0-class"). SHAPE CERTIFIED ~2148Z (base spec cert A1 + CTO arch gate 63866 CLEARS on the amended shape): the single TERMINAL-CLASS axis this TO's Phase-1 prompt named (PRESENCE_ONLY / BEHAVIOR / UNMEASURED / UNKNOWN) was found FUSED -- its precedence rule was the tell (CTO: "if an enum needs a precedence rule to resolve cases where more than one value applies, suspect two axes fused") -- and is SPLIT into REACH at MEMBER grain {NONE, PRESENCE_ONLY, BEHAVIOR} with closure reach = MIN over members (the aggregation layer DECLARED on the record) and STANDING at CLOSURE grain {CURRENT, INVALIDATED, AMBIGUOUS, BROKEN}; no ordering language survives. ACCEPTANCE READS AGAINST THE CERTIFIED SHAPE: I3's "PRESENCE_ONLY / BEHAVIOR" = the reach axis (closure reach is the MIN -- one executing member never licenses BEHAVIOR over unexecuted members); I4's "UNMEASURED/AMBIGUOUS" = standing AMBIGUOUS; I5's "UNMEASURED on re-read" = standing INVALIDATED; DIVERGENT stays OFF both axes (a bundle verdict); resolved_via BUILD_INPUT:<field> REQUIRED (a no-basis hop REFUSED, m2). Census note (CTO): pin the token-census surface list to the named canonical set incl. SYSTEM_DEFINITIONS -- an omitted surface returns a clean zero indistinguishable from a real absence.</status>
    <project_code>NFRA_EPISTEMY</project_code>
  </metadata>

  <objective>
    Build COMPONENT 3 -- THE IDENTITY + SUPPORT-CLOSURE COMPILER -- "makes 'what changed / what
    supports this' answerable at the right grain" (PRD sec.1 row 3). The estate's own measured
    instance of the gap is the Lambda source map: it pairs a Lambda with its REPO DIR at NAME
    grain and compares no bytes (CLAUDE.md Deployment Rule 4, corrected 2026-08-12 after a live
    Lambda was found running bytes older than its own tree while every check passed). This
    component compiles, for any claim or artifact, the typed chain of hops that supports it --
    and terminates HONESTLY where the evidence stops.
  </objective>

  <context>
    SPEC OF RECORD, three sources (CRO base 63752 names all three as the certification basis):
    (1) PRD sec.2.1 support_pointers + sec.2.5 (Eligibility_Evaluation consumes the support
    closure; "a new member is never covered by an old enumerated waiver"); (2) Response II sec.2.5
    (org/tier1_exec/4.0.0_SA_CRO/deliverables/RESPONSE_II_MUTATION_BUNDLE_AND_ADOPTIONS_20260820.md:147-156)
    -- the LOGICAL-FACT vs SUBSTRATE-REALIZATION split, the full evidence chain, the AMBIGUITY
    CHECK ("no second plausible home" -- our two-homes defect, internalized), and EXPIRY SEMANTICS:
    when one side changes, the equivalence claim becomes UNMEASURED rather than silently true or
    automatically false; "the chain's most dangerous hop is the last one (deployed -> EXECUTING)
    ... any identity bundle that terminates at 'deployed artifact digest' has verified PRESENCE,
    not BEHAVIOR"; (3) CLAUDE.md Rule 22a build-input resolution: deployed bytes are diffed against
    THE SOURCE THE ARTIFACT IS BUILT FROM, resolved through the BUILD INPUT (source-map entry /
    package manifest), NEVER by filename; on EC2 a staged object may be INERT (first-boot-only
    pull) -- staged = DESIRED, executing = APPLIED; an expected log's absence is evidence too.

    WHAT THE COMPILER IS: given a logical fact ("Lambda F runs code C@v", "served key K is produced
    by script S") it emits the SUPPORT CLOSURE -- the ordered set of hops {logical fact ->
    substrate realization -> identity evidence -> vintage}, each hop typed by evidence class and
    by the instrument that produced it, plus the closure's TERMINAL CLASS: PRESENCE_ONLY (stops at
    a deployed digest / staged object), BEHAVIOR (reaches an executing read -- on-instance/runtime
    read, runner exit-log, an exercised path), or UNMEASURED (a side changed since, or the
    ambiguity check found a second plausible home). The lambda source map is a BUILD INPUT it
    READS; it never becomes a bytes comparator and this TO does not rewrite it.

    CONSUMES C1: every acquisition the compiler performs (a head-object, a get-function, a package
    download, a git show) emits an Observation_Record; a failed acquisition is UNKNOWN and the
    closure's terminal reflects it -- never a clean "no drift". BIND-TIME CONDITION, CTO 63744
    verbatim, pinned: "no consumer may parse, branch on, or key off `plane` until the ratified
    plane enum + separate substrate field land" -- ~A's rider commit carries the split; until its
    hash is reported, carry the field opaque. S6 absence-semantics model: every nullable field in
    your objects names what its absence disqualifies.

    RIDERS (every NFRA_EPISTEMY TO, verbatim): (a) sec.2.9 is NOT buildable spec -- the harm
    surfaces are OPEN requirements (sec.4b); do not build against them. (b) CITE-NOT-COPY on shared
    objects; ANY new or changed schema object (Support_Closure / Identity_Bundle are NEW objects)
    routes through 4.0.0_SA_CRO base as registry executor with its Rule-24 record + token census
    -- NEVER landed in-lane; base's S3-style spec cert precedes 1.0.0_SA_CTO's arch gate. (c)
    interim status shapes resolve into the envelope. FIRST ACT = S0 ground-read of the source map
    (denominator: entries; how many resolve to a package manifest; how many Lambdas appear in >1
    repo home -- print the counts).
  </context>

  <compiler_tools_mandate>
    Phase 1: S0 (above) + comp-pipescript deployed (the existing MATCH/STALE/MISSING sweep is a
    precursor at filename grain -- name exactly what it does and does not resolve) + the Rule-24
    pre-record for the closure's TERMINAL-CLASS axis (MECE over the declared layer: PRESENCE_ONLY /
    BEHAVIOR / UNMEASURED / UNKNOWN -- hunt the uncovered member before committing).
    Phase 2: mutant battery BEFORE commit: (m1) two repo homes for one logical producer -> the
    closure reads UNMEASURED/AMBIGUOUS, never CLEAN and never DRIFT; (m2) a filename-resolved hop
    smuggled in -> the build-input check fires; (m3) one side's hash changed after the closure was
    compiled -> UNMEASURED on re-read; (m4) a closure terminating at deployed digest labelled
    BEHAVIOR -> REFUSED; (m5) a failed acquisition -> UNKNOWN terminal, no zero; determinism.
    Phase 3: live closures for >= 3 real Lambdas resolved through the source map + package
    manifest, INCLUDING the measured 2026-08-12 two-copies specimen (see 22a's record) -> must read
    UNMEASURED/AMBIGUOUS; one EC2 case (staged-vs-executing) -> PRESENCE_ONLY unless an on-instance
    read is taken (state which; an SSM read is an operational act -- do it only if it is zero-risk
    read-only, else fixture it and SAY fixture).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: Observation_Record (PRD sec.2.1) -- consumed, never edited here; the
      envelope's author 4.0.0_SA_CRO~A owns its riders.
    - shared_resource: NEW objects Support_Closure / Identity_Bundle -> 4.0.0_SA_CRO base registry
      -executes (S2 program), 1.0.0_SA_CTO arch-gates; CTO also holds the deployed-vs-built-from
      census + the apply-time assertion gate candidate (Rule 22a) -- your compiler is the
      INSTRUMENT that census would run on; do not arm the gate (proposal only).
    - consumer: component 4 (lease service -- invalidation against REAL support identities, not
      names) will lease closure members; component 2 (4.0.0_SA_CRO~A) mints the certificates your
      hops may reference. Stage nothing for either; make your objects leasable (vintage +
      invalidation predicates).
    - source map: infra/aws/lambda/ci/lambda-source-map.json -- READ as build input; any proposed
      change to its shape is a CTO matter, not this TO.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is COMPONENT 3 as cut -- I1 objects, I2 live closures,
    I3 last-hop honesty, I4 ambiguity, I5 expiry, I6 envelope join + battery, I7 proof;
    exhaustive over the component; components 2/4 OUTSIDE.)
    I1  Support_Closure + Identity_Bundle objects schema-native, citing PRD sec.2.1/2.5 + Response II
        sec.2.5 + Rule 22a as sources of record; Rule-24 record + token census through base; CTO
        gate; every nullable carries its S6 absence semantic.
    I2  LIVE CLOSURES for >= 3 real Lambdas, each hop resolved through the BUILD INPUT (source-map
        entry -> package manifest -> deployed package bytes), denominators printed.
    I3  LAST-HOP HONESTY: a closure ending at a deployed digest or a staged S3 object reads
        PRESENCE_ONLY; only an executing read (runtime/on-instance/exercised path) reads BEHAVIOR;
        the EC2 staged-vs-executing case handled and labelled (live or fixture, stated).
    I4  AMBIGUITY CHECK: the two-copies specimen reads UNMEASURED/AMBIGUOUS -- never "drift",
        never "clean"; m1/m2 fire.
    I5  EXPIRY: one side changes -> UNMEASURED on re-read (m3); closures carry vintage +
        invalidation predicates (leasable by component 4).
    I6  Every acquisition emits an Observation_Record (UNKNOWN on failure, m5); `plane` carried
        opaque until the rider hash is reported, then consumed as the ratified enum; battery m1-m5
        FIRE; determinism stable.
    I7  Proof instance VALID rc=0 positional I1-I7; RAVC close to COO, cc 1.0.0_SA_CTO + 4.0.0_SA_CRO
        (spec cert).
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>I1,I2,I3,I4,I5,I6,I7</expected_criteria>
    <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_EPISTEMY.C3-IDENTITY_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Bounds: read-only against live AWS (head-object / get-function / package download -- no deploys, no update-function-code, no TF); no source-map rewrite; nothing armed (no alert, monitor, or gate -- candidates proposed only); comp-iam floor before any new boto3 call. Normal cadence; surprise channel: one line to COO. Your C4-LEASE TO is STAGED behind this one (same dir) and activates on this close.</requirement>
  </requirements>
</task_order>
