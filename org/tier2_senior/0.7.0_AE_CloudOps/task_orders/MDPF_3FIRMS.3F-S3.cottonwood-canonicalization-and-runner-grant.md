<task_order>
<id>MDPF_3FIRMS.3F-S3</id>
<title>Cottonwood silver canonicalization + the MDPF runner's additive IAM grant (Rule 22a verification mandatory)</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-S (Silver)</workstream>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<joint_assignee>0.4.0_DS_ClientPlatform (canonicalization determination + exercised-read validation)</joint_assignee>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:24Z</issued_at>
<status>complete</status>
<!-- 20260722T2108Z AC-4 CLOSED JOINTLY + TO COMPLETE (0.7.0_AE + 0.4.0_DS):
     EXERCISED runner-role read (behavioral proof, not simulate): SSM adc0f11f-0001-4111-835e on
     i-02448edb624a7a7cf under the Andrew-cleared lifecycle (chain: CTO GO 210124Z [evidence] ->
     withdrawal 210234Z [freeze held] -> Andrew conditional clearance ~2103Z at COO terminal,
     condition-1 idle MET -> CTO re-issue 210350Z [re-stop]; found parked state RESTORED, verified
     stopped). Output: caller_arn=assumed-role/mdpf-daily-runner-ec2-role/i-02448edb624a7a7cf,
     fact_holdings date=2026-07-20 rows=16762 cols=24 verdict=ROWS-RETURNED.
     DS INDEPENDENT VALIDATION (msg 210720Z): 4 limbs -- identity, rows/cols == authoring-side read,
     object ETag a6ea4428/388478B == head-object same-minute, script ETag c2473364 == staging receipt.
     Record: AE msg 210554Z + DS msg 210720Z. CTO acceptance 210550Z.
     dim_model_portfolio exercise stays sequenced to first G8/G3 population (granted + simulated;
     rows impossible until populated -- not a blocker, a sequence). -->

<!-- 20260722T2052Z 0.7.0_AE_CloudOps: RF-10 found HALF-STALE at live state (cottonwood half landed
     1746Z pre-hold under Andrew carve-out); CTO 203928Z narrowed scope to the gold/dim_model_portfolio/*
     pure-add and issued CONDITIONAL APPLY GO. Grant APPLIED + verified (ledger 20260722T2041Z closed 7/7,
     tag mdpf-pipeline-v1.8.0). OUTSTANDING: AC-4 exercised runner-role read (DS thread open 204804Z;
     cottonwood at next natural pass, dim_model_portfolio after first population) + AC-6 canonicalization
     determination (joint with DS, process proposed). -->
<!-- 20260722T2057Z AC-6 DETERMINATION RECORDED (joint, explicit, per scope (a)):
     **fact_holdings IS CANONICAL for the Cottonwood AUA total; fact_holdings_s2 is NOT a holdings
     table** -- it is the BD vendor 'Timestamps' sheet landed as section 2.
     DS half (0.4.0_DS msg 20260722T205453Z): empirical reads @repo 61365878d, partition date=2026-07-20
     -- fact_holdings 16,762 rows x 24 cols (= the verified $458,114,003.10 / 913-account universe);
     fact_holdings_s2 5 rows x 7 cols key-value (Created (Eastern) / Template Name=Assets_Dim / dates).
     AE half (0.7.0_AE, this session): mechanism SOURCE-CONFIRMED -- mirror_schemas.py TIMESTAMPS_SECTION
     ("The BD vendor 'Timestamps' sheet (present in EVERY cottonwood xlsx)... Lands as section 2:
     fact_{feed}_s2") @HEAD 61365878d; artifact corroboration list-objects-v2 date=2026-07-20:
     fact_holdings 388,478 B vs fact_holdings_s2 4,565 B.
     CONSEQUENCES: (a) live builder reading fact_holdings is CORRECT AS-IS -- no read-path change, 3F-G3
     hazard clause moot on this point; (b) PRD sect-1.2 COT row naming _s2 as total_aua source is a TEXT
     DEFECT (schwab pattern-match; _s{N} is mechanical per-section, semantics differ per vendor) -- PRD
     amendment routed to CTO via COO (DS report @58d24b18e); (c) landing _s2 remains CORRECT Rule-17
     behavior (never-drop-a-sheet). AC-6 CLOSED. -->


<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z -> COO decomposition.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §4 WS-S row 3F-S3; §2.5 RF-10; §3.1; §8.8</ref>
</references>

<read_this_first priority="BLOCKING">
⛔⛔ **BEFORE ANY `safe-apply`, ANY TERRAFORM, OR ANY DEPLOY ACTION: READ YOUR INBOX ROOT.**
A `[STOP]`-prefixed message from `1.0.0_SA_CTO` (~20:27Z) sits UNREAD there. It **WITHDRAWS**: your WS-5
TF apply GO, Andrew's 1425Z D2 GO, and CTO's own prior outstanding direction to you — all under LD-0333,
the sovereign fabric hold.

**DO NOT ASSUME THE HALTGT CHECKPOINT CAUGHT YOU.** CTO's own finding: the checkpoint blocked only
because your session was dead and nothing drained your inbox. **Once your watcher arms, that block
evaporates** — it was an accident of your death, not a control. He recorded it as such explicitly.

**A GO YOU CARRIED INTO THIS SESSION IS A MESSAGE, NOT AN AUTHORIZATION.** Re-read the durable carrier
at fire time. Under LD-0333 the ONLY authorization path is Andrew -> CTO -> cascade.
</read_this_first>

<scope>
(a) **CANONICALIZATION DETERMINATION (with DS):** confirm whether `fact_holdings_s2` or `fact_holdings`
    is canonical for the Cottonwood AUA total. PRD §3.1 answers the architectural half — **silver IS the
    canonical source for the firm total**. But the live builder reads `fact_holdings` (raw vendor
    headers) while `_s2` exists over the same date range. ⚠ **This is an OPEN S4 determination — decide
    it explicitly and record why. NOT silently either.**
(b) **THE GRANT (yours):** the MDPF runner currently **CANNOT READ** `blackdiamond/cottonwood/silver/*`
    — its IAM grant enumerates five ARNs and Cottonwood is absent. Apply the **ADDITIVE two-statement**
    fix for `blackdiamond/cottonwood/silver/*` and `gold/dim_model_portfolio/*`.

**ADDITIVE ONLY.** New-territory rule: pure adds. A TF plan that is not pure "to add" is out of scope —
stop and surface rather than modifying an existing statement.
</scope>

<rule_22a_mandate priority="BLOCKING">
⚠ **`comp-iam` IS NOT SUFFICIENT HERE AND IT FAILS *GREEN*.** It models `(action)`, never
`(action, resource)` — **a role holding `s3:GetObject` on ANY bucket reports `[GRANTED]` for a call to
EVERY other one.** This is a NEW prefix for this role, so comp-iam will report GREEN whether or not the
grant exists.

**THE LIVE PRIMITIVE, AND THE INSTRUMENT HAS TWO INDEPENDENT FALSE-DENY MODES:**
```
aws iam simulate-principal-policy --policy-source-arn <runner role> \
    --action-names s3:GetObject --resource-arns <ONE exact key>
```
1. **A call carrying 2+ `--resource-arns` flips the HELD ones to `implicitDeny`.** -> **ONE
   `--resource-arns` PER CALL.**
2. **It EVALUATES `Condition` blocks**, so with no `--context-entries` a conditioned statement returns
   `implicitDeny` **byte-identical to a real deny**. -> pass `--context-entries` for any conditioned
   statement.

⛔ **RUN THE POSITIVE CONTROL AS A SEPARATE INVOCATION.** *A positive control is only a control if it is
run in isolation from the target* — mode (1) silently disarms the very control this rule leans on.

⛔ **DESIRED IS NOT APPLIED.** `comp-iam`'s default view parses Terraform — it cannot tell landed from
planned. Ground the final state on live `aws iam get-role-policy`.
⛔ **AND CONFIG-READ IS NOT BEHAVIOR.** The claim "the runner can read Cottonwood" is a BEHAVIORAL claim
and must be **EXERCISED**: a real read from the runner role returning rows. A policy document is not a
successful read.
</rule_22a_mandate>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam service &lt;mdpf runner&gt;  AND  comp-iam gaps</run>
      <expect>The TF-DESIRED view of the runner's grants; Cottonwood ARNs absent pre-change.</expect>
      <if_mismatch>Remember this view is DESIRED-only and fails GREEN on resources. It is a starting map, never the verdict.</if_mismatch>
    </step>
    <step>
      <run>aws iam get-role-policy --role-name &lt;runner role&gt; --policy-name &lt;policy&gt;</run>
      <expect>APPLIED truth pre-change: five ARNs, Cottonwood absent — confirming RF-10 at live state.</expect>
      <if_mismatch>If Cottonwood is already present, RF-10 is stale — STOP and report rather than applying a redundant grant.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on the runner + the IAM root before changes</run>
      <expect>Blast radius enumerated; no unexpected consumers.</expect>
      <if_mismatch>Document any new consumer and MCP its owner before applying.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/safe-apply.sh with a `-target`ed, NAMED plan; deploy-completion ledger OPENED first</run>
      <expect>Plan is PURE ADD (two statements). 0-diff after apply. Ledger entry open in org/critical_paths/change_management/.</expect>
      <if_mismatch>⛔ A plan that is not pure-add is OUT OF SCOPE — stop and surface. ⛔ Never bare `terraform apply`. ⛔ NEVER#5: a begun deploy FINISHES in-session or rolls back loud.</if_mismatch>
    </step>
    <step>
      <run>simulate-principal-policy — ONE --resource-arns, target key</run>
      <expect>allowed for s3:GetObject on the exact Cottonwood silver key.</expect>
      <if_mismatch>implicitDeny may be a FALSE deny from a Condition block — re-run with --context-entries before concluding the grant failed.</if_mismatch>
    </step>
    <step>
      <run>simulate-principal-policy — POSITIVE CONTROL, SEPARATE INVOCATION, one --resource-arns</run>
      <expect>A known-held ARN returns allowed, proving the instrument discriminates.</expect>
      <if_mismatch>If the control fails, the instrument is lying — do NOT record any verdict from the target call.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>EXERCISE: a real read from the RUNNER ROLE against blackdiamond/cottonwood/silver/* and gold/dim_model_portfolio/*</run>
      <expect>Rows returned. This is the only acceptable proof of the behavioral claim.</expect>
      <if_mismatch>A passing simulate with a failing read means the grant is not effective. The exercised read binds, not the config.</if_mismatch>
    </step>
    <step>
      <run>aws iam get-role-policy (post-apply) + close the deploy ledger</run>
      <expect>APPLIED state carries both new statements; ledger CLOSED in-session.</expect>
      <if_mismatch>An unclosed ledger at session end = COO alarm (NEVER#5).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>An IAM grant changes ACCESS, not data. No converter logic changes and no
  historical partition is affected. The canonicalization determination, if it changes which table the
  builder reads, is a GOLD-side change owned by 3F-G3 — not executed here.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="MDPF runner IAM role" shared_with="0.6.2_AE_PartnerETL~A (3F-S1 TF half)">
    Both TOs touch Terraform for the same runtime family. Coordinate applies — never two concurrent
    applies in one root.
  </resource>
  <resource path="fact_holdings vs fact_holdings_s2 canonical determination" shared_with="0.4.0_DS_ClientPlatform (3F-S2, 3F-G3)">
    DS owns the determination half and the downstream builder. Do not decide it unilaterally.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency type="authorization" name="LD-0333 fabric hold" status="active" blocking="true">
    Under the sovereign hold, an apply requires authorization cascaded from CTO. Your pre-hold GOs are
    WITHDRAWN. Confirm with CTO at fire time.
  </dependency>
</dependencies>

<acceptance_criteria>
1. The `[STOP]` message at your inbox root is READ and ACKed **before any apply action**.
2. Grant applied via `safe-apply` (`-target`ed, named, PURE ADD), 0-diff verified, deploy ledger opened
   AND closed in-session.
3. `simulate-principal-policy` PASS on the exact ARNs — **ONE `--resource-arns` per call** — plus an
   **isolated** positive control run as a SEPARATE invocation.
4. **An EXERCISED read from the runner role returns rows** (behavioral proof, not config).
5. Post-apply `get-role-policy` confirms APPLIED state (desired != applied).
6. The `fact_holdings` vs `_s2` canonical determination is made EXPLICITLY with DS and recorded with
   reasoning — not left silently either.
7. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>Report to 2.0.0_SA_COO; CTO gates the apply. Escalate immediately if the plan is not pure-add.</escalation>
</task_order>
