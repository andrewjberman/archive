<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R18-REL.ticket-service-release-meeting-route-attachment-routes-and-permission</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-14</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>18</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R18.md</decomp_doc> (round 18): cells `R18-mt-4` and `R18-tf-5`, ONE release.
<owned_cells>R18-mt-4 R18-tf-5</owned_cells>
</decomp_ref>

  <objective>
    Release the ticket service so the Meeting Request outcome route, the two trade-form attachment routes, the coordinator's routing, the two attachment
    environment variables and the S3 permission on the three firm prefixes are LIVE together: build the `opal-ticket-api` package from the merged tree,
    `safe-apply` the Terraform source, and read every part back. STAGED: it starts only on the issuer's GO, which names a signed never-widen pair.
  </objective>

  <context>
    **The pair is your whole procedure.** The issuer writes it after the worker orders `TO-R18-L1`, `L2`, `TR1`, `TR2`, `TR3` are merged, at
    `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_REL/R18_REL_PAIR.md`, and the CTO signs its half. It names the merge commit you
    build from (`built_from_sha`), the expected Terraform plan (3 new route resources, two Lambda environment variables, the `ROUTING_MATRIX`
    value, one IAM statement `TicketAttachmentsTradeForm`, nothing else), the rollback per key, and the laptop's role request for the bucket policy and
    CORS, which must be DONE before you apply (C-DEPLOY: a Dell writes no bucket policy). You do NOT start without the GO.
    Read first when the GO comes: the pair; `deliverables/0.9.0_WK_TCKT_VNEXT~43/ATTACH_ADDRESS.json` (the per-firm buckets, the bucket template and the key template, builder output);
    the wire contract (`decompositions/TCKT_VNEXT_DECOMP_R18.md`, section WIRE CONTRACT); and the build procedure of the earlier ticket release
    (`org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-y-320*.md`, the BUILD of the package that carries the owner check), which is the model for building
    the zip and comparing it with the live package member by member.
    **Ordering with the other release of the same Lambda:** `2.0.0_SA_COO~Y2` owns a release pair for `opal-ticket-api` (the owner check, AR-y-316/320). Before you build, read
    the live `CodeSha256` against the tree's build and read `org/critical_paths/.open_deploys/` in EVERY live worktree. If an open entry names `opal-ticket-api`, or the live
    code is not what the tree's HEAD minus this round builds, STOP and report to the issuer; the two releases are then ordered or merged by the issuer, never raced.
  </context>

  <go>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-16 ~16:5xZ; gate limb: none graded this modification; it narrows and names the GO, no placeholder, no path widened). CONDITIONAL GO. THE PAIR IS NOW the COMBINED pair (it supersedes `R18_REL/R18_REL_PAIR.md`, which is VOID: it bound a `lambda_function.py` blob round 19 changed): COO half in `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_REL/R18_R19_COMBINED_REL_PAIR.md` (git blob `643ba43746582b1a50c91923a58a23b9a7979715`, sha256 `fc1bf170a8a42d2b0e02679d581e7268ea153b132b7f3b650005bb245e60589b`; @c2802ebfb2), CTO half in `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/R18_R19_COMBINED_REL_PAIR_CTO_HALF.md` (git blob `2f52cca81d01d28bae2b4637a5f6a2463148560b`, @6bdc8ef4f4, msg 9624). `built_from_sha` = `de2fdb4a4f01520fd166dca8abb21f4541446f47` (its `lambda_function.py` blob is `501c46097813`, its `main.tf` blob `748e680fd7f8`). BEFORE STEP 1 measure with `git hash-object` the pair's two files above and the six files of the pair's section 1 (`lambda_function.py`, `main.tf`, `ATTACH_ADDRESS.json`, `r18_rel_check.py`, `r19_rel_check.py`, `r19_mig_check.py`) at the working tree you build from and at `built_from_sha`; any difference is a STOP and no GO. ONE APPLY carries both rounds: `TO-R19-REL` is folded into this apply (it gets its own result file and check from the SAME apply, never a second apply). The pair's sections 3 and 4 are your preconditions and expected plan (precondition 2 needs `python .../r19_mig_check.py` printing `MIG-OK` and `R19_MIG_RESULT.json` present; precondition 3.1 reads the three buckets as the pair's corrected wording says: the bucket Allow carries `s3:GetObject` only and `s3:PutObject` comes from this release's identity statement, so a missing bucket Allow for PutObject is NOT a STOP). THE CTO'S THREE CONDITIONS bind: (1) the after-read after `TO-R18-RUN` is zero `WE_CLIENT_SENT` AND at least one `WE_CLIENT_NO_CONTACT` with the events scanned printed (the issuer reads it; you record the apply-end timestamp it reads from); (2) your receipt carries this sentence VERBATIM: "requester ack and pickup notices are off until the firm contact map is set"; (3) a rollback goes RELEASE first, then markers. Results: `R18_REL_RESULT.json` (as below) AND `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r19_rel/R19_REL_RESULT.json` (the same hashes in each); both checks (`r18_rel_check.py`, `r19_rel_check.py`) must print `REL-OK` before the ledger closes.
    The GO's other steps are unchanged:
    1. STEP 0: open the NEVER-2 ledger entry (`deploy_ledger.py open`, leg per step below) and keep it open until the read-backs pass.
    2. STEP 1: build the package from `built_from_sha`; print its member list and sha256; compare with the live package; the members that differ must be exactly the ticket Lambda's source.
    3. STEP 2: confirm the laptop's bucket policy and CORS exist (read-only `get-bucket-policy`, `get-bucket-cors` on EACH of the three firm buckets of `ATTACH_ADDRESS.json`); any one absent: STOP. Read the statements' PREFIX too: it must be `portal/<firm>/state/ticket_attachments/trade-form/` (snake_case); a bucket policy built from the earlier kebab-case rows (`ticket-attachments`, which existed for a short window in exemptions.json on box/dell1) is a STOP, whatever else reads correct.
    4. STEP 3: `safe-apply` plan only; print the plan summary; it must equal the pair's expected plan exactly or STOP.
    5. STEP 4: apply under `safe-apply`, upload the package as the pair says, wait for the function to be `Active`/`Successful`.
    6. STEP 5: read back; run the issuer's check (the criterion). Close the ledger entry only after it prints REL-OK.
    7. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r18_rel/R18_REL_RESULT.json` with the keys `built_from_sha`, `package_sha256`, `code_sha256_before`, `code_sha256_after`
       (the Lambda's base64 CodeSha256 values), `plan_summary`, `change_ledger` (the entry slug), `pair` (the pair file path and blob), `bucket_policy_read`, `cors_read` (each an object keyed by the three firms), `claim` (`measured`).
    8. Write the proof-of-spec instance in your deliverables folder, validate it, flip this order to `complete`, write your session log and report once to `2.0.0_SA_COO~V2`.
       If a STOP fires, report it FIRST with the world as left (and roll back per the pair if the apply was partial: a confirmed deploy is never left half-landed).
  </go>

  <bounds>
    The blast radius is the pair's: the `opal-ticket-api` Lambda code and environment, three API route resources on API `7k3ed8px20`, one inline policy statement on
    `opal-ticket-api-role`. No other function, route, table, role, bucket, secret or Terraform stack. No bucket policy (the laptop's). No ticket is created, read in detail or changed.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R18REL-AC1" cell_refs="R18-mt-4 R18-tf-5"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_CHECKS/r18_rel_check.py</invocation><expect>^REL-OK </expect></criterion>
</proof_of_spec>
`R18REL-AC1` at the issuance: FAIL as expected (no builder record in the main tree, no result file, no live change). The check re-reads the live Lambda configuration (CodeSha256 against the result's
after-hash, the two environment variables against the builder record, the routing value), the API's route table (each of the three route keys exactly once) and the role's policy statement (two
actions, three prefix ARNs derived from the record), with read-only calls.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: RUN by the applier after the apply (`comp-iam gaps`); necessary, not sufficient. The one new statement is in the pair.
comp-adversary: the control is the check's independent live re-read of the function, the routes and the policy, and the pair's STOP conditions.
</preflight>

# pipeline-override: a RUN/RELEASE order to the dell2 applier for an issuer cell (R18-mt-4, R18-tf-5): a deploy under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
