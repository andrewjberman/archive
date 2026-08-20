<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-r14-t1-derivation-fix</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-08-20</date>
    <status>staged -- activates at seat spawn + COO GO (lane dark at issuance; spawn routed to MSTR 1548Z)</status>
    <project_code>D2_ADVI_49F (directive row org/missions/DIRECTIVES.yaml:53; PRD docs/architecture/D2_ADVI_49F_E2E_PRD.md; LAPTOP-placed by Andrew's word)</project_code>
  </metadata>

  <objective>
    P1, deadline-bearing: fix the 49F chain's PRODUCTION date derivation so it targets the
    T-1 read frontier its own doc promises, per the RULED fix shape (CTO 63213). The fix must
    LAND + DEPLOY before 2026-08-21 12:45Z -- that fire is the re-dated FIRST green gating
    D2's sovereign FRI target (SECOND green -> repoint -> PROD promote). Every trading-day
    production run fails identically until this lands.
  </objective>

  <context>
    MECHANISM (CVO 63207, source-confirmed at HEAD 2d7ff49e58; independently verified CTO
    63213): chain_49f_entrypoint.py:230 (production branch) sets
    date = expected_last_trading_day(now), which returns T-0 on any trading day
    (lib/trading_calendar.py:101-105); the entrypoint's own doc block (:61-63) promises T-1
    per CLAUDE.md NEVER#1 -- and NAMES expected_last_trading_day as if it were the T-1
    derivation while prev_trading_day sits ten lines above it. Silver is HEALTHY at its
    correct T-1 frontier (fact_acc date=2026-08-19 written 08-20 05:46 ET) -- the requested
    T-0 partition structurally cannot exist until tomorrow. Today's 12:45Z abort: rc=1 at
    stage a00, 1.7s, nothing after ran; 15 twins not emitted; canonical 08-19 absent.

    THE FIX SHAPE IS RULED -- not yours to re-design (CTO 63213, verbatim-scope):
    (1) CALL-SITE ONLY: production branch derives date = prev_trading_day(now). Do NOT
        change expected_last_trading_day -- its semantics are correct for its name and its
        freshness consumers (comp-freshness trading_days_behind); changing the FUNCTION
        would silently shift every freshness verdict on the estate.
    (2) REFUSAL STAYS LOUD: a genuinely-missing T-1 partition still ABORTS the chain. No
        newest-existing-with-fallback -- that is the fix plus a way to hide a real outage.
    (3) DOC BLOCK corrected in the SAME commit to name prev_trading_day; battery gains
        both-directions controls. Pattern reference: c02:157's 2026-08-19 same-NEVER#1-family fix.
    CTO's P2 rider: the fix commit carries one line on the doc-vs-code seam ("a comment that
    performs compliance") per their acceptance.

    CALENDAR (COO re-date record, this commit's sibling:
    org/tier1_exec/2.0.0_SA_COO/deliverables/R14_REDATE_20260820_T0_DERIVATION_SLIP.md):
    FIRST green 2026-08-21 12:45Z -> YOUR READ of the run log by 13:15Z confirms it (named
    reader, adopted form); PB-1 13:30Z rides that day; FRI 08-22 SECOND green -> flip ->
    PROD promote UNCHANGED. Miss Thursday's fire and everything slides
    trading-day-for-trading-day (flip -> MON 08-24).
  </context>

  <compiler_tools_mandate>
    Phase 1 -- before writing:
      <run>comp-find "expected_last_trading_day" (the REQUIRED caller-audit leg)</run>
      <expect>Every call site enumerated with denominator; each confirmed as wanting EXPECTED-FRONTIER semantics (freshness checks) -- any caller wanting T-1 read-frontier semantics is a second instance of this same defect: surface it, fix only per this TO's scope</expect>
      <if_mismatch>A second read-frontier caller = surprise-channel line to COO; do not widen the fix in-lane.</if_mismatch>

      <run>comp-pipescript io chain_49f_entrypoint --pipeline bd</run>
      <expect>Orientation on the chain's IO surface before the edit (Rule 13 DS minimum); flag anything unexpected</expect>
      <if_mismatch>Unexpected consumers = flag to COO before editing.</if_mismatch>

    Phase 2 -- before committing:
      <run>The both-directions battery (ruled leg 3): trading-day morning -> D=T-1; Monday -> prior Friday; day-after-holiday -> pre-holiday day; plus the refusal control (T-1 partition absent -> loud ABORT, not fallback)</run>
      <expect>All green + the refusal control fires -- a control that cannot fail is not a control</expect>
      <if_mismatch>Do not commit; the derivation is still wrong in one direction.</if_mismatch>

    Phase 3 -- after committing:
      <run>Deploy per Rule 13 (safe-deploy DS lane incl. aws s3 cp); then comp-pipescript deployed chain_49f_entrypoint</run>
      <expect>MATCH -- deployed bytes carry the fix BEFORE the 08-21 12:45Z fire (Rule 22a: an undeployed fix passes every repo check and changes nothing)</expect>
      <if_mismatch>A STALE/MISSING read = the fix is not live; resolve before end of session, never leave for the fire to discover.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: lib/trading_calendar.py
      required_action: READ-ONLY under this TO (ruled). The caller-audit output rides your
      fix commit; any function-semantics question routes to CTO, never changed in-lane.
  </cross_domain_coordination>

  <acceptance_criteria>
    T1  Call-site fix landed: chain_49f_entrypoint.py production branch derives
        prev_trading_day(now); doc block names the same primitive; diff quoted.
    T2  Caller-audit of expected_last_trading_day: all call sites enumerated (denominator
        printed), each classified expected-frontier-correct or surfaced.
    T3  Both-directions battery + refusal control green (outputs quoted; the refusal control
        EXERCISED, not asserted).
    T4  Deployed-bytes MATCH before 2026-08-21 12:45Z (comp-pipescript deployed output quoted
        with timestamp).
    T5  2026-08-21 12:45Z FIRST green confirmed BY YOUR READ of the run log by 13:15Z --
        the named-reader row; an ABORT found = same-hour surface to COO.
    T6  Proof instance VALID rc=0 positional: T1,T2,T3,T4,T5,T6.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>T1,T2,T3,T4,T5,T6</expected_criteria>
    <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D2_ADVI_49F.R14-T1FIX_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <scope>
    <files>
      <file action="modify">data/... chain_49f_entrypoint.py (production-branch date derivation + doc block; resolve exact path via comp-pipescript)</file>
      <file action="reference">lib/trading_calendar.py (READ-ONLY; caller-audit subject)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Surprise channel: one line to 2.0.0_SA_COO, no action, keep working. A second read-frontier caller of expected_last_trading_day is the expected surprise shape.</requirement>
    <requirement id="2">Deliverables: proof instance rc=0 + session log with Compiler Tools table + RAVC close to COO (cc CVO -- their pins/oracle table gates on T5, and CTO -- fix-shape owner).</requirement>
  </requirements>
</task_order>
