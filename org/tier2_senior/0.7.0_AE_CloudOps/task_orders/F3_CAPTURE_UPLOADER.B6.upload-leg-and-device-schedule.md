# TO F3_CAPTURE_UPLOADER.B6 — the F3 operator-signal capture uploader: upload leg + device-side daily schedule

<task_order>
  <metadata>
    <to_id>F3_CAPTURE_UPLOADER.B6.upload-leg-and-device-schedule</to_id>
    <project>NFRA_ESTATE_REPORT</project>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued>2026-08-11</issued>
    <status>active</status>
    <gate>1.0.0_SA_CTO</gate>
    <verifier>3.0.0_SA_CVO</verifier>
  </metadata>

  <objective>
    Deliver B6 CORE = B6-1 (upload leg) + B6-2 (device-side daily schedule), completing the F3
    operator-signal capture path so F3's real feed EXISTS. Andrew-directed 2026-08-11 (AskUserQuestion,
    via 4.0.0_SA_CRO~B) as the pipeline's highest-leverage unbuilt item.
  </objective>

  <context>
    GOVERNING SPEC (read it; this TO commissions, it does not restate):
      org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260811_BUILD_B6_AND_COMPLETION_SPEC.md
      §3 completion table · §3a CTO arch-gate PRE-RULINGS (093024Z) · §3b CVO layout confirmation (093223Z)

    B6 IS ~70% BUILT AND THE HARD PART IS DONE. `.tools/estate-capture.py` — the device-side EXTRACTOR
    with mid-turn-input union and fail-closed HUMAN/HARNESS/UNCLASSIFIED provenance — EXISTS and is
    corpus-hardened. MISSING is plumbing only: `main()` prints / `--json` and there is NO S3 upload and
    NO schedule. Do not rebuild the extractor. BUILD LADDER rung 2: the estate already has it.

    STAFFING HAS NO OPEN GATE QUESTION. CTO pre-ruled every one at 093024Z ("Build on."): the S3 key
    layout is APPROVED as v1; v4 reconciliation is DEFERRED (do not reconcile against an unbuilt
    layout); device-side placement CONFIRMED; capture-cadence-not-monitor framing CONFIRMED; B6-3
    riding the friction-axis runner build is CORRECT SEQUENCING. CVO confirmed the layout against the
    live bucket at 093223Z.

    ⚠ MORATORIUM CHECK, RESOLVED — READ IT SO YOU DO NOT RE-LITIGATE IT: this is a CAPTURE/ARCHIVE
    CADENCE, not a monitor, alarm, notification or freshness checker. CTO confirmed the framing
    explicitly ("a schedule that ARCHIVES is a route"). The standing moratorium is NOT engaged and the
    "production pipelines must have a schedule" rule makes B6-2 MANDATORY, not optional. Build no
    alerting, no SNS, no SES, no *-monitor/*-checker naming on this path.
  </context>

  <compiler_tools_mandate>
    comp-which before writing anything new (BUILD LADDER rung 2 — the extractor already exists).
    comp-iam for the S3 write grant — and treat its output as a FLOOR, never a sufficiency verdict: it
    models (action), never (action, resource). For the NEW bucket path, ground on the live primitive
    with ONE `--resource-arns` per call and a SEPARATE positive control:
      aws iam simulate-principal-policy --policy-source-arn <role> --action-names s3:PutObject --resource-arns <exact key>
    Never use simulate-principal-policy to check whether an action NAME is real (a nonexistent action
    returns implicitDeny, indistinguishable from a missing grant) — that oracle is
    `aws accessanalyzer validate-policy`.
  </compiler_tools_mandate>

  <acceptance_criteria>
    The spec's §3 rows are the bar, plus CTO's §3a MECHANICAL GATE CHECKS named there so the build
    arrives ready, plus CVO's §3b riders. Not restated here — cite the spec.
    BEHAVIORAL, not config-read (Rule 22a): "the upload works" is EXERCISED — a real capture uploaded
    and READ BACK from S3, not an IAM verdict and not an rc=0.
  </acceptance_criteria>

  <proof_of_spec>
    <instance_path_grammar>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/PROOF_OF_SPEC_B6_{PIECE}_{YYYYMMDD}.json</instance_path_grammar>
    <criterion_id_grammar>B6-{piece}-{check}</criterion_id_grammar>
    <group id="B6-1" status="MINTED 2026-08-11 by assignee from spec §3 row B6-1 + §3a gate check (a) + §3b rider (a) + TO acceptance line"
           ids="B6-1-key-layout,B6-1-per-device-partial-visible,B6-1-idempotent,B6-1-bronze-raw,B6-1-no-data-day-loud,B6-1-iam-live-primitive,B6-1-exercised-readback"/>
    <group id="B6-2" status="MINTED 2026-08-11 by assignee from spec §3 row B6-2 + §3a gate check (b) + TO reqs 3/4/5 + do-not #3"
           ids="B6-2-device-side-daily-schedule,B6-2-group-w-floor,B6-2-exercised-run,B6-2-andrew-surfaced-at-creation,B6-2-site-z-declared-gap,B6-2-moratorium-naming"/>
    <!-- JUDGMENT CALLS (assignee, per this block's instruction):
         (1) phase enum: B6 sits outside the MDPF P1-P5 program; instances use P1-SCRIPTS (B6-1,
             a script build) and P2-TIMING (B6-2, a schedule) as the least-wrong build-phase
             values rather than NON-BUILD-OTHER (it IS a build). Flagged here so a verifier does
             not read them as MDPF-program membership.
         (2) B6-1-iam-live-primitive: the deny-capable simulate limb is UNCOMPUTABLE for the
             admin-class device principal (identity policy allows all s3:PutObject) -- declared
             in the instance per the pre-authorized UNCOMPUTABLE-with-declaration; the exercised
             upload+read-back battery is the 22a-superior behavioral evidence.
         (3) The spec's "hash-tied" language (binding docstring) applies to the LAMBDA package
             distribution, not this leg; the upload leg's integrity control is the per-put
             content-sha256 metadata + in-run read-back compare, which the mutant control
             exercises. -->

    <group id="B6-3" status="OUT_OF_SCOPE" owner="1.0.0_SA_CTO~B" note="rides the friction-axis runner build; the runner has no friction battery yet"/>
    <!--
    IDS UNMINTED BY THE ISSUER BY DESIGN: the COO has not read the spec's acceptance rows at criterion
    grain and will not hand over invented id strings — a wrong id list validates STRUCTURALLY and
    proves the wrong thing. Enumerate each piece's set from the spec's own rows at that piece's start,
    state judgment calls, append here. Surface an ambiguous row rather than guessing.
    UNCOMPUTABLE-with-declaration is PRE-AUTHORIZED (fabric-wide, CTO 092331Z).
    Validate UNPIPED — a piped rc is the pipe's, not the validator's:
      python .tools/proof-of-spec-check.py {instance}.json --expected-criteria {that piece's ids}
    The issuance lint is a PRESENCE grep on NEW task-order files; it binds issuance PRESENCE, never
    issuance CORRECTNESS. Do not read its pass as a check of this block.
    -->
  </proof_of_spec>

  <scope>
    <files>
      <file action="modify">.tools/estate-capture.py — add an upload mode. DO NOT touch the extractor logic.</file>
      <file action="create">the device-side daily schedule (Windows Task Scheduler on the laptop)</file>
      <file action="reference">the governing spec + CTO §3a pre-rulings + CVO §3b riders</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">B6-1 UPLOAD LEG — write HUMAN + UNCLASSIFIED records to s3://opal-estate-report/text-input/{YYYY-MM-DD}/{device_id}.json. Per-device key so A PARTIAL DAY IS VISIBLY PARTIAL. IDEMPOTENT (re-run overwrites that day's device file).</requirement>
    <requirement id="2">BRONZE DISCIPLINE IS LOAD-BEARING HERE: the raw capture uploads UNTOUCHED. Character classification happens LATER at friction time, NEVER at upload. Rule 17a — doing a later layer's job early is IRREVERSIBLE, and whatever the capture carried would not be recoverable.</requirement>
    <requirement id="3">B6-2 DEVICE-SIDE DAILY SCHEDULE — the tool MUST run on the DEVICE. This is FORCED, not preferred: the transcripts are device-local and the EC2 runner structurally cannot see them. Declare the schedule in GROUP-W terms (a FLOOR, never event-only) per CTO §3a.</requirement>
    <requirement id="4">⚠ SURFACE TO ANDREW AT THE MOMENT OF CREATION, do not create it silently: B6-2 registers a RECURRING SCHEDULED JOB ON ANDREW'S LAPTOP. He directed B6 and the schedule is mandatory, so the authorization exists and you are NOT blocked — but a standing scheduled task on his personal device is his to see when it appears, not to discover later. One line to him naming the task name, the cadence and how to disable it. This fabric's cron discipline is deliberately tight; a device-level daily job is that discipline's neighbour.</requirement>
    <requirement id="5">SITE-Z IS A DECLARED GAP until the tool runs there too (already in the tool's docstring). Declare it; do not silently scope it out and do not treat one device as coverage.</requirement>
    <requirement id="6">Evidence captured AS THE WORK PROCEEDS, not retro-fitted.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">B6-1 upload mode + B6-2 schedule artifacts</deliverable>
    <deliverable type="document">A schema-valid PROOF_OF_SPEC instance per piece, passing proof-of-spec-check with --expected-criteria</deliverable>
    <deliverable type="document">Session log with Compiler Tools section + the exercised read-back evidence</deliverable>
  </deliverables>

  <do_not>
    <item>Do NOT rebuild or refactor the extractor. It is battle-tested; you are adding plumbing.</item>
    <item>Do NOT classify at upload. Raw goes up untouched.</item>
    <item>Do NOT build any alert, alarm, SNS topic, SES send, notification, freshness checker or monitor on this path, and do NOT name anything *-monitor / *-checker / *-alerter. Standing moratorium.</item>
    <item>Do NOT reconcile against the v4 layout — CTO DEFERRED it; v4 does not exist yet.</item>
    <item>Do NOT build B6-3 (the runner F3-feed wire). It is CTO~B's, behind the friction-axis runner build, and the runner has no friction battery yet.</item>
    <item>Do NOT accept an IAM verdict or an rc=0 as evidence the upload works — EXERCISE it and read the object back.</item>
    <item>Do NOT create the device schedule silently (requirement 4).</item>
    <item>Do NOT hold work on a finding and do NOT manufacture an approval step. No gate exists on this TO beyond CTO's named mechanical checks.</item>
  </do_not>
</task_order>
