<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-36.bd49f-dim-compaction-one-run</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~NFRA2</issued_to>
    <date>2026-10-20</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
    <round>42</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round30.md</decomp_doc> (workstream OUTCOME, round 30, amendment 14): the one run of the compaction tool built by cell `CT-cn-1`
<owned_cells>CT-co-1</owned_cells>
</decomp_ref>

  <preflight>
comp-schedule: RUN -- this order is STAGED until the scheduled fire `opal-assets-bd49f-dim-convert-daily` (`cron(5 7 * * ? *)`, as-of yesterday UTC) of 2026-10-21 07:05Z has written `date=2026-10-20` with the fixed code; the issuer reads that fire and sends the GO (a message naming this order); no act below starts before the GO. The schedule is READ and not changed.
comp-iam: RUN -- the tool's apply mode needs `s3:PutObject` and `s3:GetObject` on the ONE key and `s3:GetObjectVersion` for the rollback proof; the seat reads its own grant first (a `head-object`/`get-object` of the key, and a dry authorization check of the put through the plan mode never writing) and STOPS if a needed action is refused; it does not widen a grant.
comp-adversary: RUN -- the wrong partition written (the `--confirm-key` refusal and the key printed in the plan line); a write before the fire (the GO and the step-1 read); a write after a failed proof (the tool refuses; the seat also reads the plan line); the compacted object read as the old (the prior `VersionId` and sha256 recorded BEFORE, the new `VersionId` read AFTER); a second run (not allowed: the tool refuses `merged=0` the second time, and the order allows exactly one apply); another partition touched (ETag listings of `date=2026-09-28`, `date=2026-10-19` and the xref before and after); the xref or any other table touched (the tool writes one key); cost (none).
risk: WORLD -- a rewrite of a served object. COO half of the never-widen pair: `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/NEVER_WIDEN_BD49F_DIM_COMPACTION_COO_HALF_20261020.md`; CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_BD49F_DIM_COMPACTION_CTO_HALF_20261020.md` @dee04e1b01. Blast radius: ONE key, `blackdiamond/49f/silver/dim_advisor_fee_role/date=2026-10-20/data.parquet` in bucket `opal-data-assets`; rollback per key: restore the prior object version, or copy `date=2026-10-19/data.parquet` forward.
lane: the seat is `0.7.0_AE_CloudOps~NFRA2`; NEVER-2 ledger opened first.
  </preflight>

  <precondition>
    Cell `CT-cn-1` is merged (the tool `data/assets/scripts/silver/bd49f_dim_compact.py` and its six tests are on `box/laptop`; the issuer names the merge commit in the GO). The GO message carries the read of the 07:05Z fire.
  </precondition>

  <go>
    GO, issuer 2.0.0_SA_COO~C, 2026-10-21 ~07:2xZ. The scheduled fire wrote `date=2026-10-20` at 07:06:23Z with the fixed code (listing read at 07:16Z; `aws s3 ls` shows local 03:06:23). Issuer's read of the fire, read-only: dim rows 288,195 against 288,194 on 2026-10-19; open rows 5,339 in both; 5,338 of 5,339 open accounts kept their `effective_from`; one account closed on 2026-10-20 (a real change). The tool is merged at 40cecd5f66f on box/laptop (`data/assets/scripts/silver/bd49f_dim_compact.py`; six tests), and the issuer's plan-mode read of the real `date=2026-10-19` partition read `rows_before=288194 rows_after=6669 merged=281525 accounts=5339 current_equal=True runs_equal=True`. Step 1's LastModified gate is therefore met; run your own step-1 read anyway.
  </go>

  <objective>
    Rewrite the one object once with its history compacted (about 288k rows to about 5.4k plus the real changes), with the three equality proofs printed, and leave every other key byte-identical.
  </objective>

  <context>
    The tool: `python data/assets/scripts/silver/bd49f_dim_compact.py --date 2026-10-20 --mode plan` (read-only, prints `COMPACT-PLAN ... current_equal=... runs_equal=...`), then `--mode apply --confirm-key blackdiamond/49f/silver/dim_advisor_fee_role/date=2026-10-20/data.parquet` (one `put_object` to the same key, read-back, proofs re-run). The bucket `opal-data-assets` has versioning Enabled (the CTO read it at signing). Run Python with `-I` from a folder that holds no stray modules; the tool imports the converter module by path (read the tool's first lines). The box CLI is v1: no `--cli-binary-format`.
  </context>

  <steps>
    0. NEVER-2: after the GO, open the ledger entry FIRST (`deploy_ledger.py open`, slug `bd49f-dim-compaction`), naming the ONE key; commit it OPEN, then act.
    1. Read, record BEFORE: `head-object` and `list-object-versions` of the key (the prior `VersionId`, size, LastModified), download the object to scratch and hash it (sha256); the object's LastModified must be AFTER 2026-10-21 07:05Z (the fire wrote it) else STOP. ETag listings (with counts) of `dim_advisor_fee_role/` and `dim_account_xref/`.
    2. `--mode plan` on the key's date: record the whole last line. It must read `current_equal=True runs_equal=True` and `merged` above 0. If `merged=0`, STOP and report (nothing to do). Any `False`: STOP and report.
    3. `--mode apply --confirm-key <the key>` ONCE. Record the whole `COMPACT-APPLY` line.
    4. AFTER: `head-object` of the key (a NEW `VersionId`); `get-object --version-id <prior>` to scratch: its sha256 must equal the BEFORE sha256 (the rollback is real). Re-list the ETags of both tables: every key other than the one is present with an equal ETag, counts printed.
    5. Close the ledger entry with the proof, write a report in `deliverables/`, flip this order.
  </steps>

  <stops>
    STOP and report (do not improvise) if: no GO has arrived; the object is older than the fire; a plan line reads False or `merged=0`; the grant is refused; the apply line reads `readback_equal=False` or `wrote=False` when merged was above 0; any other key's ETag differs after the run. ROLLBACK (restore the prior version of the one key) only if the issuer or the CTO says so, or if `readback_equal=False`. Do NOT run the apply twice and do NOT delete any version.
  </stops>

  <proof_of_spec>
    <criterion id="CTco1-AC1" cell_refs="CT-co-1"><invocation>the tool's plan line and apply line for date 2026-10-20 (both whole lines quoted)</invocation><expect>COMPACT-PLAN current_equal=True runs_equal=True merged above 0, and COMPACT-APPLY readback_equal=True wrote=True with rows_before and rows_after printed</expect></criterion>
    <criterion id="CTco1-AC2" cell_refs="CT-co-1"><invocation>aws s3api list-objects-v2 with ETags of dim_advisor_fee_role/ and dim_account_xref/ before and after (counts printed), the compacted key excluded</invocation><expect>every other key present with an equal ETag</expect></criterion>
    <criterion id="CTco1-AC3" cell_refs="CT-co-1"><invocation>aws s3api get-object --version-id of the prior VersionId, sha256 of the downloaded bytes against the BEFORE sha256</invocation><expect>equal, with a one-byte-changed negative control reading unequal</expect></criterion>
  </proof_of_spec>

  <expected_criteria>CTco1-AC1,CTco1-AC2,CTco1-AC3</expected_criteria>
</task_order>
