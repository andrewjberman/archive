<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-07-canplat-v1</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>3.0.0_SA_CVO~Z</issued_to>
    <date>2026-08-07</date>
    <status>complete</status>
    <project_code>MDPF_CANPLAT</project_code>
    <governing>VALIDATION PRD docs/architecture/MDPF_CANONICAL_PLATINUM_VALIDATION_PRD.md @2dedd8f6a (V-rubric rows V1–V8) · PRD §0 binds · V-series MEASURES ONLY</governing>
    <sequence>⛔ V-2 FIRST (Andrew-direct "an ad hoc run issued now"), THEN V-1. V9–V12 are NOT in this TO — portal/src is empty at site Z; blocker routed to MSTR~Z by COO, never absorbed by a seat.</sequence>
  </metadata>

  <standing_instruction>
    ⛔ PRD §0 BINDS, VERBATIM FORCE (full text in your G2 TO @f123fbf6e): BUILD/VALIDATE WHAT IS
    DESCRIBED, DO NOT HUNT ERRORS. **V-series MEASURES ONLY — a defect found is a SURPRISE-CHANNEL line
    to 2.0.0_SA_COO~Z, never a fix.** Specifically ruled in advance: the frozen-gold republish behaviour
    you will likely see in V-2 is EXPECTED, already ruled, NOT a finding — record it, do not correct it.
    Andrew-direct verbatim (V-PRD header): "we also need an ad hoc run issued now and make sure that it
    displays properly on the portal."
  </standing_instruction>

  <objective>
    Execute V-2 then V-1 of the Validation PRD: fire an ad-hoc run of the CURRENT chain, read the served
    bodies, confirm the portal renders all four scopes, capture the R7 pinned baseline from the post-run
    state (rows V6/V7/V8) — then validate the four live trigger entries and the one dead edge against
    the resources they touch, recording the negative results with denominators (rows V1–V5).
  </objective>

  <phase_1_v2>
    Quoting V-PRD §2 V-2 (rows V6/V7/V8):
    1. **Fire an ad-hoc run of the CURRENT chain.** There is no event chaining between hops (§1a —
       measured), so the chain is exercised by invoking each hop in its production order with real waits:
       `mdpf-daily-trigger` → (compute completes) → `mdpf-accrual-trigger` → (promotion completes) →
       the publisher. Operational invokes are sanctioned QA (CLAUDE.md ad-hoc rule). **FALLBACK, named
       in advance: if an invoke is IAM-DENIED at your seat, STOP and report the denial to COO~Z — do
       NOT work around it; V-2 then rides AE~Z's morning after their clocked block.** A denied call
       looks exactly like a call nobody made — record rc + error verbatim.
    2. **V6:** read the served BODIES of all 12 (+2 extras) — never LastModified/ETag (the publisher
       injects a fresh process timestamp; both move on frozen data). Record which artifacts advanced
       and which did not, WITH their data-as-of. Frozen = expected, not a finding.
    3. **V7:** confirm the portal DISPLAYS correctly — the actual rendered surface, all four scopes
       (playwright headless render of the deployed PROD surface; a screenshot read, not a fetch).
    4. **V8:** capture the post-run state as **THE R7 PINNED BASELINE**: explicit VersionIds at a
       stamped instant, as a NEW baseline manifest per your re-pin protocol (supersedes the 00:07:53Z
       pin as the R7 before-image; derivation history carries both). **This run IS the fixture the
       whole regression test compares against.**
  </phase_1_v2>

  <phase_2_v1>
    Quoting V-PRD §2 V-1 (rows V1–V5), read-only against the live plane:
    1. **V1:** each of the 4 entries: state, expression, timezone, **target ARN resolves to a function
       that EXISTS** (resolve it, never assume it).
    2. **V2:** per-target resource policies permit invocation from the right principal
       (`scheduler.amazonaws.com` vs `events.amazonaws.com`) AND source ARN.
    3. **V3:** floor DLQ policy names the CURRENT schedule ARN + principal; queue depth read. The known
       mis-scope (old classic-rule principal) is RECORDED, corrected at cutover, NOT chased now.
    4. **V4:** `mdpf-daily-refresh-trigger` confirmed accelerator-only, nothing depends on it (last
       fired 2026-07-30 — a dead event edge is not a defect under schedule-first; its re-point rides
       the cutover).
    5. **V5:** the NEGATIVE recorded explicitly with denominators: 0 event-invoke destinations of 4
       functions; 0 of 10 S3 notifications on gold/portal-gold/platinum. An unrecorded negative is
       re-derived by the next person.
  </phase_2_v1>

  <compiler_tools_mandate>
    comp-trigger / comp-aws for the scheduler+rule reads where they route (comp-which first); raw aws
    for OPERATIONAL invokes + policy reads is legal (operational, not inspection-gated). Every list
    call: auto-paginate, never --no-paginate, denominator printed beside any absence verdict.
  </compiler_tools_mandate>

  <do_not>
    <rule>NO fixes, no schedule changes, no policy edits, no DLQ drains. MEASURE ONLY.</rule>
    <rule>NO served-key moves/deletes. The ad-hoc run publishes through the production publisher — that
    is the sanctioned exercise; you write nothing directly.</rule>
    <rule>Do NOT correct the frozen-gold behaviour. Do NOT read mtime/ETag as freshness.</rule>
    <rule>The ad-hoc run is QA, NEVER production evidence — it cannot close any R-row.</rule>
    <rule>NO error-hunting (§0). SURPRISE: line to COO~Z, then continue. Lane commits only; push is
    MSTR~Z's; scratchpad for working files.</rule>
  </do_not>

  <deliverables>
    <deliverable type="document">V6 body-read record (advanced vs frozen, per-key data-as-of) + V7 rendered-surface evidence (all four scopes) + V8 new baseline manifest (VersionIds + stamped instant)</deliverable>
    <deliverable type="document">V1–V5 validation record with denominators + the explicit negatives</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>
</task_order>
