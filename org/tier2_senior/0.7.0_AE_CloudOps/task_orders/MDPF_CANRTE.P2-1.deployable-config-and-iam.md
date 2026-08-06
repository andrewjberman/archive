<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-deployable-config-iam</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>staged</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Make the committed configuration deployable — `route_bindings.yaml` as a Terraform-managed S3 object with
    a content hash and an exact read grant; `partner_roster.json` as a BUILD-GENERATED, HASH-TIED copy with
    NO S3 read leg at all — plus the exact write grants `mdpf-gold-lambda` needs. Both config hashes are
    recorded in every run manifest.
  </objective>

  <context>
    ### ⛔ PHASE 2 IS NOT WRONG. IT IS OVER-BROAD BY ONE FILE. (CTO~Z ruled 213508Z)

    Doc 03 Phase 2 says to manage BOTH config objects in S3 and grant `mdpf-gold-lambda` GetObject on both.
    **For the roster that is forbidden.** `dim_mdpf_aggregate_aua_timeseries.py:1718-1746`
    `_load_partner_roster()` — *"ONE committed authority in two locations of the same file — NEVER an
    S3-read fallback and NEVER a vendored copy … FAIL-CLOSED when absent (CTO ruling 230319Z: a private copy
    of a roster value is the sect-III-e defect verbatim)"* — and its SystemExit text ends **"Do NOT add
    another resolution mechanism here."**

      `partner_roster.json`  -> BUILD-GENERATED, HASH-TIED copy. **NO GetObject leg.** 230319Z applies.
      `route_bindings.yaml`  -> Terraform-managed S3 object + content hash + GetObject leg AS WRITTEN.
                                230319Z does not reach it; Phase 2's mechanism is correct for it.

    ### WHY (a), AND IT IS NOT RULE-LAWYERING — WE MEASURED (b)'s HARM TODAY

    230319Z's target is DUPLICATE AUTHORITY — more than one thing that can answer *"what is expected-ness"*
    **and can disagree.** A build-generated hash-tied copy is ONE authority plus a derived artifact that
    **cannot drift**, regenerated and hash-recorded every build; it is candidate 1 of the existing resolver,
    unchanged, zero code edit. An S3 GetObject is **a second thing that can answer the question and can be
    changed out from under a deployed function without a deploy.**

    **AND THAT IS THIS MORNING'S MEASUREMENT, NOT A PRINCIPLE.** The deployed roster copy diverged from the
    committed authority FOR NINE DAYS on `gate_policy.per_partner_max_lag_trading_days` — a CTO ruling —
    with nothing detecting it. Non-operative only because the ruling changed prose rather than the value.
    **Option (b) rebuilds that exact divergence surface inside the Lambda, with S3 as the drift vector
    instead of a hand-upload.**

    ### ⚠ THE PACKAGING CONDITION — (a) WORKS BY ADJACENCY, AND ADJACENCY IS A BUILD FACT

    `here` is `os.path.dirname(os.path.abspath(__file__))` **OF THE RESOLVING MODULE**. Flat zip root gives
    `/var/task` and candidate 1 hits — but doc 03 Phase 1 packages a thin `lambda_function.py` PLUS
    refactored modules, so **the final layout may not be flat.**
    **THE BUILD MUST PLACE THE ROSTER ADJACENT TO THE MODULE THAT RESOLVES IT, whatever the layout is.**
    Get it wrong and it fail-closes at build — loud and recoverable, but DISCOVERED rather than DESIGNED.

    ### ⚠ OPEN AND DELIBERATELY NOT DECIDED — THE PUBLISHER'S ROSTER

    Phase 2 also grants the PUBLISHER roster read access with `ROSTER_BUCKET` / `ROSTER_KEY`. **If gold reads
    a build-generated copy and the publisher reads an S3 object, THOSE TWO CAN DISAGREE** — duplicate
    authority ACROSS components rather than within one, and gold and platinum would hold different notions
    of expected scopes.
    CTO~Z's DIRECTION (explicitly NOT a ruling): both take build-generated hash-tied copies from the same
    committed authority, each recording its roster hash in its own manifest — which makes divergence
    DETECTABLE, the precise detection absent for nine days.
    **THEY DECLINED TO RULE IT because they measured the gold spine's resolver and NOT the publisher's, and
    ruling on an unmeasured resolver is the error they corrected in themselves earlier today.**
    ⛔ **P2-1 MUST NOT SILENTLY PICK ONE.** Measure the publisher's actual roster resolution (criterion 7),
    report it, and CTO~Z rules. Name it as open in the deliverable, exactly as this TO names it here.

    Reminder from P0-5, already measured by you: the deployed publisher's env carries **NO roster variables
    at all** — the roster-completeness feature IS NOT DEPLOYED. So this is a question about what the code
    *would* do once wired, which is precisely why it needs measuring rather than assuming.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-which "how do I manage an s3 config object in terraform with a content hash"</run>
      <expect>Routes to a comp-tool or runs comp-grep/comp-glob on-rails.</expect>
      <if_mismatch>Coverage gap -> COO~Z. Third distinct gap in this program would move the
      retirement-coverage pattern into build-side territory and is worth saying so.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-iam service mdpf-gold-lambda</run>
      <expect>The TF-modeled DESIRED view of the new function's grants.</expect>
      <if_mismatch>NECESSARY, NOT SUFFICIENT — comp-iam models (action), never (action, resource), and it
      FAILS GREEN: a role holding s3:GetObject on ANY bucket reports [GRANTED] for a call to EVERY other.
      Every NEW bucket/key needs the live primitive — see criteria 4 and 5.</if_mismatch>

      <run>comp-iam gaps</run>
      <expect>No new permission gaps after the iam.tf change.</expect>
      <if_mismatch>Record each gap; treat the operation list as a FLOOR, never a deletion warrant.</if_mismatch>

    Phase 3 — after committing:
      <run>comp-blast &lt;each changed resource&gt;</run>
      <expect>Radius unchanged from the Phase 1 baseline.</expect>
      <if_mismatch>Report to COO~Z. A ZERO is a LOWER BOUND — measured false zero on mdpf_aggregate_aua.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>`data/mdpf/config/partner_roster.json` (the committed authority) and the
    build-generated zip copy derived from it</shared_resource>
    <also_in_to>P1-1 (DS~Z — refactors the module that resolves it) · P1-2 (AE~Z — the build that generates
    the copy) · P5-1 (BUILD_MANIFEST records its hash)</also_in_to>
    <last_write_owner>AE~Z owns the build generation + hash-tie; DS~Z owns the resolver</last_write_owner>
    <required_action>MCP DS~Z before finalising the zip layout — the roster must land ADJACENT to the module
    that resolves it, and only DS~Z knows the post-refactor module layout. Coordination artifact, NOT an
    approval step.</required_action>

    <shared_resource>`s3://opal-data-mdpf/code/scripts/gold/partner_roster.json` — the THIRD, live,
    hand-uploaded roster that production actually reads</shared_resource>
    <also_in_to>P4-1 (route cutover) · P6-1 (retirement)</also_in_to>
    <required_action>⛔ **IT DOES NOT DIE WITH THE ACCRUAL BRIDGE.** It is synced onto the box by
    `mdpf-daily-dispatch.sh:125` and read by the gold spine on every production run —
    `_load_partner_roster()` resolves the SYNCED copy FIRST and the committed repo file is only its
    off-runner fallback. It dies when the EC2/DISPATCH ROUTE dies, a DIFFERENT event from the
    accrual-bridge retirement. **`mdpf-gold-lambda` MUST HAVE ITS ROSTER BEFORE THE SYNC STOPS**, or the
    spine loses THE ONE SOURCE OF EXPECTED-NESS mid-cutover.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `route_bindings.yaml` IS A TERRAFORM-MANAGED S3 OBJECT WITH A CONTENT HASH, sourced from the
       committed file. Cite the resource and the hash mechanism.
       ⚠ The `config/` prefix DOES NOT EXIST — measured 21:13Z with a positive control on the same command
       shape. **THIS CREATES A PREFIX, IT DOES NOT POPULATE ONE.**

    2. `partner_roster.json` HAS NO S3 READ LEG ANYWHERE IN THE IAM. It is a build-generated, hash-tied copy.
       FORBIDDEN SHORTCUT, NAMED: do not grant `GetObject` on a roster key "for safety" or "for parity with
       route_bindings." A second thing that can answer *what is expected-ness* IS the defect 230319Z names,
       and we have this morning's nine-day measurement of what it costs.

    3. THE ROSTER LANDS ADJACENT TO THE RESOLVING MODULE IN THE BUILT ARTIFACT, and the import-health test
       EXERCISES `_load_partner_roster()` FROM THE BUILT ARTIFACT — not from the repo tree.
       FORBIDDEN SHORTCUT, NAMED: "flat zip root, so `here` is `/var/task`" is an ASSUMPTION about a layout
       Phase 1 has not finalised. Adjacency is a BUILD FACT and must be exercised, not reasoned about.

    4. WRITE GRANTS ARE RESOURCE-PINNED AND VERIFIED ON THE LIVE PRIMITIVE, not on comp-iam.
       `portal/gold/mdpf/*`, the gold-run manifest prefix, and the dated `_aggregate_aua` prefix.
       ```
       aws iam simulate-principal-policy --policy-source-arn <role> --action-names <action> --resource-arns <exact key>
       ```
       **ONE `--resource-arns` PER CALL** (2+ flips held ARNs to `implicitDeny`); **run the positive control
       as a SEPARATE invocation** (a control batched with the target is corrupted by its own presence); pass
       `--context-entries` for any conditioned statement.

    5. ACTION NAMES ARE VALIDATED WITH THE RIGHT ORACLE. `simulate-principal-policy` DOES NOT VALIDATE
       ACTION NAMES — a nonexistent action returns `implicitDeny`, byte-identical to a missing grant, so a
       TYPO sends you hunting a policy gap that does not exist. Use `aws accessanalyzer validate-policy`.

    6. BOTH CONFIG HASHES ARE RECORDED IN EVERY RUN MANIFEST — the route-bindings object hash and the
       build-generated roster hash. **THIS IS THE DETECTION THAT WAS ABSENT FOR NINE DAYS.** A run manifest
       without both hashes does not discharge this criterion.

    7. THE PUBLISHER'S ROSTER RESOLUTION IS MEASURED AND REPORTED, NOT DECIDED. Read the publisher's actual
       resolution path in code and state it. Then STOP and route to COO~Z -> CTO~Z.
       ⛔ **DO NOT WIRE `ROSTER_BUCKET`/`ROSTER_KEY` IN THIS TO.** If gold reads a build-generated copy and
       the publisher reads S3, the two can disagree and gold and platinum hold different notions of expected
       scopes — duplicate authority ACROSS components. CTO~Z declined to rule it because they had not
       measured that resolver; this criterion produces the measurement they declined to rule without.
       Third state required: the deliverable says RESOLUTION MEASURED / RULING PENDING — never a default.

    8. NO NEW ALARM, SNS TOPIC, OR MONITOR IS CREATED. Hash-in-manifest is a RECORD, not a detector.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/mdpf-pipeline/config_objects.tf</file>
      <file action="modify">infra/aws/terraform/mdpf-pipeline/iam.tf</file>
      <file action="reference">data/mdpf/config/partner_roster.json</file>
      <file action="reference">data/mdpf/config/route_bindings.yaml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">route_bindings.yaml TF-managed with a content hash; creates the `config/` prefix.</requirement>
    <requirement id="2">NO roster GetObject leg anywhere.</requirement>
    <requirement id="3">Roster adjacent to the resolving module; adjacency EXERCISED from the built artifact.</requirement>
    <requirement id="4">Write grants resource-pinned and verified on the live primitive, one ARN per call.</requirement>
    <requirement id="5">Both config hashes into every run manifest.</requirement>
    <requirement id="6">Measure the publisher's roster resolution; report, do not decide.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Terraform config objects + IAM, committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">The publisher's measured roster resolution, routed to COO~Z for CTO~Z's ruling</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT GRANT ANY S3 READ ON A partner_roster.json KEY. CTO 230319Z, re-ruled 213508Z. The measured
    cost of a second authority is this morning's nine-day silent divergence.</rule>
    <rule>DO NOT WIRE THE PUBLISHER'S ROSTER ENV VARS. Measure and route; CTO~Z rules.</rule>
    <rule>DO NOT ASSUME FLAT ZIP ROOT. Exercise adjacency from the built artifact.</rule>
    <rule>DO NOT let a comp-iam GREEN stand as verification for a new bucket/key — it models (action), never
    (action, resource), and fails green.</rule>
    <rule>DO NOT batch 2+ `--resource-arns` into one simulate call, and never run the positive control in the
    same invocation as the target.</rule>
    <rule>DO NOT use `simulate-principal-policy` to check whether an ACTION NAME is real.</rule>
    <rule>NO NEW GATES. NO SHADOWS — no second config path, no parity copy, no standing comparator.
    NO ALARMS, SNS TOPICS, SES SENDS, FRESHNESS CHECKERS, OR MONITORS.</rule>
    <rule>DO NOT stop the dispatch sync before mdpf-gold-lambda has its roster. Two independent orderings
    live in Phase 4/6 and a naive "retire the EC2" step violates both.</rule>
    <rule>DO NOT use the shared dirty checkout as build input. Never rebase on SITEZ. Commit to your lane;
    push is MSTR~Z's. Working files in the scratchpad.</rule>
    <rule>DO NOT use `--no-paginate` or `--query 'length(...)'` as evidence for an absence or a denominator.</rule>
  </do_not>
</task_order>
