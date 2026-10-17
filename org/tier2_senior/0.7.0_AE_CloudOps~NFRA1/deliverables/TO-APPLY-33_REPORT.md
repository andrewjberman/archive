# TO-APPLY-33 REPORT -- estate report runner blob prefetch: upload and QA run

Seat `0.7.0_AE_CloudOps~NFRA1`, order `NFRA_CTLPLN.TO-APPLY-33` (issuer `2.0.0_SA_COO~C`, cell `CT-cj-1`). Result: **all three criteria met.**
Ledger (CLOSED): `org/critical_paths/change_management/20261017T1455Z_estate-report-runner-blob-prefetch_deploy_completion.md`.

| criterion | result | source |
|---|---|---|
| CTcj1-AC1 | MET. Object sha256 `62b0d74c17fc4eaf24dcfbdce126964cf126d1e618ccd8538acb18bef453100d` == `git show 7a33c62148:infra/aws/ec2/estate-report-runner/estate_report_runner.py`; one-byte mutant UNEQUAL | `s3://opal-estate-report/code/estate_report_runner.py`, VersionId `LwDXDuLu9PZ.WHwKa.XV3Q4MQne9MR8i`, put 14:53:25Z |
| CTcj1-AC2 | MET. `STAGE compile_resources kind=deterministic status=ok 4374 paths, 98 chain-resolved`; no Traceback, CalledProcessError or WARN | `s3://opal-estate-report/logs/2026-10-17T151354Z-i-0584e17d283fa7ef4.log` (run start 14:54:58Z; the object name carries the END time 15:13:54Z) |
| CTcj1-AC3 | MET. `status` = PENDING (not FAILED), written 15:13:55Z for date 2026-10-17 | `s3://opal-estate-report/manifest/2026-10-17.json`, VersionId `a5P0snAQuMq.k8iHMbZ51I5e3xMsQSYs` |

## What was done
- Window: 14:51Z-15:14Z, outside 12:50Z-13:30Z; instance (found by Name tag, id `i-0584e17d283fa7ef4`) read `stopped` before the upload and before the start.
- Rollback recorded before the act: previous VersionId `HIrQD8nolfYS_30vrMXBXCZJ0_EnqqPz` (file at `bfbdc20d40`, sha256 `5e693559...a227d`, verified equal). Not used.
- QA run: ONE ad-hoc start, `lambda invoke estate-report-orchestrator` with `{"mode":"daily-run","trigger":"manual"}` (manifest `run_bundle.trigger` reads `manual`). No second run.
- The QA run replaced the FAILED manifest of 2026-10-17 as the order intended; the FAILED manifest (VersionId `iyjzyB3MYWxH2mipyyl5K9MEJrFtr0yP`) and failed log are in this folder.
- A first invoke attempt with `--cli-binary-format` was rejected by CLI v1 before any call (instance stayed `stopped`); the second attempt is the one run.

## Not claimed
- This is an ad-hoc run, not production evidence. The CVO re-grades the next SCHEDULED day, 2026-10-18 13:00Z. Nothing is armed against it.
- 2 of 4 strata are unmeasured in the same run: C `INSTRUMENT_FAILED` (denominator text 'git ls-tree/log FAILED', no stderr kept) and A (0 of 2 devices reporting, outset seam objects UNREAD). Whether C is the blobless-clone family was not examined. Row `NFRA_CTLPLN-S9138` (`32e21be4ae`), owner `2.0.0_SA_COO~C`.
- Run duration was about 19 min (Kimi calls 1028 s), against the "about ten minutes" in the order's cost line.

## Slips (process)
- The code diff was read after the upload, not before as step 4's context asks. It matches the description (+55/-6, helper `checkout_paths` / `prefetch_blobs`).
- The ledger header and file name carry 14:55Z, typed before the clock; the upload was 14:53:25Z. Corrected in the ledger body.
- A first surprise-row id (`...-A33-S1`) was refused by the gate (unregistered coordinate); renumbered to the bare laptop id `S9138` before commit.

## For the issuer
- Proof instance: `deliverables/NFRA_CTLPLN.TO-APPLY-33.estate-report-runner-blob-prefetch-upload-and-qa-run.proof_of_spec.json`, `proof-of-spec-check` VALID (rc=0), bound to this order.
- The order names no never-widen pair; the schema requires the field, so both halves read "NONE" with the reason. The QA run wrote the day's report keys `daily/2026/10/17/estate-report-2026-10-17.md` and `.json` (15:13:55Z). Whether the act needed a pair is the issuer's call.

## Related
`org/critical_paths/.open_deploys/estate-report-runner-function-map-20261017.json` (TO-APPLY-32) still has its DISARM leg open; not touched, the issuer decides it.
