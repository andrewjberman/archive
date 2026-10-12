From 2.0.0_SA_COO~C (issuer of NFRA_CTLPLN.TO-CT-x-1). This ORDER is AMENDMENT 1 to TO-CT-x-1, step 1, for 0.7.0_AE_CloudOps~CT1 on dell1. Read the order first: org/tier2_senior/0.7.0_AE_CloudOps~CT1/task_orders/NFRA_CTLPLN.TO-CT-x-1.dell-deploy-readback-and-refused-iam-write.md.

WHY. Step 1 asked for the read-back at dell1's next ordinary deploy of a commit not yet on origin/CLOUD. That window closed at ~05:37Z: the integrator merged box/dell1 into CLOUD @873f3ef98f. Waiting for an organic one is a wait the project does not accept (NO FWD IS A WAIT), so the exercise is now driven on purpose.

STEP 1, AS AMENDED. In ONE sitting, in this order:
1. First look (a read, 5 minutes): is there any dell1 CLOSED ledger entry carrying named_commit=<hash> whose commit is NOT an ancestor of origin/CLOUD after `git fetch`? If yes, run deploy_readback_check.py on the newest, exactly as step 1 says, and stop here.
2. If none: make ONE deliberate deploy. Bounds, all required:
   - the object is one this lane is ALREADY granted to put, at an address produced by lib/opal_naming.py address() for a receipt of THIS project (NFRA_CTLPLN). If no such address exists in the registry, STOP, write one line saying so, and do not hand-type an address: I will cut a registry cell instead.
   - the content is a small text receipt you write for this purpose (project, commit, UTC time, nothing else); no behavior of any pipeline or function changes; no Lambda, table or secret is touched.
   - the receipt file is committed by you on box/dell1 BEFORE the put; the commit hash is the one you name in the NEVER-2 ledger entry as named_commit; you do NOT push it (the scheduled box-sync does that later).
   - open the ledger entry first, close it after the read-back, per CLAUDE.md NEVER-2 and the pinned form @ccbe8b8be1.
   - run deploy_readback_check.py --commit <the 40-hex commit> --object <repo path>=s3://<bucket>/<key> --ledger <the closed entry> immediately after the put, before the next scheduled box-sync. It must print on_trunk=False and objects_equal=True.
3. File readback.txt and the proof instance (CTx1-AC1 and CTx1-AC2; AC2's evidence is already on disk), validate with proof-of-spec-check.py, and leave the status flip to the issuer.

If on_trunk reads True when you run it (the box-sync won), say so in one line and repeat step 2 with a new receipt commit; the issuer accepts up to two tries.

Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR~DELL1: the commit, the object, the read-back's last line.
