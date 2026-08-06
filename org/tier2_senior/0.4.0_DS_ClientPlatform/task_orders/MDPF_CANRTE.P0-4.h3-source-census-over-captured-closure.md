<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-h3-source-census</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~Z</issued_to>
    <date>2026-08-06</date>
    <status>superseded -- census outputs adopted as MDPF_CANPLAT.P1-1 input; do not re-run (2.0.0_SA_COO~Z 2026-08-06 fresh decomposition off PRD @24d3eb2f8; single live dispatch authority = org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_CANPLAT_DECOMPOSITION_20260806.md. DO NOT ACT ON THIS TO.)</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Build the static import + S3 read/write graph over the CAPTURED EC2 closure (not the repo closure), so
    that (a) the provisional retirement set can be dispositioned against source-visible evidence, and (b)
    Andrew's port-completeness condition has an instrument. Also close the one open sizing question:
    WHERE COTTONWOOD'S REAL L2 PRODUCER LIVES.
  </objective>

  <context>
    Your read-only import-surface delivery (20260806T203704Z) is accepted in full and is the basis of this
    TO. Three of your findings changed scope and are folded into it.

    H3 IS RANKED FIRST IN THE PROGRAM (CTO~Z @70733b907). Its scope widened: it is no longer only a
    deletion-safety census, it is the DISCHARGE INSTRUMENT for the sovereign condition Andrew attached to an
    irreversible act. Andrew-direct 2026-08-06 @c801ec9d5: "Teardown is fine just need to make sure any
    necessary code on that ec2 is properly ported to the lambda."

    ### THE GRAPH IS BUILT OVER THE CAPTURED CLOSURE, NOT THE REPO

    CTO~Z's sharpening, and it is the whole point of the sequencing: A GRAPH BUILT FROM REPO SOURCE INHERITS
    THE VERY DIVERGENCE IT EXISTS TO DETECT. `01` s.10 and H8 establish repo-vs-deployed divergence as this
    estate's demonstrated norm, and you measured the cleanest instance of it yourself
    (`pandas_market_calendars`: absent from requirements.txt, zero repo-wide hits, exists only as a bash
    preflight line in the file being retired).

    So this TO DEPENDS ON P0-7 (AE~Z, EC2 code capture). AE~Z will MCP you the S3 URI and the denominator N
    the moment it lands. THE H14 HALF AND THE COTTONWOOD-PRODUCER HALF BELOW ARE NOT BLOCKED ON IT — start
    those now.

    ### WHAT YOU ALREADY ESTABLISHED (do not re-spend on these)

    - The 9 gold modules and their import surface, at SITEZ 73ca92eb3, denominator printed.
    - They are NOT an importable package: flat CLI scripts importing each other by BARE MODULE NAME off a
      self-inserted `sys.path`, argparse + `main()->int` + `__main__` guard throughout.
    - NAMING TRAP, recorded: `build_mdpf_spine.py` is NOT the spine — it is a 145-line driver. The spine is
      `dim_mdpf_aggregate_aua_timeseries.py` (2587 lines), imported as `spine`.
    - "Firm-parameterized" is FALSE in the incumbent — three shapes, not one, and Inflection consumes
      49financial's `dates` as its axis (a real cross-firm dependency in shipped code).
    - Channel independence does NOT hold today. Per-scope exceptions are work to ADD, not preserve.

    ### CTO~Z CLOSED HALF OF H14 ON YOUR MEASUREMENT — do not re-open it

    CTO~Z landed H14 asking as open Phase-0 work: "what computes the six per-feed frontiers today?" YOU
    ANSWERED IT — the inlined privates at `dim_mdpf_aggregate_aua_timeseries.py:154,164`. CTO~Z has recorded
    the accurate statement: the frontier is not uncomputed, IT IS COMPUTED BY A THIRD COPY THE LAW DOES NOT
    KNOW ABOUT. That item is CLOSED. Phase 0 does not re-spend on it. Credit recorded as yours.

    ### CALENDAR BINDING — RULED, so you can size P1.1

    CTO~Z RULING (20260806T204019Z): BIND `lib/trading_calendar.py` VIA THE WS-1 SHARED LAYER. Retire
    `data/mdpf/scripts/gold/_trading_day_calendar.py` and both inlined privates. Your recommendation
    carried. Four conditions attach — condition 1 (the exercised tie-out with a mutant) is YOUR work and is
    criterion 6 below. The scope bound is explicit: vendored `trading_calendar.py` copies under
    `bd-served-vintage-alarm`, `inf-etf-ownership-daily`, and `opal-assets-absence-check` ARE OTHER
    PIPELINES AND THIS RULING DOES NOT TOUCH THEM. A ruling that dissolves a workaround is not a licence to
    sweep the estate.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-which "what reads the mdpf feeder outputs and the aggregate aua prefix"</run>
      <expect>Routes to comp-pipescript / comp-estate, or runs comp-grep on-rails.</expect>
      <if_mismatch>Repeat override for one intent = COVERAGE GAP -> report to COO~Z (Rule 21).</if_mismatch>

      <run>comp-pipescript io &lt;each gold script in the closure&gt; --pipeline mdpf</run>
      <expect>COLUMN GAPS and portal consumers per script. `--pipeline` IS REQUIRED — flagless is rc=2
      REFUSED since 07-30 and once silently defaulted to bd-gold, returning clean zeros for other trees.</expect>
      <if_mismatch>Any COLUMN GAP is fixed or recorded before it reaches P1.1 — silent column omissions have
      produced zero-valued served output before.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-pipescript consumers &lt;each candidate-retirement artifact key&gt;</run>
      <expect>Consumer list per key, WITH THE DENOMINATOR of what was scanned.</expect>
      <if_mismatch>A zero here does NOT close the question — see criterion 3.</if_mismatch>

    Phase 3 — after committing: record every census result + its denominator in the session log Compiler
    Tools table. A denominator-free row is not accepted.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>The captured EC2 closure in S3 (produced by P0-7, 0.7.0_AE_CloudOps~Z)</shared_resource>
    <also_in_to>P0-7 (produces it) · P6-0 (three-bucket discharge consumes both)</also_in_to>
    <last_write_owner>0.7.0_AE_CloudOps~Z owns the capture; you own the graph built over it</last_write_owner>
    <required_action>AE~Z MCPs you the S3 URI + denominator N on landing. Build the graph over THAT, not over
    the repo. If the capture is delayed past your other work, do the H14 and Cottonwood halves first and
    report the graph half as NOT-STARTED-PENDING-CAPTURE — never as complete-with-repo-source.</required_action>

    <shared_resource>data/mdpf/scripts/gold/*.py (Rule 13, yours end-to-end) imported by
    infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/ (AE~Z)</shared_resource>
    <also_in_to>P1-1 (yours) · P1-2 (AE~Z package)</also_in_to>
    <required_action>AE~Z has delivered their half of the seam: runtime is python3.11 NOT 3.12 (hard ABI pin
    — every pandas/pyarrow layer in the account is 3.11-only; the live MDPF Lambdas are 3.12 only because
    they are thin JSON handlers touching no columnar stack), x86_64, FLAT vendoring at zip root, repo files
    are source of truth, NEVER edit a zip. Build to cp311; assume no 3.12-only syntax or wheels. You supply
    PATHS + a COMMIT for BUILD_MANIFEST.json; AE computes the hashes from the repo file at build — a hash
    supplied by hand and a hash computed from the artifact are different claims and only the second is a
    control.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. THE GRAPH IS BUILT OVER THE CAPTURED CLOSURE. State the S3 URI of the capture it was built from and
       the capture's denominator N.
       FORBIDDEN SHORTCUT, NAMED: a graph built from repo source is REJECTED for this criterion regardless
       of how complete it looks — it inherits the divergence it exists to detect. If the capture has not
       landed, report NOT-STARTED-PENDING-CAPTURE. That is an honest state; a repo-source graph labelled
       complete is not.

    2. EVERY CENSUS PRINTS ITS DENOMINATOR. Files scanned, prefixes scanned, surfaces searched. A retrieval
       that returns zero must show a POSITIVE CONTROL (a hit you know exists, found by the same command).
       WHY: a retrieval FAILURE returns a VALUE — `grep -c` counts zero inside an error message.

    3. NO CONCLUSION RESTS ON A GRAPH EDGE COUNT. Every zero-reader claim is corroborated by a literal-key
       grep PLUS `comp-pipescript consumers`, both with denominators.
       MEASURED, and this is why the rule exists: at c801ec9d5 on a fresh DB (age 0.0h, Nessie HEAD current)
       `comp-blast mdpf_aggregate_aua` returned "No downstream consumers found (no EXTRACTED edge — NOT
       provably zero)" against W-1a ledger evidence of FOUR consumers (@ad76ad830, 439 partitions
       content-verified). GRAPH SAID ZERO; GROUND TRUTH SAID FOUR — on the one artifact whose contract is
       mid-cutover. An under-reporting instrument does not produce a durable zero, it produces a FALSE
       NEGATIVE THAT LOOKS LIKE A FINDING.

    4. WHAT A ZERO MAY ASSERT. The deliverable says "NO SOURCE-VISIBLE READER" and never "no reader."
       RESERVED WORDS PROHIBITED on any absence claim: proof / provably / definitively / source-confirmed.
       The external-reader question is H10 and belongs to CVO~Z's P0-6 — it is NOT yours to close, and your
       census must not be reported as closing it. `02` already states the correct floor: a zero-reader
       result is a floor against SOURCE-VISIBLE readers.

    5. COTTONWOOD'S REAL L2 PRODUCER IS LOCATED AND NAMED — file path, and the S3 key it writes.
       WHY THIS IS A CRITERION AND NOT A NOTE: you measured that `load_cottonwood_slice(s3)` runs gates and
       then emits `gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json` BYTES VERBATIM ("the slice IS
       cot's L2 producer per F-2"). So "port the firm-parameterized spine" CANNOT be discharged by porting
       the two modules — the real producer is outside both, and its location BLOCKS SIZING of P1-1, not just
       its design. If it cannot be located, that is a FINDING reported to COO~Z + CTO~Z, not a gap to
       estimate around. `stage_mdpf_revamp_trio.py` is likely the choreography, not the producer.

    6. THE CALENDAR TIE-OUT IS EXERCISED AND CARRIES A MUTANT (CTO~Z ruling condition 1). Compute BOTH
       calendars across the full in-window range; assert set equality; PRINT THE DENOMINATOR — the NUMBER OF
       DATES COMPARED, not "matches". Then MUTATE ONE DATE and prove the comparison FAILS and localizes.
       FORBIDDEN SHORTCUT, NAMED: your in-window no-op claim (lib's set is the documented UNION; both drop
       2025-01-09 and 2026-07-03) is a HYPOTHESIS UNTIL RUN. `02` already mandates this shape — A TIE
       WITHOUT A POSITIVE FALSIFIER IS NOT PROOF. A passing equality check never made to fail has not been
       tested.

    7. `calendar_source()` ASSERTION SPECIFIED (CTO~Z ruling condition 3, ratified). State the exact
       assertion P1-1 will carry: `calendar_source() == "NYSE/pandas_market_calendars"`, per
       calendar-touching artifact, at build time and in acceptance.
       WHY IT REPLACES rather than supplements doc 02's check: doc 02's prescribed "import-health invocation"
       is FAIL-GREEN BY CONSTRUCTION — the PMC import sits in try/except ImportError, so it PASSES IN
       EXACTLY THE STATE IT EXISTS TO DETECT. That is not a weak control, it is an ANTI-CONTROL: it reports
       healthy BECAUSE the fallback engaged. This is an ASSERTION inside existing scope — it is NOT an alarm,
       monitor, or notification, and must not be written as one.

    8. THE 2027 EXPIRY IS STATED AS MEASURED FACT. Fallback `is_trading_day` is
       `iso not in _NYSE_HOLIDAYS_FALLBACK` over a set ending 2026-12-31, so FROM 2027-01-01 EVERY WEEKDAY
       READS AS A TRADING DAY — New Year's Day, MLK, Good Friday — silently, no raise, no warn, wrong
       frontier, wrong `trading_days_behind`. Under five months of runway from today.

    9. THE PROVISIONAL SET IS DISPOSITIONED PER ITEM, NOT AS A GROUP: `wsb-49f-model-aua-daily`,
       `wsd-49f-partner-held-etf-daily`, any writer/reader of `s3://opal-data-mdpf/mdpf/feeds/*`, feeder
       computations used by `mdpf_aggregate_aua.py`, and any captured script used as a library or imported
       source. Each gets its own row and its own evidence.
       Third state required: SOURCE-VISIBLE-READER-FOUND / NO-SOURCE-VISIBLE-READER / NOT-DETERMINABLE
       (with the reason). NOT-DETERMINABLE != NO READER.

    10. SCOPE BOUND HELD. The vendored `trading_calendar.py` copies under `bd-served-vintage-alarm`,
        `inf-etf-ownership-daily`, `opal-assets-absence-check` are NOT touched, NOT bound, NOT swept. Note
        the general condition for WS-1 sizing and route it to COO~Z; absorb none of it here.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/MDPF_H3_SOURCE_CENSUS_20260806.md</file>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/MDPF_CALENDAR_TIEOUT_20260806.md</file>
      <file action="reference">data/mdpf/scripts/gold/*.py</file>
      <file action="reference">lib/trading_calendar.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Build the import + S3 read/write graph over the CAPTURED closure. Never repo source.</requirement>
    <requirement id="2">Print the denominator of every scan; positive-control every zero.</requirement>
    <requirement id="3">Locate and name Cottonwood's real L2 producer — it blocks P1-1 sizing.</requirement>
    <requirement id="4">Exercise the calendar tie-out with a mutant; print dates compared.</requirement>
    <requirement id="5">Disposition the provisional set per item with a third state available.</requirement>
    <requirement id="6">Do not close H10. Do not sweep other pipelines' calendar copies.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">H3 census + calendar tie-out deliverables, committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">Cottonwood L2 producer location reported to COO~Z + CTO~Z (blocks P1-1 sizing)</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT DELETE ANYTHING. This TO dispositions; it does not retire. H13 is OPEN — S3 deletion sits on
    CLAUDE.md's human-confirmation list and Andrew's teardown word did NOT authorize it. S3 versioning is
    load-bearing for rollback.</rule>
    <rule>DO NOT CITE A ZERO-CONSUMER GRAPH RESULT AS EVIDENCE FOR A RETIREMENT. Graph edges are a LOWER
    BOUND — measured false zero on mdpf_aggregate_aua at c801ec9d5 (0 reported vs 4 real).</rule>
    <rule>DO NOT REPORT A SOURCE CENSUS AS CLOSING H10. A source census is blind to unregistered external
    and manual readers by construction. That declaration site is CVO~Z's P0-6, and it terminates in a
    RECORDED LIMITATION naming the telemetry actually checked — never in "proved."</rule>
    <rule>DO NOT build the graph from repo source and label it complete. If the capture has not landed,
    report NOT-STARTED-PENDING-CAPTURE.</rule>
    <rule>DO NOT accept an import-health pass as evidence PMC is present — the import is in try/except and
    absence does not raise.</rule>
    <rule>DO NOT bind or modify the vendored calendar copies in bd-served-vintage-alarm,
    inf-etf-ownership-daily, or opal-assets-absence-check. Other pipelines, WS-1's scope.</rule>
    <rule>NO NEW GATES — no approval step, co-sign, GO requirement, or review hold anywhere in your
    deliverable. Mechanical rails (commit-gate, safe-commit, owned-paths) are pre-existing and untouched.</rule>
    <rule>NO SHADOWS. No parallel producer, no shadow/parity/comparator prefix, no standing comparator.
    Finite QA batteries are legal; nothing stands.</rule>
    <rule>NO ALARMS, SNS TOPICS, SES SENDS, FRESHNESS CHECKERS, OR MONITORS. The calendar_source assertion is
    a build-time + acceptance ASSERTION, not a detector — do not let it be written as one.</rule>
    <rule>NEVER call a pipeline stale without resolving the TRADING CALENDAR first, in TRADING DAYS.
    Per-feed cadence is NOT one shared date. Schwab account is 08242234, EIGHT digits, never 08335338.</rule>
    <rule>DO NOT use the shared dirty checkout as build input. Never rebase on SITEZ. Commit to your lane;
    push is MSTR~Z's at :55-:00. Working files in the scratchpad — the shared tree loses uncommitted work and
    `git stash` is prohibited here.</rule>
    <rule>DO NOT touch source under data/mdpf/scripts/gold/ in this TO. It is a census + tie-out. The
    refactor is P1-1.</rule>
  </do_not>
</task_order>
