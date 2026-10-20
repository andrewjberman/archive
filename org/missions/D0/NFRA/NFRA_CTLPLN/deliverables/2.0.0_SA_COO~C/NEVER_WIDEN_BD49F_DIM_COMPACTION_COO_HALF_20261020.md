# NEVER-WIDEN co-sign, COO half: the one-time compaction of the 49F `dim_advisor_fee_role` SCD2 history (part 3 of the dim-convert fix)

**Signer:** `2.0.0_SA_COO~C` (laptop), 2026-10-20 ~20:1xZ. **CTO half:** `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_BD49F_DIM_COMPACTION_CTO_HALF_20261020.md` @dee04e1b01 (read whole at signing). **Cells:** `CT-cn-1` (the tool, a worker) and `CT-co-1` (the one run, `0.7.0_AE_CloudOps~NFRA2`), decomposition `NFRA_CTLPLN_DECOMP.round30.md` amendment 14.

## The same blast radius, in the act's own terms

- **One object:** `s3://opal-data-assets/blackdiamond/49f/silver/dim_advisor_fee_role/date=2026-10-20/data.parquet`, written in place once, and only after the scheduled 07:05Z fire of 2026-10-21 has written it with the fixed code (CodeSha256 `blu8AGfk...`, read live). Nothing else: not `date=2026-09-28`, not `date=2026-10-19`, not the xref, no other table, firm or bucket, no delete, no producer or schedule change.
- **The rule, read from the tool's own code before the run (one writer of the property: the tool; its rule is the CTO half's):** within each `account_id`, consecutive periods whose SCD2 change tuple is identical after the `DIM_SCHEMA` cast merge into one row with the earliest `effective_from` and the latest `effective_to`; every other field comes from the earliest row of the run; the open row of each account stays open with its tuple unchanged.
- **Both branches covered:** (1) real changes (about 3 a trading day were measured) stay separate periods; (2) no identical neighbours: the tool writes nothing and records `0 merged`. The tool refuses to write unless its plan mode has printed the three proofs and all read equal.
- **Three proofs before the write counts** (printed with denominators, committed with the cell): the set of current rows equal before and after; every account's ordered tuple runs equal before and after; the row count (about 288k to about 5.4k plus the real changes).
- **The on-demand arm of the proof:** the tool's read-only plan mode is run by the issuer on the real `date=2026-10-19` partition NOW (it writes nothing), so the rule is exercised on real data before the post-fire write; the post-fire run is the organic case.
- **Rollback, per key:** restore the prior object version of that one key (bucket versioning `Enabled`, read by the CTO at signing), or copy `date=2026-10-19/data.parquet` forward and let the next fire refold. The seat records the prior `VersionId` before the write.
- **Not covered by this half:** any delete of an old partition (Andrew confirms any delete); a compaction of any other partition; a re-run after a second fire has written `date=2026-10-21` (that is a new ask).

-- 2.0.0_SA_COO~C (laptop)
