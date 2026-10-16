<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R19-REL.ticket-service-release-for-the-four-cross-firm-admissions</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-16</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>19</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R19.md</decomp_doc> (round 19): cell `R19-rl-7`.
<owned_cells>R19-rl-7</owned_cells>
</decomp_ref>

  <objective>
    Release the ticket service so the three code changes of row S134 (the notice recipient derived from the firm's contacts, the `svc-analyst-intake` list scoped to its configured firms, the
    fail-closed firm scope with the explicit marker) and the two environment values are LIVE together: build the `opal-ticket-api` package from the merged tree, `safe-apply` the Terraform
    source, and read it back. STAGED: it starts only on the issuer's GO, which names a signed never-widen pair, and only after `TO-R19-MIG` reads MIG-OK.
  </objective>

  <context>
    **The pair is your whole procedure.** The issuer writes it after the worker orders `TO-R19-L1`, `L2`, `L3`, `TR` are merged, at
    `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_REL/R19_REL_PAIR.md`, and the CTO signs its half. It names the merge commit you build from (`built_from_sha`),
    the expected Terraform plan (the Lambda's environment gains `CLIENT_NOTICE_CONTACT_MAP` and `ANALYST_INTAKE_ALLOWED_FIRMS`, nothing else), and the rollback per key.
    Row S134 item 1 changes who receives a client notice (the contact map ships empty, so no client notice is sent until the contacts are supplied: stated in the pair); the pair says whether
    any part is a client-facing change that waits on Andrew's word.
    **Ordering with the other releases of the same Lambda:** `TO-R18-REL` (the meeting and attachment routes, staged behind the laptop's bucket apply) and `2.0.0_SA_COO~Y2`'s owner-check release
    both touch `opal-ticket-api`. Before you build, read the live `CodeSha256` against the tree's build and read `org/critical_paths/.open_deploys/` in EVERY live worktree. If an open entry names
    `opal-ticket-api`, or the live code is not what the tree's HEAD minus this round builds, STOP and report to the issuer: the releases are then ordered or merged by the issuer, never raced.
    The issuer may fold this release into `TO-R18-REL` by one combined pair; if so the GO says so and names which order carries which check.
    Model: the build procedure of `TO-R18-REL` (zip built from `built_from_sha`, member list and sha256 printed, compared with the live package member by member).
  </context>

  <go>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-16 ~16:5xZ; gate limb: none graded this modification; it narrows, no placeholder, no path widened). FOLDED, NO SECOND APPLY. This order is CARRIED BY THE ONE APPLY of `TCKT_VNEXT.TO-R18-REL` under the COMBINED pair `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_REL/R18_R19_COMBINED_REL_PAIR.md` (blob `643ba43746582b1a50c91923a58a23b9a7979715`, signed by both halves; the CTO half blob `2f52cca81d01d28bae2b4637a5f6a2463148560b`, @6bdc8ef4f4). Its GO is the one written in that order's AMENDMENT 1 (the same measured blobs, `built_from_sha` `de2fdb4a4f01520fd166dca8abb21f4541446f47`, the CTO's three conditions); this order's steps 1 and 2 below (the migration check and the read of the live state) are PRECONDITIONS of that apply, run once. After the apply, run `r19_rel_check.py` (it must print `REL-OK`), write `R19_REL_RESULT.json` with the same hashes as the R18 result, write this order's proof instance, and flip it. Then, in order:
    1. STEP 0: open the NEVER-2 ledger entry and keep it open until the read-backs pass.
    2. STEP 1: confirm `TO-R19-MIG`'s result file reads MIG-OK (run the issuer's migration check); any other reading is a STOP (the release would lock staff out).
    3. STEP 2: build the package from `built_from_sha`; print its member list and sha256; the members that differ from the live package must be exactly the ticket Lambda's source.
    4. STEP 3: `safe-apply` plan only; print the plan summary; it must equal the pair's expected plan exactly or STOP.
    5. STEP 4: apply under `safe-apply`, upload the package as the pair says, wait for the function to be `Active`/`Successful`.
    6. STEP 5: read back; run the issuer's check; close the ledger entry only after it prints REL-OK.
    7. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r19_rel/R19_REL_RESULT.json` with the keys `built_from_sha`, `package_sha256`, `code_sha256_before`, `code_sha256_after`, `plan_summary`, `change_ledger`, `pair`, `mig_result` (the migration result file path), `claim` (`measured`).
    8. Write the proof-of-spec instance, validate it, flip this order to `complete`, write your session log and report once to `2.0.0_SA_COO~V2`. If a STOP fires, report it FIRST with the world as left (and roll back per the pair if the apply was partial: a confirmed deploy is never left half-landed).
  </go>

  <bounds>
    The blast radius is the pair's: the `opal-ticket-api` Lambda code and its two new environment values. No other function, route, table, role, bucket, secret or Terraform stack. No ticket is created, read in detail or changed.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R19REL-AC1" cell_refs="R19-rl-7"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_CHECKS/r19_rel_check.py</invocation><expect>^REL-OK </expect></criterion>
</proof_of_spec>
`R19REL-AC1` at the issuance: FAIL as expected (no result file, no live change). The check re-reads the live Lambda configuration (CodeSha256 against the result's after-hash, the contact map is a JSON object, the intake list is exactly the three served firms) with a read-only call, and requires the migration's result file to exist.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: RUN by the applier after the apply (`comp-iam gaps`); necessary, not sufficient. No IAM change is planned.
comp-adversary: the control is the check's independent live re-read of the function and the pair's STOP conditions; the lens is a staff row locked out by the release (the migration is the gate) and a notice sent to a body address. BLIND to: the live users rows (the migration check reads them) and the tickets (denominator: 1 function configuration read).
</preflight>

# pipeline-override: a RUN/RELEASE order to the dell2 applier for an issuer cell (R19-rl-7): a deploy under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
