<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-VERIFY-e68.cottonwood-cash-mix-read-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~S</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
  </metadata>
<risk>LOCAL</risk>
<proof_genre>READ</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R12.md</decomp_doc> (round 12), the issuer act of cell `SC-e-68`
(the CASH row write, LANDED @beac685f46). This order is that act's verify leg L2, read-only.
<owned_cells>SC-e-68</owned_cells>
</decomp_ref>

  <objective>
    READ-ONLY. After the first Black Diamond-family gold run that starts after 2026-10-08T03:12:55Z, read Cottonwood's served mix
    and report: (a) the run id and its start/end times; (b) Cottonwood's mix total, equal to its total before the run within
    USD 1.00; (c) the CASH ticker's value now sits in the `cash` bucket, not `fixed_income`. The CASH amount is USD -5,480,054.44, so the expected
    move is the cash bucket lower by 5,480,054.44 and fixed_income higher by the same amount (half request :52). This is the fallback if dell1 cannot read the bucket itself (laptop 1.0.0_SA_CTO msg 106716).
  </objective>

  <context>
    The write moved one row in `etf-classifications`: ticker CASH, from fixed_income / Ultra Short Duration to cash / Cash.
    Ledger: `org/critical_paths/change_management/20261008T0312Z_secclass-e68-cash-row-m1-20261008_deploy_completion.md`, leg L2 OPEN.
    Readers of the CASH key on Cottonwood (half request section "Served mix delta, per firm", both halves SIGNED):
    `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_CASH_ROW_20261008.md` :44-52.
    The likely run is 04:00Z daily (rule bd-canonical-prices-daily, bd-gold-trigger); then 23:00Z (bd-gold-nightly-fallback), or any
    opal-data-bd silver/prices landing (MSTR msg 785).
  </context>

  <the_act>
    1. BEFORE the run, if it has not started: list the Cottonwood served mix outputs written by `C_06.client_mix_timeseries.py`
       and `D_04.client_portal_summary.py` (concentration.json), with each object's LastModified and VersionId, and record the
       firm mix total and the CASH ticker's bucket and value.
    2. Wait for the run's end. Only a run that REBUILDS Cottonwood's mix counts (CTO half AMENDMENT 1 @ef0ca3a2bc,
       org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e68_CASH_ROW_20261008.md): if the C_06, D_03 and D_04
       outputs keep a LastModified older than 03:12:55Z, the read is "not yet", not a pass; repeat at the next run (23:00Z).
    3. AFTER: read the same objects again and record the same three values.
    4. Write the result to `org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/E68_COTTONWOOD_CASH_MIX_READ_20261008.md` and commit it.
       Then send the path and hash to 2.0.0_SA_COO~M1. No write to any bucket or table.
    5. If the run did not process Cottonwood, or a read is denied, report that by action and resource, and stop.
    The rollback is the issuer's (`cash_row_write.py --rollback CASH_ROW_SNAPSHOT_20261008.json --write`, dell1). Do not run it.
  </the_act>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/E68_COTTONWOOD_CASH_MIX_READ_20261008.md
org/tier2_senior/0.7.0_AE_CloudOps~S/task_orders/MDPF_SECCLASS.TO-VERIFY-e68.cottonwood-cash-mix-read-laptop.md
</paths>

<proof_of_spec>
<criterion id="E68V-AC1" cell_refs="SC-e-68"><invocation>read the Cottonwood mix objects before and after the first BD-family gold run after 03:12:55Z</invocation><expect>outputs rebuilt after 03:12:55Z, mix total equal within USD 1.00, and the CASH ticker in the cash bucket; unrebuilt outputs read NOT-YET</expect></criterion>
</proof_of_spec>

<preflight>
comp-schedule: RUN -- MSTR msg 785 read the BD-family triggers live: bd-canonical-prices-daily 04:00Z, bd-gold-nightly-fallback 23:00Z, and opal-data-bd silver/prices landings; BLIND: whether a given run rebuilds Cottonwood, which step 2 reads.
comp-iam: DECLARED-NOT-APPLICABLE -- read-only; the laptop seat's standing read on the cottonwood bucket (it holds the e42 ledger); a denial is reported by action and resource (step 5).
comp-adversary: RUN -- BLIND on the denominator: this order names a read of a firm bucket that dell1 cannot see, so no denominator was measured at the cut; the arms named are an unrebuilt output read as a pass (step 2) and a write (none permitted).
</preflight>
</task_order>
