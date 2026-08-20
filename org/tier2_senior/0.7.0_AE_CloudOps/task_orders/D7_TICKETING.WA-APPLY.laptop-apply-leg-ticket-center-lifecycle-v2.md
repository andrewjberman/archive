<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-d7-wa-apply</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps (the laptop apply lane per the envelope law)</issued_to>
    <date>2026-08-20</date>
    <status>staged -- ACTIVATES when the SITEZ build commit 81c502cff2 is REACHABLE FROM CLOUD HEAD (0.0.0_AB_MSTR's /integrate merge, sequenced by Andrew's word tonight: merge once BOTH fabrics are quiet; MSTR~Z merges first, MSTR merges the result, deploy-exposure ceiling enumerated before leg 2). This is an ITEM queued with zero round-trips, NOT a hold and NOT a gate (MSTR 63861: "the apply leg exists for 0.7.0 only once that lands on CLOUD"). COO GO on activation; until then 0.7.0 has nothing to do beyond knowing it is coming.</status>
    <project_code>OPAL_TICKET</project_code>
  </metadata>

  <objective>
    APPLY LEG (laptop) of D7 TICKET LIFECYCLE v2 (W-A): land on the executing plane what
    0.5.0_AE_OpalETL~Z BUILT on SITEZ @81c502cff2 ("BUILD ONLY -- the apply leg is the laptop's
    per the envelope law"): infra/aws/lambda/ticket_center/lambda_function.py (+178: native
    lifecycle analytics + claim enrichment + the Andrew-direct day-one field set) and
    infra/aws/terraform/ticket-center/main.tf (+35: incl. the WA-6 grant -- dynamodb:GetItem on
    opal-users-v2 for opal-ticket-api-role, measured implicitDeny today on the live primitive,
    one --resource-arns per call + separate positive control). Terraform is the ONLY deploy
    mechanism (Deployment Rules 1-6): commit before apply -> safe-apply plan with expected rows
    enumerated -> apply -> 0-diff -> tag; deploy-completion ledger opened at start and closed
    in-session (a begun deploy FINISHES or rolls back + escalates).
  </objective>

  <context>
    Builder's record: 81c502cff2 (0.5.0_AE_OpalETL~Z) + D7_TICKETING.WA_RULE24_SCHEMA_RECORD.md
    (+116, the day-one field set's Rule-24 record). The sequencing is MSTR's and Andrew's, not
    this TO's: CLOUD +174 / SITEZ +56 since base d99006fe93, overlap 1 (org/projects/REGISTRY.md),
    merge-tree clean; both fabrics read NOT-QUIET at 2145Z. Do NOT reach for SITEZ directly --
    the files exist for this lane only once they are on CLOUD. THE ENVELOPE LAW'S TWO-PLANE READ
    binds at apply time: DESIRED (the TF plan) AND APPLIED (the live IAM primitive after apply);
    and CODE per Rule 22a: the deployed package bytes are diffed against the source they are built
    FROM at 81c502cff2, resolved through the source-map entry / package manifest, never by
    filename. Shared-file note from the W-E TO (site Z): lambda_function.py is SHARED with W-A
    (lands FIRST), W-C(b), W-D and later W-E's emit leg -- this apply establishes the base the
    others rebase onto.
  </context>

  <compiler_tools_mandate>
    Phase 1 (activation check + ground-read): `git merge-base --is-ancestor 81c502cff2 HEAD` on
    CLOUD (rc=0 = activated); comp-blast on the ticket_center Lambda; comp-iam service on it as
    the FLOOR (Rule 22a: comp-iam models (action), never (action, resource) -- the new table grant
    is verified on the live primitive only); source-map entry current for the Lambda (Rule 4 --
    the map pairs the Lambda with its repo dir; it is NOT a bytes comparator).
    Phase 2 (apply): `.tools/safe-apply.sh` with the expected plan rows ENUMERATED before apply
    (the +35 main.tf delta = the WA-6 grant + whatever else the diff shows, row by row; any row
    beyond the enumerated set = STOP and surface); 0-diff re-plan after apply; tag
    `ticket-center-v{X.Y.Z}` (push rides MSTR's integration window -- GATE 5 blocks non-MSTR
    pushes to CLOUD; say so in the proof rather than claiming a push).
    Phase 3 (two-plane + code + exercised): APPLIED -- `aws iam simulate-principal-policy
    --policy-source-arn <opal-ticket-api-role ARN> --action-names dynamodb:GetItem
    --resource-arns <opal-users-v2 table ARN>` -> allowed, ONE --resource-arns per call, the
    NEGATIVE control (a different table ARN -> implicitDeny) as a SEPARATE invocation, plus
    `get-role-policy` for the applied document; CODE -- deployed package sha vs the built-from
    source at 81c502cff2 via the source-map entry (22a CODE layer); EXERCISED -- one real claim
    enrichment resolving {name,user_id} server-side on a claimed ticket (ad-hoc QA read through
    the scoped API; coordinate the fixture with 0.5.0_AE_OpalETL~Z by MCP -- its artifacts are
    QA evidence, never production evidence).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - 0.0.0_AB_MSTR / 0.0.0_AB_MSTR~Z: the /integrate merge is the activation event; the
      deploy-exposure ceiling they enumerate before leg 2 is read BEFORE Phase 2.
    - 0.5.0_AE_OpalETL~Z: builder; WA-6 finding + the exercise fixture; their TO's own
      acceptance (WA-*) closes at site Z on YOUR apply evidence -- send them the proof pointer.
    - 1.0.0_SA_CTO / 1.0.0_SA_CTO~Z: arch acceptance of the D7 v2 shape is theirs; the apply is
      mechanics. 2.0.0_SA_COO~Z: validation of the W-A TO at site Z; cc on close.
    - Shared file lambda_function.py: W-C(b)/W-D/W-E rebase onto this landing -- state the
      landed sha in the close so the next lane resolves against it.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is the APPLY LEG as cut -- A1 activation, A2 chain,
    A3 plan discipline, A4 applied IAM, A5 code layer, A6 exercised, A7 ledger + proof; exhaustive
    over the leg; the build, the merge sequencing, and the W-E emit leg are OUTSIDE.)
    A1  ACTIVATION EVIDENCED: 81c502cff2 reachable from CLOUD HEAD (command + rc printed); the
        deploy-exposure ceiling from MSTR read and cited.
    A2  CHAIN HONORED: code -> TF -> source map current -> commit -> plan -> apply -> 0-diff -> tag
        (push status stated truthfully under GATE 5).
    A3  PLAN DISCIPLINE: expected rows enumerated BEFORE apply; applied set == enumerated set; any
        surplus row = STOP (the flip path stated, exercised or explicitly zero).
    A4  APPLIED IAM: simulate-principal-policy allowed on the exact opal-users-v2 ARN (one
        --resource-arns), negative control implicitDeny in a SEPARATE invocation, get-role-policy
        document cited -- WA-6 closed on the live primitive, not on the plan.
    A5  CODE LAYER: deployed package sha == built-from source at 81c502cff2 via the source-map
        entry (never by filename); the env/config the code expects is present on the deployed
        function (the 08-12 class: a grant to a code path that does not exist verifies perfectly).
    A6  EXERCISED: one real claim enrichment resolves {name,user_id} server-side (ad-hoc QA read,
        labelled as such); the 201 contract, the client ack frame and the 5-min runner's buzz
        unchanged (the live-production no-regression rider from the site-Z TOs).
    A7  Deploy-completion ledger opened at start, closed in-session; proof instance VALID rc=0
        positional A1-A7; RAVC close to COO, cc 0.0.0_AB_MSTR + 0.5.0_AE_OpalETL~Z + 1.0.0_SA_CTO +
        2.0.0_SA_COO~Z.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>A1,A2,A3,A4,A5,A6,A7</expected_criteria>
    <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D7_TICKETING.WA-APPLY_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Do not start before COO's GO (activation = the merge on CLOUD). Normal cadence. Terraform only; never update-function-code; never console. HALTGT checkpoint per safe-apply (nobody cites a HALTGT pass as evidence). Surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
