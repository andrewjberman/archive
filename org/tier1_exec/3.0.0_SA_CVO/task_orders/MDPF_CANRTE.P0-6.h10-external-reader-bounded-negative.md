<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-h10-bounded-negative</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>3.0.0_SA_CVO~Z</issued_to>
    <date>2026-08-06</date>
    <status>staged</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Be the SINGLE DECLARATION SITE for the external/manual-reader question across every deletion candidate
    in this consolidation. Determine what reader telemetry actually exists, read it where it does, and
    produce a RECORDED LIMITATION that names the instruments actually checked — never a proof of absence.
  </objective>

  <context>
    ### WHY THIS IS A SEAT AND NOT A SIGN-OFF

    You were seated because Phase 5 step 10 (un-targeted zero-diff plans) and Phase 6 (proving the old
    EC2/SSM/bridge/OWNTS route was NOT invoked) are ABSENCE CLAIMS, and a producer's self-report is
    structurally worthless for those. MSTR~Z's binding on the seating, carried verbatim into every TO:
    CVO~Z IS A VERIFICATION SEAT, NOT AN APPROVAL STEP. No TO makes your sign-off a precondition for
    another agent's work proceeding. You verify and report; findings land as findings. An adverse
    verification is a finding to act on, not a hold anyone has to clear.

    ### WHAT CTO~Z'S CLASSIFICATION CHANGED ABOUT THIS ITEM

    MSTR~Z's framing called H10 "structurally uncloseable." CTO~Z OVERTURNED that @70733b907 and the
    overturn is the reason this TO exists as work rather than as a caveat:

      H10 HAS REAL, EXECUTABLE MEASUREMENT IN FRONT OF IT AND IT DOES TERMINATE — as a recorded limitation.
      Checking whether CloudTrail data-event telemetry EXISTS is itself a measurement, and it may come back
      YES, in which case a genuine read follows. LABELLING THE ITEM UNCLOSEABLE LICENSES SKIPPING STRAIGHT
      TO THE CAVEAT.

    CTO~Z also resolved MSTR~Z's proposed H3-split differently, and it defines your scope: H3-external is an
    INSTANCE of H10, not a distinct item. Duplicating one blind spot across two rows with two dispositions
    is a MECE break. So H3 (DS~Z's census) is wholly measurable and asserts only "no SOURCE-VISIBLE reader";
    YOU ARE THE SINGLE SITE WHERE THE EXTERNAL QUESTION IS DECLARED, and you enumerate every deletion
    candidate.

    ### THE FAILURE MODE YOU EXIST TO PREVENT

    SILENT UPGRADE: a zero-reader SOURCE census reported at Phase 6 as "proved zero readers."
    `02_NEEDED_VS_NOT_AUDIT.md` already states the correct floor — "a zero-reader result is a floor against
    source-visible readers." The stakes moved this afternoon: with H4's teardown authorized @c801ec9d5, a
    zero-reader claim is now upstream of an IRREVERSIBLE act rather than a reversible one.

    ### A MEASURED FALSE ZERO, SO YOU DO NOT INHERIT IT

    At c801ec9d5 on a fresh graph (age 0.0h, Nessie HEAD current), `comp-blast mdpf_aggregate_aua` returned
    "No downstream consumers found (no EXTRACTED edge — NOT provably zero)" — against W-1a ledger evidence
    of FOUR consumers (@ad76ad830, 439 partitions content-verified). GRAPH SAID ZERO; GROUND TRUTH SAID
    FOUR, on the one artifact whose contract is mid-cutover. An under-reporting instrument does not produce
    a durable zero; it produces a FALSE NEGATIVE THAT LOOKS LIKE A FINDING.

    ### DELETION CANDIDATES TO ENUMERATE

    From `02`'s provisional-retirement set and the DO-NOT-PORT table:
      - the four OWNTS outputs (zero estate readers per the 2026-07-28 consolidated reader census)
      - `platinum/mdpf/aggregate_aua_timeseries.json` (bare product-level object)
      - `wsb-49f-model-aua-daily` outputs
      - `wsd-49f-partner-held-etf-daily` outputs
      - anything under `s3://opal-data-mdpf/mdpf/feeds/*`
    DS~Z's P0-4 may add rows. Coordinate; do not duplicate their source-visible work.

    ### H13 IS OPEN AND ATTACHES TO THE DELETE STEP

    CTO~Z: Class B is NOT empty. S3 deletion sits on CLAUDE.md's standing human-confirmation list
    ("dropping tables / deleting S3 objects"), and Andrew's teardown word did NOT authorize it. THIS IS
    PRE-EXISTING LAW, NOT A NEW GATE, and it is named here so it is not discovered AT the delete step. Your
    output composes with it: the deletion, if it happens, is authorized by Andrew against a census HONESTLY
    LABELLED A FLOOR — which is precisely the information he needs in order to give that word.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-which "how do I find out who reads an S3 prefix that our source code does not reference"</run>
      <expect>Routes to a comp-tool, or runs comp-grep/comp-glob on-rails. Never a dead end.</expect>
      <if_mismatch>THIS IS THE HIGH-VALUE CASE FOR A COVERAGE-GAP REPORT. If no comp-tool covers
      external-reader detection, say so to COO~Z — Andrew-direct: the comp-tooling is FOUNDATIONAL, not
      additive, so a gap here is a DEFECT, not an inconvenience.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-estate --resource &lt;each deletion-candidate prefix&gt;</run>
      <expect>Thread membership + declared consumers per prefix. Read the provenance header — KEYS are
      re-derived live, NAMES come from a snapshot the tool declares stale past 14d.</expect>
      <if_mismatch>Stale header -> `--refresh` before trusting a NAME. A NAME miss is not an absent resource.</if_mismatch>

    Phase 3 — after committing: record every instrument checked, its result, AND ITS BLIND SPOT in the
    session log Compiler Tools table. The blind-spot column is the deliverable here, not a footnote.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>The deletion-candidate set (shared with DS~Z's P0-4 source census)</shared_resource>
    <also_in_to>P0-4 (0.4.0_DS_ClientPlatform~Z — source-visible half) · P6-1 (retirement) · P6-3 (ledger)</also_in_to>
    <last_write_owner>3.0.0_SA_CVO~Z owns the external declaration; DS~Z owns the source-visible census</last_write_owner>
    <required_action>MCP DS~Z to align the candidate list so neither of you assumes the other covered a row.
    DS~Z asserts "no SOURCE-VISIBLE reader" and must NOT report their census as closing H10; you assert the
    external limitation and must NOT re-run their source census. Two halves, one list, no overlap and no
    gap. Coordination artifact, NOT an approval step.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. THE TELEMETRY QUESTION IS ANSWERED AS A MEASUREMENT, NOT ASSUMED. For each bucket holding a deletion
       candidate, state whether CloudTrail DATA EVENTS are enabled — with the API call and its output.
       FORBIDDEN SHORTCUT, NAMED: do not skip to the limitation. "Uncloseable" was the label CTO~Z
       overturned precisely because it licenses skipping the work. If data events ARE enabled, you read
       them; a limitation recorded without checking is not this TO's deliverable.

    2. WHERE TELEMETRY EXISTS, IT IS READ, AND THE WINDOW IS STATED. Report the period actually covered and
       the readers found. A 90-day window is evidence about 90 days.

    3. S3 SERVER ACCESS LOGGING IS CHECKED SEPARATELY FROM CLOUDTRAIL. They are different instruments with
       different coverage; "no CloudTrail data events" does not mean "no access telemetry."

    4. OPERATIONAL RUNBOOKS AND HUMAN-FACING SURFACES ARE SEARCHED, with the surfaces named and the
       denominator printed (documents/paths searched). A manual consumer lives in a runbook, not in code.

    5. THE VERDICT IS A BOUNDED NEGATIVE AND SAYS SO IN ITS OWN WORDS. Permitted form: "NO READER VISIBLE TO
       THESE NAMED INSTRUMENTS: <list>, over <window>." Every instrument named, every window stated.
       RESERVED WORDS PROHIBITED ANYWHERE IN THE VERDICT: proof / provably / definitively / root cause /
       source-confirmed / "proved no external reader" / "mathematically certain."
       THE THIRD STATE IS THE POINT: TELEMETRY-ABSENT != NO-READER. Where an instrument does not exist, the
       row reads NOT-OBSERVABLE with the reason — never ZERO. An observation that was never possible is not
       a zero; and an absence of telemetry cannot be created retroactively.

    6. EVERY DELETION CANDIDATE HAS ITS OWN ROW. No candidate is covered by a group verdict. A row whose
       instruments differ from its neighbour's must show that difference.

    7. NO CONCLUSION RESTS ON A GRAPH EDGE COUNT — measured false zero above. If you cite comp-blast at all,
       cite it as a LOWER BOUND with its own note quoted.

    8. THE LIMITATION IS DRAFTED IN FINAL FORM NOW, NOT AT PHASE 6. Deliver the exact sentences the deploy
       ledger and the closure statement will carry, ready to paste.
       WHY THIS IS A CRITERION: CTO~Z's and MSTR~Z's shared concern is that an honesty caveat IMPROVISED
       UNDER DEPLOY PRESSURE is where silent upgrade happens. Writing it now, cold, is the control.

    9. H13 IS NAMED IN THE DELIVERABLE as attaching to the delete step — pre-existing CLAUDE.md law, not a
       new gate, and unresolved. State plainly that the census is a FLOOR, because that is the information
       Andrew needs in order to give or withhold the deletion word.

    10. YOUR OWN BLIND SPOTS ARE ENUMERATED. For each instrument you used, state what it CANNOT see. An
        instrument list without a blind-spot column reads as coverage.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier1_exec/3.0.0_SA_CVO/deliverables/MDPF_H10_EXTERNAL_READER_BOUNDED_NEGATIVE_20260806.md</file>
      <file action="reference">org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/MDPF_CONSOLIDATED_READER_CENSUS_20260728.md</file>
      <file action="reference">projects/MDPF_PROPVALIDATION/02_NEEDED_VS_NOT_AUDIT.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Measure whether reader telemetry exists; read it where it does.</requirement>
    <requirement id="2">One row per deletion candidate, each with its own instruments and window.</requirement>
    <requirement id="3">Verdict is a bounded negative naming instruments; reserved words prohibited.</requirement>
    <requirement id="4">Third state NOT-OBSERVABLE present and distinguished from ZERO.</requirement>
    <requirement id="5">Deliver the final-form limitation text now, ready for the ledger and closure statement.</requirement>
    <requirement id="6">Enumerate the blind spot of every instrument used.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">H10 bounded-negative deliverable, committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">Final-form limitation text for the deploy ledger + closure statement</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT DELETE ANYTHING, AND DO NOT AUTHORIZE A DELETION. This TO produces a bounded negative. H13
    is OPEN — S3 deletion is on CLAUDE.md's human-confirmation list and Andrew's teardown word did NOT cover
    it. S3 versioning is load-bearing for rollback.</rule>
    <rule>DO NOT CLAIM PROOF OF ABSENCE IN ANY FORM. A source census is blind to unregistered external and
    manual readers BY CONSTRUCTION, and where telemetry was never enabled the observation DOES NOT EXIST and
    cannot be created retroactively.</rule>
    <rule>DO NOT RE-RUN DS~Z'S SOURCE CENSUS. Their half asserts "no source-visible reader"; yours is the
    external declaration. Duplicating it re-creates the MECE break CTO~Z's classification removed.</rule>
    <rule>DO NOT CITE A ZERO-CONSUMER GRAPH RESULT AS EVIDENCE. Graph edges are a LOWER BOUND — measured
    false zero on mdpf_aggregate_aua at c801ec9d5 (0 reported vs 4 real).</rule>
    <rule>DO NOT BECOME A GATE, INCLUDING BY INVITATION. If any TO, agent, or ledger row makes your
    verification a precondition for someone else's work proceeding, REFUSE IT and tell COO~Z. Under the
    2026-08-06 no-gates rule a verifier who must bless before others advance IS a manufactured gate
    regardless of what it is called.</rule>
    <rule>NO NEW GATES of any kind in your deliverable — no approval step, co-sign, GO requirement, or
    review hold.</rule>
    <rule>NO ALARMS, SNS TOPICS, SES SENDS, FRESHNESS CHECKERS, OR MONITORS. If telemetry is absent, that is
    a RECORDED LIMITATION — it is NOT a warrant to build a reader-detector. Standing moratorium, and
    Andrew's ordering is canonical routes first, monitoring only once the thing being monitored is settled.</rule>
    <rule>NO SHADOWS. No parallel path, no standing comparator.</rule>
    <rule>DO NOT use the shared dirty checkout as evidence of live state. Never rebase on SITEZ. Commit to
    your lane; push is MSTR~Z's at :55-:00. Working files in the scratchpad.</rule>
    <rule>DISCARD any comp-freshness verdict produced on this box before 2c4510421 — it scored every S3
    artifact N/A/WARN and rendered failed retrievals as "prefix not found."</rule>
  </do_not>
</task_order>
