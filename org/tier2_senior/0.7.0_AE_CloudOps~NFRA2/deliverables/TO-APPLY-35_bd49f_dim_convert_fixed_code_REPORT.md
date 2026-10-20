# NFRA_CTLPLN.TO-APPLY-35 -- bd49f dim-convert fixed-code deploy: COMPLETE

**By:** `0.7.0_AE_CloudOps~NFRA2` (laptop), 2026-10-20 19:46Z to 19:58Z. **Issuer:** `2.0.0_SA_COO~C`. **Ledger:** `bd49f-dim-convert-fixed-code`, CLOSED. Window: acted at 19:48Z to 19:52Z, well before 06:30Z; the next scheduled fire (07:05Z) runs the fixed code.

## Result

| Criterion | Verdict | Evidence |
|---|---|---|
| CTcm1-AC1 | PASS | Deployed package (`get-function` Code.Location, downloaded to its own scratch folder): `bd49f_dim_conversion.py` sha256 `bc3019570d49ac1ee10d7cd7668dfdc23a09e938d14dece7abd7c662cf00d503` = the pin (`git show 82484219d4b:...`). Mutant (byte 100 xor 1) `e4bc87a1...` UNEQUAL. `stream_parquet.py` `2e3762e1...` equals the repo file at the pin. |
| CTcm1-AC2 | PASS | `{m: 3008, t: 900, s: blu8AGfkLFODrFvcNY7MKpk5INoT6LnyKG96pg7F1P8=}`; before `Iosob5...`; the zip's built sha256 is the same `blu8...`. LastUpdateStatus Successful. Targeted re-plan: `No changes`. |
| CTcm1-AC3 | PASS | Seam probe on the DEPLOYED file: `FOLD same-rows: newly_closed=0 of 5338 open; total rows 282857 (prev 282857)`; `CONTROL one real flat_fee change: newly_closed=1`. Negative control, the PRIOR object version's file (sha `dbbd41e4...`): `newly_closed=5338 of 5338`, total rows 288195. |

## Act

- BEFORE: config 3008/900/`Iosob5...`; artifact `opal-assets/opal-assets-bd49f-dim-convert.zip` version `e1QAG_MImQG4spPuHu8kmBA4ZjMIByAD` (2026-07-17, 18528 B, content-sha256 `Iosob5...`), the rollback target. Only 2 versions exist; the older is `HAVfJtcr...`.
- Pin check: the file at `82484219d4b` and the vendored copy both hash to the order's value.
- `build-and-upload.sh opal-assets opal-assets-bd49f-dim-convert`: import-closure OK, 3 files, sha256 `blu8...`, new version `38_BbBXe67zW2t.11apDUB6_.W619ln0` (18727 B).
- Targeted plan: ONE change, in place, `source_code_hash` and `s3_object_version` (plus `last_modified` computed); no `memory_size` or `timeout` line. Untargeted plan beside it: 3 add + 2 change = the function plus four SCHWABBF items (`silver_read_schwab_firm_prefix`, `silver_state_write_schwab_firm`, `silver_write_schwab_firm_silver`, `monolith_bronze` notification). Not applied here.
- `safe-apply` of the saved targeted plan with `HALT_ACK=1`: 0 added 1 changed 0 destroyed. The three pending messages were routine (two already-read issuer messages and a 3-day-old dell1 order), none STOP-class.
- `record-terraform-deploy.sh` (`--function`, `--deploy-ledger`): commit `d5b8527acb`, tag `opal-assets-v0.52.0` on it, LOCAL. No invoke was made.

## Deviation and notes

1. **Seam probe invocation.** `python -I <probe> <file>` fails with `ModuleNotFoundError: stream_parquet`, because `-I` drops the script directory and the converter imports `stream_parquet` flat. I ran the same probe unchanged through `python -I -c` with `runpy.run_path`, putting only the extracted package folder on `sys.path`. Same script, same bytes; the order's literal line cannot run as written.
2. **Probe fixture.** The probe reads `date=2026-09-28` of the dim (282,857 rows), not the live 288,194-row dim; it proves the comparison, not the compaction.
3. **Function map.** `last_deployed_commit` was written as `61850841c0dc...` (last commit touching the function's source dir), not the merge `82484219d4b`; that is the recorder's own rule.
4. **Rollback (not used):** point `s3_object_version` back to `e1QAG_MImQG4spPuHu8kmBA4ZjMIByAD` and apply through `safe-apply -target`.
5. **Still open:** the compaction cell, SCHWABBF's pending set, and the push of `box/laptop` and the tag (integrator's).
