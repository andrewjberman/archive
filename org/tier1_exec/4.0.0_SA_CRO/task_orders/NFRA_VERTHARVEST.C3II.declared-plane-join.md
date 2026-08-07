<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-c3ii-declared-plane-join</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>4.0.0_SA_CRO</issued_to>
    <date>2026-08-07</date>
    <status>pending</status>
    <project_code>NFRA_VERTHARVEST</project_code>
  </metadata>

  <objective>
    Add the DECLARED PLANE to C3.ii vertical generation and ship the candidate list it makes
    computable. The macro registry is the denominator the harvest has never had: without a declared
    set there is no way to tell a NEW candidate from an ALREADY-DECLARED one, so the harvest can only
    produce an undifferentiated name pile that must be re-adjudicated by hand every run. Joining the
    declared plane to the applied plane makes the **NOT-DECLARED x APPLIED** cell computable — and
    that cell IS the product.
  </objective>

  <context>
    GROUNDING (read first, in full) — **v2, @251605d939. NOT the v1 @98c0991fb0 this TO originally
    cited**: `org/tier1_exec/1.0.0_SA_CTO/deliverables/C3II_MACRO_REGISTRY_GROUNDING_20260807.md`.
    v2 adopts your four corrections in full, including that CTO's own control could not fail.
    SPEC: `org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_VERTHARVEST_SPEC_20260807.md` (CTO~C;
    survived two CVO falsification rounds)

    >> **RULED 2026-08-07 ~1645Z — INHERIT. YOU ARE THE BUILD OWNER, NOT A SECOND AUTHOR.**
    Andrew-direct, base CTO terminal, VERBATIM: *"All your recs are approved, proceed"* — closing
    six open calls including inherit-vs-fresh. **TAKE `NFRA_VERTHARVEST_SPEC_20260807` FORWARD AS
    BUILD OWNER, ADDING THE DECLARED PLANE PER THE v2 GROUNDING. DO NOT COMMISSION OR AUTHOR A
    SECOND SPEC.** The spec already implements his stated pipeline shape byte for byte
    (`HARVEST -> NORMALIZE+CLUSTER -> CONDENSE(AI) -> RATIFY` = deterministic -> AI inferential ->
    human review) and has survived two CVO falsification rounds. Your job is to build it with the
    declared plane joined in, not to restate it.
    DECLARED PLANE: `org/projects/MACRO_CODES.md` (~30 rows) + `org/projects/REGISTRY.md` +
    `org/projects/{PROJECT_CODE}.json` for the project layer beneath each macro.

    ANDREW'S STEER: the macro project registry is an UNDEREXPLORED CHANNEL that *"should make it
    abundantly clear what the verticals are"*, and the pipeline shape he wants is
    **DETERMINISTIC -> AI INFERENTIAL -> HUMAN REVIEW**. The spec already implements exactly that
    (`HARVEST -> NORMALIZE+CLUSTER -> CONDENSE(AI) -> RATIFY`), byte for byte.

    ⚠ INHERIT-VS-FRESH IS AT ANDREW AND DOES NOT BLOCK YOU. Whether you take CTO~C's VERTHARVEST spec
    forward as build owner (CTO's recommendation) or author against the grounding fresh, **the
    grounding and this TO's deliverable are IDENTICAL under both readings.** Start now. Do not
    manufacture a hold on his pending answer — if he rules `fresh`, what changes is the starting
    artifact, not the work in this TO.

    ⚠ NAMING REMAINS SOVEREIGN. The loop SURFACES candidates; only a naming act admits one. The macro
    registry is a record of naming acts ALREADY PERFORMED — using it reads Andrew's prior decisions,
    it does not substitute for his next one. This TO auto-names nothing.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing anything:
      <run>comp-estate --definitions</run>
      <expect>C3 / C3.i / C3.ii / vertical / substrate present as reserved_ratified terms.</expect>
      <if_mismatch>Adopt the ratified terms; do not re-coin beside them (BUILD LADDER rung 2,
      granularity amendment). You authored Rule 24 — this is your own instrument pointed at your own
      vocabulary.</if_mismatch>

      <run>comp-estate --layers</run>
      <expect>Orientation on the applied plane you are about to measure per macro code.</expect>

      ⚠ `comp-find` is the on-rails primitive as of @a3a9df7911 (law + router repointed together).
      **It counts LINES, not nodes** — never quote its count as a denominator in a TO whose entire
      product is a set of denominators.

    Phase 2 — before committing:
      <run>comp-which "what consumes the C3.ii vertical candidate list"</run>
      <expect>Orientation. This TO produces an artifact + a finding; it modifies no producer.</expect>

    Phase 3 — after committing:
      Record every command, its output disposition, and the denominators printed, in the session log
      Compiler Tools table.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: `org/projects/MACRO_CODES.md`, `org/projects/REGISTRY.md` — READ ONLY in this TO
    - also_in_to: `1.0.0_SA_CTO~C` holds the VERTHARVEST spec and is WORKING (Phase-0 lifecycle
      sitting, rows 17/29). The spec is your INPUT; you are not editing it.
    - required_action: if the inherit ruling lands and you take the spec forward, MCP `1.0.0_SA_CTO~C`
      before writing to any file they own. Do not edit `MACRO_CODES.md` — see do_not.
  </cross_domain_coordination>

  <acceptance_criteria>

    >> 1. JOIN, DO NOT UNION. THIS IS THE WHOLE TO AND IT IS ALSO THE EASIEST THING TO GET WRONG. <<
       The macro registry enters as the **DECLARED PLANE**, never as an eighth harvest source.
       ⛔ FORBIDDEN SHORTCUT, NAMED: bolting `MACRO_CODES.md` on as a peer source is the cheapest way
       to make the harvest look better, **and it DESTROYS the spec's only natural control** — in the
       direction that reads as improved recall. The spec's single miss is `causality`, the vertical
       Andrew RETIRED 2026-08-05, whose applied plane is measured EMPTY. `MACRO_CODES.md` CONTAINS
       `CENG` = CausalityEngine. So a union makes the harvest "find" causality on day one, recall
       goes UP, and the instrument goes BLIND at the same moment.
       **A harvest that "finds" causality is reading the model, not the estate.**

    >> 2. THE CONTROL IS A **PAIR**, ASSERTED FROM THE SAME MEASUREMENT IN THE SAME PASS.
       ⛔ **AMENDED 2026-08-07 ~1650Z — v1 OF THIS CRITERION WAS UNDISCHARGEABLE AND YOU CAUGHT IT.**
       v1 said only *"assert `CENG` lands in DECLARED x NOT-APPLIED."* Run the Rule-22a question
       against it — *could this have said otherwise?* **No.** If the applied-plane measurement returns
       nothing at all (broken query, wrong prefix, empty credential, a harvest that silently no-ops),
       `CENG` lands in NOT-APPLIED **trivially, the assertion PASSES, and it passes MORE cleanly the
       more completely the instrument is dead.** *The control written to protect the harvest carried
       the exact defect the harvest's own control had.*

       **ASSERT BOTH LIMBS, SAME MEASUREMENT, SAME PASS:**
         (a) `CENG`/causality lands in **DECLARED x NOT-APPLIED-RETIRED** — RETIRED *specifically*,
             not the NOT-APPLIED union (see criterion 2a: the cell is split, and CENG's expected
             resting place is the retired half).
         (b) a **NAMED LIVE MACRO** — `MDPF` or `ADVI`, both live with a measurable applied plane —
             lands in **DECLARED x APPLIED**. Name it explicitly in the deliverable.
       `CENG`-empty is informative ONLY when something else is SIMULTANEOUSLY non-empty. A dead
       applied plane then fails the POSITIVE limb instead of silently satisfying the negative one.
       **Record that THE PAIR was asserted, not the single.**
       *Your own framing, carried verbatim because it is the general form:*
       **"AN ABSENCE ORACLE PASSES FOR MANY REASONS AND A POSITION ORACLE FAILS FOR ONE."**
       If either limb lands wrong, the join is reading the model — report it and STOP, rather than
       shipping a candidate list built on a broken join.

    2a. **THE NOT-APPLIED CELL IS SPLIT — RETIRED vs ASPIRATIONAL** (v2 grounding, and it is not
       cosmetic): **RETIRED** = was applied, deliberately ended by a NAMING ACT — a correct final
       resting place that stays there forever (`CENG`). **ASPIRATIONAL** = declared AHEAD of build,
       never applied — **NOT an end state, a WIP row** that should MOVE to DECLARED x APPLIED when
       built, **and if it never does, THAT IS A FINDING** (`TAXX`, `SSCN` — both TBD).
       Collapsing these two loses the finding and mis-sites the control.

    >> 3. THE NOT-APPLIED CELL CARRIES THREE STATES, NOT ONE — AND THIS IS THE KIMI COVERAGE CONTRACT
       REUSE, MADE CONCRETE. <<
       Base-CTO ruled (2026-08-07, adopting the COO #2x#4 finding) that **C3.ii REUSES the Kimi
       subdivision coverage contract rather than re-deriving one.** Here is where it bites:
       `MEASURED-EMPTY` (the applied plane ran and found nothing — `CENG`, the healthy control) and
       `NOT-MEASURED` (the applied-plane measurement FAILED or never ran for that code) are
       **BYTE-IDENTICAL in a naive 2x2**, and conflating them destroys the control a SECOND way — a
       failed measurement would land `CENG` in the right cell for the wrong reason, and the assertion
       in criterion 2 would pass while measuring nothing.
       Carry the contract's own vocabulary: **`codes_planned` (the denominator, known before any
       measurement fires), `codes_measured`, `codes_failed[]`, `codes_empty[]`** — where
       `codes_empty` is RAN-AND-FOUND-ZERO and `codes_failed` is ABSENCE OF MEASUREMENT.
       *Zero candidates is a RESULT. A failed measurement is an ABSENCE OF MEASUREMENT.*

    4. EVERY CELL PRINTS ITS DENOMINATOR AND A MEASUREMENT VINTAGE — declared N, applied M, and each
       of the four cells' counts. ⛔ A frameless cell count is the same hazard that has already moved
       two numbers in this program under their own authors TODAY (a 5.5x marker-set swing and a 3.6x
       resolver swing on NFRA_PYFIELD). Nothing in "12" says what it is 12 OF.

    5. THE RULE-24 VERDICT ON THE REGISTRY AXIS IS STATED AS A FINDING IN ITS OWN RIGHT, with the
       violation named per postulate: `POSN` (ONE portal page) vs `OPAL` (a SIX-project umbrella) vs
       `ADHC` (an explicit residual bucket, *"no permanent surface area"*, on a file that defines
       macro codes AS permanent surface areas) sit on one axis — postulate (ii) SAME GRAIN, arguably
       (i) MECE. Note also the file's own recorded conformance lag (the `OPAL` row added 2026-07-14
       closing a lag against its own rule 6).
       ⛔ **THIS IS A FINDING, NOT A PRECONDITION.** Do NOT make the harvest wait on fixing a taxonomy
       Andrew owns. Report it; ship the candidate list anyway. A residual bucket on a MECE axis
       absorbs exactly the members the axis failed to model — so anything landing in `ADHC` is, by
       construction, a vertical the taxonomy could not express, which is itself signal for the harvest.

    6. THE PRODUCT SHIPS: the **NOT-DECLARED x APPLIED** cell as a candidate list into Stage 2/3, with
       its denominator and vintage. Everything else in the 2x2 is bookkeeping that makes it legible.

    7. Session log with a Compiler Tools section and an archetype tag.

  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier1_exec/4.0.0_SA_CRO/deliverables/[the 2x2 + candidate list + Rule-24 finding]</file>
      <file action="reference">org/projects/MACRO_CODES.md</file>
      <file action="reference">org/projects/REGISTRY.md</file>
      <file action="reference">org/tier1_exec/1.0.0_SA_CTO/deliverables/C3II_MACRO_REGISTRY_GROUNDING_20260807.md</file>
      <file action="reference">org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_VERTHARVEST_SPEC_20260807.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Parse the declared plane to `{code, surface_area, owner, pod, pipeline}`, plus
    the project layer beneath each macro.</requirement>
    <requirement id="2">MEASURE the applied plane per macro code. CTO's grounding is explicit that this
    is UNEXERCISED — they did not run the harvest, did not parse MACRO_CODES.md programmatically, and
    did not measure the applied plane. **The 2x2's cell sizes are unmeasured BY CONSTRUCTION;
    measuring them is the work.** Every count in their §5 is a file read, not a measurement.</requirement>
    <requirement id="3">Produce the 2x2, assert the control, ship the bottom-left cell.</requirement>
    <requirement id="4">State the Rule-24 verdict per postulate.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">The 2x2 with per-cell denominators + vintage, the candidate list, and
    the Rule-24 finding.</deliverable>
    <deliverable type="commit">The parser/join code, re-derivable, with its self-test.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT union the macro registry into the harvest sources. Join only. See criterion 1.</rule>
    <rule>DO NOT auto-name, propose-as-ratified, or admit any vertical. Naming is sovereign; the loop
    surfaces candidates only.</rule>
    <rule>DO NOT EDIT `org/projects/MACRO_CODES.md` to fix the Rule-24 grain defect. Report it. The
    axis is Andrew's and the fix is a separate act — and a taxonomy edit made mid-harvest would change
    the declared plane under your own measurement.</rule>
    <rule>DO NOT make the harvest wait on the taxonomy finding, the inherit-vs-fresh ruling, or any
    other seat's answer. Nothing here is gated on anyone.</rule>
    <rule>DO NOT report a cell count without its denominator and vintage.</rule>
    <rule>DO NOT treat `MACRO_CODES.md` as ground truth — it is AUTHORITATIVE-BUT-LAGGING, which is
    precisely why it joins to the applied plane rather than replacing it.</rule>
    <rule>DO NOT re-derive a coverage vocabulary. Reuse the Kimi contract's (criterion 3) — that reuse
    is a landed architecture ruling, not a preference.</rule>
    <rule>DO NOT call any external vendor API. DO NOT build any alert, alarm, SNS topic, SES send,
    freshness checker or monitor.</rule>
  </do_not>
</task_order>
