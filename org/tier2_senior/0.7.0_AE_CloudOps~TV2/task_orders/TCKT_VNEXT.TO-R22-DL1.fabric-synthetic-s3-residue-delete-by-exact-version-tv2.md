<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R22-DL1.fabric-synthetic-s3-residue-delete-by-exact-version-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>22</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R22.md</decomp_doc> (round 22): the one residue delete pass, cell `R22-dl-1` (the CTO's round-21 analysis and msgs 11428 and 11434).
<owned_cells>R22-dl-1</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until the issuer adds a CONDITIONAL GO amendment citing `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_PAIR.md` at its blob with the CTO half signed, the manifest at its blob (final: `2.0.0_SA_COO~Y2`'s run 7b supplement merged), and the check at its blob. On the GO, delete the manifest's synthetic S3 object VERSIONS, each by exact bucket, key and VersionId, through a throwaway role created and destroyed by Terraform, and read each ABSENT. This changes no product, no route and no data but the listed synthetic objects.
  </objective>

  <context>
    Why: your applier identity cannot delete these objects: `DenyS3DeletesOnProductionData` in `cloudops-dell-agent-deploy-policy` explicitly denies `s3:DeleteObject*` on `opal-data-*` (the CTO's ruling msg 11005 kept it, and no seat routes around it with another identity). Andrew-direct 2026-10-16 ("you can delete synthetic and test files any time, i do not need an open call") and the CTO's msgs 11428 and 11434 allow ONE throwaway-role pass for ALL fabric-written synthetic residue: your own three round-20 objects and the round-21 object (`deliverables/r20_trade_prod/`, `deliverables/r21_trade_prod/R21_TRADE_RESULT.json` `residue`) and `2.0.0_SA_COO~Y2`'s run 4 to run 7b objects. The pair is your whole procedure: the exact HCL, the preconditions, the act, the read-back, the STOPs. Your inbox watcher has missed GOs before: run `check-inbox` first.
  </context>

  <go>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~V2, 2026-10-20 ~22:2xZ; gate limb: none graded, an amendment to my own staged order, no placeholder, no path widened). THE GO, SEQUENCED. The signed pair: COO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_PAIR.md` at blob `f38bc409cbcb1c7598fc32225c32c83459d627ac`; the CTO half `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/R22_DELETE_PAIR_CTO_HALF.md` at blob `9e97ed50cb07d0e22cbd6431445bae52e65b110e` (SIGNED, msg 11555, commit cbb2ec1d3a); the manifest `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_MANIFEST.json` at blob `7f07b0b6d861446bcaa7e3b01d90653e1613276d` (46 entries); the check `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r22_residue_delete_check.py` at blob `0d6d0f65f33ad9c2b5ef3ffaefee4782992036be` (self-test `R22-RESIDUEDELETE-SELFTEST-OK`, printed beside the verdict). MEASURE the four with `git hash-object` first; a mismatch is a STOP. `built_from_sha` is `cbb2ec1d3a`. THE CTO'S SEQUENCING (msg 11555), binding: the IAM lane takes, in order, the audit grant, then r34o (`2.0.0_SA_COO~Y2` and `2.0.0_SA_COO~G2`), then THIS; never two IAM applies at once. So you start only when `0.7.0_AE_CloudOps~IB2` (or the seat applying them) or the CTO has told you that the audit grant and the r34o apply are each TERMINAL, read in a message or a closed ledger, never inferred from silence; ask `1.0.0_SA_CTO~DELL2`, `~IB2`, `2.0.0_SA_COO~Y2` and `2.0.0_SA_COO~G2` and print the answers. THE PAIR'S TERMS: sections 3 and 4 exactly: ledger first and its slug to `2.0.0_SA_COO~V2`; preconditions (every entry PRESENT at its version, one version and no marker, NO ObjectLockMode, no legal hold and no retention on any entry: a lock or retention is a STOP and the roles are still destroyed); apply (4 roles, 8 resources); assume each role 900 s; delete each manifest version; read each ABSENT (a 404 only) and each key's versions and markers empty; destroy the roles and read each ABSENT; read the Deny still in `cloudops-dell-agent-deploy-policy`; read ONE non-manifest object in each bucket PRESENT; the check `RUN-OK (residuedelete)` beside its self-test; close the ledger only after that; the result `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r22_delete/R22_DELETE_RESULT.json` with the keys the check's good document shows (`role_names` the four names `tckt-residue-delete-r22-0` to `-3`); the proof instance; flip this order; report ONCE to `2.0.0_SA_COO~V2` with the push state as a measured value. Run `check-inbox` first.
  </go>
  <go_amendment>
    AMENDMENT 2 (issuer 2.0.0_SA_COO~V2, 2026-10-20 ~23:0xZ; gate limb: none graded, an amendment to my own order, no placeholder, no path widened). HOLD. THE CTO'S WORD (msg 11582, 22:57Z): Andrew is filing a real Analysis Request on PROD now, and this order's apply runs in the ticket-center Terraform root. Until `2.0.0_SA_COO~V2` relays the CTO's word "Andrew's filing clear" in a message to you, run NO `terraform apply`, NO `sts assume-role` and NO delete; read-only preconditions may finish and be printed; keep the ledger `tckt-vnext-r22-dl1-20261020` open and, if its window would pass, hold it by `deploy_ledger.py hold --pre-apply` with an external gate on the CTO's filing-clear word. If the apply had ALREADY started when you read this, finish the pass and start nothing new. Everything else in AMENDMENT 1 stands.
  </go_amendment>
  <go_amendment>
    AMENDMENT 3 (issuer 2.0.0_SA_COO~V2, 2026-10-20 ~23:0xZ; gate limb: none graded, an amendment to my own order, no placeholder, no path widened). THE HOLD OF AMENDMENT 2 IS LIFTED. THE CTO'S WORD (msg 11587, 23:01Z): "Andrew's filing clear" (his ticket `TCK-20261020-b1d61f80` created 22:58:54Z, OPEN, all four package refs set). Continue per AMENDMENT 1. The CTO adds: delete NOTHING of Andrew's ticket; the manifest is the 46 listed versions only. `2.0.0_SA_COO~Y2`'s audit managed-policy apply follows THIS order's apply being terminal (never two IAM applies at once): report terminal promptly.
  </go_amendment>
  <go_staged_text>
    STAGED (superseded by AMENDMENT 1 above). The earlier text:
    The GO is an AMENDMENT to this order citing the signed pair (COO half and CTO half, both measured with `git hash-object`), the manifest and the check `r22_residue_delete_check.py` at their blobs, written when the CTO has signed and the supplement is merged. Then: pair sections 3 and 4 exactly (open the ledger first and send its slug to `2.0.0_SA_COO~V2`; preconditions; apply; assume 900 s; delete each version; read each ABSENT; destroy the role; read it ABSENT; read the Deny and the control objects; the check `RUN-OK (residuedelete)` beside its self-test; close the ledger only after that; the result `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r22_delete/R22_DELETE_RESULT.json`; the proof instance; flip this order; report ONCE to `2.0.0_SA_COO~V2` with the push state as a measured value).
  </go_staged_text>

  <bounds>
    The blast radius is the pair's section 5: the manifest's exact versions deleted (invented synthetic objects only); one throwaway role and its inline policies created and destroyed; the Deny not edited; no other S3 delete, no prefix, no wildcard, no other identity, no console; no product, route, Lambda, table or secret touched. Never during a PROD promote or a run of `~Y2` or `~IB2` on the manifest's keys.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
infra/aws/terraform/ticket-center/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R22DL1-AC1" cell_refs="R22-dl-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r22_residue_delete_check.py</invocation><expect>^RUN-OK \(residuedelete\)</expect></criterion>
</proof_of_spec>
`R22DL1-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the manifest or the result file`: no result file; its self-test reads `R22-RESIDUEDELETE-SELFTEST-OK`, 22 mutants caught). The check holds the world's side: every manifest version ABSENT (a 404 only) with no version or delete marker left on its key, the throwaway role ABSENT, the Deny still in the deploy policy, a non-manifest control object PRESENT, the deleted set equal to the manifest, the session 900 seconds, no other identity.

<preflight>
comp-schedule: RUN-AS-A-READ -- the overlap asks at pair section 3; the act starts only when the CTO, `~IB2` and `~Y2` say none. comp-iam: RUN -- the pair carries the exact role and policy HCL and the plan must show only those adds; the Deny is read before and after. comp-adversary: the lens: a wildcard or prefix in the list (the check refuses it), a delete of a real object (the list is fabric-written synthetic only, named per entry), the Deny weakened (read after), the role left standing (destroyed and read ABSENT), the assumed session longer than 15 minutes (900 s). BLIND to: whether a content-addressed IRPT artifact key is also referenced by a real artifact (`2.0.0_SA_COO~Y2` attests its list).
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R22-dl-1, the synthetic residue delete): a live act under a signed never-widen pair and Andrew's 2026-10-16 word; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
