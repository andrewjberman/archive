<task_order>
  <metadata>
    <id>C3L.3</id>
    <slug>kimi-loop-integration</slug>
    <issued_by>1.0.0_SA_CTO (pending -- CTO issues the C3L series; drafted by 0.7.0_AE_CloudOps~B on Andrew-direct "Is the TO ready? if so proceed it now")</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-31</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "C3L" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>
      TWO gates, and BOTH are open as drafted.
      (1) CTO ISSUES. CTO ruled 181021Z "I issue them, not you" on the C3L series. This file is a DRAFT
          authored by the assignee; it is not self-issued and must not be read as such.
      (2) C3L.1 MUST LAND FIRST FOR STEPS 3-4. C3L.1 defines the walk-record schema, the
          `walk:&lt;record-id&gt;#&lt;item-id&gt;` pointer, the typed basis and the typed outcome. The RETURN half of
          this TO writes those fields and CANNOT be built against a schema that does not exist.
      >> STEPS 1-2 (the SURFACING half) ARE STARTABLE WITHOUT C3L.1 -- selection and presentation do not
         touch the record schema. STEPS 3-5 ARE NOT. Split the dispatch or issue C3L.1 alongside. <<
      Andrew's HARD PAUSE (relayed 175627Z) holds all new starts; his "proceed it now" is read as
      authorising THIS integration, NOT as a general lift -- SURFACED, NOT ASSUMED (see open_questions Q1).
    </dispatch_unblock_condition>
    <project_code>NFRA_VELOCITY (ESTATE half, WS-E8 -- C3 labeling layer)</project_code>
    <priority>
      P1 within the C3 labeling layer. This is the TO that makes the layer RIDE IN THE KIMI LOOP rather
      than be an ad-hoc campaign. Andrew fence (5), verbatim: "we need to build the system with 0.7.0~B
      into the Kimi loop not be doing anything ad hoc." Without it the walk has no trigger, and a process
      whose only trigger is a human remembering has no trigger.
    </priority>
    <sla>Steps 1-2: ~0.5d. Steps 3-5: gated on C3L.1; ~1d after it lands.</sla>
  </metadata>

  <references>
    <spec>org/tier2_senior/0.7.0_AE_CloudOps~B/C3_LABELING_LAYER_SPEC_20260731.md (v0.5) -- s.7 is the seam this TO builds; s.2.0 the two-axis frame; s.6 the legibility requirements; s.10 R1-R6.</spec>
    <origin>Andrew-direct via CTO 163330Z (author the spec) + Andrew-direct 2026-07-31 ~2050Z ("Is the TO ready? if so proceed it now"). Spec reviewed 3x by 3.0.0_SA_CVO; arch-gated by 1.0.0_SA_CTO 181021Z.</origin>
    <store>org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml -- contract_record.required = [intent_source, obligation, lifecycle_class, revalidate_by, locality]. THE REGISTRY IS THE STORE. This TO adds no store and no field.</store>
    <layer1>The estate-report / Kimi Review cycle (built, live, schedule DISABLED). infra/aws/terraform/estate-report/.</layer1>
  </references>

  <context>
    Shed is a TWO-AXIS decision -- INTENT ("is this still wanted?") and FRICTION ("what does removal
    cost?"). ONLY FRICTION WAS EVER INSTRUMENTED. All 14 landed WS-E1 declarations read
    lifecycle_class: UNDECLARED because the rule bank demands PRODUCER-ASSERTED and no mechanism ever
    ASKED a producer. WS-E3.0 closed at 0 retirements / 6-of-6 KEEP-DORMANT (@2da40ba711) -- the correct
    output of a correctly-built instrument measuring the wrong number of dimensions.

    The C3 walk is the missing INTENT sensor. THIS TO IS ITS TRIGGER. Layer 1 (the Kimi high-level
    signal) reports what MOVED and PROPOSES where prose has drifted; Layer 2 (the walk) ASSERTS.
    >> LAYER 1 NEVER LABELS. Selection is not assertion, and a surfacing mechanism that starts
       suggesting lifecycle values has become an observer-inference engine -- the one thing the rule
       bank forbids ("transience cannot be derived; it must be DECLARED"). <<
  </context>

  <scope>
    <step>1. SURFACING CONTRACT. Define how the daily cycle selects which C3 items reach the walk agenda.
      AGENDA UNIT IS THE C3.ii VERTICAL (R2). Selection inputs are permitted to include: an expired
      revalidate_by (R4 -- the maintenance loop's own re-entry), an UNDECLARED lifecycle_class, and
      Layer-1 movement signal. SELECTION MUST NOT INFER OR SUGGEST A VALUE -- it orders an agenda, it
      does not pre-fill an answer. Record WHY each item surfaced, so a walk participant can see whether
      they are being shown a maintenance re-entry or a never-declared subject; those warrant different
      conversations.</step>

    <step>2. AGENDA PRESENTATION. Render the agenda for a CTO+Andrew walk. MUST carry, per item: the
      C3.ii vertical, its constituent contract_records (1:N -- R2), current lifecycle_class + basis +
      vintage, and whether a prior assertion is STALE (R4: persists, marked stale, re-enters).
      >> AND THE 1:N COROLLARY IS A DELIVERABLE, NOT A DETAIL: a vertical whose members' assertions
         DISAGREE is itself a finding -- a vertical that is not one system, i.e. a mis-drawn naming act.
         The presentation MUST make that visible rather than averaging it away. <<
      SOURCE-FIRST (C3L.6 step 1) RUNS BEFORE ESCALATION, NOT BEFORE SURFACING -- do not build a
      source-read into the agenda builder; it belongs on the doubt path where a human has already
      looked. Building it here would spend it on every item instead of the doubted ones.</step>

    <step>3. [GATED ON C3L.1] RETURN PATH. How a walk outcome becomes a contract_record write:
      lifecycle_class + intent_source (walk:&lt;record-id&gt;#&lt;item-id&gt;) + revalidate_by, into the WS-E1
      registry. NO PARALLEL STORE -- CTO binding. The walk is the WRITER; the registry is the STORE.</step>

    <step>4. [GATED ON C3L.1] LEGIBILITY AT THE QUOTE SITE (s.6 requirement 4). A lifecycle_class
      renders as `PERMANENT [walk:2026-07-31, agreed-on-sight]` wherever it is consumed.
      >> A BARE `PERMANENT` IS A MISQUOTE, NOT A SUMMARY. << The basis travels with the label ACROSS the
      artifact boundary -- the failure this prevents happens at the quote site, in a different artifact,
      not in the record. Typed basis {WALKED_NO_DOUBT | INVESTIGATED_AND_CONFIRMED | UNEXAMINED} with
      UNEXAMINED AS THE DEFAULT, so silence renders as unexamined rather than as assent.</step>

    <step>5. VERIFY BY EXERCISE, NOT BY CONFIG READ. A synthetic agenda cycle end-to-end: an item with an
      expired revalidate_by RE-ENTERS; an UNDECLARED item SURFACES; a vertical with disagreeing members
      RENDERS THE DISAGREEMENT; a walk outcome LANDS in the registry and reads back with its basis
      attached. NEGATIVE CONTROL REQUIRED: an item that should NOT surface does not. A surfacing
      mechanism that surfaces everything is indistinguishable from one that works, and would pass every
      positive test.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Surfacing contract defined and EXERCISED: expired-revalidate_by re-entry, UNDECLARED, and Layer-1 movement each demonstrably surface an item; the recorded reason distinguishes them. NEGATIVE CONTROL: a current, declared, unmoved item does NOT surface.</ac>
    <ac id="AC2">Selection provably does not pre-fill or suggest a lifecycle value -- demonstrated by inspection of the agenda payload, not asserted. Layer 1 never labels.</ac>
    <ac id="AC3">Agenda renders the 1:N vertical-to-contract_record mapping, and a vertical whose members DISAGREE renders as a visible finding rather than being averaged or hidden.</ac>
    <ac id="AC4">[C3L.1-gated] A walk outcome writes lifecycle_class + intent_source + revalidate_by into the WS-E1 registry. Verified by reading the record back. NO second store exists anywhere in the path -- stated as a checked property, not an intention.</ac>
    <ac id="AC5">[C3L.1-gated] Every consumer-facing render of a lifecycle_class carries its basis; a bare value cannot be produced by the render path. UNEXAMINED is the default.</ac>
    <ac id="AC6">Rides IN the Kimi cycle -- no ad-hoc trigger, no human-remembering dependency (Andrew fence 5). NO new alert, SNS topic, alarm, monitor or freshness checker (standing 2026-07-28 moratorium): the walk agenda is a work product, not a notification.</ac>
    <ac id="AC7">Session log with a Compiler Tools section. No emoji / non-ASCII. RAVC2 to 1.0.0_SA_CTO, CC 3.0.0_SA_CVO.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>comp-which for the routing question; comp-blast on the estate-report/Kimi cycle surface before touching its trigger path -- this TO adds a consumer to a live pipeline.</before_write>
    <before_commit>.tools/commit-gate.sh on every .py; comp-surface-check by hand (the walk writes a governance record).</before_commit>
    <after_commit>comp-pipescript deployed if any runner-side artifact changes; RAVC2 with the exercise transcripts, not a config read.</after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    WS-E1 registry (the STORE -- shared write surface; the walk is a new writer). WS-E3 / WS-E2 / WS-E5
    are DOWNSTREAM CONSUMERS of lifecycle_class and their derivation contracts are C3L.5, not this TO --
    but a change to the record shape here reaches all three. C3L.6 owns the doubt path (source-first);
    this TO must not implement it. The C7-vs-contract_record seam (WS-E5 + MSTR~Z, independently) is
    NOT spanned here -- bridging it from this side is the parallel-store hazard under another name.
  </cross_domain_coordination>

  <open_questions>
    <q id="Q1">SCOPE OF ANDREW'S "proceed it now": read as authorising THIS integration, not as a general
      lift of the hard pause. SURFACED, NOT ASSUMED -- if he meant wider, that is his word to give.</q>
    <q id="Q2">The 29-vs-43 walk DENOMINATOR is AT ANDREW and pending. This TO consumes the population as
      an INPUT and fixes no count. Do not resolve it here.</q>
    <q id="Q3">Cadence: does the walk agenda accrue DAILY with the cycle, or accumulate for a periodic
      sitting? Andrew's "maintained" argues for continuous accrual; two-scarce-humans argues for
      batching. CTO/Andrew's call, not the assignee's.</q>
  </open_questions>
</task_order>
