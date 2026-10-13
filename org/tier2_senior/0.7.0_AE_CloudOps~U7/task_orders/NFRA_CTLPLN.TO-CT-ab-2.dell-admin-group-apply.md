<task_order id="NFRA_CTLPLN.TO-CT-ab-2.dell-admin-group-apply">
<to_id>NFRA_CTLPLN.TO-CT-ab-2.dell-admin-group-apply</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~U7</issued_to>
<date>2026-10-13</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>3</round>
<workstream>DELLADMIN</workstream>

<title>NFRA_CTLPLN DELLADMIN CT-ab-2: apply the Dell admin-group change (two memberships added, three policy documents updated, the routes-fn policy destroyed), read it back, record it -- only under a signed never-widen pair</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round12.md</decomp_doc>
<owned_cells>CT-ab-2</owned_cells>
<decomp_context>CT-ab-1 (merged) put the change in the repository: both Dell agent users join the existing group AdministratorAccessOpalCapital and every Deny that reached them goes except DenyCloudTrailWrites, DenyS3DeletesOnProductionData, DenyTableAndDatabaseDeletes and DenyAuditTrailBucketWrites. This order applies it. Andrew's rec (b): org/tier1_exec/2.0.0_SA_COO~C/deliverables/ANDREW_DIRECT_20261013_165xZ_DELL_USERS_ADMIN_GROUP_KEEP_THREE_DENIES.md. Pair: org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-ab-2_PAIR_20261013.md (read it whole; its section 1 is the write set, section 3 the expected plan, section 4 the reads).</decomp_context>
</decomp_ref>

<the_act>
START CONDITION (read before anything else): both halves of the pair read SIGNED at the same pin -- the COO half is the pair file above; the CTO half is a file under org/missions/D0/NFRA/NFRA_CTLPLN/ledger/ named for CT-ab-2 that the COO names in a broker message to you. Until both are SIGNED at one pin, do PRE-1 and PRE-2 only (read-only) and wait; a wait here is expressly qualified: it ends on the CTO's signed half, and the COO does not apply or sign for the CTO.
1. Load `/cloud-ops`. Recompute the pin hashes (pair section 1) from `git show <pin>:<path>`; a mismatch is Branch B (STOP, report).
2. PRE-1 and PRE-2 (pair section 4): print the group read, both users' groups, and run the root's plan (read-only); save the plan text to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-2.plan.txt`. The plan must read `2 to add, 3 to change, 2 to destroy` on exactly the six keys of the pair; anything else is Branch B.
3. Only with both halves SIGNED at the pin: open ONE NEVER-2 ledger entry (the six keys, the pin, the previous tree id, the consumers, the rollback), then apply through `safe-apply` (never bare `terraform apply`). Read POST-1, POST-2, POST-3 (pair section 4). Any POST-3 answer other than explicitDeny: roll back at once (one re-apply of the previous tree), file a BLOCKING row, report.
4. Write `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-2.apply-record.txt` with these final lines, exact form: `APPLY pin=<10 chars> added=<n> changed=<n> destroyed=<n>`, `POST-1 dell1=<groups> dell2=<groups>`, `POST-2 allowed=<k>/5 per user`, `POST-3 explicit_deny=<k>/4 per user`. Close the ledger entry. Report to 2.0.0_SA_COO~C.
</the_act>

<bounds>
- Writes ONLY the six keys of the pair (section 1). No other IAM object, no secret read, no data-plane call, no group created or imported, no user key minted. The previous tree id is recorded before the apply.
</bounds>

<proof_of_spec>
<criterion id="CTab2-AC1" cell_refs="CT-ab-2"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-2.apply-record.txt</invocation><expect>added=2 changed=3 destroyed=2</expect></criterion>
<criterion id="CTab2-AC2" cell_refs="CT-ab-2"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-2.apply-record.txt</invocation><expect>explicit_deny=4/4</expect></criterion>
</proof_of_spec>
<expected_criteria>CTab2-AC1,CTab2-AC2</expected_criteria>
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-2.dell-admin-group-apply.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTab2-AC1,CTab2-AC2`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~U7/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one apply.
comp-iam: RUN at step 2 -- denominator the six keys and the two users; BLIND to anything attached to the users outside this root (the PRE-1 read lists their groups; the plan lists only this root).
comp-adversary: RUN -- an apply before the CTO half is signed (the start condition); a plan with an extra destroy (Branch B); a rollback that restores a Deny the ruling removed (the previous tree is the pre-ruling tree: the rollback is the ruling's reversal, stated); a POST-3 read taken as the user instead of simulated (simulate only); BLIND: a Deny attached to the users outside this root.
lane: the <paths> block names the seat's deliverables and logs, the ledger and its sentinel, and the surprise channel.
</preflight>

Source: Andrew's rec (b); CTO ruling @53acd6fe5f section 1; CT-ab-1 merge e4ae5f7820.
</task_order>
