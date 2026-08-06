<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-ec2-code-capture</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>staged</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Capture, before any irreversible act, the complete on-disk MDPF code and installed dependency state of
    EC2 `i-02448edb624a7a7cf`, and produce the FILESYSTEM-DERIVED DENOMINATOR that Andrew's port-completeness
    condition is discharged against. This TO produces evidence only; it deletes and terminates nothing.
  </objective>

  <context>
    Andrew-direct 2026-08-06 @c801ec9d5, VERBATIM: "Teardown is fine just need to make sure any necessary
    code on that ec2 is properly ported to the lambda." Termination of the instance and its EBS is
    AUTHORIZED, conditioned on port-completeness.

    CTO~Z classification @70733b907 places this item in Class A'' — ORDERING-CRITICAL — for one reason:
    THE ACT H4 AUTHORIZES DESTROYS THE EVIDENCE THAT DISCHARGES ITS OWN CONDITION. Terminate first and
    "was all necessary code ported?" becomes permanently unanswerable, not merely unanswered.

    The hazard is measured, not hypothetical:
    - `02_NEEDED_VS_NOT_AUDIT.md` names the miss directly — "any EC2 script not directly visible in Stage 6
      but used as a library or imported source." The dispatch script enumerates TEN STAGES; imports are
      enumerated nowhere.
    - The EC2 RUNTIME-INSTALLS PACKAGES, so the authoritative record of which versions actually ran exists
      ONLY on that instance's disk. Terminating destroys the reproducibility baseline for H5.
    - `01` s.10 + H8 establish repo-vs-deployed divergence as this estate's demonstrated norm. "The repo is
      the same as the box" is precisely the assumption that has already failed here.

    Confirmed instance of that divergence, from DS~Z: `pandas_market_calendars` is required by the MDPF
    calendar shim, is absent from `requirements.txt`, and is guaranteed TODAY only by
    `mdpf-daily-dispatch.sh:183-189` and `user-data.sh:49` running `pip install "pandas_market_calendars<5"`.
    The `<5` pin is load-bearing (5.x changed the API) and exists nowhere in the repo but a bash line inside
    the file this port retires. PART OF THIS PIPELINE'S RUNTIME EXISTS IN NO COMMIT.

    THIS TO IS RANKED FIRST IN THE PROGRAM. Its output is a Phase 1 INPUT: the enumeration SCOPES the port
    rather than auditing one already built and cut over. DS~Z's static import graph (P0-4) must be built over
    the CAPTURED closure, not the repo closure — a repo-source graph inherits the very divergence it exists
    to detect. So P0-4's graph half is gated on this TO's artifact landing.

    NOT A GATE. This is a correctness condition the sovereign attached to his own authorization. Nobody
    clears it; you discharge it with evidence. If anyone proposes an approval checkpoint around it, refuse.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-which "how do I inventory code and installed packages on an EC2 instance"</run>
      <expect>Routes to a comp-tool or runs comp-grep/comp-glob on-rails. Never a dead end.</expect>
      <if_mismatch>A repeat override for one intent is a COVERAGE GAP, not an inconvenience — report it to
      COO~Z and it becomes a tool request (Rule 21).</if_mismatch>

      <run>comp-estate --resource i-02448edb624a7a7cf</run>
      <expect>The EC2's place in the MDPF thread: producers, served outputs, owning tool. Record the
      provenance header — KEYS are re-derived live, NAMES come from a snapshot the tool declares stale past
      14d.</expect>
      <if_mismatch>UNKNOWN or a stale snapshot header: `--refresh` before trusting a thread NAME. Do not
      treat a NAME miss as an absent resource.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-iam service mdpf-daily-trigger</run>
      <expect>Orientation only for the SSM/EC2 route you will be reading.</expect>
      <if_mismatch>Note gaps in the log; NECESSARY NOT SUFFICIENT — comp-iam models (action), never
      (action, resource), and it FAILS GREEN.</if_mismatch>

    Phase 3 — after committing:
      <run>comp-blast mdpf_aggregate_aua</run>
      <expect>Radius unchanged from the c801ec9d5 baseline recorded by COO~Z.</expect>
      <if_mismatch>Report to COO~Z. NOTE the recorded false zero — see acceptance criterion 7.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>The captured closure artifact in S3 (this TO's output)</shared_resource>
    <also_in_to>P0-4 (0.4.0_DS_ClientPlatform~Z — builds the static import graph OVER this artifact) ·
    P1-2 (AE~Z package) · P6-0 (three-bucket discharge, consumes this denominator)</also_in_to>
    <last_write_owner>0.7.0_AE_CloudOps~Z</last_write_owner>
    <required_action>MCP 0.4.0_DS_ClientPlatform~Z AND 2.0.0_SA_COO~Z the moment the artifact lands, with
    its exact S3 URI and the denominator N. DS~Z's P0-4 graph half is waiting on it. This is a
    notification, NOT an approval step — nobody blesses your artifact.</required_action>

    <shared_resource>EC2 i-02448edb624a7a7cf (read-only in this TO)</shared_resource>
    <also_in_to>P6-1 (retirement + teardown)</also_in_to>
    <required_action>THIS TO DOES NOT STOP, DETACH, TERMINATE, OR MODIFY THE INSTANCE. Read and snapshot
    only. Stopping EC2 is on CLAUDE.md's human-confirmation list independently of H4.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. AN EBS SNAPSHOT OF THE INSTANCE'S VOLUME(S) EXISTS AND IS COMPLETED, AND IT WAS TAKEN BEFORE ANY
       ENUMERATION. Cite snapshot ID(s), volume ID(s), and `State=completed` from `describe-snapshots`.
       WHY FIRST AND WHY NON-NEGOTIABLE: an enumerated capture CAN MISS A FILE — that is the stated hazard
       (the "library or imported source" miss). A SNAPSHOT DOES NOT ENUMERATE, SO IT CANNOT MISS. The
       inventory is what you reason from; the snapshot is what makes an enumeration error RECOVERABLE
       INSTEAD OF TERMINAL. It costs pennies and is fully inside the granted authorization.
       FORBIDDEN SHORTCUT, NAMED: do not substitute "I inventoried carefully" for the snapshot. Care is not
       a control.

    2. THE DENOMINATOR IS STATED AND IT COMES FROM THE FILESYSTEM, NOT FROM THE DISPATCH SCRIPT'S STAGE
       LIST. Report N = every `.py` under the MDPF tree on the box, plus the installed-package manifest.
       FORBIDDEN SHORTCUT, NAMED: "ten stages" is the number that HIDES the hazard — the dispatch script
       enumerates stages, not imports. A denominator derived from the stage list is REJECTED.
       State the enumeration root(s) and the command that produced N.

    3. Every file in the denominator is preserved to S3 with a recorded sha256. Cite the S3 prefix and a
       manifest mapping on-box path -> S3 key -> sha256. Capture goes EC2 -> S3 per deploy Rule 12:
       NEVER write code on the VM, NEVER inline Python in SSM.

    4. THE INSTALLED DEPENDENCY STATE IS CAPTURED AS RESOLVED FACT, NOT AS INTENT. `pip freeze` (or
       equivalent site-packages resolution) from the actual interpreter the MDPF chain uses, preserved to
       S3. Must include the RESOLVED VERSION of `pandas_market_calendars`.
       FORBIDDEN SHORTCUT, NAMED: `requirements.txt` is NOT the dependency state — it does not contain
       `pandas_market_calendars` at all. A capture citing the repo requirements file has captured nothing.

    5. WHICH INTERPRETER, stated and grounded: the python version and path the MDPF chain actually executes
       under on the box, with the command that showed it. This is H5's reproducibility baseline and it is
       destroyed by termination.

    6. THIRD STATE PRESENT. Any file that cannot be read (permissions, mount, transient) is recorded as
       UNREADABLE with the error, and counted in the denominator. UNREADABLE != ABSENT and UNREADABLE !=
       CAPTURED. A capture reporting 100% success with no unreadable class must show the check that would
       have detected one.

    7. NO CLAIM IN THIS TO RESTS ON A GRAPH EDGE COUNT. MEASURED 2026-08-06 at c801ec9d5 on a fresh DB
       (age 0.0h, Nessie HEAD current): `comp-blast mdpf_aggregate_aua` returned "No downstream consumers
       found (no EXTRACTED edge -- NOT provably zero)" for an artifact with FOUR verified consumers
       (@ad76ad830, 439 partitions content-verified). Graph edges are a LOWER BOUND.

    8. RESERVED WORDS. This TO's deliverable may NOT use "proof / provably / definitively / complete" about
       the capture's coverage. It may assert: "N files enumerated from <root> by <command>, all preserved,
       plus an EBS snapshot that does not depend on enumeration." That is the strongest true claim.

    9. THE INSTANCE IS UNCHANGED. Confirm instance state and volume attachments are identical before and
       after. This TO stops, detaches, terminates and modifies NOTHING.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_EC2_CAPTURE_20260806/manifest.json</file>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_EC2_CAPTURE_20260806/README.md</file>
      <file action="reference">infra/aws/ec2/mdpf-daily-dispatch.sh</file>
      <file action="reference">infra/aws/ec2/user-data.sh</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">EBS snapshot FIRST, before enumeration. Non-enumerating by design.</requirement>
    <requirement id="2">Enumerate from the FILESYSTEM. Record the root and the command.</requirement>
    <requirement id="3">Preserve to S3 per Rule 12. Never write code on the VM; never inline Python in SSM.</requirement>
    <requirement id="4">Capture resolved installed packages incl. the pandas_market_calendars version.</requirement>
    <requirement id="5">Record the interpreter version and path actually used by the chain.</requirement>
    <requirement id="6">Notify DS~Z + COO~Z with the S3 URI and N the moment it lands.</requirement>
    <requirement id="7">Read-only against the instance. No stop, no detach, no terminate, no modify.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Capture manifest + README under your deliverables folder, committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="artifact">The captured closure + dependency state in S3, URI recorded in the manifest</deliverable>
    <deliverable type="artifact">EBS snapshot ID(s), State=completed</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT STOP, DETACH, TERMINATE, OR MODIFY i-02448edb624a7a7cf in this TO. Read and snapshot only.
    Teardown is a separate TO (P6-1) and runs only after the P6-0 discharge.</rule>
    <rule>DO NOT DELETE ANY S3 OBJECT. H13 is OPEN — S3 deletion still sits on CLAUDE.md's
    human-confirmation list and Andrew's teardown word did NOT authorize it. S3 versioning is load-bearing
    for rollback.</rule>
    <rule>DO NOT derive the denominator from the dispatch script's ten stages. Filesystem only.</rule>
    <rule>DO NOT treat an import-health pass as evidence a dependency is present. `pandas_market_calendars`
    is imported inside a try/except ImportError — ABSENCE DOES NOT RAISE, so import-health PASSES with the
    package missing. The check cannot fail in the state it exists to detect.</rule>
    <rule>NO NEW GATES. No approval step, co-sign, GO requirement, or review hold — including around the
    port-completeness condition. Mechanical rails (safe-commit, safe-apply, safe-deploy, owned-paths) are
    pre-existing and untouched.</rule>
    <rule>NO SHADOWS. No parallel producer, no shadow/parity/comparator prefix, no standing comparator.</rule>
    <rule>NO ALARMS, SNS TOPICS, SES SENDS, FRESHNESS CHECKERS, OR MONITORS. Standing moratorium.</rule>
    <rule>DO NOT use the shared dirty checkout as build input. Never `git rebase` / `git pull --rebase` on
    SITEZ. Commit to your lane; push is MSTR~Z's. Working files in the scratchpad — the shared tree loses
    uncommitted work and `git stash` is prohibited here.</rule>
    <rule>DO NOT cite an `aws s3 ls` timestamp as evidence for any landing-time claim — it prints LOCAL
    time while s3api returns true UTC, and the two disagree SILENTLY. Cite the s3api ISO-8601 value with
    its +00:00.</rule>
  </do_not>
</task_order>
