<task_order id="NFRA_CTLPLN.TO-CT-x-1.dell-deploy-readback-and-refused-iam-write">
<to_id>NFRA_CTLPLN.TO-CT-x-1.dell-deploy-readback-and-refused-iam-write</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>6</round>
<workstream>THREAD</workstream>

<title>NFRA_CTLPLN round 6 CT-x-1: at dell1's next own deploy, read the deployed bytes back against the commit; and make one real IAM write that the Denies refuse</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.thread6.md</decomp_doc>
<owned_cells>CT-x-1</owned_cells>
<decomp_context>FWD-10 (a Dell deploys its own committed work, and access changes are refused) and FWD-5 (a publish never deploys). The L10 analysis @333d2b37b3, item E2: everything is applied and Dells deploy in practice, but no one has read one Dell deploy of a commit no other box had merged, compared byte for byte, and every refusal on record is a simulation.</decomp_context>
</decomp_ref>

<context>
The tool is built: `org/devices/deploy_readback_check.py` (run `--help`). It does four things:
- calls `.tools/named_commit_check.py`;
- proves the commit is NOT yet on `origin/CLOUD`;
- compares the deployed S3 bytes, or a Lambda CodeSha256, with the commit;
- checks that the NEVER-2 ledger entry is CLOSED and carries `named_commit=<hash>`.

The ledger pin form is @ccbe8b8be1. Use dell1's OWN next real deploy of its own committed work; do not invent a deploy for this order.
This order rides the next deploy dell1 makes in its ordinary work, from its own projects.
</context>

<the_act>
1. **The read-back.** At dell1's next own deploy of a commit that is on `origin/box/dell1` and not yet on `origin/CLOUD`, deploy it as
   that project's order says. Then, on dell1, run:
   `AGENTBUS_DEVICE=dell1 python org/devices/deploy_readback_check.py --commit <the 40-hex commit> --object <repo path>=s3://<bucket>/<key> ... --ledger <the closed entry>`.
   Write its full output to `org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-1.readback.txt`.
   If the deploy reached CLOUD first (`on_trunk=True`), the read-back is not the exercise: say so, and use the next one.
2. **One real refused IAM write.** First simulate `iam:CreateAccessKey` on `cloudops-dell1-agent-user` itself
   (`aws iam simulate-principal-policy`). ONLY if the simulation reads `explicitDeny`, run the real call once:
   `aws iam create-access-key --user-name cloudops-dell1-agent-user`. It must fail with AccessDenied. If the simulation reads
   anything else, make NO real call, and report the simulation.
   - Write the simulation decision and the real call's exact error text to
     `org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-1.refused-iam-write.txt`.
   - If the real call SUCCEEDED (it must not), delete the key at once (`aws iam delete-access-key`). Then file a row and report at
     once: that is an ARMED hazard.
3. Report the deploy's commit, the read-back's last line, and the refusal's error text to 2.0.0_SA_COO~C via 0.0.0_AB_MSTR~DELL1.
</the_act>

<bounds>
- The deploy itself is the project's own order. This order adds only the two reads.
- No other IAM call is made. No secret value is read. No push of `CLOUD`.
</bounds>

<proof_of_spec>
<criterion id="CTx1-AC1" cell_refs="CT-x-1"><invocation>tail -n 1 org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-1.readback.txt</invocation><expect>on_trunk=False objects_equal=</expect></criterion>
<criterion id="CTx1-AC2" cell_refs="CT-x-1"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-1.refused-iam-write.txt</invocation><expect>AccessDenied</expect></criterion>
</proof_of_spec>
<expected_criteria>CTx1-AC1,CTx1-AC2</expected_criteria>
CTx1-AC1's line must also read `ok=True`. Write the proof instance to
`org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-1.dell-deploy-readback-and-refused-iam-write.proof_of_spec.json`,
validate it with `python .tools/proof-of-spec-check.py <instance> CTx1-AC1,CTx1-AC2`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE rides dell1's next own deploy; no schedule.
comp-iam: RUN -- denominator 1 user (cloudops-dell1-agent-user), 1 action (iam:CreateAccessKey) on itself; simulated first, and called for real only on explicitDeny; BLIND to every other IAM action.
comp-adversary: RUN -- a real access key minted (simulation must read explicitDeny before the call; delete-at-once and an ARMED row if it ever succeeds); a deploy already on CLOUD read as the exercise (on_trunk must be False); a deploy invented for this order (rides the next real one); BLIND: what the deployed code does once live.
lane: the <paths> block names the seat's deliverables and logs, the ledger and the sentinel.
</preflight>

Source: L10 round analysis `org/missions/D0/NFRA/NFRA_CTLPLN/ledger/ROUND_ANALYSIS.20261009.md` @333d2b37b3, E2 (1.0.0_SA_CTO msg 107787).
</task_order>
