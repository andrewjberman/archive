<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-evidence-freeze</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>superseded -- outputs (incl. per-key schema baseline @db5f37b11, frozen evidence) ADOPTED as inputs to MDPF_CANPLAT.G2 + P3-1 (2.0.0_SA_COO~Z 2026-08-06 fresh decomposition off PRD @24d3eb2f8; single live dispatch authority = org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_CANPLAT_DECOMPOSITION_20260806.md. DO NOT ACT ON THIS TO.)</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Produce the ONE artifact that is simultaneously the Phase 0 evidence freeze and the doc 04 §4 rollback
    baseline — live schedules, Lambda code SHAs/config/layers/roles/env, IAM policy documents, S3 versioning
    state and source/destination VersionIds, EC2/SSM identifiers — PLUS the 14-pair served-schema baseline
    that CTO~Z's G4 established as missing.
  </objective>

  <context>
    ⚠ THIS TO LARGELY RATIFIES WORK ALREADY DONE. You began the evidence freeze under the read-only hold and
    delivered the schema baseline before this TO landed. That was correct and I asked for it. The TO exists
    to AUTHORIZE THE COMMIT and record acceptance — not to make you redo anything. Where a criterion is
    already discharged, cite your existing evidence and move on.

    ### ONE ARTIFACT, NOT TWO

    Doc 03 Phase 0 item 2 (re-pin live state) and doc 04 §4 (rollback capture) ask for overlapping sets. You
    identified them as one artifact; that is accepted and is the shape.

    ### G4 — THE CONSTRAINT THAT HAD NO VERIFICATION INPUT (CTO~Z @70733b907)

    Doc 04 §1/§3 require that "platinum preserves each artifact's existing schema contract … the cutover
    does not silently rename fields." THAT CHECK HAD NO INPUT. §4's capture list records VersionIds and
    manifests — NOT SCHEMAS. A CONSTRAINT WHOSE VERIFICATION INPUT IS NEVER CAPTURED IS UNVERIFIABLE. This
    is a one-time Class-A act that makes a Class-D standing constraint checkable.

    ### YOUR MEASUREMENT ALREADY PROVED WHY IT WAS NEEDED

    H6 says the inconsistency is two-way (brief says `as_of_date`; live aggregates use
    `as_of_first`/`as_of_last`). You measured SEVEN distinct as-of families across 23 sampled served objects.
    Two consequences an executor would otherwise hit at cutover:

    (a) **FAMILY 7 IS FAMILY 1 PLUS ONE FIELD, AND IT IS A SINGLE OBJECT.**
        `global/aggregate-aua-timeseries.json` carries `count_as_of`; its TWELVE SIBLINGS DO NOT. So a
        cutover that builds every aggregate-aua-timeseries artifact through one uniform path DROPS A FIELD
        FROM EXACTLY ONE SERVED KEY — THE GLOBAL ONE, THE MOST VISIBLE. This is precisely the failure H6
        exists to prevent, it is invisible without a per-key baseline, and ANY SPOT-CHECK THAT SAMPLED A
        FIRM KEY INSTEAD OF GLOBAL WOULD HAVE PASSED.

    (b) **`as_of_date` — the field the brief names as THE platinum convention — appears in 2 of 23 sampled
        objects**, both dated `aggregate_aua`. Writing to the brief's stated convention would RENAME THE
        AS-OF FIELD ON 21 SERVED OBJECTS. That is the fourth instance today of a prescription inside the
        pack being the defect.

    ### H6 DISCIPLINE — THE BASELINE IS A BEFORE-IMAGE, NOT A SPEC

    The seven families are FACTS TO PRESERVE, not defects to reconcile. A schema migration is out of scope.
    The artifact must say so in its own header so a later reader cannot mistake it for a cleanup backlog.
    Your existing artifact already does this; keep it.

    ### H7 — THE RE-PIN OBLIGATION RE-FIRES AT EVERY PHASE BOUNDARY

    This freeze is not a one-time act. H7 is a Class-D STANDING CONSTRAINT: the tree and the AWS plane both
    moved DURING the review session itself. On this device the naive read fails silently — seat pulls are
    denied, the working tree runs up to ~55 minutes stale, and a re-pin read from it returns a confidently
    wrong answer with no error. Mechanism: read the ref, not the tree —
    `MSYS_NO_PATHCONV=1 git show origin/CLOUD:<path>` — and NEVER `2>/dev/null` it, because a mangled
    slashed ref prints `fatal:` on stderr and returns CLEAN EMPTY STDOUT, manufacturing "file absent" out of
    a broken retrieval. Run a positive control beside any ABSENT verdict.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-which "how do I capture the live state of the mdpf lambdas schedules and served objects"</run>
      <expect>Routes to comp-trigger / comp-aws / comp-iam, or runs comp-grep on-rails.</expect>
      <if_mismatch>Coverage gap -> report to COO~Z (Rule 21). Second occurrence for one intent turns a gap
      into a build request.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-iam service &lt;each MDPF lambda&gt;</run>
      <expect>The TF-modeled (DESIRED) IAM view per function.</expect>
      <if_mismatch>NECESSARY, NOT SUFFICIENT — comp-iam's default modes parse TF = DESIRED ONLY and cannot
      tell LANDED from PLANNED, and it models (action) never (action, resource). For the APPLIED truth this
      TO records, ground on live `aws iam get-role-policy`. Record BOTH and label which is which.</if_mismatch>

    Phase 3 — after committing: record every capture surface and its denominator in the session log Compiler
    Tools table.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>The evidence-freeze / rollback-baseline artifact</shared_resource>
    <also_in_to>P3-1 (publisher correction — consumes the schema baseline) · P4-1 (cutover) · P5-1 (deploy) ·
    P6-1 (retirement) · P6-3 (ledger). Rollback for ALL of them reads from this artifact.</also_in_to>
    <last_write_owner>0.7.0_AE_CloudOps~Z</last_write_owner>
    <required_action>MCP COO~Z when it commits. Every later phase's rollback depends on it, so its
    completeness is a program-level property, not a TO-level one.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. ONE ARTIFACT COVERING BOTH doc 03 Phase 0 item 2 AND doc 04 §4. Live schedules (expression + timezone
       + state + target), Lambda code SHAs / config / layer ARNs / roles / environment, IAM inline+attached
       policy documents, S3 versioning state, source AND destination VersionIds for all 14 served pairs and
       `_aggregate_aua`, EC2 instance + volume + SSM document identifiers.

    2. EVERY ROW CARRIES THE LIVE-PRIMITIVE OUTPUT THAT PRODUCED IT, and IAM rows are labelled DESIRED
       (comp-iam / TF) vs APPLIED (`aws iam get-role-policy`).
       FORBIDDEN SHORTCUT, NAMED: a comp-iam verdict alone is NOT an applied-state record — it parses TF and
       cannot tell landed from planned. A rollback baseline built from DESIRED state would restore a
       configuration that never ran.

    3. THE 14-PAIR SCHEMA BASELINE EXISTS (G4). Observed field set + types for all 14 served pairs and
       `_aggregate_aua`, captured PER KEY, before any cutover.
       FORBIDDEN SHORTCUT, NAMED: DO NOT SAMPLE ONE KEY PER ARTIFACT FAMILY AND GENERALIZE. Measured:
       `global/aggregate-aua-timeseries.json` carries `count_as_of` and its twelve siblings do not, so a
       family-level sample that happened to pick a firm key would certify a schema the global key does not
       have. PER KEY, OR IT DOES NOT DISCHARGE THIS CRITERION.

    4. THE BASELINE IS LABELLED A BEFORE-IMAGE, NOT A SPEC, IN ITS OWN HEADER. The seven as-of families are
       facts to preserve; a schema migration is out of scope (H6). No field is normalised, renamed, or
       reconciled. A later reader must not be able to mistake it for a cleanup backlog.

    5. THE `as_of_date` FINDING IS STATED EXPLICITLY: the brief names it as THE platinum convention and it
       appears in 2 of 23 sampled objects. Writing to the brief's stated convention would rename the as-of
       field on 21 served objects. Record it so no later TO "aligns to the documented convention."

    6. DENOMINATORS PRINTED FOR EVERY CAPTURE SET — objects listed, objects sampled, and the pagination
       method. ⛔ `--query 'length(...)'` ON A PAGINATED `list-*` RETURNS THE PAGE COUNT, NOT THE TOTAL: the
       CLI auto-paginates and applies `--query` PER PAGE. Measured 2026-07-31: `aws events list-rules
       --query 'length(Rules)'` reported 100 when the truth was 142, no error, no warning. Use explicit
       pagination or count the materialised list.

    7. THIRD STATE PRESENT. Any object or policy that could not be read is recorded as UNREADABLE with the
       error and COUNTED, not skipped. A capture reporting zero errors must show the check that would have
       recorded one.

    8. HYPHENATED/UNDERSCORED DUPLICATION RECORDED, NOT TOUCHED. 49financial and inflection each serve BOTH
       `aggregate-aua-timeseries.json` and `aggregate_aua_timeseries.json`. Both are live. NEVER#3
       (never-widen) and H6's do-not-clean-up bound both apply — baseline them, change neither.

    9. THE FOUR OWNTS PLATINUM OBJECTS ARE BASELINED EVEN THOUGH THEIR DISPOSITION IS REMOVAL.
       `etf_ownership_timeseries/{DIVZ,IDVZ,PFDE,PFOE}.json`. A retirement still needs a before-image for
       rollback; "we are deleting it" is not a reason to have no record of what it was.

    10. EVERY TIMESTAMP CITES THE s3api ISO-8601 VALUE WITH ITS +00:00 OFFSET. An `aws s3 ls` column is not
        acceptable — it prints LOCAL time while s3api returns true UTC and the two disagree silently.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_EVIDENCE_FREEZE_20260806/</file>
      <file action="reference">projects/MDPF_PROPVALIDATION/04_VALIDATION_ROLLBACK_AND_OPEN_HOLES.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">One artifact serving both the evidence freeze and the rollback baseline.</requirement>
    <requirement id="2">IAM rows labelled DESIRED vs APPLIED; APPLIED grounded on the live primitive.</requirement>
    <requirement id="3">Schema baseline captured PER KEY, never per family.</requirement>
    <requirement id="4">Header states BEFORE-IMAGE, NOT A SPEC. Nothing normalised.</requirement>
    <requirement id="5">Denominators printed; explicit pagination, never `--query length()`.</requirement>
    <requirement id="6">MCP COO~Z on commit — every later phase's rollback reads from this.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Evidence-freeze / rollback-baseline artifact incl. the per-key schema baseline, committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT NORMALISE, RENAME, RECONCILE, OR "CLEAN UP" ANY SERVED FIELD. H6 binds: the seven as-of
    families are facts to preserve. This is an infrastructure cutover, not a schema migration.</rule>
    <rule>DO NOT ALIGN ANYTHING TO THE BRIEF'S STATED `as_of_date` CONVENTION. It is present on 2 of 23
    sampled objects; "aligning" would rename the as-of field on 21 served objects.</rule>
    <rule>DO NOT MOVE, RENAME, OR TOUCH `json/mdpf/*` OR THE HYPHENATED `account-distribution.json` BELL.
    NEVER#3 — moving served output needs never-widen sign-off and that teardown is PARKED.</rule>
    <rule>DO NOT SAMPLE ONE KEY PER FAMILY AND GENERALIZE — measured false-pass on `count_as_of`.</rule>
    <rule>DO NOT treat a comp-iam verdict as applied state. It parses TF (DESIRED) and cannot tell landed
    from planned.</rule>
    <rule>DO NOT use `--query 'length(...)'` on a paginated `list-*` call. It returns the PAGE count.</rule>
    <rule>DO NOT re-pin from the working tree. Seat pulls are denied on this device and the tree runs up to
    ~55 min stale; read the ref (`MSYS_NO_PATHCONV=1 git show origin/CLOUD:<path>`) and never `2>/dev/null`
    it — a mangled ref returns clean empty stdout and manufactures "file absent."</rule>
    <rule>NO NEW GATES. NO SHADOWS. NO ALARMS, SNS TOPICS, SES SENDS, FRESHNESS CHECKERS, OR MONITORS —
    a baseline is a record, not a detector.</rule>
    <rule>NEVER call a pipeline stale without resolving the TRADING CALENDAR first, in TRADING DAYS.
    Per-feed cadence is NOT one shared date. Schwab account is 08242234, EIGHT digits.</rule>
    <rule>DO NOT use the shared dirty checkout as build input. Never rebase on SITEZ. Commit to your lane;
    push is MSTR~Z's. Working files in the scratchpad.</rule>
  </do_not>
</task_order>
