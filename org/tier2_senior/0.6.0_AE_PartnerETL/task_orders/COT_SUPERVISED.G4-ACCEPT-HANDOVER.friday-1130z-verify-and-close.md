<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-21-cot-g4-accept-handover</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>THE PARTNER-ETL SEAT LIVE ON THE MORNING OF 2026-08-21 -- primary: a respawned 0.6.2_AE_PartnerETL or 0.6.0_AE_PartnerETL (spawn need routed to 0.0.0_AB_MSTR); NAMED FALLBACK, so this cannot fall through: if NO PartnerETL seat is live by 2026-08-21 10:30Z, 0.7.0_AE_CloudOps takes the verify+close leg (cloud-ops lane, read-only S3 verification, no cot script edits).</issued_to>
    <date>2026-08-21</date>
    <status>pending -- HAS A REAL CLOCK: the COT_SUPERVISED G4/G4b acceptance fire is FRI 2026-08-21 11:30Z (cron(30 7) America/New_York, live-verified ENABLED -- NOT the stale 02:00Z anchor that four seats held yesterday and that was corrected at source). ⛔ THE OWNER VANISHED AND THE CLOCK DID NOT: Andrew closed 0.6.2_AE_PartnerETL after their final log (his word at the MSTR terminal, relayed 64069), and Monitor bgx6dde2b -- armed on the landing key and emitting on LANDING / OVERDUE / poll-error -- DIED WITH THE SESSION. A Monitor is session-bound. So today nothing notices the 11:30Z landing AND NOTHING NOTICES ITS ABSENCE: the OVERDUE limb is gone too, which was the half that would have caught a no-show. That is the silent-freeze shape, which is why this TO exists rather than a note.</status>
    <project_code>COT_SUPERVISED</project_code>
  </metadata>

  <objective>
    Verify the COT_SUPERVISED G4/G4b acceptance on the FRI 11:30Z scheduled fire, mint the proof
    instance, and RAVC-close -- the leg the closed seat was going to run. NOTHING NEW IS BUILT:
    the belt verifier exists, the baseline is measured, the prereqs are verified. This is a READ,
    a JUDGEMENT and a CLOSE.
  </objective>

  <context>
    ⛔ EVERYTHING BELOW SURVIVES IN THE REPO AT NAMED PINS -- start from this evidence, never from
    scratch, and never re-derive a number that was already measured:
    - THE BELT VERIFIER: committed @d4a86a84e1, NEGATIVE-CONTROLLED 8/12 PRE-FIRE by its author
      (their own control run, not an assertion) -- so a PASS from it means something.
    - THE BASELINE, measured on the SERVED 08-19 bytes (not quoted from a QA trace): 19 columns,
      18,051 data rows, ZERO "Supervised" columns. The author's QA read was 21 columns at the
      IDENTICAL 18,051 rows -- so today's verify is a true before/after: +2 columns, ROW COUNT
      UNCHANGED. A row-count change is a FINDING, not a pass.
    - THE ORACLE: HOLDINGS_DAILY_2026-08-20.xlsx was confirmed ABSENT pre-fire, so its APPEARANCE
      is unambiguous rather than a pre-existing file that could be misread.
    - THE OBSERVED CADENCE: each run lands 11:31-11:32Z under the PRIOR business day's as-of
      (snapshot lag-1); yesterday landed 08-19 primary at 11:32:16Z AND re-landed 08-18 at
      11:31:35Z (retry-net heal). Both are normal.
    - G4b deploy prereqs verified LIVE in S3, re-verified post-merge.
    - The closed seat's final log @d172142b44 (21:06Z) is the state-of-play and carries the
      Andrew-direct clock correction (11:30Z, not 02:00Z) that four seats had been holding wrong.

    ⛔ ONE CAVEAT THAT MUST TRAVEL, AND IT WILL FIRE FALSELY IF YOU IGNORE IT (MSTR 64069,
    source-confirmed): the closed seat pinned BOTH sha256 AND LastModified for the two
    acceptance-path objects and wrote "a surprise deploy shows up as a hash change." Site Z's
    leg-2 deploy at ~01:04Z REWROTE code/bronze/cot_bronze_ingest.py WITH IDENTICAL BYTES --
    LastModified 18:06:50Z -> 01:04:18Z, ETag a1d81b96... UNCHANGED. account_attributes.json did
    NOT move (still 18:06:01Z; it is .json and never in deploy scope). THE EXECUTED BYTES ARE
    UNCHANGED AND THE ACCEPTANCE IS UNAFFECTED. But: IF ANY LIMB OF THE VERIFIER COMPARES
    LastModified AGAINST THE 18:06:50Z PIN IT FIRES FALSELY AT 11:35Z. RE-PIN cot_bronze_ingest.py
    TO 01:04:18Z, or compare sha256 ONLY. The general lesson, worth carrying past today: "a
    surprise deploy shows up as a hash change" is TRUE for a content change and BLIND TO A
    REWRITE -- an identical-bytes rewrite moves the timestamp and moves no hash, and the deploy
    gate writes UNCONDITIONALLY and verifies AFTER (safe_deploy_core.py:548 cp, :555 head-object,
    :565 compare), so "MATCH" in its output means UPLOADED-AND-VERIFIED, never SKIPPED-BECAUSE-
    IDENTICAL.
    ⛔ AND THE TRADING-CALENDAR DEFAULT BINDS ANY STALENESS READ (NEVER#1): resolve the calendar
    before calling anything stale, and count in TRADING DAYS. Today is a trading day; the lag-1
    as-of is correct behaviour, not a defect.
  </context>

  <compiler_tools_mandate>
    Pre-fire (whenever you pick this up): re-read the schedule at BOTH planes before trusting the
    clock -- infra/aws/terraform/cot-pipeline/schedule-et.tf:90 (DESIRED) and
    `aws scheduler get-schedule cot-bd-session-daily-et` (APPLIED). A schedule claim gets read at
    both planes ONCE by whoever asserts it; that discipline is what caught yesterday's stale
    anchor at four seats.
    On landing: the belt verifier @d4a86a84e1 against the SERVED bytes; denominators printed;
    boto3/s3api (UTC) for every timestamp -- NEVER `aws s3 ls`, which renders LOCAL time with no
    marker and is silently off by the UTC offset.
    On absence: if nothing has landed by a reasonable margin after 11:30Z, that is a FINDING you
    surface the same hour -- SILENCE MUST NOT READ AS SUCCESS. The dead Monitor's OVERDUE limb is
    exactly what is missing, so a human read replaces it today.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - 0.2.0_DS_PortfolioAnalytics: holds the G4b half (sentinel + silver consuming) and keys on
      the SAME fire. Coordinate on landing; do not verify their half for them.
    - 1.0.0_SA_CTO: arch-gates the acceptance; this sits inside their FRI 11:30Z / 12:45Z / 13:30Z
      belt -- and the 12:45Z R14 chain is SEAT-DISJOINT from this one by design, so neither read
      collides with the other's holder.
    - 0.0.0_AB_MSTR: owns the spawn if a PartnerETL seat is respawned.
    - 2.0.0_SA_COO: validates the close.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is the G4/G4b ACCEPTANCE READ as cut -- V1 clock, V2
    landing-or-absence, V3 served verify, V4 belt test, V5 close; exhaustive over the read; the
    G1 bronze-fetch leg, the ~A MDPF_3FIRMS TOs, and any cot code change are OUTSIDE.)
    V1  CLOCK RE-READ AT BOTH PLANES before relying on it (DESIRED + APPLIED), stated with both
        values -- not inherited from this TO or from any report, including mine.
    V2  LANDING OR ABSENCE, both handled: HOLDINGS_DAILY_2026-08-20.xlsx present -> proceed;
        absent by a stated margin after 11:30Z -> a FINDING surfaced the same hour to COO + CTO
        (silence is not success).
    V3  SERVED-BYTES VERIFY: +2 supervised columns (19 -> 21) on 18,051 UNCHANGED rows; the
        sidecar; the bronze sentinel. A row-count change is a FINDING. Timestamps read in UTC via
        boto3/s3api; the cot_bronze_ingest.py pin RE-PINNED to 01:04:18Z or the timestamp limb
        dropped in favour of sha256 (state which you did and why).
    V4  THE G4 BELT'S FIRST REAL TEST: the per-row Holding-vs-Account supervised disagreement over
        the ~18k rows, run with the verifier's negative controls intact.
    V5  Proof instance VALID rc=0 (rc UNPIPED) over V1-V5; RAVC close to 2.0.0_SA_COO cc
        1.0.0_SA_CTO + 0.2.0_DS_PortfolioAnalytics.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>V1,V2,V3,V4,V5</expected_criteria>
    <instance_path>org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/COT_SUPERVISED.G4-ACCEPT_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">READ-ONLY on cot: verify served bytes; do NOT edit a cot script, do NOT fire an ad-hoc run (production numbers come from the scheduled run; an ad-hoc run's artifacts are never production evidence). If the fire is missed or the seating falls through, the acceptance slides trading-day-for-trading-day and you surface it -- it does not silently wait. Surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
